#!/bin/bash
# Disposable fault probes on KL_pp_shadow's C6 tie-offs, run in the clone and
# restored after each. Usage: probe_tieoff.sh <clone> <outdir> <pinned-verilator-dir>
set -u
C=$1; O=$2; V=$3; export PATH="$V:$PATH"; mkdir -p "$O"; cd "$C"
F=hdl/milan/KL_pp_shadow.sv
probe() { # name, python edit, gate...
  local n=$1 edit=$2; shift 2
  python3 - "$F" "$edit" <<'PY' || { echo "$n: edit failed" >> "$O/summary.txt"; return; }
import sys
p, which = sys.argv[1], sys.argv[2]
s = open(p).read()
edits = {
 "P1_button_unbound": ("      //! no identification button on this board yet: tied off, and never read\n      //! while EN_IDENTIFY_NOTIF_P is 0 (IEEE 1722.1-2021 7.5.1, Milan 5.4.5.4)\n      .identify_button_i   (1'b0),\n", ""),
 "P2_button_no_rationale": ("      //! no identification button on this board yet: tied off, and never read\n      //! while EN_IDENTIFY_NOTIF_P is 0 (IEEE 1722.1-2021 7.5.1, Milan 5.4.5.4)\n", ""),
 "P3_param_no_rationale": ("      //! P-EN-IDENTIFY-NOTIFICATION stays 0 until a debounced board button is\n      //! wired to identify_button_i (processor lane C6, manager ruling on #80)\n", ""),
}
old, new = edits[which]
assert s.count(old) == 1, which
open(p, "w").write(s.replace(old, new))
PY
  local i=0
  for g in "$@"; do i=$((i+1)); bash -c "$g" > "$O/$n.$i.log" 2>&1; echo "$n gate$i rc=$? : $g" >> "$O/summary.txt"; done
  git checkout -q -- "$F"
}
: > "$O/summary.txt"
probe P1_button_unbound P1_button_unbound "python3 scripts/lint_rtl.py --check" "python3 scripts/check_port_contracts.py"
probe P2_button_no_rationale P2_button_no_rationale "python3 scripts/check_port_contracts.py"
probe P3_param_no_rationale P3_param_no_rationale "python3 scripts/check_port_contracts.py"
git diff --quiet && echo "restored clean" >> "$O/summary.txt"
