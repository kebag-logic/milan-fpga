Run from the exact candidate checkout. PACKET is this packet's directory. Keep all exports and temporary files under its scratch/ directory. The scripts install nothing.

```sh
python3 -B "$PACKET/probe_transmit.py" . "$PACKET"
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --selftest
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check --selftest
git diff --check 8883d499..d0a2a160
```

Fetch immutable archive 48b6c3a2475861387068bc762f423bb417dd6915 and use git archive to extract these paths beneath scratch/:

- review-evidence/894b-r1/MANIFEST.json
- review-evidence/894b-r1/author-r13
- review-evidence/894b-r1/author-r10/receipts/harness/legs-46cf2a7d/gate-8x8-1if.txt
- review-evidence/894b-r1/author-r10/receipts/harness/legs-46cf2a7d/survey-8x8-1if/survey.out
- review-evidence/894b-r1/author-r10/receipts/harness/legs-46cf2a7d/M8-VDh/costs.txt

ARCHIVE names the resulting review-evidence/894b-r1 directory:

```sh
python3 -B "$PACKET/verify_integrity.py" . "$ARCHIVE"
python3 -B "$PACKET/audit_receipts.py" "$ARCHIVE"
```

The integrity verifier hashes actual tracked bytes and compares modes and index entries. The probe exports the candidate and pinned dependencies into scratch/transmit-probe, changes only that export, runs six actual CLI checks, and restores its header. Image and large-log comparisons audit public receipts rather than rebuild or remeasure their artifacts.

The optional duplicate harness attempt used `run.py --self-test` with TMPDIR set to packet scratch/tmp and PYTHONDONTWRITEBYTECODE=1. Its deliberate interruption and partial counts are preserved. It is not a complete local pass. The complete harness result cited in REPORT.md belongs to the public author receipt.
