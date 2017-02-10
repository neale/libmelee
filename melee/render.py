#!/usr/bin/env python3
import gi

gi.require_version('Gdk', '3.0')

from gi.repository import Gdk as gdk
import numpy as np
import PIL.Image as Image
import io

class Renderer(object):

    def __init__(self, h, w):
    
        self.desktop       = gdk.get_default_root_window()
        self.desktop_shape = (self.desktop.get_width(), self.desktop.get_height())
        self.frame         = None
                
    def get_frame(self):
        bb = gdk.pixbuf_get_from_window(self.desktop, 0, 0, 640, 480)
    
        byte  = bb.get_pixels()
        mode  = 'RGBA'
        out   = io.BytesIO()
        image = Image.frombuffer(mode, (480, 240), byte, 'raw', mode, 0, 1)
        image.readonly = 0
        image.save(out, "PNG")
        out.seek(0)
        Image.open(out).show()
        #image = np.reshape(image, (480,240 ))
        self.frame = np.array(image)

    def show_frame(self):
        img = Image.fromarray(self.frame, 'RGB')
        img.show()




def test():
    
    renderer = Renderer(480, 640)
    renderer.get_frame()

if __name__ == '__main__':
    
    test()




