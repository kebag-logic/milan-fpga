# Reproduce the focused review

Use a clean detached checkout of `dd163e41438acb86e0c4d4e76df90f3f91ace1c0` with its required submodules initialized. All disposable extraction, mutation and environment directories belong under the output packet's `scratch/` directory.

Fetch evidence commit `c06e28ade922988b601abf8b6e6945bd5c890790`. Extract only these paths with `git archive` into `scratch/`:

- `review-evidence/s13-r1/author-r3/receipts`
- `review-evidence/s13-r1/author-r2/receipts/identity/MANIFEST.sha256`
- `review-evidence/s13-r1/MANIFEST.json`

Let `EVIDENCE` denote the extracted `review-evidence/s13-r1` directory, `PACKET` this review's output directory, and `REPO` the source checkout. Run these foreground commands, capturing stdout/stderr and exit codes:

```sh
rtk proxy python3 -I "$EVIDENCE/author-r3/receipts/identity/tools/replay.py" "$EVIDENCE/author-r3/receipts/identity"
rtk proxy python3 -I "$EVIDENCE/author-r3/receipts/identity/tools/rmutants.py" "$EVIDENCE/author-r3/receipts/identity" "$PACKET/scratch/mutants"
rtk proxy python3 "$PACKET/independent_compare.py" "$EVIDENCE"
rtk proxy env TMPDIR="$PACKET/scratch" python3 -B "$PACKET/wiring_probes.py" "$REPO"
rtk proxy python3 "$PACKET/verify_checkout.py" "$REPO"
```

Expected: replay ALL CLAIMS HOLD; 13/13 named operand plants; complete independent comparison; one unplanted control and five wiring probes; exact checkout and dependency bytes/modes/index.

`run_docs.py REPO OUTPUT_RECEIPTS PYTHON` runs the twelve focused documentation checks with eight workers. Set PYTHON to a disposable environment containing the hash-pinned `tools/markdown/requirements.txt` dependencies and `wavedrom==2.0.3.post3`, matching `.github/workflows/docs.yml`. Its subprocess temporary directories use the output packet's `scratch/`. All twelve final checks pass; register self-test is 61/61.

The two scoped arithmetic checks are `tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if` and `--point 8x8/1if`, executed from REPO. They do not re-measure CPU service or physical performance.

`receipts/docs-summary.txt`, `register.txt` and `register-selftest.txt` retain the initial missing-renderer refusal. `register-check-complete.*` and `register-selftest-complete.*` record the successful dependency-complete reruns. These are environment repair, with no source changes.

The independent comparator uses the old digest mapping and current decompressed content hashes for the three re-encoded gzip operands; original compressed gzip metadata was not published. Both old xz streams are reconstructed and hash-matched as an additional provenance check.

Only MANIFEST-listed files and REPORT.md are publishable. Never publish scratch/.
