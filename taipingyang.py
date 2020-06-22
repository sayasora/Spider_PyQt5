# -*- coding: utf-8 -*-

import sys
import re
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from OGtaipingyang import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from lxml import etree
import xlwt

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
        self.dict_level_l1 = {"不限": "/", "轿车(全部)": "/price/q-k9999.html", "SUV(全部)": "/price/q-k75.html",
                              "MPV": "/price/q-k74.html", "跑车": "/price/q-k111.html", "商用车(全部)": "/price/q-k112.html"}
        self.dict_level_l2 = {"不限": {"不限": "/price/q-k0.html"},
                              "轿车(全部)": {"不限": "/price/q-k9999.html", '微型车': '/price/q-k76.html', '小型车': '/price/q-k110.html',
                                         '紧凑型车': '/price/q-k73.html', '中型车': '/price/q-k72.html',
                                         '中大型车': '/price/q-k71.html', '大型车': '/price/q-k70.html'},
                              "SUV(全部)": {"不限": "/price/q-k75.html", '小型SUV': '/price/q-k131.html', '紧凑型SUV': '/price/q-k132.html',
                                          '中型SUV': '/price/q-k133.html', '中大型SUV': '/price/q-k134.html',
                                          '大型SUV': '/price/q-k135.html'},
                              "MPV": {"不限": "/price/q-k74.html"},
                              "跑车": {"不限": "/price/q-k111.html"},
                              "商用车(全部)": {"不限": "/price/q-k112.html", '微面': '/price/q-k77.html', '微卡': '/price/q-k93.html',
                                          '轻客': '/price/q-k105.html',
                                          '皮卡': '/price/q-k94.html'}}
        self.dict_brand = {
            '不限': {'不限': '/price/q-d0.html', '大众': '/price/q-d2.html', '丰田': '/price/q-d10.html', '福特': '/price/q-d21.html',
                   '现代': '/price/q-d34.html', '本田': '/price/q-d3.html', '日产': '/price/q-d15.html',
                   '别克': '/price/q-d7.html', '奥迪': '/price/q-d1.html', '宝马': '/price/q-d20.html',
                   '奔驰': '/price/q-d4.html', '雪佛兰': '/price/q-d225.html', '起亚': '/price/q-d12.html',
                   '标致': '/price/q-d41.html', '长安汽车': '/price/q-d124.html', '哈弗': '/price/q-d845.html',
                   '比亚迪': '/price/q-d107.html', 'Jeep': '/price/q-d38.html', '马自达': '/price/q-d17.html'},
            'A': {'奥迪': '/price/q-d1.html', '阿斯顿·马丁': '/price/q-d62.html', '阿尔法·罗密欧': '/price/q-d60.html',
                  'AC Schnitzer': 'javascript:void(0)', 'ALPINA': '/price/q-d7230.html', '爱驰': '/price/q-d7541.html',
                  '艾康尼克': 'javascript:void(0)'},
            'B': {'本田': '/price/q-d3.html', '奔驰': '/price/q-d4.html', '宝马': '/price/q-d20.html',
                  '别克': '/price/q-d7.html', '比亚迪': '/price/q-d107.html', '宝骏': '/price/q-d582.html',
                  '标致': '/price/q-d41.html', '保时捷': '/price/q-d44.html', '奔腾': '/price/q-d306.html',
                  '北京': '/price/q-d593.html', '宾利': '/price/q-d45.html', '北京汽车': '/price/q-d814.html',
                  '北汽新能源': '/price/q-d950.html', '北汽幻速': '/price/q-d898.html', '北汽制造': '/price/q-d122.html',
                  '宝沃': '/price/q-d1126.html', '布加迪': 'javascript:void(0)', '巴博斯': '/price/q-d723.html',
                  '北汽威旺': '/price/q-d643.html', '比速汽车': '/price/q-d7190.html', '北汽道达': '/price/q-d7311.html',
                  '比德文汽车': '/price/q-d7912.html', '北京清行': 'javascript:void(0)'},
            'C': {'长安汽车': '/price/q-d124.html', '长安欧尚': '/price/q-d613.html', '长城': '/price/q-d110.html',
                  '长安轻型车': '/price/q-d7301.html', '昌河': '/price/q-d75.html', '长安跨越': '/price/q-d7692.html',
                  '成功': '/price/q-d990.html', '长江EV': '/price/q-d7321.html'},
            'D': {'大众': '/price/q-d2.html', '东风启辰': '/price/q-d633.html', '东风风行': '/price/q-d949.html',
                  '东风风神': '/price/q-d581.html', '东风风光': '/price/q-d1139.html', '东南': '/price/q-d16.html',
                  '东风小康': '/price/q-d856.html', '东风': '/price/q-d111.html', '道奇': '/price/q-d72.html',
                  'DS': '/price/q-d754.html', '大乘汽车': '/price/q-d7691.html', '东风风度': '/price/q-d877.html',
                  '电咖': '/price/q-d7401.html', '东风富康': '/price/q-d7741.html', '大迪': 'javascript:void(0)',
                  '东风瑞泰特': '/price/q-d7562.html'},
            'F': {'丰田': '/price/q-d10.html', '福特': '/price/q-d21.html', '法拉利': '/price/q-d61.html',
                  '福田': '/price/q-d103.html', '菲亚特': '/price/q-d18.html', '福迪': '/price/q-d116.html',
                  '福汽启腾': '/price/q-d878.html'},
            'G': {'广汽传祺': '/price/q-d571.html', '观致': '/price/q-d824.html', '广汽新能源': '/price/q-d7471.html',
                  '广汽集团': '/price/q-d7711.html', 'GMC': '/price/q-d265.html', '广汽吉奥': '/price/q-d195.html',
                  '光冈': 'javascript:void(0)', '国机智骏': '/price/q-d7883.html', '国金汽车': '/price/q-d7351.html',
                  '格罗夫': 'javascript:void(0)'},
            'H': {'哈弗': '/price/q-d845.html', '红旗': '/price/q-d396.html', '海马': '/price/q-d8.html',
                  '海马郑州': '/price/q-d583.html', '汉腾': '/price/q-d1180.html', '悍马': 'javascript:void(0)',
                  '华泰': '/price/q-d115.html', '黄海': '/price/q-d133.html', '汉龙汽车': '/price/q-d7983.html',
                  '哈飞': 'javascript:void(0)', '海格': '/price/q-d876.html', '海马新能源': '/price/q-d7291.html',
                  '华普': 'javascript:void(0)', '华泰新能源': '/price/q-d1149.html', '华颂': '/price/q-d1001.html',
                  '红星': '/price/q-d7621.html', '华骐': '/price/q-d7331.html', '恒天': 'javascript:void(0)'},
            'J': {'吉利汽车': '/price/q-d13.html', 'Jeep': '/price/q-d38.html', '江淮': '/price/q-d78.html',
                  '捷达': '/price/q-d7791.html', '捷豹': '/price/q-d26.html', '捷途': '/price/q-d7501.html',
                  '金杯': '/price/q-d83.html', '江铃': '/price/q-d101.html', '金龙汽车': '/price/q-d355.html',
                  '九龙': '/price/q-d568.html', '几何汽车': '/price/q-d7861.html', '江铃集团新能源': '/price/q-d7260.html',
                  '君马汽车': '/price/q-d7322.html', '捷尼赛思': 'javascript:void(0)', '钧天汽车': '/price/q-d7781.html',
                  '金旅': '/price/q-d114.html'},
            'K': {'凯迪拉克': '/price/q-d70.html', '克莱斯勒': '/price/q-d39.html', '开瑞': '/price/q-d578.html',
                  '凯翼': '/price/q-d970.html', '科尼赛克': '/price/q-d570.html', '卡威汽车': '/price/q-d1012.html',
                  '康迪': '/price/q-d1095.html', '卡升': '/price/q-d704.html', 'KARMA': '/price/q-d7831.html',
                  'KTM': '/price/q-d888.html', '凯马': '/price/q-d1075.html', '科瑞斯的': 'javascript:void(0)'},
            'L': {'雷克萨斯': '/price/q-d30.html', '路虎': '/price/q-d29.html', '铃木': '/price/q-d73.html',
                  '领克': '/price/q-d7220.html', '林肯': '/price/q-d66.html', '雷诺': '/price/q-d40.html',
                  '兰博基尼': '/price/q-d64.html', '劳斯莱斯': '/price/q-d47.html', '猎豹汽车': '/price/q-d58.html',
                  '陆风': '/price/q-d569.html', '力帆': '/price/q-d305.html', '路特斯': '/price/q-d653.html',
                  '雷丁': '/price/q-d1022.html', 'Lorinser': '/price/q-d663.html', '理想汽车': '/price/q-d7721.html',
                  '理念': '/price/q-d604.html', '零跑': '/price/q-d7421.html', '莲花': 'javascript:void(0)',
                  'LITE': '/price/q-d7611.html', '陆地方舟': '/price/q-d939.html', '领途': '/price/q-d7701.html',
                  'LOCAL MOTORS': '/price/q-d1085.html'},
            'M': {'马自达': '/price/q-d17.html', 'MG名爵': '/price/q-d345.html', 'MINI': '/price/q-d205.html',
                  '玛莎拉蒂': '/price/q-d316.html', '迈凯伦': '/price/q-d715.html', '迈巴赫': 'javascript:void(0)',
                  '摩根': '/price/q-d908.html', '明君华凯': '/price/q-d1106.html'},
            'N': {'纳智捷': '/price/q-d623.html', '哪吒汽车': '/price/q-d7651.html', 'NEVS国能汽车': '/price/q-d7731.html',
                  '南京金龙': '/price/q-d1053.html'},
            'O': {'讴歌': '/price/q-d140.html', '欧拉': '/price/q-d7553.html', '欧宝': 'javascript:void(0)',
                  '欧朗': 'javascript:void(0)', '欧睿': 'javascript:void(0)'},
            'P': {'帕加尼': '/price/q-d573.html', 'Polestar极星': '/price/q-d7381.html'},
            'Q': {'奇瑞': '/price/q-d57.html', '起亚': '/price/q-d12.html', '乔治·巴顿': '/price/q-d7581.html',
                  '前途': '/price/q-d1074.html', '骐铃汽车': '/price/q-d1136.html', '庆铃汽车': '/price/q-d121.html'},
            'R': {'日产': '/price/q-d15.html', '荣威': '/price/q-d365.html', '瑞麒': 'javascript:void(0)',
                  '容大智造': '/price/q-d7631.html'},
            'S': {'斯柯达': '/price/q-d69.html', '三菱': '/price/q-d32.html', '上汽MAXUS': '/price/q-d673.html',
                  '斯巴鲁': '/price/q-d49.html', 'smart': '/price/q-d603.html', 'SWM斯威汽车': '/price/q-d7200.html',
                  '思铭': '/price/q-d733.html', '双龙': '/price/q-d53.html', '赛麟': '/price/q-d980.html',
                  '萨博': 'javascript:void(0)', '斯达泰克': '/price/q-d1137.html', '双环': 'javascript:void(0)',
                  '世爵': 'javascript:void(0)', 'SERES赛力斯': '/price/q-d7531.html', '上喆汽车': '/price/q-d7932.html',
                  '思皓': '/price/q-d7552.html'},
            'T': {'特斯拉': '/price/q-d774.html', '腾势': '/price/q-d743.html', '泰卡特': '/price/q-d969.html',
                  '天际': '/price/q-d7661.html'},
            'W': {'五菱': '/price/q-d118.html', '沃尔沃': '/price/q-d24.html', 'WEY': '/price/q-d7240.html',
                  '五十铃': '/price/q-d918.html', '蔚来': '/price/q-d7250.html', '潍柴汽车': '/price/q-d7942.html',
                  '威马汽车': '/price/q-d7441.html', '威麟': 'javascript:void(0)', '威兹曼': '/price/q-d753.html'},
            'X': {'现代': '/price/q-d34.html', '雪佛兰': '/price/q-d225.html', '雪铁龙': '/price/q-d6.html',
                  '星途': '/price/q-d7751.html', '小鹏汽车': '/price/q-d7210.html', '西雅特': 'javascript:void(0)',
                  '新宝骏': '/price/q-d7963.html', '星驰': '/price/q-d7361.html', '新特': '/price/q-d7551.html',
                  '新凯': '/price/q-d7461.html'},
            'Y': {'英菲尼迪': '/price/q-d28.html', '一汽': '/price/q-d9.html', '依维柯': '/price/q-d132.html',
                  '野马汽车': '/price/q-d516.html', '驭胜': '/price/q-d7511.html', '御捷': '/price/q-d1063.html',
                  '英致': '/price/q-d919.html', '云度新能源': '/price/q-d7271.html', '永源': '/price/q-d275.html',
                  '云雀汽车': '/price/q-d7491.html', '延龙汽车': '/price/q-d7641.html', '裕路': '/price/q-d7371.html'},
            'Z': {'众泰': '/price/q-d307.html', '中华': '/price/q-d104.html', '知豆': '/price/q-d929.html',
                  '中欧': '/price/q-d506.html', '中兴': '/price/q-d125.html', '之诺': '/price/q-d866.html',
                  '中顺': 'javascript:void(0)'}
        }
        self.dict_price = {
             '不限': '/price/q-p0.html', '5万以下': '/price/q-p1.html', '5-8万': '/price/q-p2.html', '8-10万': '/price/q-p3.html',
             '10-15万': '/price/q-p4.html', '15-20万': '/price/q-p5.html', '20-25万': '/price/q-p6.html',
             '25-35万': '/price/q-p7.html', '35-50万': '/price/q-p8.html', '50-100万': '/price/q-p9.html',
             '100万以上': '/price/q-p10.html'
        }
        # "https://price.pcauto.com.cn/price/q-d7421-p5-k110.html"


        #子窗口名字修改
        self.setWindowTitle("欢迎使用太平洋汽车网爬取程序")
        #子窗口最大化
        self.showMaximized()
        self.textBrowser_3.append("欢迎使用太平洋汽车网爬取程序，请设置爬虫参数\r")

        # 设置表格
        self.model = QStandardItemModel(0, 10)
        # 设置水平方向十个头标签文本内容
        self.model.setHorizontalHeaderLabels(
            ['级别1', '级别2', '品牌', '搜索价格区间', '页码', '编号', '名称', '官方指导价', '评论数量', '评分']
        )

        self.tableView = QtWidgets.QTableView(self.frame_2)
        self.tableView.setObjectName("tableView")
        self.tableView.setModel(self.model)
        self.horizontalLayout_3.addWidget(self.tableView)

        # 本程序不需要导入数据
        self.pushButton_8.setEnabled(False)

        # 定义接口数据
        self.interface_data = []
        self.interface_data_state = True
        self.pushButton_1.clicked.connect(lambda: self.check_data())

        # 更改swichbtn状态
        self.select_btn = 1
        self.select_btn_translate = "热度降序"
        self.radioButton_1.setChecked(True)
        self.radioButton_1.clicked.connect(lambda: self.selectbtn(1))
        self.radioButton_2.clicked.connect(lambda: self.selectbtn(2))
        self.radioButton_3.clicked.connect(lambda: self.selectbtn(3))

        # 价格 页码可输入范围
        self.spinBox_3.setRange(1, 109)
        self.spinBox_4.setRange(1, 109)

        # 创建导入导出文件位置
        self.in_address = ""
        self.out_address = ""
        # self.pushButton_8.clicked.connect(self.getfile)
        self.pushButton_9.clicked.connect(self.savefile)

        # 设置开始按钮
        self.pushButton_4.setEnabled(False)
        self.pushButton_4.clicked.connect(self.start_btn)

        # 设置中止按钮
        self.pushButton_5.setEnabled(False)
        self.pushButton_5.clicked.connect(self.main_stop_thread)

        # 设置清空参数按钮
        self.pushButton_2.clicked.connect(self.clean_frame_6)

        # 设置清除提示窗口
        self.pushButton_3.clicked.connect(self.clean_textBrowser_3)

        # 数据保存按钮，保存为excel
        self.pushButton_6.setEnabled(False)
        self.pushButton_6.clicked.connect(self.save_excel)


        #三个下拉列表框设置
        for keys, values in self.dict_level_l1.items():
            self.comboBox.addItem(keys, values)
        self.comboBox.activated.connect(self.combobox_change_level)

        for keys, values in self.dict_brand.items():
            self.comboBox_2.addItem(keys, values)
        self.comboBox_2.activated.connect(self.combobox_change_brand)

        self.comboBox_3.clear()
        for keys, values in self.dict_price.items():
            self.comboBox_3.addItem(keys, values)

        self.combobox_change_level(0)
        self.combobox_change_brand(0)






    # 第一个联动函数
    def combobox_change_level(self, i):
        self.comboBox_11.clear()
        a = self.comboBox.itemText(i)
        for keys, values in self.dict_level_l2[a].items():
            self.comboBox_11.addItem(keys, values)


    # 第二个联动函数
    def combobox_change_brand(self, i):
        self.comboBox_22.clear()
        a = self.comboBox_2.itemText(i)
        for keys, values in self.dict_brand[a].items():
            self.comboBox_22.addItem(keys, values)

    # 选择商品排序槽函数
    def selectbtn(self, i):
        self.select_btn = i
        # 翻译按钮
        self.translate_radio(i)


    #状态选择翻译
    def translate_radio(self, i):
        a = {"1": "热度降序", "2": "最新", "3": "价格降序"}
        self.select_btn_translate = a[str(i)]
    #
    # 导入文件按钮槽函数
    def getfile(self):
        a = QFileDialog.getOpenFileName(self, '请选择要打开的文件', 'c:\\', "Data files (*.xlsx *.xls *.csv)")
        self.pushButton_8.setText(a[0])
        self.in_address = a[0]
    #
    # 导出文件按钮槽函数
    def savefile(self):
        a = QFileDialog.getSaveFileName(self, '请选择要保存的位置', 'c:\\', "Data files (*.xls)")
        self.pushButton_9.setText(a[0])
        self.out_address = a[0]

    #
    # 清空参数函数
    def clean_frame_6(self):
        self.comboBox.setCurrentIndex(0)
        self.comboBox_2.setCurrentIndex(0)
        self.comboBox_3.setCurrentIndex(0)
        self.spinBox_3.setValue(1)
        self.spinBox_4.setValue(1)
        self.radioButton_1.setChecked(True)
        self.pushButton_9.setText("点击选择")
        self.out_address = ''

        self.textBrowser_3.append("已成功清除参数\r")
    #
    # 清除提示窗口函数
    def clean_textBrowser_3(self):
        self.textBrowser_3.clear()

    # 检查按钮对应槽函数
    def check_data(self):
        if self.pushButton_1.text() == "取消":
            self.frame_6.setEnabled(True)
            self.pushButton_1.setText("检查参数")
            self.pushButton_4.setEnabled(False)
            self.pushButton_2.setEnabled(True)
            self.textBrowser_3.append("请重新输入需要修改的参数\r")
        else:
            self.interface_data = [self.comboBox.currentText(), self.comboBox_11.currentText(),
                                   self.comboBox_2.currentText(), self.comboBox_22.currentText(),
                                   self.comboBox_3.currentText(),
                                   self.select_btn, self.spinBox_3.text(), self.spinBox_4.text(),
                                   self.in_address, self.out_address, ""]
            print(self.interface_data)
            if int(self.interface_data[6]) > int(self.interface_data[7]):
                self.textBrowser_3.append("商品页码搜索区间有误\r")
                self.interface_data_state = False
            if self.interface_data[9] == "":
                self.textBrowser_3.append("请设置导出文件的位置\r")
                self.interface_data_state = False
            #
            # 网址
            kk = self.dict_level_l2[self.interface_data[0]][self.interface_data[1]]
            dd = self.dict_brand[self.interface_data[2]][self.interface_data[3]]
            pp = self.dict_price[self.interface_data[4]]
            kk = re.sub("\D+", "", kk)
            dd = re.sub("\D+", "", dd)
            pp = re.sub("\D+", "", pp)
            self.interface_data[10] = "https://price.pcauto.com.cn/price/q-d" + dd + "-p" + pp + "-k" + kk + "-o" + str(int(self.interface_data[5])-1) + "-n1.html"

            self.textBrowser_1.setText(
                "级别：" + self.interface_data[0] + "  " + self.interface_data[1] +
                "\r\r品牌：" + self.interface_data[3] +
                "\r\r价格：" + self.interface_data[4] +
                "\r\r搜索规则：" + self.select_btn_translate +
                "\r\r搜索页数：" + self.interface_data[6] + " 到 " + self.interface_data[7] + " 页" +
                "\r\r导入位置：" + self.interface_data[8] +
                "\r\r导出位置：" + self.interface_data[9] +
                "\r\r当前网址：" + self.interface_data[10]
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

    # 开始按钮槽函数
    def start_btn(self):

        # 准备创建Excel
        self.book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        self.sheet = self.book.add_sheet('Sheet1', cell_overwrite_ok=True)
        a = ['序号', '级别1', '级别2', '品牌', '搜索价格区间', '页码', '编号', '名称', '官方指导价', '评论数量', '评分']
        for i in range(len(a)):
            self.sheet.write(0, i, a[i])

        # 设置变量excel排数
        self.book_row = 1
        #
        # #清空表格
        self.model.clear()
        self.model.setHorizontalHeaderLabels(
            ['级别1', '级别2', '品牌', '搜索价格区间', '页码', '编号', '名称', '官方指导价', '评论数量', '评分']
        )

        # 开启另一个线程
        self.thread.setidentity(self.interface_data)
        self.thread.start()

    def main_stop_thread(self):
        print("main_stop_thread")
        self.textBrowser_3.append("正在中止程序，请稍等...\r")
        self.pushButton_5.setEnabled(False)
        self.thread.stop_thread()



    # 显示表格函数
    def showtable(self, a):
        print(a)
        self.model.appendRow(
            [QStandardItem(str(a["level1"])),
             QStandardItem(str(a["level2"])),
             QStandardItem(str(a["brand"])),
             QStandardItem(str(a["price_s"])),
             QStandardItem(str(a["page"])),
             QStandardItem(str(a["id"])),
             QStandardItem(str(a["name"])),
             QStandardItem(str(a["price"])),
             QStandardItem(str(a["count"])),
             QStandardItem(str(a["avgScore"]))
             ]
        )
    #
        self.sheet.write(self.book_row, 0, self.book_row)
        self.sheet.write(self.book_row, 1, a["level1"])
        self.sheet.write(self.book_row, 2, a["level2"])
        self.sheet.write(self.book_row, 3, a["brand"])
        self.sheet.write(self.book_row, 4, a["price_s"])
        self.sheet.write(self.book_row, 5, a["page"])
        self.sheet.write(self.book_row, 6, a["id"])
        self.sheet.write(self.book_row, 7, a["name"])
        self.sheet.write(self.book_row, 8, a["price"])
        self.sheet.write(self.book_row, 9, a["count"])
        self.sheet.write(self.book_row, 10, a["avgScore"])

        self.book_row = self.book_row + 1
    #
    # 显示报错
    def showerror(self, a):
        self.textBrowser_3.append(a)
    #
    # 子线程状态，按钮禁用
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
    # 确认保存为excel函数
    def save_excel(self):
        self.book.save(self.interface_data[9])
        self.textBrowser_3.append("已经成功保存到" + self.interface_data[9] + '\r')
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
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
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

    def get_commemts(self, page):
        url = self.identity[10]
        url = re.sub(r"-n\d+", "-n%s" % page, url)

        text = self.get_text(url)
        html = etree.HTML(text)

        id = html.xpath("//a[@class='btn-toggle']/@data-sgid")
        a = html.xpath("//div[@class='tit']/a[@class='sname']//text()")
        b = html.xpath("//div[@class='con']/dl[@class='con-dl']/dd[contains(@class,'emphs')]/text()")

        if id == []:
            return False
        else:
            for i in range(len(id)):
                dict_car = {"level1": self.identity[0], "level2": self.identity[1], "brand": self.identity[3], "price_s": self.identity[4], "page": page, "id": id[i], "name": a[i], "price": b[i]}
                url2 = "https://price.pcauto.com.cn/comment/interface/auto/serial/get_comment_avg_score_4serial_json.jsp?sgid=%s&callback=getDriverScore" % id[i]
                x = self.get_text(url2)
                y = re.findall("({.*?})", x, re.S)[0]
                y = eval(y)
                dict_car.update(y)
                self.result_thread.emit(dict_car)
            return True



    def run(self):
        self.error_thread.emit("开始爬取,等耐心等待...\r")
        self.state_thread.emit(1)


        for ii in range(int(self.identity[6]), int(self.identity[7])+1):
            self.error_thread.emit("需爬取到第 " + str(self.identity[7]) + " 页，正在爬取第 " + str(ii) + " 页。")
            if self.get_commemts(ii) == False:
                self.error_thread.emit("此页商品数目不足,，或超过筛选条件页数，请扩大筛选条件或减少搜索页数。\r")
                break
        #
            if self.working == False:
                break

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