
from __future__ import absolute_import

import os
import csv
import cv2

from glob import glob
from os import listdir

IMAGE_INPUT_PATH = "./input_image/"
TEXT_INPUT_PATH = "./output_text/"
OUTPUT_IMAGE_PATH = "./test_image/"

def openCsvFile(path):
    
    
    peopleCoordinate = []
    inputFile = open(path, newline='')
    
    rows = csv.DictReader(inputFile)
    for row in rows:
        temp = []
        temp.append(row['Number'])
        temp.append(row['xmin'])
        temp.append(row['ymin'])
        temp.append(row['xmax'])
        temp.append(row['ymax'])
        
        peopleCoordinate.append(temp)
    
    return peopleCoordinate

def computeCenter(coordinate):
    '''
    :param corrdinate:(number, xmin, ymin, xmax, ymax) 
    '''

    center_x = int((int(coordinate[3]) + int(coordinate[1])) / 2)
    center_y = int((int(coordinate[4]) + int(coordinate[2])) / 2)

    return center_x, center_y


def distance_play(image_folder, image_file, peopleCoordinates):

    img = cv2.imread(os.path.join(image_folder, image_file))
    print(image_file)
    for peopleCoordinate in peopleCoordinates:
        for coor in peopleCoordinate:
            center_x, center_y = computeCenter(coordinate=coor)
            print(center_x, center_x)
            img = cv2.circle(img, (center_x, center_y), 5, (255, 255, 0), -1)
        
    
    cv2.imshow("test", img)
    cv2.waitKey(1)
    cv2.imwrite(os.path.join(OUTPUT_IMAGE_PATH, image_file), img)

def computeIoU(rect1, rect2):
    """
    Compute Iou
    :param rec1: (x1, y1, x2, y2)

    :return True IoU >= 0.95
    :return False
    """

    # Compute area of each rectangles
    rect_area1 = (rect1[2] - rect1[0]) * (rect1[3] - rect1[1])
    rect_area2 = (rect2[2] - rect2[0]) * (rect2[3] - rect2[1]) 

    # Compute the sum area
    sum_area = rect_area1 + rect_area2

    # Find the each edge of intersect rectangle
    left_line = max(rect1[0], rect2[0])
    right_line = max(rect1[2], rect2[2])
    top_line = max(rect1[1], rect2[1])
    bottom_line = max(rect1[3], rect2[3])

    if left_line >= right_line or top_line >= bottom_line:
        return False
    
    intersect = (right_line - left_line) * (bottom_line - top_line)
    iou = (intersect / (sum_area - intersect)) * 1.0

    if iou >= 0.8:
        return True
    else:
        return False



if __name__=='__main__':
    
    image_dirs = listdir(IMAGE_INPUT_PATH)
    
    text_dirs = listdir(TEXT_INPUT_PATH)
    #print(image_dirs)
    image_files = glob(os.path.join(IMAGE_INPUT_PATH, image_dirs[0],'*.jpg'))
    text_files = glob(os.path.join(TEXT_INPUT_PATH, text_dirs[0], "*.csv"))
    
    image = None
    print(image_files[0][len(IMAGE_INPUT_PATH):])
    coordinates = []
    count = 0
    for text_file, image_file in zip(text_files, image_files):
        if count < 10:
            coordinates.append(openCsvFile(text_file))
            distance_play(image_folder=IMAGE_INPUT_PATH, image_file=image_file[len(IMAGE_INPUT_PATH):], peopleCoordinates=coordinates)
            count+= 1
        else:
            coordinates.pop(1)
            coordinates.append(openCsvFile(text_file))
            distance_play(image_folder=IMAGE_INPUT_PATH, image_file=image_file[len(IMAGE_INPUT_PATH):], peopleCoordinates=coordinates)
            count+= 1
    