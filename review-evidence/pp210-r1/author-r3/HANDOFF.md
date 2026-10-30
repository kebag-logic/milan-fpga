# HANDOFF: issue #210 round 3 (PR #211)

Status: REVIEW READY (posted on #210 as issuecomment-6523976813; TAKEN was issuecomment-6523622485).

- Base: main `a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645`.
- Round-1 head `18a4dc1fcf91528a52737d5ea830b5acd5d543c4`; round-2 head `0ea635ea22eeb6d97335c4e814eede1ac0d67ebc` (pushed as PR #211).
- Round-3 head: `6d1d038343e1f0a6b2027cce857a33528b8c2ac7` on local branch `docs-sweep`, four commits on top of `0ea635e` (no rebase, nothing pushed, PR #211 not edited). Delta: 11 files, +81/-42 (`git diff --stat 0ea635e..6d1d038`).
- Inputs read: the latest [A10] comment on #210 (issuecomment-6522013513) and the round-2 rule it applies (issuecomment-6521384962); report R743-2 (findings, prior-findings table, probes, suggestions); the round-2 handoff; `hdl/aecp/ucpu_pkg.sv:49-88`; the `run` recipes of `tb/acmp_nvm`, `tb/adp_engine`, `tb/dyn_state`, `tb/aecp_notify`, `tb/nvm_port`, `tb/pp_top`; `tb/srp_top/Makefile` `STORE_SHAPES`; `tb/srp_admission/Makefile` `shapes`; `tb/timer_map/shape_elab.sh` `LEGAL` and `timer_map_wrap.sv:106-108`; `tb/nvm_port/measure_figures.py` `MODELS` and `FIGURE_RE`; `hdl/packet_engine/KL_pp_nvm_port.sv:204-248` (state enum).

Commits (one-line subjects):

| Commit | Subject |
|---|---|
| `d77a94b` | Link the concept page banner's µISA row to the 06 µISA table instead of counting the operations |
| `208de11` | Link the guide, gate, build and shape counts in the README and suite READMEs to the files that define them |
| `506afbe` | Fail the inventory gate on a µISA count outside 06, and link the 09 and inventory build, model and guide counts |
| `6d1d038` | Hold the rest of 06's µISA heading line to the restated-count check |

## Round-3 items

| Item | Status | Change (file:line at head) | Evidence |
|---|---|---|---|
| R743-2 F1: the concept page's banner says "a different 29-operation ISA" | fixed by linking, and now gated | `IEEE_1722_1_Hardware_Protocol_Processor.md:18` now reads "a different ISA, the `ucpu_op_e` enum in `hdl/aecp/ucpu_pkg.sv`; 06 §8 (`#8-µcode-architecture`) lists it and records which sketch operations were dropped and why". No count. | `ucpu_pkg.sv:49-88` declares 30 members (`OP_NOP = 5'd0` to `OP_SHIFT_R = 5'd29`); 06 §8's heading and table are already derived from it (round 2). The link gate resolves the new anchor (`links: 1418 checked, OK`). |
| Recurrence guard for F1's class (R743-2's optional "add the banner to the derived checks") | done | `scripts/check-doc-inventory.py:112-131` (`UISA_COUNT`, `restated_uisa`), `:178`; self-test cases `:274-281`, `:297-300`; doc: module docstring `:14-20`, `docs/INVENTORY.md:12-14`, 09 §7 `inventory` row `:138` | `make inventory` now fails on any line that names the ISA and states an operation count (`29-operation ISA`, `30 ops`, `µISA (N operations)`) on a current or generated page, or inside a retired page's opening banner (its first block of `>` lines). Only the derived heading text on 06's own line is exempt; anything else on that line is held. A retired page's body is history and is not scanned (`docs/10_RESOURCE_AND_EFFORT.md:536` keeps its 2026-08-11 statement). Mutants below. |
| Sweep: other restated counts of a tree-defined set on the PR's changed pages | done; each restatement linked or reworded, one test-comment finding | see the sweep table | method below |

### Sweep method and scope

The PR's changed pages are the 33 Markdown files `git diff --name-only a9e84b66..0ea635e -- '*.md'` lists, plus the concept page F1 names. For each, I grepped the whole page for a number or number word followed by a set noun (operations, ops, builds, shapes, bounds, pages, guides, gates, targets, suites, models, states, configurations), and read every hit's context. I also read every line the PR adds that holds a number (`git diff -U0 a9e84b66..0ea635e`, 260 lines). A hit counted as a restatement when the set is enumerated in one file in the tree (a Makefile recipe or variable, an enum, a list constant, a directory) and the page states its size. Each such hit is now a link to that file, or a phrase that does not count ("every suite build", "the others"). The class has no other gate-cheap form, so only the µISA count got a new check.

Kept, with the reason:
- Measured tallies (`388 checks`, `62 at 2x2`, `33 AECP rows`, `40 of 40 KILLED`, the `tb/nvm_port` `N of 393` figures). These are measurements of a run, dated or re-measured, and the inventory's evidence column or the `tb/nvm_port` figures gate holds them. They are not restated definitions.
- Counts the sentence itself enumerates for a set the architecture defines (02 "six kinds of face: class A … class F", 04 "two hardwired state machines …: one advertise machine … and one talker-discovery machine", "the two main-memory masters", the "two-flop synchronizer" R743-1 F2 was settled on). The architecture is the specification of record for these. A change to them is an architecture change that rewrites the sentence.
- Counts a standard defines (05 "Milan's 8-state binding and probing machine", Milan v1.2 listener state machine; 06 `:548` "exactly two shapes", 1722.1-2021 Figure 7-40's two forms).
- Local references to items the same sentence names ("all three agree" for magic, version and checksum; `tb/pp_top` "in both builds" for the main and DV-fixture builds of section DV; ordinals "the second is 37").
- Dated history (`tb/pp_top/README.md:1310` "the 27 `hazards` arms" at a named change's head; `docs/10_RESOURCE_AND_EFFORT.md:536`).
- The method is a grep and a read, not a proof. The restated-count class outside the µISA is held by review, not by a gate.

### Sweep changes (file:line at head)

| File:line | Was | Now | Defining file |
|---|---|---|---|
| `README.md:23` | "you should not need the other two" | "the others" | `docs/guides/` |
| `README.md:37` | "Browsing all three … the three guides plus the diagram inventory" | "Browsing every guide … every guide plus …" | `docs/guides/` |
| `README.md:74` | `make check` comment listing six gates, a partial list of its prerequisites | "as CI runs them; 09 §7 lists each one" | `Makefile` `check:`, which 09 §7 is derived from |
| `docs/INVENTORY.md:48` | "the three task guides" | "the task guides" | `docs/guides/` |
| `docs/INVENTORY.md:110` | "run 393 checks in each of three builds" | "in each suite build" | `tb/nvm_port/Makefile` `run` |
| `docs/architecture/09_verification.md:341` | "every run of all three builds" | "every run of every build" | `tb/aecp_notify/Makefile:46-58` |
| `09_verification.md:376-379` | "against nine device models, four of which …, in three builds" | the models of `measure_figures.py`'s `MODELS` (linked), "some of which", "one build at each of … 100, 37 and 20 (its Makefile's `run`)" | `tb/nvm_port/measure_figures.py:500-513` (9 models, 4 handshake); `tb/nvm_port/Makefile:17-19, 45-51` |
| `09_verification.md:382-383` | `tb/acmp_nvm` "in two builds" | "in the builds of its Makefile's `run`" (linked) | `tb/acmp_nvm/Makefile:33-42` |
| `09_verification.md:389` | "in each of the twelve owed states" | "in each state of the port's machine in which the device owes an event" | `KL_pp_nvm_port.sv:204-219, 248` (four request, four wait, four data-phase states: 12) |
| `09_verification.md:392` | "the three builds" | "every suite build" | `tb/nvm_port/Makefile` `run` |
| `tb/acmp_nvm/README.md:8-9` | "388 checks over two builds" | "over the builds of the Makefile's `run`" (linked) | `tb/acmp_nvm/Makefile:33-42` (awk `NR != 2`) |
| `tb/adp_engine/README.md:6-9` | "1359 checks in two builds … summed over both" | "over the builds of the Makefile's `run` … summed over them" | `tb/adp_engine/Makefile:34-41` |
| `tb/dyn_state/README.md:12-13` | "builds and runs two shapes, 2x2 and the shipping 1x1" | "the shapes of the Makefile's `run`", tally "(62 at 2x2, 56 at the shipping 1x1)" | `tb/dyn_state/Makefile:19-28` |
| `tb/nvm_port/README.md:15` | "393 checks in each of three builds" | "in each suite build of the Makefile's `run`" (linked) | `tb/nvm_port/Makefile:45-48` |
| `tb/nvm_port/README.md:17` | "is built three times:" | "is built once at each of the Makefile's `TMO`, `TMO_ALT` and `TMO_MIN`:" | `tb/nvm_port/Makefile:17-19` |
| `tb/nvm_port/README.md:74` | "in each of the twelve states in which the device owes" | "in each state of `KL_pp_nvm_port.sv`'s machine in which the device owes" | `KL_pp_nvm_port.sv:204-219` |
| `tb/nvm_port/README.md:498-499` | "**the twelve owed states.** In each of the four requests, four waits and four data phases" | "**the owed states.** In each request, wait and data-phase state of the port's machine" | as above |
| `tb/nvm_port/README.md:812` | "requires all three builds green" | "requires every suite build green" | `tb/nvm_port/Makefile` `run` |
| `tb/srp_top/README.md:19-20`, `:641` | "FIFO arms at four shapes"; heading "Timer-arm FIFOs at four shapes (issue #230)" | "at each of the Makefile's `STORE_SHAPES`" (linked); heading "… at every store shape (issue #230)", and the one link to it updated | `tb/srp_top/Makefile:30` (`1x1 2x2 3x5 9x9`) |
| `tb/srp_top/README.md:710`, `:758` | "the admission suite … at its five shapes" (twice) | "at each of its Makefile's `shapes`" (linked); "at each of the admission suite's shapes" | `tb/srp_admission/Makefile:17-22` (N = 1, 2, 3, 5, 8) |
| `tb/timer_map/README.md:39` | "at ten shapes: `1×1` …" (it then named eight of the ten) | "at every shape of `LEGAL` in `shape_elab.sh` (linked), among them `1×1` …" | `tb/timer_map/shape_elab.sh:42` |
| `tb/timer_map/README.md:57`, `:93` | "both maps at the ten shapes" | "at the same shapes (`SI_TBL_C`, `SO_TBL_C`)"; "at gate 1's shapes" | `tb/timer_map/timer_map_wrap.sv:106-108`, the same ten pairs as `LEGAL` |

Each replaced count was true at `0ea635e`: the fix is the class, not a wrong value. The one exception is `tb/timer_map/README.md:39`, which named eight shapes under "ten". Its count was right, but the list was partial, and it now says "among them".

No other page links to the renamed `tb/srp_top` heading (`git grep timer-arm-fifos` finds only the updated link). The consumer's tree at PR #805's head does not link to it either.

## Findings the docs cannot fix (new this round, then carried)

| Where | What | Source line or clause | Which is wrong |
|---|---|---|---|
| `tb/pp_top/sim_main.cpp:20` (new) | "The suite builds six times (Makefile)" | `tb/pp_top/Makefile:171-189`: `run` builds `Vpp_top_sim`, `_vid`, `_idn`, `_line`, then `budget`, `timer-defaults`, `interfaces`, and its awk requires `NR != 7` | the test comment (a restated build count in a test source, outside this lane's remit) |
| `hdl/aecp/ucpu_pkg.sv:14`, `:48` (round 2) | comments say "the 29 operations of 06 §8" | the same file's enum declares 30 | the RTL comments |
| `docs/diagrams/22-aecp-descriptor-fetch.svg:155` (round 2) | "IEEE 1722.1-2021 §9.2.1.1 gives a controller 100 ms before it retries" | no §9.2.1.1; §9.3.2.6 | the figure (hand-authored SVG) |
| `tb/pp_top/notify_mutants.py:3`, `tb/pp_top/notify_phases.hpp:2` (round 2) | "lane C6" | #210 rule: no lane labels | the test comments |
| `hdl/top/protocol_processor_top.sv:666`, `hdl/srp/KL_srp_admission.sv:10` (round 1) | 802.1Q §34.6.1.1 | 802.1Q-2014 has §34.6.1 only | the RTL comments |
| `hdl/aecp/KL_aecp_resp_buf.sv:32`, `tb/pp_top/sim_main.cpp:3737` (round 1) | 1722.1 §9.2.1.1, 100 ms | §9.3.2.6; 100 ms is `T-BUDGET-AECP-WC` | the comments |
| `tb/acmp_talker/sim_main.cpp:99` (round 1) | 802.1Q §35.2.2.7.4 | §35.2.2.7.2, Table 35-3 | the test comment |
| nine suite READMEs' mutation records (round 1) | 156 R-numbered review labels | #210 rule: no review labels | the docs; the replacement reference is the owner's choice, hence "Refs #210" |

## Suggestions from R743-2

- S1 (a second `check:` line passes the target-table check): not taken. No such line exists in the tree. The [A10] round-3 comment does not name it, and it is the target table's limit, not this round's class.
- S2 (a stricter marker for a member's 06 spelling): not taken. The fallback fails closed, as the report says.
- S3 (name the commit mutants ran on): taken. Every mutant below ran on a disposable clone of exactly `6d1d038`.

## Gates (all foreground, logged, never piped; receipts in `receipts/`)

| Gate | Base `a9e84b66` | Head `6d1d038` |
|---|---|---|
| `make -j8 check` | 0 | 0; `inventory selftest: 30 cases, OK`; `inventory: 63 Markdown files, OK`; `links: 1418 checked, OK` |
| `python3 scripts/gen_matrix.py --check` | 0 | 0 |
| `python3 scripts/check_upc_map.py` | 0 | 0 |
| `python3 scripts/check_m9_opcodes.py --selftest`, then plain | 0, 0 | 0, 0 |
| `./scripts/lint_hdl.sh` (pinned Verilator 5.050) | 0 | 0 |
| `tb/nvm_port` figures gate, README-derived inputs (claims, their matches, figure spans, arm rows, matrix, size claims, coverage problems) | — | byte-identical to `0ea635e` (`receipts/nvm-inputs-{0ea635e,6d1d038}.json`). The full `make -C tb/nvm_port figures` was not run here (over one foreground command's time). CI runs it. |

The same set also passed at the intermediate head `506afbe` before the last commit.

Planted mutants (disposable clone of `6d1d038`, `scripts/plant.sh`, restored after each; `receipts/plant-6d1d038.txt`; clean control rc 0 before and after, end state `6d1d038` with an empty status):

| Mutant | `make inventory` |
|---|---|
| M1: the banner back to its `0ea635e` text ("29-operation ISA") | rc 2: `RESTATED: IEEE_1722_1_Hardware_Protocol_Processor.md:18` |
| M2: the banner states the true count ("30-operation ISA") | rc 2: same finding. A correct restatement is still a restatement |
| M3: a current page (`tb/ucpu/README.md`) says "the 30 operations of the µISA" | rc 2: `RESTATED: tb/ucpu/README.md:123` |
| M4: 06's heading line gets "(the µISA has 30 ops)" beside the derived heading | rc 2: `RESTATED: docs/architecture/06_aecp_engine.md:1427` (this mutant passed at `506afbe`; `6d1d038` closes it) |
| M5: M1 under the round-2 gate script (`0ea635e`) | rc 0: the round-2 gate does not see it (R743-2 probe L3), so the new check is what catches M1 |
| C1 (control): the retired page's body, `docs/10_RESOURCE_AND_EFFORT.md:536`, changes its historical count | rc 0: a retired body is history and is not held |
| self-test | 30 cases: 25 planted faults, each caught by name, and 5 clean controls (5 new: current page, retired banner, retired body, 06's heading clean, 06's heading line with an extra count) |

Consumer gates (a script changed, so required): milan-fpga cloned in scratch at PR #805's head `e06ade312a80eb578579365134ab797cda90622b`, submodules initialized. Its gptp-processor gitlink is `f97c18035be6` (the adoption) and stays there. The repository this lane changes is the protocol-processor submodule, so that is the gitlink moved, as in rounds 1 and 2. `git -C protocol-processor rev-parse --show-toplevel` was checked before every git command in it. The gitlink was staged in scratch only, never committed or pushed, and restored to the adopted pin `f65c8ff7` afterwards. Results for the 24 submodule-reading gates (`scripts/consumer_gates.sh`; `receipts/consumer-{base,head}.txt`): verdicts identical at base and at head. 22 pass. `check_submodule_docs.py` and `submodule_boundaries.gen.py --check` fail identically at both, because the consumer's pin record names `f65c8ff7`. `check_py_idiom.py` passes at head with the changed script, its metrics equal to base (no line over 120 columns; the new function is annotated and has a docstring).

## Not done, and why

- The full `make -C tb/nvm_port figures` run: over one foreground command's time. The equivalence of its README inputs is shown instead.
- `tb/pp_top/sim_main.cpp:20` and the carried RTL, test and SVG items: outside this lane's Markdown-and-docs-gate remit; findings above.
- "Closes #210": not used, because the 156 R-labels remain.

## Inventory at head (generated from `docs/INVENTORY.md` at `6d1d038`, 63 rows, held by `make inventory`)

| File | Purpose | Audience | Describes | Status | Evidence |
|---|---|---|---|---|---|
| `README.md` | what the processor is, the start-here path, repository map, how to build and check | new reader | the repository | current | sweep checks; start-here path added in this sweep; it links to the inventory's Retired heading rather than counting the retired pages |
| `docs/README.md` | documentation conventions: reading order, ID registries, figure rules, citation rules, editing workflow | author | `docs/`, and the gates through 09 §7 | current | sweep checks; its editing workflow now names the inventory row a new page needs |
| `docs/GLOSSARY.md` | defined terms, each pointing at its home | new reader | the vocabulary of every page | current | written in this sweep; each cited clause number read in its standard |
| `docs/INVENTORY.md` | this page: every Markdown file and its status | author, new reader | every Markdown file | current | held by `make inventory`, whose derived checks this page's summary lists |
| `docs/guides/README.md` | the task guides and the diagram inventory | new reader | `docs/guides/`, `docs/diagrams/` | current | sweep checks |
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
| `IEEE_1722_1_Hardware_Protocol_Processor.md` | the original concept sketch the compliance review read | compliance reviewer | nothing in the tree | superseded | banner points at `docs/architecture/`; its µISA row links 06 §8 instead of counting the operations |
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
| `tb/nvm_port/README.md` | the class F NVM port, its deadline, resets and device models | verification | `KL_pp_nvm_port` | current | run 393 checks in each suite build, as stated; the summary names the Makefile's `BUILDS` instead of counting the builds; its figures gate (`make -C tb/nvm_port figures`, CI) holds the rest |
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
