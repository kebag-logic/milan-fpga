# [A518] Lane C10 (tooling): HANDOFF

Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
Branch: `c10-tooling`, from `main` `f4167536`
Issues: #25 (item 1), #17 (item 2), #22 (item 3), #37 (item 4). Supersedes PR #26.

Status: round 2 DONE at head `cd08ca7b3d962ab040d8aaa023c57e7b0e010a6d` (see "Round 2" at the end; not pushed; REVIEW READY posted, comment 5970441890). Round 1: DONE at head `54f9411ab9a4b4aea58393f7fa1303ddcc96ee3c`; TAKEN posted on #25 (comment 5967294275); REVIEW READY posted with the head (comment 5968833276); pushed by the manager as PR #149, reviewed NEGATIVE by R448-1 and R449-1.

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

## Round 2

Assignment: #25 comment 5969440297, answering R448-1 (PR #149 comment 5969219155) and
R449-1 (PR #149 comment 5969434371), both NEGATIVE at `54f9411a`. New one-line commits on
top of `54f9411a`; no rebase, no amend, no push. Tools as round 1; the parent's pinned
Markdown renderer, HDL parser and wavedrom were installed in a scratch venv under
`$VALIDATION_STORAGE` (not in this directory) so the parent's documentation gates could run.

Status: DONE at head `cd08ca7b3d962ab040d8aaa023c57e7b0e010a6d` (not pushed). REVIEW READY posted on #25 with the head (comment 5970441890).

Commits after `54f9411a` (head `cd08ca7b3d962ab040d8aaa023c57e7b0e010a6d`):

| Commit | Item | What |
|---|---|---|
| `1a5f555` | 2 | the census reads `module NAME` from sv2v's all.v, so a split header is counted |
| `6ba4659` | 3 | `MAXP_BOUND_C` computed from `$bits(dev_len_o)` and `HDR_LEN_C`, in the guard's condition and message; no line moves |
| `522d49a` | 4 | `elab_bounds.sh` grades the refusal's class (Verilator) and, where sv2v and yosys exist, a yosys stop at 65528 |
| `137ac73` | 5 | the three stale `KL_pp_nvm_port.sv` citations, the shadow instance's line, R449-1 R1's run.sh wording (the subject's "four stale citations" counts the shadow one with the three) |
| `cd08ca7` | 1 (found) | run.sh's census and elaboration loop moved into functions, their name lists quoted: the parent's shell-idiom gate failed on run.sh at `54f9411a` (in neither review) |

### Finding-by-finding table

| Finding | Severity | Resolution | Evidence |
|---|---|---|---|
| R448-1 F1 = R449-1 F1: with c10 the parent's `check_rtl_source_lists.py --selftest` fails 1 of 49 | MAJOR | `parent-adoption-c10-1269cdaf.patch` amended: the "record is non-empty" arm is replaced by two arms on a synthetic population drawn from the live pin (item 1) | at `1269cdaf` + c8 + p2 + c10, processor at the head: gate 3 rc 0, its self-test rc 0, 50 of 50; reproduced first: round-1 c10 gives 48 of 49 |
| R448-1 F2: three stale `KL_pp_nvm_port.sv` citations (R449-1 R2's is the first) | MINOR | `137ac73`: `sim_main.cpp:1443` `:234-245` -> `:244-255`; `README.md:407` `:366` -> `:376`; `README.md:413` `:380` -> `:390` | `sed -n '244,255p;376p;390p'` shows `dev_cmd_owned_w`'s window, `state_r <= S_WEREQ;`, `state_r <= S_WEWAIT;`; the reviewer's grep finds nothing |
| R448-1 S1: compute the payload bound | SUGGESTION | taken, as item 3 | below |
| R448-1 S2: `README.md` cites `protocol_processor_top.sv:2714` | SUGGESTION | `137ac73`: `:2726`, the `KL_acmp_nvm_shadow #(` line at the head | `sed -n 2726p` |
| R449-1 F2: the census misses a split module header | MINOR | `1a5f555`: declared modules are read from sv2v's all.v (item 2) | the reviewer's `yosys_fault.sh ... newmod KL_r449_newmod`, unchanged: rc 0 at `54f9411a`, rc 1 naming `KL_r449_newmod` at the head |
| R449-1 F3: the bound is a mirrored literal | MINOR | `6ba4659` (item 3) | the reviewer's `nvm_bound_probe.sh`, unchanged: `pristine` equals the old `derived` row; `hdr10` gives `elab_bounds.sh` rc 1, `ELAB FAIL MAX_PAYLOAD_P=65527` |
| R449-1 F4: `$error` or `$warning` passes `elab_bounds.sh` | MINOR | `522d49a` (item 4) | same probe: `err` and `warn` rc 1 (were rc 0); pristine rc 0 |
| R449-1 R1: run.sh:9-10 "status files" | RESIDUE | `137ac73`, the exact text | `run.sh:9-10` |
| R449-1 R2: `sim_main.cpp:1443` | RESIDUE | `137ac73` (as R448-1 F2) | above |
| R449-1 R3: `CODE_QUALITY.md:612-616` | RESIDUE | the exact text, in the amended c10 patch | the patch's `CODE_QUALITY.md` hunk |
| R449-1 S1: other module-scope `$error` guards | SUGGESTION | not this lane's (151's scope, per the assignment) | `elab_bounds.sh` still grades `MEM_TIMEOUT_CYC_P`'s `$error` by name only |
| found here: the parent's shell-idiom gate (`check_sh_idiom.py`, docs workflow) fails on `protocol-processor/syn/yosys/run.sh` from `5c20350` on: 2 unquoted expansions (the census's `printf ... $missing` / `$stale`) and "top-heavy long script" (282 lines, 40% in functions) | (adoption blocker) | `cd08ca7`: the census and the elaboration loop are functions, called where they ran; the lists print through `sed 's/^/  /' <<<` | the parent's own scorer: 0 findings, 57% in functions; `check_sh_idiom.py` rc 0 at configurations b and c (it is rc 1 with the processor at `5c20350`, `b5e3b97` and `54f9411a`; rc 0 at `631eeb34` and `f4167536`, whose run.sh is 38 lines) |

### Item 1: the adoption patch leaves the parent green

`parent-adoption-c10-1269cdaf.patch` (this directory), amended: sha256
`55e62329f52e352bdd56b6d37bf2877aa952063f43221bb3f1d8583274ea34b9`, 7,133 bytes (round 1:
`6870d2ed...e304b`, 2,764 bytes). It applies after c8 then p2 at `1269cdaf` (`git apply
--check` clean, then `git apply`), and changes four files:

- `scripts/processor_yosys_tops.budget`, `scripts/xvlog.budget`: as round 1 (the six lines
  deleted; the xvlog ratchet banks `protocol_processor_top.sv`, line notes 557 and 383).
- `scripts/check_rtl_source_lists_selftest.py`, `_arms_processor_tops_live` (`:367-401`):
  the arm "the record is non-empty at this pin, so the refusal arms grade a live
  population" is replaced by two arms on a synthetic population drawn from the live pin,
  whatever the record holds. The live top `min(tops & declared)` (`KL_acmp_nvm_shadow`) is
  taken out of the array: with no record, the real `verdict()` must print `TOPS DRIFT`
  naming it and return 1, and with a synthetic record it must be debt (`([], [])`). Put
  back with that record left behind, `verdict()` must print `STALE RECORD` naming it and
  return 1. The `else` branch's count follows (3 -> 4). 49 -> 50 checks.
- `docs/development/CODE_QUALITY.md:612-617`: R449-1 R3's exact text.

Red proof, gate 3's self-test against planted defects in `scripts/check_rtl_source_lists.py`
(`$VALIDATION_STORAGE/c10-a518/r2/g3_selftest_mutants.sh`; each restored byte-identical):

| Defect planted | old self-test, six recorded (`1269cdaf`, pin `631eeb34`) | new self-test, six recorded | new self-test, record empty (c8 + p2 + c10) |
|---|---|---|---|
| none (control) | rc 0, 49/49 | rc 0, 50/50 | rc 0, 50/50 |
| `compare_tops` never reports stale | rc 1 (1 FAIL) | rc 1: the fixture arm and the new STALE RECORD arm | rc 1, the same 2 |
| `compare_tops` never reports unrecorded | rc 1 (5) | rc 1 (6, the new TOPS DRIFT arm among them) | rc 1 (6) |
| `verdict()` drops the STALE RECORD finding | **rc 0, missed** | rc 1: the new STALE RECORD arm alone | rc 1: the new STALE RECORD arm alone |
| `verdict()` drops the TOPS DRIFT finding | rc 1 (1) | rc 1 (2) | rc 1 (2) |
| the record is not credited (`unrecorded = missing`) | rc 1 (3) | rc 1 (4) | rc 1 (2) |

So the new arms pass with six recorded and with none, and they grade one defect the old
self-test missed even with its six.

(the gate tables follow under "Gates")

### Item 2: a layout-independent census

`1a5f555`, `syn/yosys/run.sh:152-186` at the head: sv2v runs before the census, and the
census reads `^module[[:space:]]+((automatic|static)[[:space:]]+)?NAME` from all.v, keeping
the last word. sv2v writes every module header as `module NAME` at the start of a line
however the source lays it out, and all.v is exactly what yosys reads. It keeps a lifetime
keyword (`module automatic NAME`), hence the optional word. At the head, 42 declared = 42 tops.

| Planted (scratch copy) | `54f9411a` | head |
|---|---|---|
| R449-1's `yosys_fault.sh ... newmod KL_r449_newmod`, unchanged (`module` alone, the name on the next line, an undeclared instance inside) | rc 0, 42 OK, parsed once (missed) | rc 1: `modules declared under hdl/ with no entry in the tops array: KL_r449_newmod` |
| the same header, the module added to `tops` | | rc 1: `YOSYS FAIL KL_c10_layout: ERROR: Module \c10_absent_module referenced in module \KL_c10_layout ...`, 43 tops, parsed 2 times |
| the same header, no fault, added to `tops` | | rc 0, 43 OK, parsed once |
| `module automatic` with the name on the next line | | rc 1, census names `KL_c10_layout` (the source-text grep would have named `automatic`) |
| a block comment between `module` and the name | | rc 1, census names `KL_c10_layout` |
| `drop KL_srp_top`, `bogus KL_r449_gone` (R449-1's probes) | rc 1, named | rc 1, named, same lines |

(`$VALIDATION_STORAGE/c10-a518/r2/item2/layout_probe.sh`.) R449-1's whole fault set (18 cases)
replayed at the head with its `yosys_fault.sh` and `fault_batch_one.sh`, unchanged: every
row's rc, OK count, parse count and named tops equal its `receipts/faults/SUMMARY.md`,
except `own-newmod` (rc 0 -> rc 1, named by the census).

### Item 3: the `MAX_PAYLOAD_P` bound derived

`6ba4659`, `hdl/packet_engine/KL_pp_nvm_port.sv:196-200`:
`localparam int unsigned MAXP_BOUND_C = (1 << $bits(dev_len_o)) - 1 - int'(HDR_LEN_C);`,
`if (MAX_PAYLOAD_P > MAXP_BOUND_C)`, and `$fatal(1, "KL_pp_nvm_port: MAX_PAYLOAD_P=%0d is above
%0d: %0d + it overflows dev_len_o", MAX_PAYLOAD_P, MAXP_BOUND_C, HDR_LEN_C)`. The banner
(`:112-114`) names `MAXP_BOUND_C` instead of the number. The comment above the guard lost
one line for the localparam, so the file keeps 643 lines and every line below `:192`
stays put (the citations of item 5 and the figures gate's ARMS table depend on that).
`hdl/` holds no `65527` any more; the bench (`elab_bounds.sh`, `Makefile` `FUZZ_MAXP`) keeps
it as the specification value. The message reads exactly as before at the shipped values.

- R449-1's `nvm_bound_probe.sh`, unchanged, at the head:
  `pristine elab_bounds rc=0 sv2v rc=0 yosys@65527 rc=0 yosys@65528 rc=1` (= its old
  `derived` row); `hdr10 elab_bounds rc=1 ... yosys@65527 rc=1` with `ELAB FAIL
  MAX_PAYLOAD_P=65527` and `MAX_PAYLOAD_P=65527 is above 65525: 10 + it overflows dev_len_o`:
  the bound follows the field. (`derived` can no longer be planted, its assertion fails
  because the shipped guard is already derived, so that row runs the pristine file.)
- No logic: sv2v + yosys `synth` of the port, `54f9411a` vs head, at `MAX_PAYLOAD_P` 1024
  and 65527: the netlists are identical but for the name of one unused sv2v cast wire
  (which embeds the file name and line), and `stat` is identical.
- Vivado 2026.1 (`$VALIDATION_STORAGE/c10-a518/r2/viv/`; no other job of this lane ran, the host's other
  tenants did), on a `git archive` of `cd08ca7`: `synth_design -rtl` of the port elaborates at 1024 and 65527 and refuses 65528
  with `ERROR: [Synth 8-6058] Synth Error: KL_pp_nvm_port: MAX_PAYLOAD_P=65528 is above
  65527: 8 + it overflows dev_len_o [.../KL_pp_nvm_port.sv:198]`. The OOC run
  (`syn/ooc/protocol_processor_ooc.tcl` + `write_verilog -mode design`, 185 s): netlist
  19,508,014 bytes, sha256 without its `// Date` line
  `4baf5a8ceff9979470e908d87527cddc87b1eb125b0282f3839b0f0411a4e200`, the base's and round
  1's; `util.rpt` and `util_hier.rpt` bodies identical to round 1's; 7 `Synth 8-6901`. So
  the out-of-context cost table above holds at the round-2 head.

### Item 4: the bench grades the severity

`522d49a`, `tb/nvm_port/elab_bounds.sh`:
- `refused()` (`:56-76`) takes the classes the refusal line may carry. `MAX_PAYLOAD_P`'s must
  be `%Warning-USERFATAL` or `%Error` (`:114`); the line that names the parameter and the
  bound is the one graded. `MEM_TIMEOUT_CYC_P` keeps "any warning or error" (`:112`): its
  `$error` guard is 151's scope.
- `yosys_at` and `fatal_in_yosys` (`:78-109`, called at `:115`): with sv2v and yosys on PATH, yosys must
  elaborate 65527 and stop at 65528 on the guard's `$finish`; without them it prints
  `YOSYS SKIP` and the class check stands alone.
- Docs: `tb/nvm_port/README.md:23-26`, `tb/nvm_port/Makefile:64-67`,
  `docs/architecture/09_verification.md:351`.

Green: 4 `ELAB OK`, 6 `GUARD OK` (the class printed), `YOSYS OK MAX_PAYLOAD_P=65527
elaborates, MAX_PAYLOAD_P=65528 stops at the guard's $finish`, rc 0, 1 s.

Mutants (`$VALIDATION_STORAGE/c10-a518/r2/item4/mutants.sh`, scratch copies, pinned Verilator):

| Mutant | head bench | `54f9411a` bench |
|---|---|---|
| `$fatal(1, ...)` -> `$error(...)` | rc 1: `GUARD FAIL MAX_PAYLOAD_P=65528 refused as %Warning-USERERROR, not as %(Warning-USERFATAL\|Error)` (x3) and `YOSYS FAIL MAX_PAYLOAD_P=65528 elaborated; the guard is not a $fatal` | rc 0, 6 GUARD OK (missed) |
| `-> $warning(...)` | rc 1: `refused as %Warning-USERWARN` (x3), `YOSYS FAIL` | rc 0 (missed) |
| `$error`, sv2v and yosys off PATH | rc 1: the three class failures, `YOSYS SKIP` | |
| guard deleted | rc 1: `GUARD FAIL ... elaborated` and two unnamed, `YOSYS FAIL` | |
| bound + 1 (no `- 1`) | rc 1: `GUARD FAIL MAX_PAYLOAD_P=65528 elaborated`, `YOSYS FAIL` | |
| `>=` | rc 1: `ELAB FAIL MAX_PAYLOAD_P=65527`, `YOSYS FAIL MAX_PAYLOAD_P=65527 did not elaborate` | |
| message without the bound | rc 1: the three `failed without naming the parameter and its bound` | |
| the precedent's `initial` placement | rc 1: `GUARD FAIL MAX_PAYLOAD_P=65528 elaborated` (+2) | |
| `HDR_LEN_C` = 10 | rc 1: `ELAB FAIL MAX_PAYLOAD_P=65527`, three refusals not naming 65527, `YOSYS FAIL ... 65527 did not elaborate` | |

R449-1's probe, unchanged: `err elab_bounds rc=1`, `warn elab_bounds rc=1` (round 1: 0, 0).

### Item 5: citations and wording

`137ac73`. Every line citation into `KL_pp_nvm_port.sv` in the tree was listed and checked
against the text it names; the full set the guard's ten lines moved, over both rounds:

| Site (head) | Round 1 (`54f9411`) | Round 2 (`137ac73`) | Names |
|---|---|---|---|
| `tb/nvm_port/README.md:226` | `:234-245` -> `:244-255` | | `dev_cmd_owned_w` |
| `tb/nvm_port/README.md:1135`, `sim_main.cpp:1441`, `measure_figures.py:117` | `:340-344` -> `:350-354` | | the sticky `done_seen_r` set |
| `tb/nvm_port/sim_main.cpp:1328` | `:436-439` -> `:446-449` | | the `S_WWAIT` arm |
| `measure_figures.py` ARMS table | twelve lines + 10 | | the `if (dev_err_i)` arms |
| `tb/nvm_port/sim_main.cpp:1443` | missed | `:234-245` -> `:244-255` | `dev_cmd_owned_w` |
| `tb/nvm_port/README.md:407` | missed | `` `:366` `` -> `` `:376` `` | `state_r <= S_WEREQ;` |
| `tb/nvm_port/README.md:413` | missed | `` `:380` `` -> `` `:390` `` | `state_r <= S_WEWAIT;` |
| `tb/nvm_port/README.md:106` (pre-existing, R448-1 S2) | | `protocol_processor_top.sv:2714` -> `:2726` | the `KL_acmp_nvm_shadow #(` instance |

Unmoved and checked: `sim_main.cpp:1591` `:33-34` (above the guard); the shadow citations
at `README.md:102-104` (`KL_acmp_nvm_shadow.sv:482-483`, `:775`, `:391-395`, `:90-92`) and
`KL_aecp_nvm_writer.sv:482-485`. `syn/yosys/run.sh:9-10`: R449-1 R1's exact text. Item 3
keeps every line of the port in place, so no citation moves again.

### Gates

Processor, pinned Verilator 5.050, in this checkout (logs and rc files under
`$VALIDATION_STORAGE/c10-a518/r2/run/`). The suites, figures and campaigns ran at `137ac73`
concurrently (hence the longer wall times); `cd08ca7` changes only `syn/yosys/run.sh`,
which none of them builds. The Yosys gate rows are at `cd08ca7`'s content.

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | 33 suites, **1,020,253** checks, 0 failing (round 1's tally exactly; `pp_top` 9,222, `nvm_port` 1,219); 1,276 s |
| `./scripts/lint_hdl.sh` | 0 | 41 of 41 `LINT OK` |
| `make check` | 0 | 41 mermaid + 18 wavedrom, 1,105 links, 115 REQ rows, 17 GAP, 94 rows 0 untested, 28 parameters |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `./syn/yosys/run.sh` (jemalloc; `YOSYS_MALLOC=none`) | 0; 0 | 42 `YOSYS OK`, `all.v parsed 1 time(s)`, `YOSYS XILINX OK KL_aecp_engine`; verdict lines identical between the two and to `137ac73`'s; 38 s, 46 s |
| `./syn/yosys/run.sh --selftest-alloc` | 0 | PASS |
| `make -C tb/nvm_port figures` | 0 | all measured figures agree with the tree (160 builds); 1,302 s |
| `tb/nvm_port/elab_bounds.sh` (also in `make`) | 0 | 4 ELAB OK, 6 GUARD OK, YOSYS OK |
| `aecp_dispatch_mutants.py --jobs 4` | 0 | 4 controls PASS, 40 of 40 KILLED, 44/44; 402 s |
| `aecp_mutants.py --jobs 4` | 0 | 5 controls PASS, 55 of 55 KILLED, 60/60; 602 s |
| `tb/srp_top/mutants.py --jobs 4` | 0 | 90 checks, 0 FAIL (11 controls, 78 KILLED); 791 s |
| `tb/maap/mutants.py --jobs 4` | 0 | 32 checks, 0 FAIL; 102 s |
| `tb/adp_engine/mutants.py --jobs 4` | 0 | 32 checks, 0 FAIL; 150 s |
| R449-1 `yosys_fault.sh` (18 cases), `nvm_bound_probe.sh`; R448-1/R449-1 gate-3 self-test | as stated | see items 1-4 |

Parent consumers, in a fresh scratch parent at `$VALIDATION_STORAGE/c10-a518/r2/parent` (never
the trusted checkout): a `git archive` of `1269cdaf` committed into a new repository (tree
`84537179...` = the trusted checkout's, 984 index entries, gitlinks added), gptp-processor
`5dce647a` and verilog-axis `48ff7a7e` registered at their pins, protocol-processor a clone
of this branch, `external` uninitialised. Three configurations, `git submodule status` and
porcelain clean before and after each:

- a: dev `1269cdaf` as it is, processor pin `631eeb34`.
- b: + `parent-adoption-c8-cdf49d1a.patch` then `parent-adoption-p2-cdf49d1a.patch` (each
  after a clean `git apply --check`), processor gitlink `cd08ca7`.
- c: + the amended `parent-adoption-c10-1269cdaf.patch` (clean `--check`).

The 16, and item 1's self-tests:

| # | Command | b (c8 + p2) | c (+ c10) | Result at c |
|---:|---|---:|---:|---|
| 1 | `scripts/check_cpp_idiom.py` | 0 | 0 | 169 translation units; long function 0 <= 0, build without warnings 0 <= 0 |
| 2 | `scripts/check_py_idiom.py` | 0 | 0 | 301 modules; long function 9 <= 9, long module 10 <= 10, over-long line 0 <= 0 (the self-test file is among them) |
| 3 | `scripts/check_rtl_source_lists.py` | **1** | 0 | b: six `STALE RECORD`; c: `protocol-processor 42/42 tops, 0 recorded` |
| 3s | `scripts/check_rtl_source_lists.py --selftest` | **1** | 0 | b: 47 of 49 (the live arms see six stale records); c: **50 of 50** |
| 4 | `scripts/pp_srcs.py --check --selftest` | 0 | 0 | 46 sources derived, self-test passed (reads both budgets) |
| 5 | `scripts/check_port_contracts.py` | 0 | 0 | protocol-processor 1,756 ports (unchanged) |
| 6 | `scripts/measure_naming.py --check` | 0 | 0 | 96 candidates, all recorded |
| 7 | `scripts/measure_test_evidence.py --check` | 0 | 0 | 72 <= 77, 10 <= 10, 0 <= 0, 3 <= 3 |
| 8 | `scripts/docs_check.py` | 0 | 0 | 0 findings over 185 md + 956 files (reads all four patched files) |
| 9 | `scripts/xvlog_gate.py --check` (xvlog on PATH, alone) | **1** | 0 | b: `BANK IT ... protocol_processor_top.sv\|VRFC 10-3380\|srp_class_a_prio_w no longer occurs`; c: `PASS (3 finding(s) == ratchet; 0 hdl/, 3 pinned processors)`, 142 s |
| 9s | `scripts/xvlog_gate.py --selftest` (xvlog on PATH) | | 0 | PASS; without xvlog it is rc 1 at a, b and c alike ("the planted use-before-declaration produced no matching finding") |
| 10 | `sw/builder/test_builder.py` | | 0 | ALL GATES PASS EXCEPT 1 NOT RUN (its gate 11 needs a local board build tree, as in round 1); 1,184 s |
| 11 | `scripts/lint_rtl.py --check` | 0 | 0 | 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j16` | | 0 | 606, 646, 606, 311 checks, 0 failures; 245 s |
| 13, 14 | `make -C tb/verilator/nvm_cosim lint`, `quick` | | 0, 0 | lint pass (the port's new localparam under the parent's flags); 315 of 315 |
| 15 | `make -C tb/verilator/milan_dp -j16 VERILATOR_JOBS=3` | | 0 | 9 `RESULT: PASS`, 0 FAIL; 1,588 s |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | | 0 | 0 failures; 5 of 5 leg-defect arms; 371 s |
| s | `scripts/check_entity_shape.py --self-test` | 0 | 0 | PASS (reads both budgets) |
| s | `scripts/check_todo_ownership.py --selftest` | 0 | 0 | 45 of 45 (reads both budgets) |

Gates 10 and 12-16 ran at c only: they read none of the four files the c10 patch changes
(it touches two budgets, a self-test and a document), so b's result is c's.

"Every other parent self-test that reads either budget" was found by tracing, not by
grepping. Every python command in the parent's workflows and `run_all_suites.sh`
preflights (91 commands) ran under `strace -f -e open,openat,execve` at a, b and c, and the
files each process tree opened were recorded (`$VALIDATION_STORAGE/c10-a518/r2/census-{a,b,c}/`).
The self-tests that open `processor_yosys_tops.budget` or `xvlog.budget` are
`check_rtl_source_lists.py --selftest`, `pp_srcs.py --check --selftest`,
`check_entity_shape.py --self-test`, `check_todo_ownership.py --selftest` and
`xvlog_gate.py --selftest`: all rc 0 at c (the last with xvlog). The other commands that
open a patched file are `check_baremetal_only.py --check`, `check_hygiene.py --check/--selftest`,
`check_py_idiom.py` and its self-test, `measure_test_evidence.py --check/--selftest`,
`check_feature_status.py`, `check_gptp_docs.py`, `check_archive.py`, `check_doc_paths.py`
and `gen_toc.py`. With the parent's pinned renderer installed,
`check_em_dash.py --base cfg-b` (0 findings over the patch's 6 added Markdown lines),
`check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors` are rc 0 at c.

Of the 91, the ones not rc 0 at c, none caused by this lane:

| Command | a | b | c | Cause |
|---|---:|---:|---:|---|
| `scripts/check_submodule_docs.py` | 0 | 1 | 1 | the pin bump: "protocol-processor: documented pin differs from Git", and the submodule diagram stale |
| `docs/diagrams/submodule_boundaries.gen.py --check`, `--selftest` | 0 | 1 | 1 | the same diagram, generated from the pin |
| `syn/yosys/ooc_selftest.py` | 0 | 2 | 2 | the pin bump: "rom_digests.tsv has no ucode.hex row for its owning processor pin" (recorded with `./ooc.sh --record-rom-digests`) |
| `scripts/check_doc_paths.py` | 0 | 1 | 1 | the p2 patch: its `docs/design/SAVED_STATE_MATERIALIZATION.md` row W13 cites `tb/acmp_nvm` and `tb/nvm_port` without the `protocol-processor/` prefix |
| `scripts/xvlog_gate.py --selftest` | 1 | 1 | 1 | no xvlog in the census; rc 0 with xvlog (above) |
| `scripts/test_suite_cancellation.py` | 1 | 0 | 1 | ptrace: "owned descendants remain" under `strace -f`; rc 0 at c without strace |

The first three need the adopted SHA (this PR's merge commit, not `cd08ca7`), so they
belong to the adoption commit, not to a patch prepared now. The fourth is p2's, which this
lane does not edit. `check_sh_idiom.py`: rc 0 at a, b and c (it was rc 1 with the processor at
`54f9411a`, see the finding table).
