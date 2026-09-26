[R328] NEGATIVE - exact head 104c8a54b183cd9215ed1e3a2e1be1634f48d33d

Round R328-1, internal independent review of kebag-logic/milan-fpga PR #579 for issue #502.
Head `104c8a54b183cd9215ed1e3a2e1be1634f48d33d`, tree `c1d413a847312074618f45635750252aea21e197`.
Base `831f94f4146cc45ec476f8c8dcf5afac7cd8eacf` (live dev at review time).
Commits reviewed: `87e263fd` (implementation on dev `7eb3b0d4`) and `104c8a54` (merge of dev `831f94f4`).

## Summary

The RTL change is correct. Pending now rises on the accepting edge of every changed live name or map write. It stays sticky until reset. An oracle I added watches the name RAM and the map stores directly, independent of the trigger, and it confirms this. The pin, ROM ledger, regenerated diagram and merge resolution are all correct. The firmware and CSR inputs are byte-identical to base. All 24 gates and suites I ran pass.

The verdict is NEGATIVE because three MINOR findings are open:

- **F1 (Tests):** no test sends a map command that is refused at record validation. A mutant that raises pending on validation beats (phase 4) instead of commit beats (phase 5) survives the whole suite.
- **F2 (Docs):** the materialization page's section 1 still describes the replaced mark trigger as the current source. Its section 5.2 names a register that no longer exists.
- **F3 (Docs):** the new explicit mutation target is missing from the testing page's list of explicit campaigns.

There are no BLOCKER or MAJOR findings. No prior public review findings existed on the PR or the issue, so none needed to be resolved or retained.

## Reconstruction

- Contract: AGENTS.md sections 3 to 8, CONTRIBUTING.md sections 1 to 3 and 6, docs/README.md.
- Scope: the issue #502 body, plus comments 5844866872 (decision and scope), 5845129498 (processor export decision), 5846418959 (round 2: pin 870ff88a, class-7 on `aecp_name_wr_o`, class-6 on `amap_edit_req_o` phase 5, mark stays the commit trigger, consumer form, disposition) and 5847404798 (merge-dev).
- Authorities: REQUIREMENTS.md section 1, SAVED_STATE_SNAPSHOT_OWNERSHIP.md sections 6.1, 11 and 13, and SAVED_STATE_MATERIALIZATION.md sections 1, 2, 5.2 and 10.
- Processor contract at the pin: `protocol_processor_top.sv:358-375` and `:646-667`, `KL_aecp_desc_store.sv:449-457` and `:540-548`, and the `gen_ucode.py` ADD/REMOVE_AUDIO_MAPPINGS and SET_NAME programs.
- Diff: `git diff 831f94f4..104c8a54` (18 paths), plus both commits individually.
- Executable evidence: my own runs, listed below. From the public packet at `dc9d0928`/review-evidence/502-r1 I read only the area records.

## Findings

### F1 - MINOR - Tests - tb/verilator/pp_shadow/sim_main.cpp:1385-1432 - refused-at-validation map control missing; a wrong-phase trigger survives

- **Authority:** my brief asks me to verify that "refused edits raise nothing" and to write a gate-on-the-wrong-phase mutant. AGENTS.md section 6 Tests asks whether "positive, negative, and boundary behavior is covered" and whether "each new test can fail for the defect it claims to detect".
- **What the suite covers:** the only refused-edit control is "K12 static output refused" (`sim_main.cpp:1405-1411`). That command is refused at transaction begin, before any record beat exists.
- **What it misses:** no command is refused at record validation (processor phase 4, answered BAD_ARGUMENTS). The program issues phase-4 beats for such commands but never reaches phase 5 (`gen_ucode.py` E_AMADD, and the top contract at `protocol_processor_top.sv:358-364`).
- **Mutant evidence:** mutant `phase4_validate` (`3'd5` changed to `3'd4` at `hdl/milan/KL_pp_shadow.sv:942`) SURVIVES both the static leg and the dynamic leg (`receipts/reviewer_mutants.log`).
- **Why nothing else catches it:** a search of `tb/verilator/pp_shadow/sim_main.cpp` and the `tb/verilator/milan_dp*/` sources shows no other assertion on `nvm_pend`. Only the K section grades it.
- **Shipping behaviour is correct:** with a record-refused ADD_AUDIO_MAPPINGS (stream_index 0x7fff) added, the shipping glue answers status 7 and leaves pending clear. The same probe kills `phase4_validate` in both legs (`receipts/oracle_probe_shipping.log`, `receipts/oracle_probe_mutants.log`).
- **Impact:** a regression that took the trigger from the validation beat would pass every gate. That regression would make any refused map command latch pending until reset, and it would also raise pending before the live write rather than on it. The acceptance's refused/unchanged control would then no longer be enforced.
- **Required outcome:** the shipping K12 sequence includes at least one map command refused at record validation, in each map direction that accepts edits. The command must be graded for its refusal status and for pending remaining clear. A trigger taken from phase 4 must fail the suite.
- **Verification:** rerun `make -C tb/verilator/pp_shadow`. Then apply the `phase4_validate` mutant (`reviewer_mutants.py <repo> <scratch> phase4_validate`) and confirm it is KILLED by a named refused-record check in both legs.

### F2 - MINOR - Docs - docs/design/SAVED_STATE_MATERIALIZATION.md:127-131, :142-143, :476 - current-source description still names the replaced mark trigger

- **Authority:** issue #502 scope item 3 names this page. AGENTS.md section 6 Docs requires that "changed contracts are reflected in authoritative docs".
- **Section 1 at head:** it says the parent's `pend_i` includes "a sticky bit a class-6 or class-7 commit mark sets (`hdl/milan/KL_pp_shadow.sv` lines 935 to 946)". Its table column "How a change is seen today" reads "the class-6 commit mark" and "the class-7 commit mark". At head that code is gone: `KL_pp_shadow.sv:941-953` triggers on `aecp_name_wr_w` and map phase 5, and the marks feed only `unused_aecp_marks_w`.
- **Section 5.2:** line 476 names `aecp_mark_pend_r`, a register that no longer exists. It is now `aecp_live_pend_r`.
- **Why this is not already covered:** the paragraph added at lines 221-238 corrects section 2 only. The present-tense section 1 and its line citation now contradict it.
- **Impact:** a cold reader of the page this issue was scoped to update gets the wrong trigger for the current source. The dangling identifier also breaks a search for the stage-2/3 glue the page proposes.
- **Required outcome:** section 1's prose and table describe the head's triggers (accepted name write and map phase 5) with a correct location. Section 5.2 names the register that exists, or states the change generically.
- **Verification:** read the three locations against `KL_pp_shadow.sv` at the new head. The docs, em-dash, style and path gates pass.

### F3 - MINOR - Docs - docs/testing/TESTING.md:259-273 - new explicit mutation campaign not listed

- **Authority:** `TESTING.md:259-261` says "A long mutation campaign is an explicit target ... #367 settled that rule and this page keeps the list of such targets".
- **What is missing:** `make -C tb/verilator/pp_shadow pending-mutant` is an explicit target outside the default `run` and outside every gate. Nothing under `scripts/`, `.github/` or `docs/testing/` invokes it; `scripts/measure_test_evidence.py:600` only carries its disposition. It is missing from the "Explicit campaign | Command | Who runs it" table. Only `tb/verilator/pp_shadow/README.md:57-60` and `:84-88` mention it.
- **Impact:** the killed late-mark mutant is the executable guard for the acceptance's "a mutant that triggers on the mark again must fail". Future changes to the pending glue, the `pp_shadow` K section or the map/name exports get no pointer to run it, so the guard can rot unrun.
- **Required outcome:** the testing page's campaign table lists the target and its command. Its "Who runs it" field names the files whose change requires it.
- **Verification:** read the table and run `make -C tb/verilator/pp_shadow pending-mutant`.

### S1 - SUGGESTION - Conformance, Robustness - hdl/milan/KL_pp_shadow.sv:941-942 - duplicate map records raise sticky pending with nothing changed

- **Evidence:** phase 5 is offered for every validated record, including an ADD of a mapping that already exists.
- **Shipping behaviour:** the probe's live-state oracle shows 0 state changes for the duplicate while pending latches. This follows the assignment's explicit choice of the phase-5 export (5846418959), and it is disclosed at `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:968`, `SAVED_STATE_MATERIALIZATION.md:228` and `tb/verilator/pp_shadow/README.md:69`. False-pending is the conservative direction the contract permits.
- **Scenario the harness cannot show:** on a durable baseline, one re-sent existing mapping flips status to pending until reset. The harness cannot show this because its only duplicate follows a real add (`sim_main.cpp:1428-1429`).
- **Optional:** when D3 lands, or earlier, qualify the map trigger with the datapath's change condition. Alternatively, record the trade-off as an explicit maintainer decision.

### S2 - SUGGESTION - Tests - tb/verilator/pp_shadow/sim_main.cpp:283-296 - the unsaved interval starts at the trigger signals, not at the live state

- **Evidence:** the observer defines "unsaved" from `aecp_name_wr_w` and `amap_edit_req_o && phase == 5`, which are the glue's own inputs. So the check cannot see a live change that precedes the export.
- **Current state:** at this pin the export and the live write coincide. My oracle (name RAM `u_pp.u_aecp.u_store.name_r`, `amap_in_store_r`, `amap_out_owner_v_r`, `amap_out_owner_r`, `amap_out_cluster_r`, `cmap_flat_w`) finds the first change on the same cycle as the first trigger in every case. The processor's own `name_wr_mutant.py` guards the export.
- **Optional:** anchor the interval on the live state, as `receipts/oracle/probe_main.patch` does.

## Lens results

These are the clean-lens lines. Tests and Docs are unclean because F1, F2 and F3 are open; their PASS lines record what was covered clean within each lens.

[R328] PASS Conformance - hdl/milan/KL_pp_shadow.sv:921-953 at 104c8a54; protocol-processor@870ff88a hdl/top/protocol_processor_top.sv:358-375,646-667, hdl/aecp/KL_aecp_desc_store.sv:449-457,540-548, hdl/aecp/ucode/gen_ucode.py (E_AMADD, set_name); hdl/milan/milan_datapath.sv:4255-4391 - checked against the 5844866872 and 5846418959 decisions:
- class 7 rises on `aecp_name_wr_o`, which is the name-RAM write enable itself outside boot load.
- class 6 rises on `amap_edit_req_o` && phase 5, the edge where `amap_in_store_r` and the output owner/cluster registers take the change.
- the backend registers `pend_i` on that edge (`KL_nvm_backend.sv:755-796`).
- the marks still fire once per changed command with the correct group, graded by "K command marks" and "K mark group".
- the open-port consumer form is gone (`KL_pp_shadow.sv:1080`), and both `DUT_READER_DISPOSITIONS` entries are present (`scripts/measure_test_evidence.py:597-602`).
- the late-mark mutant fails both K10 and K12 (`receipts/pending_mutant.log`).
- the independent oracle finds no live change without pending (`receipts/oracle_probe_shipping.log`).
- the pin is `870ff88a` (PR 121 merge), a descendant of `0922e434`.
- the ledger rows for `870ff88a` equal my regenerated ROM digests, and the `0922e434` rows are retained (`receipts/rom_ledger_check.txt`).
- firmware, `sw/`, `sw/litex/`, `hdl/common/csr/` and `configs/` trees are identical to base and to the implementation base (`receipts/firmware_unchanged.txt`), so no capture re-measure is owed.
- area: base and head shadow digests match `area.json` (455c6d63 to 6a0090d8); LUT 60855 to 60766, FF and RAM unchanged.

[R328] PASS RTL - hdl/milan/KL_pp_shadow.sv:921-953,1080 at 104c8a54; hdl/milan/milan_datapath.sv:7419-7421; hdl/milan/KL_nvm_backend.sv:755-796 - checked:
- clock: `clk_i` = `axis_clk` for the shadow, the processor, the map-edit commit block and the backend. The `rst_n` = `axis_resetn` statement is accurate, and no crossing is introduced.
- reset: the new latch uses synchronous active-low reset, matching CONTRIBUTING section 1 and the backend. Reset only clears toward pending-by-open-records, so no reset ordering yields a false durable.
- timing: the pulse is ORed combinationally into `pend_i`, so status rises on the write edge. The one-cycle-delay mutant is killed (`receipts/reviewer_mutants.log`).
- widths and handshake: the 3-bit phase compare is exact. Phase 5 has no backpressure (`milan_datapath.sv:4244` ties wait to 0), and the processor ignores wait on phase 5.
- lint: `lint_rtl --check`, `check_sv_idiom`, `check_port_contracts` and `check_wire_accountability` pass (`receipts/gates_summary.txt`).

[R328] PASS Robustness - pp_shadow K10/K12 at 104c8a54 plus reviewer probe (`receipts/oracle/*.log`, `receipts/reviewer_mutants.log`) - checked:
- unchanged SET_NAME and a repeated identical SET_NAME raise no pulse.
- zero-record map commands, begin-refused static-output edits and record-refused edits (probe) raise nothing.
- a held phase-5 request is idempotent: the datapath de-duplicates it and the latch is sticky.
- a snapshot ARM/ATTEST/ACK does not retire pending.
- reset restores the durable baseline, and the `reset_sets_sticky` mutant is killed.
- both map directions and both output-map configurations (static default, dynamic fixture) run.
- S1 is a conservative false-pending, not a false-durable.

[R328] PASS Tests (partial; lens UNCLEAN by F1) - tb/verilator/pp_shadow/{sim_main.cpp,Makefile,pending_mutant.py,pending_probes.vlt,fixtures/pending.yaml} at 104c8a54 - checked:
- K10/K12 drive real SET_NAME, ADD/REMOVE_AUDIO_MAPPINGS and GET_* frames through the shipping datapath. Probes are read-only `public_flat_rd`, and nothing is forced.
- `make` passes 520+520+520+159 checks (`receipts/pp_shadow_make.log`).
- killed: `pending-mutant`, `drop_name`, `drop_map`, `delay_one_cycle`, `pulse_only_no_sticky`, `phase0_begin`, `phase1_begin_commit`, `phase2_finish`, `map_any_phase` and `reset_sets_sticky`. `phase4_validate` survives (F1).
- `nvm_backend` passes 525+208 checks with 4 negative controls red, and `nvm_cosim` passes 465 checks with 39/39 mutants killed (`receipts/suite_*.log`).

[R328] PASS Docs (partial; lens UNCLEAN by F2, F3) - CHANGELOG.md, docs/reference/SUBMODULES.md, docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md sections 6.1, 11 and 13, docs/diagrams/* and tb/verilator/pp_shadow/README.md at 104c8a54 - checked:
- the changelog entry, pin table and history, section 6.1 source list and section 11 rows match the RTL.
- `submodule_boundaries.gen.py --check`, `check_diagram_pngs`, `check_submodule_docs`, `docs_check`, `check_em_dash --base 831f94f4`, `check_doc_style`, `gen_toc --check`, `check_doc_paths` and `check_feature_status` pass.

## Assigned verification items

1. **Glue:** met. The glue raises pending on the accepting edge in the backend domain, and the clock-domain statement is correct. The mark keeps its completion role. Unchanged, repeated and refused name commands, zero-record map commands and refused map commands raise nothing at head. The exception is a duplicate map record (S1, disclosed).
2. **K10/K12:** they use real commands, both map directions, reset and the durable baseline. The lane's mutant fails both checks on rerun. Ten of my own mutants were run: nine were killed, and the wrong-phase one survives (F1).
3. **Pin and ledger:** met. The pin is `870ff88a`. Its ROM rows equal the digests that `ooc.sh --record-rom-digests` computes from the pinned generators, and the `0922e434` rows are retained. The diagram and manifest pass the generator's `--check` and the raster check. They are byte-identical to the implementation parent, which was generated at the same pin.
4. **Firmware and area:** met. Firmware and CSR inputs are unchanged, and the capture, bare-metal and firmware self-test gates pass. The area delta is reported and tied to the exact source digests.
5. **Merge:** met. `git merge-tree 87e263fd 831f94f4` conflicts on CHANGELOG.md, SUBMODULES.md, the diagram trio, the manifest and the gitlink. The head differs from that auto-merge only on those paths. The ROM ledger auto-merged identically. No path outside dev's own changes moved (`receipts/merge_check.txt`, `receipts/remerge_tree.txt`).
6. **Repository gates:** all 24 gates and suites I ran pass (`receipts/gates_summary.txt`). The full banks were not run here; see Limits.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | KL_pp_shadow.sv:921-953,1080; processor top/desc_store/gen_ucode at 870ff88a; milan_datapath.sv:4255-4391; rom_digests.tsv; SUBMODULES.md; area.json; sw/, csr, configs trees | R328-1 | 104c8a54b183cd9215ed1e3a2e1be1634f48d33d |
| RTL | CLEAN | KL_pp_shadow.sv:921-953; milan_datapath.sv:7419-7421,4244; KL_nvm_backend.sv:755-796; lint, SV idiom, port-contract and wire-accountability gates | R328-1 | 104c8a54b183cd9215ed1e3a2e1be1634f48d33d |
| Robustness | CLEAN | pp_shadow K10/K12 both legs; reviewer refused-record and oracle probe; reset/ACK/duplicate/held-beat paths | R328-1 | 104c8a54b183cd9215ed1e3a2e1be1634f48d33d |
| Tests | UNCLEAN (F1 open) | pp_shadow sim_main.cpp/Makefile/pending_mutant.py/vlt/fixture; 11 mutants; nvm_backend; nvm_cosim | R328-1 | 104c8a54b183cd9215ed1e3a2e1be1634f48d33d |
| Docs | UNCLEAN (F2, F3 open) | CHANGELOG.md; SUBMODULES.md; SAVED_STATE_SNAPSHOT_OWNERSHIP.md; SAVED_STATE_MATERIALIZATION.md; TESTING.md; pp_shadow README; diagrams | R328-1 | 104c8a54b183cd9215ed1e3a2e1be1634f48d33d |

## Limits

- **Verilator substitution:** the requested binary `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist. I used Verilator 5.050 through `$VALIDATION_STORAGE/502-manager-r1/pinned-tool-bin/verilator` (wrapper sha256 905795b9..., verilator_bin 44898b22...), behind a local wrapper that caps build parallelism at 8 (`receipts/tool_identity.txt`, `receipts/verilator_wrapper.sh`).
- **Not run by me:** full parent/PP/gPTP sweeps, `milan_dp`, Yosys (including the OOC area; I checked the area record only against source digests), builder, behave, xvlog, the processor `pp_top` suite and `name_wr_mutant.py`, act and hardware. Physical calibration is NOT RUN, and skipped field campaigns are not hardware proof.
- **Scope of the probe:** my oracle and refused-record probe ran only in the `pp_shadow` harness shapes (1x1 static, and the dynamic-output fixture). Firmware control-face channel-map writes (`cfg_chmap_wr_*`) are outside #502 and were not graded.
- **Hosted checks:** snapshot at 2026-09-26T17:28:59Z. 17 runs had completed successfully, including `rtl-fast`, `docs-check`, `docs-check-no-git`, `elaborate`, `wire-accountability`, `full-ci-gate` and all four Yosys shards. Verilator shards 1/5 and 4/5 were still in progress, and the `verilator-suites` and `yosys-portability` aggregates were not yet emitted. The physical gPTP job was skipped (`receipts/hosted_checks_snapshot.txt`).
- **Clone restore:** after the probes, ignored build outputs were removed. 911 tracked superproject blobs and 248 processor blobs rehash to their index entries with correct modes, no index flags are set, and the gitlinks are at the pins (`receipts/restore_verification.txt`).

## Pending manager duties

- Route F1-F3 to the executor. After the fix, a re-review at the new head must re-cover Tests and Docs. It must also re-cover any lens whose artifacts the fix touches.
- Accept the hosted `verilator-suites` and `yosys-portability` aggregates at the exact head, and the act replica.
- Run the candidate-merge full bar against live dev at the merge turn, then post-merge containment.
- Obtain the external review (R329), and the maintainer's merge authorization.

R328-1 FINISHED
