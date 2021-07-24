import requests
import json
import pandas as pd
from tabulate import tabulate
from unit import request_unit, auth_request_unit, token_unit
class apisim:
    def __init__(self,  loop=False, verbose=False) -> None:
        super().__init__()
        self.loop = loop
        self.verbose = verbose
        self._mode = []
        self._units = []
        self._tables = any
        self._token = []
        self._calls = 0

    def login(self, req_unit, auth_unit, command=None):
        if command == None:
            response = requests.post(req_unit.url[0], data = auth_unit.payload)
            jstoken = json.loads(response.text)
            token = token_unit(jstoken['access'], req_unit.url[0])
            self._token = token
            print(self._token.token)
            return token

    def from_file(self, input_file, mode, url=None):
        urls_to_call = []
        data_to_push = []
        if mode == "get":
            try:
                with open(input_file, "r") as reader:
                    for line in reader.readlines():
                        urls_to_call.append(line)
                    x = request_unit(urls_to_call, mode)
                    self.multi_request(x)

            except TypeError:
                print("file does not exist")
                return
        if mode == "post":
            try:
                with open(input_file, "r") as reader:
                    for line in reader.readlines():
                        data_to_push.append(line)
                    self.multi_request(url, mode, body=data_to_push)

            except TypeError:
                print("file does not exist")

    def print_responses(self):
        self._tables = pd.DataFrame(self._units)
        self._tables.columns = ["endpoint", "value", "time", "mode", "status", "outcome"]
        print("\n")
        print(tabulate(self._tables, headers='keys', tablefmt='psql'))

    def check_login(self, req_unit, auth_unit):
        if self._token == []:
            return self.login(req_unit, auth_unit)

    def call(self, mode, urls=None, command=None ,input_file=None, password=None, username=None):
        x = request_unit(urls, mode)
        y = auth_request_unit({"username": username, "password": password})
        if command == None:
            print(x)
            return self.multi_request(x)
        if command == "login":
            print('in login')
            return self.login(x, y)
        if command == "safe":
            return self.multi_safe_request(x)
        if command == "file":
            if mode == "get":
                return self.from_file(input_file, mode)
            if mode == "post":
                return self.from_file(input_file, mode, url=urls)







