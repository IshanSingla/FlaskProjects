from model import findmovie
import os
from flask import *


app = Flask(__name__)
app.secret_key = 'IshanSingla'

@app.route('/')
def home():
    if request.method == "POST":
        try:
            search = request.json['search']
        except KeyError:
            search=None
    else:
        search = request.args.get('search')

    if search == None:
        return jsonify({"error": "search is required to Find any movie!"})
    try: 
        result=findmovie(search)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": e})

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, threaded=True,
            host='127.0.0.1', port=os.getenv('PORT', 9050))