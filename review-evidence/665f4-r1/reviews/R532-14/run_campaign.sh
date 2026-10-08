#!/bin/sh
# Usage: run_campaign.sh <act_ci.py copy> <scratch-root> <receipts-dir>
# Runs every probe mutation (at most 16 at once); one log and rc file per mutation.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
src=$1; root=$2; out=$3
mkdir -p "$root" "$out"
python3 -I -c 'import importlib.util,sys;s=importlib.util.spec_from_file_location("p",sys.argv[1]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);print("\n".join([*m.MUTATIONS,*m.COMBINED]))' "$here/probe_manifest.py" |
  xargs -P 16 -I{} sh -c 'rm -rf "$1/run-$2"; python3 -I "$0" "$3" "$2" "$1/run-$2" > "$4/probe-$2.log" 2>&1; echo $? > "$4/probe-$2.rc"' "$here/probe_manifest.py" "$root" {} "$src" "$out"
