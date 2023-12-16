import os
import shutil

from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from django.views import generic

from file_server_app import utils
from fserver import settings


# Create your views here.
class ContentList(generic.ListView):
    local_ip = utils.get_ip()
    template_name = 'content.html'

    def get(self, request, *args, **kwargs):
        path = kwargs.get('path', '')
        if os.path.isfile(path):
            return utils.build_file_response(path)
        return super().get(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        path = kwargs.get('path', '')
        for file in request.FILES.getlist('files'):
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            source: str = str(os.path.join(settings.MEDIA_URL, filename))
            destination: str = str(os.path.join(path, filename))
            try:
                shutil.move(source, destination)
            except Exception as e:
                return {
                    'error': {
                        'path': f'{source} -> {destination}',
                        'details': e
                    }
                }
        return redirect('./')

    def get_queryset(self):
        path = self.kwargs.get('path', '')
        if os.path.isdir(path):
            qs = utils.get_directories_files_in_path(path)
        else:
            qs = {
                'drives': utils.get_all_drive_letters(),
            }
        qs |= {'local_ip': self.local_ip}
        return qs
