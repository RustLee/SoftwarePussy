import sys
sys.path.append("..") # Adds higher directory to python modules path.
import os
from django.db import models
from login.models import *
import datetime
BASE_DIR = os.getcwd()
#digitalwork_path = os.path.join(BASE_DIR, 'data','upload')
#output_path = os.path.join(BASE_DIR, 'data', 'download')

digitalwork_path = ".\\data\\upload"
output_path = ".\\data\\download"


# Create your models here.
# class User(models.Model):
#     username = models.CharField(max_length=30)
#     password = models.CharField(max_length=20)

# class File(models.Model):
#     Ftypes = (
#         ('raw', '无水印'),
#         ('encoded', '有水印')
#     )
#     f = models.FileField(upload_to='./upload')
#     filename = models.CharField(max_length=100, default='f')
#     ftype = models.CharField(max_length=10, choices=Ftypes, default='raw')


supported_formats = {
    'image': ('png', 'jpg', 'jepg'),
    'audio': ('wav',),
    'video': ('mp4',)
}


from django.test import TestCase

# Create your tests here.

def get_id():
    f = open('id.txt', 'r')
    old_id = int(f.read())
    new_id = old_id + 1
    f.close()
    f = open('id.txt', 'w')
    f.truncate()
    f.write(str(new_id))
    f.close()
    return old_id


class UserAction(models.Model):
    Optpyes = (
        ('encode', '添加水印'),
        ('decode', '解析水印')
    )
    Fstatus = (
        ('raw', '无水印'),
        ('encoded', '有水印')
    )

    Ftypes = (
        ('image', '图片'),
        ('audio', '音频'),
        ('video', '视频')
    )

    

    formats = [ subname for name in supported_formats.values() for subname in name]
    Fformats = tuple([(f, f) for f in formats])


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField('date published')
    optype = models.CharField(max_length=10, choices=Optpyes, default='encode')

    #upload_path = models.CharField(max_length=100, default='./data/upload')
    upload_file = models.FileField(upload_to = digitalwork_path)
    upload_filepath = models.CharField(max_length=100, blank=True)

    upload_fstatus = models.CharField(max_length=10, choices=Fstatus, blank=True)
    upload_ftype = models.CharField(max_length=10, choices = Ftypes, blank=True)
    upload_fformat = models.CharField(max_length=10, choices=Fformats, blank=True )


    upload_watermark_string = models.CharField(max_length=100, default='default watermark')

class FeedBack(models.Model):
    Optpyes = (
        ('encode', '添加水印'),
        ('decode', '解析水印')
    )
    Ftypes = (
        ('raw', '无水印'),
        ('encoded', '有水印')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField('date published')
    optype = models.CharField(max_length=10, choices=Optpyes, default='encode')

    #download_path = models.CharField(max_length=100, default='./data/download')
    download_file = models.FileField(upload_to='./data/download')
    download_filename = models.CharField(max_length=100, default='f')
    download_ftype = models.CharField(max_length=10, choices=Ftypes, default='encoded')

