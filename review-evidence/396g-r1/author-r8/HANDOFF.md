# HANDOFF: #396 part A round 8 (release gate plan), executor [A674h]

Status: **REVIEW READY** at `a7a514fbf5572ce08394cd727c9cc9085745c79f` (tree `7bdbb8703e4e4dd34c86adb234af37ec68a2e6d3`),
branch `396-release-gate-plan`. One round-8 commit sits on the round-7 head `5fdabc1c4c76206bd2528435c56d88466c0f972e`,
which is not rewritten. Base dev `e76a755afc0536453161e3cd33f6f4d2dcd7641f`. Nothing is pushed, and no PR operation ran.

- Round-8 assignment: #396 issuecomment-6443031364. Its ruling (R699-7 F1 option (b), final for the listing-position
  class): outside the swept scope the property promises coverage, not position.
- Findings answered: R699-7 (PR #786 issuecomment-6443018323) F1 (MINOR), R1 and R2 (RESIDUE), S1 and S2
  (SUGGESTION). The lower edge was ruled after the round-7 STOP in issuecomment-6442502921.
- TAKEN: issuecomment-6443121924. REVIEW READY: issuecomment-6447565851 (text in `READY-COMMENT.md`).
- The prompt's trailing "Round 4" paragraph (commits on `4d69e192`, "REVIEW READY - round 4", a Round 4 PR section) is
  the standing template of earlier rounds; it is applied as round 8: commits on `5fdabc1c` (`4d69e192` is an ancestor
  and untouched), "[A674h] REVIEW READY - round 8", and a Round 8 section in `PR-BODY.md`.
- Remote checked: `origin` is `https://github.com/kebag-logic/milan-fpga.git`; the branch descends from `e76a755a`.
  No git command ran inside a submodule; the gitlinks equal the base (`receipts/gates/head.txt`;
  `git diff --stat e76a755a HEAD -- protocol-processor gptp-processor external third_party` is empty). No RTL,
  firmware, builder, Vivado, hardware, bench or flashing action ran.
- R699-7 packet: `origin/396g-review-evidence` at `ffe4804a`, `review-evidence/396g-r1/reviews/R699-7/`. It was
  extracted to a scratch directory outside this one; every file matches its `MANIFEST.sha256`. Its probe scripts ran
  unchanged (`python3 -I -B <script> <export of a7a514fb> ...`).
- Commit (one line, no body, no trailer): `a7a514fb` `Promise coverage, not position, for each audio event outside the
  exactness scope, gate every unit by it, and add a control that leaves a slip uncovered on one channel (#396)`.

## How the ruling was applied

1. **The rule, stated exactly** in REQ-VER-06, TESTING 6d, `AUDIO_COUNTER_LIMITS[0]`, the `audio.counter-classified`
   text and the PR body: never `PASS`; each event covered on each channel it changes by at least one listing whose
   samples overlap [first word - 63, last word + 63]; an event inside a constant-mask excursion on the same channel may
   be covered by that excursion's listing alone; inside the scope each listing begins within 63 samples of the first
   word (at its `capture_index`); outside it, coverage, not position. Every outside-scope sentence about where a listing
   begins is dropped, including the interrupted-excursion limit's "listed from its first word" and the pin's name.
   Two qualifiers already at `5fdabc1c` stay, because the rule is false at pinned cases without them: "the bytes show"
   (events that cancel or only move an arm leave a clean run's bytes) and the void exception (an event that masks a
   planted arm). Published in TAKEN and in the PR body.
2. **The gate.** `reaches` was already the ruling's overlap test, so no gate logic changed; its docstrings and
   failure words now say "covered". The fuzz asserts it for every unit of both families (384 compositions); the two
   sweeps still assert exact listing in the scope. New control #298 leaves a DUT slip uncovered on channel 3; the
   gate kills it at seed 0. R699-7's `probe_reach.py` reports 0 units uncovered by the rule (each reported unit is
   checked by `scripts/classify_reach.py`).
3. **Residue.** R1 and R2 applied as written; the PR body says the lower edge was ruled in issuecomment-6442502921.

STOP condition (a swept case changes its grade or listing): **not met.** No grader line changed (the commit touches
string constants, docstrings, two failure messages and a test name in the planner). The 445 sweep captures dump
byte-identically at `5fdabc1c` and `a7a514fb`, digest `5f0b7f12…` (`receipts/round8/sweeps_compare.log`).

## Changes (file:line at `a7a514fb`; `tb/tools/torture_campaign.py` unless named)

| Change | Where | Reason |
|---|---|---|
| Property: covered on each channel by an overlapping listing; listing samples defined; the excursion clause; inside the scope a listing begins within 63 of the first word; outside it coverage, not position | `REQUIREMENTS.md:408`-`:419` | Ruling item 1 |
| Same, with the 63's reason; the two sentences that justified the old lower edge dropped | `docs/testing/TESTING.md:1487`-`:1501` | Ruling item 1 |
| Interrupted-excursion limit: "An interrupted one is listed from its first word" dropped | `docs/testing/TESTING.md:1456`-`:1457`; `counter_limits` `:3812`-`:3814` | Ruling item 1 ("drop every outside-scope sentence about where a listing begins") |
| Gate paragraph: R1's "slips in three draws of seven"; the check stated as coverage, both directions | `docs/testing/TESTING.md:1510`-`:1512` | R1; ruling item 2 |
| Pinned-shape bullet and the pin's name | `docs/testing/TESTING.md:1532`-`:1533` | Ruling item 1 |
| `audio.counter-classified` text | `:3338`-`:3348` | Ruling item 1 |
| `AUDIO_COUNTER_LIMITS[0]` | `:3752`-`:3759` | Ruling item 1 |
| `_close` docstring no longer says where the excursion is listed | `:4859`-`:4861` | Ruling item 1 |
| `_fuzz_nested` docstring: "a slip in three draws of seven" | `:9420`-`:9423` | R1 |
| `_fuzz_check` and `reaches` docstrings; failure words "a DUT event is not covered", "a DUT listing covers no DUT event" | `:9460`-`:9470`, `:9479`-`:9480`, `:9500`, `:9504` | Ruling item 2 |
| Gate test docstring | `:9507`-`:9515` | Ruling item 2 |
| Pin renamed `test_audio_excursion_a_slip_interrupts_keeps_its_bit_flip`, docstring says it pins one reading; assertions unchanged | `:9575`-`:9583` | Ruling item 1 (its old name and docstring said "listed from its first word") |
| `_INTERRUPTED` follows the rename; control #298 | `tb/tools/torture_release_audio_mutants.py:27`, `:233`-`:237` | Ruling item 2 |
| PR body: Round 8 section, `audio` row, Round 7 item 1 and decision paragraph (R2), Round 7 item 2 (R1), Round 6 item 1, references, validation counts, limitations (R2's risk closed) | `PR-BODY.md` | Ruling items 1 and 3; R1; R2 |

## New check, planted defect and failing words

| Arm | Planted defect (control #) | First failing words |
|---|---|---|
| `test_audio_compositions_never_pass_and_list_every_event` `:9507` (coverage per unit and channel) | a DUT slip's listing removed on channel 3 after attribution (#298) | `AssertionError: seed=0: False is not true : ('a DUT event is not covered', 'slip', 245, 3, 'FAIL', …` (`receipts/round8/quick_named_audio_mutants.log`) |
| `test_audio_excursion_a_slip_interrupts_keeps_its_bit_flip` `:9575` (renamed) | a returned excursion's bit-flip left for the hold (#295, unchanged) | `AssertionError: Tuples differ: (0, 6097, 'dropped', 1021, '') != (0, 4424, 'bit-flip', 1673, '0x00080100')` |

A first version of #298 dropped the slip inside `_record`. It also hid the planted slip arms on channel 3, so the gate
failed at its clean-run check, not at coverage. It was moved after attribution before the commit
(`receipts/round8/` holds only the committed version's runs).

## Evidence at `a7a514fb`

R699-7's scripts, unchanged (`receipts/r699-7_probes/`):

| Probe | Result | vs R699-7's receipt |
|---|---|---|
| `probe_reach.py` nested 8192 / 16384, seeds 0-47 | 6 / 6 units | byte-identical |
| `probe_reach.py` arm 16384, seeds 0-287 | 0 units | byte-identical |
| `probe_reach.py` nested 8192 / 16384, seeds 0-1999 | 226 / 228 units | byte-identical |
| `probe_dump.py` nested 16384 seeds 0, 11, 21; 8192 seed 0 | each ends `fuzz_check: ('FAIL', set())` | byte-identical |
| `probe_new_mutants.py`, last 4 controls (#295-#298) | pristine named tests pass; each control fails its named test | adds #298 |

Round-8 measurements (`receipts/round8/`; scripts in `scripts/`):

- `reach_coverage.jsonl` (`classify_reach.py` over `probe_reach.py`'s outputs, independent of the planner): 0 uncovered.
  Gate seeds: 12 of 12 covered by the excursion's own listing. Seeds 0-1999: 450 of 454 so; 4 by another
  overlapping listing (seed 248 at 16384, a copy past the return; seed 1592, a slip pair read as one bit-flip).
- `census_*.jsonl` (`coverage_census.py`): gate seeds, 1,771 unit-channels, all covered; 10,000 seeds per family and
  length: 0 gate refusals; uncovered unit-channels are void beside a missed arm (109, 109, 4, 0) or excused as
  cancelled or clean (9, 9, 20, 20). Arm-led then nested; 8192 then 16384 frames.
- `s1_fuzz_vs_295.log`: with #295, R699-6's case is still covered (`_fuzz_check` passes, the gate passes); only the pin fails.
- `quick_named_audio_mutants.log`: 79 of 79 audio controls fail their named arm alone; #290-#292 at seeds 1, 146, 12.
- `sweeps_*.digest.json`, `sweeps_compare.log`: the STOP check (4.85 MB dumps kept out, sha256 recorded).
- `sweep_scope_check_a7a514fb.json`: inside the scope, all 4,356 swept events in captures that do not void have a listing
  beginning within 1 sample of the first word on each channel, and are covered.

## Gate table (exact head `a7a514fb`, never piped; `receipts/gates/`)

| Command | rc | Result |
|---|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | 0 | 120 tests OK (`selftest.log`) |
| `python3 -u -B tb/tools/torture_release_mutants.py` (background, on the `a7a514fb` export, polled) | 0 | `PASS: 298 mutations killed; source unchanged`, 13:39 to 16:30 UTC, 2 h 51 min on a shared host (`release_mutants.log`, `.start`, `.end`, `.export_sha256.txt`) |
| `cd tests && behave --no-capture -f plain` (rtl-fast bdd-conformance) | 0 | 14 features, 495 scenarios, 2286 steps (`bdd_conformance.summary.txt`; the 230 KB log is hashed there) |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | 0 | 176 scenarios, 665 steps |
| `docs_check.py` (pinned renderer) | 0 | 0 findings, 210 md + 1420 scrubbed files |
| `gen_toc.py --check` / `--verify-anchors` (pinned) | 0 / 0 | 149 pages / 538 fragment links |
| `check_em_dash.py --base origin/dev` (pinned; origin/dev `97aab1d0`) | 0 | 0 findings over 539 added lines in 9 pages |
| `check_em_dash.py --base e76a755a` (pinned) | 0 | 0 findings over 525 added lines in 5 pages |
| `check_doc_style.py` (pinned) | 0 | 23 documents OK |
| `check_doc_paths.py` (pinned) | 0 | 1065 cited paths resolve |
| `python3 -B scripts/check_py_idiom.py` | 0 | every ratchet holds |
| `python3 -B scripts/check_feature_status.py` and `--self-test` | 0, 0 | 0 findings; 46/46 |
| `torture_campaign.py --coverage-by-area --areas soak,audio,power` | 0 | three areas complete (`"missing": {}`) |
| `torture_campaign.py --plan --areas soak,audio,power --json` | 0 | `plan.json` |
| `git diff --check origin/dev HEAD`; `git diff --check`; porcelain | 0, 0, 0 | clean; porcelain empty |

All but the driver come from `scripts/run_head_gates.sh` (absolute paths) at the checked-out head (`head.txt`).

## Acceptance status (issue #396)

Unchanged from rounds 1 to 7. Items 1, 2 and 5 are met at the desk, and so is the desk half of item 4. Items 3 and 4
need the bench (part B), so the PR body says "Relates to #396".

## Open items and risks

- The two kept qualifiers ("the bytes show", the void exception) are not in the ruling's words; they were at the head
  the STOP ruling sent to review, and without them the rule is false at pinned cases. Flagged publicly.
- S1 not adopted: under coverage no property check can see #295; the pin does.
- S2 not adopted: the masked allowance stays wide; a void blocks the release.
- The fuzz and the census are seeded samples.
- Part-B routing unchanged: REBOOT and sine limits (issuecomment-6409128703), `restore_bound_s = 30`.
- Ignored `__pycache__` directories in the worktree date from 2026-10-26, before this round, and were left alone.
- Scratch outside the tree: `/tmp` exports, the packet extraction and the sweep dumps.

## Receipts

`receipts/INDEX.md` is generated from the files present (name, bytes, SHA-256) by `scripts/make_index.py`;
`receipts/rc.txt` lists every recorded return code.
