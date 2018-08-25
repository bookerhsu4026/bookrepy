# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 01:00:17 2018

@author: linzino
"""


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

line_bot_api.push_message('Ube6a1a56c1466ec56cee2ae59ca0b17b', TextSendMessage(text='你可以開始了'))

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

    print('uid: '+uid)
    print('name:'+nameid)

    # 傳送圖片
    if event.message.text == '我要看文字雲週報':
        message = ImageSendMessage(
            original_content_url='https://i.imgur.com/vxQMxtm.png',
            preview_image_url='https://i.imgur.com/vxQMxtm.png'
        )
    # 傳送影片
    elif event.message.text == '試試看影片':
        message = VideoSendMessage(
            original_content_url='https://i.imgur.com/hOKAE06.mp4',
            preview_image_url='https://i.imgur.com/hOKAE06.mp4'
        )
    # 傳送位置
    elif event.message.text == '我要看發生地點':
        message = LocationSendMessage(
            title='消息地點',
            address='桃園',
            latitude=24.984210,
            longitude=121.293203
        )
    # 傳送貼圖
    elif event.message.text == '給我一個貼圖':
        message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )
    # 傳送組圖訊息
    elif event.message.text == '我要看報紙':
        message = ImagemapSendMessage(
            base_url='https://i.imgur.com/PjvwT6d.png',
            alt_text='Imagemap',
            base_size=BaseSize(height=1040, width=1040),
            actions=[
                URIImagemapAction(
                    link_uri='https://tw.appledaily.com/',
                    area=ImagemapArea(
                        x=0, y=0, width=520, height=1040
                    )
                ),
                MessageImagemapAction(
                    text='您需要付費喔！',
                    area=ImagemapArea(
                        x=520, y=0, width=520, height=1040
                    )
                )
            ]
        )
    # 傳送確認介面訊息
    elif event.message.text == '我想要評分':
        message = TemplateSendMessage(
            alt_text='你覺得這個機器人方便嗎？',
            template=ConfirmTemplate(
                text='你覺得這個機器人方便嗎？',
                actions=[
                    MessageTemplateAction(
                        label='很棒！',
                        text='ＧＯＯＤ'
                    ),
                    MessageTemplateAction(
                        label='有待加強',
                        text='ＢＡＤ'
                    )
                ]
            )
        )
        # 傳送按鈕介面訊息
    elif event.message.text == '新聞預警':
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/vkqbLnz.png',
                title='Menu',
                text='Please select',
                actions=[
                    MessageTemplateAction(
                        label='發生地點',
                        text='我要看發生地點'
                    ),
                    MessageTemplateAction(
                        label='文字雲週報',
                        text='我要看文字雲週報'
                    ),
                    URITemplateAction(
                        label='Uri',
                        uri='https://tw.appledaily.com/local/realtime/20180817/1412804'
                    )
                ]
            )
        )
    # 傳送多重按鈕介面訊息
    elif event.message.text == '所有功能':
        message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/vkqbLnz.png',
                        title='新聞預警',
                        text='新聞來源-蘋果新聞',
                        actions=[
                            MessageTemplateAction(
                                label='發生地點',
                                text='我要看發生地點'
                            ),
                            MessageTemplateAction(
                                label='文字雲週報',
                                text='我要看文字雲週報'
                            ),
                            URITemplateAction(
                                label='Uri',
                                uri='https://tw.appledaily.com/local/realtime/20180817/1412804'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/Dt97YFG.png',
                        title='其他功能',
                        text='這裡存放各種功能！',
                        actions=[
                            MessageTemplateAction(
                                label='為機器人評分',
                                text='我想要評分'
                            ),
                            MessageTemplateAction(
                                label='更多新聞',
                                text='我要看報紙'
                            ),
                            MessageTemplateAction(
                                label='放鬆一下',
                                text='給我一個貼圖'
                            )
                        ]
                    )
                ]
            )
        )
    # 傳送多重圖片訊息
    elif event.message.text == '10':
        message = TemplateSendMessage(
            alt_text='ImageCarousel template',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/N3oQXjW.png',
                        action=PostbackTemplateAction(
                            label='postback1',
                            text='postback text1',
                            data='action=buy&itemid=1'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/OBdCHB9.png',
                        action=PostbackTemplateAction(
                            label='postback2',
                            text='postback text2',
                            data='action=buy&itemid=2'
                        )
                    )
                ]
            )
        )
    else:
        message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)


if __name__ == '__main__':
    app.run(debug=True)