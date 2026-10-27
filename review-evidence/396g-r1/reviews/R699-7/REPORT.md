[R699] NEGATIVE - exact head 5fdabc1c4c76206bd2528435c56d88466c0f972e

# R699-7: internal cleared-context delta review, issue #396 part A, PR #786

Head `5fdabc1c4c76206bd2528435c56d88466c0f972e`, tree `dcf4ae711002ba47e61a61a85eb4369ac63a8fce`, source base `e76a755a`. The previously reviewed head is `b206d88b` (R699-6). The delta is two commits, `73be3b36` and `5fdabc1c`, and touches four files: `REQUIREMENTS.md`, `docs/testing/TESTING.md`, `tb/tools/torture_campaign.py` and `tb/tools/torture_release_audio_mutants.py`. Both commits are one line, with no trailers.

## Scope reconstructed

- Issue #396 acceptance 1, 2 and 5, plus the desk half of 4, per the part-A assignment (issuecomment-6408079016). Items 3 and 4 need the bench (part B), so the PR correctly says "Relates to #396".
- Owner decisions:
  - 2026-10-04 audio design: item 1, every discontinuity classified at its sample; item 4, a per-event record "to localize the source".
  - 2026-10-26 decisions: 24 h; 200 cycles; the stricter criteria; the gate written in both documents.
  - 2026-10-26 follow-ups: REBOOT, and sine limits set at baseline + 6 dB.
- Round-7 assignment (issuecomment-6435672624):
  - Item 1: outside the exactness scope, a DUT event never grades PASS, is listed on each channel it changes, and each listing is bounded relative to the event's first and last words. Inside the scope, the listing is within 63 samples of the first word.
  - Item 2: the fuzz gate asserts that bound for every generated composition, "including a slip inside a constant-mask excursion".
  - Item 3: pin R699-6's case.
- Ruling on the author's STOP (issuecomment-6442502921): the lower edge is "no earlier than 63 samples before the event's first word"; the upper edge is "no later than 63 samples after its last word".

## Verdict

**NEGATIVE.** One MINOR is open (F1). There are also two RESIDUE items and two SUGGESTIONs. There is no BLOCKER or MAJOR.

- **R699-6 F1 is resolved.** The grader fix in `_close` (`tb/tools/torture_campaign.py:4852-4888`) is contained. It changes only the hold's re-read path, so the returned excursion's bit-flip is no longer lost. The new pin fails at `b206d88b` and passes here. Its control is killed by name. The author's swept-case dumps are byte-identical across both heads (hash-verified).
- **The fail-safe half of the property holds.** In my probes, no capture with a DUT event grades PASS: 4,000 nested compositions over the two capture lengths, and the gate's 288 arm-led seeds.
- **The new localisation sentence does not hold for compositions the new nested family generates (F1).** An event inside a constant-mask excursion can be "listed" on that channel only by the excursion's enclosing listing, which begins hundreds of samples earlier. Or its own listing comes after the excursion returns, hundreds of samples after its word. The gate measures "listed" as any overlap with the event's words widened by 63 samples, and an enclosing listing always overlaps. So the gate cannot fail on this. In the gate's own 96 nested compositions, it happens 12 times.

## Findings

### F1 MINOR: Conformance, Robustness, Tests, Docs. An event inside a constant-mask excursion is not listed within the stated bound, and the gate's overlap test cannot see it

**Where.**
- The claim:
  - `REQUIREMENTS.md:410` ("Each listing falls no earlier than 63 samples before the event's first word and no later than 63 samples after its last.");
  - `docs/testing/TESTING.md:1497`;
  - `AUDIO_COUNTER_LIMITS[0]` (`tb/tools/torture_campaign.py:3750-3754`);
  - the `audio.counter-classified` text (`:3341-3345`);
  - the PR body, lines 122 and 184.
- The gate:
  - `_fuzz_reach` (`:9433-9438`) returns `max(low - last, first - high, 0)`, which is overlap;
  - `reaches` (`:9474-9477`) and the stray check (`:9498`) use it;
  - `_fuzz_nested` (`:9415-9428`) generates the shape.

**Authority.**
- Round-7 assignment items 1 and 2 (the bound, and a gate that asserts it for "a slip inside a constant-mask excursion").
- The STOP ruling's two edges.
- Owner audio design item 4 (localise the source).

**Evidence.** From `probe_reach.py` and `probe_dump.py`; receipts are under `receipts/`.
- Gate seeds, `_fuzz_nested` unchanged (`reach_nested_8192_0-48.jsonl`, `reach_nested_16384_0-48.jsonl`):
  - 6 units at each capture length have no DUT listing on their channel that begins within [first word - 63, last word + 63].
  - Each one passes the gate only through the excursion's enclosing listing. The units are nested seeds 0, 11, 18, 21 (two units) and 47.
- 16384 frames, nested seed 11 (`dump_nested_16384_11.txt`):
  - The composition is an excursion of mask `0x01000000` over channel 3's words 8520 to 9509, plus a DUT drop of 1024 at 9008 on every channel.
  - Channels 0 to 2 list `dropped 1024` at 9008.
  - Channel 3 lists `bit-flip 990` at 8520, with mask `0x01080100` (the slip read into the corruption), and `dropped 1024` at **9510**.
  - So the slip's only listing on channel 3 is 502 samples after its word. If the enclosing bit-flip is counted as the slip's listing instead, that listing begins 488 samples before the slip's word. Either way the stated bound fails.
  - `_fuzz_check` returns `('FAIL', set())`: it passes the case.
- Seed 0 (`dump_nested_16384_0.txt`): a whole-block drop of 2048 at 1441, inside channel 3's excursion 863 to 2655, is listed on channel 3 at 2656. That is 1,215 samples late.
- Seeds 21 and 47: a silence of 33 samples and one-word corruptions inside an excursion. On that channel, they appear only as words of the excursion's single `bit-flip` listing, which begins 244 to 782 samples before them.
- Rate (`reach_nested_{8192,16384}_0-2000.jsonl`):
  - 226 and 228 units in 2,000 nested seeds per length.
  - Kinds: slips 131 and 136, silences 43 and 42, swaps 23 and 21, copies 15 and 15, one-word corruptions 14 and 14 (8192 then 16384).
  - Some are in FAIL runs and some in NOT RUN runs.
  - The arm-led family's gate seeds 0 to 287: 0 (`reach_arm_16384_0-288.jsonl`).
- The author's literal-edge probe (`author-r7/scripts/early_distance.py`, hash-verified) also counts a listing as present when it meets [first, last + 63] by overlap. So the published round-7 measurements did not examine this shape.
- This is not R699-6 F1, which is fixed. That finding was the excursion listed late from the slip. This is the event inside the excursion listed late, or only by the excursion's own listing.

**Impact.**
- The release verdict is unaffected: every case grades FAIL or NOT RUN, never PASS.
- The per-event record points an investigator at the excursion's return, up to 1,215 samples (25 ms at 48 kHz) after the slip, on the channel that carried the excursion.
- REQ-VER-06's new normative sentence is false under its plain reading.
- The gate presented as proving the bound cannot fail on this shape, and ruling item 2 names this shape explicitly.

**Required outcome:** either of these.
- (a) The grader lists each DUT event inside an excursion on each channel it changes, with a listing that begins within [first word - 63, last word + 63]. The class may be any class outside the scope. The gate's `reaches` then requires that start, rather than overlap, for each unit.
- (b) Or, if (a) is not contained, publish the limit and obtain a manager decision. Then state it in REQ-VER-06, TESTING 6d, `AUDIO_COUNTER_LIMITS[0]`, the assertion text and the PR body. For example: an event inside a constant-mask excursion on the same channel may be listed only by that excursion's listing, or after its return, at most 63 samples past the excursion's last word. Make the gate check exactly that statement, and pin one example. Option (b) narrows the ruled bound, so it needs the decision before it is written.

**Verification.**
- `probe_reach.py <repo> nested {8192,16384} 0 48 16` reports 0 offending units, or only units inside a newly decided and stated shape that the gate checks.
- A control that moves a nested slip's listing on the excursion's channel to after the excursion's last word, by more than 63 samples past the slip, is killed by the fuzz gate (option a) or by the new pin (option b).

### R1 RESIDUE: Docs. "mostly slips" overstates the nested family's mix

- Where: `docs/testing/TESTING.md:1510`, the `_fuzz_nested` docstring (`tb/tools/torture_campaign.py:9417`) and PR body line 132.
- The generator draws slip in 3 of 7 kinds (`:9427`), which is 43%, not a majority.
- Exact fix: replace "mostly slips" with "slips in three draws of seven", or "more often slips than any other kind".

### R2 RESIDUE: Docs. The PR body still calls the lower edge an open decision

- Where: PR body line 122 ("(the open decision above)") and the risk at line 525.
- The STOP was ruled in issuecomment-6442502921.
- Exact fix: replace "(the open decision above)" with "(as ruled in issuecomment-6442502921)", and close the line-525 risk with the same link.

### S1 SUGGESTION: Tests. Let the nested family reach R699-6's mechanism

- The PR body records that none of the 96 nested seeds reaches the interrupted-excursion re-read path, so only the pin guards it.
- One fixed nested seed (or a placement that holds the slip less than 64 samples before the return, with an excursion mask the hold reads as one) would let the fuzz also kill the "returned excursion's bit-flip left for the hold" control.

### S2 SUGGESTION: Tests. R699-6 S2 still applies

- In a void run, the masked allowance (`:9484-9487`) excuses any unit near a missed arm, not only the unit whose removal restores it.
- This is optional, because a void blocks the release.

## Prior findings at this head

| Finding | Status at `5fdabc1c` | Evidence |
|---|---|---|
| R699-6 F1 (MINOR): an excursion a slip interrupts is listed only from the slip | **Resolved** under round-7 item 3, first option.<br>- `_close` keeps `_returned`'s bit-flip apart and records it first (`:4877-4888`).<br>- Pin `test_audio_excursion_a_slip_interrupts_is_listed_from_its_first_word` (`:9570`).<br>- The limit is stated in `TESTING.md:1457-1458` and `AUDIO_COUNTER_LIMITS`. | - My control run (`receipts/new_mutants.txt`): the pristine pin passes; the mutant fails with `(0, 6097, 'dropped', 1021, '') != (0, 4424, 'bit-flip', 1673, '0x00080100')`.<br>- Author transplant log: the pin fails at `b206d88b`.<br>- R699-6's `probe_gap` receipt now reads `gap_over_63: 0, max_gap: 1`.<br>- `fuzz_8192_2M` reads `violations: 0`.<br>All hash-verified (`receipts/author_evidence_check.txt`). |
| R699-6 S1 (SUGGESTION): measure from the words a unit changes | **Adopted.** `_fuzz_reach` now measures first to last word, and seed 2017152 passes. The cancellation rebuild keeps the composition's order. | `fuzz_8192_2M.json`: 0 violations. |
| R699-6 S2 (SUGGESTION): the masked allowance is wide | Not adopted. It is optional, and retained as S2 above. | `:9484-9487` |
| R699-6 S3 (SUGGESTION): the PR body's dated 600 s figure | **Adopted.** | PR body |
| R699-5 and earlier R699 findings | **Resolved**, as R699-6 recorded. The delta touches only `_close`'s returned path and the fuzz. | `git diff b206d88b..5fdabc1c` |
| R700-1 to R700-3 findings | **Resolved**, as recorded at their heads. Their causes are untouched by this delta: the qualified interval, the tag rules, the power and soak checks, and capture-loss handling. | Same diff |

## Gates and probes at this head (rc 0 unless stated)

**My gates.** Receipts are in `receipts/`.
- `torture_campaign.py --self-test`: 120 tests OK.
- `behave features/torture_campaign_plan.feature`: 176 scenarios, 665 steps.
- `docs_check.py`: 0 findings. `check_doc_paths.py`: OK. `check_doc_style.py`: OK. `git diff --check e76a755a HEAD`: clean.
- `gen_toc.py --check`, `--verify-anchors`, and `check_em_dash.py --base e76a755a` and `--base b206d88b`: 0 findings, under the hash-locked pinned renderer in a scratch virtual environment. Without the renderer they exit 2, and those runs are not counted.
- Delta lines: no em dash, and no lane label, review round, reviewer ID or comment ID.

**Delta controls** (`probe_new_mutants.py`, named test only, against a scratch copy): all three round-7 controls are killed by their named test, and both named tests pass pristine.
- "returned excursion's bit-flip left for the hold": killed by the pin.
- #296 and #297: killed by the fuzz at seed 0.

**Author evidence** (evidence tree `19865d0b`): 14 round-7 files were checked against `MANIFEST.json`, and all match.
- `rc.txt`: every gate is rc 0.
- `head.txt` names this head, tree and gitlinks.
- `selftest.log`: 120 OK.
- TOC and em-dash: 0 findings.
- `sweeps_compare.log`: IDENTICAL.
- The 297-control serial driver run is taken from the author's receipts and was not rerun.

**Hosted, inspected only** (`receipts/hosted_checks.tsv`, when read): 11 pass, 36 pending, 1 skipped. The Yosys and Verilator shards were still pending. The manager owns hosted and act acceptance.

**Clone restored** (`receipts/restore_check.log`).
- My probes' bytecode cache under `tb/tools/__pycache__` (ignored, created by this review) was removed.
- Porcelain, including ignored files, is empty.
- Index and worktree match HEAD.
- The `ls-files -s` digest equals the tree digest.
- All three gitlinks match the base.

## Lens coverage

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Round-7 assignment items 1 to 3 and the STOP ruling, against `REQUIREMENTS.md:402-430`, `AUDIO_COUNTER_LIMITS` `:3749-3760`, assertion text `:3338-3352`, and my nested and arm-led probes | R699-7 | `5fdabc1c4c76206bd2528435c56d88466c0f972e` |
| RTL | CLEAN | No RTL, firmware, builder or gitlink change in `b206d88b..5fdabc1c` (`git diff --stat`; gitlinks in `restore_check.log` equal the base). Grader state handling in `_close`/`_returned`/`_hold`/`_split` (`:4650-4888`) was traced: the flip is net-zero and ends before the window's tokens, so the balance and the hold's offsets are unchanged. RTL coverage of the rest was banked by R699-1 and is untouched. | R699-7 (delta); R699-1 (rest) | `5fdabc1c4c76206bd2528435c56d88466c0f972e` |
| Robustness | UNCLEAN (F1) | 4,000 nested compositions (both lengths) and 288 arm-led compositions. Dumps of nested seeds 0, 11 and 21. The pin's composed case. | R699-7 | `5fdabc1c4c76206bd2528435c56d88466c0f972e` |
| Tests | UNCLEAN (F1) | `_fuzz_nested`, `_fuzz_reach`, `_fuzz_check` and `reaches`/stray (`:9361-9536`). The new pin `:9570`. `tb/tools/torture_release_audio_mutants.py:221-232`. Three controls run. Self-test and plan feature. | R699-7 | `5fdabc1c4c76206bd2528435c56d88466c0f972e` |
| Docs | UNCLEAN (F1; R1 and R2 are RESIDUE) | `REQUIREMENTS.md:406-420`, `TESTING.md:1454-1536`, `AUDIO_QUALIFICATION`/`AUDIO_COUNTER_LIMITS`, the `_close` docstring, the PR body round-7 section. Docs, TOC, anchor, em-dash, style and path gates. | R699-7 | `5fdabc1c4c76206bd2528435c56d88466c0f972e` |

## Real limits

- My probes are seeded samples, not exhaustive. F1 is a counterexample, and the other counts bound nothing beyond the seeds run.
- I did not trace which reading path produces the late listing in F1. Its cause is inferred from outputs.
- I did not rerun the full 297-control serial driver. I ran the three delta controls and hash-checked the author's receipts.
- Physical calibration was NOT RUN. Acceptance items 3 and 4 are part B, and field skips are not hardware proof.
- No manager source bank runs at this head, and I claim none.

## Pending manager duties

- Route F1, deciding (a) or (b). Option (b) narrows the ruled bound. Carry R1 and R2 to the residue checklist.
- Build and validate the current-dev merge candidate (source base `e76a755a`, live dev `97aab1d0f28bd753a3e11df6278d5cac54f964dd`), with builder and native receipts linked on the PR.
- Hosted and act acceptance at the exact head (Yosys and Verilator shards were pending when read).
- Part-B routing still open: REBOOT and sine limits (issuecomment-6409128703), and `restore_bound_s = 30`.

## Receipts

Listed in `MANIFEST.sha256`. Scripts run as `python3 -I <script> <path to the clone> ...` and import only `tb/tools/torture_campaign.py` from it.

R699-7 FINISHED
