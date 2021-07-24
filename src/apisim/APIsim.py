from typing import List
import requests
import json
import pandas as pd
from tabulate import tabulate
import argparse

from unit import request_unit, auth_request_unit, token_unit
from customrequests import customrequest


class apisim:
    def __init__(self,  loop=False, verbose=False, repeat=0, print_steps=True) -> None:
        super().__init__()
        self.loop = loop
        self.verbose = verbose
        self.repeat = repeat
        self.print_steps = print_steps

    def data_from_file(self, input_file, mode, url=None):
        pass

    def requests_from_file(self):
        pass

    def _print_responses(self, resp_list: List):
        tables = pd.DataFrame(resp_list)
        tables.columns = ["endpoint", "value",
                          "time", "mode", "status", "outcome"]
        print("\n")
        print(tabulate(tables, headers='keys', tablefmt='psql'))

    def call(self, mode, urls=None, command=None, input_file=None, password=None, username=None):
        x = request_unit(urls, mode)
        y = auth_request_unit({"username": username, "password": password})
        req = customrequest()
        if command == None:
            req.multi_request(req_unit=x)
            self._print_responses(req.return_responses())
        if command == "login":
            return req.login(x, y)
        if command == "safe":
            return req.multi_safe_request(x)
        if command == "file":
            if mode == "get":
                return self.from_file(input_file, mode)
            if mode == "post":
                return self.from_file(input_file, mode, url=urls)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='APIsim',
                                     usage='%(prog)s [options] url(s)',
                                     description='Simulate users calling an api')

    parser.add_argument('--url',
                        type=str,
                        help='the api url to call',
                        nargs='*'
                        )
    parser.add_argument('--creds',
                        type=str,
                        help='credentials to get a token',
                        nargs='+'
                        )

    parser.add_argument('--repeat',
                        '-r',
                        type=int,
                        help='times to repeat the call',
                        default=1
                        )

    parser.add_argument('--command',
                        '-c',
                        type=str,
                        help='Type of request',
                        )

    parser.add_argument('--delay',
                        '-d',
                        type=int,
                        help='seconds delay between repeats',
                        default=0
                        )

    parser.add_argument('--file',
                        '-f',
                        type=str,
                        help='input file to get data',
                        default=""
                        )

    parser.add_argument('--printsteps',
                        '-ps',
                        help='print the api calling steps',
                        action="store_true"
                        )
    parser.add_argument('--fallback',
                        '-fb',
                        action="store_true",
                        help='fallback to tor if fails'
                        )

    parser.add_argument("-v", "--verbose", action="store_true",
                        help="increase output verbosity")

    args = parser.parse_args()
    ps = False
    if args.printsteps:
        ps = True
    u = apisim(
        repeat=args.repeat,
        print_steps=ps)

    if args.fallback:
        u.fallback_enabled = True

    if args.url:
        url_list = args.url

    if args.command == "login":
        u.call(command="login", urls=url_list, mode="post",
               username=args.creds[0], password=args.creds[1])

    if args.command == "get":
        u.call(urls=url_list, mode=(args.command))

    if args.file:
        if args.command == "get":
            u.call(command="file", mode=(args.command), input_file=args.file)
        if args.command == "post":
            u.call(command="file", mode=(args.command),
                   urls=args.url, input_file=args.file)
