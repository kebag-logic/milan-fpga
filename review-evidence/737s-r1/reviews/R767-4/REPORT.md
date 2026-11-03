[R767] POSITIVE - exact head 9104a8fc68979a7a8795859e8704aef27ea0634d

Round R767-4, internal cleared-context review of PR #836 / issue #737. Head `9104a8fc68979a7a8795859e8704aef27ea0634d`, tree `858d8230dbb684404e9b1a3c033ebfe6aa68ddc7`. Round 4 delta `3b323864..9104a8fc` (three commits: `f3a49b93`, `56e6021a`, `9104a8fc`). It touches four files: `scripts/ci_litex_legs.py`, `scripts/ci_gate_workflows.py` (a comment only), `ci/image/command-table.json` (one pin) and `docs/testing/CI_WORKFLOWS.md`. No workflow, template, HDL or test file changes.

Authority: the manager's round 4 ruling on #737 (issuecomment-6615561789). Executor's REVIEW READY: issuecomment-6617179916.

**Verdict.** All five lenses are clean. The open items are two RESIDUE wording items and two SUGGESTIONs. Every ruling item is met. The author's two departures from the ruling's arithmetic (`LEG_BUDGET` 926, allowance 443) follow from the frozen set's maxima, measured by the stated method, and are accepted. The hosted runs at the exact head all completed green. None of them triggers ruling item 3.

## 1. Ruling item 1: the last re-measurement

I recomputed every component from the jobs API for run 41705989293, attempts 1 and 2 (`receipts/jobs-41705989293-a{1,2}.json`, script `scripts/recompute_r4.py`, output `receipts/recompute-41705989293.txt`). The verdict rows come from the six LiteX job logs (`receipts/rows-41705989293.txt`).

| Component | Stated | Recomputed (run 41705989293) | Agrees |
|---|---:|---|---|
| Setup (span less gate steps and Verilator build) | 739 | a2 `elaborate-gates-1`: 1449 - 710 = 739. Others: 525, 395, 559, 513, 203 / 206, 426, 466, 197 | yes |
| `test_gptp_tx_timestamp` (`LARGEST`) | 477 | a1 459, a2 477 | yes |
| Other `LARGEST` members | unchanged | soc 409 / 472 (≤510), ctrl 240 / 277 (≤284), retained 236 / 331 (≤336), cpu 52 / 70 (≤72), boot 18 / 25, mem 11 / 14 (≤15), gmii 0 / 0 | yes |
| Self-test (leg step less its rows) | 4 | a2 leg 0: 481 - 477 = 4. Others: 3, 2, 3 / 3, 2. Log: step 20:37:11.49 to 20:45:12.12 = 480.6 s | yes |
| Cold Verilator | 431 | 393, 316, 378 (≤431) | yes |
| Builder legs 0 / 1 | 1130 / 1119 | 1010, 1098 / 737, 710 | yes |
| Collector | 183 | a1 183, a2 182 | yes |
| Tail | 29 | a1 29, a2 23 | yes |
| Largest depth-one checkout | 26 | `Cancel late CI failures` a1 26 (aggregate 3 / 15; fail-fast 5 / 10) | yes |
| Aggregate span less checkout | 85 | 18 / 14 (≤85) | yes |
| Spans | 1535 / 1132 / 1414 / 1148 / 1233; 1304 / 1449 / 907 / 909 / 948 | identical | yes |
| Largest checkout / LiteX install / VexiiRiscv | 274 / 277 / 108 | a2 w1 274; a1 w2 277; a2 w1 108 | yes |

Derived figures. My probe (`scripts/probe_budget.py`, `receipts/probe_budget.txt`) imports the head module in memory and edits no file. Its results:
- `LEG_BUDGET` = 2700 - 600 - 739 - 431 - 4 = 926.
- The legs are 461 / 440 / 520 at `SECONDS` and 477 / 448 / 794 at `LARGEST`, so they fit.
- Cold projections are 1651 / 1622 / 1968, warm projections 1220 / 1191 / 1537, and the margins 1049 / 1078 / 732.
- The 927 control is refused: "a LiteX leg holds 927 measured seconds at its largest, above its 926; re-derive the legs or add a leg". The value 926 is accepted.

By hand:
- The builders project at 739 + 1130 = 1869 and 739 + 1119 = 1858, with margins 831 and 842.
- The aggregate is 26 + 85 = 111, with a margin of 69 against 180.
- The allowance is 111 + 183 + 120 + 29 = 443.
- The workflow figure is 1869 + 443 = 2312 (38.5 min) and 1968 + 443 = 2411 (40.2 min), that is 512 and 611 s above 1800.
- The earlier figures are 1615 + 398 = 2013, 1713 + 398 = 2111, 1615 + 338 = 1953 and 255 + 1130 + 338 = 1723.

These figures agree in all four places:
- the code (`scripts/ci_litex_legs.py:47-79`, `scripts/ci_gate_workflows.py:62-64`);
- `docs/testing/CI_WORKFLOWS.md:1671-1692, 3137-3185, 3238-3242, 3280-3300, 3347-3349`;
- the live PR body (Round 4 tables);
- the packet's `PR-BODY.md`, which matches the live body byte for byte apart from a trailing newline.

The command-table pin `5efe84df…` equals `sha256sum scripts/ci_litex_legs.py`.

The departures are accepted on their evidence:
- **`LEG_BUDGET` 926, not 927.** The ruling also orders "use the maxima over the frozen set as you measure them". Round 3's own receipt took the self-test as the leg step less its rows (596 - 593), and that method gives 4 at a2 leg 0, confirmed to the sub-second in the log. Keeping 3 would state a maximum the frozen set exceeds. The change is conservative: the partition still fits, and the 927 control is refused.
- **Allowance 443.** The depth-one checkout is a named component, and it rose to 26 in a1. 436 would keep a superseded 19.

## 2. Ruling items 2 and 3: the frozen set and the merge bar

- `CI_WORKFLOWS.md:3187-3191` freezes the cited runs at the list in `:3137-3140`. That list is the round 3 set plus 41705989293 attempts 1 and 2. The text says later hosted runs, including this change's own, "do not reopen them; they feed the next re-measurement under #737 acceptance 1, which follows this rule". So the rule's "a later hosted measurement" now governs the next re-measurement and not this PR, as item 2 requires.
- `:3201-3206` puts the merge bar directly after the re-measurement rule. It lists a job at its timeout, an elaborate worker's span above 2100 s, a LiteX simulation unrun, run twice or unreported, and a refusing union verifier. It also says a component above its figure inside those limits is an observation for acceptance 1.
- The PR body's Round 4 section has one sentence linking the ruling (body line 94).
- **The 2100 s line is scoped to elaborate workers.** I judge this consistent with the ruling's intent, for four reasons:
  - The ruling's parenthetical derives 2100 from "its 2700 s limit less the 600 s headroom". The 600 s headroom is the elaborate-only `HEADROOM` constant.
  - Item 4 applies the line to worker 4 only.
  - The ruling was written over run 41705989293, in which the 120-minute watcher ran 2299 s, and the manager called that run green.
  - The only workflow this PR changes is `elaborate.yml` (`git diff --stat e61a4afa..9104a8fc -- .github`). The 45-minute jobs in `docs.yml` and `rtl-fast.yml` keep their own bounds and are judged by cause.

  This is not a finding. See S2.

## 3. Prior findings, judged at their cause at this head

Read after my own pass over the diff (`receipts/prior-6615556366.md`, `receipts/prior-6615559663.md`).

| Finding | State at 9104a8fc |
|---|---|
| R767-3-F1 = R768-3-F1 (exact-head run above the stated maxima) | **Resolved.** The run joined the cited set and every figure was recomputed (section 1). The class is closed by the freeze and the merge bar (section 2). |
| R768-3-F2 (`rtl-full` union at its 2-minute limit) | **Settled by the ruling, outside this PR** (`rtl.yml` is unchanged; the class is #837). At this head `rtl-full` 41732022450 is 36 success and 1 skipped (the nightly physical gPTP job), with no union timeout. |
| R767-3-R1 | **Resolved, exact text:** `CI_WORKFLOWS.md:3147` reads "Their largest measured job times with the LiteX legs apart are 1535", with the figures re-measured. |
| R767-3-R2 | **Resolved, both halves.** In the docs, `:3170-3172` reads "and `ci_gate_workflows_selftest.py`, through the LiteX leg controls, requires each LiteX worker's generated limit to equal the 2700 seconds it starts from". In the PR body, Round 3 item 1 reads "The gate workflow self-test requires …" and How to validate reads "fails `ci_gate_workflows_selftest.py` in its LiteX leg controls". Neither old phrase remains. |
| R768-3-RS1 | **Resolved, exact text:** `:3216` "on metadata that builder leg 1 had generated". |
| R768-3-S2 | **Taken:** `:1671-1676` are rewrapped, with no line over 78 columns. |
| R767-3-S2 | **Taken:** the PR body's "Superseded (round 2)" section, placed after Round 4, holds round 2's derived table and workflow paragraph. |
| R767-3-S1, R768-3-S1, observations | Declined by the ruling (#837 / no change). Not reopened. |

## 4. Hosted runs at the exact head, judged only by ruling item 3

Receipts: `receipts/hosted-9104a8fc-jobs.json`, `-summary.txt`, `-litex-rows.txt`, `-union.txt`. All four workflows ran attempt 1 and completed successfully, 71 jobs in all: elaborate 41732022509 (9 jobs), docs 41732022313 (9), rtl-fast 41732022398 (16) and rtl-full 41732022450 (36 success, 1 skipped by schedule).

- **Job at its timeout:** none. Every executed job concluded `success`.
- **Elaborate worker span above 2100 s:** none. Workers 0 to 4 took 1216, 1260, 627, 591 and 876 s; the largest is 840 s inside the line. The LiteX workers restored Verilator.
- **LiteX simulations:** each of the eight ran exactly once and passed. gptp 457 on leg 0; cpu 67, gmii 1, boot 23, mem 14 and retained 305 on leg 1; ctrl 270 and soc 478 on leg 2.
- **Union verifier:** it passed: "elaborate: 5 source gates exactly once; all worker jobs successful", and the LiteX union runs inside `ci_gate_receipts.py verify` (`scripts/ci_gate_receipts.py:131-132`).
- **Observations only, inside limits, for #737 acceptance 1, not findings:**
  - `test_gmii_rx_capture` took 1 s against `LARGEST` 0.
  - Fail-fast watchers ran 1940 to 3756 s under their own limits.

The manager owns hosted and act acceptance. This section records only what the jobs API and logs show.

## 5. Lenses

```text
[R767] PASS Conformance - scripts/ci_litex_legs.py:47-79, docs/testing/CI_WORKFLOWS.md:3137-3206, PR body Round 4, receipts/recompute-41705989293.txt, receipts/rows-41705989293.txt - every ruling item 1 figure recomputed from the jobs API and logs over the frozen set and found equal in code, docs and PR body; the 926/443 departures follow the ruling's "maxima as you measure them"; items 2 and 3 are written beside the rule with the later-measurement wording moved to the next re-measurement; hosted at 9104a8fc meets the item 3 bar.
[R767] PASS RTL - git diff --stat 3b323864..9104a8fc (no HDL, workflow or template file), .github/workflows/elaborate.yml timeout-minutes 45/3/15/120/3 unchanged since 3b323864, receipts/probe_budget.txt - no HDL in scope; the timing and resource reading of this lens (job limits, the leg partition against LEG_BUDGET, margins 732 to 1078 s, aggregate 69 s) was checked against the derivation and holds.
[R767] PASS Robustness - scripts/ci_litex_legs.py:119-121 (refusal), receipts/probe_budget.txt (927 refused, 926 accepted), receipts/hosted-9104a8fc-summary.txt - the over-budget path refuses at one second above the budget; the slowest cold projection is 132 s inside 2100; the aggregate's 3-minute limit keeps 69 s; no hosted job at its timeout.
[R767] PASS Tests - receipts/gates_rc.txt and gate_*.log (ci_gate_workflows.py --check, ci_gate_workflows_selftest.py, ci_litex_legs.py legs, ci_litex_legs_selftest.py, ci_events.py --check, each rc 0 at head), git diff --check e61a4afa..9104a8fc clean, published author-r4 receipts - no test file changes in the delta; the existing controls pass at the new constants, and the author's 927/926 control and dropped-member controls, verified in the packet, can fail for the defect they name.
[R767] PASS Docs - docs/testing/CI_WORKFLOWS.md:1671-1692, 3137-3222, 3280-3300, 3347-3349; PR body Round 3, Round 4, Superseded (round 2), How to validate - figures agree with code; the prior residues are fixed with their exact texts; open wording is RESIDUE only (R1, R2), which leaves the lens clean by the residue rule.
```

## 6. Findings

### R767-4-R1 - RESIDUE - Docs - the PR body calls the 927 control "above both budgets"
- **Where:** PR #836 body, "Where the arithmetic differs from the reviews and the ruling", second bullet, last sentence (body line 133).
- **Evidence:** "The control uses 927, which is above both budgets." 927 is above `LEG_BUDGET` 926 but equal to the ruling's quoted 927, not above it. The control itself is correct (`receipts/probe_budget.txt`; packet `g10-control-largest-over-budget.txt`).
- **Impact:** wording only. It changes no figure or control.
- **Exact fix:** replace it with "The control uses 927, one second above the 926 s budget and equal to the ruling's quoted figure; it is refused, and 926 is accepted."

### R767-4-R2 - RESIDUE - Docs - "they were 338 and 1953" pairs two values with the plural "figures"
- **Where:** `docs/testing/CI_WORKFLOWS.md:3289-3290`.
- **Evidence:** "… the allowance was 398 seconds and the figures 2013 and 2111; before attempt 3 of run 41678609075 raised the aggregate's figure, they were 338 and 1953." At that point only the warm figure was stated (1615 + 338 = 1953; at `3b323864` the text read "the allowance was 338 seconds and the figure 1953").
- **Impact:** wording only. A reader may look for a missing cold value.
- **Exact fix:** "… raised the aggregate's figure, the allowance was 338 seconds and the warm figure 1953."

### R767-4-S1 - SUGGESTION - Docs - the code comment still points at the rule "a later hosted measurement follows"
- **Where:** `scripts/ci_litex_legs.py:50-51`.
- **Evidence:** the docs now apply that rule to the next re-measurement under #737 acceptance 1 (`CI_WORKFLOWS.md:3187-3191`). The comment is still true, but it reads as if any later run re-sets `LARGEST`.
- **Optional change:** "docs/testing/CI_WORKFLOWS.md states the rule the next re-measurement follows (#737)". This needs the command-table pin updated with it.

### R767-4-S2 - SUGGESTION - Conformance, Docs - record the 2100 s line's elaborate scoping on #737
- **Where:** `CI_WORKFLOWS.md:3203`, PR body line 94, and the REVIEW READY's open question.
- **Evidence:** the ruling says "a job's measured span". The author narrowed it to elaborate workers and said so publicly. Section 2 finds this consistent with the ruling's intent.
- **Optional change:** the manager confirms the scoping in one line on #737, so that the next re-measurement inherits a recorded decision rather than a reviewer's reading.

### Observations, not findings
- The self-test component, "leg step less its verdict rows", also absorbs whole-second row truncation and per-member runner overhead. At a2 leg 0 the self-test itself took 2.2 s and the row was 477 for 478.2 s of simulation. This is conservative and the docs state the definition.
- The author's local leg runs (gptp 518 s, soc 570 s) exceed the hosted `LARGEST`. They are local machine figures and outside the frozen hosted set.
- Comment rule: the delta's new source comments name run IDs, workers and attempts with `#737`. They contain no lane label, round, reviewer ID or comment ID, so there is no RESIDUE.

## 7. Packet verification

- The 79 files under `review-evidence/737s-r1/author-r4/` at `24a7eef7a100c7a9e765988acabc9bc5a1877c01` were fetched by blob. Each one's sha256 equals its `published_sha256` in `MANIFEST.json`; there are no extras and none missing.
- Every receipt `.rc` names head `9104a8fc68979a7a8795859e8704aef27ea0634d`. Each has rc 0 except the two intended refusal controls (`g10a-control-dropped`, `g11b-verify-dropped`, rc 1).
- In the local legs every simulation passed once.
- The evidence commit carries no GitHub signature (`verification.reason: unsigned`), so the packet is checked by manifest hash, not by signature.

## 8. Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ruling items 1-3; `scripts/ci_litex_legs.py:47-79`; `CI_WORKFLOWS.md:3137-3206`; PR body Round 4; jobs API and logs for 41705989293 a1/a2 and 41732022509 | R767-4 | 9104a8fc68979a7a8795859e8704aef27ea0634d |
| RTL | CLEAN | delta file list (no HDL, workflow or template); `elaborate.yml` limits; partition and margin derivation | R767-4 | 9104a8fc68979a7a8795859e8704aef27ea0634d |
| Robustness | CLEAN | `partition()` refusal; 927/926 probe; 2100 s and aggregate margins; hosted job conclusions | R767-4 | 9104a8fc68979a7a8795859e8704aef27ea0634d |
| Tests | CLEAN | five focused gates rc 0 at head; `git diff --check`; author-r4 receipts and controls | R767-4 | 9104a8fc68979a7a8795859e8704aef27ea0634d |
| Docs | CLEAN (RESIDUE R1, R2 carried) | `CI_WORKFLOWS.md` changed regions; PR body; prior residue texts | R767-4 | 9104a8fc68979a7a8795859e8704aef27ea0634d |

Code outside the round 4 delta keeps its prior lens verdicts. The delta changes only constants, comments, a pin and prose, so nothing those verdicts depend on has changed.

## 9. Real limits

- This was a delta review. The full parent, PP, gPTP, Yosys and builder banks, act/Docker and the LiteX simulations were not run by this reviewer. The author's published leg receipts stand for the latter.
- No manager source bank exists at this head, and none is inferred. Physical calibration was NOT RUN; skips are not hardware proof.
- The self-test figure in earlier cited runs was not re-derived from their logs. I relied on round 3's published 596 - 593 receipt. The new run's 4 is the maximum unless an earlier run exceeded it, which the round 3 reviews did not find.
- The packet is checked by manifest hash only (unsigned commit).

## 10. Pending manager duties

- Hosted and act acceptance at 9104a8fc. All four workflows were green when observed, 71 jobs.
- The current-dev merge candidate (builder and native banks) at the merge turn. Base `e61a4afa` equals live dev `e61a4afa` as of the brief.
- Carry R767-4-R1 and R767-4-R2 to the residue checklist. Optionally record S2 on #737.
- The second independent positive (the external review) and the full completion bar. #737 acceptance 1 stays open, and so does #837.

Clone state after the review: HEAD `9104a8fc`, `git status --porcelain` empty, no index changes. The six submodule gitlinks are unchanged (external `efeb541a`, gptp-processor `135afd04`, protocol-processor `a9e84b66`, lwSRP `08ee86e8`, tsn-c-stack `70936b77`, verilog-axis `48ff7a7e`).

R767-4 FINISHED
