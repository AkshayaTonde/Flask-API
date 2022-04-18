
from ipaddress import collapse_addresses
from turtle import update
from pymongo import MongoClient
import pymongo
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from bson import ObjectId


app = Flask(__name__)
CORS(app)

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
@app.route('/addUser', methods=['POST'])
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
    
   # post_list.sort(key="_id")
    return json.loads(JSONEncoder().encode({"results": post_list}))

#View posts by the category
@app.route('/api/ViewPostByCategory/<post_category>', methods=['GET'])
def ViewPostByCategory(post_category):

    collection = db["Posts"]
    #print("Post category value : ", post_category, type(post_category))
    
    #

    post_list = []
    for post in collection.find({"post_category" : int(post_category)}):
        print(post)
        post_list.append(post)

    return json.loads(JSONEncoder().encode({"results": post_list}))

#Create a new post 
#This will accept input from request JSON request and 
@app.route('/api/createPost', methods=['POST'])
def createPost():
    collection = db["Posts"]

    """
    {
        "_id": 2
        "creator_id": 1,
        "post_text": "Test Text",
        "media": "URL",
        "timestamp": {
        "$timestamp": {
            "t": 0,
             "i": 0
            }
        },
        "like": [""],
        "post_category": 1
    }  

    """
    #_id = request.json["_id"]
    creator_id= request.json["creator_id"]
    post_text=request.json["post_text"]
    media = request.json["media"]
    timestamp=request.json["timestamp"]
    like=request.json["like"]
    post_category=request.json["post_category"]

    user_id = collection.insert_one({"creator_id": creator_id, "post_text": post_text,"media":media,"timestamp": timestamp,"like":[ ],"post_category": post_category })

    return {"Result":"Success"}

#API to like the post 
@app.route('/api/likePost', methods=['PUT'])
def voteLike():

    collection = db["Posts"]
    postid= request.json["postid"]
    userid= request.json["userid"]

    post = collection.find_one({"_id" : int(postid)})
    likes= post["like"]

    if userid in post["like"]:
        return {"Result": 0}
    else:
        likes.append(userid)

    collection.find_one_and_update({'_id':postid},{ '$set': { "like" : likes} })
    
    return ({"Results": 1})

#delete Post 
#yet to make to progress 
@app.route('/api/deletePost', methods=['delete'])
def deletePost():

    collection = db["Posts"]
    postid= request.json["postid"]
    userid= request.json["userid"]

    post = collection.find_one({"_id" : int(postid)})
    likes= post["like"]

    if userid in post["like"]:
        return {"Result": 0}
    else:
        likes.append(userid)

    collection.find_one_and_update({'_id':postid},{ '$set': { "like" : likes} })
    
    return ({"Results": 1})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')
