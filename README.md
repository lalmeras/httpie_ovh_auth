# Auth plugin for OVH API

Plugin uses environement variables OVH\_CLIENT\_ID, OVH\_CLIENT\_SECRET
and OVH\_CONSUMER\_KEY to perform httpie authentication.

You can find URLs to create your application credentials
(client id and secret) here:
https://github.com/ovh/python-ovh#1-create-an-application

Then use it in https://api.ovh.com/console/#/auth/credential#POST
to obtain a consumer key. You need to visit the page ``validationUrl``
to provide your credentials and an expiration delay to validate
this consumer key.

Rename ``auth.env.tpl`` to ``auth.env`` and insert your credentials.

Configure your environment before running httpie by sourcing this file:

```
source auth.env
```


# Implementation

Here is the official API implementation: https://github.com/ovh/python-ovh


# OVH API

API documentation available here: https://api.ovh.com/ 


# Development

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
