[R430] POSITIVE - exact head 4a40b1798e463d09aafd74632408003229bcc673

# R430-1: independent internal review of protocol-processor PR #142 (closes #141)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head: `4a40b1798e463d09aafd74632408003229bcc673`, tree `b258cbd7b41dc2b96354173e9297427295be117b`
- Base: `03c842a780064048b0a1a3de29214174a1c13934` (processor `main`); four commits `c8edfe5`, `9afbc48`, `39fd019`, `4a40b17`
- Round: R430-1, a cleared-context reconstruction from public state. Review start: PR #142 comment 5946215199.
- Scope authorities: the #141 body; the assignment (#141 comment 5942683005); the ruling on the two flagged citation sites (#141 comment 5946147101, the newest [A10]); milan-fpga `docs/design/MEDIA_CLOCK_FOLLOWING.md` at dev `cdf49d1a`, its "Protocol-processor changes" section and decision D1; the parent `AGENTS.md` section 6 and `CONTRIBUTING.md` section 6 at `cdf49d1a`. The processor repository has no `AGENTS.md` or `CONTRIBUTING.md` of its own, so its `README.md` and `docs/README.md` conventions applied.
- Clause text was read in IEEE 1722.1-2021 and Milan v1.2 (Final, 2023-11-30). The specifications are not distributed and are not part of this packet.

## Verdict

**POSITIVE.** Every item of #141's frozen acceptance, and of the assignment and the ruling, is met in full at this head. No BLOCKER, MAJOR, MINOR or RESIDUE finding is open. Two SUGGESTIONs are recorded; neither makes the verdict NEGATIVE.

Prior public review findings on PR #142: **none exist.** The PR has no reviews and no inline comments, and its only issue comments are the two review-start notices. The [A10] ruling on #141 (comment 5946147101) flagged two citation sites. Both are resolved at this head; see row R below.

## Acceptance, item by item

| # | Item (issue body, assignment, ruling) | Result at head | Evidence |
|---|---|---|---|
| P | Pre-check: the SET range check and the restore check accept any index below `clock_sources_count`, over a list of any length; STOP otherwise | **Met, no STOP** | `hdl/aecp/ucode/gen_ucode.py:1660-1664`: the count is read from lane[47:32] into r9 with FMT_W, then `CHECK_ARG ra=12 rb=9 fmt=FMT_W REL_LT`. `hdl/aecp/KL_aecp_ucpu.sv:222-237,249`: the compare zero-extends `fmt(ra)` to 16 bits and runs a 33-bit unsigned subtract, so this is an unsigned 16-bit `index < count`. `hdl/aecp/KL_aecp_engine.sv:1563`: r12 is `{48'd0, setval_r[63:48]}`. `hdl/aecp/KL_aecp_nvm_writer.sv:502`: `rval_r[15:0] < sb_rdata_i[47:32]`, with the lane at `CD_SRCCNT_C = 72` (`:319`), whose bytes 74-75 are `clock_sources_count` (IEEE Table 7-61). `KL_aecp_dyn_state.sv:186,333,352`: the row, its write and the export are all 16 bits. |
| 1a | L6 and REQ-MDL-005 state Milan v1.2 5.3.3.6's set as a minimum | **Met** | `docs/architecture/07_memory_maps.md:135`; `docs/00_MILAN_COMPLIANCE_REVIEW.md:425`. Checked against Milan v1.2 5.3.3.6: "exactly one" binds each CRF-capable input, and the single AAF input when no CRF input exists; INTERNAL is "at least one"; no count is set for an AAF input beside a CRF input. |
| 1b | Allow one INPUT_STREAM source per AAF input beside the CRF input's | **Met** | Same two rows. L6 credits the location to IEEE 1722.1-2021 7.2.9.2, Table 7-17 (INPUT_STREAM: "sourced from the media clock of an Input Stream"), which I verified. |
| 1c | Order INTERNAL 0, CRF 1, AAF input k at 2+k (milan-fpga D1) | **Met** | Same two rows. This matches D1 = L1 in the design ("Source list and order"). L6 adds that the processor reads no order, which is true: neither path decodes the order. |
| 1d | BAD_ARGUMENTS credited to IEEE 1722.1-2021 7.2.32 and Table 7-141, not to Milan 5.4.2.15/16; 7.4.23.1 only for the response carrying the current index | **Met** | L6, REQ-MDL-005, `06_aecp_engine.md:462` and `gen_ucode.py:1629-1638`. Verified in the texts: Table 7-61 (in 7.2.32) defines `clock_sources` as "the list of CLOCK_SOURCE descriptor indices which the clock_source_index may be set to", maximum 216. Table 7-141 row 7 is BAD_ARGUMENTS. 7.4.23.1 says "The response always contains the current value". Milan 5.4.2.15/.16 defer to 7.4.23/7.4.24 and add only the lock refusal. I swept every remaining `7.4.23.1` citation in the tree: `06_aecp_engine.md:731`, `gen_ucode.py:1619,1643,1752`, `KL_aecp_engine.sv:1032,3431`, `sim_main.cpp:7068,7231,11172`, `d3_phases.hpp:2823,2896` and `tb/pp_top/README.md:260,1684`. Each cites it for the command, its format, or the current-value response, never for membership. |
| R | Ruling: fix 06 §6.4 (`06_aecp_engine.md:462`) and the `gen_ucode.py` E_SCLKS comment; prove the generator change is comment-only by regenerating every ROM byte-identical | **Met** | Both sites now credit 7.2.32 and Table 7-141. The ROMs were regenerated from `git archive` exports of `hdl/` at base and head. `ucode.hex` (26,624 B) `3559d0a6...b053`, `ltn_rom.hex` (6,138 B) `23cc67ee...e956` and `image.bin` (1,880 B) `20356f59...b62c` are identical, and equal the PR's table. `gen_ucode.py` is the only `hdl/` file that changed. Its token stream with comment and blank-line tokens dropped is 13,424 tokens, identical at base and head (`receipts/rom_identity.txt`). |
| 2a | 10-source domain: SET(9) accepted, notifies once, reads back | **Met** | D3C1 (`tb/pp_top/d3_phases.hpp:2827-2871`): a byte-exact SUCCESS carrying 9; exactly one unsolicited response to the second controller, sequence 0; one store write, one NVM_MARK and one NOTIFY_ENQ; GET, the row with its valid flag, and `aecp_clk_src_index_o` all read 9. |
| 2b | Index 10: BAD_ARGUMENTS carrying the current index; stores and notifies nothing | **Met** | D3C2 (`:2897-2937`): a byte-exact BAD_ARGUMENTS carrying 9; no write, mark, enqueue or frame to the second controller; GET, the row and the export still read 9; nothing pending and no device operation for two debounce windows. |
| 2c | A saved AAF index survives the D3 save and restore (REQ-AEM-013, D3S1/D3R1 pair) | **Met** | D3C3 (`:2873-2895`, `:2939-2963`): one ERASE and one WRITE of record 0x0A, a byte-exact F07.8 frame, and no other record. Across a power cycle: COMPLETE, 1 applied, 26 blank; the row, GET and the export read 9. |
| 2d | A saved index at or above a smaller image's count is refused on restore | **Met** | D3C4 (`:2965-2989`): the saved 9 over a 9-source image (at the count) and over the suite's 3-source image (above it). Each is refused, COMPLETE with 0 applied and 1 refused; the row stays unset, and GET and the export read 0. |
| 2e | Each check has a failing mutant | **Met, re-run** | Every non-premise D3C check is failed by at least one of the six new controls. All six were re-run here, and each is KILLED with exactly the README's failing count (T1). |
| G | Every suite and campaign rc 0 (D3 87/87, dispatch 37/37) | **Met for every part this review re-ran; the rest is the author's evidence** | The driver tables hold exactly 87 D3 controls and 37 dispatch arms (counted by import). I re-ran the 4 new D3 controls, the 5 controls whose counts were raised, the `d3` dispatch control and its 2 new arms. The full 87- and 37-arm campaigns were not re-run (see limits). |

## Lens results (each with the artifact examined at the exact head)

```text
[R430] PASS Conformance - docs/architecture/07_memory_maps.md:135, docs/00_MILAN_COMPLIANCE_REVIEW.md:382,425, docs/architecture/06_aecp_engine.md:462, hdl/aecp/ucode/gen_ucode.py:1629-1648 - each clause claim read against Milan v1.2 5.3.3.6, 5.4.2.15, 5.4.2.16 and IEEE 1722.1-2021 7.2.9.2/Table 7-17, 7.2.32/Table 7-61 (incl. max 216), Table 7-141 row 7, 7.4.23 and 7.4.23.1; the order checked against milan-fpga MEDIA_CLOCK_FOLLOWING.md D1 = L1 at cdf49d1a; the wire behaviour checked in D3C1/D3C2 byte-exact frames (Figure 7-47 body, unsolicited bit at byte 36, sequence 0)
[R430] PASS RTL - hdl/aecp/ucode/gen_ucode.py:1649-1686, hdl/aecp/KL_aecp_ucpu.sv:222-251, hdl/aecp/KL_aecp_engine.sv:1563, hdl/aecp/KL_aecp_nvm_writer.sv:315-319,497-503, hdl/aecp/KL_aecp_dyn_state.sv:114,186,333,352, tb/pp_top/pp_top_wrap.sv:337-339,583 - no RTL or microcode change (git diff -- hdl is one comment; all three generated ROM/image outputs byte-identical); 16-bit unsigned widths on the SET compare, the restore compare, the row and the export; the wrap change only connects the top's existing output to a bench port, and no new Verilator warning names it in the four builds
[R430] PASS Robustness - tb/pp_top/d3_phases.hpp:2745-2998, tb/pp_top/sim_main.cpp:7222-7240 - the boundary (count itself), the last valid index, refusal against an already-saved row (no second save, no pending record for two windows), restore at and above a smaller image's count, the 16-bit maximum 0xFFFF (existing W10e-h); probes: export narrowed to 3 bits KILLED by 3 D3C checks, restore rule reading clock_sources_offset KILLED by 4 D3C + 2 D3R2 checks (receipts/probes); one residual width gap recorded as S1
[R430] PASS Tests - tb/pp_top/d3_phases.hpp:2745-2998 (17 D3C checks), tb/pp_top/sim_main.cpp:10747, tb/pp_top/d3_mutants.py:461-483, tb/pp_top/aecp_dispatch_mutants.py:119-134, tb/pp_top/aecp_dispatch_mutations/sclks-bound-{three,inclusive}.patch - D3 150/0 at head vs 133/0 at base (+17); the whole default build 8,624/0; the other three builds 20/0, 218/0, 56/0 (8,918 total); the six new controls and five raised controls KILLED at the README's counts; sclks-bound-three and clks_row_two_bits planted in the whole default build fail D3C's 11 and 10 checks and nothing else, as the README claims; expected frames are built independently by the bench (aecp_frame), not read from the DUT
[R430] PASS Docs - tb/pp_top/README.md:249-279,902-909,920-987,1065-1067,1106-1152, docs/architecture/09_verification.md:206-214, docs/00_MILAN_COMPLIANCE_REVIEW.md:382, PR #142 body (equal to the published review-evidence/pp141-r1/author/PR-BODY.md apart from a trailing newline) - every recorded count re-measured where re-run (T1); no stale 83-control count remains; make check, gen_matrix.py --check, check_upc_map.py, check_m9_opcodes.py and git diff --check 03c842a7..HEAD all rc 0
```

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE finding.

```text
S1 [R430] SUGGESTION Tests, Robustness - hdl/aecp/ucode/gen_ucode.py:1663-1664 (E_SCLKS CHECK_ARG fmt) and tb/pp_top - the SET range check's compare width is not graded
Requirement/evidence: The pre-check rests on the SET compare being 16 bits wide (FMT_W). A disposable probe changed only that compare to FMT_B (byte-wide). Planted in the whole default tb/pp_top build, it passes all 8,624 checks (receipts/probes/default-sclks_byte_compare.log). The existing refusals test 3 and 0xFFFF (sim_main.cpp:7222-7240), and 0xFFFF's low byte (255) is already at or above any count. D3C tests 9 and 10. The gap predates this PR and lies outside #141's frozen acceptance, which names indices 9 and 10 only. Valid indices are below 216 (Table 7-61), so the byte-wide defect only matters for an out-of-list index of 256 or more.
Impact: A regression to a byte-wide compare would accept, store, announce and persist an unlisted index such as 0x0109 over the ten-source domain, and no test would fail.
Required outcome (optional): add a refusal of an index whose low byte is below the count (e.g. SET_CLOCK_SOURCE(0x0109) on the ten-source domain, BAD_ARGUMENTS carrying the current index), with the FMT_B arm as its control.
Verification: the new arm fails with the compare at FMT_B and passes at head.

S2 [R430] SUGGESTION Docs - docs/architecture/07_memory_maps.md:135, docs/00_MILAN_COMPLIANCE_REVIEW.md:425 - the D1 index numbers are stated without D1's own condition
Requirement/evidence: milan-fpga MEDIA_CLOCK_FOLLOWING.md ("Shapes without INTERNAL or CRF") says the class order holds on every shape, but "CRF is index 1" holds only where both INTERNAL and CRF are declared. A shape without outputs may omit INTERNAL, and then CRF is 0 and AAF input k is 1 + k. L6 states the class rule ("orders the list by class"), and both rows give the numbers exactly as the frozen acceptance words them. The processor reads no order, so no processor behaviour depends on this.
Impact: none on the processor. A reader of REQ-MDL-005 alone could take the numbers as unconditional.
Required outcome (optional): qualify the numbers with "on shapes that declare INTERNAL and CRF (all shipping shapes)", or link to D1.
Verification: text check.
```

## Re-measured evidence (T1)

| Run | Result at head | Matches the record |
|---|---|---|
| `make -C tb/pp_top d3` | `D3: 150 checks, 0 failures`, rc 0 (`receipts/d3_head.log`) | yes (README, PR) |
| section D3 at base `03c842a7` (git-archive export) | `D3: 133 checks, 0 failures`, rc 0 (`receipts/d3_base.log`) | yes (+17) |
| whole default build `./obj_dir/Vpp_top_sim` | `8624 checks, 0 failures`, rc 0 (`receipts/pp_top_default_head.log`) | yes |
| fixture (VID 5A3C), line (584), timebase builds | 20/0, 218/0, 56/0, each rc 0 | yes (8,918 total) |
| `make -C tb/pp_top fixture-guards` | OK, rc 0 | - |
| `d3_mutants.py --only` the 4 new controls | golden PASS; `clks_row_two_bits` 10, `clks_restore_count_narrowed` 2, `clks_restore_index_narrowed` 4, `clks_restore_bound_inclusive` 4 (including D3R2's two), all KILLED, rc 0 (`receipts/d3m_clks/`) | yes |
| `d3_mutants.py --only` the 5 raised controls | golden PASS; `TRG_clks` 10, `RPL_clks` 5, `rule_ignored` 7, `unframed_reads_as_device_error` 42, `done_without_d3` 45, all KILLED, rc 0; the D3C checks among them are exactly the ones the README names (`receipts/d3m_raised/`) | yes |
| `aecp_dispatch_mutants.py --only sclks-bound-three,sclks-bound-inclusive` | `control d3` PASS; 11 and 6 failures, each named check present, KILLED; `3 checks: 3 PASS`, rc 0 (`receipts/dispatch_sclks/`) | yes |
| reviewer probe: `sclks_bound_three` in the whole default build | 8,624 checks, 11 failures, all D3C | yes ("nothing else") |
| reviewer probe: `clks_row_two_bits` in the whole default build | 8,624 checks, 10 failures, all D3C | yes ("nothing else") |
| reviewer probe: export narrowed to 3 bits (D3) | 3 failures, all D3C | (new, KILLED) |
| reviewer probe: restore rule reads `clock_sources_offset` (D3) | 6 failures: 4 D3C, 2 D3R2 | (new, KILLED) |
| reviewer probe: SET compare FMT_B (whole default build) | 8,624 checks, 0 failures | S1 |
| ROM regeneration base vs head | three outputs byte-identical, hashes as in the PR | yes |
| `make check`; `gen_matrix.py --check`; `check_upc_map.py`; `check_m9_opcodes.py`; `git diff --check 03c842a7 HEAD` | all rc 0 (1,017 links, 115 REQ, 17 GAP, 94 rows 0 untested, 26 parameters; 59 constants / 87 entry points; 30 opcodes) | yes |

All simulations used Verilator 5.050 (`receipts/tool_identity.txt`). The job-capping wrapper `scripts/verilator_j8.sh` held compile jobs to at most 8 at any time. Every command ran in the foreground.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | L6 `07_memory_maps.md:135`; REQ-MDL-005 `00:425`; REQ-AEM-013 `00:382`; 06 §6.4 `06_aecp_engine.md:462`; `gen_ucode.py:1629-1648`; D3C byte-exact frames; Milan v1.2 5.3.3.6, 5.4.2.15/.16; IEEE 1722.1-2021 7.2.9.2, 7.2.32, Table 7-61, Table 7-141, 7.4.23, 7.4.23.1; design D1 | R430-1 | `4a40b1798e463d09aafd74632408003229bcc673` |
| RTL | CLEAN | `gen_ucode.py:1649-1686`; `KL_aecp_ucpu.sv:222-251`; `KL_aecp_engine.sv:1563`; `KL_aecp_nvm_writer.sv:315-319,497-503`; `KL_aecp_dyn_state.sv:114,186,333,352`; `protocol_processor_top.sv:712,3862`; `pp_top_wrap.sv:337-339,583`; ROM identity receipt | R430-1 | `4a40b1798e463d09aafd74632408003229bcc673` |
| Robustness | CLEAN (S1 is a SUGGESTION) | `d3_phases.hpp:2745-2998`; `sim_main.cpp:7222-7240`; four reviewer probes | R430-1 | `4a40b1798e463d09aafd74632408003229bcc673` |
| Tests | CLEAN (S1 is a SUGGESTION) | `d3_phases.hpp:2745-2998`; `sim_main.cpp:10747`; `d3_mutants.py:461-483`; `aecp_dispatch_mutants.py:119-134`; both new patches; the re-runs in T1 | R430-1 | `4a40b1798e463d09aafd74632408003229bcc673` |
| Docs | CLEAN (S2 is a SUGGESTION) | `tb/pp_top/README.md` D3C prose and the D3 and dispatch tables; `09_verification.md:206-214`; REQ rows; PR #142 body; the published evidence `review-evidence/pp141-r1` at milan-fpga `d57953c0` | R430-1 | `4a40b1798e463d09aafd74632408003229bcc673` |

## Real limits

- **Full campaigns not re-run.** Of `d3_mutants.py` I re-ran 9 of 87 controls (the 4 new and the 5 whose counts changed) plus the golden. Of `aecp_dispatch_mutants.py` I re-ran the `d3` control and its 2 new arms out of 37 arms. The other 78 D3 controls and 35 dispatch arms grade RTL and ROMs that are byte-identical to the base's. Their unchanged counts, and the PASS of the other campaigns (`aecp-mutants`, `acmp_mutants`, `gsi_mutants`, MAAP, ADP, SRP, nvm_port figures and the rest), rest on the author's record at `39fd019` and the manager's banks.
- **Not run:** `scripts/run_suites.sh`, `scripts/lint_hdl.sh`, `make -C tb/pp_top line-guards`, and every suite other than `tb/pp_top`, under the review's limits. No `hdl/` byte other than one comment changed, and all generated ROMs are identical, so no other suite's inputs moved.
- Hosted CI at the exact head, when read: `docs-gates` and `portability` had completed with success on both runs (36969627550, 36969624563); `suites` was still in progress on both (`receipts/hosted_checks.txt`). That is a snapshot, not acceptance.
- Parent consumer gates, the donor bank and the final current-dev candidate were not run here. Physical calibration was NOT RUN, and no field result or skip is hardware proof.
- The parent's own L6 (`docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:89` at milan-fpga `cdf49d1a`) still credits the membership test to 7.4.23.1. That is on the parent design's documentation list, not this PR's scope.

## Pending manager duties

1. The donor bank and the parent consumer set at milan-fpga dev `cdf49d1a28527562888f0a903de51b6b15b1244f`, with #137's `acmp_mutants.py` disposition line, against this head.
2. The final current-dev candidate at the merge turn (source base `03c842a7`, live dev `cdf49d1a`).
3. Hosted/act acceptance: the `suites` job conclusion at the exact head.
4. The parent-side follow-ups the design lists (the parent L6 citation and the pin bump), outside this PR.
5. No residue items to carry from this round.

## Packet

- `scripts/verilator_j8.sh`: caps Verilator's `-j` at `$VJOBS`. `scripts/rom_identity.sh`: regenerates the ROMs from base and head exports. `scripts/probe.py`: the reviewer's disposable probes, each planted in a scratch copy.
- `receipts/`: raw logs and results JSON for every run in T1, the hosted-check snapshot, the tool identity, and the clone restore verification. Local paths are replaced with placeholders. `receipts/pp_top_fixture_vid.log` holds the `fixture-guards` pass, followed by a failed first VID build attempt. That failure was the reviewer's own command error, an unexpanded `$(HDL)` in a hand-typed source list, not the tree. The VID build was then re-run through make, and passed (`receipts/pp_top_vid.log`).
- The clone was restored after the probes and verified. HEAD and tree are as above, and the index tree is `b258cbd7`. `git status --ignored` is empty. All 470 tracked blobs and modes are byte-identical to the index. This repository records no submodule gitlinks (0 entries of mode 160000), so none needed checking (`receipts/clone_restore_verify.txt`).

R430-1 FINISHED
