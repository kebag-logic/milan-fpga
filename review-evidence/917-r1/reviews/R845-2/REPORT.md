[R845] NEGATIVE - exact head 8f73ade54366cc832bad3386c8b6f3bbb12ca5e4

Round R845-2: an internal, cleared-context, independent review of issue #917 / PR #918. It is a delta review of `3926c271..8f73ade5`, one commit by the executor, answering R845-1 (NEGATIVE) and R846-1 (NEGATIVE) under the manager's round-2 ruling on R846-1 F2. The tree is `ae584aff6a5a4e2dc9dde81b170c893cde65a2da`; the source base is `cec88385`.

## Verdict in brief

Every round-1 finding is answered at its cause, and each answer checks out against code and receipts:

- **B7, B8 and B9** are real checks. Each one fails by name for its planted RTL defect through both adapters (author receipts). I added my own plants in the host model, and B7, B8 and B9 each catch theirs by name there too (P2).
- **The clause attributions** now match the standard's text (P7).
- **The budget grader** credits a held commit to its own frame. It refuses the commit cases it is meant to refuse. Its old rule is planted and caught, both on synthetic logs and on the real logs.
- **The `aecp-held` rows** at 1x1 and 8x8/1if fit their bound and their 6 ms allowance.
- **The RTL** changed in comments only.

**One MINOR finding remains**, so the verdict is NEGATIVE. FR_NFR.md 3.4.1's held-allowance column and the held margins computed from it are a hand-written copy of the per-channel figure that the generator derives from `refill_ms`. No gate ties the two together. I changed AECP's `refill_ms` in a disposable copy: the generated table moved to 11 ms, FR_NFR still read 6 ms and 213 ms, and every contract and doc gate passed (P1). That departs from the ruling's term "stated once and generated from mailbox.yaml's refill_ms". It also contradicts FR_NFR's own sentence that "a change to a channel's `refill_ms` moves them".

Beyond that: two RESIDUE items (wording only), and three SUGGESTIONs.

## Scope reconstructed

I read, in this order:

1. AGENTS.md and CONTRIBUTING.md (by section).
2. docs/README.md.
3. Issue #917: the frozen acceptance, plus the decision on #665 ruling item 2 (hold, not drop; the table's figures stay; no firmware image change).
4. The manager's round-2 ruling on R846-1 F2, as restated in the assignment and in the PR's Round 2 section. It sets a per-path ingress allowance:
   - a record that finds a token keeps 64 clocks / 1 ms;
   - a held record gets one refill period of its channel plus 1 ms, stated once and generated from `refill_ms`;
   - every margin that subtracts ingress is recomputed;
   - the grader's attribution is fixed;
   - a held scenario with a negative control is added;
   - no bound changes.
5. The interface authorities: FR_NFR.md 3.4.1, MAILBOX_CONTRACT.md (generated), MAILBOX_SPLIT.md "The held frame", and `mailbox.yaml`.
6. IEEE 1722.1-2021 9.2.2, 9.2.2.4, 9.3.2.6 and 9.3.6, read in the standard's text.
7. `git diff cec88385..8f73ade5` and the round-2 delta `3926c271..8f73ade5`. I read the delta before any evidence.
8. The author packet `review-evidence/917-r1/author-r2` at archive `24755cf4`.
9. Only after my own pass: R845-1 (PR #918 issuecomment-6899723183) and R846-1 (issuecomment-6899591157).

## Findings

### F1 - MINOR - Conformance, Docs, Tests - FR_NFR's held allowance and held margins are an unchecked copy of the generated per-channel figure

- **Where:**
  - `docs/reference/FR_NFR.md:422-436`: the "`T_ingress`, held" column (6 ms) and the held margins 173/183, 213/223, 223/233 and 213/223. The sentence at `:425` says "a change to a channel's `refill_ms` moves them".
  - `sw/mailbox/mailbox_emit.py:216-235`: the generated per-channel column.
- **Authority/evidence:**
  - The round-2 ruling requires the held allowance to be "stated once and generated from mailbox.yaml's refill_ms".
  - The per-channel figure is generated into MAILBOX_CONTRACT.md (`:874-882`). The harness also derives it from the contract (`held.py:28-30`).
  - FR_NFR states it a second time, by hand, in the normative margin table. No gate compares the two: `gen_mailbox.py --check`/`--crosscheck` cover only generated outputs, and `docs_check.py` does not read the figure.
  - Probe P1 (`receipts/P1-fr-nfr-mirror.txt`) used a disposable copy of 8f73ade5 with AECP `refill_ms` changed from 5 to 10, then ran `gen_mailbox.py --write`:
    - MAILBOX_CONTRACT's AECP row became "11 ms";
    - `--check`, `--crosscheck` and `docs_check.py` all passed with 0 findings;
    - FR_NFR.md still reads `6 ms | 213 ms | 223 ms` for the AECP rows.
  - Today's figures are arithmetically right: 200-20-1-6=173, 240-20-1-6=213, 250-20-1-6=223, and +10 ms at the proposal. The defect is that nothing keeps them right.
- **Impact:**
  - A later change to a channel's rate would leave FR_NFR 3.4.1's normative response margins overstated with every gate green. For AECP at 10 ms they would be 5 ms too large.
  - The harness would meanwhile hold records to the new allowance. The two authorities would disagree silently, which is exactly the drift the ruling's "generated" term exists to prevent.
  - The figure, the margins and the clause claim are not wording, so this is not residue.
- **Required outcome:** the held allowance in FR_NFR 3.4.1's table, and the held margins computed from it, are either generated from the contract or checked against it by a gate that fails when they diverge. For example, `gen_mailbox.py --check` or a docs gate could recompute timeout - bound - `T_egress` - (`refill_ms` + 1) for each held row's channel. Alternatively, FR_NFR could state the held allowance only by reference to the generated table, and keep the held margin figures where a generator writes them. The FR_NFR sentence at `:425` must describe the mechanism that actually exists.
- **Verification:**
  - Rerun P1 (`refill_ms` 5 to 10 in a disposable copy, regenerate): a gate must fail, or FR_NFR's held rows must move to 11 ms and 208/218/208 ms.
  - At the unchanged head, the figures stay as published and every gate passes.

### R1 - RESIDUE - Docs - `tb/verilator/mbx/suite.hpp:1648-1650`: a new source comment names bench lane labels

- **Rule:** source comments never show bench lane labels (owner comment rule, 2026-10-15). This comment is new in the reviewed delta.
- **Exact fix:** change "`// #917, what a held record leaves for the frames behind it: the free space past it (B7), the frames the filter refuses behind it (B8) and a channel closed while it is held (B9).`" to "`// #917, what a held record leaves for the frames behind it: the free space past it, the frames the filter refuses behind it and a channel closed while it is held.`"
- **Not covered by this residue:** the `"B7 ..."` strings passed to `ck_.dec`/`ck_.that` and used in `mutants.py` arms. Those are executable check names, not comments.

### R2 - RESIDUE - Docs - PR #918 body, "Known limitations", the CPU budget harness bullet: the stated reason for "none of them holds a record" is wrong

- **Problem:** the bullet says that in the recorded 94-group logs "a hold there would have been a commit following no frame, a refusal". At `cec88385` and `84d8a214`, however, the harness observed only `commit_w`, and a held record's commit is `rel_w`. So a hold in those logs prints no line at all (P8).
- **The conclusion still stands:** round 1's own receipt (`author-r1/receipts/budget/compare-1x1.txt`) shows all 94 logs byte-identical between the base, which drops a no-token frame, and `84d8a214`, which holds it. So no population frame met an empty bucket. Only the reason is wrong; no figure, verdict or measurement changes.
- **Exact fix:** replace "(a hold there would have been a commit following no frame, a refusal, and both recorded runs have none)" with "(the base, which drops a frame its bucket has no token for, and `84d8a214`, which holds it, recorded byte-identical logs for all 94 groups, so no frame of the population met an empty bucket)".

### S1 - SUGGESTION - Tests - the `aecp-held` group at the two-interface 8x8 point

- `held.groups()` is part of every point's population (`scenario.py:995-999`), and the harness README says group `aecp-held` "measures it at every point".
- It was run at 1x1 and 8x8/1if, as the ruling asks. The two-interface `8x8` point has not run it.
- **Suggestion:** run it with the next population run, or state the points it has run at.

### S2 - SUGGESTION - Docs (evidence packet) - `review-evidence/917-r1/author-r2/INDEX.md` is stale for four files

- Four rows do not match their files (P6). Each committed file is 8-12 bytes shorter than its INDEX row, which is consistent with a sanitizing pass after indexing:
  - `receipts/workflows/logs/docs__docs-gates-1__gate_25_0.log`
  - `docs__docs-gates-2__gate_25_1.log`
  - `elaborate__elaborate-gates-0__gate_15_0.log`
  - `elaborate__elaborate-gates-1__gate_15_1.log`
- The other 426 rows match. The archive commit pins the content, and the four logs' verdict lines are intact (`ALL GATES PASS EXCEPT n NOT RUN`, with reasons). None of them supports a delta claim this review relies on, and the workflow acceptance is the manager's.
- The packet is neither signed (the archive commit carries no signature) nor accompanied by a signature file. The INDEX is its only attestation besides git.
- **Suggestion:** regenerate INDEX.md after the last sanitizing pass.

### S3 - SUGGESTION - Docs - say that the held row's figure already includes its ingress

- The `aecp-held` row is measured from the frame's last byte, so its 5.236 ms includes the 4.986 ms held delay. It is graded against the 20 ms bound.
- FR_NFR's held margins then subtract the 6 ms held `T_ingress` again, on top of that bound. This is conservative, not wrong.
- **Suggestion:** one sentence in FR_NFR 3.4.1 or the harness README saying the held row's measurement already contains its ingress, so a reader does not take the two as one quantity counted twice.

## Prior public findings, resolved or retained at this head

| Prior finding | State at 8f73ade5 | Evidence |
|---|---|---|
| R845-1 F1 MINOR (Tests, Robustness, Docs): free space past a held record | **Resolved** | <ul><li>B7 (`suite.hpp:1652-1692`) fills the ring to room for one record; the held record takes it; the next frame counts in RX_DROP, not RATE_DROP; unread records and the held one are byte for byte.</li><li>Arm `rx-space-from-the-committed-head` (+`-axil`), `mutants.py:679-681`, is caught by name: "B7 with the ring holding room for one record…" got=0 exp=1 (author `mutants-full-8f73ade5.log`, clean clone, 242/242).</li><li>My model plant of the same defect is caught by name on the host model (P2).</li><li>The README row (`README.md:452`) now matches its arm (`mutants.py:674-676` removes the `cused_w` guard).</li></ul> |
| R845-1 F2 MINOR (Tests, Robustness): filtered and cut frames behind a held one | **Resolved** | <ul><li>B8 (`suite.hpp:1694-1720`) sends a foreign target, a 22-byte cut and a 14-byte stub: no counter, no ERR, and the held record is committed whole.</li><li>Arm `rx-refused-behind-held-counted` is caught by name (got=2 exp=0).</li><li>My model plant is caught by name (P2).</li></ul> |
| R845-1 F3 MINOR (Tests, Robustness): close with a frame held | **Resolved** | <ul><li>B9 (`suite.hpp:1722-1745`) closes the channel with `FILTER_EN` while a frame is held. The frame is committed at the next refill, and the closed channel then takes and counts nothing.</li><li>Arm `rx-release-gated-on-open` (`mutants.py:687`) is caught by name (got=16 exp=17).</li><li>My model plant is caught by name (P2).</li><li>The documented behaviour is unchanged (`MAILBOX_SPLIT.md:296-299`).</li></ul> |
| R845-1 R1 / R846-1 R1 RESIDUE: issue-comment ID in source comments | **Resolved** | <ul><li>No added source line in `cec88385..8f73ade5` carries `6894152131` or any comment ID.</li><li>The only occurrence in the tree is the ruling link in `docs/design/MAILBOX_SPLIT.md:275`, a prose page, which the rule allows.</li></ul> |
| R845-1 R2 RESIDUE: "What is dropped" overstates | **Resolved** | `MAILBOX_SPLIT.md:306-311` uses the exact fix and adds the RX_DROP case; `KL_mbx_rx.sv:38-49` and `mailbox.yaml:1098-1100` agree. |
| R845-1 S1 SUGGESTION: state the one-in-flight limit | **Taken** | `MAILBOX_SPLIT.md:312-317` "Its limit", and PR Known limitations. |
| R846-1 F1 MINOR (Conformance, Docs): one-in-flight attributed to 9.2.2.4; bench deadline called a timeout | **Resolved** | <ul><li>One in flight is now #917's measured workload; pipelining is cited to 9.2.2, whose text permits it; timeout and retry are cited to 9.3.2.6 and 9.3.6 (P7).</li><li>B0's deadline is next-refill delivery (`suite.hpp:394-400`).</li><li>9.2.2.4 remains only on the message_type filter rows.</li><li>B0/B1/B2 are green (shard receipt), and `rx-drop-instead-of-hold` is caught by B0 by name.</li></ul> |
| R846-1 F2 MAJOR (Conformance, Tests, Docs): held path vs. ingress allowance and attribution | **Resolved in its cause; F1 above is a new MINOR on how the allowance is stated** | <ul><li>Per-path allowance: FR_NFR 3.4.1 (`:422-438`) and the generated channel table (`MAILBOX_CONTRACT.md:874-882`).</li><li>Margins recomputed and arithmetically correct.</li><li>The 64-cycle token bound is kept (`grade.py:56`).</li><li>Attribution: `held.py:33-62`. RXH binds the frame just ended. RXR is credited to the channel's held frame, never a later or another channel's frame. Refused: a commit with no hold (duplicate or other channel), a second hold, and a commit outside (end, end+allowance]. Never-committed records are not served, and their probe gets "no start", which `run.py:112` counts.</li><li>Synthetic checks: nine, all pass in my own self-test run at the head (P3, `self-test: 0 failures`); the old rule's mutant (`selftest_mutants.py:446`) is caught by name.</li><li>Real logs at 1x1 and 8x8/1if (author receipts): one RXH and one RXR each; the held record is credited to the probe and the two followers are refused; the negative control is refused ("the receive commit at 100500065 follows no frame"); rows 5.236 / 5.114 ms with ingress 4.986 ms, allowance 6.0 ms, budget 20 ms.</li><li>94-group regrade byte-identical at base and head (1x1).</li></ul> |

## Per-lens results

The format is: lens, result, artifact (at 8f73ade5), and what was checked against what.

- `[R845] UNCLEAN Conformance — docs/reference/FR_NFR.md:422-436, sw/mailbox/mailbox_emit.py:216-235 — F1`
  - The per-path allowance follows the ruling in value: 1 ms with a token, refill+1 ms held, AECP and ACMP 6 ms. Every margin that subtracts ingress is recomputed correctly, and no bound changed.
  - The ruling's "stated once and generated" term is not met for FR_NFR's copy (P1).
  - Clause attributions 9.2.2, 9.2.2.4, 9.3.2.6 and 9.3.6 match the standard's text (P7).
  - #917's bench acceptance holds as before: 50 one-in-flight reads none lost (B0), the third behind a held one counted (B1), and no firmware image change (46 fixture images and both split images identical by hash, author receipts).
- `[R845] PASS RTL — hdl/milan/mailbox/KL_mbx_rx.sv (8f73ade5), receipts/P4-rtl-comment-only.txt — comment-only delta`
  - The non-comment source is identical to 3926c271: 577 lines, by my own comment-stripped compare. sv2v output is byte-identical (author receipt).
  - `hdl/`, `sw/firmware/` and every submodule gitlink are otherwise untouched.
  - The rewritten header comment (`:35-49`) matches the code: `vd_acc_r` requires `!bad_w` ("fits"), and `rel_w[c] = refill_w[c] && held_r[c]` is not gated on `open_i` ("open channel or not").
  - Both round-1 RTL verdicts at 3926c271 were CLEAN, and nothing they depend on changed.
- `[R845] PASS Robustness — tb/verilator/mbx/suite.hpp:1648-1745, receipts/P2-model-plants.txt — invalid state behind a held record`
  - Covered behind a held record: a full ring (B7), filter-refused frames and truncated ones (B8), and a channel closed while one is held (B9).
  - Each is graded on both adapters and on the host model (547/547 unplanted). Each one's planted defect is caught by name on the RTL (author) and on the model (mine).
  - Reset during a hold (B3) and a refill in the header clock (B5/B6) are unchanged and green.
  - In the grader, malformed observation orders are refused: no hold, second hold, late, other channel, never committed.
- `[R845] UNCLEAN Tests — FR_NFR.md:422-436 (no gate), receipts/P1-fr-nfr-mirror.txt — F1`
  - Otherwise clean:
    - the new mailbox checks each fail for their claimed defect (242/242, three new arms plus the corrected row);
    - the harness's nine held checks pass, and the old attribution is caught by name (P3);
    - the real-log negative control is caught;
    - the 94-group regrade is byte-identical;
    - firmware control mutants 699/699; shard 1/4 17/17, with `milan_dp_render` rerun at rc 0 after a wall-clock timeout.
- `[R845] UNCLEAN Docs — FR_NFR.md:425 — F1`; residue R1 and R2 do not leave the lens unclean.
  - MAILBOX_SPLIT "The held frame" (`:273-338`), the mbx README (`:168`, `:433-456`), the harness README "A held record", and the suite counts (`MAILBOX_SPLIT.md:1778`, `:1785`: 622/629, 667/674 and 547) match the shard receipt.

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | FR_NFR.md 3.4.1, MAILBOX_CONTRACT.md channel table, mailbox_emit.py, MAILBOX_SPLIT.md "The held frame", KL_mbx_rx.sv header, IEEE 1722.1-2021 9.2.2/9.2.2.4/9.3.2.6/9.3.6, #917 acceptance and #665 ruling item 2, round-2 ruling | R845-2 | 8f73ade54366cc832bad3386c8b6f3bbb12ca5e4 |
| RTL | CLEAN | KL_mbx_rx.sv (comment-only delta: P4, author sv2v receipt), verdict/release logic `:569-613`, `:731-746` | R845-2 | 8f73ade54366cc832bad3386c8b6f3bbb12ca5e4 |
| Robustness | CLEAN | suite.hpp B7-B9 `:1648-1745`, host model `mbx_model.c:258-275,551-571` with plants (P2), held.py refusals | R845-2 | 8f73ade54366cc832bad3386c8b6f3bbb12ca5e4 |
| Tests | UNCLEAN (F1) | mutants.py `:674-691`, mutants-full receipt 242/242, round2-arms receipt, model plants P2, selftest_held.py and selftest_mutants.py `:446-448` with my self-test run P3, aecp-held receipts (1x1, 8x8-1if), regrade94 receipts, shard 1/4 receipt, workflow receipts, P1 | R845-2 | 8f73ade54366cc832bad3386c8b6f3bbb12ca5e4 |
| Docs | UNCLEAN (F1) | FR_NFR.md, MAILBOX_SPLIT.md, MAILBOX_CONTRACT.md, mbx README, ctrl_service_budget README, PR body Round 2 and Known limitations, author packet INDEX (P6) | R845-2 | 8f73ade54366cc832bad3386c8b6f3bbb12ca5e4 |

## My probes and receipts

| Receipt | What it shows |
|---|---|
| `receipts/P1-fr-nfr-mirror.txt` | AECP `refill_ms` 5 to 10 in a disposable copy: the generated table moves to 11 ms, all contract and doc gates pass, FR_NFR still says 6 ms / 213 ms (F1) |
| `receipts/P2-model-plants.txt`, `scripts/model_plants.py` | The host model at two interfaces: unplanted 547/0. Three plants (space from RX_HEAD, filter-refused counted as a rate drop, release gated on open) are each caught by B7, B8 and B9 by name |
| `receipts/P3-budget-selftest-8f73ade5.log` | `run.py --self-test` at the head: nine held checks PASS, the old-rule mutant caught, `self-test: 0 failures` |
| `receipts/P4-rtl-comment-only.txt` | KL_mbx_rx.sv non-comment source identical, 3926c271 against 8f73ade5 |
| `receipts/P5-clone-restored.txt` | The clone after probes: HEAD/tree exact, porcelain 0, index equal to HEAD, 1608 tracked blobs equal by hash, submodule gitlinks matching |
| `receipts/P6-packet-index.txt` | Author packet INDEX against its files: 426 of 430 match, 4 workflow logs differ (S2) |
| `receipts/P7-clause-check.txt` | The cited IEEE 1722.1-2021 clauses against the standard's text |
| `receipts/P8-population-hold.txt` | Why the 94-group population holds no record, and why the PR's stated reason is wrong (R2) |

## Real limits of this round

- **No manager source bank at this head.** Source-head execution evidence is the author's published receipts. I spot-checked them and reran only the harness self-test, the model plants, the generator/doc gates in P1 and a comment-stripped RTL compare.
- **Not run by me:** the mailbox suite through the adapters, `make mutants`, the `aecp-held` scenario, the 94-group regrade, firmware gates, image builds and the shard. For those I relied on the author's receipts.
- **No hosted check runs** exist for 8f73ade5 (the check-runs and workflow-runs APIs report 0). Hosted/act acceptance is the manager's.
- **Physical calibration NOT RUN.** The on-hardware acceptance (three descriptor walks with none unanswered) is not run, and field skips are not hardware proof.
- **The 8x8/1if harness exits 1** on three stated-cost lines (build passes during link-up over `ctrl_loop.h`'s one-interface costs). The existing `aecp` group shows the same lines (author control receipt). It is KNOWN and belongs to #914's 8x8/1if measurement; every row is within its bound. It is not a finding of this PR.
- **The two-interface `8x8` point** has not run `aecp-held` (S1).
- **The author packet is unsigned**, and its INDEX is stale for four files (S2).

## Pending manager duties

- Rule on F1's remedy, generating or gating FR_NFR's held columns, and re-review the fixing head.
- Carry R1 and R2 to the residue checklist.
- Hosted/act acceptance at the exact PR head, and the current-dev merge-candidate build (source base `cec88385`, live dev `6b66f66d89cf25d2717687bcc2c3bf617685a99a`) with its builder and native banks.
- Post-merge containment.
- Keep `Closes #917` pending the hardware walks, as the PR's Known limitations ask.

R845-2 FINISHED
