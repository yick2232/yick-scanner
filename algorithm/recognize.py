#!/usr/bin/env python
#-*- coding:utf-8 -*-


import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import json
import ctypes
import logging
import tornado.options
from tornado.options import parse_command_line
from tornado.options import options, define

try:
    define('img-file', default = '/tmp/files/P70214-185110.jpg')
except Exception as e:
    logging.info(e)

try:
    define('tesseract', default = '/home/ubuntu/apps/tesseract/api/tesseract')
except Exception as e:
    logging.info(e)


def Singleton(cls):
    instance = cls()
    instance.__call__ = lambda: instance
    return instance


@Singleton
class Recognizer:
    def __init__(self, libname = '/home/ubuntu/apps/tesseract/api/.libs/libtesseract.so.4.0.0', lang = 'chi_sim'):
        self.libname = libname
        self.lang = lang
        self.tesseract = ctypes.cdll.LoadLibrary(self.libname)
        self.TESSDATA_PREFIX = os.environ.get('TESSDATA_PREFIX')
        self.api = self.tesseract.TessBaseAPICreate()
        self.recognizer = self.tesseract.TessBaseAPIInit3(self.api, self.TESSDATA_PREFIX, self.lang)


def recognize(tesseract, image_file):
    logging.info(image_file)
    #recognizer = Recognizer()
    #text_out = recognizer.tesseract.TessBaseAPIProcessPages(recognizer.api, image_file, None, 0, None)
    #text_out = recognizer.tesseract.TessBaseAPIGetUTF8Text(recognizer.api)
    #result_text = ctypes.string_at(text_out)
    result_file = image_file[: image_file.rfind('.') + 1] + 'result'
    cmd = '%s %s %s -l chi_sim' % (tesseract, image_file, result_file)
    os.system(cmd)
    result_text = u''
    result_file += '.txt'
    with open(result_file, 'rb') as result_file:
        result_text += '\n'.join(result_file.readlines())
    return result_text


def main():
    recognizer = Recognizer()
    text = recognizer.recognize(options.tesseract, options.img_file)
    logging.info(text)


if __name__ == '__main__':
    parse_command_line()
    logging.info('ok')
    main()
