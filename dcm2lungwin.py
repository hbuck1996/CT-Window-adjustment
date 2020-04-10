# -*- coding=utf-8 -*-

import pydicom
import os
import numpy
from os.path import splitext
import PIL.Image as Image

def getfile(file):
    dcm = pydicom.dcmread(file)
    img2 = dcm.pixel_array * dcm.RescaleSlope + dcm.RescaleIntercept
    return img2

def get_window_size(window_type):
    if window_type =='lung':#肺窗
        center = -600
        width = 1200
    elif window_type =='Mediastinal':#纵膈窗
        center =40
        width =400
    return center, width

#调整CT图像的窗宽窗位

def setDicomWinWidthWinCenter(img_data, window_type):
    img_temp = img_data
    rows =len(img_temp)
    cols =len(img_temp[0])
    center, width = get_window_size(window_type)
    img_temp.flags.writeable =True
    min = (2 * center - width) /2.0 +0.5
    max = (2 * center + width) /2.0 +0.5
    dFactor =255.0 / (max - min)
    for i in numpy.arange(rows):
        for j in numpy.arange(cols):
            img_temp[i, j] =int((img_temp[i, j]-min)*dFactor)
    min_index = img_temp <0
    img_temp[min_index] =0
    max_index = img_temp >255
    img_temp[max_index] =255
    return img_temp

pathin = 'dcmin/'
pathout = 'dcmout/'
for root, dirs, files in os.walk(pathin):
    for i in range(len(files)):
        filename = files[i]
        im = getfile(pathin + filename)
        im1 = setDicomWinWidthWinCenter(im, 'lung')
        dcm_img = Image.fromarray(im1)
        dcm_img = dcm_img.convert('L')
        output = splitext(files[i])[0]+"." +"png"
        dcm_img.save(pathout + output)

