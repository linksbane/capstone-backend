from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origins": "https://pmar-capstone-frontend.herokuapp.com"
    }
})

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False)
    datetime = db.Column(db.String(100), unique=False)
    body = db.Column(db.String(144), unique=False)

    def __init__(self, title, datetime, body):
        self.title = title
        self.datetime = datetime
        self.body = body


class PostSchema(ma.Schema):
    class Meta:
        fields = ('title', 'datetime', 'body')


post_schema = PostSchema()
posts_schema = PostsSchema(many=True)

# Endpoint to create a new post
@app.route('/post', methods=["POST"])
def add_post():
    title = request.json['title']
    datetime = request.json['datetime']
    body = request.json['body']

    new_post = Post(title, datetime, body)

    db.session.add(new_post)
    db.session.commit()

    post = Post.query.get(new_post.id)

    return post_schema.jsonify(post)


# Endpoint to query all post
@app.route("/posts", methods=["GET"])
def get_posts():
    all_posts = Post.query.all()
    result = posts_schema.dump(all_posts)
    return jsonify(result.data)


# Endpoint for querying a single post
@app.route("/post/<id>", methods=["GET"])
def get_post(id):
    post = Post.query.get(id)
    return post_schema.jsonify(post)


# Endpoint for updating a post
@app.route("/post/<id>", methods=["PUT"])
def post_update(id):
    post = Post.query.get(id)
    title = request.json['title']
    content = request.json['content']

    post.title = title
    post.content = content

    db.session.commit()
    return post_schema.jsonify(post)


# Endpoint for deleting a record
@app.route("/post/<id>", methods=["DELETE"])
def post_delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()

    return "Guide was successfully deleted"


if __name__ == '__main__':
    app.run(debug=True)


