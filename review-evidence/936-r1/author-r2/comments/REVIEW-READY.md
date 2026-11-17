[A793] REVIEW READY
Commit: `d1aa4c44` on `936-stream-notice`, PR #944 (base dev-soft-core `70f4056f`; 15 commits; round 2 is `343dfe43` to `d1aa4c44` on round 1's `7cfb8a04`)
Changed (round 2, answering R862-1 issuecomment-6953846656 and R861-1 issuecomment-6954572914):
- **R862-1-F1, the declaration's notice timed.** `bc921e68` adds the CPU budget harness arm `talker-notices` (`talker_notice.py`): `valid-destinations`' fixture with the stream observation answering every attempt.
  - Each of its eight `talker-notice-<k>` groups registers 16 controllers and starts a save, as `notice-retried-<k>` does.
  - It times a real PROBE_TX's declaration (`notice.declared`) and a range-losing ANNOUNCE's withdrawal (`notice.withdrawn`) of source 0. Each runs through SRP's record, the SRP delivery and the AECP bridge, from the event's mailbox RX commit to the last registration's STREAM_OUTPUT 0 GET_STREAM_INFO commit (for the declaration, the later of that and the PROBE_TX response).
  - Each event comes k ms into `notice-retried`'s load: every receive channel at its refill rate with its bursts, and a grandmaster change every pass. SRP's channel carries Listener Ready for another entity's stream, since one for source 0's would open its gate by itself.
  - Bound: the asynchronous notifications' existing 20 ms (FR_NFR.md 3.4.1, family `notify`); none added or moved. A row over it, or with no notice, fails the run whatever its options record.
  - Plants `declared-notice-dropped` (the bridge raises nothing) and `declared-notice-delayed` (the record held 25 ms) with their verdict; self-test checks. `d1aa4c44` keeps this Python within Rule 12: the arm's registrations in `talker_notice.py`, so `build.py` changes three lines at its 1,000, and `run.py`'s new branches as functions.
- **R861-F1, no idle pass with the notice owed.** `33f24ca3`: `ctrl_app_srp.c` `deliver` reports a taken record as owed output (`pending = noticed`).
  - Tests, each stepping single passes: `App.NoPassIsIdleWhileAStreamOutputsNoticeIsOwed` (from an idle loop, the first idle pass comes only after both controllers' notices) and `SrpGate.F936BThePassThatTakesTheRecordOwesItsNotice` (a real PROBE_TX and its 15 s expiry: the pass that takes each record returns nonzero).
  - Plants `app-output-notice-owed-unreported` (AECP campaign) and `talker-notice-owed-unreported` (both SRP campaigns). `83f1785f` moves the existing plant `binding-poll-adds-access`'s anchor to the new text. `d1aa4c44` moves the five #936 AECP plants, unchanged, into `aecp_notice_mutants.py`, which the campaign composes like its other sub-modules (Rule 12, `aecp_mutants.py` at 1,000 lines).
  - Product images: that change adds 8 B of rom in five split images; the other images and every sram figure are unchanged, and `57a10c8d` states the figures in `SPLIT_CONTROL_MEMORY.md` and the ledger reason.
- **Residues.** `343dfe43`: the dest-MAC owed row names `#943` (twin README, `twin_compare.py`'s label), and `ctrl_memory.py:247`'s comment uses R862-1-R1's exact replacement.
- **R861's questions 1 and 2** (the 1x1/1if held-egress growth; the 8x8/1if refused-attempt rounds) are recorded in the PR body as ruled not defects of this PR and owed to #894.
- No RTL, mailbox-contract or CPU-budget-bound change.
Validation (each on a fresh clean clone; workflow jobs replayed step by step, every `run:` step rc 0 or not run for a stated reason, only tool installs present on the host and hosted step recorders):
- `firmware-unit`: PASS, `fw_coverage.py --check` 39 files, the saved-state store's 526 tests.
- `firmware-srp-mutants`: 447 caught, none escaped (13 `talker-notice-*` in each campaign). `firmware-aecp-mutants`: 304 caught, none escaped (5 `app-output-notice-*`). `firmware-control-mutants`: 716 of 716.
- docs `wire-accountability`, `docs-check-no-git`, `docs-gates-0/1/2`, `docs-check`: PASS (61 steps).
- Twin: 1 finding, `split-talker-failed`, PR #935's stale row; the 20 plants other than `srp-plus-k` (PR #935's stale words) refused in both runs, 40 of 40.
- CPU budget harness `--self-test`: 0 failures; `check_py_idiom.py`: PASS (long function 9 of 9, long module 10 of 10).
- `talker-notices` at 1x1/1if and 8x8/1if: 16 rows each, every row within 20 ms (2.043 to 6.887 ms; 2.245 to 7.553 ms), 16 recipients each, 0 refusals, no `STATED` line, rc 0. `declared-notice-dropped` and `declared-notice-delayed` at 1x1/1if: each `caught: 16 of 16`. Image, origin, recipients, final commit, elapsed, bound and rc of every row are in the receipts' per-row table (the PR body has the per-run table).
- `answering-later` (1x1/1if, 8x8/1if) and `answering-every-port` (1x1/1if): PASS, 0 refusals, 0 misses.
- Release image byte-identical to the base (`bios.bin` 1x1 `860d4771`, 8x8 `d8851b6d`). `plat_ledger.py` PASS at every point; the size fixture and its arms within their entries.
Acceptance criteria:
- Decided by the specs: obliged (Milan v1.2 5.4.5.2, Table 5.22; IEEE 1722.1-2021 7.5.2). Met.
- Sent from where SRP changes the declaration, within AECP's notice bounds: `declare_sources` records it, the delivery takes it and reports it owed, and the bridge raises it on AECP's notice path. The new rows time it end to end at 20 ms. Met.
- A unit test and a planted defect cover it: eight tests; 13 `talker-notice-*` and 5 `app-output-notice-*` plants, each caught by name. Met.
- The twin row is deleted with its evidence: `stream-output-0-notices` deleted; STREAM_OUTPUT 0's notices match but for `stream_dest_mac` (#943), held by its own row with its plants. Met.
- The CPU service-budget harness shows the notice rows within their bounds. The declared and withdrawn Talker's rows: at most 6.887 ms (1x1/1if) and 7.553 ms (8x8/1if) against 20 ms, the dropped and delayed controls caught by name. The existing notice rows hold too: `answering-later` at most 8.392 and 8.164 ms against 20 ms; `answering-every-port` (1x1/1if) 192 notices at most 27.294 ms against 140 ms. Met.
Open risks/questions:
- Lane conflicts:
  - PR #935 (`37255683`): text conflicts in the twin's Makefile, README and `twin_compare.py`; round 1's scratch merge resolved them with a clean twin.
  - PR #932 (`0fdfdba7`): text conflicts in the memory ledger; the second to land re-measures.
  - PR #914 (now `e1ecce20`): one text conflict in `run.py`'s `all_groups`; keeping both lines resolves it.
- #943 owns the split's `stream_dest_mac` and the face's other STREAM_OUTPUT gaps.
