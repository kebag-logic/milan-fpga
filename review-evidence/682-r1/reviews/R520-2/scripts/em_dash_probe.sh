#!/usr/bin/env bash
# Usage: em_dash_probe.sh <source-repo> <python> <scratch-dir> <receipt-dir> <base> <head>
# The em-dash gate judges committed lines in base..HEAD, so each probe commits
# its edit in a disposable clone (never the review clone) and runs the gate there.
set -u
src=$1; py=$2; scr=$3; out=$4; base=$5; head=$6
mkdir -p "$out"; : > "$out/em_probe_rc.tsv"
rm -rf "$scr"; git clone -q --no-checkout "$src" "$scr"; cd "$scr"
git -c advice.detachedHead=false checkout -q "$head"
git config user.name probe; git config user.email probe@invalid
one() { name=$1; file=$2; old=$3; new=$4
  git checkout -q --detach "$head"
  "$py" -I -c 'import sys;p,o,n=sys.argv[1:4];s=open(p,encoding="utf-8").read();assert s.count(o)==1;open(p,"w",encoding="utf-8").write(s.replace(o,n))' "$file" "$old" "$new"
  git commit -qam "probe $name"
  "$py" scripts/check_em_dash.py --base "$base" > "$out/$name.log" 2>&1; rc=$?
  v=SURVIVED; [ "$rc" -ne 0 ] && v=KILLED
  printf '%s\t%s\t%s\n' "$name" "$rc" "$v" >> "$out/em_probe_rc.tsv"; }
one E1_changelog CHANGELOG.md "- It also carries #164." "- It also carries #164 $(printf '—') the last."
one E2_recipe docs/testing/PP_SHADOW_BASELINE_RECIPE.md "Current baseline F was recorded with" "Current baseline F $(printf '—') was recorded with"
cat "$out/em_probe_rc.tsv"
