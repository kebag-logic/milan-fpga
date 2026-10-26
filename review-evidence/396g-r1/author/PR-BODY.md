[A674]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN at the desk: planner self-test 94/94, release mutation controls 192/192 killed,
behave 452 scenarios (plan feature 133), every documentation gate rc 0.
`396-release-gate-plan` -> `dev`, one commit on dev `e76a755a`.
The bench runs (acceptance items 3 and 4) are #396 part B and remain open.

## Linked Issue / roles

Relates to #396

This is part A of #396 (the plan, the assertion contract and the documents).
Acceptance items 3 and 4 need the bench, so this PR must not close the Issue.

Executor: `[A674]`
Internal cleared-context reviewer: assigned by the manager
External reviewer: assigned by the manager

## Description

The [owner decisions of 2026-10-26](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-6408072465)
replace the seven-day soak and the 160/40 cold-cut mix that PR #586 merged.
This PR applies them to the plan, its offline graders and the documents.

| Piece | Change |
|---|---|
| `soak` | 24 h by default (`--soak-duration-s 86400`), interval 60 s. Zero `SEQ_NUM_MISMATCH`, `STREAM_INTERRUPTED`, `LATE_TIMESTAMP` and `EARLY_TIMESTAMP` growth on every Stream Input, CRF included. Zero `MEDIA_UNLOCKED` growth outside a recorded planted event, explained or not. New oracle `check_release_soak_counters`. The merged `mr`/`tu`, `asCapable`, `AVTPRX_TSD` and uptime rules are unchanged. |
| `audio` | The existing identity area gains `audio.integrity`, the [2026-10-04 signal design](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5978644444) run inside the soak window. It puts a bit-exact counter on every digital path and every bound AAF channel, in both directions. New grader `grade_audio_counter_capture` classifies each event at its sample: n dropped, n repeated, n samples of silence (replaced or inserted), a bit-flip mask, or a channel swap. Planted drop, repeat and flip arms at both ends: a missed arm voids the run. Capture-side losses are attributed apart. Each event carries wall and gPTP times, capture index, words, and a context window for the counter, SLIP and gPTP walks. The analog sine pair (997 Hz, 9,973 Hz) is planned, with its limits undecided. |
| `power` | 200 cycles: `power.idle` 100 and `power.journal_commit` 50 cold cuts, and `power.soft_reset` 50 resets with power held on. A soft reset's T0 is its host-timestamped reset command. Every cycle restores the eight Milan items of #70's inventory and the binding, as data (`RELEASE_PERSISTED_ITEMS`). New oracle `check_release_state_restored` refuses a pre-cycle value equal to its default (#70's vacuity trap). The ADP, automatic-restore and #75 reconnect bounds are unchanged. |
| Negative controls | `power.control.first-boot-restart` (#366) must fail `power.single-boot`. `power.control.persistence-disabled` must fail `power.state-restored`. `audio.control.planted-drop` must fail `audio.zero-dut-glitches` and classify the drop exactly, graded offline on a synthetic capture. `run_release_control` runs each desk fixture through its oracle. |
| Audit | The per-area audit refuses a missing index, direction or CRF sink in any release repeat. It also refuses a dropped or downgraded required assertion, a missing phase, a cycle mix that does not sum to the total, and a missing control. The audio identity audit excludes the release steps so that they cannot mask an index-0-only identity loop. |
| Docs | REQ-VER-06 and REQ-VER-05's blocker sentence; CONTRIBUTING section 3 gains the gate for release PRs; TESTING 6d documents the inputs, verdicts, controls and retention per 6b; the README roadmap reads 24 h; the persistence design's restated numbers follow. |

Counter layout: S32 words, with the 24-bit sample in bits 31:8 and bits 7:0 zero (the #451 and #629 layout).
Sample bits 15:12 carry the channel index plus one, and bits 11:0 a sample counter modulo 4096.
Eight channels peak near -47 dBFS, and the wrap is an 11.7 Hz sawtooth at 48 kHz.
Slips are decided modulo 4096: a shift of 2048 or more aliases, and an exact multiple of 4096 is invisible.
The grader reads headerless interleaved S32 in either byte order, the format `tb/tools/thdn.py` and the #451 capture use.
It streams a 24-hour file in chunks; the clean fast path grades about 36 capture-minutes per second.

## Authoritative references

- #396 owner decisions issuecomment-6408072465; assignment issuecomment-6408079016;
  audio design issuecomment-5978644444; `mr`/`tu` rule issuecomment-5857765949 (unchanged).
- Milan v1.2 5.3.8.10 with Table 5.6 (counters, reset on not-bound to bound); 5.3.5.1, 5.3.7.1,
  5.3.7.6, 5.3.8.1-5.3.8.3, 5.3.8.7, 5.3.9.1, 5.3.10.1, 5.3.11.1, 5.3.13 (saved state);
  5.5.1.4 ("a power cycle or a simple reset"); 5.5.2.4/5.5.2.6; 5.6.2/5.6.3; Annex B.1.1.
- IEEE 1722-2016 4.4.4.3, 4.4.4.6, 4.4.4.7, 7.3.5. IEEE 1722.1-2021 6.2.2.5, 7.4.43.
- REQUIREMENTS.md section 8; CONTRIBUTING.md section 3; docs/testing/TESTING.md sections 6, 6b, 6d;
  docs/testing/methodology.md (R2: every new check ships a control that fails it).

## How to get into the same state

```sh
git fetch origin
git switch 396-release-gate-plan
git submodule update --init protocol-processor gptp-processor
python3 -m pip install behave
python3 -m pip install -r tools/markdown/requirements.txt
```

## How to validate

```sh
python3 -B tb/tools/torture_campaign.py --self-test
python3 -B tb/tools/torture_release_mutants.py
python3 -B tb/tools/torture_campaign.py --coverage-by-area --areas soak,audio,power
python3 -B tb/tools/torture_campaign.py --plan --areas soak,audio,power --json
cd tests && behave --no-capture -f plain && cd ..
python3 -B scripts/docs_check.py
python3 -B scripts/gen_toc.py --check
python3 -B scripts/gen_toc.py --verify-anchors
python3 -B scripts/check_em_dash.py --base origin/dev
python3 -B scripts/check_doc_style.py
python3 -B scripts/check_doc_paths.py
python3 -B scripts/check_py_idiom.py
git diff --check origin/dev HEAD
```

Expected result / pass criteria: every command exits 0. The self-test runs 94 tests OK.
The mutation driver prints `PASS: 192 mutations killed; source unchanged`.
Behave reports 452 scenarios passed, the plan feature 133.
The coverage audit reports `soak`, `audio` and `power` complete.
The docs gates report zero findings.

## Known limitations / out of scope

- The bench runs on the shipping image, and the two power controls on their known-defect images,
  are #396 part B (acceptance items 3 and 4). Nothing here touches hardware.
- No limit is decided yet for the analog sine pair's THD+N or predictor residual.
  `audio.analog-sine-pair` stays NOT RUN, so no release can qualify, until a recorded decision sets them.
- `restore_bound_s = 30` stays provisional, pending ratification from #397 and #75.
- The soft-reset mechanism is bench-declared and recorded per cycle; AECP REBOOT is not
  implemented by the processor and cannot serve.
- The counter cannot see slips that are exact multiples of 4096 samples. The soak's sequence and
  interruption counters remain the check for those.
- No firmware, RTL, builder or submodule change.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (part A: items 1, 2, 5 and the desk half of 4; items 3 and 4 open)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
