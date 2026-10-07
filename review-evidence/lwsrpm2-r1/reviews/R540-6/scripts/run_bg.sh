#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
# usage: run_bg.sh <label> <cmd...>; writes receipts/<label>.log and .rc
PKT=$(cd "$(dirname "$0")/.." && pwd)
label=$1; shift
rm -f "$PKT/receipts/$label.rc"
( "$@" > "$PKT/receipts/$label.log" 2>&1; echo $? > "$PKT/receipts/$label.rc" ) &
