# R813-1 receipts: how each was produced

Clone: a detached clone at `5fb6904ffe12effc4bde6bf5313faea7a3beebdc` (tree `7903e4d6821ca7fbd0e80a5d86220f18daf615f8`),
submodules at their gitlinks. Verilator: the pinned 5.050 (`verilator --version` prints
`Verilator 5.050 2026-07-01 rev v5.050`), passed as `VERILATOR=` to every build. `$HOME` stands in for the
host's home directory in the build logs. `M` is `tb/verilator/milan_dp`.

| Receipt | Command (from the clone unless noted) | rc |
|---|---|---|
| `receipts/srptx.log`, `srptx.rc`, `wire-/hold-/licence-report.json`, `srptx-captures.sha256` | `scripts/job_srptx.sh $M`: `make -j3 srptx`, then `python3 -B srptx_plants.py obj_srptx` | 0 |
| `receipts/srptx-mutants.log`, `.rc` | in `$M`: `VERILATOR=<pinned> VERILATOR_JOBS=4 python3 -B srptx_mutants.py` | 0 |
| `receipts/split.log` | `scripts/job_split.sh $M`: `make -j8 split` (rc 0); its `split-mutants` half was cut by the host power-off and re-run below | 0 (split) |
| `receipts/split-mutants.log`, `.rc` | in `$M`: `make VERILATOR=<pinned> VERILATOR_JOBS=4 split-mutants` | 0 |
| `receipts/build-twin.log`, `.rc` | `make build-twin` at the head; binaries copied out of the tree for the next row | 0 |
| `receipts/twin.log`, `.rc` | `scripts/job_twin.sh $M <binaries> <out>`: the `twin` and `twin-plants` recipes of `$M/Makefile`, on those binaries | 0 |
| `receipts/base-twin-build.log`, `base-twin.rc`, `base-twin-run.log` | the same `build-twin-sp` and split-half run in a tree whose `milan_dp` files are the base `1d6bf555`'s (`basetree-identity.txt`) | 0 |
| `receipts/twin-split-identity.txt` | `sha256sum` of the base's and the head's twin split capture | IDENTICAL |
| `receipts/basetree-identity.txt` | `git hash-object` of the base tree's `milan_dp` files against `git rev-parse 1d6bf555:<path>`; `git diff --stat` base..head of the shared firmware, RTL and submodules | all MATCH, no change |
| `receipts/probe-grader.log`, `.rc` | `python3 -I scripts/probe_grader.py $M <captures> <work>`: 24 reviewer malformations and boundaries | 0 (24 of 24) |
| `receipts/knockout.log`, `.rc` | `python3 -I scripts/knockout.py $M <captures> <work>`: each capture plant against a copy of the grader with its own check disabled | 0 (23 of 23) |
| `receipts/time-coverage.log` | `python3 -I scripts/time_coverage.py $M <captures>` | - |
| `receipts/srptx-repro.txt` | the head's split-half binary, `--srptx licence` run twice, compared with and without the timers' `id` field | - |
| `receipts/docs_check.log`, `.rc` | `python3 -B scripts/docs_check.py` | 0 |
| `receipts/test_evidence.log`, `.rc` | `python3 -B scripts/measure_test_evidence.py --check` | 0 |
| `receipts/hosted-check-runs-5fb6904f.tsv` | `gh api repos/kebag-logic/milan-fpga/commits/<head>/check-runs` (name, status, conclusion), read-only | - |
| `receipts/restore-check.txt` | `git status`, `git diff --quiet`, `git diff --cached --quiet`, `git write-tree`, each gitlink against its submodule HEAD, after every probe | clean |

`<captures>` are the three captures `make srptx` wrote at the head (their hashes in `srptx-captures.sha256`).
