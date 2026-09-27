# R329-5 sweep and full-read disposition at 90ab4a3da5b676f90b768b4f22b77ce7d0bd911d

Reference (RTL at head): `hdl/milan/KL_pp_shadow.sv:945-957`

    aecp_live_wr_w = aecp_name_wr_w | amap_live_wr_i
    nvm_pend_w     = aecp_dyn_dirty_o | (|nvm_unflushed_w) | aecp_live_wr_w | aecp_live_pend_r

`aecp_live_pend_r` is set by `aecp_live_wr_w` and cleared only by reset (`:947-954`).
The class-6/7 marks end on `unused_aecp_marks_w` (`:942-943`).
The map pulse is `milan_datapath.sv:4269-4271` (`amap_edit_live_wr_p`, phase 5 AND an
actual input or output change). The processor's map program skips `NVM_MARK` on an
unchanged map (`protocol-processor/hdl/aecp/ucode/gen_ucode.py:1789-1791`).

Legend: OK-CUR = correct current-state text; OK-HIST = labelled history;
OK-PROP = proposed D3 text, consistent with 5.2 / section 10 prose; OK-OTHER = unrelated
lexical match; SUGG = reported as a suggestion in REPORT.md.

## 1. Whole-tree pattern sweep (`sweep.sh`, `tree_grep_head.txt`, 27 lines)

| Hit | Disposition |
|---|---|
| CHANGELOG.md:45 late-mark mutant | OK-CUR (the historical mutant's name) |
| CHANGELOG.md:258 original mark trigger | OK-HIST (entry opens "Historical behavior before issue #502") |
| MATERIALIZATION.md:132 current `pend_i` | OK-CUR, equals RTL |
| MATERIALIZATION.md:220 class-6/7 marks as triggers | OK-HIST ("historical pre-#502 glue", :219) |
| MATERIALIZATION.md:252 late-mark mutant | OK-CUR |
| MATERIALIZATION.md:467 `amap_edit_req_o AND phase == 5` | OK-PROP (section 5.1, the proposed D3 writer's map trigger; UNRESOLVED 11 states its limit) |
| MATERIALIZATION.md:486 mark trigger | OK-PROP (amendment alternative) |
| MATERIALIZATION.md:493 final `pend_i` | OK-PROP ("proposed final composition") |
| MATERIALIZATION.md:614 `pend_i` in 6.3 | OK-PROP (section 6, proposed) |
| MATERIALIZATION.md:1698 stage 3 "sticky live-name/map bit is deleted" | SUGG (S1): incomplete against :495 and :1712 |
| MATERIALIZATION.md:1794 "sticky bit" | OK-OTHER (a diagnostic counter) |
| MATERIALIZATION.md:2072 mark-based pending | OK-HIST |
| MATERIALIZATION.md:2086 pre-#502 mark trigger | OK-HIST |
| OWNERSHIP.md:981 class-6/7 marks keep completion meaning | OK-CUR |
| OWNERSHIP.md:1362 current `pend_i` | OK-CUR, equals RTL (R329-4 F1 closed) |
| OWNERSHIP.md:1388 original parent use | OK-HIST ("Original parent use") |
| docs/testing/TESTING.md:268 late-mark control | OK-CUR |
| hdl/milan/KL_pp_shadow.sv:927 later marks delimit completion | OK-CUR |
| scripts/measure_test_evidence.py:601 late mark trigger | OK-CUR (mutation campaign text) |
| tb/verilator/milan_dp/sim_nxn.cpp:574 sticky bitmaps | OK-OTHER |
| tb/verilator/nvm_backend/sim_main.cpp:441, :857 `pend_i =` | OK-OTHER (harness input drive) |
| tb/verilator/pp_shadow/README.md:101 late-mark | OK-CUR |
| tb/verilator/pp_shadow/pending_mutant.py:4, :60, :64, :67 | OK-CUR (the historical mutant) |

## 2. Name/map pending statements outside the two pages (`tree_grep_namemap_pending.txt`, 39 lines)

Every hit read. Relevant ones:

| Hit | Disposition |
|---|---|
| CHANGELOG.md:35-45 (#502 entry) | OK-CUR |
| CHANGELOG.md:254-281 (0x0060 entry) | OK-HIST (labelled at :256-258) |
| docs/design/SAVED_STATE_FASTCONNECT.md:1371-1378 (12.2) | OK-CUR; :1380 "That manager" lost its antecedent in this PR: SUGG (S3) |
| hdl/common/csr/milan_csr.sv:180-199 | OK-HIST for 0x0060, then the #502 note at :194-196 |
| hdl/milan/KL_nvm_backend.sv:196-204 (`pend_i` contract) | OK-CUR ("accepted live name/map writes with their sticky history") |
| docs/reference/SUBMODULES.md:57-62 | OK-CUR |
| tb/verilator/milan_dp/sim_nxn.cpp:2324 | OK-CUR (label) |
| tb/verilator/nvm_cosim/cosim_top.sv:424-431 | OK-CUR |
| tb/verilator/pp_shadow/README.md:50-102 | OK-CUR |
| docs/reference/REGISTER_MAP.md:2239 `PP_STAT[11]` | not in the pattern list; read by hand. Generic ("a change the producer still holds"), unchanged by this PR, not stale against #502 |
| the rest (CI, builder, gPTP, AEM tools) | OK-OTHER |

## 3. Full read, `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` (1938 lines, every section)

| Section | Pending/trigger content | Disposition |
|---|---|---|
| Status block :25-37 | D1/D2 landed; #502 closes the tail window; names use accepted writes, maps actual phase-5 writes | OK-CUR |
| Preamble :95-102 | historical source labelled; current sources point to 6.1 | OK-CUR |
| 2 :219-245 | historical defects at 36ee8a37 | OK-HIST |
| 3 rule 9 :301-315 | pending follows remaining sources (6.1) | OK-CUR (matches backend `pend_w = pend_r | unres_w`) |
| 4 :317-370 | open vector | OK-CUR (backend `:1118-1138`) |
| 5.1 :402 | [22] = pend OR any record open | OK-CUR |
| 5.3 :514-517 | refused RELOAD retires nothing; open records and producer sources assert pending | OK-CUR (`open_n_w` unchanged on refusal) |
| 5.3 terminal rows :646-715 | [22] ordering-dependent; falls when nothing is open (W4, no producer work) | OK-CUR |
| 5.4 :827 | reset row: open at reset; WRITE completion or accepted RELOAD closes | OK-CUR (`:1128-1133`) |
| 6 :929-930 | `pend' = pend_i`; `nvm_pend = pend OR open` | OK-CUR (`KL_nvm_backend.sv:786, 790`) |
| 6.1 :949-1011 | five sources, pulse bypass, accepting edge, clearing rules | OK-CUR, equals RTL |
| 11 table :1262-1282 | name/map rows: #502 triggers | OK-CUR; :1280-1281 causal wording: SUGG (S4) |
| 13 D1 :1361-1365 | current composition | OK-CUR (R329-4 F1 closed) |
| 13 D2 :1388-1395 | original use labelled; #502 replaces it | OK-HIST / OK-CUR |
| 14 :1432-1436 | old writer keeps records open | OK-OTHER (DERIVED, not #502) |
| 17 :1506-1537 | no-load boot; D3 note | OK-CUR |
| 20 items 1-3 :1748-1761 | D2 item closed for reporting; #502 uses live acceptance | OK-CUR |
| 1, 7-10, 12, 15, 16, 18, 19, 21 | no present-tense statement of the composition or trigger beyond the above | OK |

## 4. Full read, `SAVED_STATE_MATERIALIZATION.md` (2249 lines, every section)

| Section | Pending/trigger content | Disposition |
|---|---|---|
| Status, preamble :6-63 | historical source labelled; #502 notes current; 3-13 proposed | OK |
| 1 :121-162 | current `pend_i`, pulse, history, table rows | OK-CUR, equals RTL |
| 2 :181-254 | tracked-glue table and mark tail labelled historical; #502 paragraph current | OK-HIST / OK-CUR (map mark skip verified in `gen_ucode.py:1789-1791`) |
| 3 rule 3 :274-283, rule 6 :302-305 | proposed triggers; proposed source retires pulse and history | OK-PROP |
| 4 :394, :447 | "pending from the write" for candidates | OK-PROP |
| 5.1 :465-467 | proposed snoop and map trigger | OK-PROP |
| 5.2 :490-496 | proposed final composition; stage 3 removes both terms | OK-PROP |
| 6.3 :613-614 | proposed next-state | OK-PROP |
| 7.1 :726-744 | proposed relay; replaces levels and the direct pulse | OK-PROP |
| 8.x, 9 | restore; no current composition statement | OK |
| 10 bullets :1664-1686 | #502 correction current; release prerequisite | OK-CUR |
| 10 table :1696-1698 | stage 1 loses dyn level; stage 2 "sticky pending source stops taking live name writes"; stage 3 "sticky live-name/map bit is deleted" | SUGG (S1): both rows omit the direct pulse the prose at :1707-1712 retires |
| 10 prose :1707-1712 | #502 pulse and history; stage 2 and 3 retirement | OK-CUR / OK-PROP |
| 11 :1731 | mark trigger rejected, historical | OK-HIST |
| 12 :1837-1838 | proposed latency; current covers accepting edge | OK |
| 13 :1850-1852 | D3 hand-off; current sources sticky | OK |
| 15 items 1, 3, 11 | amendment; #502 resolved; D3 limitation vs current actual-write trigger | OK |
| 16 :2238-2246 | round-one answers labelled historical | OK-HIST |

Result: no remaining current-state statement of the pending sources, the `pend_i`
composition, the trigger or the D2 bit contradicts the RTL at head. Three
wording points (S1, S3, S4) are reported as suggestions.
