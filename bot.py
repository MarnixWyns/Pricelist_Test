"""
Copyright (c) 2021 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

from flask import Flask, request, jsonify
from webexteamssdk import WebexTeamsAPI
import os, csv

# get environment variables
WT_BOT_TOKEN = os.environ['WT_BOT_TOKEN']

# uncomment next line if you are implementing a notifier bot
#WT_ROOM_ID = os.environ['WT_ROOM_ID']

# uncomment next line if you are implementing a controller bot
WT_BOT_EMAIL = os.environ['WT_BOT_EMAIL']

# start Flask and WT connection
app = Flask(__name__)
api = WebexTeamsAPI(access_token=WT_BOT_TOKEN)

# Import csv file with data and translate into a dictionary
with open('./pricelist.csv', mode='r') as infile:
    reader = csv.reader(infile)
    data = list(reader)

countries = {}

for i in data: 
    split = i[0].split(';')
    countries[split[0]] = {
        "code": split[0],
        "country": split[1],
        "pl": split[3]
    }


# defining the decorater and route registration for incoming alerts
@app.route('/', methods=['POST'])
def alert_received():
    raw_json = request.get_json()

    if raw_json["data"]["personEmail"] != WT_BOT_EMAIL:


        message_id = raw_json["data"]["id"]

        message = api.messages.get(message_id).text.strip()

        print(message)

        input = message.upper()


        # customize the behaviour of the bot here
        response = ""
        try:
            if message == "help":
                response = "Hello, I provide information about what price list to use for a certain country. Simply send me a message like `us` or `Belgium` and I will provide you the price list."
            elif message.len() == 2:
                pricelist = countries[input]["pl"]
                response = "The price list for {} is {}".format(message, pricelist)
            else: 
                for i in countries:
                    if countries[i]["country"] == input:
                        pricelist = countries[i]["pl"]
                        print(pricelist)
                        response = "The price list for {} is {}".format(message, pricelist)
        except Exception as e:
            print(e)
            response = "It seems something went wrong or I couldn't find that price list :("
        


        # uncomment if you are implementing a controller bot
        WT_ROOM_ID = raw_json['data']['roomId']
        personEmail_json = raw_json['data']['personEmail']
        if personEmail_json != WT_BOT_EMAIL:
            api.messages.create(roomId=WT_ROOM_ID, markdown=response)


    return jsonify({'success': True})

if __name__=="__main__":
    app.run()