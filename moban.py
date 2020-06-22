# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from OGmoban import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import xlwt
import xlrd

class ChildWindow(QMainWindow, Ui_MainWindow):
    close_singnal = pyqtSignal(str)
    def __init__(self, parent=None):
        super(ChildWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()

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
            self.thread.break_work()
            self.close_singnal.emit("sayasora")
        else:
            event.ignore()

    def initUI(self):
        self.set_all()

        # 开始按钮禁用
        self.pushButton_4.setEnabled(False)
        # 导出按钮禁用
        self.pushButton_6.setEnabled(False)
        # 中止按钮禁用
        self.pushButton_5.setEnabled(False)

        self.in_address = []

        self.open_chose()

        self.set_table()

        # 三个逻辑按钮
        self.checkBox_4.stateChanged.connect(self.change_box3)
        self.checkBox_3.stateChanged.connect(self.change_box4)
        self.radioButton.toggled.connect(self.change_box5)

        # 导入按钮连接
        self.pushButton_8.clicked.connect(self.get_file)

        # 开始 检查 清空连接函数
        self.pushButton_1.clicked.connect(self.check_data)
        self.pushButton_2.clicked.connect(self.clean_param)
        self.pushButton_3.clicked.connect(self.clean_text)
        self.pushButton_4.clicked.connect(self.run_thread)
        self.pushButton_6.clicked.connect(self.out_file)

        self.clean_param()


    def open1(self):
        # 第1行
        self.lineEdit.setMaxLength(20)
        self.label_1.setEnabled(True)
        self.lineEdit.setEnabled(True)
        self.comboBox.setEnabled(True)

    def open2(self):
        # 第2行
        self.label_2.setEnabled(True)
        self.comboBox_2.setEnabled(True)
        self.comboBox_3.setEnabled(True)
        self.comboBox_4.setEnabled(True)

    def open3(self):
        # 第3行
        self.label_3.setEnabled(True)
        self.label_31.setEnabled(True)
        self.doubleSpinBox_3.setEnabled(True)
        self.doubleSpinBox_4.setEnabled(True)
        self.checkBox_4.setEnabled(True)

    def open4(self):
        # 第4行
        self.label_4.setEnabled(True)
        self.label_41.setEnabled(True)
        self.spinBox_5.setEnabled(True)
        self.spinBox_6.setEnabled(True)
        self.checkBox_3.setEnabled(True)

    def open5(self):
        # 第5行
        self.label_5.setEnabled(True)
        self.radioButton.setEnabled(True)
        self.checkBox_12.setEnabled(True)
        self.checkBox_13.setEnabled(True)
        self.checkBox_21.setEnabled(True)
        self.checkBox_22.setEnabled(True)
        self.checkBox_23.setEnabled(True)
        self.checkBox_31.setEnabled(True)
        self.checkBox_32.setEnabled(True)
        self.checkBox_33.setEnabled(True)
        self.checkBox_31.setEnabled(True)
        self.checkBox_32.setEnabled(True)
        self.checkBox_33.setEnabled(True)
        self.checkBox_41.setEnabled(True)
        self.checkBox_42.setEnabled(True)
        self.checkBox_43.setEnabled(True)
        self.checkBox_51.setEnabled(True)
        self.checkBox_52.setEnabled(True)
        self.checkBox_53.setEnabled(True)

    def open6(self):
        # 第6行
        self.label_6.setEnabled(True)
        self.label_61.setEnabled(True)
        self.dateEdit.setEnabled(True)
        self.dateEdit_2.setEnabled(True)

    def open7(self):
        # 第7行
        self.label_7.setEnabled(True)
        self.pushButton_8.setEnabled(True)
        self.pushButton_8.setMaximumWidth(300)

    def open8(self):
        # 第8行
        self.label.setEnabled(True)
        self.label_21.setEnabled(True)
        self.spinBox_9.setEnabled(True)
        self.label_22.setEnabled(True)
        self.spinBox_10.setEnabled(True)
        self.label_23.setEnabled(True)
        self.checkBox_6.setEnabled(True)

    def close8(self):
        # 第8行
        self.label.setEnabled(False)
        self.label_21.setEnabled(False)
        self.spinBox_9.setEnabled(False)
        self.label_22.setEnabled(False)
        self.spinBox_10.setEnabled(False)
        self.label_23.setEnabled(False)
        self.checkBox_6.setEnabled(False)

    # 第三行逻辑可选按钮
    def change_box3(self):
        if self.checkBox_4.isChecked():
            self.doubleSpinBox_3.setValue(0.00)
            self.doubleSpinBox_4.setValue(0.00)
            self.doubleSpinBox_3.setEnabled(False)
            self.doubleSpinBox_4.setEnabled(False)
        else:
            self.doubleSpinBox_3.setEnabled(True)
            self.doubleSpinBox_4.setEnabled(True)

    # 第四行逻辑可选按钮
    def change_box4(self):
        if self.checkBox_3.isChecked():
            self.spinBox_5.setValue(0)
            self.spinBox_6.setValue(0)
            self.spinBox_5.setEnabled(False)
            self.spinBox_6.setEnabled(False)
        else:
            self.spinBox_5.setEnabled(True)
            self.spinBox_6.setEnabled(True)

    # 第五行逻辑可选按钮
    def change_box5(self):
        if self.radioButton.isChecked():
            self.checkBox_12.setChecked(True)
            self.checkBox_13.setChecked(True)
            self.checkBox_21.setChecked(True)
            self.checkBox_22.setChecked(True)
            self.checkBox_23.setChecked(True)
            self.checkBox_31.setChecked(True)
            self.checkBox_32.setChecked(True)
            self.checkBox_33.setChecked(True)
            self.checkBox_31.setChecked(True)
            self.checkBox_32.setChecked(True)
            self.checkBox_33.setChecked(True)
            self.checkBox_41.setChecked(True)
            self.checkBox_42.setChecked(True)
            self.checkBox_43.setChecked(True)
            self.checkBox_51.setChecked(True)
            self.checkBox_52.setChecked(True)
            self.checkBox_53.setChecked(True)

            self.checkBox_12.setEnabled(False)
            self.checkBox_13.setEnabled(False)
            self.checkBox_21.setEnabled(False)
            self.checkBox_22.setEnabled(False)
            self.checkBox_23.setEnabled(False)
            self.checkBox_31.setEnabled(False)
            self.checkBox_32.setEnabled(False)
            self.checkBox_33.setEnabled(False)
            self.checkBox_31.setEnabled(False)
            self.checkBox_32.setEnabled(False)
            self.checkBox_33.setEnabled(False)
            self.checkBox_41.setEnabled(False)
            self.checkBox_42.setEnabled(False)
            self.checkBox_43.setEnabled(False)
            self.checkBox_51.setEnabled(False)
            self.checkBox_52.setEnabled(False)
            self.checkBox_53.setEnabled(False)
        else:
            self.checkBox_12.setChecked(False)
            self.checkBox_13.setChecked(False)
            self.checkBox_21.setChecked(False)
            self.checkBox_22.setChecked(False)
            self.checkBox_23.setChecked(False)
            self.checkBox_31.setChecked(False)
            self.checkBox_32.setChecked(False)
            self.checkBox_33.setChecked(False)
            self.checkBox_31.setChecked(False)
            self.checkBox_32.setChecked(False)
            self.checkBox_33.setChecked(False)
            self.checkBox_41.setChecked(False)
            self.checkBox_42.setChecked(False)
            self.checkBox_43.setChecked(False)
            self.checkBox_51.setChecked(False)
            self.checkBox_52.setChecked(False)
            self.checkBox_53.setChecked(False)

            self.checkBox_12.setEnabled(True)
            self.checkBox_13.setEnabled(True)
            self.checkBox_21.setEnabled(True)
            self.checkBox_22.setEnabled(True)
            self.checkBox_23.setEnabled(True)
            self.checkBox_31.setEnabled(True)
            self.checkBox_32.setEnabled(True)
            self.checkBox_33.setEnabled(True)
            self.checkBox_31.setEnabled(True)
            self.checkBox_32.setEnabled(True)
            self.checkBox_33.setEnabled(True)
            self.checkBox_41.setEnabled(True)
            self.checkBox_42.setEnabled(True)
            self.checkBox_43.setEnabled(True)
            self.checkBox_51.setEnabled(True)
            self.checkBox_52.setEnabled(True)
            self.checkBox_53.setEnabled(True)

    # 导入按钮函数
    def get_file(self):
        a = QFileDialog.getOpenFileName(self, '请选择要打开的文件', 'c:\\', "Data files (*.xls)")
        self.pushButton_8.setText(a[0])
        self.in_address = a[0]
        if a[0]:
            self.open8()
        else:
            self.pushButton_8.setText("点击选择")
            self.close8()

    # 清空参数按钮
    def clean_param(self):
        self.lineEdit.setText("")
        self.comboBox.setCurrentIndex(0)
        self.comboBox_2.setCurrentIndex(0)
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.checkBox_4.setChecked(True)
        self.checkBox_3.setChecked(True)
        self.radioButton.setChecked(True)
        self.dateEdit.setMinimumDate(QDate(int(2000), int(1), int(1)))
        self.dateEdit_2.setMinimumDate(QDate(int(2000), int(1), int(1)))
        self.pushButton_8.setText("点击选择")
        self.spinBox_9.setValue(0)
        self.spinBox_10.setValue(0)
        self.checkBox_6.setChecked(False)
        self.close8()


    # 请空提示窗口
    def clean_text(self):
        self.textBrowser_3.clear()

    # 添加提示窗口
    def add_text(self, text):
        self.textBrowser_3.append(str(text))

    # 状态栏显示信息
    def show_msg(self, text):
        self.label_16.setText(text)

    # 电池栏
    def show_img(self, text):
        self.progressBar_3.setValue(int(text))

    # 检查按钮对应槽函数
    def check_data(self):
        if self.pushButton_1.text() == "取消":
            self.frame_6.setEnabled(True)
            self.pushButton_1.setText("检查参数")
            self.pushButton_4.setEnabled(False)
            self.pushButton_2.setEnabled(True)
            self.label_13.setText("准备参数中")
            self.textBrowser_3.append("请重新输入需要修改的参数")
        else:
            self.textBrowser_3.append("开始检查参数，请等待...")
            #刷新界面
            QApplication.processEvents()
            self.param = {"1 1": self.lineEdit.text(), "1 2": self.comboBox.currentText(),
                          "2 1": self.comboBox_2.currentText(), "2 2": self.comboBox_3.currentText(),
                          "2 3": self.comboBox_4.currentText(),
                          "3 1": self.doubleSpinBox_3.text(), "3 2": self.doubleSpinBox_4.text(),
                          "3 3": self.checkBox_4.isChecked(),
                          "4 1": self.spinBox_5.text(), "4 2": self.spinBox_6.text(),
                          "4 3": self.checkBox_3.isChecked(),
                          "6 1": self.dateEdit.text(), "6 2": self.dateEdit_2.text(),
                          '8 1': self.spinBox_9.text(), "8 2": self.spinBox_10.text(),
                          }
            lists = []
            for i in [self.checkBox_12, self.checkBox_13, self.checkBox_21, self.checkBox_22, self.checkBox_23,
                      self.checkBox_31, self.checkBox_32, self.checkBox_33, self.checkBox_41, self.checkBox_42,
                      self.checkBox_43, self.checkBox_51, self.checkBox_52, self.checkBox_53]:
                if i.isChecked() and (i.text() != "checkbox") and (i.text() != "Checkbox"):
                    lists.append(i.text())
            self.param["5"] = lists

            self.show_param()
            self.find_error()

            if self.in_address:
                self.check_file(self.in_address, self.spinBox_9.text(), self.spinBox_10.text(), self.checkBox_6.isChecked())

            if self.interface_data_state:
                self.pushButton_4.setEnabled(True)
                self.pushButton_2.setEnabled(False)
                self.frame_6.setEnabled(False)
                self.label_13.setText("准备开始爬取")
                self.pushButton_1.setText("取消")
                self.textBrowser_3.append("爬虫参数设置无误，准备开始")

    # 检查导入文件
    def check_file(self, x: str, a: int, b: int, c: bool):
        if c:
            d = 0
        else:
            d = 1
        try:
            workbook = xlrd.open_workbook(x)  # 打开xls文件
            try:
                sheet = workbook.sheet_by_index(int(a) - 1)  # 根据sheet索引读取sheet中的所有内容
                try:
                    content = sheet.col_values(int(b) - 1)  # 第一列内容
                    if len(content) < 2:
                        self.interface_data_state = False
                        self.textBrowser_1.append("数据量为："+str(len(content))+"请重新检查文件参数")
                        self.textBrowser_3.append("数据量为："+str(len(content))+"请重新检查文件参数")
                    elif len(content) < 10:
                        self.textBrowser_1.append("请注意！数据量为：" + str(len(content)))
                        self.textBrowser_1.append("文件数据预览：" + str(content[d:len(content)]))
                        self.textBrowser_3.append("爬虫参数设置无误，准备开始")
                        self.data = content[d:]
                    else:
                        self.textBrowser_1.append("数据量为：" + str(len(content)))
                        self.textBrowser_1.append("文件数据预览：" + str(content[d:10]))
                        self.data = content[d:]
                except:
                    self.interface_data_state = False
                    self.textBrowser_1.append("数据位置中，列范围出错")
                    self.textBrowser_3.append("数据位置中，列范围出错")
            except:
                self.interface_data_state = False
                self.textBrowser_1.append("数据位置中，表格范围出错")
                self.textBrowser_3.append("数据位置中，表格范围出错")
        except:
            self.interface_data_state = False
            self.textBrowser_1.append("文件有误，无法打开此文件")
            self.textBrowser_3.append("文件有误，无法打开此文件")
        # sheet_name = workbook.sheet_names()  # 打印所有sheet名称，是个列表
        # sheet1= workbook.sheet_by_name('Sheet1')  # 根据sheet名称读取sheet中的所有内容

    def set_table(self):
        # 设置表格
        self.model = QStandardItemModel(0, len(self.table_list))
        # 设置水平方向3个头标签文本内容
        self.model.setHorizontalHeaderLabels(self.table_list)

        self.tableView = QtWidgets.QTableView(self.frame_2)
        self.tableView.setObjectName("tableView")
        self.tableView.setModel(self.model)
        self.horizontalLayout_3.addWidget(self.tableView)

    def run_thread(self):
        print(self.param)
        # 清空表格
        self.model.clear()
        self.model.setHorizontalHeaderLabels(self.table_list)

        # 设置excel
        self.book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        self.sheet = self.book.add_sheet('Sheet1', cell_overwrite_ok=True)
        for i in range(len(self.table_list)):
            self.sheet.write(0, i, self.table_list[i])
        # 设置变量excel排数
        self.book_row = 1

        self.pushButton_1.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_6.setEnabled(False)
        self.pushButton_5.setEnabled(True)
        self.label_13.setText("爬取中")

        self.thread.setidentity(self.param)
        self.thread.start()

    def out_file(self):
        a = QFileDialog.getSaveFileName(self, '请选择要保存的位置', 'c:\\', "Data files (*.xls)")
        out_address = a[0]
        if a[0]:
            self.book.save(out_address)
            self.textBrowser_3.append("已经成功保存到" + out_address)
            self.pushButton_6.setEnabled(False)
        else:
            self.textBrowser_3.append("已取消导出操作")

    def over_thread(self):
        self.pushButton_1.setEnabled(True)
        self.pushButton_4.setEnabled(True)
        self.pushButton_6.setEnabled(True)
        self.pushButton_5.setEnabled(False)
        self.label_13.setText("爬取完成")
        self.pushButton_6.setEnabled(True)

    # 选择开启的功能
    def open_chose(self):
        pass
        # self.open1()
        # self.open2()
        # self.open3()
        # self.open4()
        # self.open5()
        # self.open6()
        # self.open7()

    # 检查参数是否正确
    def find_error(self):
        pass
        # self.interface_data_state = True
        # if not self.param["1 1"]:
        #     self.interface_data_state = False
        # if not self.in_address:
        #     self.interface_data_state = False
        # if self.param["4 1"] > self.param["4 2"]:
        #     self.interface_data_state = False
        #     self.textBrowser_3.append("页码参数设置有误，请重新输入")
        # if self.param["5"] == []:
        #     self.interface_data_state = False
        #     self.textBrowser_3.append("请至少勾选一个项目")

    # 显示参数列表
    def show_param(self):
        pass
        # if self.param["3 3"]:
        #     text3 = "全部"
        # else:
        #     text3 = self.param["3 1"] + " 到 " + self.param["3 2"]
        # if self.param["4 3"]:
        #     text4 = "全部"
        # else:
        #     text4 = self.param["4 1"] + " 到 " + self.param["4 2"]
        # self.textBrowser_1.setText(
        #     # "关键字：" + self.param["1 1"] +
        #     # "\r关键字：" + self.param["1 2"] +
        #     # "\r搜索规则：" + self.param["2 1"] + " " + self.param["2 2"] + " " + self.param["2 3"] +
        #     # "\r价格区间：" + text3 +
        #     "搜索页数：" + text4 +
        #     "\r多选项目：" + str(self.param["5"])
        #     # "\r日期：" + self.param["6 1"] + " 至 " + self.param["6 2"]
        # )

    def set_all(self):
        pass
        # self.thread = yangshi()
        # self.thread.error_thread.connect(self.add_text)
        # self.thread.result_thread.connect(self.show_table)
        # self.thread.state_thread.connect(self.over_thread)
        # self.thread.msg_thread.connect(self.show_msg)
        # self.thread.img_thread.connect(self.show_img)
        #
        # self.pushButton_5.clicked.connect(self.thread.break_work)
        #
        #
        # #子窗口名字修改
        # self.setWindowTitle("央视新闻爬虫")
        #
        # # 子窗口最大化
        # # self.showMaximized()
        #
        # # box标题
        # self.groupBox.setTitle("央视新闻")
        #
        # # 表格
        # self.table_list = ["分类", "id", "图片2", "标题", "关键字", "图片1", "时间", "简要", "网址"]
        #
        # self.spinBox_5.setRange(1, 7)
        # self.spinBox_6.setRange(1, 7)
        #
        # self.checkBox_12.setText("新闻")
        # self.checkBox_13.setText("国内")
        # self.checkBox_21.setText("国际")
        # self.checkBox_22.setText("社会")
        # self.checkBox_23.setText("法制")
        # self.checkBox_31.setText("文娱")
        # self.checkBox_32.setText("科技")
        # self.checkBox_33.setText("生活")
        # self.checkBox_41.setText("教育")

    def show_table(self, a):
        pass
        # self.model.appendRow(
        #     [QStandardItem(str(a["type"])),
        #      QStandardItem(str(a["id"])),
        #      QStandardItem(str(a["image2"])),
        #      QStandardItem(str(a["title"])),
        #      QStandardItem(str(a["keywords"])),
        #      QStandardItem(str(a["image"])),
        #      QStandardItem(str(a["focus_date"])),
        #      QStandardItem(str(a["brief"])),
        #      QStandardItem(str(a["url"]))
        #      ]
        # )
        # self.tableView.scrollToBottom()
        #
        # self.sheet.write(self.book_row, 0, a["type"])
        # self.sheet.write(self.book_row, 1, a["id"])
        # self.sheet.write(self.book_row, 2, a["image2"])
        # self.sheet.write(self.book_row, 3, a["title"])
        # self.sheet.write(self.book_row, 4, a["keywords"])
        # self.sheet.write(self.book_row, 5, a["image"])
        # self.sheet.write(self.book_row, 6, a["focus_date"])
        # self.sheet.write(self.book_row, 7, a["brief"])
        # self.sheet.write(self.book_row, 8, a["url"])
        #
        # self.book_row = self.book_row + 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = ChildWindow()
    form.show()
    sys.exit(app.exec_())