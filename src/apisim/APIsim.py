from typing import Text
import requests
import json
import time
import tqdm
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from torpy.http.requests import TorRequests, tor_requests_session

from tqdm.cli import main
from tabulate import tabulate
from multiprocessing.pool import ThreadPool

class apisim:
    def __init__(self, endpoints=None, commands=None, body=None, loop=False, repeat=0, sleeptime=0, print_steps=False, verbose=False, fallback_enabled=True) -> None:
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
        self._status = []
        self._outcome = []
        self.fallback_enabled = fallback_enabled
        self._tables = any
        self._login = any
        self._password = any
        self._auth = any
        self._token = any
        self._calls = 0

    def multi_safe_request(self, url, mode):
        if self.print_steps:
            self._calls += 1
            print(str(self._calls) + " Safe "+ mode + ' on endpoint ' + url)

        with TorRequests() as tor_requests:
            with tor_requests.get_session(retries=3) as sess:
                def process(url):
                    try:
                        res = sess.get(url, timeout=30)
                        self._responses.append(res.text)
                        self._elapsed_time.append(res.elapsed.total_seconds())
                        self._status.append(res.status_code)
                        return r.text
                    except BaseException:
                        print('get link %s error', url)

                pool = ThreadPool(10)
                for i, w in enumerate(pool._pool):
                    w.name = 'Worker{}'.format(i)
                results = pool.map(process, [url])
                pool.close()
                pool.join()
        self._endpoints.append(url)
        self._mode.append(mode)
        self._outcome.append("Success (Tor)")
  

    def multi_request(self, urls, mode, body=None):
        def req(url):
                if mode == 'get':
                    res = requests.get(url, stream=True)
                if mode == 'post':
                    res = requests.post(url, stream=True, data=body)
                self._mode.append(mode)
                self._responses.append(res.content)
                self._endpoints.append(url)
                self._elapsed_time.append(res.elapsed.total_seconds())
                self._status.append(res.status_code)
                self._calls += 1
                if res.status_code == 429:
                    self._outcome.append("Failed")
                    if self.fallback_enabled:
                            self.multi_safe_request(url, mode)
                else: 
                    self._outcome.append("Succes")
                if self.print_steps:
                    print(str(self._calls) + "'" + self.commands + "'" + ' on endpoint ' + url)
      
        threads = []

        with ThreadPoolExecutor(max_workers=50) as executor:
            for url in urls:
                if self.print_steps:
                    for repeat in tqdm.tqdm(range(self.repeat)):
                        threads.append(executor.submit(req, url))
                else:
                    for repeat in range(self.repeat):
                        threads.append(executor.submit(req, url))

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
                    self.multi_request(urls_to_call, mode)

            except TypeError:
                print("file does not exist")
        if mode == "post":
            try:
                with open(input_file, "r") as reader:
                    for line in reader.readlines():
                        data_to_push.append(line)
                    self.multi_request(url, mode, body=data_to_push)

            except TypeError:
                print("file does not exist")



    def print_responses(self):
        self._tables = pd.DataFrame(
                list(zip(self._endpoints, self._responses, self._elapsed_time, self._mode, self._status, self._outcome)))
        self._tables.columns = ["endpoint", "value", "time", "mode", "status", "outcome"]
        print("\n")
        print(tabulate(self._tables, headers='keys', tablefmt='psql'))
        #return

    def call(self, mode, urls=None, command=None ,input_file=None):
        if command == None:
            return self.multi_request(urls, mode)
        if command == "safe":
            return self.multi_safe_request(urls, mode)
        if command == "file":
            if mode == "get":
                return self.from_file(input_file, mode)
            if mode == "post":
                return self.from_file(input_file, mode, url=urls)





