[R699] NEGATIVE - exact head 21faa48242e021177a1dc702f28e51347c6a7a57

# R699-1: internal cleared-context review of PR #786 (issue #396 part A)

- **Head:** `21faa48242e021177a1dc702f28e51347c6a7a57`, tree `dff7043fb74a2b30bca12bc48fa9e7d6fafd3296`.
- **Base:** dev `e76a755afc0536453161e3cd33f6f4d2dcd7641f`.
- **Delta:** one commit, 9 files. No RTL, firmware, builder or submodule change.
- **Executor:** [A674]. This reviewer: [R699], internal, cleared context.
- **Reconstructed from:**
  - AGENTS.md and CONTRIBUTING.md.
  - Issue #396's body and comments: owner decisions 6408072465, assignment 6408079016, audio signal design 5978644444, and the `mr`/`tu` rule 5857762351 as corrected by 5857765949.
  - REQUIREMENTS.md section 8 and #70's eight-item inventory.
  - The extracted text of Milan v1.2 and IEEE 1722-2016.
  - The diff `e76a755a..21faa482`.
  - The author's published receipts at `080e38fb` `review-evidence/396g-r1`.
  - The exact-head hosted check runs.
- **Prior findings:** PR #786 had no prior review findings at this head. Its only comments are the two review-start notices.

The verdict is **NEGATIVE**. Three MINOR findings are open:

- F1 under Conformance, Robustness and Tests;
- F2 under Tests;
- F3 under Docs and Tests.

One RESIDUE and three SUGGESTIONs are recorded as well. No BLOCKER or MAJOR was found. The RTL lens is clean.

## Findings

### F1 MINOR: Conformance, Robustness, Tests. The grader misclassifies compound and edge events, and a static swap voids the run

**Where:** `tb/tools/torture_campaign.py:3681-3843` (`_CounterScan`, used by `grade_audio_counter_capture` at `:3938`).

**Authority:**
- The audio signal design (issue #396 comment 5978644444) item 1, restated in REQ-VER-06 (REQUIREMENTS.md "Each discontinuity is classified at its sample"): every discontinuity is classified exactly at its sample, as n dropped, n repeated, n samples of silence, a bit-corruption mask or a channel swap.
- The design's stated purpose is "so a later investigation can name the source of any error".
- The plan's own assertion is `audio.counter-classified` (`:3332`).

**Evidence:** a reviewer-owned generator that does not use the planner's synthesizer (`scripts/grader_probe.py`, `scripts/grader_probe2.py`, receipts `receipts/grader_probe.log` and `receipts/grader_probe2.log`).

The canonical isolated events all classify exactly, with index, size, mask and partner right:
- drops of 1 to 2047;
- repeats of 1 to 2048;
- replaced and inserted silence;
- single-word flips in the pad, sign and counter bits;
- a mid-run swap, and a swap that runs to the end of the capture;
- little-endian captures and chunked input.

These cases do not:

| Probe | Input | Grader reports | Design class |
|---|---|---|---|
| `Q-dup-then-skip-k1` | One-sample hold, then a skip at once: `c-1` received for `c`, then `c+1` | `bit-flip` mask `0x00000300`, every channel | 1 repeated, then 1 dropped |
| `Q-skip-then-dup-k1` | A skip, then a hold at once | `bit-flip` mask `0x00000100` | 1 dropped, then 1 repeated |
| `P3-flip-0x00100000`, `Q-tag-flip-nonreciprocal` | One-bit flip in the channel-number field of one channel; the partner keeps its own word | `swap`, partner 1 | `bit-flip`, mask `0x00100000` |
| `P4-burst-0x00000100x2`, `x3`, `P4-burst-0x00000200x2` | A 2- or 3-sample corruption confined to counter bits | Chains of `dropped`/`repeated`, plus one `bit-flip` with mask `0x00001E00` | One `bit-flip` with n = 2 or 3 and its mask |
| `Q-static-swap-0-2`, `Q-static-swap-1-3` | A channel swap present from the first frame, with the decided arms planted | Each swapped channel is one `bit-flip` run over the whole capture. The planted drop and repeat are missed there, so the verdict is **NOT RUN, "void: a planted arm was missed"** | FAIL, class `swap` |

Bursts in the pad and sign bits are classified correctly (`P4-burst-0x00000001x3`, `P4-burst-0x80000000x2`).

**Impact:**
- No case reaches PASS.
- A dup and a skip in adjacent samples is the media-boundary slip mechanism that `SLIP_LB`/`SLIP_TDM` count (docs/reference/REGISTER_MAP.md 0x8D4/0x8D8). The grader reports it as bit corruption, which points an investigation at the wrong source.
- A static channel-map error yields a void run. Under 6d a void run is a broken measurement to re-run, not a failed assertion to file as a finding. So a DUT defect is reported as a capture or source problem.
- None of these cases is tested. The grader's class tests build their captures with the planner's own `synthesize_counter_capture` and plant only isolated canonical events.

**Required outcome:**
- Each listed case is classified in the design's classes. Examples:
  - compare a mismatching word with the previous received word;
  - require reciprocity before calling a swap;
  - recognise a burst whose net shift is zero as one corruption;
  - acquire the channel numbers at capture start, so that a static swap is a swap and its counters are tracked.
- A case that is genuinely ambiguous is stated as a limit in TESTING.md 6d and in the `audio.counter-classified` text, and a test pins the documented behaviour.
- In every case, a DUT defect with every planted arm present must not void the run.
- Note the interaction: the planted flip arm, mask `0x00000100` (`:3606`), applied at an odd counter equals the previous sample. A "previous word" rule must not reclassify the arm.

**Verification:** rerun both probe scripts at the new head. Each listed case reports its design class or its documented limit. The static swap with the arms present returns FAIL. New self-test arms fail when each rule is removed.

### F2 MINOR: Tests. Three reviewer mutants survive both suites

**Where:** `scripts/reviewer_mutants.py`, receipt `receipts/reviewer_mutants.log`. It ran 28 mutants against a pristine export of the head: 25 killed, 3 survived, 0 invalid. The pristine control passed both suites.

**Survivors** (the planner self-test and the plan feature both still pass):
- **G07, `:3876`:** a logged capture loss is attributed when it appears on only one counter channel.
  - TESTING.md 6d says "A logged loss is a slip at that index on every counter channel" and "A logged loss the capture does not show is NOT RUN".
  - The every-channel half has no test.
- **R03, `check_release_state_restored` `:3549`:** a soft reset supplied with a `committed` snapshot is graded as a commit cut and accepts the new snapshot.
  - 6d says "Idle cuts and soft resets require the exact pre-cycle committed snapshot".
  - No test supplies a committed snapshot on a soft reset.
- **G12, `_CounterScan._open`:** a swap run is extended when its partner channel changes.
  - No test covers a swap whose partner changes.

**Impact:** each mutant weakens a documented rule, and no gate notices.

**Required outcome:** a self-test arm or plan scenario kills each survivor, or a stated argument shows the mutant equivalent.

**Verification:** rerun `scripts/reviewer_mutants.py` unchanged at the new head. G07, G12 and R03 must be KILLED, with the control still passing.

### F3 MINOR: Docs, Tests. The claimed backstop for 4096-multiple slips does not hold on two paths

**Where:**
- `docs/testing/TESTING.md:1305`: "The soak's sequence and interruption counters remain the check for those."
- The same sentence in the PR body's "Known limitations".

**Authority and evidence:**
- Milan v1.2 Table 5.6 counts `SEQ_NUM_MISMATCH` on received Stream Data AVTPDUs with a non-sequential `sequence_num`. It counts `STREAM_INTERRUPTED` when playback is interrupted.
- A 4096-multiple slip in two places changes neither counter on either entity:
  - inside the DUT talker, between the TDM junction and the packetizer;
  - on the DUT's TDM loop.
- In both, the AVTPDUs stay sequential and playback is not interrupted.
- `SLIP_TDM`/`SLIP_LB` (REGISTER_MAP.md 0x8D4/0x8D8) do count those skips. But the plan walks them only as event context (`audio.event-record`), and no assertion grades their growth.

**Judgement of the open item:** the blind spot itself is honest. It follows from the decided signal level, about -48 dBFS, which leaves 4 tag bits and 12 counter bits. It is stated correctly in the code (`audio.counter-classified`, the grader docstring and `counter_limits`). Only the backstop claim overreaches.

**Impact:** a reader is told that the blind spot is covered. On the outbound and loop paths it is not.

**Required outcome:** one of these.
- State the blind spot without the backstop, naming the paths where nothing grades it.
- Or add, through a recorded decision, a graded check that sees it, such as `SLIP_*` growth over the run.

**Verification:** read the text at the next head. If a check is added, a test plants a 4096-sample slip and the new check fails on it.

### R1 RESIDUE: Docs. Issue-comment IDs appear in new source comments

**Where:**
- `tb/tools/torture_campaign.py:3317`: `#: Issue #396 audio signal design (issuecomment-5978644444), run inside the`
- `tb/tools/torture_campaign.py:3591`: `#: Issue #396 decision 2026-10-04 (issuecomment-5978644444): a bit-exact`

**Authority:** the owner comment rule of 2026-10-15. Source comments never show issue-comment IDs. A new instance in the delta is RESIDUE.

**Exact fix:**
- At `:3317`, replace `(issuecomment-5978644444)` with `of 2026-10-04`.
- At `:3591`, delete ` (issuecomment-5978644444)`.

**Not counted:** `tests/steps/torture_release_steps.py:239` keeps "round 3", but that word was already on the base line. It is an existing instance and #746 tracks it.

### S1 SUGGESTION: Conformance. "At the start and at the end" is enforced as "in each half"

`:4013` accepts arms anywhere in each half of the capture. Probe `P6-arms-only-mid-capture` places every arm within 300 frames of the midpoint, and the result is PASS. TESTING.md:1320 states the halves rule honestly. Consider one of these:
- record a placement window for the arms;
- or word the assertion and REQ-VER-06 as "in each half".

### S2 SUGGESTION: Robustness. The fast path covers only phase-aligned, all-counter captures

The fast path at `:3977` runs only when every channel carries the counter and all channels share one phase. The sine pair may share a capture with counter channels, and streams of different latency may share one too. Either takes the slow path.

Measured on this host (`receipts/grader_throughput.log`), 8 channels at 48 kHz:
- clean: 8.45 capture-minutes per second with 1 MiB chunks;
- one-channel offset: 0.08 capture-minutes per second, about 5 h for a 24 h capture.

The author's 36.5 figure used 128 KiB chunks on another host. The figure depends on host and chunk size. A per-channel fast path would remove the cliff.

### S3 SUGGESTION: Conformance. Tables 4.1/4.2 are not cited

Issue #396's authority list names Milan v1.2 4.2.6.2.2/4.2.6.2.3 with Tables 4.1/4.2, the gPTP interval and timeout tolerances. No soak assertion cites them, before or after this delta. The decided criteria do not require them, and `soak.gptp-continuity` correctly cites 4.2.6.2.4 for `asCapable`. An interval and timeout tolerance hold over the soak would close the compliance matrix's open "long-duration holds" item. That is a candidate for its own issue.

## The brief's checks

### 1. Plan, criteria and clauses

`--plan --areas soak,audio,power --json` (`receipts/plan_json.log`) emits five repeats and three controls:
- `soak.continuous`: 86400 s, interval 60 s;
- `audio.integrity`: 86400 s, context 5 s, window `soak.continuous`;
- `power.idle`, `power.journal_commit` and `power.soft_reset`: 100, 50 and 50 of 200;
- the controls: `audio.control.planted-drop`, `power.control.first-boot-restart` and `power.control.persistence-disabled`.

All 50 release assertions are SHALL and carry an authority (`receipts/assert_clauses.log`).

Each clause was checked against the extracted standard text:

| Clause | What it says | Where the plan uses it |
|---|---|---|
| Milan 5.3.8.10, Table 5.6 | The counters, their 32-bit wrap, and zeroing on a not-bound to bound transition | Matches the oracle's "decrease = reset" rule |
| Milan 4.2.6.2.4 | `asCapable` | `asCapable` |
| Milan 5.5.1.4 | Its text includes "a power cycle or a simple reset" | Soft-reset authority |
| Milan 5.5.2.6 | Auto Connect | Restoration |
| Milan Annex B.1.1 | `tu` set for 0.25 s on a GM change | `tu` |
| IEEE 1722-2016 4.4.4.6 | `sequence_num` | Sequence counters |
| IEEE 1722-2016 4.4.4.7 | `tu` | `tu` |
| IEEE 1722-2016 7.3.5 | `pcm_data_payload` | Carrying the counter |

The stricter criteria are exactly the decided set:
- zero growth of `SEQ_NUM_MISMATCH`, `STREAM_INTERRUPTED`, `LATE_TIMESTAMP` and `EARLY_TIMESTAMP` on every Stream Input, CRF included, with no planted-event excuse;
- zero `MEDIA_UNLOCKED` growth outside a planted event of that input, whatever the cause;
- `asCapable` and `tu` rules unchanged from the merged rule.

The oracle adds "one increment per planted event per input". That is stricter, not weaker. Nothing weaker was found. Independent probes S1 to S7 behave as the decision requires, including a CRF `EARLY_TIMESTAMP`, a planted event on another input, sequence growth inside a planted window, and a wrap. Reviewer mutants S01 to S04 are all killed.

### 2. Audio grader

- All five classes are exact for isolated events.
- A missed arm voids the run, even when a DUT event is also present.
- Logged capture losses are attributed apart, and a logged loss that is absent is NOT RUN.
- Arms at a single end are void.
- Torn frames, empty captures and bad layouts are NOT RUN.
- Compound and edge events: see F1.
- Self-tests rerun: 94 tests OK.
- Reviewer grader mutants G01 to G12: 10 killed, G07 and G12 survive (F2).

### 3. Power and negative controls

- The cycle mix sums to 200: 150 cold, 50 of them in a commit, and 50 soft resets.
- The eight items match #70's list, plus the binding.
- Every phase carries `power.state-restored`, `power.adp-valid-time` (T0-based, 20 s), `power.rebind-bound` (#75, under 1 s) and `power.automatic-restore-bound`.
- The three controls each FAIL their named assertion offline and PASS once the defect is removed.
- Reviewer mutants C01 to C03 are killed.
- Probes R1 to R4 grade each item independently and refuse mixed commit state.

### 4. Documents

These all agree on 24 h, 200 cycles = 100/50/50, the stricter criteria and the eight items plus the binding:
- REQ-VER-06 and REQ-VER-05's blocker sentence;
- CONTRIBUTING.md section 3, which also gains the release-PR rule;
- TESTING.md 6d;
- the README roadmap ("24 h soak");
- SAVED_STATE_MATERIALIZATION.md.

No stale seven-day or 160/40 text remains in tracked Markdown. Public text names "the reference peer" and "an external digital capture". No bench product, host path or lane label was added. Exceptions: F3 and R1.

### 5. Gates

All rc 0 at the exact head, run in this clone (`receipts/*.rc`):

| Gate | Result |
|---|---|
| `--self-test` | 94 OK |
| `torture_release_mutants.py` | 192 killed |
| `cd tests && behave` | 452 scenarios, 2154 steps |
| Plan feature | 133 scenarios |
| `docs_check.py` | 0 findings |
| `check_doc_paths.py` | 1065 paths |
| `gen_toc.py --check` and `--verify-anchors` | Pass |
| `check_em_dash.py --base e76a755a` | 0 findings over 222 lines |
| `check_doc_style.py` | Pass |
| `check_py_idiom.py` | Pass |
| `check_feature_status.py` and `--self-test` | Pass |
| `--coverage-by-area --areas soak,audio,power` | Missing `{}` |
| `git diff --check` | Clean |

The Markdown gates ran under the pinned renderer: cmarkgfm 2025.10.22, html5lib 1.1.

### The author's open items

- **Analog sine limits.**
  - Stated honestly: `audio.analog-sine-pair` is NOT RUN, so no release can qualify.
  - The limits are an owner or manager decision. They correctly remain a recorded open item, not work for this PR.
- **Soft-reset mechanism.**
  - Stated honestly. The DUT refuses REBOOT (0x002A) with NOT_IMPLEMENTED (docs/findings/451_TDM8_FIRST_LIGHT.md:388).
  - At pin `ed211803`, the processor's REBOOT SUCCESS answer appears only as a planted defect (`protocol-processor/tb/pp_top/README.md:1386`).
  - The mechanism is bench work (part B), and the plan records it per cycle.
- **4096-multiple blind spot.** Honest as a limit; the backstop claim is F3. A graded mitigation would add a criterion, so it needs a decision first.
- **`restore_bound_s = 30` provisional.** Carried over unchanged.

## Lens coverage

[R699] PASS RTL - `git diff --stat e76a755a..21faa482 -- hdl sw protocol-processor gptp-processor external third_party` (empty); HEAD gitlinks `ed211803`/`55680bff`/`efeb541a` unchanged from base; docs/reference/REGISTER_MAP.md:1300 (AVTPRX_TSD 0x6EC) and :1922-1923 (SLIP_LB/SLIP_TDM 0x8D4/0x8D8) - no RTL in the delta; every register address and width the plan cites matches the register map; S32 layout bits 31:8 matches `tb/tools/thdn.py:61-66`.

- **Conformance: UNCLEAN (F1).** These were examined and found clean:
  - the criteria, mix, inventory, timing origins and clauses in `tb/tools/torture_campaign.py:3113-3377`;
  - REQUIREMENTS.md:317-483;
  - against Milan v1.2 5.3.8.10/Table 5.6, 4.2.6.2.4, 5.5.1.4, 5.5.2.6 and B.1.1, IEEE 1722-2016 4.4.4.6/4.4.4.7/7.3.5, and #70's list.
- **Robustness: UNCLEAN (F1).** These were examined and found clean:
  - malformed, torn and empty captures, invalid logs, overflow (`max_events`), byte order and chunking;
  - soak reads that are missing, unordered or out of range, and counter wraps;
  - state snapshots that are missing or at their defaults.
- **Tests: UNCLEAN (F1, F2, F3).**
  - Examined: `_ReleaseGateChecks` (`:6738-7103`), `tests/features/torture_campaign_plan.feature:301-576` and `tests/steps/torture_release_steps.py`.
  - 192 author mutants are killed and 25 of 28 reviewer mutants are killed.
- **Docs: UNCLEAN (F3).** R1 is residue and does not make the lens unclean. Examined: REQUIREMENTS.md section 8, CONTRIBUTING.md:421-439, TESTING.md 6d (:1021-1457), README.md:346, SAVED_STATE_MATERIALIZATION.md:2950-2959 and the PR body.

### Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | `torture_campaign.py:3113-3377, 3549-4021`; REQUIREMENTS.md:317-483; Milan v1.2 and IEEE 1722-2016 text; issue #70 list | R699-1 | `21faa48242e021177a1dc702f28e51347c6a7a57` |
| RTL | CLEAN | Empty RTL/firmware/submodule diff; gitlinks; REGISTER_MAP.md:1300, :1922-1923; thdn.py:61-66 | R699-1 | `21faa48242e021177a1dc702f28e51347c6a7a57` |
| Robustness | UNCLEAN (F1) | Grader, soak and state oracles under the probe set in `receipts/grader_probe*.log` | R699-1 | `21faa48242e021177a1dc702f28e51347c6a7a57` |
| Tests | UNCLEAN (F1, F2, F3) | Self-test, plan feature and steps, author mutant driver, reviewer mutants `receipts/reviewer_mutants.log` | R699-1 | `21faa48242e021177a1dc702f28e51347c6a7a57` |
| Docs | UNCLEAN (F3; R1 residue) | REQUIREMENTS.md section 8, CONTRIBUTING.md section 3, TESTING.md 6d, README.md:346, SAVED_STATE_MATERIALIZATION.md, PR body | R699-1 | `21faa48242e021177a1dc702f28e51347c6a7a57` |

## Real limits

- **Source validation only.** This review ran source-head gates in an isolated clone. It is not the current-dev merge candidate. No manager source bank ran at this head, and none is claimed or inferred.
- **No physical evidence.** Physical calibration was NOT RUN. Acceptance items 3 and 4 (the bench soak, the audio run, the power campaign, and the two power controls on known-defect images) are part B and remain open. Desk controls are not hardware proof.
- **Hosted contexts were inspected, not accepted** (`receipts/hosted_failed_steps.log`, `receipts/hosted_dev_base.log`).
  - Executed and green at this head: `bdd-conformance`, `verilator-lint`, `docs-check-no-git`.
  - Failed or cancelled:
    - `docs-gates-0/1/2`, `docs-check`, `firmware-*`, `elaborate`, `verilator-suites`, `yosys-portability`, `wire-accountability`, `full-ci-gate`, `publication-census`;
    - `rtl-fast`, cancelled.
  - Most failed in dependency-install steps, for example pip `ResolutionImpossible` and the GoogleTest install, before any gate ran.
  - `docs-gates-0/1`, `full-ci-gate`, `publication-census`, `verilator-suites` and `wire-accountability` fail at dev base `e76a755a` too.
  - This PR touches no workflow or dependency file. Hosted and replica acceptance belong to the manager.
- **Probe scope.** The probes cover classification on synthetic captures only. No real capture was graded.

## Pending manager duties

- Carry R1 to the residue checklist.
- Route F1 to F3 to the executor. Decide whether F3's mitigation needs an owner decision.
- Build and validate the current-dev merge candidate (builder and native banks), then link the receipts.
- Hosted and replica acceptance at the final head.
- Record the analog sine-pair limit decision. Ratify `restore_bound_s`.
- An external review is still required.

## Receipts

Every publishable file is listed in `MANIFEST.sha256`:
- the scripts under `scripts/`;
- the raw logs and return codes under `receipts/`.

Probes and mutants ran on a `git archive` export of the head. That export's `torture_campaign.py` blob is `8d087941fe`, the same as `HEAD:tb/tools/torture_campaign.py`. The review clone was restored and verified (`receipts/restore_check.log`): HEAD, the tree, the index tree and all gitlinks match, and the porcelain status is empty.

R699-1 FINISHED
