[R743] NEGATIVE - exact head 18a4dc1fcf91528a52737d5ea830b5acd5d543c4

# R743-1: independent review of protocol-processor PR #211 (issue #210, part of milan-fpga #797)

- Head `18a4dc1fcf91528a52737d5ea830b5acd5d543c4`, tree `7cdbc61bb2296f923585b42d3cd0a01baf6d3991` (verified in the review clone). Base `main` `a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645`. Whole-PR review of 5 commits, 36 files: Markdown, `Makefile`, `scripts/check-doc-inventory.py` (new), `scripts/check-links.py`.
- Inputs read, in order: the repository has no `AGENTS.md` or `CONTRIBUTING.md`; `docs/README.md`; issue #210's body and milan-fpga #797's body (no comments); PR metadata through the two permitted calls only; the full diff and history; the standards texts (IEEE 1722.1-2021, IEEE 1722-2016, IEEE 802.1Q-2014, Milan v1.2); the RTL, generators and suites at the head; the published author evidence at milan-fpga `9167129d` `review-evidence/pp210-r1`; exact-head hosted check-runs (read only).
- Verdict basis: three MINOR findings, each a numeric or normative statement this PR adds on a page its own inventory marks current, contradicted by the tree. Every gate passes, every planted fault is caught, and build outputs are unchanged. The verdict is NEGATIVE only because of those three statements.

## Findings

### R743-1-F1: MINOR. README says two pages are kept for provenance, but three are
- **Lenses:** Docs.
- **Where:** `README.md:28-29` (added by this PR): "two pages are kept for provenance only and say so in a banner."
- **Evidence:** `docs/INVENTORY.md` "Retired" lists three `superseded` rows. Each page opens with a quoted banner that the gate accepts: `IEEE_1722_1_Hardware_Protocol_Processor.md:4`, `docs/10_RESOURCE_AND_EFFORT.md:1`, `docs/history/02-class-a-word-stream.md:4`. `docs/README.md:44` also calls the history page "provenance only".
- **Impact:** this count is on the start-here page, which the inventory marks current, and the tree contradicts it. A new reader is told there are two retired pages when there are three. It breaks #210's acceptance "no document marked current contradicts the code". It is a count in prose, so under the "unsure, MINOR" rule it is not RESIDUE.
- **Required outcome:** say "three pages", or name them (the concept sketch, `docs/10_RESOURCE_AND_EFFORT.md`, `docs/history/`).
- **Verification:** the sentence's count equals the number of `superseded`/`obsolete` rows in `docs/INVENTORY.md`, and `make check` passes.

### R743-1-F2: MINOR. The new 02 summary says every clock-domain crossing is the integrator's; one is inside the processor
- **Lenses:** Docs, RTL.
- **Where:** `docs/architecture/02_interfaces.md:8-9` (added): "All of them are in the one core clock domain: every clock-domain crossing, the MAC FIFOs included, is the integrator's (§2)."
- **Evidence:** the page's own §2 rule 3 (`02_interfaces.md:121-124`) says "`identify_button_i` is the one input whose 2-flop synchronizer is inside the core, and only with P-EN-IDENTIFY-NOTIFICATION = 1". The RTL agrees: `hdl/aecp/KL_aecp_notify.sv:1031-1032` has `(* ASYNC_REG = "TRUE" *) btn_q1_r`, `btn_q2_r`. The integrator guide also agrees: `docs/guides/integrator.md:39` says "No clock-domain crossing lives inside this processor but one", and `:45-50` says `identify_button_i` "may come straight from a pin".
- **Impact:** the summary of the specification of record states a contract (where the crossings are, and that every face is in the core domain) that the RTL and the same page's §2 contradict. This is a normative statement on a current page, not wording.
- **Required outcome:** for example: "...all in the one core clock domain, and every clock-domain crossing is the integrator's (the MAC FIFOs included) but one: with P-EN-IDENTIFY-NOTIFICATION = 1, `identify_button_i` passes the processor's own two-flop synchroniser (§2 rule 3)."
- **Verification:** read the summary against §2 rule 3 and `KL_aecp_notify.sv:1031`; `make check` passes.

### R743-1-F3: MINOR. The new `tb/nvm_port` summary says `make` runs three builds; it runs seven
- **Lenses:** Docs, Tests.
- **Where:** `tb/nvm_port/README.md:6` (added): "`make` runs three builds".
- **Evidence:** `tb/nvm_port/Makefile:20` sets `FUZZ_TMOS = 1 2 3 37` and `:41` sets `BUILDS = $(words 1 2 3 $(FUZZ_TMOS))`, which is 7. The `run` target builds the suite at three bounds and the fuzz harness at four, and refuses unless it sees 7 tallies. My run at the head printed 393, 393, 393, 10, 10, 10, 10, for a total of 1,219 (`receipts/suites-head-2/nvm_port.log`). The README body (`:12-20`) itself describes three suite builds and then the fuzz harness at four bounds.
- **Impact:** a figure-like count in the summary of a page marked current disagrees with the Makefile and with the run. The page's figure gate does not see it (it contains no digits), so no gate holds it.
- **Required outcome:** for example: "`make` builds and runs the suite at three deadline bounds and the randomized harness at four".
- **Verification:** the count matches `BUILDS`, and `make -C tb/nvm_port figures` stays green in CI.

### R743-1-RES1: RESIDUE. Three workflow-lane labels remain, and the PR body implies they were removed
- **Lenses:** none (wording in prose and in the PR body; no measurement or clause is affected).
- **Where:** `docs/00_MILAN_COMPLIANCE_REVIEW.md:577` "(lane C6)", `:588` "(lane C6)", and `tb/pp_top/README.md:2728` "## Lane C6: notifications and identify ...". All three predate this PR, and the PR adds no lane label. The PR body's table says the lane labels in "00, 01, 06, 08, 09 and seven suite READMEs" became plain references, and "Not fixed here" lists only the R-labels.
- **Exact fix:** delete " (lane C6)" at 00:577 and 00:588, and retitle `tb/pp_top/README.md:2728` to "## Notifications and identify (issues #54, #58, #80, #86)" (no link targets `#lane-c6…`; checked with `git grep '#lane-c6'`). Alternatively, add the three to the PR body's "Not fixed here".

### R743-1-RES2: RESIDUE. The glossary says it carries no values, but one entry carries one
- **Lenses:** none (wording).
- **Where:** `docs/GLOSSARY.md:5` "A definition here never carries a value", and `:87` "make a simulated millisecond cost a hundred clocks". The value is accurate per `docs/guides/hdl-engineer.md:281-282`.
- **Exact fix:** in `:87` write "make a simulated millisecond cost far fewer clocks", keeping the link to HDL engineer guide §7.

### Suggestions (do not affect the verdict)
- **R743-1-S1 (Robustness, gate):** `check-doc-inventory.py` does not compare a row's link target with its backticked path. Probe P11: a `tb/prng/README.md` row linking to `../tb/ucpu/README.md` passes both `inventory` and `links`. Requiring `link == relpath(path, docs/)` would close this.
- **R743-1-S2 (Robustness, gate):** the `*.md` pathspec is case-sensitive. Probe P12: a planted `docs/NOTES.MD` passes. No such file exists today.
- **R743-1-S3 (gate):** the `stale` status says "the evidence names the tracking issue", but the gate does not require an `#N` in the evidence. No row is `stale` today.
- **R743-1-S4 (Conformance, citation):** "Milan wins (Milan §5.5.2.1)" in `docs/GLOSSARY.md:17` repeats the existing `README.md:88`, `docs/README.md:150-151`, `01_overview.md:55`, `00:47` and `00` §8 item 12. Milan v1.2 §5.5.2.1 grants precedence over ACMP only. The general rule is Milan §4.2 ("This specification supersede the standards referenced below", which takes in Section 5 through §4.2.4). Citing §4.2 beside §5.5.2.1 would make the citation exact. The principle itself holds, so this is not a contradiction.

## Lens results

| Lens | Result | Evidence |
|---|---|---|
| Conformance | CLEAN | 31 statements checked against the clause text and the RTL (table below). Every clause correction the PR makes is right: 1722.1-2021 has no §9.2.1.1 (9.2.1 is "Overview" only), and §9.3.2.6 gives 250 ms timeout and 240 ms respond. 802.1Q-2014 has no §35.2.2.7.4 or §34.6.1.1; §35.2.2.7.2/Table 35-3 has Ignore 0, AskingFailed 1, Ready 2, ReadyFailed 3, which `srp_pkg.sv:57-62` matches; §34.6.1 is Talker behavior (per-stream idleSlope). REBOOT text matches §7.4.43/.1/.2 and Figure 7-68. The F2 statement is a CDC contract, not a clause, so it is scored under RTL and Docs. S4 is a citation-precision suggestion only. |
| RTL | UNCLEAN (F2) | The 01 §5 shutdown text matches `protocol_processor_top.sv:2027` (`adp_enable_w = entity_enable_i && restore_done_o && !rbt_adp_off_w`), `restore_done_o` latching once per boot (`KL_acmp_nvm_shadow.sv:371`), and `KL_adp_engine.sv:645-694` (DEPARTING on enable fall only). No `shutdown` port exists. F07.1 lists exactly the two `$readmemh` ROMs in `hdl/` (`KL_aecp_ucpu.sv:150`, `KL_pp_acmp_listener.sv:423`). No RTL consumer of a dispatch ROM, a response-size ROM or `P-DESCR-IMAGE-BYTES`. F08.4's 68 and 91 match `pp_pkg.sv:228-233` and are graded by `tb/timer_map` (`want[]` at `sim_main.cpp:315`). `resp_mem_wr_{done,ready}_i` are top ports (`:386`, `:390`). `ctr_word_o` = 32 carries `counters_valid` (`:425`). F2: the 02 summary contradicts `KL_aecp_notify.sv:1031`. |
| Robustness | CLEAN | The inventory gate fails closed: a row not in link form becomes `NO ROW`, a missing inventory is refused, git failure raises. All 15 plants are caught with rc 1 (`make` rc 2). Exact-head anchor cross-check against an independent GitHub-rule model: 665 anchor links, 0 disagreements at head; at base it names exactly the 16 links the PR fixes. The duplicate-heading `-1` gap can only refuse valid links, as the PR states. S1 and S2 are open-ended limits, not defects of the stated scope. |
| Tests | UNCLEAN (F3) | All 34 suites other than `pp_top` and `srp_top` run at head, rc 0, with every tally equal to its inventory row (24 + 10, `receipts/suites-head*/summary.txt`). That includes the five re-measured ones (prng 76, dispatch 211, desc_store 586, timer_map 1,360, dyn_state 118 = 62 + 56) and srp_admission 991,231. The new `tb/dyn_state/README.md` groups A to H match `sim_main.cpp`'s check labels and `KL_aecp_dyn_state.sv`'s ports (`dbg_oob_o`, region 0x2 valid). `tb/dyn_state/shape_tally.txt` is rewritten to the same bytes. F3: the `nvm_port` summary's build count is wrong. |
| Docs | UNCLEAN (F1, F2, F3) | 63 Markdown files, 63 rows, and the gate passes. Start-here path, glossary, summaries and banners are present. Labels: R-label occurrences go 158 to 156 (the two in 09 removed, none added), A523 goes 17 to 0, and no new lane, review, tool, model, host or device name appears in added lines. Remaining: RES1, RES2. |

## Spot-checked statements (31)

| # | Statement (page) | Checked against | Result |
|---|---|---|---|
| 1 | 01 §5: SHUTDOWN is the fall of ADP's effective enable (requested enable, or REBOOT); no shutdown port | top `:2021-2027`, ports, `KL_adp_engine.sv:645-694` | holds |
| 2 | 01 F01.5 P-TIMER-SLOTS points at 08 §5 (68, 91) | `pp_pkg.sv:228-233`, `tb/timer_map` | holds |
| 3 | 01 F01.5 P-DISPATCH-ROM-W has no RTL consumer | `grep -ri dispatch_rom hdl` empty; 06 §8.1 | holds |
| 4 | 02 F02.10 FourPackedEvent at 802.1Q §35.2.2.7.2, Table 35-3; codes 0 to 3 | 802.1Q-2014 text; `srp_pkg.sv:57-62` | holds |
| 5 | 802.1Q-2014 has no §35.2.2.7.4 | 35.2.2.7 has .1, .2, then 35.2.2.8 | holds |
| 6 | granted idleSlope at §34.6.1 (no §34.6.1.1) | 802.1Q-2014 §34.6.1 Talker behavior; 34.6.2 follows | holds |
| 7 | 03 §7.1: `T-BUDGET-AECP-WC` is 10,000,000 clocks, inside §9.3.2.6's `T-AECP-RESP` | F08.1 rows 24, 50 (240 ms; ≤ 100 ms); 1722.1-2021 §9.3.2.6 | holds |
| 8 | 1722.1-2021 has no §9.2.1.1 | 9.2.1 Overview has no subclause | holds |
| 9 | REBOOT: ENTITY 0, MEMORY_OBJECT target, ENTITY_LOCKED/ACQUIRED, notification on success | 1722.1-2021 §7.4.43, .1, .2, Figure 7-68 | holds |
| 10 | 07 F07.1: µcode ROM + listener transition ROM; dispatch and response-size ROMs specified, none ships | `$readmemh` sites; 06 `:1477`, `:1690` | holds |
| 11 | 00 §8 item 8: counters from the integrator's `ctr_*` face, `counters_valid` included | top `:422-430`; 06 `:746` | holds |
| 12 | integrator §4.2 port names | top `:386`, `:390` | holds |
| 13 | HDL guide §9: two-stage direct decode (pop, then registered re-dispatch) | 06 §8.1 `:1690-1700` | holds |
| 14 | HDL guide §9: F03.1 says it predates the move; `P-DESCR-IMAGE-BYTES` has no consumer | 03 `:25`; grep empty | holds |
| 15 | 08 F08.1 MRP values from Milan Table 4.3 | Milan v1.2 Table 4.3 | holds |
| 16 | 02 summary: every CDC is the integrator's | 02 §2 rule 3; `KL_aecp_notify.sv:1031` | **F2** |
| 17 | 02 summary: class B includes gPTP, AVTP, mclk, ctr read faces | 02 §4 "Class B", §4.3 to §4.6 | holds |
| 18 | 05 summary: 8-state listener machine; §5.1 boot restore; §6bis talker | F01.4 Δ15; 05 `:153`, `:408` | holds |
| 19 | 10 summary: 802.1Q §10, §11, §35; Milan §4.2.7, §4.3, §4.4; §6.5 Δ13 | standards' TOCs; 10 `:735`; F01.4 Δ13 | holds |
| 20 | 04 summary / engine: Milan §5.6.1 boot gate, §5.6.3, §5.6.4 | Milan v1.2 §5.6.1 "start ADP only when ready" | holds |
| 21 | glossary: bind/unbind/probe = CONNECT_RX/DISCONNECT_RX/CONNECT_TX (Milan §5.5.2.2) | Milan v1.2 §5.5.2.2 | holds |
| 22 | glossary: registry {EID, MAC, port} (Milan §5.3.4.2); PAAD (Milan §1) | Milan v1.2 §5.3.4.2, §1 | holds |
| 23 | glossary: entity_id §6.2.2.7; ADPDU §6.2, ACMPDU §8.2, AECPDU §9.2; Stream I/O §7.2.6; §7.5 | 1722.1-2021 headings | holds |
| 24 | glossary: cdl at 1722-2016 §4.4.5.4; PDU = cdl + 12 | 1722-2016 §4.4.5.4 | holds |
| 25 | glossary: DR2a/DR2c/DR3a in the consumer's `SAVED_STATE_MATERIALIZATION.md` §15.1 | milan-fpga `1e80128f`: §15.1 "Manager decision register" | holds |
| 26 | dyn_state README Milan cites §5.3.5.1, §5.3.7.1, §5.3.7.6, §5.3.8.1, §5.3.8.7, §5.3.11.1, §5.3.12, §5.4.2.5 | Milan v1.2 headings and text | holds |
| 27 | docs/10 banner: its §10 advised against the SRP substitution; §1b is the measured outcome | docs/10 `:69`, `:600-625` | holds |
| 28 | 00 "How to read": §5 gaps, §6 matrix F00.1, §7 to §8 live | 00 headings `:84`, `:375-377`, `:566`, `:598` | holds |
| 29 | README: two pages kept for provenance under a banner | INVENTORY Retired (three rows), three banners | **F1** |
| 30 | nvm_port summary: `make` runs three builds | Makefile `BUILDS` = 7; run log | **F3** |
| 31 | 09 §7 lists every `make check` target, `inventory` included | Makefile `check:` versus the 09 table rows (12 of 12) | holds |

Plus every "run N checks" figure in the inventory, checked by running 34 suites.

## Gates (receipts `receipts/gates-{base,head}/`)

| Gate | Base `a9e84b66` | Head `18a4dc1` |
|---|---|---|
| `make check` (pinned wavedrom 2.0.3.post3, mmdc 11.16.0) | 0 | 0; `inventory: 63 Markdown files, OK`; selftest 12 cases OK |
| `python3 scripts/gen_matrix.py --check` | 0 | 0 |
| `python3 scripts/check_upc_map.py` | 0 | 0 |
| `python3 scripts/check_m9_opcodes.py --selftest`, then plain | 0, 0 | 0, 0 |
| `./scripts/lint_hdl.sh` (Verilator 5.050, identity printed `Verilator 5.050 2026-07-01 rev v5.050`) | 0 | 0 |
| 34 suites (all but `pp_top`, `srp_top`) | not needed: no tb or hdl byte changed | 34 of 34 rc 0, tallies as listed |
| hosted, exact head (read only) | n/a | docs-gates success (runs 41043142178, 41043150656), portability success (both); suites `in_progress` when last read (11:11 UTC) |

## Planted faults (`receipts/plant-probes.txt`, script `scripts/plant_probes.sh`, disposable clone of the head)

| Plant | Gate result |
|---|---|
| P1 stale entry: row for `tb/gone/README.md` | `NO FILE`, rc 1 |
| P2 stale entry: `tb/prng/README.md` deleted, row kept | `NO FILE`, rc 1 |
| P3 missing file: untracked `docs/architecture/12_new.md` | `NO ROW`, rc 1 |
| P4 missing file: staged `tb/new_suite/README.md` | `NO ROW`, rc 1 |
| P5 superseded page marked current | `BANNERED`, rc 1 |
| P6 current page given a superseded banner | `BANNERED`, rc 1 |
| P7 row not in link form | `NO ROW`, rc 1 |
| P8 status `fresh` / P9 empty evidence / P10 duplicate row | `BAD STATUS` / `NO EVIDENCE` / `DUPLICATE ROW`, rc 1 each |
| P11 row links to another existing page (limit) | passes inventory and links (S1) |
| P12 `docs/NOTES.MD` (limit) | passes (S2) |
| L1 broken file link / L2 broken anchor / L3 old collapsed anchor re-planted | `missing target` / `missing anchor` / `missing anchor`, rc 1 each |
| L4 `make inventory`, `make check` with a planted page | rc 2, rc 2 |
| End state | head `18a4dc1`, only the untracked venv symlink |

## Build and ROM outputs (`receipts/build-outputs-*.sha256`, `receipts/build-outputs-diff.txt`)

At base and head, in clean clones: `gen_ucode.py` → `ucode.hex` and `gen_ltn_rom.py` → `ltn_rom.hex` are byte-identical (`49a993be…`, `23cc67ee…`). `MODULE_MATRIX.md` regenerated is identical. Verilator `--cc` of `protocol_processor_top` gives 21 C++/header files that are identical; the `.mk` differs only in its temp work-dir name and is identical once that name is mapped. `check_aecp_commands.py --write` leaves 06 byte-equal to the committed 06 in each tree. By construction: the only non-Markdown changes are the `Makefile` (an `inventory` target added to `check` and `.PHONY`, plus a comment), a new gate script, and the link checker's slug function. No generator, RTL, tb source or workflow reads any of them (`grep` over `*.py`, `*.sh`, Makefiles, `*.yml`, `*.tcl`). The single `tb/nvm_port/README.md` change is a 5-line insertion with no digit and no table row, so the figure gate's README input set is unchanged.

## Ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | 1722.1-2021 §6.2, §7.2.6, §7.4.43, §9.2, §9.3.2.6; 1722-2016 §4.4.5.4, Annex B; 802.1Q-2014 §10, §11, §34.6.1, §35.2.2.7, Table 35-3; Milan v1.2 §1, §4.2, Table 4.3, §5.3.x, §5.5.2.x, §5.6.x; every clause the diff adds or corrects | R743-1 | 18a4dc1fcf91528a52737d5ea830b5acd5d543c4 |
| RTL | UNCLEAN (F2) | `protocol_processor_top.sv`, `KL_adp_engine.sv`, `KL_acmp_nvm_shadow.sv`, `KL_aecp_notify.sv`, `pp_pkg.sv`, `srp_pkg.sv`, ROM sites, top ports | R743-1 | 18a4dc1fcf91528a52737d5ea830b5acd5d543c4 |
| Robustness | CLEAN | `scripts/check-doc-inventory.py`, `scripts/check-links.py`, `Makefile`; 15 plants plus 2 limit probes; independent anchor model over 665 links | R743-1 | 18a4dc1fcf91528a52737d5ea830b5acd5d543c4 |
| Tests | UNCLEAN (F3) | 34 suites run at head; `tb/dyn_state` README/suite/RTL; `tb/nvm_port` Makefile and README; inventory tallies | R743-1 | 18a4dc1fcf91528a52737d5ea830b5acd5d543c4 |
| Docs | UNCLEAN (F1, F2, F3) | all 36 changed files; `docs/INVENTORY.md` against 63 files; glossary; summaries; banners; label, privacy and tool scan of 678 added lines | R743-1 | 18a4dc1fcf91528a52737d5ea830b5acd5d543c4 |

## Real limits
- `tb/pp_top` and `tb/srp_top` were not run (run time), and neither were the CI mutation campaigns or `make -C tb/nvm_port figures`. Their inputs are unchanged by construction (no hdl or tb source byte changed; the nvm_port README change has no figure shape). The hosted suites job, which runs them, was still in progress at exact head when last read.
- The full IEEE and Milan texts were read only at the clauses listed. The sweep's "every clause number exists" claim for unchanged pages was sampled, not exhaustively re-proven.
- The anchor cross-check uses an independent approximation of GitHub's slug rule, not GitHub's renderer.
- Consumer (milan-fpga) gates were not re-run here. The author's published receipts claim them.
- No physical calibration or hardware was involved. No manager source bank ran at this head, and none is claimed.

## Pending manager duties
- Hosted and act acceptance at the exact head, including the `suites` job (it was `in_progress`; it carries `make -C tb/nvm_port figures` and the mutation campaigns).
- The current-dev merge candidate (source base `a9e84b66`, live dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`) with the builder and native banks at the merge turn.
- Carry RES1 and RES2 to the residue checklist.

## Prior public review findings
Read only after this verdict and ledger were on disk: see the section below.

R743-1 FINISHED
