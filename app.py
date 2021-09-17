from flask import Flask, render_template, jsonify, request, flash, session
import jwt
import hashlib
import datetime

import requests

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


# @app.route('/')
# def home():
#     return render_template('index.html')


##해더
@app.route('/header')
def header():
    userid = session.get('logged_in')
    return render_template('header.html', userid=userid)


##푸터
@app.route('/footer')
def footer():
    return render_template('footer.html')


## 로그인 페이지로 이동
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        if session.get('logged_in'):
            userid = session.get('logged_in')
            return render_template('albumlist.html', userid=userid)

        return render_template('index.html')
    elif request.method == 'POST':
        userid = request.form.get("userid", type=str)
        pw = request.form.get("userPW", type=str)

        if userid == "":
            flash("아이디를 입력하세요")
            return render_template('index.html')
        elif pw == "":
            flash("비밀번호를 입력하세요")
            return render_template('index.html')
        else:
            users = db.users
            id_check = users.find_one({"id": userid})
            hapw = hashlib.sha256(pw.encode('utf-8')).hexdigest()

            if id_check is None:
                flash("아이디가 존재하지 않습니다.")
                return render_template('index.html')
            elif id_check["password"] == hapw:
                session["logged_in"] = userid
                return render_template('albumlist.html', userid=userid)
            else:
                flash("비밀번호가 틀렸습니다.")
                return render_template('index.html')


# 로그아웃
@app.route("/logout", methods=["GET"])
def logout():
    session.pop('logged_in', None)
    return render_template('index.html')


# 회원가입 페이지

@app.route('/register')
def sign_up_main():
    return render_template('register.html')


@app.route('/check_dup_name', methods=['POST'])
def check_dup_name():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    print(exists)
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/check_dup_id', methods=['POST'])
def check_dup_id():
    id_receive = request.form['id_give']
    exists = bool(db.users.find_one({"id": id_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/dododo')
def what():
    return render_template('prac.html')


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    id_receive = request.form['id_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,  # 아이디
        "password": password_hash,  # 비밀번호
        "id": id_receive,  # 프로필 이름 기본값은 아이디

    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


# -----------------------------------------------------------------------------
@app.route('/albumdata', methods=['GET'])
def albumdata():
    sample_receive = request.args.get('sample_give')
    if sample_receive is None:
        return render_template('albumdata.html')
    else:
        sample_receive = request.args.get('sample_give')
        print(sample_receive)
        data = sample_receive
        userid = session.get('logged_in')
        return render_template('albumdata.html', msg="일단 연결은 되네", data=data, userid=userid)


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

    return jsonify({'msg': albumliset})


@app.route('/albumdata/onereview', methods=['POST'])
def find_reviewone():
    name = request.form['name']
    date = request.form['date']
    print(name)
    albumliset = list(db.review.find({"albumtitle": "Butter", "date": "2021.09.11", "nickname": name}, {'_id': False}))
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
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y.%m.%d')
    titlename = request.form['title']
    doc = {
        'nickname': name_receive,  # 유저
        'review': oneReview_receive,  # 한줄평
        'rete': rate_receive,  # 평가
        'date': nowDate,  # 리뷰 날짜
        'morereview': detailReview_receive,  # 상세리뷰
        'albumtitle': titlename  # 댓글에 해당하는 엘범
    }

    db.review.insert_one(doc)
    return jsonify({'msg': '리뷰를 작성했습니다!'})


# 앨범리스트 API
@app.route('/listing', methods=['GET'])
def listing():
    album = list(db.album.find({}, {'_id': False}))
    return jsonify({'album': album})


# # 엘범 정보 크롤링 만들예정인 공간
# @app.route('/temptestdo', methods=["GET"])
# def 크롤링():
#     # testlist = [("test","testdo"),("test2","testdo2")]
#
#     doc = {
#         'albumtitle': "Butter",  ## 앨범 타이틀
#         'albumimage': "https://cdnimg.melon.co.kr/cm2/album/images/106/95/099/10695099_20210827102823_500.jpg?d999c8c02eeb31ea881ea04dca7c4ae8/melon/resize/282/quality/80/optimize",
#         ## 앨범 이미지
#         'artist': "방탄",  ## 가수명
#         'date': "2021.09.15",  ## 앨범 발매일
#         'genre': "랩",  ## 앨범 장르
#         'agency': "카카오",  ## 앨범 기획사
#         'publisher': "어딜까",  ## 앨범 발매사
#         'singlist': 'testlist'  ## 앨범 곡리스트
#     }

# 앨범리뷰삭제 API
# @app.route('/delete', methods=['POST'])
# def reviewDelete():
#     name_receive = request.form['name_give']
#     db.review.delete_one({'name': name_receive})
#     return jsonify({'msg': '삭제한 내용은 다시 되돌릴 수 없습니다. 그래도 삭제 하시겠습니까?'})


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