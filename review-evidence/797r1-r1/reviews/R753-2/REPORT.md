[R753] NEGATIVE - exact head 96bfa8513978ebc8c2f2e73bd98914b56e84bf12

Round R753-2, internal cleared-context review of kebag-logic/milan-fpga PR #825 (#797 lane R1), tree `816e6324dd4f2f38240faca3e85f547a85a32168`, round-2 delta against `a8bcfba9`, with live dev `1f29f189` merged.

## Verdict

Every finding of R753-1 is closed at its cause. The generator and its gate now hold: resets and access types agree with a simulation of `milan_csr` at shipping parameters, all 45 of my plants fail as required, and four mutants of the generator's guards are each killed by `--selftest`.

The verdict is NEGATIVE because five MINOR defects are open on the generated page and the design notes:

- Three statements do not describe the merged tree: when firmware writes `MAC_STATUS` (#70), what the entity-enable bits do (#70), and the REBOOT hold on `milan_mac_phy_crg_reset` (#787).
- The read-condition tables mix "and" and "or" without grouping on 23 rows of six registers, so their ordinary reading contradicts the RTL.
- The `ADP_CMD` rows, new in this delta, say the strobes store and read back. They read 0.

No RTL changed in this PR, so none of this is a hardware defect. All five are fixes to `scripts/register_descriptions.json` or the condition wording in `scripts/register_page.py`, plus the matching notes lines.

## Findings

### F1 - MINOR - Conformance, Docs - `MAC_STATUS` says firmware writes it only while the saved-state writer runs

- **Where:** `docs/reference/REGISTER_MAP.md:516` (from `scripts/register_descriptions.json:1268`); `docs/design/CSR_REGISTER_NOTES.md:164` and `:198`.
- **Authority:** #797 acceptance: no current document contains a statement the code contradicts. Round-2 check 3: the page describes the merged tree.
- **Evidence:** #70 merged in this delta. `sw/firmware/milan_baremetal/milan_baremetal.c:1099-1102` polls the PHY when `nvm_started` is 0 if `phy_live` is set, and `:1671` sets `phy_live` on every path through `nvm_boot()`. `:1676` installs the idle hook on the persistence-disabled path. The comment at `:1092-1094` states the rule.
- **Impact:** a reader on a persistence-disabled boot concludes `MAC_STATUS` keeps its reset value of `0x0000000D`. Firmware publishes the real link there. Commit `96bfa851` restated this sentence on the page after the merge.
- **Required outcome:** the page and both notes lines state that firmware publishes from MDIO on every boot path that reached `nvm_boot()`, and that nothing writes it after a CSR identity mismatch.
- **Verification:** re-read against the cited firmware lines; `--check` fresh.

### F2 - MINOR - Conformance, RTL, Docs - The page says either bit enables the entity; the fabric holds the enable until the restore releases it

- **Where:** `docs/reference/REGISTER_MAP.md:96`, `:1166`, `:1189`, `:4361` (from `scripts/register_descriptions.json:1689`, `:3864` and the two notes); `docs/design/CSR_REGISTER_NOTES.md:86`, `:348`, `:1229`.
- **Evidence:** `protocol-processor/hdl/top/protocol_processor_top.sv:2027` at the pin `a9e84b66`: `adp_enable_w = entity_enable_i && restore_done_o && !rbt_adp_off_w`. `hdl/milan/milan_datapath.sv:9586` also gates on `!amr_rs_hold_r`. `milan_baremetal.c:1846-1849`, new with #70: "The two writes REQUEST the enable; the fabric holds it until the restore walk releases it at COMPLETE or DEFAULTS, and a CLOSED restore holds it until reset." `docs/design/SAVED_STATE_MATERIALIZATION.md` section 5.3 gives the same formula.
- **Note on age:** the processor gate predates this delta (`f65c8ff7` already had it), and I did not raise it in R753-1. The merge changes what the statement depends on, because #70 made "request" the stated contract.
- **Impact:** software that reads `PP_CTRL[0]` as 1 is told the entity is enabled while ADP may still be held, or held until reset after CLOSED. This is the distinction #70 exists to report.
- **Required outcome:** the page and notes say the bits request the enable, and name the release and the CLOSED case. Exact wording for line 96: "`PP_CTRL[0]` or `ADP_CTRL[0]` requests the entity enable. The fabric holds it until the restore releases it."
- **Verification:** re-read against the cited lines; `--check` fresh; `check_doc_style.py` rc 0.

### F3 - MINOR - Conformance, Docs - The page omits #787's hardware set of `milan_mac_phy_crg_reset`

- **Where:** `docs/reference/REGISTER_MAP.md`, row `0xF0001800` (from `scripts/register_descriptions.json:1059`), and the `PHY_RESET_N` row (`:1297`), which calls this CSR the PHY reset that reaches the pin. `REBOOT` appears nowhere on the page, in the notes or in the descriptions file (grep count 0).
- **Authority:** #797 issuecomment-6522974767: side effects are stated in the field's row. Round-2 check 3 names #787's registers.
- **Evidence:** `sw/litex/milan_soc.py:2132`: `self.sync += If(reboot_phy_hold_sys, self.phy.crg._reset.storage.eq(1))`. `:2115-2123` and `docs/design/REBOOT_RESET.md:39` say an AECP REBOOT holds the PHY in reset through this storage, as a level that only rises, and that a CPU write in the same cycle clears it for that one cycle only. `milan_csr.sv` itself did not change in the merge, so this is the only register-visible effect of #787.
- **Impact:** the row describes a plain software RW bit. A reader debugging a link drop after REBOOT is not told the hardware owns this bit from that point.
- **Required outcome:** the row states that an AECP REBOOT sets the storage and holds it, and links `docs/design/REBOOT_RESET.md`.
- **Verification:** re-read against `milan_soc.py:2115-2132`; `--check` fresh.

### F4 - MINOR - Conformance, RTL, Tests, Docs - Read conditions lose their grouping, so the ordinary reading contradicts the RTL

- **Where:** "When / A read returns" tables on 23 rows of `STRMW_CTRL`, `STRMW_DMAC_LO`, `STRMW_DMAC_HI`, `STRMW_FMT_LO`, `STRMW_FMT_HI` and `STRMW_SRP` (`receipts/when_rows.txt`). Cause: `scripts/register_page.py:137-138` and `:150`, which flatten nested `&&` and `||` with no grouping. No selftest control covers grouping, so the closure of R753-1 F5 ("each condition in plain words") is checked only for the presence of words.
- **Evidence:** the first `STRMW_CTRL` row reads "the selected stream exists and no snapshot is running and `STRM_SEL[8]` selects a listener or the stream index `STRM_SEL[3:0]` is not 0 and `STRM_SEL[8]` selects a talker" and returns `i_tctx_rd_data`. Read normally, a listener at index 0 matches this row. My simulation with distinct constants on each input (`receipts/window_probe.txt`) reads `0x11111111`, the `i_lctx_rd_data` value. Rows 3 to 5 begin "the selected stream does not exist or ..." and return `aaf_ctrl[0]`; read normally, a missing stream returns that bit. Talker index 1 with `AAF_CTRL[0]` at 1 reads 0. The rows are true only with brackets the page does not print: `hdl/common/csr/milan_csr.sv:1130-1136` and `:2533-2542`.
- **Impact:** the table cannot be used without the RTL beside it, and a programmer would predict the wrong source for a window read.
- **Required outcome:** every row is unambiguous, by grouping or by flattening to one conjunction per row, and rows repeating a term are simplified. By the simulation, `STRMW_CTRL` is: listener, stream exists, no snapshot gives `i_lctx_rd_data`; talker above index 0, stream exists, no snapshot gives `i_tctx_rd_data`; talker index 0 gives `{31'd0, aaf_ctrl[0]}`; anything else gives 0. A selftest control holds it.
- **Verification:** `scripts/gen_window_probe.py` agrees with each row read as printed; the new control fails when grouping is removed.

### F5 - MINOR - Conformance, RTL, Docs - `ADP_CMD` rows say the strobes store and read back; they read 0

- **Where:** `docs/reference/REGISTER_MAP.md:1410-1411`, from `scripts/register_descriptions.json:1868-1869`. New in this delta: at `a8bcfba9` this register had no field text.
- **Evidence:** `hdl/common/csr/milan_csr.sv:1799-1802` are self-clearing strobes. `receipts/oracle_raw.txt` line for `0x640` reads `w1=00000000`. The type cell (`W1S`), the page's own "`W1S` command strobes read back 0" and `docs/design/CSR_REGISTER_NOTES.md` ("self-clear as before") all disagree with the row. "Reaches no logic" is correct: `hdl/milan/milan_datapath.sv:2780-2781` leaves both outputs open.
- **Impact:** a false readback claim on the field's own row, contradicted by the same row's type.
- **Required outcome:** exact text: "Inert strobe: self-clears and reads 0, and reaches no logic. Was advertise-now." and the same with "Was depart."
- **Verification:** re-read against the oracle line; `--check` fresh.

### SUGGESTIONS

- **S1:** the link-guard state diagram omits `SETTLE --> HOLD` on a re-death (`hdl/common/KL_link_guard.sv:291-294`), and the servo diagram omits the returns to `IDLE` (`hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:972`). Labels are checked against the RTL, but edges are not. Neither diagram claims to be exhaustive, so this is optional.
- **S2:** the `CHMAP_LOOP` sequence diagram reads the word with no busy poll, while the `STRM_SNAP` and `PP_STAT` diagrams show the poll loop. The notes carry the bound of 16 clocks.
- **S3:** the `milan_csr.sv` side effects name internal flops such as `pp_busy_r` and `lctx_wr_p_r`. A reader may prefer the outward effect, where one exists.

### RESIDUE

Purely wording; the manager carries these to the residue checklist.

- **R1:** five rows run a carried fragment into the generated sentence with no stop: lines 623, 992, 993, 2358 and 4420, for example "(hold MAC sys-side in reset) A write stores 0". Exact fix: end each fragment with a full stop in `scripts/register_descriptions.json`.
- **R2:** `MAC_STATUS` rows read "full_duplex." and "link_up." and "speed (0=10,1=100,2=1000)". Exact fix: "Full duplex.", "Link up.", "Speed: 0 = 10, 1 = 100, 2 = 1000 Mb/s."
- **R3:** the `CHMAP_LOOP[31:28]` row says only "Reserved." at reset `Dh`, while the page says reserved read-only bits read 0. Exact fix: "Reserved: 0 on a measurement, `Dh` in the poison." (`milan_csr.sv:1307-1309`).

## Round-1 findings at this head

| Finding | Status | Evidence at this head |
|---|---|---|
| F1 Reset says X on fixed words | Closed | `receipts/oracle_compare.txt`: the only "X, but no input moves it" row is `RST_EPOCH`, which has no reset clause, and its row says so. `CHMAP_LOOP` reads `0xDEADDEAD`. The 37 other lines are the expected behaviour R753-1 listed: window words write through to engines the harness does not model, `CHMAP_SNAP` moves after an arm, and `PP_*` write a different register than they read. Each row says so |
| F2 Window added under a green gate | Closed | `receipts/plant_probes.txt`: range window, literal arm and the 0x86C value all fail. Mutant `range_term` killed. 203 sections now, 0x86C has its own, 0 undocumented decoded words |
| F3 Flop reset drifts from the ROM | Closed | `mac_ifg`, `mac_ctrl`, `tcam_ctrl` and `LWSRP_LATENCY_RST_C` each refuse, rc 2. Mutant `flop_rom` killed, 6 controls fail |
| F4 Unread forms | Closed | `receipts/write_probe.txt`: both write forms exit 2 on `--write`. `CHMAP_LOOP` fields come from the RTL. The poison, `PPS_WIDTH` and snapshot plants fail |
| F5 Side effects outside the row | Closed for the rows; see new F4 and F5 | `receipts/row_audit.txt`: 0 empty of 498. `I2SPB_STAT` states the half-clear. `PP_SPADDR` states the doorbell. The `SCRATCH` doorbell plant fails and the regenerated row names it |
| F6 Gate skips 56% of the page | Closed | `receipts/notes_anchors.txt`: 0 `Note` tables. `check_doc_style.py` rc 0. Mutant `cell_cap` killed. `receipts/cell_stats.txt`: 18,500 words in cells, largest cell at the 200-word cap by the gate's own count |
| F7 Retained prose contradicted | Closed | `STRMW_SRP` row and `receipts/window_probe.txt` (index 0 reads `i_lwsrp_status`), `STRM_SEL[9]` is `W` and reads 0, reserved-bit rule, legacy legend gone, prune table states the shipping `I2SPB_P` and `LPF_P` |
| F8 Memory-map overprint | Closed | `receipts/memory_map_render.png`: plain labels, no overprint, no markup |
| S1, S2 | Closed | `receipts/MAC_CTRL_render.png` splits per lane; `CAP` fields are named |
| R1, R2, R3 | Closed | no `see note` and no `Group summary` on the page or notes; legend corrected |

## Round-2 checks

1. **The gate.** `gen_register_reference.py --check` rc 0, `--selftest` 58/58. 45 plants, 0 misses (`receipts/plant_probes.txt`). Each plant also ran `--write`, so the log shows what the regenerated page says. A comment-only edit stays fresh. A behaviour change with no page text fails on the source digest alone, and the PR body discloses that this asks a person to reread the prose.
2. **Generator mutants.** `receipts/generator_mutants.txt`: clean copy 58/58; `range_term`, `flop_rom`, `cell_cap` and `fingerprint` each make `--selftest` exit 1, naming the control.
3. **Design notes.** `receipts/old_sentences_hand.txt` and `old_sentences_r1.txt`: 87 of 1,655 and 90 of 2,770 sentences are absent from page and notes together. By inspection these are bit lists split across field rows, section headings, removed bench captures and the dropped statements R753-1 accepted. `receipts/fact_keywords.txt` confirms each sampled fact survives on the page or in the notes. All 166 links from page to notes resolve (`receipts/notes_anchors.txt`). The notes carry the false statements of F1 and F2. I found no other contradiction in the sections read: `0x100`, `0x7D8`, the ADP group and the entity-enable passages. The notes' banner says the reference and the RTL win.
4. **Merged tree.** `hdl/common/csr/milan_csr.sv` is unchanged by the merge. `receipts/soc_crosscheck.txt`: the extract matches the author's export with 0 differences, and the two new parameters are `REBOOT_MAC_*`. The export's `csr.csv` differs from round 1 only in its timestamp and the ISA string's order. #806: `port_enabled_i` takes `eff_link_w` (`milan_datapath.sv:8934`), and no row states otherwise, so nothing on the page is false. #814 adds pipeline stages with CSR names unchanged; no address moved. #818 is a build gate with no register. #787 is F3. #70 is F1 and F2.
5. **Docs workflow.** `docs.yml` and the template carry the step as `gate_50`, and `ci_events.py --check` and `ci_gate_workflows.py --check` are rc 0. Gates in `receipts/gates/` are rc 0, including `check_em_dash.py`, `gen_toc.py` both forms, `check_doc_paths.py`, `docs_check.py` and `git diff --check 1f29f189 HEAD`. The behave `counters_contract_milan.feature` is rc 0.
6. **Diagrams.** All ten Mermaid blocks parse with the library's own parser, run locally with no upload (`receipts/mermaid_parse.txt`). This closes the author's open risk 3 for syntax; they were not rendered visually. Device labels: a grep of the page, notes and descriptions finds none.
7. **ETH_GUARD.** The page states the code. `sw/litex/milan_soc.py:1622` and `:2162` bind the level, and nothing else reads it. Implementing the gating is out of this PR by ruling and was not assessed.
8. **Comment rule.** The new generator sources carry no lane labels, review rounds, reviewer IDs or issue-comment IDs. Two `issuecomment` links in the notes (`:1102`, `:1112`) are carried prose citing decisions, not source comments, so no RESIDUE arises.

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3, F4, F5) | #797 owner rules; `docs/reference/REGISTER_MAP.md`; `receipts/oracle_compare.txt`; `milan_baremetal.c:1099-1102,1846-1849`; `milan_soc.py:2132`; `protocol_processor_top.sv:2027` | R753-2 | 96bfa8513978ebc8c2f2e73bd98914b56e84bf12 |
| RTL | UNCLEAN (F2, F4, F5) | `hdl/common/csr/milan_csr.sv` under simulation at shipping parameters; `receipts/window_probe.txt`; `milan_datapath.sv:2780-2781,9586`; `KL_link_guard.sv`; `KL_mmcm_drp_servo.sv` | R753-2 | 96bfa8513978ebc8c2f2e73bd98914b56e84bf12 |
| Robustness | CLEAN | `scripts/register_sv.py`, `register_decode.py`, `register_fields.py`; `receipts/plant_probes.txt` (45 plants, 0 misses); `receipts/write_probe.txt`; refusals in `receipts/generator_mutants.txt` | R753-2 | 96bfa8513978ebc8c2f2e73bd98914b56e84bf12 |
| Tests | UNCLEAN (F4) | `scripts/register_selftest.py` 58/58; four killed generator mutants; no control covers condition grouping | R753-2 | 96bfa8513978ebc8c2f2e73bd98914b56e84bf12 |
| Docs | UNCLEAN (F1, F2, F3, F4, F5) | page; `docs/design/CSR_REGISTER_NOTES.md`; `docs/diagrams/README.md`; `receipts/memory_map_render.png`; `receipts/mermaid_parse.txt`; sentence survival receipts | R753-2 | 96bfa8513978ebc8c2f2e73bd98914b56e84bf12 |

## Prior public findings

Read only after this round's verdict and ledger were on disk. PR #825 has no GitHub reviews or inline comments; its findings are the two round-1 comments. Round-1 findings of R753 are in the table above. R754-1 (issuecomment-6562982241) at this head:

| Finding | Status | Evidence at this head |
|---|---|---|
| F1 `--check` fresh on real changes | Resolved | My 45 plants cover the same classes. The author's rerun of R754's 39 rows is published (`author-r2/receipts/plants/r754_mutants.tsv`), and I read its carve-out, `_END`, no-prefix, consumed-bit and CBS rows, each refused rc 2. I did not rerun R754's own driver. A register with no name or purpose refuses (`REG new live read arm` in `receipts/plant_probes.txt`) |
| F2 Gate skips 55% of the page | Resolved | same as R753 F6 |
| F3 Reset and Type cells | Resolved | same as R753 F1; `PTP_PPS_CTRL[0]` is now `R` reserved at `PPS_P` = 0, and `[16]` tells the reader to read it first |
| F4 Carried prose | Resolved | same as R753 F7; the `STRM_SEL` row now says `[8]` and `[3:0]` still store and still gate the window, and `receipts/window_probe.txt` agrees |
| F5 Memory-map overprint | Resolved | same as R753 F8 |
| F6 Side effects and pseudo-code conditions | Side effects resolved. Conditions retained in part as this round's F4 | The pseudo-code is gone, but its replacement loses the grouping |
| F7 Mechanisms without diagrams | Resolved | ten blocks on the page, all parse; the mechanisms R754 named each have one |
| F8 Device labels | Resolved | a grep for both labels counts 0 in page, notes and descriptions |
| S1, S2, S3 | Resolved | render; named `CAP` fields; no `if False else` left in `scripts/register_fields.py` |
| S4 | Out of this PR by ruling | RTL comments; not assessed |
| R1 to R6 | Resolved | no `see note`, `Group summary`, `lane-K`, `#617 round 3` or `35.2.2.7.4` on the page or notes; `docs/DOC_GENERATION.md:175-179` names both generators |

## Hosted evidence at this head

Observed, not accepted; the manager owns acceptance. At the time of writing: COMPLETED/SKIPPED 1, COMPLETED/SUCCESS 11, IN_PROGRESS/ 7, QUEUED/ 30.

- `docs-gates-0`, `docs-gates-1`, `docs-gates-2`, `docs-check-no-git` and `wire-accountability` concluded success at this head. In run 41359351300, job `docs-gates-0` ran the step "Register reference freshness gate", and that step concluded success.
- `docs-check` is queued, and the docs run has not concluded.
- `Physical gPTP (nightly and manual)` is skipped, so it is not execution evidence.
- Most other contexts are still queued or in progress. No failure or cancellation is visible.

## Real limits

- **SoC export:** no LiteX here, so no export was rerun. The check used the author's published `csr.csv` and `aem_desc.json`. Their hash matches the extract's `csr_csv_sha256` by the generator's own rule. The export's top-level Verilog is not published, so the extract's two new `REBOOT_MAC_*` parameters were not checked against it. The page does not print them.
- **Simulation scope:** `milan_csr` alone at shipping parameters with Verilator 5.050 (identity verified), handshake inputs tied and no engines. Window words were checked at the selections listed, not against an engine. The datapath, firmware and processor lines in F1 to F3 were read, not simulated.
- **Notes:** about 31,000 words were sampled, not all checked. The sentence-survival check is textual, and absent sentences were judged by inspection and by keyword.
- **Mermaid:** blocks parse locally; they were not rendered visually. FSM edges were spot-checked on two diagrams only.
- **Gates:** only the docs-workflow steps named above and one behave feature ran here. The full behave suite, builder bank, Verilator sweep and Yosys were not run and are not claimed. Author receipts report 58 workflow steps rc 0.
- **Packet:** all 189 `author-r2` files match the published manifest hashes. The commit carrying them shows as unsigned on GitHub, so the check is hash-to-manifest within that commit.
- **Physical calibration NOT RUN.** Nothing here is hardware proof. No manager source bank runs at this head.
- **Clone state:** `receipts/restore_check.txt` shows the head, tree, index and all six gitlinks unchanged, with 0 status lines. Plants and mutants ran only in scratch copies.

## Pending manager duties

- Hosted and act acceptance at the exact head, after this round's fixes.
- The current-dev merge candidate (builder and native banks) against live dev `1f29f189279f9fc0132f4918e47342b87d22f33a`.
- External review.
- Carry R1, R2 and R3 to the residue checklist.
- Lane conflict with PR #815: step renumbering, and D0's inventory listing the new notes page. D0-009's removal also rests on the #70 fact behind F1.
- The ETH_GUARD decision remains open and outside this PR.

R753-2 FINISHED
