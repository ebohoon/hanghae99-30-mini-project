from flask import Flask, render_template, jsonify, request, flash, session
app = Flask(__name__)

#테스트 improt
from bson.json_util import dumps
import json

##파이 몽고 DB
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.LYAlbum

#엘범 리스트 DB
# db.album.insert_one(doc)

#리뷰 리스트 DB
# db.review.insert_one(doc)

app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = '이걸보다니.. 대단한걸?'

@app.route('/')
def home():
    return render_template('index.html')

##해더
@app.route('/header')
def header():
    return render_template('header.html')

##푸터
@app.route('/footer')
def footer():
    return render_template('footer.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/albumdata', methods=['GET'])
def albumdata():
    sample_receive = request.args.get('sample_give')
    if sample_receive is None:
        return render_template('albumdata.html')
    else:
        sample_receive = request.args.get('sample_give')
        print(sample_receive)
        data = sample_receive
        return render_template('albumdata.html', msg = "일단 연결은 되네", data = data)
    

@app.route('/albumdata/find', methods=['POST'])
def find_orderlist():
    titlere = request.form['sample_give']
    albumliset = list(db.album.find({"albumtitle": titlere},{'_id':False}))
    print(albumliset)
    return jsonify({'msg':albumliset})


#엘범 정보 크롤링 만들예정인 공간
@app.route('/temptestdo', methods=["GET", "POST"])
def 크롤링():
    
    testlist = [("test","testdo"),("test2","testdo2")]

    doc = {
        'albumtitle': "Butter",         ## 앨범 타이틀
        'albumimage': "http://sdfsdj",         ## 앨범 이미지
        'artist': "방탄",                ## 가수명
        'date': "2021.09.15",               ## 앨범 발매일
        'genre': "랩",                    ## 앨범 장르
        'agency': "카카오",                 ## 앨범 기획사
        'publisher': "어딜까",              ## 앨범 발매사
        'singlist': testlist              ## 앨범 곡리스트
    }

    db.album.insert_one(doc)
    flash("더미데이터 입력완료")
    return render_template('index.html')
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)