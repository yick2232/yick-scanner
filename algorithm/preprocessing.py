#!/usr/bin/env python
#-*- coding:utf-8 -*-


import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import cv2 as cv
import logging
import numpy
import tornado.options
from tornado.options import parse_command_line
from tornado.options import options, define

try:
    define('img-file', default = '/tmp/files/P70214-185110.jpg')
except Exception as e:
    logging.info(e)

define('size', default = 1000)
define('min-area', 2000)
define('min-x', default = 10)
define('min-y', default = 10)


def to_binary(image):
    # 将图像转换为固定大小
    image = cv.resize(image, (options.size, options.size), interpolation = cv.INTER_AREA)

    # 转换成灰度图
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # 滤波
    gray = cv.GaussianBlur(gray, (5, 5), 0)
    gray = cv.medianBlur(gray, 5)
    
    # 提取Sobel直角特征，求x方向的梯度
    sobel_x = cv.Sobel(gray, cv.CV_8U, 1, 0, 3)
    #sobel_x = gray
    
    # OTSU提取二值图像
    retval, thresh = cv.threshold(sobel_x, 0, 255, cv.THRESH_OTSU)

    return thresh


def get_contours(image):
    # 膨胀
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (30, 9))
    image = cv.dilate(image, kernel, iterations = 1)

    # 腐蚀
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (24, 6))
    image = cv.erode(image, kernel, iterations = 1)
    
    #cv.imwrite('erode.jpg', image)

    # 再次膨胀
    #image = cv.dilate(image, kernel, iterations = 3)
    
    im2, contours, hierarchy = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    #logging.info('-' * 100)
    #logging.info(type(im2))
    #cv.imwrite('coutours.jpg', im2)
    return contours


def contours_filter(contours):
    res = list()
    count = [0 for a in xrange(4)]
    for contour in contours:
        area = cv.contourArea(contour)
        count[0] += 1
        # 过滤掉面积小的
        if area < options.min_area:
            continue
        count[1] += 1
        x, y, w, h = cv.boundingRect(contour)
        # 过滤掉竖状的
        if w <= h:
            continue
        count[2] += 1
        # 过滤掉靠近边缘的
        if x < options.min_x or y < options.min_y:
            continue
        if (x + w > options.size - options.min_x or
            y + h > options.size - options.min_y):
            continue
        count[3] += 1
        res.append(contour)
    logging.info(count)
    logging.info(len(res))
    return res


def get_image_by_contours(image, contours):
    logging.info(type(contours))
    logging.info(len(contours))
    
    # 将图像转换为固定大小
    image = cv.resize(image, (options.size, options.size), interpolation = cv.INTER_AREA)

    # 转换成灰度图
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # 滤波
    #gray = cv.GaussianBlur(gray, (5, 5), 0)
    #gray = cv.medianBlur(gray, 5)

    # 用OTSU转换二值图像
    retval, thresh = cv.threshold(gray, 0, 255, cv.THRESH_OTSU | cv.THRESH_TOZERO_INV)
    #cv.imwrite('thresh.jpg', thresh)

    image = thresh

    def reduction_size(x, y, w, h):
        X, Y = image.shape
        x_rate = X / options.size
        y_rate = Y / options.size
        x *= x_rate
        y *= y_rate
        w *= x_rate
        h *= y_rate
        return x, y, w, h

    image_of_text_list = list()
    for index in xrange(len(contours)):
        x, y, w, h = cv.boundingRect(contours[index])
        #logging.info('x: %d, y: %d, w: %d, h: %d' % (x, y, w, h))
        #x, y, w, h = reduction_size(x, y, w, h)
        logging.info('x: %d, y: %d, w: %d, h: %d' % (x, y, w, h))
        #image = cv.rectangle(image, (x, y), (x + w, y + h), (255, 0, 255), 2)
        tmp = image[y : y + h, x : x + w]
        #cv.imwrite('tmp%d.jpg' % index, tmp)
        image_of_text_list.append(tmp)

    #cv.imwrite('draw.jpg', image)
    return image_of_text_list


def preprocessing(image_file):
    logging.info(image_file)
    image = cv.imread(image_file)
    image_bin = to_binary(image.copy())
    #cv.imwrite('image_bin.jpg', image_bin)
    contours = get_contours(image_bin.copy())
    contours = contours_filter(contours)
    image_of_text_list = get_image_by_contours(image.copy(), contours)
    image_files_list, dir_name = list(), image_file[:image_file.rfind('/')]
    for index in xrange(len(image_of_text_list)):
        image_tmp_file = '%s/tmp%d.jpg' % (dir_name, index)
        cv.imwrite(image_tmp_file, image_of_text_list[index])
        image_files_list.append(image_tmp_file)
    return image_files_list


def main():
    img_file = options.img_file
    image_of_text_list = preprocessing(img_file)


if __name__ == '__main__':
    parse_command_line()
    main()
