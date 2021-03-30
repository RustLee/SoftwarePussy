import os
import cv2
from PIL import Image
from digital_watermark import WaterMark


class VideoFrame:

    def __init__(self, filepath):
        self.cap = cv2.VideoCapture(filepath)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.size = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self.bwm = WaterMark(password_wm=1, password_img=1)

    def video2image_encode(self):
        succeed = self.cap.isOpened()
        frame_count = 0
        while succeed:
            frame_count += 1
            succeed, frame = self.cap.read()
            if frame is not None:
                if frame_count % 17 == 0:
                    self.bwm.read_img_frame(frame)
                    self.bwm.read_wm('./watermark/qr_img_04.png')
                    self.bwm.embed('../frame/%d.jpg' % frame_count)
                else:
                    cv2.imwrite('../frame/%d.jpg' % frame_count, frame)
        self.cap.release()
        print('processed {} images'.format(frame_count))

    def video2image_decode(self):
        succeed = self.cap.isOpened()
        frame_count = 0
        while succeed:
            frame_count += 1
            succeed, frame = self.cap.read()
            if frame is not None:
                if frame_count % 17 == 0:
                    self.bwm.read_img_frame(frame)
                    self.bwm.extract('../frame/%d.jpg' % frame_count, wm_shape=(155, 155),
                                     out_wm_name='../output/video_extracted_{}.jpg'.format(frame_count), )
        self.cap.release()
        print('processed {} images'.format(frame_count))

    def image2video(self, filepath):
        forrcc = cv2.VideoWriter_fourcc(*'mp4v')
        images = os.listdir('../frame')
        im = Image.open('../frame/' + images[0])
        vw = cv2.VideoWriter(filepath, forrcc, self.fps, im.size)

        os.chdir('../frame')
        for image in range(len(images)):
            image_file = str(image + 1) + '.jpg'
            try:
                frame = cv2.imread(image_file)
                vw.write(frame)
            except Exception as exc:
                print(image_file, exc)
        vw.release()
        print(filepath, 'Synthetic success!')


if __name__ == '__main__':
    filepath = '../video/test_video_2.mp4'
    vf = VideoFrame(filepath)
    # vf.video2image_encode()
    # vf.image2video('../video/test_video_2.mp4')
    vf.video2image_decode()
