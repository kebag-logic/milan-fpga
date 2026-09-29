[R404] NEGATIVE - exact head 5c57927413e0dae279f06a75d2a58e3fec8a2bb0

Round R404-4 is a cleared-context internal delta review of PR #622 (bench lane B2, issue #606). It covers `fb4a1b89..5c579274`, one docs commit by [A449], under the round-4 assignment (issue 606 comment 5889146437), which answers F6 of R404-3 and R405-3.

- Exact head: `5c57927413e0dae279f06a75d2a58e3fec8a2bb0`, tree `5613d2b3b7b0f0b8b8d710216647631401bf1265`.
- Evidence: `b2-review-evidence` at `d677a15a`. The `author/` tree is `fdde402a`, unchanged since `666d8897`.

## Verdict summary

- **F6 is resolved on the page.**
  - `docs/findings/606_FIRST_BIND_MEASUREMENT.md:277` now reads "No state-changing command addressed a DUT stream input: the 210 `CONNECT_RX` and `DISCONNECT_RX` went to the reference peer, and every AECP command was a GET_ or READ_."
  - `:279` names the reads as reads, which write no record: 228 GET_RX_STATE, 228 GET_COUNTERS and 4 READ_DESCRIPTOR.
  - Every number re-derives exactly from the archive.
- **F6 is resolved in the quoted PR-body clause.** The Round 2 F2 bullet now says "no state-changing command addressed one", followed by the same two sentences as the page.
- **The tables are byte-identical.** All 21 tables on both pages are unchanged, the PR body's 17 table lines are unchanged, and no changed line starts with `|`.
- **The gates pass.** All pinned Markdown gates and repository docs gates return rc 0.
- **Nothing else changed.** The commit changes one file (+3/−1). The commit message is one line with no trailers, and the gitlinks are unchanged.
- **F7 is new, and the verdict is NEGATIVE.** The same F2 bullet opens its derivation with "210 ACMP commands all to the peer's input". The archive holds 809 distinct ACMP commands, and 232 of them went to the DUT.
  - Two sentences later, the bullet itself names 228 GET_RX_STATE to the DUT's stream inputs. GET_RX_STATE is an ACMP command, so the bullet contradicts itself.
  - This is the same defect class as F6: "command" is used where the census supports only "state-changing command".
  - The phrase has stood since the round-2 body, and I passed over it in R404-2 and R404-3. That was my own omission, and I am disclosing it here.
  - The page is correct. The fix is a PR-body edit only, and it needs no commit.

## Authorities, in the order read

- AGENTS.md sections 3 and 5 to 8.
- CONTRIBUTING.md `:402`: commits are one line, with no trailers.
- `docs/README.md` and `docs/findings/README.md` (`:12` indexes the #606 page).
- The round-4 assignment 5889146437, and my R404-3 F6 (5889116666) with its required outcome.
- `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 11, the `0x20 to 0x2F` row (`:1285`): the binding records' only writer is `KL_acmp_nvm_shadow` through `KL_pp_nvm_port`, driven by the per-sink dirty for binding, parameters and started state.
- `docs/design/SAVED_STATE_FASTCONNECT.md` section 4.2 (`:275`): records `0x20`..`0x2F` are indexed by sink.
- Next, the diff `13eda870..5c579274` and `fb4a1b89..5c579274`, and the history (4 commits).
- Then the live PR body, read at 11:30:03Z (`receipts/pr_body_at_read_r4.md`), and the evidence archive.
- Prior public review findings were read only after this verdict's findings and ledger were drafted.

## Assigned checks

1. **The census on the page: pass** (`receipts/census_sentence_r4.txt`, `receipts/poll_census_r4.txt`, `receipts/saved_state_r4_rerun.txt`).
   - **The archive counts, with the 112 byte-copy `snapshot.jsonl` files excluded:**
     - State-changing ACMP: `{(mt 6, listener_uid 8): 105, (mt 8, listener_uid 8): 105}`, that is 210, all to the peer's Stream Input 8.
     - The AECP names are GET_AVB_INFO, GET_CLOCK_SOURCE, GET_CONFIGURATION, GET_COUNTERS, GET_SAMPLING_RATE and READ_DESCRIPTOR, all GET_ or READ_.
     - Commands addressed to a DUT STREAM_INPUT (type 5): GET_RX_STATE 228, GET_COUNTERS 228, READ_DESCRIPTOR 4, total 460. 0 of them are state-changing.
   - **The page against those counts:**
     - `:277` and `:279` state exactly those facts.
     - "(the polls above)" is exact: the 228 are the 226 Stream Input 1 polls at `:267` plus the 2 Stream Input 0 polls at `:268`.
     - "which write no record" agrees with section 11: a read changes no binding, parameter or started state.
     - The conclusion at `:283` is unchanged and still rests on the census plus commits 2 / 0 and slots 229 / 230 (`:281`).
   - **Reproducibility:** `poll_census_r4.txt` and `saved_state_r4_rerun.txt` reproduce my round-3 receipts byte for byte, apart from the header line.
2. **The PR body's Round 2 F2 bullet: F6's clause passes, the derivation phrase fails (F7).**
   - The F6 clause is replaced. The bullet now carries the page's two sentences verbatim, and every number checks (`census_sentence_r4.txt`: 5 of 6 body checks OK).
   - The remaining FAIL is F7.
   - The Round 4 section is accurate: "the 460 reads" = 228 + 228 + 4, and "every table is byte-identical to round 3" matches `tables_r4.txt`.
3. **Tables: pass** (`receipts/tables_r4.txt`, unmodified `tables_r2.py`).
   - `fb4a1b89` to `5c579274`, and `d7676373` to `5c579274`:
     - #606 page, 10 of 10 tables IDENTICAL;
     - #608 page, 11 of 11 IDENTICAL;
     - 0 table lines lost.
   - The PR body's per-bind table is identical to the page's.
   - The body's 17 table lines are identical between the round-3 and round-4 bodies.
   - 0 changed lines start with `|`.
4. **Gates: pass, all rc 0** (`receipts/gates/summary.txt`). The pinned environment is cmarkgfm 2025.10.22, cffi 2.1.1, pycparser 3.0, html5lib 1.1, six 1.17.0 and webencodings 0.6.1, installed with `--require-hashes` from `tools/markdown/requirements.txt` (`receipts/gates/env.txt`).
   - `docs_check.py`: 0 findings across 176 md and 938 scrubbed files.
   - `check_doc_style.py`.
   - `gen_toc.py --check`.
   - `check_em_dash.py`: 0 findings over 914 lines from `13eda870`, and 0 over 3 lines from `fb4a1b89`; arms 339/339.
   - `check_doc_paths.py`: 854 paths.
   - `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `check_feature_status.py --self-test`.
   - `git diff --check`, from the base and from round 3.
   - The worktree stayed clean.
5. **Nothing else changed: pass** (`receipts/clone_integrity_r4.txt`).
   - `git diff --raw fb4a1b89 5c579274`: one entry, `M docs/findings/606_FIRST_BIND_MEASUREMENT.md`, 100644 to 100644, blob `a6b23e26` to `19dadb8b`, +3/−1. The diff is the `:277` rewrite and the new `:278-279`.
   - Over the whole PR, `13eda870..HEAD` still touches the two pages and `docs/findings/README.md`.
   - The four gitlinks are identical to `13eda870`: `external efeb541a`, `gptp-processor 5dce647a`, `protocol-processor c951a9ff`, `third_party/verilog-axis 48ff7a7e`.
   - The PR body changed only in the F2 bullet and the added Round 4 section.

## Findings

### F7 MINOR: the PR body's F2 bullet says the lane's 210 ACMP commands all went to the peer's input

- **ID:** F7. The numbering continues from R404-3 / R405-3 F6.
- **Severity:** MINOR.
- **Lenses:** Conformance, Docs.
- **Where:** PR #622 body, Round 2 F2 bullet (`receipts/pr_body_at_read_r4.md:78`): "The #606 page gives the derivation: 226 console samples, 210 ACMP commands all to the peer's input, and no AECP write."
- **Authority/evidence:**
  - The round-4 assignment asks that the PR body's Round 2 F2 bullet "state the census as recorded". F6's required outcome made the same demand of the page and the PR body.
  - AGENTS section 6, `Docs`: the PR must give a cold reviewer accurate evidence.
  - `receipts/acmp_census_r4.txt`: the transcripts carry 809 distinct ACMP commands.
    - 210 were `CONNECT_RX` and `DISCONNECT_RX`, all to the peer's Stream Input 8.
    - 232 were addressed to the DUT: 226 + 2 GET_RX_STATE to its Stream Inputs 1 and 0, and 2 + 2 GET_TX_STATE to its Stream Outputs 0 and 1.
    - Every state record carries an ACMPDU-shaped response.
  - The page states the census correctly at `:264-265`: "The lane's only state-changing commands were 105 `CONNECT_RX` and 105 `DISCONNECT_RX`. All went to the reference peer's Stream Input 8".
  - Two sentences after the phrase, the bullet names "228 GET_RX_STATE" among "the commands that did address the DUT's stream inputs".
  - `receipts/census_sentence_r4.txt` fails this one claim. When only this phrase is qualified, `receipts/mutate_r4.txt` C1 passes.
- **Impact:**
  - The bullet summarising the saved-state derivation misstates its ACMP census, and it contradicts its own later sentence.
  - It is the same loose "command" for "state-changing command" that F6 was raised against, left in the bullet that F6's fix edited.
  - No number, table, verdict or conclusion changes. The page itself is correct.
- **Required outcome:** The bullet states the ACMP census as recorded. For example: "210 state-changing ACMP commands (105 `CONNECT_RX`, 105 `DISCONNECT_RX`), all to the peer's input". Dropping the phrase, and relying on the census sentences that follow, also satisfies this. This is a PR-body edit. No commit is needed, and the page stays as it is.
- **Verification:** `scripts/census_sentence_r4.py` returns rc 0 against the edited body, and the body's table lines stay identical (`tables_r2.py`).

### Suggestions (non-blocking, no lens effect)

- **R404-3 S4 and R405-3 S1 (Docs), still applicable, not in the round-4 assignment.** `606…:255` names `author-r2/scripts/saved_state_b2.py` as the derivation. That script prints 338 + 2 including the copies, while the page states 226 + 2. `:269` explains the difference. This could ride with the F7 body edit only if the maintainer wants a page commit. It does not affect coverage.
- **R405-2 S4 / R405-3 S2 (Docs)** is untouched and still applicable. R405 owns it.

## Prior public findings on this PR

Read after the independent pass above.

| Finding | State at `5c579274` |
|---|---|
| R404-3 F6 MINOR (Conformance, Docs): "no command addressed a DUT stream input" | **Resolved.** The page `:277`/`:279` and the body's clause state the census as recorded (checks 1 and 2). Its residual sibling phrase in the same bullet is filed as F7. |
| R405-3 F6 MINOR (Conformance, Docs): the same, "460 read commands did" | **Resolved** on the same evidence. Its first alternative outcome is met: the premise says "state-changing" and the reads are named. R405 owns its final disposition. |
| R404-2 F5, R405-2 F5 MINOR | Resolved at `fb4a1b89` (R404-3, R405-3). The delta does not touch `:267-269`, so they remain resolved. |
| R404-1 F1-F4, R405-1 F1-F4 MINOR | Resolved at `d7676373`. They are untouched by this delta. |
| R404-3 S4, R405-3 S1, R405-3 S2 | Not taken. Out of the round-4 scope. Still optional. |
| R405-2 F4 residual: pre-redaction commits `2c9f3df2`, `51bfa948` served by SHA | GitHub-side removal. The manager owns it. It is not a head finding. |

## Per-lens results

- `[R404] UNCLEAN Conformance - PR #622 body :78 (receipts/pr_body_at_read_r4.md), receipts/acmp_census_r4.txt - F7`: the page's census (`606…:277-279`) conforms to the assignment and to F6's required outcome. Assignment items 1, 3, 4 and 5 conform. F7 is the one departure, in the body bullet the assignment names.
- `[R404] PASS RTL - git diff --raw fb4a1b89..5c579274 and 13eda870..5c579274 (receipts/clone_integrity_r4.txt); SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1285 section 11 row 0x20-0x2F; SAVED_STATE_FASTCONNECT.md:275 - no HDL, constraint, script or gitlink is in the PR (one docs page, mode 100644 unchanged, four gitlinks identical to 13eda870); the new claim that the reads "write no record" matches the authority: the only binding-record writer is KL_acmp_nvm_shadow through KL_pp_nvm_port, on a per-sink binding, parameter or started-state change, and records are indexed by sink.`
- `[R404] PASS Robustness - receipts/census_sentence_r4.txt, receipts/acmp_census_r4.txt, receipts/poll_census_r4.txt - checked the census at its edges: no state-changing transaction names any listener other than uid 8; no AECP name outside GET_/READ_; the DUT-stream-input set contains exactly GET_RX_STATE, GET_COUNTERS and READ_DESCRIPTOR and nothing else; the 4 DUT GET_TX_STATE records address stream outputs, not inputs, and are correctly excluded from the 460; 112 of 112 snapshot.jsonl copies are excluded; 0 of 228 polls read non-zero status or connection count; the author/ tree is unchanged since 666d8897.`
- `[R404] PASS Tests - receipts/mutate_r4.txt - this PR adds no executable test; the round's evidence chain was proved able to fail on scratch copies: M1 page reverted to the round-3 F6 sentence, M2 GET_COUNTERS 228 to 226, M3 reads sentence removed, M4 210 to 200, M5 one CONNECT_RX to a DUT stream input added to the archive, M6 one SET_STREAM_FORMAT to a DUT stream input, M7 one per-bind table cell changed (tables_r2.py reports CHANGED and the body table no longer matches): 7 of 7 killed; C0, the unmodified control, fails only on F7; and C1, the body with F7's phrase qualified, passes.`
- `[R404] UNCLEAN Docs - PR #622 body :78 - F7`: both changed page lines were read at the head in context (`606…:255-290`), and the live PR body was read in full. The page's delta, the body's F6 clause and the body's Round 4 section are accurate against the archive. The gates are rc 0.

## Ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F7 open) | `606…:255-290`; PR body `:78`, `:91-93`; assignment 5889146437; `author/` transcripts at `d677a15a` | R404-4 | `5c57927413e0dae279f06a75d2a58e3fec8a2bb0` |
| RTL | CLEAN | `git diff --raw` (base and round 3), four gitlinks, `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1285`, `SAVED_STATE_FASTCONNECT.md:275` | R404-4 | `5c57927413e0dae279f06a75d2a58e3fec8a2bb0` |
| Robustness | CLEAN | `receipts/census_sentence_r4.txt`, `acmp_census_r4.txt`, `poll_census_r4.txt`, `saved_state_r4_rerun.txt` | R404-4 | `5c57927413e0dae279f06a75d2a58e3fec8a2bb0` |
| Tests | CLEAN | `receipts/mutate_r4.txt`, `tables_r4.txt`, `gates/summary.txt` | R404-4 | `5c57927413e0dae279f06a75d2a58e3fec8a2bb0` |
| Docs | UNCLEAN (F7 open) | `606…` delta in context, `docs/findings/README.md`, the full live PR body, gates | R404-4 | `5c57927413e0dae279f06a75d2a58e3fec8a2bb0` |

F7 lives in the PR body, not in the tree. If it is fixed by a body edit alone, the head does not move. In that case:

- RTL, Robustness and Tests stay banked at `5c579274`.
- The page's share of Conformance and Docs is already clean at `5c579274`.
- Only a re-read of the edited body, against `census_sentence_r4.py`, is needed to clear Conformance and Docs.
- Any new commit re-opens the lenses whose scope it touches.

## Real limits

- **Delta review only.** I re-derived the round-4 census claims and checked identity for every table. I did not recompute the round-2-covered measurement values inside those tables.
- **Banks not run.** I ran no builder, parent, processor, gPTP or Yosys bank, no act, and no hardware. The pinned Verilator was not used, because no RTL is in scope.
- **No hardware proof.** Physical calibration was NOT RUN. Field skips are not hardware proof.
- **Redacted archive.** The archived transcripts are the redacted copies. Command names, destinations, descriptor types and counts are not affected by the redaction.
- **Command identification.** ACMP GET_RX_STATE / GET_TX_STATE are identified by the `state-<type>-<index>` label and the ACMPDU-shaped response, as in the page, the author's receipts and R405-3's reading of the controller source. I did not re-read the standard's text.
- **Hosted evidence.** At 11:34Z the exact head had no check runs, no commit statuses and no workflow runs (`receipts/hosted_checks_r4.txt`), so no hosted evidence was judged.
- **Clone untouched.** No tracked file in the review clone was modified. The gate run left an ignored `scripts/__pycache__/`, which I removed. At the end: HEAD `5c579274`, tree `5613d2b3`, 0 status lines including ignored files, index modes and blobs equal to `HEAD` for 966 entries, gitlinks unchanged. The probes used scratch copies, since removed. The evidence-branch clone and the gate environment stay in the unpublished scratch area.

## Pending manager duties

- **F7:** edit the PR body's Round 2 F2 bullet, then request re-verification.
- **Hosted and act acceptance** at the final head. None exists at `5c579274`.
- **Candidate merge** against live dev `79c36963`, which R405-3 reported conflicts in `docs/findings/README.md`. It must be built and validated at the merge turn.
- **Pre-redaction commits** `2c9f3df2` and `51bfa948` need GitHub-side removal.

R404-4 FINISHED
