#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from digital_watermark import WaterMark

bwm1 = WaterMark(password_wm=1, password_img=1)
# 读取原图
bwm1.read_img('pic/ori_img_2.png')
# 读取水印
bwm1.read_wm('pic/watermark_3.png')
# 打上盲水印
bwm1.embed('output/embedded_4.png')

# %% 解水印


bwm1 = WaterMark(password_wm=1, password_img=1)
# 注意需要设定水印的长宽wm_shape
bwm1.extract(filename='output/embedded_4.png', wm_shape=(100, 300), out_wm_name='output/wm_extracted_4.png', )
