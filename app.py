from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

##파이 몽고 DB
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.LYAlbum

#엘범 리스트 DB
# db.album.insert_one(doc)

#리뷰 리스트 DB
# db.review.insert_one(doc)



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


@app.route('/albumdata')
def albumdata():
    return render_template('albumdata.html')

#엘범 정보 크롤링 만들예정인 공간
@app.route('/temptestdo')
def 크롤링():
    doc = {
        'albumtitle': "타이틀이름!",         ## 앨범 타이틀
        'albumimage': "이미지 이름",         ## 앨범 이미지
        'artist': "가수이름",                ## 가수명
        'date': "2021.09.15",               ## 앨범 발매일
        'genre': "장르",                    ## 앨범 장르
        'agency': "기획사",                 ## 앨범 기획사
        'singlist': "곡리스트"              ## 앨범 곡리스트
    }

    db.album.insert_one(doc)
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)