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
           print_steps=ps,
           fallback_enabled=True)
   
if args.fallback:
   u.fallback_enabled = True

if args.url:
   url_list = args.url

if args.command == "login":
   u.call(command="login", urls=url_list, mode="post", username=args.creds[0], password=args.creds[1])

if args.command == "get":
   u.call(urls=url_list, mode=(args.command))

   
if args.file:
   if args.command == "get":
      u.call(command="file", mode=(args.command), input_file=args.file)
   if args.command == "post":
      u.call(command="file", mode=(args.command), urls=args.url, input_file=args.file)



if args.verbose:
   u.print_responses()