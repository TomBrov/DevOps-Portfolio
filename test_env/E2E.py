import requests
import sys


def add_one(person, ip):
    headers = {"Accept": "application/json"}
    requests.post(f'http://{ip}/api/person', json=person, headers=headers)


def delete_one(id, ip):
    headers = {"Accept": "application/json"}
    requests.request('DELETE', f'http://{ip}/api/person', json={'_id': id}, headers=headers)


def get_all(ip):
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url=f'http://{ip}/api/person', headers=headers)
    subjects = []
    for subject in response.json():
        subjects.append(subject)
    return subjects


def update_one(ip, uid, parameter, value):
    response = requests.request('PUT', url=f"http://{ip}/api/person",
                                json={'_id': uid, 'parameter': parameter, 'value': value})


def get_one(ip, uid):
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url=f"http://{ip}/api/person/{uid}", headers=headers)
    return response.json()


if __name__ == '__main__':
    ip = sys.argv[1]
    people_list = [{'Name': 'Tom Brovender', 'Phone': '0508710417', "Address": 'Har Shaul 907'},
                   {'Name': 'Eden Altman', 'Phone': '0546648749', "Address": 'Gary Bartiani 5'}]
    for person in people_list:
        add_one(person, ip)
    people = get_all(ip)
    if not people:
        print("ERROR: Test failed - get wasn't successful")
        exit(1)
    uid = people[0]['_id']
    param = 'Phone'
    parameter_value = people[1][param]
    update_one(ip, uid, param, parameter_value)
    person = get_one(ip, uid)
    if parameter_value != person[param]:
        print("ERROR: Test failed - update wasn't successful")
        exit(1)
    for person in people:
        uid = person['_id']
        delete_one(uid, ip)
    people = get_all(ip)
    if people:
        print("ERROR: Test failed - deletion wasn't successful")
        exit(1)
    print('E2E Test Passed Successfully')