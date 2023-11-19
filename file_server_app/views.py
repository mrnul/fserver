import os
from http import HTTPStatus

from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest
from django.shortcuts import render

from file_server_app import utils


# Create your views here.
def drives(request: HttpRequest):
    return render(request, 'drives.html', context={'letters': utils.get_all_drive_letters()})


def content(request: HttpRequest, path: str):
    if request.method == 'POST' and 'myfile' in request.FILES and request.FILES['myfile']:
        my_file = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(os.path.join(request.path, my_file.name), my_file)

    if os.path.isdir(path):
        return utils.build_dir_response(request, path)
    elif os.path.isfile(path):
        return utils.build_file_response(request, path)
    return utils.build_error_response(request, path, 'Content not found', HTTPStatus.NOT_FOUND)
