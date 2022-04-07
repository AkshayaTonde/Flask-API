from ipaddress import collapse_addresses
import pymongo
import flask
from pymongo import MongoClient
from flask import Flask
from flask import request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
@app.route("/") 
def show():
    cluster = MongoClient("mongodb+srv://akshaya:akshaya1@cluster0.solpc.mongodb.net/CAOne?retryWrites=true&w=majority")

    db = cluster["CAOne"]
    colection = db["Users"]

    # #to inser the document 
    # #post = {"_id": 0, "name": "Leena", "username":"idleena", "email":"leena@gmail.com", "profilepict":" ","password": "123", "fav_Cat":["1" , "2"]}
    # #colection.insert_one(post)

    # #to read database 
    results = colection.find({})

    return flask.jsonify([result for result in results])


if __name__ == "__main__":
  app.run(host='0.0.0.0',port='8080')
