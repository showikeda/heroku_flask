from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)


app = Flask(__name__)

ACCESS_TOKEN = 'ThEtSeZxHCbGW6sBSxKmfFNh5fLgKmGD1EBpx5' \
               '00p/uxETHM/sNcZ7QlnCNx3+166GM5WjbDS4kTV+QB' \
               'P2R3Y3Hkd7PgZOhy+TYZOPacRK7dTb+19jXWnyUhIS' \
               'oTQROP8zFJkceANdWEPo+UwTHrqwdB04t89/1O/w1cDnyilFU='
SECRET = 'd4295de78cd39c615fb7783d78ed9076'

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )


if __name__ == '__main__':
    app.run()
