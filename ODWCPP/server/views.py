import sys
sys.path.append('../')
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.utils import timezone
# Create your views here.
from .models import UserAction, supported_formats, digitalwork_path
from .utils import getFileFormat, encode_handeler, decode_handeler
from login.models import User




class UploadFileForm(forms.Form):
    filename = forms.FileField()
    wm_str = forms.CharField(required=False)


# def index(request):
#     return render(request, 'server/index.html')
    # return HttpResponse('this is index page')
# def index(request):
#     if not request.session.get('is_login', None):
#         return redirect('/login/')
#     return render(request, 'server/index.html')

def encodeindex(request):
    #return HttpResponse('this is encode index page')
    if not request.session.get('is_login', None):
        return redirect('/login/')
    unsupport_type = False 
    messages = {
        'unsupported_type': '暂不支持该类文件类型',
        'no_str': '请输入文本',
        'no_img': '请上传作为水印的图片',
    }
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # 获取表单数据
            f = form.cleaned_data['filename']
            wm_str = form.cleaned_data['wm_str']
            if not wm_str:
                return render(request, 'server/encode_index.html', 
                    {'form': form, 
                    'no_str': True,
                    'message': messages['no_str']
                    })

            # 获取数据库数据
            action = UserAction()
            action.time = timezone.now()
            action.upload_file = f
            action.upload_filepath = os.path.join(digitalwork_path, str(f))
            action.optype = 'encode'
            action.upload_fstatus = 'raw'
            action.upload_watermark_string = wm_str

            unsupport_type = True
            file_format = getFileFormat(str(f))
            for file_type in supported_formats.keys():
                if file_format in supported_formats[file_type]:
                    action.upload_ftype = file_type
                    action.upload_fformat = file_format
                    unsupport_type = False
                    break
            if unsupport_type:
                return render(request, 'server/encode_index.html', {'form': form, 'unsupport_type':unsupport_type, 'message':messages['unsupported_type']})
            else:
                cur_user = User.objects.get(name= request.session['user_name'])
                action.user = cur_user
                action.save()
                action_id = action.id
                request.session['action_id'] = action_id
                return HttpResponseRedirect(reverse('server:encoderesult_index'))
    else:
        form = UploadFileForm()
    return render(request, 'server/encode_index.html', {'form': form, 'unsupport_type':unsupport_type, 'message':messages['unsupported_type'] })

def encoderesult_index(request):
    return render(request, 'server/encode_result.html',{})
    #return HttpResponse('result')

isdone = 0
path = ''
def start_processing(request):
    global isdone
    global path
    path = ''
    isdone = 0
    action_id = request.session.get('action_id')
    action = UserAction.objects.get(id=action_id)
    if action.optype == 'encode':
        #path = 'data/download/test.txt'
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~start encoding")
        path = encode_handeler(action_id)
        if not path:
            print("error!")
            isdone = -1
        else:
            isdone = 1
    else:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~start decoding")
        path = decode_handeler(action_id)
        isdone = 1


def show_progress(request):
    global isdone
    print("--------------isdone:{}".format(isdone))
    if isdone == 1:
        return HttpResponse('1')
    elif isdone == -1:
        return HttpResponse('-1')
    else:
        return HttpResponse('0')

def file_download(request):
    global path
    zipfile = open(path, 'rb')
    response = HttpResponse(zipfile)
    filename = path.split("\\")[-1]
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = "attachment;filename=" + filename
    path = ''
    return response

def decodeindex(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    unsupport_type = False 
    messages = {
        'unsupported_type': '暂不支持该类文件类型',
        'no_img': '请上传图片',
    }
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # 获取表单数据
            f = form.cleaned_data['filename']
            # 获取数据库数据
            action = UserAction()
            action.time = timezone.now()
            action.upload_file = f
            action.upload_filepath = os.path.join(digitalwork_path, str(f))
            action.optype = 'decode'
            action.upload_fstatus = 'encoded'

            unsupport_type = True
            file_format = getFileFormat(str(f))
            for file_type in supported_formats.keys():
                if file_format in supported_formats[file_type]:
                    action.upload_ftype = file_type
                    action.upload_fformat = file_format
                    unsupport_type = False
                    break
            if unsupport_type:
                return render(request, 'server/decode_index.html', {'form': form, 'unsupport_type':unsupport_type, 'message':messages['unsupported_type']})
            else:
                cur_user = User.objects.get(name= request.session['user_name'])
                action.user = cur_user
                action.save()
                action_id = action.id
                request.session['action_id'] = action_id
                return HttpResponseRedirect(reverse('server:decoderesult_index'))
    else:
        form = UploadFileForm()
    return render(request, 'server/decode_index.html', {'form': form, 'unsupport_type':unsupport_type, 'message':messages['unsupported_type'] })

def decoderesult_index(request):
    return render(request, 'server/decode_result.html',{})

def teamindex(request):
    return render(request, 'server/team.html')

def errorindex(request):
    return render(request, 'server/error.html')

# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             # 获取表单数据
#             filename = form.cleaned_data['filename']
#             # 获取数据库数据
#             upfile = UploadFile()
#             upfile.filename = filename
#             upfile.save()
#             return HttpResponse('file upload ok !')
#     else:
#         form = UploadFileForm()
#     return render('server/encode_index.html', {'form': form})

