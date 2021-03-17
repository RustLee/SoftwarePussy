#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# embed string
import numpy as np
from digital_watermark import WaterMark
import time

bwm1 = WaterMark(password_img=1, password_wm=1)
bwm1.read_img('pic/ori_img_1.jpg')
wm = '@SP-Official' + '--' + time.strftime('%Y-%m-%d', time.localtime())
bwm1.read_wm(wm, mode='str')
bwm1.embed('output/embedded.png')
len_wm = len(bwm1.wm_bit)
print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))

# %% 解水印
bwm1 = WaterMark(password_img=1, password_wm=1)
wm_extract = bwm1.extract('output/embedded.png', wm_shape=len_wm, mode='str')
print(wm_extract)

assert wm == wm_extract, '提取水印和原水印不一致'
