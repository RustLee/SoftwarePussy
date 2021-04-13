import librosa as lib
import numpy as np
import time
import copy
import soundfile
import qrcode
from PIL import Image,ImageDraw,ImageFont
from pydub import AudioSegment
import array
from pyzbar import pyzbar
import zxing


class audio_watermark():

    def __init__(self,length = 2, L = 10, a = 1.1, N = 120,div = 1):
        self.length = length
        self.L = L
        self.a = a
        self.N = N
        self.div = div

    def db(self, num, length = 8):
        bList = []
        for i in range(length):
            bList.append(num % 2)
            num //= 2
        bList.reverse()
        return bList

    def encode(self, code):
        W = []
        for line in code:
            for bit in line:
                #print(bit)
                W.append(1 if bit else 0)
        return W

    def DCT(self, f):
        N = len(f)
        C = np.zeros(N)
        a = [np.sqrt(1/N)] + [np.sqrt(2/N)]*(N-1)
        t = time.time()
        k = np.pi/(2*N)
        for i in range(N):
            sum = 0
            for j in range(N):
                sum += f[j]*np.cos((k*(2*j+1)*i))
            C[i] = sum*a[i]
            if C[i] == 0:
                C[i] = 0.000001
        return C

    def IDCT(self, C):
        N = len(C)
        f = [0]*N
        a = [np.sqrt(1/N)] + [np.sqrt(2/N)]*(N-1)
        k = np.pi/(2*N)
        for i in range(N):
            sum = 0
            for j in range(N):
                sum += a[j]*C[j]*np.cos((2*i+1)*j*k)
            f[i] = sum
        return f

    def DCT_CLM(self, C):
        N = len(C)
        a = self.a
        F = 0
        for c in C:
            F += np.log2(np.abs(c)/a)
        F /= N
        return np.abs(F)

    def QF(self,F,w):
        length = self.length
        if int((F + length) / length) % 2 == w:
            QF = int(F / length)*length + length/2
        else:
            QF = int(F / length)*length - length/2
        return QF

    def QC(self, C,F,QFW):
        a = self.a
        CS = []
        for c in C:
            if QFW == 0:
                CS.append(np.sign(c) * a)
            else:
                t1 = np.sign(c)
                t2 = (np.abs(c)**(QFW/F))
                #print(c,QFW,F,t2)
                t3 = (a**(1-QFW/F))
                CS.append( t1 * t2 * t3 )
        return CS

    def type_change(self,filepath,filename,output_type):
        audio = AudioSegment.from_file(filepath)
        audio.export(f"{filename}",format=f"{output_type}")

    def add_watermark(self,x,code):
        length = self.length
        W = self.encode(code)
        #N = len(W) + 16
        N = len(W)
        L = self.L
        P = len(x)//(L*N)
        xp = []
        for i in range(P):
            #st = self.db(i//256)*2
            for j in range(N):
                C = self.DCT(np.array(x[i*N*L+j*L:i*N*L+j*L+L]))
                F = self.DCT_CLM(C)
                #if j < 16:
                #    QFW = self.QF(F,st[j])
                #else:
                    #QFW = self.QF(F,W[j - 16])
                QFW = self.QF(F, W[j])
                CS = self.QC(C,F,QFW)
                xp += self.IDCT(CS)
            #print((i+1)/P*100,'%')

        xp += list(x[P*N*L:len(x)])
        return xp

    def check_tag(self,data):
        num = [0]*(len(data) - 8)
        for i in range(8):
            num[0] *= 2
            num[0] += data[i]
        for i in range(len(num)-8):
            if data[i] == 1:
                num[i+1] = num[i] - 128
            num[i + 1] += num [i + 8]
        maxsum = 0
        maxarg = 0
        for i in range(min(self.N + 16,len(num) - 8)):
            if num[i] != num[i + 8]:
                num[i] = 0
            else:
                sum = 0
                for j in range(i,len(num),self.N + 16):
                    if num[j] == num[i]:
                        sum += 1
                if sum > maxsum:
                    maxsum = sum
                    maxarg = i
        return 0

    def check_watermark(self,x):
        length = self.length
        N = self.N
        M = N**2
        W = [0]*M
        data = []
        L = self.L
        P = len(x)//(L*M)
        for i in range(P):
            for j in range(M):
                #print("{}-{}".format(i,j))
                C = self.DCT(x[i*M*L+j*L:i*M*L+j*L+L])
                F = self.DCT_CLM(C)
                W[j] += int((F+length)/length)%2
                #data.append(int((F+length)/length)%2)
            #print((i+1)/P*100,'%')
        #start = self.check_tag(data)
        '''for i in range(start,len(data),N+16):
            if i+16+N >= len(data):
                break
            for j in range(N):
                W[j] += data[i+16+j]'''
        code = []
        for i in range(N):
            line = []
            for j in range(N):
                line.append(True if W[i*N+j] > P/2 else False)
            code.append(line)
        return code

    def draw_qrcode(self, code):
        N = len(code)
        img = Image.new('RGBA', (N, N), 'white')
        idrw = ImageDraw.Draw(img)
        for i in range(N):
            for j in range(N):
                if code[i][j]:
                    idrw.rectangle((i, j, i, j), fill='black')
        self.draw_location(idrw)
        return img

    def draw_big_martix(self, idrw, xy, div):
        x = xy[0]
        y = xy[1]
        idrw.rectangle((x*div, y*div, (x + 9)*div - 1, (y + 9)*div - 1), fill='white')
        idrw.rectangle(((x + 1)*div, (y + 1)*div, (x + 8)*div - 1, (y + 8)*div - 1), fill='black')
        idrw.rectangle(((x + 2)*div, (y + 2)*div, (x + 7)*div - 1, (y + 7)*div - 1), fill='white')
        idrw.rectangle(((x + 3)*div, (y + 3)*div, (x + 6)*div - 1, (y + 6)*div - 1), fill='black')

    def draw_small_martix(self, idrw, xy, div):
        x = xy[0]
        y = xy[1]
        idrw.rectangle((x*div, y*div, (x + 5)*div - 1, (y + 5)*div - 1), fill='black')
        idrw.rectangle(((x + 1)*div, (y + 1)*div, (x + 4)*div - 1, (y + 4)*div - 1), fill='white')
        idrw.rectangle(((x + 2)*div, (y + 2)*div, (x + 3)*div - 1, (y + 3)*div - 1), fill='black')

    def draw_mini_martix(self, idrw, xy, color, div):
        x = xy[0]
        y = xy[1]
        idrw.rectangle((x*div, y*div, x*div + 1, y*div + 1), fill=color)

    def draw_location(self, idrw):
        n = int(self.N ** 0.5)
        div = self.div
        self.draw_big_martix(idrw, (-1, -1), div)
        self.draw_big_martix(idrw, (-1, n - 8), div)
        self.draw_big_martix(idrw, (n - 8, -1), div)
        self.draw_small_martix(idrw, (4, (n // 2 - 2) * 1), div)
        self.draw_small_martix(idrw, (n // 2 - 2, 4), div)
        self.draw_small_martix(idrw, (n // 2 - 2, n // 2 - 2), div)
        self.draw_small_martix(idrw, (n - 9, n // 2 - 2), div)
        self.draw_small_martix(idrw, (n // 2 - 2, n - 9), div)
        self.draw_small_martix(idrw, (n - 9, n * 1 - 9), div)
        for i in range(8, n - 8):
            colorMap = {0: 'black', 1: 'white'}
            self.draw_mini_martix(idrw, (6, i), colorMap[i % 2], div)
            self.draw_mini_martix(idrw, (i, 6), colorMap[i % 2], div)

    def stand(self,n,q):
        num = int(n)
        if num >= q:
            return q-1
        elif num < -q:
            return -q
        else:
            return num

    def add_process(self,inputname,outputname,text):
        t0 = time.time()
        code = self.text2code(text)
        sound = AudioSegment.from_file(inputname)
        q = 2 ** (sound.sample_width * 8 - 1)
        samples = [i / q for i in list(sound.get_array_of_samples())]
        #print(max(samples),min(samples))
        #print(sound.get_array_of_samples())
        if sound.channels == 1:
            nsamples = self.add_watermark(samples,code)
        else:
            n = len(samples)//2
            samples1 = [samples[2*i] for i in range(n)]
            samples2 = [samples[2*i+1] for i in range(n)]
            samples1 = self.add_watermark(samples1,code)
            #samples2 = self.add_watermark(samples2,code)
            nsamples = [samples1[i//2] if i % 2 == 0 else samples2[i//2] for i in range(2*n)]

        #print(max(nsamples),min(nsamples))
        nsamples = array.array(sound.array_type, [self.stand(i*q,q) for i in nsamples])
        nsound = sound._spawn(nsamples)
        nsound.export(outputname,format=outputname.split('.')[-1])
        t1 = time.time()
        print(f"{inputname}->{outputname}:{(t1-t0)/60}mins")

    def check_process(self,filename,code):
        t0 = time.time()
        code = self.extend(code)
        sound = AudioSegment.from_file(filename)
        q = 2 ** (sound.sample_width * 8 - 1)
        samples = [i / q for i in list(sound.get_array_of_samples())]
        N = len(code)
        if sound.channels == 1:
            ncode = self.check_watermark(samples)
            sum = 0
            for i in range(N):
                for j in range(N):
                    if ncode[i][j] != code[i][j]:
                        sum += 1
            print(filename+f':{sum/N**2}')

        else:
            n = len(samples) // 2
            samples1 = [samples[2 * i] for i in range(n)]
            samples2 = [samples[2 * i + 1] for i in range(n)]
            ncode1 = self.check_watermark(samples1)
            ncode2 = self.check_watermark(samples2)
            sum = 0
            for i in range(N):
                for j in range(N):
                    if ncode1[i][j] != code[i][j]:
                        sum += 1
            print(filename+f'-1:{sum/N**2}')
            sum = 0
            for i in range(N):
                for j in range(N):
                    if ncode2[i][j] != code[i][j]:
                        sum += 1
            print(filename+f'-2:{sum/N**2}')
        t1 = time.time()
        print(f"check{filename}:{(t1-t0)/60}mins")

    def draw_process(self,inputname,outputname):
        t0 = time.time()
        sound = AudioSegment.from_file(inputname)
        q = 2 ** (sound.sample_width * 8 - 1)
        samples = [i / q for i in list(sound.get_array_of_samples())]
        if sound.channels == 1:
            ncode = self.check_watermark(samples)
            img = self.code2image(ncode)
            img.save(outputname)

        else:
            n = len(samples) // 2
            samples = [samples[2 * i] for i in range(n)]
            #samples2 = [samples[2 * i + 1] for i in range(n)]
            ncode = self.check_watermark(samples)
            #ncode2 = self.check_watermark(samples2)
            img = self.code2image(ncode)
            img.save(outputname)
            #img2 = self.draw_qrcode(ncode2)
            #img2.save('2_'+outputname)
        t1 = time.time()
        print(f"draw{inputname}:{(t1 - t0) / 60}mins")

    def extend(self,code):
        div = self.div
        ncode = []
        for i in range(len(code)):
            row = []
            for j in range(len(code)):
                row += [code[i][j]]*div
            ncode += [row]*div
        return ncode

    def decode(self,filename):
        reader = zxing.BarCodeReader()
        barcode = reader.decode(filename)
        print(barcode.parsed)
        return barcode.parsed

    def getlen(self,c):
        if c >= u'\u4e00' and c <=u'\u9fa5':
            return 16
        else:
            return 8

    def text2code(self,text):
        N = self.N
        if len(text) > 56:
            fontsize = 8
        else:
            fontsize = 16
        n = N//fontsize
        font = ImageFont.truetype('simhei', fontsize, encoding='utf-8')
        image = Image.new('1', (N, N), 'white')
        draw = ImageDraw.Draw(image)
        k = 0
        tag = 0
        while tag != len(text):
            length = 0
            line = ""
            while tag != len(text) and length + self.getlen(text[tag]) <= N:
                length += self.getlen(text[tag])
                line += text[tag]
                tag += 1
            draw.text((0, fontsize*k),
                  line,
                  font=font)
            k += 1
        return np.array(image, dtype=int)

    def code2image(self,code):
        N = self.N
        ncode = [[False]*N for i in range(N)]
        for i in range(N):
            for j in range(N):
                ncode[i][j] = True if code[i][j] == 1 else False
        return Image.fromarray(np.array(ncode))

if __name__ == '__main__':
    data = "SP-OFFICIAL 测试文字效果"
    aw = audio_watermark()
    #加水印（大小限制中文不要超过225）
    aw.add_process('test.mp3','test-af.mp3',data)
    #测水印
    aw.draw_process('test-af.mp3','test-af.png')