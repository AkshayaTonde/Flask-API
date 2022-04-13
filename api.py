from flask import Flask, jsonify, make_response, request
from flask_mongoengine import MongoEngine
from api_constants import mongodb_password

app = Flask(__name__)

database_name = "CAOne"
DB_URI = "mongodb+srv://akshaya:{}@cluster0.solpc.mongodb.net/{}?retryWrites=true&w=majority".format(mongodb_password, database_name
)

app.config["MONGODB_HOST"]= DB_URI

db = MongoEngine()
db.init_app(app)

class Posts(db.Document): 
     
    _id = db.IntField()
    post_id = db.IntField()
    creator_id = db.IntField()
    post_text = db.StringField()
    category_id = db.IntField()

    def to_json(self):
        # Converts the object to JSON 
        return {
            "_id": self.id,
            "post_id": self.post_id,
            "creator_id": self.creator_id,
            "post_text" : self.post_text,
            "category_id": self.category_id
        }

class Users(db.Document):

    _id = db.IntField()
    name = db.StringField()
    username = db.StringField()
    password = db.StringField()
    email = db.StringField()
    profilepict = db.StringField()
    fav_cat = db.StringField()

    def to_json(self):
        # Converts the object to JSON 
        return {
            "_id": self.id,
            "name": self.name,
            "username": self.username,
            "password" : self.password,
            "email": self.email,
            "profilepict" : self.profilepict,
            "fav_cat" : self.fav_cat
        }


@app.route('/api/viewUsers', methods=['GET'])
def viewUsers():
    users_list =[]

    for user in Users.objects:
        print(user)
        users_list.append(user)
        
    return make_response(jsonify(users_list), 200)


@app.route('/api/addUser', methods=['POST'])
def addUser():

    content = request.json
    new_user = Users(_id= 5,name= "Saurabh", username="saurabh@1", password="Saurabh@1", email="mypass1234", profilepict="/one.jpg", fav_cat="[1,2,3]")
    #new_user = users(_id= content['_id'],name= content['name'], username=content['username'], password=content['password'], email=content['email'], profilepict=content['profilepict'], fav_cat=content['fav_cat'])
    new_user.save()
    return make_response("User added to table", 200)

@app.route('/api/addPost', methods=['GET'])
def db_AddPost():

    post2 = Posts(_id = 1, post_id = 1, creator_id=2, post_text="Inserted via API" )
    post2.save()
    return make_response("Success", 201)

#Method and API to show all posts if GET is called 
# If post method is called then a new post will be added 
@app.route('/api/showAllPosts', methods=['GET', 'POST'])
def db_showposts():

    # when user lands onto landing page all the posts should be visible to the user 
    # this uses posts collection and retrives all the documents 
    if request.method == 'GET':
        posts =[]

        for post in Posts.objects:
            posts.append(post)
        
        return make_response(jsonify(posts), 200)

    #When user creates a new post and that needs to be added to the posts collection in mongoDB
    elif request.method == 'POST':
        content = request.json

        new_post = Posts(_id = content['_id'], post_id = content['post_id'], creator_id= content['creator_id'], post_text= content['post_text'] )
        new_post.save()

        return make_response("Added a new post", 201)

#method and API to show the posts by the chosen category
@app.route('/api/ShowPostsByCategory/<category_id>', methods=['GET'])
def db_showpost_byCat(category_id):
    if request.method == 'GET':

        postObj = Posts.objects(category_id = category_id)

        posts =[]

        for post in postObj :
            posts.append(post)

        if posts: 
            return make_response(jsonify(posts), 200)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')

