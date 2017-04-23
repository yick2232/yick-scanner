#!/usr/bin/env python
#-*- coding:utf-8 -*-


import sys
reload(sys)
sys.setdefaultencoding('utf8')

import re
import logging
import tornado.options
from tornado.options import parse_command_line
from tornado.options import options, define
from collections import defaultdict
from preprocessing import preprocessing
from recognize import recognize

try:
    define('img-file', default = '/tmp/files/P70214-185110.jpg')
except Exception as e:
    logging.info(e)


remove_space = lambda text: ''.join([ch for ch in text if ch not in ['', ' ', '\t', '\n']])


def is_name(text):
    if u'姓名：' in text:
        return text[text.find(u'姓名：') + len(u'姓名') : ]
    if u'姓名' in text:
        return text[text.find(u'姓名') + len(u'姓名') : ]
    if len(text) in [2, 3, 4]:
        return text
    return None
    

def is_phone_number(text):
    pattern = r'1\d{10}'
    match = re.search(pattern, text)
    if match is None:
        return None
    return match.group()


def is_email(text):
    pattern = r'(^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$)'
    match = re.search(pattern, text)
    if match is None:
        return None
    return match.group()


def analyze(tesseract, image_file):
    image_files_list = preprocessing(image_file)
    result = defaultdict(lambda: '')
    for image_file in image_files_list:
        if 'tmp0.jpg' in image_file:
            continue
        text = recognize(tesseract, image_file)
        text = unicode(text)
        text = remove_space(text)

        logging.info(text)
        if is_name(text):
            result['Name'] = is_name(text)
        elif is_phone_number(text):
            result['PhoneNumber'] = is_phone_number(text)
        elif is_email(text):
            result['Email'] = is_email(text)

    return result
            

def main():
    image_file = options.img_file
    result = analyze(image_file)
    for key, value in result.iteritems():
        logging.info('%s: %s' % (key, value[0]))


if __name__ == '__main__':
    parse_command_line()
    main()
