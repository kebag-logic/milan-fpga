[R699] NEGATIVE - exact head 4d69e1923ce8209029af6e084336f13cca834c29

# R699-3: internal cleared-context delta review of PR #786 (issue #396 part A)

- **Head:** `4d69e1923ce8209029af6e084336f13cca834c29`, tree `55e22fe10172e2965687b6fbab734cab19fe183d`.
- **Delta reviewed:** `a3e24ac5..4d69e192`, two commits by the round-3 executor (`9da26126`, `4d69e192`). Six files changed: REQUIREMENTS.md, TESTING.md, the planner, the release mutant driver, the plan feature and its steps. There is no RTL, firmware, builder or submodule change. Source base is dev `e76a755a`.
- **Reconstructed from:**
  - AGENTS.md and CONTRIBUTING.md;
  - the round-3 assignment (issue #396 comment 6413452035);
  - the executor's TAKEN and REVIEW READY comments;
  - REQ-VER-06 (REQUIREMENTS.md:402-445) and TESTING 6d;
  - the diff;
  - the author's round-3 receipts at `a1ee144d` `review-evidence/396g-r1/author-r3`;
  - the exact-head hosted check runs.
- **Prior findings:** I read the prior public findings (R700-2, PR comment 6413374622) only after my own pass. My round-2 report is my own earlier output.
- **Scope rule:** my round-2 ledger stands for code this delta does not touch.

## Verdict

The verdict is **NEGATIVE**. Two MINOR findings are open, both under Conformance, Robustness, Tests and Docs. There is no BLOCKER, MAJOR or RESIDUE. RTL is clean.

Most of the delta is right:
- **The qualified interval** (R700-2 F1, items 1 and 4) holds in 1,818 independent boundary cases.
- **The acquisition boundary** (R699-2 F3, item 5) is tested, and N07 is killed.
- **The invalid-anchor commit** (item 6) makes that arm stricter.
- **Mutants:** all 249 author mutants and all 16 of my new delta mutants are killed.

The open findings concern the two compound rules this round claims are now uniform:
- **F1:** a one-word corruption, the planted flip arm included, followed within 64 samples by a whole-block slip is misgraded. It voids the run in up to 254 of 256 placements.
- **F2:** the constant-mask rule still breaks in two shapes:
  - when a one-word corruption sits within 64 samples of a long excursion;
  - when a code-bit corruption covering a whole block ends on a block boundary.

## Findings

### F1 MINOR: Conformance, Robustness, Tests, Docs. A whole-block slip within 64 samples after a one-word corruption is misgraded; after the planted flip arm it voids the run

This retains R699-2 F1 in part. The round-2 cases are fixed; this is their mirror image.

**Where:**
- `tb/tools/torture_campaign.py:3945-3955`: `_audio_labels` takes the longest single-offset run from each word.
- `:3960-3977`: `_audio_candidates` offers only offsets near `reference` (the last fitted offset) and `final`, not the offset in force before the departure.
- Claims:
  - `docs/testing/TESTING.md:1343-1346`: "a slip and a corruption in one window are both graded … one corrupted word never hides the slips beside it, and arms may be planted closer than 64 samples";
  - `REQUIREMENTS.md:413`;
  - the docstring at `tb/tools/torture_campaign.py:3910-3912`;
  - the PR body's Round 3 row for R699-2 F1.

**Authority:**
- Round-3 assignment item 3: "A slip and a one-word corruption in one 64-sample window are both graded, and they never void a run whose arms are all present".
- REQ-VER-06: every discontinuity is classified at its sample.
- TESTING 6d: `located_within` "gives the samples it may have happened at".

**Evidence:** all from my own independent encoder (`scripts/r3_probe.py`), never the planner's synthesizer.

1. **Void runs** (`receipts/r3_arm_void_probe.log`). A DUT slip at arm + k (k = 1 to 64) after either planted flip arm (index 700 or F-200, channel 1, mask `0x100`), on every channel or on channel 1 alone. The run is **NOT RUN, "void: a planted arm was missed"** in:

   | DUT slip size | Void placements |
   |---|---|
   | +4096 | 254 of 256 |
   | -4096 | 128 of 256 |
   | +8192 | 128 of 256 |
   | -2048 | 130 of 256 |
   | 1, 3, -2, 100 and +2048 | 0 of 256 |

   Example (`receipts/r3_detail.log`, `A-drop4096-5-after-flip`): a 4096 drop at 705. Channel 1 reports `dropped 4096` at 700 (the arm's index) and `bit-flip` at 704. The arm is lost.

2. **Misgrading with an ordinary DUT corruption** (`receipts/r3_cluster_probe.log`, group FB; tallies in `receipts/r3_classify.log`). A one-word corruption on channel 2 at 3000 (mask `0x100` or `0x80000`), then a whole-block slip of ±2048, ±4096 or 8192 at 3000 + k:
   - 433 of 660 cases deviate, across k = 1 to 64.
   - In 217 of them the corruption is not reported at its sample. It is absorbed into the slip, which moves to the corruption's index, up to 50 samples early. Phantom `0x100` bit-flips are added in 186 of those.
   - 413 place the slip outside its stated location. For example, `FB-0x100-then-4096-at+5` reports channel 2's drop at 3002 with no `located_within`.
   - At k = 64 and over, every case is exact.
3. **The same mislocation after a planted drop or repeat** (group SB). A 3-sample drop or 2-sample repeat at 3000, then a ±4096 slip within 64 samples: 89 of 260 cases report the block slip at a sample its event excludes. In `A-drop4096-5-after-repeat` the slip at 505 is reported at 502, with no `located_within`. That verdict is FAIL with the arm found.

The documented cluster limit (TESTING.md:1379-1381) allows smallest sizes and code-bit `bit-flip`s inside a cluster. It does not allow:
- a corruption to vanish into a slip;
- a slip to be reported at a sample it was not at, without bounds;
- an arm to be lost.

These follow from the greedy longest-run fit: once a wrong offset is fitted, the offset in force before the excursion is no longer a candidate.

My round-2 probes did not catch this because they put the slip before the corruption. They now pass unmodified: compound 30 of 30 OK, and A2/A3 FAIL with the arm found.

**Impact:**
- A DUT whole-block slip within about 1.3 ms after a planted flip arm makes the release run void (NOT RUN), not FAIL. That hides a DUT defect behind a re-run, which is the outcome item 3 forbids.
- Elsewhere the verdict stays FAIL, but corruptions disappear or are invented, and slips are placed outside their stated bounds. That misdirects diagnosis.
- Nothing PASSes falsely.

**Required outcome:**
- A whole-block slip after a one-word corruption, or after a short slip, within 64 samples is graded in its class: the corruption at its sample, and the slip with a location that contains its sample.
- A DUT slip of any size beside any planted arm FAILs with every arm found.
- If some part is bit-identical, state that limit exactly in TESTING 6d, REQ-VER-06 and `counter_limits`, and pin it, rather than claiming "never hides".

**Verification:** rerun these unchanged:
- `scripts/r3_arm_void_probe.py`: no NOT RUN line.
- `scripts/r3_cluster_probe.py`: groups FB and SB OK, or each deviation covered by a stated, pinned limit.
- A new self-test arm fails at this head.

### F2 MINOR: Conformance, Robustness, Tests, Docs. The constant-mask rule still changes in two shapes

This retains R700-2 F2 in part.

**Where:**
- `tb/tools/torture_campaign.py:4338-4343`: `_step` releases a held excursion on any followed word whose XOR with the old track is not the mask. That includes a word exactly on the old track, which is the return itself.
- `:4386-4410`: `_close` adopts or releases the hold only on a window whose every word shares the one mask.
- Claims:
  - `REQUIREMENTS.md:412`, "one bit-flip, at any length";
  - `TESTING.md:1340`, `:1348-1351`, `:1371`;
  - `AUDIO_COUNTER_LIMITS` at `tb/tools/torture_campaign.py:3734-3735`;
  - the assertion text at `:3347`;
  - the PR body's R700-2 F2 row.

**Authority:**
- Assignment item 2: "One rule for constant-mask corruption at every length … An unqualified exact-class claim must not change silently".
- TESTING.md:1350: "If the words return to the old track, the whole excursion is one `bit-flip`."

**Evidence** (`receipts/r3_cluster_probe.log`, `receipts/r3_detail.log`):
- **(a) A neighbouring one-word corruption** (group CF). A 100-word `0x80000` or `0x40000` excursion on channel 2, plus one `0x100` word 1 to 64 samples before its start or after its end, reads as **`dropped 1024`/`repeated 1024`** (or 512): 28 of 32 cases. At 70 samples it is exact. With the planted flip arm as the neighbour (`A-ch1-0x80000x100-ends-5-before-flip`), the verdict is FAIL with the arm found, and the class is a slip pair.
- **(b) A code-bit corruption over a whole block that ends on a block boundary** (group CB). XOR `0x100` from 5000, 6100, 6143 or 6144 to 8192, 10240 or 12288 reports `repeated 499717421056` and the matching `dropped` at the return, located `[8192, 8194]`. For more than one block, it also reports `repeated 4096` at each block boundary. 12 of 12 cases.
  - The same corruption ending 1 to 50 samples later is one exact `bit-flip`: 28 of 28.
  - The return's `located_within` shows the first returned words also fitting the held track, so the per-word release at `:4341` fires on the return.

The interior constant-mask sweep itself passes. Masks `0x100`, `0x80000`, `0x40000`, `0x200`, `0x00F00F00`, `0x80100` and `0x1` over 2 to 4097 words, at three start points, chunked and both byte orders, give 270 of 273 exact. The 3 failures are the CB shape. So R700-2 F2's 64-sample switch is fixed.

**Impact:** the run FAILs. But a corruption, the hold's own target, is reported as a slip pair: 1024 samples in (a), and about 120 days at 48 kHz in (b). That contradicts the "at any length" rule in two documented places, and neither shape is tested or stated as a limit.

**Required outcome:**
- A return to the old track never releases a hold as slips.
- An excursion with one constant mask is one `bit-flip` whatever one-word event lies within 64 samples of it.
- Or state each exception exactly in TESTING 6d, REQ-VER-06 and `counter_limits`, and pin it.

**Verification:**
- Rerun `scripts/r3_cluster_probe.py` unchanged: groups CF and CB OK, or each deviation a stated, pinned limit.
- A self-test arm fails at this head.

### S1 SUGGESTION: Docs. A slip just inside the interval's end may still be `unresolved`

A whole-block slip at F-64 to F-66 lies inside the qualified interval. It can still read as `unresolved` (`receipts/r3_probe.log`, 6 rows). That happens because fewer than 64 clean samples follow its first differing code bit. This matches TESTING.md:1382-1383 and still FAILs. The self-test comment "With guard samples the same slip is sized exactly" and the PR body's "with and without guard samples" read as if the guard always gives an exact class. One sentence could say that the interval decides what is proved clean, not which class a slip near the end receives.

### S2 SUGGESTION: Robustness, Docs. A channel the DUT never drives reads as a layout error

A counter channel that never acquires is NOT RUN, with the reason "check the layout and byte order". That covers the case where the DUT outputs nothing valid on one channel for the whole run. The release still cannot qualify, so this is fail-safe. Consider naming the DUT possibility in the reason or in TESTING 6d.

## Prior findings at this head

| Finding | Status at `4d69e192` | Evidence |
|---|---|---|
| R700-2 F1 (MAJOR): capture-boundary slips earn PASS | **Resolved.** See the R700-2 F1 notes below the table. | `receipts/r3_probe.log`, groups E and S; `receipts/edge_probe_r2.log`; `receipts/r3_reviewer_mutants.log` V01 to V06, V11, V12 and V14 |
| R700-2 F2 (MINOR): constant-mask rule changes at 64 | **Resolved at the stated lengths; retained in part as F2.** 63, 64, 65, 100 and 2000-word excursions are one `bit-flip`, chunked and in both byte orders. So is the round-2 reproducer (`0x100` at 3000 to 3099). | Group M, 270 of 273 |
| R699-2 F1 (MINOR): slip and one-word corruption in one window | **Resolved for every round-2 case; retained in part as F1** (corruption first, then a whole-block slip). | See the R699-2 F1 notes below the table. |
| R699-2 F2 (MINOR): whole-block slip in the last 63 samples | **Resolved.** X1 at F-20 to F-63 reads `unresolved`, mask `0x100`, with `located_within` holding the slip. F-64 is exact. X4 (a logged loss at F-30) is NOT RUN by name. | `receipts/edge_probe_r2.log` |
| R699-2 F3 (MINOR): N07 survives | **Resolved.** | See the R699-2 F3 notes below the table. |
| R699-2 S1 to S4 | **All adopted and verified.** See the suggestion notes below the table. | `receipts/throughput_misuse_r2.log` |
| Round-1 findings | Unchanged by this delta. The round-1 cases in `grader_probe_r2.py` remain OK. | `receipts/port_grader_probe_r2.log` |

**R700-2 F1, in detail:**
- Each verdict states `qualified`. It runs from 63 samples after the last acquisition to F-63, with frames, seconds, acquisition span and unobserved frames.
- PASS needs `required_s` observed seconds (86400 by default). Losses are not counted.
- An arm or a loss outside the interval is NOT RUN by name.
- 648 end cases and 1170 start cases were run: ±2048, ±4096, 8192 and 6291456, k = 1 to 130, both byte orders, with 7-byte and 113-byte chunks. Every undetected slip lies outside the interval with a PASS that proves only the interval.
  - Every detected boundary slip is `unresolved` with a location that holds it, or exact inside the interval.
  - The 13 E-group deviations are my probe's over-strict expectation (F-64 to F-66, see S1), plus the F-150 rows, which are F1.
- The author's pinned endpoint pair `f395a643…` is in `test_audio_boundary_block_slips_are_unresolved`.

**R699-2 F1, in detail:**
- `compound_probe_r2.py`, unmodified: 30 of 30 OK.
- `arm_interaction_probe_r2.py`, unmodified:
  - A2 to A5 FAIL with every arm found;
  - A1 is NOT RUN only by the 24 h rule;
  - ported to pass `required_s`, A1 PASSes at 10, 40 and 63 apart.

**R699-2 F3, in detail:**
- `reviewer_mutants_r2.py`, unmodified: 32 killed, 0 survived, 0 invalid.
- The author's matching mutant is killed by `test_audio_capture_losses_advance_the_clocks`.
- The N07 probe reports 8214.

**R699-2 S1 to S4, in detail:**
- **S1:** the "start once the counter flows" rule is in TESTING.md:1394-1397.
- **S2:** `anchor_gaps` is in every verdict; V15 is killed.
- **S3:** a channel not acquired within 65536 frames is refused in 0.87 s.
- **S4:** the bound is documented.

## The brief's items

1. **Qualified interval.** Met; see R700-2 F1 above. The run passes only with at least `required_s` observed seconds in the interval: V05, the off-by-one mutant, is killed. An unobservable tail is never proved clean. Boundary whole-block slips are `unresolved` with and without guards, in both byte orders, chunked.
2. **One constant-mask rule at every length.** Met at every length. **Not met** next to a one-word event, or at a block-boundary return (F2).
3. **Slip and one-word corruption in one window.** Met when the slip comes first, and for non-block slips either way. **Not met** for a whole-block slip after the corruption, and the run can be void (F1).
4. **Whole-block slip in the last 63 samples.** Met.
5. **"At or before" boundary.** Met. The test is at `tb/tools/torture_campaign.py:8014`, and N07 fails it.
6. **Invalid-anchor commit `4d69e192`.** Met. With the 24 h default, every anchor case was NOT RUN for the length reason, so the arm was vacuous. The arm now passes `required_s` and asserts each defect's exact refusal reason. It adds a valid-anchor PASS control and one new case (wall time equal to the start). Every assertion is equal or stricter; no earlier arm is weakened.
   - I checked every other `NOT RUN` assertion in the audio self-tests: each passes `required_s` (`_grade`, `_independent`, explicit calls), or asserts the reason.
   - Author mutants N30 and N31 are killed.

**Documents follow:**
- REQ-VER-06, TESTING 6d, the assertion texts, `qualification`, `counter_limits`, `capture_start` and the PR body follow every change, except F1's and F2's claims.
- No new comment-rule residue was found: no lane label, round, reviewer ID or comment ID in the delta's added lines.

## Gates (exact head, all rc 0)

| Gate | Result |
|---|---|
| `torture_campaign.py --self-test` | 108 tests OK |
| `torture_release_mutants.py` table, run in parallel with the driver's criteria (`scripts/release_mutants_parallel.py`) | 249 killed, export unchanged. The serial driver exceeds the 10-minute foreground limit here. |
| `cd tests && behave --no-capture -f plain` (clone, no bytecode) | 14 features, 481 scenarios, 2244 steps passed |
| Plan feature | 162 scenarios, 623 steps |
| `docs_check.py` | 0 findings over 210 md files |
| `gen_toc.py --check` | OK |
| `gen_toc.py --verify-anchors` | 538 anchors |
| `check_em_dash.py --base e76a755a` | 0 findings over 361 lines |
| `check_em_dash.py --base a3e24ac5` | 0 findings over 69 lines |
| `check_doc_style.py` | OK |
| `check_doc_paths.py` | 1065 paths |
| `check_py_idiom.py` | Within budget |
| `check_feature_status.py` and `--self-test` | 0 findings |
| `--coverage-by-area --areas soak,audio,power` | Complete |
| `git diff --check e76a755a HEAD` | Clean |
| Reviewer delta mutants (`scripts/r3_reviewer_mutants.py`) | 16 of 16 killed, control passing |

The Markdown gates ran under the pinned renderer (`tools/markdown/requirements.txt`, hash-locked) in a private venv. A first behave run in the export errored only because the export lacks the gPTP submodule. It is not a receipt.

**Author evidence, spot-checked.** The evidence commit `a1ee144d` is unsigned at the git level. Four receipts match the published `INDEX.md` sha256 (`receipts/author_r3_spotcheck.log`):
- `rc.txt` is all 0;
- `selftest.log` reads 108 OK;
- `release_mutants.log` reads 249 killed;
- my unmodified round-2 mutants read 32 killed.

`head.txt` names this head and tree. My own reruns agree.

**Hosted, inspected only** (`receipts/hosted_checks.log`): 64 contexts succeeded at this exact head, including `rtl-fast`, `verilator-suites`, `yosys-portability`, `bdd-conformance`, `docs-check` and `docs-gates-*`. One was skipped: "Physical gPTP (nightly and manual)", which is not hardware proof. The manager owns hosted and replica acceptance.

## Lens coverage

[R699] PASS RTL - `git diff --stat e76a755a..4d69e192 -- hdl sw protocol-processor gptp-processor external third_party` (empty); index gitlinks equal HEAD and the top-level three equal base `efeb541a`/`55680bff`/`ed211803` (`receipts/restore_check.log`) - no RTL, firmware or submodule in the delta; the S32 counter layout (`tb/tools/torture_campaign.py:3661-3690`) is unchanged.

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | REQ-VER-06 `REQUIREMENTS.md:402-445`; round-3 assignment items 1 to 6; grader `tb/tools/torture_campaign.py:3688-3743, 3901-4500, 4648-4803`; assertion texts `:3323-3384`; `receipts/r3_probe.log`, `r3_cluster_probe.log`, `r3_arm_void_probe.log` | R699-3 | `4d69e1923ce8209029af6e084336f13cca834c29` |
| RTL | CLEAN | Empty RTL/firmware/submodule diff; gitlinks; S32 layout | R699-3 (delta); R699-1 for the rest | `4d69e1923ce8209029af6e084336f13cca834c29` |
| Robustness | UNCLEAN (F1, F2) | Boundary sweeps (E 648, S 1170), mask sweep (M 273), arm interplay (A 29, V 2304), cluster sweeps (FB 660, SB 260, CF 32, CB 40); misuse throughput; round-2 probes unmodified and ported | R699-3 | `4d69e1923ce8209029af6e084336f13cca834c29` |
| Tests | UNCLEAN (F1, F2) | Self-test `:8105-8331` and the anchor arm `:8035-8052`; plan feature `:477-516` and steps; `receipts/release_mutants_parallel.log` (249); `receipts/reviewer_mutants_r2.log` (32); `receipts/r3_reviewer_mutants.log` (16) | R699-3 | `4d69e1923ce8209029af6e084336f13cca834c29` |
| Docs | UNCLEAN (F1, F2) | REQ-VER-06 `:409-433`; TESTING 6d `:1272-1440`; plan `qualification`/`counter_limits`/`capture_start`; PR body Round 3 section | R699-3 | `4d69e1923ce8209029af6e084336f13cca834c29` |

## Real limits

- **Source validation only.** Gates and probes ran in an isolated clone and a `git archive` export of the exact head. No manager source bank ran at this head, and none is claimed or inferred. The current-dev merge candidate (base `e76a755a`, live dev `76de691e`) is not validated here.
- **No physical evidence.** Physical calibration was NOT RUN. The bench soak, the audio run and the power campaign are part B. Field skips are not hardware proof.
- **Synthetic captures only.** All classification evidence comes from synthetic captures built with my own encoder. No real capture was graded.
- **Root causes are inferred.** F1's and F2's root-cause sentences are inferred from the observed outputs and the code. The required outcomes do not depend on them.

## Pending manager duties

- Route F1 and F2, with S1 and S2, to the executor.
- Build and validate the current-dev merge candidate (builder and native banks), and link the receipts.
- Hosted and replica acceptance at the final head.
- Carried over:
  - record owner decision 6409128703 in the plan (AECP REBOOT; sine-pair limits);
  - ratify `restore_bound_s = 30`;
  - complete the external review at the final head.

## Receipts

Every publishable file is listed in `MANIFEST.sha256`:
- **Round-2 scripts:** under `scripts/`, byte-identical to my round-2 manifest.
- **The `required_s` port:** `scripts/port/grader_probe_r2.py`. Its only change is a short shim that passes `required_s`.
- **New round-3 scripts:**
  - `r3_probe.py`, `r3_cluster_probe.py`, `r3_arm_void_probe.py`, `r3_detail.py` and `r3_classify.py`;
  - `r3_reviewer_mutants.py` and `release_mutants_parallel.py`.
- **Raw logs and return codes:** under `receipts/`.

The review clone was never modified. `receipts/restore_check.log` shows:
- HEAD, tree and index tree all match;
- porcelain and diff-index are empty;
- all six gitlinks are intact;
- the export's planner blob `300919bc` equals `HEAD:tb/tools/torture_campaign.py`.

R699-3 FINISHED
