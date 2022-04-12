
from ipaddress import collapse_addresses
from pymongo import MongoClient
import pymongo
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from bson import ObjectId

app = Flask(__name__)
CORS(app)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.route("/getUsers", methods=['GET'])
def show():
    client = MongoClient("mongodb+srv://akshaya:akshaya1@cluster0.solpc.mongodb.net/CAOne?retryWrites=true&w=majority")
    db = client.CAOne
    collection = db["Users"]

    results = collection.find({})

    r_list = []
    for r in results:
        r_list.append(r)
       # print(r)
    return json.loads(JSONEncoder().encode({"results": r_list}))

@app.route("/getPosts", methods=['GET'])
def showAllPosts():


  if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')
