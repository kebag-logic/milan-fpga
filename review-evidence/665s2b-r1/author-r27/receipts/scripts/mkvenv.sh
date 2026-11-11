#!/bin/bash
set -u
G=<scratch>/gates
/usr/bin/python3 -m venv $G/venv && PIP_NO_CACHE_DIR=1 HOME=$G/home $G/venv/bin/python3 -m pip install --no-cache-dir -r $G/requirements.txt
