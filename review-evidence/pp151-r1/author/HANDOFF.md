# [A593] HANDOFF: processor #151, parameter guards that stop every front end

Status: DONE, REVIEW READY at head `ef86ea848dbfb0d869108a1987accb203a17474d` (issue #151
comment 6105034104). Resumed 2026-10-10 21:34 after a usage-limit stop at 21:06: no
tree file was left planted (`git status` clean); the six head campaigns the stop cut or never
started were re-run; every Vivado run was queued on the shared exclusive lock. The lock was
heavily contended (six other lanes' routes and syntheses): the first queued Vivado campaign
waited 8,740 s and was then ended by an outside SIGTERM (rc 143) before it ever held the lock;
it was re-queued at 00:09 in priority order and ran from 03:40 (the Vivado campaign, the OOC
netlists, the base tree's Vivado legs), each run alone under the lock, done 05:27.

### Acceptance (issue #151 and the assignment)

| Item | Met | Where |
|---|---|---|
| Inventory of every elaboration guard in `hdl/`, file:line | yes, 31 in 13 files (the issue listed 11) | section 2 |
| Every guard stops Verilator lint (as `lint_hdl.sh` and the parent run it), sv2v + Yosys at the CI pins, xvlog/Vivado | yes: each violating case refused as a `$fatal` at the guard's line by Verilator 5.050, sv2v 0.0.12 + Yosys 0.66 (and 0.0.13), xelab and `synth_design -rtl`; Verilator with the parent's flags exits 1 `USERFATAL` (the parent's wrapper hides it: a parent-side finding, section 9) | sections 4, 9 |
| Nearest passing set elaborates in each | yes, 31 of 31 in all five | section 4 |
| Design decision recorded in the coding rules with its measurement | yes: `$fatal` everywhere, module scope; HDL engineer guide section 2 row and section 2.1, `hdl/README.md` rule 6 | section 3 |
| No guard changes its condition | yes: 29 `$error(` to `$fatal(1, ` on the same line, the listener's `initial` to module scope, conditions and messages byte-identical, no RTL line moves | sections 3, 0 |
| Shipping shapes' netlists and ROM digests identical at base and head | yes: 55 Yosys netlists (incl. the five configs' shapes), the Vivado OOC netlist at default and 9x9 (byte-identical but the Date line), both ROM images | section 6 |
| A bench grades severity; a `$error` and a `$warning` mutant of every guard killed by name | yes: `tb/elab_guards`; 98 of 98 under each sv2v (31 `error`, 31 `warning`, 31 `initial`, 5 bench arms), 14 of 14 through the Vivado legs | section 5 |
| Suites, `lint_hdl.sh`, `make check`, `gen_matrix.py --check`, `syn/yosys/run.sh` pass at base and head, records identical | rc 0 at both; identical but for the lane's own additions (`run_suites.sh`: one added suite line and its total; `make check`: four links and four files counted) and the moved `all.v` line numbers in eight Yosys warnings, each named and masked | section 6 |
| Every campaign that builds a changed file, base and head | 15 of 15 rc 0 and identical | section 8 |
| Scratch parent at dev `e8454e27`, gitlink at head: Yosys elaboration and Verilator lint pass; no shipping shape trips a guard | yes | section 9 |

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Branch: `pp151-guards`, from main `2cbed0a987c1e68402658d69459ab7e5aa571adc`
- Assignment: issue #151, comment 6098621173 (lane manager [A10]; reviewers [R604], [R605])
- TAKEN posted: issue #151 comment 6098634009
- REVIEW READY posted: issue #151 comment 6105034104, 2026-10-11
- Head: `ef86ea848dbfb0d869108a1987accb203a17474d` (every record below is at this head)

## 0. Commits (branch `pp151-guards`, not pushed)

| Commit | Subject | Files |
|---|---|---|
| `93857992bf785bac35b9a382370b45414c0dbc48` | Make every elaboration guard a module-scope $fatal | the 13 guarded RTL files; `tb/nvm_port/elab_bounds.sh`, its README; `tb/pp_top/if_guards.py`, `line_guards.py`, its README; the five patches whose context quotes a guard |
| `eb7e596e0eba99a0533a7420399862b7e87c47be` | Grade every elaboration guard as a $fatal in each front end and record the rule | `tb/elab_guards/{guards.py,Makefile,README.md}`; `docs/guides/hdl-engineer.md`; `hdl/README.md` |
| `ef86ea848dbfb0d869108a1987accb203a17474d` | Kill each guard's $error, $warning and initial-block forms by name | `tb/elab_guards/{mutants.py,Makefile,README.md}` |

29 files, +942 / -63. Each step was checked before its commit (lint, the changed benches,
`make check`, the matrix; the suite; the campaign).

## 1. Toolchain identities

| Front end | Identity | How it was established |
|---|---|---|
| Verilator | 5.050, `rev v5.050` | the pinned wrapper (the host default is 5.052) |
| sv2v | v0.0.12, binary sha256 `b29952bc8f400ca90207507db0ff6763263e03d3eec711da80338430ed636b9b` | equals the binary inside the release zip the parent CI pins (zip sha256 `ff8c9eea5bc029b372fb4953427625cddb7cf7e58c1240623ac9f260818d5a00`, `elaborate.yml`, `rtl.yml`, `rtl-fast.yml`, `docs.yml` at parent dev `e8454e27`) |
| Yosys | 0.66, `git sha1 86f2ddebc`, built from tag `v0.66` (`86f2ddebce7e98ce7cacc27e8a5c14cb53b51b51`), bundled ABC `5d51a5e420f5de493d07bf61109a977248c86ffb`; yosys sha256 `26fd39a924f096b75c1f54c12ef1493780eaccd7e9579d860d90ac55c231a981` | the parent CI's `YOSYS_VERSION: v0.66`, built from the upstream tag |
| Vivado / xsim | 2026.1 (`Vivado Simulator v2026.1`) | the only installed version |

The brief said the pinned sv2v and Yosys were under the shared tools directory. They were
not there; the identical sv2v binary and a clean tag build of Yosys 0.66 were found
elsewhere on the host and copied into the lane's scratch directory. The host's default
`sv2v` on PATH is v0.0.13 (sha256 `b80a8ac6...`) and its packaged Yosys is
`0.66 (86f2ddebc-dirty)`; neither is the pinned pair, and section 3 shows why that matters.

The processor's own hosted `portability` job does not pin either tool: it installs the
`latest` sv2v release and the distribution's Yosys.

## 2. Guard inventory (file:line at base `2cbed0a9`)

Every elaboration-time severity task in `hdl/` (`$fatal`, `$error`, `$warning`, `$info`, in
any scope), and every other construct written to stop elaboration. The search also
covered `initial` blocks, `$finish`/`$stop`, constant-function assertions and deliberate
missing-module instances: there are no others. 31 guards in 13 files.

| # | File:line (the `if`) | Block | Severity at base | Scope at base | Condition |
|---:|---|---|---|---|---|
| 1 | `hdl/acmp/KL_acmp_nvm_shadow.sv:537` | `g_backoff_check` | `$error` | module | `RETRY_BACKOFF_CYC_P < 1` |
| 2 | `hdl/acmp/KL_acmp_nvm_shadow.sv:544` | `g_rs_tmo_check` | `$error` | module | `RS_TMO_CYC_P < 1` |
| 3 | `hdl/acmp/KL_pp_acmp_listener.sv:345-347` | `parameter_checks` | `$fatal(1, ...)` | **`initial` block** | `STRM_TIMEOUT_CYC_P == 0` |
| 4 | `hdl/aecp/KL_aecp_desc_store.sv:262` | `gen_g_line_align` | `$error` | module | `(LINE_BYTES_P % 8) != 0` |
| 5 | `hdl/aecp/KL_aecp_desc_store.sv:266` | `gen_g_beats` | `$error` | module | `(LINE_LANES_C > 511) \|\| ((IDX_ENTRIES_P * 2) > 511)` |
| 6 | `hdl/aecp/KL_aecp_desc_store.sv:269` | `gen_g_names` | `$error` | module | `(NAME_ENTRIES_P == 0) \|\| (NAME_ENTRIES_P > 1024)` |
| 7 | `hdl/aecp/KL_aecp_desc_store.sv:272` | `gen_g_base_align` | `$error` | module | `DESC_BASE_P[2:0] != 3'd0` |
| 8 | `hdl/aecp/KL_aecp_engine.sv:943` | `gen_g_frame_fit` | `$error` | module | `FRAME_MAX_C > TX_OVERSIZE_BYTES_P` |
| 9 | `hdl/aecp/KL_aecp_engine.sv:948` | `gen_g_resp_cap_fit` | `$error` | module | `RESP_BUF_C < ucpu_pkg::RESP_CAP_C` |
| 10 | `hdl/aecp/KL_aecp_engine.sv:963` | `gen_g_line_step` | `$error` | module | `(LINE_BYTES_P % 8) != 0` |
| 11 | `hdl/aecp/KL_aecp_engine.sv:967` | `gen_g_gamap_page_fit` | `$error` | module | `RESP_BUF_C < 24 + 8 * ucpu_pkg::GAMAP_PAGE_MAX_C` |
| 12 | `hdl/aecp/KL_aecp_engine.sv:971` | `gen_g_line_ceiling` | `$error` | module | `RESP_BUF_C > RESP_CURSOR_BYTES_C` |
| 13 | `hdl/aecp/KL_aecp_notify.sv:366` | `g_rows_guard` | `$error` | module | `(N_IF_P > 1) && (((N_IF_P & (N_IF_P - 1)) != 0) \|\| (N_CTRL_P < 2))` |
| 14 | `hdl/aecp/KL_aecp_nvm_writer.sv:310-314` | `g_shape_check` | `$error` | module | any of the five group counts outside its id block |
| 15 | `hdl/aecp/KL_aecp_nvm_writer.sv:317` | `g_backoff_check` | `$error` | module | `RETRY_BACKOFF_CYC_P < 1` |
| 16 | `hdl/aecp/KL_aecp_nvm_writer.sv:321` | `g_rs_tmo_check` | `$error` | module | `RS_TMO_CYC_P < 1` |
| 17 | `hdl/aecp/KL_aecp_nvm_writer.sv:325` | `g_rs_agg_check` | `$error` | module | `RS_AGG_CYC_P < 1` |
| 18 | `hdl/aecp/KL_aecp_resp_buf.sv:193` | `gen_g_base_align` | `$error` | module | `RESP_BASE_P[2:0] != 3'd0` |
| 19 | `hdl/aecp/KL_aecp_resp_buf.sv:196` | `gen_g_size` | `$error` | module | `RESP_BYTES_P <= 16` |
| 20 | `hdl/aecp/KL_aecp_resp_buf.sv:200` | `gen_g_beats` | `$error` | module | `LANES_C > 511` |
| 21 | `hdl/aecp/KL_aecp_ucpu.sv:295-296` | `gen_g_d8_cap` | `$error` | module | `(RESP_D8_CAP_BYTES_P < RESP_CAP_C) \|\| (RESP_D8_CAP_BYTES_P > 1024)` |
| 22 | `hdl/packet_engine/KL_pp_nvm_port.sv:188` | `g_tmo_check` | `$error` | module | `(MEM_TIMEOUT_CYC_P < 1) \|\| (MEM_TIMEOUT_CYC_P > 32'h7FFF_FFFF)` |
| 23 | `hdl/packet_engine/KL_pp_nvm_port.sv:197` | `g_maxp_check` | `$fatal(1, ...)` | module | `MAX_PAYLOAD_P > MAXP_BOUND_C` |
| 24 | `hdl/packet_engine/KL_pp_originator.sv:148` | `g_inflight_check` | `$error` | module | `INFLIGHT_P < 32'd1 \|\| INFLIGHT_P > IFL_N_C` |
| 25 | `hdl/packet_engine/KL_pp_release_merge.sv:37` | `g_slot_count_check` | `$error` | module | `N_SLOTS_P < 1` |
| 26 | `hdl/srp/KL_srp_encoder.sv:147` | `g_depth_check` | `$error` | module | `WORST_BYTES_C > TX_STD_BYTES_P` |
| 27 | `hdl/top/protocol_processor_top.sv:875` | `gen_g_avb_if` | `$error` | module | `(N_AVB_IF_P < 32'd1) \|\| (N_AVB_IF_P > 32'd2)` |
| 28 | `hdl/top/protocol_processor_top.sv:879` | `gen_g_tmr_aw` | `$error` | module | `TMR_SLOTS_C > (32'd1 << TMR_AW_C)` |
| 29 | `hdl/top/protocol_processor_top.sv:883` | `gen_g_tmr_fit` | `$error` | module | `TMR_MAP_C.srp_ls + N_STREAM_IN_P > TMR_SLOTS_C` |
| 30 | `hdl/top/protocol_processor_top.sv:887-896` | `gen_g_tmr_overlap` | `$error` | module | the slot groups' running sums out of order |
| 31 | `hdl/top/protocol_processor_top.sv:900-910` | `gen_g_owner_overlap` | `$error` | module | the owner-tag ranges out of order, or past `0xC0` / 256 |

Issue #151's body lists 11 of them (rows 1, 2, 22, 24, 25, 26, 27-31). The other 20 are
the AECP set (rows 4-21) and the listener (row 3).

## 3. Design decision and the measurement behind it

**Decision: every guard is a module-scope `$fatal(1, <its unchanged message>)`.** 30 of the
31 guards change form: 29 module-scope `$error(` become `$fatal(1, ` on the same line
(continuation lines keep their column, as `g_maxp_check` does), and the listener's
`initial begin : parameter_checks if (STRM_TIMEOUT_CYC_P == 0) $fatal(...)` becomes the
module-scope `if (STRM_TIMEOUT_CYC_P == 0) begin : g_strm_tmo_check $fatal(...) end`, in the
same four lines (one is a `//!` comment saying why). No condition and no message text
changes, and no line in any RTL file moves (so no `file:line` citation into `hdl/` goes
stale). `g_maxp_check` is already in that form.

Why `$fatal` rather than a measured per-front-end form: at the CI-pinned versions a
module-scope `$error` *is* refused by every front end (table below, and the per-guard base
run in section 4), so a per-front-end rule would have said "keep `$error`". But that
refusal in Yosys exists only because sv2v 0.0.12 passes the task through: sv2v 0.0.13, the
`latest` the processor's own hosted `portability` job installs, lowers `$error` to an
`initial $display`, which Yosys never runs, and all 29 base `$error` guards then elaborate
(measured, section 4). `$fatal` is lowered to `$display` + `$finish(1)`, which Yosys runs,
so it is refused under both. Module scope is forced by Verilator lint and xelab, which never
evaluate an `initial` block (the listener's base guard is missed by both).

This corrects issue #151's premise as it applies to the pinned toolchain: R449-1's "sv2v +
Yosys elaborate through a module-scope `$error`" holds for sv2v 0.0.13, not for the pinned
sv2v 0.0.12.

Recorded in the coding rules: `docs/guides/hdl-engineer.md` section 2 (a new "Elaboration
guards" row) and new section 2.1 with the table below; `hdl/README.md` rule 6.

Probe: one module, one guard `if (P_P > 4) begin : g_p_check <task>(...); end`, each task
at module scope and in an `initial` block, violating (`P_P = 5`) and passing (`P_P = 1`).
Every passing case is rc 0 in every front end.

| Form at `P_P = 5` | Verilator 5.050 lint (lint_hdl.sh flags; parent flags) | sv2v 0.0.12 + Yosys 0.66 | sv2v 0.0.13 + Yosys 0.66 | Vivado `xelab` | Vivado `synth_design -rtl` |
|---|---|---|---|---|---|
| module `$fatal(1, ...)` | rc 1 `%Warning-USERFATAL` | rc 1 `ERROR: FATAL: .` | rc 1 `ERROR: System task $finish executed.` | rc 1 `ERROR: [VRFC 10-8279] $fatal : ...` | rc 1 `ERROR: [Synth 8-6058] Synth Error: ...` |
| module `$error` | rc 1 `%Warning-USERERROR` | rc 1 `ERROR: <message>.` | **rc 0** (lowered to `initial $display`) | rc 1 `ERROR: [XSIM 43-4462] ... $error : ...` | rc 1 `[Synth 8-6058]` |
| module `$warning` | rc 1 `%Warning-USERWARN` | **rc 0** `Warning: ...` | **rc 0** | **rc 0** `WARNING: [VRFC 10-8281]` | **rc 0** `WARNING: [Synth 8-6060]` |
| module `$info` | **rc 0** | **rc 0** | **rc 0** | **rc 0** | **rc 0** |
| `initial` `$fatal` | **rc 0** | rc 1 `Can't resolve task name '$fatal'` | rc 1 `$finish executed` | **rc 0** | rc 1 `[Synth 8-6058]` |
| `initial` `$error` | **rc 0** | rc 1 `Can't resolve task name '$error'` | not measured | **rc 0** | rc 1 `[Synth 8-6058]` |

## 4. Per-guard, per-front-end refusal table

Every guard at the head, through every front end: the violating case refused in the front
end's own words, at the guard's own line, as a `$fatal`; the nearest passing case
elaborating clean. Verilator runs `scripts/lint_hdl.sh`'s flags; Yosys runs as
`syn/yosys/run.sh` runs a top (sv2v over the tree, `read_verilog -defer`, `chparam`,
`hierarchy -check -top`, `proc`, `opt_clean`); xelab after `xvlog` over the tree;
`synth_design -rtl -part xc7a100tfgg484-2`. Each guard is elaborated in its own module, the
top's five in `protocol_processor_top`. "same text" means the Vivado message is
character-for-character Verilator's. Yosys 0.66 prints `$fatal(1, ...)` as `FATAL: .` (it
takes the finish number for the text); the bench locates that line inside the guard's
block in the lowered file. Source logs: `tb/elab_guards` at the head `ef86ea84` under each
toolset (155 of 155 each), and its two Vivado legs at the head (155 of 155: the control of
the Vivado campaign, section 5). The table is generated from those three logs; an earlier
Vivado run on a scratch tree byte-identical in `hdl/` and the bench gives the same table.

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

Rows 28-30 have no violating parameter set: `TMR_AW_C` is `$clog2(TMR_SLOTS_C)`, every
timer-slot base is the running sum of the extents before it, and `TMR_SLOTS_C` is the map's
own end, so their conditions are false at every shape that elaborates (`N_AVB_IF_P = 0`
reaches row 29, with row 27 refusing first). Their violating case is one derived value moved
by one in a scratch copy of `hdl/` (`plant` in `GUARDS`); the guard's condition is what
refuses it. Three passing cases are at 2, not at the guard's boundary 1: at 1 they elaborate
but Verilator `-Wall` calls `x >= 32'(N - 1)` constant (`UNSIGNED`), a lint finding.

**The same bench at base** (the tree before this lane, graded by the head's bench; Verilator +
Yosys: 156 checks, 94 PASS, 62 FAIL under sv2v 0.0.12; xelab + synth_design: 156 checks, 123
PASS, 33 FAIL, rc 1, 785 s under the lock):

| Front end | Result at base | What fails |
|---|---|---|
| Verilator lint | 30 GUARD FAIL | the 29 `$error` guards are refused as `%Warning-USERERROR`, not as a fatal; the listener's `initial` guard is never reported (at `STRM_TIMEOUT_CYC_P=0` the lint's only findings are `ASCRANGE` from the zero-width timeout counter, not the guard) |
| sv2v 0.0.12 + Yosys 0.66 | 30 GUARD FAIL | the 29 `$error` guards are refused, but as `ERROR: <message>.`; the listener's as ``Can't resolve task name `$fatal'`` |
| sv2v 0.0.13 + Yosys 0.66 | 30 GUARD FAIL | **the 29 `$error` guards elaborate** ("the guard did not stop it"); the listener's is refused at its lowered `$finish` but under the old block name |
| inventory | 2 FAIL | `parameter_checks` is a severity task no guard accounts for; `g_strm_tmo_check` is absent |
| xelab | 30 GUARD FAIL | the 29 `$error` guards are refused, but as `ERROR: [XSIM 43-4462] File <file>, line <n>: $error : ...`, not as a fatal; the listener's `initial` guard is never run (xelab stops later, at `[VRFC 10-9955] illegal size casting to zero or negative value for width [hdl/acmp/KL_pp_acmp_listener.sv:1499]`, not at the guard) |
| synth_design -rtl | 1 GUARD FAIL | the 29 `$error` guards pass: Vivado synthesis refuses a `$error` in a `$fatal`'s words (`[Synth 8-6058]`, section 3). The listener's `initial` `$fatal` is refused at its line (:347), but under the old block `parameter_checks`, so the bench does not count it for `g_strm_tmo_check` |

`KL_pp_nvm_port.g_maxp_check` (already `$fatal`) passes everywhere at base. Every passing
case elaborates at base too.

## 5. New checks and their failing mutants

| New or changed check | Where | Planted mutant that fails it | Result |
|---|---|---|---|
| inventory: every severity task is a listed guard | `tb/elab_guards/guards.py` | `bench:unlisted` (a new `$fatal` guard in `KL_pp_release_merge`) | KILLED, `FAIL: inventory KL_pp_release_merge.g_unlisted_check` |
| inventory: every listed guard is in `hdl/` | same | `bench:deleted` (`KL_aecp_engine.gen_g_line_step` removed) | KILLED, `FAIL: inventory KL_aecp_engine.gen_g_line_step: 0 severity tasks, not 1` |
| GUARD verilator (USERFATAL at the guard's line, with its words) | same | 31 `error`, 31 `warning`, 31 `initial`; `bench:message`; `bench:loosened`; `bench:deleted` | all KILLED, each by name |
| GUARD yosys (FATAL or `$finish` inside the guard's block) | same | 31 `error`, 31 `warning`, 31 `initial` (sv2v 0.0.12; under 0.0.13 the `initial` arms survive this leg only); `bench:loosened`; `bench:deleted` (refusal at another guard's line) | all KILLED, each by name |
| ELAB verilator / yosys (nearest passing case clean) | same | `bench:tightened` (`>` to `>=`) | KILLED in both legs |
| GUARD xsim (`[VRFC 10-8279] $fatal` at the guard's line) | same | 4 `error`, 4 `warning`, 3 `initial` arms, `bench:deleted`, `bench:loosened` (Vivado campaign, below) | all KILLED by name |
| GUARD synth (`[Synth 8-6058]` at the guard's line) | same | 4 `warning` arms, `bench:deleted`, `bench:loosened`; not the `error` and `initial` arms, by design: Vivado synthesis refuses those forms too, with the same words (section 3) | KILLED |
| ELAB xsim, ELAB synth | same | `bench:tightened` | KILLED in both legs |
| `elab_bounds.sh`: `MEM_TIMEOUT_CYC_P` refusal must be `USERFATAL` (was any warning) | `tb/nvm_port/elab_bounds.sh` | `g_tmo_check` as `$error`, as `$warning` | rc 2, `GUARD FAIL MEM_TIMEOUT_CYC_P=0 refused as %Warning-USERERROR` (resp. `USERWARN`) |
| `elab_bounds.sh`: Yosys leg accepts `FATAL` (sv2v 0.0.12) as well as `$finish`, never another ERROR | same | `g_maxp_check` and `g_tmo_check` as `$error` under sv2v 0.0.12 | rc 2, `YOSYS FAIL ...=65528 failed, but not at the guard's $fatal`; under 0.0.13 `... elaborated; the guard is not a $fatal`; `$warning`: `elaborated` under both |
| `elab_bounds.sh`: new Yosys leg for `MEM_TIMEOUT_CYC_P` (1 builds, 0 refused) | same | `g_tmo_check` as `$error` / `$warning` | killed as above |
| `if_guards.py`: refusal must be `USERFATAL` (was `USERERROR`) | `tb/pp_top/if_guards.py` | `gen_g_avb_if` as `$error`, as `$warning` | rc 2, `FAIL: if guard 0` and `FAIL: if guard 3` |
| `line_guards.py`: refusal must be `USERFATAL` (was `USERERROR`) | `tb/pp_top/line_guards.py` | `gen_g_line_step`, `gen_g_gamap_page_fit`, `gen_g_line_ceiling` as `$error`, as `$warning` | rc 2, `FAIL: line guard 580` / `568` / `1016` |

The campaign (`make -C tb/elab_guards mutants`, 98 arms + control), at the head:

| Toolchain | Control | Killed | `error` arms | `warning` arms | `initial` arms | Wall |
|---|---|---|---|---|---|---|
| Verilator 5.050, sv2v 0.0.12, Yosys 0.66 | PASS | 98 of 98 | 31, each by both legs | 31, each by both legs | 31, each by both legs | 703 s |
| Verilator 5.050, sv2v 0.0.13, Yosys 0.66 | PASS | 98 of 98 | 31, each by both legs | 31, each by both legs | 31, by Verilator only | 682 s |

The Vivado campaign (`mutants.py --frontend xsim --frontend synth --jobs 1`, under the
exclusive lock, at the head), a 14-arm subset: its control is the full bench through both
Vivado legs (rc 0, 155 of 155, 14 min), then each arm (9 min together):

| Arm | Killed by |
|---|---|
| `KL_pp_acmp_listener.g_strm_tmo_check:error` | GUARD xsim (xelab passes the `$error` and stops later at `[VRFC 10-9955]`, a zero-width cast) |
| `KL_pp_acmp_listener.g_strm_tmo_check:warning` | GUARD xsim, GUARD synth |
| `KL_pp_acmp_listener.g_strm_tmo_check:initial` | GUARD xsim |
| `KL_aecp_engine.gen_g_line_ceiling:warning` | GUARD xsim, GUARD synth (both stop one level down, at `KL_aecp_ucpu.gen_g_d8_cap`) |
| `KL_pp_nvm_port.g_tmo_check:error` | GUARD xsim (`[XSIM 43-4462]`, a `$error`) |
| `KL_pp_nvm_port.g_tmo_check:warning` | GUARD xsim, GUARD synth (both elaborate) |
| `KL_pp_nvm_port.g_tmo_check:initial` | GUARD xsim (elaborates) |
| `protocol_processor_top.gen_g_tmr_overlap:error` | GUARD xsim |
| `protocol_processor_top.gen_g_owner_overlap:error` | GUARD xsim |
| `protocol_processor_top.gen_g_owner_overlap:warning` | GUARD xsim, GUARD synth |
| `protocol_processor_top.gen_g_owner_overlap:initial` | GUARD xsim |
| `bench:deleted` | inventory, GUARD xsim, GUARD synth |
| `bench:tightened` | ELAB xsim, ELAB synth |
| `bench:loosened` | GUARD xsim, GUARD synth (synth stops later, `[Synth 8-524]` part-select) |

14 of 14 killed, rc 0. The subset is not all 93 severity arms because every arm's Vivado run
holds the shared lock; xelab, the leg that tells the forms apart, killed every one of them.

The consumer-bench mutants (16 runs: `elab_bounds.sh` under both sv2v, `if-guards`,
`line-guards`), each in a scratch copy: 16 of 16 failed their bench (rc 2), at the head.

## 6. Base/head record identity

Base `2cbed0a9` and head `ef86ea84` records, Verilator 5.050 throughout. Where a record is
"identical but", the named difference is the only one: the logs are identical with it masked.

| Record | Base | Head | Identity |
|---|---|---|---|
| `scripts/lint_hdl.sh` | rc 0, 41 `LINT OK` | rc 0, 41 `LINT OK` | identical |
| `make check` | rc 0 | rc 0 | identical except two counts: `links: 1187` to `1191` (the four links this lane adds: the guide's row to `guards.py` and to section 2.1, `hdl/README.md` rule 6, the suite README) and `ids: 563 files` to `567` (the suite's four files) |
| `python3 scripts/gen_matrix.py --check` | rc 0, 94 rows, 0 untested | same | identical |
| `syn/yosys/run.sh`, sv2v 0.0.12 + Yosys 0.66 | rc 0, 42 `YOSYS OK`, parsed once, `YOSYS XILINX OK` | same | identical but for eight Yosys memory warnings whose `all.v:<line>` moves (the lowered listener guard is one line longer, ahead of `KL_aecp_engine` in `all.v`); identical with those numbers masked |
| `syn/yosys/run.sh`, sv2v 0.0.13 + packaged Yosys 0.66 | rc 0, same verdicts | same | identical but for the same eight warnings' `all.v:<line>`, moved by 8 to 74 lines (each lowered `$fatal` is longer than a lowered `$error`) |
| `scripts/run_suites.sh` | rc 0, 3 gates PASS, 34 suites, 1,029,620 checks, 0 failing (1,622 s) | rc 0, 3 gates PASS, 35 suites, 1,029,775 checks, 0 failing (1,816 s, beside two campaigns) | all 37 base result lines (3 gates, 34 suites) identical; the one added line is `PASS elab_guards (155 checks: 155 PASS, 0 FAIL)`, and the total grows by its 155 |
| `scripts/run_suites.sh`, pinned sv2v 0.0.12 + Yosys 0.66 on PATH | not run whole: its `tb/nvm_port` step fails alone at base (next row, `nvm_elab_pinned`) | rc 0 (1,344 s) | the head log is byte-identical to the head record above |
| `make -C tb/nvm_port elab`, pinned sv2v 0.0.12 | rc 2: `YOSYS FAIL MAX_PAYLOAD_P=65528 failed, but not at the guard's $finish` / `port.v:95: ERROR: FATAL: .` | rc 0: both Yosys lines `YOSYS OK ... stops at the guard's $fatal` | the lane's fix (section 10) |
| Netlists, Yosys (55) and ROM images (2) | | | **57 of 57 identical** (below) |
| Vivado OOC netlist, default shape (`syn/ooc/protocol_processor_ooc.tcl`, then `write_verilog -mode funcsim`) | rc 0, 17,376,531 bytes; 29,096 LUTs, 25,459 registers, 19 BRAM tiles | rc 0, 17,376,531 bytes | **identical but its `// Date` line** (sha256 without it `e5c3b98b...` both); `util.rpt` identical; ROM images `518b900c...` / `23cc67ee...` both |
| Vivado OOC netlist, 9x9 (`N_STREAM_IN_P` = `N_STREAM_OUT_P` = 9, the `endstation_ax7101_8x8` stream shape) | rc 0, 17,882,923 bytes; 29,951 LUTs, 26,415 registers, 20.5 BRAM tiles | rc 0, 17,882,923 bytes | **identical but its `// Date` line** (sha256 without it `56bbaf5b...` both); `util.rpt` identical |

Netlists: every `syn/yosys/run.sh` top at its defaults (42) and `protocol_processor_top` at
13 more shapes (1x1, 9x9, 4x4, 1x8, 8x1, 16x16, 2x2, 5x5, and the parent's five configs as
`milan_datapath` binds them, `N_STREAM_IN_P` = the config's `ADP_LISTENER_SINK_C`,
`N_STREAM_OUT_P` = `ADP_TALKER_SRC_C`, `DESC_NAME_ENTRIES_P` = `AEM_NAME_ENTRIES_C`:
`endstation_arty_4x4` 5x5/55, `endstation_arty_8ch` 5x5/87, `endstation_arty_current` 2x1/29,
`endstation_ax7101_1x1_tdm8` 2x2/39, `endstation_ax7101_8x8` 9x9/107, all at 50 MHz),
each elaborated in a fresh Yosys 0.66 (sv2v 0.0.12) as `run.sh` does and written with
`write_verilog -noattr -norename`. Compared with `all.v` line numbers masked, Yosys
auto-indices replaced by their rank, and lines sorted: base and head equal for all 55, and
`ucode.hex` (`518b900c...`) and `ltn_rom.hex` (`23cc67ee...`) equal, which are also the
parent's `rom_digests.tsv` rows for its current pin `2ad2f845`. Unmasked, they differ only
in those line numbers and in auto-index numbering (the base listener's `initial` block
spends a few indices the head's generate block does not).

## 7. Suites

`scripts/run_suites.sh` at base: rc 0, 3 gates PASS, 34 suites, 1,029,620 checks, 0 failing, with the
pinned Verilator and the host's default sv2v 0.0.13 / packaged Yosys 0.66 on PATH. (With the
pinned sv2v 0.0.12 on PATH, base's nvm_port suite fails in `elab_bounds.sh`, section 10.)
Head: rc 0, 3 gates PASS, 35 suites, 1,029,775 checks, 0 failing, same PATH. The 34 existing suites and 3 gates print
the same line each (nvm_port 1,219, pp_top 10,470, timer_map 1,360, ...); `elab_guards` is the
one added line (155 checks here, its Yosys leg on sv2v 0.0.13; 93 where sv2v or yosys is
absent, as in the processor's hosted suites job).

`tb/elab_guards` at the head: 155 of 155 with sv2v 0.0.12 + Yosys 0.66 (116 s) and with
sv2v 0.0.13 + Yosys 0.66 (167 s). Its Vivado legs (`make vivado`'s two front ends): 155 of
155 at the head, 14 min under the lock (the Vivado campaign's control).

The head's `run_suites.sh` was also run with the pinned sv2v 0.0.12 + Yosys 0.66 first on
PATH: rc 0, its log byte-identical to the head record above (so `elab_guards`' Yosys leg
and `elab_bounds.sh`'s pass under both sv2v). At base that toolset fails `tb/nvm_port`
(`make -C tb/nvm_port elab`, rc 2, recorded in `records/base/nvm_elab_pinned.*`).

## 8. Campaigns

Every campaign that builds a changed file, base `2cbed0a9` and head `ef86ea84`, each in
its own output directory, the pinned Verilator 5.050, `--jobs 4` at base and 3 at head where
the driver has it (two campaigns at once). Identity: the two logs compared with the output
directory's label, temp-directory suffixes and seconds masked; the three drivers that print
arms in completion order are compared as sorted lines (`evidence/campaigns/compare/`).

| Campaign | Builds a changed file through | Base | Head | Identity |
|---|---|---|---|---|
| `tb/pp_top/d3_mutants.py` | `protocol_processor_top` | rc 0, 110 of 110 KILLED, goldens PASS (4,214 s) | rc 0, 110 of 110 KILLED, goldens PASS (4,708 s) | identical as sorted lines (117) |
| `tb/pp_top/notify_mutants.py` | top | rc 0, 93 of 93 KILLED, goldens PASS (1,052 s) | rc 0, 93 of 93 KILLED, goldens PASS (1,176 s) | identical as sorted lines (107) |
| `tb/srp_top/mutants.py` | `KL_srp_encoder` | rc 0, 137 checks PASS (997 s) | rc 0, 137 checks PASS (1,218 s) | identical (138 lines) |
| `tb/pp_top/acmp_mutants.py` | top | rc 0, 51 of 51 KILLED, goldens PASS (1,604 s) | rc 0, 51 of 51 KILLED, goldens PASS (1,536 s) | identical as sorted lines (58) |
| `tb/pp_top/aecp_mutants.py` | top | rc 0, 67 checks PASS (730 s) | rc 0, 67 checks PASS (716 s) | identical (700 lines) |
| `tb/pp_top/aecp_dispatch_mutants.py` | top (and its line-guard patches) | rc 0, 44 checks PASS (558 s) | rc 0, 44 checks PASS (633 s) | identical (275 lines) |
| `tb/adp_engine/mutants.py` | top (and its `if-top-range-*` patches) | rc 0, 62 checks PASS (286 s) | rc 0, 62 checks PASS (377 s) | identical (422 lines) |
| `tb/pp_top/gsi_mutants.py` | top | rc 0, 20 detected by named checks (522 s) | rc 0, 20 detected by named checks (889 s) | identical (23 lines) |
| `tb/maap/mutants.py` | top (`maap-internal`) | rc 0, 32 checks PASS (121 s) | rc 0, 32 checks PASS (214 s) | identical (101 lines) |
| `tb/pp_top/ctr_mutants.py` | top | rc 0, 18 checks PASS (228 s) | rc 0, 18 checks PASS (407 s) | identical (113 lines) |
| `tb/srp_admission/mutants.py` | `KL_srp_top` (encoder) | rc 0, 12 checks PASS (322 s) | rc 0, 12 checks PASS (574 s) | identical (13 lines) |
| `tb/name_state/mutants.py` | `KL_aecp_desc_store`, `KL_aecp_nvm_writer` | rc 0, 16 arms KILLED (321 s) | rc 0, 16 arms KILLED (438 s) | identical as sorted lines (17) |
| `tb/pp_top/name_wr_mutant.py` | top | rc 0, decode killed, golden and restored PASS (64 s) | same (82 s) | identical (4 lines) |
| `tb/desc_mem_guard/mutate.py` | `KL_aecp_desc_store` | rc 0, completed byte assertion detected (7 s) | same (7 s) | identical (2 lines) |
| `make -C tb/nvm_port figures` | `KL_pp_nvm_port` | rc 0, all measured figures agree with the tree (944 s) | same (1,077 s) | identical (173 lines) |
| `make -C tb/elab_guards mutants` | every guarded module | (new) | rc 0, 98 of 98 under each sv2v | |

15 of 15 existing campaigns: rc 0 at base and head, every record identical. (A first head
pass was cut by the usage-limit stop with `gsi` and `maap` part-run; both were re-run from a
fresh output directory, and the four not started then were run in the same pass.)

Not run, as they build no changed file: `tb/acmp_talker/retry_mutants.py` (its bench builds
`pp_pkg.sv`, `srp_pkg.sv` and `KL_acmp_talker.sv`, none changed) and
`tb/desc_store/lint_mutations.py` (mutations of the descriptor model for the image
generator's semantic lint; it reads no RTL).

## 9. Scratch parent

Clone of kebag-logic/milan-fpga at dev `e8454e2751d05b02ee8e5a571857589ab358ab86` (its
`protocol-processor` gitlink there is `2ad2f845`, an ancestor of base, 49 commits behind).
`third_party/verilog-axis` (`48ff7a7e`) and `gptp-processor` (`5dce647a`) from their pins.
The processor submodule was checked out at base `2cbed0a9`, then at the head, the head
fetched from the lane's local path; the gitlink staged in the parent's index each time
(`git update-index --cacheinfo`), never committed, never pushed, no config changed.

| Parent gate (pinned toolchain) | gitlink base `2cbed0a9` | gitlink head |
|---|---|---|
| `scripts/lint_rtl.py --check --self-test --jobs 4` | rc 0, `LINT GATE: PASS (90 violation(s) <= ratchet 90; 18 waived, 0 justified lint_off)` | identical log |
| `syn/yosys/run.sh --mode elaborate` (every top) | rc 0, 61 tops PASS, tap purity PASS | identical with timings masked |
| shipping shapes: the parent's own `lint_one` on `milan_datapath` per config (its generated shape header first, `N_STREAMS`, 50 MHz) | rc 0; 5 configs: 0 `USER*` diagnostics from any path, 0 hard | rc 0; identical log |

No shipping shape trips a guard: no `USER*` diagnostic in Verilator's raw output for any of
the five configs (the parent gate hides processor-path diagnostics, so the raw output was
read), and the processor's own netlist record (section 6) elaborates the five configs'
processor parameter sets with no refusal in Yosys.

**Parent lint gate finding (parent-side, not changeable here).** With one `-G` override that
trips a processor guard (`KL_pp_shadow`, `-GN_STREAM_IN_P=40`), the parent's own `lint_one`:

| gitlink | Verilator (the parent's flags) | `lint_one` verdict |
|---|---|---|
| base | rc 1; `%Warning-USERERROR: protocol-processor/hdl/top/protocol_processor_top.sv:911:5: F08.4: owner tags OVERLAP at SI=40 SO=8 (8-bit expiry bus)` (and `KL_aecp_nvm_writer.sv:315`) | 0 hard errors; the processor-path diagnostics dropped |
| head | rc 1; `%Warning-USERFATAL:` the same two lines | 0 hard errors; dropped |

So Verilator, run as the parent runs it, refuses the guard at the head as a fatal; the
parent's wrapper discards every `protocol-processor/` diagnostic before its hard-error
test and never reads Verilator's exit status, whatever the severity. Closing that needs a
parent change (for example, treat `USERFATAL` from any path, or a non-zero exit with no
counted finding, as a hard error).

## 10. Open items

- At base, with the CI-pinned sv2v 0.0.12 + Yosys 0.66 on PATH, `tb/nvm_port/elab_bounds.sh`
  (run by the nvm_port suite) fails: `YOSYS FAIL MAX_PAYLOAD_P=65528 failed, but not at the
  guard's $finish` / `port.v:95: ERROR: FATAL: .`. Its Yosys leg required the word
  `$finish`, which only sv2v 0.0.13's lowering produces; sv2v 0.0.12 passes `$fatal` to
  Yosys, which refuses it in its own words. Fixed in this lane (the leg accepts `ERROR: FATAL`
  or `$finish`, and still refuses a `$error`'s `ERROR: <message>`). Because of it, the base
  `run_suites.sh` record is taken with the host's default sv2v 0.0.13 (section 7).
- The parent's `scripts/lint_rtl.py` drops every Verilator diagnostic whose path is under
  `protocol-processor/` before it tests for a hard error, and it does not read Verilator's
  exit status (`lint_one`, and `HARD_RE` excludes `%Error: Exiting due to`). Measured on
  the scratch parent (section 9): a tripped processor guard is `USERFATAL`, rc 1 from
  Verilator at the head, and the gate counts 0 hard errors. The same gate also counts 0
  hard errors for the parent's own `KL_nvm_backend.sv:285` `$error` guard in that run.
  Parent-side; named for the manager.
- Out of this lane's permitted scope, so left as they are and named here for the manager:
  `docs/guides/integrator.md:114` ("exceeding either raises `$error`") and
  `docs/diagrams/21-integration-faces.svg:53` ("stops the build with $error") now name the
  wrong task; `docs/architecture/09_verification.md`'s verification table has no row for
  the new `tb/elab_guards` suite. Each is one line of wording.

## 11. Evidence (`evidence/`, host paths replaced by `<scratch>`, `<lane>`, `<tools>`, `<vivado>`)

| Directory | Holds |
|---|---|
| `records/{base,head}/` | each gate's `.log`, `.rc`, `.env` (tool identities, tree head) and `.cmd`: `lint_hdl`, `make_check`, `gen_matrix`, `yosys_pinned` / `yosys_host` (`syn/yosys/run.sh` under sv2v 0.0.12 / 0.0.13), `run_suites`, `run_suites_pinned` (head), `nvm_elab_pinned`, `elab_guards_*` (head); `vivado_chain*.txt` the Vivado queue log |
| `bench/` | `tb/elab_guards` at base and head under each toolset and through the Vivado legs; `guard-table-head.md` (section 4's table, generated) |
| `mutants/` | the campaign logs: both sv2v, the Vivado subset (`head-xelab-synth.log`), the consumer-bench mutants |
| `campaigns/{base,head,compare}/` | the 15 campaigns' logs, rc and commands; the masked diffs and the generated table |
| `parent/{base,head}/` | the scratch parent's gates, the shipping-shape lint and the lint-gate measurement |
| `netlists/` | the 57 Yosys netlist and ROM digests per side; the OOC runs' `util.rpt`, rc, seconds, masked digest and size |
| `probe/` | the eight one-guard probe modules behind section 3 |
| `scripts/` | every script that produced a record |

Kept out of the output directory (over 200 KB), sha256 and size:

| Artifact | sha256 | Bytes |
|---|---|---|
| OOC funcsim netlist, base, default shape | `84e99a8ec87ba026d99ca43669192028a448d8a0b56edfaaa69f3e6c148b6aef` | 17,376,531 |
| OOC funcsim netlist, head, default shape | `35bebd183b3c9ea726bce799a6ce25de926048b9cc2dc635bb1f05dbfee3a880` | 17,376,531 |
| OOC funcsim netlist, base, 9x9 | `d6448fa2b83b9511ee8a7f3e35c990303ae2ab73a5942b336da383dc5c9e4174` | 17,882,923 |
| OOC funcsim netlist, head, 9x9 | `4a00d1a890b99003af39e33b3290c240271e61c8d8767eae07d09264701d9bf9` | 17,882,923 |

(The raw digests differ only by the `// Date` line; without it base and head are
`e5c3b98b...` at the default shape and `56bbaf5b...` at 9x9, each pair equal.) The Vivado
console logs of the OOC runs (about 255 KB each) and the Yosys netlists themselves stay in
the scratch directory.
