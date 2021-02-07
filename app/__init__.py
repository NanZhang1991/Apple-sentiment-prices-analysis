# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, resources=r'/*')
@app.route('/')
def hello_world():
    return 'Hello World!'

app.debug = True

from .view.pri_i_view import price_index as price_index_blueprint
app.register_blueprint(price_index_blueprint, url_prefix='/price_index')  

from .view.sentiments_view import sentiments as sentiments_blueprint
app.register_blueprint(sentiments_blueprint, url_prefix='/sentiments')  