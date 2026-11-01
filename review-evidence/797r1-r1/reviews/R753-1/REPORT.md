[R753] NEGATIVE - exact head a8bcfba9426db350018c9cee95f4905fb364d8f0

Round R753-1, internal cleared-context review of kebag-logic/milan-fpga PR #825 (#797 lane R1), tree `ed52fc55315c9ceba93687d502b6af989440b032`, over dev `1e80128f`.

## Verdict

The generated tables are largely right. An independent Verilator harness drove the real `milan_csr` at the shipping parameters and compared all 202 sections and 381 fields, parsed from the page text. Offsets and access codes agree with the RTL, and the SoC facts agree with the published export. The verdict is NEGATIVE for these reasons:

- The Reset column states `X` on 22 words whose reset the register file fixes, including the `0xDEADDEAD` poison at `CHMAP_LOOP`.
- `--check` stays fresh when a new register window is added, so the parser can still silently drop a register.
- `--check` stays fresh for reset, subfield and doorbell changes the page claims to cover.
- Over half the page's words sit in one-column tables the concise-prose gate does not read, which leaves the owner's short-paragraph rule unenforced on them.
- Some retained prose is contradicted by the RTL or the export.

No RTL changes in this PR, so none of this is a hardware defect. The defects are in the generated reference and its gate.

## Findings

### F1 - MAJOR - Conformance, RTL, Docs - Reset column says X on 22 words the RTL fixes

- **Where:** `docs/reference/REGISTER_MAP.md` headings, summary rows and field rows listed below; cause at `scripts/register_fields.py:551-580` and `scripts/register_fields.py:291-294`.
- **Authority:** owner layout in #797 issuecomment-6522974767 requires `[reset = 0xNNNNNNNN]`. The page's own legend defines `X` as "Set by the block that drives this input, not by the register file".
- **Evidence:** `receipts/oracle_compare.txt`. With every input low and then high, these words read one constant from reset.

| Word | Page reset | RTL reads | RTL source |
|---|---|---|---|
| `CHMAP_LOOP` 0x914 | `0xXXXXXXXX` | `0xDEADDEAD` | `hdl/common/csr/milan_csr.sv:1308-1319`, `:1017` |
| `PTP_PPS_WIDTH` 0x55C | `0xXXXXXXXX` | `0` at the page's own `PPS_P` = 0 | `:2332` |
| `ACMP_TALKER[2]` 0x66C | `X` | `0`, the register file's own `acmp_lobs[0]` | `:2390`, `:2715`, `:1594` |
| `STRMW_STATE` 0x82C, `STRMW_PDUS` 0x858 | `0xXXXXXXXX` | `0` | `:2563-2564`, `:2932` |
| `STRMW_CNTn` 0x830-0x854 (10 words) | `0xXXXXXXXX` | `0` | `:2592-2598` |
| `STRMW_SID_LO/HI`, `STRMW_DMAC_LO/HI` 0x814-0x820 | `0xXXXXXXXX` | `0` at the reset selection | `:2543-2560` |
| `STRMW_CTLR_LO/HI`, `STRMW_BIND` 0x860-0x868 | `0xXXXXXXXX` | `0` at the reset selection, and the row calls it a structural zero | `:2579-2590` |

- **Mechanism:** a read through a ternary becomes `complex`, an array element such as `snap_shadow_r[0]` misses the reset table, and an `o_` port has no reset entry. Each falls through to `None`, which prints as `X`. Nothing refuses.
- **Not counted:** `RST_EPOCH` 0x720 also never follows an input, but it has no reset clause and counts resets, so `X` is a fair reading there. `ADP_GPTP_GM_*` and `AS2_*` do follow their inputs, so `X` is correct in effect, although the parser reached it through a tokenizer refusal on `'0`.
- **Impact:** a reader is told an external block sets these values. The poison word exists so that software can tell "no measurement" from a value, and its reset is the one number the heading hides.
- **Required outcome:** `X` appears only on bits an input can move. Every other bit shows its value, or the generator refuses.
- **Verification:** rerun `scripts/build_oracle.sh` and `scripts/compare_oracle.py`; no "page reset X, but no input moves it" line remains except a justified `RST_EPOCH`.

### F2 - MAJOR - Conformance, Robustness, Tests - `--check` stays fresh when a register window is added

- **Where:** `scripts/register_fields.py:104` (`MARKER_RE`) and `:719`; `scripts/register_rtl.py:607-610` (case labels never compared with the address list).
- **Authority:** owner freshness rule in #797 issuecomment-6522974767; review check 2; the PR body's "a new address inside and outside every module".
- **Evidence:** `receipts/plant_probes.txt`. Each of these exits 0 with "fresh (202 registers...)":
  - a new `A_PLANTW_BASE`/`A_PLANTW_END` pair with a live read term;
  - a literal `16'h7F8:` read arm;
  - a changed value at the 0x86C window hole.
- **What does work:** a plain new `A_*` localparam fails, with or without an arm, as the selftest shows. The range form is the shape this file uses for STAT, LTAP, APRB and the gap.
- **Impact:** a new decoded register window can land with no page entry and a green gate.
- **Required outcome:** every decoded read or write target is on the page or refused: any range term or case label the generator does not recognise stops it.
- **Verification:** the three plants above fail `--check`, and each has a selftest control.

### F3 - MAJOR - Robustness, Tests, RTL - A reset change on the flop of a shadow-served word passes the gate

- **Where:** `scripts/register_fields.py:551-561`; `scripts/register_selftest.py:85-87` (the only reset-block control plants `eth_guard`, a live word).
- **Authority:** `scripts/gen_register_reference.py:14-16` says reset values are read from the `csr_default` table and the reset block; `hdl/common/csr/milan_csr.sv:1989-1990` says the ROM must mirror the reset block; review check 2 ("a changed reset").
- **Evidence:** `receipts/plant_probes.txt`. `mac_ifg <= 32'h0D`, `mac_ctrl <= 32'h12`, `tcam_ctrl <= 32'h0` and `LWSRP_LATENCY_RST_C` = 9 all exit 0. These flops drive output ports, so the page would state a reset the port does not have. At this head all 60 compared flops agree with the ROM, so nothing is wrong today.
- **Impact:** the failure the RTL comment warns about passes the gate that claims to cover reset values.
- **Required outcome:** the generator compares each shadow-served word's flop reset with its ROM value and refuses a difference.
- **Verification:** the four plants fail `--check`, with a selftest control.

### F4 - MINOR - Robustness, Tests, RTL - Words the parser cannot read are opaque, and an unread write arm is published as read-only

- **Where:** `scripts/register_fields.py:291-294` and `:467-472`, `:511-516`; `CHMAP_LOOP_RD` row on the page.
- **Evidence (`--check` stays fresh):** `receipts/plant_probes.txt` for swapping `CHMAP_LOOP[17:16]`, changing the poison constant, changing the `PPS_WIDTH` expression and changing the snapshot reset. A plant that makes `IRQ_STATUS[1]` clear on read also stays fresh, while the page's legend says no register clears on read. `CHMAP_LOOP` is built inside `milan_csr.sv` from named bits, yet the page gives one `[31:0]` field and hand-kept prose.
- **Evidence (wrong regeneration):** `receipts/write_probe.txt`. After `chmap_sel <= s_axi_wdata & 32'h1FF` or `mcsrv_ctrl[1:0] <= s_axi_wdata[1:0]`, `--check` does report stale, but `--write` exits 0 and publishes those writable fields as `R`.
- **Impact:** `register_rtl.py` defines `Refusal` as "an input the generator cannot honestly turn into a page", but these inputs produce a confident wrong page.
- **Required outcome:** an unparsed write statement or read expression refuses, and `CHMAP_LOOP` fields come from the RTL.
- **Verification:** both write forms exit 2 on `--write`, and the `CHMAP_LOOP` swap fails `--check`.

### F5 - MINOR - Conformance, Tests, Docs - Side effects are not in the field's row

- **Where:** `scripts/register_page.py:159-173` (only `magic:` is rendered; `pulse:` is computed and discarded); page rows in `receipts/row_audit.txt`.
- **Authority:** #797 issuecomment-6522974767: "side effects (write-one-to-clear, read-to-clear, doorbells, ETH_GUARD unlock) stated in the field's row."
- **Evidence:** 12 W1C, W1S and R/W1S rows have an empty description, including `IRQ_STATUS[2:1]`, `ADP_CMD[1:0]`, `I2SPB_STAT`, `JNL_CTRL[2:0]`, `STRM_SNAP[0]` and `CHMAP_SNAP[0]`. The doorbell `PP_SPADDR[19:0]` is also empty: its "posts a read" sits in a Note below the table. Overall, 148 of the 381 field rows have no description. A new doorbell added to the `SCRATCH` arm leaves `--check` fresh (`receipts/plant_probes.txt`).
- **Impact:** `I2SPB_STAT` shows why this matters. The legend says writing 1 clears a latched bit, while the RTL clears a whole counter half on any set bit (`milan_csr.sv:1775-1778`), and only a Note says so.
- **Required outcome:** each side effect is in its field's row, and the generated `pulse:` effects reach the page.
- **Verification:** `scripts/row_audit.py` lists no side-effect row without text; the doorbell plant fails `--check`.

### F6 - MAJOR - Conformance, Tests, Docs - The concise-prose gate does not read 56% of the page

- **Where:** `scripts/register_page.py:263-296` (`notes_block`, `note_table`); `scripts/check_doc_style.py:144`.
- **Authority:** #797 issuecomment-6522974767 section 1: "No paragraph over the limit. Split long ones." Tables are exempt there as tables; #797 issuecomment-6523093123 requires paragraphs within the 20-word rule.
- **Evidence:** `receipts/note_cells.txt` and `receipts/note_as_paragraph.txt`.
  - 454 rows in 184 one-column `| Note |` tables carry 31,033 of the page's 55,197 words. The median row is 43 words, and 333 rows exceed 20 words.
  - One cell, the `VERSION` changelog at line 313, is 4,953 words.
  - The repository's own analyzer reports 0 findings on the page, and 1,371 when those rows are rendered as paragraphs (526 paragraph-limit, 845 sentence-limit).
  - The other 23 gated documents have no `| Note |` table.
- **Impact:** `check_doc_style.py` lists the page and passes, while the rule it exists to enforce does not reach most of the page's prose. A reader gets a 4,953-word table cell.
- **Disclosure:** the PR body says the descriptions file is large and moving history out is later work. It does not say the gate skips this prose.
- **Required outcome:** the prose obeys the limit, or history moves to its own page, and the gate cannot be satisfied by wrapping a paragraph in a one-column table.
- **Verification:** `scripts/note_as_paragraph_probe.py` reports 0 findings, or the maintainer records an exemption on #797.

### F7 - MINOR - Conformance, RTL, Docs - Retained prose contradicted by the RTL or the export

| Page line | Statement | Against |
|---|---|---|
| 3662, `STRMW_SRP` row | "STRUCTURAL ZERO at every index ... reads 0 -- including at idx 0, whose live hard alias of `LWSRP_STATUS` went with the port" | `milan_csr.sv:2574-2576` serves `i_lwsrp_status` at idx 0; `hdl/milan/milan_datapath.sv:2796` drives it live; oracle 0x85C reads `ffffffff` with inputs high |
| `STRM_SEL` note | "Only these bits are stored/read back", listing `[9]` | `milan_csr.sv:2535` does not return `[9]`; oracle reads `0x10F` after writing all ones. The page's own field row correctly says `W` |
| 106 | "Unused bits read 0" | Oracle `MAC_CTRL` reads `ffffffff` after writing all ones, and the page's legend says reserved `R/W` bits store |
| 105 | Legacy legend `RO`, `RW`, `ROc` "read latches/clears" | The page's legend uses `R` and `R/W` and says no register clears on read |
| 114 | "Every one defaults to PRESENT, so a shipping build's map is exactly what this page describes" | `scripts/register_map_soc.json` has `I2SPB_P` 0 and `LPF_P` 0; `configs/endstation_ax7101_1x1_tdm8.yaml:35,39`. The `I2SPB_*` sections do not say they read a structural zero on the shipping build |

- **Impact:** the issue's acceptance requires that no current document contains a statement contradicted by the code.
- **Required outcome:** each row corrected in `scripts/register_descriptions.json` to match the cited source.
- **Verification:** re-read the rows against the same lines and the oracle.

### F8 - MINOR - Docs - Memory-map diagram labels overprint their addresses

- **Where:** `docs/diagrams/memory_map.svg` and `.drawio`, rows `0x90000768` and `0x90000778`; cause at `docs/diagrams/memory_map.gen.py:59`.
- **Evidence:** `receipts/memory_map_render.png`. The two long module headings run through the address text. The labels also carry raw backticks and a status emoji that the renderer cannot draw.
- **Impact:** those two address ranges cannot be read in the published render. Addresses are correct in the source text.
- **Required outcome:** every label fits its block and carries no Markdown markup.
- **Verification:** re-render and inspect; a width check in `--check` would hold it.

### SUGGESTIONS

- **S1:** a field spanning several WaveDrom lanes draws blank unshaded rows with no bit numbers. See `receipts/MAC_CTRL_render.png`, where bits 23:8 of `RESERVED` look undefined. Splitting a field per lane would fix it.
- **S2:** `CAP` fields are named `BIT14` and `BITS23_16`. The description cell has the meaning, but a named field would read better.

### RESIDUE

Purely wording; the manager carries these to the residue checklist.

- **R1:** `TCAM_KEY_LO` row reads "`byte0 in [31:24]`? no - see note", and no such note exists. Exact fix: "match key `[31:0]` (destination MAC)".
- **R2:** 33 note rows read like leftover labels, for example "Group summary Identification / IRQ (global)". Exact fix: delete the `Group summary` rows or turn them into a heading.
- **R3:** legend line "Reserved fields read as `R-0`." Exact fix: "Reserved read-only fields read as `R-0`.", because `LWSRP_CTRL[4:2]` is reserved `R/W-4h`.

## Review checks

### 1. Sample of registers against `hdl/common/csr/milan_csr.sv`

Every row below agrees for offset, width, access, reset and field meaning, unless a finding is named. The oracle covers all 202 sections; these are the ones also read by hand.

| Register | Offset, access, reset on page | RTL lines | Oracle |
|---|---|---|---|
| `ID` | 0x000, R, `0x4D494C4E` | 741, 1994 | constant |
| `CAP` | 0x008, R, `0x00407E05` | 741, 1998-2001 | constant |
| `SCRATCH` | 0x00C, R/W, 0 | 741, 1674, 2055 | follows writes |
| `IRQ_STATUS` | 0x010, `[2:1]` R/W1C, `[0]` reserved | 742, 1676-1679, 1974-1975, 2313 | agrees (F5 for row text) |
| `MAC_CTRL` | 0x100, R/W, `0x13` | 743, 1576, 1680, 2002, 2672-2688 | follows writes |
| `PHY_RESET` | 0x11C, R/W guarded, 1 | 744, 1577, 1688, 2004, 2387, 2692 | guarded reads 1; open reads `ffffffff` |
| `STATS_CTRL` | 0x200, `[1:0]` W1S | 745, 1689-1696 | reads 0 |
| `STATn` | 0x210 to 0x230, R, 0 | 1046, 1048, 2478-2479 | reads 0 |
| `CBS_*n` | 0x400 to 0x48C, stride 0x20, table | 1047, 1509-1513, 2037-2044, 2082-2090 | every queue agrees |
| `PTP_INCR` | 0x504, R/W, `0x14000000` | 748, 1212-1213, 1583, 2018 | 20 ns at 50 MHz |
| `PTP_CMD` | 0x520, `[2:0]` W1S | 750, 1704-1708 | reads 0 |
| `PTP_PPS_CTRL` | 0x548, `[16]` R, `[1]` W1S, `[0]` W | 753, 1716-1719, 2324 | agrees at `PPS_P` 0 |
| `ADP_TALK` | 0x618, R, `0x48010002` | 757, 1390-1391, 2021 | constant from the shape header |
| `ADP_CMD` | 0x640, `[1:0]` W1S | 760, 1799-1802 | reads 0 |
| `LWSRP_CTRL` | 0x680, R/W, `0x10`, reserved `[4:2]` `4h` | 770, 1600, 1724, 2027, 2863-2869 | follows writes |
| `I2SPB_STAT` | 0x6D8, R/W1C, X | 780, 1775-1778, 2409 | input-driven (F5) |
| `TCAM_CMD` | 0x718, `[16]` W1S, `[8]` and `[4:0]` W | 795, 1946-1952, 2900-2902 | reads 0 |
| `LINK_CTRL` | 0x71C, R/W, 1, `[1]` masked | 796, 1602, 1728-1730, 2033, 2388, 2854-2857 | guarded `fffffffd` |
| `CRF_CTRL` | 0x738, `[31]` R, `[0]` R/W | 803, 1737, 2414, 2843 | agrees |
| `CRFT_CTRL` | 0x750, `[31:2]` R, `[1:0]` R/W | 820, 1740, 2419, 2845-2846 | agrees |
| `REST_CMD` | 0x7B4, `[31]` R/W1S, `[23:10]` W, `[9:8]` reads status | 857, 1931-1939, 2472 | agrees, latches at first commit |
| `JNL_CTRL` | 0x7B8, `[2:0]` W1S, `[31:30]` R | 868, 1901-1905, 2423 | agrees |
| `ETH_GUARD` | 0x7D8, `[0]` key-compared, 1 | 897, 1578, 1731, 2389 | key clears; any other word sets |
| `STRM_SEL` | 0x800, `[9]` W, `[8]`, `[3:0]` R/W | 1022, 1808-1812, 2534-2535 | `0x10F` after all ones |
| `LTAP_CTRL` | 0x870, `[1]` R/W reset 1, `[0]` R/W1S | 925, 1615, 1747-1750, 2453 | agrees |
| `CHMAP_SNAP` | 0x910, R, `0xC5000300`, `[0]` R/W1S | 961, 1279-1287, 2462, 2759 | agrees |
| `PP_STAT` | 0x924, R, tag `5Bh` | 979, 2265-2275 | agrees |
| `PP_SPADDR` | 0x928, `[19:0]` R/W | 980, 2206-2214, 2276 | agrees (F5 for the doorbell) |

Oracle exceptions other than F1 are expected behaviour, not defects:

- window words write through to engines the harness does not model;
- `CHMAP_WORD` is refused while disarmed;
- `CHMAP_SNAP[4]` and `[2]` move after an arm;
- `PP_SPDATA`, `PP_NVM_DATA` and `PP_NVM_STAT` write a different register than they read, and their rows say so.

An address scan from 0x000 to 0xFFC found one decoded word without a section, the 0x86C hole, which the `STRMW_BIND` row names. Receipts: `receipts/oracle_raw.txt`, `receipts/oracle_compare.txt`, `receipts/offset_check.txt`. The three CBS offset mismatches in `offset_check.txt` come from the checker reading `A_CBS_BASE + 0x4` as the base; the oracle confirms those offsets.

### 2. Silent-drop plants

45 scratch-copy plants ran through the workflow's `--check` entry: 13 misses, 28 correct failures or the clean control, and 4 informational. See `receipts/plant_probes.txt`. The plain plants the brief names all fail as required: a new register, a renamed field and a changed reset in the ROM or a live flop. The misses are F2, F3, F4 and F5. All 16 selftest controls pass (`receipts/gates/gen_selftest.log`).

### 3. SoC facts

`receipts/soc_crosscheck.txt`: the committed extract matches the published export for 8 regions, 9 banks, 79 CSR registers, 85 constants and the 5 processor windows, with 0 differences; the `csr.csv` hash matches. The page, SVG and draw.io carry every region and bank, and the 13 page CSR rows agree. Editing the SVG or the extract fails the memory-map check (`receipts/memory_map_plants.txt`). F8 is a legibility defect only.

### 4. The 12 dropped fragments

Each was checked against the code or the standard. All 12 are false or obsolete, or kept in another wording, so dropping them is sound.

| Fragment | Result | Checked against |
|---|---|---|
| Old page title | obsolete; ABI statement kept | page Reading section |
| "VERSION `0x0002_0055` adds lane 4" | kept, reworded | `TXARB_DIAG` note |
| Offset "pinned at the Milan 2 ms" | false | page 0x0053 row; `SET_STREAM_INFO` in the processor sources |
| `phy_reset_n` holds the PHY in reset | false on the shipping SoC | `sw/litex/milan_soc.py` connects no `o_phy_reset_n` |
| Firmware publishes PHY state | kept with its condition | `milan_baremetal.c:1042-1078`, `:1094` |
| Switch-cycle acceptance on #599 | obsolete | #599 is CLOSED |
| 802.1Q 35.2.2.7.4 | false | 802.1Q-2018 has 35.2.2.7.1 and .2, no .4; FourPackedEvents is .2 |
| "Milan Table 7-156" | false | IEEE 1722.1-2021 Table 7-156 is the STREAM_INPUT `counters_valid` table |
| Nothing persists a binding | false | `hdl/milan/KL_pp_shadow.sv:82`, `:408` |
| Milan 5.3.8.2 "not met" | stale; ledger row `state.nonvolatile-persistence` is `partial` | `docs/reference/milan_feature_status.json` |
| Shipping AX7101 shape is 8 | false | `sw/litex/build.sh:378`, the extract's shape |
| Un-anchored Section 21 pointer | kept as an anchored link | `docs/limitations/TROUBLESHOOTING.md:521` |

An independent sentence-level pass found 39 of 1,655 old sentences absent (`receipts/old_sentences.txt`). They are these fragments plus bit lists split across field rows. Spot checks of the split rows found the facts present.

`hdl/common/csr/milan_csr.sv:865-867` still says 5.3.8.2 is not met. That comment is outside this PR's diff.

### 5. CI wiring and style gate

The wiring is correct. The docs workflow runs on every pull request with no path filter (`.github/workflows/docs.yml:1066-1070`), and the step follows the wavedrom install. These gates all exit 0 in `receipts/gates/`: `ci_events.py --check`, `ci_gate_workflows.py --check`, `generate_ci_evidence_pins.py --check`, the two generators, `check_doc_style.py`, `docs_check.py`, `check_em_dash.py`, `check_doc_paths.py`, `gen_toc.py` (both forms) and `check_feature_status.py --self-test`. The `check_py_idiom.py` gate and the selected builder and behave tests also pass.

The command-table hashes match both registered scripts, and `sw/builder/test_builder.py` gate 18a passes with its RTL comparison unchanged. The style gate lists the page but does not reach most of its prose (F6).

### 6. Author's open risk 1, ETH_GUARD

The page states the code correctly. `sw/litex/milan_soc.py:1568` and `:2070` bind `self.eth_guard` to the datapath output, and nothing else reads it. `milan_soc.py:2067-2069` calls the gating future work. So the `milan_mac_phy_crg_reset` CSR is not gated, as the row and note say. The guard's two levers behave as the row says: guarded `PHY_RESET` reads 1 and `LINK_CTRL` reads `fffffffd` after writing all ones.

`hdl/common/csr/milan_csr.sv:708` and `:890` still claim the gating. Those comments are outside this diff, and the page names the conflict. The decision between implementing the gating and correcting the comment remains open.

### Comment rule

No lane labels, review rounds, reviewer IDs or issue-comment IDs appear in the source comments this delta adds. The page's `issuecomment` links are prose carried from the old page, which had 6 lines of that kind. No RESIDUE arises from this rule.

## Prior public findings

Read only after this round's verdict and ledger were on disk. PR #825 has no earlier review: its one comment is the review-start notice (issuecomment-6562425023), with no reviews and no inline comments. So there is nothing to resolve or retain. #797 records no exemption for the one-column note tables in F6.

## Hosted evidence at this head

Observed, not accepted; the manager owns acceptance.

- `rtl-fast` and `elaborate` concluded success.
- `docs-check` concluded cancelled, so the new freshness step has no completed hosted run at this head. Local gate runs in this round and the author's receipts are its only execution evidence.
- Run 41098987841 (`rtl-full`) concluded cancelled, with cancelled Verilator and Yosys shards. Its `Union` jobs fail at their "Require successful owners and every case exactly once" step, and `verilator-suites` and `yosys-portability` conclude failure. These conclusions fit the cancellation, but this round did not establish the cause.

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F5, F6, F7) | #797 body and the two owner comments; page layout; oracle comparison; `receipts/row_audit.txt`; 802.1Q-2018 and 1722.1-2021 clauses | R753-1 | a8bcfba9426db350018c9cee95f4905fb364d8f0 |
| RTL | UNCLEAN (F1, F3, F4, F7) | `hdl/common/csr/milan_csr.sv` decodes, reset blocks and read muxes; `hdl/milan/milan_datapath.sv` instance; `receipts/oracle_compare.txt` | R753-1 | a8bcfba9426db350018c9cee95f4905fb364d8f0 |
| Robustness | UNCLEAN (F2, F3, F4) | `scripts/register_rtl.py`, `register_fields.py`, `gen_register_reference.py`; `receipts/plant_probes.txt`; `receipts/write_probe.txt` | R753-1 | a8bcfba9426db350018c9cee95f4905fb364d8f0 |
| Tests | UNCLEAN (F2, F3, F4, F5, F6) | `scripts/register_selftest.py`; selftest run; 45 plants; `scripts/check_doc_style.py`; `receipts/note_as_paragraph.txt` | R753-1 | a8bcfba9426db350018c9cee95f4905fb364d8f0 |
| Docs | UNCLEAN (F1, F5, F6, F7, F8) | `docs/reference/REGISTER_MAP.md`, `REGISTER_MAP_CLASSES.md` diff, `docs/diagrams/README.md`, memory-map and sampled register renders, dropped-fragment review | R753-1 | a8bcfba9426db350018c9cee95f4905fb364d8f0 |

## Real limits

- **SoC export:** no LiteX here, so no export was rerun. The check used the published `csr.csv` and `aem_desc.json`. The export's generated top-level Verilog is not published, so `datapath_parameters` were checked only for the clock, `I2SPB_P` and `LPF_P` against the shape config.
- **Oracle scope:** it runs `milan_csr` alone at the shipping parameters, with handshake inputs tied and no engines, so window words are checked at reset selection and not against an engine. The datapath's own wiring was read, not simulated.
- **Prose:** the 31,033 words of notes were sampled, not all checked. Statements about other blocks, the processor and silicon history were not verified.
- **Gates:** the full behave suite and the full builder bank were not rerun; author receipts report them green. Only focused tests ran here. No hardware was used.
- **Author material:** the author's dropped-statement table was read after this round's own diff, oracle and plant work.

## Pending manager duties

- Hosted and act acceptance at the merge candidate.
- The current-dev merge candidate (builder and native banks) against live dev `1f29f189279f9fc0132f4918e47342b87d22f33a`.
- External review.
- Carry R1, R2 and R3 to the residue checklist.
- The ETH_GUARD decision, and lane conflict handling with PR #815.

R753-1 FINISHED
