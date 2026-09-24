#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Delta probe for the SRP stream suite split: runs tb/srp_stream_fsms at the
# ancestor and at the exact head, plain and with a per-check trace, plus two
# RTL mutants from the suite README and one fault probe (a dropped call).
#
# usage: run_delta_probe.sh CLONE OUT_DIR VERILATOR [SCRATCH]
# Trees are extracted with `git archive` into SCRATCH; CLONE is only read.
# Builds use `-j 8` in place of the Makefile's `-j 0` (job cap); nothing else
# in the recipe changes. Every run is foreground; rc is recorded per run.
set -eu
CLONE=$1
OUT=$2
VER=$3
SCR=${4:-$OUT/scratch}
ANC=a14ef8b4787b5309dd9ab472e82ae2b4a3fdbb72
HEAD=a024ab51b926690be5ade8ec35ec1fa7dd23981b
mkdir -p "$OUT/receipts" "$SCR"
SUITE=tb/srp_stream_fsms

extract() {  # label commit
  rm -rf "$SCR/$1"
  mkdir -p "$SCR/$1"
  git -C "$CLONE" archive "$2" | tar -x -C "$SCR/$1"
  sed -i 's/--build -j 0/--build -j 8/' "$SCR/$1/$SUITE/Makefile"
}

trace_macro() {  # label: each CHECK also prints seq, result and its message
  python3 - "$SCR/$1/$SUITE/sim_main.cpp" <<'EOF'
import sys
p = sys.argv[1]
s = open(p).read()
old = ('#define CHECK(cond, ...) do { \\\n  ++checks; \\\n'
       '  if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\\n"); } \\\n'
       '} while (0)\n')
new = ('#define CHECK(cond, ...) do { \\\n  ++checks; \\\n'
       '  const bool ok_ = (cond); \\\n'
       '  printf("TRACE %d %s: ", checks, ok_ ? "PASS" : "FAIL"); '
       'printf(__VA_ARGS__); printf("\\n"); \\\n'
       '  if (!ok_) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\\n"); } \\\n'
       '} while (0)\n')
assert s.count(old) == 1, "CHECK macro not found verbatim"
open(p, "w").write(s.replace(old, new))
EOF
}

edit() {  # label file old new  (exactly one occurrence required)
  python3 - "$SCR/$1/$2" "$3" "$4" <<'EOF'
import sys
p, old, new = sys.argv[1:4]
s = open(p).read()
assert s.count(old) == 1, f"site not unique/absent: {old!r}"
open(p, "w").write(s.replace(old, new))
EOF
}

run() {  # label
  set +e
  make -C "$SCR/$1/$SUITE" run VERILATOR="$VER" > "$SCR/$1.build.log" 2>&1
  rc=$?
  set -e
  grep -v '^make\|^- V e r\|^- Verilator\|^ccache\|^g++\|^echo\|^rm \|^ar \|^/usr\|^python' \
    "$SCR/$1.build.log" | grep -E '^(TRACE|FAIL|[0-9]+ checks)' > "$OUT/receipts/$1.out" || true
  grep -c 'warning:' "$SCR/$1.build.log" > "$OUT/receipts/$1.warnings" || true
  echo "$1 rc=$rc $(tail -n 1 "$OUT/receipts/$1.out")" | tee -a "$OUT/receipts/runs.txt"
}

: > "$OUT/receipts/runs.txt"
"$VER" --version >> "$OUT/receipts/runs.txt"

for pair in "anc:$ANC" "head:$HEAD"; do
  l=${pair%%:*}; c=${pair#*:}
  extract "$l-plain" "$c";  run "$l-plain"
  extract "$l-trace" "$c";  trace_macro "$l-trace"; run "$l-trace"
  extract "$l-mut-sink0" "$c"
  edit "$l-mut-sink0" hdl/srp/KL_srp_listener_fsm.sv \
    "fchg_diff_w = (fcode_r[fchg_ix_w] != evt_failure_code_i)
               || (fsysid_r[fchg_ix_w] != evt_failure_system_id_i);" \
    "fchg_diff_w = (fcode_r[0] != evt_failure_code_i)
               || (fsysid_r[0] != evt_failure_system_id_i);"
  run "$l-mut-sink0"
  extract "$l-mut-nostrobe" "$c"
  edit "$l-mut-nostrobe" hdl/srp/KL_srp_listener_fsm.sv \
    "if (ind_fchg_w[s]) evt_tk_fail_chg_o[s]   <= 1'b1;" \
    "if (ind_fchg_w[s]) evt_tk_fail_chg_o[s]   <= 1'b0;"
  run "$l-mut-nostrobe"
done

# fault probe: the head without the call to the third scenario must lose checks
extract head-fault-dropcall "$HEAD"
edit head-fault-dropcall "$SUITE/sim_main.cpp" \
  "  listener_failure_change_notifies_registered_sinks_on_a_shared_stream();

  printf(" \
  "
  printf("
run head-fault-dropcall

cd "$OUT/receipts"
for v in plain trace mut-sink0 mut-nostrobe; do
  if cmp -s "anc-$v.out" "head-$v.out"; then r=IDENTICAL; else r=DIFFERENT; fi
  echo "compare $v: $r ($(wc -l < "head-$v.out") lines)" | tee -a runs.txt
done
echo "trace checks at head: $(grep -c '^TRACE' head-trace.out), PASS $(grep -c '^TRACE [0-9]* PASS' head-trace.out)" | tee -a runs.txt
