from bson import json_util
import json
from bson.objectid import ObjectId
from flask import Flask, make_response, request
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config['SECRET_KEY'] = "0ded6d0d92e37d744ce16aaee869af12ec0936b6"
app.config["MONGO_URI"] = "mongodb+srv://vt:{}@cluster0.ql3khj7.mongodb.net/{}?retryWrites=true&w=majority".format('pass', 'sample_restaurants')
mongo = PyMongo(app)
airbnb_data_collection = mongo.db.restaurants


@app.route("/", methods=['GET'])
def retriveAll():
    try:
        datas = list()
        for data in airbnb_data_collection.find():
            datas.append(data)
        if not datas:
            return make_response("", 404)
        return json.dumps(datas, default=json_util.default)
    except:
        return "Something went wrong!"


@app.route("/createRecord", methods=['GET', 'POST'])
def createRecord():
    try:
        airbnb_data_collection.insert_one(request.json)
        return make_response("", 201)
    except:
        return "Something went wrong!"

@app.route("/<id>", methods=['GET'])
def retriveByID(id):
    try:
        data = airbnb_data_collection.find_one({"_id": ObjectId(id)})
        return json.dumps(data, default=json_util.default)
    except:
        return "Something went wrong!"


@app.route("/delete/<id>", methods=['DELETE'])
def deleteByID(id):
    try:
        airbnb_data_collection.delete_one({"_id": ObjectId(id)})
        return "DELETED"
    except:
        return "Something went wrong!"


@app.route("/deleterestaurantid/<restaurant_id>", methods=['DELETE'])
def deleteByRestaurant_id(restaurant_id):
    try:
        airbnb_data_collection.delete_one({"restaurant_id": restaurant_id})
        return "DELETED"
    except:
        return "Something went wrong!"

@app.route("/update/<restaurant_id>", methods=['POST' ,'GET' ,'PUT'])
def updateByUserName(restaurant_id):
    try:
        data = airbnb_data_collection.find_one({"restaurant_id": restaurant_id})
        if data:
            airbnb_data_collection.update_one({"restaurant_id": restaurant_id}, {"$set": request.json})
            return "UPDATED"
        return make_response("", 404)
    except:
        return "Something went wrong!"

if __name__ == '__main__':
    app.run(debug=True)
