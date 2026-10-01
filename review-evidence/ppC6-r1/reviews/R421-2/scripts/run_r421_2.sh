#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# R421-2 reviewer runs for processor PR #139 at 88e0bf82888d6ad83b500425a786814da467610b.
# Portable: needs git, Verilator 5.050, sv2v, yosys, python3, make, g++.
# Usage: run_r421_2.sh <processor clone holding the head> <work dir> [step...]
# Steps (default all): identify mutants probes arms r1rtl r1probe equiv lint
# Nothing is written to the clone: every step works on `git archive` exports.
# VERILATOR (default: verilator on PATH) must be 5.050; builds are capped at
# eight parallel jobs (two mutant copies x four, or one build x eight).
set -euo pipefail
clone=$(realpath "$1"); work=$(realpath -m "$2"); shift 2
steps=${*:-identify mutants probes arms r1rtl r1probe equiv lint}
here=$(dirname "$(realpath "$0")")
head=88e0bf82888d6ad83b500425a786814da467610b
main=3f3ea56ba61829718a6a288600ab4fdac73aa5ba
merge=a011b14a5c19dab52b115259750a229e2a9c69dc   # round-1 RTL on the merged tree
pin=${VERILATOR:-$(command -v verilator)}
"$pin" --version | grep -q 'Verilator 5.050' || { echo "need Verilator 5.050" >&2; exit 2; }
export PIN_VERILATOR=$pin
vw="$here/verilator-j8.sh"
mkdir -p "$work/receipts"
test "$(git -C "$clone" rev-parse "$head^{tree}")" = 5cc519fb073c2ab124e6f77b55aafbba9cdc24f1

export_tree() {  # export_tree <rev> <dir>
  rm -rf "$2"; mkdir -p "$2"; git -C "$clone" archive "$1" | tar -x -C "$2"
}
with_hdl_of() {  # with_hdl_of <rev> <tree>: replace the tree's hdl/ by <rev>'s
  rm -rf "$2/hdl"; git -C "$clone" archive "$1" hdl | tar -x -C "$2"
}
ident_run() {  # ident_run <tree> <log>: section ID (third build) alone
  (cd "$1/tb/pp_top" && VJOBS=8 make identify-build VERILATOR="$vw" > /dev/null 2>&1 \
     && ./obj_idn/Vpp_top_idn) > "$2" 2>&1 || true
}

for s in $steps; do case $s in
identify)   # section ID 106 and ID0 3 at the head
  export_tree "$head" "$work/head"
  (cd "$work/head/tb/pp_top" && make identify VERILATOR="$vw") \
    > "$work/receipts/01-pp_top-identify-head.log" 2>&1 ;;
mutants)    # the lane's 34 controls
  export_tree "$head" "$work/mut"
  (cd "$work/mut" && VJOBS=4 python3 tb/pp_top/notify_mutants.py --output "$work/nm" \
     --verilator "$vw" --jobs 2) > "$work/receipts/02-notify-mutants-head.stdout" 2>&1
  cp "$work/nm/results.json" "$work/receipts/02-notify-mutants-head-results.json" ;;
probes)     # six reviewer probe mutants against the lane's own section ID
  export_tree "$head" "$work/ptree"
  VJOBS=4 python3 "$here/r421_probes.py" --root "$work/ptree" --output "$work/probes1" \
     --verilator "$vw" --jobs 2 > "$work/receipts/03-probes-head.stdout" 2>&1
  cp "$work/probes1/results.json" "$work/receipts/03-probes-head-results.json" ;;
arms)       # reviewer arms R421a-d at the head, then the two targeted mutants
  export_tree "$head" "$work/arms"; python3 "$here/r421_arms.py" "$work/arms"
  ident_run "$work/arms" "$work/receipts/05-probe-arms-golden-head.log"
  export_tree "$head" "$work/arms-noc"; python3 "$here/r421_arms.py" "$work/arms-noc" --without-c
  VJOBS=4 python3 "$here/r421_probes.py" --root "$work/arms-noc" --output "$work/probes2" \
     --verilator "$vw" --jobs 2 --set arms > "$work/receipts/06-probe-arms-mutants.stdout" 2>&1
  cp "$work/probes2/results.json" "$work/receipts/06-probe-arms-mutants-results.json" ;;
r1rtl)      # the head's tests, and the reviewer arms, on the round-1 RTL
  export_tree "$head" "$work/r1"; with_hdl_of "$merge" "$work/r1"
  ident_run "$work/r1" "$work/receipts/12-head-ID-on-round1-rtl.log"
  export_tree "$head" "$work/r1a"; python3 "$here/r421_arms.py" "$work/r1a"; with_hdl_of "$merge" "$work/r1a"
  ident_run "$work/r1a" "$work/receipts/13-probe-arms-on-round1-rtl.log" ;;
r1probe)    # R421-1's contention/stall probe (P1, P2), unchanged, at the head
  export_tree "$head" "$work/r1p"; cp "$here/r421_ident_probe.hpp" "$work/r1p/tb/pp_top/"
  python3 - "$work/r1p/tb/pp_top/sim_main.cpp" <<'PY'
import sys; from pathlib import Path
p = Path(sys.argv[1]); t = p.read_text()
a = '#include "notify_phases.hpp"\n'; assert t.count(a) == 1
t = t.replace(a, a + '#include <functional>\n#include "r421_ident_probe.hpp"\n')
b = '  run_identify(h);\n  const char* const build = "identify";\n'; assert t.count(b) == 1
t = t.replace(b, '  if (argc == 2 && std::strcmp(argv[1], "--r421-probe") == 0) { run_r421_probe(h); return 0; }\n' + b)
p.write_text(t)
PY
  (cd "$work/r1p/tb/pp_top" && VJOBS=8 make identify-build VERILATOR="$vw" > /dev/null 2>&1 \
     && ./obj_idn/Vpp_top_idn --r421-probe) > "$work/receipts/16-r421-1-probe-rerun-at-head.log" 2>&1 ;;
equiv)      # KL_aecp_notify at EN_IDENTIFY_NOTIF_P = 0 against main's
  mkdir -p "$work/equiv"
  for r in base:$main head:$head; do
    d=$work/equiv/${r%%:*}; export_tree "${r#*:}" "$d"
    (cd "$d" && sv2v hdl/common/pp_pkg.sv hdl/aecp/KL_aecp_notify.sv > all.v)
  done
  (cd "$work/equiv" && yosys -q -l equiv.log -p "script $here/equiv_notify_r2.ys" > /dev/null) ;;
lint)       # zero-tolerance lint, plus notify and the top at parameter 1
  export_tree "$head" "$work/lint"; mkdir -p "$work/pinbin"; ln -sf "$pin" "$work/pinbin/verilator"
  (cd "$work/lint" && PATH="$work/pinbin:$PATH" ./scripts/lint_hdl.sh) > "$work/receipts/07-lint_hdl-head.log" 2>&1
  (cd "$work/lint" && pkgs=$(find hdl -name '*_pkg.sv' | sort) && all=$(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort) \
   && for t in KL_aecp_notify protocol_processor_top; do
        echo "== $t -GEN_IDENTIFY_NOTIF_P=1"
        "$pin" --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM \
          --top-module "$t" -GEN_IDENTIFY_NOTIF_P=1 $pkgs $all 2>&1 | grep -E '%(Warning|Error)' | head -5
        echo "rc=${PIPESTATUS[0]}"
      done) > "$work/receipts/08-lint-en1.log" 2>&1 ;;
*) echo "unknown step $s" >&2; exit 2 ;;
esac; done
