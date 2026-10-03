# [A518] Lane C10 (tooling): HANDOFF

Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
Branch: `c10-tooling`, from `main` `f4167536`
Issues: #25 (item 1), #17 (item 2), #22 (item 3), #37 (item 4). Supersedes PR #26.

Status: DONE at head `54f9411ab9a4b4aea58393f7fa1303ddcc96ee3c` (not pushed; no PR opened). TAKEN posted on #25 (comment 5967294275); REVIEW READY posted with the head (comment 5968833276).

Commits on `c10-tooling` after `main` `f4167536` (one-line subjects; plus the branch's own two,
`2182f27` and `7f35ed2`, kept by the merge):

| Commit | Item | What |
|---|---|---|
| `5c20350` | 1 | merge of `25-cover-every-module-and-stop-reparsing`, `--no-ff` (parents `f4167536`, `7f35ed2`) |
| `b5e3b97` | 1 | parse `all.v` once; a failing top still named |
| `5fbb22f` | 1 | the allocator comment's figures re-measured |
| `746216b` | 2 | `MAX_PAYLOAD_P` above 65527 refused at elaboration |
| `34b5246` | 3 | `protocol_processor_top.sv` declarations above first use |
| `8473c04` | 4 | pp_top AX section NSD and three mutants |
| `ba24dfc` | 4 | the dispatch campaign's re-run recorded (one count moved) |
| `54f9411` | 2 | nvm_port's figures table and three line citations follow the guard's ten lines |

Tools: Verilator 5.050 (pinned), Yosys 0.66, sv2v 0.0.13, Vivado 2026.1, one 16-CPU host.

## Item 1: #25, the Yosys gate covers every module, parses once

Commits:
- `5c20350` merge of `25-cover-every-module-and-stop-reparsing` (`7f35ed2`), `--no-ff`,
  parents `f4167536` and `7f35ed2`. One conflict, `syn/yosys/run.sh`: the branch's
  structure (census, jemalloc, pool) with main's `pipefail`, its sv2v-line comment and
  the three modules main added since (`KL_aecp_desc_mem_guard`, `KL_pp_nvm_mgr_arb`,
  `KL_pp_acmp_lsn_admit`). Gate at the merge: rc 0, 42 OK, XILINX OK.
- `b5e3b97` parse once: `syn/yosys/run.sh:201-267`. One yosys reads `all.v` once
  (`read_verilog -defer`), `design -save`, then per top `design -load`,
  `hierarchy -check -top T; proc; opt_clean`. Markers on stderr name the failing top;
  after a failure a fresh run resumes at the next top, so every top gets a verdict
  (a green gate parses exactly once, printed as `all.v parsed 1 time(s)`). The pool,
  `YOSYS_JOBS` and per-top re-parse are gone. RAMB36E1 regression unchanged
  (`run.sh:275-277`).
- `5fbb22f` the allocator comment's figures re-measured for the parse-once gate.

Census (from the branch, `run.sh:152-173`): fails when a declared module has no top, or
a top names no declared module. 42 declared, 42 tops.

Red proofs (scratch `git archive` copies, fault = an instance of an undeclared module
before the module's `endmodule`):

| Planted fault | `main` f4167536 gate | head gate |
|---|---|---|
| in `KL_acmp_nvm_shadow` | rc 0, 36 OK (missed) | rc 1: `YOSYS FAIL KL_acmp_nvm_shadow: ERROR: Module \c10_absent_module referenced in module \KL_acmp_nvm_shadow ...`, then `protocol_processor_top` |
| in `KL_mrp_strip` | rc 0 (missed) | rc 1: `YOSYS FAIL KL_mrp_strip`, then `protocol_processor_top` |
| in `KL_pp_dispatch_fifo` | rc 1, caught through its parent `KL_pp_dispatch` | rc 1: `KL_pp_dispatch`, `KL_pp_dispatch_fifo`, `protocol_processor_top` |
| in `KL_srp_admission` | rc 0 (missed) | rc 1: `KL_srp_admission`, `KL_srp_top`, `protocol_processor_top` |
| in `KL_srp_top` | rc 0 (missed) | rc 1: `YOSYS FAIL KL_srp_top`, then `protocol_processor_top` |
| in `protocol_processor_top` | rc 0 (missed) | rc 1: `YOSYS FAIL protocol_processor_top` (1 parse) |
| two faults, `KL_mrp_strip` + `KL_srp_admission` | - | rc 1, 4 FAIL lines, each top named, `parsed 4 time(s)` |
| `KL_srp_top` dropped from `tops` | - | rc 1: `modules declared under hdl/ with no entry in the tops array: KL_srp_top` |
| `KL_c10_gone` added to `tops` | - | rc 1: `tops array names modules that no longer exist under hdl/: KL_c10_gone` |
| syntax fault planted in `all.v` after sv2v, inside `KL_srp_top` | - | rc 1: `YOSYS FAIL all.v in module KL_srp_top: all.v:20318: ERROR: syntax error, unexpected '@'`, then all 42 `not elaborated, the parse failed` |

Note: the issue's claim that `KL_pp_dispatch_fifo` is unreached no longer holds at main:
`KL_pp_dispatch` instantiates it, so main's gate catches a fault there through the parent.
Five of the six were uncovered.

Wall time, end to end (`./syn/yosys/run.sh`, sv2v + elaboration + XILINX regression),
each run alone on the same host, three interleaved rounds, median:

| Revision | Tops | Rounds (s) | Median | Peak RSS |
|---|---:|---|---:|---:|
| `main` f4167536 (one process per top, full re-parse) | 36 | 83.30, 90.51, 88.80 | **88.80 s** | 0.80 GB |
| `5c20350` merge (PR #26's 16-way pool, `-defer`) | 42 | 28.70, 30.00, 30.04 | 30.00 s | 0.81 GB |
| head `b5e3b97` (parsed once, jemalloc; `5fbb22f` changes only a comment) | 42 | 35.97, 34.24, 36.57 | **35.97 s** | 0.80 GB |
| head, `YOSYS_MALLOC=none` | 42 | 51.22, 48.12, 45.66 | 48.12 s | 0.80 GB |

The elaboration step alone on one staged `all.v`: main's per-top loop 50.89 s (36 tops);
parsed once 10.00 s (42 tops, jemalloc), 12.5-14.0 s on the system allocator; the
pool 7.21 s (16-way, system allocator). Verdict lines identical between the merge, the head and the head on the
system allocator (only the new `parsed 1 time(s)` line differs). Peak RSS is the
XILINX regression's.

## Item 2: #17, MAX_PAYLOAD_P bound

Commits `746216b` and `54f9411`.
- `hdl/packet_engine/KL_pp_nvm_port.sv:112-114` banner; `:192-200` the guard:
  `if (MAX_PAYLOAD_P > 65527) begin : g_maxp_check $fatal(1, "KL_pp_nvm_port:
  MAX_PAYLOAD_P=%0d is above 65527: 8 + it overflows dev_len_o", ...)`.
- Placement: the precedent's `$fatal(1, ...)` (`KL_pp_acmp_listener.sv:344-347`), at
  module scope like the port's own `g_tmo_check` and every other guard in `hdl/`.
  Measured on a two-module probe and on the port: the precedent's literal `initial`
  placement is NOT refused at elaboration by Verilator 5.050 (lint and `--build` rc 0;
  it stops at simulation time 0). The module-scope `$fatal` fails elaboration in all
  three front ends:

| Front end, `MAX_PAYLOAD_P` = 65528 | `initial` + `$fatal` | module scope `$fatal` (this change) | module scope `$error` |
|---|---|---|---|
| Verilator 5.050 `--lint-only -Wall` | rc 0 (missed) | rc 1, `%Warning-USERFATAL ... MAX_PAYLOAD_P=65528 is above 65527` | rc 1 |
| sv2v + Yosys 0.66 | rc 1 (`$finish` executed) | rc 1 (`port.v:90: ERROR: System task $finish executed`, the guard's line; Yosys prints no `$display` text) | rc 0 (missed) |
| Vivado 2026.1 `synth_design -rtl` | rc 1 | rc 1, `[Synth 8-6058] Synth Error: KL_pp_nvm_port: MAX_PAYLOAD_P=65528 is above 65527 ...` | - |

At 65527 all three elaborate.
- Test: `tb/nvm_port/elab_bounds.sh` (run by `make` in `tb/nvm_port`): legal 1024 and
  65527 lint clean; 65528, 65535 and 4294967295 refused with `MAX_PAYLOAD_P=<v> is above
  65527`. Docs: `tb/nvm_port/README.md:19-22`, `tb/nvm_port/Makefile` `elab` comment,
  `docs/architecture/09_verification.md` §8.6 table, new row.
- Mutants (scratch copies, `elab_bounds.sh` rc 1 for each):

| Mutant | Failing claims |
|---|---|
| guard deleted | `GUARD FAIL MAX_PAYLOAD_P=65528 elaborated`; 65535 and 2^32-1 fail without the name (CMPCONST only) |
| bound `> 65528` | `GUARD FAIL MAX_PAYLOAD_P=65528 elaborated` |
| bound `>= 65527` | `ELAB FAIL MAX_PAYLOAD_P=65527 (a legal value must elaborate clean)` |
| message without the bound | all three refused values: `failed without naming the parameter and its bound` |
| the precedent's `initial` placement | `GUARD FAIL MAX_PAYLOAD_P=65528 elaborated` (+2) |

- The guard moves every line below it in `KL_pp_nvm_port.sv` down by ten.
  `make -C tb/nvm_port figures` caught that, as it exists to: its ARMS table names the
  twelve `if (dev_err_i)` arms by line ("KL_pp_nvm_port.sv:376 is not an `if (dev_err_i)`
  arm any more", rc 2). `54f9411` moves the table and the three cited line ranges
  (`:234-245`, `:340-344`, `:436-439`, cited at `tb/nvm_port/README.md:222`, `:1131`,
  `sim_main.cpp:1328`, `:1441` and `measure_figures.py:117`) by ten. Each was checked against the text it names; the
  `:33-34` citation is above the guard and stays. The figures gate is then rc 0
  ("all measured figures agree with the tree", 160 Verilator builds, 848 s).

## Item 3: #22, declare before use in protocol_processor_top.sv

Commit `34b5246`, `hdl/top/protocol_processor_top.sv` only: seven declaration groups moved
above their first use, nothing else (the sorted multiset of non-blank lines before and
after differs by one added comment line, `:2933`):
- `:935-953` the SRP class-D lanes (19 signals) above the class-D fabric face's assigns;
- `:975` `tkr_declaring_w` above `acmp_declaring_o`;
- `:978-986` the binding view (`bound_r`, `bound_sid_r`, `bound_dmac_r`, `bound_vlan_r`,
  `bound_eid_r`) and `lstn_dbg_busy_w` above the debounce;
- `:1004-1005` `adp_dbg_aidx_nc_w` above `adp_next_avail_index_o`;
- `:1825-1828` `lstn_act_settle_w` (with `lstn_act_teardown_w`) and its sid, da, vlan
  above `binding_view`;
- `:2933-2943` u_notify's arm, monitor-arm and PRNG faces above the arm-port mux.

Evidence:
- `xvlog -sv` (Vivado 2026.1), packages first then one module per invocation, every
  `.sv` under `hdl/`: base 37 of 41 modules analyse; head 38 of 41.
  `protocol_processor_top.sv` goes from `VRFC 10-3380 srp_class_a_prio_w` to clean.
  The three that still fail are outside item 3: `KL_aecp_notify.sv:557` `pd_ix_w`,
  `KL_pp_originator.sv:194` `cancel_hit_w`, `KL_pp_rx_validator.sv:383` `vd_push_w`.
- Vivado OOC `Synth 8-6901`: 51 -> 7 (44 -> 0 in `protocol_processor_top.sv`; the 7 are
  those three files: 3 + 2 + 2).
- Behaviour unchanged, the netlist: the synthesized OOC netlist
  (`write_verilog -mode design`, 19,508,014 bytes) of base `f4167536` and of `34b5246`
  differ only in the `// Date` line; sha256 without it `4baf5a8c...a4e200` for both.
  `util.rpt` and `util_hier.rpt` bodies identical (`c082f3e9...daf03`, `01eb5244...a1cb`),
  WNS identical. RTL is unchanged from `34b5246` to the head (`git diff 34b5246 HEAD --
  hdl` empty), so this holds at the head.
- Verilator 5.050 lint of the top rc 0, 0 warnings; `lint_hdl.sh` 41 of 41.
- The suites: `main` and the head give the same tally in every suite but `tb/pp_top`,
  whose +26 are item 4's NSD checks (see Suites).

#22 is NOT closed by this lane: its acceptance needs every module under `hdl/` clean
under xvlog and zero `Synth 8-6901` for the parent's `KL_pp_shadow`; the three files
above still carry 7. Item 3 is scoped to `protocol_processor_top.sv`.

## Item 4: #37, SET_CLOCK_SOURCE NO_SUCH_DESCRIPTOR arm

Commit `8473c04`. No microprogram change.
- Arm: `tb/pp_top/sim_main.cpp:11538-11562`, `nsd_set_clock_source_on_an_absent_domain()`
  in section AX (`AecpResponsePhase`), called at `:11860` after LK; header list `:11221`.
  - NSD0: the holder changes clock source 2 -> 1 (one store write, one enqueue). E_SCLKS
    leaves the replaced 2 in r6; the µCPU loads only r12-r15 per dispatch
    (`KL_aecp_ucpu.sv:515-521`), so r6 survives into the next program.
  - NSD1: a second controller's SET_CLOCK_SOURCE(2) on CLOCK_DOMAIN 1 (absent):
    NO_SUCH_DESCRIPTOR, byte-exact, zero body, cdl 20, no unsolicited frame at the
    registered holder, no store write, NVM mark or notify enqueue.
  - NSD2: GET_CLOCK_SOURCE still reads the stored 1.
  - NSD3: under the bench's lock, the same command: ENTITY_LOCKED, zero body (the lock
    outranks the miss), nothing moved.
  - 13 checks, in the default build and the line build (AX runs in both): `tb/pp_top`
    9,196 -> 9,222.
- Renumbering since #37 was filed: #53 (`692ad8f`) moved the miss branch from E_SCLKS + 4
  to E_SCLKS + 3 and its target from the in-line tail to the out-of-line E_SCLKSRF
  (ROM 1144), whose first word is CHECK_LOCK.
- Mutants (`tb/pp_top/aecp_dispatch_mutations/`, run by `aecp_dispatch_mutants.py`,
  `:132-144`; records `tb/pp_top/README.md:1129-1131` and the paragraph at `:1177`):

| Arm | Planted | Failing checks (named first) |
|---|---|---|
| `sclks-miss-target-next-word` | branch target one word on (SCLKS_EMIT, past CHECK_LOCK) | NSD3, LK4 (NO_SUCH_DESCRIPTOR where ENTITY_LOCKED is due) |
| `sclks-miss-preload-dropped` | E_SCLKS + 1 `MOVE r6, 0` -> NOP | NSD1, NSD3 (carry 2); LK4 and LK5 pass: NSD is the only arm grading the preload |
| `sclks-miss-branch-dropped` | the miss branch -> NOP | NSD1, LK5 (BAD_ARGUMENTS) |
| target one word back (E_SCLKSRF - 1, ROM 1143) | measured EQUIVALENT: 1143 is unplaced fill, a NOP (`gen_ucode.py` fill, `1143 % 3 == 0`), which runs on into E_SCLKSRF's CHECK_LOCK; 928 of 928 checks pass. Not a campaign arm (the driver counts only kills) |

Run of the three arms alone: control PASS, 3 of 3 KILLED (`--jobs 4`, 36 s).
- Docs: `tb/pp_top/README.md:1824` (AX section, NSD bullet), the campaign table and
  paragraph; `docs/architecture/09_verification.md:163` (§8.1, clock_source row).

## Out-of-context cost, before and after

`syn/ooc/protocol_processor_ooc.tcl` (the complete processor, default shape, all ports,
xc7a100tfgg484-2, 10 ns), Vivado 2026.1, each run alone, through a scratch wrapper that
sources the in-tree recipe and then writes the netlist (`write_verilog -mode design`).
Base `f4167536`; head `34b5246`, whose `hdl/` is the final head's (`git diff 34b5246
54f9411 -- hdl` is empty). Items 2 and 3 are the only RTL changes.

| Resource | Base `f4167536` | Head | Delta |
|---|---:|---:|---:|
| Slice LUTs (logic + memory) | 30,658 (29,436 + 1,222) | 30,658 (29,436 + 1,222) | 0 |
| Slice registers | 31,944 | 31,944 | 0 |
| F7 / F8 muxes | 1,482 / 57 | 1,482 / 57 | 0 |
| RAMB36 / RAMB18 / DSP | 23 / 2 / 4 | 23 / 2 / 4 | 0 |
| WNS / TNS (OOC, no timing claim) | -9.844 / -9502.546 ns | -9.844 / -9502.546 ns | 0 |
| `Synth 8-6901` (use before declaration) | 51: 44 in `protocol_processor_top.sv` (43 identifiers), 3 `KL_aecp_notify`, 2 `KL_pp_originator`, 2 `KL_pp_rx_validator` | 7: 3 `KL_aecp_notify`, 2 `KL_pp_originator`, 2 `KL_pp_rx_validator` | -44 |

Equal. Stronger than the counts: the whole synthesized netlist (19,508,014 bytes) is
byte-identical but for its `// Date` line (sha256 without it `4baf5a8c...0f0411a4e200`, both),
and the `util.rpt` / `util_hier.rpt` bodies are identical (`c082f3e9...e9ddaf03`,
`01eb5244...f2c5a1cb`). Runs: base 155 s, head 160 s (the first base run, 171 s, gave the
same figures).

## Suites and entry points

All with the pinned Verilator 5.050, at the final head `54f9411` unless stated.

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | 33 suites, **1,020,253** checks, 0 failing, 545 s. `tb/pp_top` 9,196 -> **9,222** (+26: NSD's 13 in the default and line builds). A sweep of `main` `f4167536` (a scratch copy, same host): rc 0, 1,020,227 checks, and `pp_top` is the only per-suite difference. A first sweep at `8473c04` gave the head's per-suite tallies exactly (845 s, run beside the light gates) |
| `./scripts/lint_hdl.sh` | 0 | 41 of 41 `LINT OK` |
| `make check` | 0 | 41 mermaid + 18 wavedrom blocks, 1,105 links, 115 REQ rows, 17 GAP, 94 module rows 0 untested, 28 parameters |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `./syn/yosys/run.sh` | 0 | 42 `YOSYS OK`, `all.v parsed 1 time(s)`, `YOSYS XILINX OK KL_aecp_engine` (RAMB36E1 assertions unchanged) |
| `./syn/yosys/run.sh --selftest-alloc` | 0 | allocator selection self-test PASS |
| `make -C tb/nvm_port figures` | 0 | all measured figures agree with the tree; 160 Verilator builds, 848 s |
| `python3 tb/pp_top/aecp_dispatch_mutants.py --jobs 6` | 0 | 4 controls PASS, **40 of 40 KILLED** (37 + this lane's 3), 330 s; counts as the README table (one moved: `lk-sclks-miss-lock-nop` 1 -> 2, NSD3) |
| `python3 tb/pp_top/aecp_mutants.py --jobs 6` | 0 | 5 controls PASS, 55 of 55 KILLED, 309 s |
| `python3 tb/srp_top/mutants.py --jobs 6` | 0 | 90 checks, 0 FAIL (11 controls, 78 KILLED), 360 s |
| `python3 tb/maap/mutants.py --jobs 6` | 0 | 32 checks, 0 FAIL, 55 s |
| `python3 tb/adp_engine/mutants.py --jobs 6` | 0 | 32 checks, 0 FAIL, 101 s |
| `tb/nvm_port/elab_bounds.sh` (in `make`) | 0 | 4 ELAB OK, 6 GUARD OK |

The five campaigns are the HDL workflow's, run through their drivers with `--jobs` (the
workflow runs them through make at the default 4). They ran at `8473c04`; since then only
`tb/pp_top/README.md` and `tb/nvm_port/` changed, which none of them builds. The
`aecp-dispatch` arms of item 4 alone: control PASS, 3 of 3 KILLED.

## Gates

| Gate | rc | Result |
|---|---:|---|
| every processor suite and entry point | 0 | above |
| the Yosys gate with every top | 0 | 42 of 42 declared modules are tops, parsed once |
| the parent consumer set (16) | see below | |

## Parent consumer set (milan-fpga dev 1269cdaf + c8 + p2 patches)

Scratch copy at `$VALIDATION_STORAGE/c10-a518/parent` (scratch only, never the trusted checkout):
a `git archive` of the trusted checkout at `1269cdaf` committed into a fresh repository.
Its tree, gitlinks included, is identical to `1269cdaf` (984 index entries). The submodules
are real checkouts registered with `git submodule init`: gptp-processor `5dce647a` and
verilog-axis `48ff7a7e` cloned from their remotes, and protocol-processor a scratch clone of
this branch at the head `54f9411` with the gitlink recorded there. `external` is left
uninitialised, as the parent's own guide allows. `git submodule status` shows ' ' for all
three. `parent-adoption-c8-cdf49d1a.patch` (sha256 `aa5a88eb...0ad209`, 8,482 bytes),
then `parent-adoption-p2-cdf49d1a.patch` (sha256 `590f791d...39fa`, 11,888 bytes) were
each applied after a clean `git apply --check` and committed; porcelain empty for every gate.
Pinned Verilator 5.050 and Vivado 2026.1's `xvlog` on PATH (gate 9 SKIPs without it).

| # | Command | c8 + p2 | + c10 patch | Result |
|---:|---|---:|---:|---|
| 1 | `scripts/check_cpp_idiom.py` | 0 | 0 | 169 translation units; multi-declarator 0 <= 0, long function 0 <= 0, build without warnings 0 <= 0 |
| 2 | `scripts/check_py_idiom.py` | 0 | 0 | 301 modules; long module 10 <= 10, over-long line 0 <= 0 |
| 3 | `scripts/check_rtl_source_lists.py` | **1** | 0 | c8+p2: six `STALE RECORD: scripts/processor_yosys_tops.budget names '<m>' but protocol-processor/syn/yosys/run.sh elaborates it`, one per newly added top (the six of #25). + c10: `107 files ..., 4 of 4 consumer list(s); protocol-processor 42/42 tops, 0 recorded` |
| 4 | `scripts/pp_srcs.py --check --selftest` | 0 | 0 | 46 tracked sources derived, self-test passed |
| 5 | `scripts/check_port_contracts.py` | 0 | 0 | protocol-processor 1,756 ports, undocumented 111 <= 111 (no port change) |
| 6 | `scripts/measure_naming.py --check` | 0 | 0 | 96 candidates, all recorded |
| 7 | `scripts/measure_test_evidence.py --check` | 0 | 0 | 72 <= 77, 10 <= 10, 0 <= 0 unexplained DUT readers, 3 <= 3 |
| 8 | `scripts/docs_check.py` | 0 | 0 | 0 findings over 185 md + 956 files |
| 9 | `scripts/xvlog_gate.py --check` (alone, last) | **1** | 0 | c8+p2: `BANK IT [submodules]: protocol-processor:hdl/top/protocol_processor_top.sv\|VRFC 10-3380\|srp_class_a_prio_w no longer occurs`; 3 findings remain (the three files of item 3's note). + c10: `PASS (3 finding(s) == ratchet; 0 hdl/, 3 pinned processors)` |
| 10 | `sw/builder/test_builder.py` | 0 | (not re-run) | ALL GATES PASS EXCEPT 1 NOT RUN (its gate 11 needs a local board build tree, as in earlier lanes); 1,122 s |
| 11 | `scripts/lint_rtl.py --check` | 0 | 0 | 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j16` | 0 | (not re-run) | 606, 646, 606 and 311 checks, 0 failures; 203 s |
| 13, 14 | `make -C tb/verilator/nvm_cosim lint`, `quick` | 0, 0 | (not re-run) | lint pass; 315 of 315 |
| 15 | `make -C tb/verilator/milan_dp -j16 VERILATOR_JOBS=3` | 0 | (not re-run) | 9 RESULT: PASS, 0 FAIL, the mutant arms caught; 1,580 s |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | 0 | (not re-run) | 0 failures; 5 of 5 leg-defect arms caught; 346 s |

With the two patches the assignment names, 14 of 16 are rc 0. Gates 3 and 9 are rc 1
**by the parent's own design**, and only for this lane's intended effects. The parent's
`scripts/processor_yosys_tops.budget` says of the six: "the pin bump that brings it in
deletes the line here, because a name that has become a top is refused as STALE". Its
`scripts/xvlog.budget` "--check FAILS ... on any listed finding that no longer occurs (bank
the fix)", and the fix is banked by a normal run. Neither is a port, parameter or behaviour
change, so this is not a STOP condition.

`parent-adoption-c10-1269cdaf.patch` (in this directory; sha256 `6870d2ed...e304b`, 2,764
bytes; applies after c8 then p2) is that bookkeeping and nothing else:
- `scripts/processor_yosys_tops.budget`: the six lines deleted, and the header's sentence
  about them put in the past tense.
- `scripts/xvlog.budget`: regenerated by `scripts/xvlog_gate.py` (a normal run). The
  `protocol_processor_top.sv` key is gone; the other three keys stay, with their line notes
  refreshed (557, 383).

With it, gates 1-9 and 11 re-ran rc 0. Gates 10 and 12-16 read neither budget file (no
file under `sw/` or `tb/verilator/` names either), so their c8+p2 results stand. The
parent's `docs/development/CODE_QUALITY.md:611-616` describes the six as recorded; the
adoption lane may want to reword it.

## Parent-visible list

1. No port, parameter or register of `protocol_processor_top` changed (gate 5:
   1,756 processor ports). `KL_pp_shadow` needs no edit.
2. `syn/yosys/run.sh` elaborates all 42 modules: the parent's tops budget must drop its
   six lines (gate 3), see the c10 patch.
3. `protocol_processor_top.sv` is xvlog-clean: the parent's xvlog ratchet must bank it
   (gate 9), see the c10 patch. The parent's `KL_pp_shadow` synthesis loses the 44
   `Synth 8-6901` warnings from that file; 7 remain in three other files (#22 stays open).
4. `KL_pp_nvm_port` refuses `MAX_PAYLOAD_P` above 65527 at elaboration. The top does not
   override it; `nvm_cosim` instantiates the port at its default.
5. The ROM generators are unchanged from `main` (`hdl/aecp/ucode/gen_ucode.py`,
   `hdl/acmp/rom/gen_ltn_rom.py` untouched), so the ROM digests equal `main`'s. The OOC
   netlist is identical to `main`'s.
6. Processor documents the parent reads: 09 §8.1 (clock_source row) and §8.6 (a new
   row). F01.5, F08.1, the integrator guide and diagram 21 are unchanged.

## What remains

- #22: the three other files (`KL_aecp_notify.sv`, `KL_pp_originator.sv`,
  `KL_pp_rx_validator.sv`) and the integrator-side `KL_pp_shadow` `Synth 8-6901` count.
- #25's note on pinning yosys and sv2v in the `portability` workflow (not in its acceptance)
  is not done; the workflow still installs whatever apt and `releases/latest` resolve to.
- Hosted CI on the branch: not run (no push in this lane).
