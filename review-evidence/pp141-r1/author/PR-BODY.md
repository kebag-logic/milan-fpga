[A490]

Closes #141

Lane P141 for #141 (assignment: #141 comment 5942683005), the processor part of milan-fpga #629. The design is milan-fpga `docs/design/MEDIA_CLOCK_FOLLOWING.md`, section "Protocol-processor changes", at dev `cdf49d1a`. Branch `pp141-clock-sources` from `main` `03c842a7`, one or more commits per item, in the assignment's order:

| Commit | Item |
|---|---|
| `c8edfe5` | 1. Documentation: L6 (07 §3.1) and REQ-MDL-005 |
| `9afbc48` | 2. Tests at `tb/pp_top`, section D3C, and their six mutants |
| `39fd019` | 2. Their records: the `tb/pp_top` README, 09 §8.2 and REQ-AEM-013 |
| `4a40b17` | Review ruling (#141): 06 §6.4's SET_CLOCK_SOURCE row and the E_SCLKS comment in `gen_ucode.py` credit the membership test to IEEE 1722.1-2021 §7.2.32 and Table 7-141 |

No RTL or microcode change, as the issue expected. The only `hdl/` change is one comment in `hdl/aecp/ucode/gen_ucode.py`, and every generated ROM is byte-identical to the base's (below). No port, parameter or register-map change.

## The pre-check: no STOP

Both checks already accept any index below `clock_sources_count`, over a list of any length:

- The SET range check, `hdl/aecp/ucode/gen_ucode.py:1663-1664`: `CHECK_ARG` of the index against the located domain's `clock_sources_count`, `REL_LT`, over 16 bits. The index arrives in r12 as `{48'd0, index}` (`hdl/aecp/KL_aecp_engine.sv:1563`).
- The restore compare, `hdl/aecp/KL_aecp_nvm_writer.sv:502`: `rval_r[15:0] < sb_rdata_i[47:32]`.
- The row that holds the index is 16 bits wide (`hdl/aecp/KL_aecp_dyn_state.sv:186`), and so is the exported `aecp_clk_src_index_o`.

## 1. Documentation (`c8edfe5`)

Clauses, read in IEEE 1722.1-2021 and Milan v1.2:

- **Milan v1.2 §5.3.3.6** requires at least one CLOCK_SOURCE per Clock Domain and at least one INTERNAL source when the Configuration has a Stream Output. It requires exactly one INPUT_STREAM source per CRF-capable Stream Input, or one on the single AAF Stream Input when the Configuration has no CRF input. It sets no count for an AAF input beside a CRF input.
- **Milan v1.2 §5.4.2.15/.16** require SET/GET_CLOCK_SOURCE as IEEE 7.4.23/7.4.24 specify them, and §5.4.2.15 adds the lock refusal. Neither states an argument rule.
- **IEEE 1722.1-2021 §7.2.32, Table 7-61**: `clock_sources` is "the list of CLOCK_SOURCE descriptor indices which the clock_source_index may be set to", with `clock_sources_count` at most 216.
- **IEEE 1722.1-2021 Table 7-141**: BAD_ARGUMENTS (7), "one or more of the values in the fields of the frame were deemed to be bad".
- **IEEE 1722.1-2021 §7.4.23.1**: the response carries the current value, the new one on success and the old one on failure. It states no membership test; the old L6 text credited one to it.
- **IEEE 1722.1-2021 §7.2.9.2, Table 7-17**: INPUT_STREAM, "sourced from the media clock of an Input Stream", so an AAF STREAM_INPUT is a valid location.

| Site | Change |
|---|---|
| `docs/architecture/07_memory_maps.md:135`, L6 | §5.3.3.6's set is stated as a minimum. One INPUT_STREAM source per AAF input is allowed beside the CRF input's (§7.2.9.2, Table 7-17). The order is INTERNAL 0, CRF 1, AAF input k at 2 + k (milan-fpga D1), and the processor reads no order. The identity list may have any length up to Table 7-61's 216. Membership is credited to IEEE 1722.1-2021 §7.2.32, BAD_ARGUMENTS to Table 7-141, the current index in the refusal to §7.4.23.1, and Milan §5.4.2.15/.16 add no argument rule. The clause column now reads Milan v1.2 §5.3.3.6, §7.5; IEEE 1722.1-2021 §7.2.9.2, §7.2.32, Table 7-141, §7.4.23.1. |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:425`, REQ-MDL-005 | The same minimum, AAF allowance and order. BAD_ARGUMENTS is credited to IEEE 1722.1-2021 §7.2.32 and Table 7-141, not to Milan §5.4.2.15/.16. The clause column gains IEEE 1722.1-2021 §7.2.32 and Table 7-141; the Arch column names the processor's range check over L6's identity list. |

### The two sites the review ruled on (`4a40b17`)

Two more sites credited the bound's membership test to IEEE §7.4.23.1. The review ruled that both be fixed here, crediting the test as L6 does:

| Site | Change |
|---|---|
| `docs/architecture/06_aecp_engine.md:462`, 06 §6.4's SET_CLOCK_SOURCE row | The bound equals "the membership test of IEEE 1722.1-2021 §7.2.32 (`clock_sources`, the indices `clock_source_index` may be set to)". The refusal is "`BAD_ARGUMENTS` (IEEE 1722.1-2021 Table 7-141) carrying the CURRENT index (the value GET_CLOCK_SOURCE reads; §7.4.23.1)". |
| `hdl/aecp/ucode/gen_ucode.py:1629-1638`, the E_SCLKS range-check comment | "the membership test of IEEE 1722.1-2021 §7.2.32 (clock_sources, the indices clock_source_index may be set to)" and "BAD_ARGUMENTS (Table 7-141)". The rest of the paragraph is re-wrapped, with its words unchanged. |

The other §7.4.23.1 citations in the tree are left as they are: they cite it for the command, or for the response carrying the current value, which is what that clause says.

The generator change is a comment only. To prove it, each tree's `hdl/` was exported with `git archive` at `39fd019` and at `4a40b17`, and every generator was run in each. `39fd019`'s `hdl/` equals the base `03c842a7`'s. Every output is byte-identical:

| Output | Bytes | sha256 (both heads) |
|---|---:|---|
| `ucode.hex`, from `gen_ucode.py` (2048 words, 87 programs) | 26,624 | `3559d0a64b51062a4dc47744ead112a0cc839f389bb2d16ba0133b03baf4b053` |
| `ltn_rom.hex`, from `gen_ltn_rom.py` | 6,138 | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` |
| `image.bin`, from `gen_desc_image.py` over `example_milan_8.json` | 1,880 | `20356f5967e45a9eafcf8a63c5c933dca75fccb5d6bbc16941dc91dc2483b62c` |

`gen_ucode.py` is the only `hdl/` file that differs between the two exports. With comment and blank-line tokens dropped, its 13,424 Python tokens are identical. No file cites `gen_ucode.py` by line number, so the one added line moves no reference.

## 2. Tests: `tb/pp_top` section D3C (`9afbc48`, `39fd019`)

`D3ClockSourcePhase` (`tb/pp_top/d3_phases.hpp`) runs in section D3 (`make -C tb/pp_top d3`, `--d3-only`) on a fresh model. Its image is the suite's own, re-packed by the bench's independent packer with a ten-source identity list: INTERNAL 0, CRF 1 and AAF inputs 0 to 7 at 2 to 9, the 8x8 shape. The suite's own image lists three sources. Neither image carries a CLOCK_SOURCE descriptor, because neither the SET program nor the restore rule reads one. The arms run in the order D3C1, D3C3's save, D3C2, D3C3's restore, D3C4, so the refusal is graded against a row that is already saved, and a refusal that stored anything would show as a second save.

| Check | What it grades (17 checks) |
|---|---|
| D3C1 (6, two of them premises) | SET_CLOCK_SOURCE(9), AAF input 7, answers SUCCESS byte-exact carrying 9. A registered second controller receives exactly one unsolicited SET_CLOCK_SOURCE carrying 9, sequence 0. The store write, NVM_MARK and NOTIFY_ENQ strobes each move once. GET_CLOCK_SOURCE reads 9 byte-exact, and so do the row and the top's exported `aecp_clk_src_index_o`. |
| D3C2 (4) | SET_CLOCK_SOURCE(10), the count itself, answers BAD_ARGUMENTS byte-exact carrying the 9 in force. It writes, marks and enqueues nothing, and the second controller hears nothing. GET, the row and the export still read 9. Nothing is pending and the device sees no operation for two debounce windows. |
| D3C3 (3) | The D3S1/D3R1 pair for an AAF index (REQ-AEM-013). The save is exactly one ERASE and one WRITE of record 0x0A, the byte-exact F07.8 frame of 9, with no other record moving. Across a power cycle the walk starts from cleared rows and ends COMPLETE (1 applied, 0 refused, 26 blank of 27); the row with its valid flag, GET and the export read 9. |
| D3C4 (4) | The record D3C3 saved, restored over a nine-source image (at the count) and over the suite's three-source image (above it). Each walk refuses it and ends COMPLETE (0 applied, 1 refused); the row stays unset, and GET and the export read the image's 0. |

The wrap now connects the top's `aecp_clk_src_index_o` to a bench output; it was left open before. This is a test-harness change only. The rate image helper became `d3_image_repacked`, shared by D3R3b's ten-rate image and D3C's source lists; D3R3b's image is byte-identical.

### The mutants

Each test has at least one mutant that fails it, and each mutant is KILLED by its named check in a completed run:

| Mutant | Driver | Defect | Named check | Failing checks |
|---|---|---|---|---|
| `sclks-bound-three` | `aecp_dispatch_mutants.py`, `d3` target | E_SCLKS's bound is the constant 3, the suite list's count | `D3C1: SET_CLOCK_SOURCE(9) ...` | 11: every D3C check built on the accepted 9 |
| `sclks-bound-inclusive` | `aecp_dispatch_mutants.py`, `d3` target | E_SCLKS accepts `count >= index` | `D3C2: SET_CLOCK_SOURCE(10) ...` | 6: D3C2's four, and D3C3's two restore checks, whose saved 10 the restore rule refuses |
| `clks_row_two_bits` | `d3_mutants.py` | the clock-source row stores the index's low two bits | `D3C1 readback`, `D3C3 save` | 10 |
| `clks_restore_count_narrowed` | `d3_mutants.py` | the restore rule reads the count's low three bits | `D3C3 restore` | 2 |
| `clks_restore_index_narrowed` | `d3_mutants.py` | the restore rule compares the index's low three bits | `D3C4 at the count`, `D3C4 above the count` | 4 |
| `clks_restore_bound_inclusive` | `d3_mutants.py` | the restore rule accepts index == count | `D3C4 at the count` | 4: D3C4's at-the-count pair and D3R2's two |

Four of the six fail only D3C checks wherever they were run:

- With `sclks-bound-three` or `clks_row_two_bits` planted, the whole default build (8,624 checks) fails D3C's 11 and 10 checks, and nothing else. They were run in scratch copies.
- In section D3, the two narrowed restore rules fail only D3C checks.
- The inclusive restore bound also fails D3R2, whose "clock source 3 of 3" is the only other check in section D3 that grades the bound.

The new D3C checks also raise the failing counts of five existing D3 controls; the `tb/pp_top` README records each one: `TRG_clks` (5 to 10), `RPL_clks` (3 to 5), `rule_ignored` (3 to 7), `unframed_reads_as_device_error` (38 to 42) and `done_without_d3` (42 to 45). Every other recorded count is unchanged. The `aecp_dispatch_mutants.py` campaign gains the `d3` target, so CI's `make -C tb/pp_top aecp-dispatch-mutants` step now also runs one `d3` control and two arms.

Records: `tb/pp_top/README.md` (section D3C under "What it proves"; the D3 and the AECP dispatch mutation tables), `docs/architecture/09_verification.md` §8.2 (a D3C row; 87 controls), and REQ-AEM-013's finding cell (D3C1 to D3C4 beside D3S1/D3R1).

## Validation

At the head `4a40b17`, after the ruling's comment-only commit, all rc 0:

| Command | Result |
|---|---|
| `make check` | 41 mermaid and 18 wavedrom blocks, 1,017 links, 115 REQ rows, 17 GAP findings, 94 module rows with 0 untested, 26 parameters |
| CI's docs job, one by one: `check-links.py`, `check-matrix.py`, `check-integrator-params.py`, `render-wavedrom.py --check`, `make stale`; and `gen_matrix.py --check` | the same figures |
| `git diff --check 39fd019 HEAD` and `git diff --check 03c842a7 HEAD` | clean |
| `scripts/check_upc_map.py`, which parses `gen_ucode.py` | 59 engine constants and 87 entry points agree |
| `scripts/check_m9_opcodes.py` | 30 engine opcodes, all swept by M9 |

Under the targeted re-measure rule, a comment-only change with identical ROMs re-runs no campaign. The suites, campaigns and parent consumer gates below ran at `39fd019`, whose RTL and ROMs equal this head's.

Every command below ran at `39fd019`, one at a time, with Verilator 5.050 and builds capped at eight jobs. The run started from a tree with every build product deleted. All are rc 0:

| Command | Result |
|---|---|
| `./scripts/run_suites.sh` | 33 suites, 1,018,860 checks, 0 failing. `tb/pp_top` has 8,918 (default 8,624, fixture 20, line 218, timebase 56); the 17 new checks are section D3's (150; 133 at the base) |
| `./scripts/lint_hdl.sh` | 41 modules |
| `make check` | 1,017 links, 115 REQ rows, 17 GAP findings |
| `python3 scripts/gen_matrix.py --check` | 94 rows, 0 untested |
| `git diff --check 03c842a7 HEAD` | clean |
| `make -C tb/pp_top` targets `name-writes`, `gsi-internal`, `maap-internal`, `adp-config`, `deadline`, `d3`, `hazards`, `budget`, `aecp-dispatch`, `aecp-line`, and `--acmp-only` | 85, 6,182, 34, 55, 64, 150, 176, 56, 915, 218 and 43 checks, 0 failures each |

| Campaign | Result |
|---|---|
| `make -C tb/pp_top aecp-mutants` | 5 controls PASS, 55 of 55 KILLED; the one `d3`-target arm fails its recorded 1 |
| `make -C tb/pp_top aecp-dispatch-mutants` | 4 controls PASS (`d3` new), 37 of 37 KILLED; every count equals the README |
| `python3 tb/pp_top/d3_mutants.py --jobs 2` | 87 of 87 KILLED, 3 goldens PASS; all 75 `tb/pp_top` rows equal the README |
| `python3 tb/pp_top/acmp_mutants.py --jobs 1` | 19 of 19 KILLED, 3 goldens PASS; every count equals #137's table |
| `python3 tb/pp_top/gsi_mutants.py` | 20 detected; golden and restored PASS |
| `python3 tb/pp_top/name_wr_mutant.py` | killed |
| `make -C tb/maap mutants` | 32 of 32 |
| `make -C tb/adp_engine mutants` | 32 of 32 |
| `make -C tb/srp_top mutants` | 90 of 90, assertion coverage 65/65 |
| `make -C tb/nvm_port figures` | all measured figures agree with the tree (see below) |
| `python3 tb/acmp_talker/retry_mutants.py` | 62 killed, 7 equivalence and 1 performance control |
| `python3 tb/srp_admission/mutants.py` | 12 of 12 |
| `python3 tb/desc_mem_guard/mutate.py` | detected |

`make -C tb/nvm_port figures` first failed, rc 2:

- `measure_figures.py` could not read `dc354be~1` and `62d96d6~1`, two historical revisions that `tb/nvm_port/pre_fix_forms.py` pins. This checkout's object store lacked them; it is not shallow, and no remote branch still holds them.
- Both commits were fetched from origin by full SHA. The fetch took objects only: no ref, branch or tree file changed.
- Re-run alone at the same head, the check is rc 0.

The fault is in the checkout, not in this lane's change.

## Parent consumer gates

The scratch parent was built as follows:

- It is a `git archive` of a read-only checkout at milan-fpga dev `cdf49d1a`. Its index (984 entries) and its tree (`904f3079`) equal that checkout's.
- Submodules:
  - `gptp-processor` (`5dce647a`) and `third_party/verilog-axis` (`48ff7a7e`) are at their recorded pins. They were fetched from their recorded URLs, because that checkout carries no submodule contents.
  - `external` is recorded and uninitialized, as in the checkout.
  - `protocol-processor` is a clone of this branch at `39fd019`, with the gitlink staged at it.
- #137's `acmp_mutants.py` disposition line (+4 lines in `scripts/measure_test_evidence.py`, the text in #137's body) is applied. Apart from the gitlink, it is the only change against `cdf49d1a`. `scripts/test_evidence.budget` is untouched.

The gates ran one at a time with Verilator 5.050, and `xvlog` from the bench Vivado 2026.1 never ran beside a Verilator build. All 16 are rc 0:

| # | Gate | Result |
|---:|---|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | every ratchet held |
| 3 | `xvlog_gate.py --check` | 4 findings == ratchet, none new, pinned at `protocol-processor@39fd0191` |
| 4, 5 | `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | 36/42 tops, 6 recorded |
| 6 | `sw/builder/test_builder.py` | all gates pass except 1 not run: the calibration gate needs a board build tree that is not on this host |
| 7 | `make -C tb/verilator/pp_shadow -j8` | 606, 606, 646 and 311 checks, 0 failures |
| 8 | `check_port_contracts.py` | 48 literal-bound, 59 without a rationale, lowerable by 3 |
| 9 | `measure_naming.py --check` | 96 recorded |
| 10 | `measure_test_evidence.py --check` | 72 <= 77 suites without a mutation arm, 0 <= 0 unexplained DUT-source readers, 3 <= 3 wall-clock-dependent files; the same after the builds |
| 11 | `docs_check.py` | 0 findings |
| 12, 13 | `make -C tb/verilator/nvm_cosim lint`, `quick` | 315 of 315 |
| 14 | `make -C tb/verilator/milan_dp -j8` | every RESULT PASS (9) |
| 15 | `make -C tb/verilator/milan_dp_render -j8` | leg defects 5/5 |
| 16 | `lint_rtl.py --check` | 90 <= 90 |

## Parent-visible list

- **No interface or behaviour change.**
  - The only `hdl/` change is one comment in `gen_ucode.py`, and every ROM is byte-identical to the base's. No port, parameter, register-map or microcode change.
  - The processor RTL at this head is `main` `03c842a7`'s. Its differences from the parent's pin `b2db3a97` are main's own (#135 to #140), not this lane's. The parent set above ran them with the gitlink at `39fd019`.
  - The parent reads `gen_ucode.py` in two ways, and a comment changes neither. `sw/builder/aem_image_checks.py` parses it with `ast`, which drops comments. The `pp_shadow`, `milan_dp` and `milan_dp_render` builds generate `ucode.hex` from it, and that file is byte-identical.
- **No new parent registry entry from this lane, and no budget change.**
  - `d3_mutants.py` gains four controls inside its existing disposition: each plants one saved-state defect (the clock-source row or the restore rule) from its own table.
  - `aecp_dispatch_mutants.py` applies patches and reads only logs.
  - `measure_test_evidence.py --check` holds 0 <= 0 unexplained readers with #137's line alone. That line is still owed by the pin bump.
- **Processor totals at this head:** `tb/pp_top` has 8,918 checks, section D3 150, and the sweep 1,018,860. No parent file at `cdf49d1a` quotes these counts.
- **Names for adoption.**
  - The parent design's "Protocol-processor changes" (`docs/design/MEDIA_CLOCK_FOLLOWING.md:1272`) describes these tests. It can cite `tb/pp_top` D3C1 to D3C4; D3C3 is the D3S1/D3R1 pair for an AAF index.
  - The parent's own L6 (`docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:89`) still cites "IEEE 7.4.23.1". The processor's L6, 06 §6.4 and range-check comment now credit the membership to IEEE 1722.1-2021 §7.2.32 and BAD_ARGUMENTS to Table 7-141. The parent's row is already on the design's documentation list.
  - The design's processor documentation item (L6, REQ-MDL-005 and the range-check comment) is now met in full. Its line cites are against the pin `b2db3a97` (`gen_ucode.py:1414` and `:1410-1440`). At this head the comment is `gen_ucode.py:1629-1638`, and the program, E_SCLKS with its out-of-line tail E_SCLKSRF, is `:1649-1686`.
- **The top's `aecp_clk_src_index_o` is unchanged.** Only the processor's bench now connects it. The parent's `KL_pp_shadow` binding of it is untouched.
