# -*- coding: utf-8 -*-

import sys
from moban import ChildWindow as a
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import re

class ChildWindow(a):
    def __init__(self, parent=None):
        super(ChildWindow, self).__init__(parent)


    # 选择开启的功能
    def open_chose(self):
        # self.open1()
        # self.open2()
        # self.open3()
        self.open4()
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
        if self.param["4 1"] > self.param["4 2"]:
            self.interface_data_state = False
            self.textBrowser_3.append("页码参数设置有误，请重新输入")
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
            "搜索页数：" + text4 +
            "\r多选项目：" + str(self.param["5"])
            # "\r日期：" + self.param["6 1"] + " 至 " + self.param["6 2"]
        )

    def set_all(self):
        print("yangshi")
        self.thread = yangshi()
        self.thread.error_thread.connect(self.add_text)
        self.thread.result_thread.connect(self.show_table)
        self.thread.state_thread.connect(self.over_thread)
        self.thread.msg_thread.connect(self.show_msg)
        self.thread.img_thread.connect(self.show_img)

        self.pushButton_5.clicked.connect(self.thread.break_work)

        # 子窗口名字修改
        self.setWindowTitle("央视新闻爬虫")

        # 子窗口最大化
        # self.showMaximized()

        # box标题
        self.groupBox.setTitle("央视新闻")

        # 表格
        self.table_list = ["分类", "id", "图片2", "标题", "关键字", "图片1", "时间", "简要", "网址"]

        self.spinBox_5.setRange(1, 7)
        self.spinBox_6.setRange(1, 7)

        self.checkBox_12.setText("新闻")
        self.checkBox_13.setText("国内")
        self.checkBox_21.setText("国际")
        self.checkBox_22.setText("社会")
        self.checkBox_23.setText("法制")
        self.checkBox_31.setText("文娱")
        self.checkBox_32.setText("科技")
        self.checkBox_33.setText("生活")
        self.checkBox_41.setText("教育")

    def show_table(self, a):
        self.model.appendRow(
            [QStandardItem(str(a["type"])),
             QStandardItem(str(a["id"])),
             QStandardItem(str(a["image2"])),
             QStandardItem(str(a["title"])),
             QStandardItem(str(a["keywords"])),
             QStandardItem(str(a["image"])),
             QStandardItem(str(a["focus_date"])),
             QStandardItem(str(a["brief"])),
             QStandardItem(str(a["url"]))
             ]
        )
        self.tableView.scrollToBottom()

        self.sheet.write(self.book_row, 0, a["type"])
        self.sheet.write(self.book_row, 1, a["id"])
        self.sheet.write(self.book_row, 2, a["image2"])
        self.sheet.write(self.book_row, 3, a["title"])
        self.sheet.write(self.book_row, 4, a["keywords"])
        self.sheet.write(self.book_row, 5, a["image"])
        self.sheet.write(self.book_row, 6, a["focus_date"])
        self.sheet.write(self.book_row, 7, a["brief"])
        self.sheet.write(self.book_row, 8, a["url"])

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
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

        self.dicts = {
            "新闻": '"http://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/news_%s.jsonp?cb=t&cb=news" % i',
            "国内": '"http://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/china_%s.jsonp" % i',
            "国际": '"http://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/world_%s.jsonp?cb=t&cb=world" % i',
            "社会": '"http://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/society_%s.jsonp?cb=t&cb=society" % i',
            "法制": '"http://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/law_%s.jsonp?cb=t&cb=law" % i',
            "文娱": '"http://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/ent_%s.jsonp?cb=t&cb=ent" % i',
            "科技": '"http://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/tech_%s.jsonp?cb=t&cb=tech" % i',
            "生活": '"http://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/life_%s.jsonp?cb=t&cb=life" % i',
            "教育": '"http://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/edu_%s.jsonp?cb=t&cb=edu" % i'
        }

    def setidentity(self, dict):
        self.working = True
        self.identity = dict
        if self.identity["4 3"]:
            self.identity["4 1"] = 1
            self.identity["4 2"] = 7
        self.now = 0
        self.all = (int(self.identity["4 2"]) - int(self.identity["4 1"]) + 1) * len(self.identity["5"])
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
            response = requests.get(url, headers=self.headers, verify=False, timeout=2)
        except:
            try:
                response = requests.get(url, headers=self.headers, verify=False, timeout=2)
            except:
                try:
                    response = requests.get(url, headers=self.headers, verify=False, timeout=2)
                except:
                    i = 0
        if i == 1:
            response.encoding = response.apparent_encoding
            text = response.text
            return text
        else:
            return None

    def crawl(self, keyword, page1, page2):
        page1 = int(page1)
        page2 = int(page2)
        for i in range(page1, page2 + 1):
            if self.working:
                url = eval(self.dicts[keyword])
                self.show_text("正在爬取关键字: " + keyword + "      页码进度: " + str(i-page1+1) + " / " + str(page2-page1+1))
                self.show_msg("关键字: " + keyword + "  页码：" + str(i-page1+1))
                self.show_img(int(self.now/self.all*100))
                self.now = self.now+1
                text = self.get_text(url)
                if text:
                    a = re.findall(".*?\((.*)\)", text)[0]
                    try:
                        print(a)
                        a = eval(a)
                        for ii in a["data"]["list"]:
                            ii["type"] = str(keyword)
                            self.final_data(ii)
                    except:
                        self.show_text("关键字：" + str(keyword) + "出错，请求返回格式有误")
                else:
                    self.show_text("关键字：" + str(keyword) + "爬取出错，无法访问该网址")
            else:
                break

    def run(self):
        for i in range(len(self.identity["5"])):
            if self.working:
                self.show_text("正在爬取关键字: "+str(self.identity["5"][i])+"      关键字进度: "+str(i+1)+" / "+str(len(self.identity["5"])))
                # self.crawl(self.identity["key"][i], self.identity["page1"], self.identity["page2"])
                self.crawl(self.identity["5"][i], self.identity["4 1"], self.identity["4 2"])
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
    b = a()
    b.show()
    sys.exit(app.exec_())