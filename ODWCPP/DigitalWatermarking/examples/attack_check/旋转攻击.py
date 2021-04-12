# -*- coding: utf-8 -*-
# run origin.py to generate the embedded image

from digital_watermark import attck_check
from digital_watermark import WaterMark

# 旋转攻击
attck_check.rot_att('output/embedded.png', 'output/旋转攻击.png', angle=45)
attck_check.rot_att('output/旋转攻击.png', 'output/旋转攻击_还原.png', angle=-45)

# %%提取水印
bwm1 = WaterMark(password_wm=1, password_img=1)
bwm1.extract(filename='output/旋转攻击_还原.png', wm_shape=(128, 128), out_wm_name='output/旋转攻击_提取水印.png')

