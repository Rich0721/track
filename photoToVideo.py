import os
from glob import glob
import cv2


TEST_PATH = "./test_image/20190601125502000/"

images = glob(os.path.join(TEST_PATH, "*.jpg"))

img_array = []

for img in images:
    read = cv2.imread(img)
    h, w, layers = read.shape
    size = (w, h)
    img_array.append(read)

out = cv2.VideoWriter("test.mp4", cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

for i in range(len(img_array)):
    out.write(img_array[i])

out.release()