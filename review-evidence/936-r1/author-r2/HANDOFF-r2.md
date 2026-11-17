# #936 round 2 handoff ([A793])

Lane `936-stream-notice`, PR #944 (base dev-soft-core `70f4056f`), round 1 published at `7cfb8a04`. Nothing pushed;
the manager pushes. Round 2 answers both NEGATIVE reviews: R862-1 (PR #944 issuecomment-6953846656) and R861-1
(issuecomment-6954572914).

Public record on #936: TAKEN issuecomment-6932988493, STOP issuecomment-6935670442, round 1's REVIEW READY
issuecomment-6953386992. Round 2's one REVIEW READY: issuecomment-6960339991 (head `d1aa4c44`), text in `comments/REVIEW-READY.md`. Nothing pushed.

## Commits on `7cfb8a04`

| Commit | What | Answers |
|---|---|---|
| `343dfe43` | the dest-MAC owed row's owner is `#943` (twin README cell, `twin_compare.py`'s printed label); the ledger comment at `ctrl_memory.py:247` names the debt by R862-1-R1's exact words, no lane label | R862-1-R1/R2, R861-RES1/RES2 |
| `bc921e68` | CPU budget harness: the `talker-notices` arm and its `talker-notice-<k>` groups (`talker_notice.py`), the rows `notice.declared` and `notice.withdrawn` held by `run.notice_misses`, the plants `declared-notice-dropped` and `declared-notice-delayed` with their verdict, self-test checks, README | R862-1-F1 |
| `33f24ca3` | `ctrl_app_srp.c` `deliver`: a pass that takes SRP's record reports output owed (`pending = noticed`), so no pass is idle while the notice is unsent; tests `App.NoPassIsIdleWhileAStreamOutputsNoticeIsOwed` and `SrpGate.F936BThePassThatTakesTheRecordOwesItsNotice`; plants `app-output-notice-owed-unreported` (AECP campaign) and `talker-notice-owed-unreported` (both SRP campaigns); `TAKE`'s anchor follows the new text; SRP README | R861-F1 |
| `57a10c8d` | `SPLIT_CONTROL_MEMORY.md` and the fixture entry's reason in `ctrl_memory.py` state the final image's figures (8 B more at five images; the `talker-notices` arm's images) | the figures `33f24ca3` moved |
| `83f1785f` | the existing SRP plant `binding-poll-adds-access` anchored on `bool pending = false;`, which `33f24ca3` replaced: found by the SRP campaign at `57a10c8d` ("has 0 planting sites"); now anchored on `bool pending = noticed;`, the same defect | the SRP campaign |
| `d1aa4c44` | found by the docs jobs at `83f1785f`: Rule 12's ratchet (`check_py_idiom.py`) counted two more long modules (`build.py`, `aecp_mutants.py`, each exactly 1,000 lines at round 1) and two more long functions (`run.py`'s `verdict` 101 and `main` 104). The five #936 AECP plants move to `aecp_notice_mutants.py` (same set, 304 defects); the talker arms' variants, plants and control kinds to `talker_notice.py`, so `build.py` changes three lines and stays at 1,000; `run.py`'s new branches become `declared_verdict` and `print_notices`. The budget README's bare `FR_NFR.md` reference becomes a link (`docs_check.py`) | the docs jobs |

**Final head: `d1aa4c44`.** Every gate below ran on fresh clean clones of it. `33f24ca3..d1aa4c44` changes no
firmware source the product images are built from.

## R862-1-F1: the declared and withdrawn Talker's notice, timed

- **Arm** `talker-notices` (`tb/verilator/ctrl_service_budget/talker_notice.py`): `valid-destinations`' fixture with
  the face block's stream observation answering zeroed values at every attempt (as `answering-ports`').
- **Groups** `talker-notice-<k>`, k = 0..7. Each registers 16 controllers on every interface, starts a save at 1.7 s,
  then two rows on source 0's interface (family `notify`, bound min(T_svc, 24) = 20 ms, W = 0):
  - `notice.declared`: a PROBE_TX at NOW_MS 3,000 + k. The row runs from its ACMP RX commit to the later of its
    PROBE_TX response and the last of 16 recipients' STREAM_OUTPUT 0 GET_STREAM_INFO notices.
  - `notice.withdrawn`: a peer ANNOUNCE of the range at 3,600 + k (`talker_window.PEER_MAC`, compare_MAC FALSE). The
    row runs from its MAAP RX commit to the last recipient's notice.
- **Load.** Each event comes k ms into 130 ms of `save_window.arrivals` (every channel at its refill rate with its
  bursts) plus `flood gm 1`. The event's channel's load starts one refill period after the event, so its bucket
  admits the burst whole. SRP's channel carries a same-size Listener Ready for `BRIDGE_MAC << 16`. The load's own one
  names source 0's stream, `scenario.listener_ready`, and would open the DA gate by itself.
- **Failing.** A row over its bound fails the run in `run.notice_misses`; a missing notice is the row's refusal. Both
  apply whatever the options record.
- **Plants** `declared-notice-dropped` (no `aecp_changed(6, ...)`) and `declared-notice-delayed` (the bridge holds the
  record 25 ms). `run.declared_verdict` catches them only when both rows of every group fail for the plant's reason.
- **Self-test** (`selftest_notice.talker_checks`): the groups' shape, a late row fails, each plant caught only for its
  own reason, and both run every group of the arm.

## R861-F1: no idle pass with the notice owed

- `ctrl_app_srp.c` `deliver`: `noticed` records whether the take found a record, and `pending` starts there. A taking
  pass is never the loop's idle pass, and the bridge raises the notice in the next pass. Once it is raised, AECP's own
  retry holds it (`aecp_retry` returns `owed || retry_held`, and a notice it cannot send arms AECP's timer).
- Tried and dropped: taking the record after the gate. `srp_mbx_gate` only records the gate; the declaration
  (`declare_sources`) runs in a pass given whole to THE TRANSMIT, where no poll runs. So the next pass's take is the
  earliest either way.
- Tests: `App.NoPassIsIdleWhileAStreamOutputsNoticeIsOwed` (one and two interfaces) and
  `SrpGate.F936BThePassThatTakesTheRecordOwesItsNotice` (8x8/2if, a real PROBE_TX and its 15 s expiry).
- Plants: `app-output-notice-owed-unreported` (AECP campaign) and `talker-notice-owed-unreported` (both SRP
  campaigns), each caught by name.

## Gates at `d1aa4c44` (fresh clean clones)

Every workflow job replayed step by step (`run_wf.py`), each `run:` step rc 0 or not run for a stated reason (only tool
installs the host has and the hosted step recorders), verified by `verify_sel.py`. Tables in `receipts/workflows/`.

| Gate | Result at `d1aa4c44` |
|---|---|
| rtl-fast `firmware-unit` | PASS: firmware suites and RV32 builds, saved-state store 526 tests, `fw_coverage.py --check` PASS (39 files) |
| rtl-fast `firmware-srp-mutants` | PASS: both SRP campaigns, 447 caught, none escaped; the 13 `talker-notice-*` plants caught in each, `talker-notice-owed-unreported` and `binding-poll-adds-access` included |
| rtl-fast `firmware-aecp-mutants` | PASS: 304 caught, none escaped; the 5 `app-output-notice-*` plants caught, `app-output-notice-owed-unreported` included |
| rtl-fast `firmware-control-mutants` | PASS: 716 of 716 caught |
| docs `wire-accountability`, `docs-check-no-git`, `docs-gates-0/1/2`, `docs-check` | PASS (61 steps; the link-health, Python-idiom and no-git checks that failed at `83f1785f` included) |
| twin | 1 finding, `split-talker-failed`, PR #935's stale row; `stream-output-0-dest-mac` holds |
| twin plants | `srp-plus-k` escapes by its stale words (PR #935's); the other 20 plants refused in both runs, 40 of 40; tree clean |
| CPU budget harness self-test; `check_py_idiom.py` | `self-test: 0 failures`; Rule 12 PASS (long function 9 of 9, long module 10 of 10) |
| `talker-notices`, 1x1/1if and 8x8/1if | PASS: 16 rows each, every one within 20 ms, at most 6.887 and 7.553 ms; 0 refusals; no `STATED` line; rc 0 |
| `declared-notice-dropped`, `declared-notice-delayed` (1x1/1if) | `CONTROL ... caught: 16 of 16` each: no notification to any registration, and 26.641 to 30.568 ms against 20 |
| `answering-later`, 1x1/1if and 8x8/1if | PASS: the retried notice at most 8.392 and 8.164 ms against 20 ms; 0 refusals, 0 misses |
| `answering-every-port`, 1x1/1if | PASS: 192 notices at most 27.294 ms against 140 ms; 0 refusals, 0 misses |
| release image | byte-identical to the base: `bios.bin` 1x1 `860d4771`, 8x8 `d8851b6d`; disassembly and debug-stripped ELF identical |
| split images, `plat_ledger.py` | PASS at every point: rom 117,688 / 119,304 / 130,392 / 131,976 B at 1x1/1if, 1x1/2if, 8x8/1if, 8x8/2if (43, 44, 56, 60.5 RAMB36); `ctrl_plat` unchanged; product ROM banks unchanged |
| size fixture | 112,624 / 114,216 / 125,280 / 126,832 B (41.0, 42.5, 55.0, 59.0 RAMB36); every-port 127,140, valid-destinations 126,992, talker-notices 127,048 B at 8x8/2if (59.5) |

## Harness

| Run | Image `ctrl_app.elf` | Rows | Elapsed, ms | Refusals | Misses | `STATED` | rc |
|---|---|---:|---|---:|---:|---:|---:|
| `talker-notices` 1x1/1if | `ec6f0066` | 16 | 2.043 to 6.887 | 0 | 0 | 0 | 0 |
| `talker-notices` 8x8/1if | `b8d11ef5` | 16 | 2.245 to 7.553 | 0 | 0 | 0 | 0 |
| `declared-notice-dropped` 1x1/1if | `cebd7792` | 16 | none: "no notification" | 16 | 0 | 0 | 0, caught 16 of 16 |
| `declared-notice-delayed` 1x1/1if | `25a65fe5` | 16 | 26.641 to 30.568 | 0 | 16 | 0 | 0, caught 16 of 16 |
| `answering-later` 1x1/1if | | 8 | 8.061 to 8.392 (bound 20) | 0 | 0 | 0 | 0 |
| `answering-later` 8x8/1if | | 8 | 7.931 to 8.164 (bound 20) | 0 | 0 | 0 | 0 |
| `answering-every-port` 1x1/1if | | 192 notices | 1.858 to 27.294 (bound 140) | 0 | 0 | 0 | 0 |

Every row's origin and final commit: `receipts/budget/talker-notice-rows.md`. The unplanted runs' images are the size
fixture's `talker-notices` images at `d1aa4c44`. The same seven legs on `33f24ca3`, with byte-identical split images,
printed identical `NOTICE`, `REFUSED`, `BUDGET`, `STATED` and `CONTROL` lines (`receipts/superseded-33f24ca3-harness/`).

## Open

- **R861's questions 1 and 2**: ruled not defects of this PR and owed to #894; stated in the PR body.
- **Lane conflicts** (`git merge-tree` of `d1aa4c44`):
  - PR #935 `37255683`: the twin's `Makefile`, `README.md` and `twin_compare.py`.
  - PR #932 `0fdfdba7`: the memory ledger's four files.
  - PR #914 `e1ecce20`: one hunk in `run.py`'s `all_groups`, where #914 passes `spec` to `talker_window.groups`; keep
    both. #914's `build.py` uses `talker_window` only in the two lines this PR replaces.
- **#943** owns the split's `stream_dest_mac` and the face's other STREAM_OUTPUT gaps.

## Runner notes

No host restart in round 2. Between 18:35 and 18:43 my queue runner's count missed the `r2-*` unit names, so its cap
read 1 throughout. Exactly eight jobs were queued, so eight ran. The count now takes every unit of the lane.
Superseded runs, kept in the receipts:
- `57a10c8d`: the SRP campaign refused on `binding-poll-adds-access`; the AECP, control, docs and twin runs were
  stopped by name as cut.
- `83f1785f`: the docs jobs found the Rule 12 ratchet and the bare link.
- The harness legs at `33f24ca3` (identical images): the same results as at `d1aa4c44`.
