from flask import Flask, render_template, request, jsonify
import mongo

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/api/person/<personal_id>', methods=['GET'])
def person(personal_id):
    contact = mongo.get_contact(personal_id)
    if bool(contact):
        return jsonify(contact)
    else:
        return "404 Not Found"


@app.route('/api/person', methods=['PUT'])
def update_user():
    person_id = request.json['_id']
    parameter = request.json['parameter']
    new_value = request.json['value']
    mongo.update_contact(person_id, parameter, new_value)
    return "200 OK"


@app.route('/api/person', methods=['POST'])
def add_user():
    name = request.json['Name']
    phone = request.json['Phone']
    address = request.json['Address']
    mongo.add_contact(name, phone, address)
    return "201 Created"


@app.route('/api/person', methods=['GET'])
def collection():
    full_collection = mongo.get_contacts()
    return jsonify(full_collection)


@app.route('/api/person', methods=['DELETE'])
def delete_user():
    personal_id = request.json['_id']
    mongo.delete_contact(personal_id)
    return "200 OK"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)