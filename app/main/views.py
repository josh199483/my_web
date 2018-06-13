"""
建立時間: 2018
作者: Tony
說明:
    多語言機制
"""

from flask import session, request, session
from .. import babel
from . import main
from ..models.mongodb import Basic

@main.before_request   
def version():
    # session['logo'] = Basic.getBasicData('logo')['value'] 
    session['version'] = 1.03

# 每次收到request之後執行
# 在每個response之前新增header關閉快取記錄
@main.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

# query: 每次頁面請求時, 都詢問語系「session['lang']」; 若無, 則使用預設的 「lang = 'zh'」
@babel.localeselector
def get_locale(): # 切換語系 
    lang = 'zh'
    if 'lang' in session:
        return session['lang']
    else:
        return lang

# update: 更改語系, 將 lang 存入 「session['lang']」中
@main.route('/changeLanguage')
def changeLanguage(): # 點選語言, 回傳切換後的語系 
    lang = request.args.to_dict()['lang']
    session['lang'] = lang
    return lang
