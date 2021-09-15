from flask import Flask, render_template, jsonify, request, flash
app = Flask(__name__)

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


@app.route('/albumdata')
def albumdata():
    return render_template('albumdata.html')

@app.route('/albumlist')
def albumlist():
    return render_template('albumlist.html')

@app.route('/listing', methods=['GET'])
def listing():
    album = list(db.album.find({},{'_id':False}))
    return jsonify({'album': album})

#엘범 정보 크롤링 만들예정인 공간
@app.route('/temptestdo', methods=["GET", "POST"])
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
    flash("더미데이터 입력완료")
    return render_template('index.html')

@app.route('/review', methods=['GET'])
def show_review():
    sample_receive = request.args.get('sample_give')
    print(sample_receive)
    return jsonify({'msg': 'GET 연결 완료!'})

@app.route('/review', methods=['POST'])
def make_review():
    return jsonify({'msg': 'POST 요청 완료!'})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)