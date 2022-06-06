from os.path import exists
from os import remove
import requests


base_url = "https://bt-anv.tls.ai/bt/api"


def login(user, password):
    credentials = {"username": user, "password": password}
    resp = requests.post(url=f'{base_url}/login', json=credentials, verify=False)
    token = resp.json()["token"]
    return token


def get_subjects(token, offset, limit):
    print(f"fetching subjects {offset} up to {offset+limit}")
    subjects = []
    querystring = {"offset": f"{offset}", "sortOrder": "desc", "limit": f"{limit}"}
    headers = {"Accept": "application/json",
               "Authorization": "Bearer " + token}
    response = requests.request("GET", url=f'{base_url}/subjects', headers=headers, params=querystring, verify=False)
    for subject in response.json()['items']:
        subjects.append({
            'name': subject['name'],
            'createdAt': subject['createdAt'],
            'description': subject['description'],
            'groups': subject['groups'],
        })
    return subjects


def write_subjects(token):
    subjects = []
    offset = 0
    limit = 1000
    current_subjects = get_subjects(token, offset, limit)
    while len(current_subjects) == limit:
        subjects+=current_subjects
        offset += limit
        current_subjects = get_subjects(token, offset, limit)

    subjects+=current_subjects

    path = "/Users/User/Desktop/WatchList.txt"

    if exists(path):
        remove(path)

    offset = 0
    total = offset + len(subjects)

    with open(path, "w") as file:
        for subject in subjects:
            file.write(f"{subject.__str__()}\n")
            offset +=1
            print(f"writing to file {offset}/{total}")
    print(f"File is Ready at {path}")


def get_cameras(token, offset, limit):
    print(f"fetching cameras {offset} up to {offset+limit}")
    cameras = []
    querystring = { "offset": f"{offset}", "sortOrder": "desc", "limit": f"{limit}"}
    headers = {"Accept": "application/json",
               "Authorization": "Bearer " + token}
    response = requests.request("GET", url=f"{base_url}/cameras", headers=headers, params=querystring, verify=False)
    for camera in response.json()['items']:
        cameras.append({
            'name': camera['title'],
            'id': camera['id'],
            'pipe': camera['pipe'],
            'url': camera['videoUrl'],
            'group': camera['cameraGroupId'],
        })
    return cameras


def write_cameras(token):
    subjects = []
    offset = 0
    limit = 1000

    current_cameras = get_cameras(token, offset, limit)
    while len(current_cameras) == limit:
        cameras+=current_cameras
        offset += limit
        current_cameras = get_cameras(token, offset, limit)

    cameras+=current_cameras

    path = "/Users/User/Desktop/Cameras.txt"

    if exists(path):
        remove(path)

    offset = 0
    total = offset + len(subjects)

    with open(path, "w") as file:
        for camera in cameras:
            file.write(f"{camera.__str__()}\n")
            offset +=1
            print(f"writing to file {offset}/{total}")
    print(f"File is Ready at {path}")


def get_license(token):
    headers = {"Accept": "application/json",
               "Authorization": "Bearer " + token}
    response = requests.request("GET", url=f"{base_url}/bt-licensing/details/license-details", headers=headers, verify=False)
    license = response.json()

    file = open("/Users/User/Desktop/license.txt", "w")
    file.write(f'{license}')
    file.close()


if __name__ == '__main__':
    token = login('AnyVisionAdmin', 'AVpa$$word!')
    get_subjects(token, 0, 1000000)
    write_subjects(token)
    get_cameras(token, 0, 1000)
    get_license(token)