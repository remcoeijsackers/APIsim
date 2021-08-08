from typing import List
import argparse

from unit import request_unit
from customrequests import customrequest
from transformer import datatransformer

from cli.apisimdashboard import dashboard
from db.db import query
from util.util import Settings, helpers
class apisim:
    def __init__(self, print_steps, table, fallback, store, repeat) -> None:
        super().__init__()
        self.table = table
        self.print_steps = print_steps
        self.fallback = fallback
        self.repeat = repeat
        self.store = store
        self._req_unit = request_unit

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
        if self.table:
            self.__print_responses(req.return_responses())

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
        h = helpers()
        return h.print_help()



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

    parser.add_argument('--commands', choices=['verbose', 'fallback', 'table', 'store'],
                        nargs="+",
                        type=str,
                        help='type of command',
                        )

    parser.add_argument("-v", "--visual", action="store_true",
                        help="show cli dashboard", default=False)

    parser.add_argument("-q", "--query", action="store_true",
                        help="query the db", default=False)
    
    parser.add_argument("-e", "--edit", action="store_true",
                        help="edit the settings")

    settings = Settings("src/apisim/config/config.yaml")
    cu = settings.loadconfig()

    args = parser.parse_args()
    ps = cu.auto_printsteps
    t = cu.auto_printtable
    s = cu.auto_store
    fb = cu.auto_fallback
    r = cu.count_repeat

    try:
        if 'verbose' in args.commands:
            ps = True
        if 'table' in args.commands:
            t = True
        if 'store' in args.commands:
            s = True
        if 'fallback' in args.commands:
            fb = True
    except:
        pass
    
    u = apisim(print_steps=ps, table=t, fallback=fb, store=s, repeat=args.repeat)

    if args.edit:
        u.edit_settings()

    if args.query:
        u.query_db()

    if args.creds:
        u.authcall(urls=args.url, mode=(args.mode), loginurl=args.authurl,
                   username=args.creds[0], password=args.creds[1])

    if args.url:
        if not args.visual:
            u.call(urls=args.url, mode=(args.mode))
        else:
            u.dashboardcall(args.mode, args.url)

    if not args.url and not args.creds and not args.edit and not args.query:
        print(u.print_help() + '\n please provide an url to login to')




