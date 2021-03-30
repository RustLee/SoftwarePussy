#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 除了嵌入图片，也可以嵌入比特类数据
import numpy as np
from digital_watermark import WaterMark

bwm1 = WaterMark(password_img=1, password_wm=1)

# 读取原图
bwm1.read_img('pic/ori_img.jpg')

# 读取水印
wm = [True, False, True, True, True, False, True, True, False, True]
bwm1.read_wm(wm, mode='bit')

# 打上盲水印
bwm1.embed('output/watermark_img.png')

# %% 解水印

# 注意设定水印的长宽wm_shape
bwm1 = WaterMark(password_img=1, password_wm=1)
wm_extract = bwm1.extract('output/watermark_img.png', wm_shape=10, mode='bit')
print(wm_extract)

assert np.all(wm == (wm_extract > 0.5)), '提取水印和原水印不一致'
