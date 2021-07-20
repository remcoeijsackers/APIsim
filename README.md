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