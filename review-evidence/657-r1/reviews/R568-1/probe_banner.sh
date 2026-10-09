#!/bin/sh
# Usage: probe_banner.sh <clone>
# Shows when a nested `make -s -C` prints its directory banner into a query's
# stdout, and that --no-print-directory suppresses it (the #657 driver fix).
cd "$1" || exit 99
make --version | head -1
echo "--- plain -s -C";                      make -s -C tb/verilator/milan_dp print-srcs 2>&1 | head -c 160; echo
echo "--- MAKEFLAGS=w";                       MAKEFLAGS=w make -s -C tb/verilator/milan_dp print-srcs 2>&1 | head -c 160; echo
echo "--- MAKEFLAGS=w --no-print-directory";  MAKEFLAGS=w make --no-print-directory -s -C tb/verilator/milan_dp print-srcs 2>&1 | head -c 160; echo
