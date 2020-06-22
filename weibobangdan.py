# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from OGweibobangdan import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from lxml import etree
import xlwt
import re
import time

class ChildWindow(QMainWindow, Ui_MainWindow):
    close_singnal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ChildWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
#
        self.thread = MyThread()
        self.thread.result_thread.connect(self.showtable)
        self.thread.error_thread.connect(self.showerror)
        self.thread.state_thread.connect(self.not_click)
#
    def closeEvent(self, event):
        """
        对MainWindow的函数closeEvent进行重构
        退出软件时结束所有进程
        :param event:
        :return:
        """
        reply = QtWidgets.QMessageBox.question(self,
                                               '确认',
                                               "程序爬取的内容需要右下角手动保存!!\n是否确认退出？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            self.thread.stop_thread()
            self.close_singnal.emit("sayasora")
        else:
            event.ignore()
#
    def initUI(self):
        #子窗口名字修改
        self.setWindowTitle("欢迎使用微博榜单爬取程序")
        #子窗口最大化
        self.showMaximized()
        self.textBrowser_3.append("欢迎使用微博榜单爬取程序，请设置爬虫参数\r")

        # 设置表格
        self.model = QStandardItemModel(0, 6)
        # 设置水平方向十五个头标签文本内容
        self.model.setHorizontalHeaderLabels(
            ['分类', '页码', '标题', '阅读数', '主持人', '正文']
        )

        self.tableView = QtWidgets.QTableView(self.frame_2)
        self.tableView.setObjectName("tableView")
        self.tableView.setModel(self.model)
        self.horizontalLayout_3.addWidget(self.tableView)
#
#         #本程序不需要导入数据
#         self.pushButton_8.setEnabled(False)
#
        #定义接口数据
        self.interface_data = []
        self.interface_data_state = True
        self.pushButton_1.clicked.connect(lambda: self.check_data())
#
        #更改swichbtn状态
#         self.select_btn = 1
#         self.select_btn_translate = "综合默认"
        self.radioButton_39.setChecked(True)
#         self.radioButton_1.clicked.connect(lambda: self.selectbtn(1))
#         self.radioButton_2.clicked.connect(lambda: self.selectbtn(2))
#         self.radioButton_3.clicked.connect(lambda: self.selectbtn(3))
#         self.radioButton_4.clicked.connect(lambda: self.selectbtn(4))
#         self.radioButton_5.clicked.connect(lambda: self.selectbtn(5))
#         self.radioButton_6.clicked.connect(lambda: self.selectbtn(6))
#
#         #价格 页码可输入范围
#         self.spinBox_1.setRange(0, 99999999)
#         self.spinBox_2.setRange(0, 99999999)
#         self.spinBox_3.setRange(1, 100)
#         self.spinBox_4.setRange(1, 100)
#
#         #默认勾选  默认禁用价格选择
#         self.checkBox.setChecked(True)
#         self.spinBox_1.setEnabled(False)
#         self.spinBox_2.setEnabled(False)
#         self.checkBox.stateChanged.connect(self.change_checkbox)
#
        #创建导入导出文件位置
        # self.in_address = ""
        self.out_address = ""
        # self.pushButton_8.clicked.connect(self.getfile)
        self.pushButton_10.clicked.connect(self.savefile)
#
        #设置开始按钮
        self.pushButton_4.setEnabled(False)
        self.pushButton_4.clicked.connect(self.start_btn)

        #设置中止按钮
        self.pushButton_5.setEnabled(False)
        self.pushButton_5.clicked.connect(self.main_stop_thread)
#
        #设置清空参数按钮
        self.pushButton_2.clicked.connect(self.clean_frame_6)

        #设置清除结果窗口，提示窗口
        self.pushButton_3.clicked.connect(self.clean_textBrowser_3)
#
#         #数据保存按钮，保存为excel
#         self.pushButton_6.setEnabled(False)
#         self.pushButton_6.clicked.connect(self.save_excel)
#
#
#
#     #选择商品排序槽函数
#     def selectbtn(self, i):
#         self.select_btn = i
#         #翻译按钮
#         self.translate_radio(i)
#
#     #勾选是非限制价格槽函数
#     def change_checkbox(self):
#         if self.checkBox.isChecked():
#             self.spinBox_1.setEnabled(False)
#             self.spinBox_2.setEnabled(False)
#             self.spinBox_1.setValue(0)
#             self.spinBox_2.setValue(0)
#         else:
#             self.spinBox_1.setEnabled(True)
#             self.spinBox_2.setEnabled(True)
#
#     #导入文件按钮槽函数
#     def getfile(self):
#         a = QFileDialog.getOpenFileName(self, '请选择要打开的文件', 'c:\\', "Data files (*.xlsx *.xls *.csv)")
#         self.pushButton_8.setText(a[0])
#         self.in_address = a[0]
#
    #导出文件按钮槽函数
    def savefile(self):
        a = QFileDialog.getSaveFileName(self, '请选择要保存的位置', 'c:\\', "Data files (*.xls)")
        self.pushButton_10.setText(a[0])
        self.out_address = a[0]
#
#     #状态选择翻译
#     def translate_radio(self, i):
#         a = {"1": "默认排序", "2": "销量最高", "3": "价格升序", "4": "价格降序", "5": "评论数量", "6": "最新发布"}
#         self.select_btn_translate = a[str(i)]
#
    #清空参数函数
    def clean_frame_6(self):
        self.radioButton_39.click()
        self.pushButton_10.setText("点击选择")
        self.out_address = ''
        self.textBrowser_3.append("已成功清除参数\r")
#
    #清除提示窗口函数
    def clean_textBrowser_3(self):
        self.textBrowser_3.clear()
#
    #检查按钮对应槽函数
    def check_data(self):
        if self.pushButton_1.text() == "取消":
            self.frame_6.setEnabled(True)
            self.pushButton_1.setText("检查参数")
            self.pushButton_4.setEnabled(False)
            self.pushButton_2.setEnabled(True)
            self.textBrowser_3.append("请重新输入需要修改的参数\r")
        else:
            self.interface_data = [1, self.out_address]
            for i in range(53):
                try:
                    if eval("self.radioButton_" + str(i)).isChecked():
                        self.interface_data[0] = eval("self.radioButton_" + str(i)).text()
                except:
                    pass
            print(self.interface_data)
        #     if self.interface_data[0] == "":
        #         self.textBrowser_3.append("商品名称不能为空\r")
        #         self.interface_data_state = False
        #     if float(self.interface_data[2]) > float(self.interface_data[3]):
        #         self.textBrowser_3.append("商品价格搜索区间有误\r")
        #         self.interface_data_state = False
        #     if int(self.interface_data[4]) > int(self.interface_data[5]):
        #         self.textBrowser_3.append("商品页码搜索区间有误\r")
        #         self.interface_data_state = False
            if self.interface_data[1] == "":
                self.textBrowser_3.append("请设置导出文件的位置\r")
                self.interface_data_state = False
        #
            self.textBrowser_1.setText(
                "榜单类型：" + self.interface_data[0] +
                "\r\r导出位置：" + self.interface_data[1]
            )
        #
            if self.interface_data_state:
                self.pushButton_4.setEnabled(True)
                self.pushButton_2.setEnabled(False)
                self.frame_6.setEnabled(False)
                self.pushButton_1.setText("取消")
                self.textBrowser_3.append("爬虫参数设置无误，准备开始\r")
            else:
                self.pushButton_4.setEnabled(False)

            self.interface_data_state = True
#
    #开始按钮槽函数
    def start_btn(self):

        #准备创建Excel
        self.book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        self.sheet = self.book.add_sheet('Sheet1', cell_overwrite_ok=True)
        a = ['分类', '页码', '标题', '阅读数', '主持人', '正文']
        for i in range(6):
            self.sheet.write(0, i, a[i])
        # 设置变量excel排数
        self.book_row = 1

        #清空表格
        self.model.clear()
        self.model.setHorizontalHeaderLabels(
            ['分类', '页码', '标题', '阅读数', '主持人', '正文']
        )

        #开启另一个线程
        self.thread.setidentity(self.interface_data)
        self.thread.start()
#
    def main_stop_thread(self):
        self.textBrowser_3.append("正在中止程序，请稍等...\r")
        self.pushButton_5.setEnabled(False)
        self.thread.stop_thread()
#
#
    #显示表格函数
    def showtable(self, a):
        print(a)
        self.model.appendRow(
            [QStandardItem(str(self.interface_data[0])),
             QStandardItem(str(a["page"])),
             QStandardItem(str(a["tittle"])),
             QStandardItem(str(a["read"])),
             QStandardItem(str(a["man"])),
             QStandardItem(str(a["article"])),
             ]
        )
#
#         ['分类', '页码', '标题', '阅读数', '主持人', '正文']
        self.sheet.write(self.book_row, 0, self.interface_data[0])
        self.sheet.write(self.book_row, 1, a["page"])
        self.sheet.write(self.book_row, 2, a["tittle"])
        self.sheet.write(self.book_row, 3, a["read"])
        self.sheet.write(self.book_row, 4, a["man"])


        self.book_row = self.book_row + 1
#
#
#
    #显示报错
    def showerror(self, a):
        self.textBrowser_3.append(a)
#
    #子线程状态，按钮禁用
    def not_click(self, a):
        if a == 1:
            self.pushButton_1.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            self.pushButton_6.setEnabled(False)
            self.pushButton_5.setEnabled(True)
        else:
            self.pushButton_1.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            self.pushButton_6.setEnabled(True)
            self.pushButton_5.setEnabled(False)
#
#     #确认保存为excel函数
#     def save_excel(self):
#         self.book.save(self.interface_data[7])
#         self.textBrowser_3.append("已经成功保存到"+self.interface_data[7]+'\r')
#         self.pushButton_6.setEnabled(False)
#
#
#
#
class MyThread(QThread):

    #定义thread信号,传递结果字典
    result_thread = pyqtSignal(dict)
    error_thread = pyqtSignal(str)
    state_thread = pyqtSignal(int)

    def __init__(self, parent=None):
        super(MyThread, self).__init__(parent)

        self.identity = []
        self.working = True

    def stop_thread(self):
        self.working = False
#
    def setidentity(self, list):
        self.identity = list

    def translate_list(self, list):
        b = [None, None]

        # 商品分类参数
        fl = {
            "话题榜": "231650_ctg1_-_all", "新时代": "231650_ctg1_-_epoch", "社会": "231650_ctg1_-_1", "互联网": "231650_ctg1_-_138", "科普": "231650_ctg1_-_3", "数码": "231650_ctg1_-_131", "财经": "231650_ctg1_-_7", "创意征集": "231650_ctg1_-_9", "其他": "231650_ctg1_-_8",
            "明星": "231650_ctg1_-_2", "综艺": "231650_ctg1_-_102", "电视剧": "231650_ctg1_-_101", "电影": "231650_ctg1_-_100", "音乐": "231650_ctg1_-_146", "汽车": "231650_ctg1_-_117", "体育": "231650_ctg1_-_98", "运动健身": "231650_ctg1_-_111", "健康": "231650_ctg1_-_113",
            "军事": "231650_ctg1_-_144", "美图": "231650_ctg1_-_123", "情感": "231650_ctg1_-_5", "搞笑": "231650_ctg1_-_140", "游戏": "231650_ctg1_-_126", "旅游": "231650_ctg1_-_93", "育儿": "231650_ctg1_-_116", "教育": "231650_ctg1_-_133", "美食": "231650_ctg1_-_91",
            "公益": "231650_ctg1_-_6", "房产": "231650_ctg1_-_137", "星座": "231650_ctg1_-_145", "读书": "231650_ctg1_-_94", "艺术": "231650_ctg1_-_142", "时尚美妆": "231650_ctg1_-_114", "动漫": "231650_ctg1_-_97", "萌宠": "231650_ctg1_-_128", "生活记录": "231650_ctg1_-_120",
        }
        b[0] = fl[list[0]]

        b[1] = list[1]
        print(b)
        return b

    # def get_url(self, list, page):
    #
    #     if list[1] == "" and list[2] == "":
    #         m = ""
    #         n = ""
    #     elif list[1] == "" or list[2] == "":
    #         m = ""
    #         n = "/"
    #     else:
    #         m = "/"
    #         n = "/"
    #
    #     url = "https://" + list[0] + ".meituan.com/meishi/" + list[2] + m + list[1] + n + "pn" + str(page) + "/" + list[3]
    #     print(url)
    #     return self.get_text(url)

    def get_text(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Cookie': 'SINAGLOBAL=3793266496145.7417.1572276926339; SUB=_2AkMq65uef8NxqwJRmPoVxWziZYpyww7EieKct2pFJRMxHRl-yT83qkwitRB6AWu1ccs-BorJlPSLfWJoculiAcjnDxDe; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WW4aiGcon9_zL2Zwv737sZV; login_sid_t=25ce420bfe5c41d65820ee6f86f18b40; cross_origin_proto=SSL; _s_tentry=www.baidu.com; UOR=,,www.baidu.com; Apache=4629884696360.706.1572409313059; ULV=1572409313066:2:2:2:4629884696360.706.1572409313059:1572276926351; YF-Page-G0=70333fc8bc96e3a01b1d703feab3b41c|1572427744|1572427744'
        }
        try:
            response = requests.get(url=url, headers=headers)
            if response.encoding is None or response.encoding == 'ISO-8859-1':
                response.encoding = response.apparent_encoding
            html_txt = response.text
            if response.status_code != 200:
                return None
            return html_txt
        except Exception as e:
            print("error", str(e))

    def get_commemts_1(self, fl):
        # a = get_text("https://weibo.com/")
        # print(a)
        # text = get_text("https://s.weibo.com/top/summary?cate=realtimehot")
        # html = etree.HTML(text)
        # result_tittle = html.xpath('//td[@class="td-02"]/a/text()')
        # result_hot = html.xpath('//td[@class="td-02"]/span/text()')
        # print(result_tittle)
        # print(result_hot)
        #
        # text2 = get_text("https://s.weibo.com/top/summary?cate=socialevent")
        # html2 = etree.HTML(text2)
        # result_tittle2 = html2.xpath('//td[@class="td-02"]/a/text()')
        # print(result_tittle2)
        #
        # print(get_text("https://d.weibo.com/231650_ctg1_-_page_local_list#"))
        url = "https://d.weibo.com/%s?cfs=920&Pl_Discover_Pt6Rank__4_filter=&Pl_Discover_Pt6Rank__4_page=1#Pl_Discover_Pt6Rank__4" % fl
        print(url)
        text = self.get_text(url)
        all = re.findall(r'(alt=\\"#.*?)<li class=\\"pt_li S_', text, re.S)
        last = re.findall(r'DSC_topicon\\">15<\\/span>(.*?)<span>上一页<\\/span>', text, re.S)

        for x in all:
            tittle = re.findall(r'class=\\"S_txt1\\".*?#(.*?)#<\\/a>', x, re.S)
            article = re.findall(r'subtitle\\">\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t(.*?)\\t\\t', x, re.S)
            read = re.findall(r'number\\">(.*?)<\\/span>', x, re.S)
            from_the = re.findall(
                r'class=\\"tlink S_txt1\\"   >\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t(.*?)\\t\\n\\t\\t', x, re.S)
            n = {"page": "1", "tittle": str(tittle).strip("['']"), "article": str(article).strip("['']"),
                 "read": str(read).strip("['']"),
                 "man": str(from_the).strip("['']")}
            self.result_thread.emit(n)
        last = last[0]
        tittle = re.findall(r'class=\\"S_txt1\\".*?#(.*?)#<\\/a>', last, re.S)
        article = re.findall(r'subtitle\\">\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t(.*?)\\t\\t', last, re.S)
        read = re.findall(r'number\\">(.*?)<\\/span>', last, re.S)
        from_the = re.findall(
            r'class=\\"tlink S_txt1\\"   >\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t(.*?)\\t\\n\\t\\t', last, re.S)
        n = {"page": "1", "tittle": str(tittle).strip("['']"), "article": str(article).strip("['']"), "read": str(read).strip("['']"),
             "man": str(from_the).strip("['']")}
        self.result_thread.emit(n)
        time.sleep(3)

    def get_commemts_2(self, fl):
        # a = get_text("https://weibo.com/")
        # print(a)
        # text = get_text("https://s.weibo.com/top/summary?cate=realtimehot")
        # html = etree.HTML(text)
        # result_tittle = html.xpath('//td[@class="td-02"]/a/text()')
        # result_hot = html.xpath('//td[@class="td-02"]/span/text()')
        # print(result_tittle)
        # print(result_hot)
        #
        # text2 = get_text("https://s.weibo.com/top/summary?cate=socialevent")
        # html2 = etree.HTML(text2)
        # result_tittle2 = html2.xpath('//td[@class="td-02"]/a/text()')
        # print(result_tittle2)
        #
        # print(get_text("https://d.weibo.com/231650_ctg1_-_page_local_list#"))

        url = "https://d.weibo.com/%s?cfs=920&Pl_Discover_Pt6Rank__4_filter=&Pl_Discover_Pt6Rank__4_page=2#Pl_Discover_Pt6Rank__4" % fl
        print(url)
        text = self.get_text(url)
        all = re.findall(r'(alt=\\"#.*?)<li class=\\"pt_li S_', text, re.S)
        last = re.findall(r'DSC_topicon\\">30<\\/span>(.*?)<span>上一页<\\/span>', text, re.S)

        for x in all:
            tittle = re.findall(r'class=\\"S_txt1\\".*?#(.*?)#<\\/a>', x, re.S)
            article = re.findall(r'subtitle\\">\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t(.*?)\\t\\t', x, re.S)
            read = re.findall(r'number\\">(.*?)<\\/span>', x, re.S)
            from_the = re.findall(
                r'class=\\"tlink S_txt1\\"   >\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t(.*?)\\t\\n\\t\\t', x, re.S)
            n = {"page": "2", "tittle": str(tittle).strip("['']"), "article": str(article).strip("['']"),
                 "read": str(read).strip("['']"),
                 "man": str(from_the).strip("['']")}
            self.result_thread.emit(n)

        last = last[0]
        tittle = re.findall(r'class=\\"S_txt1\\".*?#(.*?)#<\\/a>', last, re.S)
        article = re.findall(r'subtitle\\">\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t(.*?)\\t\\t', last, re.S)
        read = re.findall(r'number\\">(.*?)<\\/span>', last, re.S)
        from_the = re.findall(
            r'class=\\"tlink S_txt1\\"   >\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t(.*?)\\t\\n\\t\\t', last, re.S)
        n = {"page": "2", "tittle": str(tittle).strip("['']"), "article": str(article).strip("['']"),
             "read": str(read).strip("['']"),
             "man": str(from_the).strip("['']")}
        self.result_thread.emit(n)
        time.sleep(3)

    def get_commemts_3(self, fl):
        # a = get_text("https://weibo.com/")
        # print(a)
        # text = get_text("https://s.weibo.com/top/summary?cate=realtimehot")
        # html = etree.HTML(text)
        # result_tittle = html.xpath('//td[@class="td-02"]/a/text()')
        # result_hot = html.xpath('//td[@class="td-02"]/span/text()')
        # print(result_tittle)
        # print(result_hot)
        #
        # text2 = get_text("https://s.weibo.com/top/summary?cate=socialevent")
        # html2 = etree.HTML(text2)
        # result_tittle2 = html2.xpath('//td[@class="td-02"]/a/text()')
        # print(result_tittle2)
        #
        # print(get_text("https://d.weibo.com/231650_ctg1_-_page_local_list#"))

        url = "https://d.weibo.com/%s?cfs=920&Pl_Discover_Pt6Rank__4_filter=&Pl_Discover_Pt6Rank__4_page=3#Pl_Discover_Pt6Rank__4" % fl
        print(url)
        text = self.get_text(url)
        all = re.findall(r'(alt=\\"#.*?)<li class=\\"pt_li S_', text, re.S)
        last = re.findall(r'DSC_topicon\\">45<\\/span>(.*?)<span>上一页<\\/span>', text, re.S)

        for x in all:
            tittle = re.findall(r'class=\\"S_txt1\\".*?#(.*?)#<\\/a>', x, re.S)
            article = re.findall(r'subtitle\\">\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t(.*?)\\t\\t', x, re.S)
            read = re.findall(r'number\\">(.*?)<\\/span>', x, re.S)
            from_the = re.findall(
                r'class=\\"tlink S_txt1\\"   >\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t(.*?)\\t\\n\\t\\t', x, re.S)
            n = {"page": "3", "tittle": str(tittle).strip("['']"), "article": str(article).strip("['']"),
                 "read": str(read).strip("['']"),
                 "man": str(from_the).strip("['']")}
            self.result_thread.emit(n)

        last = last[0]
        tittle = re.findall(r'class=\\"S_txt1\\".*?#(.*?)#<\\/a>', last, re.S)
        article = re.findall(r'subtitle\\">\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t(.*?)\\t\\t', last, re.S)
        read = re.findall(r'number\\">(.*?)<\\/span>', last, re.S)
        from_the = re.findall(
            r'class=\\"tlink S_txt1\\"   >\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t(.*?)\\t\\n\\t\\t', last, re.S)
        n = {"page": "3", "tittle": str(tittle).strip("['']"), "article": str(article).strip("['']"),
             "read": str(read).strip("['']"),
             "man": str(from_the).strip("['']")}
        self.result_thread.emit(n)
        time.sleep(1)

    def get_commemts_4(self, fl):
        # a = get_text("https://weibo.com/")
        # print(a)
        # text = get_text("https://s.weibo.com/top/summary?cate=realtimehot")
        # html = etree.HTML(text)
        # result_tittle = html.xpath('//td[@class="td-02"]/a/text()')
        # result_hot = html.xpath('//td[@class="td-02"]/span/text()')
        # print(result_tittle)
        # print(result_hot)
        #
        # text2 = get_text("https://s.weibo.com/top/summary?cate=socialevent")
        # html2 = etree.HTML(text2)
        # result_tittle2 = html2.xpath('//td[@class="td-02"]/a/text()')
        # print(result_tittle2)
        #
        # print(get_text("https://d.weibo.com/231650_ctg1_-_page_local_list#"))

        url = "https://d.weibo.com/%s?cfs=920&Pl_Discover_Pt6Rank__4_filter=&Pl_Discover_Pt6Rank__4_page=4#Pl_Discover_Pt6Rank__4" % fl
        print(url)
        text = self.get_text(url)
        all = re.findall(r'(alt=\\"#.*?)<li class=\\"pt_li S_', text, re.S)
        last = re.findall(r'DSC_topicon\\">60<\\/span>(.*?)<span>上一页<\\/span>', text, re.S)

        for x in all:
            tittle = re.findall(r'class=\\"S_txt1\\".*?#(.*?)#<\\/a>', x, re.S)
            article = re.findall(r'subtitle\\">\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t(.*?)\\t\\t', x, re.S)
            read = re.findall(r'number\\">(.*?)<\\/span>', x, re.S)
            from_the = re.findall(
                r'class=\\"tlink S_txt1\\"   >\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t(.*?)\\t\\n\\t\\t', x, re.S)
            n = {"page": "4", "tittle": str(tittle).strip("['']"), "article": str(article).strip("['']"),
                 "read": str(read).strip("['']"),
                 "man": str(from_the).strip("['']")}
            self.result_thread.emit(n)

        last = last[0]
        tittle = re.findall(r'class=\\"S_txt1\\".*?#(.*?)#<\\/a>', last, re.S)
        article = re.findall(r'subtitle\\">\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t(.*?)\\t\\t', last, re.S)
        read = re.findall(r'number\\">(.*?)<\\/span>', last, re.S)
        from_the = re.findall(
            r'class=\\"tlink S_txt1\\"   >\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t(.*?)\\t\\n\\t\\t', last, re.S)
        n = {"page": "4", "tittle": str(tittle).strip("['']"), "article": str(article).strip("['']"),
             "read": str(read).strip("['']"),
             "man": str(from_the).strip("['']")}
        self.result_thread.emit(n)



    def run(self):
        self.working = True
        print(self.translate_list(self.identity))
        self.error_thread.emit("开始爬取,等耐心等待...\r")
        self.state_thread.emit(1)

        try:
            a = self.translate_list(self.identity)
            self.get_commemts_1(a[0])
        except Exception as e:
            print(e)
            self.error_thread.emit("cookie已失效，请重新设置\r")

        try:
            if self.working == True:
                self.get_commemts_2(a[0])
                print(123123)
            if self.working == True:
                self.get_commemts_3(a[0])
            if self.working == True:
                self.get_commemts_4(a[0])
            self.error_thread.emit("已完成爬取\r")
        except:
            self.error_thread.emit("已完成爬取\r")

        self.state_thread.emit(0)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = ChildWindow()
    form.show()
    sys.exit(app.exec_())