[R407] POSITIVE - exact head 20ec92b7b190d03c46e40be89d236bc9a0702a59

# R407-2: external independent review of PR #136 (lane C3, ADP), round 2

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #136, issue #40 (round-2 assignment: #40 comment 5893098818).
- Exact head `20ec92b7b190d03c46e40be89d236bc9a0702a59`, tree `a3d4eb5a6e6b8bf770b683d9ab5bd71a916dab6d`, reviewed in an isolated detached clone.
- Diff judged: `b2db3a970cedbbff2f8ba813acb96122c442bc58..20ec92b7`, plus the merge `cae0988` (parents `9185c49`, `b2db3a9`) and the four round-2 commits `9c9431a`, `c9f915e`, `b27e038`, `20ec92b`.
- Verdict: **POSITIVE**. There is no open BLOCKER, MAJOR or MINOR finding. Five SUGGESTIONs are retained (section 5). None of them affects the verdict.

## 1. Reconstruction

- **Repository rules.** The repository has no `AGENTS.md` or `CONTRIBUTING.md`, and no `.gitmodules`. I read `README.md`, `docs/README.md` (conventions and single-source rules), `.github/workflows/hdl.yml`, and the `tb/pp_top` and `tb/adp_engine` READMEs.
- **Scope decisions.** I read the #40 body (frozen acceptance 1-4) and every #40 comment:
  - the lane assignment 5888002660;
  - the round-2 assignment 5893098818, with items 1-3 and its gates;
  - the TAKEN and REVIEW READY markers.
- **The PR.** I read the PR body, including its Round 2 section and the round-2 parent-visible list. It is identical to the published `author-r2/PR-BODY.md` apart from the author tag line.
- **Evidence branch.** At milan-fpga `c2424a31`, `review-evidence/ppC3-r1/author-r2/` holds `HANDOFF.md` and `parent-adaptation-132-c1.patch`. The patch's sha256 is `2ba66803…c420`, as the handoff states. It touches 13 parent files, all #132/C1 harness and shadow edits, and none of them is this lane's.
- **Order of reading.** I read the other reviewer's round-1 report (R406-1, PR comment 5892168191) only after my verdict and ledger were fixed: `receipts/verdict_and_ledger_before_prior_findings.md`, timestamped 04:42:55Z. My own role's round-1 report (R407-1) was read after my independent pass over the diff.

## 2. Round-2 questions

### (1) The merge resolution: is the flag exactly the store's flag in every case?

**Mechanics.**
- A fresh `git merge-tree 9185c49 b2db3a97` conflicts in exactly `hdl/aecp/KL_aecp_engine.sv` and `tb/pp_top/sim_main.cpp`.
- `git diff <re-merge tree> cae0988` touches only the conflict regions of those two files. Every other file in the merge commit is git's own auto-merge.

**`KL_aecp_engine.sv`.**
- Main's `u_dyn_didx_w`/`dyn_didx_w` (`:1782-1785`) replace the branch's `dyn_ix_w`.
- The flag block `dyn_cfg_valid` (`:1803-1814`) decodes `st_req_w && dyn_sel_w && st_we_w && st_addr_w[19:16]==RGN_DYN_C && st_addr_w[15:3]==0 && dyn_didx_w==0`. Every one of those signals is taken after the D3 writer's 2:1 selection (`:1554-1557`, `:1597-1599`). The flag resets on `store_rst_n_w = rst_n && !d3_rb_rst_w` (`:1545`, `:1804`).
- The store is `KL_aecp_dyn_state`, instantiated at `:1817-1839` with:
  - `.rst_n(store_rst_n_w)`;
  - `.st_req_i(st_req_w && dyn_sel_w)`;
  - `.st_we_i(st_we_w)`;
  - `.st_addr_i(st_addr_w)`;
  - `.desc_index_i(dyn_didx_w)`.
- The store's set term is `take_wr_w = st_req_i && st_we_i && region==RGN_DYN && in_range_w` (`KL_aecp_dyn_state.sv:266`), with `in_range_w = desc_index_i < 1` for selector 0 (`:206`, `:218`). It sets `cfg_v_r` at `:329-330` and clears it only under `rst_n` (`:291-292`).
- Term by term, the two flops share the same clock, the same set condition (`didx < 1` is `didx == 0`) and the same reset. The flag is therefore the store's flag by construction.

**`sim_main.cpp` `main()`.** The resolution keeps main's section order (Suite, GSI, name writes, D3) and main's `--dr3a` early return. It adds `--adp-only` with a single `one_section` flag and runs AD last. Every mode selects the same sections as on main, plus AD.

**Executed equivalence, beyond the suite's own windows.**
- `scripts/flag_equivalence_probe.sh` exports the exact head and adds a monitor inside the engine that compares `dyn_cfg_v_r` with `u_dyn.cfg_v_r` in every clock. It then runs the full default `tb/pp_top` (7,924 + 20 checks).
- Result: 0 mismatches, all checks pass, rc 0 (`receipts/probe-head.log`).
- Every way the flag can move was exercised: 15 µCPU writes of the configuration row, 16 writer (restore) writes, 8 hard resets and 10 roll-backs with the flag set.
- The refused SETs in the same run (W18d `0xFFFF`, W18d2 the count boundary, `sim_main.cpp:7444,7451`) and W18g (the row left unchanged) pass with no split.
- Positive control: the same probe with `cfg-valid-hard-reset` planted reports 20 mismatch lines and AD fails 2 (`receipts/probe-ctl-hard-reset.log`), so the monitor can see a split.

The case list the assignment names therefore holds: reset, roll-back, restore, a µCPU SET and a refused SET.

**The writer in service.** In service the writer never writes the store: `sb_we_o = !done_r && (ws_r == W_APPLY)` (`KL_aecp_nvm_writer.sv:1084`). Its service ownership is a one-cycle latch read.

### (2) The restore path, AD5 and AD6

**The path in the RTL.**
- Record 0x00 maps to selector 0, row 0 (`KL_aecp_nvm_writer.sv:99`, `:459-460`).
- The pass-1 rule is W_NCFG: the value must be below `configurations_count`, read from region 0xD (`:616`, `:734`, `:831-834`).
- W_APPLY then drives `{RGN_DYN_C, sel 0}` with `sb_didx_o = ridx_w = 0` while `bus_o` holds the bus (`:845-848`, `:1078`, `:1084-1087`).
- ADP is released only by `restore_done_o` (`protocol_processor_top.sv:1708-1709`), and the ADPDU index selection is `protocol_processor_top.sv:1723`.

**AD5, the restored configuration** (`tb/pp_top/sim_main.cpp:10216`).
- SET(0) is saved. Premise: the device bytes equal `d3_record(0x00, 0, 2)`.
- A power cycle keeps the device. The first ENTITY_AVAILABLE is byte-exact at 0, and GET_CONFIGURATION and ENTITY.current_configuration also read 0 (the image default is 1).
- The flag equals the store's in every clock from the reset to that advert. The store side is the tap `pp_top_wrap.sv:721`; the published side is `:722`, which reads `u_dut.aecp_cur_cfg_v_w`, the wire the ADPDU mux reads.

**AD6, the roll-back** (`:10241`).
- The restore applies record 0x00. Record 0x50 is read whole in pass 0 and erased before pass 1, which aborts with cause 5.
- Premises: `applied`, `erased`, `restore_rb_o`, and the row unset.
- All three views then carry 1, with no split.

Both arms pass: AD is 55/55 alone, and 7,944/7,944 in the full suite.

### (3) R406-1 F-1: AD7 and the three new mutants

**AD7** (`:10271`) does a SUCCESS SET(0) and then a reset onto an erased device. Premises: `restore_blank_o` and the row unset. All three views carry the image default 1, with no split.

**Mutants.** My rerun of the lane's own driver, in six disjoint `--only` chunks (`receipts/adp_mutants/chunk*.txt`), reports 2 controls passing and 30 of 30 arms KILLED. The new arms:

| Arm | Failures | What fails |
|---|---|---|
| `cfg-valid-ucpu-bus` | 3 | AD5's advert carries 1 while GET reads 0; flag splits of 31,203 clocks in AD5 and 461 in AD6 |
| `cfg-valid-hard-reset` | 2 | AD6's advert carries 0; a 96,227-clock split |
| `cfg-valid-no-reset` | 5 | AD7 x2, AD6 x2, AD5's split |

Every one of the 30 counts equals `tb/adp_engine/README.md` and the PR's round-2 table.

**Regenerated patches.** For the four refreshed patches (`cfg-valid-any-selector`, `cfg-valid-not-sticky`, `cfg-overlay-only`, `cfg-nonzero-for-valid`), the +/- lines are byte-identical to round 1's (`receipts/patch_refresh_compare.txt`). Only the context moved.

**Gate record.** The README's full-run record for `gate-enable-dropped` was reproduced exactly (`receipts/gate_full_run.log`): 4 failures of 7,924, namely D3R14, AD0 x2 and AD1b.

### (4) Composition at the merged head

Every command ran locally at the exact head, with at most 8 CPUs.

| Command | rc | Result | Receipt |
|---|---:|---|---|
| `./scripts/run_suites.sh` | 0 | 33 suites, 1,017,162 checks, 0 failing (adp_engine 1,367; pp_top 7,944; D3 133 inside it) | `receipts/run_suites.log` |
| `make -C tb/adp_engine mutants` (driver, 6 `--only` chunks) | 0 | 2 controls pass, 30/30 KILLED, counts equal to the README | `receipts/adp_mutants/` |
| `tb/pp_top/d3_mutants.py --jobs 6` | 0 | 83 of 83 KILLED by their named checks; goldens PASS | `receipts/d3_mutants.txt` |
| `make -C tb/srp_top mutants` | 0 | 11 controls pass, 90/90, assertion coverage 65/65 | `receipts/campaigns/srp_top_mutants.txt` |
| `tb/pp_top/gsi_mutants.py` | 0 | 20 detected; golden and restored PASS | `receipts/campaigns/gsi_mutants.txt` |
| `tb/pp_top/name_wr_mutant.py` | 0 | decode killed; golden and restored PASS | `receipts/campaigns/name_wr_mutant.txt` |
| `tb/acmp_talker/retry_mutants.py` | 0 | 62 killed, 7 equivalence and 1 performance controls | `receipts/campaigns/retry_mutants.txt` |
| `tb/srp_admission/mutants.py` | 0 | 12/12 | `receipts/campaigns/srp_admission_mut.txt` |
| `tb/desc_mem_guard/mutate.py` | 0 | hold-deleted mutant detected (its mutant build fails by design, make rc 2) | `receipts/campaigns/desc_mem_guard.txt` |
| `Vpp_top_sim --adp-only / --d3-only / --gsi-internal-only / --name-writes-only / --dr3a` | 0 each | 55/0, 133/0, 6,182/0, 85/0; `--dr3a` prints its measurement table (ungraded by design) | `receipts/pp_top_entry_*.txt` |
| `./scripts/lint_hdl.sh` | 0 | 41 modules LINT OK | `receipts/lint_hdl.txt` |
| `make check` | 0 | lint, WaveDrom, links (981), both matrices, parameters, stale | `receipts/make_check.txt` |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested | `receipts/gen_matrix_check.txt` |
| `git diff --check` `c951a9ff..HEAD` and `b2db3a97..HEAD` | 0 | | `receipts/static_git.txt` |
| comment-stripped headers, `b2db3a97` vs head | n/a | 7 modules identical; `KL_aecp_engine` +1 output `dyn_cur_config_v_o` | `receipts/port_lists.txt` |

Hosted CI at the exact head, read only (`receipts/hosted_runs.txt`, `receipts/hosted_steps.txt`):
- Both the `pull_request` and the `push` run of `hdl` succeeded.
- Every gate step executed and succeeded: lint and every suite, the SRP LeaveAll campaign, the ADP campaign, the matrix, the `nvm_port` figures, docs-gates and portability.
- The only skipped step is "Build Verilator v5.050", a cache hit. It is a context skip, not a gate skip.

### (5) The PR body's Round 2 section and parent-visible list

The Round 2 section's commit table, the merge narrative, the AD5-AD7 descriptions, the mutation table and the validation table all agree with what I executed and read.

Parent-visible list, item by item:
- **Item 1.** The interface change is only `KL_aecp_engine` +1 output. I measured this against main; the other 7 headers are identical.
- **Item 2.** What the merge brings is named as #132's consolidated list, #133's section 4 and #133's composed-head note. The combined adaptation patch contains no lane edit, which is consistent with "this lane adds no parent edit".
- **Item 3.** The `current_cfg_i` meaning matches the RTL: `protocol_processor_top.sv:1723`, and the port comment at `:211-215`.
- **Items 4 and 5.** The ratchet note and the entry points match the tree.
- **The parent bank.** I did not run the parent consumer bank at dev `ec0cc0c1` (out of scope). It remains the manager's.

## 3. Lens results

- **Conformance.**
  - IEEE 1722.1-2021 §6.2.2.18 and §7.4.8.2, as the PR and the docs cite them: the ADPDU index, GET_CONFIGURATION and ENTITY.current_configuration now agree across SET (AD2-AD4), restore (AD5), roll-back (AD6) and reset (AD7).
  - Milan v1.2 §5.6.2: invariance holds, with no new configuration-dependent field.
  - Milan §5.6.1: ADP stays gated behind the restore release (`top.sv:1709`).
  - The frozen #40 acceptance 1-4 stays met at the merged head.
  - The AEM_CONFIGURATION_INDEX_VALID question is retained as a manager decision (R5 below). It predates the lane, and the acceptance requires the index to move.
- **RTL.**
  - The merge resolution matches the re-merge with only the two conflict regions resolved.
  - The flag equals the store's term by term (section 2 (1)).
  - The flag has no new port; its one output was already in round 1.
  - The ADP index is sampled at build (`bld_cfg_r`), unchanged since round 1.
  - Lint is clean.
- **Robustness.**
  - The whole-run probe exercises every flag-moving event, with 0 splits and a working control.
  - The writer never writes in service.
  - The roll-back and the hard reset clear the flag and the row in the same clock.
  - Refused SETs write nothing and split nothing.
  - The campaign isolation is unchanged: a scratch tree, a positive control per suite and target, and the named-check kill rule.
- **Tests.**
  - AD5-AD7 grade the byte-exact first advert, GET, ENTITY and a per-clock flag equality over the reboot window. Their premises (saved bytes, applied/erased/rolled back, blank device) are themselves checked.
  - Each new arm is killed by the check it names.
  - The counts are reproduced exactly.
  - Every #132 and C1 campaign and entry point passes.
- **Docs.**
  - The round-2 docs name the restore and the roll-back consistently: 02 §2 rule 4, the 04 §3 field row (with a link to 07 F07.9, anchor present), the 09 §8.1 row, integrator §6, the `protocol_processor_top.sv` port and selection comments, the engine's port and block comments, and both READMEs.
  - `make check` passes.

## 4. Prior public findings at this head

| Prior item | Status at `20ec92b7` | Evidence |
|---|---|---|
| R406-1 **F-1** (MINOR): the flag's reset ungraded | **RESOLVED** | AD7 (`sim_main.cpp:10271`). `cfg-valid-no-reset` KILLED with AD7 named, 5 failures. Rows added to the README and PR tables. My rerun: 30/30. The optional refused-SET leg was not taken (see R2). |
| R406-1 S-1 (SUGGESTION): AEM_CONFIGURATION_INDEX_VALID | RETAINED as SUGGESTION R5 | `pp_adp_pkg.sv:53` `ADP_ENTITY_CAPS_C = 0x0000C588` (flag clear); the 04 row still cites §6.2.2.18 unconditionally |
| R406-1 S-2 (SUGGESTION): scope "from then on" to reset | RESOLVED | integrator §6 (`docs/guides/integrator.md:254-263`) and 02 §2 rule 4 now say "while the row is unset: from reset, and after a roll-back" |
| R406-1 S-3 (SUGGESTION): tautological cell counts | RETAINED as SUGGESTION R4 | `tb/adp_engine/sim_main.cpp:1559,1561` unchanged |
| R407-1 S1 (SUGGESTION): F04.3 "domain mismatch, index > last" row | RETAINED as SUGGESTION R1 | `tb/adp_engine/sim_main.cpp` unchanged since `9185c49`; `DiscRow` (`:230`) still has only `V_DOMS` |
| R407-1 S2 (SUGGESTION): refused-SET and reset legs in AD | reset leg RESOLVED (AD5-AD7); refused-SET leg RETAINED as R2 | AD7 and the AD5/AD6 reboots; the refused-SET case is covered structurally and by this round's whole-run probe, but not by a suite check |
| R407-1 S3 (SUGGESTION): the 09 blank line; "until reset" | "until reset" RESOLVED; blank line RETAINED as R3 | `docs/architecture/09_verification.md:142-143` |
| R407-1 O1 / O2 / O3 | O1 = R5; O2 still true (the S3 pre-flush check does not see the gate mutant, and the README says so); O3 unchanged | `receipts/gate_full_run.log` |

## 5. Findings

There is no open BLOCKER, MAJOR or MINOR finding. The retained SUGGESTIONs follow; none affects the verdict or any lens.

**R1: SUGGESTION.** Carried from R407-1 S1.
- **Lenses:** Tests, Conformance.
- **Where:** `tb/adp_engine/sim_main.cpp:230` (`DiscRow`).
- **Evidence:** the F04.3 walk has no "domain mismatch, index > last" x TK_DISCOVERED row.
- **Impact:** a domain-only regression on the fresh-index branch would pass. The shipped RTL is correct.
- **Outcome:** add the row, or state the partition choice in the README.
- **Verification:** a domain analogue of `disc-fresh-checks-gm` turns red.

**R2: SUGGESTION.** The remainder of R407-1 S2 and R406-1 F-1's optional leg.
- **Lenses:** Tests.
- **Where:** `tb/pp_top/sim_main.cpp` `AdpConfigPhase`.
- **Evidence:** no AD arm sends a refused SET_CONFIGURATION on the unset row and then compares the ADPDU, GET and ENTITY. The equivalence holds structurally and in this round's whole-run probe, which includes W18d/W18d2.
- **Impact:** low. A future writer that lets a refused SET reach the row would be caught only by W18g's GET check, not by an ADPDU check.
- **Outcome:** optionally, add the leg.
- **Verification:** AD passes, and a patch letting the refusal write turns it red.

**R3: SUGGESTION.** Carried from R407-1 S3.
- **Lenses:** Docs.
- **Where:** `docs/architecture/09_verification.md:142-143`.
- **Evidence:** a missing blank line joins the MTXW paragraph to the next one.
- **Outcome:** add the blank line.

**R4: SUGGESTION.** Carried from R406-1 S-3.
- **Lenses:** Tests.
- **Where:** `tb/adp_engine/sim_main.cpp:1559,1561`.
- **Evidence:** the cell counts count loop iterations, so they cannot fail.
- **Outcome:** count graded cells instead.

**R5: SUGGESTION.** R406-1 S-1 and R407-1 O1.
- **Lenses:** Conformance, Docs.
- **Where:** `hdl/adp/pp_adp_pkg.sv:53`; `docs/architecture/04_adp_engine.md:80`.
- **Evidence:** the capability flag is clear while the index moves. This predates the lane, and the frozen acceptance requires the movement.
- **Outcome:** a manager or spec-owner decision, recorded in 04.

## 6. Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN (R1, R5 are SUGGESTIONs) | #40 acceptance 1-4 and both assignments; IEEE §6.2.2.18 / §7.4.8.2 and Milan §5.6.1 / §5.6.2 as cited; AD1-AD7 three-view agreement; `pp_adp_pkg.sv:53`; the restore rule `KL_aecp_nvm_writer.sv:616`; whole-run probe | R407-2 | 20ec92b7b190d03c46e40be89d236bc9a0702a59 |
| RTL | CLEAN | re-merge vs `cae0988`; `KL_aecp_engine.sv:1545,1554-1559,1597-1599,1782-1785,1803-1839`; `KL_aecp_dyn_state.sv:206,218,262-266,290-330`; `KL_aecp_nvm_writer.sv:99,459-460,616,734,831-848,1078-1087`; `protocol_processor_top.sv:211-215,1708-1723,1753,3690`; `KL_adp_engine.sv` `bld_cfg_r`; header comparison; lint 41/41 | R407-2 | 20ec92b7b190d03c46e40be89d236bc9a0702a59 |
| Robustness | CLEAN | whole-run flag probe (0 splits; 15/16/8/10 events) with its control (20 splits); refused SETs W18d/W18d2/W18g; in-service writer read-only; reset symmetry; campaign isolation | R407-2 | 20ec92b7b190d03c46e40be89d236bc9a0702a59 |
| Tests | CLEAN (R1, R2, R4 are SUGGESTIONs) | `sim_main.cpp:10144-10318` (AD5-AD7, `reboot`, `graded_step`, `first_advert_agrees`); `pp_top_wrap.sv:375,720-722`; `mutants.py`; 7 new/refreshed patches; ADP 30/30; D3 83/83; srp_top 90/90; GSI; name-write; retry; admission; desc_mem_guard; 33 suites; entry points; gate full-run record | R407-2 | 20ec92b7b190d03c46e40be89d236bc9a0702a59 |
| Docs | CLEAN (R3, R5 are SUGGESTIONs) | 02 §2 rule 4; 04 §3 row; 09 §8.1 row; integrator §6; top and engine comments; `tb/pp_top/README.md` AD; `tb/adp_engine/README.md` campaign table (checked against my logs); PR Round 2 section and parent-visible list; `make check`; `gen_matrix --check` | R407-2 | 20ec92b7b190d03c46e40be89d236bc9a0702a59 |

## 7. Real limits

- **Simulator.**
  - The assigned path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host.
  - I used the sibling manager wrapper `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator`. It reports `Verilator 5.050 2026-07-01 rev v5.050`, the CI pin. Its install root is redacted as `<PINNED-SIMULATOR-ROOT>`.
  - The wrapper and binary hashes are in `receipts/tool_identity.txt`.
- **Parallelism.** Every run was pinned to 8 CPUs with `taskset -c 0-7`. The ADP campaign ran as 6 concurrent driver invocations over disjoint `--only` lists. The composition campaigns ran as 6 concurrent jobs. The D3 campaign ran alone with `--jobs 6`.
- **Not run (out of scope):**
  - the Yosys portability bank (hosted `portability` succeeded);
  - `make -C tb/nvm_port figures`, which needs PR #13's objects (hosted step succeeded);
  - the parent consumer bank at dev `ec0cc0c1` and the donor full bank;
  - the gPTP and builder banks.
- **The parent-visible claim.** "The parent instantiates `KL_aecp_engine` nowhere" rests on the author's read-only grep and the manager's parent bank. I verified the processor-side header identity only.
- **The specifications.** The PDFs are not available here. Clauses were judged as the repository and PR quote them.
- **No hardware.** No hardware, no physical calibration, no Docker or act. Field skips are not hardware proof.
- **Clone state.** All build products I created (and the `make check` WaveDrom venv) were removed. `scripts/verify_clone_restored.sh` reports:
  - HEAD, the tree and the index tree equal the exact head;
  - 358 tracked files are byte- and mode-identical to their blobs;
  - there is no tracked, untracked or ignored drift, and there are no gitlinks (none are required).
  - The receipt is `receipts/clone_restored.txt`.

## 8. Pending manager duties

- Post the donor full bank and the parent consumer bank at milan-fpga dev `ec0cc0c1`, with the combined #132 + C1 adaptation applied and the gitlink at this head.
- Build and accept the final current-dev candidate at the merge turn. The source base is `b2db3a97` and live dev is `ec0cc0c1`. Hosted and act acceptance stay with the manager.
- R5: decide on AEM_CONFIGURATION_INDEX_VALID.
- Keep #85 item 4 (available_index interop against a live controller) open for a bench lane.

Publishable files are listed in `MANIFEST.sha256`. `scratch/` is disposable and is not published.

R407-2 FINISHED
