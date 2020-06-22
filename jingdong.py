# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from OGjingdong import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from lxml import etree
import xlwt
import time

class ChildWindow(QMainWindow, Ui_MainWindow):
    close_singnal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ChildWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()

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



    def initUI(self):
        #子窗口名字修改
        self.setWindowTitle("欢迎使用京东网页的爬取程序")
        #子窗口最大化
        self.showMaximized()
        self.textBrowser_3.append("欢迎使用京东网页的爬取程序，请设置爬虫参数\r")

        # 设置表格
        self.model = QStandardItemModel(0, 15)
        # 设置水平方向十五个头标签文本内容
        self.model.setHorizontalHeaderLabels(
            ['页码', '个数', '编号', '标题', '价格', '评论数', '好评数', '好评率', '一般评价', '中评率', '差评数', '差评率', '追评数', '带视频评价数', '商品图片']
        )

        self.tableView = QtWidgets.QTableView(self.frame_2)
        self.tableView.setObjectName("tableView")
        self.tableView.setModel(self.model)
        self.horizontalLayout_3.addWidget(self.tableView)

        #本程序不需要导入数据
        self.pushButton_8.setEnabled(False)

        #定义接口数据
        self.interface_data = []
        self.interface_data_state = True
        self.pushButton_1.clicked.connect(lambda: self.check_data())

        #更改swichbtn状态
        self.select_btn = 1
        self.select_btn_translate = "综合默认"
        self.radioButton_1.setChecked(True)
        self.radioButton_1.clicked.connect(lambda: self.selectbtn(1))
        self.radioButton_2.clicked.connect(lambda: self.selectbtn(2))
        self.radioButton_3.clicked.connect(lambda: self.selectbtn(3))
        self.radioButton_4.clicked.connect(lambda: self.selectbtn(4))
        self.radioButton_5.clicked.connect(lambda: self.selectbtn(5))
        self.radioButton_6.clicked.connect(lambda: self.selectbtn(6))

        #价格 页码可输入范围
        self.spinBox_1.setRange(0, 99999999)
        self.spinBox_2.setRange(0, 99999999)
        self.spinBox_3.setRange(1, 100)
        self.spinBox_4.setRange(1, 100)

        #默认勾选  默认禁用价格选择
        self.checkBox.setChecked(True)
        self.spinBox_1.setEnabled(False)
        self.spinBox_2.setEnabled(False)
        self.checkBox.stateChanged.connect(self.change_checkbox)

        #创建导入导出文件位置
        self.in_address = ""
        self.out_address = ""
        self.pushButton_8.clicked.connect(self.getfile)
        self.pushButton_9.clicked.connect(self.savefile)

        #设置开始按钮
        self.pushButton_4.setEnabled(False)
        self.pushButton_4.clicked.connect(self.start_btn)

        #设置中止按钮
        self.pushButton_5.setEnabled(False)
        self.pushButton_5.clicked.connect(self.main_stop_thread)

        #设置清空参数按钮

        # #设置清除结果窗口，提示窗口
        self.pushButton_2.clicked.connect(self.clean_frame_6)
        self.pushButton_3.clicked.connect(self.clean_textBrowser_3)

        #数据保存按钮，保存为excel
        self.pushButton_6.setEnabled(False)
        self.pushButton_6.clicked.connect(self.save_excel)



    #选择商品排序槽函数
    def selectbtn(self, i):
        self.select_btn = i
        #翻译按钮
        self.translate_radio(i)

    #勾选是非限制价格槽函数
    def change_checkbox(self):
        if self.checkBox.isChecked():
            self.spinBox_1.setEnabled(False)
            self.spinBox_2.setEnabled(False)
            self.spinBox_1.setValue(0)
            self.spinBox_2.setValue(0)
        else:
            self.spinBox_1.setEnabled(True)
            self.spinBox_2.setEnabled(True)

    #导入文件按钮槽函数
    def getfile(self):
        a = QFileDialog.getOpenFileName(self, '请选择要打开的文件', 'c:\\', "Data files (*.xlsx *.xls *.csv)")
        self.pushButton_8.setText(a[0])
        self.in_address = a[0]

    #导出文件按钮槽函数
    def savefile(self):
        a = QFileDialog.getSaveFileName(self, '请选择要保存的位置', 'c:\\', "Data files (*.xls)")
        self.pushButton_9.setText(a[0])
        self.out_address = a[0]

    #状态选择翻译
    def translate_radio(self, i):
        a = {"1": "默认排序", "2": "销量最高", "3": "价格升序", "4": "价格降序", "5": "评论数量", "6": "最新发布"}
        self.select_btn_translate = a[str(i)]

    #清空参数函数
    def clean_frame_6(self):
        self.lineEdit_1.setText(None)
        self.radioButton_1.click()
        if self.checkBox.isChecked() == False:
            self.checkBox.click()
        self.spinBox_3.setValue(1)
        self.spinBox_4.setValue(1)
        self.pushButton_9.setText("点击选择")
        self.out_address = ''
        self.textBrowser_3.append("已成功清除参数\r")

    #清除提示窗口函数
    def clean_textBrowser_3(self):
        self.textBrowser_3.clear()

    #检查按钮对应槽函数
    def check_data(self):
        if self.pushButton_1.text() == "取消":
            self.frame_6.setEnabled(True)
            self.pushButton_1.setText("检查参数")
            self.pushButton_4.setEnabled(False)
            self.pushButton_2.setEnabled(True)
            self.textBrowser_3.append("请重新输入需要修改的参数\r")
        else:
            self.interface_data = [self.lineEdit_1.text(), self.select_btn, self.spinBox_1.text(), self.spinBox_2.text(), self.spinBox_3.text(), self.spinBox_4.text(), self.in_address, self.out_address]
            if self.interface_data[0] == "":
                self.textBrowser_3.append("商品名称不能为空\r")
                self.interface_data_state = False
            if float(self.interface_data[2]) > float(self.interface_data[3]):
                self.textBrowser_3.append("商品价格搜索区间有误\r")
                self.interface_data_state = False
            if int(self.interface_data[4]) > int(self.interface_data[5]):
                self.textBrowser_3.append("商品页码搜索区间有误\r")
                self.interface_data_state = False
            if self.interface_data[7] == "":
                self.textBrowser_3.append("请设置导出文件的位置\r")
                self.interface_data_state = False

            self.textBrowser_1.setText(
                "商品名称：" + self.interface_data[0] +
                "\r\r搜索规则：" + self.select_btn_translate +
                "\r\r价格区间：" + self.interface_data[2] + " 到 " + self.interface_data[3] + " 元" +
                "\r\r搜索页数：" + self.interface_data[4] + " 到 " + self.interface_data[5] + " 页" +
                "\r\r导入位置：" + self.interface_data[6] +
                "\r\r导出位置：" + self.interface_data[7]
            )

            if self.interface_data_state:
                self.pushButton_4.setEnabled(True)
                self.pushButton_2.setEnabled(False)
                self.frame_6.setEnabled(False)
                self.pushButton_1.setText("取消")
                self.textBrowser_3.append("爬虫参数设置无误，准备开始\r")
            else:
                self.pushButton_4.setEnabled(False)

            self.interface_data_state = True

    #开始按钮槽函数
    def start_btn(self):

        #准备创建Excel
        self.book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        self.sheet = self.book.add_sheet('Sheet1', cell_overwrite_ok=True)
        a = ['序号', '页码', '个数', '编号', '标题', '价格', '评论数', '好评数', '好评率', '一般评价', '中评率', '差评数', '差评率', '追评数', '带视频评价数', '商品图片']
        for i in range(16):
            self.sheet.write(0, i, a[i])
        # 设置变量excel排数
        self.book_row = 1

        #清空表格
        self.model.clear()
        self.model.setHorizontalHeaderLabels(
            ['页码', '个数', '编号', '标题', '价格', '评论数', '好评数', '好评率', '一般评价', '中评率', '差评数', '差评率', '追评数', '带视频评价数', '商品图片']
        )

        #开启另一个线程
        self.thread.setidentity(self.interface_data)
        self.thread.start()

    def main_stop_thread(self):
        self.textBrowser_3.append("正在中止程序，请稍等...\r")
        self.pushButton_5.setEnabled(False)
        self.thread.stop_thread()


    #显示表格函数
    def showtable(self, a):
        print(a)
        self.model.appendRow(
            [QStandardItem(str(a["page"])),
             QStandardItem(str(a["x"])),
             QStandardItem(a["number"]),
             QStandardItem(a["title"]),
             QStandardItem(a["price"]),
             QStandardItem(str(a["CommentCount"])),
             QStandardItem(str(a["GoodCount"])),
             QStandardItem(str(a["GoodRate"])),
             QStandardItem(str(a["GeneralCount"])),
             QStandardItem(str(a["GeneralRate"])),
             QStandardItem(str(a["PoorCount"])),
             QStandardItem(str(a["PoorRate"])),
             QStandardItem(str(a["AfterCount"])),
             QStandardItem(str(a["VideoCount"])),
             QStandardItem(a["img"])
             ]
        )

        self.sheet.write(self.book_row, 0, self.book_row)
        self.sheet.write(self.book_row, 1, a["page"])
        self.sheet.write(self.book_row, 2, a["x"])
        self.sheet.write(self.book_row, 3, a["number"])
        self.sheet.write(self.book_row, 4, a["title"])
        self.sheet.write(self.book_row, 5, a["price"])
        self.sheet.write(self.book_row, 6, a["CommentCount"])
        self.sheet.write(self.book_row, 7, a["GoodCount"])
        self.sheet.write(self.book_row, 8, a["GoodRate"])
        self.sheet.write(self.book_row, 9, a["GeneralCount"])
        self.sheet.write(self.book_row, 10, a["GeneralRate"])
        self.sheet.write(self.book_row, 11, a["PoorCount"])
        self.sheet.write(self.book_row, 12, a["PoorRate"])
        self.sheet.write(self.book_row, 13, a["AfterCount"])
        self.sheet.write(self.book_row, 14, a["VideoCount"])
        self.sheet.write(self.book_row, 15, a["img"])

        self.book_row = self.book_row + 1



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

    #确认保存为excel函数
    def save_excel(self):
        self.book.save(self.interface_data[7])
        self.textBrowser_3.append("已经成功保存到"+self.interface_data[7]+'\r')
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

    def setidentity(self, list):
        self.identity = list

    def get_text(self, url):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        }

        try:
            response = self.a(url=url, headers=headers)
            response.encoding = 'utf-8'
            return response.text
        except Exception as e:
            "出错 页码！！"
            response = self.a(url=url, headers=headers)
            response.encoding = 'utf-8'
            return response.text

    def translate_list(self, list):
        b = [None, None, None, None, None, None, None]

        # 商品分类参数
        c = [0, 3, 2, 1, 4, 5]
        b[1] = c[int(list[1] - 1)]

        if int(list[2]) == 0 and int(list[3]) == 0:
            b[2] = None
        else:
            b[2] = "exprice_" + list[2] + "-" + list[3]

        b[0] = list[0]
        b[3] = list[4]
        b[4] = list[5]
        b[6] = list[7]

        print(b)
        return b

    def get_url(self, list, page):
        url = "https://search.jd.com/search?"
        params = {
            "keyword": list[0],
            "enc": "utf-8",
            "qrst": "1",
            "rt": "1",
            "stop": "1",
            "vt": "2",
            "wq": list[0],
            "psort": list[1],
            "stock": "1",
            "page": int(page) * 2 - 1,
            "s": "61",
            "click": "0",
            "ev": list[2]
        }

        print(11)
        b = self.a1(url, params)
        b = b.url
        print(22)
        return b

    def a1(self, url, params):
        try:
            headers = {
                'Host': 'search.jd.com',
                'cache-control': 'max-age=0',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
                'sec-fetch-dest': 'document',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'referer': 'https://search.jd.com/search',
                'accept-language': 'zh-CN,zh;q=0.9',
            }
            b = requests.get(url=url, params=params, timeout=2, headers=headers, verify=False)
            return b
        except:
            print("a1出错")
            self.a1(url=url, params=params)

    def a(self, url, headers):
        try:
            b = requests.get(url, headers=headers, timeout=2, verify=False)
            return b
        except:
            time.sleep(1)
            print("adsfadfadfadfadfasdfasdf")
            self.a(url, headers)

    def get_commemts(self, a):
        url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds=%s' % a
        headers = {
            'Host': 'club.jd.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'sec-fetch-dest': 'document',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'accept-language': 'zh-CN,zh;q=0.9',
        }

        b = self.a(url, headers)
        while b == None:
            b = self.a(url, headers)
        c = eval(b.text)
        c = eval(str(c['CommentsCount']).strip('[]'))
        product = {
            'number': a,
            'CommentCount': c['CommentCount'],
            'GoodCount': c['GoodCount'],
            'GoodRate': c['GoodRate'],
            'GeneralCount': c['GeneralCount'],
            'GeneralRate': c['GeneralRate'],
            'PoorCount': c['PoorCount'],
            'PoorRate': c['PoorRate'],
            'AfterCount': c['AfterCount'],
            'VideoCount': c['VideoCount']
        }
        return product

    def get_response(self, url, page):
        text = self.get_text(url)
        if '<div class="nf-content">' in text:
            return 0
        else:
            html = etree.HTML(str(text))
            result1 = html.xpath('//li[@class="gl-item"]//div[@class="p-price"]//i/text()')
            result2 = html.xpath('//li[@class="gl-item"]//div[@class="p-img"]/a/@title')
            # result3 = html.xpath('//li[@class="gl-item"]//div[@class="p-commit"]/strong/a/@onclick')
            result4 = html.xpath("//div[@class='p-img']/a/img/@src")
            result5 = html.xpath('//li[@class="gl-item"]/@data-sku')

            for x in range(len(result1)):
                d = {
                    'page': page,
                    'x': x+1,
                    'number': result5[x],
                    'title': result2[x],
                    'price': result1[x],
                    'img': result4[x]
                }
                d.update(self.get_commemts(d['number']))
                self.result_thread.emit(d)

    def run(self):
        self.error_thread.emit("开始爬取,等耐心等待...\r")
        self.state_thread.emit(1)


        for i in range(int(self.identity[4]), int(self.identity[5])+1):
            # try:
            print(self.identity)
            self.error_thread.emit("共需" + str(self.identity[5]) + "页，正在爬取第 " + str(i) + " 页")
            a = self.translate_list(self.identity)
            url = self.get_url(a, i)
            if self.get_response(url, i) == 0:
                print(123123)
                self.error_thread.emit("此页商品数目不足30条,无此价格区间商品，或超过筛选条件页数，请扩大筛选条件或减少搜索页数，或ip已被屏蔽。\r")
                break
            if self.working == False:
                break
            # except Exception as e:
            #     self.error_thread.emit("此页商品数目不足30条,无此价格区间商品，或超过筛选条件页数，请扩大筛选条件或减少搜索页数，或ip已被屏蔽。\r")
            #     print(e)
            #     break

        if self.working:
            self.error_thread.emit("\r已完成爬取\r")
        else:
            self.error_thread.emit("\r已中止程序\r")
            self.working = True

        self.state_thread.emit(0)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = ChildWindow()
    form.show()
    sys.exit(app.exec_())