from ipaddress import collapse_addresses
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://akshaya:akshaya1@cluster0.solpc.mongodb.net/CAOne?retryWrites=true&w=majority")

db = cluster["CAOne"]
colection = db["Users"]

#to inser the document 
#post = {"_id": 0, "name": "Leena", "username":"idleena", "email":"leena@gmail.com", "profilepict":" ","password": "123", "fav_Cat":["1" , "2"]}
#colection.insert_one(post)

#to read database 

results = colection.find({"name":"Neha"})

for result in results:
    print(result)