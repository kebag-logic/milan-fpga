# HANDOFF — lane P141 ([A490])

Issue: Mister-M-alt/protocol-processor-control-plane-avb-milan #141 (assignment comment 5942683005).
Branch `pp141-clock-sources` from processor `main` `03c842a7`. Parent design: milan-fpga dev `cdf49d1a`,
`docs/design/MEDIA_CLOCK_FOLLOWING.md`, "Protocol-processor changes".

Head: `4a40b17` (`4a40b1798e463d09aafd74632408003229bcc673`; local branch; not pushed, no PR opened, per the
assignment's limits). The first REVIEW READY was at `39fd019`; `4a40b17` applies the reviewer's ruling
(#141 comment 5946147101) on the two sites flagged below.

| Commit | Item |
|---|---|
| `c8edfe5` | 1. Documentation: L6 and REQ-MDL-005 |
| `9afbc48` | 2. Tests at `tb/pp_top` (section D3C) and their six mutants |
| `39fd019` | 2. Records: `tb/pp_top/README.md`, 09 §8.2, REQ-AEM-013 |
| `4a40b17` | Ruling: 06 §6.4's SET_CLOCK_SOURCE row and the E_SCLKS comment in `gen_ucode.py` (comment only) |

## Status

- [x] Remote and base confirmed (origin is the processor repository; HEAD was `03c842a7`).
- [x] TAKEN posted on #141 (comment 5942693171).
- [x] Pre-check, no STOP (below).
- [x] Item 1: documentation (`c8edfe5`).
- [x] Item 2: tests and mutants (`9afbc48`, `39fd019`).
- [x] Processor suites, entry points and every campaign at the head: all rc 0 (one environmental re-run, below).
- [x] Parent consumer set at milan-fpga dev `cdf49d1a` + #137's line: 16 of 16 rc 0.
- [x] REVIEW READY posted on #141 with the head `39fd019153033b33ad2ce5fea72be05ddab526a8` (comment 5946139630).
- [x] Ruling (comment 5946147101) applied in one commit, `4a40b17`: 06:462 and the `gen_ucode.py` comment.
- [x] Every ROM regenerated at `39fd019` and `4a40b17`: byte-identical; the generator's non-comment tokens identical.
- [x] Docs checks, `make check` and `git diff --check` at `4a40b17`: all rc 0.
- [x] REVIEW READY posted again with the head `4a40b1798e463d09aafd74632408003229bcc673` (comment 5946201759).
  TAKEN was not posted again.

## Pre-check: no STOP

- SET range check `hdl/aecp/ucode/gen_ucode.py:1663-1664` at `4a40b17` (`:1662-1663` at `39fd019`; the ruling's
  comment gained one line above it): `CHECK_ARG` of the index (r12 = `{48'd0, index}`,
  `hdl/aecp/KL_aecp_engine.sv:1563`) against the located CLOCK_DOMAIN's `clock_sources_count`, `REL_LT`, 16 bits.
- Restore compare `hdl/aecp/KL_aecp_nvm_writer.sv:502`: `rval_r[15:0] < sb_rdata_i[47:32]`.
- The row is 16 bits (`hdl/aecp/KL_aecp_dyn_state.sv:186`); the top's `aecp_clk_src_index_o` is 16 bits.
- Both accept any index below the count, over a list of any length. `git diff 03c842a7..39fd019 -- hdl` is empty;
  `git diff 03c842a7..4a40b17 -- hdl` is the one comment in `gen_ucode.py` (+6 -5 lines), and every ROM is
  byte-identical (below).

## Item 1: documentation (c8edfe5)

Clauses read (IEEE 1722.1-2021 and Milan v1.2):

- Milan v1.2 §5.3.3.6: at least one CLOCK_SOURCE per Clock Domain; exactly one INPUT_STREAM source per
  CRF-capable Stream Input, or on the single AAF Stream Input when the Configuration has no CRF input;
  at least one INTERNAL source when the Configuration has a Stream Output. No count for an AAF input
  beside a CRF input.
- Milan v1.2 §5.4.2.15/.16: implement SET/GET_CLOCK_SOURCE per IEEE 7.4.23/7.4.24, and the lock
  refusal. No argument rule.
- IEEE 1722.1-2021 §7.2.32, Table 7-61: `clock_sources` is "the list of CLOCK_SOURCE descriptor indices
  which the clock_source_index may be set to"; `clock_sources_count` at most 216.
- IEEE 1722.1-2021 Table 7-141: BAD_ARGUMENTS (7), "one or more of the values in the fields of the frame
  were deemed to be bad".
- IEEE 1722.1-2021 §7.4.23.1: the response carries the current value (new on success, old on failure).
  It states no membership test; the old L6 text credited one to it.
- IEEE 1722.1-2021 §7.2.9.2, Table 7-17: INPUT_STREAM, "sourced from the media clock of an Input Stream".

| File:line | Change |
|---|---|
| `docs/architecture/07_memory_maps.md:135` (L6) | §5.3.3.6's set stated as a minimum; one INPUT_STREAM source per AAF input allowed beside the CRF input's (§7.2.9.2, Table 7-17); order INTERNAL 0, CRF 1, AAF input k at 2 + k (milan-fpga D1), the processor reading no order; the identity list of any length up to Table 7-61's 216; membership credited to IEEE 1722.1-2021 §7.2.32 and BAD_ARGUMENTS to Table 7-141 (carrying the current index, §7.4.23.1); Milan §5.4.2.15/.16 add no argument rule. Clause column: Milan v1.2 §5.3.3.6, §7.5; IEEE 1722.1-2021 §7.2.9.2, §7.2.32, Table 7-141, §7.4.23.1 |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:425` (REQ-MDL-005) | the same minimum, AAF allowance and order; BAD_ARGUMENTS credited to IEEE 1722.1-2021 §7.2.32 and Table 7-141, not to Milan §5.4.2.15/.16. Clause column gains IEEE 1722.1-2021 §7.2.32, Table 7-141; Arch column names the processor's range check over L6's identity list |

Item 2's records (`39fd019`):

| File:line | Change |
|---|---|
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:382` (REQ-AEM-013) | finding cell cites D3C1 to D3C4 (#141) beside D3S1/D3R1 |
| `docs/architecture/09_verification.md:206-212` (§8.2) | a D3C row; 87 controls in `d3_mutants.py`; D3C1/D3C2's two controls in `aecp_dispatch_mutants.py` (`d3` target) |
| `tb/pp_top/README.md:249-279` | section D3C under "What it proves" |
| `tb/pp_top/README.md:887-987` (D3 negative controls) | 87 KILLED; five moved counts explained; four new rows (984-987) |
| `tb/pp_top/README.md:1050-1152` (AECP dispatch controls) | the `d3` target; two new rows (1106-1107) and their failure sets (1147-1152) |

Flagged at `39fd019` for a ruling, fixed in `4a40b17` (next section):

- `docs/architecture/06_aecp_engine.md:462` (06 §6.4, SET_CLOCK_SOURCE row) said the bound equals
  "the membership test of IEEE §7.4.23.1".
- `hdl/aecp/ucode/gen_ucode.py:1629-1633` (comment) said "the membership test §7.4.23.1 asks for".

## Ruling applied (4a40b17)

The reviewer's ruling (#141 comment 5946147101): fix both sites in this lane, crediting the membership test to
IEEE 1722.1-2021 §7.2.32 and Table 7-141 as L6 does; the generator change is a comment only, proven by
regenerating every ROM; run the docs checks, `make check` and `git diff --check`; no campaign re-run.

| File:line | Change | Clause |
|---|---|---|
| `docs/architecture/06_aecp_engine.md:462` (06 §6.4, SET_CLOCK_SOURCE row) | "the membership test of IEEE §7.4.23.1" becomes "the membership test of IEEE 1722.1-2021 §7.2.32 (`clock_sources`, the indices `clock_source_index` may be set to)"; the refusal reads "`BAD_ARGUMENTS` (IEEE 1722.1-2021 Table 7-141) carrying the CURRENT index (the value GET_CLOCK_SOURCE reads; §7.4.23.1)", as L6 words it | IEEE 1722.1-2021 §7.2.32, Table 7-141, §7.4.23.1 |
| `hdl/aecp/ucode/gen_ucode.py:1629-1638` (E_SCLKS range-check comment; was 1629-1637) | "the membership test §7.4.23.1 asks for" becomes "the membership test of IEEE 1722.1-2021 §7.2.32 (clock_sources, the indices clock_source_index may be set to)"; "BAD_ARGUMENTS (Table 7-141) carrying the CURRENT index"; the rest of the paragraph re-wrapped, words unchanged | IEEE 1722.1-2021 §7.2.32, Table 7-141 |

Left as they are: the other §7.4.23.1 citations in the tree (`gen_ucode.py:158`, `:1619`, `:1643`, `:1752`;
06:731; `tb/pp_top`; `KL_aecp_engine.sv:1032`, `:3431`) cite it for the command or for the response
carrying the current value, which is what §7.4.23.1 says. No other site credits a membership test to it.
No file cites `gen_ucode.py` by line, so the one added line moves no reference.

ROM proof: each tree exported with `git archive <commit> hdl` into scratch and every generator run there
(`gen_ucode.py -o ucode.hex`, `gen_ltn_rom.py -o ltn_rom.hex`, and the descriptor image
`gen_desc_image.py -i example_milan_8.json -o image.bin -m image.map`, the three generators the tree's
Makefiles and `syn/yosys/run.sh` call). `cmp` finds every output identical; files kept in scratch only.

| Output | Bytes | sha256 at `39fd019` | sha256 at `4a40b17` |
|---|---:|---|---|
| `ucode.hex` (2048 words, 87 programs) | 26,624 | `3559d0a64b51062a4dc47744ead112a0cc839f389bb2d16ba0133b03baf4b053` | same |
| `ltn_rom.hex` (128 x 32 b) | 6,138 | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | same |
| `image.bin` | 1,880 | `20356f5967e45a9eafcf8a63c5c933dca75fccb5d6bbc16941dc91dc2483b62c` | same |
| `image.map` | 772 | `23a43044fb99a73dad794de102be27d31d938c0d5b758c5c2cbbdcbee895091c` | same |

`diff -rq` of the two `hdl/` exports reports `gen_ucode.py` alone; a Python `tokenize` pass over both
versions, dropping comment and blank-line tokens, finds the 13,424 remaining tokens identical.

| Command at `4a40b17` | rc | Result |
|---|---:|---|
| `make check` | 0 | 41 mermaid + 18 wavedrom, 1,017 links, 115 REQ rows / 17 GAPs, 94 module rows / 0 untested, 26 parameters |
| CI docs job one by one: `check-links.py`, `check-matrix.py`, `check-integrator-params.py`, `render-wavedrom.py --check`, `make stale`; and `gen_matrix.py --check` | 0 each | the same figures |
| `git diff --check 39fd019 HEAD`, `git diff --check 03c842a7 HEAD` | 0, 0 | |
| `python3 scripts/check_upc_map.py` (parses `gen_ucode.py`) | 0 | 59 engine constants, 87 entry points agree |
| `python3 scripts/check_m9_opcodes.py` | 0 | 30 engine opcodes, all swept by M9 |

Not re-run at `4a40b17`, per the ruling's targeted re-measure rule (comment-only change, ROMs identical): the
suites, entry points and campaigns below, and the parent consumer set. Their results are at `39fd019`, whose
RTL and ROMs equal `4a40b17`'s.

## Item 2: tests and their mutants

Section D3C, `tb/pp_top/d3_phases.hpp:2745-2998` (`D3ClockSourcePhase`, run from `run_d3`,
`tb/pp_top/sim_main.cpp:10747`), on a fresh model over the suite image re-packed with a ten-source
identity list (`d3_image_with_sources`, `tb/pp_top/d3_phases.hpp:911`; the shared re-packer
`d3_image_repacked` at `:864`, D3R3b's image byte-identical). The wrap connects the top's
`aecp_clk_src_index_o` (`tb/pp_top/pp_top_wrap.sv:339`, `:583`). 17 new checks; D3 150 (was 133);
`tb/pp_top` 8,918 (was 8,901).

| Test (assignment item 2) | Checks | Mutant that fails it (driver) | Its failing checks |
|---|---|---|---|
| SET_CLOCK_SOURCE over a 10-source domain accepts 9, notifies once, reads back | D3C1 (SUCCESS byte-exact; exactly one unsolicited to a registered second controller; one store write, NVM_MARK and NOTIFY_ENQ; GET, row and export read 9) | `sclks-bound-three` (aecp_dispatch_mutants.py, `d3`): E_SCLKS's bound the constant 3; `clks_row_two_bits` (d3_mutants.py): the row keeps 2 bits | 11; 10 |
| index 10 answers BAD_ARGUMENTS carrying the current index, stores and notifies nothing | D3C2 (byte-exact refusal carrying 9; no write, mark, enqueue or unsolicited frame; GET, row, export 9; nothing pending and no device operation for two windows) | `sclks-bound-inclusive` (aecp_dispatch_mutants.py, `d3`): `count >= index` | 6 |
| a saved AAF index survives the D3 save and restore (REQ-AEM-013, the D3S1/D3R1 pair) | D3C3 save (one ERASE and WRITE of 0x0A, byte-exact, no other record); D3C3 restore (COMPLETE 1/0/26 of 27 from cleared rows; row, GET, export 9) | `clks_restore_count_narrowed` (d3_mutants.py): the rule reads the count's low 3 bits; also `clks_row_two_bits` (save), `TRG_clks`, `RPL_clks` | 2; 10 |
| a saved index at or above a smaller image's count is refused on restore | D3C4 at the count (9 of 9) and above it (9 of 3): COMPLETE 0 applied, 1 refused; row unset, GET and export 0 | `clks_restore_index_narrowed` (d3_mutants.py): the rule compares the index's low 3 bits; `clks_restore_bound_inclusive`: `<=` (the at-the-count arm, and D3R2) | 4; 4 |

In the whole default build (8,624 checks, scratch copies), `sclks-bound-three` fails D3C's 11 checks and
nothing else, and `clks_row_two_bits` D3C's 10: the three-source suite could not see either defect.
Five existing D3 controls now also fail D3C checks (README records each): `TRG_clks` 5 -> 10,
`RPL_clks` 3 -> 5, `rule_ignored` 3 -> 7, `unframed_reads_as_device_error` 38 -> 42,
`done_without_d3` 42 -> 45. Every other recorded count is unchanged.

## Processor gates at the head 39fd019

Pinned Verilator 5.050 through a scratch shim that caps `--build -j 0` at 8 jobs; one command at a time;
from a tree with every build product deleted (`git clean -fdX` first). Logs in scratch, not here.

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | 33 suites, 1,018,860 checks, 0 failing; `tb/pp_top` 8,918 |
| `./scripts/lint_hdl.sh` | 0 | 41 modules LINT OK |
| `make check` | 0 | 41 mermaid + 18 wavedrom, 1,017 links, 115 REQ rows / 17 GAPs, 94 module rows, 26 parameters |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `git diff --check 03c842a7 HEAD` | 0 | |
| `make -C tb/pp_top name-writes` / `gsi-internal` / `maap-internal` / `adp-config` / `deadline` / `d3` / `hazards` / `budget` / `aecp-dispatch` / `aecp-line` | 0 each | 85 / 6,182 / 34 / 55 / 64 / 150 / 176 / 56 / 915 / 218 checks, 0 failures |
| `tb/pp_top/obj_dir/Vpp_top_sim --acmp-only` | 0 | 43 checks |
| `make -C tb/pp_top` (before the sweep, clean) | 0 | 8,918: default 8,624, fixture 20, line 218, timebase 56 |

| Campaign | rc | Result |
|---|---:|---|
| `make -C tb/pp_top aecp-mutants` | 0 | 5 controls PASS, 55 of 55 KILLED; the one `d3`-target arm fails its recorded 1 |
| `make -C tb/pp_top aecp-dispatch-mutants` | 0 | 4 controls PASS (now incl. `d3`), 37 of 37 KILLED; every count equals the README |
| `python3 tb/pp_top/d3_mutants.py --jobs 2` | 0 | 87 of 87 KILLED, 3 goldens PASS; all 75 `tb/pp_top` rows equal the README |
| `python3 tb/pp_top/acmp_mutants.py --jobs 1` | 0 | 19 of 19 KILLED, 3 goldens; every count equals #137's table |
| `python3 tb/pp_top/gsi_mutants.py` | 0 | 20 detected; golden and restored PASS |
| `python3 tb/pp_top/name_wr_mutant.py` | 0 | killed |
| `make -C tb/maap mutants` | 0 | 32 of 32 |
| `make -C tb/adp_engine mutants` | 0 | 32 of 32 |
| `make -C tb/srp_top mutants` | 0 | 90 of 90, assertion coverage 65/65 |
| `make -C tb/nvm_port figures` | 2, then 0 | first run: `measure_figures.py` could not read `dc354be~1` and `62d96d6~1` (this checkout's object store lacked both; not shallow). Fetched by full SHA from origin, objects only, no ref or branch change; re-run: all measured figures agree with the tree |
| `python3 tb/acmp_talker/retry_mutants.py` | 0 | 62 killed, 7 equivalence, 1 performance control |
| `python3 tb/srp_admission/mutants.py` | 0 | 12 of 12 |
| `python3 tb/desc_mem_guard/mutate.py` | 0 | detected |

## Parent consumer set

Run at `39fd019`; not re-run at `4a40b17` (comment-only change, every ROM byte-identical; the ruling's
targeted re-measure rule). Gate 3's pin line would name the new head. The parent reads `gen_ucode.py` in two
ways, both unchanged by a comment: `sw/builder/aem_image_checks.py:22-25` parses it with `ast` (comments are
not in the tree; the non-comment tokens are identical), and the `pp_shadow`, `milan_dp` and `milan_dp_render`
Makefiles generate `ucode.hex` from it (byte-identical, above).

Scratch parent: a `git archive` of the read-only checkout at milan-fpga dev `cdf49d1a`. Its index (984
entries) and tree (`904f3079`) equal the checkout's. `gptp-processor` (`5dce647a`) and
`third_party/verilog-axis` (`48ff7a7e`) are at their recorded pins, fetched from their recorded URLs
because the checkout carries no submodule contents. `external` is recorded and uninitialized, as in
the checkout. `protocol-processor` is a clone of this branch at `39fd019`, with the gitlink staged.
#137's `acmp_mutants.py` disposition line (+4 lines in `scripts/measure_test_evidence.py`, the text
in #137's body) is the only other change; `scripts/test_evidence.budget` is untouched. The trusted
checkout was never modified. The gates ran one at a time, Verilator 5.050; `xvlog` (bench Vivado 2026.1)
ran alone.

| # | Gate | rc | Result |
|---:|---|---:|---|
| 1 | `python3 scripts/check_cpp_idiom.py` | 0 | every ratchet held |
| 2 | `python3 scripts/check_py_idiom.py` | 0 | every ratchet held |
| 3 | `python3 scripts/xvlog_gate.py --check` | 0 | 4 findings == ratchet, none new; pinned at protocol-processor@39fd0191 |
| 4 | `python3 scripts/check_rtl_source_lists.py` | 0 | 36/42 tops, 6 recorded |
| 5 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | |
| 6 | `python3 sw/builder/test_builder.py` | 0 | all gates pass except 1 not run (calibration gate: board build tree not on this host) |
| 7 | `make -C tb/verilator/pp_shadow -j8` | 0 | 606, 606, 646, 311 checks, 0 failures |
| 8 | `python3 scripts/check_port_contracts.py` | 0 | 48 literal-bound, 59 without a rationale, lowerable by 3 |
| 9 | `python3 scripts/measure_naming.py --check` | 0 | 96 recorded |
| 10 | `python3 scripts/measure_test_evidence.py --check` | 0 | 72 <= 77, 10 <= 10, 0 <= 0 unexplained DUT readers, 3 <= 3 wall-clock files; same after the builds |
| 11 | `python3 scripts/docs_check.py` | 0 | 0 findings |
| 12 | `make -C tb/verilator/nvm_cosim lint` | 0 | |
| 13 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315 of 315 |
| 14 | `make -C tb/verilator/milan_dp -j8` | 0 | every RESULT PASS (9) |
| 15 | `make -C tb/verilator/milan_dp_render -j8` | 0 | leg defects 5/5 |
| 16 | `python3 scripts/lint_rtl.py --check` | 0 | 90 <= 90 |

## Parent-visible

- No interface or behaviour change: `git diff 03c842a7..4a40b17 -- hdl` is one comment in `gen_ucode.py`;
  every ROM is byte-identical to `39fd019`'s (and `39fd019`'s `hdl/` equals `03c842a7`'s). No port,
  parameter, register-map or microcode change. The processor RTL differs from the parent's pin `b2db3a97`
  only by main's own merges (#135 to #140); the parent set above ran them with the gitlink at `39fd019`.
- No new parent registry entry and no budget change from this lane: `d3_mutants.py` (already
  dispositioned) gains four saved-state controls; `aecp_dispatch_mutants.py` applies patches and reads
  logs only. #137's `acmp_mutants.py` line is still owed by the pin bump.
- Processor totals at this head: `tb/pp_top` 8,918, section D3 150, the sweep 1,018,860; no parent file
  at `cdf49d1a` quotes them.
- For adoption: the parent design (`docs/design/MEDIA_CLOCK_FOLLOWING.md:1272`) can cite `tb/pp_top`
  D3C1 to D3C4 (D3C3 is the D3S1/D3R1 pair for an AAF index); the parent's own L6
  (`docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:89`) still credits "IEEE 7.4.23.1", already on the
  design's documentation list.
- The design's processor documentation item (`MEDIA_CLOCK_FOLLOWING.md:1261-1266`: L6, REQ-MDL-005 and
  the range-check comment) is now met in full; 06 §6.4's row, which the design does not name, credits
  the same clauses. The design's line cites are against the pin `b2db3a97` (`gen_ucode.py:1414`,
  `:1410-1440`); at this head the comment is `gen_ucode.py:1629-1638` and the program `:1649-1686`
  (E_SCLKS and its out-of-line tail E_SCLKSRF).
- `aecp_clk_src_index_o` is unchanged; only the processor bench now connects it.
- CI: the processor's `make -C tb/pp_top aecp-dispatch-mutants` step now also runs the `d3` control and
  two arms (the whole campaign took 747 s here).

## Environment notes

- `make -C tb/nvm_port figures` first failed (rc 2): `measure_figures.py` reads `dc354be~1` and
  `62d96d6~1`, absent from this checkout's object store (not shallow; no remote branch still holds
  them). Both were fetched from origin by full SHA (objects only, no ref or branch change); the re-run
  is rc 0. Not caused by this lane.
- Verilator: the pinned 5.050 through a scratch wrapper that turns the suites' `--build -j 0` into
  `-j 8`; long runs were started detached in scratch and waited on in the foreground until done.
- Build products were removed from the tree at the end (`git clean -fdX`); scratch stays under
  the scratch area, nothing large is in this directory.
- At `4a40b17`, `make check` and `render-wavedrom.py --check` bootstrap the ignored `.venv-wavedrom/` in
  the tree; it was removed after each run (`git clean -fdX`), and the tree is clean.

## Files in this directory

- `HANDOFF.md` (this file), `PR-BODY.md` (the PR description, for whoever opens the PR).
