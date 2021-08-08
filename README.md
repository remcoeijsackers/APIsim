# APIsim
apisim allows users to easily handle multiple requests,
and outputs & stores usable data. 
## Installation

### source
`pip install .`
## Usage - CLI

call 'get' on an endpoint,
`apisim 'https://api.agify.io?name=apisim'`

call 'post' on an endpoint 100 times, fallback to tor if failed
`apisim --url 'https://api.agify.io?name=apisim' -r=100 -m=post --commands fallback`

call 'get' on an endpoint, print each step 
`apisim --url 'https://api.agify.io?name=apisim' -m=get --commands verbose`

call 'get' on multiple endpoints, print out the results in a table
`apisim --url 'https://api.agify.io?name=apisim' 'https://api.agify.io?name=python' 'https://api.agify.io?name=rest' -m=get --commands table`

#### Authenticate

authenticate on a api, call 'get' on a endpoint, print out the results in a table
`apisim --authurl 'https://api.test.io/api/token/'  --creds testaccount bot123 --mode=get --url 'https://api.test.io/api/data/' --commands verbose`

#### Cli Dashboard

authenticate on a api, call 'get' on a endpoint, print out the results in ascii dashboard
`apisim --authurl 'https://api.test.io/api/token/'  --creds testaccount bot123 --mode=get --url 'https://api.test.io/api/data/' --visual`

#### Store & Query
call 'get' on a endpoint, store the results in the db
`apisim --mode=get --url 'https://api.test.io/api/data/' --commands store`

query the database 
`apisim -q (optional filters)`

change the settings
`apisim -e`
