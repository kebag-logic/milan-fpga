[A458]

Closes #76
Closes #74
Closes #53
Closes #50
Closes #82

Lane C5b of the PP program: AECP dispatch and response (assignment: #76 comment 5906184962). Branch `c5b-aecp-dispatch` from `main` `0451d83d`, head `54c1e2b`. Items in the assignment's order, one or more commits each:

| Commit | Item |
|---|---|
| `b5fd772` | 1. #76: the M9 sweep covers every opcode the engine decodes |
| `b87007b` | 2. #74: A5b sends REBOOT, START/ABORT_OPERATION, OPERATION_STATUS and SET/GET_MEMORY_OBJECT_LENGTH |
| `692ad8f` | 3. #53: the ENTITY_LOCKED arm of SET_SAMPLING_RATE, SET_CLOCK_SOURCE and SET_CONTROL (RTL fix) |
| `13a001f` | 4. #50: a response above cdl 524 through TX slot 4, and the GET_AUDIO_MAP page (RTL fix) |
| `9c3cdb7` | 5. #82: READ_DESCRIPTOR carries the current values; the oversize path; the model rules (RTL fix) |
| `596ab8e` | the AECP mutation record restated at the head |
| `344daec` | the new uCPU parameter named for its unit (`RESP_D8_CAP_BYTES_P`), for the parent naming gate |
| `54c1e2b` | 5. #82: a STREAM's `current_format` from its SET_STREAM_FORMAT row, so an unset stream stays its image (parent `milan_dp` nxndv) |

RTL changes are confined to `hdl/aecp/KL_aecp_engine.sv`, `KL_aecp_ucpu.sv`, `ucpu_pkg.sv` and `ucode/gen_ucode.py`. No port, parameter or register of `protocol_processor_top` changes. The one new parameter (`KL_aecp_ucpu.RESP_D8_CAP_BYTES_P`) is internal, set by the engine. The new top-level legs run in `tb/pp_top` section AX on a fresh processor after AD, so the main timeline does not move. `make aecp-dispatch` runs A5b, M9 and AX alone. `tb/pp_top/aecp_mutants.py` plants every arm below from an explicit patch in `tb/pp_top/aecp_mutations/`.

## 1. #76 (GAP-01): M9 covers every decoded opcode

- M9's `kOpcodes` grows from 23 to the engine's 30 `OP_*_C`: 0x0008, 0x000E, 0x0010, 0x0011, 0x002C, 0x002D and 0x004B are added. Each is sent on message types 2, 4, 6, 8, 10, 12 and 14.
  - ADD/REMOVE_AUDIO_MAPPINGS carry a real STREAM_PORT_INPUT body.
  - The three writers are also sent with a whole body. M9b3 to M9b5 read the published format row, the presentation-offset row and the CLOCK_DOMAIN name back unmoved.
- `scripts/check_m9_opcodes.py` holds `kOpcodes` to exactly the engine's `OP_*_C` set.
  - It has a `--selftest` of six fixtures, four of which must fail.
  - `scripts/run_suites.sh` runs it before any suite.
  - At the base it fails naming exactly the seven opcodes.
- **Mutation.** Each of the seven `aem_w` message-type guards removed fails its own `M9: mt=4 word XXXX` row: 9, 9, 9, 7, 7, 7 and 7 checks. Recorded in `tb/pp_top/README.md`.
- 03 section 7 no longer promises a response-size ROM (IEEE 1722.1-2021 9.3.5.3.3; the echo sizing of 06 section 8.2). No RTL change.

## 2. #74 (REQ-FWX-001): A5b sends the named opcodes

- A5b sends these outer AEM commands and grades each byte-exact NOT_IMPLEMENTED echo, the cdl off the wire and the wire length:
  - REBOOT 0x002A
  - START_OPERATION 0x0037
  - ABORT_OPERATION 0x0038
  - OPERATION_STATUS 0x0039, as a command
  - SET_MEMORY_OBJECT_LENGTH 0x0047
  - GET_MEMORY_OBJECT_LENGTH 0x0048

  Clauses: IEEE 1722.1-2021 7.4.43, 7.4.53 to 7.4.55, 7.4.72, 7.4.73 and 9.3.5.3.3.
- **Mutation.** A REBOOT SUCCESS arm in the pop decode fails the byte-exact echo. It is the only check that sees it: length and cdl are unchanged. No RTL change.

## 3. #53 (REQ-AEM-014): ENTITY_LOCKED carries the value in force

**Clause.** Milan v1.2 5.4.2.13, 5.4.2.15 and 5.4.2.17 add the refusal of a foreign SET while locked, and say nothing of its body. IEEE 1722.1-2021 7.4.21.1, 7.4.23.1 and 7.4.25.1 do: "The response always contains the current value, that is it contains the new value if the command succeeds or the old value if it fails".

**Defect and fix.** At the base the lock was checked first and refused through zero-bodied stubs. `gen_ucode.py` E_SSRATE, E_SCLKS and E_SCTRL now locate the target and read the value in force before `CHECK_LOCK`, with nothing written before it. They refuse through their own response form. The stubs and their engine µPC constants are gone. Recorded in 06 section 6.8.

**Tests** (AX LK1 to LK6). A second controller's SET is refused byte-exact at the response form's cdl (20, 20, 17):
- **LK1** on the unset rows: the image's 96000 and clock source 2, and IDENTIFY's reset 0.
- **LK3** on the rows the holder set in **LK2**: 48000, 1 and 255.

Each refusal writes, marks and notifies nothing, sends no unsolicited frame, and a GET still reads the value. **LK4**: the lock outranks a locate miss. **LK5**: the holder's miss is answered NO_SUCH_DESCRIPTOR. **LK6**: the holder is served.

**Mutation.** Each CHECK_LOCK replaced with NOP, main and miss path, fails 9/1, 9/1 and 9/1 checks. The base generator itself (`lk-prefix-zero-body`, the reproduction) fails 5.

## 4. #50 (REQ-AEM-001): above cdl 524 through TX slot 4, and the GET_AUDIO_MAP page

**Clause.** Milan v1.2 5.4.1 lets the responses of READ_DESCRIPTOR, GET_AVB_INFO, GET_AS_PATH, GET_AUDIO_MAP and ADD/REMOVE_AUDIO_MAPPINGS exceed cdl 524. Milan 5.4.2.26 bounds a GET_AUDIO_MAP subset at 176 channels. IEEE 1722.1-2021 7.4.44.2 and Table 7-141 give the page and NO_RESOURCES (8).

**Defect.** GET_AUDIO_MAP's records rode APPEND, which stops at cdl 524. A page above 62 mappings therefore dropped records while `number_of_mappings` still named them all. That page is reachable at the parent's 8x8 shape: one Stream Port Output subset of 64 stream channels.

**Fix.** The records take the oversize path. A page of up to 71 records is served whole, whatever the parent ships:
- `KL_aecp_ucpu.sv`: an APPEND with `cnd[0]` (D8) fills the response buffer, `RESP_D8_CAP_BYTES_P` = the engine's 592 B, instead of stopping at 524. Inside a GET_DYNAMIC_INFO batch it still stops at 524 (IEEE 7.4.76.1).
- `gen_ucode.py` E_GAMAP: the record APPEND takes D8. A page above `GAMAP_PAGE_MAX` = 71 answers NO_RESOURCES with `number_of_mappings` 0 and no record, so the count never names a record the response does not carry.
- `ucpu_pkg.sv` gets `GAMAP_PAGE_MAX_C` = 71, and `scripts/check_upc_map.py` holds it to the generator's `GAMAP_PAGE_MAX`.
- The engine refuses to elaborate a line below 561 B, whose buffer could not hold the page.

The alternative, a 62-record cap, would have refused a page the parent's 8x8 build can produce.

**Tests.**
- **OV1 to OV5** read four configuration-1 descriptors: AUDIO_MAPs of 576, 536 and 528 B, and a 534-byte CLOCK_DOMAIN. Frames are 618, 578, 570 and 576 B. Each read is graded byte-exact, with cdl off the wire (above 524) and the wire length.
- New wrap taps show one grant carrying the engine's oversize request, the frame leaving through slot 4 exactly when the frame exceeds 576 B, and slot 4 free afterwards.
- **PG1 to PG10**: pages of 62, 63, 64, 65, 66 and 71 mappings are served whole (slot 4 from 66). Pages of 72, 176 and 256 answer NO_RESOURCES. The 3-mapping page is then served again.
- PG2 to PG6 fail at the base. `tb/ucpu` P11b/P11c grade the D8 cap and the batch exception.

**Mutation.** `txs_oversize_o` forced to 0 fails 18 checks (acceptance 2), and so does the top's routing tied off. The request at 576 B fails 4. `pg-append-524`, the reproduction, fails 14. The page cap dropped fails 10; the cap one late fails 4. In `tb/ucpu`, the D8 flag ignored and the batch exception dropped fail 2 each.

**Docs.**
- 06 section 3 now states what the engine does, command by command.
- `P-MAP-SUBSET-CH-MAX` in F01.5 becomes 71, with Milan's 176 kept as the permission.
- Also updated: 03 section 7, 06 section 6.5, the µISA and F06.14 rows, 09 F09.4, and the integrator guide.

## 5. #82 (GAP-08): READ_DESCRIPTOR current values, the oversize path, the model rules

**Clause.** IEEE 1722.1-2021 7.2.3 (`current_sampling_rate`), 7.2.32 (`clock_source_index`) and 7.2.6 (`current_format`) are the values GET_SAMPLING_RATE (7.4.22), GET_CLOCK_SOURCE (7.4.24) and GET_STREAM_FORMAT (7.4.10) return. At the base, READ_DESCRIPTOR served the image's default after a SET.

**Fix.** At the payload walk's seam, next to the existing ENTITY overlay, the engine re-dispatches a configuration-0 READ_DESCRIPTOR by type:

| Type | Program |
|---|---|
| AUDIO_UNIT | E_RDESCAU |
| CLOCK_DOMAIN | E_RDESCCD |
| STREAM_INPUT | E_RDESCSI |
| STREAM_OUTPUT | E_RDESCSO |

Each program:
1. copies the image around the field;
2. builds the field from the dynamic-state row its SET, or the D3 restore, wrote;
3. rebuilds the rest of the field's lane from the image lane;
4. copies the tail with a new COPY_BUFFER TAIL (`cnd[0]`: rf[ra] less a lane-aligned start, since the µISA has no subtract).

An unset row, a descriptor too short for the lane, or any other configuration keeps the image bytes. Configuration 0 because that is where the GET/SET family locates.

A first cut took a STREAM's `current_format` from the integrator face GET_STREAM_FORMAT reads. The parent's `milan_dp` nxndv leg then failed, because at that shape the face and the image disagree before any SET. The overlay now takes the processor's own row, which the face serves once it is published (the settings fold). An unset stream stays its image, and no new face request is made.

**Tests.**
- **RD0**, before any SET: the rate and clock source are the image's, which the GETs read, and each stream is its image.
- **RD1**: after SET_SAMPLING_RATE, SET_CLOCK_SOURCE (0, then 1) and SET_STREAM_FORMAT on STREAM_INPUT 0 and STREAM_OUTPUT 1, each READ_DESCRIPTOR is byte-exact carrying the GET's value. STREAM_OUTPUT 0, never set, stays its image.
- **RD2**: configuration 1's CLOCK_DOMAIN keeps its image while configuration 0 holds 1.
- Every RD1 read after a SET fails at the base. Acceptance 2 is OV1, OV2 and OV5 above.

**Mutation.** Removing the re-dispatch (the reproduction) fails 5. Each program serving only the image fails 1 (AUDIO_UNIT) and 2 (CLOCK_DOMAIN). The unset test removed fails 1 (AUDIO_UNIT) and 3 (streams). STREAM_OUTPUT reading the input row fails 2. The configuration guard dropped fails 2. The TAIL count uncut fails 5.

**Model rules.** Model lint L1 to L9 and the Table 7-8 layout (formats at 138, R = 0) are explicitly the consumer's, as 07 section 3.1 already said and the parent's descriptor-ownership contract accepts:
- 00 section 6.6: REQ-MDL-001 to REQ-MDL-011 now name the consumer's model (07 section 3.1), Ver "—".
- 07 section 3.2: the image carries Table 7-8, built by the consumer.
- 07 section 3.3: what READ_DESCRIPTOR serves; nothing is appended.

**Ceiling.** 07 section 3.3 and 03 section 7 state the actual Δ8 ceiling: the response buffer, cdl 592 and a 618-byte frame at the default line.

## Validation

Verilator 5.052 with make capped at eight jobs; heavy builds ran one at a time.

Processor, at `54c1e2b`:

| Command | rc | Result |
|---|---:|---|
| `run_suites.sh` pre-gates (`check_upc_map.py`, `check_m9_opcodes.py --selftest` and plain) | 0 | 58 engine constants and 86 entry points agree; 30 opcodes swept |
| `make` in each of the 33 suites under `tb/` | 0 each | 1,017,540 checks, 0 failing (`tb/pp_top` 8,310, `tb/ucpu` 398) |
| `./scripts/lint_hdl.sh` | 0 | 41 modules |
| `make check` | 0 | lint, WaveDrom, links, both matrices, parameters, stale |
| `./syn/yosys/run.sh` | 0 | 36 tops, and the engine's Xilinx map |
| `make -C tb/pp_top fixture-guards`, `tb/desc_store/test_gen_desc_image.py` | 0 | |
| `python3 tb/pp_top/aecp_mutants.py` | 0 | 29 of 29 KILLED by their named checks; control PASS |
| `python3 tb/pp_top/d3_mutants.py --jobs 1 --only ...`, 14 chunks | 0 | 83 of 83 KILLED; goldens PASS |
| `python3 tb/pp_top/gsi_mutants.py` | 0 | 20 detected; golden and restored PASS |
| `python3 tb/pp_top/name_wr_mutant.py` | 0 | killed; golden and restored PASS |
| `tb/srp_top/mutants.py --only ...`, 8 chunks | 0 | 78 of 78 KILLED; assertion coverage 65 of 65 over the chunks |
| `tb/adp_engine/mutants.py --only ...`, 3 chunks | 0 | 30 of 30 KILLED |
| `tb/srp_admission/mutants.py`, `tb/acmp_talker/retry_mutants.py`, `tb/desc_mem_guard/mutate.py`, `make -C tb/nvm_port figures` | 0 | 12 PASS; 62 killed with 7 equivalence and 1 performance controls; detected; figures agree |

`run_suites.sh` was not run as one invocation. Warm, it needs about 640 s, beyond the 600 s bound on one command in this environment. Instead, its two pre-gates and the same `make` in each of the 33 suites ran separately, all rc 0. Three campaigns were split with their own `--only` for the same reason.

Parent consumer set (the manager's sixteen commands) in a scratch parent exported from milan-fpga dev `ec0cc0c1`:
- Every regular file is identical to the trusted index.
- `gptp-processor` and `third_party/verilog-axis` are at their recorded pins; `external` is recorded and uninitialized.
- The `protocol-processor` gitlink is staged at `54c1e2b`.
- The manager's combined adaptation (`parent-adaptation-132-c1.patch`) is applied with `git apply`.

| Command | rc |
|---|---:|
| `python3 scripts/check_cpp_idiom.py` | 0 |
| `python3 scripts/check_py_idiom.py` | 0 |
| `python3 scripts/xvlog_gate.py --check` | 0 |
| `python3 scripts/check_rtl_source_lists.py` | 0 |
| `python3 scripts/pp_srcs.py --check --selftest` | 0 |
| `python3 sw/builder/test_builder.py` | 0 (gate 11 not run: it needs a hardware build tree) |
| `make -C tb/verilator/pp_shadow -j8` | 0 |
| `python3 scripts/check_port_contracts.py` | 0 |
| `python3 scripts/measure_naming.py --check` | 0 |
| `python3 scripts/measure_test_evidence.py --check` | 0 |
| `python3 scripts/docs_check.py` | 0 |
| `make -C tb/verilator/nvm_cosim lint` | 0 |
| `make -C tb/verilator/nvm_cosim quick` | 0 |
| `make -C tb/verilator/milan_dp -j8` | 0 |
| `make -C tb/verilator/milan_dp_render -j8` | 0 |
| `python3 scripts/lint_rtl.py --check` | 0 |

Two gates failed on intermediate heads, and both are fixed at the head:
- At `596ab8e`, `measure_naming --check` flagged the new parameter's name. Fixed by `344daec`.
- At `344daec`, `milan_dp` failed the nxndv leg on the face-sourced STREAM overlay. Fixed by `54c1e2b`.

## Parent-visible, for the pin-adoption lane

- **No interface change.** No port, parameter or register of `protocol_processor_top` changes. The parent's `PP_DESC_LINE_BYTES_P` (576) is above the new 561-byte floor.
- **GET_AUDIO_MAP pages of 63 to 71 records are now served whole.** They go above cdl 524, and through the oversize slot from 66 records. Before, they carried 62 records under the full count. In the parent this is reachable only at the 8x8 Stream Port Output subset. Above 71 the page answers NO_RESOURCES, which no parent shape reaches. `P-MAP-SUBSET-CH-MAX` is documented as 71.
- **READ_DESCRIPTOR carries stored current values.** For configuration-0 AUDIO_UNIT, CLOCK_DOMAIN and STREAM_INPUT/OUTPUT, it carries what a SET or the D3 restore stored. Before either, it is the image, unchanged.
- **Observation, no processor action.** At the nxndv shape the parent's face serves a stream_format for STREAM_INPUT 1 that differs from its image's `current_format` before any SET. GET_STREAM_FORMAT and READ_DESCRIPTOR therefore disagree there until a SET.
- **The locked refusals now carry the value in force.** This covers SET_SAMPLING_RATE, SET_CLOCK_SOURCE and SET_CONTROL; before, they carried a zero body.
- **No new parent registry entry.** The new driver `protocol-processor/tb/pp_top/aecp_mutants.py` applies patch files in a scratch copy and reads only logs. `measure_test_evidence.py --check` counts 0 unexplained DUT-source readers at the head. The adaptation's existing `d3_mutants.py` entry is still needed.
- **Processor suite totals move.** `tb/pp_top` is at 8,310 checks, `tb/ucpu` at 398, and the sweep at 1,017,540.
- **Rows that can cite the new grading at adoption.** In `docs/reference/MILAN_COMPLIANCE_MATRIX.md`:
  - 5.4.2.4: `tb/pp_top` AX RD and OV
  - 5.4.2.13 to .18: AX LK
  - 5.4.2.26: AX PG
  - 9.3.5.3.3: A5b's named opcodes and M9's thirty

## What remains

- #76's requirement tickets #38, #51 and #60 are their own issues and are not addressed here.
- The L1 to L10 model rules are the consumer's (07 section 3.1). Their open follow-ups (#38, #39, #60, #89) are unchanged.
- GET_AUDIO_MAP carries at most 71 records per page, while Milan permits subsets of 176. Carrying more needs a larger response buffer.
- The GET/SET family, and so the READ_DESCRIPTOR overlay, addresses configuration 0 only. A multi-configuration image needs the locate key changed.
- Persisting and restoring maps and names stays under GAP-09 (#70).
- No hardware was used.
