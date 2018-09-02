# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 01:00:17 2018

@author: linzino
"""

import requests, re, feedparser, random
from lxml import etree
from flask import Flask, request, abort
#from chatterbot import ChatBot

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    URITemplateAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton
)

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('cXtIw9d8+oQbrXZ/3hEBocCNTpsroaNVWid2LiVlekEa8jnhW2CnKAKqfXvhWPUFGaLa81z7sYmUtCy+C5pXyYTW5ePpp+fRB8SbdwgoIPHwoQgNejTUnD4J+VTw4jUJ4DoZtkPR0NGwKBpUcslbmQdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('7e27ba98cfbaa7d09bef1435b55deb5f')

#line_bot_api.push_message('Ube6a1a56c1466ec56cee2ae59ca0b17b', TextSendMessage(text='你可以開始了'))
is_buy = False
#category
category_set = ('1900000000',
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
        '3500000000')

# 建立一個 ChatBot 物件
#chatbot = ChatBot(
#    'Ron Obvious',
#    trainer = 'chatterbot.trainers.ChatterBotCorpusTrainer'
#)

# 基於英文的自動學習套件
#chatbot.train("chatterbot.corpus.english")

def getNews():
    """
    建立一個抓最新消息的function
    """
    rss_url = 'http://feeds.feedburner.com/cnaFirstNews'
    # 抓取資料
    rss = feedparser.parse(rss_url)
#    # 抓取第一個文章標題
#    title = rss['entries'][0]['title']
#    # 抓取第一個文章標題
#    link = rss.entries[0]['link']
#    
#    tmp = title + ' ' +link
    tmp = []
    for i, entry in enumerate(rss.entries, start=0):
        tmp.append(entry['title'] + ' ' + entry['link'])
        if i > 3:
            break
    
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
        for img in _imgs:
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
        #end loop

    #endif
    return _img_data

def getmomo_top30(category):

    target_url = 'https://m.momoshop.com.tw/category.momo?cn={}&top30=y&imgSH=fourCardStyle'.format(category)
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
        for img in _imgs:
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
        #end loop

    #endif
    return _img_data

def get_push_msg(img_data):

    if (len(img_data) > 0):
        _msg_columns = []
        for idx, col in enumerate(img_data, start=0):
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
                
            if idx > 8:
                break
                        
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
def handle_text_message(event):
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
        text_message = getNews()
        message =[TextSendMessage(text_message[i]) for i in range(0,len(text_message)-1)]
    # 傳送貼圖
    elif text == '給我一個貼圖':
        is_buy = False
        package_id = random.randint(1, 2)
        sticker_id = 1
        if package_id == '1':
            sticker_id = random.randint(1, 88)
            if sticker_id > 17:
                sticker_id = sticker_id + 83
            if sticker_id > 139:
                sticker_id = sticker_id + 262
        else:
            sticker_id = random.randint(18, 114)
            if sticker_id < 17:
                sticker_id = sticker_id + 17
            if sticker_id > 47:
                sticker_id = sticker_id + 93
            if sticker_id > 179:
                sticker_id = sticker_id + 313
                
#        sticker_id = '{}'.format(sticker_id)
        print('package_id: '+str(package_id))
        print('sticker_id:'+str(sticker_id))
        message = StickerSendMessage(
            package_id=package_id,
            sticker_id=sticker_id
        )
    elif text[0] == '買':
        text = text[1:]
        print('keyword={}'.format(text))
        _data = getmomo_search(text)
        _message_columns = get_push_msg(_data)
        message = None
        if _message_columns is None:
#            message = TextSendMessage(text='沒賣 {}'.format(text))
            message = StickerSendMessage(
                    package_id=2,
                    sticker_id=152
                )
        else:
            message = TemplateSendMessage(
                alt_text=text,
                template=CarouselTemplate(
                    columns=_message_columns
                )
            )           
    elif text == 'top30':
        print('keyword={}'.format(text))
        _data = getmomo_top30(list(category_set)[random.randint(0, len(category_set)-1)])
        _message_columns = get_push_msg(_data)
        message = None
        if _message_columns is None:
#            message = TextSendMessage(text='沒 {}'.format(text))
            message = StickerSendMessage(
                    package_id=1,
                    sticker_id=420
                )
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
        if _message_columns is None:
#            message = TextSendMessage(text='沒賣 {}'.format(text))
            message = StickerSendMessage(
                    package_id=2,
                    sticker_id=39
                )
        else:
            message = TemplateSendMessage(
                alt_text=text,
                template=CarouselTemplate(
                    columns=_message_columns
                )
            )           
    else:
        response_message = text #chatbot.get_response(message)
        message = TextSendMessage(text='貓喵@#$:{}'.format(response_message))
        
    print('is_buy:'+str(is_buy))
    line_bot_api.reply_message(event.reply_token,message)

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=1,
            sticker_id=406)
    )

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        LocationSendMessage(
            title=event.message.title, address=event.message.address,
            latitude=event.message.latitude, longitude=event.message.longitude
        )
    )

# Other Message Type
@handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage))
def handle_content_message(event):
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
    elif isinstance(event.message, VideoMessage):
        ext = 'mp4'
    elif isinstance(event.message, AudioMessage):
        ext = 'm4a'
    else:
        return

#    message_content = line_bot_api.get_message_content(event.message.id)
#    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
#        for chunk in message_content.iter_content():
#            tf.write(chunk)
#        tempfile_path = tf.name
#
#    dist_path = tempfile_path + '.' + ext
#    dist_name = os.path.basename(dist_path)
#    os.rename(tempfile_path, dist_path)
#
#    line_bot_api.reply_message(
#        event.reply_token, [
#            TextSendMessage(text='Save content.'),
#            TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
#        ])


@handler.add(MessageEvent, message=FileMessage)
def handle_file_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
#    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix='file-', delete=False) as tf:
#        for chunk in message_content.iter_content():
#            tf.write(chunk)
#        tempfile_path = tf.name
#
#    dist_path = tempfile_path + '-' + event.message.file_name
#    dist_name = os.path.basename(dist_path)
#    os.rename(tempfile_path, dist_path)
#
#    line_bot_api.reply_message(
#        event.reply_token, [
#            TextSendMessage(text='Save file.'),
#            TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
#        ])

@handler.add(FollowEvent)
def handle_follow(event):

    profile = line_bot_api.get_profile(event.source.user_id)
    nameid = profile.display_name
    uid = profile.user_id

    print('follow uid: '+uid+', name:'+nameid)
    
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='Got follow'))


@handler.add(UnfollowEvent)
def handle_unfollow():
    app.logger.info("Got Unfollow")


@handler.add(JoinEvent)
def handle_join(event):
    
    profile = line_bot_api.get_profile(event.source.user_id)
    nameid = profile.display_name
    uid = profile.user_id

    print('join uid: '+uid+', name:'+nameid)
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Joined this ' + event.source.type))

@handler.add(LeaveEvent)
def handle_leave():
    app.logger.info("Got leave")


if __name__ == '__main__':
    app.run(debug=True)