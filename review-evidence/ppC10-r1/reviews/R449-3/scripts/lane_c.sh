#!/usr/bin/env bash
# Lane C: notify, ACMP, GSI and name-write campaigns, 3 jobs each.
P="${PACKET_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"; S="$P/scratch"; V="$S/bin/verilator"
cd $S/camp-tree
python3 tb/pp_top/notify_mutants.py --output $S/camp-out/notify --verilator $V --jobs 3; echo "notify rc=$?"
python3 tb/pp_top/acmp_mutants.py --output $S/camp-out/acmp --verilator $V --jobs 3; echo "acmp rc=$?"
python3 tb/pp_top/gsi_mutants.py --output $S/camp-out/gsi --verilator $V --jobs 3; echo "gsi rc=$?"
python3 tb/pp_top/name_wr_mutant.py --output $S/camp-out/name_wr; echo "name_wr rc=$?"
