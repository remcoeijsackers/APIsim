from typing import List
import pandas as pd
import argparse

from unit import request_unit
from customrequests import customrequest
from transformer import datatransformer

from cli.apisimdashboard import dashboard
from db.db import query

class apisim:
    def __init__(self, verbose=False, store=False) -> None:
        super().__init__()
        self.verbose = verbose
        self.store = store
        self._req_unit = request_unit

    def data_from_file(self, input_file, mode, url=None):
        pass

    def requests_from_file(self):
        pass

    def _print_responses(self, resp_list: List):
        trans = datatransformer()
        print(trans.print_response_table(resp_list))

    def dashboard(self, mode, urls, repeat=1, fallback=True):
        self._req_unit = request_unit(urls, mode)
        x = dashboard(mode, urls, repeat, self._req_unit)
        return x

    def query_db(self):
        q = query()
        print(q.get())


    def call(self, mode, urls=None, command=None, input_file=None, password=None, username=None, repeat=1, loginurl=None, print_steps=False, fallback=False, print_table=False):
        self._req_unit = request_unit(urls, mode)
        req = customrequest(
            repeat=repeat, print_steps=print_steps, fallback_enabled=fallback, store=self.store)
        if username and password:
            self._req_unit = request_unit(
                urls, mode, {"username": username, "password": password}, auth_url=loginurl[0])

        if command == None:
            req.multi_request(req_unit=self._req_unit)
            if print_table:
                self._print_responses(req.return_responses())

        if command == "safe":
            return req.multi_safe_request(self._req_unit)
        if command == "file":
            if mode == "get":
                return self.from_file(input_file, mode)
            if mode == "post":
                return self.from_file(input_file, mode, url=urls)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='APIsim',
                                     usage='%(prog)s [options] url(s)',
                                     description='Simulate users calling an api')

    parser.add_argument('eurl', type=str, nargs='*',
                    help='url when no flags are provided')

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
    parser.add_argument('--authurl',
                        type=str,
                        help='url to get a token',
                        nargs=1
                        )

    parser.add_argument('--repeat',
                        '-r',
                        type=int,
                        help='times to repeat the call',
                        default=1
                        )

    parser.add_argument('--mode',
                        '-m',
                        type=str,
                        help='Type of request',
                        default="get"
                        )

    parser.add_argument('--command',
                        type=str,
                        help='type of command',
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
                        help="increase output verbosity", default=False)

    parser.add_argument("-s", "--store", action="store_true",
                        help="store the results of the requests", default=False)
    
    parser.add_argument("-q", "--query", action="store_true",
                        help="query the db", default=False)

    args = parser.parse_args()

    u = apisim()
    if args.store:
        u = apisim(store=True)

    if args.query:
        u.query_db()
        
    if args.file:
        if args.mode == "get":
            u.call(command="file", mode=(args.mode), input_file=args.file, print_table=args.verbose)
        if args.mode == "post":
            u.call(command="file", mode=(args.mode),
                   urls=args.url, input_file=args.file)

    if args.command == None:
        if args.creds:
            u.call(urls=args.url, mode=(args.mode), loginurl=args.authurl,
                   username=args.creds[0], password=args.creds[1], repeat=args.repeat, print_steps=args.printsteps, fallback=args.fallback, print_table=args.verbose)
        else:
            if args.url:
                u.call(urls=args.url, mode=(args.mode),
                   repeat=args.repeat, print_steps=args.printsteps, fallback=args.fallback, print_table=args.verbose)
            else:
                if args.eurl:
                    u.call(urls=args.eurl, mode=("get"),
                   repeat=args.repeat, print_steps=args.printsteps, fallback=args.fallback, print_table=args.verbose)
                else: 
                    print("please provide an url to call")

    if args.command == "visual":
        u.dashboard(args.mode, args.url, repeat=args.repeat)


