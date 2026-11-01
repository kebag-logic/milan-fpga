[R754] NEGATIVE - exact head a8bcfba9426db350018c9cee95f4905fb364d8f0

Round R754-1, external cleared-context review of kebag-logic/milan-fpga PR #825 (#797 lane R1), tree `ed52fc55315c9ceba93687d502b6af989440b032`, over dev `1e80128f`.

## Verdict

The generated tables are mostly right. A separate simulation of the real `milan_csr` at the shipping parameters compared all 202 register sections, 256 words and 8,192 bit checks with the page text. Every offset, every numeric reset and every access code agrees with the RTL, apart from the exceptions in F3. The SoC facts match the published export. The ETH_GUARD row states the code correctly.

The verdict is NEGATIVE for these reasons:

- The parser can still silently drop a register. `--check` reports fresh on 15 of 18 harder plants.
- The short-paragraph gate does not read over half the page's words.
- Some generated Reset and Type cells, and some carried prose, are false against the RTL.

This PR changes no RTL, so none of this is a hardware defect. The defects are in the generated reference and its gates.

## Findings

### F1 - MAJOR - Conformance, RTL, Robustness, Tests - `--check` stays fresh on real register and behaviour changes

- **Where:**
  - `scripts/register_fields.py:104` and `:719` skip labels ending `_END` or `_BASE`.
  - `scripts/register_rtl.py:687` takes addresses from `A_*` labels only, and `:607-610` never compares case labels with them.
  - `scripts/register_rtl.py:622` and `:627` read only the named blocks.
  - `scripts/register_fields.py:291-294`, `:297-379` and `:467-472` fall back without refusing.
  - `scripts/register_fields.py:551-561` takes a shadow word's reset from the ROM only.
  - `scripts/gen_register_reference.py:127-158` requires no purpose or name.
- **Authority:** the brief's check 2; #797 issuecomment-6522974767 ("the gate fails on any difference"); #797 issuecomment-6489587365 (fail on any register the map is missing); `scripts/register_rtl.py:35` ("An input the generator cannot honestly turn into a page").
- **Evidence:** `receipts/mutants.tsv`. All 20 plain plants fail as required, including a new register, a renamed field and a changed reset. These harder plants all exit 0 with "fresh (202 registers...)":

| Row | Plant | Consequence the page would hide |
|---|---|---|
| 22, 23 | Case arm on a literal address `16'h7F8`, read or write | A decoded word with no page entry. The RTL already uses this form at `milan_csr.sv:2599` for 0x86C |
| 35 | New register `A_PLANT_END` with a live read arm | A decoded word with no page entry |
| 36 | New register `R_PLANT`, no `A_` prefix, with a live read arm | A decoded word with no page entry |
| 25, 26 | `A_SLIP_TDM` or `A_MCSRV_CTRL` removed from `rd_in_window` (`milan_csr.sv:2612-2632`) | The register reads 0 while the page calls it live. The page itself warns about this carve-out at line 3727 |
| 20, 21 | Reset-block value of `mac_ctrl` or `scratch` changed, ROM unchanged | The output port resets to a value the page does not state. At this head the flops and the ROM agree, so nothing is wrong today |
| 27 | New write arm in a block other than the two parsed | A word listed `R` becomes a write target |
| 30 | `A_CRF_DELTA` read masked to 8 bits | The page still states a 32-bit field |
| 31 | A read of `IRQ_RAW` made to clear `irq_mask` | The legend still says no register clears on read (`register_fields.py:29`) |
| 33 | `mac_ctrl[9]` consumed inside `o_irq` | The row still says "drives nothing" |
| 37 | CBS word offset moved in `is_plain_rw` | The page keeps the old layout. Array geometry is hard-coded at `register_fields.py:694-702`, against that module's "Nothing here is hand-kept register data" (`:8`) |
| 24, 34 | 0x86C poison value changed; the `STRMW_SRP` alias removed | Hand-kept prose goes untested |

- **Two further gaps:**
  - A register with no description passes. After `--write`, `--check` is fresh with a blank purpose and blank name, against the owner's "a one-sentence purpose" rule.
  - An unparsed write form regenerates wrongly. After `chmap_sel <= s_axi_wdata & 32'h1FF`, `--check` does report stale, but `--write` exits 0 and publishes `CHMAP_SEL` as read-only. This reproduces the finding R753 published.
- **Impact:** the page can lose a register or misstate one under a green gate, which is the failure this generator exists to end.
- **Required outcome:**
  - Every decoded read or write target is on the page or refused.
  - `rd_in_window` reachability is derived or checked.
  - A shadow word's flop reset is compared with its ROM value, and a difference is refused.
  - An expression or statement outside the grammar refuses.
  - A register without purpose and name refuses.
- **Verification:** `scripts/mutants.py` rows 20-37 each fail or are explained. Each new class gets a selftest control.

### F2 - MAJOR - Conformance, Tests, Docs - The short-paragraph gate does not read 55% of the page

- **Where:** `scripts/register_page.py:263-296` (`notes_block`, `note_table`); `scripts/check_doc_style.py:37` adds the page, and its table exemption is in `prose_blocks`.
- **Authority:** #797 issuecomment-6522974767 section 1 ("No paragraph over the limit. Split long ones."; "each page a lane rewrites or marks current is added to `DOCUMENTS` in the same PR and passes the gate"); #797 issuecomment-6523093123 ("paragraphs within the 20-word rule").
- **Evidence:** `receipts/note_rows.txt` and `receipts/note_probe.txt`.
  - 454 one-column `| Note |` rows hold 30,097 of the page's 55,197 words.
  - 331 rows exceed 20 words, 58 exceed 100, and 2 exceed 500.
  - Line 313 is one 4,847-word table cell.
  - A probe added a 340-word note to `ETH_GUARD`. `--write` and `--check` stayed green, and `check_doc_style.analyze` reported 0 findings on that page. The selftest's prose control only covers a module purpose.
  - No owner or manager record on #797 exempts these rows. The PR body says the descriptions file is large, not that the gate skips this prose.
- **Impact:** `check_doc_style.py` lists the page and passes, while the rule does not reach most of its prose. A prose paragraph wrapped in a one-column table is still prose.
- **Required outcome:** the prose obeys the limit, or history moves to its own page. The gate must not be satisfiable by wrapping a paragraph in a one-column table. A maintainer exemption recorded on #797 would also clear this.
- **Verification:** render the note rows as paragraphs, run `check_doc_style.analyze`, and expect 0 findings.

### F3 - MINOR - Conformance, RTL, Docs - Generated Reset and Type cells are false against the RTL

- **Where:** page headings, summary rows and field rows listed below; cause at `scripts/register_fields.py:291-294` and `:566-579`, and at `:335-337` for the Type case.
- **Authority:** the legend defines `X` as "Set by the block that drives this input, not by the register file" and `W` as "The written value is used"; owner layout `[reset = 0xNNNNNNNN]`.
- **Evidence:** `receipts/compare_page.txt` and `receipts/sim_directed.txt`. Both input patterns read one constant from reset, except where the table says otherwise.

| Word | Page | RTL | Source |
|---|---|---|---|
| `CHMAP_LOOP` 0x914 | `X` | `0xDEADDEAD` | `milan_csr.sv:1017`, `:1308-1319`, `:2765` |
| `PTP_PPS_WIDTH` 0x55C | `X` | 0 at the page's own `PPS_P` = 0 | `:2332` |
| `ACMP_TALKER[2]` 0x66C | `X` | 0, the register file's own `acmp_lobs[0]` | `:1594`, `:2390`, `:2715` |
| `STRMW_STATE` 0x82C, `STRMW_PDUS` 0x858 | `X` | 0 | `:2563-2564`, `:2932` |
| `STRMW_CNTn` 0x830-0x854 (10 words) | `X` | 0 until a SNAP | `:2592-2598`, `:2933` |
| `STRMW_SID_LO/HI`, `STRMW_DMAC_LO/HI` 0x814-0x820 | `X` | 0 at the reset selection; these move only after `i_acmp_tbl_gnt`, which the datapath ties to `1'b0` | `:2543-2560`, `:3154` |
| `STRMW_CTLR_LO/HI`, `STRMW_BIND` 0x860-0x868 | `X` | 0 at the reset selection, under the same tie; the rows call them a structural zero | `:2579-2590` |
| `PTP_PPS_CTRL[0]` line 1082 | Type `W` | At `PPS_P` = 0 the write is unobservable and the value reaches nothing (`W-NO-EFFECT`). At `PPS_P` = 1 the bit is R/W. The note below the table says `RW` | `:1717`, `:2324`, `:2709` |

- **Note:** `RST_EPOCH` is a counter that survives reset, so `X` is fair, although its legend sentence is not.
- **Impact:** readers are told an external block sets these values. The poison word exists so software can tell "no measurement" from a value, and its reset is the number the heading hides.
- **Required outcome:** `X` appears only on bits an input can move, and the Type cell is true at the documented build parameters.
- **Verification:** rerun `scripts/compare_page.py`; no `X-NOT-INPUT` or `W-NO-EFFECT PPS_ENABLE` row remains, except a justified `RST_EPOCH`.

### F4 - MINOR - Conformance, Docs - Carried prose contradicted by the RTL or the export

| Page line | Statement | Against |
|---|---|---|
| 3662, `STRMW_SRP` row | "STRUCTURAL ZERO at every index ... reads 0 -- including at idx 0, whose live hard alias of `LWSRP_STATUS` went with the port" | `milan_csr.sv:2574-2576` serves `i_lwsrp_status` at idx 0, and `milan_datapath.sv:2796` drives it live. Measured 0xFFFFFFFF at 0x85C for dir 0 and dir 1 with that input high. The page's own line 3433 says the opposite |
| 3480, `STRM_SEL` note | "`[8]`/`[3:0]` are ignored while set" | `milan_csr.sv:3088-3090` selects the talker row when `[8]` is set, whatever `[9]` says. `:1109-1110` and `:3086-3087` gate on `[3:0]` |
| 3480, `STRM_SEL` note | "Only these bits are stored/read back", listing `[9]` | `:2535` does not return `[9]`. Measured 0 after writing 0x200. The field row correctly says `W` |
| 106 | "Unused bits read 0" | Reserved `R/W` bits store: `PHY_RESET` read 0xFFFFFFFE after that value was written, unguarded, and the legend says reserved `R/W` fields store |
| 105 | Second legend: `RO`, `RW`, `ROc` "read latches/clears" | The page's own legend uses `R` and `R/W` and says no register clears on read |
| 114 | "Every one defaults to PRESENT, so a shipping build's map is exactly what this page describes" | `scripts/register_map_soc.json` has `I2SPB_P` 0 and `LPF_P` 0, and the `I2SPB_*` sections do not say they read a structural zero on the shipping build |

- **Authority:** #797 acceptance: "no document marked current contains a statement contradicted by the code or a clause".
- **Impact:** a diagnostic that trusts the `STRMW_SRP` row reads a live word as an anomaly. The others misdescribe the selection and the build.
- **Required outcome:** each row is corrected in `scripts/register_descriptions.json` against the cited source.
- **Verification:** re-read the rows against the same lines and `receipts/sim_directed.txt`.

### F5 - MINOR - Docs - Memory-map diagram labels overprint their addresses

- **Where:** `docs/diagrams/memory_map.svg` and `.drawio`, rows `0x90000768` and `0x90000778`; cause at `docs/diagrams/memory_map.gen.py` in `rows`, where the heading text goes through unshortened.
- **Authority:** `docs/diagrams/README.md`, "Every current render needs visual inspection".
- **Evidence:** a render of the committed SVG. Two long module headings run through the address text. The labels also carry raw backticks and a status emoji the renderer cannot draw.
- **Impact:** those two address ranges cannot be read in the published diagram. The addresses are correct in the source text.
- **Required outcome:** every label fits its block and carries no Markdown markup.
- **Verification:** re-render and inspect. A width check in `--check` would hold it.

### F6 - MINOR - Conformance, Tests, Docs - Side effects are not in the field's row, and conditions print as pseudo-code

- **Where:** `scripts/register_page.py:159-173`, `:183`, and rows on the page.
- **Authority:** #797 issuecomment-6522974767: "side effects (write-one-to-clear, read-to-clear, doorbells, ETH_GUARD unlock) stated in the field's row."
- **Evidence:**
  - 12 W1S, R/W1S and R/W1C rows have an empty description, for example `I2SPB_STAT[31:16]`, whose legend wording ("writing 1 clears it") understates `milan_csr.sv:1775-1778`, where any set bit restarts the whole half.
  - The doorbell `PP_SPADDR[19:0]` (`R/W`, empty row, section at line 4326) posts a read at `:2206-2214`, and only the Note says so.
  - Rows 3509, 3510, 3558 and 3574 print conditions such as `win_in_range_w not !strm_dir_r strm_idx_r == 4'd0`, which is neither RTL nor prose.
  - Overall, 148 field rows have no description.
- **Impact:** a reader of the table sees plain storage where the hardware fires an action.
- **Required outcome:** each side effect is in its field's row, and generated conditions read as sentences.
- **Verification:** no W1S, W1C or doorbell row is empty, and a planted doorbell fails `--check`.

### F7 - MINOR - Conformance, Docs - Mechanisms the page explains have no diagram

- **Where:** `docs/reference/REGISTER_MAP.md`: 0 Mermaid blocks. Of its 204 images, only `memory_map.svg` and `wd_linkguard_reset.svg` are not bit-field diagrams.
- **Authority:** #797 issuecomment-6523093123: "**Rule for every area lane:** each mechanism a page explains gets a diagram next to its text"; "A page is current only when that count is zero."
- **Evidence:** the page explains several sequences in prose only: `SEL`, `SNAP`, poll `busy`, read the block (line 3436); the posted side-port read (0x928, 0x92C); the `CHMAP_SNAP` arm and readback (heading at line 4107); the `ETH_GUARD` armed and disarmed states. The lane's takeover comment scopes only the `reg` diagrams and does not record an exemption. R753 did not raise this, and it is this round's own reading of the rule.
- **Impact:** the page cannot be marked current under the owner's rule.
- **Required outcome:** those mechanisms get generated diagrams, or the manager records on #797 that lane R1 is exempt and which lane owns them.
- **Verification:** D0's "mechanisms without a diagram" count for this page is zero, or the exemption is linked.

### F8 - MINOR - Docs - Device labels in the descriptions file

- **Where:** page line 3442 (`silicon m001g`) and line 4061 (`mf51 silicon`), carried in `scripts/register_descriptions.json`.
- **Authority:** #797 rule "No private bench hosts, devices, addresses or serials."
- **Evidence:** both labels are carried from the old page, and this PR's new source file now holds them. This round could not establish that they are public names. A defect touching a privacy rule cannot be RESIDUE, and an unsure case is MINOR.
- **Impact:** a possible private device name on a public reference page.
- **Required outcome:** say "measured on silicon" with no device label, or the owner records that the labels are public.
- **Verification:** search the page and the descriptions file for both strings.

### SUGGESTIONS

- **S1:** a field spanning several WaveDrom lanes draws blank unshaded rows with no bit numbers. In `MAC_CTRL.svg`, bits 23:8 of `RESERVED` look undefined. Splitting a field per lane would fix it.
- **S2:** `CAP` fields are named `BIT15`, `BIT14` and `BITS23_16`, and `CAP[15]` has no text. RTL `1'b0` reads as reserved. Naming the fields would read better.
- **S3:** `scripts/register_fields.py:588` has a dead expression, `label[2:] if False else label`.
- **S4:** the RTL comments at `hdl/milan/KL_pp_shadow.sv:688` and `hdl/milan/milan_datapath.sv:8651` still cite 802.1Q 35.2.2.7.4, while the page now cites 35.2.2.7.2. Both are outside this diff.

### RESIDUE

Purely wording; the manager carries these to the residue checklist.

- **R1:** line 2301, `TCAM_KEY_LO`: "match key `[31:0]` (dest MAC, MSB-first: byte0 in `[31:24]`? no - see note)", and no such note exists. Exact fix: "match key `[31:0]` (destination MAC)".
- **R2:** 33 note rows read like leftover labels, for example "Group summary Identification / IRQ (global)". Exact fix: delete the `Group summary` rows or make them a heading.
- **R3:** legend line "Reserved fields read as `R-0`." Exact fix: "Reserved read-only fields read as `R-0`.", because `LWSRP_CTRL[4:2]` is reserved `R/W-4h`.
- **R4:** line 3457, "the lane-K engines". Exact fix: "the context engines".
- **R5:** line 3874, "#617 round 3". Exact fix: "#617".
- **R6:** `docs/DOC_GENERATION.md` does not name the new generators. Exact fix: add `python3 scripts/gen_register_reference.py --write` and `python3 docs/diagrams/memory_map.gen.py`.

## Review checks

### 1. Registers against `hdl/common/csr/milan_csr.sv`

The simulation covers every register. These 35 were also read by hand. "Measured" means `receipts/compare_page.txt`, `receipts/attribution.txt` or `receipts/sim_directed.txt` agree.

| Register | Offset, access, reset on page | RTL lines | Result |
|---|---|---|---|
| `ID` | 0x000, R, `0x4D494C4E` | 741, 1994 | Measured |
| `VERSION` | 0x004, R, `0x00020060` | 201, 741, 1995 | Measured |
| `CAP` | 0x008, R, `0x00407E05` | 741, 1998-2001 | Measured |
| `SCRATCH` | 0x00C, R/W, 0 | 741, 1674, 2055 | Measured |
| `IRQ_STATUS` | 0x010, `[2:1]` R/W1C, `[0]` reserved | 742, 1676-1679, 1974-1975, 2313 | Measured, set and clear (F6 for row text) |
| `MAC_CTRL` | 0x100, R/W, `0x13` | 743, 1576, 1680, 2002, 2672-2688 | Measured |
| `MAC_STATUS` | 0x110, R, X | 744, 2315 | Measured per input port |
| `PHY_RESET` | 0x11C, R/W guarded, 1 | 744, 1577, 1688, 2004, 2387, 2692 | Measured, guarded and unguarded |
| `STATS_CTRL` | 0x200, `[1:0]` W1S | 745, 1689-1696 | Measured, pulses on the named ports |
| `CBS_*n` | 0x400-0x48C, stride 0x20, table | 1047, 1509-1513, 2037-2044, 2082-2090 | Measured, every queue |
| `CBS_CTRLn` | `[0]` R/W, `[31:1]` R | 2088-2090 | Measured 1 after all ones |
| `PTP_INCR` | 0x504, R/W, `0x14000000` | 748, 1212-1213, 1583, 2018 | Measured, 20 ns at 50 MHz |
| `PTP_CMD` | 0x520, `[2:0]` W1S | 750, 1704-1708 | Measured |
| `PTP_PPS_CTRL` | 0x548, `[16]` R, `[1]` W1S, `[0]` W | 753, 1716-1719, 2324 | F3 for `[0]` |
| `ADP_CTRL` | 0x600, R/W, `0xA00` | 756, 1590, 2019, 2877-2878 | Measured |
| `ADP_TALKER` | 0x618, R, shape constant | 757, 1390-1391, 2021 | Measured |
| `ADP_CMD` | 0x640, `[1:0]` W1S | 760, 1799-1802 | Measured |
| `AAF_CTRL` | 0x654, R/W, 0 | 763, 1722, 2713-2714, 2875 | Measured, plus the window alias |
| `LWSRP_CTRL` | 0x680, R/W, `0x10`, `[4:2]` reserved `4h` | 770, 1600, 1724, 2027, 2863-2869 | Measured |
| `I2SPB_STAT` | 0x6D8, R/W1C, X | 780, 1775-1778, 2409 | Measured (F6) |
| `TCAM_CMD` | 0x718, `[16]` W1S, `[8]` and `[4:0]` W | 795, 1946-1952, 2900-2902 | Measured, latches only with `[16]` |
| `LINK_CTRL` | 0x71C, R/W, 1, `[1]` masked | 796, 1602, 1728-1730, 2033, 2388, 2854-2857 | Measured `0xFFFFFFFD` guarded |
| `RST_EPOCH` | 0x720, R, X | 797, 2300, 2413, 2819-2823 | Measured, counts releases |
| `CRF_CTRL` | 0x738, `[31]` R, `[0]` R/W | 803, 1737, 2414, 2843 | Measured |
| `CRFT_CTRL` | 0x750, `[31:2]` R, `[1:0]` R/W | 820, 1740, 2419, 2845-2846 | Measured |
| `REST_CMD` | 0x7B4, `[31]` R/W1S, `[23:10]` W, `[9:8]` reads status | 857, 1931-1939, 2472 | Measured, latches at commit |
| `JNL_CTRL` | 0x7B8, `[2:0]` W1S, `[31:30]` R | 868, 1901-1905, 2423 | Measured |
| `ETH_GUARD` | 0x7D8, `[0]` key-compared, 1 | 897, 1578, 1731, 2389 | Measured: key clears, any other word sets |
| `ASP_CMD` | 0x7E4, `[7:0]` R, X | 901, 2476, 2851-2853 | Measured per input port |
| `STRM_SEL` | 0x800, `[9]` W, `[8]`, `[3:0]` R/W | 1022, 1808-1812, 2534-2535 | Measured (F4 for the note) |
| `STRM_SNAP` | 0x804, `[0]` R/W1S | 1023, 2913, 2536-2537 | Measured |
| `LTAP_CTRL` | 0x870, `[1]` R/W reset 1, `[0]` R/W1S | 925, 1615, 1747-1750, 2453 | Measured |
| `CHMAP_WORD` | 0x908, `[15:0]` gated, `[31:16]` reads 0 | 956, 1757-1766, 2456 | Measured, refusal and accept |
| `CHMAP_SNAP` | 0x910, R, `0xC5000300`, `[0]` R/W1S | 961, 1279-1287, 2462, 2759 | Measured, timeout path |
| `PP_STAT` | 0x924, R, tag `5Bh` | 979, 2265-2275 | Measured per input port |

- **Offsets:** all 193 single-word sections match the RTL localparam they name (`receipts/offset_check.txt`).
- **Field names:** the input walk drove each of 134 input ports alone and read every word. `receipts/attribution.txt` lists each moved bit under its page field. Its `DIFF` rows are `RST_EPOCH` counting a reset release in every run, plus 10 rows read one by one: `STRMW_SRP` is F4, `I2SPB_STAT` fields carry the clear strobes' names (F6), and `LTAP_CLR`, `AEMP_COMMIT`, `AEMP_ABORT`, `STRMW_CTRL` and `STRMW_FMT_*` read a differently named source, as their rows or notes state.
- **Write side:** 32,768 single-bit writes across 0x000-0xFFC name the outputs each write moves. The raw table is reproducible with `scripts/run_all.sh`.
- **Comparator rows that are not defects:** `receipts/compare_page.txt` holds rows that this round read and explained.
  - `RW-NOT-STORED` on `PHY_RESET`, `LINK_CTRL[1]` and `ETH_GUARD`: the guard, shown unguarded in `receipts/sim_directed.txt`.
  - `RW-NOT-STORED` on `STRMW_*` and `PP_*`: these write a different store than they read, and the rows say so.
  - `RW-NOT-STORED` on `CHMAP_WORD`: refused while disarmed.
  - `W-NO-EFFECT` on `TCAM_CMD` and `REST_FLAGS`: these latch only with the commit bit.
  - `R-BUT-OUTPUT` on `LTAP_CTRL`: a one-bit write clears `[1]`.
  - `R-BUT-OUTPUT` on `PP_SPADDR`: the doorbell (F6).
  - `RESET-INPUT-DEP`: sticky inputs held high through reset release.
- **Address scan:** a scan of 0x000 to 0xFFC found one decoded word without a section, the 0x86C hole, which only the `STRMW_BIND` row names.

### 2. Silent-drop plants

`receipts/mutants.tsv` has 39 rows. All 20 plain plants fail: a new register, renamed fields with and without a description, resets in the ROM, flop, CBS table and generated include, the offset, the decodes, the assigns and `VERSION`. The comment-only control stays fresh. Of 18 harder plants, 3 fail correctly and 15 stay fresh (F1). The 16 selftest controls pass (`receipts/gates/regself.txt`).

### 3. SoC facts

The committed extract matches the published export: 8 regions, 9 banks, 79 CSR registers and 5 processor windows, with 0 differences, and the `csr.csv` hash matches. The page and the memory-map diagram carry every region and bank. `--check --soc-from` on a directory built from the published files plus a top-level file written from the extract's parameters returns fresh. It returns 1 for a moved bank, 1 for a changed parameter and 2 for a missing top level. `MILAN_CLK_FREQ_HZ`, `I2SPB_P`, `LPF_P` and the two gPTP latencies agree with `configs/endstation_ax7101_1x1_tdm8.yaml`. F5 is a legibility defect only.

### 4. The 12 dropped fragments

All 12 are false or obsolete, or kept in another wording, so dropping them is sound. `tools/survival.py` from the author's packet reproduces 1,600 of 1,612 at this head.

| Fragment | Result | Checked against |
|---|---|---|
| Old page title | obsolete; ABI statement kept | page Reading section |
| "VERSION `0x0002_0055` adds lane 4" | kept, reworded | page line for `A_TXARB_DIAG` |
| Offset "pinned at the Milan 2 ms" | false | page 0x0053 row; `stream-info.set-acc-lat` is implemented in the ledger |
| `phy_reset_n` holds the PHY in reset | false on the shipping SoC | `sw/litex/milan_soc.py` connects no such output; `milan_datapath.sv:2343` only exports it |
| Firmware publishes PHY state | kept with its condition | `milan_baremetal.c:1086`, `:1094` |
| Switch-cycle acceptance on #599 | obsolete | #599 is CLOSED; `docs/findings/599_394_E1_LINK_CYCLES.md` exists |
| 802.1Q 35.2.2.7.4 | replaced by 35.2.2.7.2 (Table 35-3) | the repository's firmware cites 802.1Q-2018 35.2.2.7.2 at `sw/firmware/ctrl/srp/README.md:359`. No copy of the standard was read in this round; R753 reports checking the standard |
| "Milan Table 7-156" | false | IEEE 1722.1-2021 per `milan_datapath.sv:3706-3707` and the RTL comments; standard not read in this round |
| Nothing persists a binding | false | `hdl/milan/KL_pp_shadow.sv:1123` instantiates `KL_nvm_backend` |
| Milan 5.3.8.2 "not met" | stale | ledger row `state.nonvolatile-persistence` is `partial`; `docs/reference/MILAN_COMPLIANCE_MATRIX.md:180` |
| Shipping AX7101 shape is 8 | false | `sw/litex/build.sh:195`, `:378`; the extract's shape |
| Un-anchored Section 21 pointer | kept as an anchored link | `docs/limitations/TROUBLESHOOTING.md:521` |

Issue #70 is still open with a title saying nothing survives a power cycle, while the kept text says the binding survives since 2026-09-21. `docs/reference/FR_NFR.md:166` and `docs/design/SAVED_STATE_MATERIALIZATION.md:163` agree with the kept text. The issue's state is a tracker matter, not a page defect. This round did not verify the silicon claim itself.

### 5. CI wiring and style gate

The wiring is correct. The workflow runs on every pull request with no path filter (`.github/workflows/docs.yml:1066-1070`). The step follows the wavedrom install, and the template, generated workflow, `scripts/ci_events.py` pin (52 steps) and `ci/image/command-table.json` hashes all agree.

These gates exit 0 in `receipts/gates/`: `ci_events.py --check` and `--selftest`, `ci_gate_workflows.py --check`, `gen_register_reference.py --check` and `--selftest`, `memory_map.gen.py --check`, `check_doc_style.py`, `docs_check.py`, `check_em_dash.py`, `check_doc_paths.py`, `gen_toc.py` in both forms, and `check_feature_status.py --self-test`.

`tests/features/counters_contract_milan.feature` passes 88 scenarios. The six rows of builder gate 18a match their new regular expression; the bank itself was not rerun. The style gate lists the page but does not reach most of its prose (F2).

### 6. Author's open risk 1, ETH_GUARD

The page states the code correctly. `sw/litex/milan_soc.py:1568` and `:2070` bind `self.eth_guard` to the datapath output, and nothing else reads it. `:2067-2069` calls the gating future work. So `milan_mac_phy_crg_reset` is not gated, as the row and note say.

The two levers behave as the row says, measured: guarded `PHY_RESET` stays 1 and `LINK_CTRL` reads `0xFFFFFFFD` after all ones; after the unlock key both store; any other word re-arms.

`hdl/common/csr/milan_csr.sv:708` and `:890` still claim the gating, outside this diff, and the page names the conflict. #797's scope addition 6489587365 also says the guard gates that reset. The decision between implementing the gating and correcting the comments remains open.

### Comment rule

No bench lane labels, review rounds, reviewer IDs or issue-comment IDs appear in the source comments of the five new scripts, `memory_map.gen.py` or the added CI and builder comment lines. No RESIDUE arises from this rule. R4 and R5 are prose in the descriptions file, and the page's 6 `issuecomment` links are rulings carried from the old page.

## Prior public findings

Read only after this round's verdict and ledger were on disk (`receipts/verdict_preread.md`). The one earlier review on this PR is R753-1, at this same head. All its findings stay open here, and none is resolved at this head.

| R753 finding | State at this head | This round |
|---|---|---|
| F1 Reset `X` on 22 words | Retained, independently measured | F3. Rated MINOR here, MAJOR there; it blocks either way |
| F2 New register window stays fresh | Retained, same class reproduced | F1 rows 22-24, 35, 36 |
| F3 Reset change on a shadow word's flop | Retained, reproduced | F1 rows 20, 21 |
| F4 Opaque words, unread write arm published as read-only | Retained; wrong regeneration reproduced with its `chmap_sel` plant | F1 rows 30, 31 and further gaps |
| F5 Side effects not in the row | Retained; the 12 and 148 counts reproduced | F6 |
| F6 Gate does not read the notes | Retained; 30,097 words here against 31,033 there, because this round excludes table bars | F2 |
| F7 Prose against RTL or export | Retained, all five rows re-read | F4, with one added row |
| F8 Memory-map overprint | Retained, re-rendered | F5 |
| S1, S2 | Retained | S1, S2 |
| R1, R2, R3 | Retained | R1, R2, R3 |

## Hosted evidence at this head

Observed, not accepted; the manager owns acceptance.

- `rtl-fast` and `elaborate` concluded success.
- `docs` run 41098987728 concluded cancelled. Its `docs-gates-0` to `-2` and `docs-check-no-git` jobs succeeded, and `docs-check` was cancelled, so the new freshness step has no completed hosted run at this head. Local runs in this round and the author's receipts are its only execution evidence.
- `rtl-full` run 41098987841 concluded cancelled, and `verilator-suites` and `yosys-portability` concluded failure. This round did not establish the cause.

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3, F4, F6, F7) | #797 body and comments 6489587365, 6522974767, 6523093123; page layout; `receipts/compare_page.txt`; `receipts/sim_directed.txt`; dropped-fragment table | R754-1 | a8bcfba9426db350018c9cee95f4905fb364d8f0 |
| RTL | UNCLEAN (F1, F3) | `hdl/common/csr/milan_csr.sv` decodes, reset blocks, read muxes; `hdl/milan/milan_datapath.sv` instance; `receipts/attribution.txt`. No RTL file changed in this PR | R754-1 | a8bcfba9426db350018c9cee95f4905fb364d8f0 |
| Robustness | UNCLEAN (F1) | `scripts/register_rtl.py`, `register_fields.py`, `gen_register_reference.py`; `receipts/mutants.tsv`; `--soc-from` paths | R754-1 | a8bcfba9426db350018c9cee95f4905fb364d8f0 |
| Tests | UNCLEAN (F1, F2, F6) | `scripts/register_selftest.py`; selftest run; 39 plants; `scripts/check_doc_style.py`; `tests/features/counters_contract_milan.feature`; gate 18a expression | R754-1 | a8bcfba9426db350018c9cee95f4905fb364d8f0 |
| Docs | UNCLEAN (F2, F3, F4, F5, F6, F7, F8) | `docs/reference/REGISTER_MAP.md`, `REGISTER_MAP_CLASSES.md` diff, `docs/diagrams/README.md`, `memory_map.svg` and sampled `regmap` renders, `receipts/note_rows.txt` | R754-1 | a8bcfba9426db350018c9cee95f4905fb364d8f0 |

## Real limits

- **SoC export:** no LiteX here, so no export was rerun. The check used the published `csr.csv` and `aem_desc.json`. The export's generated top-level Verilog is not published, so `datapath_parameters` were checked against the shape config and the SoC source, not against a build.
- **Simulation scope:** it runs `milan_csr` alone at the shipping parameters, with handshake inputs tied and no engines. Window words were exercised at the reset selection and in the directed talker and out-of-range cases, not against an engine. Datapath wiring was read, not simulated.
- **Prose:** the 30,097 words of notes were sampled, not all checked. Statements about other blocks, the processor and silicon history were not verified.
- **Standards:** no IEEE or Milan text was read in this round. Clause conclusions rest on repository sources and are marked where they appear.
- **Gates:** the full behave suite, the builder bank and the Verilator and Yosys banks were not rerun. Author receipts report behave and the builder gate green and state that the Verilator sweep and Yosys were not run. No hardware was used. Physical calibration was not run, and field skips are not hardware proof.
- **Isolation:** before the verdict was on disk, this round read the #797 body, the two owner comments named in the brief by ID, the states of #599 and #70 and the body of #70, and the public author packet. It also made one read of the PR's `statusCheckRollup`, which is outside the two PR commands the brief allows. That read returned check names and conclusions only, with no review text, and no finding depended on it. Comment 6489587365 and the lane's takeover comment were read after the verdict and support F1 and F7 without changing them.
- **Restore:** `receipts/restore_check.txt` shows the exact head, tree, clean index, clean tracked bytes and modes, and the five required submodule gitlinks.

## Pending manager duties

- Hosted and act acceptance, including a completed `docs-check` at the final head.
- The current-dev merge candidate (builder and native banks) against live dev `1f29f189279f9fc0132f4918e47342b87d22f33a`.
- Carry R1 to R6 to the residue checklist.
- The ETH_GUARD decision, any exemption decision for F2 or F7, and lane conflict handling with PR #815.

R754-1 FINISHED
