# APIsim

## Installation
Api testing and automation
### pypi
`pip install APIsim`

### source
`./setup.py`
## Usage - CLI

call 'get' on an endpoint 100 times, fallback to tor if failed
`apisim --url 'https://api.agify.io?name=apisim' -r=100 -c=get -fb`

call 'get' on an endpoint, print each step
`apisim --url 'https://api.agify.io?name=apisim' -c=get -ps`

call 'get' on multiple endpoints, print out the results in a table
`apisim --url 'https://api.agify.io?name=apisim' 'https://api.agify.io?name=python' 'https://api.agify.io?name=rest' -r=100 -c=get -v`

authenticate on a api, call 'get' on a endpoint, print out the results in a table
`apisim --authurl 'https://api.test.io/api/token/'  --creds testaccount bot123 --command=get --url 'https://api.test.io/api/data/' -v`

## Capabilities

* The user can run any number of requests, and get the response (meta)data in any number of formats.
* The user can set the requests to run on a schedule/loop continuosly, and should be able to easily pipe trough the output. 
* The user can store the outputs, and qeury it easily. 

* The user can set up 'missions' that can consist of multiple unrelated requests, and tie this to a schedule.

* The user can provide an input file for 2 goals;
    * A file with endpoints that the program will call with set rules. 
    * A file with data that the program will push with set rules.

* The user can provide an output file for 2 goals;
    * A file that will contain all the mission data
    * A file that will contain the response data of the requests