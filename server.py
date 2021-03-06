import qrcode
import Tkinter
from PIL import Image, ImageTk, ImageSequence
from visvis.vvmovie.images2gif import writeGif, GifWriter
import time
import cv2
import sys, os
from cStringIO import StringIO
from pymongo import MongoClient
from bson.binary import Binary
import socket

mongo_client = MongoClient(host="162.243.43.38")
db = mongo_client.pix
coll = db.pictures

vc = cv2.VideoCapture(0)

#ip = socket.gethostbyname(socket.gethostname())
ip = "162.243.43.38"
port = "80"

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
        img = Image.fromarray(frame)
        self.frames.append(img)
        self.root.after(100, self.add_frame)


    def take_photo(self, time):
        rval, frame = vc.read()
        img = Image.fromarray(frame)
        fp = StringIO()
        img.save(fp, format="JPEG")
        coll.insert({"time" : time, "picture" : Binary(fp.getvalue())})


    def update_code(self):
        self.take_photo(self.now)
        self.now = time.strftime("%Y-%m-%d-%H-%M-%S")
       
        url = "http://%s:%s/qr/%s" % (ip, port, self.now)
        self.img = qrcode.make(data=url)
        self.tkimage = ImageTk.PhotoImage(self.img)

        self.root.geometry('%dx%d' % (self.img.size[0], self.img.size[1]))
        self.tkimage = ImageTk.PhotoImage(self.img)
        self.label_image.configure(image=self.tkimage)
        self.label_image.pack()

        #self.root.after(100, self.add_frame)
        self.root.after(5000, self.update_code)

app = StupidApp()
