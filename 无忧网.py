import sys, os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from moban import ChildWindow as a
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
# import qdarkstyle
import re
from lxml import etree

class ChildWindow(a):
    def __init__(self, parent=None):
        super(ChildWindow, self).__init__(parent)

    def open1(self):
        # 第1行
        self.lineEdit.setMaxLength(200)
        self.label_1.setEnabled(True)
        self.label_1.setText('网址：')
        self.lineEdit.setEnabled(True)

    # def open8(self):
    #     # 第8行
    #     self.label.setEnabled(True)
    #     self.label.setText('番剧集数:')
    #     self.label_21.setEnabled(True)
    #     self.spinBox_9.setEnabled(True)
    #     self.label_22.setEnabled(True)
    #     # self.spinBox_10.setEnabled(True)
    #     # self.label_23.setEnabled(True)
    #     # self.checkBox_6.setEnabled(True)
    #     self.label_23.close()
    #     self.label_22.setText('集')
    #     self.checkBox_6.close()
    #     self.spinBox_10.close()
    #
    # def close8(self):
    #     pass


    # 选择开启的功能
    def open_chose(self):
        self.open1()
        # self.open2()
        # self.open3()
        self.open4()
        # self.open5()
        # self.open6()
        # self.open7()
        # self.open8()

    # 检查参数是否正确
    def find_error(self):
        self.interface_data_state = True
        if not self.param["1 1"]:
            self.interface_data_state = False
            self.textBrowser_3.append("未输入网址，请输入")
        # if not self.in_address:
        #     self.interface_data_state = False
        if int(self.param["4 1"]) > int(self.param["4 2"]):
            self.interface_data_state = False
            self.textBrowser_3.append("页码参数设置有误，请重新输入")
        if self.param["4 3"] is False and self.param["4 1"] == '0':
            self.interface_data_state = False
            self.textBrowser_3.append("页码不能为0")
        # if self.param["5"] == []:
        #     self.interface_data_state = False
        #     self.textBrowser_3.append("请至少勾选一个项目")

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
            "网址：" + self.param["1 1"] +
            # "\r网址：" + self.param["1 2"] +
            # "\r类型：" + self.param["1 2"] +
            # "\r搜索规则：" + self.param["2 1"] +
            # "\r价格区间：" + text3 +
            "\r搜索页数：" + text4
            # "\r多选项目：" + str(self.param["5"])
            # "\r日期：" + self.param["6 1"] + " 至 " + self.param["6 2"]
            # "\r番剧集数：" + self.param['8 1']
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
        self.setWindowTitle("无忧网信息爬虫")

        # 子窗口最大化
        # self.showMaximized()

        # box标题
        self.groupBox.setTitle("无忧网信息")

        # 表格
        self.table_list = ['页码', "信息", '福利', "类型", "规模", "需求", "职位", "公司", "地点1", "薪资", "发布时间", "网址"]

        # self.checkBox_12.setText("要闻")
        # self.checkBox_13.setText("国内")
        # self.checkBox_21.setText("国际")
        # self.checkBox_22.setText("独家")
        # self.checkBox_23.setText("军事")
        # self.checkBox_31.setText("财经")
        # self.checkBox_32.setText("科技")
        # self.checkBox_33.setText("体育")
        # self.checkBox_41.setText("娱乐")
        # self.checkBox_42.setText("时尚")
        # self.checkBox_43.setText("汽车")
        # self.checkBox_51.setText("房产")
        # self.checkBox_52.setText("航空")
        # self.checkBox_53.setText("健康")

    def show_table(self, a):
        self.model.appendRow(
            [QStandardItem(str(a["页码"])),
             QStandardItem(str(a["信息"])),
             QStandardItem(str(a["福利"])),
             QStandardItem(str(a["类型"])),
             QStandardItem(str(a["规模"])),
             QStandardItem(str(a["需求"])),
             QStandardItem(str(a["职位"])),
             QStandardItem(str(a["公司"])),
             QStandardItem(str(a['地点1'])),
             QStandardItem(str(a['薪资'])),
             QStandardItem(str(a['发布时间'])),
             QStandardItem(str(a['网址'])),
             ]
        )
        self.tableView.scrollToBottom()

        self.sheet.write(self.book_row, 0, a["页码"])
        self.sheet.write(self.book_row, 1, a["信息"])
        self.sheet.write(self.book_row, 2, a["福利"])
        self.sheet.write(self.book_row, 3, a["类型"])
        self.sheet.write(self.book_row, 4, a["规模"])
        self.sheet.write(self.book_row, 5, a["需求"])
        self.sheet.write(self.book_row, 6, a["职位"])
        self.sheet.write(self.book_row, 7, a["公司"])
        self.sheet.write(self.book_row, 8, a['地点1'])
        self.sheet.write(self.book_row, 9, a['薪资'])
        self.sheet.write(self.book_row, 10, a['发布时间'])
        self.sheet.write(self.book_row, 11, a['网址'])

        self.book_row = self.book_row + 1



class yangshi(QThread):
    result_thread = pyqtSignal(dict)
    error_thread = pyqtSignal(str)
    state_thread = pyqtSignal(bool)
    msg_thread = pyqtSignal(str)
    img_thread = pyqtSignal(int)

    def __init__(self, parent=None):
        super(yangshi, self).__init__(parent)

    def setidentity(self, dict):
        self.working = True
        self.identity = dict
        self.now = 0
        # self.all = len(self.identity["5"])

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

    def get_page(self, url):
        headers = {
            'Host': 'search.51job.com',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'Sec-Fetch-Dest': 'document',
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            # 'Referer': 'https://search.51job.com/list/090200,000000,0000,39,9,99,%2B,2,3.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

        try:
            response = requests.get(url, headers=headers, timeout=2)
        except:
            try:
                response = requests.get(url, headers=headers, timeout=2)
            except:
                try:
                    response = requests.get(url, headers=headers, timeout=2)
                except:
                    response = requests.get(url, headers=headers, timeout=2)
        response.encoding = 'gbk'
        result = etree.HTML(response.text)
        results = result.xpath("//div[@class='p_in']/span[@class='td'][1]//text()")[0]
        page = re.findall('共(.*?)页', results)[0]
        return page

    def get1(self, url):
        headers = {
            'Host': 'search.51job.com',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'Sec-Fetch-Dest': 'document',
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            # 'Referer': 'https://search.51job.com/list/090200,000000,0000,39,9,99,%2B,2,3.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

        try:
            response = requests.get(url, headers=headers, timeout=2)
        except:
            try:
                response = requests.get(url, headers=headers, timeout=2)
            except:
                try:
                    response = requests.get(url, headers=headers, timeout=2)
                except:
                    response = requests.get(url, headers=headers, timeout=2)
        response.encoding = 'gbk'
        result = etree.HTML(response.text)
        results = result.xpath("//div[@id='resultList']/div[@class='el']")
        for i in results:
            dicts = {}
            dicts['职位'] = i.xpath("./p[1]//span/a/@title")
            dicts['公司'] = i.xpath("./span[@class='t2']/a//text()")
            dicts['地点1'] = i.xpath("./span[@class='t3']//text()")
            dicts['薪资'] = i.xpath("./span[@class='t4']//text()")
            dicts['发布时间'] = i.xpath("./span[@class='t5']//text()")
            dicts['网址'] = i.xpath("./p[1]//span/a/@href")[0]
            yield dicts

    def get2(self, url, dict3, page):
        headers = {
            'Host': 'search.51job.com',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'Sec-Fetch-Dest': 'document',
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            # 'Referer': 'https://search.51job.com/list/090200,000000,0000,39,9,99,%2B,2,3.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        try:
            response = requests.get(url, headers=headers, timeout=2)
        except:
            try:
                response = requests.get(url, headers=headers, timeout=2)
            except:
                try:
                    response = requests.get(url, headers=headers, timeout=2)
                except:
                    response = requests.get(url, headers=headers, timeout=2)
        response.encoding = 'gbk'
        html = etree.HTML(response.text)
        results1 = html.xpath("//div[@class='cn']/p[@class='msg ltype']//text()")
        a = []
        for i in results1:
            i = i.replace('\xa0', "")
            if i != '|':
                a.append(i)
        results2 = html.xpath("//div[@class='t1']/span[@class='sp4']//text()")
        results3 = html.xpath("//div[@class='com_tag']/p[@class='at'][1]//text()")
        results4 = html.xpath("//div[@class='com_tag']/p[@class='at'][2]//text()")
        results5 = html.xpath("//div[@class='com_tag']/p[@class='at'][3]/a//text()")
        dicts = {'页码': page, '信息': a, "福利": results2, '类型': results3, '规模': results4, '需求': results5}
        dicts.update(dict3)
        self.final_data(dicts)

    def change_url(self, url, page):
        c = re.sub('([\d]+).html', '测试', url)
        c = c.replace('测试', str(page) + '.html')
        return c

    def run(self):
        try:
            all_page = int(self.get_page(self.identity['1 1']))
        except:
            self.show_text("网址有误，或分类有误，请修改网址或分类")
            self.working = False

        if self.working == True:
            if self.identity['4 3']:
                for page in range(1, all_page + 1):
                    if self.working:
                        self.show_msg("页码: " + str(page))
                        self.show_img(int(page / all_page * 100))
                        self.show_text("正在爬取页码: " + str(page) + "      页码进度: " + str(page) + " / " + str(all_page))
                        url = self.change_url(self.identity['1 1'], page)
                        a = self.get1(url)
                        for i in a:
                            if self.working == True:
                                url2 = i['网址']
                                self.get2(url2, i, page)
                            else:
                                break
                    else:
                        break
            else:
                for page in range(int(self.identity['4 1']), int(self.identity['4 2']) + 1):
                    if self.working:
                        self.show_msg("页码: " + str(page))
                        self.show_img(int((page-int(self.identity['4 1'])+1) / (int(self.identity['4 2'])-int(self.identity['4 1'])+1) * 100))
                        self.show_text("正在爬取页码: " + str(page) + "      页码进度: " + str(page) + " / " + str(self.identity['4 2']))
                        url = self.change_url(self.identity['1 1'], page)
                        a = self.get1(url)
                        for i in a:
                            if self.working == True:
                                url2 = i['网址']
                                self.get2(url2, i, page)
                            else:
                                break
                    else:
                        break

            self.state_thread.emit(False)
            if self.working:
                self.error_thread.emit("爬取完成")
                # self.img_thread.emit(100)
            else:
                self.error_thread.emit("已中止程序")

        # for i in range(int(self.identity['4 1']), int(self.identity['4 2'])+1):
        #     if self.working:
        #         # self.show_text("正在爬取页码: "+str(i)+"      页码进度: "+str(i+1)+" / "+str(len(self.identity["5"])))
        #         # self.crawl(self.identity["key"][i], self.identity["page1"], self.identity["page2"])
        #         self.crawl(i)
        #     else:
        #         break
        self.state_thread.emit(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyleSheet(qdarkstyle.load_stylesheet())
    form = ChildWindow()
    form.show()
    sys.exit(app.exec_())