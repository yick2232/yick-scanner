#!/usr/bin/env python
#-*- coding:utf-8 -*-


import os
import sys
import json
import logging
import wsgiref.simple_server
from tornado import web
from tornado import wsgi
from tornado import ioloop
from tornado import httpserver
from tornado.options import define
from tornado.options import options
from tornado.options import parse_command_line
from mongo_utils import save_to_mongo

sys.path.append('../algorithm')
from recognize import Recognizer
from analyze import analyze

reload(sys)
sys.setdefaultencoding('utf8')


define('port', default = 8888, help = '服务器监听端口', type = str)
define('data-dir', default = '/home/ubuntu/yick-scanner/data', type = str)
try:
    define('tesseract', default = '/home/ubuntu/apps/tesseract/api/tesseract')
except Exception as e:
    logging.info(e)


class IndexHandler(web.RequestHandler):
    def get(self):
        pass

    def save(self, file_name, file_body):
        with open(file_name, 'wb') as save_file:
            print >> save_file, file_body
    
    def post(self):
        logging.info('服务器接收到post请求')
        result = None
        for field_name, files in self.request.files.items():
            for info in files:
                file_name, content_type = info['filename'], info['content_type']
                body = info['body']
                dir_name = options.data_dir + '/' + file_name[:file_name.rfind('.')]
                if not os.path.exists(dir_name):
                    os.system('mkdir -p %s' % dir_name)
                file_name = dir_name + '/' + file_name
                self.save(file_name, body)
                logging.info('save image is ok.')
                result = analyze(options.tesseract, file_name)
                logging.info('POST "%s" "%s" %d bytes',
                             file_name, content_type, len(body))
        logging.info(type(result))
        if result is not None:
            logging.info(len(result))
        for key, value in result.iteritems():
            logging.info('key, %s, value: %s', key, value)
        save_to_mongo(result)
        self.write(json.dumps(result, ensure_ascii=False).encode('utf8'))


def start_server(handlers = None, port = 8888, numprocs = 2):

    cmd = 'mkdir -p %s' % options.data_dir
    os.system(cmd)
    
    # 单例模式 先加载进内存初始化
    recognizer_instance = Recognizer()

    app = web.Application(handlers = [(r'/', IndexHandler)])
    app = wsgi.WSGIAdapter(app)
    server = wsgiref.simple_server.make_server('', port, app)
    server.serve_forever()


def main():
    start_server(port = options.port)


if __name__ == '__main__':
    parse_command_line()
    main()
