from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=1024)
    file = forms.FileField()