import mimetypes
import os

from django.http import StreamingHttpResponse, HttpResponse

from fserver import settings


def get_all_drive_letters() -> list[str]:
    drives = [chr(letter) for letter in range(ord('A'), ord('Z'))
              if os.path.exists(chr(letter) + ':/')]
    return drives


def get_directories_files_in_path(path: str) -> dict:
    try:
        directories = []
        files = []
        for item in os.listdir(path):
            path_to_check = os.path.join(path, item)
            if os.path.isfile(path_to_check):
                files.append({'name': item, 'size': os.path.getsize(path_to_check) / (1024.0 ** 2)})
            elif os.path.isdir(path_to_check):
                directories.append(item)
        return {
            'directories': directories,
            'files': files,
            'dots_parts': build_dots_parts(path),
            'drives': get_all_drive_letters()
        }
    except OSError as e:
        return {
            'error': {
                'path': path,
                'details': str(e)
            }
        }


def build_dots_parts(path: str):
    dots_parts = []
    parts = os.path.normpath(path).split(os.path.sep)
    dots = ''
    for part in reversed(parts):
        if len(part) == 0:  # C:// gets split into ['C:', '']
            continue
        dots_parts.append({'dots': dots, 'part': part})
        dots += '../'
    return list(reversed(dots_parts))


def browser_should_handle_it(content_type):
    if content_type is None:
        return False
    for ct in settings.BROWSER_SHOULD_HANDLE_CONTENT_TYPE:
        if ct in content_type:
            return True
    return False


def build_file_response(path: str):
    try:
        content_type = mimetypes.MimeTypes().guess_type(path, False)[0]
        response = StreamingHttpResponse(open(path, 'rb'), content_type=content_type)
        # if not browser_should_handle_it(content_type):
        #     response['Content-Type'] = f'{content_type};'
        #     response['Content-Disposition'] = f'attachment; filename="{os.path.basename(path)}"'
        return response
    except OSError as e:
        return HttpResponse(f'Error while trying to access {path}: {e}')
