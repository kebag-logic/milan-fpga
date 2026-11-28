#!/bin/sh
# Reviewer probes for PR #1020 at 701f294405d47a81eed1079d32b54e1eea4a4f31.
# Set CLONE (a clean checkout at that head), PACKET (this directory), and the
# variables env.sh needs (a Verilator 5.050 on PATH; migen, litex and liteeth
# on PYTHONPATH). Nothing here writes inside CLONE except ignored __pycache__.
set -u
. "$PACKET/scripts/env.sh"
S="$PACKET/scratch"; G="$PACKET/receipts/gates"
cd "$CLONE"

# 1. the USB/LED suite (92,755 checks), its 72 planted defects, egress plants
make -C tb/verilator/usbnet run OBJ="$S/runs/suite" JOBS=4 > "$S/runs/suite.log" 2>&1
(cd tb/verilator/usbnet && MUTANT_DIR="$S/mut/all" JOBS=2 python3 mutants.py) > "$S/mut/all.log" 2>&1
(cd tb/verilator/usbnet && python3 egress_measure.py "$S/runs/egress-plants" --plants) > "$S/runs/egress-plants.log" 2>&1

# 2. ledger: self-test, independent derivation, three disposable doc plants
python3 tb/verilator/ctrl_service_budget/egress_ledger.py --selftest > "$G/ledger-selftest.log" 2>&1
python3 -I "$PACKET/scripts/ledger_probe.py" "$CLONE"
# plants: copy docs/, tb/verilator/ctrl_service_budget/ and scripts/ from HEAD into a
# scratch tree, edit one USB_NET_PATH.md ledger row, run the self-test there (must fail)

# 3. gates (all pass except the two below)
python3 scripts/ci_scope.py --selftest            # FAILS: USB_NET_PATH.md not in GATE_READ_DOCS
python3 scripts/suite_shards.py --selftest        # FAILS: head worker 25/27 1299 s > 1276 s
python3 scripts/check_baremetal_only.py --check   # FAILS: 5 findings, identical at 640699e6
python3 scripts/docs_inventory.py --check
python3 scripts/docs_check.py
python3 scripts/lint_rtl.py --check
python3 scripts/check_port_contracts.py
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest

# 4. published packet: both manifests
python3 -I "$PACKET/scripts/verify_packet.py" "<extracted review-evidence/usbnet-r1 with MANIFEST.json>"
