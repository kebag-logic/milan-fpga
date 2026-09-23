# A195 handoff: #523 / PR #526, R257-2-F1 (Tests)

## Head

- Commit `015edd9ab2248289ff000f6ef14890be1812ba7b`, tree `fc03d0313af978c147bf734f9905fdc427a2b758`.
- Parent `26353960ae2763cc09741d0f7bcc720621bd5148` (the reviewed head).
- Subject: `Assert the sweep shell's cancellation report and log attribution at every boundary` (one line, no trailers).
- Not pushed. No PR, issue-label or project edit. The worktree is clean.
- Diff `26353960..015edd9a`: `scripts/test_suite_cancellation.py` only, +63 -7.
  - No production, docs, workflow or ratchet file changed.
  - Blob `839a8703` (sha256 `2a5de7dd...25d6`). The base blob is `abb73afb` (sha256 `0821f97a...18cf`).

## What the test now pins

The sweep's normal preflight already runs this file (`scripts/run_all_suites.sh:272`). That wiring is unchanged, so the new arms are owned by the normal entry point.

1. `cancel_report()` (test_suite_cancellation.py:114-127). Every graceful cancellation arm now asserts three things:
   - The shell's own line, `CANCELLED: INT|TERM; no completed sweep result`, is present. The owner's `signal N` line no longer satisfies the check.
   - After log preparation (preflight, command, transition): exactly one `partial logs: <requested OUT>` line, and no not-prepared line.
   - Before preparation (selection, lock wait): the `logs were not prepared for this invocation` line, and no `partial logs:` line. The previous invocation's logs in OUT must also be byte-unchanged.
2. A new `lock_wait()` arm, for INT and TERM (test_suite_cancellation.py:211-242, run from `main()` at line 379).
   - The test holds the tree lock, and the sweep runs with `--wait`.
   - The boundary is the sweep shell's own `flock` child, seen in `/proc` under the launched entry. No delay and no shim is involved.
   - After the signal, the arm expects exit 128+N, the not-prepared report and the previous logs intact. No prerequisite and no suite may run.

## Mutation evidence

Harness: `scripts/mutate.py` in this packet.
- Each copy is `git archive 015edd9a scripts` with exactly one textual defect in `run_all_suites.sh`. The replaced text must occur once.
- The copy's own test file then runs: the new blob, and separately the base blob from `26353960`.
- Copies lived under `/tmp`; the lane was never mutated.
- Receipts: `receipts/mutants/{new,base1,base2}-results.json`, plus a full transcript per run.

| Mutant | Base test (26353960) | New test (015edd9a) | Where the new test fails |
|---|---|---|---|
| `none` (unmodified) | PASS (0) | PASS (0) | - |
| `logs-ready-early` (LOGS_READY=1 from the start) | PASS (0) | RED (1) | cancel_report:125, from cancellation (selection) |
| `logs-ready-never-set` | PASS (0) | RED (1) | cancel_report:123 (preflight) |
| `no-partial-logs-message` | PASS (0) | RED (1) | cancel_report:123 |
| `no-term-trap` | PASS (0) | RED (1) | cancel_report:119 (shell line missing) |
| `no-int-trap` | RED (1) | RED (1) | cancel_report:119 |
| `no-unprepared-message` | PASS (0) | RED (1) | cancel_report:125 |
| `report-inverted` (`= 1` becomes `!= 1`) | PASS (0) | RED (1) | cancel_report:125 |
| `partial-logs-wrong-dir` (prints `$ROOT/.suite-logs`) | PASS (0) | RED (1) | cancel_report:123 |
| `int-reported-as-term` (INT trap names TERM) | PASS (0) | RED (1) | cancel_report:119 |
| `prepare-before-lock` (logs cleared before locking) | PASS (0) | RED (1) | cancel_report:125, from **lock_wait**:240 only |

- The four defects R257-2-F1 names survive the base test and are red under the new one. The same holds for five further removals or corruptions.
- `prepare-before-lock` is caught only by the new lock-wait arm.
- The mutant names follow the finding. The exact textual edits are this harness's own (see `MUTANTS` in mutate.py). The reviewer's `probe_mutations.py` was not used.

### Through the normal entry point

These runs use a disposable `git archive` copy of the whole head. A PATH `make` guard (`receipts/20-guard-make.sh`) makes any suite build fail instantly, so no suite bank can run.

- **Mutant** `logs-ready-early`: `bash scripts/run_all_suites.sh OUT` exits **2** with `ABORTING: sweep cancellation controls failed.` (`receipts/20-entry-point-mutant.txt`).
  - Its preflight log shows the `cancel_report` assertion (`receipts/20-entry-point-logs/`).
  - Nothing ran after the first preflight.
- **Unmodified head**, with `--shard 1/60`: the sweep's own `preflight/test_suite_cancellation.log` shows both `cancel-lock-wait-*` arms and `suite cancellation: PASS` (`receipts/21-entry-point-logs/`).
  - The sweep then stopped with exit 2 at the later `check_merge_containment` self-test ("could not locate Git's legacy graft file").
  - That stop comes from the copy: it is an archive, not a Git checkout. It is not a product failure, and no suite ran.

## Gates at the head

| Command | Exit | Receipt |
|---|---|---|
| `python3 scripts/test_suite_cancellation.py` (clean tree at 015edd9a) | 0 (40 s) | receipts/40-head-test.txt; transcripts in receipts/40-head-transcripts/ |
| `python3 scripts/check_py_idiom.py` | 0 | receipts/gates/head-check_py_idiom.py.txt |
| `python3 scripts/check_sh_idiom.py` | 0 | receipts/gates/head-check_sh_idiom.py.txt |
| `make -C tb/verilator/gptp_shadow lifecycle` | 0 (47 s), `mutant lifecycle: PASS`, nested-SIGINT 130, nested-SIGTERM 143 | receipts/30-gptp-shadow-lifecycle.txt |
| `check_py_idiom.py --selftest` | 0 (54/54) | receipts/gates/check_py_idiom.py__selftest.txt |
| `check_sh_idiom.py --selftest` | 0 (48/48) | receipts/gates/check_sh_idiom.py__selftest.txt |
| `measure_fail_fast.py --check` | 0 | receipts/gates/measure_fail_fast.py__check.txt |
| `measure_test_evidence.py --check` | 0 | receipts/gates/measure_test_evidence.py__check.txt |
| lock-wait arms, 25 repetitions per signal | 0 (50/50, 17.5 s) | receipts/41-lock-wait-repeat.txt |

- The first four rows and the lock-wait repeat ran at the committed head.
- The two selftests and the two ratchet checks ran on the pre-commit worktree. Its only change was the file later committed, byte-identical to blob `839a8703`.
- Baseline before the change: the unmodified test at `26353960` exits 0 (receipts/00-baseline-head-test.txt).

## Limits

- Not run: full banks, act/Docker, hosted CI, hardware. The PR head is not pushed, so no hosted evidence exists for 015edd9a.
- The lock-wait arm needs `flock(1)`, as the existing `lock_free()` hard-stop check already does. The `mkdir` fallback lock is not exercised.
- Ignored `tb/verilator/gptp_shadow/obj_dir` and `gptp_ucode.hex` in the lane predate this session (09:27) and were left in place. No leftover process was found under my scratch paths, and my scratch copies were removed.
- Packet host paths are unnormalised. Every file is listed in MANIFEST.sha256.

REVIEW READY posted: https://github.com/kebag-logic/milan-fpga/issues/523#issuecomment-5794119960
