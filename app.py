# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 01:00:17 2018

@author: linzino
"""

import requests
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

def getmomo(keyword):

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
        response = requests.get(url=target_url, headers=headers)
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
            _img_data.append({
                'image_url':img.attrib['src'],
                'label':img.attrib['alt'][:12],
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
            _msg_columns.append(ImageCarouselColumn(
                        image_url=col['image_url'],
                        action=URITemplateAction(
                            label=col['label'],
                            uri=col['uri']
                        )
                    )
                )
        #end for    

        return _msg_columns;
    #end if
    return null;
#end def


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

    print('uid: '+uid)
    print('name:'+nameid)
    print('event.message.text:'+type(event.message.text))

    # 傳送圖片
    if event.message.text == '買東西':
        is_buy = True
        message = TextSendMessage(text='喵買啥:')
#    elif event.message.text == '買東西':
#        message = ImageSendMessage(
#            original_content_url='https://i.imgur.com/vxQMxtm.png',
#            preview_image_url='https://i.imgur.com/vxQMxtm.png'
#        )
    # 傳送影片
    elif event.message.text == '試試看影片':
        is_buy = False
        message = VideoSendMessage(
            original_content_url='https://i.imgur.com/hOKAE06.mp4',
            preview_image_url='https://i.imgur.com/hOKAE06.mp4'
        )
    # 傳送位置
    elif event.message.text == '我要看發生地點':
        is_buy = False
        message = LocationSendMessage(
            title='消息地點',
            address='桃園',
            latitude=24.984210,
            longitude=121.293203
        )
    # 傳送貼圖
    elif event.message.text == '給我一個貼圖':
        is_buy = False
        message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )
    # 傳送組圖訊息
#    elif event.message.text == '我要看報紙':
#        message = ImagemapSendMessage(
#            base_url='https://i.imgur.com/PjvwT6d.png',
#            alt_text='Imagemap',
#            base_size=BaseSize(height=1040, width=1040),
#            actions=[
#                URIImagemapAction(
#                    link_uri='https://tw.appledaily.com/',
#                    area=ImagemapArea(
#                        x=0, y=0, width=520, height=1040
#                    )
#                ),
#                MessageImagemapAction(
#                    text='您需要付費喔！',
#                    area=ImagemapArea(
#                        x=520, y=0, width=520, height=1040
#                    )
#                )
#            ]
#        )
#    # 傳送確認介面訊息
#    elif event.message.text == '我想要評分':
#        message = TemplateSendMessage(
#            alt_text='你覺得這個機器人方便嗎？',
#            template=ConfirmTemplate(
#                text='你覺得這個機器人方便嗎？',
#                actions=[
#                    MessageTemplateAction(
#                        label='很棒！',
#                        text='ＧＯＯＤ'
#                    ),
#                    MessageTemplateAction(
#                        label='有待加強',
#                        text='ＢＡＤ'
#                    )
#                ]
#            )
#        )
#        # 傳送按鈕介面訊息
#    elif event.message.text == '新聞預警':
#        message = TemplateSendMessage(
#            alt_text='Buttons template',
#            template=ButtonsTemplate(
#                thumbnail_image_url='https://i.imgur.com/vkqbLnz.png',
#                title='Menu',
#                text='Please select',
#                actions=[
#                    MessageTemplateAction(
#                        label='發生地點',
#                        text='我要看發生地點'
#                    ),
#                    MessageTemplateAction(
#                        label='文字雲週報',
#                        text='我要看文字雲週報'
#                    ),
#                    URITemplateAction(
#                        label='Uri',
#                        uri='https://tw.appledaily.com/local/realtime/20180817/1412804'
#                    )
#                ]
#            )
#        )
#    # 傳送多重按鈕介面訊息
#    elif event.message.text == '所有功能':
#        message = TemplateSendMessage(
#            alt_text='Carousel template',
#            template=CarouselTemplate(
#                columns=[
#                    CarouselColumn(
#                        thumbnail_image_url='https://i.imgur.com/vkqbLnz.png',
#                        title='新聞預警',
#                        text='新聞來源-蘋果新聞',
#                        actions=[
#                            MessageTemplateAction(
#                                label='發生地點',
#                                text='我要看發生地點'
#                            ),
#                            MessageTemplateAction(
#                                label='文字雲週報',
#                                text='我要看文字雲週報'
#                            ),
#                            URITemplateAction(
#                                label='Uri',
#                                uri='https://tw.appledaily.com/local/realtime/20180817/1412804'
#                            )
#                        ]
#                    ),
#                    CarouselColumn(
#                        thumbnail_image_url='https://i.imgur.com/Dt97YFG.png',
#                        title='其他功能',
#                        text='這裡存放各種功能！',
#                        actions=[
#                            MessageTemplateAction(
#                                label='為機器人評分',
#                                text='我想要評分'
#                            ),
#                            MessageTemplateAction(
#                                label='更多新聞',
#                                text='我要看報紙'
#                            ),
#                            MessageTemplateAction(
#                                label='放鬆一下',
#                                text='給我一個貼圖'
#                            )
#                        ]
#                    )
#                ]
#            )
#        )
#    # 傳送多重圖片訊息
#    elif event.message.text == '10':
#        message = TemplateSendMessage(
#            alt_text='ImageCarousel template',
#            template=ImageCarouselTemplate(
#                columns=[
#                    ImageCarouselColumn(
#                        image_url='https://i.imgur.com/N3oQXjW.png',
#                        action=PostbackTemplateAction(
#                            label='postback1',
#                            text='postback text1',
#                            data='action=buy&itemid=1'
#                        )
#                    ),
#                    ImageCarouselColumn(
#                        image_url='https://i.imgur.com/OBdCHB9.png',
#                        action=PostbackTemplateAction(
#                            label='postback2',
#                            text='postback text2',
#                            data='action=buy&itemid=2'
#                        )
#                    )
#                ]
#            )
#        )
    elif event.message.text[0] == '買':
         print('keyword={}'.format(event.message.text[1:]))
        _cols = getmomo(event.message.text[1:])
        message = get_push_msg(_cols)
        if (message is None):
            message = TextSendMessage(text='買沒:{}'.format(event.message.text[1:]))       
    elif is_buy:
        print('keyword={}'.format(event.message.text))
        _cols = getmomo(event.message.text)
        message = get_push_msg(_cols)
        if (message is None):
            message = TextSendMessage(text='買沒:{}'.format(event.message.text))
    else:
        message = TextSendMessage(text='肥貓喵:{}'.format(event.message.text))
        
    line_bot_api.reply_message(event.reply_token,message)


if __name__ == '__main__':
    app.run(debug=True)