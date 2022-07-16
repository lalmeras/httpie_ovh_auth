# Auth plugin for OVH API

## Obtain API credentials

You can find URLs to create your application credentials
(client id and secret) here:
https://github.com/ovh/python-ovh#1-create-an-application

Then, you need to perform a customer key request and validation.

```
# Replace $OVH_CLIENT_ID with the appropriate value
# Add needed method and path in accessRules list
http -b post https://api.ovh.com/1.0/auth/credential X-Ovh-Application:$OVH_CLIENT_ID accessRules:='[{"method": "GET", "path": "/*"}]'
{
    "consumerKey": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "state": "pendingValidation",
    "validationUrl": "https://eu.api.ovh.com/auth/?credentialToken=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
}
```

Visit ``validationUrl`` to validate your consumer key (you need to authenticate
and choose an expiration delay).


## Credentials in environment

Plugin can use environement variables `OVH_CLIENT_ID`,
`OVH_CLIENT_SECRET` and `OVH_CONSUMER_KEY` to perform httpie authentication.
`OVH_CLIENT_*` come from application creation. `OVH_CONSUMER_KEY` is the
`consumerKey` attribute obtained from credential validation.

Rename ``auth.env.tpl`` to ``auth.env`` and insert your credentials.

Configure your environment before running httpie commands by sourcing this file:

```
# Setup environment variables
source auth.env
# Check authentication setup with profile API
http -b --auth-type ovh https://api.ovh.com/1.0/me
```


## Credentials with ``-a`` option

Not yet implemented.


## Credentials with configuration file

Not yet implemented.


## Interactive credential generation

Not yet implmented.


## Implementation

Here is the official API implementation: https://github.com/ovh/python-ovh

This library does not depend on `python-ovh`.


## OVH API

API documentation available here: https://api.ovh.com/


## Development

```
## install pipenv
# dnf install pipenv or apt install pipenv
## init virtualenv with pipenv
pipenv install --dev
## launch tests in pipenv environment
pipenv run pytest
## launch tests for all envs
pipenv run tox
```

## Release

Stable branch is `master`; development branch is `dev`. Usual release steps are :

```
# install dev tools and switch in pipenv
pipenv install --dev
pipenv shell

# if needed, update Pipfile.lock and commit changes
pipenv lock --clear
pipenv install --dev

# prepare dev branch for release...
# check CHANGELOG.md, README.md, ...
# ...
# update version (1.1.0, 1.2.0, ...)
git fetch
git checkout master
git pull
git merge origin/dev
tbump VERSION
git checkout dev
tbump --no-tag VERSION.dev0

# publish (pypi credentials required)
git checkout vVERSION
rm -rf dist build
python -m build --sdist --wheel
# fake upload
# run pypi-server in another shell
mkdir -p /tmp/packages && pypi-server run -P . -a . /tmp/packages/
twine upload  -u "" -p "" --repository-url http://localhost:8080/ dist/*.whl dist/*.tar.gz

# real upload
twine upload dist/*.whl dist/*.tar.gz
```

