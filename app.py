import sys
import logging
import json
import eventlet
import redis

from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


app = Flask(__name__)


socketio = SocketIO(app, async_mode='eventlet')


pubsub = redis.Redis().pubsub(ignore_subscribe_messages=True)
pubsub.subscribe('wincam-detector')


def worker():
    while True:
        message = pubsub.get_message()
        if message:
            socketio.emit('state', message['data'], namespace='/')
        eventlet.sleep(0.1)
eventlet.spawn(worker)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app)
