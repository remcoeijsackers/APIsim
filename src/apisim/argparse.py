import argparse
from APIsim import apisim

class pparser(argparse):
   def __init__(self) -> None:
      self.pars = argparse.ArgumentParser(prog='APIsim',
                                    usage='%(prog)s [options] url(s)',
                                    description='Simulate users calling an api')

parser = pparser

parser.add_argument('--url',
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

parser.add_argument('--command',
                        '-c', 
                       type=str,
                       help='Type of request',
                       default="get"
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
                       type=bool,
                       help='print the api calling steps',
                       default=False
                    )
parser.add_argument('--fallback',
                        '-fb', 
                        action="store_true",
                        help='fallback to tor if fails'
                    )

parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")

args = parser.parse_args()

if args.url:
   url_list = args.url
   u = apisim(endpoints=url_list,
           commands=(args.command),
           repeat=args.repeat, 
           sleeptime=args.delay, 
           print_steps=args.printsteps,
           fallback_enabled=False)
   if len(url_list) > 1:
      u._backup_mode="multi"
   if args.fallback:
      u.fallback_enabled = True
   u.call()
   if args.verbose:
      u.print_responses()