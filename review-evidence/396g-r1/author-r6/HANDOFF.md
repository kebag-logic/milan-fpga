# HANDOFF: #396 part A round 6 (release gate plan), executor [A674f]

Status: **REVIEW READY** at `b206d88b937257ca5ccf1753c5fa211605c9f7e6`, branch `396-release-gate-plan`.
Three round-6 commits sit on the round-5 head `910d4b94c4d5334b1869f42e9653c308a15d0dba`, which is not rewritten.
Base dev is `e76a755afc0536453161e3cd33f6f4d2dcd7641f`. Nothing is pushed, and no PR operation ran.

- Round-6 assignment: #396 issuecomment-6432123822. Findings answered: R699-5 (PR #786 issuecomment-6432113562)
  H1 and H2 (MINOR), residue R1, suggestions S1 to S3.
- TAKEN: issuecomment-6432424300. REVIEW READY: issuecomment-6434987923.
- Remote checked: `origin` is `https://github.com/kebag-logic/milan-fpga.git`; the branch descends from `e76a755a`.
  No git command ran inside a submodule; the gitlinks are unchanged (`receipts/gates/head.txt`). No RTL, firmware,
  builder, hardware, bench or flashing action ran.
- R699-5's six probe scripts were run from its published packet after a sha256 check against its `MANIFEST.sha256`
  (6 of 6 OK; the bytecode file the manifest lists is not published).
- Commits, one line, no body, no trailer:
  - `6c9d566d`: `Claim for every audio capture that a DUT event never grades PASS and is listed, gate it by a seeded
    composition fuzz, scope exact classes to the swept shapes and pin two shapes outside them (#396)`;
  - `9c20c08e`: `Give each release control 1200 seconds before a timeout counts as no kill (#396)` (S1, one line);
  - `b206d88b`: `State that the slip-before sweep's masks make no channel number zero or another channel's, and that
    each event is listed on each channel it changes (#396)` (two wording errors found on re-reading `6c9d566d`).
- The first control runs at `9c20c08e` were stopped by hand for the `b206d88b` wording fix (it changes a
  `counter_limits` string). Their partial logs are in `receipts/stopped_9c20c08e/`; both runs were restarted at
  `b206d88b`.

## How the ruling was applied

1. **Property with an exactness scope.** For every capture: a DUT event the bytes show never grades PASS, and each is
   listed within 63 samples of its sample on each channel it changes. The one exception is an event that masks a planted
   arm at its sample: the run is then void, and the reason says so (S3). Events that cancel, or only move an arm within
   its tolerance, leave a clean run's bytes. Exact classification is claimed only for: one event with at least 64 clean
   samples between it and every other event and arm (except an excursion whose mask clears its channel number); the
   composition sweep's one-word corruptions; the slip-before sweep. Everything else fails or voids and may read
   otherwise. Each exhaustive sentence the ruling names is narrowed (table below).
   - Interpretation, published in the PR body: the scope includes one event away from the arms, classified by rules 1
     to 4 and the limits, each pinned by an arm. No sweep covers it; dropping it would withdraw the plan's per-event
     claim. R699-5's isolated fuzz finds nothing there beyond the stated neighbour-word limit and H1's spanning runs.
   - Why 63 samples and not "at its sample": outside the scope a reading may place an event elsewhere in its window. A
     slip of whole blocks can show up to 63 samples after it happened, and an adjacent event bounds its
     `located_within`. Measured on the prototype at `910d4b94` over 100,000 compositions: distances 1 to 59 occur, never
     more.
2. **The gate.** `test_audio_compositions_never_pass_and_list_every_event`, a seeded fuzz (288 compositions) that
   asserts the property only. Three controls make a composition PASS or drop an event from the list; the fuzz kills
   each. Its oracle needs three allowances (a moved arm, cancelling events, a masked arm), each pinned once.
3. **H1 and H2**, second option: stated outside the scope, one example each pinned. The first option would add a
   reading per shape, which the ruling closes.
4. **S1**, one line: `timeout=600` to `timeout=1200` for each control's self-test.

STOP condition (any swept case changes its grade): **not met**. No reading changes; the void reason's text is the
only behavioural change. R699-5's probes at `b206d88b` give logs identical to `910d4b94` apart from three void reasons
in their new wording (`receipts/r699-5/compare_910d4b94_b206d88b.log`), and the `910d4b94` logs are byte-identical to
R699-5's published receipts (`receipts/r699-5/base_vs_reviewer_receipts.log`). R699-4's `r4_net_sweep` and `r4_arm_corruption_sweep`, run unchanged at `b206d88b`, are byte-identical to R699-5's runs at `910d4b94` (`receipts/r699-4_sweeps_b206d88b/compare.log`). The in-tree sweeps pass.

## Changes (file:line at `b206d88b`; `tb/tools/torture_campaign.py` unless named)

| Change | Where | Reason |
|---|---|---|
| `AUDIO_ARM_MISSED_REASON`, naming a DUT event at the arm's sample as a possible cause; returned for a missed arm | `:3725`, `:5295` | S3; ruling item 1 ("the void reason says a DUT event may be the cause") |
| Property and scope entries in `counter_limits`; "inside the scope" on the slip, void and excursion entries; two out-of-scope entries; "never an unbalanced slip" | `AUDIO_COUNTER_LIMITS` `:3747`-`:3803` (`:3748`, `:3752`, `:3757`, `:3760`, `:3787`, `:3795`, `:3800`, `:3802`) | Items 1 and 3; R1 |
| `audio.counter-classified`: property, scope, out-of-scope compositions; `audio.planted-arms-found`: a DUT event on or beside an arm, the reason | `:3338`, `:3364` | Item 1; H1 |
| `_read` docstring: "never adds a DUT event"; the readings tried are not every reading | `:4669`-`:4684` | H1 (the reading-choice guarantee) |
| `_unbalanced` docstring and the balance arm's docstring: "never an unbalanced slip" | `:4897`, `:9259` | R1 |
| Composition sweep's void cases compare the reason constant | `:9229` | S3 |
| Property fuzz: sizes and seeds, unit maker, composer, reach, clean-run words, check, arm | `:9354`-`:9488` | Item 2 |
| H1 pin; H2 pin | `:9489`, `:9507` | Item 3 |
| REQ-VER-06 audio block | `REQUIREMENTS.md:408`-`:425` | Item 1; H1, H2, R1 |
| TESTING 6d: zero-word line; rule 4; "either order" scoped; R1; reading choice; void list scoped to one word; property and scope paragraph | `docs/testing/TESTING.md:1294`, `:1341`-`:1343`, `:1350`, `:1374`, `:1377`-`:1383`, `:1466`-`:1478`, `:1485`-`:1518` | Items 1 and 3; H1, H2, R1 |
| behave step reads the reason constant | `tests/steps/torture_release_steps.py:606` | S3 |
| Five controls; one re-anchored | `tb/tools/torture_release_audio_mutants.py:24`-`:26`, `:205`-`:222`; `tb/tools/torture_release_mutants.py:761`-`:762` | Each new arm has a planted defect; the missed-arm line now returns the constant |
| Per-control timeout 1200 s | `tb/tools/torture_release_mutants.py:909` | S1 |

## New checks, planted defects and failing words

`receipts/round6/quick_named_mutants.log` (named arm alone, on the `b206d88b` export) and
`receipts/round6/mutant_seeds.log` (the composition each fuzz control mis-grades):

| Arm | Planted defect (control #) | First failing words |
|---|---|---|
| `test_audio_compositions_never_pass_and_list_every_event` `:9461` | a DUT event inside a found arm's tolerance taken as the arm (#289) | `AssertionError: seed=1: False is not true : ('a DUT event passed', ...` (a 67-word excursion beside the repeat arm grades PASS) |
| same | a flip arm found in any corruption carrying its mask bit (#290) | `AssertionError: seed=146: False is not true : ('a DUT event passed', ...` (a two-word `0x100000` excursion over the flip arm grades PASS) |
| same | a slip arm found at its own sample whatever its size (#291) | `AssertionError: seed=12: False is not true : ('a DUT event is not listed', 'slip', 300, 0, 'NOT RUN', ...` |
| `test_audio_excursion_over_a_slip_arm_may_void` `:9489` | a missed arm's void reason without its possible DUT cause (#292) | `AssertionError: 'or a DUT event at its sample may have masked it' not found in 'void: a planted arm was missed'` |
| `test_audio_excursion_clearing_its_channel_number_is_split` `:9507` | a zero word after a stored word kept as data (#293) | `+  (0, 4096, 'bit-flip', 49, '0x00100000')]` |
| (re-anchored) `test_audio_grader_attribution` | missed arm accepted (#176) | `FAIL  : void: a planted arm was missed; the source may not have planted it, or a DUT event at its sample may have masked it` |

The full self-test kills #289 in `test_audio_arm_interplay_at_the_release_tolerance`,
`test_audio_planted_arms_beside_block_slips` and the fuzz. It kills #290 in the composition sweep and the fuzz, and
#291 in the composition sweep, `test_audio_grader_attribution` and the fuzz. The fuzz finds all three only after its
generator was weighted toward single events on an arm's own sample (scratch trial, recorded here, not a receipt).

Against the round-5 grader (`receipts/round6/transplant_round6_arms.log`: the three arms transplanted onto the
`910d4b94` planner, with the round-5 reason): the fuzz and the H2 pin pass, because they pin a property and a shape
that grader already met; the H1 pin fails on the reason.

Fuzz validation at `b206d88b` beyond the self-test (`scripts/fuzz_range.py`, the in-tree generator and check
unchanged): 70,000 seeds (288 to 70,287), 0 violations; 41,357 FAIL, 28,637 NOT RUN, 6 PASS (each byte-identical to a
clean run with each arm at its logged sample or where the grader found it); allowances: masked 267, cancelled 14; largest listing distance 62
(`receipts/round6/fuzz_range/summary.txt`).

## Gate table (exact head `b206d88b`, never piped; `receipts/gates/`)

| Command | rc | Result |
|---|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | 0 | 119 tests OK, 34.8 s under host load (`selftest.log`) |
| `python3 -B tb/tools/torture_release_mutants.py` (background, on the `b206d88b` export, polled) | 0 | `PASS: 294 mutations killed; source unchanged`, 2 h 43 min on a shared host (`release_mutants.log`, `.start`, `.end`) |
| R699-5's `parallel_mutants.py` on the `b206d88b` export, 8 jobs (the driver's kill rule and 600 s limit) | 0 | `PASS: 294 of 294 killed`; source unchanged; slowest #195 at 315 s (`parallel_mutants.log`) |
| `cd tests && behave --no-capture -f plain` (rtl-fast bdd-conformance) | 0 | 14 features, 495 scenarios, 2286 steps (`bdd_conformance.summary.txt`; the full log is hashed there) |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | 0 | 176 scenarios, 665 steps |
| `docs_check.py` (pinned renderer) | 0 | 0 findings, 210 md + 1420 scrubbed files |
| `gen_toc.py --check` / `--verify-anchors` (pinned) | 0 / 0 | 149 pages / 538 fragment links |
| `check_em_dash.py --base origin/dev` (pinned) | 0 | 0 findings over 510 added lines in 9 pages |
| `check_doc_style.py` (pinned) | 0 | 23 documents OK |
| `check_doc_paths.py` (pinned) | 0 | 1065 cited paths resolve |
| `python3 -B scripts/check_py_idiom.py` | 0 | every ratchet holds (514 modules) |
| `python3 -B scripts/check_feature_status.py` and `--self-test` | 0, 0 | 0 findings; 46/46 |
| `torture_campaign.py --coverage-by-area --areas soak,audio,power` | 0 | three areas complete (`"missing": {}`) |
| `torture_campaign.py --plan --areas soak,audio,power --json` | 0 | 17 steps (`plan.json`) |
| `git diff --check origin/dev HEAD`; `git diff --check`; porcelain | 0, 0, 0 | clean; porcelain empty |

All but the two control runs come from `scripts/run_head_gates.sh` at the checked-out head (`head.txt`).

The gates ran with `PYTHONDONTWRITEBYTECODE=1` or `-B`, so no bytecode was written into the tree.

## Acceptance status (issue #396)

Unchanged from rounds 1 to 5. Items 1, 2 and 5 are met at the desk, and so is the desk half of item 4. Items 3 and 4
need the bench (part B), so the PR body says "Relates to #396".

## Open items and risks

- H1 and H2 remain as behaviour, now stated outside the exactness scope; H1 still voids 3,848 of R699-5's 12,480
  grid cases, unchanged, and a void blocks the release.
- The property's listing tolerance is 63 samples, not "at its sample"; the ruling's wording is "listed at its
  sample". The PR body states the reason (outside the scope, a reading may place an event elsewhere in its window).
- The fuzz is a seeded sample (288 compositions per self-test, 70,000 more checked offline), not exhaustive.
- The scope includes single events away from the arms (interpretation above), pinned per rule, not swept.
- Owner decision issuecomment-6409128703 (AECP REBOOT for the soft resets; sine-pair limits at baseline + 6 dB) is
  still not in the plan text, for the manager to route. `restore_bound_s = 30` stays provisional.
- Scratch outside the tree: `/tmp` exports and mutant copies of this session; one stopped driver's temporary copy was
  removed. Older `release-controls-*` directories predate this session and were left alone.

## Receipts

`receipts/INDEX.md` is generated from the files present (name, bytes, SHA-256) by `scripts/make_index.py`.
`receipts/rc.txt` lists every recorded return code. Those that are not 0 are expected:
- R699-5's `r5_fuzz` exits 1 whenever a seed deviates. Isolated gives 77 and before gives 28, the same at `910d4b94`,
  `9c20c08e` and `b206d88b`, and in R699-5's own receipts.
- The parallel run stopped by hand at `9c20c08e` exits 1.
The scripts that produced receipts are in `scripts/`. `fuzz_before.log` (924,835 bytes) exceeds 200 KB at each head;
each is replaced by `fuzz_before.log.sha256.txt` after the comparisons were recorded.
