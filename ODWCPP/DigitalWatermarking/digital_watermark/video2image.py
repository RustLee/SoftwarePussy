import os
import cv2
from PIL import Image
from .digital_watermark import WaterMark
import os

cur_path = os.getcwd()
tmp_path = os.path.join(cur_path, 'tmp/')

class VideoFrame:

    def __init__(self, filepath):
        self.cap = cv2.VideoCapture(filepath)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.size = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self.bwm = WaterMark(password_wm=1, password_img=1)

        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)

    def video2image_encode(self, wm_path):
        succeed = self.cap.isOpened()
        frame_count = 0
        while succeed:
            frame_count += 1
            succeed, frame = self.cap.read()
            if frame is not None:
                if frame_count % 100 == 0:
                    self.bwm.read_img_frame(frame)
                    self.bwm.read_wm(wm_path)
                    self.bwm.embed(tmp_path + '%d.jpg' % frame_count)
                else:
                    cv2.imwrite(tmp_path + '%d.jpg' % frame_count, frame)
        self.cap.release()
        print('processed {} images'.format(frame_count))
        return tmp_path

    def video2image_decode(self, wm_path):
        succeed = self.cap.isOpened()
        frame_count = 0
        while succeed:
            frame_count += 1
            succeed, frame = self.cap.read()
            if frame is not None:
                if frame_count % 100 == 0:
                    self.bwm.read_img_frame(frame)
                    cv2.imwrite(tmp_path + '%d.jpg' % frame_count, frame)
                    self.bwm.extract(tmp_path + '%d.jpg' % frame_count, wm_shape=(118, 118), out_wm_name=wm_path )
                    break

        self.cap.release()
        print('processed {} images'.format(frame_count))
        return tmp_path

    def image2video(self, filepath):
        forrcc = cv2.VideoWriter_fourcc(*'mp4v')
        images = os.listdir(tmp_path)
        im = Image.open(tmp_path + images[0])
        vw = cv2.VideoWriter(filepath, forrcc, self.fps, im.size)

        pre_path = os.getcwd()
        os.chdir(tmp_path)
        for image in range(len(images)):
            image_file = str(image + 1) + '.jpg'
            try:
                frame = cv2.imread(image_file)
                vw.write(frame)
            except Exception as exc:
                print(image_file, exc)
        vw.release()
        os.chdir(pre_path)
        print(filepath, 'Synthetic success!')




if __name__ == '__main__':
    filepath = '../video/test_video_2.mp4'
    vf = VideoFrame(filepath)
    # vf.video2image_encode()
    # vf.image2video('../video/test_video_2.mp4')
    vf.video2image_decode()
