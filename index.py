from flask import Flask, flash, jsonify, request, render_template, send_file
import firebase_admin, asyncio, os, pyqrcode, requests
from firebase_admin import db,credentials
from pyppeteer import launch
from lyrics_extractor import SongLyrics
from datetime import datetime, date

cred = credentials.Certificate('1.json')
default_app = firebase_admin.initialize_app( cred,{'databaseURL':"https://flask-c50a2-default-rtdb.asia-southeast1.firebasedatabase.app/"})

app = Flask(__name__)

app.secret_key = 'i_iz_noob'
loop = asyncio.get_event_loop()

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/api')
def api():
    return render_template("api.html")

@app.route('/api/key', methods=['GET','POST'])
def key():
    if request.method == "POST":
        data = request.get_json()
        try:
            key=data['Key']
            proxy=data['Proxy']
        except KeyError:
            return jsonify({"error": "Key/Proxy is required"})
    else:
        key = request.args.get('Key')
        if key is None:
            return jsonify({"error": "Key is required"})
        proxy = request.args.get('Proxy')
        if proxy is None:
            return jsonify({"error": "Proxy is required"})
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
        stat="Key is Invalid"
    return jsonify({
        "stats":stat
    })

@app.route('/api/carbon', methods=['GET', 'POST'])
def carbon():
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
        loop.run_until_complete(get_response(data, ('/tmp/carbon_screenshot.png')))
        return send_file(('/tmp/carbon_screenshot.png'), mimetype='image/png')
    except Exception as e:
        ish=str(e)
        return jsonify({"error": str(e)})

@app.route('/api/morse', methods=['GET','POST'])
def morse():
    if request.method == "POST":
        data = request.get_json()
        try:
            encode=data['encode']
        except KeyError:
            encode=None
        try:
            decode=data['decode']
        except KeyError:
            decode=None
    else:
        encode= request.args.get('encode')
        decode= request.args.get('decode')

    if not encode==None:
        result = encrypt(encode.upper())
        return jsonify({
            "word": f"{encode}",
            "morse": f"{result}",
            })
    elif not decode==None:
        result = decrypt(decode)
        return jsonify({
            "morse": f"{decode}",
            "word": f"{result}",
            })
    else:
        return jsonify({
            "error": "No Parameter given",
            })

@app.route('/api/lyrics', methods=['GET','POST'])
def lyrics():
    if request.method == "POST":
        data = request.get_json()
        try:
            encode=data['song']
        except KeyError:
            encode=None
    else:
        encode= request.args.get('song')

    if not encode==None:
        extract_lyrics = SongLyrics("AIzaSyAIZtzGSufntqJSf_xjU-nDMtw-I4HS93A","c711d9ef47b126b53")
        ishan=extract_lyrics.get_lyrics(encode)
        return jsonify(ishan)
    else:
        return jsonify({
            "error": "No Parameter given",
            })

@app.route('/api/qr', methods=['GET','POST'])
def qr():
    if request.method == "POST":
        data = request.get_json()
        try:
            encode=data['text']
        except KeyError:
            encode=None
    else:
        encode= request.args.get('text')
    try:
        if not encode==None:
            url = pyqrcode.create(encode)
            url.png('/tmp/qr.png', scale = 6)
            return send_file(('/tmp/qr.png'), mimetype='image/png')
        else:
            return jsonify({
                "error": "No Parameter given",
            })
    except Exception as e:
        return jsonify({
                "error": f"{e}",
            })

@app.route('/api/notes', methods=['GET','POST'])
def notes():
    if request.method == "POST":
        data = request.get_json()
        try:
            encode=data['text']
        except KeyError:
            encode=None
    else:
        encode= request.args.get('text')
    try:
        if not encode==None:
            data = requests.get(f"https://pywhatkit.herokuapp.com/handwriting?text={encode}&rgb=0,0,0")
            if data.status_code==200:
                with open(('/tmp/notes.png'), "wb") as file:
                    file.write(data.content)
                    file.close()

                return send_file(('/tmp/notes.png'), mimetype='image/png')
            else:
                return jsonify({
                "error": "Error in api",
            })
        else:
            return jsonify({
                "error": "No Parameter given",
            })
    except Exception as e:
        return jsonify({
                "error": f"{e}",
            })

@app.route('/api/moneyin', methods=['GET', 'POST'])
def moneyin():
    data = None
    if request.method == "POST":
        data = request.json
        try:
            userid = data['userid']
        except KeyError:
            return jsonify({"error": "userid is required to work"})
        try:
            amount = data['amount']
        except KeyError:
            return jsonify({"error": "amount is required to work"})
    else:
        userid = request.args.get('userid')
        if userid is None:
            return jsonify({"error": "userid is required to work"})
        amount = request.args.get('amount')
        if amount is None:
            return jsonify({"error": "amount is required to work"})
    try:
        ballence = (db.reference(f"/Details/{userid}/ballence")).get()
        if ballence== None:
            ballence=0
        ballence+=int(amount)
        Transiction = (db.reference(f"/Details/{userid}/Transiction")).get()
        if Transiction== None:
            Transiction=[]
        Transict = (db.reference(f"/Details/{userid}/Transiction/{len(Transiction)}/type")).set("CR")
        Transict = (db.reference(f"/Details/{userid}/Transiction/{len(Transiction)}/amount")).set(int(amount))
        Transict = (db.reference(f"/Details/{userid}/Transiction/{len(Transiction)}/time")).set( f"{datetime.today()}")
        ball = (db.reference(f"/Details/{userid}/ballence")).set(ballence)
        return jsonify({"stats": f"Ballence Add sucessfully Now Ballence is {ballence}Rs"})
            
    except Exception as e:
        return jsonify({"error": f"{e}"})

@app.route('/api/moneyout', methods=['GET', 'POST'])
def moneyout():
    data = None
    if request.method == "POST":
        data = request.json
        try:
            userid = data['userid']
        except KeyError:
            return jsonify({"error": "userid is required to work"})
        try:
            amount = data['amount']
        except KeyError:
            return jsonify({"error": "amount is required to work"})
    else:
        userid = request.args.get('userid')
        if userid is None:
            return jsonify({"error": "userid is required to work"})
        amount = request.args.get('amount')
        if amount is None:
            return jsonify({"error": "amount is required to work"})
    try:
        ballence = (db.reference(f"/Details/{userid}/ballence")).get()
        if ballence== None:
            ballence=0
        ballence-=int(amount)
        if ballence<0:
            return jsonify({"stats": f"Insufficient Ballence"})
        Transiction = (db.reference(f"/Details/{userid}/Transiction")).get()
        if Transiction== None:
            Transiction=[]
        Transict = (db.reference(f"/Details/{userid}/Transiction/{len(Transiction)}/type")).set("DR")
        Transict = (db.reference(f"/Details/{userid}/Transiction/{len(Transiction)}/amount")).set(int(amount))
        Transict = (db.reference(f"/Details/{userid}/Transiction/{len(Transiction)}/time")).set( f"{datetime.today()}")
        ballen= (db.reference(f"/Details/{userid}/ballence")).set(ballence)
        return jsonify({"stats": f"Ballence Decrease sucessfully Now Ballence is {ballence}Rs"})
            
    except Exception as e:
        return jsonify({"error": f"{e}"})

@app.route('/api/moneycheck', methods=['GET', 'POST'])
def moneycheck():
    data = None
    if request.method == "POST":
        data = request.json
        try:
            userid = data['userid']
        except KeyError:
            return jsonify({"error": "userid is required to work"})
    else:
        userid = request.args.get('userid')
        if userid is None:
            return jsonify({"error": "userid is required to work"})
    try:
        ballence = (db.reference(f"/Details/{userid}/ballence")).get()
        if ballence== None:
            ballence=0
        return jsonify({"stats": f"Now Ballence is {ballence}Rs"})
            
    except Exception as e:
        return jsonify({"error": f"{e}"})

@app.route('/api/moneytrans', methods=['GET', 'POST'])
def moneytrans():
    data = None
    if request.method == "POST":
        data = request.json
        try:
            userid = data['userid']
        except KeyError:
            return jsonify({"error": "userid is required to work"})
    else:
        userid = request.args.get('userid')
        if userid is None:
            return jsonify({"error": "userid is required to work"})
    try:

        Transiction = (db.reference(f"/Details/{userid}/Transiction")).get()
        if Transiction== None:
            Transiction=[
                {
                    "type": "-",
                    "amount": "-",
                    "date/time": "-"
                }
            ]
        ballence = (db.reference(f"/Details/{userid}/ballence")).get()
        if ballence== None:
            ballence=0
        return jsonify({
                "ballence": ballence,
                "transiction": Transiction,

            }
        )
            
    except Exception as e:
        return jsonify({"error": f"{e}"})



defaultOptions = {
        "backgroundColor": "rgba(171, 184, 195, 1)",
        "code": "",
        "dropShadow": True,
        "dropShadowBlurRadius": "68px",
        "dropShadowOffsetY": "20px",
        "exportSize": "2x",
        "fontFamily": "Hack",
        "firstLineNumber": 1,
        "fontSize": "14px",
        "language": "auto",
        "lineNumbers": False,
        "paddingHorizontal": "56px",
        "paddingVertical": "56px",
        "squaredImage": False,
        "theme": "seti",
        "watermark": False,
        "widthAdjustment": True,
        "windowControls": True,
        "windowTheme": None,
    }

optionToQueryParam = {
        "backgroundColor": "bg",
        "code": "code",
        "dropShadow": "ds",
        "dropShadowBlurRadius": "dsblur",
        "dropShadowOffsetY": "dsyoff",
        "exportSize": "es",
        "fontFamily": "fm",
        "firstLineNumber": "fl",
        "fontSize": "fs",
        "language": "l",
        "lineNumbers": "ln",
        "paddingHorizontal": "ph",
        "paddingVertical": "pv",
        "squaredImage": "si",
        "theme": "t",
        "watermark": "wm",
        "widthAdjustment": "wa",
        "windowControls": "wc",
        "windowTheme": "wt",
    }

optionToQueryParam = {
        "backgroundColor": "bg",
        "code": "code",
        "dropShadow": "ds",
        "dropShadowBlurRadius": "dsblur",
        "dropShadowOffsetY": "dsyoff",
        "exportSize": "es",
        "fontFamily": "fm",
        "firstLineNumber": "fl",
        "fontSize": "fs",
        "language": "l",
        "lineNumbers": "ln",
        "paddingHorizontal": "ph",
        "paddingVertical": "pv",
        "squaredImage": "si",
        "theme": "t",
        "watermark": "wm",
        "widthAdjustment": "wa",
        "windowControls": "wc",
        "windowTheme": "wt",
    }

ignoredOptions = [
        "backgroundImage",
        "backgroundImageSelection",
        "backgroundMode",
        "squaredImage",
        "hiddenCharacters",
        "name",
        "lineHeight",
        "loading",
        "icon",
        "isVisible",
        "selectedLines",
    ]


async def get_response(body_, path):
        browser = await launch(defaultViewPort=None,
                             handleSIGINT=False,
                             handleSIGTERM=False,
                             handleSIGHUP=False,
                             headless=True,
                             args=['--no-sandbox', '--disable-setuid-sandbox'])
        page = await browser.newPage()
        await page._client.send('Page.setDownloadBehavior', {
             'behavior': 'allow', 
             'downloadPath': os.getcwd()+"/tmp"
         })
        first = True
        url = ""
        validatedBody = {}
        if not body_['code']:
            raise Exception("code is required for creating carbon")

        for option in body_:
            if option in ignoredOptions:
                print(f"Unsupported option: {option} found. Ignoring!")
                continue
            if (not (option in defaultOptions)):
                continue
            validatedBody[option] = body_[option]
        try:
            s=validatedBody['backgroundColor'].upper()
            for ch in s:
                if ((ch < '0' or ch > '9') and (ch < 'A' or ch > 'F')):  
                    ishan= False
            ishan= True
            if validatedBody['backgroundColor'].startswith('#') or ishan == True:
                h=validatedBody['backgroundColor']
                h = h.lstrip('#')
                validatedBody['backgroundColor'] =  ('rgb'+str(tuple(int(h[i:i+2], 16) for i in (0, 2, 4))))
        except KeyError:
            pass
        for option in validatedBody:
            if first:
                first = False
                url = "https://carbon.now.sh/" + \
                    f"?{optionToQueryParam[option]}={validatedBody[option]}"
            else:
                url = url + \
                    f"&{optionToQueryParam[option]}={validatedBody[option]}"
        await page.goto(url, timeout=1000)
        element = await page.querySelector("#export-container  .container-bg")
        img = await element.screenshot({'path': path})
        await browser.close()
        return (path)
        data = requests.get(url)
        if data.status_code==200:

                with open(path, "wb") as file:
                    file.write(data.content)
                    file.close()

                return send_file(path, mimetype='image/png')
        else:
                return jsonify({
                "error": "Error in api",
                })

MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',

                    'C':'-.-.', 'D':'-..', 'E':'.',

                    'F':'..-.', 'G':'--.', 'H':'....',

                    'I':'..', 'J':'.---', 'K':'-.-',

                    'L':'.-..', 'M':'--', 'N':'-.',

                    'O':'---', 'P':'.--.', 'Q':'--.-',

                    'R':'.-.', 'S':'...', 'T':'-',

                    'U':'..-', 'V':'...-', 'W':'.--',

                    'X':'-..-', 'Y':'-.--', 'Z':'--..',

                    '1':'.----', '2':'..---', '3':'...--',

                    '4':'....-', '5':'.....', '6':'-....',

                    '7':'--...', '8':'---..', '9':'----.',

                    '0':'-----', ', ':'--..--', '.':'.-.-.-',

                    '?':'..--..', '/':'-..-.', '-':'-....-',

                    '(':'-.--.', ')':'-.--.-'}

def encrypt(message):
    cipher = ''
    for letter in message:
        if letter != ' ':
            cipher += MORSE_CODE_DICT[letter] + ' '
        else:
            cipher += ' '
    return cipher

def decrypt(message):
    message += ' '
    decipher = ''
    citext = ''
    for letter in message:
        if (letter != ' '):
            i = 0
            citext += letter
        else:
            i += 1
            if i == 2 :
                decipher += ' '
            else:
                decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT
                .values()).index(citext)]
                citext = ''
    return decipher

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
