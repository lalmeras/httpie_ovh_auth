#! /bin/bash

GPG_USER="httpieovhauth@gmail.com"
GPG_OPTS="--pinentry-mode loopback --passphrase-fd 0"
echo "${gpg_passphrase}" | \
  gpg $GPG_OPTS --import httpieovhauth.gpg
python setup.py sdist bdist_wheel --python-tag py3
for file in dist/*; do
  echo "$gpg_passphrase" | \
    gpg --detach-sign -u "$GPG_USER" -o "$file.asc" "$file";
done;
TWINE_PASSWORD="${pypi_token}" twine upload -u __token__ dist/*