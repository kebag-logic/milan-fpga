# R606-4 commands

`PACKET` is this packet, `CLONE` the detached clone at `8ab2b5399ecc725ff0ad4421c0e64ef03b89d28d`.
Disposable trees live under `$PACKET/scratch` (not published).

1. Merge reproduction: `git merge-tree --write-tree --name-only ce10328c c6bd08c6`, then `git diff <that tree> 9c57147d` (receipts `remerge_*`); per-file `git patch-id --verbatim` of `git diff ac2c5e77 ce10328c -- <f>` against `git diff c6bd08c6 HEAD -- <f>` (`patchid_lane_vs_head.txt`).
2. Environment: `scripts/ci_rv32_sdk.py --destination <dir> --archive <pinned archive>` (twice: one for the links, one at `$HOME/br-milan-rv32/host`); a CPython 3.12.3 venv with `pip install -r sw/litex/litex_pins.txt pyyaml`, `scripts/ci_litex_env.py`, `PYTHON=<venv python> sw/litex/patches/apply.sh`; a CPython 3.12.3 venv with the docs job's installs; sv2v v0.0.12 from its release digest; the scoped Verilator 5.050. `scripts/env.sh` sets `HOME`, `MILAN_RV32_CC`, `PATH`.
3. Runtime: `scripts/ctrl_image_runtime_nossp.py` (the repository's `ctrl_image_runtime.py` plus `-fno-stack-protector`) over picolibc / compiler-rt data checkouts (`receipts/fit/runtime_sources.txt`) and the venv's `litex/soc/software`.
4. Fit: `scripts/link_points.sh <tree> <out> <python> <runtime>` for a disposable clone at `ce10328c` (submodules at its pins) and for `$CLONE`; `scripts/fit_summary.py <out-a> <out-b>`.
5. `scripts/campaign_litex.sh` (aggregate self-test, aggregate, elaboration gate), `scripts/campaign_docs.sh c6bd08c6` (docs.yml commands), `scripts/rerun_elab.sh` (the elaboration gate alone after the overlapping first run).
6. `scripts/campaign_exports.sh <dev clone at c6bd08c6>`, using `scripts/soc_export.py`; digests by `scripts/export_digest.py <dev export> <head export> <dev tree> <head tree>`.
7. Hosted inspection: `gh run list --commit 8ab2b539...` and `gh run view <id> --json jobs` (read only).
8. Clone restore check: `git write-tree`, `git status --porcelain`, `git ls-files -v`, `git hash-object --no-filters` and mode of every tracked file, gitlinks, submodule status (`receipts/restore_verify.txt`).
