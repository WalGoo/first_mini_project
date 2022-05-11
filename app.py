from pymongo import MongoClient
import jwt
import datetime
import certifi
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

ca = certifi.where()

client = MongoClient('mongodb://54.180.153.6/', 27017, username="321bee", password="hagisireo123")
db = client.testdb1


#####################################################
#####             HTML 파일 뿌리기                #####
#####################################################


@app.route('/')
def main():
    return render_template("login.html")


@app.route('/detail')
def detail():
    return render_template("project.html")


@app.route('/main')
def main_page():
    return render_template('index.html')


#####################################################
######                로그인 API               #######
#####################################################


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('login.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('project.html', msg=msg)


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.userlog.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=5)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,  # 아이디
        "password": password_hash,  # 비밀번호
    }
    db.userlog.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.userlog.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


#####################################################
#####                DB 접근 API                ######
#####################################################


@app.route('/givemethat', methods=["POST"])
def give_exer_type():
    exer_type = request.form['exer_type_give']
    if exer_type == 'uSanSo':
        usanso = list(db.test2.find({}, {'exer_name': True, '_id': False}))
        return jsonify({'uSanSo': usanso})
    elif exer_type == 'health':
        health = list(db.test1.find({}, {'exer_name': True, '_id': False}))
        return jsonify({'health': health})


## DB에 접근하여 알맞는 값을 보내주는 api 입니다.

@app.route('/givemeresult', methods=["POST"])
def result():
    exer_name_receive = request.form['exer_name_give']
    exer_type_receive = request.form['exer_type_give']
    if exer_type_receive == 'uSanSo':
        met = db.test2.find_one({'exer_name': exer_name_receive}, {'_id': False})
    elif exer_type_receive == 'health':
        met = db.test1.find_one({'exer_name': exer_name_receive}, {'_id': False})
    return jsonify({'met': met})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
