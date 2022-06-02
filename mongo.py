import pymongo
import os


def connection():
    #MONGO_URI = os.getenv('MONGODB_URI')
    #myclient = pymongo.MongoClient(f"{MONGO_URI}")
    myclient = pymongo.MongoClient('mongodb://localhost:27017')
    mydb = myclient["contacts"]
    mycol = mydb["customers"]
    return mycol


def add_contact(name, phone):
    collection = connection()
    Newid = int(len(get_contacts()))+1
    collection.insert_one({'_id':f"{Newid}", "name":name, "phone":phone})


def update_contact(id):
    collection = connection()
    person = collection.update_one({'_id':f"{id}"})
    #update query here



def delete_contact(id):
    collection = connection()
    person = collection.find_one_and_delete({'_id':f"{id}"})
    collection.delete_one(person)


def get_contact(id):
    chosen_col = connection()
    person = chosen_col.find_one({'_id':f"{id}"})
    return person


def get_contacts():
    collection = connection()
    people = collection.find({})
    people = list(people)
    return people
