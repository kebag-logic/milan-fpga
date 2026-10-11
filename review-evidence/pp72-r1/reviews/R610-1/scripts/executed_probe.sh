#!/usr/bin/env bash
# The executed half on a planted dead tag. In a disposable clone at the reviewed
# head, wrap tb/srp_encoder's tagged E1 check (and its tag) in a branch that is
# never taken, so the check and its tag compile but never run. The static half
# must still pass; srp_encoder is then run with REQ_TAG_LOG set, its evidence
# and tally are spliced into the full head sweep's evidence and run_suites.sh
# output (every other suite's lines unchanged), and the executed half must name
# the dead tag. A control does the same splice with the unplanted suite.
# usage: executed_probe.sh CLONE HEAD_SWEEP_DIR OUTDIR   (SIM_BIN as sweep.sh)
set -u
clone=$1; sweep=$2; out=$3
export PATH="${SIM_BIN:?}:$PATH"
mkdir -p "$out"
cd "$clone" || exit 2
F=tb/srp_encoder/sim_main.cpp
splice() {  # label
  local label=$1 ev="$out/$1.evidence" log="$out/$1.suites"
  rm -f "$ev" "$out/$1.srp_encoder.txt"
  (cd tb/srp_encoder && make clean >/dev/null 2>&1; REQ_TAG_LOG="$ev.local" make) \
    >"$out/$1.srp_encoder.txt" 2>&1
  echo "srp_encoder make rc=$?" >>"$out/$1.srp_encoder.txt"
  tally=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$out/$1.srp_encoder.txt" | tail -1)
  { grep -v '^srp_encoder ' "$sweep/req-tags.txt"; cat "$ev.local" 2>/dev/null; } >"$ev"
  sed "s/^PASS srp_encoder (.*)\$/PASS srp_encoder ($tally)/" "$sweep/suites.txt" >"$log"
  python3 scripts/check-req-tags.py >"$out/$label.static.txt" 2>&1
  echo "static rc=$?" >>"$out/$label.static.txt"
  python3 scripts/check-req-tags.py --suites "$log" --evidence "$ev" >"$out/$label.executed.txt" 2>&1
  echo "executed rc=$?" >>"$out/$label.executed.txt"
  rm -f "$ev.local"
}
git checkout -q -- . && git clean -qfd tb
splice control
python3 - "$F" <<'EOF'
import sys
p = sys.argv[1]; s = open(p).read()
old = '    REQ_TAG("REQ-SRP-003", "DIR", "E1 dual EndMark explicit ahead of MAC padding");\n'
assert s.count(old) == 1
s = s.replace(old, '    if (got.size() > 100000) {  // never taken: planted dead tag\n' + old, 1)
tail = '"E1 dual EndMark explicit ahead of MAC padding");\n'
i = s.index(tail, s.index('CHECK(got[26] == 0')) + len(tail)
s = s[:i] + '    }\n' + s[i:]
open(p, "w").write(s)
EOF
git diff >"$out/planted.diff"
splice planted
git checkout -q -- . && git clean -qfdx tb/srp_encoder
git status --short >"$out/restore-status.txt"; git rev-parse HEAD >>"$out/restore-status.txt"
