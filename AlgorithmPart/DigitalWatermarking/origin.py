#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from digital_watermark import WaterMark

bwm1 = WaterMark(password_wm=1, password_img=1)
# 读取原图
bwm1.read_img('pic/ori_img_2.png')
# 读取水印
bwm1.read_wm(wm_content='digital_watermark/watermark/qr_img_04.png')
# 打上盲水印
bwm1.embed('output/embedded_7.png')

# %% 解水印


bwm1 = WaterMark(password_wm=1, password_img=1)
# 注意需要设定水印的长宽wm_shape
bwm1.extract(filename='output/embedded_7.png', wm_shape=(155, 155), out_wm_name='output/wm_extracted_6.png', )
