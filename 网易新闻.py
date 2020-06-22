# -*- coding: utf-8 -*-

import sys
from moban import ChildWindow as a
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import qdarkstyle
import re

class ChildWindow(a):
    def __init__(self, parent=None):
        super(ChildWindow, self).__init__(parent)

    # 选择开启的功能
    def open_chose(self):
        # self.open1()
        # self.open2()
        # self.open3()
        # self.open4()
        self.open5()
        # self.open6()
        # self.open7()

    # 检查参数是否正确
    def find_error(self):
        self.interface_data_state = True
        # if not self.param["1 1"]:
        #     self.interface_data_state = False
        # if not self.in_address:
        #     self.interface_data_state = False
        # if self.param["4 1"] > self.param["4 2"]:
        #     self.interface_data_state = False
        #     self.textBrowser_3.append("页码参数设置有误，请重新输入")
        if self.param["5"] == []:
            self.interface_data_state = False
            self.textBrowser_3.append("请至少勾选一个项目")

    # 显示参数列表
    def show_param(self):
        if self.param["3 3"]:
            text3 = "全部"
        else:
            text3 = self.param["3 1"] + " 到 " + self.param["3 2"]
        if self.param["4 3"]:
            text4 = "全部"
        else:
            text4 = self.param["4 1"] + " 到 " + self.param["4 2"]
        self.textBrowser_1.setText(
            # "关键字：" + self.param["1 1"] +
            # "\r关键字：" + self.param["1 2"] +
            # "\r搜索规则：" + self.param["2 1"] + " " + self.param["2 2"] + " " + self.param["2 3"] +
            # "\r价格区间：" + text3 +
            # "搜索页数：" + text4 +
            "多选项目：" + str(self.param["5"])
            # "\r日期：" + self.param["6 1"] + " 至 " + self.param["6 2"]
        )

    def set_all(self):
        self.thread = yangshi()
        self.thread.error_thread.connect(self.add_text)
        self.thread.result_thread.connect(self.show_table)
        self.thread.state_thread.connect(self.over_thread)
        self.thread.msg_thread.connect(self.show_msg)
        self.thread.img_thread.connect(self.show_img)

        self.pushButton_5.clicked.connect(self.thread.break_work)

        # 子窗口名字修改
        self.setWindowTitle("网易新闻爬虫")

        # 子窗口最大化
        # self.showMaximized()

        # box标题
        self.groupBox.setTitle("网易新闻")

        # 表格
        self.table_list = ["分类", "标题", "新闻网址", "评论网址", "跟帖次数", "红框分类", "标签", "关键字1", "关键字1网址", "关键字2", "关键字2网址", "关键字3", "关键字3网址", "时间", "新闻类型", "频道名称", "来源", "图片"]

        self.checkBox_12.setText("要闻")
        self.checkBox_13.setText("国内")
        self.checkBox_21.setText("国际")
        self.checkBox_22.setText("独家")
        self.checkBox_23.setText("军事")
        self.checkBox_31.setText("财经")
        self.checkBox_32.setText("科技")
        self.checkBox_33.setText("体育")
        self.checkBox_41.setText("娱乐")
        self.checkBox_42.setText("时尚")
        self.checkBox_43.setText("汽车")
        self.checkBox_51.setText("房产")
        self.checkBox_52.setText("航空")
        self.checkBox_53.setText("健康")

    def show_table(self, a):
        self.model.appendRow(
            [QStandardItem(str(a["分类"])),
             QStandardItem(str(a["title"])),
             QStandardItem(str(a["docurl"])),
             QStandardItem(str(a["commenturl"])),
             QStandardItem(str(a["tienum"])),
             QStandardItem(str(a["tlastid"])),
             QStandardItem(str(a["label"])),
             QStandardItem(str(a["keywords"][0]["keyname"])),
             QStandardItem(str(a["keywords"][0]["akey_link"])),
             QStandardItem(str(a["keywords"][1]["keyname"])),
             QStandardItem(str(a["keywords"][1]["akey_link"])),
             QStandardItem(str(a["keywords"][2]["keyname"])),
             QStandardItem(str(a["keywords"][2]["akey_link"])),
             QStandardItem(str(a["time"])),
             QStandardItem(str(a["newstype"])),
             QStandardItem(str(a["channelname"])),
             QStandardItem(str(a["source"])),
             QStandardItem(str(a["imgurl"]))
             ]
        )
        self.tableView.scrollToBottom()

        self.sheet.write(self.book_row, 0, a["分类"])
        self.sheet.write(self.book_row, 1, a["title"])
        self.sheet.write(self.book_row, 2, a["docurl"])
        self.sheet.write(self.book_row, 3, a["commenturl"])
        self.sheet.write(self.book_row, 4, a["tienum"])
        self.sheet.write(self.book_row, 5, a["tlastid"])
        self.sheet.write(self.book_row, 6, a["label"])
        self.sheet.write(self.book_row, 7, a["keywords"][0]["keyname"])
        self.sheet.write(self.book_row, 8, a["keywords"][0]["akey_link"])
        self.sheet.write(self.book_row, 9, a["keywords"][1]["keyname"])
        self.sheet.write(self.book_row, 10, a["keywords"][1]["akey_link"])
        self.sheet.write(self.book_row, 11, a["keywords"][2]["keyname"])
        self.sheet.write(self.book_row, 12, a["keywords"][2]["akey_link"])
        self.sheet.write(self.book_row, 13, a["time"])
        self.sheet.write(self.book_row, 14, a["newstype"])
        self.sheet.write(self.book_row, 15, a["channelname"])
        self.sheet.write(self.book_row, 16, a["source"])
        self.sheet.write(self.book_row, 17, a["imgurl"])



        self.book_row = self.book_row + 1



class yangshi(QThread):
    result_thread = pyqtSignal(dict)
    error_thread = pyqtSignal(str)
    state_thread = pyqtSignal(bool)
    msg_thread = pyqtSignal(str)
    img_thread = pyqtSignal(int)

    def __init__(self, parent=None):
        super(yangshi, self).__init__(parent)

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
        }

        self.dicts = {
            "要闻": "https://temp.163.com/special/00804KVA/cm_yaowen.js?callback=data_callback",
            "国内": "https://temp.163.com/special/00804KVA/cm_guonei.js?callback=data_callback",
            "国际": "https://temp.163.com/special/00804KVA/cm_guoji.js?callback=data_callback",
            "独家": "https://temp.163.com/special/00804KVA/cm_dujia.js?callback=data_callback",
            "军事": "https://temp.163.com/special/00804KVA/cm_war.js?callback=data_callback",
            "财经": "https://temp.163.com/special/00804KVA/cm_money.js?callback=data_callback",
            "科技": "https://temp.163.com/special/00804KVA/cm_tech.js?callback=data_callback",
            "体育": "https://temp.163.com/special/00804KVA/cm_sports.js?callback=data_callback",
            "娱乐": "https://temp.163.com/special/00804KVA/cm_ent.js?callback=data_callback",
            "时尚": "https://temp.163.com/special/00804KVA/cm_lady.js?callback=data_callback",
            "汽车": "https://temp.163.com/special/00804KVA/cm_auto.js?callback=data_callback",
            "房产": "https://temp.163.com/special/00804KVA/cm_houseshanghai.js?callback=data_callback",
            "航空": "https://temp.163.com/special/00804KVA/cm_hangkong.js?callback=data_callback",
            "健康": "https://temp.163.com/special/00804KVA/cm_jiankang.js?callback=data_callback"
        }

    def setidentity(self, dict):
        self.working = True
        self.identity = dict
        self.now = 0
        self.all = len(self.identity["5"])
        print(dict)

    def show_text(self, text:str):
        self.error_thread.emit(text)
        # print(text)

    def show_msg(self, text):
        self.msg_thread.emit(text)

    def show_img(self, text):
        self.img_thread.emit(text)

    def final_data(self, dict):
        self.result_thread.emit(dict)
        # print(dict)

    def break_work(self):
        self.show_text("正在中止程序...")
        self.working = False

    def get_text(self, url:str):
        i = 1
        try:
            response = requests.get(url, headers=self.headers, verify=True, timeout=2)
        except:
            try:
                response = requests.get(url, headers=self.headers, verify=True, timeout=2)
            except:
                try:
                    response = requests.get(url, headers=self.headers, verify=True, timeout=2)
                except:
                    i = 0
        if i == 1:
            response.encoding = response.apparent_encoding
            text = response.text
            return text
        else:
            return None

    def crawl(self, keyword):
        if self.working:
            url = self.dicts[keyword]
            # self.show_text("正在爬取关键字: " + keyword)
            self.show_msg("关键字: " + keyword )
            self.show_img(int(self.now/self.all*100))
            self.now = self.now+1
            text = self.get_text(url)
            if text:
                a = re.findall(".*?\((.*)\)", text, re.S)[0]
                a = str(a).replace("\n","").replace(" ","")
                try:
                    a = eval(a)
                    print(a)
                    for ii in a:
                        while len(ii["keywords"]) < 3:
                            ii["keywords"].append({'akey_link': '', 'keyname': ''})
                        ii["分类"] = keyword
                        self.final_data(ii)
                except:
                    self.show_text("关键字：" + str(keyword) + "出错，请求返回格式有误")
            else:
                self.show_text("关键字：" + str(keyword) + "爬取出错，无法访问该网址")

    def run(self):
        for i in range(len(self.identity["5"])):
            if self.working:
                self.show_text("正在爬取关键字: "+str(self.identity["5"][i])+"      关键字进度: "+str(i+1)+" / "+str(len(self.identity["5"])))
                # self.crawl(self.identity["key"][i], self.identity["page1"], self.identity["page2"])
                self.crawl(self.identity["5"][i])
            else:
                break
        self.state_thread.emit(False)
        if self.working:
            self.error_thread.emit("爬取完成")
            self.img_thread.emit(100)
        else:
            self.error_thread.emit("已中止程序")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyleSheet(qdarkstyle.load_stylesheet())
    form = ChildWindow()
    form.show()
    sys.exit(app.exec_())