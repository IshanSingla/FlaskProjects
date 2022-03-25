from flask import Flask, request, jsonify, redirect
import json, os, secrets
from flask.json import JSONEncoder
from bson import json_util
from pymongo import MongoClient

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj): return json_util.default(obj)

cluster = MongoClient(os.getenv('pymongo'))
collection = cluster['users']['users']
token = cluster['users']['token']
public = cluster['users']['public_token']

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

def create_token(userid):
    APItoken = secrets.token_hex(int(os.getenv('hex')))
    token.update_one(
            {"user":userid},
            {
                "$set": {
                    "token": APItoken
                }
            },
            upsert=True,
        )
    return APItoken

def create_public_token(userid):
    PAPItoken = secrets.token_hex(int(os.getenv('hex')))
    public.update_one(
            {"user":userid},
            {
                "$set": {
                    "public_token": PAPItoken
                }
            },
            upsert=True,
        )
    return PAPItoken


@app.route('/public', methods = ['GET'])
def pbtoken():
    user = request.args.get('id')
    cred = request.args.get('token')
    admin = token.find_one({"token":cred}, {"user":1})
    if admin == None:
        return jsonify({"error":"invalid token."})
    if user == None:
        return jsonify({"error":"please provide user."})
    return jsonify({
        "status":"success",
        "user":user,
        "token": create_public_token(user)
    })


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('pass')
        if password == os.getenv('password'):
            return jsonify({
                "user_registered":"true",
                "user":user,
                "token": create_token(user)
            })
        else:
            return jsonify({"error":"no such user."})
    else:
        return redirect(os.getenv('docspage'))
    return 
    

@app.route('/find', methods = ['GET'])
def find():
    userid = request.args.get("id")
    token = request.args.get("token")
    cred = request.args.get("token")
    if token != None:
        true_token = public.find_one({"public_token":token}, {"user":1})
    else:
        return jsonify({"error":"invalid token"})
    if true_token == None:
        token_check = token.find_one({"token":cred}, {"user":1})
        if token_check == None:
            return jsonify({"error":"invalid token"})
    for i in collection.find({"user_id":userid}, {'_id':0}):
        print(i['reason'])
        return jsonify({
            "flagged":True,
            "user_id":i['user_id'],
            "reason": i['reason']
        })
    try:
        return i
    except UnboundLocalError:
        return jsonify({"flagged":False})
    

@app.route('/unban', methods = ['GET'])
def unban():
    userid = request.args.get("id")
    cred = request.args.get('cred')
    admin = token.find_one({"token":cred}, {"user":1})
    if admin == None:
        return jsonify({"error":"not admin."})
    query = {"user_id":str(userid)}
    collection.delete_many(query)
    return jsonify({
        "flagged":False,
        "user_id":userid,
        "update":"user unbanned successfully."
    })
    

@app.route('/ban', methods = ['GET'])
def ban():
    user = request.args.get('id')
    cred = request.args.get('cred')
    reason = request.args.get('reason')
    admin = token.find_one({"token":cred}, {"user":1})
    if admin == None:
        return jsonify({"error":"be an admin first."})
    if reason == None:
        return jsonify({"error":"you will have to give a reason."})
    collection.update_one(
            {"user_id":user},
            {
                "$set": {
                    "reason": reason
                }
            },
            upsert=True,
        )   
    return jsonify({
        "flagged":True,
        "user_id":user,
        "reason":reason
    })


@app.route('/all',methods = ['GET'])
def all():
    cred = request.args.get("token")
    admin = token.find_one({"token":cred}, {"user":1})
    if admin == None:
        return jsonify({"error":"be an admin first."})
    total = []
    for i in collection.find({},{'_id':0}):
        total.append(i)
    data = json.loads(json.dumps(total))
    return jsonify(data)


@app.route('/stats', methods=['GET'])
def stats():
    for i in collection.find({}, {'_id':0}):
        banned = len(i['user_id'])
        return jsonify({
            "total_flagged_users":banned
        })

@app.route('/admin/user', methods=['GET'])
def getuser():
    APItoken = request.args.get("token")
    for i in token.find({"token":APItoken}, {'_id':0}):
        return i
    try:
        return i
    except UnboundLocalError:
        return jsonify({"error":"no such token found."})
    return 



    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv('PORT', 6969))