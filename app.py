# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 01:00:17 2018

@author: linzino
"""

import requests, re, feedparser, random
from lxml import etree
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('cXtIw9d8+oQbrXZ/3hEBocCNTpsroaNVWid2LiVlekEa8jnhW2CnKAKqfXvhWPUFGaLa81z7sYmUtCy+C5pXyYTW5ePpp+fRB8SbdwgoIPHwoQgNejTUnD4J+VTw4jUJ4DoZtkPR0NGwKBpUcslbmQdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('7e27ba98cfbaa7d09bef1435b55deb5f')

#line_bot_api.push_message('Ube6a1a56c1466ec56cee2ae59ca0b17b', TextSendMessage(text='你可以開始了'))
is_buy = False
#category
category_set = ['1900000000',
        '2900000000',
        '1100000000',
        '1200000000',
        '2000000000',
        '1300000000',
        '1400000000',
        '1500000000',
        '3100000000',
        '3900000000',
        '1700000000',
        '2500000000',
        '2700000000',
        '1800000000',
        '1600000000',
        '4000000000',
        '4100000000',
        '3500000000',
        '2400000000',
        '1900000000',
        '2900000000',
        '1100000000',
        '1200000000',
        '2000000000',
        '1300000000',
        '1400000000',
        '1500000000',
        '3100000000',
        '3900000000',
        '1700000000',
        '2500000000',
        '2700000000',
        '1800000000',
        '1600000000',
        '4000000000',
        '4100000000',
        '3500000000']

def getNews():
    """
    建立一個抓最新消息的function
    """
    rss_url = 'http://feeds.feedburner.com/cnaFirstNews'
    # 抓取資料
    rss = feedparser.parse(rss_url)
    #取亂數
    idx = random.randint(0, len(rss.entries)-1)
    # 抓取第一個文章標題
    title = rss.entries[idx]['title']
    # 抓取第一個文章標題
    link = rss.entries[idx]['link']
    
    tmp = title + ' ' +link
    return tmp

def getmomo_search(keyword):

    target_url = 'https://m.momoshop.com.tw/search.momo?searchKeyword={}&couponSeq=&searchType=1&cateLevel=-1&ent=k&_imgSH=fourCardStyle'.format(keyword)
    print(target_url)
    headers = {
           'accept-encoding': 'gzip, deflate, br', 
           'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7', 
           'Cache-Control': 'no-cache',
           'pragma': 'no-cache',
           'Upgrade-Insecure-Requests': '1',
           'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
           'content-type': 'application/x-www-form-urlencoded',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'cookie':''
           }

    # handle request body
    try:
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url=target_url, headers=headers, timeout=5)
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        return []
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        return []
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print(e)
        return []
    
    _html = etree.HTML(response.text)
    _imgs = _html.xpath('//article[contains(@class, "prdListArea")]//li[@class="goodsItemLi"]/a[not(@class="trackbtn")]/img[position()<3]')
    _img_data = []
    
    if len(_imgs) > 1:   
        for idx, img in enumerate(_imgs, start=0):
            _alt = img.attrib['alt']
            match = re.search(r'【.+】(.+)', _alt)
            if match is None:
                _alt = _alt
            else:
                _alt = match.group(1)
            _img_data.append({
                'image_url':img.attrib['src'],
                'label':_alt,
                'uri':'https://m.momoshop.com.tw'+img.getparent().attrib['href']
            })
            if idx > 4:
                break
        #end loop

    #endif
    return _img_data

def getmomo_top30(category):

    target_url = 'https://m.momoshop.com.tw/category.momo?cn={}&top30=y&imgSH=fourCardStyle'.format(category_set[random.randint(0, len(category_set)-1)])
    print(target_url)
    headers = {
           'accept-encoding': 'gzip, deflate, br', 
           'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7', 
           'Cache-Control': 'no-cache',
           'pragma': 'no-cache',
           'Upgrade-Insecure-Requests': '1',
           'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
           'content-type': 'application/x-www-form-urlencoded',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'cookie':''
           }

    # handle request body
    try:
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url=target_url, headers=headers, timeout=5)
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        return []
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        return []
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print(e)
        return []
    
    html = etree.HTML(response.text)
    _imgs = html.xpath('//article[contains(@class, "prdListArea")]//li/a[not(@class="trackbtn")]/img[position()<3]')
    _img_data = []
    
    if len(_imgs) > 1:   
        for idx, img in enumerate(_imgs, start=0):
            _alt = img.attrib['alt']
            match = re.search(r'【.+】(.+)', _alt)
            if match is None:
                _alt = _alt
            else:
                _alt = match.group(1)
            _img_data.append({
                'image_url':img.attrib['org'],
                'label':_alt,
                'uri':'https://m.momoshop.com.tw'+img.getparent().attrib['href']
            })
            if idx > 4:
                break
        #end loop

    #endif
    return _img_data

def get_push_msg(img_data):

    if (len(img_data) > 0):
        _msg_columns = []
        for col in img_data:
            _msg_columns.append(CarouselColumn(
                thumbnail_image_url=col['image_url'],
#                title='',
                text=col['label'],
                actions=[
                    URITemplateAction(
                        label='去逛逛',
                        uri=col['uri']
                    )
                ]
            ))
                        
        #end for    

        return _msg_columns;
    #end if
    return None


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

#訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 取得個人資料
    profile = line_bot_api.get_profile(event.source.user_id)
    nameid = profile.display_name
    uid = profile.user_id
    global is_buy
    text = event.message.text

    print('uid: '+uid)
    print('name:'+nameid)
    print('is_buy:'+str(is_buy))
    print(text)

    # 買東西
    if text == '我要買東西':
        is_buy = True
        message = TextSendMessage(text='貓喵買啥:')
    # 傳送影片
    elif text == '我要看新聞':
        is_buy = False
        message =TextSendMessage( getNews())
    # 傳送位置
    elif text == '我要看發生地點':
        is_buy = False
        message = LocationSendMessage(
            title='消息地點',
            address='桃園',
            latitude=24.984210,
            longitude=121.293203
        )
    # 傳送貼圖
    elif text == '給我一個貼圖':
        is_buy = False
        random.seed()
        message = StickerSendMessage(
            package_id='{}'.format(random.randint(1, 5)),
            sticker_id='{}'.format(random.randint(1, 10))
        )
    elif text[0] == '買':
        text = text[1:]
        print('keyword={}'.format(text))
        _data = getmomo_search(text)
        _message_columns = get_push_msg(_data)
        message = None
        if (_message_columns is None):
            message = TextSendMessage(text='沒賣 {}'.format(text))
        else:
            message = TemplateSendMessage(
                alt_text=text,
                template=CarouselTemplate(
                    columns=_message_columns
                )
            )           
    elif text == 'top30':
        print('keyword={}'.format(text))
        _data = getmomo_top30(text)
        _message_columns = get_push_msg(_data)
        message = None
        if (_message_columns is None):
            message = TextSendMessage(text='沒 {}'.format(text))
        else:
            message = TemplateSendMessage(
                alt_text=text,
                template=CarouselTemplate(
                    columns=_message_columns
                )
            ) 
    elif is_buy:
        print('keyword={}'.format(text))
        _data = getmomo_search(text)
        _message_columns = get_push_msg(_data)
        message = None
        if (len(_message_columns) == 0):
            message = TextSendMessage(text='沒賣 {}'.format(text))
        else:
            message = TemplateSendMessage(
                alt_text=text,
                template=CarouselTemplate(
                    columns=_message_columns
                )
            )           
    else:
        message = TextSendMessage(text='貓喵@#$:{}'.format(text))
        
    print('is_buy:'+str(is_buy))
    line_bot_api.reply_message(event.reply_token,message)


if __name__ == '__main__':
    app.run(debug=True)