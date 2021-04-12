from PIL import Image, ImageDraw, ImageFont
import time


class WaterMark:
    def __init__(self):
        self.font = ImageFont.truetype('../font/TallTiny/TallTiny-Bold.otf', 80, index=0)

    def add_text_to_image(self, image, text):
        rgba_image = image.convert('RGBA')
        text_overlay = Image.new('RGBA', rgba_image.size, (40, 175, 234, 0))
        image_draw = ImageDraw.Draw(text_overlay)
        text_size_x, text_size_y = image_draw.textsize(text, font=self.font)
        # 设置文本文字位置
        # text_xy = (rgba_image.size[0] - text_size_x, rgba_image.size[1] - text_size_y)  #底部
        text_xy = ((rgba_image.size[0] - text_size_x) / 2, (rgba_image.size[1] - text_size_y) / 2)  # 中间
        # size[0]是长，size[1]是宽

        # 设置文本颜色和透明度
        image_draw.text(text_xy, text, font=self.font, fill=(76, 234, 124, 180))
        image_with_text = Image.alpha_composite(rgba_image, text_overlay)
        return image_with_text

    def add_watermark_to_image(self, image, watermark):
        rgba_image = image.convert('RGBA')
        rgba_watermark = watermark.convert('RGBA')

        image_x, image_y = rgba_image.size
        watermark_x, watermark_y = rgba_watermark.size

        # 缩放水印图片
        scale = 10
        watermark_scale = max(image_x / (scale * watermark_x), image_y / (scale * watermark_y))
        new_size = (int(watermark_x * watermark_scale), int(watermark_y * watermark_scale))
        rgba_watermark = rgba_watermark.resize(new_size, resample=Image.ANTIALIAS)
        # 透明度
        rgba_watermark_mask = rgba_watermark.convert("L").point(lambda x: min(x, 180))
        rgba_watermark.putalpha(rgba_watermark_mask)

        watermark_x, watermark_y = rgba_watermark.size
        # 水印位置
        # rgba_image.paste(rgba_watermark, (image_x - watermark_x, image_y - watermark_y), rgba_watermark_mask) #右下角
        rgba_image.paste(rgba_watermark, (image_x - watermark_x, 0), rgba_watermark_mask)  # 右上角

        return rgba_image


if __name__ == '__main__':
    wm = WaterMark()
    pic = Image.open('../pic/ori_img_3.png')
    watermark = Image.open('../pic/S.png')
    # msg = '@SP-Official' + '--' + time.strftime('%Y-%m-%d', time.localtime())
    pic_processed = wm.add_watermark_to_image(pic, watermark)
    pic_processed.save('../output/wm_img_3.png')
