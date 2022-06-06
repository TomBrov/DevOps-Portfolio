import requests
import sys


def add_one(person, ip):
    requests.post(f'http://{ip}/api/person', json=person)


def get_all(ip):
    subjects = []
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url=f'{ip}/api/person', headers=headers)
    for subject in response.json()['items']:
        subjects.append({
            'name': subject['name'],
            'createdAt': subject['createdAt'],
            'description': subject['description'],
            'groups': subject['groups'],
        })
    return subjects


def update_one(ip, uid, parameter, value):
    headers = {"Accept": "application/json"}
    response = requests.request("PUT", url=f"{ip}/api/person", headers=headers, json={'_id': uid, 'parameter': parameter, 'value': value})
    return response


def get_one(ip):
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url=f"{ip}/api/person", headers=headers)
    return response


if __name__ == '__main__':
    ip = sys.argv[0]
    people = [{'name': 'Tom', 'phone': '0508710417', "address": 'Har Shaul 907'}]
    for person in people:
        add_one(person, ip)
    people = get_all(ip)
    person = people[0]
    print(person)
    uid = person['_id']
    name = person['Name']
    new_name = 'Thomas'
    update_one(ip, uid, 'name', new_name)
    print(get_one(uid))