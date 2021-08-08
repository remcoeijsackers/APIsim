from typing import List
import pandas as pd
import argparse

from unit import request_unit, config_unit
from customrequests import customrequest
from transformer import datatransformer

from cli.apisimdashboard import dashboard
from db.db import query
from util.util import Settings, helpers
class apisim:
    def __init__(self, print_steps, verbose, fallback, store, repeat) -> None:
        super().__init__()
        self.verbose = verbose
        self.print_steps = print_steps
        self.fallback = fallback
        self.repeat = repeat
        self.store = store
        self._req_unit = request_unit

    def __data_from_file(self, input_file, mode, url=None):
        pass

    def __data_to_file(self, output_file, mode, url=None):
        pass

    def __requests_from_file(self):
        pass

    def __print_responses(self, resp_list: List):
        trans = datatransformer()
        print(trans.print_response_table(resp_list))

    def dashboardcall(self, mode, urls) -> dashboard:
        self._req_unit = request_unit(urls, mode)
        dash = dashboard(mode, urls, self.repeat, self._req_unit)
        return dash
    
    def call(self, mode, urls=None, password=None, username=None, loginurl=None):
        self._req_unit = request_unit(urls, mode)
        req = customrequest(
            repeat=self.repeat, print_steps=self.print_steps, fallback_enabled=self.fallback, store=self.store)
        if username and password:
            self._req_unit = request_unit(
                urls, mode, {"username": username, "password": password}, auth_url=loginurl[0])

        req.multi_request(req_unit=self._req_unit)
        if self.verbose:
            self.__print_responses(req.return_responses())

    def filecall(self, mode, xfile):
        if mode == "get":
            return self.__data_from_file(xfile, mode)
        if mode == "post":
            return self.from_file(xfile, mode, url=urls)

    def safecall(self, mode) -> None:
        req = customrequest(
            repeat=self.repeat, print_steps=self.print_steps, fallback_enabled=self.fallback, store=self.store)
        return req.multi_safe_request(self._req_unit)

    def edit_settings(self) -> None:
        return self.settings.editconfig()

    def query_db(self) -> None:
        q = query()
        print(q.get())
    
    def print_help(self) -> None:
        print(helpers.print_help())



if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='APIsim',
                                     usage='%(prog)s [options] url(s)',
                                     description='Simulate users calling an api')

    parser.add_argument('url',
                        type=str,
                        help='the api url to call',
                        nargs='*'
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

    parser.add_argument('--commands', choices=['ps', 'fb', 'v', 's', 'dash'],
                        nargs="+",
                        type=str,
                        help='type of command',
                        )

    parser.add_argument('--file',
                        '-f',
                        type=str,
                        help='input file to get data',
                        default=""
                        )

    parser.add_argument("-q", "--query", action="store_true",
                        help="query the db", default=False)
    
    parser.add_argument("-e", "--edit", action="store_true",
                        help="edit the settings")

    settings = Settings("src/apisim/config/config.yaml")
    cu = settings.loadconfig()

    args = parser.parse_args()
    ps = cu.auto_printsteps
    v = cu.auto_printtable
    s = cu.auto_storeo
    fb = cu.auto_fallback
    r = cu.count_repeat

    try:
        if 'ps' in args.commands:
            ps = True
        if 'v' in args.commands:
            v = True
        if 's' in args.commands:
            s = True
        if 'fb' in args.commands:
            fb = True
    except:
        pass
    
    u = apisim(ps, v, fb, s, args.repeat)

    if args.edit:
        u.edit_settings()

    if args.query:
        u.query_db()
        
    if args.file:
        if args.mode == "get":
            u.filecall(command="file", mode=(args.mode), input_file=args.file, print_table=args.verbose)
        if args.mode == "post":
            u.filecall(command="file", mode=(args.mode),
                   urls=args.url, input_file=args.file)

    if args.creds:
        u.authcall(urls=args.url, mode=(args.mode), loginurl=args.authurl,
                   username=args.creds[0], password=args.creds[1], repeat=args.repeat, print_steps=args.printsteps, fallback=args.fallback, print_table=args.verbose)

    if args.url:
        u.call(urls=args.url, mode=(args.mode),
                   repeat=args.repeat, print_steps=args.printsteps, fallback=args.fallback, print_table=args.verbose)
    else:
        if not args.edit or args.query:
            print(u.print_help()+ '\n please provide an url to login to')

    if "dash" in args.commands:
        u.dashboardcall(args.mode, args.url, repeat=args.repeat)


