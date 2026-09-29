[R399] POSITIVE - exact head 99bfd4bc3180bab97d47f63056513fb39eea6a37

# R399-4: external independent confirmation review of processor PR #133 (lane C1), R399-3 F1

- **Repository:** Mister-M-alt/protocol-processor-control-plane-avb-milan
- **Scope:** issue #108, PR #133
- **Exact head:** `99bfd4bc3180bab97d47f63056513fb39eea6a37`, tree `d8ec1053bf0968ed462d8a419a0cf859c41e9c3c`. This is the same head as R399-3: no commit since, and the PR API head is `99bfd4bc`.
- **Source base:** `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`
- **Parent live dev:** `79c36963660c10e4c1c11a744fb5bff41a552b8b`. It is still the dev head at this review. Its processor gitlink is `c951a9ff`.

## Verdict basis

- **R399-3 F1 (MINOR, Docs) is RESOLVED.** The PR body now ends with "Composed head `99bfd4bc` (manager note, R399-3 F1)". Its items 1-3 meet F1's required outcome items 1-3 point by point (section 2).
  - The rest of the body is byte-identical to the revision I read in round 3. The change is a pure 14-line append.
  - The closing references are exactly #29, #64, #65 and #108.
  - The 14 parent entries named in the manager's comment 5890073527 re-derive as PR #132's consolidated list (12 files), plus section 4's `sim_crf_licence.cpp`, plus the gitlink.
- **No MINOR or higher finding is open.**
- **Non-blocking items:**
  - R399-3 S1 is retained as a SUGGESTION and routed to the processor issue that owns `tb/pp_top` coverage.
  - One new SUGGESTION (S2, Docs) is routed to the parent pin-adoption lane.
  - The three round-2 SUGGESTIONs are retained.
- **Source is unchanged, so the round-3 source judgement carries.** I re-confirmed it at this head: the SRP and top suites, the docs gates, lint, the composition recomputation and the clone integrity check.
- **Pre-read record.** My verdict and ledger were fixed in `receipts/pre_read_verdict.md` before I read the other reviewer's reports.

## 1. Reconstruction (in order)

1. **Governance.** The processor repository has no `AGENTS.md` or `CONTRIBUTING.md` and no submodules. I read `README.md`, `docs/README.md` and the `Makefile` gates, as in round 3.
2. **Issue #108.**
   - The body (acceptance 1-3).
   - Manager assignment 5883702094: items 1-4, where item 4 is the parent-visible list in the PR body.
   - Round-2 assignment 5886235840.
   - The executor TAKEN and REVIEW READY notes.
3. **PR #133.**
   - The body now, and its edit history (three revisions: 07:18:21Z, 09:58:59Z and 12:13:58Z).
   - The closing references.
   - The manager's comments: 5890073527 (the combined bank) and 5890098447 (review start).
   - My own R399-3 report, 5890060845 (`receipts/r399-3-report.md`).
4. **PR #132's body** and its section "Parent-visible for pin adoption: rounds 1-6, consolidated" (`receipts/pr132-body.md`).
5. **Diff and history.**
   - `git diff c951a9ff..99bfd4bc`, split into C1 (`412efeb7`) and #132 (`d352bbaa`) by `scripts/composition_check.sh`.
   - The C1 port and parameter scope check (`receipts/scope_item2_ports.txt`).
6. **Public evidence.**
   - `kebag-logic/milan-fpga` `a6427910…/review-evidence/ppC1-r1`: still the round-1 author packet only (`receipts/public_evidence_ppC1-r1.txt`).
   - The parent files at `79c36963`, fetched through the public API.
   - The hosted checks at the exact head.
7. **Prior public reviews** (R398-1, R398-2), read after `receipts/pre_read_verdict.md` was written.

## 2. R399-3 F1 against the amended body

### 2.1 The body change is a pure append

`scripts/body_check.sh` (`receipts/body_check.txt`, `receipts/pr133-body-diff-r3-to-now.txt`, `receipts/pr133-edit-history.json`) establishes the following.

**Revisions.**
- The body revision current during round 3 was the 09:58:59Z edit: 213 lines, sha256 `775aa8f0…`. No edit fell between it and 12:13:58Z, so it is the body R399-3 read.
- The live body (sha256 `6c823d72…`) equals the 12:13:58Z revision. The REST and GraphQL bodies are identical.

**Diff.** `diff` reports `213a214,227`: 14 lines added after the last round-3 line, and 0 removed or changed. Sections 1-4, Validation, What remains, Round 2 and the "round-1 record" sentence are byte-unchanged.

**Closing references.**
- The body keeps `Closes #29`, `Closes #108`, `Closes #64` and `Closes #65`, at lines 3-6 as before.
- GitHub's closing references are exactly [29, 64, 65, 108].

### 2.2 Item by item

**Item 1: name the combined pin-adoption edits. MET.**
- Required: the pin-adoption edits at this head are #132's consolidated list (rounds 1-6) plus C1's section 4: crflic `>= 3` at `sim_crf_licence.cpp:953,956`, the `milan_dp/README.md` `[C]` row and "What it cannot show", and the parent documents.
- The note's item 1 says exactly this. It names #132's list by its heading and lists the three section-4 components.
- Its added sentence, "The two lists touch no common parent file", is true of the lists as written. Neither list names a file the other names (`receipts/fileset_check.txt`). S2 below concerns the adoption edits the lists imply, not their text.

**Item 2: scope the section-4 claims to C1's own commits. MET.**
- Required: "rc 0 as is", "one expectation to re-base" and "no interface change" are scoped to C1's commits (`412efeb7` against `c951a9ff`).
- The note's item 2 scopes all three quoted phrases to `412efeb7` against `c951a9ff`. It also states that #132's ports, parameters and snapshot word 37 reach this head through the merge.
- I checked this against the RTL (`receipts/scope_item2_ports.txt`, raw `git diff`):
  - C1's only declaration-line change in `KL_srp_top.sv` or the top is the `active_o` comment text. The declaration itself is unchanged, and the top's change is the `srp_active_o` comment.
  - #132 adds `restore_closed_o`, `restore_rb_o`, `rs_cause_o`, `restore_cause_o` and `d3_unflushed_o` (head `protocol_processor_top.sv:479,483,487,491,516`).
  - #132 adds `NVM_RS_AGG_CYC_P` and `NVM_RETRY_BACKOFF_CYC_P` (`:146`, `:151`) and changes the default of `NVM_RS_TMO_CYC_P`.
  - The scoped statements are therefore true, and the unscoped reading is withdrawn.

**Item 3: record the manager's combined-edit bank. MET.**
- Required: record the manager's combined-edit parent bank result at dev `79c36963`, or point to it.
- The note's item 3 records "16 of 16 commands rc 0" at `79c36963` with both lists applied, and links comment 5890073527.
- That comment names the setup (gitlink at `99bfd4bc`, #132's consolidated edits, the section-4 crflic edit), the 16 commands and the 14 entries.
- I did not rerun the bank; the brief does not allow it. The result is the manager's attested evidence, and its setup is consistent (2.3).

### 2.3 The combined-edit file set, re-derived

`scripts/fileset_check.sh` reads the parent at `79c36963` through the public API (`receipts/fileset_check.txt`). It maps each edit in #132's consolidated list to a parent file and checks that the edit's target exists there:

| #132 consolidated-list edit | Parent file at `79c36963` | Target present |
|---|---|---|
| Top ports, parameters, glue | `hdl/milan/KL_pp_shadow.sv` | yes (the top instance) |
| Evidence classifier (`DUT_READER_DISPOSITIONS`) | `scripts/measure_test_evidence.py` | yes |
| `PP_CTRL[1]` in `gmstep`, `gptp`/`gptp-lat` | `milan_dp/sim_gmstep.cpp`, `milan_dp/sim_gptp.cpp` | yes (no walk today) |
| `ax1x1gptp` walk in `configure()` | `milan_dp/sim_ax1x1gptp.cpp` | yes |
| Image-less legs (main, `nolpf`, `ax1x1`; `aclk`) | `milan_dp/sim_main.cpp`, `milan_dp/sim_aclk.cpp` | yes |
| `sim_nxn` legs: degrade arm retired, `[AECP-WTMO]` moved | `milan_dp/sim_nxn.cpp` | yes |
| `milan_dp_render` T8 REMOVE wait | `milan_dp_render/sim_tdm8_render.cpp` (T8 at `:2082`) | yes |
| `pp_shadow` K, K10, K12, M2, P3 | `pp_shadow/sim_main.cpp` | yes |
| `cosim_top.sv` pins and derivations | `nvm_cosim/cosim_top.sv` | yes |
| B1-B4 give-up window | `nvm_cosim/cosim_cases.cpp` (`erase_fault_case`, `idle(1500)` at `:488`, B1-B4 at `:496-499`) | yes |
| Firmware boot path | not applied (#132: "no consumer-set gate exercises it") | n/a |

Adding C1's section-4 crflic edit (`milan_dp/sim_crf_licence.cpp`, still `>= 4` at `:953,956`, blob `6f9d17b1`) and the gitlink gives 13 files plus the gitlink. That is exactly the 14 entries comment 5890073527 names.

C1's section-4 parent documents are not in the bank's edit set. The bank is a gate run, and the comment applies only "this PR's section 4 crflic edit". That is consistent with R399-3 F1 item 3, which asked for the bank with the declared code edits.

## 3. Findings

No BLOCKER, MAJOR or MINOR finding is open.

### S2: SUGGESTION (new). Lens: Docs

**Summary.** The two lists' implied adoption edits meet in the parent `milan_dp` README. #132's consolidated list changes behaviour that `tb/verilator/milan_dp/README.md` documents, and names no parent document for it.

**Where.** `tb/verilator/milan_dp/README.md` at parent dev `79c36963` (blob `3f05559f`):
- `:869-882` states that every leg drives the degrade path and that "The `[AECP]` checks in `sim_nxn.cpp` grade that path … `BAD_ARGUMENTS`". #132's list retires that arm in every `sim_nxn.cpp` leg and replaces it with two hold checks.
- `:633-637` lists `sim_main`, `sim_nxn`, `sim_aclk` and `milan_dp_render` as the harnesses that set `PP_CTRL[1]`. #132 adds `gmstep`, `gptp` and `ax1x1gptp`.

**Authority.**
- #108 assignment item 4 (the parent-visible list).
- #132's consolidated list.
- The manager note's item 1 sentence "The two lists touch no common parent file".

**Impact.**
- The note is true of the lists' text.
- A pin-adoption lane that applies only the named edits would update this README for C1's `[C]` row and issue-108 sentence, but leave its `[AECP]` degrade-path and walk-harness passages stale.
- No gate catches it: `docs_check.py` passed in the 16-command bank.
- This is a residue of #132's merged list, not of C1's text, so it does not block this PR.

**Suggested outcome.** The pin-adoption lane (parent evidence owner milan-fpga #76) updates `milan_dp/README.md:633-637,869-882` together with C1's rows at `:443,528-530`, in one edit of that file.

**Verification.** At pin adoption, the README names the hold checks in place of the degrade arm, and names all the walk-starting harnesses.

### Retained SUGGESTIONs (no source change since round 3)

**R399-3 S1: SUGGESTION. Lens: Tests.** No in-tree check grades C1's rLA! restart at the full top while #132's D3 writer holds AECP. `tb/pp_top/pp_top_wrap.sv` leaves `srp_active_o` and the SRP status outputs unconnected.
- State: RETAINED, unchanged.
- Where it goes: a processor residue, for the manager to route to the processor (PP) issue that owns `tb/pp_top` / SRP full-top coverage. It is not a pin-adoption item.

**R398-2 S1 = R399-2 S1: SUGGESTION.** A dropped LeaveAll re-arm silences that application's own LeaveAll until the next rLA! or reset.
- State: RETAINED.
- Where it goes: the manager's routing to a processor issue.

**R398-2 S2 = R399-2 S2: SUGGESTION.** No committed check covers a `now_ms` wrap.
- State: RETAINED.
- Where it goes: as above.

**R399-2 S3: SUGGESTION.** Superseded mutant counts remain in the `tb/srp_top/README.md` tables.
- State: RETAINED.
- Where it goes: as above.

## 4. Prior public review findings at this head

| Finding | State at `99bfd4bc` | Evidence |
|---|---|---|
| R399-3 F1 (MINOR, Docs): the parent-visible list does not read with #132's | RESOLVED | Section 2: pure-append body note, items 1-3 met, file set re-derived |
| R399-3 S1 (SUGGESTION, Tests) | RETAINED | source unchanged (composition check: every C1-only and #132-only file equals its lane head) |
| R398-1 F1 (MINOR, Docs): the milan_dp README omitted | RESOLVED | body section 4 unchanged (pure append); README blob `3f05559f` unchanged at `79c36963` |
| R398-1 S1 = R399-1 S2; R398-1 S3; R399-1 S3 | RESOLVED | docs 10 §6.2 and §6.5 unchanged since `412efeb7`; `make check` rc 0 |
| R398-1 S2; R399-1 S1 | RESOLVED | `srp_top` 2200/2200 at this head (default run). The P8 lines report 0 own MSRP and MVRP LeaveAlls at arm delays 3, 4, 8 and 16 (`receipts/suites/srp_top.log:372-375`). The round-3 campaign (78/78 killed) covers the unchanged source |
| R398-2 S1 = R399-2 S1; R398-2 S2 = R399-2 S2; R399-2 S3 | RETAINED, SUGGESTION | `KL_srp_top.sv`, `tb/srp_top` unchanged |

## 5. Lens results

**Conformance: CLEAN.**
- 802.1Q-2014 Table 10-5 rLA! ("Start leavealltimer, Passive"), per application with the 10.7.5.20 scoping, is unchanged at `hdl/srp/KL_srp_top.sv:1028-1033` and `:1233-1241`. It is graded by `srp_top` P1-P8 and Q1-Q4 (Milan Table 4.3) and R1-R4 (Milan 4.3.2): 2200/2200 at this head (`receipts/suites/srp_top.log`).
- The body's scoped claims match the clause-level behaviour.

**RTL: CLEAN.**
- `git merge-tree --write-tree 412efeb7 d352bbaa` = `d8ec1053`, the head tree.
- The shared-service instances and `KL_srp_top` are byte-identical across base, C1, #132 and head.
- #132's top diff names no SRP net (`receipts/composition_check.txt`).
- C1 changes no port or parameter; its changes there are comments only (`receipts/scope_item2_ports.txt`).
- `lint_hdl` rc 0 (`receipts/lint_hdl.log`).

**Robustness: CLEAN.**
- The source is unchanged, and the round-3 full-top probe results (AECP flood in hold and booted) carry.
- The retained dropped-re-arm SUGGESTION is unchanged in exposure: the arm lines are identical in all four revisions.

**Tests: CLEAN (SUGGESTIONs only).**
- At this head: `srp_top` 2200, `srp_encoder` 581, `srp_stream_fsms` 1219 and `pp_top` 7888, all rc 0 (`receipts/suites/SUMMARY.txt`). The counts are identical to round 3.
- Hosted runs 36558392722 (pull_request) and 36558385720 (push): every job succeeded (`receipts/hosted_checks.txt`). The only skipped step is "Build Verilator v5.050", skipped on a cache hit; every other step executed.
- S1 is retained.

**Docs: CLEAN (S2 new, SUGGESTION).**
- F1 is resolved (section 2).
- `make check` rc 0: matrices, parameters 26/26/26, links (`receipts/make_check.log`).
- `gen_matrix.py --check` rc 0.

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_srp_top.sv:1028-1033,1233-1241`; `srp_top` P1-P8, Q1-Q4 and R1-R4 at the head (2200/2200); body section 4 and the composed-head note against the clause | R399-4 | 99bfd4bc3180bab97d47f63056513fb39eea6a37 |
| RTL | CLEAN | merge-tree recomputation; the four instances byte-compared; C1 and #132 port/parameter declaration diffs (raw); head top `:146,151,479-516`; `lint_hdl` | R399-4 | 99bfd4bc3180bab97d47f63056513fb39eea6a37 |
| Robustness | CLEAN | source identity to round 3 (every lane-only file equals its lane head); arm lines identical; round-3 probe receipts carried | R399-4 (carries R399-3 probe) | 99bfd4bc3180bab97d47f63056513fb39eea6a37 |
| Tests | CLEAN (SUGGESTIONs only) | `srp_top`, `srp_encoder`, `srp_stream_fsms`, `pp_top` at the head; hosted jobs and steps at the head; round-3 campaigns carried (source unchanged) | R399-4 | 99bfd4bc3180bab97d47f63056513fb39eea6a37 |
| Docs | CLEAN (S2 SUGGESTION) | PR body revisions 09:58:59Z and 12:13:58Z, and their diff; closing references; manager comment 5890073527; PR #132 consolidated list; 14 parent entries at `79c36963`; `milan_dp/README.md:443,528-530,633-637,869-882`; `make check`; `gen_matrix --check` | R399-4 | 99bfd4bc3180bab97d47f63056513fb39eea6a37 |

## 7. Real limits

**Not run by this review:**
- the parent consumer bank and the donor bank (the combined-edit 16/16 and the donor 9/9 are the manager's attested results);
- the full processor, gPTP, Yosys and builder banks;
- the mutation campaigns (not rerun: source unchanged since round 3, which ran them at this head);
- act, hardware and physical calibration. Physical calibration was NOT RUN, and field skips are not hardware proof.

**Manager source banks.** The public evidence tree `a6427910…/review-evidence/ppC1-r1` still holds only the round-1 author packet. The manager's source static/builder and native bank pass at this head is not independently verified here. The hosted run and my local suites are the executable evidence I inspected.

**Combined edits.** I did not apply the combined edits to a parent. The file-set check reads targets at `79c36963` and does not show that the edit script applies.

**Tool path.** The brief's `372-manager-candidate1/pinned-tool-bin/verilator` path does not exist on this host. I used a scratch wrapper to the same Verilator 5.050 binary that all 199 manager `pinned-tool-bin` wrappers present point to. Its sha256 is identical to round 3's (`receipts/tool_identity.txt`).

**Standards text.** The 802.1Q and Milan texts are not distributed. Clause wording is as quoted in the issue and the tree.

## 8. Pending manager duties

1. Two independent positive reviews at this head, then the final current-dev candidate at the merge turn (source base `c951a9ff`, live dev `79c36963`), and hosted/act acceptance.
2. At pin adoption (parent #76), the combined list:
   - #132's consolidated edits, including the firmware boot-path obligation;
   - C1's crflic `>= 3` and the parent documents;
   - S2's `milan_dp/README.md` passages, in the same edit as C1's rows.
3. Route the processor residue to the relevant PP issue:
   - R399-3 S1 (full-top rLA! under the D3 hold, `tb/pp_top`);
   - the dropped-re-arm re-issue;
   - the `now_ms` wrap check;
   - the `srp_top` README count cells;
   - the author's re-DECLARE_TALKER VLAN refcount leak.

## 9. Packet

- **`scripts/`:**
  - `body_check.sh` (body revision diff and closing references);
  - `fileset_check.sh` (parent file-set re-derivation);
  - `composition_check.sh` and `run_suite_subset.sh`, carried from round 3.
- **`receipts/`:** raw outputs, with host paths replaced by placeholders. It also holds my R399-3 report text, the PR #133 body revisions, the PR #132 body and the manager's comment 5890073527.
- **`MANIFEST.sha256`:** every published file. Disposable trees stayed under `scratch/`.
- **Clone integrity:** the clone is byte-exact at the head. 329 tracked entries were re-hashed with modes checked, and 0 differ. The index and worktree equal HEAD, `git status --ignored` is empty, and there are no gitlinks (`receipts/clone_integrity.txt`).

R399-4 FINISHED
