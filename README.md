# Auth plugin for OVH API

Plugin uses environement variables OVH\_CLIENT\_ID, OVH\_CLIENT\_SECRET
and OVH\_CONSUMER\_KEY to perform httpie authentication.

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

Rename ``auth.env.tpl`` to ``auth.env`` and insert your credentials.

Configure your environment before running httpie commands by sourcing this file:

```
source auth.env
```

Trigger OVH authentication with ``--auth-type`` parameter:

```
http -b --auth-type ovh https://api.ovh.com/1.0/me
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
