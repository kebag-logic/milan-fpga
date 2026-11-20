#!/bin/bash
# platled.sh CLONE OUT: plat_ledger.py --self-test alone (the platform image at its four points and its controls).
. <scratch>/bin/env.sh
export MAKEFLAGS=-j4 PYTHONUNBUFFERED=1
cd $1 && echo "HEAD $(git rev-parse --short=8 HEAD) start $(date +%T)"
mkdir -p $2/pl; python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir $2/pl --self-test > $2/plat-ledger.log 2>&1; echo "plat_ledger rc=$? END $(date +%T)"
