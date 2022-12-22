#!/usr/bin/env python3

import threading
from random import randint
from flask import Flask, jsonify

app = Flask(__name__)
USER_ID = {}


@app.route('/vk_id/<username>', methods=['GET'])
def get_user_id(username):
    if username:
        if username not in USER_ID:
            user_id = randint(9999, 99999)
            USER_ID[username] = user_id
        return jsonify({'vk_id': USER_ID[username]}), 200
    else:
        return jsonify({}), 404


def run_mock():
    server = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': '5000'})

    server.start()
    return server


if __name__ == '__main__':
    run_mock()
