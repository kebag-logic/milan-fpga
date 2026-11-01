#!/usr/bin/env bash
# Disposable negative controls for this delta. Each extracts the exact head into a new directory and edits only that copy.
# Usage: run_probes.sh <clone> <scratch-dir> <log-dir>
set -u
clone=$1; scratch=$2; logs=$3
probe() { # name, replacement sentence
  local name=$1 text=$2 dir
  dir=$(mktemp -d "$scratch/probe.XXXXXX")
  git -C "$clone" archive HEAD | tar -x -C "$dir"
  ( cd "$dir" && TEXT="$text" python3 -I -c "
import os
p='docs/guides/gptp/MANAGER.md'; s=open(p).read()
a='This guide covers the fabric plane until F6.'
assert a in s
open(p,'w').write(s.replace(a,os.environ['TEXT']))
" && PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_doc_style.py ) >"$logs/$name.log" 2>&1
  echo $? >"$logs/$name.rc"
  echo "$name rc=$(cat "$logs/$name.rc")"
}
probe mut_style_r4_prior_text 'This guide covers the fabric plane, which owns product time until F6.'
probe mut_style_long_sentence 'This guide covers the fabric plane until F6, when the firmware owner takes the protocol and servo in all of its detail.'
