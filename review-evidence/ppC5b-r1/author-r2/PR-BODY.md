[A458]

Closes #76
Closes #74
Closes #53
Closes #50
Closes #82

Lane C5b of the PP program: AECP dispatch and response (assignment: #76 comment 5906184962; round 2: #76 comment 5921225908). Branch `c5b-aecp-dispatch` from `main` `0451d83d`, merged with `main` `d5f73bac`; head `2acd402`. Round 1's items, in the assignment's order, one or more commits each:

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

Round 2's commits are listed in the Round 2 section below.

RTL changes are confined to `hdl/aecp/KL_aecp_engine.sv`, `KL_aecp_ucpu.sv`, `ucpu_pkg.sv` and `ucode/gen_ucode.py` (plus comments in `hdl/top/protocol_processor_top.sv`). No port or register of `protocol_processor_top` changes, and no parameter is added or removed; the legal range of `DESC_LINE_BYTES_P` is now stated and enforced (Round 2, item 3). The one new uCPU parameter (`KL_aecp_ucpu.RESP_D8_CAP_BYTES_P`) is internal, set by the engine. The new top-level legs run in `tb/pp_top` section AX on a fresh processor after AD, so the main timeline does not move. `make aecp-dispatch` runs A5b, M9 and AX alone. `tb/pp_top/aecp_dispatch_mutants.py` plants every arm below from an explicit patch in `tb/pp_top/aecp_dispatch_mutations/`.

## 1. #76 (GAP-01): M9 covers every decoded opcode

- M9's `kOpcodes` grows from 23 to the engine's 30 `OP_*_C`: 0x0008, 0x000E, 0x0010, 0x0011, 0x002C, 0x002D and 0x004B are added. Each is sent on message types 2, 4, 6, 8, 10, 12 and 14.
  - ADD/REMOVE_AUDIO_MAPPINGS carry a real STREAM_PORT_INPUT body.
  - The three writers are also sent with a whole body. M9b3 to M9b5 read the published format row, the presentation-offset row and the CLOCK_DOMAIN name back unmoved.
- `scripts/check_m9_opcodes.py` holds `kOpcodes` to exactly the engine's `OP_*_C` set.
  - It has a `--selftest` of eight fixtures, six of which must fail (round 2 added two).
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

Each refusal writes, marks and notifies nothing, sends no unsolicited frame, and a GET still reads the value. **LK4**: the lock outranks a locate miss. **LK5**: the holder's miss is answered NO_SUCH_DESCRIPTOR. **LK6**: the holder is served. Round 2 adds **LK3b/LK3c** (SET_CONTROL's out-of-range refusal; see Round 2, item 2).

**Mutation.** Each CHECK_LOCK replaced with NOP, main and miss path, fails 9/1, 9/1 and 12/1 checks. The base generator itself (`lk-prefix-zero-body`, the reproduction) fails 7.

## 4. #50 (REQ-AEM-001): above cdl 524 through TX slot 4, and the GET_AUDIO_MAP page

**Clause.** Milan v1.2 5.4.1 lets the responses of READ_DESCRIPTOR, GET_AVB_INFO, GET_AS_PATH, GET_AUDIO_MAP and ADD/REMOVE_AUDIO_MAPPINGS exceed cdl 524. Milan 5.4.2.26 bounds a GET_AUDIO_MAP subset at 176 channels. IEEE 1722.1-2021 7.4.44.2 and Table 7-141 give the page and NO_RESOURCES (8).

**Defect.** GET_AUDIO_MAP's records rode APPEND, which stops at cdl 524. A page above 62 mappings therefore dropped records while `number_of_mappings` still named them all. That page is reachable at the parent's 8x8 shape: one Stream Port Output subset of 64 stream channels.

**Fix.** The records take the oversize path. A page of up to 71 records is served whole, whatever the parent ships:
- `KL_aecp_ucpu.sv`: an APPEND with `cnd[0]` (D8) fills the response buffer, `RESP_D8_CAP_BYTES_P` = the engine's buffer (592 B at the default line), instead of stopping at 524. Inside a GET_DYNAMIC_INFO batch it still stops at 524 (IEEE 7.4.76.1).
- `gen_ucode.py` E_GAMAP: the record APPEND takes D8. A page above `GAMAP_PAGE_MAX` = 71 answers NO_RESOURCES with `number_of_mappings` 0 and no record, so the count never names a record the response does not carry.
- `ucpu_pkg.sv` gets `GAMAP_PAGE_MAX_C` = 71, and `scripts/check_upc_map.py` holds it to the generator's `GAMAP_PAGE_MAX`.
- The engine refuses to elaborate a line whose `16 + DESC_LINE_BYTES_P` reservation could not hold the page: below 576 B since round 2 (item 3 there).

The alternative, a 62-record cap, would have refused a page the parent's 8x8 build can produce.

**Tests.**
- **OV1 to OV5** read four configuration-1 descriptors: AUDIO_MAPs of 576 (the whole line), 536 and 528 B, and a 534-byte CLOCK_DOMAIN. Frames are 618, 578, 570 and 576 B. Each read is graded byte-exact, with cdl off the wire (above 524) and the wire length.
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
- Round 2 adds **RD3** (after the D3 restore) and **RD4** (a STREAM short of its lane); see Round 2, item 6.
- Every RD1 read after a SET fails at the base. Acceptance 2 is OV1, OV2 and OV5 above.

**Mutation** (counts at the round-2 head, with RD3). Removing the re-dispatch (the reproduction) fails 9. Each program serving only the image fails 2 (AUDIO_UNIT) and 3 (CLOCK_DOMAIN). The unset test removed fails 1 (AUDIO_UNIT) and 4 (streams). STREAM_OUTPUT reading the input row fails 4. The configuration guard dropped fails 2. The TAIL count uncut fails 9.

**Model rules.** Model lint L1 to L9 and the Table 7-8 layout (formats at 138, R = 0) are explicitly the consumer's, as 07 section 3.1 already said and the parent's descriptor-ownership contract accepts:
- 00 section 6.6: REQ-MDL-001 to REQ-MDL-011 now name the consumer's model (07 section 3.1), Ver "—".
- 07 section 3.2: the image carries Table 7-8, built by the consumer.
- 07 section 3.3: what READ_DESCRIPTOR serves; nothing is appended.

**Ceiling.** 07 section 3.3 and 03 section 7 state the actual Δ8 ceiling: the response buffer, cdl 592 and a 618-byte frame at the default line.

## Validation (round 1, at `54c1e2b`)

Verilator 5.052 with make capped at eight jobs; heavy builds ran one at a time. All 33 suites rc 0 (1,017,540 checks), `lint_hdl.sh`, `make check`, Yosys, fixture guards, the AECP campaign (29 of 29 KILLED), D3 83 of 83, and the other campaigns; the parent consumer set (the manager's sixteen commands) all rc 0 at milan-fpga dev `ec0cc0c1` with the combined adaptation applied. Two parent gates failed on intermediate heads and were fixed (`596ab8e` naming, `344daec` nxndv). Round 2's validation below supersedes this at the new head.

## Round 2 (assignment: #76 comment 5921225908)

Reviews R416-1 (three MINOR, two suggestions) and R417-1 (two MINOR, two suggestions) were both NEGATIVE; both confirmed the conformance and the RTL. Every finding is closed below and every suggestion taken (one in part, with the reason). Commits, in the assignment's order:

| Commit | Item |
|---|---|
| `a4ba9f7` | 1. Merge `main` `d5f73bac` (#135, #136), a merge commit |
| `b0b30ea` | 2. SET_CONTROL's out-of-range BAD_ARGUMENTS graded while IDENTIFY holds 255 (R416-1 F1, R417-1 F2) |
| `f7fa70b` | 3. The line-size contract: a multiple of 8 from 576 to 1008, the response buffer exactly the reservation, graded at a non-default line (R416-1 F2, R417-1 F1; RTL fix) |
| `a91fe0e` | 4. The `.gitattributes` whitespace exemption for the mutation patches (R416-1 F3) |
| `9437b16` | 5. The mutation driver renamed to `aecp_dispatch_mutants.py` / `aecp_dispatch_mutations/` / `aecp-dispatch-mutants` |
| `44fda60` | 6. R416-1 S2 and R417-1 S1: `check_m9_opcodes.py` counts every `OP_*_C` |
| `2acd402` | 6. R417-1 S2 and R416-1 S1: READ_DESCRIPTOR after the D3 restore (AX RD3) and a short STREAM (AX RD4) |

### R2.1 Merge of `main` `d5f73bac`

A merge commit, keeping both sides. Main brought the MAAP coverage lane (#135) and its own merge of #136: `hdl/maap/KL_pp_maap.sv`, a `tb/maap` patch campaign (and its `.gitattributes` entry and CI step), `tb/rx_validator` F29, 00 REQ-MAAP-007, 11, and pp_top's `maap-internal` mode (section MP, MP7). Three conflicts, all in `tb/pp_top`, resolved with both sides kept: the Makefile's `.PHONY` (both sets of targets), `sim_main.cpp`'s section flags (`maap_only` and `aecp_only` both in `one_section`, main's `run_maap_internal` call kept) and the README tail (section MP, then section AX). No patch anchor moved: every lane patch targets `hdl/aecp` or `hdl/top`, which equal the lane side, and every MAAP patch targets files that equal main's; every patch of every campaign passes `git apply --check` at the merge.

### R2.2 SET_CONTROL's out-of-range BAD_ARGUMENTS (R416-1 F1, R417-1 F2)

**Clause.** IEEE 1722.1-2021 7.4.25.1, "the old value if it fails". The behaviour was conformant at `54c1e2b` (the out-of-range arm shares the refusal tail that emits the value in force) but ungraded: W13 runs while IDENTIFY is at its reset 0, where a zero body and the value in force are the same byte.

**Tests** (AX, after LK3, IDENTIFY at 255): **LK3b**, the holder under its own lock sends SET_CONTROL(128); **LK3c**, the lock released, a second controller sends the same. Each is answered BAD_ARGUMENTS at cdl 17 carrying 255, byte-exact, with no dynamic-store write, NVM mark or notification; LK3c also sees no unsolicited frame at the registered holder (a notification goes to every registered controller but the requester), and GET and the face still read 255.

**Mutation.** `sctrl-badarg-zero-body`, the out-of-range arm branched back to the zero-bodied `E_BADARG1` (the reviewer probe's change), fails 2 (LK3b and LK3c). The new checks also move `lk-sctrl-lock-nop` to 12 and `lk-prefix-zero-body` to 7.

### R2.3 The line-size contract (R416-1 F2, R417-1 F1)

R417-1 F1's first option: the floor and the Δ8 cap agree with the documented reservation.

**Fix** (`KL_aecp_engine.sv`):
- The response buffer is exactly `16 + DESC_LINE_BYTES_P`, the reservation of the integrator guide section 5 and 07 section 3.3.2 (it was rounded up to 16). The Δ8 APPEND cap and the buffer's drop fence are that same size. Nothing changes at the default 576 (592 either way).
- The legal line is a multiple of 8 from 576 (`24 + 8·GAMAP_PAGE_MAX_C - 16`: the reservation must hold a whole 71-record page) to 1008 (the reservation may not pass the 1024 bytes the 10-bit response cursor addresses). Three elaboration guards refuse anything else, each naming `DESC_LINE_BYTES_P`: `... is not a multiple of 8`, `... is below 576: no room for a 71-record GET_AUDIO_MAP page`, `... is above 1008: 16 + line passes the 1024-byte cursor`.
- Verilator reports an elaboration `$error` as a USERERROR warning, so the refusal stops a zero-warning lint or a synthesis run; a `-Wno-fatal` simulation build carries past it (which is why R417-1's probe at 561 elaborated).

**Tests.**
- `tb/pp_top/line_guards.py` (`make line-guards`, run by `make`) lints the real top with `lint_hdl.sh`'s flags at 576, 584 and 1008, which must lint clean, and at 568, 1016 and 580, which must be refused by the engine's message naming the parameter.
- A third pp_top build, `obj_line` (`LINE_FIXTURE` = 584; `make aecp-line` alone), runs section AX at a non-default line whose 600-byte reservation is not a multiple of 16. OV1 and OV5 read a 584-byte whole-line descriptor (cdl 600, frame 626).
- **RB**, in the default and the line build: the response-memory model now counts every strobed byte outside the reservation instead of dropping it unseen. RB demands none, the top's elaborated line (a new wrap tap) equal to the bench's, and OV1's whole-line response to reach the reservation's last byte.

**Mutation.** `line-floor-rounded` (the floor on the rounded buffer, as at `54c1e2b`) lets 568 lint clean: fails `line guard 568`. `line-ceiling-dropped` leaves 1016 refused only by the uCPU's own message, which does not name the parameter: fails `line guard 1016`. `line-buffer-fixed-592` (the buffer fixed at the default's 592) truncates OV1 and OV5 at 584: fails 7. `rb-rounded-buffer-no-page-cap` (the rounded buffer and the page cap dropped together) writes 8 bytes past 600: RB fails, with 9 PG checks. RB's arm needs both sites: at a legal line the page cap and the store's line bound keep every writer inside the reservation, and the buffer drops a byte past it. Scratch probes at 584: the rounding alone fails nothing, and the page cap dropped alone stays inside the reservation (72 records, 600 bytes) while PG fails.

**Docs.** F01.5 gains `P-DESC-LINE-BYTES` (576; a multiple of 8 from 576 to 1008) and `P-MAP-SUBSET-CH-MAX` is reworded; the integrator guide's `DESC_LINE_BYTES_P` row states the range and section 5 says the processor writes nothing past the reservation; 06 section 3 and 07 sections 3.3.1 and 3.3.2 state the range and the buffer; the top's banner comments; `tb/pp_top/README.md`.

### R2.4 The whitespace exemption (R416-1 F3)

`.gitattributes` exempts `tb/pp_top/aecp_dispatch_mutations/*.patch` from the trailing-whitespace check, in the form of the srp_top, maap and adp_engine entries: unified-diff context keeps a blank source line as one space. `git diff --check 0451d83d HEAD` is rc 0 (it was rc 2, seven hits, all in these patches); every patch still applies.

### R2.5 The mutation driver renamed

The lane-C5a collision is removed: `tb/pp_top/aecp_mutants.py` is now `tb/pp_top/aecp_dispatch_mutants.py`, its patches `tb/pp_top/aecp_dispatch_mutations/` (35 arms), its make target `aecp-dispatch-mutants` and its output variable `AECP_DISPATCH_MUTANT_OUTPUT`. The README, the Makefile, the bench's comment, `.gitattributes` and this body follow; no CI step ran this driver, so none changed. `aecp_mutants.py` and `aecp-mutants` are free for lane C5a. Every arm stays KILLED.

### R2.6 Suggestions

- **R416-1 S2, R417-1 S1** (taken): `check_m9_opcodes.py` counts every `OP_*_C` localparam (comments stripped), and refuses one written in any other form (another width, radix or type) and an opcode under two names, instead of dropping it from the comparison. Two new failing fixtures; the docstrings say eight fixtures, six failing.
- **R417-1 S2** (taken): AX **RD3**. Once RD1's rows reach the NVM device, a power cycle carries it and both restore walks write the rows back. With no SET since the reset, the GETs read 48000, clock source 1 and the 2ch format, and each READ_DESCRIPTOR carries them (06 section 6.1, 07 section 3.3: "a SET or the D3 restore").
- **R416-1 S1** (taken for the STREAM guard): AX **RD4** gives configuration 0's STREAM_OUTPUTs 80 bytes (short of `current_format`'s second lane, 88), power-cycles and sets STREAM_OUTPUT 1's format; READ_DESCRIPTOR serves the 80 image bytes whole. `rd-str-short-guard-nop` is KILLED (the wrapped TAIL count leaves no response inside the bound). **Retained** for the AUDIO_UNIT and CLOCK_DOMAIN guards: no SET or restore can set a row over such a descriptor, because SET_SAMPLING_RATE walks the AUDIO_UNIT's own rate list and SET_CLOCK_SOURCE checks the CLOCK_DOMAIN's own `clock_sources_count` (@74), neither of which a descriptor short of its lane holds, and the restore rules judge the same fields; a stream format is judged by the integrator's face. The reviewer's three-guard probe fails only RD4 here.

### Validation (round 2, at `2acd402`)

Verilator 5.052 with make capped at eight jobs, Yosys 0.66; heavy builds ran one at a time. Commands longer than the 600 s bound on one command here were split with their drivers' own `--only`, or (the two drivers without it, and the two long parent commands) started in the background and awaited before anything else ran.

| Command | rc | Result |
|---|---:|---|
| `run_suites.sh` pre-gates (`check_upc_map.py`, `check_m9_opcodes.py --selftest` and plain) | 0 | 58 engine constants and 86 entry points agree; selftest 8 of 8; 30 opcodes swept |
| `make` in each of the 33 suites under `tb/`, in the tree and again on a clean `git archive` export | 0 each | 1,017,973 checks, 0 failing (`tb/pp_top` 8,562 = 8,324 + 20 + 218 over its three builds; `tb/ucpu` 398) |
| `./scripts/lint_hdl.sh` | 0 | 41 modules |
| `make check`, `gen_matrix.py --check` | 0 | lint, WaveDrom, links, both matrices, parameters, stale |
| `./syn/yosys/run.sh` | 0 | 36 tops, and the engine's Xilinx map |
| `make -C tb/pp_top fixture-guards` and `line-guards`, `tb/desc_store/test_gen_desc_image.py` | 0 | 4 cases; 6 cases; OK |
| `git diff --check 0451d83d HEAD` | 0 | |
| `make -C tb/pp_top aecp-dispatch-mutants` | 0 | 35 of 35 KILLED by their named checks; three controls PASS |
| `tb/pp_top/d3_mutants.py --jobs 1 --only ...`, 14 chunks | 0 | 83 of 83 KILLED; goldens PASS |
| `tb/pp_top/gsi_mutants.py`, `tb/pp_top/name_wr_mutant.py` | 0 | 20 detected; killed; goldens and restored PASS |
| `tb/maap/mutants.py --only ...`, 2 chunks (from `main`) | 0 | 29 of 29 arm rows KILLED |
| `tb/srp_top/mutants.py --only ...`, 8 chunks; `tb/adp_engine/mutants.py --only ...`, 3 chunks | 0 | 78 of 78; 30 of 30 KILLED |
| `tb/srp_admission/mutants.py`, `tb/acmp_talker/retry_mutants.py`, `tb/desc_mem_guard/mutate.py`, `make -C tb/nvm_port figures` | 0 | 12 PASS; 62 killed with 7 equivalence and 1 performance controls; detected; figures agree |
| `tb/ucpu` by hand in scratch | — | D8 flag ignored 2, batch exception dropped 2, TAIL uncut 1 failing checks |

Parent consumer set (the manager's sixteen commands) in a scratch parent exported from milan-fpga dev `e4b771f9`, which carries the #132 + C1 adaptation:
- Every regular file is identical to the trusted index.
- `gptp-processor` and `third_party/verilog-axis` are at their recorded pins; `external` is recorded and uninitialized.
- The `protocol-processor` gitlink is at `2acd402`, a scratch clone of this branch; no patch is applied.

| Command | rc |
|---|---:|
| `python3 scripts/check_cpp_idiom.py` | 0 |
| `python3 scripts/check_py_idiom.py` | 0 |
| `python3 scripts/xvlog_gate.py --check` | 0 (4 findings == ratchet) |
| `python3 scripts/check_rtl_source_lists.py` | 0 |
| `python3 scripts/pp_srcs.py --check --selftest` | 0 |
| `python3 sw/builder/test_builder.py` | 0 (gate 11 not run: it needs a hardware build tree) |
| `make -C tb/verilator/pp_shadow -j8` | 0 |
| `python3 scripts/check_port_contracts.py` | 0 |
| `python3 scripts/measure_naming.py --check` | 0 |
| `python3 scripts/measure_test_evidence.py --check` | 0 (0 unexplained DUT-source readers) |
| `python3 scripts/docs_check.py` | 0 |
| `make -C tb/verilator/nvm_cosim lint` | 0 |
| `make -C tb/verilator/nvm_cosim quick` | 0 |
| `make -C tb/verilator/milan_dp -j8` | 0 (every leg PASS, nxndv included) |
| `make -C tb/verilator/milan_dp_render -j8` | 0 |
| `python3 scripts/lint_rtl.py --check` | 0 (90 <= 90) |

### Parent-visible, for the pin-adoption lane

This list supersedes round 1's at the new head.

- **No port, register or parameter is added or removed.** `DESC_LINE_BYTES_P` now has a stated and enforced legal range: a multiple of 8 from 576 to 1008 (`P-DESC-LINE-BYTES`, F01.5).
  - Elaboration refuses any other line with a message naming `DESC_LINE_BYTES_P`. At the lane base any line elaborated; round 1's head refused below 561 and above 1008, the latter only through an internal parameter's message.
  - The parent's `PP_DESC_LINE_BYTES_P` = 576 is the floor and is unaffected.
  - The refusal is an elaboration `$error`, which Verilator reports as a USERERROR warning: it stops a zero-warning lint or synthesis, not a `-Wno-fatal` simulation build.
- **The response buffer is exactly the `16 + DESC_LINE_BYTES_P` bytes the integrator reserves at `RESP_BASE_P`.** It was rounded up to 16 bytes. The processor writes nothing past the reservation. Nothing changes at 576 (592 either way).
- **SET_CONTROL's out-of-range BAD_ARGUMENTS now carries the value in force (before: zero)** (IEEE 1722.1-2021 7.4.25.1). A controller that sends SET_CONTROL(IDENTIFY, 128) while identifying gets 255 back.
- **The locked refusals carry the value in force.** This covers SET_SAMPLING_RATE, SET_CLOCK_SOURCE and SET_CONTROL; before, they carried a zero body.
- **GET_AUDIO_MAP pages of 63 to 71 records are served whole.** They go above cdl 524, and through the oversize slot from 66 records. Before, they carried 62 records under the full count. In the parent this is reachable only at the 8x8 Stream Port Output subset. Above 71 the page answers NO_RESOURCES, which no parent shape reaches. `P-MAP-SUBSET-CH-MAX` is documented as 71.
- **READ_DESCRIPTOR carries stored current values.** For configuration-0 AUDIO_UNIT, CLOCK_DOMAIN and STREAM_INPUT/OUTPUT, it carries what a SET or the D3 restore stored (both now graded). Before either, and for a STREAM too short for `current_format`'s lane, it is the image, unchanged.
- **Observation, no processor action.** At the nxndv shape the parent's face serves a stream_format for STREAM_INPUT 1 that differs from its image's `current_format` before any SET. GET_STREAM_FORMAT and READ_DESCRIPTOR therefore disagree there until a SET.
- **The mutation driver is renamed, and there is no new parent registry entry.** It is now `protocol-processor/tb/pp_top/aecp_dispatch_mutants.py`, with its patches in `aecp_dispatch_mutations/` and the target `aecp-dispatch-mutants`; `aecp_mutants.py` is lane C5a's name. The new `tb/pp_top/line_guards.py` lints the real top from the sources its Makefile passes. Neither reads a DUT source: the parent's `measure_test_evidence.py --check` counts 0 unexplained DUT-source readers at this head.
- **This head carries processor `main` `d5f73bac`** (#135, #136: the MAAP coverage lane), merged; its own changes are that lane's to list.
- **Processor suite totals move.** `tb/pp_top` is at 8,562 checks over three builds (the third is the line fixture), `tb/ucpu` at 398, and the sweep at 1,017,973.
- **Rows that can cite the new grading at adoption.** In `docs/reference/MILAN_COMPLIANCE_MATRIX.md`:
  - 5.4.2.4: `tb/pp_top` AX RD (RD0 to RD4), OV and RB
  - 5.4.2.13 to .18: AX LK, with LK3b/LK3c
  - 5.4.2.26: AX PG
  - 9.3.5.3.3: A5b's named opcodes and M9's thirty

### What remains

- #76's requirement tickets #38, #51 and #60 are their own issues and are not addressed here.
- The L1 to L10 model rules are the consumer's (07 section 3.1). Their open follow-ups (#38, #39, #60, #89) are unchanged.
- GET_AUDIO_MAP carries at most 71 records per page, while Milan permits subsets of 176. The page cap is fixed at the smallest legal line's reservation; carrying more needs a larger cap and floor.
- The GET/SET family, and so the READ_DESCRIPTOR overlay, addresses configuration 0 only. A multi-configuration image needs the locate key changed.
- The AUDIO_UNIT and CLOCK_DOMAIN too-short guards stay ungraded: no SET or restore can reach them (R2.6).
- Persisting and restoring maps and names stays under GAP-09 (#70).
- No hardware was used. The parent builder's gate 11 was not run: it needs a hardware build tree.
