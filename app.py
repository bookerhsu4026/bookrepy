# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 01:00:17 2018

@author: linzino
"""

import requests, re, feedparser, random
import urllib
from lxml import etree
from flask import Flask, request, abort
from concurrent.futures import ThreadPoolExecutor

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
    URITemplateAction, MessageTemplateAction,
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

headers = {
       'accept-encoding': 'gzip, deflate, br', 
       'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7', 
       'Cache-Control': 'no-cache',
       'pragma': 'no-cache',
       'Upgrade-Insecure-Requests': '1',
       'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
       'content-type': 'application/x-www-form-urlencoded',
       'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
       'cookie':''
       }

CWB_AUTHED_KEY = 'CWB-2D440B6F-B34D-4763-A117-B7763E4B84F2'

executor = ThreadPoolExecutor(3)


def get_news_push(userid):
    """
    建立一個抓最新消息的function
    """
    print('uid: '+userid)
    rss_url = 'http://feeds.feedburner.com/cnaFirstNews'
    # 抓取資料
    rss = feedparser.parse(rss_url)
#    
#    tmp = title + ' ' +link
    tmp = []
    for i, entry in enumerate(rss.entries[:5], start=0):
        tmp.append(entry['title'] + ' ' + entry['link'])
    #end if
    
    if (len(tmp)>0):
        message =TextSendMessage("\n".join(tmp))
        line_bot_api.push_message(userid, message)
    #end if
    print('get_news_push: end')

def get_current_weather(city,userid):
    """
    Get current weather in specific city.

    Args:
        city: City Name

    Returns:
        Current weather string
    """
    response = urllib.request.urlopen('http://opendata.cwb.gov.tw/opendataapi?dataid=F-C0032-001&authorizationkey={}'.format(CWB_AUTHED_KEY))
    tree = etree.parse(response).getroot()

    for location in tree.findall('.//{urn:cwb:gov:tw:cwbcommon:0.1}location'):
        if city in location[0].text:
            # If the city is found, access its child direct.
            message = TextSendMessage(text='%s目前的天氣為%s。\n' \
                   '溫度為 %s 至 %s ℃，降雨機率為 %s %%。' \
                   % (location[0].text, location[1][1][2][0].text,
                      location[3][1][2][0].text, location[2][1][2][0].text,
                      location[5][1][2][0].text))
            
            line_bot_api.push_message(userid, message)
            return        

    message = TextSendMessage(text='很抱歉，無法提供您{}的天氣。'.format(city))
    line_bot_api.push_message(userid, message)

def getmomo_search_push(keyword,userid):
    print('uid: '+userid)
    print('keyword:'+keyword)           
    target_url = 'https://m.momoshop.com.tw/search.momo?searchKeyword={}&couponSeq=&searchType=1&cateLevel=-1&ent=k&_imgSH=fourCardStyle'.format(keyword)
    print(target_url)
    
    # handle request body
    try:
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url=target_url, headers=headers, timeout=15)
    except requests.exceptions.Timeout as tim:
        # Maybe set up for a retry, or continue in a retry loop
        print(tim)
        return
    except requests.exceptions.TooManyRedirects as man:
        # Tell the user their URL was bad and try a different one
        print(man)
        return
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print(e)
        return
    except requests.exceptions.HTTPError as err:
        print(err)
        return
  
    _html = etree.HTML(response.text)
    _imgs = _html.xpath('//article[contains(@class, "prdListArea")]//li[@class="goodsItemLi"]/a[not(@class="trackbtn")]/img[position()<3]')
    message = None
    
    if len(_imgs) > 0:   
        _columns = []
        for idx, img in enumerate(_imgs[:8], start=0):
            _title = img.attrib['title']
            match = re.search(r'【.+】(.+)', _title)
            if match is not None:
                _title = match.group(1)
            #end if
    
            _columns.append(CarouselColumn(
                    thumbnail_image_url=('https:'+img.attrib['src']) if 'http' not in img.attrib['src'] else img.attrib['src'],
        #                title='',
                    text=_title,
                    actions=[
                        URITemplateAction(
                            label='去逛逛',
                            uri=('https://m.momoshop.com.tw'+img.getparent().attrib['href']) if 'http' not in img.getparent().attrib['href'] else img.getparent().attrib['href']
                        )
                    ]
                )
            )
    
        #end for
        
        print(_columns)
    
        message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=_columns
            )
        )
    
        line_bot_api.push_message(userid, message)
    #end if
    print('getmomo_search_push:end')

def getmomo_top30_push(category,userid):
    print('uid: '+userid)
    print('category:'+category)
    target_url = 'https://m.momoshop.com.tw/category.momo?cn={}&top30=y&imgSH=fourCardStyle'.format(category)
    
    # handle request body
    try:
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url=target_url, headers=headers, timeout=15)
    except requests.exceptions.Timeout as tim:
        # Maybe set up for a retry, or continue in a retry loop
        print(tim)
        return
    except requests.exceptions.TooManyRedirects as man:
        # Tell the user their URL was bad and try a different one
        print(man)
        return
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print(e)
        return
    except requests.exceptions.HTTPError as err:
        print(err)
        return
      
    html = etree.HTML(response.text)
    _imgs = html.xpath('//article[@class="prdListArea"]//li//img[@class="goodsImg"]')
    message = None
    print(len(_imgs))
    if len(_imgs) > 0:   
        _carouse_columns = []
        for idx, img in enumerate(_imgs[:8], start=0):
            _alt = img.attrib['alt']
            match = re.search(r'【.+】(.+)', _alt)
            if match is not None:
                _alt = match.group(1)
            #end if
            print(img.attrib)

            _colu = CarouselColumn(
                thumbnail_image_url=('https:'+img.attrib['org']) if 'http' not in img.attrib['org'] else img.attrib['org'],
    #                title='',
                text=_alt,
                actions=[
                    URITemplateAction(
                        label='去看看',
                        uri=('https://m.momoshop.com.tw'+img.getparent().attrib['href']) if 'http' not in img.getparent().attrib['href'] else img.getparent().attrib['href']
                    )
                ]
            )
            _carouse_columns.append(_colu)
    
        #end for
        
        print(_carouse_columns)
       
        message = TemplateSendMessage(
            alt_text='Momo TOP30',
            template=CarouselTemplate(
                columns=_carouse_columns
            )
        )

        line_bot_api.push_message(userid, message)
    #end if
    print('getmomo_top30_push: end')

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

    elif text == '新聞':
        is_buy = False
        executor.submit(get_news_push,uid)

        message = StickerSendMessage(
                package_id=2,
                sticker_id=31
            )

    # 傳送貼圖
    elif text == '貼圖':
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

        print('package_id: '+str(package_id))
        print('sticker_id:'+str(sticker_id))
        message = StickerSendMessage(
            package_id=package_id,
            sticker_id=sticker_id
        )

    elif text[0] == '買':
        text = text[1:]
        print('keyword={}'.format(text))
        executor.submit(getmomo_search_push,text,uid)

        message = StickerSendMessage(
                package_id=2,
                sticker_id=31
            )
          
    elif text.lower() == 'top30':
        print('keyword={}'.format(text))
        executor.submit(getmomo_top30_push,category_set[random.randint(0, len(category_set)-1)],uid)

        message = StickerSendMessage(
                package_id=1,
                sticker_id=119
            )

    elif u'天氣' in text:
        print('keyword={}'.format(text))
        re_weather = re.compile(r"(\w+)天氣")
        city = re.match(re_weather,text)
        executor.submit(get_current_weather,re.sub(r"(縣|市)", "", re.sub(r"台", "臺", city.group(1))),uid)

        message = StickerSendMessage(
                package_id=2,
                sticker_id=25
            )     
    elif is_buy:
        print('keyword={}'.format(text))
        executor.submit(getmomo_search_push,text,uid)

        message = StickerSendMessage(
                package_id=2,
                sticker_id=22
            ) 
    elif text.isnumeric():
        print('stock_id={}'.format(text))

        message = StickerSendMessage(
                package_id=11539,
                sticker_id=52114112
            )
    else:
        response_message = text #chatbot.get_response(message)
        message = TextSendMessage(text='貓喵@#$:{}'.format(response_message))

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

@handler.add(MessageEvent, message=FileMessage)
def handle_file_message(event):
    mm = None

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
