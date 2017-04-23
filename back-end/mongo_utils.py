#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import logging
from pymongo import MongoClient
from tornado.options import define
from tornado.options import options
from tornado.options import parse_command_line


define('mongo_addr', default = 'mongodb://yick:22322232@yick-tencent-ubuntu:27017')
define('database', default = 'scanner')
define('collection', default = 'res')


def save_to_mongo(res):
    #连接mongodb, 访问相应的database和collection
    client = MongoClient(options.mongo_addr)
    database = client[options.database]
    collection = database[options.collection]
    ret = collection.insert(res)
    if ret is None:
        logging.info('Save to mongo failed.')
        return False
    return True


def main():
    res = {'Name': 'rice'}
    save_to_mongo(res)


if __name__ == '__main__':
    parse_command_line()
    main()
