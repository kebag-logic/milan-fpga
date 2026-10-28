STATUS: REVIEW READY (merge round, executor [A680h]): head `0052e62e46582b701aa91d879c766b41682bfd3e`; every gate rc 0

# #665 lane S1 ([A680h]): merge round on PR #795

- Branch `665-s1-faces` (`origin` is `kebag-logic/milan-fpga`), from `dev-soft-core` `e76a755a`. Nothing pushed.
- Assignment: #665 issuecomment-6447669608. TAKEN: issuecomment-6447685643 (text in `TAKEN-COMMENT.md`); REVIEW READY:
  issuecomment-6450366910 (text in `REVIEW-READY-COMMENT.md`).
- Rulings still in force: 6421238472 (round-5 design), 6425357821 (memory). Reviews at `424b1489`: R701-6 and
  R702-6, both POSITIVE.

## Work list (assignment 6447669608)

- [x] 1. Merge `origin/dev-soft-core` `6660a1a0` into `665-s1-faces` as a merge commit (no rebase); resolve
  `ctrl_configs.py` keeping both sides. No other change.
- [x] 2. Gates (table below), all rc 0
- [x] 3. PR-BODY.md, REVIEW READY (text in `REVIEW-READY-COMMENT.md`)

## The merge

Merge commit `0052e62e`, parents `424b1489` (S1 round 6) and `6660a1a0` (dev-soft-core, PR #792 merged). It brings
S2's 36 files (`tb/verilator/ctrl_service_budget/`, the CI workflows and their scripts, `docs/testing/`, two
`tb/verilator/milan_dp*/README.md`, `sw/firmware/gtest/README.md`, `sw/firmware/ctrl/test/ctrl_configs.py`).

Only one file is changed by both sides since `e76a755a`: `sw/firmware/ctrl/test/ctrl_configs.py`. Git stopped on one
hunk, at the end of `OUTSIDE` (`ctrl_configs.py:179-202` at the merge head), where each side appended after
`sw/mailbox/publication_census.py`:

- S1 (`424b1489`): `sw/mailbox/census_ports.py` (`:179-180`), "classifies every port of the processor wrapper in
  the census's netlists, naming the firmware that writes each face (#665 S1); it compiles nothing".
- S2 (`6660a1a0`): the CPU budget harness's comment and its five `OUTSIDE` entries (`:181-202`: `build.py`,
  `runtime_ssp.py`, `scenario.py`, `selftest.py`, `split_soc.py`).

Resolution: both kept verbatim, each with its own reason: S1's entry first (it stays beside the other
`sw/mailbox/` entries), then S2's comment and entries. S2's `SUITES` entry (`fixture_variant.py`) merged without a
conflict.

Checks on the resolution:
- `git diff 424b1489 0052e62e -- sw/firmware/ctrl/test/ctrl_configs.py` is exactly S2's additions (both hunks);
  `git diff 6660a1a0 0052e62e -- sw/firmware/ctrl/test/ctrl_configs.py` is exactly S1's two-line entry.
- The files differing from `424b1489` are exactly the files `e76a755a..6660a1a0` changes, and those differing from
  `6660a1a0` exactly the files `e76a755a..424b1489` changes; every file but `ctrl_configs.py` equals the version
  of the parent that changed it (`git diff --quiet` per file).
- No new check and no planted mutant this round: nothing is added; the resolution is the change.

## Gate table

Head `0052e62e46582b701aa91d879c766b41682bfd3e` for every row. `git diff --stat 424b1489 0052e62e -- sw/firmware/`:
`ctrl_configs.py` (+26) and `sw/firmware/gtest/README.md` (S2's one line); no firmware source, test or exclusion.

| Gate | Result | Receipt (`receipts/`) |
|---|---|---|
| rtl-fast `firmware-boundary`, its steps as the workflow runs them (`probes/firmware_boundary.sh`: the CPU-derived budgets and `MAKEFLAGS`, the submodules, `ci_rv32_sdk_selftest.py`, `ci_rv32_sdk.py`, `ctrl_boundary.py --require-rv32 --selftest --without verilator`; LiteX and migen on `PYTHONPATH`, CPUs 32-47, its own unit) | rc 0, 1,031 s: SDK self-test OK; the pinned archive installed into a new scratch destination and verified (archive sha256 `d42680e9...b78f`), then `--verify-only` again; `ctrl_boundary: PASS`, 2,864 compiled sources of 3,094 invocations, 0 findings (round 6: the same counts) | `gates/firmware-boundary.txt` |
| the same, first attempt with `--destination ~/br-milan-rv32/host` (the workflow's literal step) | rc 1 at the SDK step: "missing regular SDK provenance receipt; incomplete install". That tree is the host's own SDK, never installed by `ci_rv32_sdk.py`; the installer's docstring requires a local run to name a new destination, and it never replaces an unreceipted tree. Not a defect of the head | `gates/firmware-boundary-host-sdk-refused.txt` |
| `ctrl_boundary.py --require-rv32 --selftest --only verilator` (not in the assignment's list; run because the conflicted file is the boundary's own classification table; pinned Verilator 5.050 first on `PATH`, own unit) | rc 0, PASS, 623 s: 775 compiled sources of 885 recorded invocations, 0 findings (round 6: 790 of 887; the counts follow what each `make` finds up to date in the checkout, as noted at round 6) | `gates/ctrl-boundary-only-verilator.txt` |
| `test_ctrl_nvm.py --require-rv32 --jobs 4` (rtl-fast `firmware-unit`'s step; it reads `ctrl_configs.py`'s `BUILDERS`) | rc 0, 101 s: "saved-state store gate (#665 F1): OK across 5 shape(s), 435 tests" | `gates/test-ctrl-nvm.txt` |
| `test_ctrl_firmware.py --require-rv32 --self-test --shard k/4`, four separate units (MemoryMax 8G, CPUs 32-35, 36-39, 40-43, 44-47) | rc 0 each (351, 1,221, 547, 847 s); shard sizes [61, 529, 138, 279] over 1,007 invocations; plants caught 61, 528 of 528, AECP 137 of 137, 280; 0 escaped (round 6: the same) | `fw/shard-*.txt` |
| `fw_coverage.py --check --jobs 8` | rc 0, 31 files at 100 %: `aecp.c` 417/417, 360/360; `aecp_commands.c` 450/450, 374/374; `aecp_face.c` 172/172, 152/152; `ctrl_app_aecp.c` 164/164, 124/124 | `gates/fw-coverage-check.txt` |
| `test_builder.py --require-rv32` (own unit, without `MILAN_RV32_CC`) | rc 0, "ALL GATES PASS EXCEPT 1 NOT RUN": gate 11 needs a local Arty build report this host lacks (as at round 6); 1,541 s | `gates/test-builder.txt` |
| linked images, four points (`probes/image_points.sh ... ledgered`, the `-fno-stack-protector` runtime; ruling 6425357821) | link and plan rc 0 at each: 37.0, 40.5, 50.5 within 56; 8x8 two interfaces 57.5 with `--ledgered-point`; refused without it (rc 2); the override refused on the other three (rc 2). The four ELFs are byte-identical to round 6's (`424b1489`) and every plan file equals round 6's | `images/` |
| S2's harness self-test `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` | rc 0, "self-test: 0 failures", 62 grader mutants caught (`selftest_mutants.py` runs inside it; run alone it is a library and does nothing) | `gates/harness-selftest.txt` |
| docs gates (`probes/docs_gates.sh`: the docs workflow's 69 commands needing no runner install; command list re-checked against this head's `docs.yml`, which the merge changes only in `runs-on`) | 69 of 69 rc 0 | `gates/docs-gates.txt` |
| the bare-metal scope gate, `check_baremetal_only.py --check` and `--selftest` | rc 0 each (inside the docs gates) | `gates/docs-gates.txt` |
| the docs workflow's CI-tooling self-tests the merge brings scripts for (`probes/docs_ci_selftests.sh`: 15 `ci_*` self-tests and checks, `act_ci.py --selftest`, `test_firmware_compiler.py --selftest`) | 16 of 16 rc 0 | `gates/docs-ci-selftests.txt` |
| `cd tests && behave --no-capture -f plain` | rc 0: 14 features, 406 scenarios, 1,977 steps | `gates/behave.txt` |
| four-shard Verilator sweep (`native-shards.py`, pinned Verilator 5.050 and sv2v 0.0.12, CPUs 112-115, 116-119, 120-123, 124-127) | rc 0 each (4,740, 4,086, 5,275, 3,825 s, on 4 CPUs each): shards 0 to 3 pass 15, 17, 16 and 16 suites (64 of 64), 250,913 + 1,536,446 + 380,086 + 23,679 = 2,191,124 checks, 0 in-suite failures, 0 timed out; declared skips only `tsn_fuzz`'s two field campaigns (tsn-gen not installed). Suites and checks equal round 6's at `424b1489` | `sweep/sweep-0052e62e/` |

Not run: `gen_mailbox.py --check --crosscheck`, the census, `lint_rtl.py`, `KL_mbx` OOC. The merge changes no file under
`hdl/`, `sw/mailbox/`, `syn/` or `configs/` and no generated file; round 4's and 5's receipts stand, and the sweep
runs `mbx` again. The docs workflow's wavedrom, HDL-reference-install and builder-leg steps need runner installs;
the builder legs are `test_builder.py`, run above.

## Process notes

- The workflow's literal SDK step (`ci_rv32_sdk.py --destination ~/br-milan-rv32/host`) refused this host's own SDK
  tree (no installer receipt). The installer installs into an absent prefix or verifies a receipted one and never
  replaces anything; its docstring requires local runs to name a new destination. The boundary job was re-run with
  the pinned archive (already on the host, checked by the installer against the pinned digest) installed into a new
  scratch destination; the boundary itself finds the SDK compiler as in every earlier round.
- `selftest_mutants.py` run alone is a library and does nothing (its no-op receipt was discarded); its 62 mutants run
  inside `run.py --self-test`.
- The firmware self-test shards, `ctrl_boundary.py` and `test_builder.py` each ran in their own unit (MemoryMax 8G,
  peak well under 1 GB); the sweep's four units ran on 112-127 with MemAvailable above 40 GB throughout. No Vivado.
- The sweep's four shard clones are `$LANES/665s1-a680h-shard{0..3}` (made by `native-shards.py`), outside
  the tree; the SDK installed for the boundary job is in the work directory, not in this output directory.

## Receipts

`receipts/INDEX.md` is generated from the files present by `probes/collect_receipts.sh` (host paths replaced by
placeholders; files over 200 KB listed in `receipts/large-files.txt` with size and sha256, never copied;
`gates/docs-ci-selftests-summary.txt` carries the large CI self-test log's status lines). Scripts under `probes/`:
`run_gate.sh` (a command's log and its rc), `firmware_boundary.sh` (the rtl-fast job's steps), `docs_gates.sh` (round
5's, unchanged), `docs_ci_selftests.sh` (the CI-tooling self-tests), `image_points.sh` (round 5's, unchanged),
`collect_receipts.sh`.
