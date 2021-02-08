#! /bin/python3

import sys
import os.path
import subprocess
import functools

VENV = "venv"

this_script = sys.argv[0]

if not os.path.isfile(this_script):
    raise Error("Current script %s not found" % (this_script))

this_path = os.path.dirname(this_script)
this_path = os.path.relpath(this_path)
venv = os.path.join(this_path, VENV)
pip = os.path.join(venv, 'bin/pip')

def check_call(*args, **kwargs):
    subprocess.check_call(*args, stdout=sys.stderr, **kwargs)

def pip_install(package_or_requirement, is_requirement=False, editable=False,
        upgrade=False):
    args = []
    if editable: args.append("--editable")
    if upgrade: args.append("--upgrade")
    if is_requirement:
        args.append("-r")
        args.append(package_or_requirement)
    else:
        args.append(package_or_requirement)
    check_call([
        pip,
        "install",
        ] + args)

check_call([
    "virtualenv",
    "-p",
    "python3",
    venv])
pip_install("pip", upgrade=True)
pip_install(this_path, editable=True)
pip_install("requirements-dev.txt", is_requirement=True)

print("Run: eval $( %s )" % (sys.argv[0],), file=sys.stderr)
print("source %s" % (os.path.join(venv, 'bin/activate'),))
