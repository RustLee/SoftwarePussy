# -*- coding: utf-8 -*-
# run origin.py to generate the embedded image
import sys
sys.path.append('../')
from digital_watermark import attck_check
from digital_watermark import WaterMark

# 一次纵向裁剪打击
attck_check.cut_att_height('../output/encoded_file.png', '../output/ver_atk.png', ratio=0.65)
attck_check.anti_cut_att('../output/ver_atk.png', '../output/ver_atk_fill.png', origin_shape=(1200, 1920))

# %%纵向裁剪打击.png
bwm1 = WaterMark(password_wm=1, password_img=1)
bwm1.extract(filename="../output/ver_atk_fill.png", wm_shape=(117, 117), out_wm_name="../output/ver_atk_wm.png")
