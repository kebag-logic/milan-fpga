# HANDOFF: [A458] lane C5b (AECP dispatch and response)

Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, branch `c5b-aecp-dispatch`
from `main` `0451d83d9d3f2ed5f4513c59ac5ac219ad9dd7ff`. Assignment: #76 comment 5906184962.
TAKEN: #76 comment 5906189934 (2026-09-30). REVIEW READY: #76 comment 5914935818, head `54c1e2b`.

Status: DONE. Head `54c1e2b11c90e7063fc5882b15ddea5e4335d411` (not pushed; no PR opened).
The session was cut by a host power-off at 10:30 and resumed at 11:36; the uncommitted item-4
work was kept, reviewed and reworked (item 4, "Decision on the cap").

## Environment

- Verilator 5.052 (system), run through a scratch wrapper outside every tree
  (`$VALIDATION_STORAGE/bin/verilator`) that rewrites the suites' `-j 0` to `-j 8` (`-j 0` resolves
  to the host's 128 hardware threads). Nothing else is changed; every Makefile and command is the
  tree's own. The host is shared with other lanes; heavy builds ran one at a time.
- Scratch parent: `$VALIDATION_STORAGE/parent-c5b`, a `git archive` export of milan-fpga dev
  `ec0cc0c1` (regular-file index identical to the trusted checkout's, 973 files), `gptp-processor`
  at `5dce647a` and `third_party/verilog-axis` at `48ff7a7e` fetched at their recorded pins,
  `external` recorded and uninitialized as in the trusted checkout, `protocol-processor` a local
  clone of this lane with the gitlink staged at the lane commit under test, and the manager's
  `parent-adaptation-132-c1.patch` applied with `git apply` (sha256
  `2ba6680373831206006933dddf7c97615f4870526c476a5b371b995702ddc420`, 17.7 KB; the applied diff
  equals the patch). The trusted checkout was only read.
- Receipts in `receipts/` here (all under 6 KB): `suites-54c1e2b.txt`, `aecp-mutants-54c1e2b.json`,
  `d3-mutants-54c1e2b.txt`, `parent-gates-54c1e2b.txt`. Full logs stay in `$VALIDATION_STORAGE/c5b-*`.

## Commits (in order, one-line subjects)

| Commit | Item |
|---|---|
| `b5fd772` | 1. #76: M9 sweeps every decoded opcode; `check_m9_opcodes.py`; seven guard mutants |
| `b87007b` | 2. #74: A5b sends REBOOT, START/ABORT_OPERATION, OPERATION_STATUS, SET/GET_MEMORY_OBJECT_LENGTH |
| `692ad8f` | 3. #53: ENTITY_LOCKED carries the value in force (RTL fix), section AX LK |
| `13a001f` | 4. #50: GET_AUDIO_MAP page of up to 71 records through a buffer-wide APPEND (RTL fix), AX OV/PG |
| `9c3cdb7` | 5. #82: READ_DESCRIPTOR current-value overlays (RTL fix), AX RD; 00/07 re-disposition |
| `596ab8e` | the AECP mutation record restated at the head (`ov-oversize-at-576` 4) |
| `344daec` | the uCPU parameter named for its unit (`RESP_D8_CAP_BYTES_P`; the parent naming gate) |
| `54c1e2b` | 5. #82 reworked: a STREAM's current_format from its SET row, not the face (the parent `milan_dp` nxndv leg) |

`git diff 0451d83d..54c1e2b -- hdl` touches only `hdl/aecp/KL_aecp_engine.sv`, `KL_aecp_ucpu.sv`,
`ucpu_pkg.sv` and `ucode/gen_ucode.py`. No port of `protocol_processor_top` or of any module
changes; the one new parameter (`KL_aecp_ucpu.RESP_D8_CAP_BYTES_P`) is internal, set by the engine.

## Per-item detail

### 1. #76 (GAP-01): M9 covers every decoded opcode

- `tb/pp_top` M9 `kOpcodes` grows from 23 to the engine's 30 `OP_*_C` opcodes (adds 0x0008,
  0x000E, 0x0010, 0x0011, 0x002C, 0x002D, 0x004B), each on message types 2, 4, 6, 8, 10, 12, 14.
  ADD/REMOVE get a real STREAM_PORT_INPUT body; the three new writers (SET_STREAM_FORMAT,
  SET_STREAM_INFO, SET_NAME) are also sent once with a whole command body, and M9b3/M9b4/M9b5
  read the published format row, the presentation-offset row and the CLOCK_DOMAIN name back.
- `scripts/check_m9_opcodes.py` (with `--selftest`, 6 fixtures incl. 4 that must fail) holds
  `kOpcodes` to exactly the engine's `OP_*_C` set; `scripts/run_suites.sh` runs it before any suite.
  At the base it fails listing exactly the seven opcodes of the ticket (the failing arm).
- Mutants: each of the seven `aem_w` guards removed, each KILLED by its `M9: mt=4 word XXXX` row
  (9, 9, 9, 7, 7, 7, 7 failing checks; the writers also fail M9b3-M9b5).
- Docs: 03 section 7 no longer promises a response-size ROM (echo sizing, 06 section 8.2).
- `--aecp-dispatch-only` / `make aecp-dispatch` (A5b + M9, then section AX). No RTL change.

### 2. #74 (REQ-FWX-001): A5b sends the named opcodes

- A5b rows: REBOOT 0x002A (4 B), START_OPERATION 0x0037 (12 B), ABORT_OPERATION 0x0038 (8 B),
  OPERATION_STATUS 0x0039 as a command (8 B), SET_MEMORY_OBJECT_LENGTH 0x0047 (12 B),
  GET_MEMORY_OBJECT_LENGTH 0x0048 (4 B): byte-exact NOT_IMPLEMENTED echo, cdl off the wire, wire
  length (IEEE 1722.1-2021 7.4.43, 7.4.53-7.4.55, 7.4.72, 7.4.73; 9.3.5.3.3).
- Mutant `a5b-reboot-success-arm`: KILLED, 1 failing check (the byte-exact echo). No RTL change.

### 3. #53 (REQ-AEM-014): the ENTITY_LOCKED arm of SET_SAMPLING_RATE, SET_CLOCK_SOURCE, SET_CONTROL

- Tests (pp_top section AX, a fresh processor after AD): LK1 unset rows (image 96000, clock source
  2, IDENTIFY 0), LK2 the holder sets 48000, 1, 255, LK3 the set rows, LK4 locate miss under lock
  (ENTITY_LOCKED, zero body), LK5 the holder's miss (NO_SUCH_DESCRIPTOR), LK6 the holder is served.
  Every refusal byte-exact at the response form's cdl (20, 20, 17), and no dyn-store write, NVM mark,
  notification or unsolicited frame; GET still reads the value.
- Failing arm at the base: zero-bodied stubs E_LOCKED4/E_LOCKED1 (LK1/LK3 bodies zero).
- RTL fix: `hdl/aecp/ucode/gen_ucode.py` E_SSRATE, E_SCLKS, E_SCTRL locate and read the value in
  force before `CHECK_LOCK` and refuse through their own response form; the stubs and
  `KL_aecp_engine.sv` UPC_LOCKED4_C/UPC_LOCKED1_C removed. Clause: IEEE 1722.1-2021 7.4.21.1,
  7.4.23.1, 7.4.25.1 ("the old value if it fails"); Milan v1.2 5.4.2.13/.15/.17. Doc: 06 section 6.8.
- Mutants, all KILLED: `lk-ssrate-lock-nop` 9, `lk-ssrate-miss-lock-nop` 1, `lk-sclks-lock-nop` 9,
  `lk-sclks-miss-lock-nop` 1, `lk-sctrl-lock-nop` 9, `lk-sctrl-miss-lock-nop` 1,
  `lk-prefix-zero-body` (the base generator: the issue reproduction) 5.

### 4. #50 (REQ-AEM-001): a response above cdl 524 through the oversize slot; the GET_AUDIO_MAP cap

- Decision on the cap. The uncommitted work found after the power-off capped a page at 62 records
  (the cdl-524 APPEND). That lowers `P-MAP-SUBSET-CH-MAX` below a shape the parent ships:
  milan-fpga `hdl/milan/milan_datapath.sv` answers a Stream Port Output with one subset of
  `N_STREAMS * 8` stream channels (`AMAP_OUT_NMAPS_C = 1`), 64 at the 8x8 build, so a 63- or
  64-mapping page is reachable there, and a 62 cap would answer it NO_RESOURCES: a parent-visible
  change (STOP condition). Instead the record loop takes the oversize path Milan 5.4.1 permits
  (acceptance 3's first option): a page of up to 71 records is served whole (the 592-byte
  response buffer: cdl 592, a 618-byte frame through slot 4). Every parent shape fits (input pages
  at most 11, output subsets at most 64). Above 71 the page answers NO_RESOURCES with
  `number_of_mappings` 0 and no record.
- RTL fix (clause Milan v1.2 5.4.1, 5.4.2.26; IEEE 1722.1-2021 7.4.44.2, Table 7-141 status 8):
  - `hdl/aecp/KL_aecp_ucpu.sv`: parameter `RESP_D8_CAP_BYTES_P` (default 592) and `append_cap_w`:
    an APPEND with `cnd[0]` (D8) skips past it instead of `RESP_CAP_C` (524), except inside a
    GET_DYNAMIC_INFO batch (IEEE 7.4.76.1); elaboration guard 524..1024.
  - `hdl/aecp/KL_aecp_engine.sv`: passes `RESP_BUF_C`; guard `gen_g_gamap_page_fit` refuses a buffer
    below 24 + 8 x 71 (a descriptor line below 561 B).
  - `hdl/aecp/ucpu_pkg.sv`: `GAMAP_PAGE_MAX_C = 71`; `scripts/check_upc_map.py` holds it to the
    generator's `GAMAP_PAGE_MAX` (proven to refuse a drift in scratch).
  - `gen_ucode.py` E_GAMAP: the page check (above 71: count 0 on every arm, SUCCESS becomes
    NO_RESOURCES) and the record APPEND with `cnd=D8`; unit program E_OVF8.
- Tests: pp_top AX OV1-OV5 (READ_DESCRIPTOR of configuration-1 descriptors of 576, 536, 528 B
  and a 534-byte CLOCK_DOMAIN: byte-exact, cdl, wire length, one grant with the engine's oversize
  request, the serializer's slot, slot 4 free after; new wrap taps) and PG1-PG10 (pages of 62,
  63, 64, 65, 66, 71 served whole, slot 4 from 66; 72, 176, 256 NO_RESOURCES; 3 again). Failing
  arms at the base: PG2-PG6. tb/ucpu P11b/P11c.
- Mutants (pp_top), all KILLED: `ov-oversize-never` (acceptance 2) 18, `ov-oversize-at-576` 4,
  `ov-top-oversize-dropped` 18, `pg-append-524` (reproduction) 14, `pg-cap-dropped` 10,
  `pg-cap-off-by-one` 4. tb/ucpu in scratch: D8 flag ignored 2 (P11b), batch exception dropped
  2 (P11c).
- Docs: 06 section 3 (per-command oversize rule and the real ceiling), 6.5, the µISA row,
  F06.14 0x002B; F01.5 `P-MAP-SUBSET-CH-MAX` 176 -> 71; 03 section 7; 09 F09.4; integrator guide
  (`DESC_LINE_BYTES_P` at least 561); 00 REQ-AEM-001/-020 Arch; tb READMEs.

### 5. #82 (GAP-08): READ_DESCRIPTOR current values, the oversize path, the model rules

- RTL fix (clause IEEE 1722.1-2021 7.2.3 current_sampling_rate, 7.2.32 clock_source_index,
  7.2.6 current_format, the values 7.4.22/7.4.24/7.4.10 return): at the payload-walk seam
  (`hdl/aecp/KL_aecp_engine.sv`, after the E_RDESCENT re-dispatch) a READ_DESCRIPTOR of
  configuration 0 re-dispatches AUDIO_UNIT to E_RDESCAU, CLOCK_DOMAIN to E_RDESCCD, STREAM_INPUT
  to E_RDESCSI and STREAM_OUTPUT to E_RDESCSO (shared emit E_RDESCSF). Each copies the image
  around the field, builds the field from the dynamic-state row its SET (or the D3 restore) wrote
  (`SEL_RATE`, `SEL_CLKSRC`, `SEL_FMTIN`, `SEL_FMTOUT`), rebuilds the rest of the field's lane
  from the image lane, and copies the tail with the new COPY_BUFFER TAIL
  (`KL_aecp_ucpu.sv`: `cnd[0]` count = rf[ra] - start; the µISA has no subtract). An unset row, a
  descriptor too short for the lane, or another configuration keeps the image bytes.
- Why the row, not the face, for STREAM (commit `54c1e2b`): the first cut took `current_format`
  from the Milan-info face GET_STREAM_FORMAT reads. The parent's `milan_dp` nxndv leg then failed
  `[AECP-IMG] STREAM_INPUT,1` / `[AECP-MODEL] READ_DESCRIPTOR type 0x0005 index 1` (2 bytes differ
  from the image): at that shape the parent's face serves a format for STREAM_INPUT 1 that is not
  its image's `current_format` before any SET. Changing what the parent reads before a SET is a
  parent-visible change, so the overlay takes the processor's own row, which the face serves once
  published (the settings fold); an unset stream stays its image. That also removed the new
  face request the first cut added.
- Tests: pp_top AX RD0 (before any SET: rate and clock source are the image's, which the GETs
  read; each stream is its image exactly), RD1 (after SET_SAMPLING_RATE(48000),
  SET_CLOCK_SOURCE(0) then (1), SET_STREAM_FORMAT(2ch) on STREAM_INPUT 0 and STREAM_OUTPUT 1,
  READ_DESCRIPTOR byte-exact carrying the GET's value; STREAM_OUTPUT 0 never set is its image),
  RD2 (configuration 1's CLOCK_DOMAIN keeps its image while configuration 0 holds 1). Failing
  arms at the base: every RD1 read after a SET. Acceptance 2 is OV1/OV2/OV5 (item 4). tb/ucpu P9b.
- Mutants (pp_top), all KILLED: `rd-base-no-overlay` (reproduction) 5, `rd-au-image-only` 1,
  `rd-au-unset-overlays` 1, `rd-cd-image-only` 2, `rd-str-unset-overlays` 3,
  `rd-so-reads-input-row` 2, `rd-cfg-any` 2, `rd-tail-uncut` 5 (also 1 in tb/ucpu, P9b).
- Model lint L1-L9 and Table 7-8: re-dispositioned to the consumer, matching what 07 section 3.1
  already stated and the parent's `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` accepts (L1-L10,
  Table 7-8 emission at 138, R = 0): 00 section 6.6 REQ-MDL-001..011 Arch "consumer's model (07
  section 3.1 ownership)", Doc 07 section 3.1, Ver "—"; 07 section 3.2 (the image carries Table
  7-8, built by the consumer), 3.3 (what READ_DESCRIPTOR serves; no tail assembly); GAP-08 row.
- Ceiling (acceptance 4): 07 section 3.3 and 03 section 7 state cdl 592 / 618-byte frame at the
  default line, READ_DESCRIPTOR from 509 B, GET_AUDIO_MAP from 63 records, the others below 524.

### 6. The parent-visible list

1. No port, parameter or register of `protocol_processor_top` changes. The parent's
   `PP_DESC_LINE_BYTES_P` is 576; the new elaboration guard needs at least 561.
2. GET_AUDIO_MAP: a page of 63 to 71 records is now served whole (cdl up to 592, a frame above
   576 through the oversize slot from 66 records); before, the response carried 62 records while
   `number_of_mappings` named them all. Reachable in the parent only at the 8x8 shape's Stream
   Port Output subset (64 stream channels) with 63 or more mapped to one port. A page above 71
   answers NO_RESOURCES; no parent shape reaches it. `P-MAP-SUBSET-CH-MAX` is documented as 71.
3. READ_DESCRIPTOR of configuration-0 AUDIO_UNIT, CLOCK_DOMAIN and STREAM_INPUT/OUTPUT carries the
   value a SET or the D3 restore stored (as ENTITY already did for current_configuration); before
   any SET or restore it is the image, unchanged. The parent's 5.4.2.4 row can cite pp_top AX RD.
4. Observation for the parent (no processor action): at the nxndv shape the parent's face serves a
   stream_format for STREAM_INPUT 1 that differs from its image's `current_format` before any SET,
   so GET_STREAM_FORMAT and READ_DESCRIPTOR disagree there until a SET.
5. ENTITY_LOCKED refusals of SET_SAMPLING_RATE/SET_CLOCK_SOURCE/SET_CONTROL now carry the value in
   force (was a zero body). The parent's 5.4.2.13-.18 rows can cite pp_top AX LK.
6. New mutation driver `tb/pp_top/aecp_mutants.py` (patches in `tb/pp_top/aecp_mutations/`): the
   parent's `measure_test_evidence.py --check` counts 0 unexplained DUT-source readers at the head
   with the combined adaptation, so no `DUT_READER_DISPOSITIONS` entry is needed (it applies patch
   files with `git apply` in a scratch copy and reads only logs). The adaptation's existing
   `d3_mutants.py` entry is still required.
7. Processor suite totals at the head: pp_top 8,310, ucpu 398, all 33 suites 1,017,540 checks.
8. Parent matrix rows that can cite the new grading at adoption (`docs/reference/
   MILAN_COMPLIANCE_MATRIX.md`): 5.4.2.4 (AX RD, OV), 5.4.2.13-.18 (AX LK), 5.4.2.26 (AX PG),
   9.3.5.3.3 (A5b's six named opcodes, M9's thirty).

## Suite table (processor, head `54c1e2b`)

| Command | rc | Result |
|---|---:|---|
| `scripts/run_suites.sh` pre-gates: `check_upc_map.py`, `check_m9_opcodes.py --selftest` and plain | 0 | 58 engine constants / 86 entry points agree; 6 of 6 selftest; 30 opcodes swept |
| `make` in each of the 33 `tb/*/` suites (what `run_suites.sh` runs) | 0 each | 1,017,540 checks, 0 failing (pp_top 8,310 = 8,290 + 20; srp_admission 991,231; ucpu 398) |
| `./scripts/lint_hdl.sh` | 0 | 41 modules |
| `make check` | 0 | 41 mermaid + 18 wavedrom, links 988, matrix 115 REQ / 17 GAP, modmatrix 94 rows 0 untested, parameters 26 |
| `./syn/yosys/run.sh` | 0 | 36 tops YOSYS OK + KL_aecp_engine Xilinx map OK |
| `make -C tb/pp_top fixture-guards` | 0 | 4 cases PASS (and its unittest) |
| `tb/desc_store/test_gen_desc_image.py` | 0 | OK |

`run_suites.sh` as one invocation was not run: warm, it needs about 640 s (pp_top 280 s,
srp_top 160 s, the rest) and a foreground command here is bounded at 600 s. Its two pre-gates and
the 33 suites were run as separate commands with the same `make`, all rc 0 (per-suite list in
`receipts/suites-54c1e2b.txt`).

## Mutant table (head `54c1e2b`)

| Driver | rc | Result |
|---|---:|---|
| `tb/pp_top/aecp_mutants.py` (this lane) | 0 | 29 of 29 arms KILLED by their named check; control PASS (`receipts/aecp-mutants-54c1e2b.json`) |
| `tb/pp_top/d3_mutants.py --jobs 1 --only <chunk>` x14 | 0 each | 83 of 83 KILLED; goldens PASS in every chunk (`receipts/d3-mutants-54c1e2b.txt`) |
| `tb/pp_top/gsi_mutants.py` | 0 | 20 detected; golden and restored PASS |
| `tb/pp_top/name_wr_mutant.py` | 0 | decode killed; golden and restored PASS |
| `make -C tb/srp_top mutants` as `mutants.py --only <chunk>` x8 | 0 each | 78 of 78 arm records KILLED; assertion coverage 65/65 recomputed over the chunks |
| `make -C tb/adp_engine mutants` as `mutants.py --only <chunk>` x3 | 0 each | 30 of 30 KILLED; controls PASS |
| `tb/srp_admission/mutants.py` | 0 | 12 checks PASS |
| `tb/acmp_talker/retry_mutants.py` | 0 | 62 killed, 7 equivalence controls, 1 performance control |
| `tb/desc_mem_guard/mutate.py` | 0 | hold-deleted mutant detected |
| `make -C tb/nvm_port figures` | 0 | figures agree |
| tb/ucpu by hand in scratch | — | D8 flag ignored 2, batch exception dropped 2, TAIL uncut 1 failing checks |

Chunking: the three campaigns were split with their own `--only` so each command stays in the
600 s bound; d3 with `--jobs 1` so only one heavy build runs at a time. One unchunked srp_top run
was stopped by PID and rerun in chunks. `name_wr_mutant.py` once ran without the -j8 wrapper on
PATH (rc 0); it was rerun with it (rc 0).

## Parent consumer gate table (scratch parent, gitlink `54c1e2b`, adaptation applied)

| Command | rc | Result |
|---|---:|---|
| `python3 scripts/check_cpp_idiom.py` | 0 | |
| `python3 scripts/check_py_idiom.py` | 0 | |
| `python3 scripts/xvlog_gate.py --check` | 0 | 4 findings == ratchet |
| `python3 scripts/check_rtl_source_lists.py` | 0 | |
| `python3 scripts/pp_srcs.py --check --selftest` | 0 | |
| `python3 sw/builder/test_builder.py` | 0 | all gates pass except gate 11, not run (hardware build tree absent) |
| `make -C tb/verilator/pp_shadow -j8` | 0 | 295 checks |
| `python3 scripts/check_port_contracts.py` | 0 | |
| `python3 scripts/measure_naming.py --check` | 0 | 96 recorded |
| `python3 scripts/measure_test_evidence.py --check` | 0 | 0 unexplained DUT-source readers |
| `python3 scripts/docs_check.py` | 0 | 0 findings |
| `make -C tb/verilator/nvm_cosim lint` | 0 | |
| `make -C tb/verilator/nvm_cosim quick` | 0 | 315 checks |
| `make -C tb/verilator/milan_dp -j8` | 0 | every leg PASS |
| `make -C tb/verilator/milan_dp_render -j8` | 0 | PASS |
| `python3 scripts/lint_rtl.py --check` | 0 | 90 <= 90 |

Intermediate heads: at `596ab8e` `measure_naming --check` failed on `RESP_D8_CAP_P` (fixed by
`344daec`); at `344daec` `milan_dp` failed the nxndv leg (fixed by `54c1e2b`). Four commands ran
past 600 s (`test_builder.py` twice, 951 s and 966 s; `milan_dp` 1502 s; `gsi_mutants.py`; the
srp_admission driver 704 s). The session's background continuation carried them to completion
while I waited on each process in the foreground, and the session did not end meanwhile.

## What remains

- #76's requirement tickets #38, #51 and #60 are their own issues; not addressed here.
- The model rules L1-L10 are the consumer's (07 section 3.1); the open follow-ups there (#38,
  #39, #60, #89) are unchanged.
- GET_AUDIO_MAP carries at most 71 records per page (Milan allows subsets of 176); more needs a
  larger response buffer.
- The GET/SET family, and so the READ_DESCRIPTOR overlay, address configuration 0 (the literal
  locate key); a multi-configuration image needs that key changed.
- Persisting and restoring maps and names stays under GAP-09 (#70).
- No hardware was used.
