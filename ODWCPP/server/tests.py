from django.test import TestCase
import os
# Create your tests here.

def get_id():
    f = open('id.txt', 'r')
    id = int(f.read())
    new_id = id + 1
    f.close()
    f = open('id.txt', 'w')
    f.truncate()
    f.write(str(new_id))
    f.close()
    return id

if __name__ == '__main__':
    import zipfile
    #把整个文件夹内的文件打包
    zipName = r'E:\Project\learnDjango\ODWCPP\data\download\haolin\encoding\2021-04-12_21-14-30\2021-04-12_21-14-30.zip'
 
    f = zipfile.ZipFile( zipName, 'w', zipfile.ZIP_DEFLATED )
    for dirpath, dirnames, filenames in os.walk( "E:\\Project\\learnDjango\\ODWCPP\\data\\download\\haolin\\encoding\\2021-04-12_21-14-30" ):
        for filename in filenames:
            f.write(os.path.join(dirpath,filename))
    f.close()
