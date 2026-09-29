[R405] POSITIVE - exact head 5c57927413e0dae279f06a75d2a58e3fec8a2bb0

# R405-5: external confirmation round for PR #622 (issue #606, with #608 and #75)

- Round R405-5, external independent reviewer, cleared context. The review start is PR comment 5889529153 (`receipts/review_start_5889529153.txt`).
- Exact head `5c57927413e0dae279f06a75d2a58e3fec8a2bb0`, tree `5613d2b3b7b0f0b8b8d710216647631401bf1265`. This is the same head as R405-4; no commit has been made since.
- Scope of this round: my R405-4 finding F7, in the PR body only. The manager edited the PR body, which F7's required outcome allows. My other R405-4 results stand as that round's ledger records them.

F7 is resolved. The Round 2 F2 bullet now reads "210 state-changing ACMP commands (105 `CONNECT_RX`, 105 `DISCONNECT_RX`), all to the peer's input, and no AECP write". That is the census as recorded, and it agrees with the census sentences that follow it in the same bullet and with the #606 page.

Nothing else changed:
- The body's other lines are unchanged. The only other difference is one trailing blank line, which renders nothing.
- The body's 17 table lines are byte-identical.
- The body carries no closing reference; it relates to #606, #608 and #75.
- The tree, blobs and gitlinks are the ones R405-4 reviewed.

No finding is open.

## Authorities, in the order read

1. `AGENTS.md` and `CONTRIBUTING.md` at the head: the verdict and ledger format, and lens coverage banked against a commit (section 7).
2. The issue #606 scope and my R405-4 report and receipts (`../b2-r405-4-packet`, all 20 files checked against its `MANIFEST.sha256`). F7's required outcome: the bullet's derivation clause states the state-changing ACMP count as recorded, as a PR-body edit only.
3. The #606 page at the head, `docs/findings/606_FIRST_BIND_MEASUREMENT.md:262-279`.
4. Public evidence on branch `b2-review-evidence`, live tip `32d9cc79`:
   - `review-evidence/b2-r1/author/` is still tree `fdde402a`, the same tree as at `666d8897` and at R405-4;
   - `MANIFEST.json`;
   - `reviews/` on that branch was not extracted or read.
5. The live PR #622 body and metadata (`receipts/pr622.json`, `receipts/pr622_body.md`), GitHub's closing-reference field, and hosted state at the exact head.

I read no other reviewer's report until the verdict, finding result and ledger below were written.

## Checks

### Check 1: the body changed only in F7's clause

My R405-4 snapshot of the body (sha256 `dd0f0896…`) was diffed against the live body (`4ee4193e…`, last edited 11:38:44Z). The diff is in `receipts/pr_body_r4_r5.txt`. There are exactly two hunks:
- `:78`, the Round 2 F2 bullet: "210 ACMP commands all to the peer's input" became "210 state-changing ACMP commands (105 `CONNECT_RX`, 105 `DISCONNECT_RX`), all to the peer's input". The rest of the line is byte-identical.
- `97a98`: one blank line was added at the end of the body, which now ends in four newlines instead of three. It renders nothing.

### Check 2: the bullet states the census as recorded

**Census re-run.** I re-extracted `author/` and `MANIFEST.json` from the live evidence branch and re-ran my round-4 census unmodified (`scripts/r405_4_census.py`, `receipts/census_r405_5.txt`).
- All 561 transcripts equal `published_sha256`.
- The output is byte-identical to `receipts/census_r405_4.txt` of R405-4.
- RESULT PASS, rc 0.

**Bullet against the census.** `scripts/r405_5_body_census.py` (`receipts/body_census_r405_5.txt`) reads the census receipt, the live body and the page. All 24 checks pass, rc 0:

| Bullet statement | Recorded (census) | Page |
|---|---|---|
| 210 state-changing ACMP commands, 105 `CONNECT_RX` and 105 `DISCONNECT_RX`, all to the peer's input | The only state-changing commands are 105 CONNECT_RX and 105 DISCONNECT_RX, all to peer input 8 | `:264-265` |
| no AECP write | The AECP commands seen are only GET_AVB_INFO, GET_CLOCK_SOURCE, GET_CONFIGURATION, GET_COUNTERS, GET_SAMPLING_RATE and READ_DESCRIPTOR | `:266` |
| Stream Input 1 unbound in 226 polls; Input 0 at the two censuses only | GET_RX_STATE 226 to input 1 and 2 to input 0 | `:267-268` |
| "The 210 `CONNECT_RX` and `DISCONNECT_RX` went to the reference peer" | Same 210 | `:277` |
| 228 GET_RX_STATE, 228 GET_COUNTERS, 4 READ_DESCRIPTOR to the DUT's inputs | 228 / 228 / 4, total 460 | `:279` |
| 226 console samples; commits (2 / 0); slots (229 / 230) | Unchanged text | `:262` and the restore tables |

The script also checks two further points:
- No unqualified "*n* ACMP commands" remains anywhere in the body.
- The bullet does not claim the 809-command ACMP total.

The bullet's first statement of the 210 now carries the same qualifier as its second. So the bullet agrees with itself, with the census that follows it, and with the page.

**Control.** Run on my R405-4 snapshot of the body, the same script fails exactly the four F7 checks: clause present, no unqualified count, old text absent, and the two statements agree. rc 1.

### Check 3: the body's tables are unchanged

`scripts/r405_tables.py`, unmodified since R405-2, keys each table by its header (`receipts/pr_body_r4_r5.txt`):
- 2 of 2 tables are SAME: the verdict table (10 lines) and the bind table (7 lines);
- positionally, all 17 `|` lines are identical, sha256 `a287bf70…` both before and after.

### Check 4: no closing reference

- GitHub's `closingIssuesReferences` for PR #622 has `totalCount` 0 (`receipts/pr_body_r4_r5.txt`).
- A keyword scan finds no `close`, `fix` or `resolve` form followed by an issue reference or issue URL.
- The body keeps "Relates to #606", "Relates to #608" and "Relates to #75".
- The body's own sentence "No issue closes here." (`:7`) names no issue, and "was resolved by" (`:79`) names a commit, so neither is a closing reference.

### Check 5: nothing else changed at the head

Head and tree are unchanged, as are the page blobs and gitlinks (`receipts/clone_integrity_r405_5_pre.txt`, `receipts/hosted_and_external_r405_5.txt`).
- `refs/heads/b2-bench-0929` and `refs/pull/622/head` are both `5c579274`. The PR's last commit is `5c579274`.
- The tree is `5613d2b3`. The three page blobs are the R405-4 blobs: `19dadb8b`, `c69870c5` and `01b2ecb1`.
- The four gitlinks are `efeb541a`, `5dce647a`, `c951a9ff` and `48ff7a7e`.
- Whole-PR scope `13eda870..head` is still the 3 files, +914 / −1.

**Gates.** I re-ran the pinned Markdown gates at the head. The environment is a fresh venv installed with `--require-hashes` from `tools/markdown/requirements.txt`: `cmarkgfm==2025.10.22`, `html5lib==1.1`, Python 3.14.7 (`receipts/gates_r405_5.txt`). All rc 0:
- `docs_check.py`: 0 findings, 176 md and 938 scrubbed files;
- `check_doc_style.py`;
- `gen_toc.py --check`;
- `gen_toc.py --verify-anchors`: 249 links;
- `check_em_dash.py --base 13eda870`: 914 added lines;
- `check_em_dash.py --selftest`: 339 arms;
- `check_doc_paths.py`: 854 paths;
- `check_feature_status.py`;
- `git diff --check 13eda870 HEAD`.

### Fault probes on this round's checkers

`scripts/r405_5_probes.sh` runs on disposable copies of the live body under scratch (`receipts/probes_r405_5.txt`). The control passes. Each seeded fault is detected:

| Mutant | Fault | Result |
|---|---|---|
| M1 | "state-changing" removed from the clause | body census rc 1 |
| M2 | split changed to 106 / 104 | body census rc 1 |
| M3 | "Relates to #606" changed to "Closes #606" | body census rc 1 |
| M4 | READ_DESCRIPTOR count 4 changed to 5 | body census rc 1 |
| M5 | one verdict-table cell changed | tables: 1 identical, 1 changed |

## Findings

**No finding is open at this head.**

- **F7 (MINOR, Conformance and Docs, R405-4): resolved.** This was the PR body's Round 2 F2 bullet, "210 ACMP commands all to the peer's input". The clause now names the state-changing count as recorded, with its split and target. The bullet agrees with its later census sentences and with page `:264-265` and `:277-279` (checks 1 to 3). This was a PR-body edit only, and the tree is unchanged (check 5).

### Suggestions (optional, no lens effect; carried, not re-litigated)

- **S1 (Docs).** `606…:255` still names the round-2 `saved_state_b2.py` as the derivation. `author-r4/scripts/census_b2r4.py` is the script that prints the `:277-279` counts.
- **S2 (Docs).** `608…:32` and `:229` say processor PR #133 "implements" or "adds" the leavealltimer restart. PR #133 is still open and unmerged, and processor #108 and #134 are open (`receipts/external_r405_5.txt`).

## Lens results

`[R405] PASS Conformance — PR #622 body :78 (receipts/pr622_body.md); receipts/census_r405_5.txt; receipts/body_census_r405_5.txt — the Round 2 F2 bullet's ACMP clause, reads and polls re-derived from the 561 archived transcripts; F7 resolved; the body carries no closing reference (closingIssuesReferences 0), and the Relates to lines for #606, #608 and #75 are kept.`

`[R405] PASS RTL — receipts/clone_integrity_r405_5_pre.txt (tree 5613d2b3, gitlinks efeb541a/5dce647a/c951a9ff/48ff7a7e) — no commit since R405-4, which covered RTL clean at this head against SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1285 and KL_acmp_nvm_shadow.sv at c951a9ff. A PR-body edit is outside RTL scope. The bullet's "reads, which write no record" is the page's :279 wording that R405-4 checked against that contract.`

`[R405] PASS Robustness — receipts/census_r405_5.txt, receipts/probes_r405_5.txt — the census re-run is byte-identical to R405-4 (copies excluded, inputs 0 and 1 counted separately, the wire has no non-read ACMP to a DUT listener). The body checker detects each of four seeded body faults, and the table checker detects a one-cell change.`

`[R405] PASS Tests — receipts/gates_r405_5.txt, receipts/pr_body_r4_r5.txt, receipts/body_census_r405_5.txt — the pinned Markdown gates are rc 0 at the head. The PR body's 2 tables and 17 table lines are identical. The body checker passes on the live body and fails the four F7 checks on the R405-4 body.`

`[R405] PASS Docs — PR #622 body (receipts/pr_body_r4_r5.txt: :78 and one trailing blank line only); docs/findings/606_FIRST_BIND_MEASUREMENT.md:262-279 — the bullet now agrees with the page and with itself. The page blobs are unchanged. S1 and S2 are optional.`

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | PR body `:78` against `receipts/census_r405_5.txt` (561 transcripts re-extracted from `b2-review-evidence` `32d9cc79`, `author/` tree `fdde402a`); `606…:262-279`; `closingIssuesReferences` | R405-5 | `5c57927413e0dae279f06a75d2a58e3fec8a2bb0` |
| RTL | CLEAN | delta and gitlinks (unchanged since R405-4); `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1285`, `KL_acmp_nvm_shadow.sv` and `protocol_processor_top.sv:2483-2485` at `c951a9ff` | R405-4 (no commit since; the body edit is outside scope) | `5c57927413e0dae279f06a75d2a58e3fec8a2bb0` |
| Robustness | CLEAN | `receipts/census_r405_5.txt`, `receipts/probes_r405_5.txt`; R405-4 `probes_r405_4.txt` and `label_payload_r405_4.txt` | R405-4, re-confirmed R405-5 | `5c57927413e0dae279f06a75d2a58e3fec8a2bb0` |
| Tests | CLEAN | `receipts/gates_r405_5.txt`, `receipts/pr_body_r4_r5.txt`, `receipts/body_census_r405_5.txt`, `receipts/probes_r405_5.txt` | R405-4, re-confirmed R405-5 | `5c57927413e0dae279f06a75d2a58e3fec8a2bb0` |
| Docs | CLEAN | PR body (full diff from the R405-4 snapshot); the three page blobs `19dadb8b`, `c69870c5` and `01b2ecb1` | R405-5 | `5c57927413e0dae279f06a75d2a58e3fec8a2bb0` |

All five lenses are banked at the exact head. A later commit that touches a lens's scope un-covers that lens. A later edit to the PR body re-opens Conformance and Docs for the body.

## Real limits

- This was a confirmation round on one PR-body clause. I did not recompute the page's measurement values, which rounds 1 and 2 covered. I did not re-derive the RTL reading, which R405-4 covered at this head.
- I ran no builder, parent, processor, gPTP or Yosys bank, no Verilator, no act and no hardware. None is relevant to a PR-body edit. The scoped Verilator was not used, so its identity was not checked.
- `check_baremetal_only.py --check` was not run: this host has no YAML library, and nothing was installed. No YAML changed.
- Physical calibration was NOT RUN, and nothing here is hardware proof.
- The census reads redacted transcripts. I verified them against `published_sha256`. The redaction touches only the `controller` field, which the census does not read.
- The `external` submodule is not initialized in this clone. Its gitlink `efeb541a` is unchanged.
- Clone state (`receipts/clone_integrity_r405_5_post.txt`):
  - running the gates created an ignored `scripts/__pycache__/`, which I removed;
  - afterwards HEAD, the index tree and `write-tree` are all `5613d2b3`;
  - `git diff --raw HEAD` is empty, and nothing is untracked or ignored;
  - the four gitlinks are unchanged, and the three initialized submodules are clean at their gitlinks;
  - the scratch `git merge-tree` wrote objects only.

## Prior public findings on this PR

This section was added after the verdict, finding result and ledger above were written. It uses R404-4 (PR comment 5889481776, `receipts/r404_4_public_comment.txt`), which I read in full for the first time here, and my own R405-4.

| Item | Disposition at `5c579274`, live PR body |
|---|---|
| R405-4 F7, MINOR (Conformance, Docs): "210 ACMP commands all to the peer's input" | **Resolved** (checks 1 to 4). |
| R404-4 F7, MINOR (Conformance, Docs): the same phrase | **Resolved.** This is the same defect on the same line. The live clause is word for word R404-4's example outcome. R404-4 counts 232 ACMP commands to the DUT (228 GET_RX_STATE to its inputs and 4 GET_TX_STATE to its outputs); my census has the same 228 + 4 (`receipts/census_r405_5.txt`). The final disposition belongs to R404. |
| R404-3 F6 and R405-3 F6, MINOR | Resolved at `5c579274` (R404-4, R405-4). The body edit does not touch the F6 sentences. |
| R404-2 F5, R405-2 F5; R404-1 F1-F4, R405-1 F1-F4, MINOR | Remain resolved. The tree is unchanged since R405-4. |
| R404-3 S4, R405-3 S1 and S2, R405-2 S4 | Not taken, and optional. Carried as S1 and S2. |
| R405-2 F4 residual: pre-redaction commits served by SHA | `2c9f3df2` and `51bfa948` still resolve (`receipts/hosted_and_external_r405_5.txt`). This is GitHub-side and belongs to the manager; it is not a head finding. |
| R404-5, the same round at this head | Its review started at 11:40:52Z. No verdict was published when I listed comments, so there is nothing to reconcile. |

## Pending manager duties

- **Hosted evidence.** The exact head has 0 check runs, 0 commit statuses and 0 workflow runs (`receipts/hosted_and_external_r405_5.txt`). Hosted and act acceptance belongs to the manager.
- **Candidate merge.** A scratch `git merge-tree` of `5c579274` into live dev `79c36963` (merge base `13eda870`) still has a content conflict in `docs/findings/README.md` (`receipts/merge_probe_r405_5.txt`). GitHub reports `mergeable_state=dirty`. The manager must resolve this in the merge-turn candidate, validate it, and check that the resolved index keeps both sides' rows.
- **Pre-redaction commits.** `2c9f3df2` and `51bfa948` are still served by SHA and need GitHub-side removal.
- **Merge rules.** Merge needs the second independent positive and explicit maintainer authorization.

R405-5 FINISHED
