#!/usr/bin/env bash
# campaigns.sh <tag> <tree> [jobs]: every campaign that builds a changed file, in order,
# each via gate.sh (log + rc per campaign); outputs under out/<tag>/.
set -u
tag="$1"; tree="$2"; jobs="${3:-3}"
G=<scratch>/r2/bin/gate.sh
O=<scratch>/r2/out/$tag
rm -rf "$O"; mkdir -p "$O"
run() { local name="$1" dir="$2"; shift 2; "$G" "$tag-camp-$name" "$tree/$dir" "$@"; }
run srp_top        tb/srp_top    python3 mutants.py --output "$O/srp_top" --jobs "$jobs"
run srp_admission  tb/srp_admission python3 mutants.py --output "$O/srp_admission" --jobs "$jobs"
run aecp           tb/pp_top     python3 aecp_mutants.py --output "$O/aecp" --jobs "$jobs"
run aecp_dispatch  tb/pp_top     python3 aecp_dispatch_mutants.py --output "$O/aecp_dispatch" --verilator verilator --jobs "$jobs"
run ctr            tb/pp_top     python3 ctr_mutants.py --output "$O/ctr" --jobs "$jobs"
run notify         tb/pp_top     python3 notify_mutants.py --output "$O/notify" --verilator verilator --jobs "$jobs"
run gsi            tb/pp_top     python3 gsi_mutants.py --output "$O/gsi" --verilator verilator --jobs "$jobs"
run name_wr        tb/pp_top     python3 name_wr_mutant.py --output "$O/name_wr"
run acmp           tb/pp_top     python3 acmp_mutants.py --output "$O/acmp" --verilator verilator --jobs "$jobs"
run d3             tb/pp_top     python3 d3_mutants.py --output "$O/d3" --verilator verilator --jobs "$jobs"
run adp            tb/adp_engine python3 mutants.py --output "$O/adp" --jobs "$jobs"
run maap           tb/maap       python3 mutants.py --output "$O/maap" --jobs "$jobs"
run name_state     tb/name_state python3 mutants.py --output "$O/name_state" --verilator verilator --jobs 2
run elab_mutants   tb/elab_guards python3 -B mutants.py --output "$O/elab_mutants" --verilator verilator --jobs "$jobs"
echo "campaigns $tag done"
