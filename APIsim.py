
from apib import req_tor
from types import new_class
from typing import Text
import requests
import json
import asyncio
import time
import tqdm
import pandas as pd
import requests
from multiprocessing.dummy import Pool as ThreadPool
from concurrent.futures import ThreadPoolExecutor, as_completed
from torpy.http.requests import TorRequests

from tqdm.cli import main

# https://stackoverflow.com/questions/62007674/multi-thread-requests-python3


class abreaker:
    def __init__(self, endpoints, commands=None, body=None, loop=False, repeat=0, sleeptime=0) -> None:
        super().__init__()
        self.endpoints = endpoints
        self.commands = commands
        self.body = body
        self.loop = loop
        self.repeat = repeat
        self.sleeptime = int(sleeptime)
        self._responses = []
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

    def multi_request(self):
        def req(url):
            try:
                res = requests.get(url, stream=True)
                self._responses.append(res.content)
            except requests.exceptions.RequestException as e:
                print(e)
                return e
        threads = []

        with ThreadPoolExecutor(max_workers=50) as executor:
            for url in self.endpoints:
                for repeat in tqdm.tqdm(range(self.repeat)):
                    threads.append(executor.submit(req, url))

            for task in as_completed(threads):
                self._tables = pd.DataFrame(
                    list(zip(self.endpoints, self._responses)))
                self._tables.columns = ["endpoint", "value"]
                return task.result()

        return self._tables

    def save_request(self):
        def req_tor(url):
            try:
                with TorRequests() as tor_requests:
                    with tor_requests.get_session() as sess:
                        res = sess.get(url).json()
                        self._responses.append(res)
            except e:
                return e
        for url in self.endpoints:
            req_tor(url)

        self._tables = pd.DataFrame(
            list(zip(self.endpoints, self._responses)))
        self._tables.columns = ["endpoint", "value"]
        return self._tables

    def login(self, url, username, password, command=None):
        if command == None:
            data = '{%s,%s}'.format(username, password)
            self._token = requests.get(url, data=data)
        if command == "account":
            self._login = username
            self._password = password

    def print_responses(self):
        print(self._tables)

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

    def push(self, command=None):
        pass


url_list = ['http://httpbin.org/ip', 'http://httpbin.org/ip']
u = abreaker(endpoints=url_list,
             commands=("get"),
             # body=(",data={}".format(js)),
             repeat=5)

u.call()
u.print_responses()
