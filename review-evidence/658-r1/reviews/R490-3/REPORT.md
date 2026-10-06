[R490] POSITIVE - exact head 0f3d37dbffc4ca3f0e0f69499de80fc256a7db57

Round R490-3, internal cleared-context review of issue #658 / PR #670. The exact head is `0f3d37dbffc4ca3f0e0f69499de80fc256a7db57`, tree `09e56fc45c22d563612af8602d2e6ef67d954a49`. The assignment is 6009196984; the review start is 6010225881.

## Verdict

**POSITIVE.** All five lenses were applied to the round-3 delta: three commits on `5747a8cb`, the head R490-2 found POSITIVE. No BLOCKER, MAJOR, MINOR or RESIDUE is open. One new SUGGESTION, S1, concerns a stale count in a docs row. That count was already stale at the base and at dev, so it belongs in a separate issue. Every earlier public finding on this PR is still resolved at this head. The earlier SUGGESTIONs are carried forward unchanged, because every artifact they cite is byte-identical to `5747a8cb`.

The verdict and ledger were drafted (`receipts/draft_verdict_and_ledger.md`, written 2026-10-06T05:57:26Z) before any earlier reviewer report on this PR was read. The reconciliation in the "Prior public findings" section came after that draft and changed neither.

## What the delta is, reconstructed

- **`c79c178e`** is a `--no-ff` merge of dev `a1e9839e` (#666, #668) onto `5747a8cb`.
- **`e8f7d247`** moves `DUT_READER_DISPOSITIONS` from `scripts/measure_test_evidence.py` into the new `scripts/measure_test_evidence_readers.py`. It also changes the pointer at `docs/development/CODE_QUALITY.md:1761`.
- **`0f3d37db`** is a `--no-ff` merge of dev `423ac5d9` (#669).

Authority for the round: assignment 6009196984, items 1-4 ("No other change"). The functional scope is unchanged from the stage-2 ruling 5988843004, with acceptance criteria frozen.

## Evidence (receipts in this packet)

### E1. The merges are mechanical, and no lane file changed in them

- **Both merges equal the automatic merge.** For each merge commit, `git merge-tree --write-tree <parent1> <parent2>` reproduces the recorded tree exactly:
  - `c79c178e`: `edb11ab6…` recorded, `edb11ab6…` recomputed.
  - `0f3d37db`: `09e56fc4…` recorded, `09e56fc4…` recomputed.
  - So neither merge carries a hand edit or a conflict resolution.
- **Ancestry holds.** `510fae60` is an ancestor of `a1e9839e`, and `a1e9839e` is an ancestor of `423ac5d9`.
- **The lane's own diff is unchanged.** `git diff 510fae60 5747a8cb` equals `git diff 423ac5d9 0f3d37db`, ignoring `index` lines. The three files of the move commit are excluded from that comparison, and the result is `LANE_DIFF_IDENTICAL`. Every lane hunk is therefore carried into the head byte for byte.
- **The overlap is the one file the move resolves.** Of the 20 files the lane changed and the 118 files dev changed since `510fae60`, only `scripts/measure_test_evidence.py` is in both.
- **The lane's artifacts are byte-identical to `5747a8cb`.** `git diff --stat 5747a8cb 0f3d37db` is empty over:
  - `hdl/milan/milan_datapath.sv`;
  - `tb/verilator/{milan_dp,milan_dp_render,capture_coherence,pp_shadow}`;
  - `CHANGELOG.md`, `SAVED_STATE_MATERIALIZATION.md`, `REGISTER_MAP.md`, `ENDSTATION_BUILDER.md`, `CHANNEL_MAP_64.md` and `TESTING.md`.
- **Gitlinks are unchanged** at all five points (`5747a8cb`, `c79c178e`, `e8f7d247`, `423ac5d9` and `0f3d37db`): processor `ead80360…`, gPTP `5dce647a…`.
- **Dev's HDL changes do not reach the lane's suites.** Apart from `hdl/milan/mailbox/*`, dev's HDL delta since `5747a8cb` is `README-tests.md` files only.
  - No file under `tb/verilator/{milan_dp,milan_dp_render,capture_coherence,pp_shadow,milan_dp_mclk}`, and nothing in `milan_datapath.sv`, names the mailbox.
  - The mentions of `sw/litex/build.sh` in those Makefiles are comments.
  - Dev's `sw/litex/milan_soc.py` hunk is gated by the default-off `--ctrl-mailbox`.

### E2. The table moved unchanged

Files: `receipts/table_*.txt`, `receipts/move_probes/Q0_order.out`.

- **Byte-identical.** The `DUT_READER_DISPOSITIONS = {` … `}` block is the same 135 lines with the same sha256, `ad10ad7a7409b6808cc6658a619d9007c63d50fc68afd73df8962bde7eedc193`, in both places:
  - at `c79c178e:scripts/measure_test_evidence.py`;
  - at `0f3d37db:scripts/measure_test_evidence_readers.py:20-154`.
- **Same items in the same order.** Parsing both tables gives 35 entries each, and `list(old.items()) == list(new.items())` is True. The measurement no longer defines a table at the head.
- **No other line changed in `measure_test_evidence.py`.** The commit removes the 135 table lines. It adds the import at `:105` and rewrites the comment at `:589-591`, which names the new module.

### E3. The measurement's behaviour is unchanged

Files: `receipts/move_equivalence/`, script `scripts/move_equivalence.sh`.

`python3 scripts/measure_test_evidence.py`, `--check` and `--selftest` each exit 0 at every point. Their outputs are byte-identical (`cmp`) in two pairs:

- `c79c178e` against `e8f7d247`;
- a scratch merge of `423ac5d9` into `c79c178e`, a dangling commit `8c086df1` that is never published, against `0f3d37db`.

What the head reports:

- `--check` prints `[PASS] every DUT-source reader has a current disposition`.
- `--selftest` reports 101 checks, 101 PASS.

### E4. The idiom ratchet holds, and the new module is inside the gate

Files: `receipts/move_equivalence/*.4.out` and `*.5.out`, `receipts/move_probes/`, script `scripts/move_probes.sh`.

- **Before and after the move.** `check_py_idiom.py` exits 1 with `long module 11 > ratchet 10` at `c79c178e` and at the scratch pre-#669 merge. It exits 0 with `long module: 10 <= 10` at `e8f7d247` and at the head, and every other ratchet is unchanged.
- **The selftest passes** 54/54 at all four points.
- **The budgets are untouched.** `git diff 5747a8cb 0f3d37db` and `git diff 423ac5d9 0f3d37db` are both empty over `scripts/py_idiom.budget` and `scripts/test_evidence.budget`.
- **Planted probes.** Each edits one file in place and is restored by `git checkout --`:
  - **Q1** drops the `acmp_mutants.py` entry from the new module. `--check` exits 1 with "1 unexplained DUT-source reader(s)".
  - **Q2** adds a stale entry. `--check` exits 1 and names `tb/no_such/reader.py`.
  - **Q3** pads the new module past 1000 lines. `check_py_idiom.py` exits 1 with `long module 11 > ratchet 10`.
  - **Q4** adds a 200-character line. It exits 1 with `over-long line 1 > ratchet 0`.
  - So the measurement really reads the moved table, and the new module really is inside the idiom gate's population. Its passing with every rule at 0 is a real result, not a population miss.
- **Header and mode match the neighbours.** The new module is mode 100644 with a `#!/usr/bin/env python3` shebang and an SPDX header (`CERN-OHL-W-2.0`). That matches its sibling helper modules (`measure_test_evidence_selftest.py`, `lint_rtl_policy.py`) and 66 of the 68 SPDX-headed scripts.

### E5. No gate registration is needed (the author's claim holds)

- **ci_scope covers the path.** Its rule is stated at `scripts/ci_scope.py:12-19`: every file under `scripts/` is relevant.
  - Probe Q5 pipes `scripts/measure_test_evidence_readers.py` into `ci_scope.py`, which prints `true`.
  - Q6, `ci_scope.py --selftest`, gives `selftest: PASS`.
- **The documentation workflow runs on every PR.** `.github/workflows/docs.yml:3-6` has a bare `pull_request:` trigger and no path filter. The gates that read the module therefore run whatever changes: `measure_test_evidence.py --check/--selftest` (`:313-314`) and `check_py_idiom.py` (`:356-357`).
- **No inventory names helper modules.** `git grep` finds no script inventory or docs page that lists them: there is no `scripts/*.md`, and sibling helpers are named only by the scripts that import them. The four classifier-gated workflows read `ci_scope.py`, so no other list exists to update.

### E6. Docs gates pass at the head

Files: `receipts/gates/`. All 15 exit 0:

- `docs_check.py`, `check_doc_style.py` and `check_doc_paths.py`;
- `check_hygiene.py --check`, `measure_naming.py --check`, `measure_fail_fast.py --check` and `check_todo_ownership.py`;
- `ci_events.py --check`, `check_feature_status.py`, `check_sh_idiom.py` and `DOC_MAP.gen.py --check`;
- `check_em_dash.py --base 5747a8cb` and `--base 423ac5d9`;
- `gen_toc.py --check` and `--verify-anchors`.

The last four ran with the pinned Markdown renderer (cmarkgfm 2025.10.22, html5lib 1.1, matching `tools/markdown/requirements.txt`) first on PATH.

### E7. The lane's focused leg passes at the exact head

Files: `receipts/dynmap/`.

- **Result.** `make -j16 dynmap` passes with 162 checks, 0 failures, rc 0. It ran in a scratch clone at `0f3d37db` with the same submodule gitlinks.
- **Simulator.** The pinned simulator identifies as `Verilator 5.050 2026-07-01 rev v5.050`; its wrapper's sha256 is `905795b9…`.
- **Agreement with round 2.** The count equals the round-2 count. The leg's inputs are byte-identical to `5747a8cb` (E1).
- **Redaction.** Host paths in the published log are replaced (`redaction.txt`).

### E8. The clone is restored

File: `receipts/restore_check.txt`.

- HEAD is `0f3d37db` with tree `09e56fc4`.
- Worktree against HEAD and index against HEAD are both quiet.
- The index modes and blobs equal `ls-tree -r HEAD`, and there are 0 untracked files outside the ignore rules.
- The gitlinks are `external efeb541a`, `gptp-processor 5dce647a`, `protocol-processor ead80360` and `verilog-axis 48ff7a7e`. The three checked-out submodules sit at their gitlinks and are clean.
- Ignored `__pycache__/` from the probe runs is left in place.

## Findings

### S1 - SUGGESTION - Docs - `docs/development/CODE_QUALITY.md:1761` - the row's count of classified readers is stale (it predates this lane)

- **Authority and evidence.** The row says "Nine readers are explicitly classified: eight mutation campaigns and one structural boundary check." That was true when it was written: `954924ea5` (2026-09-15) had 9 entries. The table now holds:
  - 33 entries at the base `e6172750`;
  - 34 at dev `423ac5d9`;
  - 35 at this head (E2).

  This round's edit to the same row, the pointer to `scripts/measure_test_evidence_readers.py` ("which the gate imports, prints on every run and requires to match the readers exactly"), is accurate. The "0" in the count column is accurate too.
- **Impact.** A reader of the row is told the population is 9 when it is 35. The gate itself counts from the live table, so no measurement is affected.
- **Required outcome.** None for this PR: the assignment is "No other change", and the staleness is in dev already. A separate issue should correct the count, or drop it in favour of "the live disposition list".
- **Verification.** The row's count equals `len(DUT_READER_DISPOSITIONS)` at that issue's head.

No other finding.

## Prior public findings on this PR, reconciled at `0f3d37db`

Every cited artifact is byte-identical to `5747a8cb` (E1), so each R490-2 and R491-2 resolution carries to this head unchanged.

| Finding | Status at `0f3d37db` |
|---|---|
| R490-1 F1 (MINOR, Tests): the guard arms are untested | RESOLVED, unchanged. The `[DYNMAP]` guard-arm checks still run in the 162/0 at this head (E7). |
| R490-1 F2 (MINOR, Docs and Tests): the gPTP-leg claim | RESOLVED, unchanged. The PR body's lines 198-202 still state what the leg grades and what `[DYNMAP]` grades. |
| R490-1 R1 (RESIDUE): `CHANGELOG.md:54` | RESOLVED, as the split accepted in R490-2. `CHANGELOG.md` is unchanged since `5747a8cb`. |
| R490-1 R2 (RESIDUE): `REGISTER_MAP.md` | RESOLVED, unchanged. |
| R491-1 F1 (MINOR, Docs): `SAVED_STATE_MATERIALIZATION.md` | RESOLVED, unchanged. |
| R490-1 S1, retained as R490-2 S2 (SUGGESTION, Tests): the talker end-to-end check runs inside the boot window | RETAINED, optional. `capture_coherence/sim_dp.cpp` is unchanged. |
| R490-2 S1 (SUGGESTION, Tests): the render RAM hold site is live on the Arty input shapes | RETAINED, optional, under #583. |
| R491-1 S1 (SUGGESTION, RTL): a shipping-shape edit-wait specialization | RETAINED, optional. The RTL is unchanged. |

## Lens coverage

- **[R490] PASS Conformance.**
  - Artifacts: assignment 6009196984, items 1-4, against the commits `c79c178e`, `e8f7d247` and `0f3d37db`.
  - Merge trees equal `merge-tree` of their parents, and the lane diff is identical (E1).
  - The table moved byte-identically with the same order (E2), and the behaviour is identical (E3).
  - Ratchets are unchanged and the gate passes (E4); the registration claim is checked (E5).
  - The stage-2 functional conformance artifacts are byte-identical to `5747a8cb`, and `[DYNMAP]` is 162/0 at this head (E7).
- **[R490] PASS RTL.**
  - `hdl/milan/milan_datapath.sv` is byte-identical to `5747a8cb`.
  - Dev's `hdl/` delta (`hdl/milan/mailbox/*`, `README-tests.md` files) is not instantiated by `milan_datapath` and not compiled by any lane suite. Its `sw/litex/milan_soc.py` hookup is behind the default-off `--ctrl-mailbox`.
  - The processor and gPTP gitlinks are unchanged, and the merges are conflict-free automatic merges (E1).
- **[R490] PASS Robustness.**
  - The `scripts/measure_test_evidence_readers.py` failure paths: a missing entry and a stale entry each fail `--check` (Q1, Q2). Over-length and over-long-line forms fail `check_py_idiom.py` (Q3, Q4).
  - The import is static and is resolved by the measurement's existing `sys.path` insert at `scripts/measure_test_evidence.py:103-106`.
  - The lane's boot-window robustness artifacts are unchanged (E1).
- **[R490] PASS Tests.**
  - `measure_test_evidence.py` default, `--check` and `--selftest` (101/101) give byte-identical outputs across both move pairs (E3).
  - `check_py_idiom.py --selftest` is 54/54 at all four points (E4).
  - The probes show both gates depend on the new module (Q1-Q4).
  - `make dynmap` is 162/0 at the exact head with the pinned simulator (E7).
  - No test or selftest was changed.
- **[R490] PASS Docs.**
  - `docs/development/CODE_QUALITY.md:1761` names the new home and the import correctly.
  - The new module's docstring (`scripts/measure_test_evidence_readers.py:4-18`) matches the gate's behaviour as probed in Q1 and Q2. The comment at `scripts/measure_test_evidence.py:589-591` is accurate.
  - These PR-body passages are consistent with E1-E5: lines 16-30 (status and feeders), 87, 99 (the move row), 108-111 (area standing) and 176-197.
  - The 15 docs gates exit 0 (E6).
  - S1 is a SUGGESTION and predates this lane.

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment 6009196984 items 1-4; merge trees; lane diff; table identity and order; measurement output identity; registration claim; `[DYNMAP]` 162/0 | R490-3 | `0f3d37dbffc4ca3f0e0f69499de80fc256a7db57` |
| RTL | CLEAN | `hdl/milan/milan_datapath.sv` (unchanged since `5747a8cb`); dev `hdl/` delta (mailbox, default-off, uninstantiated by the lane); gitlinks; merge-tree equality | R490-3 | `0f3d37dbffc4ca3f0e0f69499de80fc256a7db57` |
| Robustness | CLEAN | `scripts/measure_test_evidence_readers.py` and the measurement's import (`:103-106`, `:748-749`, `:810`); probes Q1-Q4; lane boot-window artifacts unchanged | R490-3 | `0f3d37dbffc4ca3f0e0f69499de80fc256a7db57` |
| Tests | CLEAN | `measure_test_evidence.py` default, `--check` and `--selftest` byte-identity (2 pairs); `check_py_idiom.py` and its selftest at 4 points; probes Q1-Q6; `make dynmap` 162/0 at the head | R490-3 | `0f3d37dbffc4ca3f0e0f69499de80fc256a7db57` |
| Docs | CLEAN | `docs/development/CODE_QUALITY.md:1761`; readers docstring; `measure_test_evidence.py:589-591`; PR body lines 16-30, 87, 99, 108-111, 176-197; 15 docs gates | R490-3 | `0f3d37dbffc4ca3f0e0f69499de80fc256a7db57` |

The functional lens coverage of rounds 1-2, R490-2 at `5747a8cb`, stays valid at this head. Nothing within those lenses' functional scope changed between `5747a8cb` and `0f3d37db` (E1). This round re-covered all five lenses at the exact head for the delta.

## Real limits

- **Banks I did not run.** These were outside my allowance, and I rely on the author's and manager's reports for them:
  - the full 48-command builder bank;
  - the full `milan_dp` suite and the other lane suites;
  - the mailbox and firmware feeder suites (`mbx`, `test_ctrl_firmware.py`, `test_ctrl_nvm.py`, the LiteX simulations);
  - Yosys, `xvlog_gate.py` and the OOC area point.

  What this round ran itself is listed under E3-E7.
- **Manager evidence is not yet public.** The tree named for public evidence (`d445cbd4…/review-evidence/658-r1`) holds only rounds 1-2 author evidence. I found no round-3 manager bank receipts there or in the PR and issue comments, so the manager's "banks passed at this head" is not yet a public artifact I could inspect.
- **Hosted runs were partly in flight.** A hosted check-run snapshot at 2026-10-06T05:57Z (`receipts/hosted_check_runs_snapshot.tsv`) shows:
  - 10 executed and successful;
  - 1 skipped context ("Physical gPTP (nightly and manual)"), which is not an executed job;
  - 8 still in progress: `docs-check`, `elaborate`, Verilator shards 0-4 and `yosys-elaboration`.

  This snapshot is not acceptance.
- **Host interpreter.** The host interpreter is Python 3.14.7, and hosted CI uses 3.12.
- **No hardware.** No hardware was used. Physical calibration is NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Hosted exact-head completion, and the act-first local replica.
- Publication of the round-3 bank receipts.
- Final candidate merge validation against live dev. The head already contains dev `423ac5d9`.
- The `route-1x1` area record on the merge result, and the AX7101 bench read of the power-on maps after flashing.
- When #645 lands, its new reader dispositions belong in `scripts/measure_test_evidence_readers.py`, not in the measurement.
- File S1 as a separate issue if wanted.
- Before merge: no review round in flight, explicit maintainer merge authorization, then post-merge containment.

No RESIDUE item from this round.

R490-3 FINISHED
