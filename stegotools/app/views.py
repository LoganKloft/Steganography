import json

from django.http import JsonResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from .utils import exf
from .utils import lsb

# Create your views here.
def index(request):
    if request.method == 'POST' and request.FILES['upload']:
        global image
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        return JsonResponse({'name':upload.name})
    return render(request, 'app/index.html')

def log(request):
    # convert data to python dictionary
    image_json = request.POST.get('image')
    image_json = json.loads(image_json)

    # get url of image
    fss = FileSystemStorage()
    file = fss.url(image_json['name'])
    print(file)

    # retrieve image exif data
    exif = exf.exf(file)
    ext = file.split('.')[-1]
    data = None
    if ext.lower() == 'png':
        data = exif.get(True)
    else:
        data = exif.get(False)

    # retrieve lsb encoding of message
    message = 'cannot encode jpg'
    if ext.lower() == 'png':
        lsb_encoder = lsb.lsb()
        message = lsb_encoder.decode(file)
    print(message)

    return JsonResponse(data)

def encode(request):
    # separate data
    image_name = None
    message = ''
    exif_data = {}

    for key, value in request.POST.items():
        if key == 'message':
            message = value
        elif key == 'image-src':
            print(value)
            l = value.split('/')
            image_name = '/' + l[-2] + '/' + l[-1]
        else:
            exif_data[key] = value
    
    print(exif_data)
    print(image_name)
    print(message)

    # encode exif data
    # exif = exf.exf(image_name)

    # encode message if PNG
    ext = image_name.split('.')[-1]
    if (ext.lower() == 'png'):
        lsb_encoder = lsb.lsb()
        lsb_encoder.encode(image_name, message)

    # send image url back so can be downloaded
    return JsonResponse({})