from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import db,credentials
cred = credentials.Certificate('1.json')
default_app = firebase_admin.initialize_app( cred,{'databaseURL':"https://flask-c50a2-default-rtdb.asia-southeast1.firebasedatabase.app/"})
Keys = (db.reference(f"/Key/")).get()

app=Flask(__name__)

@app.route('/')
def _():
    return "Hello, World"

@app.route('/Key/', methods=['POST'])
def __():
    data = request.get_json()
    key=data['Key']
    proxy=data['Proxy']

    if key in Keys:
        proxys = (db.reference(f"/Proxy/{key}/")).get()
        if proxys ==None:
            proxys=[]
        if not len(proxys)<10:
            stat="Too Many Proxies Ask Owner to Restart"
        else:
            if not proxy in proxys:
                proxys.append(f"{proxy}")
                pro= (db.reference(f"/Proxy/{key}/")).set(proxys)
            stat="Done"
    else:
        stat="Invalid"
    return jsonify({
        "stats":stat
    })



"""
@app.route('/Gen/<string:n>')
def gen(n):
    key="".join(n[0:8])
    proxys = (db.reference(f"/Proxy/{key}/")).get()
    if proxys ==None:
        stat="Key Not Available in DataBase"
    return jsonify({
        "stats":stat
    })

@app.route('/Clear/<string:n>')
def Clear(n):
    key="".join(n[0:8])
    if not key in Keys:
        stat="Key Not Available"
    else:
        pros= (db.reference(f"/Proxy/{key}/")).get()
        pro= (db.reference(f"/Proxy/{key}/")).set([])
        stat=f"{pros} Terminated"
    return jsonify({
        "stats":stat
    })
"""

if __name__ == "__main__":
    app.run(use_reloader=True, threaded=True)
