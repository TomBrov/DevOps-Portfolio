from flask import Flask, render_template, request, jsonify
import mongo


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/api/person/<id>', methods=['PUT',  'DELETE', 'GET'])
def person(id):
    if request.method == 'PUT':
        mongo.update_contact(id)
    elif request.method == 'DELETE':
        mongo.delete_contact(id)
    elif request.method == 'GET':
        contact = mongo.get_contact(id)
        return jsonify(contact)


@app.route('/api/person', methods=['POST'])
def add_user():
    name = request.json['name']
    phone = request.json['phone']
    print(phone)
    mongo.add_contact(name, phone)
    return '200'


@app.route('/api/person', methods=['GET'])
def collection():
        mycol = mongo.get_contacts()
        return jsonify(mycol)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
