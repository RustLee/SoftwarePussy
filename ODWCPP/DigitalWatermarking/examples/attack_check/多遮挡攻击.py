# coding=utf-8
# run origin.py to generate the embedded image

from digital_watermark import attck_check
from digital_watermark import WaterMark

# %%
# 攻击
attck_check.shelter_att('output/embedded.png', 'output/多遮挡攻击.png', ratio=0.1, n=10)

# %%多遮挡攻击.png
bwm1 = WaterMark(password_wm=1, password_img=1)
bwm1.extract(filename='output/多遮挡攻击.png', wm_shape=(128, 128), out_wm_name='output/多遮挡攻击_提取水印.png')

