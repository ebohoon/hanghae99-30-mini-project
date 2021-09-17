from flask import Flask, render_template, jsonify, request, flash, session

app = Flask(__name__)

# 테스트 improt
from bson.json_util import dumps
import json

##파이 몽고 DB
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.LYAlbum

# 엘범 리스트 DB
# db.album.insert_one(doc)

# 리뷰 리스트 DB
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
        return render_template('albumdata.html', msg="일단 연결은 되네", data=data)


@app.route('/albumdata/find', methods=['POST'])
def find_alumdatalist():
    titlere = request.form['sample_give']
    albumliset = list(db.album.find({"albumtitle": titlere}, {'_id': False}))
    print(albumliset)
    return jsonify({'msg': albumliset})


@app.route('/albumdata/reviewfind', methods=['POST'])
def find_reviewlist():
    titlere = request.form['sample_give']
    albumliset = list(db.review.find({"albumtitle": titlere}, {'_id': False}))
    print(albumliset)
    return jsonify({'msg': albumliset})


@app.route('/albumlist')
def albumlist():
    return render_template('albumlist.html')

@app.route('/albumreview')
def albumreview():
    return render_template('albumreview.html')

# 앨범리뷰쓰기 API
@app.route('/write', methods=['POST'])
def reviewWrite():
    name_receive = request.form['name_give']
    oneReview_receive = request.form['oneReview_give']
    rate_receive = request.form['rate_give']
    detailReview_receive = request.form['detailReview_give']

    doc = {
        'name': name_receive,               # name_receive
        'oneReview': oneReview_receive,          # oneReview_receive
        'rate': rate_receive,                 # rate_receive
        'detailReview': detailReview_receive   # detailReview_receive
    }
    db.review.insert_one(doc)
    return jsonify({'msg': '리뷰를 작성했습니다!'})

# 앨범리뷰삭제 API
# @app.route('/delete', methods=['POST'])
# def reviewDelete():
#     name_receive = request.form['name_give']
#     db.review.delete_one({'name': name_receive})
#     return jsonify({'msg': '삭제한 내용은 다시 되돌릴 수 없습니다. 그래도 삭제 하시겠습니까?'})

# 앨범리스트 API
@app.route('/listing', methods=['GET'])
def listing():
    album = list(db.album.find({}, {'_id': False}))
    return jsonify({'album': album})

# 앨범리스트 리뷰 보기 API
@app.route('/review', methods=['GET'])
def show_review():
    sample_receive = request.args.get('sample_give')
    print(sample_receive)
    return jsonify({'msg': '리뷰를 보러 가볼까요?'})

# 앨범리스트 리뷰 작성 API
@app.route('/review', methods=['POST'])
def make_review():
    return jsonify({'msg': '리뷰를 쓰러 가볼까요?'})

    flash("더미데이터 입력완료")
    return render_template('index.html')


# 엘범 정보 크롤링 만들예정인 공간
@app.route('/temptestdo', methods=["GET", "POST"])
def 크롤링():
    testlist = [("test", "testdo"), ("test2", "testdo2")]

    doc = {
        'albumtitle': "Butter",  ## 앨범 타이틀
        'albumimage': "http://sdfsdj",  ## 앨범 이미지
        'artist': "방탄",  ## 가수명
        'date': "2021.09.15",  ## 앨범 발매일
        'genre': "랩",  ## 앨범 장르
        'agency': "카카오",  ## 앨범 기획사
        'publisher': "어딜까",  ## 앨범 발매사
        'singlist': testlist  ## 앨범 곡리스트
    }

    db.album.insert_one(doc)
    flash("더미데이터 입력완료")
    return render_template('index.html')


## 리뷰 더미데이터 생성
@app.route('/temptestdo11', methods=["GET", "POST"])
def 리뷰더미데이터():
    doc = {
        'review': "BTS최고다!",  # 한줄평
        'nickname': "도도",  # 닉네임
        'rete': "3",  # 별점
        'date': "2021.09.15",  # 리뷰 날짜
        'morereview': "랩",  # 리뷰
        'albumtitle': "Butter"  # 해당 엘범타이틀
    }

    db.review.insert_one(doc)
    flash("더미데이터 입력완료")
    return render_template('index.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
