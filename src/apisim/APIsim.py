import requests
import json
import time
import tqdm
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from torpy.http.requests import TorRequests, tor_requests_session
import sys

from tqdm.cli import main
from tabulate import tabulate
from multiprocessing.pool import ThreadPool
from unit import request_unit, response_unit
class apisim:
    def __init__(self,  loop=False, repeat=0, sleeptime=0, print_steps=False, verbose=False, fallback_enabled=True) -> None:
        super().__init__()
        self.loop = loop
        self.repeat = repeat
        self.print_steps = print_steps
        self.verbose = verbose
        self.sleeptime = int(sleeptime)
        self._mode = []
        self._units = []
        self.fallback_enabled = fallback_enabled
        self._tables = any
        self._login = any
        self._password = any
        self._auth = any
        self._token = any
        self._calls = 0

    def multi_safe_request(self, req_unit):
        
        if self.print_steps:
            self._calls += 1
            print(str(self._calls) + " Safe "+ " '" + req_unit.mode + "'" + ' on endpoint ' + req_unit.url[0])


        with TorRequests() as tor_requests:
            with tor_requests.get_session(retries=3) as sess:
                def process(url):
                    status=""
                    try:
                        res = sess.get(req_unit.url[0], timeout=30)
                        status = "Succes (Tor)"
                        return res.text
                    except BaseException:
                        status = "Failed (Tor)"
                        print('get link %s error', req_unit.url[0])
                    finally:
                        response = response_unit(req_unit.url[0], res.content, req_unit.mode, res.elapsed.total_seconds(), res.status_code, status)
                        self._units.append(response)

                pool = ThreadPool(10)
                for i, w in enumerate(pool._pool):
                    w.name = 'Worker{}'.format(i)
                results = pool.map(process, [req_unit.url[0]])
                pool.close()
                pool.join()
        

    def multi_request(self, req_unit):
        
        def req(req_unit):
            status = ""
            if req_unit.mode == 'get':
                res = requests.get(req_unit.url[0], stream=True)
            if req_unit.mode == 'post':
                res = requests.post(req_unit.url[0], stream=True, data=req_unit.body[0])
            if res.status_code != 200:
                status = "Failed"
                if self.fallback_enabled:
                        self.multi_safe_request_2(req_unit)
            else:
                status = "Succes"
            x = response_unit(req_unit.url[0],res.content, req_unit.mode, res.elapsed.total_seconds(), res.status_code, status)
            self._calls += 1
            if self.print_steps:
                print(str(self._calls) + " '" + req_unit.mode + "'" + ' on endpoint ' + req_unit.url[0])
            self._units.append(x)
            

        threads = []

        with ThreadPoolExecutor(max_workers=50) as executor:
            for url in req_unit.url:
                if self.print_steps:
                    for repeat in tqdm.tqdm(range(self.repeat)):
                        threads.append(executor.submit(req, req_unit))
                else:
                    for repeat in range(self.repeat):
                        threads.append(executor.submit(req, req_unit))

    def login(self, url, username, password, command=None):
        if command == None:
            data = '{%s,%s}'.format(username, password)
            self._token = requests.get(url, data=data)
        if command == "account":
            self._login = username
            self._password = password
        if command == "key":
            pass
    
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


    def call(self, mode, urls=None, command=None ,input_file=None):
        x = request_unit(urls, mode)
        if command == None:
            return self.multi_request_2(x)
        if command == "safe":
            return self.multi_safe_request(x)
        if command == "file":
            if mode == "get":
                return self.from_file(input_file, mode)
            if mode == "post":
                return self.from_file(input_file, mode, url=urls)





