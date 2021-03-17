import qrcode
import cv2
import time


class QrcodeMaker:
    def __init__(self):
        self.qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4
        )

    def qrcode_init(self, msg, filename):
        qr_maker = self.qr
        qr_maker.add_data(msg)
        qr_maker.make(fit=True)
        img = qr_maker.make_image(fill_color='black', back_color='white')
        img.save(filename)


if __name__ == '__main__':
    qr = QrcodeMaker()
    msg = '@SP-Official' + '--' + time.strftime('%Y-%m-%d', time.localtime())
    qr.qrcode_init(msg, "./qr_img_01.png")
