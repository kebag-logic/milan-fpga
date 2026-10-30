# HANDOFF: issue #210 round 2 (PR #211)

Status: REVIEW READY.

- Base: main `a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645`.
- Round-1 head: `18a4dc1fcf91528a52737d5ea830b5acd5d543c4` (pushed as PR #211).
- Round-2 head: `0ea635ea22eeb6d97335c4e814eede1ac0d67ebc` on local branch `docs-sweep`: six commits on top of `18a4dc1`, no rebase, nothing pushed, no PR edited.
- Inputs read: issue #210 body and the latest [A10] comment (issuecomment-6521384962); reports R743-1 and R744-1; the round-1 handoff; IEEE 802.1Q-2014 §34.3, §34.3.2, §34.6, §34.6.1 (clause text); `hdl/aecp/ucpu_pkg.sv`, `KL_aecp_ucpu.sv`, `gen_ucode.py`, `KL_aecp_notify.sv`, `tb/nvm_port/Makefile` and `measure_figures.py`, the top `Makefile`.

## Round-2 items

| Item | Status | Change (file:line at head) | Evidence |
|---|---|---|---|
| R744-1 F1 (= R743-1 F4): 02 cites 802.1Q §34.6.1.1 | fixed | `docs/architecture/02_interfaces.md:283-289` | 802.1Q-2014 has §34.6.1 Talker behavior and §34.6.2, no §34.6.1.1. Confirming the sentence against the clause bodies found two more misattributions in it: the quote "used by the credit-based shaper algorithm (8.6.8.2) as ... idleSlope" is §34.3(d) (not §34.6.1), and SRP being operIdleSlope's sole source is §34.3.2 (§34.3(c) only says adminIdleSlope then has no effect). The sentence now cites §34.3(d) with its exact wording, §34.3.2 with §34.3(c), and §34.6.1 for the per-stream idleSlope ("the idleSlope set to the bandwidth requirement of the stream"). `git grep '34\.6\.1\.1' -- '*.md'` leaves only the superseded `docs/10_RESOURCE_AND_EFFORT.md:583`. |
| R744-1 F2 (= R743-1 F5): 06 µISA says 29 operations, omits `SHIFT_R` | fixed, and now gated | `docs/architecture/06_aecp_engine.md:1427` (30 operations), `:1434` (`SHIFT_R` in Data: a logical right shift of the 64-bit operand by `imm[5:0]`) | `ucpu_pkg.sv:51-87` declares 30 members, the last `OP_SHIFT_R = 5'd29`; `KL_aecp_ucpu.sv:681-684` executes `opa_e_r >> uop_e_r.imm[5:0]` with `opa_e_r` 64 bits (`:178`); `gen_ucode.py:33` maps it. The new derived check holds the table to the enum. |
| R743-1 F1: README counts two retired pages; there are three | fixed by linking | `README.md:28-30` | The sentence links to `docs/INVENTORY.md#retired` and states no count, so it cannot drift. |
| R743-1 F2: 02 summary says every CDC is the integrator's | fixed | `docs/architecture/02_interfaces.md:8-11` | Now says every crossing but one; with P-EN-IDENTIFY-NOTIFICATION = 1, `identify_button_i` passes the processor's own two-flop synchronizer (§2 rule 3). RTL: `KL_aecp_notify.sv:1022` (`if (EN_IDENTIFY_NOTIF_P)`), `:1031-1032` (`ASYNC_REG` `btn_q1_r`, `btn_q2_r`). |
| R743-1 F3: nvm_port summary says `make` runs three builds; it runs seven | fixed by linking | `tb/nvm_port/README.md:6-9` | The summary says `make` builds and runs the suite at each deadline bound, then the harness at each of its bounds, and points at the Makefile's `BUILDS` (`tb/nvm_port/Makefile:41`, `$(words 1 2 3 $(FUZZ_TMOS))` = 7). No digit and no `N of M` shape is added, so the figures gate's README inputs are unchanged (see Gates). |
| Recurrence rule (derive tree-defined counts and lists, or link) | done | `scripts/check-doc-inventory.py:13-18, 45-124`; `Makefile:6, 73-75`; `docs/INVENTORY.md:8-13`; `docs/architecture/09_verification.md:138` | `make inventory` now derives (a) the 06 §8 µISA count and its table's operation set from `ucpu_pkg.sv`'s `ucpu_op_e` enum, and (b) the 09 §7 target table from the Makefile's `check:` prerequisites. The README's retired-page count and the nvm_port build count are replaced by links. Fails closed: an enum member not in `OP_X = 5'dN` form, a missing heading, table, enum or rule, or a missing page or defining file is a finding. |
| R743-1 F6: diagram 22 SVG cites §9.2.1.1 and 100 ms | NOT fixed: finding | `docs/diagrams/22-aecp-descriptor-fetch.svg:155` | Not Markdown, and outside this round's [A10] list; this lane edits Markdown and docs-gate scripts only. Recorded below. |
| R743-1 RES1: three lane labels | fixed | `docs/00_MILAN_COMPLIANCE_REVIEW.md:577`, `:588`; `tb/pp_top/README.md:2728` | No link targeted `#lane-c6…` (`git grep '#lane-c6'` empty before and after). |
| R743-1 RES2: the glossary carries a value | fixed | `docs/GLOSSARY.md:87` | "far fewer clocks", the link to the HDL guide §7 kept. |
| Found this round: one more lane label | fixed | `tb/adp_engine/README.md:330` | "lane P1's AD8 and AD9" now names the change by its issues, as round 1 did in the same file. No tooling reads that row (`tb/adp_engine/Makefile`, no README parser). |
| R743-1 S1 to S4 (suggestions) | not taken | | Suggestions only; S1 (row link equals its path) and S2 (`*.MD`) are gate-hardening that no current row needs. |

Search for the same class elsewhere: every current page's "N builds", "N operations" and "N retired/superseded pages" was grepped. The remaining build counts (`tb/aecp_notify` three, `tb/acmp_nvm` two, `tb/adp_engine` two, `tb/nvm_port` body and 09 "three builds" of the suite) match their Makefiles' default `run` recipes.

## Findings the docs cannot fix (carried and new)

| Where | What | Source line or clause | Which is wrong |
|---|---|---|---|
| `docs/diagrams/22-aecp-descriptor-fetch.svg:155` | "IEEE 1722.1-2021 §9.2.1.1 gives a controller 100 ms before it retries" | 1722.1-2021 §9.2.1 is Overview with no subclause; §9.3.2.6 sets 250 ms timeout, 240 ms respond; 03 §7.1 states the right budget | the figure. Hand-authored SVG, outside this lane's Markdown-only remit; suggested text: "the AECP design budget T-BUDGET-AECP-WC, inside IEEE 1722.1-2021 §9.3.2.6's T-AECP-RESP, against roughly one microsecond per memory access" |
| `hdl/aecp/ucpu_pkg.sv:14`, `:48` (new) | comments say "the 29 operations of 06 §8" | the same file's enum declares 30 (`:87` `OP_SHIFT_R`); 06 now says 30 | the RTL comments |
| `tb/pp_top/notify_mutants.py:3`, `tb/pp_top/notify_phases.hpp:2` (new) | "lane C6" in test-source comments | #210 rule: no lane labels in text | the test comments |
| `hdl/top/protocol_processor_top.sv:666`, `hdl/srp/KL_srp_admission.sv:10` (round 1) | 802.1Q §34.6.1.1 | 802.1Q-2014 has no §34.6.1.1; §34.6.1 | the RTL comments |
| `hdl/aecp/KL_aecp_resp_buf.sv:32`, `tb/pp_top/sim_main.cpp:3737` (round 1) | IEEE 1722.1 §9.2.1.1, 100 ms | no such clause; §9.3.2.6 240 ms; 100 ms is `T-BUDGET-AECP-WC` | the comments |
| `tb/acmp_talker/sim_main.cpp:99` (round 1) | 802.1Q §35.2.2.7.4 | §35.2.2.7.2, Table 35-3 | the test comment |
| nine suite READMEs' mutation records (round 1) | 156 R-numbered review labels | #210 rule: no review labels | the docs, but the replacement reference is the owner's choice; hence "Refs #210", not "Closes" |

## Inventory at head (from `docs/INVENTORY.md`, 63 rows, held by `make inventory`)

Status counts: 59 current, 1 generated, 3 superseded. Rows changed this round: `README.md`, `docs/INVENTORY.md`, 02, 06, 09, `tb/nvm_port/README.md` (evidence cells).

| File | Purpose | Audience | Describes | Status | Evidence |
|---|---|---|---|---|---|
| `README.md` | what the processor is, the start-here path, repository map, how to build and check | new reader | the repository | current | sweep checks; start-here path added in this sweep; it links to the inventory's Retired heading rather than counting the retired pages |
| `docs/README.md` | documentation conventions: reading order, ID registries, figure rules, citation rules, editing workflow | author | `docs/`, and the gates through 09 §7 | current | sweep checks; its editing workflow now names the inventory row a new page needs |
| `docs/GLOSSARY.md` | defined terms, each pointing at its home | new reader | the vocabulary of every page | current | written in this sweep; each cited clause number read in its standard |
| `docs/INVENTORY.md` | this page: every Markdown file and its status | author, new reader | every Markdown file | current | held by `make inventory`, whose derived checks this page's summary lists |
| `docs/guides/README.md` | the three task guides and the diagram inventory | new reader | `docs/guides/`, `docs/diagrams/` | current | sweep checks |
| `docs/guides/hdl-engineer.md` | conventions, block structure, shared-service contracts, running the suites, known spec and tree divergences | HDL engineer | `hdl/`, `tb/`, `scripts/` | current | sweep checks; §9 divergence table re-read against the RTL: the shutdown row is resolved by 01 §5 and removed, the dispatch row reworded to the engine banner, the on-chip image row narrowed to F03.1 (F07.1 is already current) |
| `docs/guides/integrator.md` | the instantiation contract: ports, parameters, clocking and reset, memory masters, tie-offs, bring-up order | integrator | `hdl/top/protocol_processor_top.sv` | current | sweep checks; `make params` holds its parameter table to the top; two shortened port names spelled out |
| `docs/guides/operator.md` | what appears on the wire, what a controller sees, the snapshot and control windows, bring-up ladder | operator | the side port (`KL_pp_side_port`), the wire behaviour | current | sweep checks |
| `docs/architecture/01_overview.md` | scope, top level, operational model, Milan deltas (F01.4), parameter master table (F01.5) | new reader, HDL engineer | the whole processor; `protocol_processor_top` parameters | current | sweep checks; F01.5 compared with the top, `pp_pkg`, `ucpu_pkg`, `KL_pp_trace_ring`, `KL_mrp_strip`, `KL_acmp_talker` and the NVM producers: the stale timer-slot example removed (08 §5 owns it), P-DISPATCH-ROM-W marked as having no RTL consumer, the shutdown model corrected to the enable's fall (`protocol_processor_top.sv:2027`); F01.4 clause topics read in Milan v1.2 |
| `docs/architecture/02_interfaces.md` | every external contract, interface classes A to F, the status dictionary F02.10 | integrator, HDL engineer | the top's ports | current | sweep checks; its 802.1Q citations corrected (§35.2.2.7.2; §34.6.1 in F02.10 and §4.1, where §34.3(d) and §34.3.2 now carry what §4.1 had attributed to §34.6.1); the summary's clock-domain statement matches §2 rule 3 and `KL_aecp_notify.sv` |
| `docs/architecture/03_packet_engine.md` | the shared RX and TX datapath: validation, slots, dispatch, scoreboard, originator, TX arbitration | HDL engineer | `hdl/packet_engine/` | current | sweep checks; a citation of a clause IEEE 1722.1-2021 does not have corrected to `T-BUDGET-AECP-WC` and §9.3.2.6 |
| `docs/architecture/04_adp_engine.md` | discovery: the advertise and talker-discovery state machines | HDL engineer, compliance reviewer | `hdl/adp/KL_adp_engine.sv` | current | sweep checks |
| `docs/architecture/05_acmp_engine.md` | Milan connection management: the listener machine, its transition matrix F05.3, the stateless talker | HDL engineer, compliance reviewer | `hdl/acmp/` | current | sweep checks; anchors repointed to GitHub's rule |
| `docs/architecture/06_aecp_engine.md` | AEM and MVU commands, the command master table F06.14, registry, notifications, lock, µcode | HDL engineer, compliance reviewer | `hdl/aecp/` | current | sweep checks; F06.14 is held to the command table by `make aecpcmd`; the §8 µISA count and table are held to `ucpu_pkg.sv` by `make inventory` (`SHIFT_R` added) |
| `docs/architecture/07_memory_maps.md` | the entity model, records, NVM layout and flows, side-port map | HDL engineer, integrator | `hdl/aecp/desc/`, the NVM producers, `KL_pp_side_port` | current | sweep checks; F07.1's ROM node corrected: no dispatch or response-size ROM ships (06 §8.1) |
| `docs/architecture/08_timing.md` | every timing constant (F08.1), timer hardware, budgets, the timer slot map F08.4 | HDL engineer, compliance reviewer | `hdl/common/KL_pp_timer_service.sv`, `pp_pkg::pp_timer_map()` | current | sweep checks; F08.4's 68 and 91 slots recomputed from `pp_pkg.sv`; F08.1 clause topics and the MRP and AECP values read in Milan v1.2 Table 4.3 and IEEE 1722.1-2021 §9.3.2.6 |
| `docs/architecture/09_verification.md` | test categories, traceability, the documentation gates (§7), the suites and their evidence (§8) | verification | `tb/`, `scripts/` | current | sweep checks; `make inventory` holds the §7 table to the `check` rule |
| `docs/architecture/10_srp_engine.md` | the MSRP and MVRP endpoint participant | HDL engineer, compliance reviewer | `hdl/srp/` | current | sweep checks; one 802.1Q citation corrected (§34.6.1) |
| `docs/architecture/11_maap_engine.md` | the IEEE 1722-2016 Annex B block claim | HDL engineer, compliance reviewer | `hdl/maap/KL_pp_maap.sv` | current | sweep checks |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md` | the review of the concept document (§1 to §4), the gap register (§5), the requirement matrix (§6) and dispositions (§7, §8) | compliance reviewer | Milan v1.2 against the architecture | current | sweep checks; `make matrix` and `make reqtags` hold §5 and §6; its §1 to §4 review the superseded concept document and say so |
| `docs/traceability/MODULE_MATRIX.md` | which suites compile each module | verification | `hdl/` against `tb/` | generated | `scripts/gen_matrix.py --check` (`make modmatrix`) |
| `docs/diagrams/README.md` | the diagram classes, sources, exports and toolchain | author | `docs/diagrams/` | current | sweep checks; `make figures` holds the file classes |
| `IEEE_1722_1_Hardware_Protocol_Processor.md` | the original concept sketch the compliance review read | compliance reviewer | nothing in the tree | superseded | banner points at `docs/architecture/` |
| `docs/10_RESOURCE_AND_EFFORT.md` | the planning analysis of 2026-08-11 and the measured substitution outcome of 2026-08-14 | maintainer | the decision to build this processor | superseded | bannered in this sweep: its estimates and recommendations predate the build, and the processor now also serves SRP, which its §10 advised against; points at `syn/ooc/README.md` and the architecture |
| `docs/history/02-class-a-word-stream.md` | the 32-bit class-A word stream the first design specified and no port carries | HDL engineer | nothing in the tree | superseded | banner points at 02 §3 and the integrator guide §3 |
| `hdl/README.md` | the RTL layout, coding rules and the submodule consumption contract | HDL engineer, integrator | `hdl/` | current | sweep checks |
| `syn/ooc/README.md` | out-of-context synthesis recipes and the recorded area measurements, each with its date and trees | HDL engineer | `syn/ooc/`, the processor's area | current | sweep checks; its measurements are dated records of the trees they name |
| `tb/acmp_listener/README.md` | the listener executor against the F05.3 matrix | verification | `KL_pp_acmp_listener` | current | run 3,170 checks, as stated |
| `tb/acmp_nvm/README.md` | the binding NVM shadow and the manager arbiter | verification | `KL_acmp_nvm_shadow`, `KL_pp_nvm_mgr_arb` | current | run 388 checks, as stated |
| `tb/acmp_talker/README.md` | the stateless talker responder and its DA gate | verification | `KL_acmp_talker` | current | run 1,561 checks, as stated |
| `tb/adp_engine/README.md` | the ADP engine, with the walk of F04.2 and F04.3 | verification | `KL_adp_engine` | current | run 1,359 checks, as stated |
| `tb/aecp_cmds/README.md` | what the AECP engine decodes and dispatches, observed, and the record the command gate reads | verification | `KL_aecp_engine`, `tb/aecp_cmds/decode.json` | current | run 181 checks; `make aecpcmd` holds its record |
| `tb/aecp_notify/README.md` | the registry monitor lifecycle and notification controls | verification | `KL_aecp_notify` | current | run 131 checks, as stated |
| `tb/ca_originator/README.md` | the CONTROLLER_AVAILABLE frame builder | verification | `KL_aecp_ca_originator` | current | run 16 checks |
| `tb/desc_mem_guard/README.md` | descriptor memory response isolation | verification | `KL_aecp_desc_mem_guard` | current | run 78 checks |
| `tb/desc_store/README.md` | the entity-model store and the descriptor model lint | verification | `KL_aecp_desc_store`, `hdl/aecp/desc/` | current | run 586 checks; headline corrected from 584 |
| `tb/dispatch/README.md` | the normalized-transaction path into dispatch | verification | `KL_pp_normalizer`, `KL_pp_dispatch` | current | run 211 checks; headline corrected from 179, mutation record dated |
| `tb/dyn_state/README.md` | the dynamic-state store | verification | `KL_aecp_dyn_state` | current | written in this sweep (the suite had none); run 118 checks |
| `tb/elab_guards/README.md` | every elaboration guard stops every front end | verification, HDL engineer | the parameter guards in `hdl/` | current | run 155 checks |
| `tb/event_router/README.md` | the event fan-in and fan-out | verification | `KL_pp_event_router` | current | run 81 checks, as stated |
| `tb/lsn_admit/README.md` | the listener admission gate | verification | `KL_pp_acmp_lsn_admit` | current | run 18 checks, as stated |
| `tb/maap/README.md` | the MAAP engine against IEEE 1722-2016 Annex B | verification | `KL_pp_maap` | current | run 196 checks |
| `tb/name_state/README.md` | the complete saved-name inventory through real frames, port and reset | verification | the D3 writer's name records | current | run 1,236 checks, as stated |
| `tb/nvm_port/README.md` | the class F NVM port, its deadline, resets and device models | verification | `KL_pp_nvm_port` | current | run 393 checks in each of three builds, as stated; the summary names the Makefile's `BUILDS` instead of counting the builds; its figures gate (`make -C tb/nvm_port figures`, CI) holds the rest |
| `tb/originator/README.md` | the originator and inflight table | verification | `KL_pp_originator` | current | run 107 checks, as stated |
| `tb/pp_top/README.md` | the processor top end to end, section by section, with its mutation campaigns | verification | `protocol_processor_top` | current | sweep checks; not re-run here (run time); one clause citation corrected |
| `tb/prng/README.md` | the PRNG | verification | `KL_pp_prng` | current | run 76 checks; headline corrected from 57, mutation record dated |
| `tb/release_merge/README.md` | the TX slot release merge | verification | `KL_pp_release_merge` | current | run 18 checks |
| `tb/resp_buf/README.md` | the AECP response buffer in main memory | verification | `KL_aecp_resp_buf` | current | run 64 checks, as stated; one clause citation corrected |
| `tb/rx_slots/README.md` | the RX slot pool | verification | `KL_pp_rx_slots` | current | run 130 checks, as stated |
| `tb/rx_validator/README.md` | the RX validator | verification | `KL_pp_rx_validator` | current | run 555 checks, as stated |
| `tb/scoreboard/README.md` | the admission scoreboard against F03.7 | verification | `KL_pp_scoreboard` | current | run 3,705 checks, as stated |
| `tb/side_port/README.md` | the management side port and trace ring | verification | `KL_pp_side_port`, `KL_pp_trace_ring` | current | run 368 checks, as stated |
| `tb/srp_admission/README.md` | SRP admission freshness across shapes | verification | `KL_srp_admission` | current | run 991,231 checks at eight sources |
| `tb/srp_decoder/README.md` | the MRPDU vector decoder | verification | `KL_srp_decoder` | current | run 190 checks, as stated |
| `tb/srp_encoder/README.md` | the MRPDU encoder with the Domain and VLAN machines | verification | `KL_srp_encoder`, `KL_srp_domain`, `KL_srp_vlan` | current | run 593 checks, as stated |
| `tb/srp_stream_fsms/README.md` | the per-stream talker and listener machines | verification | `KL_srp_talker_fsm`, `KL_srp_listener_fsm` | current | run 1,435 checks, as stated |
| `tb/srp_top/README.md` | the assembled SRP engine end to end | verification | `KL_srp_top` | current | sweep checks; not re-run here (run time) |
| `tb/timer_map/README.md` | the F08.4 slot map and the 02 §5 event-router map | verification | `pp_pkg::pp_timer_map()`, `pp_pkg::pp_evr_map()` | current | run 1,360 checks; headline corrected from 1,187 |
| `tb/timer_service/README.md` | the timer service | verification | `KL_pp_timer_service` | current | run 48 checks, as stated |
| `tb/tx_arbiter/README.md` | the TX arbiter | verification | `KL_pp_tx_arbiter` | current | run 67 checks, as stated |
| `tb/tx_slots/README.md` | the TX slot pool | verification | `KL_pp_tx_slots` | current | run 95 checks, as stated |
| `tb/ucpu/README.md` | the µCPU executes the 06 §8 µISA | verification | `KL_aecp_ucpu` | current | run 447 checks, as stated |

## Gates (all foreground, logged, never piped)

| Gate | Base `a9e84b66` | Head `0ea635e` |
|---|---|---|
| `make -j8 check` (wavedrom, Mermaid CLI 11.16.0) | 0 | 0; `inventory selftest: 25 cases, OK`; `inventory: 63 Markdown files, OK`; links 1408 OK |
| `python3 scripts/gen_matrix.py --check` | 0 | 0 |
| `python3 scripts/check_upc_map.py` | 0 | 0 |
| `python3 scripts/check_m9_opcodes.py --selftest`, then plain | 0, 0 | 0, 0 |
| `./scripts/lint_hdl.sh` (pinned 5.050) | 0 | 0 |
| `tb/nvm_port` figures gate, README-derived inputs (claim coverage, arm rows, matrix, every claim's matches, every figure-shaped span) | identical | identical (byte-equal JSON); the full gate was not run (over one foreground command's time); CI runs it |

The same set also passed at the intermediate head `06c934b` before the last Markdown-only commit.

Planted mutants (disposable clone of `06c934b`, restored after each; clean control rc 0 before and after):

| Mutant | Verdict |
|---|---|
| M1: 06 put back to the round-1 text (29 operations, no `SHIFT_R`) | `make inventory` rc 2: `says 29 operations, the enum declares 30`; `table lacks SHIFT_R` |
| M2: the `inventory` row dropped from 09 §7 | rc 2: ``table lacks `inventory` `` |
| M3: a target added to the Makefile's `check:` rule | rc 1: ``table lacks `spelling` `` |
| M4: an enum member `OP_ROT_L = 5'd30` added | rc 1: `says 30 operations, the enum declares 31`; `table lacks ROT_L` |
| M5: `OP_SHIFT_R` written `5'h1d` | rc 1: `unparsed enum member: 30 OP_ names, 29 in the form OP_X = 5'dN` |
| M6: 06 heading says 31 operations | rc 2: `says 31 operations, the enum declares 30` |
| self-test | 25 cases (12 inventory, 8 µISA, 4 target-table, 1 missing defining file): 22 planted faults, each caught by name, and 3 clean controls |

Consumer gates (a script and the Makefile changed, so required): milan-fpga cloned in scratch at PR #805's head `e06ade312a80eb578579365134ab797cda90622b`, whose gptp-processor gitlink is `f97c18035be6` (the adoption). The assignment text says to move the gptp-processor gitlink; as in round 1 the gitlink moved is protocol-processor's, the submodule this repository is (gptp-processor is a different repository and stays at f97c1803). `git -C protocol-processor rev-parse --show-toplevel` was checked first. Gitlink staged in scratch only, never committed or pushed. 24 submodule-reading gates (docs, doc paths, submodule docs and its self-test, boundary diagram, hygiene, py/sh/cpp/sv idiom, TODO ownership, naming, fail-fast, test evidence, control flow, cohesion, RTL and SoC source lists, `pp_srcs`, port contracts, CI scope): identical verdicts with the processor at base and at head. 22 pass; `check_submodule_docs.py` and `submodule_boundaries.gen.py --check` fail identically at both, because the consumer's pin record names the adopted pin `f65c8ff7`. The Python idiom gate scans the new script (517 modules at head against 516 at base) and every metric is unchanged.

## Not done, and why

- The full `make -C tb/nvm_port figures` run: over one foreground command's time on this host; equivalence of its README inputs shown instead.
- Diagram 22 and the RTL and test comments: outside this lane's remit; findings above.
- "Closes #210": not used, because the 156 R-labels remain.
