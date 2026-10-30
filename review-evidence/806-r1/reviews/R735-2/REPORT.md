[R735] POSITIVE - exact head 0c45ebf28e2c11352aa4ad40d46780143b1a77ab

# Internal cleared-context review of PR #813 (#806), round R735-2 (delta)

- Head `0c45ebf28e2c11352aa4ad40d46780143b1a77ab`, tree `9aa2966798bf164913cef087f6bdf09bd2e69bcf`. Source base and live dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`.
- Delta over the round-1 head `f99405af`: one commit, three documents (`CHANGELOG.md`, `docs/design/AREA_BUDGET.md`, `docs/reference/SUBMODULES.md`), 7 insertions and 3 deletions.
- Round evidence: the author-r2 packet at public commit `8311a3a1` (`review-evidence/806-r1/author-r2`).
- Isolation:
  - Before the verdict, PR data came only from `gh pr view --json title,body,headRefOid,baseRefName,baseRefOid,files,commits` (`receipts/pr813_view.json`).
  - Before the verdict I also read my own round-1 reports (R735-1, R736-1), the #806 issue body, and the #814, #818 and #817 issue bodies (`receipts/issues-814-818-817-bodies.txt`).
  - `INDEPENDENT-VERDICT.md` holds the verdict and ledger. It was written at 2026-10-30T19:02:17Z, before any comment list was fetched.
  - After that I read the PR's comment index and the #806/#814/#818 comment indexes (`receipts/*index*`), plus four manager rulings (`receipts/rulings.txt`).
- No manager source bank runs at this head, and I infer none.

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR is open. All five lenses were applied to the delta and are clean at this head. Lens verdicts on the unchanged code are carried from R735-1, because nothing they depend on changed (see "What the delta can reach"). There is one RESIDUE, R735-2-R1, and two new SUGGESTIONs, S6 and S7. The round-1 SUGGESTIONs S1 to S5 are carried unchanged. The prior RESIDUE R736-1-R1 is RESOLVED.

## What the delta can reach

- `git diff --stat f99405af..0c45ebf2` lists only the three documents. `git diff --raw` shows mode `100644` on both sides of each.
- No RTL, test, script, record, generated file or gitlink changed.
- `git diff --raw cf3ef596..0c45ebf2`, filtered for files other than `.md`, is empty. So since the round-1 bank's synthesis inputs (`cf3ef596`), only Markdown has changed: the directive runs' synthesis checkpoint is this head's.
- Gitlinks at head equal the round-1 bank's (`receipts/source-integrity.txt` against the packet's `author/receipts/vivado/bank-head-and-pins.txt`):
  - `gptp-processor` `135afd04`
  - `protocol-processor` `f65c8ff7`
  - `lwSRP` `08ee86e8`
  - `tsn-c-stack` `70936b77`
  - `verilog-axis` `48ff7a7e`
  - inactive `external` `efeb541a`
- The R735-1 RTL, Robustness, Tests and Conformance verdicts rest on executable artifacts that are byte-identical at this head, so they stand.

## The delta, sentence by sentence

| Location | Old | New | Check |
|---|---|---|---|
| `CHANGELOG.md:76-77` | "That refusal needs an owner decision (#806)." | "Timing recovery is ruled under #814/#818." / "The best directive meets the build floor at every corner." | Matches the manager's prescribed text (#806 issuecomment-6522650491 item 4). It points to the 2026-10-30 ruling (#814 issuecomment-6522621984), which #818 implements. The floor claim is backed by the directive evidence below. |
| `docs/design/AREA_BUDGET.md:144-145` | "...so the gate refuses it; #806 holds the owner decision that refusal needs." | "...so the gate refuses it." / "Timing recovery is ruled under [#814]/[#818]; this change meets the build floor at every corner on its best directive." | Prescribed text, verbatim. Both links resolve to the right issues. "The gate refuses it" stays true of the committed `pp_resource_gate.py`, since #818 is not merged. See R735-2-R1 for the sentence after it. |
| `docs/reference/SUBMODULES.md:429-431` | "#806 holds the owner decision this refusal needs." | "Timing recovery is ruled under #814/#818." / "The best directive meets the build floor at every corner." | Same as the changelog. |

- **Measurements.** No measured figure, verdict, tolerance or threshold changed. The +0.032 ns, 0.408 ns, +0.440 ns, 0.25 ns and 27-slice figures are byte-identical to round 1.
- **Comment rule.** The delta has no source comments and names no lane, round or reviewer.

## Round evidence: the two extra placement directives

### Packet integrity

`scripts/verify_packet.py` writes `receipts/packet-verify.txt`.

- **Manifest.** All 425 entries of `review-evidence/806-r1/MANIFEST.json` match their published sha256, and no file is unlisted.
- **Author-r2 index.** All 89 rows of `INDEX.md` were checked. 79 match the published bytes. The other 10 are exactly the 10 files the manifest marks `path_redacted`, and for each the index hash equals the manifest's `original_sha256`.
- **Commit.** The evidence commit `8311a3a1` is unsigned on GitHub (`receipts/evidence-commit.json`). The packet is hash-anchored, not signature-anchored.

### Same inputs, only the place directive changed

`scripts/check_directive_runs.py` writes `receipts/directive-check.txt` (rc 0). I checked each run's `baseline_implementation.tcl` against the head's own `syn/ooc/pp_baseline.py` and `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:142-185`:

- It starts `set_param general.maxThreads 32` and then `open_checkpoint {.../gateware/alinx_ax7101_synth.dcp}`.
- It ends with exactly `REPORTS + PP_REPORTS + SCOPE_TIMING + quit`.
- It has exactly one `place_design` line, with its own directive. `ExtraPostPlacementOpt` does not appear.
- The two scripts differ in that one line only (`diff`: line 20).

Other inputs:

- **Synthesis checkpoint.** Both scripts open the checkpoint under the round-1 bank's `viv-cf3ef596` tree. `synth-dcp.sha256.before` and `.after` both read `7253a8c0...`, so the checkpoint was not rewritten.
- **IOB packing.** `alinx_ax7101_iob_pack.rpt` is byte-identical (`fc36d445...`) in the round-1 shipping route and in both directive runs.
- **Clock constraints.** Each script sources `clock_constraints.tcl` from the `cf3ef596` clone, whose synthesis inputs equal this head's (see "What the delta can reach").
- **Limit.** The round-1 receipts do not record the checkpoint's hash, and the shipping `alinx_ax7101.tcl` itself is not published. The checkpoint's identity rests on its path, the round-1 bank head file and the unchanged hash, and the script tail rests on the recipe's derivation.

### Figures and the worst corners

- **Utilization.** The head's own gate parser, `pp_resource_gate.utilization(..., "route")`, run on each published `baseline_utilization.rpt`, gives exactly the stated LUT / FF / SLICE / BRAM / RAMB / DSP figures:
  - AltSpreadLogic_high: 51,874 / 53,787 / 15,837.
  - ExtraTimingOpt: 51,849 / 53,787 / 15,837.
- **Routing.** Both `alinx_ax7101_route_status.rpt` files report 0 nets with routing errors (102,971 and 102,962 routable nets). Both `vivado.rc` are 0.
- **No negative slack.** All eight `*_negative.rpt` files are `report_timing -delay_type min_max -slack_lesser_than 0` and read "No timing paths found". So setup and hold are non-negative at every corner of both runs, which proves the hold floor (0 ns) directly.
- **Worst setup.** AltSpreadLogic_high's `worst-setup-path-Slow_0C.txt` reads "Slack (MET) : 0.235ns", Path Type "Setup (Max at Slow Process Corner)". `alinx_ax7101_signoff_grade.txt` states that the fixed Slow/Fast models cover 0 to 85 C and that Tj is power metadata only. So Slow_85C equals Slow_0C, and the operating reports' hashes agree.
- **The stated corners are the worst.** `directive-figures.txt` was extracted with the gate's parsers from each corner's Design Timing Summary (`scripts/directive_figures.py`). Per directive:
  - Worst-corner WNS: +0.235 ns (AltSpreadLogic_high) and +0.218 ns (ExtraTimingOpt), both at the Slow corners. Fast setup is +1.633 ns.
  - Worst-corner WHS: +0.011 ns, at the Fast corners. The pair "+0.235 / +0.037" is the Slow-corner pair, not the worst hold. The PR body's table (Slow and Fast columns) and its gate line ("WHS +0.011 ns") state this correctly.
- **The floor at every corner.** Every corner of both runs meets the build floor (WNS >= +0.030 ns, WHS >= 0). With round 1's ExtraPostPlacementOpt (+0.032 / +0.034), the best directive by worst-corner WNS is AltSpreadLogic_high. That is the delta's "best directive".
- **Limit.** The Fast-corner and Slow_85C summary values, and the hold values, rest on the author's extraction from the unpublished signoff timing reports, whose hashes are published in `large.sha256`. The published raw bytes prove: no negative slack anywhere, Slow worst setup +0.235 ns, and Slow_0C = Slow_85C by model. See S7.

## Gates run here at this head

- **Docs gates.** Each is rc 0 (`receipts/own-docs/`):
  - `scripts/check_doc_style.py`
  - `scripts/docs_check.py`
  - `scripts/check_submodule_docs.py`
  - `scripts/check_gptp_docs.py`
  - `scripts/check_hygiene.py --check`
  - `syn/ooc/pp_resource_gate.py check-baseline`
- **Author's docs receipts at `0c45ebf2`.** The docs workflow is 44 steps, 0 failed, 2 skipped by rule (`docs-0c45ebf2/all.out`, `all.rc` 0). The static table is all rc 0 (`static-0c45ebf2/table.txt`).
- **Integrity.** `scripts/verify_tree.py` writes `receipts/source-integrity.txt` (rc 0):
  - all 1,453 tracked entries match HEAD in bytes and mode;
  - stage-0 index only, with no hidden flags;
  - the gitlinks listed above;
  - a clean status.

  Nothing in the clone was edited. No probe tree was needed this round.
- **Hosted snapshot.** At the exact head (`receipts/hosted-contexts.txt`), 23 contexts are success, 1 skipped, 28 queued or in progress, and none failed. This is a snapshot, not an aggregate verdict.

## Findings

**R735-2-R1 - RESIDUE - Docs - `docs/design/AREA_BUDGET.md:146` - "therefore" has lost its antecedent.**
- Evidence: line 146 reads "The next growth on the shipping image therefore has no slice room". Its reason is the slice sentence at :143 (27 of 15,850 left). The delta put a second timing sentence (:145) between them, so "therefore" now reads as following from "this change meets the build floor".
- Impact: wording only. No figure, verdict or claim changes.
- Exact fix: change line 146's opening to "With 27 slices left, the next growth on the shipping image has no slice room and needs its own owner decision", keeping the link.
- Verification: `check_doc_style.py` rc 0. The sentence names its reason.

**S6 - SUGGESTION - Docs - `docs/design/AREA_BUDGET.md:143-145`, `docs/reference/SUBMODULES.md:414, 431`, `CHANGELOG.md:70, 77` - "best directive" is not named on the pages.**
- Evidence: the 27-slice figure is the recipe's shipping directive (ExtraPostPlacementOpt). The "best directive" of the new sentence is AltSpreadLogic_high, with 15,837 slices (13 free), and the pages name neither. The 13:15 ruling builds the shipping image from the best directive.
- Not a finding: the manager's record rule (issuecomment-6525285974) re-records once on dev from the release image's routes. The author lists this as open risk (1).
- Optional outcome: say "on the recipe's shipping directive" in the slice sentence, or name AltSpreadLogic_high and its +0.235 ns WNS in the new one.

**S7 - SUGGESTION - Tests, Docs - `review-evidence/806-r1/author-r2/receipts/directives/*/` - the per-corner timing summaries are not published.**
- Evidence: only the Slow_0C worst path and the no-negative-slack reports are raw. The Fast and hold figures are the author's extraction, with the source reports' hashes recorded.
- Optional outcome: publish each corner's "Design Timing Summary" block, or a parser receipt over `alinx_ax7101_signoff_*_timing.rpt`, so the +0.011 ns worst hold and the +1.633 ns Fast setup can be re-read. #818's checker will make this routine.

**Carried from R735-1, unchanged (none of their artifacts is in the delta):**
- S1 (Tests): the toggle check's one-interval bound.
- S2 (Tests, Robustness): no silence check while the port is disabled.
- S3 (Tests): no parent test of shadow-level withdrawal.
- S4 (Robustness): the guard-disabled arm is not graded.
- S5 (Docs): no traceability row for 10.2.4.11.

All five remain optional.

**Withdrawn after reading the rulings.** My pre-verdict file listed a second RESIDUE: that "ruled under #814/#818" calls a gate-rule change a "recovery". After the checkpoint I read #806 issuecomment-6522650491. It prescribes that sentence verbatim, and it accurately points to the ruling that #818 implements, so I withdraw it. The verdict is unchanged.

## Prior public review findings at this head

At listing time, after the checkpoint, PR #813 had:
- three review-start comments;
- two verdicts, both mine from round 1 (R736-1 and R735-1, both POSITIVE at `f99405af`);
- 0 submitted reviews and 0 inline comments.

There are no other reviewers' findings.

**R736-1-R1 (RESIDUE, Docs): RESOLVED.**
- At its cause: the three "owner decision" sentences are gone from `CHANGELOG.md:76`, `AREA_BUDGET.md:144` and `SUBMODULES.md:429`. A grep of the three pages finds "owner decision" only in pre-existing, unrelated lines: AREA_BUDGET :121, :146, :147, :525 and CHANGELOG :146, :403.
- PR body: it no longer carries the "accept and re-record, or recover" choice or "the area gate's open decision". It cites #814/#818 (lines 30, 102 and 182 of the body), and its DoD checkboxes stay open.
- Why the text differs from R736-1-R1's suggestion: that suggestion said "no floor or fall exception". It was superseded by the 2026-10-30 13:15 ruling, which makes the fall a warning and keeps the floor exception forbidden. The new text follows the later ruling, as the manager prescribed.

**R735-1 S1 to S5: retained** as optional SUGGESTIONs, listed above.

**Later rulings checked against the delta.**
- The #814 reversal (issuecomment-6527475726) puts #814 back in the release because of the integration image. It states that the integration "decides the image, not this PR".
- The record addendum judges each adoption on its own route set under #818.
- Neither makes the delta's sentences false: this change's own route set meets the floor at every corner on its best directive.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Delta claims against the #814 ruling issuecomment-6522621984 (floor at every corner on the best of three directives; fall a warning), the #818 body, the record addendum issuecomment-6525285974 and #806 round-2 item 4; the floor in `docs/integration/BUILDING.md` section 5; the record at `AREA_BUDGET.md:132-140` (fall 0.205 ns and +57 slices recomputed); unchanged executable conformance from R735-1 (`milan_datapath.sv:3194-3195, 8903`, the shadow and engine port, 802.1AS-2011 10.2.4.11, Milan 4.2.6.2.4/.5) | R735-2 (delta); R735-1 (unchanged code) | `0c45ebf28e2c11352aa4ad40d46780143b1a77ab` |
| RTL | CLEAN | `git diff --stat/--raw f99405af..0c45ebf2` and `cf3ef596..0c45ebf2`: no HDL, constraint or gitlink change; gitlinks equal the round-1 bank (`receipts/source-integrity.txt`); both directive scripts' `place_design` lines, synthesis checkpoint and identical IOB pack; R735-1's RTL evidence stands at identical bytes | R735-2 (delta); R735-1 | `0c45ebf28e2c11352aa4ad40d46780143b1a77ab` |
| Robustness | CLEAN | No executable artifact in the delta (diff raw). Per-corner robustness of the claim: all eight `*_negative.rpt` (min_max, slack < 0) empty; route status 0 errors; `signoff_grade.txt` model coverage 0 to 85 C; R735-1 W1-W7/T1/E-probe evidence unchanged | R735-2 (delta); R735-1 | `0c45ebf28e2c11352aa4ad40d46780143b1a77ab` |
| Tests | CLEAN (S7 optional) | Round evidence: `directive-figures.txt`, `scripts/directive_figures.py`, `make_directive_runs.py`, both `baseline_implementation.tcl` against `pp_baseline.py` and the recipe (`receipts/directive-check.txt`); gate-parser utilization re-run; `worst-setup-path-Slow_0C.txt`; packet hashes (`receipts/packet-verify.txt`); gate logs ("NOT COMPARABLE", which #818 resolves); docs gates rc 0 here (`receipts/own-docs/`) and in the author's `docs-0c45ebf2` and `static-0c45ebf2`; no test bytes changed since R735-1 | R735-2 (delta); R735-1 | `0c45ebf28e2c11352aa4ad40d46780143b1a77ab` |
| Docs | CLEAN (R1 residue; S6, S7 optional) | `CHANGELOG.md:60-79`, `docs/design/AREA_BUDGET.md:128-147`, `docs/reference/SUBMODULES.md:410-436` at head; the PR body (`receipts/pr813_view.json`) for R736-1-R1; `check_doc_style.py`, `docs_check.py`, `check_submodule_docs.py`, `check_gptp_docs.py`, `check_hygiene.py --check` rc 0 | R735-2 | `0c45ebf28e2c11352aa4ad40d46780143b1a77ab` |

## Real limits

- Physical calibration was NOT RUN, and no hardware was used. #806's second acceptance, the in-house link-toggle gPTP scenario on a built image, is outstanding. Field skips are not hardware proof.
- I ran no Vivado, sweep, Yosys, builder, docs-workflow or simulation bank this round. The round's timing evidence is the author's two directive runs, checked against their published bytes (see "Figures and the worst corners").
- The synthesis checkpoint's identity rests on its path, the bank head file and the unchanged hash. The round-1 receipts do not record its hash, and the shipping `alinx_ax7101.tcl` is not published.
- The Fast and hold summary values rest on the author's extraction (S7). The floor itself is proven by the published no-negative-slack reports for hold and the Slow worst path for setup. Fast setup is proven non-negative by the raw reports, and +1.633 ns by the extraction.
- The committed resource gate refuses directive runs as "NOT COMPARABLE", so no committed gate has judged them. #818 adds that comparison.
- The evidence commit is unsigned. Its integrity here is by hash.
- One published receipt (`receipts/rulings.txt`) replaces a host path prefix in a quoted public comment with `<mgmt>`. `receipts/redactions.txt` records both hashes.

## Pending manager duties

- **#818.** Judge this PR's three-directive route set with the #818 gate once it is available, as the record rule prescribes. Do not re-record in this PR: the record is re-recorded once on dev after the last release merge.
- **Merge candidate.** Validate the current-dev merge candidate (builder and native banks), publish the receipts, and own hosted and act acceptance at the exact head. 28 contexts were still pending at the snapshot, and the physical gPTP context was skipped, not executed.
- **Release integration.** Per issuecomment-6527475726, the integration image with #814 decides the shipping image's timing, and this PR's route set does not stand in for it.
- **From R735-1.** Watch the `milan_dp` leg 0 hosted window and refresh `PIECE_SECONDS`, as `docs/testing/CI_WORKFLOWS.md:519` prescribes.
- **Bench.** Keep `Relates to #806` and the issue open until the built-image link-toggle scenario passes on the bench.
- **Residue checklist.** Carry R735-2-R1.

R735-2 FINISHED
