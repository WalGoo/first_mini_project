from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient

## 아이피, id, pw, db 기입해주셔야됩니다 !!!

client = MongoClient('mongodb://54.180.153.6/', 27017, username="321bee", password="hagisireo123")

db = client.testdb1


@app.route('/')
def home():
    return render_template('index.html')

## 아래의 api들은 큰 분류에 맞는 Collection 에서데이터를 받아와 클라이언트에게 넘겨줍니다.
## api명은 수정...해주시면 감사하겠습니다.

@app.route('/givemethat/uSanSo', methods=["GET"])
def give_uSanSo():
    uSanSo = list(db.test2.find({}, {'exer_name': True, '_id': False}))
    print(uSanSo)
    return jsonify({'uSanSo': uSanSo})


@app.route('/givemethat/health', methods=["GET"])
def give_health():
    health = list(db.test1.find({}, {'exer_name': True, '_id': False}))
    print(health)
    return jsonify({'health': health})


## DB에 접근하여 알맞는 값을 보내주는 api 입니다.

@app.route('/givemeresult', methods=["POST"])
def result():
    exer_name_receive = request.form['exer_name_give']
    exer_type_receive = request.form['exer_type_give']
    if exer_type_receive == 'uSanSo':
        met = db.test2.find_one({'exer_name': exer_name_receive}, {'_id': False})
        print(met)
    elif exer_type_receive == 'health':
        met = db.test1.find_one({'exer_name': exer_name_receive}, {'_id': False})
        print(met)
    return jsonify({'met': met})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
