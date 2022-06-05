import json

import pymongo
import os
import uuid


def connection():
    MONGO_URI = os.getenv('MONGO_URI')
    myclient = pymongo.MongoClient(f'{MONGO_URI}')
    #myclient = pymongo.MongoClient('mongodb://localhost:27017')
    mydb = myclient["contacts"]
    mycol = mydb["personal"]
    return mycol


def add_contact(name, phone, address):
    collection = connection()
    personal_id = str(uuid.uuid4())[0:8]
    collection.insert_one({"_id": personal_id, "name": name, "phone": phone, "address": address})


def update_contact(personal_id, parameter, value):
    collection = connection()
    person = collection.find_one({'_id': f"{personal_id}"})
    queries = {f'{parameter}': f'{person[parameter]}'}
    new_values = {"$set": {f'{parameter}': f'{value}'}}
    collection.update_one(queries, new_values)


def delete_contact(personal_id):
    collection = connection()
    person = collection.find_one_and_delete({'_id': f"{personal_id}"})
    collection.delete_one(person)


def get_contact(personal_id):
    chosen_col = connection()
    person = chosen_col.find_one({'_id': f"{personal_id}"})
    return person


def get_contacts():
    collection = connection()
    people = collection.find({})
    people = list(people)
    return people