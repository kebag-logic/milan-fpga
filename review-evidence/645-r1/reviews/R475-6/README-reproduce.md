Reviewer receipts for R475-6 at `1e79ebdc06528edff74c0a7f530f20f99e3326a2`.

All build products and disposable inputs belong under `scratch/`, which is excluded from publication. The scripts accept the source checkout as their first argument and locate this packet from their own path. `REVIEW_SIM` must name the required pinned simulator executable; its observed version and executable hash are in `simulator-identity.txt`. Python 3, a C++ build environment and the reviewed dependencies are required.

Run these scripts in order, each as a foreground command:

```sh
export REVIEW_SIM=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
python3 run-focused.py /path/to/exact-head-checkout
python3 run-static-checks.py /path/to/exact-head-checkout
python3 run-dynamics.py /path/to/exact-head-checkout
python3 run-trace-probe.py /path/to/exact-head-checkout
python3 audit-evidence.py /path/to/exact-head-checkout
python3 verify-tree.py /path/to/exact-head-checkout
```

The launchers run independent children concurrently and wait for all children. Builds request `make -j16`; `sim-cap.py` limits each concurrent compiler to four workers. The initial controller campaign uses two simultaneous builds, keeping the maximum aggregate compiler workers at sixteen. The dynamic campaign uses four fine-pull jobs alongside the two longer source-switch legs. No shell job is detached.

Each executed task retains its command, combined raw output, process return code and elapsed seconds. Controller child receipts are copied from scratch into `control-receipts/`; fine-pull receipts are directly in `small-pull-receipts/`. `author-receipts/` contains copies of public evidence, not reviewer executions. `public-evidence-index.json` maps inspected public files to their published git blobs and byte hashes.

`run-trace-probe.py` reproduces the counterexample on unchanged source: the simulation passes, but the generated table counts one slip. A zero script return code means both commands executed, not that the table is correct. `audit-evidence.py` verifies and records the discrepancy; it intentionally asserts the currently observed defect. After a source repair, replace that assertion with the corrected expected value and add actual-slip controls. `independent-verdict.txt` records the independent conclusions before prior-finding reconciliation; REPORT.md is the final verdict.

`verify-tree.py` compares every tracked file's raw bytes and executable/symlink mode with its git blob, checks stage-zero index entries, and repeats that check inside each initialized required dependency. It writes `tree-verification.json`. `MANIFEST.sha256` excludes all scratch files and lists the publishable packet.
