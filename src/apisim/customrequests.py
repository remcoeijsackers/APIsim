import requests
import json
from concurrent.futures import ThreadPoolExecutor
from torpy.http.requests import TorRequests
from unit import request_unit, response_unit
from multiprocessing.pool import ThreadPool
import tqdm


class customrequest:
    def __init__(self, verbose=False, fallback_enabled=False, repeat=1, print_steps=False) -> None:
        super().__init__()
        self._response = None
        self._units = []
        self._failed_requests = []
        self.verbose = verbose
        self.fallback_enabled = fallback_enabled
        self.repeat = repeat
        self.print_steps = print_steps
        self._calls = 0
        self._token = ""  # TODO: This needs to be handled on a per request_unit instance

    def return_responses(self):
        return self._units

    def multi_safe_request(self, req_unit: request_unit) -> None:
        self._calls += 1
        if self.print_steps:
            print(str(self._calls) + " Safe " + " '" + req_unit.mode +
                  "'" + ' on endpoint ' + req_unit.url[0])

        with TorRequests() as tor_requests:
            with tor_requests.get_session(retries=3) as sess:
                def process(url):
                    status = ""
                    try:
                        if req_unit.token != "":
                            headers = {
                                'Authorization': 'Bearer {}'.format(req_unit.token)}
                        else:
                            headers = None
                        res = sess.get(
                            req_unit.url[0], headers=headers, timeout=30)

                        if res.status_code != 200:
                            status = "Failed (Tor)"
                        else:
                            status = "Succes (Tor)"
                        return res.text
                    except BaseException:
                        status = "Failed (Tor)"
                        print('get link {} error', req_unit.url[0])
                    finally:
                        response = response_unit(
                            req_unit.url[0], value=res.content, mode=req_unit.mode, time=res.elapsed.total_seconds(), status=res.status_code, outcome=status)
                        self._units.append(response)

                pool = ThreadPool(10)
                for i, w in enumerate(pool._pool):
                    w.name = 'Worker{}'.format(i)
                results = pool.map(process, [req_unit.url[0]])
                pool.close()
                pool.join()

    def multi_request(self, req_unit: request_unit) -> response_unit:
        """
        Carries out the request(s) in a request unit.
        Param: req_unit: a request unit class instance
        """
        if req_unit.auth:
            req_unit = self.login(req_unit)

        def req(req_unit):
            status = ""

            headers = {
                'Authorization': 'Bearer {}'.format(req_unit.token)}

            if req_unit.mode == 'get':
                res = requests.get(
                    req_unit.url[0], stream=True, headers=headers)
            if req_unit.mode == 'post':
                res = requests.post(
                    req_unit.url[0], stream=True, data=req_unit.body[0], headers=headers)
            if res.status_code != 200:
                status = "Failed"
                if self.fallback_enabled:
                    self._failed_requests.append(req_unit)
            else:
                status = "Succes"
            response = response_unit(
                req_unit.url[0], value=res.content, mode=req_unit.mode, time=res.elapsed.total_seconds(), status=res.status_code, outcome=status)
            self._calls += 1
            if self.print_steps:
                print(str(self._calls) + " '" + req_unit.mode +
                      "'" + ' on endpoint ' + req_unit.url[0])
            self._units.append(response)

        threads = []

        with ThreadPoolExecutor(max_workers=50) as executor:
            for url in req_unit.url:
                for i in range(self.repeat):
                    threads.append(executor.submit(req, req_unit))

    def custom_request(self, req_unit: request_unit) -> response_unit:
        """
        Carries out the request(s) in a request unit.
        Param: req_unit: a request unit class instance
        """
        if req_unit.auth:
            req_unit = self.login(req_unit)

        def req(req_unit):
            status = ""

            headers = {
                'Authorization': 'Bearer {}'.format(req_unit.token)}

            if req_unit.mode == 'get':
                res = requests.get(
                    req_unit.url[0], stream=True, headers=headers)
            if req_unit.mode == 'post':
                res = requests.post(
                    req_unit.url[0], stream=True, data=req_unit.body[0], headers=headers)
            if res.status_code != 200:
                status = "Failed"
                if self.fallback_enabled:
                    self._failed_requests.append(req_unit)
            else:
                status = "Succes"
            response = response_unit(
                req_unit.url[0], value=res.content, mode=req_unit.mode, time=res.elapsed.total_seconds(), status=res.status_code, outcome=status)
            self._calls += 1
            if self.print_steps:
                print(str(self._calls) + " '" + req_unit.mode +
                      "'" + ' on endpoint ' + req_unit.url[0])
            self._units.append(response)
            return response

        for url in req_unit.url:
            for i in range(self.repeat):
                return req(req_unit)
                          


        if self.fallback_enabled:
            # TODO: multi safe request should receive a list
            for unit in self._failed_requests:
                self.multi_safe_request(unit)

    def login(self, req_unit: request_unit):
        response = requests.post(req_unit.auth_url, data=req_unit.auth)
        jstoken = json.loads(response.text)
        req_unit.token = jstoken['access']
        return req_unit

    def check_login(self, req_unit: request_unit):
        if self._token == []:
            return self.login(req_unit)


class filerequest:
    def __init__(self) -> None:
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
