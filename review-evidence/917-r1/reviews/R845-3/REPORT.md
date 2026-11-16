[R845] POSITIVE - exact head 394612c55148b43354359daeab2aa88d4f019ec2

Round R845-3. Internal cleared-context review of PR #918 (issue #917). This round reviews the delta `8f73ade5..394612c5`: two commits, `93163957` and `394612c5`. They answer R845-2 (NEGATIVE: F1 MINOR, R1, R2, S1-S3) and R846-2 (NEGATIVE: F1 MINOR, R1).

- Tree: `e10ca2a5920b466be5561dcbe323fb942043497f`.
- Source base: `cec88385`.
- The merge candidate against live dev `6b66f66d` is the manager's job and is not claimed here.

## Verdict in brief

- **R845-2 F1 is resolved.** FR_NFR 3.4.1's margin table is now written between markers by `sw/mailbox/mailbox_margins.py`, from each row's channel's `refill_ms`. `gen_mailbox.py --check` names each row that differs.
  - My own rerun of probe P1 (`refill_ms` 5 -> 10) fails `--check` on all three AECP rows.
  - After `--write` those rows read 11 ms and 208/218/208 ms, and ACMP's row does not change.
- **R846-2 F1 is resolved.** `held.py` now has two ordering guards:
  - `overtaken`: a commit on a channel that is holding a record is refused.
  - `follows_hold`: a held record's commit stamped at or before its hold is refused.
  - Both review histories are standing negative controls. Removing either guard fails its named self-test.
  - The reviewer's `probe_attribution.py` gives byte-identical output at this head on my run and in the author's receipt.
- **All residue and suggestions are resolved or taken:** R1 (both reviews), R2 (exact text), S1 and S3. S2 is retained (it is a publication issue).
- **No RTL, firmware, configs, YAML or generated contract output changed.** The git trees are identical.
- **New items this round:** four SUGGESTIONs and three RESIDUE items. None of them is MINOR or worse, so every lens is clean.

## Scope reconstructed

- **Issue #917** (frozen): a command arriving with no token is held and delivered at the next refill. Only a command behind a held one may be dropped, and it is counted. The table figures stay (burst 16, refill 5 ms). No firmware image change.
  - Acceptance: 50 back-to-back AECP reads with none lost; a third command behind a held one is dropped and counted; three hardware descriptor walks; load, rows and timing unchanged.
- **The round-2 ruling** behind R845-2 F1: the held allowance is "stated once and generated from mailbox.yaml's refill_ms".
- **This delta's artifacts:**
  - `sw/mailbox/mailbox_margins.py` (new) and `sw/mailbox/gen_mailbox.py`
  - `docs/reference/FR_NFR.md` 3.4.1
  - `scripts/ci_scope.py`
  - `docs/testing/CI_WORKFLOWS.md` and `docs/design/MAILBOX_SPLIT.md`
  - `tb/verilator/ctrl_service_budget/{held.py, grade.py, selftest_held.py, selftest_mutants.py, README.md}`
  - one comment in `tb/verilator/mbx/suite.hpp`
- **Known and not a finding of this PR:** no hosted CI job runs `gen_mailbox.py --check`. This is pre-existing, `CI_WORKFLOWS.md:211` says so, and it belongs to a separate issue.

## Findings (all new at this head; none is MINOR or worse)

### S1 - SUGGESTION - Tests - `tb/verilator/ctrl_service_budget/held.py:52`, `selftest_held.py:80`: the equality boundary of `follows_hold` is not pinned

- **Evidence:** the guard refuses `cycle <= held_at`, and the README and docstring state "at or before its hold". The standing control stamps the commit at 1060, before the hold at 1070. It never stamps it in the hold's own clock.
  - Probe P2 (`receipts/probes.log`) changes the guard to `cycle < held_at`. An `RXR` in the hold's clock (1070) is then graded, and all 13 held checks still pass. So the boundary mutant escapes.
  - At the reviewed head the same history is refused: "does not follow its hold at 1070" (P2b).
- **Why only a suggestion:**
  - The head's behaviour is correct.
  - The RTL cannot produce this history: `KL_mbx_rx.sv:745` `rel_w[c] = refill_w[c] && held_r[c]` uses the registered `held_r`, and a refill in the header clock gives a token rather than a hold (`:613`).
  - R846-2 F1's required outcome, that removing either guard fails a named test, is met.
- **Suggested outcome:** add a control where the commit is stamped in its hold's clock, so `<` instead of `<=` fails by name.

### S2 - SUGGESTION - Tests - `sw/mailbox/mailbox_margins.py:104`, `gen_mailbox.py:505`: a margin of exactly 0 ms is not pinned

- **Evidence:** FR_NFR requires `T_ingress + T_svc + T_egress + T_network < timeout`, so a 0 ms margin must fail. The code does refuse it (`<= 0`); P3 plants a 27 ms ACMP timeout and gets "leaves no margin: 0 ms".
  - But the self-test arm plants -2 ms. With `< 0` mutated in, `--selftest` still exits 0 (P3).
- **Suggested outcome:** plant a zero margin in the arm, or add a second arm for it.

### S3 - SUGGESTION - Robustness - `sw/mailbox/mailbox_margins.py:86`, `:98`: nothing pins the table's header columns or its set of rows

- **Evidence:** written cells are placed by column position, and the header's labels are not compared with those positions.
  - Deleting a deadline row leaves `--check` clean.
  - `--write` writes a table that has a non-positive margin and exits 0. A later `--check` would fail on it.
- **Why only a suggestion:** R845-2 F1 asked that the written cells follow `refill_ms`, and they do. The stated rows are hand-written by design (`FR_NFR.md:428`).
- **Suggested outcome:** check the header row literally, and have `--write` report a non-positive margin.

### S4 - SUGGESTION - Docs (evidence packet) - `review-evidence/917-r1/author-r3/INDEX.md` at archive `887dbc64` (retains R845-2 S2)

- **Evidence:** 223 of 227 rows match their files (`receipts/packet_index_verify.txt`). The 4 that do not are the same 4 workflow logs as in round 2:
  - `docs__docs-gates-1__gate_25_0.log`
  - `docs__docs-gates-2__gate_25_1.log`
  - `elaborate__elaborate-gates-0__gate_15_0.log`
  - `elaborate__elaborate-gates-1__gate_15_1.log`
- Each published copy is 8 bytes shorter than its INDEX row. That fits a sanitizing pass made by publication after the author indexed the packet.
- The archive commit carries no signature (`%G?` = N). The INDEX is the packet's only attestation besides git.
- None of the four logs supports a delta claim this review relies on.
- **Suggested outcome (publication):** regenerate INDEX.md after the last rewrite at publication, or sign the archive. See also residue X3.

### X1 - RESIDUE - Docs - `docs/reference/FR_NFR.md:429`

- **Problem:** the line says the generator "writes the other six columns from `mailbox.yaml`". The token `T_ingress` (1 ms), and the 1 ms in the held allowance, come from the generator's `T_INGRESS_MS` (`mailbox_emit.py:218`), not from `mailbox.yaml`.
- **Exact fix:** replace "writes the other six columns from [`mailbox.yaml`](../../sw/mailbox/mailbox.yaml):" with "writes the other six columns from [`mailbox.yaml`](../../sw/mailbox/mailbox.yaml) and the contract's 1 ms `T_ingress`:".

### X2 - RESIDUE - Docs - PR #918 body, Status, line 20

- **Problem:** the stale line "Author packets: [...author-r1 and author-r2](.../tree/24755cf4/...) ...; round 3's receipts join them as `author-r3` when published." still stands above its replacement at line 22.
- **Exact fix:** delete line 20 and keep line 22 ("Author packets: [...author-r1 to author-r3](.../tree/887dbc64/...)").

### X3 - RESIDUE - Docs - PR #918 body, Round 3 table, the R845-2 S2 row

- **Problem:** the row says "Round 3's INDEX is generated last, after the last sanitizing pass". The published packet contradicts this for four files (S4).
- **Exact fix:** replace that sentence with "Round 3's INDEX matched its 227 files as handed over; in the published copy four workflow logs are again 8 bytes shorter than their rows, a rewrite at publication after indexing".

### Not a finding

`scripts/ci_scope.py:65` re-flows a pre-existing comment that carries "#665 F0". This is an existing instance carried onto a re-wrapped line, not a new one, and #746 tracks it. No other comment line added in this delta carries a bench label, lane name, round, reviewer ID or comment ID. I scanned every added line.

## Prior public findings, resolved or retained at this head

| Prior finding | Status at 394612c5 | Evidence |
|---|---|---|
| R845-2 F1 MINOR (Conformance, Docs, Tests): FR_NFR held allowance and margins are an unchecked copy | **Resolved** | <ul><li>The table sits between markers (`FR_NFR.md:432-439`). A Channel column was added; all figures are unchanged from 8f73ade5.</li><li>`mailbox_margins.py:54-68` computes the six written cells from the row's channel's `refill_ms` and `T_INGRESS_MS`.</li><li>`findings()` (`:88-105`) names the row whose cells differ, and each non-positive margin.</li><li>`check_drift` runs it (`gen_mailbox.py:180`); `write_all` splices it (`:183-199`).</li><li>The `:425` sentence is replaced by `:425-430`, which describes this mechanism (except X1's wording).</li><li>My run at the head: `--check`, `--crosscheck` and `--selftest` all rc 0; the 5 margin arms are ok.</li><li>My P1: `--check` rc 1 names all three AECP rows ("the contract gives 1 ms / 218 ms / 228 ms / 11 ms / 208 ms / 218 ms"). `--write` gives 11 ms and 208 / 218 / 208 ms (218 / 228 / 218 at the proposal), ACMP unchanged, and the recheck is rc 0.</li><li>`ci_scope.py` lists FR_NFR.md in `GATE_READ_DOCS` (`:75`) with a case at `:295`. Its self-test passes and includes "gate-read page docs/reference/FR_NFR.md (named at sw/mailbox/mailbox_margins.py:26) is relevant" and the mutation arm.</li><li>`CI_WORKFLOWS.md:207-211` and `MAILBOX_SPLIT.md:305-307` updated.</li></ul> |
| R846-2 F1 MINOR (Tests, Robustness): commit-order validation incomplete | **Resolved** | <ul><li>`held.overtaken` (`held.py:42-47`) runs on every `RXC` through `held.commit` (`:57-61`, `grade.py:196`).</li><li>`held.follows_hold` (`:50-54`) runs on every `RXR` in `release` (`:71`).</li><li>Standing controls (`selftest_held.py:72-94`): both review histories are refused by name. Another channel's commit between the hold and its commit is credited to its own frame, and so is one in the clock of the held commit; the held record stays measured, start 1059.</li><li>`selftest_mutants.py:449-452` removes each guard. My budget self-test run: all checks PASS; the two guard mutants are caught by the named checks; 216 mutants caught, 0 escaped, rc 0.</li><li>The reviewer's `probe_attribution.py`, unmodified, against my clone: output identical to the author's receipt, refusing "overtakes the record it holds" and "does not follow its hold at 1070". The valid held-and-follower and other-channel cases stay measured.</li><li>The equality boundary is a suggestion only (S1).</li></ul> |
| R845-2 R1 / R846-2 R1 RESIDUE: bench labels in a `suite.hpp` comment | **Resolved** | `suite.hpp:1648-1650` reads as both reviews' exact fix. The check-name strings are untouched. |
| R845-2 R2 RESIDUE: the PR population bullet's reason | **Resolved** | PR body Known limitations (line 168) carries the exact replacement text. |
| R845-2 S1 SUGGESTION: `aecp-held` at two-interface 8x8 | **Taken** | <ul><li>Author receipt `held-8x8/run.log`: point `8x8`, image built with `--interfaces 2 --ledgered-point 8x8-two-interfaces`, `run.py` `POINTS['8x8'] = (…_8x8, 2)`.</li><li>Row 5.310 ms against a 20 ms budget, fits; ingress 4.986 ms against a 6.0 ms allowance.</li><li>One RXH and one RXR. The two followers are refused. The old-rule negative control is refused.</li></ul> |
| R845-2 S2 SUGGESTION: stale author INDEX | **Retained** as S4 (publication) | `receipts/packet_index_verify.txt` |
| R845-2 S3 SUGGESTION: the held row already contains its ingress | **Taken** | `FR_NFR.md:444` and `ctrl_service_budget/README.md:396`. Both are accurate: the held path starts at `rxh:<channel>`, so its figure includes the delay that the held margins subtract again. |

## Per-lens results (artifacts at 394612c5)

- `[R845] PASS Conformance — docs/reference/FR_NFR.md:425-444, sw/mailbox/mailbox_margins.py:54-105, receipts/probes.log P1 — margin table vs. FR_NFR's inequality and the round-2 ruling`
  - Every written cell equals timeout - bound - `T_egress` - `T_ingress` for its row's channel, at the bound and at the 10 ms proposal, for a token and for a held record (`refill_ms` + 1 ms).
  - The published figures are unchanged: ACMP 6 ms held, 173/183; AECP 213/223, 223/233, 213/223.
  - The allowance is now stated once and generated, which the ruling requires. A rate change moves the rows or fails the check (P1).
  - #917's acceptance is unaffected: no RTL, firmware or contract change (`receipts/trees_reviewer.txt`), and 46 fixture images plus both split images are identical by hash (author `images/*`, firmware ELF hashes match the base record).
- `[R845] PASS RTL — receipts/trees_reviewer.txt (hdl tree 363860ab… at 8f73ade5 and 394612c5), hdl/milan/mailbox/KL_mbx_rx.sv:613,745 — no RTL-scope artifact changed`
  - The hdl, sw/firmware and configs trees, `mailbox.yaml`, `MAILBOX_CONTRACT.md` and every submodule gitlink are identical. The only `suite.hpp` change is a comment.
  - So R845-2's RTL coverage at 8f73ade5 stands, because nothing in its scope changed.
  - I re-read the hold and release logic only to confirm the grader's new assumption: release in a later clock than the hold, and no same-channel `RXC` while held.
- `[R845] PASS Robustness — tb/verilator/ctrl_service_budget/held.py:42-77, sw/mailbox/mailbox_margins.py:37-86, receipts/probes.log, receipts/probe_attribution_reviewer.log — invalid ordering and malformed table input`
  - These invalid histories are refused: same-channel overtaking, release at or before the hold (including the same clock, P2b), orphan, duplicate, second hold, late release.
  - Other-channel activity between the hold and its commit, or in the commit's clock, is still credited to its own frame.
  - A malformed table is reported as one finding: missing markers, unknown channel, wrong cell count, a non-millisecond cell, or a header with no proposal.
  - S3 is a suggestion.
- `[R845] PASS Tests — receipts/gen_mailbox_selftest.log, receipts/budget_selftest.log (216 mutants caught, 0 escaped), receipts/ci_scope_selftest.log, receipts/probes.log P1-P3 — each new check fails for its claimed defect`
  - The margin arms name a hand edit, an un-regenerated rate, a non-positive margin and an unknown channel, and the regeneration arm checks that only AECP's held cells move.
  - The guard mutants fail their named checks.
  - The `ci_scope` mutation rejects FR_NFR.md filed as docs-only.
  - Author receipts:
    - regrade byte-identical for the recorded held runs (1x1, 8x8-1if), the no-hold control (`results-aecp`) and the 94-group base and head populations (`regrade/regrade.log`, rc 0);
    - mbx mutants 242/242;
    - local gates rc 0;
    - 9 workflow jobs "failed 0".
  - S1 and S2 are suggestions.
- `[R845] PASS Docs — FR_NFR.md:425-444, CI_WORKFLOWS.md:204-211, MAILBOX_SPLIT.md:302-307, ctrl_service_budget/README.md:384-399, gen_mailbox.py:11-25, held.py:1-14, PR #918 body Round 3 and Known limitations, author packet INDEX — changed contracts described where they are authoritative`
  - Each description matches the code.
  - X1-X3 are residue; S4 is a suggestion.

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | FR_NFR.md 3.4.1 `:425-444` (table `:432-439`), mailbox_margins.py, gen_mailbox.py check/write paths, round-2 ruling, #917 acceptance, trees and image receipts, P1 | R845-3 | 394612c55148b43354359daeab2aa88d4f019ec2 |
| RTL | CLEAN | Tree identity for hdl/sw/firmware/configs/YAML/contract and submodule gitlinks (8f73ade5 = 394612c5); KL_mbx_rx.sv `:613`, `:745` re-read for the grader's ordering assumption | R845-2, whose RTL scope is untouched since; confirmed by R845-3 | 8f73ade54366cc832bad3386c8b6f3bbb12ca5e4 (ancestor; RTL scope unchanged to 394612c5) |
| Robustness | CLEAN (S3 suggestion) | held.py `:42-77`, grade.py `:196`, selftest_held.py `:72-94`, mailbox_margins.py `:37-105`, P2/P2b/P3, reviewer probe_attribution rerun | R845-3 | 394612c55148b43354359daeab2aa88d4f019ec2 |
| Tests | CLEAN (S1, S2 suggestions) | gen_mailbox `--selftest` (my run), budget self-test (my run, 216/216), ci_scope `--selftest` (my run), selftest_mutants.py `:449-452`, author regrade, mbx mutants, local and workflow receipts | R845-3 | 394612c55148b43354359daeab2aa88d4f019ec2 |
| Docs | CLEAN (X1-X3 residue, S4 suggestion) | FR_NFR.md, CI_WORKFLOWS.md, MAILBOX_SPLIT.md, ctrl_service_budget README, generator and grader docstrings, suite.hpp comment, PR body, author packet INDEX | R845-3 | 394612c55148b43354359daeab2aa88d4f019ec2 |

## My probes and receipts

| Receipt | What it shows |
|---|---|
| `receipts/gen_mailbox_{check,crosscheck,selftest}.log`, `gen_mailbox_rc.txt` | All three are rc 0 at the head, and the five margin arms are ok. |
| `receipts/ci_scope_selftest.log`, `.rc` | PASS, including the FR_NFR.md cases. |
| `receipts/budget_selftest.log`, `.rc` | 384 PASS checks, 0 FAIL, 216 mutants caught, 0 escaped, rc 0. |
| `receipts/probes.log`, `scripts/probes.sh` | P1: refill 5 -> 10, then check, write and recheck. P2/P2b: the `follows_hold` equality boundary. P3: the zero-margin boundary. All ran in disposable copies. |
| `receipts/probe_attribution_reviewer.log` | R846-2's probe, unmodified, against my clone; identical to the author's receipt. |
| `receipts/packet_index_verify.txt` | Author packet INDEX: 223 of 227 rows match. |
| `receipts/trees_reviewer.txt` | Tree and blob identity 8f73ade5 = 394612c5 outside the delta; submodule gitlinks. |
| `receipts/hosted_checks.txt` | No check runs were returned for this head SHA. |
| `receipts/restore_check.txt` | Exact head restored: index mode/blob/path equals the HEAD tree, porcelain 0 including ignored files, gitlinks as at the head. |

## Real limits

- I did not rerun any CPU-system measurement or the 94-group population. The regrade equality and the 8x8 held run are author receipts. Their large logs are published only by digest, so I could not regrade them independently.
- No mailbox Verilator suite or mutant campaign was rerun. The delta touches only a comment in `suite.hpp`, so the pinned simulator was not needed and its identity was not checked.
- The author packet is unsigned, and 4 of its INDEX rows are stale (S4).
- No hosted check runs exist at this exact head (`receipts/hosted_checks.txt`). The PR's base is `dev-soft-core`. Hosted and replica acceptance belong to the manager.
- Physical calibration was NOT RUN, and field skips are not hardware proof. #917's three hardware descriptor walks have not been done.

## Pending manager duties

- Carry X1-X3 to the residue checklist, and handle S4 at publication (regenerate the INDEX after sanitizing, or sign the archive).
- Collect the other independent review's round-3 verdict.
- Build and validate the current-dev merge candidate against live dev `6b66f66d89cf25d2717687bcc2c3bf617685a99a` (builder and native banks), and own hosted/act acceptance at the merge turn.
- Do the three hardware descriptor walks, or keep #917 open until they are done. Get merge authorization, then run post-merge containment and close the issue.
- The pre-existing gap where no hosted job runs `gen_mailbox.py --check` stays with its own issue.

R845-3 FINISHED
