# Auth plugin for OVH API

## httpie\_ovh\_auth in a nutshell

This plugin allows, based on `OVH_CLIENT_ID`, `OVH_CLIENT_SECRET` and `OVH_CONSUMER_KEY`
to perform OVH API calls with httpie tool.

```
# Configure an OVH application to get OVH_CLIENT_ID, OVH_CLIENT_SECRET
# Perform authentication to get OVH_CONSUMER_KEY
# Setup environment variables
# Perform OVH API calls with httpie
http -b --auth-type ovh https://api.ovh.com/1.0/me
```

## Obtain API credentials

You can find URLs to create your application credentials (client id and secret) here:
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


## Credentials from environment variables

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


## OVH API resources

Here is the official API implementation: https://github.com/ovh/python-ovh (this library *does not depend* on `python-ovh`).

API documentation available here: https://api.ovh.com/


# Development

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

Stable branch is `main`; development branch is `dev`. Usual release steps are :

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
# update version if needed (example: VERSION=1.1.0.dev0 to release 1.1.0)
git fetch
git checkout dev
git pull
tbump VERSION

# open a PR for version releasing
# PR merge triggers:
# * Build devN version
# * trigger version minor increment
# * trigger tag creation, dev branch update (version, merge)
# * tag is published
```


## Github actions

This actions are automatically triggered:

* Build and test on python 3.7-3.10 environments for all branches and PR
* Build and publish on test.pypi.org for all protected branches and PR; publication is ignored if version is already deployed
* Version increment for merged PR on `main` branch (increment minor part, update main and create a new tag); merge back and increment version in `dev` branch
* Build and publish on pypi.org for main with message starting with *Bump to*; fails if version is already deployed


## Github actions configuration

`testpypi` and `pypi` environments are needed. Needed secrets are:

* `PYPI_TOKEN`
* `GPG_PRIVATE_KEY` (optional)
* `GPG_PASSPHRASE` (optional)

`GPG_*` values are the same for both environments.


## Manual publication

If needed, release can be manually performed.

```
# Manual publication
# publish (pypi credentials required)
tbump RELEASE_VERSION
git checkout vRELEASE_VERSION
rm -rf dist build
python -m build --sdist --wheel
# fake upload
# run pypi-server in another shell
mkdir -p /tmp/packages && pypi-server run -P . -a . /tmp/packages/
twine upload  -u "" -p "" --repository-url http://localhost:8080/ dist/*.whl dist/*.tar.gz

# real upload
twine upload dist/*.whl dist/*.tar.gz
```

# Changelog

## 1.2.0 (2022-07-18)

* remove python 3.6 support
* added python 3.10 tests
* build system updated (pep 517, pep 660)
* restored CI (github-actions based)

## 1.1.0 (2022-07-04)

* fix httpie body type (bytes, we need to convert to str)

