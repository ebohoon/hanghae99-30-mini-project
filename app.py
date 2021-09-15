from flask import Flask, render_template, jsonify, request, flash, session
app = Flask(__name__)

#테스트 improt
from bson.json_util import dumps

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

@app.route('/orderlist/find', methods=['POST'])
def find_orderlist():
    ##로그인 확인
    id = session.get('logged_in')
    ##로그인이 안되어있으면.. 아직 쓸모없음 
    # if id is not None:
    #     test = list(db.users.find({'userid':id}))[0]['orderlisttest']
        
    #     test1 = []
    #     for a in test:
    #         test1.append(list(db.order.find({'_id':ObjectId(a)}))[0])
    #     #print(test1)
    #     return jsonify({'orderlist':dumps(test1), 'msg':'조회완료!'})
    
    phone = request.form['phone']
    orderlist = list(db.album.find({'phone':phone}))
    return jsonify({'orderlist':dumps(orderlist), 'msg':'조회완료!'})
    
    

#엘범 정보 크롤링 만들예정인 공간
@app.route('/temptestdo', methods=["GET", "POST"])
def 크롤링():
    
    testlist = [("test","testdo"),("test2","testdo2")]

    doc = {
        'albumtitle': "타이틀이름!",         ## 앨범 타이틀
        'albumimage': "이미지 이름",         ## 앨범 이미지
        'artist': "가수이름",                ## 가수명
        'date': "2021.09.15",               ## 앨범 발매일
        'genre': "장르",                    ## 앨범 장르
        'agency': "기획사",                 ## 앨범 기획사
        'singlist': testlist              ## 앨범 곡리스트
    }

    db.album.insert_one(doc)
    flash("더미데이터 입력완료")
    return render_template('index.html')
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)