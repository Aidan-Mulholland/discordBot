import discord
import json

def generate(items):
    array = []
    with open("items.json") as file:
        jsonFile = json.load(file)
        for i in items:
            array.append(jsonFile[i])
        return(jsonFile[array])