# coding=utf-8
# run origin.py to generate the embedded image

from digital_watermark import attck_check
from digital_watermark import WaterMark

# %%
# 攻击
attck_check.shelter_att('../output/embedded_4.png', '../output/hide.png', ratio=0.1, n=10)

# %% 提取水印
bwm1 = WaterMark(password_wm=1, password_img=1)
bwm1.extract(filename='../output/hide.png', wm_shape=(100, 300), out_wm_name='../output/hide_wm.png')

