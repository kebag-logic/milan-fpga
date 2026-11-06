[R777] POSITIVE - exact head 84fd22781c95f7b7e65d7d18c99a5ed49a68e11c

# R777-2 independent review: Mister-M-alt/FPGA-gPTP PR #101 (issue #100), round 2

- Exact head `84fd22781c95f7b7e65d7d18c99a5ed49a68e11c`, tree `46aadfe70a0df98aaeaf4c52efacd4793d1fd27c` (verified in the review clone).
- Previously reviewed head: `3e3f041` (R777-1 and R778-1, both POSITIVE). Source base `3e3a4e7`. Main merged: `5184fb3` (PR #99).
- Delta reviewed: `3e3f041..84fd227`. It has one merge (`1615187`, parents `3e3f041` and `5184fb3`) and three wording commits (`1400c83`, `1d61f9e`, `84fd227`).
- Scope: the round 2 assignment on issue #100 (issuecomment-6670464742). Round 1 RTL was not re-reviewed. Code the delta does not touch keeps its round 1 lens verdict.

## Verdict

POSITIVE. The merge keeps both sides:

- `hdl/` and `tb/` match one parent or the other byte for byte. The one exception is the engine harness, whose only change is main's two #98 comment hunks.
- `docs/SOURCE_EVIDENCE.md` is this branch's file with main's two parser anchors. The checker reports 20 exact anchors and 0 findings.
- The generator's ROM images and `--help` output are byte-identical to round 1.

With PR #99 and #100 together, I re-ran these at the head and every one passed:

- the parser suite and its full mutation arm;
- the engine suite, all four passes;
- the engine mutation arm's control and 27 mutants (a sample);
- the docs gate.

The author's full-arm and parent consumer receipts are intact and say what the PR claims.

The three wording items are exact. One wording residue remains, R1 below: the shortened R777-1 R1 sentence lost its conjunction. It is RESIDUE and does not affect the verdict.

There are no open BLOCKER, MAJOR or MINOR findings.

## Findings

| ID | Severity | Lenses | Location | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R1 | RESIDUE | Docs | `docs/HDL_DEVELOPER.md:328` | The prior R1 text was 12 to 13 words, and the docs gate refuses it (reproduced: `runs/docs-gate-r1-probe.log` arm A, "13 words", rc 1). So the author split it at "and", which leaves "Region 6 serves gmTimeBaseIndicator, lastGmPhaseChange as ScaledNs." That is a two-item list with no conjunction, and it can be read as serving gmTimeBaseIndicator as ScaledNs. gmTimeBaseIndicator is a 16-bit count (11.4.4.3.7; the same page at `:314` says "sixteen-bit"). The defect started in the prior review's own exact text, not in the author's split. | Wording only. No figure, check or clause claim changes, and the page states the field's width four lines earlier. | Exact fix: replace line 328 with "Region 6 serves gmTimeBaseIndicator and lastGmPhaseChange, a ScaledNs." Keep line 330 ("It also serves scaledLastGmFreqChange, scaled by 2^41."). | The docs gate passes with the fix (`runs/docs-gate-r1-probe.log` arm B, rc 0; the clone was restored afterwards). |
| S1 | SUGGESTION | Docs | Rule of exact-text residue fixes, process | The prior R1 exact fix was never checked against the repository's 10-word docs gate, so the author had to adapt it. | A round's worth of friction, nothing more. | Run every future exact docs fix through `python3 scripts/check_docs.py` before publishing it (as R1 above was). | n/a |

The author's adaptation of the prior R1 is faithful to the review's text: the same words in the same order, a full stop after "ScaledNs", "and" becoming "It also serves", and a comma before "scaled". I checked this against the review text and the head line by line. It was the right response to a gate the review text broke.

## Focus checks

### (1) The merge keeps both sides

- **Reproduced merge.** `git merge-tree --write-tree 3e3f041 5184fb3` gives tree `9ba112a`, with one conflict, in `docs/SOURCE_EVIDENCE.md`. `git diff 9ba112a 1615187` touches only that file. The conflicting hunk's five rows were resolved like this:
  - Deferred receive event: main's parser anchor `KL_gptp_rx_parser.sv#L439`.
  - Four-entry event queue, Parser arbitration priority, Priority timestamp return and Accepted-beat result face: this branch's engine anchors, `#L559`, `#L586`, `#L407` and `#L413`.
  - "Ignored receive flag bits" auto-merged to main's `#L521`. Both parser anchors equal main's file exactly.
  - The rest of the file is this branch's file. Every other file of the merge equals git's automatic merge.
- **Anchors re-pointed.** At the head, `make docs` gives rc 0 (`runs/make-docs-84fd227.log`): docs check PASS, docs selftest PASS, source evidence "20 exact, 0 findings", its selftest PASS (7 arms), diagrams PASS. The `gen_gptp_ucode.py#L1098` anchor sits above the only generator change (line 2612), so it did not move.
- **No behaviour change in `hdl/` or `tb/` beyond PR #99.** Each file changed against the base was classified against both parents:
  - Equal to `3e3f041`: `KL_gptp_engine.sv`, every engine-harness support file (`Makefile`, `mutants.py`, `p100_mutants.py`), every committed ROM image (engine, ucpu, tsngen, `syn/ooc`), `run_tsngen.py` and `check_source_evidence.py`.
  - Equal to `5184fb3`: `KL_gptp_rx_parser.sv` and all four parser-suite files. The two `check_docs*.py` files equal both parents.
  - Mixed: `tb/verilator/engine/sim_main.cpp`. Its diff against `3e3f041` is exactly main's `3e3a4e7..5184fb3` diff of that file, two comment-only hunks.
  - Mixed: `gen_gptp_ucode.py`. Its only change is the S4 help string.
- **ROM and help unchanged.** I generated the ROM image three ways, at `3e3f041` and at the head: the shipping engine arguments, the fourth pass (`--p1 255 --clock-accuracy 0xFE`) and the generator defaults. All three are byte-identical across the two heads (sha256 in `runs/gen-help-rom-identity.log`). `--help` is byte-identical too, and the regenerated engine image equals the committed one. After the suites ran, `git diff --exit-code` in the probe clone was clean.
- **Whitespace.** `git diff --check 5184fb3 84fd227` gives rc 0, and so does `3e3f041 84fd227`. The author's `merge/diff-check-5184fb3.log` agrees.
- **History.** The merge subject is exactly "Merge main 5184fb3 into 100-followup-tlv-values", with no body. It is a `--no-ff` merge with parents `3e3f041` and `5184fb3`. There was no rebase or force: `3e3f041` is an ancestor of the head.
- **Comment rule.** I scanned every added line in `hdl/ tb/ scripts/ syn/ bench/ docs/` in the delta for lane labels, review rounds, reviewer IDs or comment IDs. There are none.

### (2) PR #99 and #100 together: suites, both mutation arms, consumer gates

I ran these myself at the head in a clean clone, with pinned Verilator 5.050 (identity in `runs/verilator-version.log`):

| Run | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/parser` (suite and the full parser mutation arm) | rc 0; 482 checks: 482 PASS, 0 FAIL; arm 35 checks: 35 PASS, 0 FAIL | `runs/parser.log`, `runs/parser.rc` |
| `make -C tb/verilator/engine run` | rc 0; 2098 / 2098 / 2098 PASS (shipping, request-seeded, Sync-seeded); fourth pass (`--p1 255 --clock-accuracy 0xFE`) 61 PASS | `runs/engine-run.log`, `runs/engine-run.rc` |
| Engine mutation arm, sample: the control, the three mutants that plant PR #99's parser edits through `PARSER_EDITS` (148 to 150), and all 24 #100 controls (112 to 135), each through the arm's own `run_mutant()` | rc 0; 28 checks: 28 PASS. The control passes and every mutant is caught by name. | `runs/engine-arm-subset.log`, `runs/engine-arm-subset.rc`, `tools/arm_subset.py` |
| Engine arm, static: every one of the 159 MUTATIONS patterns appears exactly once in its target at the head. The engine arm imports PR #99's `parser/mutants.py`, so this is the merge-sensitive point. | rc 0; 159 mutants, 0 drifted | `engine-mutant-patterns-84fd227.log`, `tools/mutant_patterns.py` |

What the author's published receipts show (packet `kebag-logic/milan-fpga@0b04253`, `review-evidence/gptp100-r1/author-r2/`):

- **Packet integrity.** All 574 `MANIFEST.json` entries match their `published_sha256`, with no unlisted files. All 65 `author-r2/` files are listed; only `HANDOFF.md` is path-redacted.
- **Full engine arm.** `final/engine-arm-84fd227/jobs.md` has 160 jobs, all `ok`: 159 "mutant caught" lines plus the control, and no survivor, build failure or `[FAIL]` line. The run is 4,286 s at 8 jobs, and the tree was clean afterwards (`engine-arm-run-84fd227/02.log`, `03.log`). The job numbering and names match my index list, and my 28 results agree with theirs.
- **Repository gates.** `final/repo-gates-84fd227/results.md` lists 13 commands, all rc 0. Its parser and engine counts are the ones I reproduced.
- **Parent consumer gates.** `final/parent-A-84fd227` runs parent `2278661f` on dev `604899c0`:
  - `gptp_shadow`: "325 checks: 325 PASS, 0 FAIL", RESULT: PASS.
  - `milan_dp gptp`: "210 checks: 210 PASS, 0 FAIL".
  - `milan_dp gptp-lat`: "210 checks: 210 PASS, 0 FAIL". This leg really differs from the gptp leg: its build adds `-GGPTP_INGRESS_LAT_NS_P=296 -GGPTP_EGRESS_LAT_NS_P=104`.
  - The xvlog gate log shows "gptp-processor@84fd2278 - the superproject gitlink".
  - Parent-B's `milan_dp_gptp` reports 151 physical checks with 0 failures.
- **Area and timing.** The PR's figures match the Vivado reports in `ooc-5184fb3/` and `ooc-84fd227/`:
  - Engine: 4,905 + 490 LUTs, 3,620 FFs, 6 DSPs, WNS +2.043 ns over 12,372 endpoints.
  - Main: 4,430 + 490 LUTs, 3,461 FFs, 4 DSPs, WNS +2.249 ns over 12,004 endpoints.
  - The microCPU is unchanged at 4 DSPs.

### (3) The three wording items

- **HDL_DEVELOPER region 6** (`docs/HDL_DEVELOPER.md:328`, `:330`): the content is right. The region-6 read mux at `KL_gptp_engine.sv:1051-1053` serves `tlv_tbi_r`, the 96-bit `tlv_phase_w` (ns << 16, ScaledNs) and the 32-bit `tlv_freq_r` (×2^41). The shortening is faithful. Its one grammar residue is R1 above.
- **INTEGRATION lastGmPhaseChange** (`docs/INTEGRATION.md:857-865`): exact against 802.1AS-2011 11.4.4.3.8. The clause defines a ScaledNs equal to the current grandmaster's time minus the previous grandmaster's, at the time the current one became grandmaster. When this plane becomes grandmaster, that is this plane's time minus its former master's, the slave offset's sign. The added "not extrapolated to the handover" is exactly the outcome R778-1 S3 asked for. No RTL changed: the engine is byte-identical to `3e3f041`.
- **CLOCK_ACCURACY_UNKNOWN_C** (`hdl/ucode/gen_gptp_ucode.py:2612`, constant at `:553`): the help text that offers the 0xFE alternative now reads the constant, so grep finds a reader. The help output is byte-identical. The `--clock-accuracy 0xFE` arguments in `tb/verilator/engine/Makefile:46` and `mutants.py:93` are build commands, which cannot import the constant. That is acceptable.
- **Location claims.** The PR body and handoff give `:328`/`:330`, `:857-865` and `:2612`. All three are exact at the head.

## Prior public findings at this head

I read these only after my own pass over the delta.

| Prior item | Disposition at `84fd227` |
|---|---|
| R777-1 R1 / R778-1 P3 (RESIDUE, HDL_DEVELOPER region 6) | RESOLVED, adapted to the 10-word gate. The leftover grammar is new R1. |
| R777-1 S4 / R778-1 S4 (unused `CLOCK_ACCURACY_UNKNOWN_C`) | RESOLVED: read at `gen_gptp_ucode.py:2612`. |
| R778-1 S3 (lastGmPhaseChange vs 11.4.4.3.8) | RESOLVED by its doc outcome (`INTEGRATION.md:857-865`). |
| R777-1 S1 / R778-1 S1 (exact floor grade of scaledLastGmFreqChange) | RETAINED as SUGGESTION. The delta does not touch the harness or the RTL. On the residue checklist. |
| R777-1 S2 / R778-1 S6 (CLK_HZ_P bound for the TLV multiply) | RETAINED as SUGGESTION. Unchanged. On the residue checklist. |
| R777-1 S3 / R778-1 P1 (BTCA literal 3000 vs `ANN_RTO_MS_C`) | RETAINED as SUGGESTION. Unchanged. On the residue checklist. |
| R778-1 S2 (a Sync between an Announce's last octet and its handler) | RETAINED as SUGGESTION. Unchanged. On the residue checklist. |
| R777-1 S5 / R778-1 P2 (manager confirms 0x22 covers every parent board) | RETAINED as SUGGESTION and a manager duty, for the parent re-pin PR. |
| R777-1 R2 / R778-1 P4 (parent builder wording) and R778-1 S5 (parent `OUR_CQ` names) | RETAINED for the parent re-pin PR. Not in this repository. |

## Ledger (reviewer-owned)

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `INTEGRATION.md:857-865` against 11.4.4.3.8. `HDL_DEVELOPER.md:328-330` against 11.4.4.3.7 to 11.4.4.3.9. 8.6.2.3 b) help text. No behaviour change, so round 1's clause verdicts stand. | R777-2 (delta); R777-1 (unchanged behaviour) | `84fd227` |
| RTL | CLEAN | `KL_gptp_engine.sv` byte-identical to `3e3f041`. `KL_gptp_rx_parser.sv` byte-identical to `5184fb3`. Generator diff is the help string only. ROM images identical. | R777-2; R777-1 for engine RTL | `84fd227` |
| Robustness | CLEAN | Merge-sensitive interfaces: the engine arm's `PARSER_EDITS` import and its 159 pattern counts. The parser and engine suites pass together. Mutants 148 to 150 caught. | R777-2; R777-1 | `84fd227` |
| Tests | CLEAN | Reviewer runs: parser 482 + 35, engine 2098 × 3 + 61, arm sample 28/28, static patterns 159/159. Author receipts: full arm 160/160, repository gates 13/13 rc 0, parent A/B gates rc 0. | R777-2 | `84fd227` |
| Docs | CLEAN (R1 RESIDUE carried) | `make docs` rc 0, `SOURCE_EVIDENCE.md` merge resolution, auto-merged hunks in HDL_DEVELOPER, INTEGRATION, MANAGER, README and TEST_DEVELOPER, the three wording items, PR body round 2 section, published handoff. | R777-2 | `84fd227` |

## Real limits

- I did not re-run the full engine mutation arm. 131 of its 159 mutants rest on the author's receipt (`jobs.md`) plus my static check that every pattern still lands exactly once. All 24 #100 controls and the three parser-edit mutants were run here.
- I did not re-run the parent consumer gates, the OOC synthesis or the gaskets/tsngen/bench/lint gates; they rest on the author's receipts.
  - Parent head `2278661f` is a local, unpushed commit. The proof that its gitlink is `84fd227` is the xvlog gate's log line.
  - `results.md` lists sha256 values of the original, unredacted logs, which cannot be re-derived from the published redacted copies. Packet integrity rests on `MANIFEST.json` (574/574 match) at commit `0b04253`, which is not git-signed.
- There is no hosted CI at this head (0 check runs, 0 statuses; the repository has no workflow directory). So no hosted job was executed or skipped.
- Physical calibration NOT RUN. The parent's `tsn_fuzz` field campaign was skipped (packet generator not installed). Builder gate 11 NOT RUN (needs a LiteX place report). None of these is hardware proof.
- No manager source bank exists at this head, and none is claimed.

## Pending manager duties

- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, against live dev `604899c0`, and link its receipts.
- The parent re-pin PR needs the companion change (`gptp.clock_accuracy: 0x22` pins, the AEM default, the model-id re-pins). It should also carry R777-1 R2 / R778-1 P4, R778-1 S5, and the confirmation that the 0x22 decision covers every parent board (R777-1 S5 / R778-1 P2).
- Carry R1 (this report) and the retained SUGGESTIONs to the residue checklist.
- Hosted/act acceptance.

## Receipts

All receipts are listed in `MANIFEST.sha256`:

- `tools/`: `arm_subset.py`, `mutant_patterns.py`, `launch.sh`.
- `runs/`: the logs and rc files of every run above, the clone-integrity check and the hosted-checks query.
- `engine-mutant-patterns-84fd227.log`.

The review clone was verified after all probes:

- HEAD, index tree and worktree equal `46aadfe`.
- Every tracked blob and mode matches HEAD.
- No untracked or ignored files: three `__pycache__` directories that my static probe created were removed.
- The repository has no submodule gitlinks.

R777-2 FINISHED
