# -*- coding: utf-8 -*-

import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from OG import Ui_MainWindow
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
import time
import os
import requests


class MainWin(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent)
        self.setupUi(self)
        self.initUI()


    def initUI(self):
        self.textBrowser.append("欢迎使用本软件")
        self.treeWidget.clicked.connect(self.onTreeClicked)
        self.pushButton.clicked.connect(self.open_ck)
        self.pushButton_2.clicked.connect(self.close)

        filename = "说明.txt"
        pf = open(filename, "r", encoding='UTF-8')
        a = pf.read()
        self.textBrowser_2.setPlainText(a)
        self.selected = False

        self.setWindowTitle("欢迎使用")

        try:
            ip = requests.get("http://icanhazip.com/", timeout=2)
            self.textBrowser.append("\r您的网络通畅，当前ip地址为：" + ip.text)
        except:
            self.textBrowser.append("\r请注意：您未连接网络或网络卡顿，未连接网络将无法使用此软件。")

    def onTreeClicked(self):
        item = self.treeWidget.currentItem()
        self.name = item.text(0)

        b = ["美团", "京东", "微博榜单", "微博话题", "中国天气网", "太平洋汽车", "猫眼评分",
             "B站视频", "B站视频弹幕", "B站番剧弹幕", "央视新闻", "网易新闻", "B站评论", "无忧招聘网"]
        if self.name in b:
            filename = "%s.txt" % self.name
            pf = open(filename, "r", encoding='UTF-8')
            a = pf.read()
            self.textBrowser_2.setPlainText(a)
            self.selected = True
        else:
            filename = "说明.txt"
            pf = open(filename, "r", encoding='UTF-8')
            a = pf.read()
            self.textBrowser_2.setPlainText(a)
            self.selected = False

    def open_ck(self):
        if self.selected == True:
            if self.name == "网易新闻":
                from 网易新闻 import ChildWindow
            elif self.name == "央视新闻":
                from 央视新闻 import ChildWindow
            elif self.name == "猫眼评分":
                from maoyanpingfen import ChildWindow
            elif self.name == "美团":
                from meituan import ChildWindow
            elif self.name == "京东":
                from jingdong import ChildWindow
            elif self.name == "微博榜单":
                from weibobangdan import ChildWindow
            elif self.name == "微博话题":
                from weibohuati import ChildWindow
            elif self.name == "中国天气网":
                from zhongguo import ChildWindow
            elif self.name == "太平洋汽车":
                from taipingyang import ChildWindow
            elif self.name == "B站视频":
                from bilibili import ChildWindow
            elif self.name == "B站视频弹幕":
                from shipindanmu import ChildWindow
            elif self.name == "B站番剧弹幕":
                from fanjudanmu import ChildWindow
            elif self.name == "B站评论":
                from bilibili评论 import ChildWindow
            elif self.name == "无忧招聘网":
                from 无忧网 import ChildWindow


            self.xxxx = ChildWindow()
            self.xxxx.close_singnal.connect(self.lianjie)
            form.close()
            self.xxxx.show()
        else:
            self.textBrowser.append("\r请选择您需要的功能。")

    def lianjie(self):
        form.show()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MainWin()
    form.show()
    sys.exit(app.exec_())