[A674g]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Round 7](#round-7)** — R699-6's finding, the listing bound that answers it, the one point of the ruling left for a decision, and the tests that prove each.
- **[Round 6](#round-6)** — Each R699-5 finding, the property and exactness scope that answer it, and the test that proves it.
- **[Round 5](#round-5)** — Each R699-4 finding, its fix or its stated exception, and the test that proves it.
- **[Round 4](#round-4)** — Each R699-3 finding, its fix and the test that proves it.
- **[Round 3](#round-3)** — Each R700-2 and R699-2 finding, its fix and the test that proves it.
- **[Round 2](#round-2)** — Each R699-1 and R700-1 finding, its fix and the test that proves it.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

STOPPED for one decision (Round 7: the listing bound's lower edge); otherwise green at the desk, head `5fdabc1c4c76206bd2528435c56d88466c0f972e`:

- planner self-test 120/120;
- release mutation controls 297/297 killed, each by its named arm, under a parallel runner with the driver's kill criterion and 1200-second limit and by the driver itself: `PASS: 297 mutations killed; source unchanged`, 2 h 51 min on a shared host;
- behave 495 scenarios, the plan feature 176;
- every documentation gate rc 0.

`396-release-gate-plan` -> `dev`: thirteen commits on dev `e76a755a`.
They are round 1 `21faa482`, round 2 `a3e24ac5`, round 3 `9da26126` and `4d69e192`, round 4 `85da3e45`, round 5 `4a460fc3`, `17a43ef2` and `910d4b94`, round 6 `6c9d566d`, `9c20c08e` and `b206d88b`, and round 7 `73be3b36` and `5fdabc1c`.
The bench runs (acceptance items 3 and 4) are #396 part B and remain open.

## Linked Issue / roles

Relates to #396

This is part A of #396 (the plan, the assertion contract and the documents).
Acceptance items 3 and 4 need the bench, so this PR must not close the Issue.

Executor: `[A674]` (round 1), `[A674b]` (round 2), `[A674c]` (round 3), `[A674d]` (round 4), `[A674e]` (round 5), `[A674f]` (round 6), `[A674g]` (round 7)
Internal cleared-context reviewer: `[R699]`
External reviewer: `[R700]`

## Description

The [owner decisions of 2026-10-26](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-6408072465)
replace the seven-day soak and the 160/40 cold-cut mix that PR #586 merged.
This PR applies them to the plan, its offline graders and the documents.

| Piece | Change |
|---|---|
| `soak` | 24 h by default (`--soak-duration-s 86400`), interval 60 s. Zero `SEQ_NUM_MISMATCH`, `STREAM_INTERRUPTED`, `LATE_TIMESTAMP` and `EARLY_TIMESTAMP` growth on every Stream Input, CRF included. Zero `MEDIA_UNLOCKED` growth outside a recorded planted event, explained or not. An increment is excused only between two reads inside the planted window, so the runner reads the input at the window's edges. Oracle `check_release_soak_counters`. The merged `mr`/`tu`, `asCapable`, `AVTPRX_TSD` and uptime rules are unchanged. |
| `audio` | The identity area gains `audio.integrity`, the [2026-10-04 signal design](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5978644444), run inside the soak window. A bit-exact counter rides on every digital path and every bound AAF channel, in both directions. The counter never repeats within a run (below). The grader `grade_audio_counter_capture` lists each event in a class: n dropped, n repeated, n samples of silence (replaced or inserted), a bit-flip mask, a channel swap, or an `unresolved` stretch at a capture's end. Each verdict states the qualified interval it proves. `PASS` needs 24 hours of observed samples in that interval. Planted drop, repeat and flip arms run in the first and the last tenth, inside the qualified interval; a missed arm voids the run. Every capture meets one property: a DUT event the bytes show never grades `PASS`, and each is listed on each channel it changes, unless it masks a planted arm and voids the run. Each listing falls no earlier than 63 samples before the event's first word and no later than 63 after its last; inside the exactness scope, within 63 samples of its first word. A seeded composition fuzz is the property's gate. Exact classification is claimed only inside a stated scope: one event away from the arms, and the compositions the two sweeps grade; any other composition fails or voids the run. On every channel the slips a reading reports sum to the shift the bytes decode; a window no reading balances is one `unresolved` event, never an unbalanced slip. Where the capture's bytes allow two readings, the planted-arm log decides at a logged arm, never at the cost of another DUT event; inside the scope, two shapes beside a planted arm void the run. Capture-side losses are attributed apart and advance the clocks, but are not observed time. Each event carries its capture and acquisition indices, its words, and anchored wall and gPTP times. The analog sine pair (997 Hz, 9,973 Hz) is planned, with its limits not yet set (below). |
| `power` | 200 cycles: `power.idle` 100 and `power.journal_commit` 50 cold cuts, and `power.soft_reset` 50 resets with power held on. A soft reset's T0 is its host-timestamped reset command. Every cycle restores the eight Milan items of #70's inventory and the binding, as data (`RELEASE_PERSISTED_ITEMS`). `check_release_state_restored` refuses a pre-cycle or pending value equal to its default. A commit cut passes only with a `ReleaseCommitCut` placing its cut inside the recorded commit window. The ADP, automatic-restore and #75 reconnect bounds are unchanged. |
| Negative controls | `power.control.first-boot-restart` (#366) must fail `power.single-boot`. `power.control.persistence-disabled` must fail `power.state-restored`. `audio.control.planted-drop` must fail `audio.zero-dut-glitches` and classify the drop exactly, graded offline on a synthetic capture. |
| Audit | The per-area audit refuses a missing index, direction or CRF sink in any release repeat. It also refuses a dropped or downgraded required assertion, a missing phase, a cycle mix that does not sum to the total, and a missing control. |
| Docs | REQ-VER-06 and REQ-VER-05's blocker sentence; CONTRIBUTING section 3's gate for release PRs; TESTING 6d's inputs, rules, limits, verdicts, controls and retention per 6b; the README roadmap (24 h); the persistence design's restated numbers. |

Counter layout: S32 words, with the 24-bit sample in bits 31:8 and bits 7:0 zero (the #451 and #629 layout).

| Sample bits | Content |
|---|---|
| 15:12 | The channel number, the channel index plus one |
| 11:1 | The absolute sample position `n`, modulo 2048 |
| 0 | Bit `n mod 32` of block `n div 2048`'s code, the block number times `0x9E3779B1` modulo 2^32 |

Thirty-two consecutive samples of one block give its number, so the counter repeats only after 2^43 samples.
That is about 530 days at 192 kHz, the highest Milan v1.2 6.2 (Table 6.1) rate; a 24-hour run is 1.66e10 samples there.
Eight channels peak near -47 dBFS, and the 2048-sample wrap is a 23.4 Hz sawtooth at 48 kHz.
The grader reads headerless interleaved S32 in either byte order and streams a 24-hour file in chunks.

## Round 7

Round 7 answers [R699-6](https://github.com/kebag-logic/milan-fpga/pull/786#issuecomment-6435666218), NEGATIVE at `b206d88b`.
It found one MINOR finding (F1) and three suggestions.
The [round-7 assignment](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-6435672624) scopes localisation the way round 6 scoped classification.
Two commits sit on `b206d88b`, which is not rewritten:

- `73be3b36` lists an excursion that a slip interrupts from its first word, with its pin and its control;
- `5fdabc1c` states the listing bound, gates it and adds two controls.

Rounds 1 to 6 are not rewritten.
The exceptions are where the ruling narrows this body's own claims: the `audio` row and Round 6 items 1 and 2. S3 dates one Round 5 figure.
Lines are at `5fdabc1c` in `tb/tools/torture_campaign.py` unless named.

**One point of the ruling is left for a decision.**
The ruling's bound, outside the scope, is that each listing falls at or after the event's first word and no later than 63 samples after its last word.
The upper edge is implemented as written.
The lower edge, "at or after the event's first word", is false at `b206d88b` and at this head, inside and outside the scope:

- Inside the scope, the composition sweep pins 8 cases that are listed one sample before the event's word.
  Each is a one-word corruption on a drop arm's next sample under mask `0x1E00`, which reads first, at the arm's sample.
  This is the stated limit "the bytes are the same either way", which `_sweep_case` (`:9169`) checks.
  Making the lower edge true would change those swept listings, which is the round's STOP condition.
- Outside the scope, the gate's own seeds break it.
  Seed 14 is a DUT repeat of 1024 at 699 beside the flip arm at 700, listed at 698 on channel 1.
  Nested seed 16 at 16384 frames is two slips of whole blocks seven samples apart, read as one slip of their sum one sample before the second.
- Over 10,000 seeds per family and capture length, the literal lower edge refuses 30 and 34 compositions of the arm-led family and 60 and 51 of the nested one, where this head's gate passes all of them (`receipts/round7/literal_*`).
  The refused listings are 1 to 5 samples early.
  Each lies within 64 samples of another event or a planted arm, where a stated limit reads the same bytes with the event earlier (`receipts/round7/early_*`).

This head therefore states the lower edge as "no earlier than 63 samples before the event's first word": round 6's bound, unchanged.
The upper edge is the ruling's.
Inside the scope, each listing also falls within 63 samples of the event's first word, as the ruling says.
The alternatives would be:

- a grader change that moves listings, which the STOP condition forbids for the swept cases;
- a lower edge of "the planted-arm tolerance or another event's reading before it", which no oracle here checks.

| Finding | Change | Test that proves it |
|---|---|---|
| F1 (MINOR): a constant-mask excursion that a DUT slip interrupts is listed only from the slip, up to 3,947 samples after its first word | Ruling item 3, the reviewer's first option, taken because it is contained. The cause: `_returned` (`:4650`) records the excursion's bit-flip from its first word, ahead of the window's own events. `_split`'s re-read (`:4829`) then replaced the events before the hold with a fresh read of the window's words, which do not include that bit-flip, so it was lost. `_close` (`:4852` docstring, `:4874`, `:4884`, `:4888`) now keeps the bit-flip apart from what the hold reads again, and records it first. The limit text says so: an interrupted excursion is listed from its first word, its words before the slip one `bit-flip` up to it where they are held as one mask (`docs/testing/TESTING.md:1457`-`:1458`; `counter_limits` `:3809`). Every swept case is unchanged (below) | `test_audio_excursion_a_slip_interrupts_is_listed_from_its_first_word` `:9570` pins R699-6's minimal case: `0x80100` over channel 0's words 4424 to 6149, with a DUT repeat of 3 at 6097. Alone, the excursion is one `bit-flip` of 1726 words. With the slip, channel 0 is listed first as a `bit-flip` of 1673 words at 4424; the other channels list the repeat at 6097; nothing is later than 63 samples after 6149. Transplanted onto `b206d88b` it fails, with channel 0 first listed as `dropped 1021` at 6097 (`receipts/round7/transplant_pin_onto_b206d88b.log`). Control #295 fails it. R699-6's `probe_gap.py`, unchanged: 0 of 6,720 cases more than 63 samples late (48 at `b206d88b`); the largest gap is 1, a slip at the excursion's first word. `probe_fuzz.py` at 8192 frames, seeds 2,000,000 to 2,019,999: 0 violations (2 at `b206d88b`). Seed 2007597 is listed from 4424 |
| S1 (SUGGESTION): measure each unit from the words it changes | Adopted through the bound. The gate measures each event from its words, first to last, so seed 2017152's listing at 2869 lies inside the 1,571-word excursion it reports. The nested family exposed one more oracle artefact of this kind. Nested seed 3468 has a copy that an excursion makes invisible. The cancellation allowance rebuilt the other units out of their order, so the swap after it no longer matched the bytes. The rebuild now keeps the composition's order (`:9493`) | `probe_seed.py` 2017152 at 8192 frames passes the check. The nested family at the new head: 0 violations over 10,000 seeds at each length (`receipts/round7/nested_10k_*`) |
| S2 (SUGGESTION): tie the masked allowance to the unit whose removal restores the arm | Not adopted. A void blocks the release, so the wider allowance hides no release defect. The round's change is the listing bound, and a tighter allowance would need its own check of compositions where two units mask one arm | — |
| S3 (SUGGESTION): a dated timeout figure | Adopted: Round 5 now reads "against the driver's 600 (1200 from `9c20c08e`)" | — |

The ruling's items:

1. **The property, scoped.**
   - For every capture: a DUT event the bytes show never grades `PASS`, and each is listed on each channel it changes, unless it masks a planted arm at its sample and the run is void.
   - A listing's samples are its words, and for a slip the samples `located_within` names as well.
     Each listing falls no earlier than 63 samples before the event's first word (the open decision above) and no later than 63 samples after its last.
   - Inside the exactness scope, each listing also falls within 63 samples of the event's first word.
   - The wording is in REQ-VER-06 (`REQUIREMENTS.md:409`-`:411`, `:416`), TESTING 6d (`docs/testing/TESTING.md:1487`-`:1501`), `counter_limits` (`:3750`) and the `audio.counter-classified` text (`:3338`).
2. **The gate.** `test_audio_compositions_never_pass_and_list_every_event` `:9502` asserts the bound for every composition.
   - `_fuzz_reach` (`:9433`) measures from the event's words, first to last; `_fuzz_check` (`:9456`) applies it per event and channel.
   - Where a run fails without voiding, every DUT listing must also fall so near an event that changes its channel (`:9474`, `:9498`).
     In a void run a missed arm's own records are DUT listings, so that half does not apply there.
     Over 10,000 seeds per family and capture length, no run that fails without voiding has a listing near no event (`receipts/round7/phantom_*`).
   - A nested family (`_fuzz_nested` `:9415`, 48 seeds per length at 8192 and 16384 frames, `:9531`) puts DUT events inside a constant-mask excursion.
     The excursion runs 64 to 2100 words anywhere, under one of the sweep's mask classes.
     It holds one or two DUT events, mostly slips, half of them less than 64 samples before its return.
     In its 96 compositions a slip lies inside the excursion in 62.
     R699-6's mechanism also needs particular masks and block positions.
     None of the 96 is listed late at `b206d88b`, and 15 of 5,000 are (`receipts/round7/nested_*_at_b206d88b.json`); the pin is the arm that fails there.
   - Controls, each failing the gate (`receipts/round7/quick_named_mutants.log`):
     - #296, a corruption of two or more words listed after its last word plus 63;
     - #297, the same corruption listed again after its last word plus 63, which only the each-listing half sees.
     Both fail at seed 0, a swap listed at 376 that reaches no DUT event.
     Without the each-listing half, #296 fails at seed 1: "a DUT event is not listed", a run at 501 on channel 3 (`receipts/round7/quick_296_without_each_listing.log`).
3. **The reviewer's case** is pinned, and the first option is taken (F1 above).

STOP condition (a swept case changes its grade or its listing): not met.
`scripts/dump_sweeps.py` grades every capture of both in-tree sweeps, 445 in all, with their four stated voids and the clean captures.
It records each capture's verdict, missed arms, reason and full event list.
The outputs at `b206d88b` and `5fdabc1c` are byte-identical, digest `5f0b7f12…` (`receipts/round7/sweeps_compare.log`).
R699-6's other probes, unchanged at this head, match its receipts byte for byte:

- `probe_isolated.py` at 16384 frames (40,000 seeds) and at 8192 (500,000 to 519,999);
- `probe_fuzz.py` at 16384 frames (1,000,000 to 1,039,999);
- `probe_fuzz.py` over the self-test's 288 seeds.

Three new controls (`tb/tools/torture_release_audio_mutants.py:27`, `:223`-`:231`); 297 in all.

## Round 6

Round 6 answers [R699-5](https://github.com/kebag-logic/milan-fpga/pull/786#issuecomment-6432113562), NEGATIVE at `910d4b94`.
It found two MINOR findings, one residue and three suggestions.
The [round-6 assignment](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-6432123822) closes the class by changing what is claimed, not by adding readings:

- the claim becomes a property, with an exactness scope;
- a seeded composition fuzz is the gate for the property;
- H1 and H2 are stated outside the scope, and one example of each is pinned.

Rounds 1 to 5 are not rewritten.
The exception is where the ruling narrows this body's own claims: the `audio` row, and Round 5's R1 row, G2 row and item 2.
Lines are at `b206d88b` in `tb/tools/torture_campaign.py` unless named.
No reading of the grader changes; its one behavioural change is the void reason's text.

| Finding | Change | Test that proves it |
|---|---|---|
| H1 (MINOR): a multi-word constant-mask excursion over a planted slip arm voids the run, outside the stated voids, although a reading of the bytes finds the arm | Ruling item 3, second option. The shape is stated outside the exactness scope and pinned; the reading choice is unchanged. The documents no longer say the grader tries every reading the bytes allow: the `_read` docstring (`:4669`, `:4678`), `docs/testing/TESTING.md:1378`-`:1383` and REQ-VER-06 (`REQUIREMENTS.md:422`-`:424`). The void list and its mask sentence are scoped to one corrupted word (`TESTING.md:1466`, `:1473`, `:1478`; `counter_limits` `:3787`). The shape is listed outside the scope (`TESTING.md:1511`-`:1515`; `counter_limits` `:3800`; `audio.planted-arms-found` `:3364`). The void reason names the possible DUT cause (S3) | `test_audio_excursion_over_a_slip_arm_may_void` `:9489` pins R699-5's worked example. `0x100` over channel 2's words 15934 to 15938, under the repeat arm, is NOT RUN with the new reason, with that arm missed and every DUT event listed at its sample. Transplanted onto the round-5 grader it fails on the reason. Control #292, the round-5 reason, fails it |
| H2 (MINOR): a constant-mask excursion whose mask clears the channel number is split at each all-zero word | Second option. The shape is stated outside the scope and pinned. Rule 4 (`TESTING.md:1341`-`:1343`) and the zero-word line (`:1294`: a corruption can still make a word zero, and it then reads as silence) are narrowed. So are REQ-VER-06 (`REQUIREMENTS.md:418`-`:419`), `counter_limits` (`:3795` and `:3802`), and this body's Round 5 G2 row and item 2 | `test_audio_excursion_clearing_its_channel_number_is_split` `:9507` pins R699-5's example: 65 words from 4080 under `0x100000` on channel 0. It checks from the bytes that the word at 4095 is zero, and pins the reading: a `bit-flip` of 15, one sample of `silence` at 4095, and a `bit-flip` of 49. It passes on the round-5 grader, since it pins that behaviour. Control #293, a zero word after a stored word kept as data, fails it |
| R1 (RESIDUE): an absolute "no slip that did not happen" sentence | As written: "So no unbalanced slip is ever reported." (`TESTING.md:1374`). The same narrowing is applied to `counter_limits` (`:3760`), the `_unbalanced` docstring (`:4897`), the balance arm's docstring (`:9259`) and this body's `audio` row | — |
| S1 (SUGGESTION): the driver's timeout margin under load | Adopted as the one-line change the ruling allows. A control's self-test may take 1200 seconds before a timeout counts as no kill (`tb/tools/torture_release_mutants.py:909`, `9c20c08e`). The pristine run keeps its 600 | The driver's own run at `b206d88b` (below) |
| S2 (SUGGESTION): widen the two sweeps | Not adopted as sweep cases. The ruling closes the class by narrowing the claim, and a wider sweep would need H1 and H2 read exactly. The property fuzz reaches both shapes, checking the property only. It covers channel-number-clearing masks, multi-word excursions over every arm, slips, silences, swaps and copies | `test_audio_compositions_never_pass_and_list_every_event` |
| S3 (SUGGESTION): name a possible DUT cause in the void reason | Adopted. `AUDIO_ARM_MISSED_REASON` (`:3725`, returned at `:5295`) reads "void: a planted arm was missed; the source may not have planted it, or a DUT event at its sample may have masked it" | The H1 pin; the composition sweep's void cases (`:9229`); behave `tests/steps/torture_release_steps.py:606` |

The ruling's items:

1. **The property and its scope.**
   - Property, for every capture: a capture with a DUT event the bytes show never grades `PASS`.
   - Each such event is listed on each channel it changes.
     Narrowed in Round 7: each listing falls no earlier than 63 samples before the event's first word and no later than 63 after its last, and inside the scope within 63 samples of its first word.
     Sixty-three samples is the furthest a slip of whole blocks can lie before the first word that shows it.
   - The one exception is a DUT event that masks a planted arm at its sample. The run is then void, and the reason names that cause.
   - Events that cancel one another, or only move an arm within its tolerance, leave a clean run's bytes.
   - Scope: exact classification is claimed only for three shapes.
     - One event with at least 64 clean samples between it and every other event and planted arm, except an excursion whose mask clears its channel number.
     - A one-word corruption 0 to 4 samples from a planted arm (the composition sweep).
     - A short slip before a constant-mask excursion whose mask makes no channel number zero or another channel's (the slip-before sweep).
   - Any other composition grades FAIL or void and may read in other classes.
   - The wording is in REQ-VER-06 (`REQUIREMENTS.md:408`-`:425`), TESTING 6d (`docs/testing/TESTING.md:1485`-`:1518`), `counter_limits` (`:3748`, `:3752`) and the `audio.counter-classified` text (`:3338`).
   - The exhaustive sentences the ruling names are narrowed: `REQUIREMENTS.md:412`-`:419` as they were, TESTING `:1293`, `:1371`, `:1378` and `:1462`-`:1473` as they were, rule 4, `counter_limits` and this body.
   - Interpretation, stated here so it can be checked: the scope includes one event at a time, away from the arms, as rules 1 to 4 and the limits classify it.
     The self-test pins each rule and limit, but no sweep covers that case.
     Leaving it out would have withdrawn the plan's basic per-event claim.
     R699-5's isolated fuzz finds no deviation there beyond the stated neighbour-word limit and H1's spanning excursions, which are not "away from the arms".
2. **The gate.** `test_audio_compositions_never_pass_and_list_every_event` `:9461` (helpers `:9354`-`:9459`).
   - It grades 288 seeded compositions at 16384 frames and the release tolerance of 2, 48 for each of the six planted arms.
   - Each has one to four DUT events. The first is at or over its arm's sample, half the time on a flip arm's own channel. The others are beside any arm, near an earlier event, or anywhere.
   - The events are slips of 1 to 4096 samples, silences (replaced or inserted), swaps, copies, one-word corruptions and constant-mask excursions of up to 2100 words.
     Their masks are the composition sweep's eight classes, the mask that clears the channel's number, or any 32-bit word.
   - `_fuzz_check` `:9426` asserts the property only.
     A `PASS` must equal, word for word on every channel, a clean run with each arm at its logged sample or where the grader found it.
     Each event must have a DUT event within 63 samples of its words, on every channel it changes (measured from its words since Round 7).
     Two allowances exist: a void with an arm missed at the event's sample, and events that leave the channel's words unchanged when removed together.
     Each allowance, and the moved-arm `PASS`, is pinned once (`:9472`).
   - Three new controls each make a composition pass or drop an event from the list, and the fuzz kills each (`receipts/round6/mutant_seeds.log`):
     - #289, a DUT event inside a found arm's tolerance taken as the arm. Seed 1, a 67-word excursion beside the repeat arm, grades `PASS`.
     - #290, a flip arm found in any corruption carrying its mask bit. Seed 146, a two-word `0x100000` excursion over the flip arm, grades `PASS`.
     - #291, a slip arm found at its own sample whatever its size. Seed 12, a DUT drop of 100 at the drop arm's sample, is taken as the arm and left unlisted.
   - Validation beyond the self-test: at `b206d88b`, the receipts' `fuzz_range.py` runs the same generator and check over 70,000 further seeds (288 to 70,287).
     No seed violates the property.
     Six grade `PASS`, each byte-identical to a clean run with each arm at its logged sample or where the grader found it.
     The allowances are a masked arm 267 times and cancelling events 14 times.
     The largest listing distance is 62 samples.
3. **H1 and H2** take the second option.
   The first would add a reading for each: an arm-led reading inside a multi-word excursion, and a zero word joined to the excursion around it.
   The ruling closes the class against new readings, and neither would be a contained change.
4. **S1** is applied as one line.

STOP condition: not met.
R699-5's probes, run unchanged at `b206d88b`, give logs identical to their run at `910d4b94`, apart from three void reasons in their new wording.
Those probes are `r5_fuzz` (isolated, before, cluster; 3,000 seeds each), `r5_arm_excursion` (12,480 cases), `r5_zero_word`, `r5_focus` and `r5_triage`.
Those `910d4b94` logs are byte-identical to R699-5's published receipts.
R699-4's `r4_net_sweep` (0 unbalanced of 7,011) and `r4_arm_corruption_sweep` (156 not FAIL of 24,768, all in the two stated voids) also run unchanged at `b206d88b`. Their logs are byte-identical to R699-5's runs of them at `910d4b94`.
The in-tree sweeps pass unchanged.

Five new controls each fail a named round-6 arm (`tb/tools/torture_release_audio_mutants.py:24`-`:26`, `:205`-`:222`).
One control is re-anchored to the reason constant (`tb/tools/torture_release_mutants.py:761`-`:762`).
In all, 294 controls.

## Round 5

Round 5 answers [R699-4](https://github.com/kebag-logic/milan-fpga/pull/786#issuecomment-6424363636), NEGATIVE at `85da3e45`.
It found four MINOR findings and one residue.
The [round-5 assignment](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-6424374359) closes the composition class by construction:

- an invariant for G3;
- for G1 and G2, a stated exception wherever a fix would need another heuristic reading;
- a self-test sweep as the gate.

[R700-3](https://github.com/kebag-logic/milan-fpga/pull/786#issuecomment-6416855079) is POSITIVE. Rounds 1 to 4 are not rewritten.
Lines are at `910d4b94` in `tb/tools/torture_campaign.py` unless named.

| Finding | Fix, or stated exception | Test that proves it |
|---|---|---|
| G3 (MINOR, regression): a one-word corruption 1 to 4 samples before a constant-mask excursion reported a whole-block slip that never returns | The cause was the hold. It built the held image against offset 0, while the reading had already recorded a slip before the masked run. Now the hold sits at the offset in force where the masked run begins: the window's opening offset, or one the reading reaches, whichever leaves the longest run (`_hold` `:4732`). If the recorded part does not end on that offset, it is read again with the masked words restored. The held slips are then read from that offset, and only where a slip of the reading may lie in the masked run (`_split` `:4772`). The invariant is explicit. `_read` ranks a reading whose slips do not sum to the decoded shift behind every reading that does (`ranked` `:4672`). `_close` keeps a per-channel ledger of decoded shift against reported slips (`:4839`, `:4857`, `_record` `:4890`). A window no reading balances becomes one `unresolved` event at its first sample, with `AUDIO_UNBALANCED_REASON` (`:3717`, `_unbalanced` `:4873`). The 44 near-boundary regressions had a second cause: a coincident word kept a code-bit excursion's offset, so the excursion ran on into its neighbour. `_audio_return` `:4181` now ends it at the first word that fits the offset in force, after a leading stretch under one mask that no single offset of whole blocks explains, and takes the coincident words after it as the return | `test_audio_slip_totals_balance_the_bytes` `:9232`. Seven shapes, each read as its bit-flips with every channel's slips summing to the arms' shift. The guard under a reading that loses a slip (`:9258`). The ranking against a tempting unbalanced reading (`:9273`). On `85da3e45`, six shapes fail (the seventh is a control), and so does the guard |
| G2 (MINOR): a slip shortly before a constant-mask excursion turned it into slips; an adjacent word was absorbed | The slip before is resolved by item 1's construction: the hold now sits at the offset in force, so that slip sizes it. Beside the excursion, a word at either end off the mask the others share is its own one-word event, when no single offset explains the excursion. Its group keeps it out of the excursion's run (`_audio_corruption` `:4211`, `:4232`; `_audio_extend` `:4310`). An excursion under one mask that ends in a slip is one bit-flip and that slip. That holds when no single offset explains its words and none is on the slip's track: as slips it would be three events or more (`_audio_excursion` `:4162`). No exception remains inside the exactness scope that Round 6 states. Outside it, a mask that clears the channel number splits the excursion at each word it makes zero (Round 6, H2) | `test_audio_slip_before_a_constant_mask` `:9207` runs the reviewer's grid, 750 cases in 150 five-channel captures. The slips are drops of 3 and repeats of 2 on every channel, 1, 2, 17, 63 and 64 samples before the excursion. The excursions run 64, 65, 100, 300 and 2049 words, at 3000, 4089 and 6143, under 0x80000, 0x40000, 0x100, 0x00F00F00 and 0x80100. On `85da3e45` it fails at its first case; 100 of its 150 captures fail there in the subtest form of `4a460fc3`. `test_audio_constant_mask_beside_one_word_events` `:9007` covers adjacent neighbours across a block boundary and beside a mask that leaves the channel number, and a slip at the return near a boundary; 8 subtests fail on `85da3e45` |
| G1 (MINOR): a one-word DUT corruption beside a planted arm voided the run | The arm-led case is fixed where one rule covers it. Each word of a two-word excursion under two masks that no single offset explains is its own corruption (`_audio_corruption` `:4232`), so a corruption beside a flip arm is graded beside it. The rest would need another heuristic reading, so, by the ruling's second option, it is stated exactly. Two voids remain. One is a corrupted word on a slip arm's own sample, or the one before it, that is its channel's word at another position at most half a block from the old or the new track's. The other is a corruption of a flip arm's own word on its channel, or of the word beside it under the arm's own mask. One limit is bit-identical: a corruption on a slip arm's own sample, or the next one, may read first, with the slip placed after it within the tolerance. TESTING 6d `docs/testing/TESTING.md:1445`-`:1471`, REQ-VER-06 `REQUIREMENTS.md:412`-`:419` and `counter_limits` (`AUDIO_COUNTER_LIMITS` `:3738`) state them. The "either order" claim is narrowed (`TESTING.md:1347`, `REQUIREMENTS.md:417`), and so is "never hides" (`TESTING.md:1374`-`:1378`, `REQUIREMENTS.md:419`) | `test_audio_composition_sweep` `:9179` grades a corruption 0 to 4 samples from each of the six arms: every channel, eight mask classes, 8192 and 16384 frames, the release tolerance of 2. That is 3456 cases in 288 captures. The bytes alone decide each case's class (`_sweep_class` `:9089`), and the outcome is checked against it (`_sweep_case` `:9113`, `_sweep_check` `:9140`). The outcome is exact; or the repeat a neighbour duplicates; or the corruption read first, checked word by word; or the void with exactly that arm missed. Every reading balances. On `85da3e45` it fails at its first case; 28 of its 288 captures fail there in the subtest form of `4a460fc3` |
| G4 (MINOR): W03 and W07 survived the self-test | New arms | `test_audio_arm_interplay_at_the_release_tolerance` `:9293` runs at tolerance 2. It covers whole-block slips beside both flip arms on two capture lengths, three slip-arm clusters near the end drop arm, and a half-block slip before the flip arm. The reviewer's unmodified `r4_reviewer_mutants.py` kills W03 and W07 there at `910d4b94` |
| R1 (RESIDUE): the reading-choice sentence | As written: "Another reading is taken only when it has fewer DUT events, or as many and finds more arms, so it never hides a DUT event" (`_read` docstring `:4647`; `docs/testing/TESTING.md:1375`). Round 6 narrows it to "never adds a DUT event", among the readings the grader tries | — |

The ruling's items:

1. **The invariant.** At the head, `scripts/r4_net_sweep.py` reports 0 unbalanced of 7011, against 270 before.
   `scripts/r4_regress_sweep.py` reports 0 regressions and 0 deviations of 3744, against 44 regressed and 850 deviating at both heads before.
   A tripwire copy raises on any unbalanced reading or on the guard firing.
   Every probe and sweep here runs clean against it; only the balance arm trips, since it plants both on purpose.
   STOP check: against the round-4 head, the seeded fuzz (6000 cases) changes five verdicts, all NOT RUN to FAIL.
   All five are a corruption on channel 1 one sample beside the flip arm, a swept shape.
   R699-3's, round-2 and R700-3's probes give outputs identical to the round-4 head, timing fields aside.
2. **The exceptions** are stated and pinned as in the G1 row; G2 has none left inside Round 6's exactness scope (H2 lies outside it).
   R699-4's own arm-corruption sweep (d = -64..64) leaves 156 placements not FAIL, against 175 before.
   They are exactly the two stated voids predicted from the bytes, each NOT RUN with only its arm missed.
   Its fuzz regression R-4857, a `0x200` word on the drop arm's own sample, falls in the first of them.
3. **The sweeps are gates.** They are `test_audio_composition_sweep` and `test_audio_slip_before_a_constant_mask`.
   They pass only when every case is exact or matches its stated class.
4. **W03 and W07** are killed by `test_audio_arm_interplay_at_the_release_tolerance`.
5. **R1** is folded in as written.

Two further facts the sweeps showed:

- One limit is newly stated: it predates this round and was found while sweeping (`docs/testing/TESTING.md:1448`-`:1450`).
  Beside a planted flip arm, on its channel, under a slip of whole blocks, the arm's word is the other track's where the two differ.
  So the bytes may be that slip on the other side of the arm, with the arm's code bit one sample over.
  Within 4 samples of the flip arms, 28 of 7680 placements read so, the same as at `85da3e45`.
  Each FAILs with every arm found, and each is checked by bytes, in the receipts and in `_sweep_mirrored` `:9165`.
- One fuzz case moves from OK to INFO: R-3626, two -4096 slips 20 samples apart.
  It still FAILs, and its slips still sum to the shift, inside the cluster limit.
  Its `located_within` no longer covers the first slip's sample.

Suggestions, each a choice:

- S1 not adopted. The void reason now has three stated causes, so a reason naming only the coincident DUT slip would mislead.
  The event list shows what lies at the arm, and TESTING 6d names every cause.
- S2 not adopted. W02, W06 and W10 change no verdict in any sweep here, and neither do W08 and W11.
  One dead check of the new code was removed instead.
- S3 adopted: the interrupted-excursion limit is also pinned with a DUT drop and a DUT repeat (`:8994`).

The first serial driver run hit its 600-second limit on one control, `block code bit dropped from the word`.
Under it every sweep case failed slowly, about 420 seconds in all.
So `910d4b94` makes both sweeps check a clean capture first and stop at their first failing case, which they name.
Under that control they now fail in about a second.
R699-4's parallel runner kills every control at `17a43ef2`.
At `910d4b94`, a parallel runner with the driver's criteria (`scripts/release_mutants_timed.py`) kills all 289.
Its slowest mutated self-test takes 288 seconds under six parallel jobs, against the driver's 600 (1200 from `9c20c08e`).
Run alone, that control's self-test takes 262 seconds at `85da3e45` and 272 at `910d4b94`.

Eighteen new planted defects each fail a named round-5 arm (`tb/tools/torture_release_audio_mutants.py:157`-`:202`).
Seven entries whose anchors the rewrite moved are re-anchored to the equivalent defect: `:72`, `:110`, `:139`, `:152`, and `tb/tools/torture_release_mutants.py:740` and `:838`-`:843`.
One keeps its anchor and now compares only the arms found, the third part of the score (`:129`). In all, 289 controls.

## Round 4

Round 4 answers [R699-3](https://github.com/kebag-logic/milan-fpga/pull/786#issuecomment-6417659353), NEGATIVE at `4d69e192`
with two MINOR findings, under the [round-4 assignment](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-6417665116).
[R700-3](https://github.com/kebag-logic/milan-fpga/pull/786#issuecomment-6416855079) is POSITIVE. Rounds 1 to 3 are not rewritten.
Lines are at `85da3e45` in `tb/tools/torture_campaign.py` unless named. Every listed self-test arm fails on `4d69e192`.

| Finding | Fix | Test that proves it |
|---|---|---|
| R699-3 F1 (MINOR): a one-word corruption followed within 64 samples by a whole-block slip was misgraded, and after the planted flip arm it voided the run | The cause was the window's labelling. Once a corrupted word fitted the closing track, the offset in force before it stopped being a candidate, and the longest run won. Now the offset in force before the last change stays a candidate (`_audio_labels` `:3960`, `:3989`). The offset nearest the one in force is kept while it fits, so each slip takes the smallest size and a slip of whole blocks sits at the first word that shows it; half a block away, the twin nearer the offset before comes first (`_audio_fit` `:4017`, `_audio_candidates` `:3995`). A departure ends at the first word from which every word up to its return fits the offset in force (`_audio_excursion` `:4127`). A one-word departure that returns a whole number of blocks away is a corruption beside that slip (`:4135`), judged against whichever track gives its mask fewer bits set (`:4144`). A whole-block slip's `located_within` runs on to the first word that shows it, the resync included (`_audio_slip` `:4173`, `_audio_upto` `:4183`); a corrupted word bounds it only where the tracks differ (`:4318`). Where the bytes allow two readings, the planted-arm log decides (`_read` `:4546`, `_cut` `:4591`, `_score` `:4618`, `_AudioSteer` `:4083`). A missed flip arm is tried as the corrupted word, judged against the offset in force or the closing one, the window opened before its start where the word was followed. A missed slip arm keeps the excursion it enters or leaves (`:4148`). A slip that differs from a slip arm by whole blocks is split into the arm and a slip beside it (`slip` `:4272`). Another reading is taken only with no more DUT events and more arms found, so the log never hides a DUT event | `test_audio_block_slip_after_a_corruption_or_a_slip` `:8661` (0x100 and 0x80000 corruptions, then ±2048, ±4096 and 8192 slips 1 to 64 samples later; 3-sample drops and 2-sample repeats then ±4096; a half-block corruption just after a slip). `test_audio_planted_arms_beside_block_slips` `:8731`: slips 1, 2, 3 and 9 samples either side of both flip arms and two slip arms, on every channel and on the arm's channel, FAIL with every arm found. Also a slip that undoes a slip arm at the next sample, and logged arms the capture does not show staying missed. The tie pin in `test_audio_slip_and_corruption_share_a_window` `:8612`. Scenarios `tests/features/torture_campaign_plan.feature:514` and `:525` |
| R699-3 F2 (MINOR): the constant-mask rule changed beside a one-word corruption, and at a code-bit corruption ending on a block boundary | Only the window's trailing words under the closing mask start a hold, so an event before them is graded on its own (`_hold` `:4624`). A followed word on the old track is a possible return, never a release; a masked word after it parts the masks (`_AudioImage.keeps` `:4426`, `clean` `:4420`, `holds` `:4434`, `:4502`). A held excursion returns when the content resumes nearer the old track than the held one (`_close` `:4688`). `_returned` `:4522` ends the bit-flip where the old track's words began and grades the rest of the window against the old track, so an event beside the excursion is its own | `test_audio_constant_mask_beside_one_word_events` `:8791`: 0x80000 and 0x40000 over 100 words with a 0x100 word 1 to 64 samples before or after, the planted flip arm as the neighbour, and a planted drop at the return. `test_audio_code_bit_corruption_ending_on_a_block` `:8814`: 0x100 from 5000, 6143 and 6144 to 8191 through 12288. Scenarios `:538` and `:549` |

Bit-identical shapes are stated exactly in TESTING 6d (`docs/testing/TESTING.md:1390`-`:1417`), REQ-VER-06 (`REQUIREMENTS.md:412`-`:414`) and `counter_limits` (`AUDIO_COUNTER_LIMITS` `:3731`).
A self-test arm pins each one by comparing the bytes:

- A code-bit corruption less than 64 samples before a slip of whole blocks may make its word the new track's. When every word between them fits both tracks, the bytes are that slip alone at the corrupted word.
- A slip of whole blocks and a code-bit corruption can give the same bytes in either order: the corrupted word is the other track's and only one word between them differs. The corruption reads first, and the slip is located after it.
- A slip followed, within the words that fit both tracks, by a slip of whole blocks gives the bytes of one slip of their sum.
- A slip pair whose total is whole blocks and whose displaced words share one mask reads as that bit-flip and a slip of whole blocks beside it.
- A DUT slip at a planted slip arm's own sample is one slip of their sum; unless the DUT slip is whole blocks, the arm is missed and the run is void.
- A constant-mask corruption that a slip interrupts reads as the slips its words show.

Suggestions, each a choice:

- R699-3 S1 adopted: the interval decides what is proved clean, not the class of a slip near its end (`docs/testing/TESTING.md:1380`; self-test comment `:8507`).
- R699-3 S2 adopted: both void reasons for an unacquired channel name the DUT not driving the counter on it (`:5049`, `:5074`; `docs/testing/TESTING.md:1434`).

R699-3's probes, rerun unmodified at `85da3e45`, every script byte-identical to its published manifest:

- `r3_arm_void_probe.py`: no NOT RUN line; 0 of 256 not FAIL at every size.
- `r3_cluster_probe.py`: FB 654 OK, 6 DEVIATION (433 before); SB 258 OK, 2 (89 before); CF 32 OK, 0 (28 before); CB 40 OK, 0 (12 before).
- `r3_probe.py`: E 642/6, S 1170/0, M 273/0 (3 before), A 21/8.
- Every remaining deviation is shown, with the reviewer's own encoder, to be its stated limit:
  - the 6 FB and 2 SB lines give bytes equal to the slip alone, or to one slip of the sum;
  - 4 A lines are FAIL with every arm found, and `located_within` holds the slip; the probe compares `capture_index` exactly;
  - 2 A lines put the DUT slip at a planted slip arm's own sample;
  - 2 A lines are a constant-mask corruption that the planted repeat interrupts;
  - the 6 E lines are S1's case.
- Round-2 probes, unmodified:
  - compound 30/30 OK;
  - the arm probe A2 to A5 FAIL, and A1 is NOT RUN only by the 24-hour rule;
  - `grader_probe_r2` has the same OK and DEVIATION per case as at `4d69e192`;
  - the `required_s` port is 110 OK, with P5 void as in the reviewer's own receipt;
  - N07 at 8214.
- `reviewer_mutants_r2.py`: 31 KILLED, 0 SURVIVED, 1 INVALID. N15's line changed; ported to it, N15 is killed.
- `r3_reviewer_mutants.py`: 13 KILLED, 0 SURVIVED, 3 INVALID. V07, V09 and V13's lines changed; ported to them, all three are killed.

R700-3's probes, rerun as byte-identical copies, since they write beside themselves:

- `delta_probes.py`, `qualified_probes.py` and `compound_ambiguity.py` give byte-identical output at `4d69e192` and at `85da3e45`.
- In `boundary_matrix.py`, `compound-4096-1-80000` now meets R700-3's compound rule.
- `compound-4096-5-100` no longer meets it: it is the stated code-bit tie, read corruption first, and the self-test pins its bytes.

Two wider sweeps with the reviewer's encoder FAIL with every arm found in all 39936 placements. They place DUT slips 1 to 64 samples either side of all six arms, on every channel or on one.
The sizes are 1, 2, 3, 5, 7, 100, 1023, 1024, 1025, 2047, 2048, 2049, 3000, 4096, 6143, 6145 and 8192 samples, most in both directions (`receipts/arm_sweep.log`, `receipts/arm_sweep_odd.log`).
Twenty-two new planted defects in `tb/tools/torture_release_audio_mutants.py` each fail a named round-4 arm.

## Round 3

Round 3 answers [R700-2](https://github.com/kebag-logic/milan-fpga/pull/786#issuecomment-6413374622) and
[R699-2](https://github.com/kebag-logic/milan-fpga/pull/786#issuecomment-6413444899), both NEGATIVE at `a3e24ac5`,
under the [round-3 assignment](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-6413452035).
Rounds 1 and 2 are not rewritten.
Lines are at `4d69e192` in `tb/tools/torture_campaign.py` unless named.

| Finding | Fix | Test that proves it |
|---|---|---|
| R700-2 F1 (MAJOR): a slip of whole blocks at a capture's boundary could earn PASS | Every verdict states its qualified interval (`_CounterScan.qualified` `:4461`, `_audio_qualified` `:4676`). It runs from 63 samples after the last channel's acquisition to 63 samples before the capture's end. `grade_audio_counter_capture` `:4709` takes `required_s`, 86400 by default. `PASS` needs that many observed seconds in the interval; a shorter one is NOT RUN (`:4799`). Logged losses are not observed time. A channel that never acquires, or an arm or logged loss outside the interval, is NOT RUN by name (`:4776`). At either end, words that differ from the track only in the code bit are one `unresolved` event with `located_within` (`_audio_boundary` `:3993`, `_audio_open` `:4081`), never an exact class | `test_audio_qualified_interval_is_stated_and_required` `:8105`. `test_audio_boundary_block_slips_are_unresolved` `:8169` keeps the reviewer's byte-identical endpoint pairs, pinned by the published capture SHA-256. They cover whole-block drops and repeats 1 to 65 samples from the end and 10 to 62 from the start, both byte orders, 113-byte chunks, and with and without guard samples. Scenarios `tests/features/torture_campaign_plan.feature:477` and `:484` |
| R700-2 F2 (MINOR): the constant-mask rule changed silently at 64 samples | One rule at every length. Sixty-four corrupted words that decode as another track are held as `_AudioImage` (`:4263`, `_audio_image_mask` `:4250`), not adopted. If the words return to the old track, the whole excursion is one `bit-flip` (`_close` `:4389`). A word off the mask releases the held events as the slips they are (`:4329`, `_release` `:4353`). Past the 65536-word bound, a constant-mask stretch stays a `bit-flip` in each piece (`_audio_excursion` `:4049`) | `test_audio_constant_mask_at_every_length` `:8249`: masks `0x100`, `0x80000`, `0x40000` and `0x200` over 2, 63, 64, 65, 100 and 2000 words, across block boundaries and chunked. Genuine slips that are images for a while are released exactly. A half-block repeat and drop is the stated bit-identical limit. An excursion the capture ends inside carries `unresolved`. Scenario `:496` |
| R699-2 F1 (MINOR): a slip and a one-word corruption in one 64-sample window were misgraded and could void a run | A run of positions is cut at each word no offset explains (`_audio_fit` `:3980`, `_audio_candidates` `:3960`, in `_audio_labels` `:3905`). Each departure is judged against the offset in force, again after every slip (`:4170`) | `test_audio_slip_and_corruption_share_a_window` `:8299` covers drop 3, repeat 2 and drop 4096. Each is followed 5, 40 or 100 samples later by a `0x80000`, `0x40000` or `0x100` flip or a two-word burst. A DUT drop beside the flip arm FAILs with the arm found, and arms 10, 40 or 63 samples apart PASS. Scenario `:509` |
| R699-2 F2 (MINOR): a whole-block slip in the last 63 samples read as a code-bit corruption | The same boundary rule: an `unresolved` event, as TESTING 6d states (`docs/testing/TESTING.md:1382`). A logged loss there is outside the qualified interval, so it is NOT RUN by name (`TESTING.md:1431`) | `test_audio_boundary_block_slips_are_unresolved`. The reviewer's edge probe, unmodified, reports `unresolved` at every `F-20` to `F-63` row |
| R699-2 F3 (MINOR): the "at or before" acquisition boundary was untested; mutant N07 survived | Test added; the code was right | `test_audio_capture_losses_advance_the_clocks` (`:8014`) checks a loss logged at an event's own index. Scenario `:514`. The reviewer's mutant runner, unchanged, kills N07 |

A round-3 regression was caught before review: the 24-hour default made a clean short capture NOT RUN.
So the invalid-anchor arm stopped depending on its anchors, and the reviewer's N30 and N31 survived.
That arm now grades against its capture's qualified length, with a valid-anchor control that must PASS (`:8038`, commit `4d69e192`).
N30 and N31 are killed again.

Suggestions, each a choice:

- R699-2 S1 adopted as documentation: a capture starts once the counter flows; leading silence fails (`TESTING.md:1394`, plan `capture_start` `:5162`).
- R699-2 S2 adopted: every verdict lists `anchor_gaps` (`_audio_anchor_gaps` `:4690`), verdict unchanged; `test_audio_anchor_gaps_are_reported` `:8337`.
- R699-2 S3 adopted: a channel that has not acquired within 65536 frames voids the run at once (`:4752`); the reviewer's misuse probe now stops in under a second.
- R699-2 S4 adopted: the window bound is documented, and its pieces keep one rule (`TESTING.md:1388`).

Bit-identical limits, each pinned by a self-test arm (TESTING 6d):

- A flip of position bit 0 can make a word equal to its neighbour; it then reads as that slip pair.
- A slip pair whose displaced words share one XOR mask reads as a `bit-flip`, at any length.
- A slip of whole blocks is found within 63 samples, sized exactly, with `located_within`.
- A slip that is the old track under one mask is held until the masks part, at most one block later.
- Between events under 64 samples apart, slips take the smallest sizes; a code bit they leave unexplained reads as a code-bit `bit-flip`.
- At either end of a capture, a code-bit-only stretch is one `unresolved` event; other unconfirmed slips carry `unresolved`.
- Nothing outside the qualified interval is proved clean.

Reviewer evidence rerun at `4d69e192`, every script byte-identical to its published manifest:

- R700-2 `delta_probes.py`, unmodified. Interior rows are unchanged. The byte-identical tail pairs and the clean control are NOT RUN, since a 0.17 s capture cannot meet the 24-hour rule. `tail-slip-8191-4096`, `tail-slip-with-64-more-frames` and `initial-slip` are `unresolved`. `constant-code-xor-64`, `-65`, `-100` and `-chunked` are one `bit-flip` each.
- The same probe ported to pass `required_s` only, with the interval recorded. The clean control and both byte-identical pairs PASS with the interval `[63, 8129)`, so the slips lie outside what is proved. `initial-slip` starts it at 73.
- R699-2 probes, unmodified:
  - the compound probe is 30/30 OK;
  - the arm probe's A2 to A5 FAIL;
  - the edge probe's X1 is `unresolved` from `F-20` to `F-63`;
  - the N07 probe gives acquisition index 8214;
  - every other DEVIATION is a clean capture NOT RUN by the 24-hour rule.
- Ported to pass `required_s` only, every line is OK except P5. P5 plants no arms, so it is void, as in the reviewer's own receipt.
- R699-2 `reviewer_mutants_r2.py`, unchanged: 32 KILLED, 0 SURVIVED, 0 INVALID. The round-1 runner, unchanged: 22 KILLED, 6 INVALID on code round 2 removed.
- The round-3 test class transplanted onto round 2's grader fails every new boundary, mask, window, interval and anchor-gap arm. A shim accepts the new keyword there, so each arm fails on behaviour.
- Nine planner defects planted at feature level each fail a named scenario.
- 30 planted defects added in `tb/tools/torture_release_mutants.py` each fail a named self-test arm.

## Round 2

Round 2 answers [R699-1](https://github.com/kebag-logic/milan-fpga/pull/786#issuecomment-6409756577) and
[R700-1](https://github.com/kebag-logic/milan-fpga/pull/786#issuecomment-6409757802), both NEGATIVE at `21faa482`,
under the [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-6409763644).
Every listed test failed on round 1's code. Line numbers below are at `a3e24ac5`.

| Finding | Fix | Test that proves it |
|---|---|---|
| R700 F1 (MAJOR): the repeating payload cannot prove zero glitches | Non-repeating counter, `audio_counter_word` `:3699`, `_audio_decode` `:3752`; windows close at 64 clean samples whose decoded position sizes every slip | `test_audio_counter_word_layout`, `test_audio_block_slips_are_sized_exactly` |
| R699 F3 (MINOR): the 4096-multiple backstop did not hold | The blind spot is gone; the backstop claim is removed | `test_audio_block_slips_are_sized_exactly` |
| R699 F1 (MINOR): compound and edge events; a static swap voided the run | Neighbour repeats, constant-mask excursions, identities acquired at capture start | `test_audio_compound_and_edge_events`, `test_audio_static_swap_fails_with_every_arm_found` |
| R700 F2 (MAJOR): tag corruption read as a swap | Tag integrity decides first; only a reciprocal exchange is a swap | `test_audio_tag_integrity_decides_first` |
| R700 F3 (MAJOR): pending defaults satisfied the commit-cut vacuity guard | `ReleaseCommitCut`; a pending default or a cut outside its window is NOT RUN | `test_release_commit_cut_evidence` |
| R700 F4 (MAJOR): planted exceptions covered whole read intervals | An increment is excused only between two reads inside its planted window | `test_release_soak_media_unlocked_planted` |
| R700 F5 (MAJOR): capture losses did not advance the event clocks | Acquisition index adds every logged loss; times interpolated between anchors | `test_audio_capture_losses_advance_the_clocks` |
| R699 F2 (MINOR): mutants G07, G12, R03 survived | Anchors kept, behaviour pinned | Killed by named arms |
| Residues; S1 and S2 adopted; S3 declined | Comment IDs removed; arms in the first and last tenth; per-channel fast path | `test_audio_arms_run_at_both_edges`, `test_audio_offset_channel_and_mixed_capture` |

Citation note: the round-2 assignment cites Milan v1.2 4.4.2.1 for the sample rate.
In Milan v1.2, 4.4.2.1 is the Listener's 2.126 ms presentation-time buffering.
The sample-rate set is in 6.2, Table 6.1, so the period is stated against that clause.

## Authoritative references

- #396 owner decisions issuecomment-6408072465 and issuecomment-6409128703; assignments issuecomment-6408079016,
  issuecomment-6409763644, issuecomment-6413452035, issuecomment-6417665116, issuecomment-6424374359 and issuecomment-6432123822;
  issuecomment-6435672624 (round 7); audio design issuecomment-5978644444;
  `mr`/`tu` rule issuecomment-5857765949 (unchanged).
- Milan v1.2 5.3.8.10 with Table 5.6 (counters, reset on not-bound to bound); 5.3.5.1, 5.3.7.1,
  5.3.7.6, 5.3.8.1-5.3.8.3, 5.3.8.7, 5.3.9.1, 5.3.10.1, 5.3.11.1, 5.3.13 (saved state);
  5.5.1.4 ("a power cycle or a simple reset"); 5.5.2.4/5.5.2.6; 5.6.2/5.6.3; 6.2 Table 6.1 (sampling rates); Annex B.1.1.
- IEEE 1722-2016 4.4.4.3, 4.4.4.6, 4.4.4.7, 7.3.5. IEEE 1722.1-2021 6.2.2.5, 7.4.43.
- REQUIREMENTS.md section 8 (REQ-VER-06); CONTRIBUTING.md section 3; docs/testing/TESTING.md sections 6, 6b, 6d;
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
python3 -B scripts/check_feature_status.py
git diff --check origin/dev HEAD
```

Expected result / pass criteria: every command exits 0.

- The self-test runs 120 tests OK, in about 30 seconds on an idle host.
- The mutation driver prints `PASS: 297 mutations killed; source unchanged`, after about two and three-quarter hours on an idle shared host.
- Behave reports 495 scenarios passed, the plan feature 176.
- The coverage audit reports `soak`, `audio` and `power` complete.
- The docs gates report zero findings.

## Known limitations / out of scope

- The bench runs on the shipping image, and the two power controls on their known-defect images,
  are #396 part B (acceptance items 3 and 4). Nothing here touches hardware.
- The bench source must implement the counter layout above.
  The capture tool must record its anchors at least every `audio_context_s` and at the capture's end.
  The power runner must record each commit cut's window and cut instant.
- Each audio capture must run past the 24 hours at both ends.
  It needs at least 63 guard samples at each end, plus any logged loss.
  The soak window outlasts 24 hours by as much. The plan states this.
- Logged capture losses are not counted as observed time, so a run with losses must capture longer. This is the strict reading of "the qualified interval covers the full 24 h".
- Owner decision issuecomment-6409128703 sets two things this plan text does not yet carry:
  - AECP REBOOT for the 50 soft resets, NOT RUN until REBOOT lands;
  - sine-pair limits at the first-hour baseline plus 6 dB.
  Both lie outside the round-4 and round-5 assignments and are for the manager to route.
  Until the limits are recorded, `audio.analog-sine-pair` stays NOT RUN, so no release can qualify.
- `restore_bound_s = 30` stays provisional, pending ratification from #397 and #75.
- The counter's wrap is 23.4 Hz at 48 kHz, no longer infrasonic as the 2026-10-04 design described; its level is unchanged.
- The bit-identical limits in TESTING 6d are properties of any finite-alphabet signal, stated rather than hidden.
  Where two readings tie, the grader takes a stated convention, and the planted-arm log decides at a logged arm.
- The release mutation driver runs the whole self-test once per defect, so it takes about two and three-quarter hours on a shared host (2 h 43 min at `b206d88b`), and far longer under load.
  The round-5 sweeps add about 10 seconds to each self-test, the round-6 fuzz about 4, and the round-7 nested family about 3.
  Each control may now take 1200 seconds before a timeout counts as no kill.
- Beside a planted flip arm, on its channel, 28 of 7680 placements of a slip of whole blocks within 4 samples read the slip on the other side of the arm.
  The bytes are identical either way, and the round-4 head reads them the same; the limit is stated and pinned by bytes.
- Of R699-4's delta mutants, W02, W06, W08, W10 and W11 still pass the self-test.
  None changes a verdict in any sweep here; S2 is not adopted (Round 5).
- Exact classification is claimed only inside the stated scope (Round 6).
  Outside it, two shapes are pinned rather than read exactly.
  H1: a multi-word excursion over a slip arm can void the run, 3,848 of R699-5's 12,480 grid cases, unchanged.
  H2: a mask that clears the channel number splits an excursion at each word it makes zero.
  A void blocks the release, and both still list every DUT event.
- The property fuzz is a seeded sample, not exhaustive.
  The self-test grades 384 compositions: 288 arm-led and 96 nested.
  Round 7 checked 20,000 more of each family offline (10,000 per family and capture length).
  R699-6's 60,000 arm-led seeds, rerun at `5fdabc1c`, show no violation.
- The listing bound's lower edge is round 6's, 63 samples before the event's first word, where the round-7 ruling says "at or after the event's first word".
  Round 7 gives the evidence and asks for a decision.
- The nested family reaches R699-6's late-listing mechanism only rarely (15 of 5,000 at `b206d88b`, none of its 96); the pin covers that mechanism.
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
