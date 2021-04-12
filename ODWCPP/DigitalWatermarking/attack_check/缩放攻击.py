# -*- coding: utf-8 -*-
# run origin.py to generate the embedded image

from digital_watermark import attck_check
from digital_watermark import WaterMark

# 缩放攻击
attck_check.resize_att('output/embedded.png', 'output/缩放攻击.png', out_shape=(800, 600))
attck_check.resize_att('output/缩放攻击.png', 'output/缩放攻击_还原.png', out_shape=(1920, 1200))
# out_shape 是分辨率，需要颠倒一下
# %%提取水印
bwm1 = WaterMark(password_wm=1, password_img=1)
bwm1.extract(filename="output/缩放攻击_还原.png", wm_shape=(128, 128), out_wm_name="output/缩放攻击_提取水印.png")
