from typing import Text
import requests
import json
import time
import tqdm
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from torpy.http.requests import TorRequests

from tqdm.cli import main
from tabulate import tabulate

class apisim:
    def __init__(self, endpoints, commands=None, body=None, loop=False, repeat=0, sleeptime=0, print_steps=False, verbose=False) -> None:
        super().__init__()
        self.endpoints = endpoints
        self.commands = commands
        self.body = body
        self.loop = loop
        self.repeat = repeat
        self.print_steps = print_steps
        self.verbose = verbose
        self.sleeptime = int(sleeptime)
        self._responses = []
        self._endpoints = []
        self._elapsed_time = []
        self._mode = []
        self._tables = any
        self._login = any
        self._password = any
        self._auth = any
        self._token = any

    def normType(self, type_var):
        if type(type_var) is str:
            return type_var
        if type(type_var) is Text or int:
            return str(type_var)
        try:
            json.dumps(type_var)
        except:
            return "unkown value"

    def slow_request(self):
        time.sleep(self.sleeptime)
        def _irequest(endpoint, command, body=None):
            if body is None:
                response = eval('requests.{}(endpoint)'.format(command))
            else:
                response = eval(
                    'requests.{}(endpoint {})'.format(command, body))
            res = response.text
            return res
        responses = []
        lendpoints = []
        loop = any
        if self.loop is True:
            loop = True

        while loop:
            if self.body is None:
                x = _irequest(self.endpoints, self.commands)
                ne = self.normType(x)
                responses.append(ne)
                lendpoints.append(self.endpoints)
            else:
                if command == "post":
                    x = self._irequest(
                        self.endpoints, self.commands, self.body)
                else:
                    x = self._irequest(self.endpoints, self.commands)
                ne = self.normType(x)
                responses.append(ne)
                lendpoints.append(self.endpoints)
            if self.sleeptime:
                time.sleep(self.sleeptime)
            if self.loop is False:
                loop = False
            self._tables = pd.DataFrame(list(zip(lendpoints, responses)))
            self._tables.columns = ["endpoint", "value"]
        return self._tables

    def safe_request(self, url):
        #time.sleep(self.sleeptime)
        print('in save request')
        def req_tor(url):
            try:
                with TorRequests() as tor_requests:
                    with tor_requests.get_session() as sess:
                        res = sess.get(url).json()
                    self._responses.append(res)
                    self._endpoints.append(url)
                    self._elapsed_time.append(0)
                    self._mode.append("safe")
            except e:
                print(e)
   
        req_tor(url)

    def multi_request(self):
        time.sleep(self.sleeptime)
        def req(url):
            try:
                if self.commands == 'get':
                    res = requests.get(url, stream=True)
                if self.commands == 'post':
                    res = requests.post(url, stream=True)
                self._mode.append(self.commands)
                self._responses.append(res.content)
                self._endpoints.append(url)
                self._elapsed_time.append(res.elapsed.total_seconds())
                if self.print_steps:
                    print("'" + self.commands + "'" + ' on endpoint ' + url)
            #except requests.exceptions.RequestException as e:
            except:
                self.safe_request(url)
     
                
        threads = []

        with ThreadPoolExecutor(max_workers=50) as executor:
            for url in self.endpoints:
                if self.verbose:
                    for repeat in tqdm.tqdm(range(self.repeat)):
                        threads.append(executor.submit(req, url))
                else:
                    for repeat in range(self.repeat):
                        threads.append(executor.submit(req, url))
            #for task in as_completed(threads):
            #    return task.result()

        self._tables = pd.DataFrame(
                list(zip(self._endpoints, self._responses, self._elapsed_time, self._mode)))
        self._tables.columns = ["endpoint", "value", "time", "mode"]
        return self._tables



    def login(self, url, username, password, command=None):
        if command == None:
            data = '{%s,%s}'.format(username, password)
            self._token = requests.get(url, data=data)
        if command == "account":
            self._login = username
            self._password = password
        if command == "key":
            pass

    def print_responses(self):
        print("\n")
        print(tabulate(self._tables, headers='keys', tablefmt='psql'))

    def call(self, command=None):
        """
        call endpoints

        Default: 
        command=None use threading and call multiple endpoints in parralel

        Options:
        command="slow" use non threading and see the steps, usefull for debugging
        command="save" use non threading and tor network to switch IP every call

        """
        if command == None:
            return self.multi_request()
        if command == "slow":
            return self.slow_request()
        if command == "save":
            return self.save_request()




