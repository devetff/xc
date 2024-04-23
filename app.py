from flask import Flask, request, render_template
from enum import Flag
import webbrowser
import requests
import hashlib
from pyfiglet import Figlet

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        number = request.form['number']
        password = request.form['password']

        url = 'https://services.orange.eg/SignIn.svc/SignInUser'

        header = {
            "net-msg-id": "61f91ede006159d16840827295301013",
            "x-microservice-name": "APMS",
            "Content-Type": "application/json; charset=UTF-8",
            "Content-Length": "166",
            "Host": "services.orange.eg",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.14.9",
        }

        data = '{"appVersion":"7.2.0","channel":{"ChannelName":"MobinilAndMe","Password":"ig3yh*mk5l42@oj7QAR8yF"},"dialNumber":"%s","isAndroid":true,"password":"%s"}' % (number, password)

        response = requests.post(url, headers=header, data=data).json()

        if 'SignInUserResult' in response and response['SignInUserResult']['ErrorCode'] == 0:
            user_id = response["SignInUserResult"]["UserData"]["UserID"]

            url22 = "https://services.orange.eg/GetToken.svc/GenerateToken"
            hd22 = {"Content-type": "application/json",
                   "Content-Length": "78",
                   "Host": "services.orange.eg",
                   "Connection": "Keep-Alive",
                   "User-Agent": "okhttp/3.12.1"}
            data22 = '{"appVersion":"2.9.8","channel":{"ChannelName":"MobinilAndMe","Password":"ig3yh*mk5l42@oj7QAR8yF"},"dialNumber":"%s","isAndroid":true,"password":"%s"}' % (number, password)
            ctv = requests.post(url22, headers=hd22, data=data22).json()["GenerateTokenResult"]["Token"]
            key = ',{.c][o^uecnlkijh*.iomv:QzCFRcd;drof/zx}w;ls.e85T^#ASwa?=(lk'
            htv = (str(hashlib.sha256((ctv + key).encode('utf-8')).hexdigest()).upper())

            url2 = "https://services.orange.eg/APIs/Promotions/api/CAF/Redeem"

            data2 = '{"Language":"ar","OSVersion":"Android7.0","PromoCode":"رمضان كريم","dial":"%s","password":"%s","Channelname":"MobinilAndMe","ChannelPassword":"ig3yh*mk5l42@oj7QAR8yF"}' % (number, password)

            header2 = {
                "_ctv": ctv,
                "_htv": htv,
                "UserId": user_id,
                "Content-Type": "application/json; charset=UTF-8",
                "Content-Length": "142",
                "Host": "services.orange.eg",
                "Connection": "Keep-Alive",
                "User-Agent": "okhttp/3.14.9",
            }

            da = data2.encode('utf-8')

            r = requests.post(url2, headers=header2, data=da).json()

            if r.get('ErrorCode') == 0:
                return render_template('index.html', message=" 500تم اضافه")
            else:
                return render_template('index.html', message="اخذت العرض سابقا يرجي المحاوله في وقت لاحق")
        else:
            return render_template('index.html', message="كلمه السر او الرقم غلط")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=81)
