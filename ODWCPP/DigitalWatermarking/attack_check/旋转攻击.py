# -*- coding: utf-8 -*-
# run origin.py to generate the embedded image

from digital_watermark import attck_check
from digital_watermark import WaterMark

# 旋转攻击
attck_check.rot_att('../output/embedded_4.png', '../output/rotate.png', angle=45)
attck_check.rot_att('../output/rotate.png', '../output/rotate_ori.png', angle=-45)

# %%提取水印
bwm1 = WaterMark(password_wm=1, password_img=1)
bwm1.extract(filename='../output/rotate_ori.png', wm_shape=(100, 300), out_wm_name='../output/rotate_w.png')

