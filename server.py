import qrcode
import Tkinter
from PIL import Image, ImageTk, ImageSequence
from visvis.vvmovie.images2gif import writeGif, GifWriter
import time
import cv2
import sys, os
from cStringIO import StringIO

vc = cv2.VideoCapture(0)

class StupidApp():
    def __init__(self):
        self.root = Tkinter.Tk()

        self.qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        self.label_image = Tkinter.Label()
        self.label_image.pack()
        self.now = time.strftime("%H:%M:%S")
        self.frames = []

        self.update_code()
        self.root.mainloop()


    def add_frame(self):
        rval, frame = vc.read()
        img = Image.fromarray(frame)#, "RGB")#.convert('P', palette=Image.ADAPTIVE)
        self.frames.append(img)
        self.root.after(100, self.add_frame)


    def take_photo(self, time):
        rval, frame = vc.read()
        img = Image.fromarray(frame, "RGB")
        #fp = String()
        img.save(time + ".jpg")


    def update_code(self):
        self.take_photo(self.now)
        self.now = time.strftime("%H-%M-%S")
        
        self.img = qrcode.make(data=self.now)
        self.tkimage = ImageTk.PhotoImage(self.img)
        self.img.save("code.png")

        self.root.geometry('%dx%d' % (self.img.size[0], self.img.size[1]))
        self.tkimage = ImageTk.PhotoImage(self.img)
        self.label_image.configure(image=self.tkimage)
        self.label_image.pack()

        #self.root.after(100, self.add_frame)
        self.root.after(1000, self.update_code)

app = StupidApp()
