#!/usr/bin/env bash
# Usage: replay_parent.sh <evidence-dir> <head-clone> <base-clone> <scratch> <out-dir>
# <evidence-dir> = kebag-logic/milan-fpga@86750aca review-evidence/pp127-r1/author-r2.
# 1) runs the published run_parent.py (original, fixed, deadline oracles) at head;
# 2) control: the deadline-anchored oracle against base 16be6768 (must fail).
# Needs the pinned Verilator 5.050 first on PATH.
set -u
ev=$(cd "$1" && pwd); head=$(cd "$2" && pwd); base=$(cd "$3" && pwd); s=$4; out=$5
mkdir -p "$s/replay" "$s/replay-base" "$out"
cp "$ev"/{run_parent.py,reproduce.cpp,run_reproduction.py,parent-expiry-oracle.patch} "$s/replay/"
(cd "$s/replay" && sha256sum run_parent.py reproduce.cpp run_reproduction.py parent-expiry-oracle.patch > "$out/replay-input-sha256.txt" \
  && python3 run_parent.py "$head" ../replay-run > "$out/replay-driver.log" 2>&1)
cp "$ev"/{reproduce.cpp,run_reproduction.py,parent-expiry-oracle.patch} "$s/replay-base/"
(cd "$s/replay-base" && patch --batch --fuzz=0 -p1 -i parent-expiry-oracle.patch \
  && python3 run_reproduction.py "$base" build > "$out/replay-base16be-deadline-oracle.log" 2>&1; \
  echo "rc=$?" >> "$out/replay-base16be-deadline-oracle.log")
