[R438] NEGATIVE - exact head 3370c6cbd5e4b096167c19ca709556a40207e538

# R438-1: milan-fpga issue #635 / PR #636, internal cleared-context review

- Head `3370c6cbd5e4b096167c19ca709556a40207e538`, tree `c7ef42fb98b23ea0a00db283f3e6ea0ba17745e5`. Twelve commits on dev `cdf49d1a28527562888f0a903de51b6b15b1244f`.
- Scope reconstructed from AGENTS.md, CONTRIBUTING.md 2.1 and 3, docs/README.md, the #635 body (frozen acceptance 1 to 5), the assignment (#635 comment 5958619779), TAKEN (5958652460), REVIEW READY (5962152491), the PR body, and the author packet at `ecc18462` (`review-evidence/635-r1`: MANIFEST.json, HANDOFF.md, PR-BODY.md, the patch). The processor PRs #135 to #140 and #142 were read for their parent-visible lists.
- The verdict is NEGATIVE on one MINOR (F1, Docs and Conformance): one parent-observable C5a change is not recorded. Everything else checked holds: the pin, the patch, every generated record, the capture gate and the RTL tie-off.

## Findings

### F1 - MINOR - Docs, Conformance - `CHANGELOG.md:45`, `docs/reference/SUBMODULES.md:114` - the C5a NOT_IMPLEMENTED echo on a broken response memory is not recorded

- **Authority.** Acceptance 5 requires that each processor change the parent can observe be recorded where the parent documents it, including "the AECP deadline and hazard faces". Processor PR #140's round-2 parent-visible list (lane C5a) says: "a command of any AECP message type but AEM_COMMAND, whose response memory fails or which is preempted past its deadline, answers NOT_IMPLEMENTED with the command echoed."
- **Evidence.** See `receipts/f1_evidence.txt`.
  - At `b2db3a97`, the processor's `docs/guides/operator.md:54` reads "Anything, while the response memory is broken: a well-formed 60-byte ENTITY_MISBEHAVING".
  - At `631eeb34`, `docs/guides/operator.md:55` adds "or, for a command that is not an AEM command (a Milan Vendor Unique one), NOT_IMPLEMENTED with the command echoed". `:326` says that for GET_MILAN_INFO this NOT_IMPLEMENTED is the fault answer, because its response memory failed or it outlived its deadline. `docs/guides/integrator.md:358` says the same for the `resp_mem_*` face.
  - The parent records only the deadline arm. `CHANGELOG.md:45` reads "Non-AEM messages on that path answer NOT_IMPLEMENTED, echoed", where "that path" is the 100 ms deadline. The C5a rows at `SUBMODULES.md:114-115` cover the deadline and the hazard classes only. No parent record names the response-memory arm.
- **Impact.** The parent's response-memory troubleshooting entry (`docs/reference/REGISTER_MAP.md:2358`) is keyed on the entity answering ENTITY_MISBEHAVING. At this pin, a controller's first Milan command (GET_MILAN_INFO) answers NOT_IMPLEMENTED under that same fault. Nothing in the parent's adoption record tells an operator or a later adopter that this answer changed with the pin. A NOT_IMPLEMENTED from GET_MILAN_INFO reads as "not a Milan entity" rather than "response memory failed". So acceptance 5's record of the C5a faces is incomplete.
- **Required outcome.** Where the parent records the C5a deadline arm (the `631eeb34` CHANGELOG section, and the parent-observable table in SUBMODULES.md), record that a non-AEM command, GET_MILAN_INFO among them, also answers NOT_IMPLEMENTED with the command echoed while the response memory is broken. At `b2db3a97` that case answered ENTITY_MISBEHAVING. A pointer from the REGISTER_MAP memory-bridge section is optional.
- **Verification.** The new text matches processor `operator.md:55` and `:326` at `631eeb34`. `scripts/docs_check.py`, `scripts/check_em_dash.py --base cdf49d1a...`, `scripts/check_doc_paths.py`, `scripts/check_doc_style.py` and `scripts/check_submodule_docs.py` stay rc 0. Re-review at the new head.

### S1 - SUGGESTION - RTL, Docs - `hdl/milan/KL_pp_shadow.sv:1099` - "manager ruling on #80" names a processor issue with a bare parent-repo number

- In this repository, a bare `#80` reads as milan-fpga #80. The ruling it means is on processor issue #80 (processor PR #139 cites "the ruling on #80" in the processor repository).
- The line is byte-identical to the supplied patch, which the assignment required. So this is optional, and it belongs with the `current_cfg_i` comment rewording the manager has already routed to #495.
- Fix: "processor lane C6, manager ruling on processor issue 80".

### Prior public findings

- At the review start (PR #636 comment 5962459229) the PR carried no review, inline review comment or reviewer finding. Only the two [A10] review-start comments existed, and #635 carried only the assignment, TAKEN and REVIEW READY.
- So there is no prior finding to resolve or retain. The re-check made after this verdict was written is recorded under "Post-verdict check".

## What was checked, per question

1. **Only processor change is the gitlink (`receipts/pin_change.txt`, `pp_merge_tree.txt`, `pp_prs.tsv`).**
   - Commit `14f8c27f` changes only `protocol-processor`, `160000` `b2db3a97` -> `631eeb34`. Base..head has no other entry under the path. The index holds one stage-0 gitlink record, and the processor checkout is clean.
   - `b2db3a97` is an ancestor of `631eeb34`. First-parent history is exactly seven merges: #136 `0451d83d`, #135 `d5f73bac`, #137 `3f3ea56b`, #138 `16ea10ac`, #140 `03c842a7`, #139 `2ebd4fe8`, #142 `631eeb34`.
   - Each merge's second parent equals that PR's recorded head SHA. Each merge's tree equals `git merge-tree --write-tree` of its parents, so no merge carries changes of its own. The branch commit counts (10+17+14+20+17+14+6 = 98) plus the seven merges equal the 105 commits in the range.
   - All seven PRs are merged into processor `main`. There is no PR #141; issue #141 is closed and was implemented by #142.
   - `631eeb34` is an ancestor of the processor's current `main`, which is 20 commits ahead, so the pin cannot dangle.
2. **Patch applied as three commits, equal byte for byte (`receipts/patch_equivalence.txt`).**
   - The patch's sha256 is `67bcd698...7bd7c`, as published.
   - `git apply --cached` on the base tree, compared with `927428d16`'s tree, differs only in the gitlink.
   - The patch-id of `14f8c27f..927428d1` equals the patch file's (`79127757...`). The three commits touch one concern each. Head blobs are `b33d91c6` and `46f3faf8`, and no later commit touches either file.
   - **Port and parameter diff of `protocol_processor_top`, two methods** (`receipts/pp_top_port_diff.txt` from `port_diff.py`, and `pp_top_header_diff.txt`, the comment-stripped header): 36 -> 37 parameters and 211 -> 212 ports. The only additions are `parameter bit EN_IDENTIFY_NOTIF_P = 1'b0` and `input wire identify_button_i`. Every other declaration line is identical.
   - **Meaning changes in the commented header** (`protocol_processor_top.sv:186-192`, `:228-243` at `631eeb34`). `current_cfg_i` is now the fallback when the configuration overlay is unset; the author disclosed this and the rewording is routed to #495. `DESC_LINE_BYTES_P` now has an enforced range of 576..1008 in steps of 8, and the parent binds 576 (`hdl/milan/milan_datapath.sv:330`, `KL_pp_shadow.sv:221`).
   - `identify_button_i` is read only inside `KL_aecp_notify`'s `gen_ident`, which is built only when `EN_IDENTIFY_NOTIF_P` is 1 (`protocol-processor/hdl/aecp/KL_aecp_notify.sv:709`, `:783`). So the tie-off comment "never read while EN_IDENTIFY_NOTIF_P is 0" is true.
   - Tying the input off is consistent with Milan v1.2 5.4.5.4, which is a SHOULD for an entity that has a user identify action. The parent's compliance matrix records 5.4.5.4 as n/a as a gap (`docs/reference/MILAN_COMPLIANCE_MATRIX.md:145`).
3. **Every pin-derived record, re-run through its generator (`logs/gen_*.log`).**
   - `ooc.sh --record-rom-digests`, `check_port_contracts.py --write-budget`, `measure_naming.py --write-budget` and `submodule_boundaries.gen.py` all rewrote byte-identical files (`git diff --exit-code`, then restored).
   - Independently, each ROM generator was run from a `git archive` of each pin (`logs/romgen.log`, `romgen.sh`). At `631eeb34`: `ltn_rom.hex` `23cc67ee...e956` (equal to the `b2db3a97` row) and `ucode.hex` `518b900c...37f8`. At `b2db3a97`: `ucode.hex` `23605682...7144`, equal to the ledger's existing row.
   - `SUBMODULES.md` is hand-edited in the same form as the `b2db3a97` and `c951a9ff` adoptions, and `check_submodule_docs.py` passes.
4. **Capture gate (`receipts/capture_census.txt`, `logs/capture.log`).**
   - `check_nvm_capture.py` rc 0, all seven controls detected.
   - The recomputed census equals the receipt's `measured_for`: 8x8 12,634 B / 156 records; 1x1 TDM8 3,218 B / 53 records; 50/50/100 MHz.
   - Firmware `milan_baremetal.c` sha256 `a73ecc25...0eb3` equals the receipt.
   - The harness (`tb/verilator/nvm_capture_cpu/*.py`) reads no processor source. So the receipt's `processor_pins` (`b2db3a97`) is provenance, and a re-measure is not owed.
5. **What the parent records as observable.**
   - The SUBMODULES lane table matches the processor merges.
   - These were verified against the processor sources at `631eeb34`:
     - the `MEDIA_CLOCK_FOLLOWING.md` status: D3C1 to D3C4 in `tb/pp_top`; six D3C mutants (`aecp_dispatch_mutants.py` `sclks-bound-three` and `sclks-bound-inclusive`, `d3_mutants.py` `clks_*` four); #142's only `hdl/` change is the `gen_ucode.py` comment; `gen_ucode.py:1654-1663` and `:1674-1711` are the range-check comment and the SET_CLOCK_SOURCE program with its refusal tail;
     - the other b2db-pinned citations (`KL_aecp_nvm_writer.sv:501-503`, `KL_aecp_dyn_state.sv:114`, `:352`), which have not moved;
     - the C2 (`cfg_maap_internal_i` tied 0), C3, C5b and C6 rows, against the processor PRs' final parent-visible lists.
   - The one gap is F1.
6. **Disclosed deviations and rulings.**
   - xvlog re-run alone: accepted. No Vivado is on this host, so it was not reproduced.
   - Sweep relaunch after nohup: accepted. `scripts/test_suite_cancellation.py:311-316` kills its probes with SIGHUP, which a nohup-inherited ignore defeats.
   - act self-test from the audited install: accepted. `scripts/act_ci.py` is unchanged on the branch, with sha256 `79579e6b...38f8` equal at base and head.
   - Test-evidence budget left at 77 (the ratchet reads 72), the stale physical README figure (it predates the lane) and the two processor suggestions to #495: taken as the manager's rulings stated in the assignment. They are not findings.

## Fault and mutation probes (`probes.sh`, `logs/probes_*.log`, `logs/probe_*.log`)

Each probe edited one tracked file in the clone, ran its gate, and restored the file from the index.

| Probe | Gate | Expected | Result |
|---|---|---|---|
| drop `.identify_button_i (1'b0)` | `lint_rtl.py --check` | fail | rc 1, new PINMISSING, `hdl/milan` 3 > 2: DETECTED |
| tie `identify_button_i` to 1 | lint + port contracts | pass | rc 0 (not read at 0; see limits) |
| bind `EN_IDENTIFY_NOTIF_P` to 1 | lint + port contracts | pass | rc 0 (no parent gate grades the value; see limits) |
| drop the `acmp_mutants.py` disposition | `measure_test_evidence.py --check` | fail | rc 1, 1 unexplained DUT-source reader: DETECTED |
| drop the `notify_mutants.py` disposition | same | fail | rc 1, same: DETECTED |
| `631eeb34` `ucode.hex` row altered | `ooc.sh KL_render_setpoint` | fail | rc 2, content digest mismatch: DETECTED |
| base `rom_digests.tsv` | same | fail | rc 2, no recorded digest at `631eeb34`: DETECTED |
| base `SUBMODULES.md` | `check_submodule_docs.py` | fail | rc 1: DETECTED |
| base boundary SVG | `submodule_boundaries.gen.py --check` | fail | rc 1, stale: DETECTED |
| base `port_docs.budget` | `check_port_contracts.py` | fail | rc 0, "can be lowered": the ratchet only fails on additions |
| base `naming.budget` | `measure_naming.py --check` | fail | rc 0: identity rows equal, only the count comment differs |

The last two rows mean the budget re-records are tightenings, not gate-forced changes. They are still the generators' exact output (item 3), so they are not defects.

## Gates run at the head (`logs/*.log`, each with its `.rc`)

| Gate | Result |
|---|---|
| `lint_rtl.py --check` (Verilator 5.050 rev v5.050, the scoped install, identity checked) | rc 0, 90 <= 90 |
| `check_port_contracts.py` | rc 0; processor 1757 ports, undocumented 111 <= 111, 59 without a rationale |
| `measure_naming.py --check` | rc 0, 96 recorded |
| `measure_test_evidence.py --check` | rc 0, 72 <= 77, 0 <= 0 unexplained readers |
| `submodule_boundaries.gen.py --check` | rc 0 |
| `check_nvm_capture.py` | rc 0 |
| `check_submodule_docs.py`, `docs_check.py`, `pp_srcs.py --check` | rc 0 |
| `check_rtl_source_lists.py` | rc 0, 107 files, 4/4 lists, processor 36/42 tops |
| `make -C tb/verilator/pp_shadow -j16` | rc 0: 606, 606, 646, 311 checks, 0 failures |
| `check-integrator-params.py` (processor) | rc 0, 27 = 27 = 27 |
| `check_doc_paths.py`, `check_py_idiom.py`, `check_doc_style.py` | rc 0 |
| `check_em_dash.py --base cdf49d1a` (pinned renderer installed into the packet scratch only) | rc 0, 0 findings over 63 added lines |

The clone was restored and verified after the probes (`receipts/restore_verification.txt`):

- HEAD, index tree and head tree are all `c7ef42fb`;
- no cached or worktree diff, and empty porcelain status;
- every tracked regular file rehashes to its index blob with a matching mode;
- the four gitlinks are at their recorded pins.

## Hosted evidence at this head (`receipts/hosted_runs.tsv`, `hosted_check_runs.tsv`, snapshot 2026-10-02 22:37Z)

- **Complete and successful:** `rtl-fast`, `docs` (docs-check, docs-check-no-git, wire-accountability), `elaborate`, and these `rtl-full` jobs: full-ci-gate, verilator-lint, yosys-elaboration, bdd-conformance, Yosys shards 0 to 3, Verilator shards 0, 2 and 3.
- **Skipped:** the physical gPTP job (nightly and manual only).
- **Still in progress:** `rtl-full` run 37070220891, with Verilator shards 1/5 and 4/5 running. The `verilator-suites` and `yosys-portability` aggregates were not yet emitted, and the commit status was `pending`.
- This contradicts the premise that every hosted context was green before the review started. The manager owns hosted acceptance.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | acceptance 1 to 5 against the diff; `protocol_processor_top` header at both pins; `KL_pp_shadow.sv:1094-1140`; Milan 5.4.5.4 / IEEE 1722.1-2021 7.5.1 tie-off; `MILAN_COMPLIANCE_MATRIX.md:145`; processor PRs #135 to #142 parent-visible lists; `operator.md:54`/`:55` at both pins | R438-1 | `3370c6cbd5e4b096167c19ca709556a40207e538` |
| RTL | CLEAN | `hdl/milan/KL_pp_shadow.sv:1094-1100`, `:1135-1140`; `protocol_processor_top.sv:186-192`, `:228-243`, `:3994`, `:4484` at `631eeb34`; `KL_aecp_notify.sv:709`, `:783`; lint 90 <= 90; port-contract gate; pp_shadow 4 builds | R438-1 | `3370c6cbd5e4b096167c19ca709556a40207e538` |
| Robustness | CLEAN | constant tie (no new CDC path or flop at 0); `DESC_LINE_BYTES_P` 576 inside the enforced 576..1008; `cfg_maap_internal_i` tied 0 (`milan_datapath.sv:2339`); deadline versus the D3 boot hold (rule (d) exemption, graded by D3O6 with mutant `dl-boot-hold-not-exempt`, `tb/pp_top/README.md:1005`); ROM-ledger refusal paths (probes); capture census unchanged | R438-1 | `3370c6cbd5e4b096167c19ca709556a40207e538` |
| Tests | CLEAN | probes table (9 detected, 2 explained); both new `DUT_READER_DISPOSITIONS` entries true to `acmp_mutants.py:166-215` and `notify_mutants.py:268-310` (isolated copy, table-planted edits, no expected value read); generator re-runs byte-identical; pp_shadow 606/606/646/311 | R438-1 | `3370c6cbd5e4b096167c19ca709556a40207e538` |
| Docs | UNCLEAN (F1) | `CHANGELOG.md:11`, `:39-59`; `docs/reference/SUBMODULES.md:25`, `:83`, `:93-119`; `docs/design/MEDIA_CLOCK_FOLLOWING.md:8`, `:1278-1286`; boundary diagram and `PNG_MANIFEST.json` (generator); docs, em-dash, path and style gates | R438-1 | `3370c6cbd5e4b096167c19ca709556a40207e538` |

## Real limits

- **Not run here:** `xvlog_gate.py` (no Vivado), `run_all_suites.sh`, `syn/yosys/run.sh`, the builder test, `milan_dp`, `milan_dp_render` and `nvm_cosim`. These are the manager's banks. No act or Docker run, no hosted re-runs, and no hardware. Physical calibration was NOT RUN.
- **Processor suites:** not re-run. Processor behaviour claims are checked against the processor's sources, docs and merged PR bodies at `631eeb34`, not by re-execution.
- **Naming count:** the base pin's count line (95, processor 21) was not re-measured, because that needs the processor checked out at `b2db3a97`. The head file is the generator's exact output.
- **Identify tie-off values:** no parent test grades `EN_IDENTIFY_NOTIF_P` = 0 or the `identify_button_i` constant. Both alternative values pass lint and the port gate. At 0 nothing reads the input, and the sequencer is graded only in the processor's simulation, as the PR states.
- **Manager's rulings:** the rulings on `test_evidence.budget` and the #495 items were taken from the assignment. At review time they were not found as a public comment on #635, #636 or #495.

## Pending manager duties

- Fix F1, then publish a re-review at the new head.
- Carry S1 (optional) to the residue checklist, beside the `current_cfg_i` comment rewording and the compliance-matrix citations already routed to #495.
- Publish the ruling that keeps `scripts/test_evidence.budget` at 77 (a ratchet tightens in its own lane), and the #495 entries for the stale `milan_dp_gptp` README figure and the two processor suggestions.
- Confirm that hosted `rtl-full` completes, with `verilator-suites` and `yosys-portability` emitted and successful at the final head.
- Run the act replica and the candidate merge build at the merge turn (live dev was `cdf49d1a` at review time), plus the containment check after the merge.

## Post-verdict check

Re-checked at 2026-10-02T22:46Z, after the verdict and ledger above were written. PR #636 has 0 reviews and 0 inline review comments, and its only issue comments are the two [A10] review-start comments. #635 has only the assignment, TAKEN and REVIEW READY. No public reviewer finding exists on this PR, so there is nothing to resolve or retain.

R438-1 FINISHED
