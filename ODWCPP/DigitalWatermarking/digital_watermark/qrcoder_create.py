import qrcode
import cv2
import time


class QrcodeMaker:
    def __init__(self):
        self.qr = qrcode.QRCode(
            version=10,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=2,
            border=1
        )

    def qrcode_init(self, msg, filename):
        qr_maker = self.qr
        qr_maker.add_data(msg)
        qr_maker.make(fit=True)
        img = qr_maker.make_image(fill_color='green', back_color='white')
        img.save(filename)


if __name__ == '__main__':
    qr = QrcodeMaker()
    msg = '@SP-Official' + '--' + time.strftime('%Y-%m-%d', time.localtime())
    qr.qrcode_init(msg, "./watermark/qr_img_04.png")
