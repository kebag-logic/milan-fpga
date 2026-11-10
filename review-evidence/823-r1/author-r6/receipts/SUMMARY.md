# Round 6 evidence (#823, format only) at 2905c8749a4573450b9999dd546bb20ae5c7fc38

The head is round 4's `30ca4b21` plus seven commits, on `dev-soft-core` `1d6bf555` (the merge base).
Every run below is on a fresh clean clone of the head unless a line says otherwise.
Each `*tree-after*` file records `git status` after its job; every one is clean.

## Workflow steps (`gates/verify.md`)

- The four workflows a pull_request to `dev-soft-core` triggers: `rtl-fast`, `elaborate`, `rtl` (as for a ready PR) and `docs`.
- 152 `run:` steps ran, all rc 0: 145 at the head, and the 7 of `rtl-fast firmware-unit` carried from `e0adcc09`.
  198 did not run, each with its reason in `gates/tools/not_run.json`. `verify_final rc=0`, 0 bad.
- Carried: `e0adcc09..2905c874` changes only `scripts/check_nvm_format_32x32.py` (one plant string).
  `firmware-unit`'s steps neither name nor scan that file (`gates/tools/carried.json`, logs in `gates/carried-e0adcc09`).
- Each job's logs come from the one root where it ran to its end at the head (`gates/JOBS.tsv`).
  The roots differ because the head moved once and the host restarted once (below).
- Runner: `gates/tools/run_wf.py`, one job per clone, step by step; drivers `gates/tools/drive.sh` with the lists
  `r6-*.txt`, `r7-*.txt`, `r8-c.txt` and `r9-*.txt`; driver logs in `gates/drivers`.
- `cd tests && behave` (`rtl-fast.bdd-conformance__ci_step_5`): 14 features, 508 scenarios, 2,330 steps passed.
- The builder bank, `test_builder.py --require-rv32`: legs 0 and 1 in `docs` and, with `--require-elaboration`, in
  `elaborate`. Each union is `builder: 107 gates exactly once; requirements judged on the union`, rc 0 (`gates/union`).
- The LiteX simulations: `elaborate.elaborate-gates-1__gate_19`, 8 of 8 PASS (`gates/litex-sim-logs`).
- The saved-state writer gate: `docs.docs-gates-0__gate_28`, `OK across 5 shape(s), and every planted defect reddened`.
- The format page's drift gate in the docs workflow: `docs.docs-gates-0__gate_26`, `0 finding(s)`,
  `control moved-lines: 0 finding(s)`, `self-test: PASS`.
- `firmware-boundary`: `ctrl_boundary: PASS`. The control mutants: `mutants: 570 of 570 caught`. The AECP and SRP
  campaigns: `test_ctrl_firmware: PASS`.

## Full sweep (`sweep/`)

- Four shard units, `scripts/run_all_suites.sh <logs> --wait --shard k/4`, spec `sweep/sweep-spec.json`.
  Shard 2, which holds `capture_coherence`, ran on four CPUs.
- Every shard's preflight passed, suite cancellation included (`sweep/shard-*/logs/preflight`). No #833 symptom.

| Shard | Suites | Passed | Timed out | Checks | In-suite failures |
|---|---:|---:|---:|---:|---:|
| 0 | 15 | 15 | 0 | 360,992 | 0 |
| 1 | 17 | 17 | 0 | 1,526,104 | 0 |
| 2 | 17 | 16 | 1 | 284,186 | 0 |
| 3 | 16 | 16 | 0 | 21,575 | 0 |

- `capture_coherence` hit its 2,400 s wall clock in shard 2: result unknown, not a failure.
  It was run again alone on four booked CPUs from shard 2's clone, with the sweep's own timeout and masked-verdict
  check (`gates/tools/rerun_suites.sh`): `capture_coherence rc=0 wall=2262s timeout=2400s`, 21,721 checks, 0 in-suite
  failures (`sweep/rerun-uncontended`).
- So 65 of 65 suites pass.
- `tsn_fuzz` rewrites the date line of two tracked `TEST_RESULTS.md` files in its clone, by design
  (`sweep/shard-3/tree-after.diff`); the counts are unchanged.

## Other gates (`extra/`)

- `extra.ctrl_nvm_selftest_final.log`: `test_ctrl_nvm.py --require-rv32 --self-test --jobs 8`, rc 0:
  `OK across 5 shape(s), 506 tests, and all 132 planted defects reddened` (127 planted defects and five controls).
  It prints `at width: MILAN_NVM3_MAPIN_ENTRIES_0 = 255, its table's limit, compiles`, `doctored build outside the host
  test: refused at compile time`, and the controls `mapin_limit_one_early` and `doctored_error_removed` caught.
  Its RV32 sizes equal round 4's at `30ca4b21` at all five shapes, so the store's code is unchanged.
- `extra.drift_gate_final.log`: `check_nvm_format_32x32.py` and its `--self-test`, rc 0, the six line-number plants
  each caught.
- `extra.diff_check_final.log`: `git diff --check 1d6bf555 2905c874`, rc 0.

## #818 waiver (`waiver/`)

- `hdl_gitlink_generated_diff.txt`: against `1d6bf555`, no HDL file, no gitlink and no tracked generated RTL changes.
- `generated_soc_rtl.md`: the shipping AX7101 SoC elaborated at both commits (no vendor run) gives the same generated
  RTL once each clone's path, the date lines and the hierarchy comment's sibling order are set aside.
  The init files, constraints and build script are byte-identical. The Arty launch line fails identically at both.

## Superseded (`superseded/`)

- `e0adcc09`, the first pass: `firmware-boundary` refused `scripts/check_nvm_format_32x32.py` as an unregistered
  program naming the firmware's tree (the list-form plant cited `sw/firmware/ctrl_nvm/...`); `2905c874` fixes it.
  Its `elaborate-gates-1` leg 1 timed out in `test_nvm_firmware.py --self-test` (1,200 s) under host load.
- `after-restart`: `elaborate-gates-1` leg 1 timed out again in `test_soc_options.py` (300 s) at host load about 250,
  niced in the shared session CPUs. On a booked range it passed (`gates/logs`).
- A host restart near 18:00 killed `firmware-boundary`, `docs-gates-1`, yosys shard 3, the first sweep and the first
  store self-test. Each ran again from a fresh clone; the partial runs are not counted.

Files over 200 KB are listed in each directory's `LARGE.tsv` by bytes and sha256.
`RAW.tsv` holds the digest of each source before host prefixes were replaced.
