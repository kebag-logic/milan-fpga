#!/usr/bin/env bash
# Lane D: the ADP, MAAP and SRP LeaveAll campaigns, 3 jobs each.
P="${PACKET_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"; S="$P/scratch"; V="$S/bin/verilator"
cd $S/camp-tree
python3 tb/adp_engine/mutants.py --output $S/camp-out/adp --jobs 3; echo "adp rc=$?"
python3 tb/maap/mutants.py --output $S/camp-out/maap --jobs 3; echo "maap rc=$?"
python3 tb/srp_top/mutants.py --output $S/camp-out/srp --jobs 3; echo "srp rc=$?"
