from flask import Flask, jsonify, request, render_template, send_file
import firebase_admin, asyncio, os
from firebase_admin import db,credentials
from flask_cors import CORS
from pyppeteer import launch

cred = credentials.Certificate('1.json')
default_app = firebase_admin.initialize_app( cred,{'databaseURL':"https://flask-c50a2-default-rtdb.asia-southeast1.firebasedatabase.app/"})

app = Flask(__name__)
app.secret_key = 'i_iz_noob'
loop = asyncio.get_event_loop()
CORS(app)
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/api')
def api():
    return render_template("api.html")


@app.route('/api/key/', methods=['GET','POST'])
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

@app.route('/api/carbon/', methods=['GET', 'POST'])
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
        loop.run_until_complete(get_response(data, (os.getcwd() + '/carbon_screenshot.png')))
        return send_file((os.getcwd() + '/carbon_screenshot.png'), mimetype='image/png')
    except Exception as e:
        ish=str(e)
        return jsonify({"error": ish})

@app.route('/api/morse/', methods=['GET','POST'])
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
            "encript": f"{result}",
            })
    elif not decode==None:
        result = decrypt(decode)
        return jsonify({
            "decrypt": f"{result}",
            })
    else:
        return jsonify({
            "error": "No Para Meter given",
            })




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
            'downloadPath': os.getcwd()
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
        await page.goto(url, timeout=100000)
        element = await page.querySelector("#export-container  .container-bg")
        img = await element.screenshot({'path': path})
        await browser.close()
        return (path)

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
    app.run(debug=True,use_reloader=True, threaded=True)
