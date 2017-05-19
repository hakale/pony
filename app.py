#!/usr/bin/env python
from flask import Flask, render_template, request, make_response, send_file
from io import StringIO, BytesIO
import os
from time import ctime
import qrcode
import json
import base64
app = Flask('arukasUpdate')


@app.route('/get_file', methods=['GET', 'POST'])
def get_file():
    return send_file('./gui-config.json')


@app.route('/get_qr_image', methods=['POST', 'GET'])
def get_qr_image():
    data = request.args.get('data')
    img = qrcode.make(data)
    img_io = BytesIO()
    img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    response = send_file(img_io, mimetype='image/jpeg')
    return response

@app.route('/')
def root():
    update_time = os.stat('gui-config.json').st_mtime
    update_time = ctime(update_time)
    with open('gui-config.json') as f:
        data = json.load(f)
    data = data['configs']
    print('load config...')
    urls=[]
    for d in data:
        method = d['method']
        password = d['password']
        hostname = d['server']
        port = d['server_port']
        st = ''.join([method, ':', password, '@', hostname, ':', str(port)]).encode('utf-8')
        url = 'ss://' + base64.b64encode(st).decode('utf-8')
        urls.append({
            'ip': hostname,
            'url':url,
            'img_url': '/get_qr_image?data=' + url})
    print('Select finish...')
    return render_template('index.html', data=urls, update_time=update_time)
    

if __name__ == '__main__':
    DEBUG = True
    SECRET_KEY = 'development key'
    app.config.from_object(__name__)
    app.run(host='0.0.0.0', port=8080)