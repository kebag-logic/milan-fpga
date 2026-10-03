#!/usr/bin/env bash
# Lane B: AECP dispatch, AECP hazard and counters campaigns, 3 jobs each.
P="${PACKET_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"; S="$P/scratch"; V="$S/bin/verilator"
cd $S/camp-tree
python3 tb/pp_top/aecp_dispatch_mutants.py --output $S/camp-out/aecp_dispatch --verilator $V --jobs 3; echo "aecp_dispatch rc=$?"
python3 tb/pp_top/aecp_mutants.py --output $S/camp-out/aecp --jobs 3; echo "aecp rc=$?"
python3 tb/pp_top/ctr_mutants.py --output $S/camp-out/ctr --jobs 3; echo "ctr rc=$?"
