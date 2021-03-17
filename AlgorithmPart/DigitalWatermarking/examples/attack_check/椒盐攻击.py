# -*- coding: utf-8 -*-
# run origin.py to generate the embedded image

from digital_watermark import attck_check
from digital_watermark import WaterMark

# %%椒盐攻击
attck_check.salt_pepper_att('output/embedded.png', 'output/椒盐攻击.png', ratio=0.05)
# ratio是椒盐概率

# %%纵向裁剪打击.png
bwm1 = WaterMark(password_wm=1, password_img=1)
bwm1.extract(filename='output/椒盐攻击.png', wm_shape=(128, 128), out_wm_name='output/椒盐攻击_提取水印.png')

