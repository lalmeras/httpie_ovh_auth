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

Plugin can use environement variables OVH\_CLIENT\_ID,
OVH\_CLIENT\_SECRET and OVH\_CONSUMER\_KEY to perform httpie authentication.

Rename ``auth.env.tpl`` to ``auth.env`` and insert your credentials.

Configure your environment before running httpie commands by sourcing this file:

```
source auth.env
```

Trigger OVH authentication with ``--auth-type`` parameter:

```
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


## OVH API

API documentation available here: https://api.ovh.com/


## Development

```
## install pipenv
# dnf install pipenv or apt install pipenv
## init virtualenv with pipenv
pipenv install --dev
## launch tests in pipenv environment
pytest
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
# update version
# increase version; may be launch multiple time to cycle dev, rc, ...
bump2version --verbose prerel [--allow-dirty] [--no-commit] [--no-tag]

# merge on main
git checkout main
git pull
git merge dev

# prepare next development version (+1dev0)
git checkout dev
bump2version --verbose --no-tag minor

# push all (launch with --dry-run to check before actual update)
# delete (git tag -d <tag> unneeded tags - dev, rc)
git push --all
git push --tag

# publish (pypi credentials required)
git checkout tag
pipenv shell
python setup.py clean --all
rm -rf dist/*
python setup.py sdist
python setup.py bdist_wheel
# fake upload
# run pypi-server in another shell
mkdir -p /tmp/packages && pypi-server -P . -a . /tmp/packages/
twine upload  -u "" -p "" --repository-url http://localhost:8080/ dist/*.whl dist/*.tar.gz

# real upload
twine upload dist/*.whl dist/*.tar.gz
```

