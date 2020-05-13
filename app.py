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

ACCESS_TOKEN = "UKMyofIFSpSLi1Ag5saBzSp4yHYtChPr" \
               "Cv9z9b3e3AYx2uvaDib/s21uV3axVER" \
               "Q6GM5WjbDS4kTV+QBP2R3Y3Hkd7PgZOhy+TYZOPac" \
               "RK7+si+UagkvvbWOgjpFJQ6IH+YrB797dPd5G" \
               "ZqiChA1qAdB04t89/1O/w1cDnyilFU="
SECRET = "d4295de78cd39c615fb7783d78ed9076"

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)


@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

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