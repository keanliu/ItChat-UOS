# -*- coding: utf-8 -*-

import itchat
# tuling plugin can be get here:
# https://github.com/littlecodersh/EasierLife/tree/master/Plugins/Tuling
# nohup python3 -m jurigged -v main.py &
from tuling import get_response
import sys
import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from zoneinfo import ZoneInfo
import json
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import time

temp_dir = Path(__file__).resolve().parent
temp_dir = Path(temp_dir).resolve().parent
sys.path.append(os.path.join(temp_dir, 'python_tools'))
import aoti.aoti_place_order_unified 


home_dir = Path.home()

size_handler = RotatingFileHandler(
    os.path.join(home_dir, 'wrapper.log'), maxBytes=10485760, backupCount=5, encoding='utf-8'
)

formatter = logging.Formatter("%(asctime)s -%(processName)s - %(threadName)s - %(levelname)s - %(message)s")
size_handler.setFormatter(formatter)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
# Get logger and add handlers
logger = logging.getLogger()
logger.addHandler(consoleHandler)
logger.addHandler(size_handler)
logger.setLevel(logging.INFO)


@itchat.msg_register('Text')
def text_reply(msg):
    # logging.info(json.dumps(msg, ensure_ascii=False, indent=4)) 
    logging.info("Got a message, from:%s; message: %s" % (msg['User']['NickName'], msg['Text'])) 
    # return u'收到：' + msg['Text'] +  "; /r/n/r/n目前不在线，回头答复您"

# @itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
# def atta_reply(msg):
#     return ({ 'Picture': u'图片', 'Recording': u'录音',
#         'Attachment': u'附件', 'Video': u'视频', }.get(msg['Type']) +
#         u'已下载到本地') # download function is: msg['Text'](msg['FileName'])

# @itchat.msg_register(['Map', 'Card', 'Note', 'Sharing'])
# def mm_reply(msg):
#     if msg['Type'] == 'Map':
#         return u'收到位置分享'
#     elif msg['Type'] == 'Sharing':
#         return u'收到分享' + msg['Text']
#     elif msg['Type'] == 'Note':
#         return u'收到：' + msg['Text']
#     elif msg['Type'] == 'Card':
#         return u'收到好友信息：' + msg['Text']['Alias']

@itchat.msg_register('Text', isGroupChat = True)
def group_reply(msg):
    # logging.info( os.environ.get('ITCHAT_UOS_ASYNC', False))
    logging.info('Got a message, from: group %s; user%s; content: %s' % (msg['User']['NickName'], msg['ActualNickName'], msg['Text']))
    # logging.info(json.dumps(msg, ensure_ascii=False, indent=4))
    if msg['isAt']:
        # return
        return u'@%s\u2005%s' % (msg['ActualNickName'], u'收到：' + msg['Text'] + "; 我不在线，回头答复您")

# @itchat.msg_register('Friends')
# def add_friend(msg):
#     itchat.add_friend(**msg['Text'])
#     itchat.send_msg(u'项目主页：github.com/littlecodersh/ItChat\n'
#         + u'源代码  ：回复源代码\n' + u'图片获取：回复获取图片\n'
#         + u'欢迎Star我的项目关注更新！', msg['RecommendInfo']['UserName'])

itchat.auto_login(hotReload=True, enableCmdQR=2)
itchat.run(blockThread=False)
itchat.send('Hello, please rememver this', toUserName='filehelper')


def is_valid_time():

    # Get the current datetime
    now = datetime.datetime.now()    
    # Get the current day of the week (0=Monday, 6=Sunday)
    day_of_week = now.weekday()    
    # Get the current time
    current_time = now.time()    
    # Define the start and end times
    start_time = datetime.time(6, 30)
    end_time = datetime.time(23, 30)    
    # Check if the current day is not Friday (4) or Saturday (5)
    if day_of_week in (4, 5):
        return False    
    # Check if the current time is within the specified range
    if start_time <= current_time <= end_time:
        return True    
    return False

def check_available_court():
    logging.info("Enter check_available_court--")   
    logging.info("is it time? %s" % str(is_valid_time())) 
    # result = aoti.aoti_place_order_unified.get_court_book_info(aoti.aoti_place_order_unified.kean_dic, aoti.aoti_place_order_unified.target_date)
    # if result:
    #     msg_text = ''
    #     for court, time_info in result:
    #         msg_text = msg_text + court[1][1] + time_info['v'] + '/r/n'
    #     logging.info(msg_text)
    to_user = '@e0bfaae9860606cacb2db54737953ee34dd6c66329014a9ec63a3b7384c69a20' # 又胖又能吃群
    to_user = "@@44c1b8fd4cb16cea6836384ca89fbacae12d60cd9dffd842d8f86cd4996f3362" # 奥体羽毛球群
    msg_text = '牛气！'
    itchat.send_msg(to_user,  msg_text)

# scheduler = BackgroundScheduler({'apscheduler.job_defaults.max_instances': 300})
scheduler = BackgroundScheduler()
scheduler.remove_all_jobs() 
# scheduler.add_job(runsync, 'interval', seconds=1, max_instances=2)
scheduler.add_job(check_available_court, 'interval', seconds=120)

try:
    scheduler.start()
    while True:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    logging.exception("Here")
    scheduler.shutdown()