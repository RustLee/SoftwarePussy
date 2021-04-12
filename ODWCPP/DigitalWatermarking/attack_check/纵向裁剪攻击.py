# -*- coding: utf-8 -*-
# run origin.py to generate the embedded image

from digital_watermark import attck_check
from digital_watermark import WaterMark

# 一次纵向裁剪打击
attck_check.cut_att_height('output/embedded.png', 'output/纵向裁剪攻击.png', ratio=0.5)
attck_check.anti_cut_att('output/纵向裁剪攻击.png', 'output/纵向裁剪攻击_填补.png', origin_shape=(1200, 1920))

# %%纵向裁剪打击.png
bwm1 = WaterMark(password_wm=1, password_img=1)
bwm1.extract(filename="output/纵向裁剪攻击_填补.png", wm_shape=(128, 128), out_wm_name="output/纵向裁剪攻击_提取水印.png")
