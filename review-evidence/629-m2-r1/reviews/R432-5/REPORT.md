[R432] POSITIVE - exact head 2bc5adc0bfd981e63e82ada5e673ce69cab4f4ee

Round R432-5. Internal independent re-review of PR #634 (issue #629, lane M2) at the **unchanged** head `2bc5adc0bfd981e63e82ada5e673ce69cab4f4ee` (tree `0a3979f48d426c6dbb50d00d2204fb6b4e5fba8c`). This round checks only the PR body. My R432-4 round was NEGATIVE on one MINOR: R432-4-F1, the gsi anchor count in the Round 4b row of the body. The code, tests, merge and image have not changed since R432-4, so this round does not re-review them.

The verdict is POSITIVE. R432-4-F1 is corrected and matches the receipt. The only other byte difference in the body is one added trailing newline. It is invisible when the body renders and changes no text, and I record it as R432-5-S1 (SUGGESTION, no action needed). No MINOR, MAJOR or BLOCKER is open.

## What I checked

1. **The corrected figure.** Line 195 of the live body (the Round 4b row "The other campaigns' controls against the reshaped request") now reads "None of the render (4), render-CSR (3), crflic (6) or gsi (12, eleven in the processor top) anchors ...". A word-level diff against the body R432-4 reviewed shows one change, `'(11, ten' -> '(12, eleven'` (`line195_worddiff.txt`).
2. **The figure against the receipt.** The author's receipt `review-evidence/629-m2-r1/author-r4b/receipts/campaigns/restart_controls_probe.log` (evidence branch tip `a1ae6104`, file last changed in `08719f06`) has these per-campaign rows: gmstep 20, render 4, render-CSR 3, crflic 6, gsi 12. It also has one contrast row, `[gmstep, as published at c1288648]`. That accounts for its closing line, "46 anchors, 0 not found exactly once". Of the 12 gsi anchors, 11 are at `protocol_processor_top.sv` and one is at `milan_datapath.sv:4936-4937`. So 20 + 4 + 3 + 6 + 12 = 45, which equals the body's stated "all 45 control anchors of the five `milan_dp` campaigns". The campaign's own table at the head agrees independently: `tb/verilator/milan_dp/gsi_mutants.py:99-131` plants 1+2+1+1+1+1+3+2 = 12 edits, 11 of them `"pp"` and one `"dp"`.
3. **No other text changed.**
   - The author file `author-r4b/PR-BODY.md` is byte-identical to the body version that R432-4 reviewed, the edit of 2026-10-03T07:53:19Z in the PR's public edit history (`body-as-reviewed-R432-4.md`).
   - The live body is the correction edit of 08:38:04Z. It differs from that version in two places only: the one figure on line 195, and one extra trailing `\n` at end of file (`body-R432-4-to-live.diff`).
   - Remove that trailing newline and the live body equals the author file with only `gsi (11, ten in the processor top)` replaced by `gsi (12, eleven in the processor top)`. The scripted equality check prints `True` (`line195_worddiff.txt`).
   - No other occurrence of the count appears in the body.
4. **The manager's correction comment** (PR #634 comment 5967252070) describes exactly this change. It states that the head is unchanged at `2bc5adc0`. It also states that the earlier REVIEW READY comment is left unedited under the assignment rule.
5. **Head and base unchanged.** PR head oid is `2bc5adc0`. Live `dev` is `1269cdafb4bb964c757baae0f0c5a932d43f540b`, the same as the source base. My clone's worktree and index equal HEAD, and the gitlinks are at their recorded commits (`head_integrity.log`). I ran no probes, so no clone restore was needed.

## Findings

### R432-5-S1 - SUGGESTION - Docs - PR #634 body, end of file - one trailing newline added by the correction edit

- **Evidence:** the live body is 325 lines and ends `Done\n\n`. The author file and the body R432-4 reviewed are 324 lines and end `Done\n` (`body-R432-4-to-live.diff`: `323a324 >` empty line).
- **Impact:** none. Markdown renders a trailing blank line as nothing. No figure, claim, measurement or verdict moves. The only cost is that a byte comparison against the author file shows a second, empty hunk.
- **Required outcome:** none. Optionally, keep the stored body byte-identical to the published author file apart from intended edits, so that future body-only re-checks diff to exactly the intended hunk.
- **Verification:** `diff author-r4b-PR-BODY.md live-PR-BODY.md` shows only the line-195 hunk.

No BLOCKER, MAJOR, MINOR or RESIDUE.

## Prior findings at this head

| Finding | Severity | State at `2bc5adc0` (R432-5) | Evidence |
|---|---|---|---|
| R432-4-F1, gsi anchor count 11/ten vs receipt 12/eleven | MINOR | **RESOLVED** | Live body line 195 reads "gsi (12, eleven in the processor top)". 20+4+3+6+12 = 45 matches `restart_controls_probe.log` and `gsi_mutants.py:99-131`. The REVIEW READY comment 5966931872 still says "gsi (11)". Under the assignment rule it is left unedited, and correction comment 5967252070 publicly supersedes it. |
| R432-4-S1, no check grades a followed-AAF restart on a PHC re-base cycle | SUGGESTION | **RETAINED** (optional Issue, the manager's) | Head unchanged |
| R432-3-S1 = R433-3-S1, `$(error)` database parse counts as read | SUGGESTION | **RETAINED** (optional Issue, the manager's) | Head unchanged |
| R432-3-R1 = R433-3-R1, "The last two" | RESIDUE | **TAKEN** (as recorded at R432-4) | Head unchanged |
| F-A512-1 (found by the author, Tests) | ruled in-PR | **RESOLVED** (as recorded at R432-4) | Head unchanged |

## Lens results

[R432] PASS Conformance — PR #634 live body line 195 vs `body-as-reviewed-R432-4.md` — the only changed text is a count, and it makes no new or altered clause, requirement or acceptance claim. The tree is unchanged at `0a3979f4`, so R432-4's conformance coverage of `hdl/milan/milan_datapath.sv:3205-3232` still stands at this head.

[R432] PASS RTL — `head_integrity.log` (tree `0a3979f4`, gitlinks `protocol-processor` `631eeb34`, `gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`, `external` `efeb541a`) — no RTL, merge or image artifact changed since R432-4, so R432-4's RTL coverage is unaffected.

[R432] PASS Robustness — `restart_controls_probe.log` ("46 anchors, 0 not found exactly once") and the unchanged head — the corrected figure agrees with the anchor guard's receipt. No robustness artifact changed since R432-4.

[R432] PASS Tests — `tb/verilator/milan_dp/gsi_mutants.py:99-131` vs body line 195 — the campaign's own table plants 12 gsi edits (11 `pp`, 1 `dp`), which equals the corrected figure. No test changed since R432-4.

[R432] PASS Docs — PR #634 live body (`live-PR-BODY.md`) vs `author-r4b/PR-BODY.md` and vs the body version R432-4 reviewed — R432-4-F1 is corrected and the row's breakdown sums to the stated 45. The only other difference is R432-5-S1, a trailing newline with no rendered effect (SUGGESTION, which does not affect coverage).

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Full: restart request `milan_datapath.sv:3205-3232` vs #602 / IEEE 1722-2016 4.4.4.3/10.4.3, CLKSRC at `631eeb34`, #629 acceptance mutants (R432-4). Delta: body line 195, no clause claim changed (R432-5). | R432-4, re-confirmed R432-5 | `2bc5adc0bfd981e63e82ada5e673ce69cab4f4ee` |
| RTL | CLEAN | Full: merge recomposition, `KL_pp_shadow.sv:1094-1140`, image receipts, lint/source-list/port-contract gates (R432-4). Delta: none in scope, tree `0a3979f4` (R432-5). | R432-4, re-confirmed R432-5 | `2bc5adc0bfd981e63e82ada5e673ce69cab4f4ee` |
| Robustness | CLEAN | Full: anchor guard, 128-row request truth table, veto probes (R432-4). Delta: receipt `restart_controls_probe.log` vs corrected figure (R432-5). | R432-4, re-confirmed R432-5 | `2bc5adc0bfd981e63e82ada5e673ce69cab4f4ee` |
| Tests | CLEAN | Full: `gmstep_mutants.py` `--all` 22/22, `milan_dp` 11,839/0, render-CSR 4/0 (R432-4). Delta: `gsi_mutants.py:99-131` vs corrected figure (R432-5). | R432-4, re-confirmed R432-5 | `2bc5adc0bfd981e63e82ada5e673ce69cab4f4ee` |
| Docs | CLEAN | Live PR body vs author `author-r4b/PR-BODY.md` and vs body as reviewed at R432-4; receipt per-campaign rows; correction comment 5967252070. CHANGELOG/design/docs gates per R432-4, tree unchanged. | R432-5 | `2bc5adc0bfd981e63e82ada5e673ce69cab4f4ee` |

All five lenses are clean at the exact head. R432-4 banked the four non-Docs lenses at this same commit, and nothing in their scope has changed since.

## Real limits

- **Scope:** this round checks the body only. It ran no build, suite, campaign or gate, and did not re-review code, tests, merge or image. Those rest on R432-4 at the same head, together with its stated limits (make 4.4.1 locally, no Vivado run, shards 0 to 3, Yosys, builder and native banks not re-run by the reviewer).
- **Body provenance:** "the body R432-4 reviewed" is the PR's public edit-history entry of 2026-10-03T07:53:19Z. That is the last edit before R432-4 started (07:54:09Z), and it is byte-identical to the author file.
- **Hosted contexts:** a snapshot at this head, taken 2026-10-03T08:40Z (`hosted_checks_snapshot.tsv`): 17 succeeded, 1 skipped, and Verilator shards 1/5 and 2/5 were still in progress. The `verilator-suites` and `yosys-portability` aggregates were not yet emitted. A skipped context is not an executed job.
- **Hardware:** physical calibration NOT RUN. There is no hardware or bench evidence, and skipped field tests are not hardware proof.
- **Stale comment:** REVIEW READY comment 5966931872 still carries "gsi (11)". Under the assignment rule it is not edited, and the body plus correction comment 5967252070 carry the correct figure.

## Pending manager duties

- Accept the exact-head hosted `verilator-suites` and `yosys-portability` contexts once emitted (shards 1/5 and 2/5 were still in progress at 08:40Z), and the `act` run.
- At the merge turn, build the final current-dev candidate on live `dev` `1269cdaf` and run the builder and native banks. Source validation at this head is separate from that candidate.
- Optionally file Issues for R432-4-S1 and R432-3-S1 = R433-3-S1. R432-5-S1 needs no action.
- Clone integrity after this round: worktree and index equal `2bc5adc0` / `0a3979f4`, and the gitlinks are at their recorded commits (`head_integrity.log`). This round planted no probe.

R432-5 FINISHED
