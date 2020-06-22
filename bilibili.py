# -*- coding: utf-8 -*-

import sys
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from OGbilibili import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from lxml import etree
import xlwt
import xlrd
import random
import re
import os

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
#
    def initUI(self):
        #子窗口名字修改
        self.setWindowTitle("欢迎使用bilbibili关键字搜索爬取程序")
        #子窗口最大化
        self.showMaximized()
        self.textBrowser_3.append("欢迎使用bilbibili关键字搜索爬取程序，请设置爬虫参数\r")

#
        # 设置表格
        self.model = QStandardItemModel(0, 13)
        # 设置水平方向3个头标签文本内容
        self.model.setHorizontalHeaderLabels(
            ['关键字', '页码', '个数', 'av号', '视频网址', '视频时长', '投稿日期', '播放量', '弹幕数量', '视频分类', 'up昵称', '视频标题', '视频详情']
        )

        self.tableView = QtWidgets.QTableView(self.frame_2)
        self.tableView.setObjectName("tableView")
        self.tableView.setModel(self.model)
        self.horizontalLayout_3.addWidget(self.tableView)
#
#         #本程序不需要导入数据
#         self.pushButton_8.setEnabled(False)
#
#         #定义接口数据
        self.interface_data = []
        self.interface_data_state = True
        self.pushButton_1.clicked.connect(lambda: self.check_data())
#
        #更改swichbtn状态
        self.select_btn = 1
        self.select_btn_translate = "单一关键字测试"
        self.radioButton_1.setChecked(True)
        self.radioButton_1.clicked.connect(lambda: self.selectbtn(1))
        self.radioButton_2.clicked.connect(lambda: self.selectbtn(2))
#

        # 设置导入提示只读
        self.textBrowser.setReadOnly(True)


        #价格 页码可输入范围
        # self.spinBox_1.setRange(0, 99999999)
        # self.spinBox_2.setRange(0, 99999999)
        self.spinBox_3.setRange(1, 50)
        self.spinBox_4.setRange(1, 50)
#
#         #默认勾选  默认禁用价格选择
#         self.checkBox.setChecked(True)
#         self.spinBox_1.setEnabled(False)
#         self.spinBox_2.setEnabled(False)
#         self.checkBox.stateChanged.connect(self.change_checkbox)
#
        #创建导入导出文件位置
        self.in_address = ""
        self.out_address = ""
        self.pushButton_8.clicked.connect(self.getfile)
        self.pushButton_9.clicked.connect(self.savefile)

        self.pushButton_8.setEnabled(False)
        self.pushButton_9.setEnabled(True)
#
        #设置开始按钮
        self.pushButton_4.setEnabled(False)
        self.pushButton_4.clicked.connect(self.start_btn)

        #设置中止按钮
        self.pushButton_5.setEnabled(False)
        self.pushButton_5.clicked.connect(self.main_stop_thread)
#
        # 设置清空参数按钮

        # 设置清除结果窗口，提示窗口
        self.pushButton_2.clicked.connect(self.clean_frame_6)
        self.pushButton_3.clicked.connect(self.clean_textBrowser_3)

        #数据保存按钮，保存为excel
        self.pushButton_6.setEnabled(False)
        self.pushButton_6.clicked.connect(self.save_excel)
#
#
#
    #选择商品排序槽函数
    def selectbtn(self, i):
        self.select_btn = i

        if self.select_btn == 1:
            self.lineEdit_1.setEnabled(True)
            self.pushButton_8.setEnabled(False)

            self.pushButton_8.setText("点击选择")
            self.in_address = ""
            # self.out_address = ""
        else:
            self.lineEdit_1.setEnabled(False)
            self.pushButton_8.setEnabled(True)
            self.pushButton_8.setText("点击选择")
            # self.pushButton_9.setEnabled(True)

            self.lineEdit_1.setText("")

        #翻译按钮
        self.translate_radio(i)
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
    #导入文件按钮槽函数
    def getfile(self):
        a = QFileDialog.getOpenFileName(self, '请选择要打开的文件', 'c:\\', "Data files (*.xls)")
        self.pushButton_8.setText(a[0])
        self.in_address = a[0]

    #导出文件按钮槽函数
    def savefile(self):
        a = QFileDialog.getSaveFileName(self, '请选择要保存的位置', 'c:\\', "Data files (*.xls)")
        self.pushButton_9.setText(a[0])
        self.out_address = a[0]

    #状态选择翻译
    def translate_radio(self, i):
        a = {"1": "单一关键字测试", "2": "批量关键字爬取"}
        self.select_btn_translate = a[str(i)]
#
    #清空参数函数
    def clean_frame_6(self):
        self.lineEdit_1.setText(None)
        self.spinBox_3.setValue(1)
        self.spinBox_4.setValue(1)
        self.radioButton_1.click()
        self.in_address = ""
        self.out_address = ""
        self.pushButton_8.setText("点击选择")
        self.pushButton_9.setText("点击选择")
        self.textBrowser_3.append("已成功清除参数\r")
#
    #清除提示窗口函数
    def clean_textBrowser_3(self):
        self.textBrowser_3.clear()

    # 获取Excel内容函数
    def get_xls(self, address):
        workbook = xlrd.open_workbook(address)  # 打开xls文件
        # sheet_name = workbook.sheet_names()  # 打印所有sheet名称，是个列表
        # sheet1= workbook.sheet_by_name('Sheet1')  # 根据sheet名称读取sheet中的所有内容
        # print(sheet.name, sheet.nrows, sheet.ncols)
        sheet = workbook.sheet_by_index(0)  # 根据sheet索引读取sheet中的所有内容
        content = sheet.col_values(0)  # 第一列内容
        return content
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
            self.interface_data = [self.lineEdit_1.text(), self.select_btn, self.spinBox_3.text(), self.spinBox_4.text(), self.in_address, self.out_address]
            print(self.interface_data)
            if self.interface_data[1] == 1:
                if self.interface_data[0] == "":
                    self.textBrowser_3.append("搜索关键字不能为空\r")
                    self.interface_data_state = False
                if int(self.interface_data[2]) > int(self.interface_data[3]):
                    self.textBrowser_3.append("页码搜索区间有误\r")
                    self.interface_data_state = False
                if self.interface_data[5] == "":
                    self.textBrowser_3.append("请设置导出文件的位置\r")
                    self.interface_data_state = False

            else:
                if int(self.interface_data[2]) > int(self.interface_data[3]):
                    self.textBrowser_3.append("页码搜索区间有误\r")
                    self.interface_data_state = False

                if self.interface_data[4] == "":
                    self.textBrowser_3.append("请设置导入文件的位置\r")
                    self.interface_data_state = False

                if self.interface_data[5] == "":
                    self.textBrowser_3.append("请设置导出文件的位置\r")
                    self.interface_data_state = False

            self.textBrowser_1.setText(
                "关键字：" + self.interface_data[0] +
                "\r\r爬取规则：" + self.select_btn_translate +
                "\r\r爬取页码：" + self.interface_data[2] + " 到 " + self.interface_data[3] + " 页"
                "\r\r导入位置：" + self.interface_data[4] +
                "\r\r导出位置：" + self.interface_data[5]
            )

            if self.interface_data_state == True and self.interface_data[1] == 2:
                try:
                    a = self.get_xls(self.interface_data[4])
                    print(a)
                except:
                    self.textBrowser_3.append("文件格式有误请重新检查导入的文件\r")
                i = 1
                if len(a) <= 2:
                    self.textBrowser_3.append("导入的Excel文件无数据或数据量<2，请重新检查导入的文件\r")
                    self.interface_data_state = False
                else:
                    self.textBrowser_1.append("\rExcel导入信息预览：")
                    for x in a:
                        print(i, x)
                        self.textBrowser_1.append(str(i)+"  "+str(x))
                        if i > 19:
                            self.textBrowser_1.append("......")
                            break
                        i = i + 1
                    if len(a) < 20:
                        self.textBrowser_3.append("Excel文档第一张表第一列内容不足10条，请将需要查找的数据移动到第一列，如确认信息正确请继续...\r")

            #
            #
            # # self.textBrowser_1.setText(
            # #     "商品名称：" + self.interface_data[0] +
            # #     "\r\r搜索规则：" + self.select_btn_translate +
            # #     "\r\r价格区间：" + self.interface_data[2] + " 到 " + self.interface_data[3] + " 元" +
            # #     "\r\r搜索页数：" + self.interface_data[4] + " 到 " + self.interface_data[5] + " 页" +
            # #     "\r\r导入位置：" + self.interface_data[6] +
            # #     "\r\r导出位置：" + self.interface_data[7]
            # # )
            # #
            if self.interface_data_state:
                self.pushButton_4.setEnabled(True)
                self.pushButton_2.setEnabled(False)
                self.frame_6.setEnabled(False)
                self.pushButton_1.setText("取消")
                self.textBrowser_3.append("爬虫参数设置无误，准备开始\r")
            else:
                self.pushButton_4.setEnabled(False)
            #
            self.interface_data_state = True
#
    #开始按钮槽函数
    def start_btn(self):

        #准备创建Excel
        self.book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        self.sheet = self.book.add_sheet('Sheet1', cell_overwrite_ok=True)
        a = ['序号', '关键字', '页码', '个数', 'av号', '视频网址', '视频时长', '投稿日期', '播放量', '弹幕数量', '视频分类', 'up昵称', '视频标题', '视频详情']
        for i in range(len(a)):
            self.sheet.write(0, i, a[i])
        # 设置变量excel排数
        self.book_row = 1

        #清空表格
        self.model.clear()
        self.model.setHorizontalHeaderLabels(
            ['关键字', '页码', '个数', 'av号', '视频网址', '视频时长', '投稿日期', '播放量', '弹幕数量', '视频分类', 'up昵称', '视频标题', '视频详情']
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
            [QStandardItem(str(a["name"])),
             QStandardItem(str(a["page"])),
             QStandardItem(str(a["number"])),
             QStandardItem(str(a["av"])),
             QStandardItem(str(a["url"])),
             QStandardItem(str(a["still_time"])),
             QStandardItem(str(a["time"])),
             QStandardItem(str(a["watch"])),
             QStandardItem(str(a["bull"])),
             QStandardItem(str(a["video_type"])),
             QStandardItem(str(a["up_name"])),
             QStandardItem(str(a["title"])),
             QStandardItem(str(a["particular"]))
             ]
        )

        self.sheet.write(self.book_row, 0, self.book_row)
        self.sheet.write(self.book_row, 1, a["name"])
        self.sheet.write(self.book_row, 2, a["page"])
        self.sheet.write(self.book_row, 3, a["number"])
        self.sheet.write(self.book_row, 4, a["av"])
        self.sheet.write(self.book_row, 5, a["url"])
        self.sheet.write(self.book_row, 6, a["still_time"])
        self.sheet.write(self.book_row, 7, a["time"])
        self.sheet.write(self.book_row, 8, a["watch"])
        self.sheet.write(self.book_row, 9, a["bull"])
        self.sheet.write(self.book_row, 10, a["video_type"])
        self.sheet.write(self.book_row, 11, a["up_name"])
        self.sheet.write(self.book_row, 12, a["title"])
        self.sheet.write(self.book_row, 13, a["particular"])

        self.book_row = self.book_row + 1
#
#
#
    #显示报错
    def showerror(self, a):
        self.textBrowser_3.append(a)

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
    #确认保存为excel函数
    def save_excel(self):
        self.book.save(self.interface_data[5])
        self.textBrowser_3.append("已经成功保存到"+self.interface_data[5]+'\r')
        self.pushButton_6.setEnabled(False)


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

    def get_text(self, url):
        x = int(random.randint(0, 6))
        User_Agent = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)"
        ]
        headers = {
            'User-Agent': User_Agent[x]
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

    def get_name(self, name, page):
        url = "https://search.bilibili.com/video?keyword=%s&page=%s" % (name, page)
        response = self.get_text(url)
        html = etree.HTML(response)
        x = len(html.xpath('//li[@class="video-item matrix"]//span[@class="so-imgTag_rb"]//text()'))
        if x == 0:
            print(0)
            product = {
                "name": name,
                "page": page,
                'number': 0,
                "av": None,
                "url": None,
                "still_time": None,
                "time": None,
                "watch": None,
                "bull": None,
                "video_type": None,
                "up_name": None,
                "title": None,
                "particular": None
            }
            self.result_thread.emit(product)
            return 0
        else:
            for i in range(1, x + 1):
                a = html.xpath('//li[@class="video-item matrix"][%s]//span[@class="so-imgTag_rb"]//text()' % i)[0]
                b = html.xpath('//li[@class="video-item matrix"][%s]//span[@class="type hide"]//text()' % i)
                c = html.xpath('//li[@class="video-item matrix"][%s]//a/@title' % i)[0]
                # d = html.xpath('//li[@class="video-item matrix"][%s]//span[@class="type avid"]//text()' % i)[0][2:]
                e = html.xpath('//li[@class="video-item matrix"][%s]//a/@href' % i)[0][2:]
                f = html.xpath('//li[@class="video-item matrix"][%s]//div[@class="des hide"]//text()' % i)[0].replace(
                    " ", "")
                g = html.xpath('//li[@class="video-item matrix"][%s]//span[@class="so-icon watch-num"]//text()' % i)[
                    0].replace("\n", "").replace(" ", "")
                h = html.xpath('//li[@class="video-item matrix"][%s]//span[@class="so-icon hide"]//text()' % i)[
                    0].replace("\n", "").replace(" ", "")
                iiii = html.xpath('//li[@class="video-item matrix"][%s]//span[@class="so-icon time"]//text()' % i)[
                    0].replace("\n", "").replace(" ", "")
                j = html.xpath('//li[@class="video-item matrix"][%s]//a[@class="up-name"]//text()' % i)[0]

                if not b:
                    b = None
                else:
                    b = b[0]

                product = {
                    "name": name,
                    "page": page,
                    'number': i,
                    "av": re.findall(r'BV(.*?)\?', e, re.S)[0],
                    "url": e,
                    "still_time": a,
                    "time": iiii,
                    "watch": g,
                    "bull": h,
                    "video_type": b,
                    "up_name": j,
                    "title": c,
                    "particular": f
                }
                self.result_thread.emit(product)
            if x == 20:
                return 1
            else:
                return 0



    # def get_name(self, name):
    #     url = 'https://s.weibo.com/weibo/%23' + name + '%23'
    #     a = self.get_response(url, name)
    #     print(a)
    #     self.result_thread.emit(a)

    def get_xls(self, address):
        workbook = xlrd.open_workbook(address)  # 打开xls文件
        # sheet_name = workbook.sheet_names()  # 打印所有sheet名称，是个列表
        # sheet1= workbook.sheet_by_name('Sheet1')  # 根据sheet名称读取sheet中的所有内容
        # print(sheet.name, sheet.nrows, sheet.ncols)
        sheet = workbook.sheet_by_index(0)  # 根据sheet索引读取sheet中的所有内容
        content = sheet.col_values(0)  # 第一列内容
        return content


    def run(self):
        self.error_thread.emit("开始爬取,等耐心等待...\r")
        self.state_thread.emit(1)

        if self.identity[1] == 1:
            page1 = self.identity[2]
            page2 = self.identity[3]
            for i in range(int(page1), int(page2)+1):
                self.error_thread.emit("正在爬取第："+ str(i) +"页")
                state = self.get_name(self.identity[0], i)
                if state == 0 or self.working == False:
                    break
        else:
            x = self.get_xls(self.identity[4])
            for iname in x:
                if self.working == False:
                    break
                try:
                    page1 = self.identity[2]
                    page2 = self.identity[3]
                    for i in range(int(page1), int(page2) + 1):
                        self.error_thread.emit("正在爬取关键字：" + iname + "      第：" + str(i) + "页")
                        state = self.get_name(iname, i)
                        if state == 0 or self.working == False:
                            break
                except:
                    self.error_thread.emit("\r睿站已禁止你访问，请等待五分钟后再轰炸，整理未爬取的关键字，继续轰炸\r")
                    self.working = False
                    break
                time.sleep(2)

        if self.working:
            self.error_thread.emit("\r已完成爬取\r")
        else:
            self.error_thread.emit("\r已中止程序\r")
            self.working = True

        # for i in range(int(self.identity[4]), int(self.identity[5])+1):
        #     try:
        #         a = self.translate_list(self.identity)
        #         url = self.get_url(a, i)
        #         self.get_response(url, i)
        #         if self.working == False:
        #             break
        #     except:
        #         self.error_thread.emit("此页商品数目不足30条,无此价格区间商品，或超过筛选条件页数，请扩大筛选条件或减少搜索页数。\r")
        #         break
        #
        self.state_thread.emit(0)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = ChildWindow()
    form.show()
    sys.exit(app.exec_())