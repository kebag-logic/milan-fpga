[A593] Every elaboration guard is a module-scope $fatal, graded as a fatal in every front end

Closes #151

Head `ef86ea848dbfb0d869108a1987accb203a17474d`, three commits on main `2cbed0a9`.

## What changes

- **Inventory.** `hdl/` has 31 elaboration-time parameter guards in 13 files, not the 11
  the issue lists: the issue's 11, the AECP set (`KL_aecp_desc_store` 4, `KL_aecp_engine` 5,
  `KL_aecp_notify` 1, `KL_aecp_nvm_writer` 4, `KL_aecp_resp_buf` 3, `KL_aecp_ucpu` 1) and
  `KL_pp_acmp_listener`'s, which sat in an `initial` block. Nothing else in `hdl/` is
  written to stop elaboration (searched: every `$fatal`/`$error`/`$warning`/`$info` in any
  scope, `initial` blocks, `$finish`/`$stop`, constant-function assertions). The table below
  lists all 31 with file:line.
- **Every guard is `if (<condition>) begin : <name> $fatal(1, "<message>"); end` at module
  scope.** 29 `$error(` become `$fatal(1, ` on the same line, continuation lines keeping
  their column as `g_maxp_check` (already `$fatal`) does. The listener's
  `initial begin : parameter_checks if (STRM_TIMEOUT_CYC_P == 0) $fatal(...)` becomes the
  module-scope block `g_strm_tmo_check`, in the same four lines. No condition and no
  message changes, and no line of any RTL file moves.
- **The coding rules record the decision with its measurement**: a new "Elaboration
  guards" row in the HDL engineer guide's section 2, its new section 2.1 (the table below),
  and `hdl/README.md` rule 6.
- **A new suite, `tb/elab_guards`, grades the class of every guard** (`guards.py`, run by
  `make` and so by `scripts/run_suites.sh`). Per guard, a violating case must be refused
  as a `$fatal` of that guard, at its own line, in each front end's own words, and the
  nearest passing case must elaborate clean. Its inventory fails any severity task in
  `hdl/` that is not one of its 31 guards, and any listed guard that is gone. Front ends:
  Verilator lint (`scripts/lint_hdl.sh`'s flags; `%Warning-USERFATAL`), sv2v + Yosys as
  `syn/yosys/run.sh` runs them (`FATAL` or the lowered `$finish`, inside the guard's block),
  and, by `make vivado`, xelab (`[VRFC 10-8279]`) and `synth_design -rtl` (`[Synth 8-6058]`).
  `make mutants` is its proof: for each guard a `$error`, a `$warning` and an
  `initial`-block mutant, plus one mutant per other check, each killed by name.
- **The existing guard benches follow the class.** `tb/nvm_port/elab_bounds.sh` grades the
  deadline guard as a fatal too and gives it the Yosys leg; that leg now accepts Yosys's own
  `FATAL` (sv2v 0.0.12 passes `$fatal` through) besides the lowered `$finish`, and still
  refuses a `$error`'s `ERROR: <message>`. `tb/pp_top/if_guards.py` and `line_guards.py`
  require `USERFATAL`. Five mutation patches (`tb/adp_engine/mutations/if-top-range-*`,
  `tb/pp_top/aecp_dispatch_mutations/line-*`) carry the new task in their context lines;
  all 298 patches under `tb/` apply at the head.

## Why `$fatal`, measured

One probe guard, violating, through each front end (each form elaborates when its
condition is false):

| Violating guard | Verilator 5.050 lint | sv2v 0.0.12 + Yosys 0.66 | sv2v 0.0.13 + Yosys 0.66 | Vivado 2026.1 xelab | Vivado 2026.1 synth_design |
|---|---|---|---|---|---|
| module scope `$fatal(1, ...)` | refused: `%Warning-USERFATAL` | refused: `ERROR: FATAL: .` | refused: `` ERROR: System task `$finish' executed. `` | refused: `[VRFC 10-8279] $fatal` | refused: `[Synth 8-6058] Synth Error` |
| module scope `$error` | refused: `%Warning-USERERROR` | refused: `ERROR: <message>.` | **elaborates** | refused: `[XSIM 43-4462] $error` | refused: `[Synth 8-6058] Synth Error` |
| module scope `$warning` | refused: `%Warning-USERWARN` | **elaborates** | **elaborates** | **elaborates** | **elaborates** |
| module scope `$info` | **elaborates** | **elaborates** | **elaborates** | **elaborates** | **elaborates** |
| `$fatal` in an `initial` block | **elaborates** | refused: ``Can't resolve task name `$fatal'`` | refused: `` System task `$finish' executed. `` | **elaborates** | refused: `[Synth 8-6058] Synth Error` |

This corrects the issue's premise for the pinned toolchain. At sv2v 0.0.12 and Yosys 0.66,
the versions the reference platform's CI pins, a module-scope `$error` *is* refused by
Yosys, because sv2v passes the task through. The miss measured in PR #149 (R449-1 F4, S1)
is sv2v 0.0.13's: it lowers `$error` to an `initial $display`, which Yosys never runs, and
this repository's own hosted `portability` job installs the latest sv2v. Measured on the
real tree with this PR's bench: at base, all 29 `$error` guards elaborate under sv2v 0.0.13.
A per-front-end rule would therefore have kept `$error` and broken on the next sv2v;
`$fatal` is refused under both. Module scope is what Verilator lint and xelab require:
neither runs an `initial` block, so the listener's guard was never seen by either.

## Every guard, every front end (head)

"same text" means Vivado's message is Verilator's, character for character. Yosys 0.66
prints a `$fatal(1, ...)` as `FATAL: .`, taking the finish number for the text; the bench
locates that line inside the guard's block in the lowered file. Rows 28 to 30 have no
violating parameter set (`TMR_AW_C` is `$clog2(TMR_SLOTS_C)`, every base is the running
sum of the extents before it, `TMR_SLOTS_C` is the map's own end; `N_AVB_IF_P = 0` reaches
row 29 only after row 27 refuses), so their violating case moves one derived value by one
in a scratch copy of `hdl/`. Three deadlines pass at 2, not 1: at 1 they elaborate, but
Verilator `-Wall` calls `x >= 32'(N - 1)` constant (`UNSIGNED`). The xelab and synth_design columns are from this head.

<details><summary>31 guards x 5 front ends</summary>

| # | Guard (its task's file:line) | Violating case | Verilator 5.050 lint | sv2v 0.0.12 + Yosys 0.66 | sv2v 0.0.13 + Yosys 0.66 | xelab | synth_design -rtl | Nearest passing case: elaborates in |
|---:|---|---|---|---|---|---|---|---|
| 1 | `KL_acmp_nvm_shadow.g_backoff_check` (hdl/acmp/KL_acmp_nvm_shadow.sv:538) | RETRY_BACKOFF_CYC_P=0 | `%Warning-USERFATAL` :538 "KL_acmp_nvm_shadow: RETRY_BACKOFF_CYC_P must be at least 1" | `` all.v:374: ERROR: FATAL: . `` | `` all.v:376: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :538, same text | `[Synth 8-6058]` :538, same text | RETRY_BACKOFF_CYC_P=1: 5 of 5 |
| 2 | `KL_acmp_nvm_shadow.g_rs_tmo_check` (hdl/acmp/KL_acmp_nvm_shadow.sv:545) | RS_TMO_CYC_P=0 | `%Warning-USERFATAL` :545 "KL_acmp_nvm_shadow: RS_TMO_CYC_P must be at least 1" | `` all.v:377: ERROR: FATAL: . `` | `` all.v:382: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :545, same text | `[Synth 8-6058]` :545, same text | RS_TMO_CYC_P=2: 5 of 5 |
| 3 | `KL_pp_acmp_listener.g_strm_tmo_check` (hdl/acmp/KL_pp_acmp_listener.sv:347) | STRM_TIMEOUT_CYC_P=0 | `%Warning-USERFATAL` :347 "STRM_TIMEOUT_CYC_P must be greater than zero" | `` all.v:2045: ERROR: FATAL: . `` | `` all.v:2053: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :347, same text | `[Synth 8-6058]` :347, same text | STRM_TIMEOUT_CYC_P=1: 5 of 5 |
| 4 | `KL_aecp_desc_store.gen_g_line_align` (hdl/aecp/KL_aecp_desc_store.sv:263) | LINE_BYTES_P=580 | `%Warning-USERFATAL` :263 "LINE_BYTES_P=580 must be a multiple of 8 (64-bit lanes)" | `` all.v:4604: ERROR: FATAL: . `` | `` all.v:4615: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :263, same text | `[Synth 8-6058]` :263, same text | LINE_BYTES_P=576: 5 of 5 |
| 5 | `KL_aecp_desc_store.gen_g_beats` (hdl/aecp/KL_aecp_desc_store.sv:267) | IDX_ENTRIES_P=256 | `%Warning-USERFATAL` :267 "a burst exceeds the 9-bit mem_req_beats_o field" | `` all.v:4607: ERROR: FATAL: . `` | `` all.v:4621: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :267, same text | `[Synth 8-6058]` :267, same text | IDX_ENTRIES_P=255: 5 of 5 |
| 6 | `KL_aecp_desc_store.gen_g_names` (hdl/aecp/KL_aecp_desc_store.sv:270) | NAME_ENTRIES_P=1025 | `%Warning-USERFATAL` :270 "NAME_ENTRIES_P=1025 must be in 1..1024" | `` all.v:4610: ERROR: FATAL: . `` | `` all.v:4627: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :270, same text | `[Synth 8-6058]` :270, same text | NAME_ENTRIES_P=1024: 5 of 5 |
| 7 | `KL_aecp_desc_store.gen_g_base_align` (hdl/aecp/KL_aecp_desc_store.sv:273) | DESC_BASE_P=0x20000004 | `%Warning-USERFATAL` :273 "DESC_BASE_P=20000004 must be 8-byte aligned" | `` all.v:4613: ERROR: FATAL: . `` | `` all.v:4633: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :273, same text | `[Synth 8-6058]` :273, same text | DESC_BASE_P=0x20000008: 5 of 5 |
| 8 | `KL_aecp_engine.gen_g_frame_fit` (hdl/aecp/KL_aecp_engine.sv:944) | TX_OVERSIZE_BYTES_P=617 | `%Warning-USERFATAL` :944 "a maximum AECP response (618 B) exceeds the oversize slot (617 B)" | `` all.v:6183: ERROR: FATAL: . `` | `` all.v:6206: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :944, same text | `[Synth 8-6058]` :944, same text | TX_OVERSIZE_BYTES_P=618: 5 of 5 |
| 9 | `KL_aecp_engine.gen_g_resp_cap_fit` (hdl/aecp/KL_aecp_engine.sv:949) | LINE_BYTES_P=504 | `%Warning-USERFATAL` :949 "response buffer (520 B) is smaller than GET_DYNAMIC_INFO limit (524 B)" | `` all.v:6189: ERROR: FATAL: . `` | `` all.v:6215: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :949, same text | `[Synth 8-6058]` :949, same text | LINE_BYTES_P=576: 5 of 5 |
| 10 | `KL_aecp_engine.gen_g_line_step` (hdl/aecp/KL_aecp_engine.sv:964) | LINE_BYTES_P=580 | `%Warning-USERFATAL` :964 "DESC_LINE_BYTES_P=580 is not a multiple of 8 (legal: 576..1008 in steps of 8)" | `` all.v:6197: ERROR: FATAL: . `` | `` all.v:6226: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :964, same text | `[Synth 8-6058]` :964, same text | LINE_BYTES_P=576: 5 of 5 |
| 11 | `KL_aecp_engine.gen_g_gamap_page_fit` (hdl/aecp/KL_aecp_engine.sv:968) | LINE_BYTES_P=568 | `%Warning-USERFATAL` :968 "DESC_LINE_BYTES_P=568 is below 576: no room for a 71-record GET_AUDIO_MAP page" | `` all.v:6200: ERROR: FATAL: . `` | `` all.v:6232: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :968, same text | `[Synth 8-6058]` :968, same text | LINE_BYTES_P=576: 5 of 5 |
| 12 | `KL_aecp_engine.gen_g_line_ceiling` (hdl/aecp/KL_aecp_engine.sv:972) | LINE_BYTES_P=1016 | `%Warning-USERFATAL` :972 "DESC_LINE_BYTES_P=1016 is above 1008: 16 + line passes the 1024-byte cursor" | `` all.v:6203: ERROR: FATAL: . `` | `` all.v:6238: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :972, same text | `[Synth 8-6058]` :972, same text | LINE_BYTES_P=1008: 5 of 5 |
| 13 | `KL_aecp_notify.g_rows_guard` (hdl/aecp/KL_aecp_notify.sv:367) | N_IF_P=2 N_CTRL_P=1 | `%Warning-USERFATAL` :367 "KL_aecp_notify: rows {index, port} need N_IF_P=2 a power of two and N_CTRL_P=1 above 1" | `` all.v:8464: ERROR: FATAL: . `` | `` all.v:8502: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :367, same text | `[Synth 8-6058]` :367, same text | N_IF_P=2 N_CTRL_P=2: 5 of 5 |
| 14 | `KL_aecp_nvm_writer.g_shape_check` (hdl/aecp/KL_aecp_nvm_writer.sv:315) | N_NAME_P=129 | `%Warning-USERFATAL` :315 "KL_aecp_nvm_writer: a group outgrows its record-id block" | `` all.v:9882: ERROR: FATAL: . `` | `` all.v:9923: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :315, same text | `[Synth 8-6058]` :315, same text | N_NAME_P=128: 5 of 5 |
| 15 | `KL_aecp_nvm_writer.g_backoff_check` (hdl/aecp/KL_aecp_nvm_writer.sv:318) | RETRY_BACKOFF_CYC_P=0 | `%Warning-USERFATAL` :318 "KL_aecp_nvm_writer: RETRY_BACKOFF_CYC_P must be at least 1" | `` all.v:9885: ERROR: FATAL: . `` | `` all.v:9929: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :318, same text | `[Synth 8-6058]` :318, same text | RETRY_BACKOFF_CYC_P=1: 5 of 5 |
| 16 | `KL_aecp_nvm_writer.g_rs_tmo_check` (hdl/aecp/KL_aecp_nvm_writer.sv:322) | RS_TMO_CYC_P=0 | `%Warning-USERFATAL` :322 "KL_aecp_nvm_writer: RS_TMO_CYC_P must be at least 1" | `` all.v:9888: ERROR: FATAL: . `` | `` all.v:9935: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :322, same text | `[Synth 8-6058]` :322, same text | RS_TMO_CYC_P=2: 5 of 5 |
| 17 | `KL_aecp_nvm_writer.g_rs_agg_check` (hdl/aecp/KL_aecp_nvm_writer.sv:326) | RS_AGG_CYC_P=0 | `%Warning-USERFATAL` :326 "KL_aecp_nvm_writer: RS_AGG_CYC_P must be at least 1" | `` all.v:9891: ERROR: FATAL: . `` | `` all.v:9941: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :326, same text | `[Synth 8-6058]` :326, same text | RS_AGG_CYC_P=2: 5 of 5 |
| 18 | `KL_aecp_resp_buf.gen_g_base_align` (hdl/aecp/KL_aecp_resp_buf.sv:194) | RESP_BASE_P=0x20100004 | `%Warning-USERFATAL` :194 "RESP_BASE_P=20100004 must be 8-byte aligned" | `` all.v:10866: ERROR: FATAL: . `` | `` all.v:10919: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :194, same text | `[Synth 8-6058]` :194, same text | RESP_BASE_P=0x20100008: 5 of 5 |
| 19 | `KL_aecp_resp_buf.gen_g_size` (hdl/aecp/KL_aecp_resp_buf.sv:197) | RESP_BYTES_P=16 | `%Warning-USERFATAL` :197 "RESP_BYTES_P=16 leaves no payload above the header record" | `` all.v:10869: ERROR: FATAL: . `` | `` all.v:10925: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :197, same text | `[Synth 8-6058]` :197, same text | RESP_BYTES_P=24: 5 of 5 |
| 20 | `KL_aecp_resp_buf.gen_g_beats` (hdl/aecp/KL_aecp_resp_buf.sv:201) | RESP_BYTES_P=4089 | `%Warning-USERFATAL` :201 "a read burst of 512 beats exceeds the 9-bit mem_req_beats_o field" | `` all.v:10872: ERROR: FATAL: . `` | `` all.v:10931: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :201, same text | `[Synth 8-6058]` :201, same text | RESP_BYTES_P=4088: 5 of 5 |
| 21 | `KL_aecp_ucpu.gen_g_d8_cap` (hdl/aecp/KL_aecp_ucpu.sv:297) | RESP_D8_CAP_BYTES_P=1025 | `%Warning-USERFATAL` :297 "RESP_D8_CAP_BYTES_P=1025 outside 524..1024 (the 10-bit cursor)" | `` all.v:11480: ERROR: FATAL: . `` | `` all.v:11542: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :297, same text | `[Synth 8-6058]` :297, same text | RESP_D8_CAP_BYTES_P=1024: 5 of 5 |
| 22 | `KL_pp_nvm_port.g_tmo_check` (hdl/packet_engine/KL_pp_nvm_port.sv:189) | MEM_TIMEOUT_CYC_P=0 | `%Warning-USERFATAL` :189 "KL_pp_nvm_port: MEM_TIMEOUT_CYC_P=0 is outside 1 to 2147483647" | `` all.v:13805: ERROR: FATAL: . `` | `` all.v:13870: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :189, same text | `[Synth 8-6058]` :189, same text | MEM_TIMEOUT_CYC_P=1: 5 of 5 |
| 23 | `KL_pp_nvm_port.g_maxp_check` (hdl/packet_engine/KL_pp_nvm_port.sv:198) | MAX_PAYLOAD_P=65528 | `%Warning-USERFATAL` :198 "KL_pp_nvm_port: MAX_PAYLOAD_P=65528 is above 65527: 8 + it overflows dev_len_o" | `` all.v:13815: ERROR: FATAL: . `` | `` all.v:13883: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :198, same text | `[Synth 8-6058]` :198, same text | MAX_PAYLOAD_P=65527: 5 of 5 |
| 24 | `KL_pp_originator.g_inflight_check` (hdl/packet_engine/KL_pp_originator.sv:149) | INFLIGHT_P=17 | `%Warning-USERFATAL` :149 "KL_pp_originator: INFLIGHT_P must be 1..16 (owner-tag nibble)" | `` all.v:14312: ERROR: FATAL: . `` | `` all.v:14383: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :149, same text | `[Synth 8-6058]` :149, same text | INFLIGHT_P=16: 5 of 5 |
| 25 | `KL_pp_release_merge.g_slot_count_check` (hdl/packet_engine/KL_pp_release_merge.sv:38) | N_SLOTS_P=0 | `%Warning-USERFATAL` :38 "KL_pp_release_merge: N_SLOTS_P must be positive" | `` all.v:14675: ERROR: FATAL: . `` | `` all.v:14749: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :38, same text | `[Synth 8-6058]` :38, same text | N_SLOTS_P=1: 5 of 5 |
| 26 | `KL_srp_encoder.g_depth_check` (hdl/srp/KL_srp_encoder.sv:148) | DEPTH_P=13 | `%Warning-USERFATAL` :148 "DEPTH_P drain cannot fit a standard TX slot" | `` all.v:17472: ERROR: FATAL: . `` | `` all.v:17549: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :148, same text | `[Synth 8-6058]` :148, same text | DEPTH_P=12: 5 of 5 |
| 27 | `protocol_processor_top.gen_g_avb_if` (hdl/top/protocol_processor_top.sv:876) | N_AVB_IF_P=3 | `%Warning-USERFATAL` :876 "F01.5: N_AVB_IF_P=3 is outside 1 to 2 (P-N-AVB-INTERFACES)" | `` all.v:21692: ERROR: FATAL: . `` | `` all.v:21772: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :876, same text | `[Synth 8-6058]` :876, same text | N_AVB_IF_P=2: 5 of 5 |
| 28 | `protocol_processor_top.gen_g_tmr_aw` (hdl/top/protocol_processor_top.sv:880) | planted shape | `%Warning-USERFATAL` :880 "F08.4: TMR_AW_C=6 cannot index P-TIMER-SLOTS=91" | `` all.v:21695: ERROR: FATAL: . `` | `` all.v:21778: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :880, same text | `[Synth 8-6058]` :880, same text | defaults: 5 of 5 |
| 29 | `protocol_processor_top.gen_g_tmr_fit` (hdl/top/protocol_processor_top.sv:884) | planted shape | `%Warning-USERFATAL` :884 "F08.4: slot map ends at 91 but P-TIMER-SLOTS=90" | `` all.v:21698: ERROR: FATAL: . `` | `` all.v:21784: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :884, same text | `[Synth 8-6058]` :884, same text | defaults: 5 of 5 |
| 30 | `protocol_processor_top.gen_g_tmr_overlap` (hdl/top/protocol_processor_top.sv:897) | planted shape | `%Warning-USERFATAL` :897 "F08.4: timer-slot groups OVERLAP at SI=8 SO=8" | `` all.v:21701: ERROR: FATAL: . `` | `` all.v:21790: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :897, same text | `[Synth 8-6058]` :897, same text | defaults: 5 of 5 |
| 31 | `protocol_processor_top.gen_g_owner_overlap` (hdl/top/protocol_processor_top.sv:911) | N_STREAM_IN_P=16 N_STREAM_OUT_P=17 | `%Warning-USERFATAL` :911 "F08.4: owner tags OVERLAP at SI=16 SO=17 (8-bit expiry bus)" | `` all.v:21710: ERROR: FATAL: . `` | `` all.v:21802: ERROR: System task `$finish' executed. `` | `[VRFC 10-8279]` :911, same text | `[Synth 8-6058]` :911, same text | N_STREAM_IN_P=16 N_STREAM_OUT_P=16: 5 of 5 |

</details>

At base, the same bench fails 62 checks: 30 Verilator (29 `USERERROR`, and the listener's
guard never reported), 30 Yosys under sv2v 0.0.12 (refused, but as `ERROR: <message>` or
``Can't resolve task name``), and 2 inventory. Under sv2v 0.0.13 the 29 `$error` guards
elaborate. xelab and synth_design at base: 33 of 156 checks fail. xelab refuses the 29
`$error` guards as `[XSIM 43-4462] ... $error`, not as a fatal, and never runs the
listener's `initial` guard (it stops later, at a zero-width cast at
`KL_pp_acmp_listener.sv:1499`); synth_design refuses all 31, a `$error` in a `$fatal`'s
words, the listener's at its line but under the old block name.

## Validation

Verilator 5.050 throughout; sv2v 0.0.12 (the binary in the release zip the reference
platform's CI pins, sha256 `ff8c9eea...` for the zip) and Yosys 0.66 built from tag `v0.66`
(`86f2ddeb`); Vivado 2026.1.

| Record | Base `2cbed0a9` | Head | Identity |
|---|---|---|---|
| `./scripts/run_suites.sh` | rc 0, 3 gates PASS, 34 suites, 1,029,620 checks, 0 failing | rc 0, 3 gates PASS, 35 suites, 1,029,775 checks, 0 failing | all 37 base result lines (3 gates, 34 suites) identical; the added line is `PASS elab_guards (155 checks: 155 PASS, 0 FAIL)` |
| `./scripts/run_suites.sh`, sv2v 0.0.12 + Yosys 0.66 first on PATH | not run whole: its `tb/nvm_port` step fails alone (`make -C tb/nvm_port elab` rc 2, the finding below) | rc 0 | the head log is byte-identical to the row above |
| `./scripts/lint_hdl.sh` | rc 0, 41 `LINT OK` | rc 0, 41 `LINT OK` | identical |
| `make check` | rc 0 | rc 0 | identical but `links: 1187` to `1191` and `ids: 563 files` to `567`: the four links and four files this PR adds |
| `python3 scripts/gen_matrix.py --check` | rc 0, 94 rows, 0 untested | rc 0, 94 rows, 0 untested | identical |
| `./syn/yosys/run.sh`, sv2v 0.0.12 | rc 0, 42 `YOSYS OK`, parsed once, `YOSYS XILINX OK` | rc 0, the same verdicts | identical but eight Yosys memory warnings whose `all.v:<line>` moves by the one line the lowered listener guard adds; identical with those masked |
| `./syn/yosys/run.sh`, sv2v 0.0.13 | rc 0, the same verdicts | rc 0, the same verdicts | identical but the same eight warnings' line numbers (each lowered `$fatal` is longer than a `$error`) |
| `make -C tb/elab_guards` | (new) | rc 0, 155 of 155 under sv2v 0.0.12 and under 0.0.13 | |
| `make -C tb/elab_guards mutants` | (new) | rc 0, 98 of 98 killed under each sv2v; each `error`, `warning` and `initial` arm killed by both legs under 0.0.12, the `initial` arms by Verilator alone under 0.0.13 | |
| `tb/elab_guards` Vivado legs (`guards.py --frontend xsim --frontend synth`, as `make vivado` runs them) and their campaign (`mutants.py --frontend xsim --frontend synth`) | (new) | rc 0, 155 of 155 (the campaign's control, on a scratch copy of this head's `hdl/`); campaign rc 0: 14 arms, 14 killed by name (4 `$error`, 4 `$warning`, 3 `initial`, `deleted`, `tightened`, `loosened`). xelab kills every severity arm; synth_design kills the `$warning` arms (it refuses a `$error` and an `initial` `$fatal` too, in the same words) | |
| Netlists | | | 55 of 55 Yosys netlists equal: every `run.sh` top at its defaults (42) and `protocol_processor_top` at 13 more shapes (1x1, 9x9, 4x4, 1x8, 8x1, 16x16, 2x2, 5x5, and the reference platform's five configs as its datapath binds them). Each elaborated in a fresh Yosys as `run.sh` does, written with `-noattr -norename`, compared with source line numbers masked, auto-indices ranked and lines sorted |
| ROM images | `ucode.hex` `518b900c...`, `ltn_rom.hex` `23cc67ee...` | same | identical, and equal to the reference platform's recorded digests for its current pin |
| Vivado out-of-context netlist (`syn/ooc/protocol_processor_ooc.tcl`) | | | identical but the `// Date` line, at the default shape (29,096 LUTs, 25,459 registers, 19 BRAM tiles) and at 9x9; `util.rpt` identical; each run alone under the exclusive lock |

The changed benches' new checks each fail on a planted mutant: `elab_bounds.sh` on
`g_tmo_check` and `g_maxp_check` as `$error` and as `$warning`, under both sv2v (the Yosys
leg alone: `failed, but not at the guard's $fatal` under 0.0.12, `elaborated` under
0.0.13); `if-guards` on `gen_g_avb_if`, and `line-guards` on the engine's three line guards,
as `$error` and as `$warning`. 16 of 16 runs failed their bench.

Every campaign that builds a changed file, base and head, with the pinned Verilator, in
identical records (output paths, temp-directory names and seconds masked; drivers that print
arms in completion order compared as sorted lines):

| Campaign | Base | Head | Identity |
|---|---|---|---|
| `tb/pp_top/d3_mutants.py` | rc 0, D3 mutations: 110 of 110 KILLED by their named checks; goldens PASS | rc 0, D3 mutations: 110 of 110 KILLED by their named checks; goldens PASS | IDENTICAL as sorted lines (117 lines; arms print in completion order) |
| `tb/pp_top/notify_mutants.py` | rc 0, C6 notification mutations: 93 of 93 KILLED by their named checks; goldens PASS | rc 0, C6 notification mutations: 93 of 93 KILLED by their named checks; goldens PASS | IDENTICAL as sorted lines (107 lines; arms print in completion order) |
| `tb/srp_top/mutants.py` | rc 0, 137 checks: 137 PASS, 0 FAIL | rc 0, 137 checks: 137 PASS, 0 FAIL | IDENTICAL (138 lines) |
| `tb/pp_top/acmp_mutants.py` | rc 0, ACMP mutations: 51 of 51 KILLED by their named checks; goldens PASS | rc 0, ACMP mutations: 51 of 51 KILLED by their named checks; goldens PASS | IDENTICAL as sorted lines (58 lines; arms print in completion order) |
| `tb/pp_top/aecp_mutants.py` | rc 0, 67 checks: 67 PASS, 0 FAIL | rc 0, 67 checks: 67 PASS, 0 FAIL | IDENTICAL (700 lines) |
| `tb/pp_top/aecp_dispatch_mutants.py` | rc 0, 44 checks: 44 PASS, 0 FAIL | rc 0, 44 checks: 44 PASS, 0 FAIL | IDENTICAL (275 lines) |
| `tb/adp_engine/mutants.py` | rc 0, 62 checks: 62 PASS, 0 FAIL | rc 0, 62 checks: 62 PASS, 0 FAIL | IDENTICAL (422 lines) |
| `tb/pp_top/gsi_mutants.py` | rc 0, GSI mutations: 20 detected by named checks; golden and restored PASS | rc 0, GSI mutations: 20 detected by named checks; golden and restored PASS | IDENTICAL (23 lines) |
| `tb/maap/mutants.py` | rc 0, 32 checks: 32 PASS, 0 FAIL | rc 0, 32 checks: 32 PASS, 0 FAIL | IDENTICAL (101 lines) |
| `tb/pp_top/ctr_mutants.py` | rc 0, 18 checks: 18 PASS, 0 FAIL | rc 0, 18 checks: 18 PASS, 0 FAIL | IDENTICAL (113 lines) |
| `tb/srp_admission/mutants.py` | rc 0, 12 checks: 12 PASS, 0 FAIL | rc 0, 12 checks: 12 PASS, 0 FAIL | IDENTICAL (13 lines) |
| `tb/name_state/mutants.py` | rc 0, 16 arms KILLED | rc 0, 16 arms KILLED | IDENTICAL as sorted lines (17 lines; arms print in completion order) |
| `tb/pp_top/name_wr_mutant.py` | rc 0, Name-write mutation: decode killed; golden and restored PASS | rc 0, Name-write mutation: decode killed; golden and restored PASS | IDENTICAL (4 lines) |
| `tb/desc_mem_guard/mutate.py` | rc 0, hold-deleted mutant: make rc=2; completed byte assertion detected=True | rc 0, hold-deleted mutant: make rc=2; completed byte assertion detected=True | IDENTICAL (2 lines) |
| `make -C tb/nvm_port figures` | rc 0, all measured figures agree with the tree | rc 0, all measured figures agree with the tree | IDENTICAL (173 lines) |

## Reference platform, scratch (dev `e8454e27`, gitlink at this head, not committed)

| Gate | gitlink `2cbed0a9` | gitlink head |
|---|---|---|
| `scripts/lint_rtl.py --check --self-test` | rc 0, `LINT GATE: PASS (90 violation(s) <= ratchet 90; 18 waived, 0 justified lint_off)` | identical |
| `syn/yosys/run.sh --mode elaborate` (every top) | rc 0, 61 tops PASS, tap purity PASS | identical (timings masked) |
| its own lint (`lint_one`) of `milan_datapath` at each shipping config (`endstation_arty_current`, `endstation_arty_4x4`, `endstation_arty_8ch`, `endstation_ax7101_1x1_tdm8`, `endstation_ax7101_8x8`; generated shape header, `N_STREAMS`, 50 MHz) | 0 `USER*` diagnostics from any path, 0 hard errors | identical |

No shipping shape trips a guard. The raw Verilator output was read for that, because of
the finding below.

## Findings outside this PR

- **The reference platform's lint gate cannot see a processor guard.** Its
  `scripts/lint_rtl.py` drops every Verilator diagnostic under `protocol-processor/` before
  its hard-error test, and never reads Verilator's exit status. With `KL_pp_shadow` linted
  at `-GN_STREAM_IN_P=40`, Verilator exits 1 with
  `%Warning-USERFATAL: protocol-processor/hdl/top/protocol_processor_top.sv:911:5: F08.4: owner tags OVERLAP at SI=40 SO=8 (8-bit expiry bus)`
  at this head (`%Warning-USERERROR` at base), and the gate reports 0 hard errors either
  way. Verilator, run as the platform runs it, refuses the guard; the platform's wrapper
  hides it whatever the severity. That needs a change there (for example: a `USERFATAL` from
  any path, or a non-zero exit with no counted finding, is a hard error). The platform's
  Yosys elaboration does stop on it.
- At base, with the pinned sv2v 0.0.12 on PATH, `tb/nvm_port`'s `elab_bounds.sh` failed
  (`YOSYS FAIL MAX_PAYLOAD_P=65528 failed, but not at the guard's $finish`): its Yosys leg
  knew only sv2v 0.0.13's words. Fixed here. The base suite record above is therefore taken
  with sv2v 0.0.13 on PATH, as is the head's; the head passes under both.
- Outside this PR's scope and left as they are: `docs/guides/integrator.md:114` ("raises
  `$error`") and the text in `docs/diagrams/21-integration-faces.svg` ("stops the build with
  $error") now name the old task, and `docs/architecture/09_verification.md`'s table has no
  row for `tb/elab_guards`.
- The hosted suites job has no sv2v or yosys, so `tb/elab_guards` runs its Verilator leg
  there (93 checks); its Yosys leg runs wherever both are installed. The `portability` job,
  which has them unpinned, does not run the suite.

## Reproduce

```sh
./scripts/run_suites.sh
./scripts/lint_hdl.sh
make check
python3 scripts/gen_matrix.py --check
./syn/yosys/run.sh
make -C tb/elab_guards
make -C tb/elab_guards vivado
make -C tb/elab_guards mutants MUTANT_OUTPUT=<new directory>
```
