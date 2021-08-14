import requests
import json
import poet
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
app=Flask(__name__) #__name__代表目前執行的模組
CORS(app)

@app.route("/") #函式的裝飾
def index():
    return render_template("index.html")

"""
@app.route("/", methods=["POST"]) #函式的裝飾
def index():
    # 取得前端傳過來的數值
    insertValues = request.get_json()
    heading = insertValues['keyin']
    result = poet.get_hidden_poetry(heading)
    return render_template("index.html"), jsonify(result)
    #return render_template("index.html")
    
"""

@app.route("/", methods=["POST"])
def postInput():
    # 取得前端傳過來的數值
    insertValues = request.get_json()
    heading = insertValues['keyin']
    result = poet.get_hidden_poetry(heading)
    return jsonify(result)


if __name__=="__main__": #如果以主程式執行
    app.run(debug=True) #立刻啟動伺服器