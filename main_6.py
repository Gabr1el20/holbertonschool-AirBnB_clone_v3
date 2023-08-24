#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    r = requests.get("http://0.0.0.0:5000/api/v1/users")
    r_j = r.json()
    print(type(r_j))
    print(len(r_j))
    for user_j in r_j:
        if user_j.get('email') in ["a@a.com", "b@b.com", "c@c.com", "d@d.com"]:
            print("OK")
        else:
            print("Missing: {}".format(user_j.get('email')))
        if user_j.get('id') is None:
            print("Missing ID for User: {}".format(user_j.get('name')))