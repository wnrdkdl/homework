from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbhomework


## HTML 화면 보여주기
@app.route('/')
def homework():
    return render_template('index.html')


# 주문하기(POST) API
@app.route('/order', methods=['POST'])
def save_order():
    # 여길 채워나가세요!
    name_receive = request.form.get('name_give')
    qty_receive = request.form.get('qty_give')
    addr_receive = request.form.get('addr_give')
    phone_receive = request.form.get('phone_give')

    doc = {
        "name": name_receive,
        "orderQty": qty_receive,
        "address": addr_receive,
        "phone": phone_receive
    }

    db.homework.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '주문 완료!'})


# 주문 목록보기(Read) API
@app.route('/order', methods=['GET'])
def view_orders():
    # 여길 채워나가세요!
    orders = list(db.homework.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'orders': orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
