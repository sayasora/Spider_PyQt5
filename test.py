import requests
import re

headers = {
    'authority': 'mall.bilibili.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-fetch-dest': 'empty',
    # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'content-type': 'application/json',
    'accept': '*/*',
    'origin': 'https://www.bilibili.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    # 'referer': 'https://www.bilibili.com/blackboard/activity-_YSKZgCaw.html?from=banner&msource=mall_sony0521_fc&native.theme=1&night=0&share_medium=iphone&share_plat=ios&share_source=COPY&share_tag=s_i&timestamp=1590376321&unique_k=IYKJVE',
    'accept-language': 'zh-CN,zh;q=0.9',
    # '$cookie': '_uuid=3F019BA6-8EF7-BE6A-1BE6-A7708E72C30797715infoc; buvid3=4CFC1D59-CFE1-4FF0-91EC-895DDAC7E80E155823infoc; CURRENT_FNVAL=16; rpdid=|(um)~|)Yk)R0J\'ul)RJJlR~J; LIVE_BUVID=AUTO9515845223143272; DedeUserID=21642212; DedeUserID__ckMd5=3e991018320e5486; SESSDATA=fae49113%2C1601011289%2Ca69f5*31; bili_jct=c09d6ceeff539c7b75ce81fa31f2db45; CURRENT_QUALITY=116; bp_t_offset_21642212=391507043791143305; bp_video_offset_21642212=391720147181941998; bsource=seo_baidu; PVID=1; msource=pc_web; deviceFingerprint=8f499c9d6f1650fd1a4dfe368d4010fe',
}

get_url = 'https://www.bilibili.com/blackboard/activity-_YSKZgCaw.html?from=banner&msource=mall_sony0521_fc&native.theme=1&night=0&share_medium=iphone&share_plat=ios&share_source=COPY&share_tag=s_i&timestamp=1590376321&unique_k=IYKJVE'
a = requests.get(get_url)
id = re.findall('window.activity = \{id: (.*?),', a.text, re.S)
id = str(id[0])
print(id)

page = '1'

data = '{"device":"h5",' \
       '"mid":0,' \
       '"pageNum":%s,' % page + \
       '"pageSize":20,' \
       '"ignoreEssenceIds":[],' \
       '"ignoreHotIds":[],' \
       '"platform":2,' \
       '"subPageSize":2,' \
       '"subjectId":"%s", ' % id + \
       '"subjectType":"3",' \
       '"version":"1.0",' \
       '"prePageLastFloorNo":null}'

# response = requests.post('https://mall.bilibili.com/mall-c/ugc/content/allList', headers=headers, data=data)
response = requests.post('https://mall.bilibili.com/mall-c/ugc/content/allHotUgcList', headers=headers, data=data)
all_dict = response.json()
print(all_dict)
if all_dict['data']['hotList'] is None:
    list = all_dict['data']['commonList']
else:
    list = all_dict['data']['hotList']

print(list)
# for i in list:
#     print(i)
#     print(i['floor'])
#     print(i['subjectId'])
#     print(i['subjectUrl'])
#     print(i['subjectName'])
#     print(i['content'])
#     print(i['imgs'])
#     print(i['ctime'])
#     print(i['lastReplyTime'])
#     print(i['upCount'])
#     print(i['downCount'])
#     print(i['replyCount'])
#     print(i['actualCount'])
#     print(i['userinfo']['mid'])
#     print(i['userinfo']['uname'])
#     print(i['userinfo']['sex'])
#     print(i['userinfo']['level'])
#     print(i['userinfo']['avatar'])
#     print(i['userinfo']['vip']['status'])