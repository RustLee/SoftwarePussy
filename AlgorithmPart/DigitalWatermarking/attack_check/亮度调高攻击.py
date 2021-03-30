# -*- coding: utf-8 -*-
# run origin.py to generate the embedded image

from digital_watermark import attck_check
from digital_watermark import WaterMark

# 亮度调高攻击
attck_check.bright_att('../output/embedded_4.png', '../output/high_light.png', ratio=1.1)

# %% 提取水印
bwm1 = WaterMark(password_wm=1, password_img=1)
bwm1.extract(filename='../output/high_light.png', wm_shape=(100, 300), out_wm_name='../output/high_light_wm.png')
