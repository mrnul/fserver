import mimetypes
import os
import socket
from http import HTTPStatus

from django.http import HttpRequest, StreamingHttpResponse
from django.shortcuts import render

from fserver import settings


def get_all_drive_letters() -> list[str]:
    drives = [chr(letter) for letter in range(ord('A'), ord('Z'))
              if os.path.exists(chr(letter) + ':/')]
    return drives


def get_directories_files_in_path(path: str):
    directories = []
    files = []
    for item in os.listdir(path):
        path_to_check = os.path.join(path, item)
        if os.path.isfile(path_to_check):
            files.append({'name': item, 'size': os.path.getsize(path_to_check) / (1024.0 ** 2)})
        elif os.path.isdir(path_to_check):
            directories.append(item)
    return directories, files


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]
    except (Exception,):
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


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


def build_dir_response(request: HttpRequest, path: str):
    try:
        dirs, files = get_directories_files_in_path(path)
        return render(request, 'content.html',
                      context={
                          'directories': dirs,
                          'files': files,
                          'dots_parts': build_dots_parts(path)
                      })
    except OSError as e:
        return build_error_response(request, path, str(e), HTTPStatus.INTERNAL_SERVER_ERROR)


def browser_should_handle_it(content_type):
    if content_type is None:
        return False
    for ct in settings.BROWSER_SHOULD_HANDLE_CONTENT_TYPE:
        if ct in content_type:
            return True
    return False


def build_file_response(request: HttpRequest, path: str):
    try:
        content_type = mimetypes.MimeTypes().guess_type(path, False)[0]
        response = StreamingHttpResponse(open(path, 'rb'), content_type=content_type)
        # if not browser_should_handle_it(content_type):
        #     response['Content-Type'] = f'{content_type};'
        #     response['Content-Disposition'] = f'attachment; filename="{os.path.basename(path)}"'
        return response
    except OSError as e:
        return build_error_response(request, path, str(e), HTTPStatus.INTERNAL_SERVER_ERROR)


def build_error_response(request: HttpRequest, path: str, details: str, error_code: int):
    return render(request, 'error.html',
                  context={
                      'error': {
                          'path': path,
                          'details': details
                      }
                  }, status=error_code)
