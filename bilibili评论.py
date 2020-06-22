# -*- coding: utf-8 -*-

import sys
from moban import ChildWindow as a
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
# import qdarkstyle
import re

class ChildWindow(a):
    def __init__(self, parent=None):
        super(ChildWindow, self).__init__(parent)

    def open1(self):
        # 第1行
        self.lineEdit.setMaxLength(200)
        self.label_1.setEnabled(True)
        self.label_1.setText('网址：')
        self.lineEdit.setEnabled(True)
        self.comboBox.setEnabled(True)
        self.comboBox.setItemText(0, "视频")
        self.comboBox.addItem("动态")
        self.comboBox.addItem("文章")
        self.comboBox.addItem("活动")
        # self.comboBox.addItem("番剧")

    def open2(self):
        # 第2行
        self.label_2.setEnabled(True)
        self.comboBox_2.setEnabled(True)
        self.comboBox_2.addItem("按时间排序")
        self.comboBox_2.setItemText(0, "按热度排序")

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
        self.open2()
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
        if self.param["4 1"] > self.param["4 2"]:
            self.interface_data_state = False
            self.textBrowser_3.append("页码参数设置有误，请重新输入")
        if self.param["4 3"] is False and self.param["4 1"] == '0':
            self.interface_data_state = False
            self.textBrowser_3.append("页码不能为0")
        # if self.param["5"] == []:
        #     self.interface_data_state = False
        #     self.textBrowser_3.append("请至少勾选一个项目")
        print(self.param)

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
            "\r类型：" + self.param["1 2"] +
            "\r搜索规则：" + self.param["2 1"] +
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
        self.setWindowTitle("bilibili评论爬取")

        # 子窗口最大化
        # self.showMaximized()

        # box标题
        self.groupBox.setTitle("b站评论")

        # 表格
        self.table_list = ["页码", 'id', "评论内容编号", "类型", "评论创建时间戳", "最后回复时间戳", "点赞数", "踩楼数", "用户id", "昵称", "性别", "签名", "头像", "等级", "是否为大会员", '评论内容']

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
        ["页码", "评论编号", "类型", "评论创建时间戳",
         "最后回复时间戳", "点赞数", "踩楼数", "用户id",
         "昵称", "性别", "签名", "头像", "等级", "是否为大会员",
         '评论内容']
        self.model.appendRow(
            [QStandardItem(str(a["page"])),
             QStandardItem(str(a["oid"])),
             QStandardItem(str(a["rpid"])),
             QStandardItem(str(a["type"])),
             QStandardItem(str(a["ctime"])),
             QStandardItem(str(a["rpid_str"])),
             QStandardItem(str(a["like"])),
             QStandardItem(str(a["action"])),
             QStandardItem(str(a['member']["mid"])),
             QStandardItem(str(a['member']["uname"])),
             QStandardItem(str(a['member']["sex"])),
             QStandardItem(str(a['member']["sign"])),
             QStandardItem(str(a['member']['avatar'])),
             QStandardItem(str(a['member']['level_info']['current_level'])),
             QStandardItem(str(a['member']['vip']['vipStatus'])),
             QStandardItem(str(a['content']['message'])),
             ]
        )
        self.tableView.scrollToBottom()

        self.sheet.write(self.book_row, 0, a["page"])
        self.sheet.write(self.book_row, 1, a["oid"])
        self.sheet.write(self.book_row, 2, a["rpid"])
        self.sheet.write(self.book_row, 3, a["type"])
        self.sheet.write(self.book_row, 4, a["ctime"])
        self.sheet.write(self.book_row, 5, a["rpid_str"])
        self.sheet.write(self.book_row, 6, a["like"])
        self.sheet.write(self.book_row, 7, a["action"])
        self.sheet.write(self.book_row, 8, a['member']["mid"])
        self.sheet.write(self.book_row, 9, a['member']["uname"])
        self.sheet.write(self.book_row, 10, a['member']["sex"])
        self.sheet.write(self.book_row, 11, a['member']["sign"])
        self.sheet.write(self.book_row, 12, a['member']['avatar'])
        self.sheet.write(self.book_row, 13, a['member']['level_info']['current_level'])
        self.sheet.write(self.book_row, 14, a['member']['vip']['vipStatus'])
        self.sheet.write(self.book_row, 15, a['content']['message'])

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

    # def get_id(self):
    #     #     a = requests.get(self.identity['1 1'])
    #     #     id = re.findall('window.activity = \{id: (.*?),', a.text, re.S)
    #     #     self.id = str(id[0])
    #     #
    #     # def get_dict(self, data):
    #     #     if self.identity['2 1'] == '按时间排序':
    #     #         response = requests.post('https://mall.bilibili.com/mall-c/ugc/content/allList', headers=self.headers, data=data)
    #     #     else:
    #     #         response = requests.post('https://mall.bilibili.com/mall-c/ugc/content/allHotUgcList', headers=self.headers, data=data)
    #     #     all_dict = response.json()
    #     #     if all_dict['data']['hotList'] is None:
    #     #         list = all_dict['data']['commonList']
    #     #     else:
    #     #         list = all_dict['data']['hotList']
    #     #     return list
    #     #
    #     # def crawl(self, page):
    #     #     if self.working:
    #     #         data = '{"device":"h5",' \
    #     #                '"mid":0,' \
    #     #                '"pageNum":%s,' % page + \
    #     #                '"pageSize":20,' \
    #     #                '"ignoreEssenceIds":[],' \
    #     #                '"ignoreHotIds":[],' \
    #     #                '"platform":2,' \
    #     #                '"subPageSize":2,' \
    #     #                '"subjectId":"%s", ' % self.id + \
    #     #                '"subjectType":"3",' \
    #     #                '"version":"1.0",' \
    #     #                '"prePageLastFloorNo":null}'
    #     #         # url = self.dicts[keyword]
    #     #         # self.show_text("正在爬取网址: " + keyword)
    #     #         # self.show_msg("网址: " + keyword )
    #     #         # self.show_img(int(self.now/self.all*100))
    #     #         # self.now = self.now+1
    #     #         # text = self.get_text(url)
    #     #         dicts = self.get_dict(data)
    #     #         for dict in dicts:
    #     #             self.final_data(dict)
    def get_id(self, url, sort):
        headers = {
            'authority': 'www.bilibili.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'sec-fetch-dest': 'document',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'referer': 'https://www.bilibili.com/',
            'accept-language': 'zh-CN,zh;q=0.9',
            # '$cookie': '_uuid=3F019BA6-8EF7-BE6A-1BE6-A7708E72C30797715infoc; buvid3=4CFC1D59-CFE1-4FF0-91EC-895DDAC7E80E155823infoc; CURRENT_FNVAL=16; rpdid=|(um)~|)Yk)R0J\'ul)RJJlR~J; LIVE_BUVID=AUTO9515845223143272; DedeUserID=21642212; DedeUserID__ckMd5=3e991018320e5486; SESSDATA=fae49113%2C1601011289%2Ca69f5*31; bili_jct=c09d6ceeff539c7b75ce81fa31f2db45; CURRENT_QUALITY=116; bp_t_offset_21642212=391507043791143305; bp_video_offset_21642212=394427527060836356; PVID=4; bsource=seo_baidu; sid=5761b6kc',
        }

        response = requests.get(url, headers=headers, verify=False)
        text = response.text

        if sort == 1:
            id = re.findall('"aid":(.*?),', text)[1]
        if sort == 4:
            id = re.findall('window.activity = \{id: (.*?),', text, re.S)[0]
        if sort == 12:
            id = re.findall('cvid: "(.*?)",', text)[0]
        if sort == 11:
            id = re.findall('"rid":(.*?),', text)[0]
        # if sort == 2:
        #     id = re.findall('"aid":(.*?),', text)[1]

        return id

    def get_dict(self, id, page, type, sort):
        headers = {
            'authority': 'api.bilibili.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'sec-fetch-dest': 'script',
            'accept': '*/*',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'no-cors',
            'accept-language': 'zh-CN,zh;q=0.9',
        }

        params = (
            ('jsonp', 'jsonp'),
            ('pn', str(page)),
            ('type', str(sort)),
            ('oid', str(id)),
            ('sort', str(type)),
        )

        response = requests.get('https://api.bilibili.com/x/v2/reply', headers=headers, params=params, verify=False)
        print('成功获取text')
        return response.json()

    def get_page(self, b_dict):
        all_count = b_dict['data']['page']['acount']
        count = b_dict['data']['page']['count']
        this_page = b_dict['data']['page']['num']
        print(count)
        print(all_count)
        return count

    def read_dict(self, b_dict):
        for i in b_dict['data']['replies']:
            i['page'] = b_dict['data']['page']['num']
            self.final_data(i)

    def trans_dict(self, dicts):
        traned_dict = {}
        sort_dict = {
            '视频': 1,
            '文章': 12,
            '动态': 11,
            '活动': 4,
            # '番剧': 2,
        }
        type_dict = {
            '按时间排序': 0,
            '按热度排序': 2
        }
        traned_dict['page1'] = dicts['4 1']
        traned_dict['page2'] = dicts['4 2']
        traned_dict['sort'] = sort_dict[dicts['1 2']]
        traned_dict['type'] = type_dict[dicts['2 1']]
        traned_dict['url'] = dicts['1 1']
        return traned_dict

    def run(self):
        outdict = self.trans_dict(self.identity)

        try:
            id = self.get_id(outdict['url'], outdict['sort'])
            numdict = self.get_dict(id, 1, 1, outdict['sort'])
            count = self.get_page(numdict)
            all_page = count // 20 + 1
        except:
            self.show_text("网址有误，或分类有误，请修改网址或分类")
            self.working = False

        if self.working == True:
            if int(outdict['page1']) == 0:
                for page in range(1, all_page + 1):
                    if self.working:
                        self.show_msg("页码: " + str(page))
                        self.show_img(int(page / all_page * 100))
                        self.show_text("正在爬取页码: " + str(page) + "      页码进度: " + str(page) + " / " + str(all_page))
                        b_dict = self.get_dict(id, page, outdict['type'], outdict['sort'])
                        self.read_dict(b_dict)
                    else:
                        break
            else:
                for page in range(int(outdict['page1']), int(outdict['page2']) + 1):
                    if self.working:
                        self.show_msg("页码: " + str(page))
                        self.show_img(int((page-int(outdict['page1'])+1) / (int(outdict['page2'])-int(outdict['page1'])+1) * 100))
                        self.show_text("正在爬取页码: " + str(page) + "      页码进度: " + str(page) + " / " + str(outdict['page2']))
                        b_dict = self.get_dict(id, page, outdict['type'], outdict['sort'])
                        self.read_dict(b_dict)
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