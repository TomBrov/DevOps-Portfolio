import pymongo
import os


def connection():
    MONGO_URI = os.getenv('MONGODB_URI')
    myclient = pymongo.MongoClient(f"{MONGO_URI}")
    mydb = myclient["contacts"]
    mycol = mydb["customers"]
    return mycol


def add_contact(id):
    collection = connection()
    collection.insert_one(id)


def update_contact(id, parameter, value):
    collection = connection()
    person = collection.find_one(id)

    #update query here


def delete_contact(id):
    collection = connection()
    person = collection.find_one(id)
    collection.delete_one(person)


def get_contact(id):
    collection = connection()
    person = collection.find_one(id)
    return person


def get_contacts():
    collection = connection()
    cursor = collection.find({})
    return cursor