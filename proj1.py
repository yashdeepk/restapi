#!flask/bin/python3

import sqlite3
import datetime

from flask import Flask
from flask import g
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from flask import abort

from flask_basicauth import BasicAuth

from dbhelper import dbhelper
from forum import forum
from thread import thread
from post import post
from Auth import Auth
from helper import helper
from user import user

dbPath = "proj.db"

app = Flask(__name__)

basic_auth = Auth(app)

@app.route("/forums", methods=['GET'])
def getForums():

    whereList = {}
    ilist = helper.getList(dbPath, forum, whereList)
    response = make_response(ilist.serialize(), 200)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/forums", methods=['POST'])
@basic_auth.required
def createForum():

    obj = forum.deserializeObject(request.json, forum)
    obj.creator = basic_auth.username

    good = helper.ifexist(dbPath, obj, ["name"], 409)
    if not good:
        return

    dbhelper.insert(dbPath, obj)
    return make_response(obj.serializeJson(), 201)

@app.route("/forums/<int:forum_id>", methods=['GET'])
def getThreadsByForum(forum_id):

    whereList = {"forum_id":forum_id}
    ilist = helper.getList(dbPath, thread, whereList)

    response = make_response(ilist.serialize(), 200)
    response.headers["Content-Type"] = "application/json"

    return response

@app.route("/forums/<int:forum_id>", methods=['POST'])
@basic_auth.required
def createThread(forum_id):

    obj = thread.deserializeObject(request.json, thread)
    obj.forum_id = forum_id
    obj.author = basic_auth.username
    obj.timestamp = datetime.datetime.now()

    good = helper.ifnotexist(dbPath, obj, ["forum_id"], 404)
    if not good:
        return

    obj = dbhelper.insert(dbPath, obj)

    response = make_response(obj.serializeJson(), 201)

    response.headers["Location"] = "{url}/{forum_id}/{thread_id}".format(url="/forums", forum_id=obj.forum_id, thread_id=obj.id)

    return response

@app.route("/forums/<int:forum_id>/<int:thread_id>", methods=['GET'])
def getPostsByThread(forum_id, thread_id):

    checkObj = thread()
    checkObj.id = thread_id
    checkObj.forum_id = forum_id

    good = helper.ifnotexist(dbPath, checkObj, ["id", "forum_id"], 404)
    if not good:
        return

    whereList = {"thread_id":thread_id}
    ilist = helper.getList(dbPath, post, whereList)

    response = make_response(ilist.serialize(), 200)
    response.headers["Content-Type"] = "application/json"

    return response

@app.route("/forums/<int:forum_id>/<int:thread_id>", methods=['POST'])
@basic_auth.required
def createPost(forum_id, thread_id):

    checkObj = thread()
    checkObj.id = thread_id
    checkObj.forum_id = forum_id

    good = helper.ifnotexist(dbPath, checkObj, ["id", "forum_id"], 404)
    if not good:
        return

    obj = post.deserializeObject(request.json, post)
    obj.thread_id = thread_id
    obj.poster = basic_auth.username
    obj.timestamp = datetime.datetime.now()
    obj = dbhelper.insert(dbPath, obj)

    response = make_response(obj.serializeJson(), 201)

    return response

@app.route("/users", methods=['POST'])
def createUser():

    obj = user.deserializeObject(request.json, user)

    good = helper.ifexist(dbPath, obj, ["username"], 409)
    if not good:
        return

    obj = dbhelper.insert(dbPath, obj)

    response = make_response("", 201)

    return response

@app.route("/users/<string:username>", methods=['PUT'])
@basic_auth.required
def changeUserPassword(username):

    obj = user.deserializeObject(request.json, user)
    obj.username = username

    good = helper.ifnotexist(dbPath, obj, ["username"], 404)
    if not good:
        return

    if obj.username != basic_auth.username:
        abort(409)

    obj = dbhelper.update(dbPath, obj, ["username"])

    response = make_response("", 200)

    return response

@app.errorhandler(404)
def notFound(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
