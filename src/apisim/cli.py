import argparse
from APIsim import apisim


parser = argparse.ArgumentParser(prog='APIsim',
                                    usage='%(prog)s [options] url(s)',
                                    description='Simulate users calling an api')

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

u = apisim(
           repeat=args.repeat, 
           sleeptime=args.delay, 
           print_steps=args.printsteps,
           fallback_enabled=True)

if args.fallback:
   u.fallback_enabled = True

if args.url:
   url_list = args.url
   u.call(urls=url_list, mode=(args.command))

if args.file:
   if args.command == "get":
      u.call(command="file", mode=(args.command), input_file=args.file)
   if args.command == "post":
      u.call(command="file", mode=(args.command), urls=args.url, input_file=args.file)



if args.verbose:
   u.print_responses()