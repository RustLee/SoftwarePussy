# -*- coding: utf-8 -*-
# run origin.py to generate the embedded image
import sys
sys.path.append('../')
from digital_watermark import attck_check
from digital_watermark import WaterMark

# %%椒盐攻击
attck_check.salt_pepper_att('../output/encoded_file.png', '../output/SP_atk.png', ratio=0.05)
# ratio是椒盐概率

# %%纵向裁剪打击.png
bwm1 = WaterMark(password_wm=1, password_img=1)
bwm1.extract(filename='../output/SP_atk.png', wm_shape=(117, 117), out_wm_name='../output/SP_atk_wm.png')

