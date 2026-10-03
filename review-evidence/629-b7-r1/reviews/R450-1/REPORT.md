[R450] NEGATIVE - exact head 4eee41a558a56024e57b27a956fdaf7910ca69dc

# R450-1: internal review of PR #644 (issue #629, bench lane B7)

- **Head:** `4eee41a558a56024e57b27a956fdaf7910ca69dc`, tree `c90f26fbb419062935cae9a0a490b3368688b6e6`, one commit on dev `bbf704ecc3ef2e9cdd4cfdb72ec085e7428d1352`.
- **Diff:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (+477 / -1) and `docs/findings/README.md` (one row). No code, RTL, test or generated file changes.
- **Evidence examined:** the public packet `review-evidence/629-b7-r1` at `95448218b342c084efa28ac266ae9415bff4ecce`. All 376 files verify against its `MANIFEST.json`; the 6 path-redacted entries are as recorded.
- **Context reconstructed in order:**
  1. AGENTS.md and CONTRIBUTING.md;
  2. docs/README.md;
  3. #629's body;
  4. the [A10] rulings (D1, D4 = A2-a, the oscillator known risk) and the lane B7 assignment (issuecomment-5969106115);
  5. `docs/design/MEDIA_CLOCK_FOLLOWING.md`, `docs/design/TIME_SYNC.md` and `docs/reference/REGISTER_MAP.md` (0x738, 0x8D4/0x8D8, 0x8E0, 0x8F8);
  6. `docs/reference/FR_NFR.md`;
  7. the diff and history;
  8. the evidence packet;
  9. PR #634's hosted checks.

## What was independently re-derived

The reviewer's scripts (`scripts/`) recomputed every figure below. The inputs are:

- the raw console register dumps (`runs/<case>/dut-*.txt`);
- the raw poll words (`runs/<case>/poll-*.jsonl`);
- the raw GET_COUNTERS payloads (`runs/<case>/events.jsonl`);
- the per-event and per-block grades (`summary/<case>/events.csv`, `blocks.csv`).

The page's prose was not used as an input.

| Case | Window s / frames | Blocks at floor | Listener drops / inserts / repeats | DUT beat | Counted ratio, ppm (re-derived = grade) | Timed ratio, ppm (+-95 %) | Servo at 21 reads; trim, ppm | Set to LOCKED, s | `SLIP_TDM` | Verdict re-derived |
|---|---|---|---|---|---|---|---|---|---|---|
| A0 | 630.31 / 30,254,880 | 444 / 630 | 470 / 291 / 0 | 0 | +5.9164 | +5.71 (0.55) | IDLE; 0 | - | static 0 | PASS as a control (beyond 2 ppm; 186 blocks off the floor) |
| A1 | 629.88 / 30,234,240 | 597 / 629 | 0 / 0 / 0 | 0 | 0 | -0.28 (1.40) | IDLE; 0 | - | static 0 | PASS |
| A2 | 628.04 / 30,145,920 | 578 / 628 | 0 / 0 / 0 | 0 | 0 | +2.15 (4.42) | IDLE; 0 | - | static 0 | PASS, resting on the capture-path attribution |
| B0 | 629.55 / 30,218,400 | 434 / 629 | 457 / 278 / 0 | 0 | +5.9235 | +5.62 (0.44) | IDLE; 0. CRF sink locked at 21 of 21 reads, +11.025 to +11.057 ppm | - | static 0 | PASS as a control |
| B-CRF | 628.53 / 30,169,440 | 559 / 628 | 0 / 0 / 0 | 0 | 0 | +1.98 (6.52) | LOCKED; -6.000 to -5.9375 | 3.085 to 3.589 (ACQUIRE 0.054 to 0.559) | static 0 | PASS |
| B-AAF | 627.74 / 30,131,520 | 564 / 627 | 0 / 0 / 0 | 0 | 0 | -1.49 (11.64) | LOCKED; -6.000 to -5.9375 | 6.578 to 7.080 (meter locked 0.064 to 0.566, rate valid 4.070 to 4.570) | static 0 | PASS, resting on the capture-path attribution |

### Checks that reproduce the page

- **B-AAF bench row.** Every criterion of the design's B AAF row was re-derived:
  - LOCKED within 15 s, and at all 21 reads;
  - meter locked and rate-valid at every read;
  - history restarts 0 to 0;
  - largest deviation 29 ns;
  - meter rate +11.0176 to +11.0430 ppm;
  - CLOCK_DOMAIN 0 at 5/4 at all three marks;
  - 0 net steps.
- **Page tables.** Every value in the page's tables equals the reviewer's figure and the re-rendered `summary/tables.md`. The tables checked are `b7-thdn-a`, `b7-offset-a`, `b7-discontinuities-a`, `b7-ratio-b`, `b7-servo-b` and the capture-path table.
  - `b7_tables.py`, re-run on the published grades, reproduces `tables.md` and `verdicts.json` byte-for-byte (`receipts/tables-rerun.md`, `receipts/verdicts-rerun.json`).
  - The window start times (14:42:08, 14:53:19, 15:04:29, 15:15:42, 15:26:55, 15:38:07 CEST) equal the run logs.
- **Timed-ratio interval.** The method is lane B6's, unchanged: `grade_b6.py` carries the identical code. Every verdict also holds under the bootstrap-only interval. Its half-widths are A1 0.43, A2 4.04, B-CRF 4.33 and B-AAF 2.43 ppm, and each holds zero.
- **Controls.**
  - The reviewer re-ran `b6_thdn.py controls` using the packet's tool copies, `d4673f55...` and `d188a1a9...`. Both equal lane B6's published hashes at the base.
  - The output is byte-equal to `controls.json` `7bbefc71...`, which is lane B6's published hash, and it reads ALL_PASS True.
  - Two disposable mutants of the tool are both killed (ALL_PASS False): one with one-frame events dropped, one with repeats reported as skips.
  - A0 and B0 are live controls, not byte-equal artifacts. They still detect the mismatch, and they ran with B6's unchanged tone (`566d3dfa...`) and analysis tool.
- **Attribution checks.**
  - `b7_absorb.py`, re-run on the published grades, reproduces `absorb.jsonl` exactly for all six cases, and it flags a planted 48 n + 13 step.
  - The reviewer's own sweep confirms the page's six absorb claims:
    - every cluster passed on a measured read-time rise within 1 ms + 2 %;
    - none passed on the gap-only or the gap-and-size branch;
    - no skip of 2 to 48 frames;
    - 47 clusters under 98 frames, all of 60 frames, each with a rise of 0.973 to 2.006 ms after a gap of 10.68 ms or more;
    - the step-backs of -15,492 and -15,780 frames are 677.25 ms and 671.25 ms, each 48 n + 12 once the loop is added.
- **Lock loss.** Derived from the raw polls and payloads:
  - unbind to rebind: 11.09 s;
  - HOLDOVER 0.054 to 0.556 s after the unbind, trim held at -5.9375 ppm;
  - GET_CLOCK_SOURCE 2 before, during and after;
  - after the rebind: meter locked 0.051 to 0.553 s, rate valid 4.073 to 4.575 s, LOCKED 5.579 to 6.081 s;
  - DUT STREAM_OUTPUT 0 MEDIA_RESET 1 -> 2 -> 2, and peer STREAM_INPUT 0 the same, 1 -> 2 -> 2;
  - CLOCK_DOMAIN 5/4 -> 5/5 -> 6/5, which keeps LOCKED equal to UNLOCKED or UNLOCKED + 1;
  - DUT STREAM_INPUT 0 MEDIA_UNLOCKED 0 -> 1, then the bank reset at the bind;
  - the 29.98 s tone-path segment has 29 clean blocks, 0 events and 0 net steps.

  All of this matches the design's "Lock loss, holdover and restart" and "`mr`" sections. Each set toggles the DUT's AAF output `mr` once: MEDIA_RESET reads 1 at every B-CRF and B-AAF mark, and 0 in A0, A1, A2 and B0.
- **Identity.** `identity-verdict.txt` matches the build's values in `expected.json`:
  - CRCs and sizes;
  - 11 live descriptors, none with a differing offset;
  - CLOCK_SOURCE 3 answers NO_SUCH_DESCRIPTOR;
  - the three clock sources in D1 order.
- **Bench procedure.**
  - The format rule held: every set was on a listener, echoed and read back, and no talker format was set.
  - All four case sets, and the shakedown's set, were restored to index 0 and read back.
  - The census differs in 1 of 46 entries, the DUT's propagation delay.
  - The NVM went from seq 0 to slots seq 17 and 16 `VD_OK`: 17 commits, `pend=1`.
- **INTERNAL clock observation.** About -5.1 ppm against gPTP time (11.04 - 5.92). The comparison with lane B6 holds: the DUT against the peer read +6.05 ppm then and +5.92 ppm now, while the peer against gPTP moved from about -17.1 to -11.04 ppm.
- **Docs gates, run by the reviewer at this head:**
  - `docs_check.py` rc 0 (0 findings; scrub self-test 23/23);
  - `check_doc_style.py` rc 0;
  - `check_doc_paths.py` rc 0;
  - in the pinned Markdown environment, in a disposable venv: `gen_toc.py --check` rc 0, `gen_toc.py --verify-anchors` rc 0, and `check_em_dash.py --base bbf704ec` rc 0;
  - every fragment link on the page resolves;
  - `git diff --check` is clean.
- **PR form.** The commit message is one line, with no trailers. The PR body says "Refs #629", not "Closes".

## The capture-path attribution: strict against conservative reading

Five clusters fall short of the 48 n + 12 signature:

| Case | Cluster | Short by | Loss | Position |
|---|---|---|---|---|
| A2 | 0 | 2 frames | 2,100 ms | 12.3 s into the window |
| A2 | 9 | 1 frame | 215 frames, holding a 59-frame step | 77.8 s |
| B-AAF | 4 | 1 frame | 1,196 ms | 82.5 s |
| B-AAF | 17 | 1 frame | 155 frames | 231.0 s |
| B-AAF | 24 | 1 frame | 4,331 frames | 366.1 s |

The page states the conservative reading at :1017-1018 and in its limits at :1088-1089.

**Under the strict reading, the verdicts change: A2 and B-AAF both FAIL.** Counted as one-frame listener events, A2 would hold 3 (its cluster 0 needs two merged repeats) and B-AAF would hold 3.

The reviewer's own weighing (`receipts/offsig.jsonl`) supports the page's PASS reading, but it is not decisive for every cluster:

- **For:**
  - At each case's measured capture deficit, the expected number of one-frame-short capture packets inside all non-control clusters is 5.26 frames; 6 are observed.
  - The two long losses fit well, at P = 0.40 and 0.60.
  - Each case shows zero listener events in about 628 s of visible audio, so a merged listener event inside about 2.4 s of lost audio is far less probable.
- **Against:** the two small clusters (155 and 215 frames) each fit the drift mechanism poorly, at about 0.25 % and 0.29 %.

So the verdicts are conditional, and the page says so. That disclosure is adequate. The defects in the paragraph's figures are F1.

## Findings

### F1. MINOR (Docs, Tests): the conservative-reading paragraph misstates two figures

- **Where:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1017-1024`, item 1 of "What the attribution can absorb".
- **Authority/evidence:**
  - The page says "it delivers 0.54 to 0.84 frames per second fewer than 48 kHz". The six windows' `frame_rate_ratio.external_capture.rate` gives deficits of 0.838, 0.543, 0.650, 0.826, **0.929** (B-CRF) and 0.765 frames/s. The range is 0.54 to 0.93.
  - The page says "A2 would then hold 2 and B-AAF 3". A2's cluster 0 is two frames short, so under a conservative reading that counts one-frame listener events, A2 holds 3, not 2. The 2 is A2's cluster count, while B-AAF's 3 is both its cluster and its frame count, so the two figures are on different bases (`receipts/offsig.jsonl`, `receipts/rederive.json`).
- **Impact:** this paragraph is the basis on which two PASS verdicts rest. A misstated drift range and an inconsistent count weaken the one argument a cold reader must weigh.
- **Required outcome:**
  - the range reads 0.54 to 0.93 frames/s, or names the windows it covers;
  - the conservative count states one basis: 3 listener frames in A2 (2 clusters) and 3 in B-AAF (3 clusters).
- **Verification:** both figures are recomputed from `summary/<case>/grade.json`.

### F2. MINOR (Docs, Tests): the run record contradicts "fixed at 14:50 CEST, before any graded case ran"

- **Where:**
  - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:756`, a claim that covers the change rows at :760-768;
  - the PR body, which repeats "fixed before any graded case ran".
- **Authority/evidence:**
  - A0, a graded case, ran from 14:41:42 to 14:52:47 CEST, with its window from 14:42:08 to 14:52:39 (`runs/a0/events.jsonl`, `runs/a0-lock.txt`).
  - The page prints A0's window start, 14:42:08, itself at :835. So 14:50 falls inside A0's window.
  - The packet's own record places one listed change, the `tone.repeats` summary fix at :768, after A0's first grade.
- **Impact:**
  - Pre-registration is the property that lets a reader trust a changed pass rule. The A0 rule moved from lane B6's "about 16 ppm" to "beyond 2 ppm", and A0 measured 5.92 ppm, which the old rule fails.
  - As written, the page asserts an ordering that the evidence contradicts.
  - The verdict itself is not in doubt: A0 shows the mismatch under any reasonable rule.
- **Required outcome:**
  - The page states the true time the criteria were fixed, relative to A0's run, with the evidence that establishes it.
  - Any criterion fixed during or after A0's window is identified as such.
  - The PR body's sentence matches.
- **Verification:** the stated time is checked against `runs/*/events.jsonl` (`receipts/timeline.txt`).

### F3. MINOR (Robustness, Docs): the page does not report an unanswered DUT AECP command in a graded window

- **Where:**
  - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:765`, "both entities' GET_COUNTERS at three marks";
  - the B0 row at :889;
  - evidence: `runs/b0/ctl.jsonl` and `runs/b0/events.jsonl`, mark `window-mark-1`.
- **Authority/evidence:**
  - The DUT's GET_COUNTERS for CLOCK_DOMAIN 0, sent at 15:20:58 CEST inside B0's window, returned TIMEOUT after 1 s.
  - It is the only non-SUCCESS answer among 336 DUT AECP commands in the eight runs (`receipts/timeline.txt`).
  - The page reports smaller unanalysed observations (the A2 CRF-output MEDIA_RESET, the ring slip, the DRP bit) but not this one.
- **Impact:** a cold reader cannot learn that the DUT failed to answer an AECP command during the acceptance bench. The protocol-processor item of #629, and response timeliness, are in this lane's evidence.
- **Required outcome:**
  - The page records the timeout: case, mark, command and target, whether it was retried, and that the next mark answered.
  - It says whether the cause is known or not analysed.
- **Verification:** the page text is checked against `runs/b0/ctl.jsonl`.

### F4. MINOR (Docs, Tests): "all SUCCESS" includes a skipped hosted context

- **Where:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1074`, the Simulation row: "PR #634's hosted checks ... all SUCCESS at its head `2bc5adc0`".
- **Authority/evidence:** at PR #634's head `2bc5adc0`, 21 contexts are SUCCESS and "Physical gPTP (nightly and manual)" is SKIPPED (`receipts/pr634-checks.json`).
- **Impact:** the page's acceptance evidence conflates a skipped hardware context with a pass, which is the distinction the completion bar requires.
- **Required outcome:** the row says that every executed context was SUCCESS and names the skipped one.
- **Verification:** the row is checked against PR #634's check rollup.

### F5. MINOR (Conformance, RTL, Robustness, Docs): the Fabric judgement omits an undeclared post-lock discontinuity on the DUT's followed receive path

- **Where:**
  - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1071`, the Fabric row: "Met for recovery and gating; the stream-to-stream switch not run at the bench";
  - :932-938, "The DUT's listener ring, outside the criteria".
- **Authority/evidence:**
  - #629's Fabric item reads "a source switch re-locks without an undeclared discontinuity".
  - The bench ran one source switch under following: INTERNAL to AAF, in B-AAF.
  - After it, the DUT's loopback ring slipped one frame (`SLIP_LB` 386 -> 388, both channel pairs), 14.7 to 44.9 s after the servo first read LOCKED, inside the graded window (`runs/baaf/dut-window-0.txt`, `dut-window-1.txt`; `receipts/timeline.txt`).
  - The declared behaviour does not cover it:
    - the design's switch contract (`docs/design/MEDIA_CLOCK_FOLLOWING.md:1043-1050`) and `TIME_SYNC.md:384-385` declare one #386 recentre after a settled source change, at most 32,768 ticks (about 0.7 s) after the aligner engages, firing at the next PDU end;
    - #632, which the page cites, is scoped to talker presentation-time phase (IEEE 1722-2016 10.8 and 4.3.5), not to the listener ring.
  - The servo is frequency-only (`hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:22-34`; `CRF_DELTA` is not a loop input), so the page's mechanism is plausible.
  - B-AAF is the only case in which audio flows through the DUT's followed receive path, the path whose THD+N is NOT RUN. This slip is that path's only continuity evidence.
- **Impact:**
  - The acceptance table reads as if the bench says nothing against the switch criterion.
  - In fact, the one switch it ran shows a discontinuity that no declaration covers.
  - The slip is left "not analysed", with no public home whose scope includes it.
- **Required outcome:**
  - The Fabric row, and the B-AAF summary row at :714, state that the INTERNAL-to-AAF switch run here is not shown free of undeclared discontinuity. They cite the post-lock `SLIP_LB` slip and the 6 dups between the set and the window.
  - The observation gets a public home: a new Issue, or a maintainer ruling that places it in #632's scope.
- **Verification:**
  - the row text;
  - the linked Issue or ruling;
  - the `SLIP_LB` values, checked against `runs/baaf/dut-*.txt`.

### F6. MINOR (Docs): the published evidence still states a capture value that its own redaction masks

- **Where:** the evidence packet `review-evidence/629-b7-r1/author/tools/`:
  - `run_b7.py:30` and `run_b6.py:13`, docstrings giving the external capture's channel count and sample format;
  - `grade_b7.py:26` and `grade_b6.py:6`, docstrings giving the same channel count.
- **Authority/evidence:**
  - The redaction pass replaced exactly this value in code with `<capture-channels>`, at `run_b7.py:87` and `run_b6.py:68`, and `redaction.json` records it. So the packet's own rule classes the value as private, yet four docstrings still carry it.
  - CONTRIBUTING.md section 6 names bench equipment by role.
  - The lane assignment (issuecomment-5929778646, carried into B7) bars instrument detail and channel maps from public text.
  - A channel count and wire format help identify the external capture. This report deliberately does not repeat the value.
- **Impact:** an instrument-identifying detail is public in the evidence commit. The page itself is clean: `docs_check.py` reports 0 findings.
- **Required outcome:**
  - The manager's evidence publication masks the value in those four docstrings, consistently with `redaction.json`.
  - It states how the already-public evidence commit is handled under the publication policy.
- **Verification:** a token scan of the republished packet.

## RESIDUE

Each item is wording only and changes no figure, verdict, test or claim. Each goes on the residue checklist.

- **R1.** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:813` reads "`b7_tables.py` renders the tables below from the grades." The page tables are rearranged from the rendered `summary/tables.md`, and every value was verified equal.
  - Exact fix: "The tables below are arranged from `summary/tables.md`, which `b7_tables.py` renders from the grades; every value is unchanged."
- **R2.** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:716` (the summary table's lock-loss row) and the PR body's lock-loss row read "LOCKED 6.1 s after the return". The measured bound is 5.58 to 6.08 s (:956).
  - Exact fix: "LOCKED 5.6 to 6.1 s after the return".

## SUGGESTIONS

- **S1.** At :1019-1024, strengthen item 1 with the quantitative check:
  - in aggregate, 5.3 short frames are expected and 6 observed;
  - the two small clusters are individually improbable under the drift mechanism;
  - zero listener events in about 628 s of visible audio per case bounds a merged listener event far lower.
- **S2.** At :865-867, add that the peer's CRF input counted 0 MEDIA_RESET across A2. The DUT CRF output's stream-start count did not reach the wire as a received toggle.
- **S3.** For the manager's privacy pass: the packet publishes the reference peer's descriptor indices (its CRF Stream Input index and two clock-source indices, in `runs/*/events.jsonl` and `summary/verdicts.json`). The page deliberately withholds them ("Equal to the set index"). Consider masking them as peer topology.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F5) | #629 body and acceptance items; the lane B7 assignment; FR_NFR.md:156, 238 and 239; the design's lock-loss and bench rows (MEDIA_CLOCK_FOLLOWING.md:1054-1117 and 1354-1372); every row of the page's acceptance table (:1062-1081) against the evidence; `mr` and the counters against IEEE 1722-2016 4.4.4.3, as the design reads it; "Refs #629" in the PR body | R450-1 | 4eee41a558a56024e57b27a956fdaf7910ca69dc |
| RTL | UNCLEAN (F5) | No RTL in the diff. The page's register decodes, re-derived from the raw dumps against REGISTER_MAP.md 0x738, 0x8D4/0x8D8, 0x8E0 and 0x8F8; the servo's frequency-only loop (`KL_mmcm_drp_servo.sv:22-34`); the switch and recentre contract (MEDIA_CLOCK_FOLLOWING.md:1035-1050, TIME_SYNC.md:372-389) against the observed `SLIP_LB` | R450-1 | 4eee41a558a56024e57b27a956fdaf7910ca69dc |
| Robustness | UNCLEAN (F3, F5) | The lock-loss polls and counters (`runs/baaf/poll-ll-*.jsonl` and the GET_COUNTERS payloads); AECP answers in all eight run logs; the capture-path stalls and losses (`grade.json` `skip_clusters` and `capture_reads`); restore and census (`restore/*`); the NVM residuals | R450-1 | 4eee41a558a56024e57b27a956fdaf7910ca69dc |
| Tests | UNCLEAN (F1, F2, F4) | The controls, re-run byte-equal, with two mutants killed; `b7_absorb.py` and `b7_tables.py` re-run byte-equal on the published grades, plus a planted off-signature step; the grader's B6 -> B7 changes against the page's change table; the pre-registration timing; PR #634's hosted checks | R450-1 | 4eee41a558a56024e57b27a956fdaf7910ca69dc |
| Docs | UNCLEAN (F1 to F6) | The whole B7 section (:691-1163), with its intro and Contents edits; the README row; the docs gates (`docs_check`, style, paths, TOC, anchors, em dash); the page's hash tables against the packet; a privacy sweep of the page and the packet | R450-1 | 4eee41a558a56024e57b27a956fdaf7910ca69dc |

No lens is banked as covered: every lens has an open MINOR at this head.

## Real limits

- **Raw captures:** `cap-lr.raw`, `cap-ts.bin` and `samples.txt` are not published.
  - The decode and the per-block metrics were therefore not re-run from audio.
  - The re-derivation starts from the published `events.csv`, `blocks.csv` and `grade.json`, and from the raw register and AECP records.
  - The raw-file hashes on the page could not be checked against bytes.
- **Hardware:** physical calibration was NOT RUN and no hardware was touched. Each case is one run, on one DUT, against one peer.
- **Masked tools:** `run_b7.py` and `grade_b7.py` cannot be run as published. Their original hashes match the page and `redaction.json`.
- **Simulation:** no simulation suite was re-run. The Simulation row rests on PR #634's merged evidence, which is outside this PR's diff.
- **Exact-head hosted contexts for PR #644:**
  - `rtl-fast`: SUCCESS;
  - `docs-check`: IN_PROGRESS when read;
  - `verilator-suites`, `yosys-portability`, the Yosys and Verilator shards and `verilator-lint`: SKIPPED by the docs-only scope, not executed.

## Pending manager duties

- Hosted and local-replica acceptance at the exact head, including the `docs-check` context that was still in progress.
- F6: republish the evidence with the value masked, and decide how the already-public commit is handled.
- At the merge turn, the final current-dev candidate (base `bbf704ec`; live dev was `bbf704ec` at review start).
- A second positive review. This round is NEGATIVE.

## Prior public findings

When this round started, PR #644 carried only the two [A10] review-start notices and no review finding.

The concurrent external round R451-1 (issuecomment-5970092043, NEGATIVE, same head) was published at 14:28Z during this round. It was read only after the verdict and ledger above were written, and it changed neither.

The head is unchanged, so no R451-1 finding is resolved. Each is retained at `4eee41a5` as follows:

| R451-1 item | Status at this head | Relation to this round |
|---|---|---|
| F1, MINOR (Tests, Docs): the A0 criterion was fixed during A0's window, contradicting :756 | Retained | The same defect as this round's F2 |
| F2, MINOR (Docs): the B7 section names no published location for packet `629-b7-a519`, unlike B6's at :621-653; its `grade-full.json` hash rows are recorded only in `RAW-ARTIFACTS.json`, not in `events.jsonl` as :1102-1103 says | Retained, verified here | No equivalent in this round. Checked: the page has no branch, commit or path for the B7 packet, and no run `events.jsonl` names `grade-full` |
| RESIDUE-1: "all SUCCESS" at :1074 with a skipped context | Retained | The same defect as this round's F4, which this round holds as MINOR: it is a test-status claim that conflates a skipped context with a pass, and CONTRIBUTING's unsure rule applies |
| RESIDUE-2: the REVIEW READY comment says "12 live descriptors"; the verdict grades 11 | Retained | Outside the diff. Confirmed: `identity-verdict.txt` has 11 descriptor checks |
| S1: the drift argument is weak for the small clusters | Open, optional | Agrees with this round's S1 and its probability figures |
| S2: cite `KL_talker_diag_ctx.sv:176-181` for A2's CRF-output count | Open, optional | Complements this round's S2 |
| S3: give the B-AAF ring slip a named home | Open | This round holds the same observation as F5 (MINOR, four lenses), because #629's Fabric item and the design's declared recentre timing leave it undeclared |

## Receipts

Paths are relative to this packet's root and listed in `MANIFEST.sha256`.

- **Scripts:**
  - `scripts/rederive.py`: the per-case re-derivation from the raw dumps and grades;
  - `scripts/offsig.py`: the off-signature clusters against capture drift;
  - `scripts/capclaims.py`: the six absorb claims;
  - `scripts/timeline.py`: run times, the B-AAF `SLIP_LB` trace and the AECP statuses;
  - `scripts/anchors.py`: the fragment links.
- **Receipts:**
  - `receipts/rederive.json`, `offsig.jsonl`, `capclaims.txt`, `timeline.txt`, `absorb-rerun.jsonl`, `tables-rerun.md` and `verdicts-rerun.json`;
  - `controls/` (the re-run and the mutants);
  - `gates/`;
  - `anchors.txt` and `clone-integrity.txt`;
  - `pr634-checks.json`, `pr644-checks.json`, `pr644.json`, `issue629.json` and `issue629_comments.json`;
  - `grade_b6_to_b7.summary.txt`.
- **Clone state:** the clone was left at exact head bytes (`receipts/clone-integrity.txt`):
  - worktree equals index equals HEAD;
  - `write-tree` gives `c90f26fb...`;
  - gitlinks: verilog-axis `48ff7a7e`, protocol-processor `631eeb34`, gptp-processor `5dce647a`, external `efeb541a` (uninitialised).

R450-1 FINISHED
