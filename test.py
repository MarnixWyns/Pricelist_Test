from flask import Flask, request, jsonify
from webexteamssdk import WebexTeamsAPI
import os, csv


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

input = "be"
input = input.upper()

if len(input) == 2:
    print(countries[input]["pl"])
else: 
    for i in countries:
        if countries[i]["country"] == input:
            print(countries[i]["pl"])

