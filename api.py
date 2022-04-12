
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

@app.route('/api/addPost', methods=['GET'])
def db_AddPost():

    post2 = Posts(_id = 1, post_id = 1, creator_id=2, post_text="Inserted via API" )
    post2.save()
    return make_response("Success", 201)

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

