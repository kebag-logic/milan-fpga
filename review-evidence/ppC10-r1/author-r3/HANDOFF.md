# [A518] Lane C10 (tooling): HANDOFF

Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
Branch: `c10-tooling`, from `main` `f4167536`
Issues: #25 (item 1), #17 (item 2), #22 (item 3), #37 (item 4). Supersedes PR #26.

Status: round 3b DONE at head `39298e03aa53d5f82c7485b8d12d2b69a47b0d55`, the merge of `main` `c4cb84ff` (see "Round 3b" at the end; not pushed; REVIEW READY posted on #25, comment 5973148371). Round 3 DONE at head `b6f17f22426fb6362c41a2faf839735c455a8651` (see "Round 3" at the end; not pushed; REVIEW READY posted, comment 5971633423). Round 2 DONE at head `cd08ca7b3d962ab040d8aaa023c57e7b0e010a6d` (see "Round 2" at the end; not pushed; REVIEW READY posted, comment 5970441890). Round 1: DONE at head `54f9411ab9a4b4aea58393f7fa1303ddcc96ee3c`; TAKEN posted on #25 (comment 5967294275); REVIEW READY posted with the head (comment 5968833276); pushed by the manager as PR #149, reviewed NEGATIVE by R448-1 and R449-1.

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

Census (from the branch, `run.sh:152-173` at round 1): fails when a declared module has no
top, or a top names no declared module. 42 declared, 42 tops. Where the declared modules
come from changed twice: round 2 read `^module NAME` from all.v, and round 3 (`b6f17f2`,
`run.sh:157-188`, `:237`, `:269-271`) takes yosys's own list of the modules it parsed. See
"Round 3".

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

## Round 3

Assignment: #25 comment 5970977905, answering R448-2 (5970948940) and R449-2 (5970973855),
both NEGATIVE at `cd08ca7b` on one shared MINOR (F1). New one-line commits on top of
`cd08ca7b`; no rebase, no amend, no push. Tools as round 2, plus yosys 0.33 (Ubuntu
24.04's package, the hosted `portability` job's) in a scratch container image, used only
to run the gate the way that job does.

Status: DONE at head `b6f17f22426fb6362c41a2faf839735c455a8651` (not pushed). REVIEW READY posted on #25 with the head (comment 5971633423).

Commits after `cd08ca7b`:

| Commit | Item | What |
|---|---|---|
| `b6f17f2` | 1 | the census takes yosys's own list of the modules it parsed from all.v; `parse_site` names a module past attribute instances and a lifetime keyword |

### Finding-by-finding table

| Finding | Severity | Resolution | Evidence |
|---|---|---|---|
| R448-2 F1 = R449-2 F1: an attributed header (`(* ... *) module X`, same line or the line before) escapes the census; `parse_site` names `module automatic` and attributed headers wrongly | MINOR | `b6f17f2`: the declared set is yosys's own `select -list =*` of the `read_verilog -defer` design it elaborates; no pattern over text. `parse_site`, which runs only when yosys has no list (a failed parse), skips attribute instances and a lifetime keyword | R448-2's `run_census_cases.sh`: `c-attr-same`, `c-attr-own` rc 1 named; `c-attr-own-top-clean` rc 0; `c-attr-own-top` rc 1 `YOSYS FAIL KL_r448_attro`. R448-2's `parse_site_unit.sh` names `KL_auto` and `KL_attr`. R449-2's `census_probe.sh`: every form red and named |
| R449-2 S1: the parent's `check_rtl_source_lists.py` census still reads `.sv` text | SUGGESTION | open; the parent's, out of this lane's scope (item 2) | below |
| R449-2 S2: `elab_bounds.sh`'s yosys leg never runs hosted | SUGGESTION | open (item 2) | below |

### Item 1: a census that does not depend on header layout

`b6f17f2`, `syn/yosys/run.sh`:

- **Where the list comes from** (`:237`, `gate_script`): after `read_verilog -defer all.v`,
  the same yosys writes `tee -q -o declared.txt select -list =*`, its own list of the
  modules it parsed (each `$abstract\NAME` under `-defer`), before `design -save parsed`.
  So yosys lists deferred modules without elaborating them, and the assignment's fallback
  (a text extraction for the census) is not needed. `=*` includes boxes: a
  `(* blackbox *)` or `(* whitebox *)` module is listed. `select -list` and not `ls`:
  yosys 0.33's `ls =*` drops boxes (5 of 7 modules in a probe file), while 0.66's lists
  them; `select -list =*` lists all 7 on both. `select -write` writes an empty file on
  0.66, so it is not used.
- **The census** (`:157-188`): `declared` is that list with the `$abstract\` prefix
  removed (`:172`); an absent or empty list is refused by name (`:171`). The two refusals
  and their messages are unchanged.
- **When it runs** (`:269-271`, in `elaborate_tops`): after the first yosys run, once that
  run's first top has begun (so the parse passed and the list is complete), and before any
  verdict line. A census failure therefore prints exactly the old lines and exits 1 with no
  `YOSYS OK` and no `parsed` line, as before; the one difference in output is that the
  `yosys allocator:` line now comes first. The cost moved: a census failure used to stop
  before yosys, and now the first run's elaboration has happened by then (about 10 s; a
  red gate only). A green gate is unchanged: one parse, then the XILINX regression.
- **Scope, stated in the comment** (`:157-168`): a module is counted when yosys parses it
  from all.v. A module in an inactive `` `ifdef `` branch is not counted: sv2v drops it,
  so yosys never sees it (round 1's `.sv`-text census counted it; round 2's and this one
  do not). A module yosys cannot parse fails the parse instead, which names it: yosys 0.33
  and 0.66 both reject `module automatic` (`syntax error, unexpected TOK_AUTOMATIC`).
- **`parse_site`** (`:244-260`): a failed parse leaves yosys no list, so this is the one
  place the gate reads all.v's text. It takes the last header at or above the cited line
  that is not closed above it: leading `(* ... *)` instances are stripped, `module` or
  `macromodule` is the first word, a lifetime keyword (`automatic`, `static`) is skipped, an
  escaped name keeps its characters, and an `endmodule` above the cited line clears the
  name (a stray line between modules names none). gawk and mawk (Ubuntu's `awk`) give the
  same answers.

Red proofs and probes. Scripts and logs: `$VALIDATION_STORAGE/c10-a518/r3/` (`p448/`, `p449/`:
the reviewers' scripts from the review-evidence branch, byte-identical, run unchanged;
`item1/`: this lane's; `out/`: logs and rc files). Trees: `git archive` copies of the head,
`cd08ca7` and `54f9411`.

R448-2's `run_census_cases.sh` and `census_cases.txt`, unchanged ("was" = R448-2's receipts
at `cd08ca7`; logs compared after normalising all.v line numbers and `$paramod` names):

| Case | was | head | Head result |
|---|---:|---:|---|
| `c-attr-same` (`(* keep_hierarchy = "yes" *) module X`, fault inside) | 0 | **1** | `modules declared under hdl/ with no entry in the tops array: KL_r448_attrs` |
| `c-attr-own` (attribute on the line before) | 0 | **1** | the same, `KL_r448_attro` |
| `c-attr-own-top-clean` (no fault, in `tops`) | 1 | **0** | 43 `YOSYS OK`, parsed once, XILINX OK |
| `c-attr-own-top` (fault, in `tops`) | 1 | 1 | `YOSYS FAIL KL_r448_attro: ERROR: Module \r448_absent_module referenced in module \KL_r448_attro ...` (was: "no longer exist") |
| `c-auto-split` (`module automatic` / name on the next line) | 1 | 1 | `YOSYS FAIL all.v in module KL_r448_auto: all.v:20749: ERROR: syntax error, unexpected TOK_AUTOMATIC, expecting TOK_ID`, then every top `not elaborated` (was: the census named it). Same rc, same module named; the line now gives the real blocker, because a `tops` entry could not make it pass |
| `c-plain`, `c-split`, `c-split-top`, `c-cmt-block`, `c-cmt-line`, `c-macro` | 1 each | 1 each | identical logs |
| `c-ifdef` | 0 | 0 | identical log (not counted, see scope) |
| `r1-split`, `r1-attr-same`, `r1-attr-own`, `r1-ifdef` (tree `54f9411`) | 0, 0, 1, 1 | same | identical logs |

R449-2's `census_probe.sh` (via `census_batch_one.sh`, its `jobs.txt`):

| Form | was | head | Head result |
|---|---:|---:|---|
| `attr` | 0 | **1** | census names `KL_r449_attr` |
| `attrline` | 0 | **1** | census names `KL_r449_attrline` |
| `attr top` | 1 ("no longer exist") | 1 | `YOSYS FAIL KL_r449_attr: ERROR: Module \r449_absent_module referenced in module \KL_r449_attr ...`, 43 tops, parsed 2 times |
| `allvauto` | 1, "in module automatic" | 1 | `YOSYS FAIL all.v in module KL_r449_allvauto: all.v:20749: ERROR: syntax error, unexpected TOK_AUTOMATIC ...` |
| `auto` | 1, census | 1 | `YOSYS FAIL all.v in module KL_r449_auto: ...` (the parse names it, as `c-auto-split`) |
| `split`, `cmtblock`, `cmtline`, `macro` | 1 each | 1 each | census names each |
| `split top` | 1 | 1 | `YOSYS FAIL KL_r449_split: ...` |
| `r1-c-attr` (tree `54f9411`) | 0 | 0 | unchanged (round 1's tree) |

`parse_site`:

- R448-2's `parse_site_unit.sh` (extracts `parse_site()` verbatim): `KL_first`, `KL_auto`,
  `KL_attr` at the head, with gawk and inside Ubuntu 24.04 (mawk); `KL_first`,
  `automatic`, `automatic` at `cd08ca7`.
- `item1/parse_site_more.sh`: every line of sv2v's lowering of fourteen header forms
  (plain, split, `automatic` split, `static`, block and line comments, `macromodule`, an
  attribute on the same line and on the line before, three attribute instances with a
  `*` in a string and `automatic`, `(* blackbox *)`, a `$` in the name, an escaped
  name), checked against the modules in source order counted by `module`/`endmodule`
  words: head 44 of 44 lines right; `cd08ca7` 24 wrong (`automatic`, `static`, the
  previous module, `KL_f_dollar`). A stray line between two modules names none; a cited
  line with no `all.v:N` names none.

New rows (`item1/probe.sh`, `item1/cases.txt`):

| Case | head |
|---|---|
| `(* blackbox *) module KL_c10_bb` with a fault inside, not in `tops` | rc 1: the census names `KL_c10_bb` |
| the same, in `tops` | rc 0: 43 OK (a box's body is not elaborated; yosys 0.33 and 0.66 both elaborate a box as a top) |
| `(* keep_hierarchy = "yes" *) module` on one line, no fault, in `tops` | rc 0: 43 OK, parsed once, XILINX OK |
| R448-2's `allv-syntax KL_srp_top` | rc 1: `YOSYS FAIL all.v in module KL_srp_top: ...` |

Mutants of `b6f17f2`'s run.sh (`item1/mutate.py`), each against the probe that must catch
it; every one is killed:

| Mutant | Probe | Head | Mutant |
|---|---|---|---|
| `select -list *` (boxes not listed) | the blackbox module, not in `tops` | rc 1, named | rc 0, 42 OK (missed) |
| the census call removed | attribute same line; plain header | rc 1, named | rc 0, rc 0 |
| round 2's census (`^module` over all.v) | attribute same line; attribute line before | rc 1, named | rc 0, rc 0 |
| round 2's `parse_site` | `module automatic` / name | names `KL_c10_auto` | names `automatic` |
| the `select -list` line removed | the clean tree | rc 0 | rc 1: `yosys parsed all.v but listed no module` |
| the census run whether or not the parse passed | `allv-syntax KL_srp_top` | names `KL_srp_top` | `yosys parsed all.v but listed no module`: the module is not named |

Two equivalent edits survive and are not counted: running the census after every run
(each run lists the same all.v), and dropping the empty-list refusal (`:171`: an empty
list then makes every top "no longer exist", still rc 1).

Yosys 0.33, the hosted `portability` job's version (Ubuntu 24.04 container: apt yosys
0.33, sv2v 0.0.13, mawk, no jemalloc, so the system allocator), `item1/cases033.txt`:

| Case | rc | Result |
|---|---:|---|
| the head, clean | 0 | 42 OK, `all.v parsed 1 time(s)`, `YOSYS XILINX OK` |
| attribute same line; attribute line before | 1, 1 | the census names each |
| attribute line before, clean, in `tops` | 0 | 43 OK, parsed once, XILINX OK |
| attribute line before, fault, in `tops` | 1 | `YOSYS FAIL KL_c10_attro: ...` |
| `(* blackbox *)`, not in `tops` | 1 | the census names it |
| `module automatic` / name | 1 | `YOSYS FAIL all.v in module KL_c10_auto: ... unexpected TOK_AUTOMATIC ...` |
| `allv-syntax KL_srp_top` | 1 | `YOSYS FAIL all.v in module KL_srp_top: ...` |

Unchanged probes:

- R449-1's 21 fault cases (`yosys_fault.sh`, `fault_batch_one.sh`, R449-2's `jobs.txt`):
  summarised by R449-2's `summarize_faults.sh`, the table equals R449-2's
  `receipts/faults/SUMMARY.md` after its own normalisation (all.v line numbers,
  `$paramod` names), every row: rc, OK count, parse count, first four FAIL lines.
- R448-2's 24 gate cases (`run_gate_cases.sh`, `gate_cases.txt`; the `h-malloc-emptyfile`
  row points at a local non-library file instead of the reviewer's packet path), plus the
  fake exit-0 yosys and `fatal KL_pp_rx_slots`: every rc equal to R448-2's receipts and
  20 + 2 logs identical. Four differ, verdicts unchanged: `h-drop-srp_top` and
  `h-add-bogus` print `yosys allocator: ...` before the census message (the census now
  runs after the parse); `h-inherited-preload-none` shows 7 fewer loader complaints about
  the inherited `LD_PRELOAD` (the census's processes now run after the allocator step
  unsets it); `h-malloc-emptyfile` differs only in the probe file's path.

Wall time, end to end (`./syn/yosys/run.sh`), three interleaved rounds, nothing else of
this lane running (the host's other tenants were: load average 27-34 on 16 CPUs),
`timing/timing.txt`:

| Revision | Rounds (s) | Median |
|---|---|---:|
| `cd08ca7` (round 2), jemalloc | 34.96, 34.99, 38.31 | 34.99 s |
| **`b6f17f2`, jemalloc** | 36.18, 36.09, 57.28 | **36.18 s** |
| `b6f17f2`, `YOSYS_MALLOC=none` | 50.05, 49.86, 50.48 | 50.05 s |

All nine runs: `all.v parsed 1 time(s)` and the same verdict lines (one md5). The list
costs one `select -list` on the parsed design (the parse plus the list take 0.23 s
alone). The run.sh comment's figures (48.12 s -> 35.97 s, -25.2%) were measured in
round 1; this round's pair is 50.05 s -> 36.18 s (-27.7%) on a busier host, so the
comment stands.

Docs: the run.sh comments are the only prose about the census in the tree; they now
state the scope above (`:7-10`, `:157-168`, `:222`, `:232-234`, `:244-248`, `:269-270`).
The PR body's §1 census bullet, its parse-failure sentence and its red-proof table are
corrected (the attributed, `automatic`, blackbox and `ifdef` rows).

### Item 2: suggestions left open

- **R449-2 S1** (open, the parent's): the parent's `check_rtl_source_lists.py`
  (`declared_modules()`, `^\s*module\s+NAME` over each `.sv`) still reads text. Run on
  the same forms (its own function, in the scratch parent), it agrees with this census on
  a plain header, a split header and an attribute on the line before. It does not count an
  attribute on the header line, a comment between `module` and the name, `macromodule` or
  `(* blackbox *)` (this census counts all four; the parent never refuses a top it does not
  count, so listing them passes both). It names `module automatic X` as `automatic` (this
  gate fails the parse and names `X`). It counts a module in an inactive `` `ifdef `` (this
  census does not, and refuses it in `tops`; a parent budget record would let both pass).
  No module of this tree has any of these forms today (gate 3: 42/42, 0 recorded). A parent
  follow-up could read the same source of truth. Out of this lane's scope.
- **R449-2 S2** (open): `tb/nvm_port/elab_bounds.sh`'s yosys leg prints `YOSYS SKIP`
  hosted, because the `suites` job installs no yosys or sv2v; only `portability` does,
  and it does not run `tb/nvm_port`. The class check alone still kills `$error` and
  `$warning`. Running `elab_bounds.sh` in `portability` would exercise the yosys leg on
  yosys 0.33; the workflow is unchanged here.

### Gates

Processor, pinned Verilator 5.050, in this checkout at `b6f17f2` (logs and rc files under
`$VALIDATION_STORAGE/c10-a518/r3/run/` and `timing/`):

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | 33 suites, **1,020,253** checks, 0 failing (round 2's tally exactly; `pp_top` 9,222, `nvm_port` 1,219, whose `make` runs `elab_bounds.sh`); 915 s |
| `./scripts/lint_hdl.sh` | 0 | 41 of 41 `LINT OK` |
| `make check` | 0 | 41 mermaid + 18 wavedrom, 1,105 links, 115 REQ rows, 17 GAP, 94 rows 0 untested, 28 parameters |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `./syn/yosys/run.sh`, three times with jemalloc and three with `YOSYS_MALLOC=none` | 0 x6 | 42 `YOSYS OK`, `all.v parsed 1 time(s)`, `YOSYS XILINX OK KL_aecp_engine`; verdict lines identical across the six and to `cd08ca7`'s three |
| `./syn/yosys/run.sh --selftest-alloc` | 0 | PASS |
| `./syn/yosys/run.sh` under yosys 0.33 (Ubuntu 24.04 container, system allocator) | 0 | 42 OK, parsed once, XILINX OK |

Not rerun this round, because `b6f17f2` changes only `syn/yosys/run.sh`, which none of
them builds: `make -C tb/nvm_port figures` and the five mutation campaigns (round 2, at
`137ac73`, all rc 0). The checkout is clean after every run (`git status --porcelain`
empty).

Parent consumers: round 2's scratch parent at `$VALIDATION_STORAGE/c10-a518/r2/parent` (never
the trusted checkout). Its ignored build products were removed first (`git clean -ffdX`,
parent and processor), the processor clone was moved to `b6f17f2`, and the gitlink was
recorded in a new scratch commit `b46f3dd`. Its tree equals a fresh worktree of `1269cdaf`
with `parent-adoption-c8-cdf49d1a.patch`, `parent-adoption-p2-cdf49d1a.patch` and
`parent-adoption-c10-1269cdaf.patch` (this directory, sha256 `aa5a88eb...`, `590f791d...`,
`55e62329...`, unchanged since round 2) each applied after a clean `git apply --check`,
apart from the processor gitlink. Porcelain is clean before and after. Logs are under
`$VALIDATION_STORAGE/c10-a518/r3/pg/`.

| # | Command | rc | Result |
|---:|---|---:|---|
| 1 | `scripts/check_cpp_idiom.py` | 0 | long function 0 <= 0, build without warnings 0 <= 0 |
| 2 | `scripts/check_py_idiom.py` | 0 | every ratchet held |
| 3 | `scripts/check_rtl_source_lists.py` | 0 | `protocol-processor 42/42 tops, 0 recorded` |
| 3s | `scripts/check_rtl_source_lists.py --selftest` | 0 | 50 of 50 |
| 4 | `scripts/pp_srcs.py --check --selftest` | 0 | sources derived, self-test passed |
| 5 | `scripts/check_port_contracts.py` | 0 | protocol-processor 1,756 ports, 111 <= 111 undocumented |
| 6 | `scripts/measure_naming.py --check` | 0 | 96 candidates, all recorded |
| 7 | `scripts/measure_test_evidence.py --check` | 0 | 72 <= 77, 10 <= 10, 0 <= 0, 3 <= 3 |
| 8 | `scripts/docs_check.py` | 0 | 0 findings over 185 md + 956 files |
| 9 | `scripts/xvlog_gate.py --check` (xvlog on PATH, alone, last) | 0 | `PASS (3 finding(s) == ratchet; 0 hdl/, 3 pinned processors)`; 145 s |
| 9s | `scripts/xvlog_gate.py --selftest` (alone) | 0 | PASS |
| 10 | `sw/builder/test_builder.py` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11 needs a local board build tree, as in rounds 1 and 2); 1,193 s |
| 11 | `scripts/lint_rtl.py --check` | 0 | 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j16` | 0 | 606, 646, 606, 311 checks, 0 failures; 240 s |
| 13, 14 | `make -C tb/verilator/nvm_cosim lint`, `quick` | 0, 0 | lint pass; `RESULT: PASS` |
| 15 | `make -C tb/verilator/milan_dp -j16 VERILATOR_JOBS=3` | 0 | 9 `RESULT: PASS`, 0 FAIL; 1,577 s |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | 0 | 0 failures; 5 of 5 leg-defect arms; 364 s |
| 17 | `scripts/check_sh_idiom.py` | 0 | unquoted expansion 3 <= 3, top-heavy long script 0 <= 0. The parent's own `scan()` on `run.sh` alone: 0 findings, 306 lines, 56% inside a function (`cd08ca7`: 290 lines, 57%) |

The other parent commands that open `protocol-processor/syn/yosys/run.sh` (round 2's
strace census) and the budget readers, all rc 0: `check_sh_idiom.py --selftest` (48/48),
`check_hygiene.py --check` and `--selftest` (35/35), `check_todo_ownership.py` and
`--selftest` (45/45), `measure_fail_fast.py --check` and `--selftest` (106/106),
`check_entity_shape.py --self-test` (219 checks, PASS).

Gates 10 and 12-16 ran concurrently with the processor suites (12, 13, 14 and 16 beside
10, then 15 beside 10). Gate 9 ran alone after everything else of this lane had finished.

## Round 3b

Assignment: #25 comment 5972322274: merge only, before the round-3 reviews. Processor
`main` moved to `c4cb84ff` (PR #150, lane P1). A `--no-ff` merge commit on top of
`b6f17f22`, plus one-line follow-up commits; no rebase, no amend, no push.

Status: DONE at head `39298e03aa53d5f82c7485b8d12d2b69a47b0d55` (the merge commit; no
follow-up commit was needed: no citation, count or record moved). Not pushed. REVIEW READY
posted on #25 with the head (comment 5973148371). No STOP condition met: the merge changes no logic, port or
parameter meaning of its own: `git diff c4cb84ff 39298e03 -- hdl` (two files, the top and
the port) has exactly the changed lines of this lane's own `f4167536..b6f17f22` RTL diff,
and `git diff b6f17f22 39298e03 -- hdl` exactly those of P1's (sorted `-U0` lines
compared).

### Item 1: the merge

`39298e03` (`git merge --no-ff origin/main`, parents `b6f17f22` and `c4cb84ff`). `main`
gained 15 commits since `f4167536` (13 of lane P1, PR #150, and two merges): 23 files,
+1,979 / -273. Four are RTL: `KL_aecp_desc_store.sv`, `KL_aecp_engine.sv`,
`KL_aecp_nvm_writer.sv` and the top's port comments. No module was added (`git diff
--name-status f4167536 c4cb84ff -- hdl` lists only `M` lines), so the Yosys gate still
has 42 tops.

Files both sides changed: `hdl/top/protocol_processor_top.sv`, `tb/pp_top/sim_main.cpp`,
`tb/pp_top/README.md`, `tb/nvm_port/README.md`, `docs/architecture/09_verification.md`.
Four merged cleanly. For each, the merge's diff against one parent is exactly the other
side's diff against the base (sorted `-U0` lines compared: equal for all four), so both
sides are kept whole: this lane's declaration reorder and its moved citations, and P1's
name stage, its D3 contract amendment (`b88240a`: 07, 02 §8.1, 06, 09, the integrator
guide and the compliance review; the top's `aecp_nvm_stb_o` port comment says the same)
and the D3KR cuts (`53e1474`: `d3_phases.hpp`, the `cuts` target, 09).

One conflict, `tb/nvm_port/README.md:105-106`: both sides had moved the same two
citations. This lane had `KL_aecp_nvm_writer.sv:482-485` and
`protocol_processor_top.sv:2726`; P1 had `:549-552` (its writer grew) and `:2730` (its
top gained five comment lines). At the merge they are `:549-552` (`frame_ok_w`'s
declaration and assign; the writer is P1's alone) and `:2731` (`KL_acmp_nvm_shadow #(`:
this lane's reorder moved it +1, P1's comments +5).

**Line citations re-derived at the merge.** Every in-tree line citation was listed
(`file:N`, `` `:N` ``, `line N`, `#LN`; `git grep` over the merged tree). The ones into a
file both sides changed, or into `KL_pp_nvm_port.sv` (this lane's alone) or
`KL_aecp_nvm_writer.sv` (P1's alone), each checked against the text it names at
`39298e03`:

| Site at the merge | Cites | Names | Verdict |
|---|---|---|---|
| `tb/nvm_port/README.md:105` | `KL_aecp_nvm_writer.sv:549-552` | `frame_ok_w` | conflict, resolved |
| `tb/nvm_port/README.md:106` | `protocol_processor_top.sv:2731` | the `KL_acmp_nvm_shadow #(` instance | conflict, resolved (+5) |
| `tb/nvm_port/README.md:1067`, `:1352` | `09_verification.md:56` | the NVM row of §8 | unmoved, holds |
| `tb/nvm_port/README.md:226`, `tb/nvm_port/sim_main.cpp:1443` | port `:244-255` | `dev_cmd_owned_w`'s window | holds (the port is this lane's alone) |
| `tb/nvm_port/README.md:407`, `:413` | port `:376`, `:390` | `state_r <= S_WEREQ;`, `state_r <= S_WEWAIT;` | holds |
| `tb/nvm_port/README.md:1138`, `sim_main.cpp:1441`, `measure_figures.py:117` | port `:350-354` | the sticky `done_seen_r` set | holds (the README line moved 1135 -> 1138 with P1's text) |
| `tb/nvm_port/sim_main.cpp:1328` | port `:446-449` | the `S_WWAIT` arm | holds |
| `tb/nvm_port/sim_main.cpp:1591` | port `:33-34` | the ERASE-then-WRITE banner | holds |
| `tb/nvm_port/README.md:102-104` | `KL_acmp_nvm_shadow.sv:482-483`, `:775`, `:391-395`, `:90-92` | crc serialise, accumulate, `rrec_ok_w`, the vendor-default policy | holds (neither side changed the shadow) |
| `measure_figures.py` ARMS table | twelve port lines | the `if (dev_err_i)` arms | holds; the figures gate re-checks it (item 2) |

The remaining in-tree citations point into files neither side changed
(`KL_pp_acmp_listener.sv:76`, `KL_acmp_talker`'s `:95-96`, `KL_pp_maap.sv:644`,
`:589-590`, the parent's `KL_pp_shadow.sv:1010`).

This lane's citations in the PR body and this file, mapped from `b6f17f22` to `39298e03`
(by diff, every range contiguous and its text unchanged):

| File | At `b6f17f22` | At the merge |
|---|---|---|
| `protocol_processor_top.sv` (item 3's groups) | `:935-953`, `:975`, `:978-986`, `:1004-1005`, `:1825-1828`, `:2933-2943` | `:940-958`, `:980`, `:983-991`, `:1009-1010`, `:1830-1833`, `:2938-2948` (+5, P1's port comments) |
| `protocol_processor_top.sv` (the shadow instance) | `:2726` | `:2731` |
| `tb/pp_top/sim_main.cpp` (item 4) | NSD `:11538-11562`, its call `:11860`, the header list `:11221` | `:11623-11647`, `:11945`, `:11306` (+85) |
| `tb/pp_top/README.md` (item 4) | AX bullet `:1824`, campaign rows `:1129-1131`, paragraph `:1177` | `:1999`, `:1292-1294`, `:1340` |
| `docs/architecture/09_verification.md` | §8.1 clock_source `:163`, §8.6 row `:351` | `:163`, `:356` |
| `tb/nvm_port/README.md` | `:19-22`, `:23-26`, `:226`, `:407`, `:413`, `:1135` | `:19-22`, `:23-26`, `:226`, `:407`, `:413`, `:1138` |

**ROMs.** Every ROM and descriptor image the processor generates, regenerated from a
`git archive` of `hdl/` at the base `f4167536`, this lane's `b6f17f22`, `main`'s `c4cb84ff`
and the merge (`$VALIDATION_STORAGE/c10-a518/r3b/rom/regen.sh`): `ucode.hex` (`518b900c...`),
`ltn_rom.hex` (`23cc67ee...`), the `example_milan_8` image and map (`20356f59...`,
`4d20db2d...`) and the linted `milan_min` image and map (`11d6491b...`, `6da275d2...`) are
byte-identical at all four. The generator's printed report differs only in the output
path it names. Neither side changed a generator or its model input (`gen_ucode.py`,
`gen_ltn_rom.py`, `gen_desc_image.py`, the model JSON), so no ROM differs, which is what
both sides explain.

### Item 2: re-measured at the merge commit

All at `39298e03`, pinned Verilator 5.050, in this checkout (logs, rc and wall-time files
under `$VALIDATION_STORAGE/c10-a518/r3b/run/`, campaign output under `r3b/camp/`). The
checkout is clean after every run.

**Out-of-context netlist, the reorder re-checked.** `main` `c4cb84ff` against the merge,
the in-tree `syn/ooc/protocol_processor_ooc.tcl` through round 1's wrapper (it then writes
`write_verilog -mode design`), Vivado 2026.1, the two runs one after the other with
nothing else of this lane running (`r3b/ooc/pair.sh`; 185 s and 171 s). Between `main`
and the merge `hdl/` differs in two files only: this lane's reorder of the top and the
port's guard.

| | `main` `c4cb84ff` | merge `39298e03` |
|---|---:|---:|
| netlist bytes | 19,658,600 | 19,658,600 |
| netlist sha256 without its `// Date` line | `5839047a...e45a4bd` | the same |
| `util.rpt`, `util_hier.rpt` | | identical but the `Date` line |
| Slice LUTs (logic + memory) | 31,165 (29,899 + 1,266) | 31,165 |
| Slice registers | 32,106 | 32,106 |
| F7 / F8 muxes | 1,503 / 56 | 1,503 / 56 |
| RAMB36 / RAMB18 / DSP | 23 / 2 / 4 | 23 / 2 / 4 |
| WNS / TNS (OOC, no timing claim) | -8.355 / -4312.697 ns | the same |
| `Synth 8-6901` | 51: 44 `protocol_processor_top.sv`, 3 `KL_aecp_notify`, 2 `KL_pp_originator`, 2 `KL_pp_rx_validator` | 7: the same three files |

So the reorder is netlist-neutral at the merge as it was at `f4167536`. The figures moved
from round 1's (30,658 LUTs) with P1's RTL, on both sides of the comparison alike.

**Suites, entry points and gates.**

| Command | rc | Result at `39298e03` | Record it must match |
|---|---:|---|---|
| `./scripts/run_suites.sh` | 0 | 33 suites, **1,021,449** checks, 0 failing; `pp_top` **10,416**, `desc_store` 586, `nvm_port` 1,219; 913 s | P1's merge record (PR #150, round 1b): 1,021,423 with `pp_top` 10,390; plus this lane's 26 (NSD's 13, default and line builds) = 1,021,449 and 10,416. Against round 3 (`b6f17f2`) two suites moved, both by P1's own figures: `desc_store` 584 -> 586, `pp_top` 9,222 -> 10,416 (+1,194) |
| `./scripts/lint_hdl.sh` | 0 | 41 of 41 `LINT OK` | 41 |
| `make check` | 0 | 41 mermaid + 18 wavedrom, **1,114** links, 115 REQ rows, 17 GAP, 94 rows 0 untested, 28 parameters | P1's 1,114 links |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested | |
| `./syn/yosys/run.sh` | 0 | **42** `YOSYS OK`, `YOSYS 42 tops, all.v parsed 1 time(s)`, `YOSYS XILINX OK KL_aecp_engine`; the census (yosys's `select -list =*` of the parsed all.v) passed, so 42 declared = 42 tops; 44 s | P1 added no module: 42 |
| `YOSYS_MALLOC=none ./syn/yosys/run.sh` | 0 | `yosys allocator: system`; verdict lines identical to the jemalloc run's; 49 s | |
| `./syn/yosys/run.sh --selftest-alloc` | 0 | PASS | |
| `tb/nvm_port/elab_bounds.sh` | 0 | 4 `ELAB OK`, 6 `GUARD OK` (USERERROR for `MEM_TIMEOUT_CYC_P`, USERFATAL for `MAX_PAYLOAD_P`), `YOSYS OK MAX_PAYLOAD_P=65527 elaborates, MAX_PAYLOAD_P=65528 stops at the guard's $finish` | round 3's lines exactly |
| `make -C tb/nvm_port figures` | 0 | `all measured figures agree with the tree`, 160 Verilator builds, 1,172 s (the ARMS table's twelve port lines and every README figure, P1's README text included) | |

**`tb/pp_top` campaigns** (each through its driver, `--jobs` as stated; `compare_counts.py`,
`compare_logs.py` and `compare_notify.py` in `r3b/tools/` compare every arm's failing-check
count with its README row):

| Campaign | rc | Controls | Arms | Counts against the README | Wall |
|---|---:|---|---|---|---:|
| `aecp_dispatch_mutants.py --jobs 3` (with this lane's three NSD arms) | 0 | 4 PASS | 40 of 40 KILLED | all 40 equal | 462 s |
| `aecp_mutants.py --jobs 3` (deadline, hazards, budget, ucpu) | 0 | 5 PASS | 55 of 55 KILLED | all 55 equal (the three hazard rows P1 moved included) | 613 s |
| `notify_mutants.py --jobs 3` | 0 | 5 goldens PASS | 40 of 40 KILLED | all 40 equal (`ident_burst_from_t0` 21, P1's record) | 471 s |
| `ctr_mutants.py --jobs 3` | 0 | 1 PASS | 17 of 17 KILLED | all 17 equal | 201 s |
| `d3_mutants.py --jobs 4` (D3, D3V, D3KR's two `cut_` controls, AD7-AD9, `tb/acmp_nvm`, `tb/rx_validator`) | 0 | 6 goldens PASS (`pp_top`, `--adp-only`, `--volatile-only`, `--cuts-only`, `acmp_nvm`, `rx_validator`) | 110 of 110 KILLED | all equal: 98 rows of this README, 11 of `tb/acmp_nvm/README.md`'s DR2c / issue-cycle / own-contract table, 1 of `tb/rx_validator/README.md` (M4, 4 FAILs) | 3,248 s |
| `acmp_mutants.py --jobs 3` | 0 | 3 goldens PASS | 19 of 19 KILLED | all equal: 14 `pp_top` rows (`N of 43`), `tb/acmp_listener`'s 93 / 50 / 40 / 30 of 2,988 / 2,984, `tb/rx_validator` M6's 27 | 215 s |
| `gsi_mutants.py --jobs 2` | 0 | golden and restored PASS | 20 of 20 failed by their named check | the README records the named check, not a count | 665 s |
| `name_wr_mutant.py` | 0 | golden and restored PASS | `decode` killed | its three required checks (`NW EIGHT`, `NW LOCKED`, `NW ABORT` pulse counts) among its failures | 55 s |
| `tb/adp_engine/mutants.py --jobs 3` (with the `pp_top adp-config` arms) | 0 | 2 PASS | 30 of 30 KILLED | all 30 equal, `cfg-valid-no-reset` 9 and `gate-enable-dropped-top` 7 as P1's rows record | 170 s |
| `tb/maap/mutants.py --jobs 3` (with the `pp_top maap-internal` legs) | 0 | 3 PASS | 27 arms, 29 runs KILLED | all 29 tallies equal (`N FAIL of M`) | 126 s |
| `tb/srp_top/mutants.py --jobs 3` (no `pp_top` leg; one of the HDL workflow's five) | 0 | 11 PASS | 78 KILLED, 90 checks 0 FAIL | every verdict line identical to round 2's | 717 s |

Every campaign of `tb/pp_top`, and the two that run `pp_top` legs, matches its record
arm for arm. No README count moved, so no record commit follows the merge.

Concurrency: the suites, the figures gate and the campaigns ran two to four at a time,
never beside a Vivado run. The unit's memory reached its 12 GB limit with page cache
(`memory.events` `max` 8,864, reclaim), with no OOM event and no kill; anonymous memory,
sampled in the busiest later window, peaked at 8.0 GB.

### Item 3: parent consumer set (17)

**Which p2 patch.** P1's PR #150 (parent-visible item 9) states that
`parent-adoption-p2-p1-1269cdaf.patch` replaces `parent-adoption-p2-cdf49d1a.patch`
for P1's adoption: it amends the parent's D3 page where it stated the old map rule. The
merge carries P1, so item 3 uses **c8 + p2-p1 + c10**, as the assignment allows. The two
patches differ only in `docs/design/SAVED_STATE_MATERIALIZATION.md` (`git diff cfg-p2
cfg-p2p1 --stat`: that one file, +28 / -13). No gate tells them apart: the ten light gates
(2, 3, 3s, 4, 5, 6, 7, 8, 11, 17) were run in both and print the same verdict lines; the
heavy gates do not read that page: no source of gates 10 and 12-16 names it or globs
Markdown, and `test_builder.py` reads six other pages by fixed path.

**Scratch parent** (`$VALIDATION_STORAGE/c10-a518/r3b/parent`, built fresh by
`r3b/parent_setup.sh`; the trusted checkout was only read): a `git archive` of
`1269cdaf` committed into a new repository (tree `84537179...`, equal to the trusted
checkout's, 984 index entries, gitlinks added), gptp-processor `5dce647a` and verilog-axis
`48ff7a7e` cloned from round 2's scratch clones at their pins, protocol-processor a
scratch clone of this branch, `external` uninitialised. Two branches, each patch applied
after a clean `git apply --check` and committed: `cfg-p2` (c8 `aa5a88eb...`, p2
`590f791d...`, c10 `55e62329...`) and `cfg-p2p1` (c8, p2-p1 `d3034e89...`, c10), each with
the processor gitlink at `39298e03`. `git submodule status` shows ' ' for the three, and
porcelain is empty before and after every gate. Logs: `r3b/pg-p2p1/`, `r3b/pg-p2/`.

| # | Command | rc | Result at `1269cdaf` + c8 + p2-p1 + c10, processor `39298e03` |
|---:|---|---:|---|
| 1 | `scripts/check_cpp_idiom.py` | 0 | multi-declarator 0 <= 0, long function 0 <= 0, build without warnings 0 <= 0 |
| 2 | `scripts/check_py_idiom.py` | 0 | every ratchet held |
| 3 | `scripts/check_rtl_source_lists.py` | 0 | `107 files ..., 4 of 4 consumer list(s) ...; protocol-processor 42/42 tops, 0 recorded` |
| 3s | `scripts/check_rtl_source_lists.py --selftest` | 0 | 50 of 50 |
| 4 | `scripts/pp_srcs.py --check --selftest` | 0 | sources derived, self-test passed |
| 5 | `scripts/check_port_contracts.py` | 0 | protocol-processor **1,759** ports (round 3: 1,756), 111 <= 111 undocumented. The three are P1's internal ports (`KL_aecp_desc_store` `sb_name_o`, `KL_aecp_nvm_writer` `nchg_i` and `nchg_ord_i`); `protocol_processor_top` keeps its 213 at `f4167536`, `b6f17f22`, `c4cb84ff` and the merge |
| 6 | `scripts/measure_naming.py --check` | 0 | 96 candidates, all recorded |
| 7 | `scripts/measure_test_evidence.py --check` | 0 | 72 <= 77, 10 <= 10, 0 <= 0, 3 <= 3 |
| 8 | `scripts/docs_check.py` | 0 | 0 findings over 185 md + 956 files |
| 9 | `scripts/xvlog_gate.py --check` (xvlog on PATH, alone, last) | 0 | `PASS (3 finding(s) == ratchet; 0 hdl/, 3 pinned processors)`; 147 s |
| 9s | `scripts/xvlog_gate.py --selftest` (alone) | 0 | PASS |
| 10 | `sw/builder/test_builder.py` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN (its gate 11 needs a local board build tree, as in rounds 1 to 3); 1,423 s |
| 11 | `scripts/lint_rtl.py --check` | 0 | 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j16` | 0 | 606, 606, 646, 311 checks, 0 failures; 229 s |
| 13, 14 | `make -C tb/verilator/nvm_cosim lint`, `quick` | 0, 0 | lint pass; 315 of 315, `RESULT: PASS` |
| 15 | `make -C tb/verilator/milan_dp -j16 VERILATOR_JOBS=3` | 0 | 9 `RESULT: PASS`, 0 FAIL; 1,640 s |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | 0 | tdm8_render 65 and 152 checks, 0 failures; 5 of 5 leg-defect arms; 355 s |
| 17 | `scripts/check_sh_idiom.py` | 0 | unquoted expansion 3 <= 3, top-heavy long script 0 <= 0 |

Gate 16 is worth a note. P1 recorded it failing two T30 INTERNAL LAW checks at dev
`bbf704ec` with P1's processor (ruled (b) on #83, 5969246536; parent defect milan-fpga
#643: the law depends on the feed's phase against the INTERNAL grid, which the name
stage's longer boot walk moves). At dev `1269cdaf` the T30 INTERNAL LAW check exists
(`sim_tdm8_render.cpp:3045`) and passes with the merge: `292 PDUs, first-event delay
18207..18207 cycles = 8.739..8.739 media ticks; the law is 8 < d/T <= 9`. So nothing here
reproduces #643, and the dev revision P1 measured is not this one.

The other parent commands that open `run.sh` or a budget (round 2's strace census), at
`cfg-p2p1`, all rc 0: `check_sh_idiom.py --selftest` (48/48), `check_hygiene.py --check`
and `--selftest` (35/35), `check_todo_ownership.py` and `--selftest` (45/45),
`measure_fail_fast.py --check` and `--selftest` (106/106), `check_entity_shape.py
--self-test` (PASS). The documentation gates that read the p2-p1 page, with the parent's
pinned renderer: `check_em_dash.py --base <dev>` (0 findings over the three patches' 81
added Markdown lines), `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`
rc 0. `check_doc_paths.py` is rc 1 on the p2 page's row W13 (`tb/acmp_nvm`,
`tb/nvm_port` without the `protocol-processor/` prefix), exactly round 2's finding: p2-p1
keeps that row, and it is not one of the 17.

### Round 3b, parent-visible

1. Adopting this head: `parent-adoption-c8-cdf49d1a.patch`, then
   `parent-adoption-p2-p1-1269cdaf.patch` (P1's replacement for the p2 patch), then
   `parent-adoption-c10-1269cdaf.patch`, unchanged since round 2 (`55e62329...`). With
   them the 17 gates are rc 0 at dev `1269cdaf`.
2. `protocol_processor_top` keeps its 213 ports; gate 5's processor count is 1,759 because
   of P1's three internal ports, not this lane.
3. ROMs: `ucode.hex` `518b900c...`, `ltn_rom.hex` `23cc67ee...`, unchanged from `f4167536`
   through the merge; the parent's ROM-digest row for the new pin is the pin bump's
   bookkeeping, as round 2 found.
4. The out-of-context netlist at this head is `main` `c4cb84ff`'s, byte for byte but its
   date line. This lane adds no cost; P1's figures stand.
5. Gate 16 (`milan_dp_render`) passes at dev `1269cdaf` with this head; P1's two T30
   INTERNAL LAW failures (milan-fpga #643) were measured at dev `bbf704ec`.

### What remains (round 3b)

- The items of "What remains" above, unchanged.
- The round-3 reviews, which the assignment says cover rounds 3 and 3b together.
