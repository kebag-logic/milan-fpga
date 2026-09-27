# Round 5 handoff

Role: author [A354]. Issue #502; PR #579.
Branch: `502-pending-live-write`.
Starting head: `92c6154a17d1f1192f20a3a642e6a01b616afb67`.
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/502#issuecomment-5854533678
Review: https://github.com/kebag-logic/milan-fpga/pull/579#issuecomment-5854531311

Status: all three assignment items complete in one local commit, `90ab4a3da5b676f90b768b4f22b77ce7d0bd911d`. All assigned gates return rc 0. The worktree is clean; the commit has not been pushed.
Both pages were read from first line to last, including tables, historical evidence and proposed behavior. Searches supplement those reads; they do not define their coverage. Section ranges below refer to the edited files. Container headings have their own rows so every section is accounted for.

## Delivered behavior examined

- `hdl/milan/KL_pp_shadow.sv:925-957`: dynamic-state level, reduced binding vector, accepted name/map pulse and its reset-only history feed the backend.
- `hdl/milan/milan_datapath.sv:4245-4271`: the map pulse shares the store-change comparisons and requires an active phase-5 beat; unchanged maps raise nothing.
- `hdl/milan/KL_nvm_backend.sv:745-796`, `:857`, `:1124-1133`: producer input is registered; pending also includes open records; whole-record completion closes its record and sets dirty.
- Current PR body read directly. Its replacement will describe Round 5 and distinguish prior-head evidence.

## Changes

1. R329-4 F1: section 13 now states the current four-term pending equation and defines its live pulse.
2. Full-read follow-through: current equations, pulse/history retirement, historical provenance and proposed D3 timing are explicit. Reset/terminal summaries now follow existing section 5.3 and backend ownership rules, including pending clearing after all records close when no producer source remains. No contract or implementation behavior is changed.
3. R329-4 S1/S2: exact-map-record diagnostic uses its case tag, including successful reads and preloaded baselines in both directions; the CSR comment is rewrapped. Payloads, predicates and expected values are unchanged.

## Full read: snapshot ownership

File: `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` (1938 lines).

| Section | Lines | Disposition |
|---|---|---|
| Preamble | 1-166 | Clarified historical evidence provenance; current #502 note points to section 6.1. D1 binding export, historical D2 marks, current live-write reporting and absent D3 writer stay distinct. |
| Contents | 167-190 | Navigation read in full; pending entry points remain sections 3, 6, 11 and 13. |
| 1. Context | 191-218 | Historical #418/#420 observations and requirement authority; no current name/map trigger claim. |
| 2. What reproduces at the current source | 219-246 | Retained historical execution at 36ee8a37/8f2f58fb; failing tracked-build results are not current #502 results. |
| 3. Decision | 247-316 | Rules 5 and 9 read. Qualified terminal pending by remaining sources and section 5.3; no permanent-pending promise after record closure. |
| 4. Record ownership: the open vector | 317-371 | Retained open-vector rules: grants open, accepted RELOAD closes all, whole-record completion closes one; no device-idle clearing. |
| 5. The capture handshake and state machine | 372-373 | Container heading; all four subsections read below. |
| 5.1 The control face | 374-430 | Retained pending publication at PP_NVM_STAT[22], distinct from load-pending [3]; pend OR open records agrees with backend. |
| 5.2 The capture state machine | 431-486 | No new producer composition; capture and load state transitions leave producer pending ownership intact. |
| 5.3 The window load: RELOAD checked by the backend | 487-815 | Corrected refused-RELOAD wording: ownership is unchanged, rather than necessarily all open. W4 and the ordering-dependent row already allow pending to fall while dirty/backed prevent durability. |
| 5.4 Reset, and the identity across a reset | 816-897 | Corrected reset-vector summary to include whole-record closure as well as accepted RELOAD; reset and identity history retained. |
| 6. Next-state functions, and the separate pending bit | 898-948 | Retained backend equations: registered pend_i OR open vector. Load-pending is a separate boot flag. |
| 6.1 The pending bit (owner decision) | 949-1012 | Read every source, pulse, reset and clear rule against KL_pp_shadow: current sources and pulse bypass match. Qualified dictionary reset wording consistently with section 4. |
| 7. The writer sequence | 1013-1139 | Writer reads load-pending for boot/restart and commits on dirty, not producer pending. O1-O4 do not replace live-write reporting. |
| 8. The round-2 concern, answered | 1140-1157 | Historical capture counterexamples; no current name/map pending composition. |
| 9. Ordering coverage | 1158-1235 | Retained dated model coverage and shipping suite description; D1 E3 and status-bit equality have no late-mark trigger claim. |
| 10. The four outcomes of a record operation | 1236-1251 | Retained pending for open records on error, silence and withheld readiness; independent of the name/map pulse. |
| 11. Persistent-field materialization | 1252-1288 | Clarified original tracing versus subsequent updates. Current table uses actual phase-5 map writes and accepted name writes, sticky until reset; no record writer exists for either. |
| 12. The section 9.2 revocation discrepancy | 1289-1337 | Retained historical revocation discrepancy and resolved alarm behavior: binding give-up can clear its source only while alarm revokes backed. |
| 13. Donor dependencies, each its own scope | 1338-1415 | Replaced stale D2 equation with all four current terms and the live-write equation. D2 original mark-trigger use remains explicitly historical; marks delimit completion. |
| 14. Old writer on new gateware, and the reverse | 1416-1437 | Retained old/new writer compatibility scenario: no RELOAD leaves initial open records; no name/map pending-source change. |
| 15. Alternatives rejected | 1438-1459 | Retained rejected alternatives and dated mutation evidence, including composite dirty and edge detection; none is presented as current pending glue. |
| 16. Per-record reporting versus one summary bit | 1460-1483 | Retained decided summary bit and diagnostic open vector; durable requires pend 0. |
| 17. Consequences | 1484-1538 | Corrected terminal-state consequence: record closure can clear pending with no producer work; dirty and writer retirement still prevent durability. D3 absence remains explicit. |
| 18. Cost | 1539-1690 | Historical area/load-pending costs and newer capture measurement; no name/map pending-source composition. |
| 19. The executable model and its omissions | 1691-1745 | Historical model and omissions at 8f2f58fb; transcribed glue and evidence totals do not claim current #502 execution. |
| 20. UNRESOLVED | 1746-1856 | Items 1-3 distinguish missing D3, historical D2 marks, current live acceptance and D1. Other pending mentions concern dated mixed-build or load/restart cases, not a current mark trigger. |
| 21. Traceability | 1857-1938 | Historical design-review traceability, pending-bit equality and boot status findings; no current producer-source replacement. |

## Full read: materialization

File: `docs/design/SAVED_STATE_MATERIALIZATION.md` (2249 lines).

| Section | Lines | Disposition |
|---|---|---|
| Preamble | 1-101 | Clarified historical evidence source and scope of proposed sections 3-13; explicit #502 notes identify current reporting. |
| Contents | 102-120 | Navigation read in full; clear rule, stages and historical reproduction remain distinct. |
| 1. Context | 121-180 | Now spells all four current pend_i terms and the name/map pulse equation; direct pulse covers acceptance and history holds until reset. |
| 2. What reproduces at the current source | 181-256 | Read historical K10/K12 mark-tail failures and current #502 explanation end to end; current pulse/history, no-change controls and missing materialization match delivered behavior. |
| 3. Decision | 257-375 | Proposal, not delivered RTL. Rule 6 now names both pulse and history replaced by per-record sources; rule 3 live triggers and rule 9 overflow pending remain proposed. |
| 4. Who writes: three candidates | 376-448 | Proposed alternatives and historical cost proxies; pending-from-write comparison does not claim that D3 shipped. |
| 5. Interfaces | 449-450 | Container heading; all three subsections read below. |
| 5.1 In the processor | 451-487 | Proposed writer snoops, phase-5 map beat, exports and dispatch ownership. Unchanged-map rewrite is explicitly a D3 limitation in section 15.11; current #502 uses actual changes. |
| 5.2 In the parent | 488-511 | Explicitly proposed final pend_i equation. Updated stage retirement to remove both current pulse and history, keeping D1 and proposed per-record reporting. |
| 5.3 In the firmware | 512-549 | Proposed firmware changes; no current pending-source equation or D2-bit claim. |
| 6. State machines and next-state functions | 550-551 | Container heading; all four subsections read below. |
| 6.1 The writer in service | 552-569 | Proposed flush and overflow states retain dirty while skipped; no current shipping pending trigger claim. |
| 6.2 The writer at boot: the restore transaction | 570-595 | Proposed restore state machine; no current pending-source composition. |
| 6.3 Next-state functions | 596-663 | Retained proposed per-record dirty/taint and pend_i equations, separate from current four-term equation in section 1. |
| 6.4 Two managers, one port | 664-715 | Proposed arbiter and permanent-silence containment retain outstanding work as pending; no port reuse or current D2 trigger claim. |
| 7. The clear rule | 716-717 | Container heading; both subsections read below. |
| 7.1 What clears, and when | 718-751 | Proposed pending-to-dirty relay is distinct from current reset-only levels; now explicitly retires the direct pulse as well as history. |
| 7.2 The orderings that carry the risk | 752-793 | Historical prototype ordering evidence: pending at power cut, IDENTIFY exclusion, group triggers and overflow; not current real-program results. |
| 8. Restore | 794-795 | Container heading; all nine subsections read below. |
| 8.1 The order | 796-894 | Proposed restore order and release boundaries; no current producer pending equation. |
| 8.2 What is proven cleared first | 895-956 | Historical cleared-first/trigger/replay controls and model limitations; no current D2-bit claim. |
| 8.3 The value rule of each group | 957-1022 | Proposed value and framing rules; no pending composition or live-write trigger change. |
| 8.4 Formats and maps are one decision | 1023-1063 | Proposed format/map coupling and synthetic versus shipping judge evidence; no pending composition. |
| 8.5 Names wait for the image walk | 1064-1076 | Proposed name replay after image walk; no current pending trigger statement. |
| 8.6 The restore is a transaction | 1077-1273 | Proposed transaction/rollback and historical faults; restored values are not live changes and introduce no new current pending source. |
| 8.7 What the status says after a restore | 1274-1300 | Proposed restore status and exclusion of restore writes from dirty; no current pending equation. |
| 8.8 Deadlines and containment | 1301-1437 | Proposed timeout/quarantine behavior: later unsaved changes stay pending while port debt lasts; prototype readings remain historical. |
| 8.9 The listener's admission (seam S4) | 1438-1615 | Pending timer expiries are listener scheduling state, not persistence pending. Proposed admission and historical L cases retained. |
| 9. What must not persist | 1616-1630 | Proposed trigger exclusions for lock, registry, IDENTIFY and unused groups; no late-mark pending claim. |
| 10. Stages | 1631-1724 | Current #502 release prerequisite is retained. Expanded stage migration to account for the direct pulse and history; proposed D3 stage claims remain separate. |
| 11. Alternatives rejected | 1725-1767 | Mark trigger explicitly rejected as historical pre-#502 behavior. Proposed overflow containment and other alternatives retained. |
| 12. Cost | 1768-1847 | Labelled derived D3 pending latency as proposed and contrasted its timing explicitly with current accepting-edge #502 reporting. |
| 13. Consequences | 1848-1911 | Clarified proposed pending-to-dirty transfer at record completion versus durable reading after acknowledgement; current unmaterialized sources remain reset-only. |
| 14. The executable model and its omissions | 1912-2039 | Historical prototype/transcribed-glue evidence and omissions; pending expiries are listener state. No new current RTL claim. |
| 15. UNRESOLVED | 2040-2172 | Read every unresolved item. Current #502 resolution, historical D2 parent use and proposed D3 amendment/retirement are distinct; unchanged-edit limitation belongs to D3. |
| 16. Traceability | 2173-2249 | Normative acceptance quotations and proposed amendments retained; historical review answers and issue statuses are explicitly labelled. |

## Whole-tree grep

Executed from the physical lane root, over the whole tracked tree:

```sh
git grep -n -E "pend_i *=|D2 sticky|D2 bit"
```

Initial result at `92c6154a` (rc 0):

```text
docs/design/SAVED_STATE_MATERIALIZATION.md:485:- `pend_i = (|nvm_unflushed_o) | d3_unflushed_o`. The `aecp_live_pend_r` bit
docs/design/SAVED_STATE_MATERIALIZATION.md:605:pend_i      = (OR of the binding manager's unflushed sinks) OR d3_unflushed
docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1355:  `pend_i = aecp_dyn_dirty_o | (|nvm_unflushed_o) | <the D2 sticky bit>`.
tb/verilator/nvm_backend/sim_main.cpp:441:  dut_->pend_i = 0;
tb/verilator/nvm_backend/sim_main.cpp:857:  dut_->pend_i = level;
```

After edits (rc 0):

```text
docs/design/SAVED_STATE_MATERIALIZATION.md:132:`pend_i = aecp_dyn_dirty_o | (|nvm_unflushed_w) | aecp_live_wr_w | aecp_live_pend_r`.
docs/design/SAVED_STATE_MATERIALIZATION.md:493:  `pend_i = (|nvm_unflushed_o) | d3_unflushed_o`.
docs/design/SAVED_STATE_MATERIALIZATION.md:614:pend_i      = (OR of the binding manager's unflushed sinks) OR d3_unflushed
docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1362:  `pend_i = aecp_dyn_dirty_o | (|nvm_unflushed_w) | aecp_live_wr_w | aecp_live_pend_r`.
tb/verilator/nvm_backend/sim_main.cpp:441:  dut_->pend_i = 0;
tb/verilator/nvm_backend/sim_main.cpp:857:  dut_->pend_i = level;
```

Disposition of every final hit:

- Materialization section 1: current four-term equation, matches the shadow.
- Materialization section 5.2: explicitly proposed final D3 equation.
- Materialization section 6.3: proposed next-state functions, not shipped composition.
- Snapshot ownership section 13: corrected current four-term equation.
- Backend harness line 441: initializes the direct unit-test input.
- Backend harness line 857: drives the direct unit-test input from its argument.
- No `D2 sticky` or `D2 bit` hit remains in the tracked tree.

## Gates

All commands run in the foreground from `$LANES/502-pending-live-write`, without pipelines. Each simulation gate has a 30-minute timeout. Documentation gates use the hash-locked Markdown packages from `tools/markdown/requirements.txt`, installed in a temporary environment outside the output directory. The system interpreter lacks cmarkgfm; that preflight was not counted as a gate result.

| Command | Result |
|---|---|
| `make -C tb/verilator/pp_shadow` | rc 0; 591 + 591 + 591 + 295 checks, zero failures |
| `make -C tb/verilator/pp_shadow pending-mutant` | rc 0; clean 295/0; historical mark mutant detected by 12 required K10/K12 failures |
| `python3 scripts/docs_check.py` | rc 0; 0 findings; 166 Markdown / 887 text files; 23/23 scrub controls; 4/4 routing arms |
| `GIT_DIR=/dev/null python3 scripts/docs_check.py` | rc 0; 0 findings; 166 Markdown / 901 text files; 22/22 scrub controls; inventory parity requires Git and is explicitly skipped |
| `python3 scripts/check_em_dash.py --base 831f94f4` | rc 0 at committed head; 292 added lines across 7 changed Markdown pages; 339/339 controls |
| `python3 scripts/check_doc_style.py` | rc 0; 22 current documents |
| `python3 scripts/gen_toc.py --check` | rc 0; 108 annotated contents lists; 17 pages below threshold |
| `python3 scripts/gen_toc.py --verify-anchors` | rc 0; 177 cross-page fragment links reproduced |
| `python3 scripts/check_doc_paths.py` | rc 0; 846 cited paths resolve |
| `git diff --check` | rc 0; worktree and 92c6154a..HEAD; no whitespace findings |

Simulation used system Verilator 5.052. Filtered receipts are `pp-shadow-summary.txt` and `pending-mutant-summary.txt`; full build logs remain temporary outside this packet. No simulation failure was suppressed. The mutant target intentionally requires its injected late-mark defect to fail.

The CSR code-token stream is identical to the starting head after comments are removed. The shadow, datapath and backend are byte-identical to the starting head. The harness diff changes diagnostic labels and their arguments only; stimuli, predicates, expected values and check counts remain unchanged. All gitlinks remain unchanged.

## Delivery

Commit: `90ab4a3da5b676f90b768b4f22b77ce7d0bd911d`.
Subject: `docs: reconcile pending sources across saved-state design pages`.
Exactly one commit follows the assigned starting head.
Replacement PR body: `PR-BODY.md`, complete and checked; live PR body was not edited.
Public review-ready comment: posted from `REVIEW-READY.md`.
URL: https://github.com/kebag-logic/milan-fpga/issues/502#issuecomment-5854606867
Independent review and merge validation remain separate responsibilities.

No push, PR creation or edit, merge, alternate checkout, hardware action or submodule edit was performed. This packet contains only small text artifacts. Build logs and the temporary documentation environment are outside it.
