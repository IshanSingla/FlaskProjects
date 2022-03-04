from flask import Flask, jsonify, request
import firebase_admin, telethon, random
from firebase_admin import db,credentials
API_ID= 12468937
API_HASH= "84355e09d8775921504c93016e1e9438"
BOT_TOKEN = "5280985880:AAEw56OVMxOHRAJ3E3RHdMF1IHqMxGI5H3I"
Owner=[2026675025,1303790979]
#client = telethon.TelegramClient(None, api_id=API_ID , api_hash=API_HASH).start(bot_token=BOT_TOKEN)
cred = credentials.Certificate('1.json')
default_app = firebase_admin.initialize_app( cred,{'databaseURL':"https://flask-c50a2-default-rtdb.asia-southeast1.firebasedatabase.app/"})
Keys = (db.reference(f"/Key/")).get()

DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 
app=Flask(__name__)

@app.route('/')
def _():
    return "Hello, World"

@app.route('/Key/<string:n>')
def __(n):
    key="".join(n[0:8])
    proxy="".join(n[8:50])

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



@app.route('/Ishan/', methods=['POST'])
def home():
        data = request.form
        return jsonify({
                "hi":data
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


@client.on(telethon.events.NewMessage(incoming=True, pattern='/start'))
async def _(e):
    but=[
            [
                telethon.Button.inline("Key Generate", b"Gen"),
                telethon.Button.inline("Terminate", b"Ter")
            ]
        ]
    await e.reply(f"**Welcome Sir!\n\nI'm Induced Account Bot \nMade for Manage Tg Accounts\n\nMade with ❤️ By @InducedBots**", buttons=but)

@client.on(telethon.events.CallbackQuery)
async def _(e):
    if e.query.user_id in Owner:
        if e.data == b"Ter":
            await e.answer('\nSkip Number',alert=True)
            async with client.conversation(e.chat_id) as xmr:
                await xmr.send_message("Send Your Key To Terminate")
                try:
                    Zip= await xmr.get_response(timeout=300)
                    if Zip.text=="/start" or Zip.text=="/help":
                        return
                    key=Zip.text
                    if not key in Keys:
                        await xmr.send_message("Key Not Available in DataBase")
                    else:
                        pros= (db.reference(f"/Proxy/{key}/")).get()
                        pro= (db.reference(f"/Proxy/{key}/")).set([])
                        await xmr.send_message(f"{pros} Terminated")
                except TimeoutError:
                    await xmr.send_message("Time Limit Reached of 5 Min.")
                    return 
        elif e.data == b"Gen":
            async with client.conversation(e.chat_id) as xmr:
                await xmr.send_message("Send Your Key To Terminate")
                try:
                    rand_digit = random.choice(DIGITS)
                    key=""
                    for x in range(0,8):
                        key+=rand_digit
                    if key in Keys:
                        await xmr.send_message("Key Already  Available in DataBase Try Agin")
                    else:
                        Keys.append(f"{key}")
                        Ke = (db.reference(f"/Key/")).set(Keys)
                        await xmr.send_message(f"{key}")
                except TimeoutError:
                    await xmr.send_message("Time Limit Reached of 5 Min.")
                    return 
"""
if __name__ == "__main__":
    app.run(use_reloader=True, threaded=True)
