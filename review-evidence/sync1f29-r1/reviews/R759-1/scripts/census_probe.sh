#!/bin/sh
# usage: census_probe.sh <planted datapath> : the port census's --check on a planted datapath. A plant must be refused by name.
cd "${CLONE:?}" && python3 -B sw/mailbox/publication_census.py --check --jobs 2 --datapath "$1"
