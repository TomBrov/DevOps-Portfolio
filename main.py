from flask import Flask, render_template, request
import pymongo

import mongo
from mongo import *


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/api/person/<id>', methods=['PUT', 'POST', 'DELETE'])
def person(id):
    if request.method == 'POST':
        mongo.add_contact(id)
    elif request.method == 'PUT':
        mongo.update_contact(id)
    elif request.method == 'DELETE':
        mongo.delete_contact(id)
    elif request.method == 'GET':
        contact = mongo.get_contact(id)
        print(contact)


@app.route('/api/person', methods=['GET'])
def collection():
    mycol = mongo.get_contacts()
    return mycol


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
