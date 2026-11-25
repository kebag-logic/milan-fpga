#!/bin/sh
# Disposable mutation probes of the round-5 delta: each probe extracts a fresh copy of the head's tool directory and
# section 13's page, plants one defect, and runs the tool's self-test; a planted defect must fail it (rc != 0).
# Usage: probe_mutations.sh <clone> <scratch dir>
set -u
C=$1; S=$2; rc_all=0
probe() {  # name, file (relative), python expression rewriting text t
  d=$S/probe-$1; rm -rf "$d"; mkdir -p "$d"
  git -C "$C" archive HEAD tb/verilator/ctrl_service_budget docs/design/SPLIT_CONTROL_MEMORY.md | tar -x -C "$d"
  python3 -I -c "import sys;p=sys.argv[1];t=open(p).read();n=$3;assert n!=t,'no change';open(p,'w').write(n)" "$d/$2" || { echo "PROBE $1: plant failed"; rc_all=1; return; }
  python3 -I "$d/tb/verilator/ctrl_service_budget/egress_ledger.py" --selftest > "$d.log" 2>&1; r=$?
  if [ $r -ne 0 ]; then echo "PROBE $1: refused (rc $r): $(grep -m1 -E '^FAIL|RESULT' "$d.log")"; else echo "PROBE $1: SURVIVED"; rc_all=1; fi
}
D=docs/design/SPLIT_CONTROL_MEMORY.md; T=tb/verilator/ctrl_service_budget/egress_ledger.py
probe doc-pinned-cell $D "t.replace('| 64.01426 | 64.09994 | 64.31 |','| 64.01426 | 64.09995 | 64.31 |')"
probe doc-ledger-cell $D "t.replace('| 63.07053 | 62.84763 | 63.23 |','| 63.07053 | 62.84763 | 63.24 |')"
probe doc-swap-columns $D "t.replace('| 63.07053 | 62.84763 | 63.23 |','| 62.84763 | 63.07053 | 63.23 |')"
probe tool-train-one-cycle $T "t.replace(\"'backlog-owed.service.aecp.last.if0': 63.07053}\",\"'backlog-owed.service.aecp.last.if0': 63.07052}\")"
probe tool-max-drops-train $T "t.replace('LISTENED[row], TRAIN[row], PINNED[row])','LISTENED[row], PINNED[row])',1)"
probe doc-row-dropped $D "t.replace([l for l in t.splitlines() if l.startswith('| \`backlog.owed_behind3.if0\` | 63.969')][0]+'\n','')"
# control: an unplanted copy passes
d=$S/probe-control; rm -rf "$d"; mkdir -p "$d"; git -C "$C" archive HEAD tb/verilator/ctrl_service_budget docs/design/SPLIT_CONTROL_MEMORY.md | tar -x -C "$d"
python3 -I "$d/tb/verilator/ctrl_service_budget/egress_ledger.py" --selftest > "$d.log" 2>&1; r=$?
echo "CONTROL unplanted copy: rc $r ($(tail -1 "$d.log"))"; [ $r -eq 0 ] || rc_all=1
exit $rc_all
