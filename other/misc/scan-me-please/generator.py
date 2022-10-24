
flag = "STDIO18{ea6deb548911c40fb068017f7a53c7e1}"

import qrcode
from PIL import Image
import numpy as np
import random

random.seed(1337)
np.random.seed(1337)

print("== creating flag.png")
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=1,
    border=0)
qr.add_data(flag)
qr.make(fit = True)
img = qr.make_image()
img.save('flag.png')
print("created flag.png")

import base64
print("== base64 flag.png")
encoded_string = ''
with open('flag.png','rb') as image_file:
    encoded_string = base64.b64encode(image_file.read()) + '=='.encode()
    print('got',encoded_string)

print("== create original-flag.png")
qr2 = qrcode.QRCode(
    version=18,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=1,
    border=0)
qr2.add_data(encoded_string)
qr2.make(fit = True)
img2 = qr2.make_image()
img2.save('original-flag.png')
print("created original-flag.png")

print("== reconstruct pixels to rickroll")
with Image.open("original-flag.png") as im:
    px = im.load()
    ab = []
    aw = []
    orig = np.zeros([im.size[0]*im.size[1], 3], dtype=np.uint8)
    i=0
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            orig[i] = (x,px[x,y],y)
            if px[x,y] == 0:
                ab.append([x,px[x,y],y])
            else:
                aw.append([x,px[x,y],y])
            i+=1
    random.shuffle(ab)
    random.shuffle(aw)
    
    #imx = Image.fromarray(orig.reshape(im.size[0],im.size[1],3),"RGB")
    #imx.show()
    
    with Image.open("rickrolled.png") as im2:
        px2 = im2.load()
        assert im.size == im2.size, "incorrect size of images"
        b = np.zeros([im.size[0]*im.size[1], 3], dtype=np.uint8)
        i = 0
        for x in range(im2.size[0]):
            for y in range(im2.size[1]):
                if px2[x,y] == (0,0,0):
                    if len(ab):
                        b[i] = ab.pop(0)
                    else:
                        b[i] = aw.pop(0)
                else:
                    if len(aw):
                        b[i] = aw.pop(0)
                    else:
                        b[i] = ab.pop(0)
                i+=1
    
        im2 = Image.fromarray(b.reshape(im.size[0],im.size[1],3),"RGB")
        #im2.show()
        im2.save('ch18_misc_scan-me-please.png')
        print("created ch18_misc_scan-me-please.png")

# cleanup
print("== cleanup test image")
import os
os.system("rm flag.png original-flag.png")
print("done")
