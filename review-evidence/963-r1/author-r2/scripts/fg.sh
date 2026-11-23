#!/usr/bin/env bash
# fg.sh <out-dir> <cwd> <cmd...>: run <cmd> in the foreground in <cwd>, under `timeout 570` so that a wave of these
# returns inside one foreground call; record argv.json, head.txt (the cwd's git HEAD), start.txt, end.txt, log.txt
# and rc (124 when the cap cut it). Environment: the lane's env.sh.
set -u
O=$1; C=$2; shift 2
T=/data-2/milan/tmp/963-a819
mkdir -p "$O"
python3 -c 'import json,sys; print(json.dumps(sys.argv[1:], indent=1))' "$@" > "$O/argv.json"
git -C "$C" rev-parse HEAD > "$O/head.txt"
date '+%Y-%m-%d %H:%M:%S %Z' > "$O/start.txt"
(
  . $T/bin/env.sh
  export TMPDIR=$T/tmp PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 MAKEFLAGS="-j8 --no-print-directory"
  cd "$C" && timeout 570 "$@"
) > "$O/log.txt" 2>&1
echo $? > "$O/rc"
date '+%Y-%m-%d %H:%M:%S %Z' > "$O/end.txt"
