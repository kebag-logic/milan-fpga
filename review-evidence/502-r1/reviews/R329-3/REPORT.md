[R329] NEGATIVE - exact head 867a2e38a4e3231545a0a24b97d1e5612a6659fe

Round R329-3 is the external independent re-review of kebag-logic/milan-fpga PR #579 for issue #502. It is a delta review.

- **Head:** `867a2e38a4e3231545a0a24b97d1e5612a6659fe`, tree `d0c5cc45362c34d2db66d61bc051659da50df2a1`.
- **Delta judged:** `5d4cf33e..867a2e38`, one commit touching 5 files: `CHANGELOG.md`, `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md`, `docs/reference/SUBMODULES.md`, `tb/verilator/pp_shadow/README.md` and `tb/verilator/pp_shadow/sim_main.cpp`.
- **Base:** source base `831f94f4`. My round R329-2 covered `5d4cf33e` in full.

Lenses applied this round: Conformance, RTL, Robustness, Tests, Docs (all five).

**Result:** Conformance, RTL, Robustness and Tests are CLEAN.

- All four round-3 assignment items are delivered and verified.
- The new committed K12 partial-refusal control kills P4 in both legs by named checks.
- There is no RTL, firmware, configuration or gitlink change.

**Why NEGATIVE:** Docs is UNCLEAN because of one new MINOR finding, R329-3-F1.
- Section 15 (UNRESOLVED), item 3 of `SAVED_STATE_MATERIALIZATION.md` still lists the #502 defect as open and present: "the status reads durable over an applied name or map for a program's tail".
- The same page's section 2 and the ownership page's UNRESOLVED item 2 now state that it is corrected.
- The text predates the PR. The PR's behaviour change made it false. I missed it at round 2.

## Reconstruction

1. I read AGENTS.md, CONTRIBUTING.md and docs/README.md.
2. I read the issue #502 body (acceptance: the two tracked-glue checks pass on the shipping glue) and the decisions already reconstructed in my rounds R329-1 and R329-2 (5844866872, 5845129498, 5846418959, 5848417938).
3. I read the round-3 assignment 5854008765 (items 1-4, no RTL change) and REVIEW READY 5854113729.
4. I read the PR #579 body at the head: `headRefOid` 867a2e38, not draft.
5. Authorities:
   - `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 6.1, the section 11 table and section 20 UNRESOLVED;
   - `SAVED_STATE_MATERIALIZATION.md` sections 1, 2, 10 and 15;
   - `docs/reference/SUBMODULES.md`;
   - `CHANGELOG.md`.
6. I read `git diff 5d4cf33e..867a2e38` and its commit (`receipts/scope-raw.log`).
7. The public evidence tree `dc9d0928:review-evidence/502-r1` holds only author sweep material from earlier rounds. The round-3 claims in REVIEW READY and the PR body were all re-executed independently here.
8. Prior public findings (R328-2's report and my own R329-2) were read for resolution only after my own pass over the diff. I did not open the other round-3 reviewer's material.

## Verification of the assigned questions

### (1) CHANGELOG and SUBMODULES describe the delivered trigger

- **`CHANGELOG.md:39-40`** now reads:
  - "Actual parent phase-5 map writes raise the same sticky source."
  - "Unchanged map records raise nothing."

  The superseded "Accepted map commit beats raise the same sticky source." is gone.
- **`docs/reference/SUBMODULES.md:61`** now reads "The parent's actual-write enable supplies the map trigger." The superseded "Map phase 5 supplies the corresponding map trigger." is gone.
- **Both match the RTL.** `amap_edit_live_wr_p` (`hdl/milan/milan_datapath.sv:4269-4271`) is the store's write condition. It reaches the shadow's `amap_live_wr_i` (`KL_pp_shadow.sv:388,945-946`). Neither line claims every commit beat or the processor phase-5 export.
- **Search of the tree outside `docs/history`** for "commit beat(s)", "phase-5 export", "Map phase 5 supplies" and "conservative":
  - No #502 map-trigger statement remains stale.
  - The remaining hits (`SAVED_STATE_MATERIALIZATION.md:2061,2117`) are the section 15 proposed future record-writer text, as at round 2.
  - The "Map phase 5 cannot stall" lines (`SAVED_STATE_SNAPSHOT_OWNERSHIP.md:967`, `KL_pp_shadow.sv:931`) concern the accepting edge and remain true.
- **`SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1263`** (R328-2 S2) now reads "nvm_pend 1 from the first actual write until reset". This matches its own change-indication column, "actual phase-5 map write enable".

### (2) The K12 partial-refusal control

**Code** (`tb/verilator/pp_shadow/sim_main.cpp:1459-1469`, inside `pending_map_commands`, run for 0x000e and, on the dynamic fixture, 0x000f):
- `pending_boot(6)` gives a fresh durable baseline, graded by "K control: reset/load permits durable status" 0x40 and the backend-pending check.
- The command is a two-record ADD. Record 0 is all zero and claims key 0.
- Record 1 differs only at payload offset 18 for input (`mapping_stream_channel` = 1, same cluster key) or offset 20 for output (`mapping_cluster_offset` = 1, same stream key). So record 1 conflicts with record 0's claim.

**Grading:**
- `pending_command(..., 7)`: the response matches, with status 7.
- `pending_map_value(type, 0, ...)`: GET_AUDIO_MAP returns 0 records.
- `pending_report(tag, 0, 0, 0)`:
  - `no_durable_claim_over_unsaved` 0 and `pending_from_accepting_edge` 0;
  - accepted name lanes 0, phase-5 records 0, marks 0 and mark group;
  - `live_state_changed` 0 from the storage observer (name RAM, input store, output owner/valid/cluster, capture map);
  - `sticky_pending_PP_STAT` 0 and `sticky_pending_PP_NVM_STAT` 0.

  This is refusal status, an unchanged map and pending clear, as assigned.

**Default target** (`receipts/pp_shadow-default.log`): `make -C tb/verilator/pp_shadow` gives rc 0, with 295 + 591 + 591 + 591 checks and 0 failures.
- Round 2 was 263 + 575 x 3. The +16 per direction is exactly boot 2, the ADD command 2, the GET command 2, the record count 1 and the report 9.
- "K12 partial refusal input" appears in all four builds.
- "K12 partial refusal output" appears in the dynamic build, which is the only build with a dynamic output port. The static builds keep "K12 static output refused".
- `make ... pending-mutant` gives rc 0: "PASS: late-mark mutant killed by K10 and K12; clean control passes" (`receipts/pending-mutant.log`).

**R328's `r328_2_dp_mutants.py`, rerun unchanged** (sha256 `5f933518...`, identical to its publication; `receipts/script-identity.txt`, `receipts/r328_2_dp_mutants/`). The shipping datapath and shadow hashes are identical before and after every mutant.

| mutant | static | dynamic | named checks |
|---|---|---|---|
| **P4_no_phase5** | **KILLED (2)** | **KILLED (4)** | **only** `K12 partial refusal input sticky_pending_PP_STAT/_PP_NVM_STAT` (static); plus `... output ...` (dynamic) |
| P1_in_only | SURVIVED | KILLED (9) | K12 output ADD/REMOVE (static leg has no dynamic output) |
| P2_out_only | KILLED (9) | KILLED (9) | K12 input ADD/REMOVE |
| P3_unqualified | KILLED (2) | KILLED (4) | `K12 duplicate *` sticky |
| P5_no_context | SURVIVED | SURVIVED | see note |
| P6_tied_low | KILLED (9) | KILLED (17) | |
| S1_shadow_ignores_input | KILLED (9) | KILLED (17) | |
| E1_no_beat, E2_priority_dropped (equivalence controls) | SURVIVED | SURVIVED | expected |

At round 2 R328 recorded P4 SURVIVED in both legs. The only change is P4, now killed by the new control.

**P5 note.** P5 drops `amap_edit_context_w` from the pulse only; the store still requires it (`:4371`, `:4382`).
- The claims are cleared at phase 0 (`:4330-4335`) and set only under `amap_edit_context_w` in phase 4 (`:4349`).
- So P5 can diverge only on a phase-5 beat presented outside an active, header-matching transaction.
- That is a processor-sequencing violation, not a command the harness can send. R328-2 reached the same conclusion. It is not a finding.

**R328's `r328_2_multirec_probe.py`, rerun unchanged** (sha256 `d58c9a1a...`; `receipts/r328_2_multirec_probe/`):
- **Shipping:** 327 checks, 0 failures; Q1/Q2 give status 7, phase-5 records 0, storage changes 0 and PP_STAT[11] 0.
- **P4:** 8 failures. These are its own Q1/Q2 sticky checks plus the 4 committed `K12 partial refusal input/output sticky_*` checks, with PP_STAT[11] = 1 and storage changes 0. The committed control therefore detects the same false pending that the probe exists for, on the same payload.
- **P5:** passes.

**My round-2 scripts, rerun with byte-identical per-mutant scripts** (`r329_mutants.py` `3aeb65eb...`, `r329_mutants_adapter.py` `9df8e35f...`, `r329_dp_mutants.py` `480c9a24...`, `r329_probe.py` `378391e9...`). The driver `scripts/r329_3_campaign.sh` runs the same mutant lists as `r329_campaign.sh`, split into parts and run with up to 8 parallel jobs. Results are in `receipts/mutant-campaign.txt`.

| leg set | result at 867a2e38 |
|---|---|
| unchanged | control PASS: dyn 295/0, static 189/0 |
| unchanged | M3 FAIL 12/8; M7 FAIL 29/19 |
| unchanged | M1, M2, M4, M5, M6, M8, M9, M10 `REFUSED anchor count 0` (never counted as kills) |
| adapter | every M and U mutant FAIL in each leg where its defect is observable |
| adapter | U8 static PASS, as at round 2 (no dynamic output in that leg) |
| adapter, changed from round 2 | M5 FAIL 12/6 (was 8/4), M9 16/10 (was 12/8), U5 12/6 (was 8/4). The increases are exactly the new `K12 partial refusal * sticky_*` checks: the phase-4 trigger fires on record 0's claim. The new control strengthens these kills. |
| parent-side | D1 FAIL dyn 10 / static PASS (as round 2); D2 FAIL 10/10; D3 FAIL 4/2 |

The shipping shadow and datapath are unchanged after every campaign.

**My probe** `r329_probe.py`, shipping and mutants M5, M6, U6 and U11 (`receipts/probe/`):
- Every `R329` result line is identical to round 2 (`receipts/probe/round2-vs-round3.txt`).
- Shipping: 327 checks, 0 failures, and P3 "pend 0, durable 1".

### (3) No RTL, firmware or configuration change; the PR body

**Scope** (`receipts/scope-raw.log`):
- `git diff 5d4cf33e..867a2e38` restricted to `hdl sw configs syn scripts .github` and every gitlink is empty (0 lines).
- All 5 paths are mode `100644` -> `100644`.
- The gitlinks `protocol-processor@870ff88a`, `gptp-processor@5dce647a` and `third_party/verilog-axis@48ff7a7e` are identical at both commits.

**PR body:**
- The stale "prepared locally / has not been applied" sentence is gone (R329-2 S1).
- Round-2 results are labelled as round-2 evidence, and the "Round 3" section is accurate against my reruns: 591 x 3 + 295; P4 killed static 2 / dynamic 4 by the named checks; 24 parent-pulse legs; multirec shipping 327/0.
- "Round 2 changes no ... submodule pin" is scoped to round 2 and is true. The pin advance is stated in the Description.
- No stale line was found.

### (4) Docs gates and pp_shadow

- **Gates:** all 23 commands in `scripts/r329_3_gates.sh` returned rc 0 in a clean disposable copy (`receipts/gates.log`). They are the round-2 list, with `git diff --check` taken against `5d4cf33e` in addition to `831f94f4`. They include `docs_check`, `check_em_dash --base 831f94f4`, `check_doc_style`, `gen_toc --check/--verify-anchors`, `check_doc_paths`, `lint_rtl --check`, `measure_test_evidence --check`, `check_port_contracts`, `check_submodule_docs` and `check_nvm_capture`.
- **No-git mode:** `GIT_DIR=/dev/null docs_check` gives rc 0 with 0 findings (`receipts/docs-check-nogit.log`).
- **pp_shadow:** as in (2).
- **Markdown gates:** these used a private venv from `tools/markdown/requirements.txt --require-hashes`.

## Findings

### R329-3-F1 - MINOR - Docs - `docs/design/SAVED_STATE_MATERIALIZATION.md:2081-2083` - UNRESOLVED item 3 still states the #502 defect as open and present

**Authority:**
- AGENTS section 6 Docs: "Changed contracts are reflected in authoritative docs".
- Issue #502, whose title and body name this exact window. It is the PR's `Closes #502`.
- The same page's section 2 (`:224-235`): "Issue #502 implements that standalone reporting correction ... Pending therefore rises on the accepting live-write edge".
- `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1738-1742`, section 20 UNRESOLVED, item 2 of the companion page, which this PR updated: "Issue #502 uses live acceptance instead, so the status no longer reads durable over them."

**Evidence** (`receipts/f1-evidence.txt`):
- Section 15 UNRESOLVED, item 3, reads: "**The mark-tail window of today's glue** (#502, open): the status reads durable over an applied name or map for a program's tail. Every stage declared shippable waits for its correction (section 10)."
- The text is byte-identical at base `831f94f4`, where it was true, and the PR diff does not touch it.
- At the head, the committed K10/K12 `no_durable_claim_over_unsaved` checks prove the opposite on the shipping glue, and the late-mark mutant must fail them.
- So the page contradicts its own section 2. It also contradicts the ownership page's UNRESOLVED list, which the PR did update.
- This is the same kind of defect as R328-1 F2 (stale sections 1 and 5.2 of this page) and R329-2 F1 (stale CHANGELOG line), both rated MINOR and fixed. I did not catch it at round 2.

**Impact:**
- A reader of the page's UNRESOLVED list, which is where open work is looked up, concludes that the shipping status still reads durable over a live name or map change.
- The reader also concludes that every stage remains blocked on an uncorrected defect.
- After the merge closes #502, the item names a closed issue as open.
- Behaviour and tests are correct; this is documentation accuracy only.

**Required outcome:** Section 15 item 3 no longer states the window as an open, present defect of the current glue. For example, it records that #502's standalone correction removes it, while section 10's release condition stays as written.

**Verification:**
- Read section 15 at the corrected head against section 2 (`:224-235`) and `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1738-1742`.
- Confirm that `docs_check`, `check_em_dash --base 831f94f4`, `check_doc_style` and `gen_toc --check/--verify-anchors` pass.
- Only a Docs re-review is needed if nothing else changes.

### R329-3-S1 - SUGGESTION - Docs - `docs/design/SAVED_STATE_MATERIALIZATION.md:1717,2070-2071` - present-tense references to the mark trigger of the glue

Line 1717 says "Triggering on the commit marks, as the tracked glue does". Lines 2070-2071 say "a mark trigger reads durable over an applied change for the program's tail (EXECUTED on today's glue, section 2)".

Both cite historical evidence that section 2 labels as "at its stated historical source", so neither is wrong as evidence. Qualifying them as the pre-#502 glue while fixing F1 would stop a cold reader from reading them as current. This is optional.

There is no BLOCKER or MAJOR finding.

## Clean-lens evidence

`[R329] PASS Conformance - CHANGELOG.md:37-44; docs/reference/SUBMODULES.md:57-62; milan_datapath.sv:4269-4271; KL_pp_shadow.sv:388,945-946 @867a2e38 - checked:`
- assignment 5854008765 items 1-4 are delivered;
- the stated trigger equals the RTL write condition (decision 5848417938, option (a));
- the partial refusal answers status 7 with no write or pending;
- the name source, the accepting edge and the duplicate behaviour are unchanged (pp_shadow 591 x 3 + 295, 0 failures).

`[R329] PASS RTL - receipts/scope-raw.log; milan_datapath.sv:4054-4090,4246-4271,4316-4400 @867a2e38 - checked:`
- zero RTL, firmware, configuration or gitlink bytes changed since `5d4cf33e`, which R329-2 covered in full (equivalence, CDC/reset, width, OOC);
- the shipping datapath and shadow sha256 are unchanged across all mutants;
- the P4 kill path is structural: phases 2/3 (`:4344-4347`) clear only `txn_active`/`out_resv`, so claims survive the abort, and the phase-5 term is what blocks a pulse there;
- the P5/E1/E2 survivals are consistent with that structure;
- lint, SV idiom and port-contract gates pass.

`[R329] PASS Robustness - sim_main.cpp:1459-1469 @867a2e38; receipts/r328_2_multirec_probe/*; receipts/r328_2_dp_mutants/* - checked:`
- the invalid-ordering, partial-validation abort path in both map directions, from a durable reset baseline: status 7, no storage change, pending clear through the abort;
- the round-2 malformed, duplicate, REMOVE, zero-record, reset and static/dynamic configuration controls retained (my probe P1-P3 identical to round 2).

`[R329] PASS Tests - sim_main.cpp:1459-1469; tb/verilator/pp_shadow/README.md:91-94; receipts/mutant-campaign.txt; receipts/r328_2_dp_mutants/fails/P4_no_phase5.*.fails.txt @867a2e38 - checked:`
- P4 is killed in both legs only by the named `K12 partial refusal * sticky_pending_*` checks;
- the new control can fail for its defect: it failed on P4 and passes on shipping;
- the mutant campaigns were re-executed: R328's 9 datapath mutants x 2 legs; my unchanged script (control, M3 and M7 run in 2 legs; 8 anchor refusals); the adapter (13 mutants x 2 legs); and the parent-side D1-D3 x 2 legs. Every observable mutant is killed. The survivors are the stated equivalence controls, P5 (unreachable divergence) and static-leg runs lacking a dynamic output;
- the default suite and pending-mutant pass;
- my probe and R328's probe give their expected results unchanged.

The Docs lens is UNCLEAN (R329-3-F1). Clean within Docs:
- `CHANGELOG.md:39-40`;
- `SUBMODULES.md:61`;
- `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1263,1738-1742`;
- `pp_shadow/README.md:91-94`;
- the PR body;
- all docs gates, in git and no-git modes.

## Completion ledger (reviewer-owned)

| lens | status | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | assignment 5854008765 items 1-4; decision 5848417938; `CHANGELOG.md:37-44`; `SUBMODULES.md:57-62`; `milan_datapath.sv:4269-4271`; `KL_pp_shadow.sv:388,945-946`; pp_shadow default receipt; PR body | R329-3 | 867a2e38a4e3231545a0a24b97d1e5612a6659fe |
| RTL | CLEAN | `receipts/scope-raw.log` (no RTL delta since R329-2's full RTL coverage at 5d4cf33e); `milan_datapath.sv:4054-4090,4246-4271,4316-4400`; shipping hashes across mutants; lint/idiom/port gates | R329-3 (delta), R329-2 (full; ancestor untouched in RTL scope) | 867a2e38a4e3231545a0a24b97d1e5612a6659fe |
| Robustness | CLEAN | `sim_main.cpp:1442-1498`; multirec probe shipping/P4/P5; probe P1-P3 shipping and 4 mutants | R329-3 | 867a2e38a4e3231545a0a24b97d1e5612a6659fe |
| Tests | CLEAN | `sim_main.cpp:1459-1469`; README:91-94; R328 dp mutants (18 legs); r329 campaign (unchanged, adapter, parent-side); multirec probe (3 runs); r329 probe (5 runs); pp_shadow default and pending-mutant | R329-3 | 867a2e38a4e3231545a0a24b97d1e5612a6659fe |
| Docs | UNCLEAN (R329-3-F1) | `CHANGELOG.md:35-46`; `SUBMODULES.md:45-70`; `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:955-971,1255-1272,1374-1384,1730-1744`; `SAVED_STATE_MATERIALIZATION.md:125-146,205-250,1650-1700,1717,2024-2090`; `pp_shadow/README.md:51-96`; PR #579 body; gates (git and no-git) | R329-3 | 867a2e38a4e3231545a0a24b97d1e5612a6659fe |

## Prior findings: closed or retained at this head

| finding | state | evidence at 867a2e38 |
|---|---|---|
| R329-2-F1 (MINOR, Docs; CHANGELOG:39 superseded trigger) | CLOSED | `CHANGELOG.md:39-40` states the actual parent phase-5 write and that unchanged records raise nothing |
| R329-2-S1 (SUGGESTION, Docs; stale PR-body publication sentence) | CLOSED | the sentence is absent from the live body; the Status line names round 3 at the exact head |
| R328-2 F1 (MINOR, Docs; CHANGELOG:39 and SUBMODULES:61) | CLOSED | both lines as in (1) |
| R328-2 S1 (SUGGESTION, Tests/Robustness; P4 survived) | CLOSED | committed `K12 partial refusal input/output`; P4 KILLED static 2 / dynamic 4 by those named checks; unchanged probe agrees |
| R328-2 S2 (SUGGESTION, Docs; PR body and OWNERSHIP:1263 wording) | CLOSED | `:1263` reads "first actual write"; PR body as above |
| Round-1 findings (R329-1 F1-F3, R328-1 F1-F3, S1-S2) | remain CLOSED | as at round 2; every M, U and D mutant tied to them is still killed by the same named checks (`receipts/mutant-campaign.txt`) |

The open set at this head is MINOR R329-3-F1 and SUGGESTION R329-3-S1.

## Real limits

- **Simulator path.** The assigned `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist. I used a private copy of the identical wrapper (sha256 `905795b9...`) from `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator`. It reports `Verilator 5.050 2026-07-01 rev v5.050`, `verilator_bin` sha256 `44898b22...` (`receipts/tool-identity.txt`). This is the same identity as round 2.
- **Driver.** My round-2 campaign driver ran with its lists unchanged but its parallelism raised from 4 to 8 (`scripts/r329_3_campaign.sh`). The per-mutant scripts are byte-identical.
- **Not run:**
  - the full parent/PP/gPTP/Yosys/builder banks and the default 55-suite sweep;
  - OOC synthesis and the `milan_dp` differential (no RTL delta);
  - nvm_backend, nvm_cosim and behave;
  - act/Docker and the hosted contexts.
- **P5 unreachability** is argued from the datapath's claim lifecycle. I did not prove it against the processor microcode.
- **Hosted snapshot** (`receipts/hosted-snapshot.txt`, 08:30Z): executed and passed: `rtl-fast`, `elaborate`, `yosys-elaboration`, `verilator-lint`, `bdd-conformance`, `changes`, `docs-check-no-git`, `wire-accountability`, `full-ci-gate`, Yosys shards 0-3 and Verilator shards 0 and 3. Pending: Verilator shards 1, 2 and 4, and `docs-check`. Physical gPTP was skipped, which is not hardware proof. Hosted acceptance is the manager's.
- **Hardware.** No hardware or physical calibration was run.
- **Receipt redaction.** Container-store and home paths in receipts are redacted to `<container-store>`/`<home>`.

## Clone integrity

- All builds, mutants, probes and gates ran in disposable copies under the packet's `scratch/`. The review clone was never edited.
- `scripts/r329_3_restore_check.sh` (`receipts/restore-check-pre.log` and `receipts/restore-check-post.log`) reports RESULT OK both before and after the probes:
  - HEAD `867a2e38...` and tree `d0c5cc45...` are exact;
  - index equals HEAD and the worktree equals the index;
  - there are 0 untracked or ignored entries;
  - every tracked blob rehashes to its index id;
  - the gitlinks `protocol-processor@870ff88a`, `gptp-processor@5dce647a` and `third_party/verilog-axis@48ff7a7e` are recorded, checked out and clean.

## Pending manager duties

- Route R329-3-F1 (one UNRESOLVED item in `SAVED_STATE_MATERIALIZATION.md`; optionally S1) to the executor. The re-review at the corrected head must re-cover Docs.
- If only that page changes, nothing within the Conformance, RTL, Robustness or Tests scope is touched. Those four lenses covered CLEAN here then remain banked at `867a2e38` for a head descending from it.
- Hosted acceptance at the exact head, including the pending Verilator shards and `docs-check`. The act replica.
- The current-dev candidate merge (source base `831f94f4`, live dev `e0920d77`) and post-merge containment.
- Maintainer merge authorization.

R329-3 FINISHED
