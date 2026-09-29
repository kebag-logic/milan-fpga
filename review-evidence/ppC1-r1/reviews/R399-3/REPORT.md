[R399] NEGATIVE - exact head 99bfd4bc3180bab97d47f63056513fb39eea6a37

# R399-3: external independent composition review of processor PR #133 (lane C1) after the merge of PR #132

- **Repository:** Mister-M-alt/protocol-processor-control-plane-avb-milan
- **Scope:** issue #108, PR #133
- **Exact head:** `99bfd4bc3180bab97d47f63056513fb39eea6a37`, tree `d8ec1053bf0968ed462d8a419a0cf859c41e9c3c`
- **What the head is:** the merge of processor `main` `d352bbaa` (PR #132, D3 lane 1) into `412efeb7`. R398-2 and R399-2 were POSITIVE at `412efeb7`.
- **Source base:** `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`

**Verdict basis.**
- One MINOR is open, F1 (Docs): PR #133's parent-visible list does not yet read together with #132's consolidated list at this composed head. Two of its statements are false with the gitlink at this head.
- Everything else about the composition is clean:
  - The merge is mechanical: a fresh merge of the two parents gives this exact tree.
  - Neither lane's top-level wiring touches the other's.
  - Both lanes' contracts appear in 08 and the integrator guide without contradiction.
  - Every suite, gate and mutation campaign I ran passes on the merged tree.
  - A full-top probe shows that C1's LeaveAll restart holds while #132's D3 writer holds AECP under a command flood.
- There is one new SUGGESTION of my own (S1). Three SUGGESTIONs from round 2 are retained. No SUGGESTION blocks.
- The verdict and ledger were fixed before I read any prior review (`receipts/pre_read_verdict.md`).

## 1. Reconstruction (what was read, in order)

1. **Governance.** The processor repository has no `AGENTS.md` or `CONTRIBUTING.md`, and no submodules. I read `README.md`, `docs/README.md` (single-source rules: timing only in F08.1, parameters only in F01.5) and the `Makefile` gates.
2. **Issue #108.**
   - The body (acceptance 1-3).
   - Manager assignment 5883702094 (items 1-4; item 4: a parent-visible list in the PR body, "even if empty").
   - Round-2 assignment 5886235840.
   - Author TAKEN / REVIEW READY notes.
3. **PR #133 body.** Rounds 1 and 2; section 4 is the parent-visible list. The body does not mention #132, `d352bba` or the merge.
4. **PR #132 body.** Rounds 1-6, with its "Parent-visible for pin adoption: rounds 1-6, consolidated" list, merged as `d352bbaa`.
5. **Manager comments on PR #133.** These are the review-start notices only. No manager evidence comment exists at this head.
6. **Diff and history.**
   - `git diff c951a9ff..99bfd4bc`, split by lane: `c951a9ff..412efeb7` (C1, 43 files) and `c951a9ff..d352bbaa` (#132, 52 files).
   - The merge commit (parents `412efeb7`, `d352bbaa`, message "Merge main into c1-srp-mrp-timers").
7. **Public evidence.**
   - `kebag-logic/milan-fpga` `a6427910…/review-evidence/ppC1-r1` holds the round-1 author packet only (`HANDOFF.md`, `PR-BODY.md`). Nothing public records the manager's source banks at this head.
   - The hosted checks at the exact head, read-only (section 6).
8. **Prior public reviews on PR #133.** R398-1, R399-1, R398-2 and R399-2, read only after `receipts/pre_read_verdict.md` was written (section 5).

## 2. Composition judgement

### 2.1 The merge is mechanical

All of the following are in `receipts/composition_check.txt` (script `scripts/composition_check.sh`):
- `git merge-tree --write-tree 412efeb7 d352bbaa` gives `d8ec1053…`, the head tree. There is no manual resolution and no extra edit.
- Every C1-only file equals `412efeb7`, and every #132-only file equals `d352bbaa`.
- Three files are touched by both lanes: `hdl/top/protocol_processor_top.sv`, `docs/architecture/08_timing.md` and `docs/guides/integrator.md`.
- The HDL sets are disjoint apart from the top. C1 changes `hdl/srp/*` only, and #132 changes `hdl/acmp`, `hdl/adp`, `hdl/aecp`, `hdl/packet_engine`. C1's only change to the top is one port comment.

### 2.2 The top-level wiring: no interference

**Ports and parameters.** `protocol_processor_top.sv` at the head equals #132's file plus C1's comment on `srp_active_o` (`hdl/top/protocol_processor_top.sv:580-581`). So:
- the head's ports and parameters are exactly #132's (for example `restore_closed_o` `:479`, `NVM_RS_AGG_CYC_P` `:146`);
- C1 adds none.

**Shared services.** These four instances are byte-identical at base, C1, #132 and head:
- `KL_pp_timer_service` (`:859`), the arm-port priority mux;
- `KL_pp_prng` (`:938`), the draw-port owner mux;
- `KL_pp_tx_arbiter` (`:4227`);
- `KL_srp_top` (`:2311`).

The 65 lines naming an arm are also identical in all four. The shared TX arbiter slots, the arm queue and its priorities, and the draw ports are therefore unchanged.

**Nets.**
- No line of #132's top diff names an SRP, MRP, arm, draw or TX net.
- `KL_aecp_nvm_writer` has no arm, draw or TX port. It counts its own deadlines from `tick_ms` and clocks (F08.1 rows at `08_timing.md:43-46`, "not a timer-service slot").

**The RX side.** #132's AECP hold admission (`:2666`, `KL_pp_rx_validator.sv:281`) drops only AVTP subtype `0xFB` at the slot gate. The MRP pass-through (`KL_pp_rx_validator.sv:104`, `:686`) is untouched, so the peer LeaveAll that drives C1's rLA! reaches `KL_srp_top` whatever the hold does.

**C1's items.**
- **The re-arm guard** (`hdl/srp/KL_srp_top.sv:1028-1033`) reads only `now_ms_i`, `cad_dl_r` and the draw state. It does not depend on the arm-path latency, and #132 adds nothing to that path.
- **`tx_mvrp_o` to the VLAN table and the licence term** are internal to `KL_srp_top`, whose instance is identical.
- **The ADP enable gate** (`:1704`, `entity_enable_i && restore_done_o`) and the D3 start (`:3622`, `.d3_go_i(lsn_released_w)`) feed nothing in the SRP engine. The engine has no enable or restore input.

**Dynamic evidence.**
- **`tb/pp_top` at the head** (C1's RTL under #132's bench): 7888/7888, including `D3: 133 checks, 0 failures` and the ADP + ACMP + SRP TX interleave sections (`receipts/suites/pp_top.log`).
- **A full-top probe** of my own (`scripts/probe/`, `receipts/probe/`), with peer MSRP LeaveAlls every 1 s for 30 s and an AECP READ_DESCRIPTOR every 100 ms throughout:

| Case | Own MSRP LeaveAll inside the peer window | Next own LeaveAll after the last peer | AECP |
|---|---|---|---|
| Head, D3 holding AECP (no restore) | 0 | +14,809 ms | held at the end, 0 responses, snapshot word 37 = 299 drops (one record resident) |
| Head, booted (both walks done) | 0 | +14,196 ms | released, 300 responses |
| `expiry-only-redraw` planted (C1's own mutant) | held: 0, booted: 1 | +6,409 / +6,396 ms | as above; 3 of 12 checks fail |

This grades C1's Table 10-5 rLA! restart at the full top in both states of #132's hold. The mutant shows that the probe is sensitive at the top.

### 2.3 The two shared documents

**`docs/architecture/08_timing.md`.**
- C1's F08.1 `T-MRP-LEAVEALL` row (`:41`, three starts: Begin!, own expiry and rLA!) and #132's rows are distinct rows of the one F08.1 table. #132's rows are `T-NVM-DEBOUNCE`, `-RS-DEADLINE`, `-RS-AGGREGATE` and `-RETRY-BACKOFF` (`:43-46`).
- #132's §2 "saved-state times" block (`:54`) and its §3 note that persistence takes no timer slot (`:166`) leave the MRP slot budget as it was.
- There is no contradiction, and the single-source rule holds (make check `matrix`, `links`, `params` pass).

**`docs/guides/integrator.md`.**
- C1's `srp_active_o` row (`:344`, the Milan 4.3.2 term, linking 10 §6.2) and #132's NVM rows and bring-up order (`:379-444`) state separate contracts.
- The bring-up order gates ADP and AECP on the restore and says nothing about the SRP licence. The licence row says nothing about the restore. Both match the RTL above.

### 2.4 Every processor suite and entry point on the merge head

All of the following passed on an exported copy of the head:

| What | Result | Receipt |
|---|---|---|
| The 14 suites whose inputs changed from base (`make -n` input map; only `pp_top` compiles both lanes) | all rc 0. `pp_top` 7888, `srp_top` 2200, `srp_encoder` 581, `srp_stream_fsms` 1219, `acmp_nvm` 360, `rx_validator` 437, `dyn_state` 118, `desc_mem_guard` 78, `desc_store` 584, `adp_engine` 533, `lsn_admit` 18, `nvm_port` 136, `ucpu` 386, `timer_map` 1360 | `receipts/suites/`, `receipts/suite_input_map.txt` |
| `scripts/check_upc_map.py` | PASS (56 constants, 80 entry points) | `receipts/check_upc_map.log` |
| `tb/pp_top/d3_mutants.py --jobs 8` | 83 of 83 KILLED by their named checks, goldens PASS, rc 0. Every edit applied exactly once to the merged top | `receipts/d3_mutants.log` |
| `tb/srp_top/mutants.py`, in 8 `--only` shards | all 78 entries KILLED, every control PASS, assertion coverage 65/65 (union of the killed tags) | `receipts/srp_top_mutants_summary.txt`, `receipts/srp_top_mutants/` |
| `make check` | rc 0 (41 mermaid + 18 wavedrom, 976 links, both matrices, parameters 26/26/26, stale) | `receipts/make_check.log` |
| `scripts/lint_hdl.sh` | rc 0, 41 modules | `receipts/lint_hdl.log` |
| `scripts/gen_matrix.py --check` | rc 0 | `receipts/gen_matrix.log` |
| `git diff --check` from `c951a9ff` and from `d352bbaa` to the head | rc 0 | `receipts/diff_check.log` |

The hosted `hdl` workflow at the exact head (push and pull_request runs) covered the rest. It ran all 33 suites (1,016,272 checks, 0 failing, identical per-suite counts to mine), the SRP LeaveAll campaign (90/90, coverage 65/65), the matrix, the `nvm_port` figures, the docs gates and the off-vendor Yosys elaboration of every top. Section 6 has the detail.

I did not run `d3_mutants.py` on the hosted side because CI does not include it; my local run covers it. Tool: Verilator 5.050, the same binary as the manager's pinned wrappers (`receipts/tool_identity.txt`; see section 8 for the path).

### 2.5 The parent-visible lists, read together: F1

At milan-fpga dev `79c36963` (`receipts/parent_pin_79c36963.txt`):
- The processor gitlink is still `c951a9ff`.
- C1's cited lines are unchanged: `sim_crf_licence.cpp:953,956` (`>= 4`) and `milan_dp/README.md:443`, `:528-530`, with blobs `6f9d17b1` and `3f05559f`, identical to `57b8c867`.
- None of #132's parent edits is present:
  - `KL_pp_shadow.sv` names none of `restore_closed_o`, `restore_rb_o`, `rs_cause_o`, `restore_cause_o`, `d3_unflushed_o`, `NVM_RS_AGG_CYC_P` or `NVM_RETRY_BACKOFF_CYC_P`;
  - `nvm_cosim/cosim_top.sv` has no `rs_agg_i`, `wr_chg` or `RETRY_BACKOFF_CYC_P`;
  - `sim_gmstep.cpp` never starts the restore walk.

Moving the gitlink to this head therefore needs #132's consolidated list plus C1's section 4. PR #133's body does not say so, which is F1. The two lists do not collide on a parent file: C1 edits `sim_crf_licence.cpp` and `milan_dp/README.md`, and #132 edits neither.

## 3. Findings

### F1: MINOR. Lens: Docs

**Summary.** At this composed head, PR #133's parent-visible list is contradicted by #132's consolidated list, and the body never points to it.

**Where.**
- PR #133 body, "## 4. Parent-visible, for the pin-adoption lane" (as amended by "## Round 2"). The bullets are "One consumer-gate expectation to re-base" and "Every other consumer command is rc 0 as is (table below)".
- The body names neither #132 nor the merge.

**Authority.**
- #108 assignment 5883702094, item 4: the parent-visible list for the pin-adoption lane, in the PR body.
- The round-3 brief: this list "must now read together with #132's consolidated list (#132's harness and cosim edits plus C1's crflic LeaveAll count)".
- PR #132's "Parent-visible for pin adoption: rounds 1-6, consolidated" list: gitlink-only, `pp_shadow`, the evidence classifier, `nvm_cosim`, `milan_dp` `gmstep`/`gptp` and `milan_dp_render` T8 fail until its edits are applied.

**Evidence.**
- `receipts/parent_pin_79c36963.txt`: at live dev `79c36963` none of #132's connections or harness edits exists.
- With the gitlink at `99bfd4bc`, "every other consumer command is rc 0 as is" is false.
- "One consumer-gate expectation to re-base" understates the edits needed.

**Impact.**
- A pin-adoption lane reading PR #133 at the head it lands would apply only the crflic edit and meet #132's failures unexplained.
- Read literally at this head, the section's "no port, parameter or register ... changes" also reads against #132's five ports, three parameters and snapshot word 37, because nothing scopes it to C1's commits.

**Required outcome.** Add a composed-head note to the PR body (no source change) that:
1. states that the pin-adoption edits at this head are #132's consolidated list (rounds 1-6) plus C1's section 4 (crflic `>= 3` at `sim_crf_licence.cpp:953,956`, the `milan_dp/README.md` `[C]` row and "What it cannot show", and the parent documents);
2. scopes "rc 0 as is", "one expectation to re-base" and "no interface change" to C1's own commits (`412efeb7` against `c951a9ff`);
3. records the manager's combined-edit parent bank result at dev `79c36963` once it has run, or points to it.

**Verification.** Re-read the PR body at this head. The combined list is named, the scoped statements no longer contradict #132's list, and the manager's combined 16-command run at `79c36963` is referenced.

### S1: SUGGESTION (new). Lens: Tests

**Summary.** No in-tree check grades C1 at the full top under #132's hold.

**Where.** `tb/pp_top/pp_top_wrap.sv` leaves `srp_active_o` and the SRP status outputs unconnected (PINMISSING in `receipts/suites/pp_top.log`). No `pp_top` section runs a peer LeaveAll through the top while the D3 writer holds AECP.

**Impact.**
- Non-interference rests on the byte-identical instances and nets (section 2.2), `pp_top`'s TX interleave, and this packet's out-of-tree probe.
- A future edit that gated the SRP engine on the restore would pass the tree.

**Suggested outcome.** Commit the probe's two cases (held and booted, with the flood) as a `pp_top` section, with `expiry-only-redraw` in `d3_mutants.py` or the `srp_top` campaign as its control.

**Verification.** At the head the section is green, and the planted re-draw fails it (as in `receipts/probe/expiry-only-redraw.run.log`).

## 4. Prior public review findings at this head

| Finding | State at `99bfd4bc` | Evidence |
|---|---|---|
| R398-1 F1 (MINOR, Docs): the list omits `tb/verilator/milan_dp/README.md` | RESOLVED (as at `412efeb7`) | PR body section 4 names the file, `:443` and `:528-530`; blob `3f05559f` unchanged at `79c36963` (`receipts/parent_pin_79c36963.txt`) |
| R398-1 S1 = R399-1 S2 (VLAN overflow, licence bound) | RESOLVED | docs 10 §6.2 unchanged since `412efeb7` (C1-only file equal to `412efeb7`) |
| R398-1 S2 (three narrow guards unexercised) | RESOLVED | `r-rearm-no-inflight`, `r-rearm-no-deadline` and `r-flag-ignores-edge-peer` KILLED here (M10, P6, P8, P7) (`receipts/srp_top_mutants/`) |
| R398-1 S3 (integrator ordering assumption) | RESOLVED | docs 10 §6.2; `integrator.md:344` links to it |
| R399-1 S1 (latency-dependent guard) | RESOLVED | `KL_srp_top.sv:1028-1033`; `rearm-at-issue` KILLED by P8 here |
| R399-1 S3 (per-type aging caveat) | RESOLVED | docs 10 §6.5 unchanged since `412efeb7` |
| R398-2 S1 = R399-2 S1 (a dropped LeaveAll re-arm silences that application's own LeaveAll until the next rLA! or reset) | RETAINED, SUGGESTION | `KL_srp_top.sv` unchanged. The exposure is unchanged by the merge: arm queue and arm lines identical, and #132 adds no arm client (`receipts/composition_check.txt`) |
| R398-2 S2 = R399-2 S2 (no committed check across a `now_ms` wrap) | RETAINED, SUGGESTION | `tb/srp_top` unchanged since `412efeb7` |
| R399-2 S3 (superseded mutant counts in `tb/srp_top/README.md` tables) | RETAINED, SUGGESTION | README unchanged since `412efeb7` |

No MINOR or higher finding from an earlier round is open. F1 is new: the merge created it.

## 5. Lens results

**Conformance: CLEAN.**
- The rLA! row of 802.1Q-2014 Table 10-5 ("Start leavealltimer, Passive"), with the per-application scoping of 10.7.5.20 as #106 applies it, is unchanged from `412efeb7`: `KL_srp_top.sv:1028-1033` and `:1233-1241`.
- It is graded at the full top in both hold states by the probe, and by `srp_top` P1-P8 and Q1-Q4.
- Milan Table 4.3 grading (Q1-Q4) and the Milan 4.3.2 licence term (R1-R4) pass.
- #132's hold changes nothing on the MRP path.

**RTL: CLEAN.**
- The merge is mechanical.
- The top's shared-service instances and the `KL_srp_top` instance are byte-identical across all four revisions.
- #132's top diff names no SRP net, and the D3 writer has no shared-service port.
- The only line either lane changed in the other's region is C1's port comment.
- `lint_hdl` is clean (41 modules), and the hosted Yosys elaboration passes.

**Robustness: CLEAN.**
- An AECP flood during the hold (299 dropped and counted, one resident record) leaves the restart intact.
- The booted case behaves the same.
- The retained S1 on the dropped re-arm is unchanged in exposure.

**Tests: CLEAN (S1 new; round-2 S2 retained; both SUGGESTIONs).**
- `pp_top` 7888 with D3 133.
- D3 campaign 83/83; `srp_top` campaign 78/78 with coverage 65/65.
- The probe control kills C1's mutant at the top.
- Hosted: all 33 suites.

**Docs: UNCLEAN (F1).**
- 08 and the integrator guide compose correctly.
- The PR body's parent-visible list does not yet read together with #132's.

## 6. Hosted checks at the exact head (read-only; the manager owns acceptance)

Runs: `hdl` pull_request 36558392722 and push 36558385720 on `99bfd4bc`, both success (`receipts/hosted_checks.txt`, `receipts/hosted_suites_tallies.txt`).

| Job | Steps |
|---|---|
| `suites` | lint and every suite; SRP LeaveAll mutation campaign; matrix; `nvm_port` figures. All executed. The one skipped step is "Build Verilator v5.050", skipped on a cache hit. Result: 33 suites, 1,016,272 checks, 0 failing; campaign 90 checks, coverage 65/65 |
| `docs-gates` | executed |
| `portability` | Yosys + sv2v elaboration of every top, executed |

The combined status API reports "pending" with no status contexts; the check runs are the executed evidence.

## 7. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_srp_top.sv:1028-1033,1233-1241`; `KL_pp_rx_validator.sv:104,281,686`; `srp_top` P1-P8, Q1-Q4, R1-R4 logs; full-top probe (held and booted) | R399-3 | 99bfd4bc3180bab97d47f63056513fb39eea6a37 |
| RTL | CLEAN | merge-tree recomputation; `protocol_processor_top.sv` at base, C1, #132 and head (instances `:859`, `:938`, `:2311`, `:4227`; the comment `:580-581`; `:1704`, `:2666`, `:3622`); `KL_aecp_nvm_writer.sv` ports; `lint_hdl` | R399-3 | 99bfd4bc3180bab97d47f63056513fb39eea6a37 |
| Robustness | CLEAN | probe with a 300-frame AECP flood in hold (word 37 = 299) and booted; arm-queue identity for the retained S1 | R399-3 | 99bfd4bc3180bab97d47f63056513fb39eea6a37 |
| Tests | CLEAN (SUGGESTIONs only) | 14 input-changed suites; `d3_mutants.py` 83/83; `srp_top` mutants 78/78, 65/65; probe control; hosted 33 suites | R399-3 | 99bfd4bc3180bab97d47f63056513fb39eea6a37 |
| Docs | UNCLEAN (F1) | `08_timing.md:41,43-46,54,166`; `integrator.md:344,379-444`; `make check`; PR #133 body section 4 and Round 2; PR #132 consolidated list; parent files at `79c36963` | R399-3 | 99bfd4bc3180bab97d47f63056513fb39eea6a37 |

## 8. Real limits

**Not run by this review:**
- the parent consumer bank, the donor full bank, and the gPTP, Yosys and builder banks;
- `run_suites.sh` in full (I ran the 14 suites whose inputs changed; the hosted run covers all 33);
- act, hardware and physical calibration. Physical calibration was NOT RUN, and field skips are not hardware proof.

**Tool path.** The brief's named Verilator wrapper (the `372-manager-candidate1` pinned tool directory) does not exist on this host. I used a wrapper of my own in scratch. It points at the same 5.050 binary as every one of the 198 manager `pinned-tool-bin/verilator` wrappers present, and I verified its version and sha256 (`receipts/tool_identity.txt`).

**Manager bank evidence.** The brief's public evidence tree (`a6427910…/review-evidence/ppC1-r1`) holds only the round-1 author packet. It contains no receipt of the manager's source static/builder and native banks at this head, so that claim is not verified here. The hosted run at the head is the public executable evidence I could inspect.

**Parent files.** I read them via the public API at `79c36963`; no parent build was run. I did not verify that the combined edits apply cleanly at `79c36963`. Between #132's measured pin `eaa88a32` and `79c36963`:
- `tb/verilator/milan_dp/sim_nxn.cpp` changed in one comment (`:7871`);
- `milan_dp/Makefile` changed (the `ax1x1gptp` clock recipe);
- `nvm_cosim/cosim_host.c` and `nvm_cosim/run_cases.py` changed.

None of these overlaps the declared edit points as far as I read them.

**Probe scope.** The probe is an out-of-tree `pp_top` harness addition. It covers MSRP only: the MVRP restart needs a held VID and is graded by `srp_top` P2, P3 and P6.

**Standards text.** The 802.1Q and Milan PDFs are not distributed. Clause wording is as quoted in the issue and the tree.

## 9. Pending manager duties

1. **F1:** amend the PR #133 body as required, then a delta check of the body.
2. **The parent consumer bank** (the 16 commands) and **the donor full bank** at milan-fpga dev `79c36963`, with the combined declared edits applied: #132's consolidated list (harness, `pp_shadow`, `nvm_cosim`, `milan_dp_render` T8, evidence-classifier line) plus C1's crflic `>= 3` at `sim_crf_licence.cpp:953,956`. Attribute each failure.
3. **The final current-dev candidate** at the merge turn (source base `c951a9ff`, live dev `79c36963`) and hosted/act acceptance.
4. **At pin adoption:** the parent documents of both lists, including `tb/verilator/milan_dp/README.md:443,528-530` and #132's firmware boot-path obligation.
5. **Follow-ups carried from the author and round 2:**
   - the re-DECLARE_TALKER VLAN refcount leak;
   - the re-issue option for a stale LeaveAll expiry (retained S1);
   - the wrap check (retained S2);
   - the README count cells (retained S3);
   - S1 here.

## 10. Packet

- `scripts/` holds the portable drivers:
  - `run_suite_subset.sh`
  - `srp_mutants_sharded.sh`
  - `srp_mutants_account.py`
  - `composition_check.sh`
  - `parent_pin_check.sh`
  - `probe/r399_probe.hpp`
  - `probe/make_probe_tree.sh`
- `receipts/` holds the raw logs, with host paths replaced by placeholders.
- `MANIFEST.sha256` lists every published file.
- Disposable trees stayed under `scratch/`.
- The clone at the head is byte-exact: 329 blobs re-hashed, 0 differing; index equals HEAD; no gitlinks exist (`receipts/clone_integrity.txt`).

R399-3 FINISHED
