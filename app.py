# from heyoo import WhatsApp
# messenger = WhatsApp('EAAJVc3j40G8BAO30KsKwZBRDifNf7I9mxfyOIy7GISIEjoF7QZCBJfPexPHGL3eRoOUvLiWInTrmMh32ZBt2GE8IJqWjMZABNSZCf0TFR3y9BBNBH1y0x1rbLNLPHslznC9ZAyZChSWKJaPcUFuzQ2Mmvm3ZAdMOOd4CwIjFMfw7IdmSaQLb5qZAZBWTyfPWuzkbvSzGwKmsLYvgZDZD',  phone_number_id='110829038490956')
# messenger.send_message('Your message ', '923462901820')
import os
import json
from heyoo import WhatsApp
from os import environ
from flask import Flask, request, make_response



messenger = WhatsApp('EAAJVc3j40G8BAO30KsKwZBRDifNf7I9mxfyOIy7GISIEjoF7QZCBJfPexPHGL3eRoOUvLiWInTrmMh32ZBt2GE8IJqWjMZABNSZCf0TFR3y9BBNBH1y0x1rbLNLPHslznC9ZAyZChSWKJaPcUFuzQ2Mmvm3ZAdMOOd4CwIjFMfw7IdmSaQLb5qZAZBWTyfPWuzkbvSzGwKmsLYvgZDZD',  phone_number_id='110829038490956')
#WhatsApp(token = "inpust accesstoken", phone_number_id="input phone number id") #messages are not recieved without this pattern


VERIFY_TOKEN = 'umer' #application secret here

#to be tested in prod environment
# messenger = WhatsApp(os.getenv("heroku whatsapp token"),phone_number_id='105582068896304')
# VERIFY_TOKEN = "heroku whatsapp token"

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, It Works"



@app.route("/webhook", methods=["GET"])
def hook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Invalid verification token"







if __name__ == '__main__':
    app.run(debug=True)