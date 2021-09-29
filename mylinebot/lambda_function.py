import os
import sys
import random
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,FollowEvent
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
import logging

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    logger.error('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    logger.error('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
hands=['グー', 'チョキ', 'パー']

def lambda_handler(event, context):
    if "x-line-signature" in event["headers"]:
        signature = event["headers"]["x-line-signature"]
    elif "X-Line-Signature" in event["headers"]:
        signature = event["headers"]["X-Line-Signature"]
    body = event["body"]
    ok_json = {"isBase64Encoded": False,
               "statusCode": 200,
               "headers": {},
               "body": ""}
    error_json = {"isBase64Encoded": False,
                  "statusCode": 500,
                  "headers": {},
                  "body": "Error"}
    
    @handler.add(FollowEvent)
    def handle_follow(line_event):
        
        line_bot_api.reply_message(
            line_event.reply_token,
            TextSendMessage(text='ジャンケンしようぜ。手を入力してください（0:グー 1:チョキ 2:パー)')
        )
    p=0
    m=0
    
    @handler.add(MessageEvent, message=TextMessage)
    def message(line_event):
        text = line_event.message.text   
        if text!='0'and text!='1' and text!='2':
            line_bot_api.reply_message(line_event.reply_token,TextSendMessage(text='ジャンケンしようぜ。手を入力してください。（0:グー 1:チョキ 2:パー)'))
        else :
            p=int(text)
            player=hands[p]
            line_bot_api.reply_message(line_event.reply_token,TextSendMessage(text=("あなたは"+player+"を出したね")))
            m=random.randint(0,2)
            com=hands[m]
            line_bot_api.push_message(line_event.source.user_id,TextSendMessage(text=("相手は"+com+"を出した")))

            if (p-m+3)%3==0 :
                line_bot_api.push_message(
                line_event.source.user_id,
                TextSendMessage(text="あいこです。もう一度。（0:グー 1:チョキ 2:パー)")
                )
            elif (p-m)%3==2:
                line_bot_api.push_message(
                line_event.source.user_id,
                TextSendMessage(text="勝ち!!")
                )   
            elif (p-m+3)%3==1:
                line_bot_api.push_message(
                line_event.source.user_id,
                TextSendMessage(text="負け!!")
                )


    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        logger.error("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            logger.error("  %s: %s" % (m.property, m.message))
        return error_json
    except InvalidSignatureError:
        return error_json

    return ok_json