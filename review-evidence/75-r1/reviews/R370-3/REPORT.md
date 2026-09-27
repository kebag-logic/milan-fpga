[R370] POSITIVE - exact head 9c18068512dec844d24fdff7fe0a3eb0d63c14f5

Round R370-3. This is the internal cleared-context review of PR #604 for issue #75, phase 2. It covers the exact head `9c18068512dec844d24fdff7fe0a3eb0d63c14f5`, tree `52012dcea83c4cd6a8b419eeeeffce89962ca526`. It is a delta review of `5c7577e5..9c180685` (one commit by [A391]) plus the round-3 evidence addendum `review-evidence/75-r1/author-r3`, published on branch `75-review-evidence` at `a07c7345177e1836c1e138c69ef91ea77cd52a91`. The whole PR diff `8bc97021..9c180685` was re-read for the lenses the delta touches.

**Result.** No BLOCKER, MAJOR or MINOR finding is open. All five lenses are clean at this head. My round-2 MINOR (R370-2-F1) and the other reviewer's round-2 MINOR (R371-2-F5) are resolved. Three SUGGESTIONs follow; they do not affect coverage. #75 stays open (`Refs #75`, no closing keyword in the PR body).

## Reconstruction

I read the following, in order:

1. AGENTS.md, CONTRIBUTING.md (commit and findings rules) and `docs/findings/README.md`.
2. The #75 body and its frozen acceptance criteria.
3. The phase-2 assignment (5859652809), the round-2 decision (5860261220) and the round-3 assignment (5860554971).
4. #606 and #608.
5. The PR diff and history. The head commit is a one-line message with no trailers, and its parent is `5c7577e5`.
6. The published evidence: `author/` at `a19f2c92`, and `author-r2/` and `author-r3/` at `a07c7345`.

I read the prior public review findings only after my own pass over the diff and evidence.

## Assignment items, verified

**Item 1 (R370-2-F1): talker cycle 1 and the declaration census. Met.**

- **Census.** Page:220-227 states 99/100 holds and counts only New, JoinIn and JoinMt. The window is [disconnect response, connect command).
- **Independent re-derivation.** I re-derived the per-hold counts from the event names in `hold-events.csv`, ignoring its `is_declaration` column. They equal `hold-declarations.csv` and `declarations-summary.json` for all 100 holds: 99 holds are declared and cycle 1 is the only exception.
- **Published records match.** For all eight published talker cycles (1-5, 13, 24, 75), the `hold-events.csv` rows and the declaration, withdrawal and empty counts equal the published `msrp.tsv` exactly. `declaration-input-hashes.csv` equals the published file hashes.
- **Boundaries.** No published DUT Talker Advertise event lies within 1 ms of a hold boundary; the closest is 0.041521 s.
- **Cycle 1 numbers (page:229-238).** Each one equals `talker-001/msrp.tsv` and `result.json` to the nanosecond:
  - Lv at +0.120687323 s, then Mt at +0.520682079 and +1.720684762 s;
  - first declaration 0.111313165 s after the response;
  - Ready 0.006299407 s later, then CRF 0.000123512 s after that;
  - latency 0.117736084 s.
- **No early declaration.** There is no DUT declaration anywhere from the disconnect response to the reconnect response.
- **Initial bind.** It has 0 declarations before its response and its first declaration at +0.079237250 s, matching page:212-213.
- **Old claim removed.** The universal claim and its "therefore differs in DUT-side state" inference are gone. Page:240-245 replaces them with a qualified statement: the shared absence alone cannot explain the delay, and causal attribution remains open.
- **#606 pointer.** Page:249 points #606 at cycle 1. The PR body repeats it, which cross-references #606.
- **Backing check.** `declarations.py` derives the count with `sum(...)` over the data, using the declaration-only event set. A control rejects the old universal claim on recorded cycle 1.
- **Receipts.** `receipts/r3-probe.txt` and `receipts/hold-declaration-probe-r2rerun.txt`. My round-2 probe, rerun unchanged, still reports cycle 1 with 0 declarations; the page now agrees.

**Item 2 (R371-2-F5 and R370-2-S1): chronology of the three talker non-stops. Met.**

- **Event lists.** For talker cycles 13, 24 and 75, the bridge Listener events for the target stream after the disconnect response in the published `msrp.tsv` equal `listener-events.csv` exactly (4 events per cycle). They also equal every row of both page tables (page:624-646).
- **Timing.** Each cycle has one Lv, at +0.009770679, +0.010356881 and +0.025307595 s. No Listener declaration follows until after the reconnect response: +0.073776413, +0.018704540 and +0.018687732 s after it.
- **CRF bracketing.** Every event is bracketed by CRF timestamps no more than 0.002000053 s apart.
- **Counts.** `stop-checks.csv` gives NOT_RESTART, DUT start/stop +0/+0 and 1000 PDUs in the hold for each cycle. The Lv-to-re-declaration PDU counts (1036, 1009, 1001) agree with the 2 ms period to within one PDU.
- **Attribution.** Page:654-661 states DUT-side at the tapped boundary, with the reason. It explicitly does not claim internal receipt or the internal cause, and leaves both under #608. The records support this.
- **#608 links.** #608 is linked from the stop-check section (page:615), the acceptance rows (page:959 and 962) and the index row (README.md:11). #608 is open and names cycles 13, 24 and 75.
- **Record publication.** The three cycle directories hold the same 17-file record set as published cycle 1. All 48 records verify against `published-records.csv`. The only transformed record is `raw-artifacts.json`, whose historical absolute path became a relative identifier; its size and sha256 equal `stop-checks.csv`.
- **Receipt.** `receipts/r3-probe.txt`.

**Items 3 and 4 (R371-2-S5 and R370-2-S2): replay rules and derived outcome. Met.**

- **Classification.** `recompute.py` and `declarations.py` contain no `assert` and no exception handler, checked on the AST. `classify_stop` is plain `if` logic; my truth table (count, early resumption, silence) passes.
- **Optimize refusal.** Both scripts refuse `-O`, `-OO` and `PYTHONOPTIMIZE=1` before reading inputs: rc 1, with the message `REFUSED: optimized execution` and no traceback.
- **Derived outcome.** `outcome_lines` applied to the published `stop-checks.csv` prints 200 hashes and 197 PASS / 3 FAIL (talker-013, -024, -075). These equal my independent counts, and the output changes when one row is mutated. Its source pins no count or cycle literal.
- **Numeric evidence unchanged.** `stop-checks.csv`, `recomputed-summary.json` and `input-hashes.csv` are byte-identical to round 2.
- **Author controls.** The author's `check_controls.py`, rerun on a scratch copy, passes 14/14 and reproduces the published `controls.json` byte for byte. It also refuses under `-O`.
- **Receipts.** `receipts/r3-probe.txt` and `receipts/author-controls-rerun.txt`.

**Probe sensitivity.** Each of 16 disposable mutations makes `scripts/r3_probe.py` fail with the check that targets it, and the unmutated copy passes (`receipts/r3-mutations.txt`). The mutations are:

- page census 100/100;
- cycle-1 Lv relabelled as a declaration;
- summary pinned to 100;
- literal census;
- old claim restored;
- wrong cycle-1 or non-stop timestamps;
- dropped table row;
- dropped `listener-events.csv` row;
- #608 link removed from the index or the acceptance row;
- classification by catching `AssertionError`;
- optimization guard removed;
- outcome pinned to 197;
- `classify_stop` ignoring the count;
- one published record byte changed.

**Round-2 probe rerun.** `scripts/stop_check_probe.py`, unchanged from round 2, passes all 49 checks against this head's page (`receipts/stop-check-probe-r2rerun.txt`). The NOT_RESTART set is {13, 24, 75}. The demonstrated distributions are listener n=100 and talker n=97, with the talker minimum 0.017426921 and maximum 0.117736084. The slope intervals are unchanged.

**Prior packets unchanged.** `author/` is identical from `a19f2c92` to `a07c7345`, and `author-r2/` is identical from `8791bfa4` to `a07c7345`. The `a07c7345` commit adds only `author-r3/` and the top-level `MANIFEST.json` (`receipts/evidence-branch.txt`). The nine round-3 artifact sizes and hashes on page:1218-1228 match the published files, and `author-r3/MANIFEST.sha256` verifies in full.

**Public hygiene of the round-3 addendum.** The scan covered 102 files: the addendum including the three cycle records, the page and index delta, the PR body and the commit message. It found no absolute path, host, instrument, peer or switch name, user name, e-mail address, lane-root variable, command-wrapper name, or tool or model name. The single hit is the scrub-category label `serial-word` inside the author's own checker `check_packet.py:37`, which is benign (`receipts/hygiene-scan.txt`). Capture interfaces are redacted and clock and entity identifiers are the accepted class. The live PR body equals `author-r3/PR-BODY.md` apart from a trailing blank line.

## Findings

None at BLOCKER, MAJOR or MINOR.

### Suggestions (do not affect lens coverage)

[R370] SUGGESTION Robustness, Docs - review-evidence/75-r1/author-r3/talker-013/msrp.tsv, talker-024/msrp.tsv, talker-075/msrp.tsv against author/talker-001..005/msrp.tsv - In all three non-stops the DUT sends its own LeaveAll within 0.1 s of the bridge Lv
ID: R370-3-S1
- **Observation.** In each non-stop cycle the DUT transmits a LeaveAll (Domain, Talker Advertise, Talker Failed and Listener) during the hold:
  - cycle 13: +0.040218046 s after the bridge Lv;
  - cycle 24: +0.089874323 s after the bridge Lv;
  - cycle 75: +0.062871172 s after the bridge Lv.
- **Contrast.** In the five published restart cycles, the earliest DUT LeaveAll in the hold is +1.510926110 s after the Lv (cycle 1). Cycle 2's is at +1.723276288 s, and cycles 3-5 have none in the hold (`receipts/r3-probe.txt`, INFO lines).
- **Why it matters.** Under 802.1Q Table 10-4, a transmitted LeaveAll leaves a registrar that is in LV in LV; only a received declaration returns it to IN. A DUT LeaveAll that coincides with the leave period is a concrete lead for #608's "responsible internal state or timer". It may be a race between the leave timer and the leaveall timer.
- **Status of the page.** The page's attribution is correct without this and is strengthened by it; the observation is not required by the round-3 assignment.
- **Suggested outcome.** Record the observation on #608. #608 can test whether a DUT LeaveAll inside the leave period separates the 3 non-stops from the 97 stops across all 100 retained talker `msrp.tsv`. That needs the private per-cycle records; public data covers 8 cycles.

[R370] SUGGESTION Docs - docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:654-655, 670; author-r3/README.md - Two wording details in the non-stop section
ID: R370-3-S2
- **"therefore" at page:655.** The sentence "The withdrawal therefore reaches the segment while DUT transmission continues" follows "No `DISCONNECT_TX` command crosses this tap". The conclusion actually follows from the CRF bracketing at page:648-652. The absence of DISCONNECT_TX shows only that the Listener withdrawal is the sole recorded stop signal. Reordering or rewording would keep the inference visibly tied to its evidence.
- **"complete chronology" at page:670.** `declarations-summary.json` holds per-cycle extrema and counts. The complete event list is in `listener-events.csv`. The addendum README says "full chronology" in the same way.

[R370] SUGGESTION Tests - review-evidence/75-r1/author-r3/run_gates.py:22-27,47,71-78; render_tables.py:29-50 - The gate and render tools still rely on `assert`
- ID: R370-3-S3.
- Under `-O` these two tools would not fail closed.
- The assignment scoped the fix to the replay, and `gates.json` records each rc independently, so this is optional. The same `sys.flags.optimize` refusal would make them consistent with `recompute.py`.

## Clean-lens evidence

[R370] PASS Conformance - page:220-255, 588-670, 955-963; README.md:11; `author-r3/declarations.py`, `hold-declarations.csv`, `hold-events.csv`, `listener-events.csv`, `declarations-summary.json`; `author/talker-001..005` and `talker-setup`; `author-r3/talker-013/024/075` - checked against the round-3 assignment items 1-4 (5860554971), #75 acceptance, the round-2 decision, #606 and #608, and 802.1Q 10.8.2.10 event coding
- All four assignment items are met, with every stated number re-derived from published records (`receipts/r3-probe.txt`, 126 PASS).
- The acceptance rows still scope criteria 1 and 2 to the measured CRF pairs and the disconnect, two-second hold, reconnect sequence.
- Talker 97/100 stays NOT MET, the initial bind stays an open exception under #606, and AAF stays unmeasured. #75 stays open.

[R370] PASS RTL - `git diff --name-status 8bc97021..9c180685` and `5c7577e5..9c180685` (two docs files); gitlinks identical at base and head; RTL-adjacent delta lines page:652, 658, 661 (`receipts/rtl-scope.txt`)
- No HDL, constraint, firmware, script, CI or interface file changes.
- The delta makes no claim about a specific module, register or state machine. It leaves the internal cause undetermined under #608. The STREAM_START/STREAM_STOP statement equals `stop-checks.csv`.
- The round-2 architecture claims are unchanged by the delta.

[R370] PASS Robustness - `author-r3/declarations.py` `decode_msrp`; `recompute.py` `classify_stop` and the optimize guard; the hold-window boundaries in the eight published TSVs; page:604-661 - checked for malformed input, boundary and configuration-dependent behaviour
- **Decoder.** The decoder refuses, with ValueError, all 20 strict truncations of a well-formed MSRP PDU and 7 malformed variants: version, unknown type, width, event byte ≥ 216, count overrun, missing end mark and length overrun. It decodes the standard event order and the Listener Ready value exactly (`receipts/r3-robustness.txt`).
- **Optimized interpreter.** Optimized execution is refused under three spellings.
- **Hold window.** No published event sits within 1 ms of a window boundary.
- **Non-stop analysis.** It refuses, rather than guessing, when a cycle has other than one Lv or no re-declaration (`declarations.py`, `require(len(leaves) == 1 and redeclarations, ...)`).

[R370] PASS Tests - `scripts/r3_probe.py` with 16/16 mutants failing (`receipts/r3-mutations.txt`); the author's `check_controls.py` rerun 14/14 with an identical `controls.json`; my round-2 probes rerun unchanged (49/49 and cycle-1 census); assigned gates at exact head - checked that each new check can fail for its defect and that the gates return 0
- **Full tree** (`receipts/gates-full.txt`), all rc 0: `docs_check.py`, `check_feature_status.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base 8bc97021`, `check_doc_paths.py`, `ci_scope.py --selftest`, `check_feature_status.py --self-test`, `git diff --check 8bc97021..9c180685` and `git diff --check` on the worktree.
- **Renderer gates.** They use the pinned renderer, installed with `--require-hashes` into a private scratch environment.
- **Bare-metal gate.** `check_baremetal_only.py --check` returns rc 0 under the system interpreter, which supplies pyyaml (`receipts/gate-baremetal-system-python.txt`). The scratch environment lacks pyyaml, and there the gate refuses with rc 2 (recorded in `gates-full.txt`).
- **Without submodules and without Git metadata.** `docs_check.py` and `check_feature_status.py` return rc 0 in both (`receipts/gates-no-submodules.txt`, `receipts/gates-no-git.txt`).
- **Tables.** All 22 page tables and the index table render with every row and cell preserved (`receipts/table-render.txt`).

[R370] PASS Docs - page:6, 205-255, 588-670, 955-963, 1213-1287; README.md:11; PR #604 body; commit `9c180685` message; `author-r3/README.md`, `HANDOFF.md` and `PR-BODY.md` - checked for accuracy against the records, links, the index row, hygiene and cold-reviewer reproducibility
- Statements match the records, and the #606 and #608 links resolve to open issues.
- The round-3 artifact table verifies, and the round-1 and round-2 packets are unchanged.
- The hygiene scan is clean apart from one benign label hit.
- The two wording details are SUGGESTION R370-3-S2 only.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #75 body and criteria; assignments 5859652809, 5860261220, 5860554971; #606; #608; page:205-255, 588-670, 955-963; README.md:11; author-r3 census and chronology files; published talker 1-5, 13, 24, 75 and setup records | R370-3 | 9c18068512dec844d24fdff7fe0a3eb0d63c14f5 |
| RTL | CLEAN | PR and delta name-status; gitlinks at base and head; RTL-adjacent delta lines page:652, 658, 661 | R370-3 | 9c18068512dec844d24fdff7fe0a3eb0d63c14f5 |
| Robustness | CLEAN | `declarations.py` decoder under truncation and malformed input; `classify_stop`; optimize refusal (3 spellings); hold-window boundaries; non-stop refusal path | R370-3 | 9c18068512dec844d24fdff7fe0a3eb0d63c14f5 |
| Tests | CLEAN | r3_probe (126 PASS) with 16/16 mutants; author controls 14/14; round-2 probes rerun; full, no-submodule and no-Git gates; table render | R370-3 | 9c18068512dec844d24fdff7fe0a3eb0d63c14f5 |
| Docs | CLEAN | whole delta and page:1-1287 context; README.md:11; PR body; commit message; author-r3 README, HANDOFF and PR-BODY; artifact hashes; hygiene scan | R370-3 | 9c18068512dec844d24fdff7fe0a3eb0d63c14f5 |

The PR is documentation-only. No later commit exists, so every lens is banked at the candidate head.

## Prior public review findings on PR #604, resolved or retained at this head

| Finding | Status at `9c180685` | Evidence |
|---|---|---|
| R370-2-F1 MINOR, cycle-1 universal claim and uncheckable backing check | RESOLVED | See item 1. The census is derived (99/100, exception [1]), cycle 1 is stated exactly, the inference is qualified, #606 is pointed at cycle 1, and a control rejects the old claim |
| R370-2-S1 non-stop characterisation | TAKEN | See item 2 and #608 |
| R370-2-S2 derived outcome | TAKEN | `outcome_lines`; mutation-sensitive |
| R371-2-F5 MINOR, non-stops unattributed and unowned | RESOLVED | See item 2. #608 is linked from all three places and names cycles 13, 24 and 75; the records are published and scrubbed; the attribution is stated with its reason |
| R371-2-S5 assertion-based classification | TAKEN | No assert or except in the replay; three optimize spellings refused |
| R371-2-S6 initial-bind cadence wording (page:215) | NOT TAKEN | Optional; unchanged at page:215; no coverage effect |
| R370-1-F1 / R371-1-F3 BLOCKER, submodule link | REMAINS RESOLVED | Docs gates pass without submodules and without Git at this head |
| R370-1-F2 MAJOR, talker restarts not shown | REMAINS RESOLVED | Stop evidence byte-identical to round 2; round-2 probe 49/49 |
| R370-1-F3 MINOR / R371-1-F1 MAJOR, initial-bind scope | REMAINS RESOLVED | Acceptance rows page:959-963 unchanged apart from the #608 links |
| R371-1-F2 MINOR, R371-1-F4 MINOR; round-1 suggestions | REMAINS RESOLVED or TAKEN | Unchanged by the delta |

## Real limits

- **Raw data is private.**
  - Raw captures and per-cycle records for talker cycles other than 1-5, 13, 24 and 75 are not public.
  - For those other 92 cycles, the census rests on the addendum's `hold-events.csv`. For the 8 public cycles I checked that file against the published TSVs, row for row, and its internal consistency holds.
  - The CRF PDU counts, bracketing timestamps and the 0.002000053 s maximum rest on the addendum's replay of private captures. I checked them for consistency with the 2 ms period and with `stop-checks.csv`.
  - I replayed no pcap. `recompute.py` and `declarations.py` were not run end to end; their functions, refusal paths and outputs were exercised.
- **S1 sample.** The S1 observation rests on 8 published cycles and is not a demonstrated cause.
- **No hardware.** Physical calibration was NOT RUN. No hardware was touched, and field skips are not hardware proof.
- **No RTL simulation.** The PR changes no RTL, so the scoped simulator was not needed and was not invoked.
- **Hosted contexts.** At inspection (`receipts/hosted-check-runs.txt`), several exact-head hosted contexts had succeeded. `docs-check`, `elaborate` and Verilator shards 1, 2 and 4 were still in progress, and the physical gPTP context was skipped. The skipped context is not an executed job. I did not treat hosted results as review evidence.
- **Unpublished patterns.** The hygiene-scan pattern list is not published because it enumerates the private terms it searches for. The receipt lists every hit.

## Pending manager duties

- Build and validate the final current-dev candidate at the merge turn (source base `8bc97021f28fb7f729418d3a00851c84ea0b50fd`, live dev `20aa4eabf310a43b654e0c74c5374c3a0458fd4b`), then the post-merge containment.
- Own hosted and act acceptance at the exact head, including the contexts still in progress at inspection.
- #606's body still states the pre-round-3 premise: "In the numbered reconnect cycles, the DUT kept its Talker Advertise through the hold". It also still says the slow path "differs from the fast path by DUT-side state". Cycle 1 contradicts both, and the page (page:249) now points #606 at cycle 1. A correction on #606 is a GitHub write outside this lane's page-and-packet scope.
- If accepted, record R370-3-S1 on #608.
- The second independent review (R371-3), the completion ledger across both reviews, and explicit maintainer authorization are still required before any merge. #75 stays open.
- Publish this report and the files listed in `MANIFEST.sha256`.

R370-3 FINISHED
