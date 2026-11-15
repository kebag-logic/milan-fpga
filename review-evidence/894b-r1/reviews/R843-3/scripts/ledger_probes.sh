#!/bin/sh
# Disposable fault probes on a copy of egress_ledger.py's tree (argument: the probe copy's root).
# Each probe plants one defect in the copy, runs the self-test, records rc, and restores the copy.
set -u
ROOT=$1
D=$ROOT/tb/verilator/ctrl_service_budget
cp "$D/egress_ledger.py" "$D/egress_ledger.py.orig"
cp "$D/scenario.py" "$D/scenario.py.orig"
cp "$ROOT/docs/design/SPLIT_CONTROL_MEMORY.md" "$ROOT/doc.orig"
probe() {
  name=$1
  (cd "$D" && python3 -I egress_ledger.py --selftest > "$ROOT/probe-$name.log" 2>&1)
  echo "$name rc=$? $(grep -c '^FAIL\|^ESCAPED\|escaped' "$ROOT/probe-$name.log") fail-lines; $(tail -1 "$ROOT/probe-$name.log")"
  cp "$D/egress_ledger.py.orig" "$D/egress_ledger.py"
  cp "$D/scenario.py.orig" "$D/scenario.py"
  cp "$ROOT/doc.orig" "$ROOT/docs/design/SPLIT_CONTROL_MEMORY.md"
}
# P1: the last 0.01 ms rounding to nearest instead of up
sed -i 's|return round(hold + -(-served // (PER_MS // 100)) / 100, 2)|return round(hold + round(served / (PER_MS // 100)) / 100, 2)|' "$D/egress_ledger.py"
grep -q 'round(served / (PER_MS' "$D/egress_ledger.py" && probe P1-round-nearest
# P2: 4 % instead of 5 % on the service, in the tool only
sed -i 's|served = -(-service \* 105 // 100)|served = -(-service * 104 // 100)|' "$D/egress_ledger.py"
grep -q '104 // 100' "$D/egress_ledger.py" && probe P2-four-percent
# P3: the scenario's hold moved to 61 ms (the tool must not silently re-derive)
sed -i "s|f'wait cycles {60 \* MS}', 'mark room', 'txready 1'|f'wait cycles {61 * MS}', 'mark room', 'txready 1'|" "$D/scenario.py"
grep -q "{61 \* MS}', 'mark room'" "$D/scenario.py" && probe P3-hold-61
# P4: section 13's merged-image measurement column edited one digit (doc not the tool's MEASURED)
sed -i 's/| `backlog.owed_behind3.if0` | 63.969 | 64.19076 | 64.41 |/| `backlog.owed_behind3.if0` | 63.969 | 64.19077 | 64.41 |/' "$ROOT/docs/design/SPLIT_CONTROL_MEMORY.md"
grep -q '64.19077' "$ROOT/docs/design/SPLIT_CONTROL_MEMORY.md" && probe P4-doc-measure-digit
# P5: run_refusals reads only the key "refused" (a misspelt key: refusals never seen)
sed -i "s|.get('refusals') or \[\]|.get('refused') or []|" "$D/egress_ledger.py"
grep -q "get('refused')" "$D/egress_ledger.py" && probe P5-refusals-key
rm -f "$D/egress_ledger.py.orig" "$D/scenario.py.orig" "$ROOT/doc.orig"
