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


@app.route("/")
def show():
    client = MongoClient("mongodb://xlash:PWzJpIo975Q7hplS@cluster0-shard-00-00.solpc.mongodb.net:27017,cluster0-shard-00-01.solpc.mongodb.net:27017,cluster0-shard-00-02.solpc.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-718qah-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client.CAOne
    collection = db["Users"]

    results = collection.find({})

    r_list = []
    for r in results:
        r_list.append(r)
        print(r)

    return JSONEncoder().encode({"results": r_list})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True)
