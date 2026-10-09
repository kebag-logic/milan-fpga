#!/bin/bash
# SPDX-License-Identifier: MIT
# usage: run_logged.sh <name> <dir> <cmd...>
# Runs the command detached in <dir>; writes receipts/runs/<name>.log and <name>.rc
# under the packet directory (default: parent of this script's directory).
P=${PACKET:-$(cd "$(dirname "$0")/.." && pwd)}
name=$1; dir=$2; shift 2
mkdir -p "$P/receipts/runs"
setsid nohup bash -c 'out=$1; dir=$2; shift 2; cd "$dir" && "$@"; echo $? > "$out.rc"' _ "$P/receipts/runs/$name" "$dir" "$@" > "$P/receipts/runs/$name.log" 2>&1 < /dev/null &
