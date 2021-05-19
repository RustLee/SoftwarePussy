import sys
import os
import zipfile
sys.path.append('../')
import time
from django.db.models import FileField
from django.forms import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from .models import UserAction, digitalwork_path, output_path
from DigitalWatermarking.digital_watermark.digital_watermark import WaterMark
from DigitalWatermarking.digital_watermark.video2image import VideoFrame
from DigitalWatermarking.digital_watermark.qrcoder_create import QrcodeMaker

from django.shortcuts import redirect
from django.urls import reverse


def encode_handeler(action_id):
    action = UserAction.objects.get(id=action_id)
    if not action:
        raise KeyError('can not find action {}'.format(action_id))
    upload_file = action.upload_filepath
    username = action.user.name
    ftype = action.upload_ftype
    fformat = action.upload_fformat

    output_filename =  time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    output_file_path = os.path.join(output_path, username, 'encoding' ,output_filename)
    os.makedirs(output_file_path)

    wm_path = os.path.join(output_file_path, 'watermark.png')
    embed_path = os.path.join(output_file_path, 'encoded_file.' + fformat)

    wm_str = action.upload_watermark_string
    qr = QrcodeMaker()
    msg = '@SP-Official' + '--' +  wm_str + '--' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    qr.qrcode_init(msg, wm_path)
    try:
        if ftype == 'image':
            bwm1 = WaterMark(password_wm=1, password_img=1)
            bwm1.read_img(upload_file)
            # 读取水印
            bwm1.read_wm(wm_path)
            # 打上盲水印
            bwm1.embed(embed_path)
        
        elif ftype == 'video':
            vf = VideoFrame(upload_file)
            tmp_path = vf.video2image_encode(wm_path)
            vf.image2video(embed_path)
            del_file(tmp_path)


        
        del_file(digitalwork_path)
        #把整个文件夹内的文件打包
        zipName = output_filename + '.zip'
        zipFilePath = os.path.join(output_file_path, zipName)


        pre_path = os.getcwd()
        os.chdir(output_file_path)
        f = zipfile.ZipFile(zipName, 'w', zipfile.ZIP_DEFLATED )
        os.chdir(pre_path)

        pre_path = os.getcwd()
        os.chdir(os.path.join(output_path, username, 'encoding'))

        for dirpath, dirnames, filenames in os.walk( output_filename ):
            for filename in filenames:
                if filename != zipName:
                    f.write(os.path.join(dirpath,filename))
        f.close()
        os.chdir(pre_path)


        return zipFilePath
    
    except AssertionError:
        print("溢出！")
        return False


def decode_handeler(action_id):
    action = UserAction.objects.get(id=action_id)
    ftype = action.upload_ftype
    if not action:
        raise KeyError('can not find action {}'.format(action_id))
    embedded_file = action.upload_filepath
    username = action.user.name
    output_filename =  time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    output_file_path = os.path.join(output_path, username, 'decoding', output_filename)
    os.makedirs(output_file_path)
    wm_path = os.path.join(output_file_path, 'watermark.png')

    if ftype == 'image':
        bwm1 = WaterMark(password_wm=1, password_img=1)
        bwm1.extract(filename=embedded_file, wm_shape=(118, 118), out_wm_name=wm_path)
    elif ftype == 'video':
        vf = VideoFrame(embedded_file)
        vf.video2image_decode(wm_path)
        


    return wm_path

    # #把整个文件夹内的文件打包
    # zipName = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())+ '.zip'
    # zipFilePath = os.path.join(output_file_path, zipName)
    # f = zipfile.ZipFile( zipFilePath, 'w', zipfile.ZIP_DEFLATED )
    # #print(os.getcwd())
    # pre_path = os.getcwd()
    # os.chdir(os.path.join(output_path, username))
    # #print(os.getcwd())
    # for dirpath, dirnames, filenames in os.walk( output_filename ):
    #     for filename in filenames:
    #         if filename != zipName:
    #             f.write(os.path.join(dirpath,filename))
    # f.close()
    # os.chdir(pre_path)
    # return zipFilePath


def getFileFormat(filename):
    """
    获取文件名的后缀
    """
    tokens = filename.split('.')
    return tokens[-1]

def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)

