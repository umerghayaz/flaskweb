from heyoo import WhatsApp
# messenger = WhatsApp('EAAJVc3j40G8BAO30KsKwZBRDifNf7I9mxfyOIy7GISIEjoF7QZCBJfPexPHGL3eRoOUvLiWInTrmMh32ZBt2GE8IJqWjMZABNSZCf0TFR3y9BBNBH1y0x1rbLNLPHslznC9ZAyZChSWKJaPcUFuzQ2Mmvm3ZAdMOOd4CwIjFMfw7IdmSaQLb5qZAZBWTyfPWuzkbvSzGwKmsLYvgZDZD',  phone_number_id='110829038490956')
# messenger.send_message('Your message ', '923462901820')
import os
import json
from heyoo import WhatsApp
from os import environ
from flask import Flask, request, make_response

import logging
#
app = Flask(__name__)
#
messenger = WhatsApp('EAAJVc3j40G8BAO30KsKwZBRDifNf7I9mxfyOIy7GISIEjoF7QZCBJfPexPHGL3eRoOUvLiWInTrmMh32ZBt2GE8IJqWjMZABNSZCf0TFR3y9BBNBH1y0x1rbLNLPHslznC9ZAyZChSWKJaPcUFuzQ2Mmvm3ZAdMOOd4CwIjFMfw7IdmSaQLb5qZAZBWTyfPWuzkbvSzGwKmsLYvgZDZD',  phone_number_id='110829038490956')
# #WhatsApp(token = "inpust accesstoken", phone_number_id="input phone number id") #messages are not recieved without this pattern
#
#
VERIFY_TOKEN = 'umer' #application secret here
#
# #to be tested in prod environment
# # messenger = WhatsApp(os.getenv("heroku whatsapp token"),phone_number_id='105582068896304')
# # VERIFY_TOKEN = "heroku whatsapp token"
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


@app.route("/webhook", methods=["GET", "POST"])
def hook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            logging.info("Verified webhook")
            response = make_response(request.args.get("hub.challenge"), 200)
            response.mimetype = "text/plain"
            return response
        logging.error("Webhook Verification failed")
        return "Invalid verification token"

    # Handle Webhook Subscriptions
    data = request.get_json()
    logging.info("Received webhook data: %s", data)
    changed_field = messenger.changed_field(data)
    if changed_field == "messages":
        new_message = messenger.get_mobile(data)
        if new_message:
            mobile = messenger.get_mobile(data)
            name = messenger.get_name(data)
            message_type = messenger.get_message_type(data)
            logging.info(
                f"New Message; sender:{mobile} name:{name} type:{message_type}"
            )
            if message_type == "text":
                message = messenger.get_message(data)
                name = messenger.get_name(data)
                logging.info("Message: %s", message)
                # messenger.send_message(f"Hi {name}, nice to connect with you", mobile)

            elif message_type == "interactive":
                message_response = messenger.get_interactive_response(data)
                intractive_type = message_response.get("type")
                message_id = message_response[intractive_type]["id"]
                message_text = message_response[intractive_type]["title"]
                logging.info(f"Interactive Message; {message_id}: {message_text}")

            elif message_type == "location":
                message_location = messenger.get_location(data)
                message_latitude = message_location["latitude"]
                message_longitude = message_location["longitude"]
                logging.info("Location: %s, %s", message_latitude, message_longitude)

            elif message_type == "image":
                image = messenger.get_image(data)
                image_id, mime_type = image["id"], image["mime_type"]
                image_url = messenger.query_media_url(image_id)
                image_filename = messenger.download_media(image_url, mime_type)
                print(f"{mobile} sent image {image_filename}")
                logging.info(f"{mobile} sent image {image_filename}")


            elif message_type == "video":
                video = messenger.get_video(data)
                video_id, mime_type = video["id"], video["mime_type"]
                video_url = messenger.query_media_url(video_id)
                video_filename = messenger.download_media(video_url, mime_type)
                print(f"{mobile} sent video {video_filename}")
                logging.info(f"{mobile} sent video {video_filename}")

            elif message_type == "audio":
                audio = messenger.get_audio(data)
                audio_id, mime_type = audio["id"], audio["mime_type"]
                audio_url = messenger.query_media_url(audio_id)
                audio_filename = messenger.download_media(audio_url, mime_type)
                print(f"{mobile} sent audio {audio_filename}")
                logging.info(f"{mobile} sent audio {audio_filename}")

            elif message_type == "file":
                file = messenger.get_file(data)
                file_id, mime_type = file["id"], file["mime_type"]
                file_url = messenger.query_media_url(file_id)
                file_filename = messenger.download_media(file_url, mime_type)
                print(f"{mobile} sent file {file_filename}")
                logging.info(f"{mobile} sent file {file_filename}")
            else:
                print(f"{mobile} sent {message_type} ")
                print(data)
        else:
            delivery = messenger.get_delivery(data)
            if delivery:
                print(f"Message : {delivery}")
            else:
                print("No new message")
    return "ok"


if __name__ == "__main__":
    app.run(port=5000, debug=True)