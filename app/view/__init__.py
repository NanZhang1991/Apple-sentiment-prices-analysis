# -*- coding: utf-8 -*-
from flask import Blueprint

price_index = Blueprint("price_index", __name__, template_folder='../templates')

sentiments= Blueprint("sentiments", __name__, template_folder='../templates')

