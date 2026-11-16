# R847-1 commands (PR #931, exact head 70c100da36330bb3862d76fa6eb003091775f310)

`<clone>` is the reviewer's detached clone at the exact head; `<packet>` this packet; `<head-copy>` and
`<mut-copy>` disposable copies of `<clone>` under `<packet>/scratch` (never published). Verilator is the pinned
5.050 (`receipts/clone-state.txt`). The LiteX steps use the host's LiteX virtual environment on `PATH`.

| Receipt | Command (run from) | rc |
|---|---|---:|
| `firmware/fw_shard{0,1,2,3}.log` | `python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs {3,3,4,4} --shard k/4 --build-dir <packet>/scratch/fwk` (`<clone>`) | 0 each |
| `firmware/fw_coverage.log` | `python3 -B sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep <packet>/scratch/cov` (`<clone>`) | 0 |
| `twin/twin_maps.log`, `twin/maps.log` | `make -j4 VERILATOR=<pinned> twin-maps` (`<head-copy>/tb/verilator/milan_dp`) | 0 |
| `twin/twin_maps_plants.log`, `twin/no-edit.log` | `make VERILATOR=<pinned> twin-maps-plants` (same) | 0 |
| `probes/twin-maps-restore-commit-cut.log` | `<mut-copy>` with `aecp_restore_commit(&c->aecp->core);` (`ctrl_app_aecp.c:262`) replaced by a comment, then `make -j4 VERILATOR=<pinned> twin-maps` | 2 (expected: the probe must fail) |
| `probes/unit-probes.{log,json}`, `probes/<name>.log` | `python3 -B <packet>/scripts/r847_probe_mutants.py <head-copy> <packet>/scratch/probes --jobs 4` | 0 (reporter) |
| `probes/unit-probe-pick.{log,json}`, `probes/face-pick-ignored.log` | the same script, `--only face-pick-ignored`, after the probe's replacement was made compilable (`pick != NULL ? k : k`) | 0 (reporter) |
| `memory/test_ctrl_memory.log` | `python3 -B sw/litex/test_ctrl_memory.py` (`<clone>`) | 0 |
| `memory/plat_ledger.log` | `python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --self-test --build-dir <packet>/scratch/plat_ledger` (`<clone>`) | 0 |
| `budget/budget1x1.log` | `python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <packet>/scratch/budget1x1 --variant answering-ports --groups aecp-fanout,aecp-largest-notice --record-budget-findings --record-share-findings --jobs 2` (`<head-copy>`) | 0 |
| `budget/budget8x8.log` | the same with `--point 8x8` (two interfaces) and `--build-dir <packet>/scratch/budget8x8` | 0 |
| `budget/budget{1x1,8x8}_records.txt` | `python3 -B <packet>/scripts/r847_edit_records.py <head-copy> <packet>/scratch/budget{1x1,8x8}/results` (the harness's own `record_classes.read_leg` and `rule`) | 0 |
| `docs/docs_check.log` | `python3 -B scripts/docs_check.py` (`<clone>`) | 0 |
| `docs/gen_toc.log` | `<md-venv>/python3 -B scripts/gen_toc.py --check` (`<clone>`) | 0 |
| `evidence-read/hosted-checks-70c100da.txt` | `gh api repos/kebag-logic/milan-fpga/commits/70c100da.../check-runs` (read only) | 0 |
| `evidence-read/author-receipts-read.sha256` | sha256 of each author receipt read from archive `62ad61af` (`review-evidence/923-r1/author-r2/receipts/...`) | - |
| `clone-state.txt` | state of `<clone>` after every probe, untracked and ignored outputs removed | - |
