[R405] NEGATIVE - exact head 5c57927413e0dae279f06a75d2a58e3fec8a2bb0

# R405-4: external delta review of PR #622 (issue #606, with #608 and #75)

- Round R405-4, external independent reviewer, cleared context, under the round-4 assignment (606 comment 5889146437, `receipts/assignment_606_5889146437.txt`).
- Exact head `5c57927413e0dae279f06a75d2a58e3fec8a2bb0`, tree `5613d2b3b7b0f0b8b8d710216647631401bf1265`.
- Delta judged: `fb4a1b89..5c579274`, one docs commit by [A449]. Whole PR: `13eda870..5c579274`.

The page fixes F6 as recorded. Its two new sentences (`606_FIRST_BIND_MEASUREMENT.md:277`, `:279`) re-derive exactly from the archived transcripts:
- no state-changing command addressed a DUT stream input;
- the 210 `CONNECT_RX` and `DISCONNECT_RX` all went to the reference peer's Stream Input 8;
- every AECP command was a GET_ or READ_;
- 460 commands did address one of the DUT's stream inputs, and all were reads: 228 GET_RX_STATE, 228 GET_COUNTERS and 4 READ_DESCRIPTOR.

Every table is byte-identical, every pinned Markdown gate passes, and nothing else in the tree changed. The PR body's new sentences are also correct.

The verdict is NEGATIVE because of one MINOR finding, **F7**, in the PR body only. The same Round 2 F2 bullet that the round was asked to make state the census as recorded still opens with "210 ACMP commands all to the peer's input". The archive holds 809 ACMP commands, and 228 of them are the GET_RX_STATE reads to the DUT's inputs that the same bullet names three sentences later. This text was present at R405-3 and I did not raise it then (see F7). The fix is a PR-body edit and needs no commit.

## Authorities, in the order read

1. `AGENTS.md`, and `CONTRIBUTING.md` for the documentation gates and the pinned Markdown lock (`tools/markdown/requirements.txt`, `--require-hashes`). Also `docs/README.md` at the head.
2. Issue #606: the round-4 assignment (5889146437) and the review start (PR comment 5889353344).
   - The assignment takes F6 of R404-3 and R405-3 as one item, for both the page and the PR body's Round 2 F2 bullet.
   - It requires the census "as recorded", byte-identical tables, and the gates run in the pinned environment. No bench.
3. Interface authorities for the page's conclusion:
   - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1285`, section 11, row `0x20 to 0x2F`: `KL_acmp_nvm_shadow` is the only record writer, driven by the per-sink dirty on binding, parameters and started state.
   - The pinned processor gitlink `c951a9ff`, `hdl/acmp/KL_acmp_nvm_shadow.sv` (`receipts/rtl_writer_gate_r405_4.txt`).
4. `git diff 13eda870..5c579274` and the delta `fb4a1b89..5c579274` (`receipts/delta_fb4a1b89_5c579274.diff`).
5. Public evidence, all on branch `b2-review-evidence`:
   - `review-evidence/b2-r1/author/`. Its tree is `fdde402a` both at `666d8897` and at the live tip `d677a15a` (`receipts/evidence_locations_r405_4.txt`).
   - `author-r4/` and `MANIFEST.json`, read at the live tip.
   - The live PR body at the head (`receipts/pr622_body.md`), and hosted state at the exact head.
   - `reviews/` on that branch was not opened.

My own R405-3 report and receipts were my starting point for F6. I read no other reviewer's findings until the verdict, findings and ledger below were written. The dispositions of prior public findings were added after that. The same-round R404-4 report was not read beyond its first line.

## Independent pass over the round-4 delta

### Scope

- The delta changes one file, `docs/findings/606_FIRST_BIND_MEASUREMENT.md`: blob `a6b23e26` becomes `19dadb8b`, mode 100644.
  - 3 lines are added and 1 removed; no changed line starts with `|`.
  - The replaced sentence is the old `:277`. The new `:277` is the premise, and the new `:279` names the reads (`receipts/delta_fb4a1b89_5c579274.diff`).
- The #608 page and `docs/findings/README.md` keep their round-3 blobs, `c69870c5` and `01b2ecb1` (`receipts/tables_identity_r405_4.txt`).
- The four gitlinks are unchanged: `efeb541a`, `5dce647a`, `c951a9ff` and `48ff7a7e`. The gitlink lists at `13eda870` and at the head hash the same.
- Whole-PR scope is still the two pages plus `docs/findings/README.md`.
- The commit subject is one line, with no trailers.
- **PR body.** The live body equals the archived `author-r4/PR-BODY.md`. Against my round-3 snapshot, it changes only the Round 2 F2 bullet (`:78`) and adds a Round 4 section (`:91-93`) (`receipts/pr_body_diff_r3_r4.txt`).

### Check 1: the census as recorded

I wrote a fresh census over the 561 archived transcripts (`scripts/r405_4_census.py`, `receipts/census_r405_4.txt`). It does not reuse the controller's "what" labels for AECP:
- the command comes from the response's `cmd`;
- the descriptor comes from the response payload;
- the ACMP target comes from the response's listener fields, cross-checked against the paired transaction records.

Integrity and copies:
- All 561 files equal `MANIFEST.json`'s `published_sha256`.
- All 112 `snapshot.jsonl` files are byte copies of `snapshot-after.jsonl` and are left out.
- The 334 controller invocations in `events.jsonl` are 224 snapshots, 5 binds, 5 unbinds and 100 cycles. None is `setup`, `restore`, `aem` or `setclock`, the modes in `author/tools/b2_controller.py` that could send CONNECT_RX to the DUT or SET_CLOCK_SOURCE.

Result, all matching the page:

| Claim | Page | Recorded |
|---|---|---|
| State-changing commands | `:264-265`, `:277` | 105 CONNECT_RX and 105 DISCONNECT_RX, all to the peer's input 8. Every CONNECT_RX names DUT output 1 as talker. The 210 ACMP transaction records pair one to one. |
| AECP commands | `:266`, `:277` | 2,356 in all, including the 2 identity READ_DESCRIPTORs. The only commands seen are GET_AVB_INFO, GET_CLOCK_SOURCE, GET_CONFIGURATION, GET_COUNTERS, GET_SAMPLING_RATE and READ_DESCRIPTOR. |
| Commands to a DUT stream input | `:279` | 460. GET_RX_STATE: 226 to input 1 and 2 to input 0. GET_COUNTERS: 226 to input 1 and 2 to input 0. READ_DESCRIPTOR: 2 to each input. |
| "the polls above" | `:267-268`, `:279` | The 228 GET_RX_STATE are the 226 + 2 polls those lines count. |

**Wire cross-check.** Across the 112 action captures (`acmp.tsv`), no non-read ACMP command frame names a DUT listener. The only state-changing frames are:
- 105 CONNECT_RX and 105 DISCONNECT_RX to the peer's input 8;
- 105 CONNECT_TX from the peer to DUT Stream Output 1. That targets an output, which `:276` already says no record holds.

**Label check.** On all 1,890 labelled GET_COUNTERS and READ_DESCRIPTOR records, the request label names the same descriptor as the response payload (`scripts/r405_4_label_payload.py`, `receipts/label_payload_r405_4.txt`).

**Author's census.** The author's `author-r4/receipts/census_b2r4.txt` reports the same counts.

**Consistency with round 3.** The counts equal my round-3 `command_census_r405_3.txt`. That file keyed commands by label; this round keys them by response.

**Conclusion.** The page's sentences `:277` and `:279` are the census as recorded. The PR body's new sentences at `:78` repeat them word for word and are equally correct.

### Check 2: "reads, which write no record" against the RTL contract

Section 11 of the ownership document makes `KL_acmp_nvm_shadow` the only writer of records `0x20 to 0x2F`. At the pinned `c951a9ff` (`receipts/rtl_writer_gate_r405_4.txt`):
- the shadow captures the listener's record write-back (`protocol_processor_top.sv:2483-2485`);
- it sets a sink's dirty only when the captured image differs from the stored one (`KL_acmp_nvm_shadow.sv:325-327` and `:615-617`).

A read-only GET_RX_STATE can cause a write-back. The comment at `:318-324` records that one once flushed a record (processor issue #92). The equality gate is what makes such a read write nothing.

The page's claim therefore holds at the pinned RTL. The measured commits (2 / 0) and slots (229 / 230), which the page gives next, are the direct evidence that nothing was written.

### Check 3: tables and gates

**Tables.** `scripts/r405_tables.py` is unmodified from rounds 2 and 3. It keys each table by its header (`receipts/tables_identity_r405_4.txt`):
- #606 page: 10 of 10 tables SAME;
- #608 page: 11 of 11 SAME;
- `docs/findings/README.md`: 1 of 1 SAME.

A positional diff of every `|` line agrees:
- #606: 86 = 86 lines, sha prefix `138630b6689bf18d`, which is the round-2 and round-3 value;
- #608: 272 = 272, `5f2f8eec875f2fff`;
- README: 13 = 13.

The PR body's 17 table lines equal my round-3 snapshot.

**Gates.** The pinned environment is a fresh venv installed with `--require-hashes` from `tools/markdown/requirements.txt`: `cmarkgfm==2025.10.22`, `html5lib==1.1`, Python 3.14.7 (`receipts/gates_r405_4.txt`). All rc 0:
- `docs_check.py`: 0 findings, 176 md and 938 scrubbed files;
- `check_doc_style.py`;
- `gen_toc.py --check`;
- `gen_toc.py --verify-anchors`: 249 links;
- `check_em_dash.py --base 13eda870`: 914 added lines;
- `check_em_dash.py --base fb4a1b89`: 3 added lines;
- `check_em_dash.py --selftest`: 339 arms;
- `check_doc_paths.py`: 854 paths;
- `check_feature_status.py`: 0 findings;
- `git diff --check`, both from `13eda870` and from `fb4a1b89`.

`check_baremetal_only.py --check` could not run here, because this host has no YAML library; see limits. The delta touches no YAML or HDL.

### Check 4: nothing else changed

The tree delta is the one-line replacement and the one added sentence (`:277-279`). No table, number, verdict, link or other section changed, and no other file or gitlink changed.

### Fault probes on the census claims

`scripts/r405_4_probes.sh` runs on disposable copies of `author/` under scratch (`receipts/probes_r405_4.txt`). On the control, both checkers pass: my `r405_4_census.py` and the author's `census_b2r4.py`. I seeded five faults:

| Mutant | Fault | My checker | Author's checker |
|---|---|---|---|
| M1 | a CONNECT_RX to DUT input 1 | FAIL | FAIL |
| M2 | one DUT GET_CLOCK_SOURCE renamed SET_CLOCK_SOURCE | FAIL | FAIL |
| M3 | one GET_COUNTERS on DUT input 1 removed | FAIL | FAIL |
| M4 | one DUT READ_DESCRIPTOR response payload retargeted from CLOCK_SOURCE to STREAM_INPUT | FAIL | passes |
| M5 | one DISCONNECT_RX retargeted to DUT input 1 | FAIL | FAIL |

On M4, the author's checker takes the descriptor from the request label, which is what "addressed" means, so M4 is outside its claim. The label check above shows that label and payload agree on every real record. This is not a finding.

## Findings

### F7 MINOR: the Round 2 F2 bullet still says "210 ACMP commands all to the peer's input"

- **ID:** F7 (numbering continues from round 3).
- **Severity:** MINOR.
- **Lenses:** Conformance, Docs.
- **Where:** the live PR #622 body, Round 2 F2 bullet (`receipts/pr622_body.md:78`): "The #606 page gives the derivation: 226 console samples, 210 ACMP commands all to the peer's input, and no AECP write."
- **Authority and evidence:**
  - The round-4 assignment asks this bullet to "state the census as recorded".
  - `receipts/census_r405_4.txt` records 809 ACMP commands:
    - 210 CONNECT_RX and DISCONNECT_RX to the peer's input 8;
    - 587 GET_RX_STATE, of which 228 went to the DUT's inputs 0 and 1, and 359 to the peer;
    - 12 GET_TX_STATE, of which 4 went to DUT outputs and 8 to peer outputs.
  - The author's `author-r4/receipts/census_b2r4.txt` lists the same.
  - GET_RX_STATE is an ACMP command: message type 10, sent at `author/tools/b2_controller.py:32` as `a.acmp(10, ...)`.
  - The same bullet, three sentences later, now says 228 GET_RX_STATE addressed the DUT's stream inputs.
  - The #606 page does not say "210 ACMP commands". It says "The lane's only state-changing commands were 105 `CONNECT_RX` and 105 `DISCONNECT_RX`" (`:264`). So the bullet also attributes its figure to the page wrongly.
  - This is F6's defect, a count stripped of "state-changing", left in the sentence before the one the round corrected.
  - The text has been in the bullet since round 2, and I did not raise it at R405-3. Conformance and Docs were not banked clean at R405-3, so no earlier clean coverage is contradicted.
- **Impact:**
  - A cold reader of the PR body is told that the ACMP traffic was 210 commands, all to the peer. The same bullet then names 228 ACMP reads to the DUT.
  - No page text, table, number on the page or conclusion is affected.
- **Required outcome:** the bullet's derivation clause states the state-changing ACMP count as recorded. For example: "210 state-changing ACMP commands (105 `CONNECT_RX`, 105 `DISCONNECT_RX`), all to the peer's Stream Input 8". Alternatively, drop the clause, since the bullet's later sentences carry the census.
  - This is a PR-body edit only; the tree at `5c579274` needs no change.
- **Verification:** the bullet agrees with `receipts/census_r405_4.txt`. The PR body's table lines stay identical.

### Suggestions (optional, no lens effect)

- **S1 (Docs, carried from R405-3 S1).** `606…:255` still names the round-2 `saved_state_b2.py` as the derivation. No derivation the page cites prints the new `:279` counts.
  - Locating `author-r4/scripts/census_b2r4.py`, which prints and checks all four statements, would let the cited derivation print the page's numbers.
- **S2 (Docs, carried from R405-3 S2).** `608…:32` and `:229` still say processor PR #133 "implements" or "adds" the leavealltimer restart.
  - PR #133 is still open and unmerged, and processor #108 and #134 are open (`receipts/hosted_and_external_r405_4.txt`).

## Prior public findings on this PR

This section was added after the verdict, findings and ledger above were written. It uses R404-3 (PR comment 5889116666, `receipts/r404_3_public_comment.txt`) and my own R405-3.

| Item | Disposition at `5c579274` |
|---|---|
| R404-3 F6 and R405-3 F6, MINOR (Conformance, Docs): "no command addressed a DUT stream input" | **Resolved.** `606…:277` now says "No state-changing command addressed a DUT stream input", and `:279` names the 460 reads. The PR body's "no command addressed one" now reads "no state-changing command addressed one", followed by the same two sentences. All of it re-derives (check 1). The unqualified count earlier in the same bullet is a separate sentence. I file it as F7 rather than retaining F6, whose quoted text is fixed. |
| R404-3 S4 (Docs): name the derivation for the poll count | **Not taken; still applicable.** `606…:255` still names only `author-r2/…/saved_state_b2.py`. This is the same point as my S1. Optional. |
| R405-3 S1, S2 | **Not taken** (outside the round-4 assignment). Carried as S1 and S2. Optional. |
| R404-2 F5, R405-2 F5 (MINOR) | **Remain resolved.** They were resolved at `fb4a1b89` by R404-3 and R405-3. The delta does not touch `606…:267-269`, and the poll counts re-derive again (check 1). |
| R404-2 S3 | Taken at `fb4a1b89`; unchanged. |
| R404-1 F1-F4, R405-1 F1-F4 (MINOR, Conformance, Docs) | Resolved at `d7676373`; the delta touches none of their text. |
| R404-1 S1, S2; R405-1 S1-S3 | Taken at `d7676373`; unchanged. |
| R405-2 S4 (processor PR #133 wording) | Not taken; this is S2. |
| R405-2 F4 residual: pre-redaction commits served by SHA | Still served. `2c9f3df2` and `51bfa948` resolve through the API (`receipts/evidence_locations_r405_4.txt`). This is not a head finding; the removal is GitHub-side and belongs to the manager. |
| R404-4, the same round at this head (PR comment 5889481776, 11:38Z) | Published during this review. I did not read it beyond its first line, `[R404] NEGATIVE`, so this round stays independent. Its findings are for the manager and the next round to reconcile with F7. |

## Lens results

`[R405] UNCLEAN Conformance — PR #622 body :78 (receipts/pr622_body.md) — F7`: the Round 2 F2 bullet's "210 ACMP commands all to the peer's input" is not the census as recorded. The page's `:277` and `:279`, and the bullet's new sentences, meet assignment item F6 (check 1).

`[R405] PASS RTL — receipts/delta_fb4a1b89_5c579274.diff; receipts/rtl_writer_gate_r405_4.txt (SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1285, KL_acmp_nvm_shadow.sv:283,305-306,318-327,612-618 at c951a9ff)`:
- the delta is one Markdown file; there is no HDL, constraint, script or gitlink change, and the four gitlinks are identical;
- the new claim "reads, which write no record" matches the only-writer contract and the shadow's equality gate on the listener's write-back.

`[R405] PASS Robustness — receipts/census_r405_4.txt, receipts/probes_r405_4.txt, receipts/label_payload_r405_4.txt`: the census's edge cases hold.
- Excluding copies (112 of 112 byte copies) and including identity reads leave the counts unchanged.
- Inputs 0 and 1 are counted separately.
- No non-read ACMP command frame names a DUT listener on the wire.
- No controller mode that could write ran.
- Each of five seeded faults is detected by the reviewer checker. The author's checker detects the four within its claim.

`[R405] PASS Tests — receipts/tables_identity_r405_4.txt, receipts/gates_r405_4.txt, receipts/probes_r405_4.txt`:
- table identity, keyed and positional, holds for all 22 tables and the PR body's 17 table lines;
- all pinned Markdown gates are rc 0 at the head;
- both census checkers fail on the faults they claim to detect and pass on the control.

`[R405] UNCLEAN Docs — PR #622 body :78 — F7`: the page delta (`606…:277-279`) and the PR body's Round 4 section (`:91-93`) are accurate against the archive.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F7 open) | `606…:255-285`; PR body `:78`, `:91-93`; round-4 assignment 5889146437; `author/` transcripts, `acmp.tsv`, `tools/b2_controller.py` | R405-4 | `5c57927413e0dae279f06a75d2a58e3fec8a2bb0` |
| RTL | CLEAN | delta diff, gitlinks, `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1285`, `KL_acmp_nvm_shadow.sv` and `protocol_processor_top.sv:2483-2485` at `c951a9ff` | R405-4 | `5c57927413e0dae279f06a75d2a58e3fec8a2bb0` |
| Robustness | CLEAN | `receipts/census_r405_4.txt`, `receipts/probes_r405_4.txt`, `receipts/label_payload_r405_4.txt` | R405-4 | `5c57927413e0dae279f06a75d2a58e3fec8a2bb0` |
| Tests | CLEAN | `receipts/tables_identity_r405_4.txt`, `receipts/gates_r405_4.txt`, `receipts/probes_r405_4.txt`, `author-r4/scripts/census_b2r4.py` | R405-4 | `5c57927413e0dae279f06a75d2a58e3fec8a2bb0` |
| Docs | UNCLEAN (F7 open) | the page's delta lines, both pages' unchanged blobs, `docs/findings/README.md`, the PR body, `b2-review-evidence` at `d677a15a` | R405-4 | `5c57927413e0dae279f06a75d2a58e3fec8a2bb0` |

F7 is in the PR body, not the tree. If it is fixed without a commit, Conformance and Docs can be re-covered at this same head, and RTL, Robustness and Tests stay banked at `5c579274`. If a commit is made, any lens whose scope that commit touches must be re-covered at the new head.

## Real limits

- This was a delta review. I re-derived the round-4 census claims and checked identity for every table. I did not recompute the measurement values in the tables, which rounds 1 and 2 covered.
- I ran no builder, parent, processor, gPTP or Yosys bank, no Verilator, no act and no hardware. None of them is relevant to a one-sentence docs delta.
- `check_baremetal_only.py --check` did not run: this host has no YAML library, and nothing was installed. The delta touches no file that gate scans for its rule, and the manager's source banks at this head cover it.
- Physical calibration was NOT RUN, and nothing here is hardware proof.
- The archived transcripts are redacted copies. I verified them against `published_sha256`; the redaction touches only the `controller` field, which the census does not read.
- The "writes no record" reading of the RTL is a static reading of the pinned shadow at `c951a9ff`. No simulation was run for it. The measured commits and slots are the empirical evidence.
- The `external` submodule is not initialized in this clone. Its gitlink `efeb541a` is unchanged, and the delta does not touch it.
- The clone was never modified (`receipts/clone_integrity_r405_4.txt`):
  - HEAD and the index tree are `5613d2b3`;
  - the worktree is clean, with nothing untracked or ignored;
  - `git diff --raw HEAD` is empty;
  - the four gitlinks are unchanged, and the three initialized submodules are clean at their gitlinks.

## Pending manager duties

- **Hosted evidence.** At review time, the exact head has 0 check runs, 0 commit statuses and 0 workflow runs (`receipts/hosted_and_external_r405_4.txt`). Hosted and act acceptance at the final head belongs to the manager.
- **Candidate merge.** GitHub reports `mergeable_state=dirty`. A scratch `git merge-tree` of `5c579274` into live dev `79c36963` (merge base `13eda870`) has a content conflict in `docs/findings/README.md` (`receipts/merge_probe_r405_4.txt`). This is unchanged from round 3. It must be resolved and validated in the merge-turn candidate.
- **PR body.** F7 is fixed in the PR body.
- **Pre-redaction commits.** `2c9f3df2` and `51bfa948` are still served by SHA and need GitHub-side removal.

R405-4 FINISHED
