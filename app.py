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

@app.route('/albumlist')
def albumlist():
    return render_template('albumlist.html')

#엘범 정보 크롤링 만들예정인 공간
def 크롤링():
    doc = {
        'albumtitle':title,             ## 앨범 타이틀
        'albumimage':image,             ## 앨범 이미지
        'artist': artist,               ## 가수명
        'date':desc,                    ## 앨범 발매일
        'genre':url_receive,            ## 앨범 장르
        'agency':comment_receive,       ## 앨범 기획사
        'singlist':singlist             ## 앨범 곡리스트
    }

    db.album.insert_one(doc)
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)