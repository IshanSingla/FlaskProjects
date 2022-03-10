from flask import Flask, jsonify, request, render_template, send_file
import firebase_admin, carbon, asyncio, os
from firebase_admin import db,credentials
cred = credentials.Certificate('1.json')
default_app = firebase_admin.initialize_app( cred,{'databaseURL':"https://flask-c50a2-default-rtdb.asia-southeast1.firebasedatabase.app/"})

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/api')
@app.route('/Api')
def api():
    return render_template("api.html")

@app.route('/Api/key/', methods=['POST'])
@app.route('/api/key/', methods=['POST'])
@app.route('/Api/Key/', methods=['POST'])
@app.route('/api/Key/', methods=['POST'])
def key():
    data = request.get_json()
    key=data['Key']
    proxy=data['Proxy']
    Keys = (db.reference(f"/Key/")).get()
    if key in Keys:
        proxys = (db.reference(f"/Proxy/{key}/")).get()
        if proxys ==None:
            proxys=[]
        if not len(proxys)<5:
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


@app.route('/Api/carbon/', methods=['GET', 'POST'])
@app.route('/api/carbon/', methods=['GET', 'POST'])
@app.route('/Api/Carbon/', methods=['GET', 'POST'])
@app.route('/api/Carbon/', methods=['GET', 'POST'])
def home():
    data = None
    if request.method == "POST":
        data = request.json
        try:
            code = data['code']
        except KeyError:
            return jsonify({"error": "Code is required to create a Carbon!"})
    else:
        code = request.args.get('code')
        if code is None:
            return jsonify({"error": "Code is required to create a Carbon!"})
        data = request.args
    try:
        carbon.get_response(carbon.createURLString(carbon.validateBody(data)), (os.getcwd() + '/carbon_screenshot.png'))
        return send_file((os.getcwd() + '/carbon_screenshot.png'), mimetype='image/png')
    except Exception as e:
        return jsonify({"error": e})

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
    app.run(debug=True,use_reloader=True, threaded=True)
