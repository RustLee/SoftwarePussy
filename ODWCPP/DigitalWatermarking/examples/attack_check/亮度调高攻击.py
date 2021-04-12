# -*- coding: utf-8 -*-
# run origin.py to generate the embedded image

from digital_watermark import attck_check
from digital_watermark import WaterMark

# 亮度调高攻击
attck_check.bright_att('output/embedded.png', 'output/亮度调高攻击.png', ratio=1.1)

# %% 提取水印
bwm1 = WaterMark(password_wm=1, password_img=1)
bwm1.extract(filename='output/亮度调高攻击.png', wm_shape=(128, 128), out_wm_name='output/亮度调高攻击_提取水印.png')
