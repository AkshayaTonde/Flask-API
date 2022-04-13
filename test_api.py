from ipaddress import collapse_addresses
from pymongo import MongoClient
import pymongo
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from bson import ObjectId


app = Flask(__name__)

client = MongoClient("mongodb+srv://akshaya:akshaya1@cluster0.solpc.mongodb.net/CAOne?retryWrites=true&w=majority")
db = client.CAOne

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

#View all the users in the system 
@app.route('/api/viewUsers', methods=['GET'])
def viewUsers():

    collection = db["Users"]
    users_list =[]

    for user in collection.find({}):
        print(user)
        users_list.append(user)
        
    return json.loads(JSONEncoder().encode({"results": users_list}))

#add users into the database 
@app.route('/api/AddUser', methods=['POST'])
def addUser():
    collection = db["Users"]

    """
    sample JSON format
    {
  "_id": 0,
  "name": "Leena",
  "username": "idleena",
  "email": "leena@gmail.com",
  "profilepict": " ",
  "password": "123",
  "fav_Cat": [
    "1",
    "2"]
}
    """
    _id = request.json["_id"]
    name = request.json["name"]
    username = request.json["username"]
    email = request.json["email"]
    profilepict = request.json["profilepict"]
    password = request.json["password"]
    fav_Cat = request.json["fav_Cat"]
    
    user_id = collection.insert_one({"_id": _id,"name": name, "username": username,"email":email,"profilepict": profilepict,"password": password,"fav_Cat": fav_Cat })

    return ({"Results ": "Success"})

#View all posts 
@app.route('/api/ViewAllPosts', methods=['GET'])
def ViewAllPosts():

    collection = db["Posts"]
    post_list =[]

    for post in collection.find({}):
        print(post)
        post_list.append(post)
        
    return json.loads(JSONEncoder().encode({"results": post_list}))

#View posts by the category
@app.route('/api/ViewPostByCategory/<post_categoty>', methods=['GET'])
def ViewPostByCategory(post_categoty):

    collection = db["Posts"]
    print("Post category value : ", post_categoty)
    

    post_list = []
    for post in collection.find({"post_categoty" : int(post_categoty)}):
        print(post)
        post_list.append(post)

    return json.loads(JSONEncoder().encode({"results": post_list}))




if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')