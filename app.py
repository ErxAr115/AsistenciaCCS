from flask import Flask
from chat_routes import chat

app = Flask(__name__)

app.register_blueprint(chat)

if __name__ == '__main__':
    app.run(debug = True)