from PIL import Image, ImageEnhance
import subprocess
import cv2
import time
import wx
import sys, os
from argparse import ArgumentParser


def take_screenshot(image_name):
    app = wx.App()
    screen = wx.ScreenDC()
    size = screen.GetSize()
    bmp = wx.Bitmap(size[0], size[1])
    mem = wx.MemoryDC(bmp)
    mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
    del mem
    image_name = image_name.split('.')[0]
    image_path = image_name + "_blah.png"
    bmp.SaveFile(image_path, wx.BITMAP_TYPE_PNG)
    img = Image.open(image_path)
    width, height = img.size
    img2 = img.crop((200, 200, 1536, 864))
    final_image_path = os.path.join(os.environ["HOMEPATH"], "Desktop", os.path.basename(image_name) + "_portratari.png")
    img2.save(final_image_path)


def start_your_engines(image_name):
    im = Image.open(image_name)

    scaledIm = im.resize((40, 192)) # resize to correct dimensions
    scaledIm = ImageEnhance.Contrast(scaledIm).enhance(3.0)
    scaledIm = ImageEnhance.Sharpness(scaledIm).enhance(2.0)
    scaledIm = ImageEnhance.Color(scaledIm).enhance(3.0)
    scaledIm = ImageEnhance.Brightness(scaledIm).enhance(1)
    threshold = 220
    fn = lambda x : 255 if x > threshold else 0
    bwim = scaledIm.convert('L').point(fn, mode='L') # convert to grayscale
    bwim.save('mask.png') # saves image in executing directory
    subprocess.call('fsb mask.png')
    # creates mask.asm 
    subprocess.call('dasm test.asm -f3 -otest.bin')
    # creates binary
    subprocess.Popen('Stella\\Stella -fullscreen 1 test.bin')
    # spins up binary in Stella
    # Screenshot and export
    time.sleep(2)
    take_screenshot(image_name)
    sys.exit()


def show_webcam(mirror = True):
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Camera Viewer")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        cv2.imshow("Camera Viewer", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "photo_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            start_your_engines(img_name)
            img_counter += 1

    cam.release()

    cv2.destroyAllWindows()


def main(image):
    if image is not None:
        start_your_engines(image)
    else:
        show_webcam(mirror = True)

    
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-i", "--image")
    args = parser.parse_args()
   
    main(args.image)



