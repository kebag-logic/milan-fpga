# [A708] protocol-processor #210, documentation sweep: handoff

Status: REVIEW READY. Local branch `docs-sweep`, not pushed; no PR opened.

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Base: main `a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645`
- Head: `18a4dc1fcf91528a52737d5ea830b5acd5d543c4` (5 commits)
  - `cf8dfc2` Documentation sweep: inventory and its gate, glossary, start-here path and summaries; stale values, citations, tallies, anchors and labels corrected (#210)
  - `04b2e9a` Grade the inventory gate's self-test on a fixture of its own, so a fault in the real inventory is named by the main check
  - `aa92526` Annotate, document and wrap the inventory gate to the consumer's Python idiom rules
  - `f67c4c8` List only the ROMs that ship in F07.1, and narrow the HDL guide's on-chip image row to F03.1
  - `18a4dc1` Say what the inventory checked on docs/README.md, which points at 09 §7 rather than listing the gates
- Diff: 36 files. Markdown, plus three docs-gate files: `Makefile` (new `inventory` target in `check`), `scripts/check-doc-inventory.py` (new), `scripts/check-links.py` (slug rule fixed). No RTL, generator, generated file, test source or workflow changed (`git diff a9e84b66 HEAD -- hdl tb/*/*.cpp tb/*/*.sv tb/*/*.py tb/*/Makefile .github` is empty).
- TAKEN: issue #210 comment 6519117148. REVIEW READY: comment 6520341258.
- Precondition (milan-fpga #797 plan comment 6518880512, lane P: "after processor #203 merges"): #203 is closed and merged at the base (PR #209).

## Acceptance (issue #210)

| Item | State | Evidence |
|---|---|---|
| every document has a status | met | `docs/INVENTORY.md`, 63 rows, held by `make inventory` (in `make check`) |
| no document marked current contradicts the code or a clause | met as far as checked | the checks below; every contradiction found is fixed in the docs or listed under findings (those are RTL and test comments, not docs) |
| the start-here path exists | met | `README.md` "Start here" (numbered path), `docs/GLOSSARY.md`, `docs/INVENTORY.md` |
| the docs gates pass | met, with one gate shown by equivalence | every gate rc 0 at base and head; the `tb/nvm_port` figures gate could not finish in one foreground command on the loaded host (see gates) |

Rules of #210 not fully met: 156 R-numbered review labels remain in 9 suite READMEs (finding F7). Because of that and the figures gate, the PR body says "Refs #210", not "Closes".

## How the docs were verified

Scratch scripts, not committed, run over every tracked Markdown file at base and head:

1. Links and anchors under GitHub's own heading-anchor rule (the repository gate collapsed whitespace and dropped `_`, so it passed 16 links GitHub cannot follow; fixed).
2. Every backticked repository path exists (hits left are paths in the consumer repository, named as such).
3. Every `*_i`, `*_o`, `*_P`, `*_C` identifier a page uses is declared or used in `hdl/` or `tb/`.
4. Every clause and table number cited under Milan v1.2, IEEE 1722.1-2021 and IEEE 802.1Q-2014 exists in the extracted standard text; 6 did not (fixed in docs, or findings in comments). A sample of 43 Milan clause numbers was read for topic (F01.4 deltas, F08.1 rows): all match.
5. F01.5 values compared with the RTL declarations (`protocol_processor_top`, `pp_pkg`, `ucpu_pkg`, `KL_pp_trace_ring`, `KL_mrp_strip`, `KL_acmp_talker`, `KL_acmp_nvm_shadow`, `KL_aecp_nvm_writer`, `KL_aecp_notify`, `KL_pp_originator`); F08.1 MRP and AECP timing values read in Milan Table 4.3, Table 5.26 and IEEE §9.3.2.6.
6. Every suite except `pp_top` and `srp_top` run at base (niced) and its tally compared with its README.
7. Status statements ("landed", "not implemented", REBOOT) checked against the merged #203 work.

## Inventory

Every Markdown file at head. Status vocabulary and audiences are defined in `docs/INVENTORY.md`; the "sweep checks" are items 1 to 5 above.

| File | Purpose | Audience | Describes | Status | Evidence |
|---|---|---|---|---|---|
| `README.md` | what the processor is, the start-here path, repository map, how to build and check | new reader | the repository | current | sweep checks; start-here path added in this sweep |
| `docs/README.md` | documentation conventions: reading order, ID registries, figure rules, citation rules, editing workflow | author | `docs/`, and the gates through 09 §7 | current | sweep checks; its editing workflow now names the inventory row a new page needs |
| `docs/GLOSSARY.md` | defined terms, each pointing at its home | new reader | the vocabulary of every page | current | written in this sweep; each cited clause number read in its standard |
| `docs/INVENTORY.md` | this page: every Markdown file and its status | author, new reader | every Markdown file | current | held by `make inventory` |
| `docs/guides/README.md` | the three task guides and the diagram inventory | new reader | `docs/guides/`, `docs/diagrams/` | current | sweep checks |
| `docs/guides/hdl-engineer.md` | conventions, block structure, shared-service contracts, running the suites, known spec and tree divergences | HDL engineer | `hdl/`, `tb/`, `scripts/` | current | sweep checks; §9 divergence table re-read against the RTL: the shutdown row is resolved by 01 §5 and removed, the dispatch row reworded to the engine banner, the on-chip image row narrowed to F03.1 (F07.1 is already current) |
| `docs/guides/integrator.md` | the instantiation contract: ports, parameters, clocking and reset, memory masters, tie-offs, bring-up order | integrator | `hdl/top/protocol_processor_top.sv` | current | sweep checks; `make params` holds its parameter table to the top; two shortened port names spelled out |
| `docs/guides/operator.md` | what appears on the wire, what a controller sees, the snapshot and control windows, bring-up ladder | operator | the side port (`KL_pp_side_port`), the wire behaviour | current | sweep checks |
| `docs/architecture/01_overview.md` | scope, top level, operational model, Milan deltas (F01.4), parameter master table (F01.5) | new reader, HDL engineer | the whole processor; `protocol_processor_top` parameters | current | sweep checks; F01.5 compared with the top, `pp_pkg`, `ucpu_pkg`, `KL_pp_trace_ring`, `KL_mrp_strip`, `KL_acmp_talker` and the NVM producers: the stale timer-slot example removed (08 §5 owns it), P-DISPATCH-ROM-W marked as having no RTL consumer, the shutdown model corrected to the enable's fall (`protocol_processor_top.sv:2027`); F01.4 clause topics read in Milan v1.2 |
| `docs/architecture/02_interfaces.md` | every external contract, interface classes A to F, the status dictionary F02.10 | integrator, HDL engineer | the top's ports | current | sweep checks; two 802.1Q citations corrected (§35.2.2.7.2, §34.6.1) |
| `docs/architecture/03_packet_engine.md` | the shared RX and TX datapath: validation, slots, dispatch, scoreboard, originator, TX arbitration | HDL engineer | `hdl/packet_engine/` | current | sweep checks; a citation of a clause IEEE 1722.1-2021 does not have corrected to `T-BUDGET-AECP-WC` and §9.3.2.6 |
| `docs/architecture/04_adp_engine.md` | discovery: the advertise and talker-discovery state machines | HDL engineer, compliance reviewer | `hdl/adp/KL_adp_engine.sv` | current | sweep checks |
| `docs/architecture/05_acmp_engine.md` | Milan connection management: the listener machine, its transition matrix F05.3, the stateless talker | HDL engineer, compliance reviewer | `hdl/acmp/` | current | sweep checks; anchors repointed to GitHub's rule |
| `docs/architecture/06_aecp_engine.md` | AEM and MVU commands, the command master table F06.14, registry, notifications, lock, µcode | HDL engineer, compliance reviewer | `hdl/aecp/` | current | sweep checks; F06.14 is held to the command table by `make aecpcmd` |
| `docs/architecture/07_memory_maps.md` | the entity model, records, NVM layout and flows, side-port map | HDL engineer, integrator | `hdl/aecp/desc/`, the NVM producers, `KL_pp_side_port` | current | sweep checks; F07.1's ROM node corrected: no dispatch or response-size ROM ships (06 §8.1) |
| `docs/architecture/08_timing.md` | every timing constant (F08.1), timer hardware, budgets, the timer slot map F08.4 | HDL engineer, compliance reviewer | `hdl/common/KL_pp_timer_service.sv`, `pp_pkg::pp_timer_map()` | current | sweep checks; F08.4's 68 and 91 slots recomputed from `pp_pkg.sv`; F08.1 clause topics and the MRP and AECP values read in Milan v1.2 Table 4.3 and IEEE 1722.1-2021 §9.3.2.6 |
| `docs/architecture/09_verification.md` | test categories, traceability, the documentation gates (§7), the suites and their evidence (§8) | verification | `tb/`, `scripts/` | current | sweep checks; §7 lists every `make check` target, `inventory` included |
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
| `tb/nvm_port/README.md` | the class F NVM port, its deadline, resets and device models | verification | `KL_pp_nvm_port` | current | run 393 checks in each of three builds, as stated; its figures gate (`make -C tb/nvm_port figures`, CI) holds the rest |
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

## Changes (file:line at head, reason)

Facts corrected:

| Where | Change | Reason |
|---|---|---|
| `docs/architecture/01_overview.md:178` | P-TIMER-SLOTS: the "66; 89" example removed, pointer to 08 §5 | stale copy of a value: `pp_pkg.sv:228-234` gives 68 and 91 (the MAAP pair added 2); 08 §5 already said 91; single-source rule |
| `docs/architecture/01_overview.md:181` | P-DISPATCH-ROM-W marked "no RTL consumer" | no dispatch ROM or generator ships (`KL_aecp_engine.sv:18-27`, 06 §8.1) |
| `docs/architecture/01_overview.md:124` | Shutdown: the SHUTDOWN event is the fall of ADP's effective enable (requested enable or REBOOT); no shutdown port | `protocol_processor_top.sv:2027`, `KL_adp_engine.sv:100`; the HDL guide listed this as a divergence |
| `docs/architecture/03_packet_engine.md:466` | "IEEE §9.2.1.1 gives an AECP command 100 ms" replaced by `T-BUDGET-AECP-WC` inside §9.3.2.6's `T-AECP-RESP` | IEEE 1722.1-2021 has no §9.2.1.1 and no 100 ms AECP limit; §9.3.2.6 is 240 ms; 100 ms is F08.1's design budget |
| `tb/pp_top/README.md:1743`, `tb/resp_buf/README.md:62` | same citation fix | same |
| `docs/architecture/02_interfaces.md:582` | 802.1Q §35.2.2.7.4 to §35.2.2.7.2, Table 35-3 | 802.1Q-2014 has no §35.2.2.7.4; FourPackedEvents is §35.2.2.7.2 |
| `docs/architecture/02_interfaces.md:587`, `docs/architecture/10_srp_engine.md:53` | 802.1Q §34.6.1.1 to §34.6.1 | no §34.6.1.1; per-stream idleSlope is in §34.6.1 Talker behavior |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:609` | decision item 8: masks are carried from the integrator's `ctr_*` face, no processor ROM | contradicted 01 §7 and 06 §6.6 (no plain-IEEE profile ROM exists) |
| `docs/architecture/07_memory_maps.md` F07.1 | ROM node lists the µcode and listener transition ROMs only | no dispatch or response-size ROM ships |
| `docs/guides/integrator.md:224` | `wr_done_i`/`wr_ready_i` spelled `resp_mem_wr_done_i`/`resp_mem_wr_ready_i` | no port has the short names (`protocol_processor_top.sv:386,390`) |
| `docs/guides/hdl-engineer.md:315` and §9 | shutdown row removed (fixed in 01 §5); dispatch row says "two stages" as the engine banner does; image row narrowed to F03.1 | rows no longer true |
| `tb/prng/README.md:5` | 57 to 76 checks | measured at base |
| `tb/dispatch/README.md:9` | 179 to 211 checks | measured at base |
| `tb/desc_store/README.md:5` | 584 to 586 checks | measured at base |
| `tb/timer_map/README.md:4` | 1187 to 1360 checks | measured at base |
| 16 links in 00, 01, 02, 05, 06, 08, integrator, `tb/acmp_talker` | anchors repointed to GitHub's form (`#42-maap--address-allocation`, `#6bis-talker-side--stateless-responder`, `#51-persisted-vs-volatile-normative-set--req-per-001002`) | they passed the repository gate but do not resolve on GitHub |

New and retired:

| Where | Change | Reason |
|---|---|---|
| `README.md:17` | numbered start-here path: README, glossary, the guide for your job, the architecture; pointer to the inventory | #210 scope: start-here README |
| `docs/GLOSSARY.md` (new) | defined terms, each with its clause or home section; no values | #210 scope: defined terms |
| `docs/INVENTORY.md` (new) | 63 rows: purpose, audience, describes, status, evidence | #210 acceptance: every document has a status |
| `tb/dyn_state/README.md` (new) | the one suite without a README; what it proves, groups A to H, tally 118 | HDL guide §6 says every suite carries one |
| `docs/10_RESOURCE_AND_EFFORT.md:4` | "Historical, superseded" banner, pointers to `syn/ooc/README.md` and the architecture | pre-build planning analysis; its §10 advised against the SRP substitution that has since happened |
| `README.md` repository map, `docs/README.md:15`, `docs/README.md:191` | the planning page marked superseded; glossary and inventory linked; "add a row with the page" in the editing workflow | |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:7` | "How to read this page today": §1 to §4 review the superseded concept document, §5 to §8 are live | the page mixes both |
| "In short." paragraphs | 02, 03, 04, 05, 06, 07, 09, 10; integrator, operator and HDL engineer guides; `tb/pp_top`, `tb/nvm_port`, `tb/srp_top` READMEs (each under the H1) | #210 scope: a short summary at the top of each long page |
| `scripts/check-doc-inventory.py` (new), `Makefile:74`, `docs/architecture/09_verification.md:138` | `make inventory`, in `make check`: one row per Markdown file, no row without a file, status vocabulary, evidence filled, banner agrees with status; `--selftest` plants 11 faults in a fixture | #797 scope 6: a cheap freshness gate |
| `scripts/check-links.py:22` | slug follows GitHub: every space one hyphen, `_` kept, inline HTML dropped | the old rule passed links GitHub cannot follow |

Workflow labels removed (#210 rule: no lane or review labels):
- `docs/00_MILAN_COMPLIANCE_REVIEW.md` ("lane C6" x2), `docs/architecture/01_overview.md:189`, `06_aecp_engine.md` ("Identify (lane C6...)"), `08_timing.md:61` and `:72`, `09_verification.md:204`, `:242`, `:290`, `:586`, `:656`;
- `tb/acmp_talker`, `tb/adp_engine`, `tb/name_state`, `tb/pp_top`, `tb/acmp_nvm`, `tb/maap`, `tb/srp_top` READMEs: "lane P1/C5a/C6/C7", "saved-state lane N", "the lane head/base", "consumer lane", and the lane label `A523` (now "lockstep").

## Findings the docs cannot fix

| # | Where | Against | Which is wrong |
|---|---|---|---|
| F1 | `hdl/top/protocol_processor_top.sv:666` (comment on `srp_granted_slope_bps_o`) | cites 802.1Q §34.6.1.1; 802.1Q-2014 has no such clause; per-stream idleSlope is §34.6.1 | the RTL comment; no behaviour |
| F2 | `hdl/srp/KL_srp_admission.sv:10` (banner) | same §34.6.1.1 | the RTL comment |
| F3 | `hdl/aecp/KL_aecp_resp_buf.sv:32` (banner) | "IEEE 1722.1 §9.2.1.1 gives an AECP command 100 ms": no §9.2.1.1 and no 100 ms limit in IEEE 1722.1-2021; §9.3.2.6 gives 240 ms; 100 ms is `T-BUDGET-AECP-WC` (F08.1) | the RTL comment |
| F4 | `tb/pp_top/sim_main.cpp:3737` (comment) | same as F3; the check's bound, 10,000,000 clocks, equals `T-BUDGET-AECP-WC` at `P-CLK-HZ`, so the check itself is right | the test comment |
| F5 | `tb/acmp_talker/sim_main.cpp:99` (comment) | cites 802.1Q §35.2.2.7.4; FourPackedEvents is §35.2.2.7.2 (Table 35-3) | the test comment |
| F6 | `tb/dyn_state/shape_tally.txt` | tracked, and rewritten by every `make` in that suite (`tb/dyn_state/Makefile` `run`), so a run that changes a count dirties the tree | test infrastructure hygiene; not a doc |
| F7 | 156 R-numbered review labels in suite mutation records: `tb/pp_top` 44, `tb/srp_top` 44, `tb/acmp_nvm` 26, `tb/nvm_port` 20, `tb/aecp_notify` 8, `tb/srp_decoder` 8, `tb/maap` 3, `tb/aecp_cmds` 2, `tb/adp_engine` 1 | #210 rule "no lane or review labels in text" | the docs; not rewritten here because each label keys a planted mutant to the review that wrote it and nothing in the tree resolves it to a link; the owner should choose the replacement reference (for example the review comment URL). `tb/nvm_port`'s also sit inside its figures gate's claims |
| F8 | `scripts/check-links.py` | GitHub suffixes duplicate heading anchors with `-1`, `-2`; the gate does not | the gate; it can only refuse a valid duplicate-heading link (none exists today), never pass a broken one |
| F9 | `docs/diagrams/03-shared-datapath.svg` (F03.1 export) | still draws the descriptor image on chip; the page says so under it | the diagram; redrawing is outside Markdown |

## Gates

Processor gates on clean clones (base `a9e84b66`, head `18a4dc1`), never piped:

| Gate | Base rc | Head rc |
|---|---|---|
| `make check` (lint, wavedrom-check, links, matrix, reqtags, modmatrix, params, aecpcmd, ids, figures, inventory at head, stale) | 0 | 0 |
| `python3 scripts/gen_matrix.py --check` | 0 | 0 |
| `python3 scripts/check_upc_map.py` | 0 | 0 |
| `python3 scripts/check_m9_opcodes.py --selftest` | 0 | 0 |
| `python3 scripts/check_m9_opcodes.py` | 0 | 0 |
| `./scripts/lint_hdl.sh` | 0 | 0 |
| `git diff --check a9e84b66 HEAD` | n/a | 0 |
| `make -C tb/nvm_port figures` (CI suites job) | not run | not completed: stopped at 560 s on a host at load 18 with the lane niced. Its README-derived inputs (claim coverage, arm rows, matrix rows, every claim's matches, every figure shape) are identical at base and head (claim coverage empty), and its measured half reads only RTL and suite sources, which are unchanged; the only edit to that README is a summary with no figure shape |

Suite tallies at base (`make` in each suite, niced): every suite but `pp_top` and `srp_top` (stopped at 280 s) ran rc 0; tallies are in the inventory rows.

Planted mutants (clean clone of head `18a4dc1`, each restored after):

| Mutant | Gate | Result |
|---|---|---|
| M1 the `tb/prng` row deleted from the inventory | `make inventory` | rc 2 (script rc 1): `NO ROW: tb/prng/README.md` |
| M2 a new `tb/planted/README.md` with no row | `make inventory` | rc 2: `NO ROW: tb/planted/README.md` |
| M3 the superseded concept page's row marked current | `make inventory` | rc 2: `BANNERED: IEEE_1722_1_Hardware_Protocol_Processor.md ...` |
| M4 a link to `02_interfaces.md#42-maap-address-allocation` (the old collapsed form) | `scripts/check-links.py` | head rc 1 (`missing anchor`); the same plant at base rc 0, which is the defect fixed |
| self-test | `scripts/check-doc-inventory.py --selftest` | 12 cases (clean fixture plus 11 planted faults), all as expected |

Consumer gates (required: non-Markdown files changed). milan-fpga at PR #805's head `e06ade31` (carries the gPTP `f97c1803` adoption), submodules initialised, the `protocol-processor` gitlink staged in that scratch clone at base `a9e84b66` and then at head `18a4dc1` (`gptp-processor` kept at `f97c1803`); never committed or pushed:

| Consumer gate | Processor at base | Processor at head |
|---|---|---|
| `python3 scripts/docs_check.py` | 0 | 0 |
| `python3 scripts/check_doc_paths.py` | 0 | 0 |
| `python3 scripts/check_submodule_docs.py` | 1 | 1 |
| `python3 scripts/check_submodule_docs.py --selftest` | 0 | 0 |
| `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 1 | 1 |
| `python3 scripts/check_hygiene.py --check` / `--selftest` | 0 / 0 | 0 / 0 |
| `python3 scripts/check_py_idiom.py` / `--selftest` | 0 / 0 | 0 / 0 (was 1 at `04b2e9a`: fixed in `aa92526`) |
| `python3 scripts/check_sh_idiom.py`, `check_cpp_idiom.py`, `check_sv_idiom.py` | 0, 0, 0 | 0, 0, 0 |
| `python3 scripts/check_todo_ownership.py` / `--selftest` | 0 / 0 | 0 / 0 |
| `python3 scripts/measure_naming.py --check`, `measure_fail_fast.py --check`, `measure_test_evidence.py --check` | 0, 0, 0 | 0, 0, 0 |
| `python3 scripts/measure_control_flow.py --selftest`, `measure_cohesion.py --selftest` | 0, 0 | 0, 0 |
| `python3 scripts/check_rtl_source_lists.py`, `check_soc_sources.py`, `pp_srcs.py --check --selftest`, `check_port_contracts.py`, `ci_scope.py --selftest` | 0 each | 0 each |

The two rc 1 rows fail identically at base and head with the same two findings ("protocol-processor: documented pin differs from Git", the submodule boundary diagram stale): the consumer's pin page and diagram name `f65c8ff7`, so any gitlink move fails them until the consumer's adoption change regenerates them. They are not caused by this change. Not run: the consumer's RTL lint and simulation workflows (no RTL changed).

## Notes for the reviewers

- `scripts/check-links.py`'s slug change is a behaviour change of an existing gate; M4 is its mutant.
- The inventory's "current" means: passed the sweep checks above, plus what its evidence cell says. Pages too long to read line by line here (06, `tb/pp_top`) were checked mechanically and by sample, not sentence by sentence.
- Scratch, toolchains and clones are under the scratch directory, not here.
