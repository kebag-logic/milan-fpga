#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Prove the generator tests are gated by the repository's own entry points.
# Usage: entry_point.sh HEAD_TREE WORK VERILATOR_BIN_DIR
# Builds two reduced copies of the head tree (tb/ holds only desc_store, so the
# sweep is focused): "control" is unmodified, "mutant" has the body/key check
# removed. For each: `make` in tb/desc_store (the target run_suites.sh invokes)
# and scripts/run_suites.sh. The only other edit is the Verilator build job cap
# (-j 0 -> -j 8) in the copy's tb/desc_store/Makefile. Expected: control rc 0/0, mutant non-zero/1.
set -uo pipefail
head=$(cd "$1" && pwd); work=$2; export PATH="$(cd "$3" && pwd):$PATH"
mkdir -p "$work"; work=$(cd "$work" && pwd)
echo "verilator: $(verilator --version)"
for kind in control mutant; do
  t="$work/$kind"; rm -rf "$t"; cp -a "$head" "$t"
  # drop every OTHER suite (a tb/ dir with a Makefile); keep shared harness dirs
  for d in "$t"/tb/*/; do
    [ "$(basename "$d")" = desc_store ] && continue
    [ -f "$d/Makefile" ] && rm -rf "$d"
  done
  # cap the Verilator C++ build at 8 jobs (reviewer resource limit); nothing else
  sed -i 's/--build -j 0/--build -j 8/' "$t/tb/desc_store/Makefile"
  if [ "$kind" = mutant ]; then
    python3 - "$t/hdl/aecp/desc/gen_desc_image.py" <<'EOF'
import re, sys
p = sys.argv[1]; s = open(p).read()
s, n = re.subn(r'        body_type = int.from_bytes\(body\[0:2\], "big"\)\n.*?f"index \{body_index\}"\)\n', "", s, flags=re.S)
assert n == 1; open(p, "w").write(s)
EOF
  fi
  echo "== $kind: generator sha256 $(sha256sum < "$t/hdl/aecp/desc/gen_desc_image.py" | cut -c1-64)"
  (cd "$t/tb/desc_store" && make) > "$work/$kind-make.log" 2>&1; mrc=$?
  echo "$kind make (default target) rc=$mrc"
  grep -E 'checks: [0-9]+ PASS|^(Ran|OK|FAILED)|make: \*\*\*|Vdesc_store_sim' "$work/$kind-make.log" | head -8
  (cd "$t/tb/desc_store" && make clean >/dev/null)
  (cd "$t" && ./scripts/run_suites.sh) > "$work/$kind-run_suites.log" 2>&1; rrc=$?
  echo "$kind run_suites.sh rc=$rrc"; grep -E '^(PASS|FAIL|UNREADABLE|suites:|UPC)' "$work/$kind-run_suites.log"
done
