#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '仅用于界面上打开目录测试'
__author__ = '皮'
__mtime__ = '12/29/2015-029'
__email__ = 'pipisorry@126.com'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.myButton = QtWidgets.QPushButton(self)
        self.myButton.setObjectName("myButton")
        self.myButton.setText("Test")
        self.myButton.clicked.connect(self.msg)

    def msg(self):
        directory1 = QFileDialog.getExistingDirectory(self, "选取文件夹", "C:/")  # 起始路径
        print(directory1)

        fileName1, filetype = QFileDialog.getOpenFileName(self, "选取文件", "C:/",
                                                          "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,注意用双分号间隔
        print(fileName1, filetype)

        files, ok1 = QFileDialog.getOpenFileNames(self, "多文件选择", "C:/", "All Files (*);;T Files (*.txt)")
        print(files, ok1)

        fileName2, ok2 = QFileDialog.getSaveFileName(self, "文件保存", "C:/", "All Files (*);;Text Files (*.txt)")


def test():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()
    sys.exit(app.exec_())
