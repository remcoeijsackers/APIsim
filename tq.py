from tq import progress_wrapped
import requests
import json
import asyncio
import time
import tqdm
import pandas as pd
import functools
import threading


class abreaker:
    def __init__(self, sleeptime=0, **kwargs) -> None:
        super().__init__()
        self.type_var = any
        self.endpoints = list(kwargs['endpoints'])
        self.loop = kwargs['loop']
        self.sleeptime = int(sleeptime)

    def provide_progress_bar(function, tstep=0.2, tqdm_kwargs={}, args=[], kwargs={}):

        ret = [None]  # Mutable var so the function can store its return value

        def myrunner(function, ret, *args, **kwargs):
            ret[0] = function(*args, **kwargs)

        thread = threading.Thread(target=myrunner, args=(
            function, ret) + tuple(args), kwargs=kwargs)
        #pbar = tqdm(**tqdm_kwargs)
        pbar = tqdm.tqdm(bar_format='{l_bar}{bar}{r_bar}')

        thread.start()
        while thread.is_alive():
            thread.join(timeout=tstep)
            pbar.update(tstep)
        pbar.close()
        return ret[0]

    def progress_wrapped(tstep=0.2, tqdm_kwargs={}):
        """Decorate a function to add a progress bar"""
        def real_decorator(function):
            @functools.wraps(function)
            def wrapper(*args, **kwargs):
                return abreaker.provide_progress_bar(function, tstep=tstep, tqdm_kwargs=tqdm_kwargs, args=args, kwargs=kwargs)
            return wrapper
        return real_decorator

    def _irequest(self, endpoint):
        response = requests.get(endpoint)
        res = response.text
        return res

    @progress_wrapped()
    def cusRequest(self):
        responses = []
        loop = any
        if self.loop is True:
            loop = True

        while loop:
            for endpoint in self.endpoints:
                x = self._irequest(endpoint)
                responses.append(x)
            if self.sleeptime:
                time.sleep(self.sleeptime)
            if self.loop is False:
                loop = False
        return pd.DataFrame(responses)

    def normType(self):
        if type(self.type_var) is json:
            return json.dumps(self.type_var)
        if type(self.type_var) is str:
            return self.type_var
        if type(self.type_var) is int:
            return str(self.type_var)


x = abreaker(
    endpoints=("https://www.random.org/strings/?num=2&len=10&digits=on&unique=on&format=plain&rnd=new",
               "https://www.random.org/strings/?num=2&len=15&digits=on&unique=on&format=plain&rnd=new"),
    loop=False,
    sleeptime=1
)
print(x.cusRequest())
