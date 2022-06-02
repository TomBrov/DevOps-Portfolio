import json
import pymongo
import os


def connection():
    #MONGO_URI = os.getenv('MONGODB_URI')
    #myclient = pymongo.MongoClient(f"{MONGO_URI}")
    myclient = pymongo.MongoClient('mongodb://localhost:27017')
    mydb = myclient["contacts"]
    mycol = mydb["customers"]
    return mycol


def add_contact(id):
    collection = connection()
    collection.insert_one(id)


def update_contact(id):
    collection = connection()
    person = collection.find_one_and_update({'id':f"{id}"})

    #update query here


def delete_contact(id):
    collection = connection()
    person = collection.find_one_and_delete({'id':f"{id}"})
    collection.delete_one(person)


def get_contact(id):
    chosen_col = connection()
    person = chosen_col.find_one({'id':f"{id}"})
    return person


def get_contacts():
    collection = connection()
    pepole = collection.find({})
    pepole = list(pepole)
    return pepole


if __name__ == '__main__':
    connection()
    #contact = '{"id":"1", "name":"Tom", "Phone":"0508710417"}'
    #contact = json.loads(contact)
    #add_contact(contact)
    #print(get_contact(1))
    #print(get_contacts())
    update_contact()
    print(get_contact(1))
