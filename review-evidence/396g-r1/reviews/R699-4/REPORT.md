[R699] NEGATIVE - exact head 85da3e4595871c1573c28b4d040b9e98463a41c9

# R699-4: internal cleared-context delta review of PR #786 (issue #396 part A)

- **Head:** `85da3e4595871c1573c28b4d040b9e98463a41c9`, tree `9ed9c6f592675f0e9bf59858b80a77c6255ccb22`.
- **Delta reviewed:** `4d69e192..85da3e45`, one commit by the round-4 executor. Eight files changed:
  - REQUIREMENTS.md and TESTING.md;
  - the planner `tb/tools/torture_campaign.py`;
  - the release mutant driver, now split into `torture_release_mutants.py` and the new `torture_release_audio_mutants.py`;
  - the plan feature, its steps, and the new `tests/steps/torture_audio_model.py`.

  There is no RTL, firmware, builder or submodule change. The source base is dev `e76a755a`.
- **Reconstructed from:**
  - AGENTS.md and CONTRIBUTING.md;
  - the round-4 assignment (PR comment 6417665116);
  - my own R699-3 report (6417659353);
  - REQ-VER-06 (`REQUIREMENTS.md:402-445`) and TESTING 6d;
  - the diff;
  - the author's round-4 receipts at `fdbd536f` `review-evidence/396g-r1/author-r4`;
  - the exact-head hosted check runs.
- **Prior findings:** I read the other reviewer's round-3 findings only after my verdict, findings and ledger were written. See "Other reviewer's round-3 findings" at the end.
- **Scope rule:** my round-3 ledger stands for code this delta does not touch.

## Verdict

The verdict is **NEGATIVE**. Four MINOR findings are open, plus one RESIDUE and three SUGGESTIONs. There is no BLOCKER or MAJOR.

**F1 is resolved. F2 is resolved in the probes as run, except one case carried as G3.** I reran my R699-3 probes unmodified (every script byte-identical to its published manifest):
- **F1:**
  - `r3_arm_void_probe.py` gives no NOT RUN in 2,304 placements: 9 sizes, 256 placements each.
  - `r3_cluster_probe.py` gives FB 654 of 660 and SB 258 of 260.
  - All 8 remaining deviations give bytes identical to the reading the grader gave, which the new limits state (group X, 10 of 10).
- **F2:**
  - CF 32 of 32 and CB 40 of 40;
  - the length sweep M 273 of 273.
  - Swept at every gap from 1 to 64 (`scripts/r4_cf_full.py`), F2(a)'s shape is exact in 255 of 256 cases. It was 0 of 256 at `4d69e192`.
  - The one exception is G3's regression: `0x100` 3 samples before a `0x80000` excursion.

The open findings come from wider probes of the rules this delta now claims. Three of the four were already present at `4d69e192`, but the delta's new text claims them. The fourth is a regression this commit introduced.
- **G1:** a one-word DUT corruption at the sample next to a planted arm voids the run. This contradicts the new rule that the arm log decides.
- **G2:** a slip shortly before a constant-mask excursion turns the excursion into slips. This contradicts "beside any one-word event".
- **G3 (regression):** a one-word corruption 1 to 4 samples before a constant-mask excursion now reports a whole-block slip that never returns. That happens in 270 of 7,011 cases at this head and 0 at `4d69e192`.
- **G4:** two mutants of the new arm-log code survive the self-test, and both bring back R699-3 F1's void. The self-test exercises arm interplay only at arm tolerance 0.

No case falsely PASSes. Every misgraded case either FAILs or is void (NOT RUN).

## Findings

### G1 MINOR: Conformance, Robustness, Tests, Docs. A one-word DUT corruption next to a planted arm voids the run, although the bytes allow the reading that finds the arm

**Where:**
- `tb/tools/torture_campaign.py:4546-4589` (`_read`). Alternative readings are tried only:
  - for a flip arm, as a forced corrupted word;
  - for a slip arm, as `keep`, or as a whole-block split in `slip` at `:4276`.
- No reading separates a one-word corruption from an adjacent arm.
- Claims:
  - `REQUIREMENTS.md:413-414`;
  - `docs/testing/TESTING.md:1343` and `:1354-1361`;
  - assertion texts `:3347-3350` and `:3361-3363`;
  - `AUDIO_COUNTER_LIMITS` `:3747-3751`;
  - the PR body: the audio row, and the Round 4 F1 row's "so the log never hides a DUT event".

**Authority:**
- REQ-VER-06 at this head: "Where the bytes allow two readings, the planted-arm log decides at a logged arm; that never hides a DUT event", and "A slip and a corruption in one 64-sample window are both graded in their classes, in either order".
- The `audio.planted-arms` assertion: "where the capture's bytes allow a reading that places an arm, the arm's log decides, never at the cost of another DUT event".
- Round-3 assignment item 3: a slip and a one-word corruption in one window "never void a run whose arms are all present".

**Evidence:** my own encoder throughout, and my standard arms. The sweep is `scripts/r4_arm_corruption_sweep.py`, log `receipts/r4_arm_corruption_sweep.log`:
- One DUT corruption at arm + d, for d from -64 to 64, every channel, and 8 masks.
- **91 of 24,576 placements at another sample are NOT RUN, "void: a planted arm was missed".** All are at d = ±1:
  - d = -1 before a slip arm, with a mask on position bits (`0x200`, `0x1E00`, `0x40000`, `0x80000`, `0x80100`), on any channel. Both ends, drop and repeat arms.
  - d = ±1 beside a flip arm, on its channel. The word and the arm merge into one 2-word `bit-flip` of a combined mask.
- The parent `4d69e192` gives 100 (`receipts/r4_arm_corruption_sweep_parent.log`), so this predates the delta.
- Examples (`receipts/r4_checks.log`, the same at arm tolerance 0 and 2):
  - `0x40000` on channel 0 at 299, before the drop-3 arm at 300, reads `dropped 512` at 299 and `repeated 509` at 300. The arm is missed, and the run is void.
  - The reading "bit-flip `0x40000` at 299, plus the arm" uses the same bytes. That is how the capture was built. It has fewer DUT events and finds every arm.
  - `0x100000` on channel 1 at 699, before the flip arm at 700, reads as `bit-flip` n = 2, mask `0x00100100`. The run is void.
  - At d = -2 and beyond, every case FAILs with the arm found.
- At the arm's own sample (d = 0), 84 of 192 are void. The stated limit (`TESTING.md:1415-1416`) covers only a DUT **slip** at a slip arm's own sample, not a corruption, and not a flip arm.
- The seeded fuzz (`receipts/r4_probe.log`, group R, 6,000 cases of 1 to 3 DUT events) has 27 NOT RUN deviations. Every one has a DUT event within one sample of an arm, or on it, or a cluster of DUT slips around the flip arm.

**Impact:** a DUT corruption within one sample of an arm makes the release run void (NOT RUN) rather than FAIL. That hides a DUT defect behind a re-run, which the new text says the log never does. The event is still listed and the release cannot qualify, so this is fail-safe. The probability per run is small.

**Required outcome:**
- At a logged arm, a one-word corruption beside or on the arm reads as that corruption plus the arm, and FAILs with every arm found.
- Or state the exact exception (d = ±1 and own sample, by arm kind and mask class) in TESTING 6d, REQ-VER-06 and `counter_limits`, narrow the "never hides" and "either order" claims to match, and pin it.

**Verification:**
- `scripts/r4_arm_corruption_sweep.py` reports no non-FAIL at d ≠ 0, or only stated, pinned shapes.
- A self-test arm fails at this head.

### G2 MINOR: Conformance, Robustness, Tests, Docs. A slip shortly before a constant-mask excursion turns the excursion into slips, some about 120 days long

**Where:**
- `tb/tools/torture_campaign.py:4624-4651` (`_hold`). The trailing masked words' XOR is taken against offset 0 (`_audio_due(track, token[1], 0)`), not the offset in force after a slip earlier in the window. This cause sentence is inferred.
- Claims:
  - `REQUIREMENTS.md:412`, "one bit-flip, at any length, beside any one-word event";
  - `TESTING.md:1365`, "an event before them is graded on its own";
  - `TESTING.md:1369`;
  - `AUDIO_COUNTER_LIMITS` `:3753-3755`, "whatever one-word event lies beside it";
  - the assertion text `:3347`.

**Authority:**
- Round-3 F2's required outcome: one bit-flip "whatever one-word event lies within 64 samples of it", or each exception stated exactly.
- The self-test itself treats a planted slip at the excursion's return as in scope (`:8803-8808`).

**Evidence:** `receipts/r4_probe.log` group C, and `receipts/r4_detail.log`.
- **A slip before:** a drop of 3 or a repeat of 2, on every channel, 1 to 63 samples before a 64- to 2,049-word excursion on channel 2. The excursion's masks are ones that decode as another track: `0x100`, `0x40000`, `0x80000`, `0x80100`.
  - **388 of 750 "before" cases misgrade.** At a gap of 64 there are 0. `0x00F00F00` is unaffected.
  - Example: `repeated 2` at 2999, then `0x100` over 3000 to 3099. It reads as `repeated 499717412864` at 3000 and `dropped 499717412864` at 3100.
  - Example: `dropped 3` at 2983, then `0x80000` over 3000 to 3099. It reads as `dropped 1024`, `repeated 2048`, `dropped 1024`.
  - With the slip 64 samples away, the same excursion is one `bit-flip`.
  - The parent gives the same 388 (`receipts/r4_probe_parent.log`), so this predates the delta.
- **An adjacent corruption with no clean word between:** a non-track mask excursion (`0x00F00F00`) absorbs the neighbour into one `bit-flip` of L+1 words, under the excursion's mask. That is 45 of 225 cases, so the neighbour is not "graded on its own". Track-decoding masks at gap 1 and 2 also misgrade near a block boundary; see G3.
- The fixed shapes mostly hold:
  - at `start 3000` with 100 words, 255 of 256 one-word neighbours at gaps 1 to 64 are exact (`receipts/r4_cf_full_export.log`; the exception is in G3);
  - every slip after the return is exact except 6 of 375 for each slip kind, at a block boundary.

**Impact:** the run FAILs. But a corruption is reported as a slip pair. One shape reports about 120 days at 48 kHz, which misdirects diagnosis. This contradicts "beside any one-word event", which this delta added.

**Required outcome:**
- An excursion with one constant mask is one `bit-flip` when a slip lies within 64 samples before it, or when a one-word corruption is next to it.
- Or state each exception exactly (slip before; adjacent word), narrow `REQUIREMENTS.md:412`, `TESTING.md:1365`/`:1369` and `counter_limits`, and pin it.

**Verification:**
- Rerun `scripts/r4_probe.py` unchanged: group C deviates only in stated, pinned shapes.
- A self-test arm fails at this head.

### G3 MINOR: Conformance, Robustness, Tests. Regression: a one-word corruption 1 to 4 samples before a constant-mask excursion now reports a whole-block slip that never returns

**Where:** the delta's new `judge` path in `_audio_excursion` (`tb/tools/torture_campaign.py:4127-4148`, `steer.judge` at `:4146`) and the slip it emits in `_audio_window_events` (`:4311-4315`). It interacts with `_hold` and `_returned`.
- A hint, not a prescribed fix: my probe mutant W11, which never updates `held` at `:3989`, restores the regressed case `C-0x100-L65-b4089-g2-both-flip` (`receipts/mutprobe/compare.log`).

**Authority:**
- `AUDIO_COUNTER_LIMITS` `:3735-3737` and `TESTING.md:1406`: "The cluster's total is exact".
- `AUDIO_COUNTER_LIMITS` `:3732`: "every slip is sized exactly".
- The round-4 brief item (3): the commit's other changes weaken no earlier arm or control.

**Evidence:**
- **The slip totals:** `scripts/r4_net_sweep.py`, the per-channel sum of reported DUT slips against the true net shift, over 7,011 constant-mask cases.
  - **At this head, 270 are unbalanced. At `4d69e192` there are 0** (`receipts/r4_net_sweep.log`, `receipts/r4_net_sweep_parent.log`).
  - Every one has a one-word corruption 1 to 4 samples before the excursion's start.
  - The excursions are `0x100` with a `0x80000` neighbour, `0x80000` with `0x100`, or `0x80100`, including mid-block starts such as 3000.
- **Example** (`receipts/r4_checks.log`): `0x100` at 4085, then `0x80000` over 4088 to 4187, on channel 2.
  - It reads as `dropped 2048` at 4085 (`located_within [4084, 4085]`) and a correct 100-word `bit-flip`.
  - Nothing returns the 2048, so channel 2's reported net is +2048 against a true 0.
  - 5,738 of the words from 4200 to 14,999 contradict a +2048 track. The reading does not match the bytes.
  - In the `0x80100` shape the net is -499717410816.
- **The focused near-boundary sweep** (`receipts/r4_regress_sweep.log` against `receipts/r4_regress_sweep_parent.log`; 3,744 cases: excursions of 64 to 100 words starting 0 to 16 samples before a block boundary, with neighbours 1 to 4 samples away):
  - 1,729 cases improved;
  - **44 regressed from exact at the parent to misgraded here**;
  - 850 misgrade at both.
- The fuzz found one more regression, R-4857 (a corruption on the drop arm's own sample beside a 6291456 slip): void at this head, FAIL at the parent.

**Impact:**
- The verdict still FAILs.
- The event log asserts a permanent 2048-sample (42.7 ms) drop on one channel, or a 120-day slip, that never happened.
- A property the documents call exact now fails where it held before this commit.

**Required outcome:**
- No reading reports a per-channel slip total that differs from the bytes' net shift.
- The near-boundary cases that were exact at `4d69e192` are exact again, or each regression is a stated, pinned limit.

**Verification:**
- `scripts/r4_net_sweep.py` reports 0 unbalanced.
- `scripts/r4_regress_sweep.py` shows no case exact at the parent and misgraded at the head.
- A self-test arm fails at this head.

### G4 MINOR: Tests. Two mutants of the new arm-log code survive the self-test while bringing back R699-3 F1's void

**Where:**
- `tb/tools/torture_campaign.py:4810` (`_audio_arm_found`, flip arm `n == 1`).
- `:4276` (the slip-arm split within `steer.tolerance`).
- Every self-test arm that puts a DUT event beside a planted arm grades with arm tolerance 0:
  - `:8122` (`_independent`), `:8658`, `:8770`;
  - `tests/steps/torture_audio_model.py:37` and `:90`.
- The release plan logs `arm_tolerance_frames: 2` (`:5408`). The only tolerance-2 grading is the clean release fixture (`:8058`, `tests/steps/torture_release_steps.py:535`).

**Authority:**
- AGENTS 6, Tests: "Each new test can fail for the defect it claims to detect".
- The round-4 assignment: "with a test that fails on `4d69e192`".

**Evidence:**
- `receipts/r4_reviewer_mutants.log`: 7 of 14 delta mutants are killed.
- `receipts/mutprobe/compare.log` diffs each survivor against the unmutated planner over my probes.
- **W03** ("a flip arm matches a run of any length"):
  - It passes the self-test.
  - It makes my **unmodified** R699-3 arm-void probe NOT RUN at the end flip arm (16184, k = 1; n = -2048 and 8192, every channel and channel 1).
  - It voids 18 more fuzz cases.
- **W07** ("a slip arm splits only at its exact index"):
  - It passes the self-test.
  - It voids 2 fuzz cases at tolerance 2.
- So the tests protecting F1's fix do not detect the defect in the end flip arm shape on a 16384-frame capture. No arm-interplay test exercises a non-zero tolerance.
- W02, W06 and W10 survive with no status change in any probe. See S2.

**Impact:** a later change could reintroduce F1's void, or break the tolerance paths, with the self-test and the 271-entry mutant table still green.

**Required outcome:** self-test arms (or release mutants) that kill W03 and W07. For example: arm interplay at the release tolerance of 2, and the end flip arm with whole-block slips 1 sample after it on a second capture length.

**Verification:** `scripts/r4_reviewer_mutants.py` kills W03 and W07 at the fixed head.

### R1 RESIDUE: Docs. The reading-choice sentence says "and finds more arms"; the code also takes a reading with fewer DUT events alone

- **Where:**
  - the `_read` docstring `tb/tools/torture_campaign.py:4553-4555`: "Another reading is taken only when it has no more DUT events and finds more arms";
  - the PR body Round 4 F1 row: "Another reading is taken only with no more DUT events and more arms found".
- **What the code does:** `_score` (`:4618-4622`) returns `(dut, -found)`, and `score < best` takes any reading with fewer DUT events, whatever its arm count. `TESTING.md:1356` is accurate.
- **Exact fix:** "Another reading is taken only when it has fewer DUT events, or as many and finds more arms, so it never hides a DUT event." Use it in both places.

### S1 SUGGESTION: Robustness, Docs. Name the coincident DUT slip in the void reason

- The stated limit (`TESTING.md:1415-1416`) voids a run when a DUT slip lands on a slip arm's own sample. `receipts/r4_probe.log` X-A-own-sample-300/500 and 12 fuzz `LIMIT-own-*` cases show it.
- That is honest, but the reason reads only "void: a planted arm was missed".
- Consider adding ", or a DUT slip at its sample" so that a re-run is not taken as a source fault alone.

### S2 SUGGESTION: Tests. Three delta mutants have no observable effect

- W02 (equal-score replacement), W06 (`_hold`'s bit-flip straddle adjustment at `:4644-4646`) and W10 (`_audio_upto` one short) change no status in any of my probes, and pass the self-test.
- W10 changes three `located_within` bounds without leaving the true sample.
- Either pin them, or simplify the code they guard.

### S3 SUGGESTION: Docs. The interrupted-excursion limit is pinned at one site

- `A constant-mask corruption that a slip interrupts reads as the slips its words show` (`TESTING.md:1417`) is pinned only with a planted repeat arm inside a 100-word `0x80000` excursion on channel 1 (`:8809-8812`).
- My probe's `A-ch0/ch1-0x80000x100-spans-repeat` agrees.
- A DUT-slip case would show that the limit is not arm-specific.

## Round-3 findings and the assignment's probes

| Item | Status at `85da3e45` | Evidence |
|---|---|---|
| R699-3 F1 (MINOR): a whole-block slip after a one-word corruption is misgraded, and voids after the flip arm | **Resolved for the shapes named.** See the F1 notes below the table. The test strength is G4. | `receipts/r3_arm_void_probe.log`, `r3_cluster_probe.log`, `r3_classify.log`, `r4_probe.log` group X, `r4_a_detail.log` |
| R699-3 F2 (MINOR): the constant-mask rule beside a one-word corruption, and at a block-boundary return | **Resolved in the probes as run; retained in one case, carried as G3.** See the F2 notes below the table. Wider shapes are G2 and G3. | `receipts/r3_cluster_probe.log`, `r3_probe.log`, `r3_detail.log`, `r4_cf_full_export.log`, `r4_cf_full_parent.log` |
| R699-3 S1 | **Adopted.** `TESTING.md:1380-1382`; the self-test comment at `:8506-8507`. | read at head |
| R699-3 S2 | **Adopted.** Both void reasons at `:5049-5050` and `:5074-5075`; `TESTING.md:1434-1435`. | read at head |
| Brief item (3): the commit's other changes weaken no earlier arm or control | **Arms and controls: met. Behaviour: not met (G3).** See the item (3) notes below the table. | `receipts/r4_mutant_table_diff.log`, `release_mutants_parallel.log`, `r3_reviewer_mutants.log`, `reviewer_mutants_r2.log`, `r4_port_n15.log`, the round-2 probe logs |
| Round-2 and earlier findings | Unchanged by this delta. The round-2 probes' statuses are identical to round 3. | as above |

**R699-3 F1, in detail:**
- The arm-void probe gives 0 not-FAIL in 2,304. Every run FAILs with every arm found.
- FB: 654 of 660 are exact. The 6 others are corruption-then-slip at k = 1 to 4. Their bytes are identical to "that slip alone at the corrupted word", as the stated limit `TESTING.md:1407-1408` says. Group X checks each case's bytes and its `located_within`.
- SB: 258 of 260. The 2 others are `3 then 4096` at +1 and +2, bytes identical to one `dropped 4099` (`TESTING.md:1412-1413`).
- `A-drop4096-5-after-flip` and `-after-repeat` now FAIL with every arm found. The true sample is inside every event's `located_within`.
- r3_probe group A's two NOT RUN are DUT slips on a slip arm's own sample, the stated limit at `TESTING.md:1415-1416`.

**R699-3 F2, in detail:**
- In the probes as run: CF 32 of 32, CB 40 of 40, and M 273 of 273 (it was 270 of 273). `r3_detail`'s `M-0x100-at-6143-n-2049` is one 2049-word `bit-flip`.
- At every gap from 1 to 64, the shape is exact in 255 of 256 cases. It was 0 of 256 at `4d69e192`.
- The exception: `0x100` at 2997 before `0x80000` over 3000 to 3099 reads as an unbalanced `dropped 2048`. That is G3's regression.

**Item (3), in detail:**
- The mutant table grows from 249 to 271 entries. None was removed. Four are re-anchored to rewritten code, as equivalent defects.
- All 271 are killed, and the export is unchanged.
- The one changed self-test arm, `test_audio_slip_and_corruption_share_a_window` `:8623-8633`, takes its limit branch only after asserting byte identity. Within that branch it still asserts the flip, the sizes and the location.
- My round-3 delta mutants give 13 killed and 3 invalid: V07, V09 and V13, whose code was rewritten. Each has an equivalent that is killed: the author's re-anchored "held excursion kept through a word off its mask", my W13, and the author's "half-block alternative dropped".
- My round-2 mutants give 31 killed and 1 invalid (N15). Ported to the new `_audio_slip`, N15 is killed by 5 tests (`receipts/r4_port_n15.log`).
- The round-2 probes' statuses are identical to round 3: compound, arm interaction (A1 is NOT RUN only by the 24 h rule), edge, throughput, grader, ported grader, and N07 at 8214.

## Documents and the comment rule

- REQ-VER-06, TESTING 6d, `counter_limits`, the assertion texts and the PR body follow every change, except the claims G1 and G2 falsify and R1's wording.
- The stated limits I could check byte-for-byte hold, in group X:
  - corruption made the new track's;
  - slip of their sum;
  - DUT slip at an arm's own sample.
- Comment rule: none of the 968 added lines contains a lane label, round, reviewer ID or comment ID (pattern scan over the delta's added lines). There is no new RESIDUE of that kind.

## Gates (exact head; all rc 0 unless stated)

| Gate | Result |
|---|---|
| `torture_campaign.py --self-test` | 112 tests OK |
| Release mutant table, in parallel with the driver's criteria (`scripts/release_mutants_parallel.py`) | 271 killed, 0 survived, 0 invalid; export unchanged |
| `cd tests && behave --no-capture -f plain` (clone, no bytecode) | 14 features, 495 scenarios, 2286 steps passed |
| Plan feature | 176 scenarios, 665 steps |
| `docs_check.py` | 0 findings over 210 md files |
| `gen_toc.py --check` | OK |
| `gen_toc.py --verify-anchors` | 538 anchors |
| `check_em_dash.py --base e76a755a` | 0 findings over 400 lines |
| `check_em_dash.py --base 4d69e192` | 0 findings over 44 lines |
| `check_doc_style.py` | OK |
| `check_doc_paths.py` | 1065 paths |
| `check_py_idiom.py` | Within budget |
| `check_feature_status.py` and `--self-test` | 0 findings |
| `--coverage-by-area --areas soak,audio,power` | Complete |
| `git diff --check` from `4d69e192` and from `e76a755a` | Clean |
| Reviewer delta mutants (`scripts/r4_reviewer_mutants.py`) | 7 of 14 killed, control passing (G4, S2). The script exits 0; survivors are findings, not errors. |

The Markdown gates ran under the hash-locked renderer pin (`tools/markdown/requirements.txt`: cmarkgfm 2025.10.22, html5lib 1.1) in a private venv.

**Author evidence, spot-checked** (`receipts/author_r4_spotcheck.log`):
- The evidence commit `fdbd536f` is unsigned at the git level.
- All 121 rows of `author-r4/receipts/INDEX.md` match their bytes and sha256.
- `head.txt` names this head, tree, parent, base and gitlinks.
- `rc.txt` is all 0.
- The self-test reads 112 OK, and the release mutants read 271 killed.
- The author's reruns of my R699-3 probes match mine: arm-void 0 of 256 per size, FB/SB/CF/CB the same counts.

**Hosted, inspected only** (`receipts/hosted_checks.log`, 54 check runs at this exact head when read):
- 43 succeeded, including `rtl-fast`, `docs-check`, `docs-check-no-git` and `bdd-conformance`.
- 9 were in progress (Verilator shards and "Fail fast across this head") and 1 was queued ("Collect CI manifest").
- "Physical gPTP (nightly and manual)" was skipped. That is not hardware proof.
- `verilator-suites` and `yosys-portability` had not concluded. The manager owns hosted and replica acceptance.

## Lens coverage

[R699] PASS RTL - `receipts/rtl_scope.log`: `git diff --stat 4d69e192..85da3e45` and `e76a755a..85da3e45` over `hdl sw protocol-processor gptp-processor external third_party syn constraints` are both empty. The index gitlinks equal HEAD, and the top-level three equal base `efeb541a`/`55680bff`/`ed211803`. `audio_counter_word` (`tb/tools/torture_campaign.py:3774`) is identical to `4d69e192`. So there is no RTL, firmware or submodule in the delta, and the S32 counter layout is unchanged.

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (G1, G2, G3) | REQ-VER-06 `REQUIREMENTS.md:402-445`; round-4 assignment items 1-2 and brief item 3; grader `tb/tools/torture_campaign.py:3929-3995, 4083-4350, 4407-4700, 4805-4812`; assertion texts `:3344-3364`; `receipts/r3_*`, `r4_probe.log`, `r4_arm_corruption_sweep.log`, `r4_net_sweep.log` | R699-4 | `85da3e4595871c1573c28b4d040b9e98463a41c9` |
| RTL | CLEAN | Empty RTL/firmware/submodule diff; gitlinks; S32 layout (`receipts/rtl_scope.log`) | R699-4 (delta); R699-1 for the rest | `85da3e4595871c1573c28b4d040b9e98463a41c9` |
| Robustness | UNCLEAN (G1, G2, G3) | Arm-adjacent sweep (24,768); constant-mask neighbour sweep C (3,375); near-boundary sweep (3,744 at head and parent); slip-total sweep (7,011 at head and parent); seeded fuzz R (6,000 at head and parent); F2(a) every-gap sweep (256 at head and parent); round-3 probes unmodified; round-2 probes unmodified | R699-4 | `85da3e4595871c1573c28b4d040b9e98463a41c9` |
| Tests | UNCLEAN (G1, G2, G3, G4) | Self-test arms `:8596-8633, 8661-8825`; `tests/features/torture_campaign_plan.feature:513-557`; `tests/steps/torture_audio_model.py`; `tests/steps/torture_release_steps.py`; `receipts/release_mutants_parallel.log` (271); `r4_mutant_table_diff.log`; `r4_reviewer_mutants.log` (14); `mutprobe/compare.log`; `r3_reviewer_mutants.log`; `reviewer_mutants_r2.log`; `r4_port_n15.log` | R699-4 | `85da3e4595871c1573c28b4d040b9e98463a41c9` |
| Docs | UNCLEAN (G1, G2) | REQ-VER-06 `:409-433`; TESTING 6d `:1338-1440`; `AUDIO_COUNTER_LIMITS` `:3731-3766`; the `_read` docstring; the PR body Round 4 section and audio row; docs gates | R699-4 | `85da3e4595871c1573c28b4d040b9e98463a41c9` |

## Real limits

- **Source validation only.** Gates and probes ran in the isolated clone and in `git archive` exports of the exact head and of `4d69e192`, which is used only for the before-and-after comparisons. No manager source bank ran at this head, and none is claimed or inferred. The current-dev merge candidate (base `e76a755a`, live dev `76de691e`) is not validated here.
- **No physical evidence.** Physical calibration was NOT RUN. The bench soak, the audio run and the power campaign are part B. Field skips are not hardware proof.
- **Synthetic captures only.** All classification evidence comes from synthetic captures built with my own encoder (`scripts/r3_probe.py`). No real capture was graded.
- **Causes are inferred.** G2's and G3's cause sentences are inferred from outputs, code and the W11 probe mutant. The required outcomes do not depend on them.
- **Pre-existing shapes.** G1 and G2 predate the delta. They are findings here because this delta's text claims them.
- **The fuzz is not exhaustive.** It is seeded (396004) and samples the space.

## Pending manager duties

- Route G1 to G4, R1 and S1 to S3 to the executor.
- Build and validate the current-dev merge candidate (builder and native banks), and link the receipts.
- Hosted and replica acceptance at the final head. `verilator-suites` and `yosys-portability` were still running at this head when read.
- Carried over:
  - record owner decision 6409128703 in the plan;
  - ratify `restore_bound_s = 30`;
  - complete the external review at the final head.

## Other reviewer's round-3 findings

R700-3 (PR comment 6416855079) is POSITIVE at `4d69e192`. I read it after the sections above were written, and it changes none of them. Its only finding is an optional suggestion.

| Finding | Status at `85da3e45` | Evidence |
|---|---|---|
| R700-3 S1 (SUGGESTION, Tests/Docs): pin two compound ambiguities | **Adopted in part; optional.** See the notes below the table. | `receipts/r4_r700_s1.log` |

**R700-3 S1, in detail.** Both byte equalities hold with my own encoder, and both runs FAIL with every arm found.
- **Drop 4096 at 3000 plus `0x100` at 3001:**
  - It reads as one `dropped 4096`, located `[3002, 3005]`. That reading has the bytes of the equal drop at 3005.
  - The general cluster and whole-block limits cover it, but there is no named equality control.
- **Drop 4096 at 3000 plus `0x80000` at 3001:**
  - It now reads as `dropped 4096` and a one-word `bit-flip 0x80000`. That is the new stated limit at `TESTING.md:1396-1397`.
  - The half-block arm of `test_audio_block_slip_after_a_corruption_or_a_slip` pins it.

R700-3's resolutions of the round-2 findings concern code this delta does not reverse. My unmodified round-2 probes agree with them (above).

## Receipts

Every publishable file is listed in `MANIFEST.sha256`.
- **Round-3 scripts:** under `scripts/` and `scripts/port/`, byte-identical to my R699-3 manifest.
- **New round-4 scripts:**
  - `r4_probe.py` and `r4_detail.py`;
  - `r4_arm_corruption_sweep.py`, `r4_regress_sweep.py` and `r4_net_sweep.py`;
  - `r4_checks.py`, `r4_a_detail.py`, `r4_cf_full.py` and `r4_r700_s1.py`;
  - `r4_reviewer_mutants.py`, `r4_mutant_probe.py` and `r4_mutant_probe_groups.py`;
  - `r4_mutant_table_diff.py` and `r4_port_n15.py`.
- **Raw logs and return codes:** under `receipts/`. `receipts/mutprobe/` holds the per-mutant probe logs, and `*_parent.log` files hold the same probe run against `4d69e192`.
- `r4_mutant_probe.py` is the single-mutant wrapper. The published per-mutant logs come from `r4_mutant_probe_groups.py`, run on each mutated copy, and `receipts/mutprobe/compare.log`.

The review clone was never modified. `receipts/restore_check.log` shows:
- HEAD, tree and index tree all match;
- porcelain and diff-index are empty, and there is no `__pycache__`;
- all six gitlinks are intact;
- the four changed tool and step files are mode 100644, with blobs equal to HEAD;
- the export's planner blob `f4a0f6e6` equals `HEAD:tb/tools/torture_campaign.py`, and the parent export's `300919bc` equals `4d69e192`'s.

R699-4 FINISHED
