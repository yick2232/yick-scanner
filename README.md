# yick-scanner
    * 毕业设计
    * 一个基于HTML5的Android app
    * 用于拍摄并识别名片上面的人物信息
    * 可以用户通过此app录入名片人物信息，高效省时。

# 背景和目的
    * 随着计算机、手机、互联网的兴起，
    * 人类从互联网时代跨入了移动互联网时代，
    * 目前正在进行着从移动互联网时代到AI时代的变迁。
    * 移动设备越来越普及，图像识别也越来越深入到人们生活的方方面面，
    * 计算机或只能设备能做的事情也越来越多，
    * 这款名片识别软件就是基于移动设备、图像处理技术和图像识别技术而开发的软件。
    * AI时代的来临，重复、枯燥并且毫无意义的工作我们都可以交给机器来解决，
    * 人类应该做一些更富有创新性的工作。
    * 目前纸质名片相较于电子名片更常见，所以本软件能够帮助人们轻松地将纸质名片数字化、信息化。
 

# 包依赖
    * 前端：H5+
    * 后台：
        * 1. pip install tornado
        * 2. pip install pymongo
        注: 需要安装mongodb，
            具体安装步骤可参考官方文档说明:
            https://docs.mongodb.com/manual/
    * 算法：
        * 1. pip install numpy
        * 2. git@github.com:opencv/opencv.git
        * 3. git@github.com:tesseract-ocr/tesseract.git
        注: 从源代码安装，opencv和tesseract均为C++项目，
            首先git clone，再进入目录查看README.md文档,
            或者进入相应的官方网站查看相关帮助文档，
            根据相关文档对源代码进行编译得到动态链接文件或者二进制文件,
            再拷贝到Python模块安装目录下

# 目录结构
    ├── algorithm
    │   ├── analyze.py
    │   ├── preprocessing.py
    │   ├── preprocessing.pyc
    │   ├── README.md
    │   ├── recognize.py
    │   └── svm.py
    ├── back-end
    │   ├── file_receiver.py
    │   ├── http_server.py
    │   ├── mongo_utils.py
    │   └── README.md
    ├── ChangeLog
    │
    ├── data
    │
    ├── front-end
    │   └── README.md
    ├── log
    │   └── run_log
    └── README.md
