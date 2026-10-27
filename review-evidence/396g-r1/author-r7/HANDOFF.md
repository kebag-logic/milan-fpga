# HANDOFF: #396 part A round 7 (release gate plan), executor [A674g]

Status: **STOP** (one decision) at `5fdabc1c4c76206bd2528435c56d88466c0f972e`, branch `396-release-gate-plan`.
Two round-7 commits sit on the round-6 head `b206d88b937257ca5ccf1753c5fa211605c9f7e6`, which is not rewritten.
Base dev is `e76a755afc0536453161e3cd33f6f4d2dcd7641f`. Nothing is pushed, and no PR operation ran.

- Round-7 assignment: #396 issuecomment-6435672624. Findings answered: R699-6 (PR #786 issuecomment-6435666218) F1
  (MINOR), suggestions S1 to S3. TAKEN: issuecomment-6438013421. STOP: issuecomment-6442469554 (text in `STOP-COMMENT.md`).
- Remote checked: `origin` is `https://github.com/kebag-logic/milan-fpga.git`; the branch descends from `e76a755a`.
  No git command ran inside a submodule; the gitlinks are unchanged (`receipts/gates/head.txt`). No RTL, firmware,
  builder, hardware, bench or flashing action ran.
- R699-6 packet: `origin/396g-review-evidence` (`e12f487b`), `review-evidence/396g-r1/reviews/R699-6/`, extracted to
  `r699-6-packet/`. Manifest check: `receipts/r699-6_manifest_check.log`. All 7 scripts are OK. `venv_install.log`
  differs from its manifest line because the packet redacted a path in a pip notice. Two files over 200 KB were
  removed (`receipts/r699-6_packet_removed_over_200k.txt`). Its probe scripts ran unchanged at the new head.
- Commits, one line each, with no body and no trailer:
  - `73be3b36`: `List a constant-mask excursion that a slip interrupts from its first word, and pin it with its control
    (#396)`;
  - `5fdabc1c`: `Bound each audio listing from 63 samples before its event's first word to 63 after its last, check
    each listing, and fuzz events inside excursions on both capture lengths (#396)`.

## Why STOP

The ruling's item 1 gives this bound, outside the scope: "each listing falls at or after the event's first word and
no later than 63 samples after its last word". The upper edge is implemented as written. The lower edge cannot be
written as a true sentence without changing swept listings, which is the round's STOP condition:

- **Inside the scope**: 8 cases of `test_audio_composition_sweep` are listed one sample before the event's word.
  Each is a one-word corruption under `0x1E00` on a drop arm's next sample (7493 at 8192 frames, 15685 at 16384, every
  channel pair). It reads first, at the arm's sample, which is the stated limit "the bytes are the same either way".
  `_sweep_case` (`tb/tools/torture_campaign.py:9169`) checks that reading
  (`receipts/round7/sweep_listing_bounds_5fdabc1c.json`; the same at `b206d88b`).
- **Outside the scope**: the gate's own seeds break it. Arm-led seed 14 at 16384 frames is a DUT repeat of 1024 at
  699 beside the flip arm, listed at 698 on channel 1. Nested seed 16 is two whole-block slips seven samples apart,
  read as one slip of their sum at 5651, one sample before the second. Over 10,000 seeds per family and capture
  length, the literal edge refuses 30 and 34 compositions (arm-led, 16384 and 8192 frames) and 60 and 51 (nested). The
  head's gate passes every one of them (`receipts/round7/literal_*.json`). The refused listings are 1 to 5 samples early,
  each within 64 samples of another event or a planted arm (`receipts/round7/early_*.json`).

So the head writes the lower edge as round 6's, "no earlier than 63 samples before the event's first word". Accepting
that wording makes the head review-ready as it stands. Insisting on the literal edge needs a grader change that
moves swept listings, which needs a new ruling.

## How the ruling was applied

1. **Property, scoped.** For every capture: a DUT event the bytes show never grades PASS, and each is listed on each
   channel it changes, unless it masks a planted arm at its sample and the run is void. A listing's samples are its
   words, and for a slip the samples `located_within` names as well. Each listing falls no earlier than 63 samples
   before the event's first word (the open point) and no later than 63 after its last. Inside the exactness scope,
   each also falls within 63 samples of the event's first word. Narrowed in REQ-VER-06, TESTING 6d,
   `AUDIO_COUNTER_LIMITS[0]`, `audio.counter-classified` and the PR body.
2. **Gate.** The fuzz asserts the bound per event and channel, measured from the event's words. Where a run fails
   without voiding, it also asserts that every DUT listing falls so near an event that changes its channel. A nested
   family puts DUT events, mostly slips, inside a constant-mask excursion at both capture lengths. Controls #296 and
   #297 list a corruption after its last word plus 63, and the gate kills both.
3. **The reviewer's case.** It is pinned, and the first option is taken because it is contained. The grader lost the
   interrupted excursion's bit-flip when the hold re-read the window, and now keeps it. Every swept case is unchanged.
4. **Suggestions.** S1: adopted through the bound, plus an oracle order fix found by the nested family. S2: not
   adopted. S3: adopted in the PR body.

STOP condition (a swept case changes its grade or its listing): **not met**. `scripts/dump_sweeps.py` records every
capture of both in-tree sweeps (445): verdict, missed arms, reason and full event list. The output is byte-identical
at `b206d88b` and `5fdabc1c`, digest `5f0b7f1203866f8e…` (`receipts/round7/sweeps_*.digest.json`,
`sweeps_compare.log`; the 4.6 MB dumps stay out of this directory).

## Changes (file:line at `5fdabc1c`; `tb/tools/torture_campaign.py` unless named)

| Change | Where | Reason |
|---|---|---|
| `_close` keeps `_returned`'s bit-flip apart from the events a hold reads again, and records it first; docstring says why | `:4852`-`:4857`, `:4874`, `:4884`, `:4888` | F1: `_split`'s re-read (`:4829`) replaced the events before the hold with a read of the window's words, which do not hold that bit-flip |
| Interrupted-excursion limit: listed from its first word, one bit-flip up to the slip where held | `counter_limits` `:3809`; `docs/testing/TESTING.md:1457`-`:1458` | F1, option 1 |
| Pin `test_audio_excursion_a_slip_interrupts_is_listed_from_its_first_word` | `:9570` | Ruling item 3 |
| Third pinned shape in TESTING 6d | `docs/testing/TESTING.md:1525`, `:1532`-`:1535` | Ruling item 3 |
| Property text: listed on each channel; the listing bound; inside the scope within 63 of the first word | `REQUIREMENTS.md:409`-`:411`, `:416`; `docs/testing/TESTING.md:1487`-`:1501`; `counter_limits` `:3750`; `audio.counter-classified` `:3338` | Ruling item 1 (lower edge: the open point) |
| `_FUZZ_NESTED`, `_fuzz_nested` | `:9368`, `:9415` | Ruling item 2: the generator reaches a slip inside a constant-mask excursion, at both capture lengths |
| `_fuzz_reach` measures from the event's words, first to last | `:9433` | Ruling item 2; S1 |
| `_fuzz_check`: `reaches`, the per-event bound, the cancellation rebuild in the composition's order, the each-listing check in a run that fails without voiding; docstring | `:9456`-`:9500` (`:9474`, `:9493`, `:9498`) | Ruling item 2 ("each listing"); the order fix answers nested seed 3468, an oracle artefact |
| Gate test: docstring; nested loop over 8192 and 16384 frames | `:9502`, `:9531` | Ruling item 2 |
| TESTING gate paragraph: the nested family and the each-listing check | `docs/testing/TESTING.md:1508`-`:1513` | Ruling item 2 |
| Three controls | `tb/tools/torture_release_audio_mutants.py:27`, `:223`-`:231` | Each new check has a planted defect |
| PR body Round 7; S3's dated figure | `PR-BODY.md` | Ruling item 1; S3 |

## New checks, planted defects and failing words

`receipts/round7/quick_named_mutants.log` (each named arm alone, on the `5fdabc1c` export):

| Arm | Planted defect (control #) | First failing words |
|---|---|---|
| `test_audio_excursion_a_slip_interrupts_is_listed_from_its_first_word` `:9570` | a returned excursion's bit-flip left for the hold to read again (#295) | `AssertionError: Tuples differ: (0, 6097, 'dropped', 1021, '') != (0, 4424, 'bit-flip', 1673, '0x00080100')` |
| `test_audio_compositions_never_pass_and_list_every_event` `:9502`, per-event bound | a corruption of two or more words listed after its last word plus 63 (#296) | at the head: `seed=0: Lists differ: [{'capture_index': 376, 'class': 'swap', …}] != [] … a DUT listing reaches no DUT event`; without the each-listing half: `seed=1: … ('a DUT event is not listed', 'run', 501, 3, 'FAIL', …` (`quick_296_without_each_listing.log`) |
| same, each-listing half | a corruption of two or more words listed again after its last word plus 63 (#297) | `seed=0: Lists differ: [{'capture_index': 376, 'class': 'swap', …}] != [] … a DUT listing reaches no DUT event` |

The pin, transplanted onto `b206d88b`'s planner, fails with `- (0, 6097, 'dropped', 1021, '')` /
`+ (0, 4424, 'bit-flip', 1673, '0x00080100')` and passes at the head (`receipts/round7/transplant_pin_onto_b206d88b.log`).
Control #295 is killed by the pin alone: no sweep sees it (`receipts/r699-6_probes/mutants_all.json`). The round-6
fuzz controls #290 to #292 are still killed by the fuzz at the same seeds (1, 146, 12), since the arm-led generator
is unchanged.

## Evidence at `5fdabc1c` (R699-6's scripts unchanged; `receipts/r699-6_probes/`)

| Probe | Result | vs `b206d88b` / R699-6 |
|---|---|---|
| `probe_gap.py` 16384 | 6,720 cases, `gap_over_63` 0, max gap 1 (a slip at the excursion's first word) | 48, max 3,947 (byte-identical to R699-6's receipt at `b206d88b`) |
| `probe_fuzz.py` 8192, 2,000,000-2,019,999 | 0 violations; FAIL 11,756, NOT RUN 8,242, PASS 2 | 2 violations (2007597, 2017152) |
| `probe_fuzz.py` 16384, 1,000,000-1,039,999 | 0 violations | byte-identical to R699-6's receipt |
| `probe_fuzz.py` 16384, 0-287 | 0 violations | byte-identical |
| `probe_seed.py` 8192 2007597, 2017152 | both pass the check; 2007597 listed from 4424 | both violated |
| `probe_case.py` F1 case, no-slip control | channel 0 first `bit-flip 1673 0x00080100` at 4424; control one `bit-flip 1726` | first `dropped 1021` at 6097; control unchanged |
| `probe_isolated.py` 16384 0-39,999; 8192 500,000-519,999 | 0 violations | byte-identical to R699-6's receipts |
| `probe_mutants.py`, all 297 controls, 6 jobs | 297 killed, slowest 352 s | — |

Round-7 measurements (`receipts/round7/`; scripts in `scripts/`):

- `interrupted_reading_*`: the grid's channel-0 readings. At the head every interrupted excursion is first listed at
  its first word. The 48 late cases now read as one bit-flip up to the slip, and no other case's reading changes.
- `interrupted_first_word_*`: nested compositions away from the arms whose inside events are all slips (2,858 at
  16384 frames, 2,602 at 8192). Every one is listed at the excursion's first word.
- `nested_10k_*`: the nested family, 10,000 seeds per length: 0 violations, 0 late.
  `nested_gate_seeds_*_at_b206d88b`, `nested_5k_16384_at_b206d88b`: the family graded by `b206d88b`'s grader. A slip
  lies inside the excursion in 62 of the 96 gate compositions. None of the 96 is late there; 15 of 5,000 are.
- `phantom_*`: 10,000 seeds per family and length. No run that fails without voiding has a listing near no event.
  Void runs have them (1,929, 1,916, 232, 467): a missed arm's records.
- `literal_*`, `early_*`: the ruling's literal lower edge (Why STOP).
- `trace_f1_*`: channel 0's window closes, holds and records for F1's case at both heads.

## Gate table (exact head `5fdabc1c`, never piped; `receipts/gates/`)

| Command | rc | Result |
|---|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | 0 | 120 tests OK (`selftest.log`) |
| `python3 -B tb/tools/torture_release_mutants.py` (background, on the `5fdabc1c` export, polled) | 0 | `PASS: 297 mutations killed; source unchanged`, 10:06 to 12:57 UTC, 2 h 51 min on a shared host (`release_mutants.log`, `.start`, `.end`, `.export_sha256.txt`) |
| R699-6's `probe_mutants.py`, all 297 controls, 6 jobs (the driver's criterion, 1200 s) | 0 | 297 killed (`../r699-6_probes/mutants_all.json`) |
| `cd tests && behave --no-capture -f plain` (rtl-fast bdd-conformance) | 0 | 14 features, 495 scenarios, 2286 steps (`bdd_conformance.summary.txt`; the full log is hashed there) |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | 0 | 176 scenarios, 665 steps |
| `docs_check.py` (pinned renderer) | 0 | 0 findings, 210 md + 1420 scrubbed files |
| `gen_toc.py --check` / `--verify-anchors` (pinned) | 0 / 0 | 149 pages / 538 fragment links |
| `check_em_dash.py --base origin/dev` (pinned; origin/dev is `97aab1d0`) | 0 | 0 findings over 536 added lines in 9 pages |
| `check_em_dash.py --base e76a755a` (pinned) | 0 | 0 findings over 522 added lines in 5 pages |
| `check_doc_style.py` (pinned) | 0 | 23 documents OK |
| `check_doc_paths.py` (pinned) | 0 | 1065 cited paths resolve |
| `python3 -B scripts/check_py_idiom.py` | 0 | every ratchet holds |
| `python3 -B scripts/check_feature_status.py` and `--self-test` | 0, 0 | 0 findings |
| `torture_campaign.py --coverage-by-area --areas soak,audio,power` | 0 | three areas complete (`"missing": {}`) |
| `torture_campaign.py --plan --areas soak,audio,power --json` | 0 | `plan.json` |
| `git diff --check origin/dev HEAD`; `git diff --check`; porcelain | 0, 0, 0 | clean; porcelain empty |

All but the two control runs come from `scripts/run_head_gates.sh` at the checked-out head (`head.txt`), with
`PYTHONDONTWRITEBYTECODE=1` or `-B`.

## Acceptance status (issue #396)

Unchanged from rounds 1 to 6. Items 1, 2 and 5 are met at the desk, and so is the desk half of item 4. Items 3 and 4
need the bench (part B), so the PR body says "Relates to #396".

## Open items and risks

- The listing bound's lower edge (Why STOP) needs a manager decision.
- S2 not adopted: the masked allowance still excuses an unlisted event whenever a missed arm lies within its span
  ±2 on its channel. A void blocks the release.
- The fuzz is a seeded sample: 384 compositions per self-test, and 20,000 per family checked offline this round.
- The nested family reaches R699-6's late-listing mechanism rarely (none of its 96; 15 of 5,000 at `b206d88b`). The
  pin is what fails on that mechanism.
- The each-listing check applies only to runs that fail without voiding.
- Owner decision issuecomment-6409128703 (AECP REBOOT for the soft resets; sine-pair limits at baseline + 6 dB) is
  still not in the plan text, for the manager to route. `restore_bound_s = 30` stays provisional.
- A first start of `run_head_gates.sh` used relative receipt paths. It was stopped by PID within seconds, and wrote
  nothing into the tree (its writes failed); it was restarted with absolute paths. Ignored `__pycache__` directories
  in the worktree date from 2026-10-26, before this round, and were left alone.
- Scratch outside the tree: `/tmp` exports and copies of this session.

## Receipts

`receipts/INDEX.md` is generated from the files present (name, bytes, SHA-256) by `scripts/make_index.py`.
`receipts/rc.txt` lists every recorded return code; all are 0.
