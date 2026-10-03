[A518]
Closes #25
Closes #17
Closes #37
Relates to #22

Lane C10 (tooling): the four items of the assignment on #25, in their order, and the
answers of rounds 2 and 3 to the reviews of PR #149 (see "Round 2" and "Round 3" at the end).
Round 3b merges `main` `c4cb84ff` (PR #150, lane P1) and re-measures at the merge (see
"Round 3b"). This PR supersedes PR #26,
whose branch `25-cover-every-module-and-stop-reparsing` is merged here with `--no-ff`, its
two commits kept. The lane adds no logic. Item 2 is an elaboration guard. Item 3 is a
reorder whose synthesized netlist, and so its out-of-context cost, is unchanged. Item 4
adds a test arm. No port changed, no parameter changed its meaning, and the microprogram
is unchanged.

## 1. #25: every `hdl/` module is a Yosys top, and the design is parsed once

- **Merge** (`5c20350`). One conflict, in `syn/yosys/run.sh`. It is resolved to the
  branch's structure (the census, the allocator selection, the elaboration step) plus
  `main`'s `pipefail`, its sv2v-line comment and the three modules `main` gained since
  (`KL_aecp_desc_mem_guard`, `KL_pp_nvm_mgr_arb`, `KL_pp_acmp_lsn_admit`). `tops` now
  names all **42** declared modules.
- **The census** refuses a declared module with no top, and a top that names no declared
  module. The declared modules are not matched in any text: they are yosys's own list of
  the modules it parsed from `all.v` (sv2v's lowering of every source), written by the
  elaboration run from its `read_verilog -defer` design with `select -list =*`
  (`b6f17f2`). So no header layout, attribute instance or comment hides a module, and
  black and white boxes are listed too. Its scope is what yosys parses: a module in an
  inactive `` `ifdef `` branch is not in `all.v` and is not counted, and a module yosys
  cannot parse (`module automatic`, for one) fails the parse instead, which names it. The
  census runs on the first run's list before any verdict is printed.
- **Parsed once** (`b5e3b97`). One yosys reads `all.v` once (`read_verilog -defer`),
  keeps it with `design -save`, and elaborates each top from a `design -load` of it, with
  the same `hierarchy -check; proc; opt_clean` as before. PR #26's 16-way pool, with one
  parse per top, is replaced. Each top's step is bracketed by two markers on stderr, so a
  failing top is named, with the log's first ERROR line. A fresh run then resumes at the
  next top, so a red gate still gives every top a verdict, in inventory order. A green
  gate parses exactly once, and says so (`YOSYS 42 tops, all.v parsed 1 time(s)`). A
  parse failure names the module of `all.v` that holds the cited line, reading past
  attribute instances and a lifetime keyword (with no parse, yosys has no list to name it
  from).
- The census and the elaboration loop are shell functions, and their name lists are
  quoted (`cd08ca7`). This keeps `run.sh` within the parent's shell-idiom gate.
- The `synth_xilinx` / `select -assert-count 6 t:RAMB36E1` regression is unchanged and
  passes.

**Red on a broken new top, naming it.** The "this head" column was measured at round 3's `b6f17f2`, before the round-3b merge of `main` `c4cb84ff`. Every rc and every named module reproduce at the merge `39298e03`, but the quoted `all.v:N` line numbers move with the merge, because P1's sources precede these modules in `all.v`: at `39298e03` the `module automatic` row reports `all.v:20859` (not 20749), and the `all.v` syntax plant reports a correspondingly later line (R448-3 F1). Each case is a scratch copy. Unless stated
otherwise, the fault is an instance of an undeclared module, planted before the
module's `endmodule`:

| Fault planted in | `main` `f4167536` | this head |
|---|---|---|
| `KL_srp_top` | rc 0, missed | rc 1: `YOSYS FAIL KL_srp_top: ERROR: Module \c10_absent_module referenced in module \KL_srp_top ...`, then `protocol_processor_top` |
| `protocol_processor_top` | rc 0, missed | rc 1: `YOSYS FAIL protocol_processor_top: ...` |
| `KL_acmp_nvm_shadow`, `KL_mrp_strip`, `KL_srp_admission` | rc 0, missed | rc 1, each named, then its parents |
| `KL_pp_dispatch_fifo` | rc 1, through its parent `KL_pp_dispatch` | rc 1: `KL_pp_dispatch`, `KL_pp_dispatch_fifo`, `protocol_processor_top` |
| two faults, `KL_mrp_strip` + `KL_srp_admission` | | rc 1, four tops named, `parsed 4 time(s)` |
| `KL_srp_top` removed from `tops` | | rc 1: `modules declared under hdl/ with no entry in the tops array: KL_srp_top` |
| a name no module declares added to `tops` | | rc 1: `tops array names modules that no longer exist under hdl/` |
| a syntax fault planted in `all.v` inside `KL_srp_top` | | rc 1: `YOSYS FAIL all.v in module KL_srp_top: all.v:20318: ERROR: syntax error ...`, every top `not elaborated` |
| a new file declaring `module` with its name on the next line, holding a fault (R449-1's `newmod` probe) | | rc 1: `modules declared under hdl/ with no entry in the tops array: KL_r449_newmod` (`54f9411` missed it: rc 0) |
| the same split header, added to `tops` | | rc 1: `YOSYS FAIL KL_c10_layout: ERROR: Module \c10_absent_module referenced in module \KL_c10_layout ...` |
| a comment between `module` and the name; `macromodule` | | rc 1, each named by the census |
| `(* keep_hierarchy = "yes" *) module X`, on one line or with the attribute on the line before, holding a fault | | rc 1, named by the census (`cd08ca7` missed both: rc 0) |
| the same, no fault, added to `tops` | | rc 0, 43 OK (`cd08ca7`: rc 1, "no longer exist") |
| the same with the fault, added to `tops` | | rc 1: `YOSYS FAIL KL_r448_attro: ERROR: Module \r448_absent_module referenced in module \KL_r448_attro ...` |
| `(* blackbox *) module X` | | rc 1, named by the census; added to `tops`, rc 0 |
| `module automatic` with the name on the next line | | rc 1: `YOSYS FAIL all.v in module KL_r448_auto: all.v:20749: ERROR: syntax error, unexpected TOK_AUTOMATIC ...`. yosys cannot parse a lifetime keyword on a module, so the parse names it (`cd08ca7` named it `automatic`) |
| a module inside an inactive `` `ifdef `` | | rc 0: not counted, since sv2v drops it and yosys never reads it |

At `main`, `KL_pp_dispatch` instantiates `KL_pp_dispatch_fifo`, so five of the six were
uncovered, not six.

**Wall time and top count**, end to end (sv2v, elaboration and the XILINX regression).
Each run was alone on the same host, three interleaved rounds, median:

| Revision | Tops | Median of three | Rounds |
|---|---:|---:|---|
| `main` `f4167536` (one yosys per top, full re-parse) | 36 | **88.80 s** | 83.30, 90.51, 88.80 |
| PR #26's pool, as merged (`5c20350`) | 42 | 30.00 s | 28.70, 30.00, 30.04 |
| **parsed once (`b5e3b97`)** | **42** | **35.97 s** | 35.97, 34.24, 36.57 |
| parsed once, `YOSYS_MALLOC=none` | 42 | 48.12 s | 51.22, 48.12, 45.66 |

The elaboration step alone, on one staged `all.v`, takes 50.89 s for `main`'s 36
per-top runs and 10.00 s parsed once for 42 tops. The verdict lines are identical across
the merge, the head and the head on the system allocator; only the new `parsed` line
differs.

## 2. #17: `MAX_PAYLOAD_P` above the field's bound fails elaboration, naming it

`KL_pp_nvm_port.sv:196-200`:

```systemverilog
localparam int unsigned MAXP_BOUND_C = (1 << $bits(dev_len_o)) - 1 - int'(HDR_LEN_C);
if (MAX_PAYLOAD_P > MAXP_BOUND_C) begin : g_maxp_check
  $fatal(1, "KL_pp_nvm_port: MAX_PAYLOAD_P=%0d is above %0d: %0d + it overflows dev_len_o",
         MAX_PAYLOAD_P, MAXP_BOUND_C, HDR_LEN_C);
end
```

The bound is computed from the length port's width and the record header, in both the
condition and the message. At the shipped values it is 65527, and the message reads
`MAX_PAYLOAD_P=65528 is above 65527: 8 + it overflows dev_len_o`. 65527 itself appears only
in the bench, as the specification value. The `$fatal(1, ...)` is
`KL_pp_acmp_listener.sv:344-347`'s, placed at module scope like the port's own
`MEM_TIMEOUT_CYC_P` guard and every other elaboration guard in `hdl/`. That placement was
measured, not assumed:

| `MAX_PAYLOAD_P` = 65528 | in an `initial` block (the precedent's placement) | at module scope (this change) | module scope, `$error` |
|---|---|---|---|
| Verilator 5.050 lint and build | rc 0: built, stops only at time 0 | rc 1, `%Warning-USERFATAL ... MAX_PAYLOAD_P=65528 is above 65527 ...` | rc 1, `%Warning-USERERROR` |
| sv2v + Yosys 0.66 | rc 1 | rc 1, at the guard's `$finish` (Yosys prints no `$display` text) | rc 0, missed |
| Vivado 2026.1 `synth_design -rtl` | rc 1 | rc 1, `[Synth 8-6058] Synth Error: KL_pp_nvm_port: MAX_PAYLOAD_P=65528 is above 65527 ...` | |

At 65527 all three elaborate. `tb/nvm_port/elab_bounds.sh`, which `make` in `tb/nvm_port`
runs, lints 1024 and 65527 clean and refuses 65528, 65535 and 2^32 - 1 by name and bound.
It also grades the class: the refusal's line must carry `%Warning-USERFATAL` (or `%Error`).
Where sv2v and yosys are installed, yosys must also elaborate 65527 and stop at 65528. A
`$error` or `$warning` guard fails both. Nine mutants each turn the bench red:

- the guard deleted;
- the bound + 1;
- `>=`;
- the message without the bound;
- the `initial` placement;
- `$error`, with and without sv2v and yosys on PATH;
- `$warning`;
- a 10-byte header.

The guard moved the port's lines down by ten. Round 2 kept every line in place. The full
set of moved line citations into `KL_pp_nvm_port.sv`:

| Site | Was | Now | Names |
|---|---|---|---|
| `tb/nvm_port/README.md:226`, `tb/nvm_port/sim_main.cpp:1443` | `:234-245` | `:244-255` | `dev_cmd_owned_w` |
| `tb/nvm_port/README.md:1138`, `sim_main.cpp:1441`, `measure_figures.py:117` | `:340-344` | `:350-354` | the sticky done set |
| `tb/nvm_port/sim_main.cpp:1328` | `:436-439` | `:446-449` | the `S_WWAIT` arm |
| `tb/nvm_port/README.md:407` | `:366` | `:376` | the transition into `S_WEREQ` |
| `tb/nvm_port/README.md:413` | `:380` | `:390` | what `S_WEREQ` transitions to |
| `measure_figures.py`'s ARMS table | twelve lines | each + 10 | the `if (dev_err_i)` arms |

`tb/nvm_port/README.md:106`'s `protocol_processor_top.sv:2714`, already stale before this
PR, is now `:2731` (`:2726` until the round-3b merge, whose five lines of P1 port comments
sit above it). The top does not override the parameter, so the change is
elaboration-only, and the OOC cost is unchanged (below).

## 3. #22: `protocol_processor_top.sv` declares before use

`34b5246` moves seven declaration groups above their first use and changes nothing else.
The sorted multiset of non-blank lines differs by one added comment line. The groups are:

- the 19 SRP class-D lanes;
- `tkr_declaring_w`;
- the binding view's five registers and `lstn_dbg_busy_w`;
- `adp_dbg_aidx_nc_w`;
- the listener's A15 settle quartet;
- u_notify's arm, monitor-arm and PRNG faces.

Evidence:

- `xvlog -sv`, packages first and one module per invocation, over every `.sv` under
  `hdl/`: `protocol_processor_top.sv` goes from `VRFC 10-3380 srp_class_a_prio_w` to
  clean (37 to 38 of 41 analyse).
- `Synth 8-6901` in the OOC run: 51 to 7, with 44 to 0 in `protocol_processor_top.sv`.
- Behaviour unchanged: the OOC synthesized netlist of base and head (19,508,014 bytes) is
  byte-identical except its `// Date` line, and so are both utilization reports.

**#22 is related, not closed.** Its acceptance asks for every module under `hdl/` clean
under xvlog and for zero `Synth 8-6901` in the integrator's `KL_pp_shadow`. Three files
outside this item still fail: `KL_aecp_notify.sv:557` `pd_ix_w`, `KL_pp_originator.sv:194`
`cancel_hit_w` and `KL_pp_rx_validator.sv:383` `vd_push_w` (7 warnings).

## 4. #37: a test arm for SET_CLOCK_SOURCE's NO_SUCH_DESCRIPTOR branch

`tb/pp_top` section AX, arm NSD (13 checks, in the default and line builds):

- **NSD0**: the holder moves clock source 2 to 1. E_SCLKS leaves the replaced 2 in r6,
  because the µCPU loads only r12 to r15 per dispatch.
- **NSD1**: a second controller's SET_CLOCK_SOURCE(2) on CLOCK_DOMAIN 1, which the image
  lacks, gets NO_SUCH_DESCRIPTOR at cdl 20 with a zero body, byte-exact. There is no store
  write, NVM mark, notify enqueue, or unsolicited frame at the registered holder.
- **NSD2**: GET_CLOCK_SOURCE still reads the stored 1.
- **NSD3**: under the bench's lock, the same command gets ENTITY_LOCKED with a zero body;
  the lock outranks the miss.

Since #53 (`692ad8f`), the miss branch is E_SCLKS + 3 (it was + 4 when #37 was filed), and
it targets the out-of-line E_SCLKSRF, whose first word is CHECK_LOCK. New arms in
`aecp_dispatch_mutants.py`:

| Arm | Failing checks |
|---|---|
| `sclks-miss-target-next-word`: the branch target moved one word on, past CHECK_LOCK | NSD3 (named), LK4 |
| `sclks-miss-preload-dropped`: E_SCLKS + 1's r6 preload replaced with NOP | NSD1 (named), NSD3. LK4 and LK5 pass, so NSD is the only arm grading the preload |
| `sclks-miss-branch-dropped`: the miss branch replaced with NOP | NSD1 (named), LK5 |

The other one-word move, to E_SCLKSRF - 1, is measured equivalent. ROM word 1143 is
unplaced fill, which `gen_ucode.py` lays as a NOP there, so the program runs on into
E_SCLKSRF's CHECK_LOCK; every check passes (928 of 928). It is recorded in the README and
is not an arm, because the driver counts only kills.

## Out-of-context cost

`syn/ooc/protocol_processor_ooc.tcl`, Vivado 2026.1, base `f4167536` and head:

| Resource | Base | Head | Delta |
|---|---:|---:|---:|
| Slice LUTs | 30,658 | 30,658 | 0 |
| Registers | 31,944 | 31,944 | 0 |
| LUT as distributed RAM | 1,222 | 1,222 | 0 |
| F7 / F8 muxes | 1,482 / 57 | 1,482 / 57 | 0 |
| RAMB36 / RAMB18 / DSP | 23 / 2 / 4 | 23 / 2 / 4 | 0 |

Equal, as required, and the netlist itself is identical. At the head, the synthesized
netlist (19,508,014 bytes) is byte-identical to the base's except its `// Date` line, and
both utilization reports are identical. That is true at round 1's `34b5246` and again at
this head, after round 2's change to the port. Both builds have the same OOC slack, so this
makes no timing claim.

At the round-3b merge the base is `main` `c4cb84ff`, which carries P1's RTL: 31,165 LUTs
(29,899 + 1,266), 32,106 registers, F7 / F8 1,503 / 56, RAMB36 / RAMB18 / DSP 23 / 2 / 4,
the same at the merge, and the two netlists (19,658,600 bytes) again differ only in the
`// Date` line. `Synth 8-6901`: 51 at `main`, 7 at the merge.

## Validation

All with the pinned Verilator 5.050. This table is rounds 1 to 3's, at `b6f17f2`; round 3b
re-ran every row at the merge `39298e03`, all rc 0 (see "Round 3b" for its figures):

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | 33 suites, **1,020,253** checks, 0 failing. `tb/pp_top` 9,196 to 9,222 (+26: NSD's 13 in the default and line builds). `main` swept on the same host: 1,020,227, and `tb/pp_top` is the only suite whose tally differs |
| `./scripts/lint_hdl.sh` | 0 | 41 of 41 |
| `make check` | 0 | 41 mermaid + 18 wavedrom blocks, 1,105 links, 115 REQ rows, 17 GAP findings, 94 module rows 0 untested, 28 parameters |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `./syn/yosys/run.sh` | 0 | 42 of 42 `YOSYS OK`, parsed once, `YOSYS XILINX OK`; the same verdict lines with `YOSYS_MALLOC=none` |
| `./syn/yosys/run.sh --selftest-alloc` | 0 | PASS |
| `tb/nvm_port/elab_bounds.sh` (in `make`) | 0 | 4 ELAB OK, 6 GUARD OK (class printed), YOSYS OK |
| `make -C tb/nvm_port figures` | 0 | all measured figures agree with the tree (160 builds) |
| `aecp_dispatch_mutants.py --jobs 4` | 0 | 4 controls PASS, 40 of 40 KILLED |
| `aecp_mutants.py --jobs 4` | 0 | 5 controls PASS, 55 of 55 KILLED |
| `tb/srp_top`, `tb/maap`, `tb/adp_engine` `mutants.py --jobs 4` | 0, 0, 0 | 90, 32, 32 checks, 0 FAIL |

The figures gate and the five campaigns ran at `137ac73`. The two later commits,
`cd08ca7` and `b6f17f2`, change only `syn/yosys/run.sh`, which none of them builds. The
suites, lint, `make check`, the matrix, the Yosys gate and its allocator self-test ran
again at `b6f17f2`, with the results above (see "Round 3"). Round 2's probes, unchanged:

- R449-1's `yosys_fault.sh`: 18 cases, every row equal to its published table, except
  `newmod` (rc 0 to rc 1).
- `nvm_bound_probe.sh`: `pristine` rc 0, with yosys refusing 65528. `err`, `warn` and
  `hdr10` give rc 1.

**Parent consumer set** at milan-fpga dev `1269cdaf`, in a scratch copy: a `git archive`
of dev (984 index entries, tree identical), gptp-processor `5dce647a` and verilog-axis
`48ff7a7e` at their pins, and protocol-processor at this head with its gitlink recorded.
`parent-adoption-c8-cdf49d1a.patch`, then `parent-adoption-p2-cdf49d1a.patch`, then the
amended `parent-adoption-c10-1269cdaf.patch` were each applied after a clean
`git apply --check`:

| # | Command | c8 + p2 | + c10 | Result with c10 |
|---:|---|---:|---:|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | 0, 0 | 0, 0 | every ratchet held: long function 0 <= 0 and 9 <= 9, long module 10 <= 10, build without warnings 0 <= 0 |
| 3 | `check_rtl_source_lists.py` | **1** | 0 | c8 + p2: six `STALE RECORD`, one per new top; + c10: `protocol-processor 42/42 tops, 0 recorded` |
| 3 | `check_rtl_source_lists.py --selftest` | **1** | 0 | 50 of 50 (47 of 49 without c10) |
| 4 | `pp_srcs.py --check --selftest` | 0 | 0 | 46 sources derived, self-test passed |
| 5 | `check_port_contracts.py` | 0 | 0 | processor 1,756 ports, unchanged |
| 6, 7 | `measure_naming.py --check`, `measure_test_evidence.py --check` | 0, 0 | 0, 0 | 96 recorded; 72 <= 77, 0 <= 0 unexplained DUT readers |
| 8 | `docs_check.py` | 0 | 0 | 0 findings |
| 9 | `xvlog_gate.py --check` (alone, last) | **1** | 0 | c8 + p2: `BANK IT: protocol_processor_top.sv\|VRFC 10-3380\|srp_class_a_prio_w no longer occurs`; + c10: `PASS (3 finding(s) == ratchet)` |
| 9 | `xvlog_gate.py --selftest` | | 0 | PASS |
| 10, 11 | `sw/builder/test_builder.py`, `lint_rtl.py --check` | -, 0 | 0, 0 | all gates pass except gate 11, not run (it needs a local build tree, as before); 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j16` | - | 0 | 606, 646, 606 and 311 checks, 0 failures |
| 13, 14 | `make -C tb/verilator/nvm_cosim lint`, `quick` | - | 0, 0 | pass; 315 of 315 |
| 15 | `make -C tb/verilator/milan_dp -j16 VERILATOR_JOBS=3` | - | 0 | 9 RESULT: PASS |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | - | 0 | 0 failures; 5 of 5 leg-defect arms caught |
| 17 | `check_sh_idiom.py` | 0 | 0 | unquoted expansion 3 <= 3, top-heavy long script 0 <= 0 |
| | `check_entity_shape.py --self-test`, `check_todo_ownership.py --selftest` | 0, 0 | 0, 0 | PASS; 45 of 45 |

The self-tests that read either budget were found by tracing, not by name. Every python
command in the parent's workflows and suite-runner preflights (91) ran under `strace -f`
in three configurations: dev as it is, c8 + p2, and + c10. The self-tests whose process
opens `processor_yosys_tops.budget` or `xvlog.budget` are `check_rtl_source_lists`,
`pp_srcs`, `check_entity_shape`, `check_todo_ownership` and `xvlog_gate`; all are rc 0 with
c10. With the parent's pinned Markdown renderer installed, the documentation gates that
read the patched page are also rc 0 with c10: `check_em_dash.py --base` (0 findings in the
patch's added lines), `check_doc_style.py` and `gen_toc.py --check` / `--verify-anchors`.

Five commands of the 91 are rc 0 at dev and not rc 0 with c8 + p2, with or without c10.
None of the five comes from this PR's change. Four are the pin bump's own bookkeeping,
which needs the adopted SHA:

- `check_submodule_docs.py` and `submodule_boundaries.gen.py --check` / `--selftest`: the
  documented pin and the submodule diagram;
- `syn/yosys/ooc_selftest.py`: the ROM-digest row for the new pin
  (`./ooc.sh --record-rom-digests`).

The fifth, `check_doc_paths.py`, comes from the p2 patch. Its design-document row W13
cites `tb/acmp_nvm` and `tb/nvm_port` without the `protocol-processor/` prefix.

Two more are artifacts of the traced run, not of a configuration:

- `xvlog_gate.py --selftest` is rc 1 everywhere without xvlog on PATH, and rc 0 with it
  (above).
- `test_suite_cancellation.py` trips its process-ownership check under ptrace. It is rc 0
  untraced with c10.

Gates 10 and 12-16 ran with c10 only. They read none of the four files c10 changes.
Round 3 ran the "+ c10" column again with the processor at `b6f17f2`, all 17 and the
self-tests: every result is as listed (see "Round 3").

## Parent-visible list

1. **No port, parameter or register change** of `protocol_processor_top`.
   `KL_pp_shadow` needs no edit.
2. **Adopting this head needs `parent-adoption-c10-1269cdaf.patch`** after c8 and the p2
   patch; since the round-3b merge, P1's `parent-adoption-p2-p1-1269cdaf.patch` takes the p2
   patch's place, as PR #150 states. It changes four files:
   - `processor_yosys_tops.budget` loses its six lines;
   - `xvlog.budget` banks `protocol_processor_top.sv`;
   - `scripts/check_rtl_source_lists_selftest.py` replaces the arm "the record is non-empty
     at this pin" with two arms on a synthetic population drawn from the live pin. A live top
     taken out of the array must reach the verdict as `TOPS DRIFT` with exit 1, and be debt
     once recorded. Its record left behind once it is a top again must reach the verdict as
     `STALE RECORD` with exit 1. This holds with six records and with none, and the new
     self-test catches a `verdict()` that drops `STALE RECORD`, which the old one missed;
   - `docs/development/CODE_QUALITY.md`: the paragraph on the six now says they were drift
     and were deleted.

   `KL_pp_shadow` synthesis drops the 44 `Synth 8-6901` warnings from
   `protocol_processor_top.sv`. 7 remain, in the three files #22 still names.
3. `syn/yosys/run.sh` now passes the parent's shell-idiom gate (`check_sh_idiom.py`). At
   `54f9411` it failed that gate, with two unquoted expansions and a top-heavy script.
4. `KL_pp_nvm_port` refuses `MAX_PAYLOAD_P` above `(1 << $bits(dev_len_o)) - 1 - HDR_LEN_C`
   (65527) at elaboration. Nothing in the parent sets it.
5. The ROM generators are unchanged from `main`, so the ROM digests are `main`'s, and the
   OOC netlist is identical to `main`'s.
6. Processor documents the parent reads: 09 §8.1 (clock_source row) and §8.6 (one new
   row). F01.5, F08.1, the integrator guide and diagram 21 are unchanged.

## Not done here

- #22's three other files and the integrator-side `Synth 8-6901` count (hence "Relates to").
- #25's side note on pinning yosys and sv2v in the `portability` workflow. It is not in that
  issue's acceptance, and the workflow is unchanged.
- The other module-scope `$error` guards in `hdl/` (R449-1 S1): issue 151's scope.
- R449-2 S1: the parent's own census in `check_rtl_source_lists.py` still reads `.sv`
  text; a parent follow-up. R449-2 S2: `elab_bounds.sh`'s yosys leg runs only where yosys
  is installed, which the hosted `suites` job does not do (see "Round 3").

## Round 2

Round 2 answers R448-1 and R449-1, both NEGATIVE at `54f9411`. Five one-line commits
follow `54f9411`, with no rebase:

- `1a5f555`: the census;
- `6ba4659`: the derived bound;
- `522d49a`: the bench grades the class;
- `137ac73`: citations and wording;
- `cd08ca7`: run.sh's functions, for the parent's shell-idiom gate.

| Finding | Severity | Resolution | Evidence |
|---|---|---|---|
| R448-1 F1, R449-1 F1: with c10, the parent's `check_rtl_source_lists.py --selftest` fails 1 of 49 | MAJOR | the c10 patch replaces the "record is non-empty" arm with two arms on a synthetic population drawn from the live pin, and carries R449-1 R3's text | with c8 + p2 + c10 and this head: gate 3 rc 0 and its self-test rc 0 (50 of 50); every other self-test that opens either budget is rc 0 (traced, above) |
| R448-1 F2, R449-1 R2: three stale `KL_pp_nvm_port.sv` citations (R449-1 R2's is one of R448-1's) | MINOR | `:244-255`, `:376`, `:390` | the full moved set is in §2's table |
| R448-1 S1, R449-1 F3: the bound is a mirrored literal | SUGGESTION, MINOR | `MAXP_BOUND_C` from `$bits(dev_len_o)` and `HDR_LEN_C`, in the condition and the message. The port keeps every line in place. 65527 is left only in the bench | R449-1's `nvm_bound_probe.sh`, unchanged: `pristine` now equals its old `derived` row. `hdr10` gives `elab_bounds.sh` rc 1, `ELAB FAIL MAX_PAYLOAD_P=65527` ("is above 65525: 10 + it ..."). No logic: the yosys netlists at 1024 and 65527 and the Vivado OOC netlist are unchanged |
| R449-1 F4: `$error` and `$warning` pass the bench | MINOR | `elab_bounds.sh` requires `%Warning-USERFATAL` or `%Error` on the refusal line, plus the yosys leg | `err` and `warn` give rc 1 (were 0); `$error` with no sv2v or yosys on PATH also gives rc 1 |
| R449-1 F2: a split module header escapes the census | MINOR | declared modules are read from sv2v's all.v | R449-1's `yosys_fault.sh ... newmod`, unchanged: rc 1, `KL_r449_newmod` named (was rc 0). Its other 17 cases are unchanged row for row |
| R448-1 S2: `protocol_processor_top.sv:2714` | SUGGESTION | `:2726` (`:2731` since the round-3b merge) | the shadow instance's line |
| R449-1 R1: run.sh says "status files" | RESIDUE | the exact text | `run.sh:9-10` |
| R449-1 R3: `CODE_QUALITY.md:612-616` | RESIDUE | the exact text, in the c10 patch | |
| R449-1 S1: other module-scope `$error` guards | SUGGESTION | not this PR's (issue 151) | the deadline guard is still graded by name only |
| found in round 2: the parent's `check_sh_idiom.py` fails on `run.sh` (2 unquoted expansions, "top-heavy long script", 40% in functions) | adoption blocker | the census and the elaboration loop are functions, called where they ran, and their lists are quoted | the parent's scorer: 0 findings, 57% in functions; `check_sh_idiom.py` rc 0 with c8 + p2 and with c10 |

## Round 3

Round 3 answers R448-2 and R449-2, both NEGATIVE at `cd08ca7` on one shared MINOR. One
one-line commit follows `cd08ca7`, with no rebase: `b6f17f2`, the census and
`parse_site`.

| Finding | Severity | Resolution | Evidence |
|---|---|---|---|
| R448-2 F1 = R449-2 F1: a header with a leading attribute instance (`(* ... *) module X`, on one line or the attribute on the line before) escapes the census; `parse_site` names `module automatic` and attributed headers wrongly | MINOR | the declared set is yosys's own `select -list =*` of the `read_verilog -defer` design the gate elaborates, not a text pattern. `parse_site`, needed only when the parse fails and yosys has no list, reads past attribute instances and a lifetime keyword | below |
| R449-2 S1: the parent's own census reads `.sv` text | SUGGESTION | open: the parent's `check_rtl_source_lists.py`, out of this PR's scope | below |
| R449-2 S2: `elab_bounds.sh`'s yosys leg never runs hosted | SUGGESTION | open: the workflow is unchanged | below |

**Why yosys's list.** yosys lists deferred modules without elaborating them: under
`-defer` each parsed module is `$abstract\NAME`, and the same run that elaborates the
tops writes that list right after the parse. So the census needs no text extraction.
`select -list =*` and not `ls`: yosys 0.33, the hosted `portability` job's, drops black
and white boxes from `ls =*`, and `select -list =*` names them on 0.33 and 0.66. The census
runs on the first run's list before any verdict line, so a census failure prints exactly
the lines it printed before. The one change in output is that the `yosys allocator:` line
now comes first.

**The reviewers' probes, unchanged:**

- R448-2's `run_census_cases.sh`:
  - `c-attr-same` and `c-attr-own` give rc 1, naming `KL_r448_attrs` and `KL_r448_attro`.
  - `c-attr-own-top-clean` gives rc 0 (43 OK, parsed once, XILINX OK).
  - `c-attr-own-top` gives rc 1, `YOSYS FAIL KL_r448_attro: ...`.
  - `c-auto-split` is still rc 1 and still names `KL_r448_auto`, now through the parse
    failure (`unexpected TOK_AUTOMATIC`), which is the real blocker; a `tops` entry could
    not make it pass.
  - Every other row's log is identical to R448-2's receipt.
- R448-2's `parse_site_unit.sh` names `KL_first`, `KL_auto` and `KL_attr`, with gawk and
  with Ubuntu's mawk.
- R449-2's `census_probe.sh`: `attr` and `attrline` give rc 1, each named. `attr top` gives
  `YOSYS FAIL KL_r449_attr: ...`, and `allvauto` names `KL_r449_allvauto`. Every other form
  is red and named.
- R449-1's 21 fault cases, summarised by R449-2's own script: the table equals R449-2's
  `SUMMARY.md` row for row.
- R448-2's 24 gate cases, plus the fake exit-0 yosys and the fatal-class fault: every rc
  is equal. Every verdict line is equal; the only differences are the line order above
  and seven fewer loader complaints in the inherited-`LD_PRELOAD` case (the census's
  processes now run after that variable is unset).

**Mutants of this change**, each killed by its probe:

- `select -list *`, with no boxes: a `(* blackbox *)` module is missed.
- The census call removed, or round 2's text census: an attributed module is missed.
- Round 2's `parse_site`: `automatic` is named.
- The list line removed: the clean gate fails, `yosys parsed all.v but listed no module`.
- The census run when the parse failed: that module is no longer named.

**yosys 0.33** (Ubuntu 24.04, sv2v 0.0.13, mawk, the system allocator, as the hosted job):

- The clean head gives 42 OK, `parsed 1 time(s)` and XILINX OK.
- The attributed, blackbox, `automatic` and `all.v` syntax rows give the same verdicts as
  on 0.66.

**One parse, measured again.** Three interleaved rounds, end to end, on a busy shared host
(load average 27-34 on 16 CPUs):

| Revision | Median |
|---|---:|
| `cd08ca7`, jemalloc | 34.99 s |
| this head, jemalloc | 36.18 s |
| this head, `YOSYS_MALLOC=none` | 50.05 s |

All nine runs report `all.v parsed 1 time(s)` and print the same verdict lines.

**The scope, stated.** A module is counted when yosys parses it from `all.v`. That
includes every header layout, attribute instances and boxes. A module in an inactive
`` `ifdef `` is not counted, which round 1's `.sv`-text census did count. The `run.sh`
comments and §1 say so.

**Open suggestions.**

- **R449-2 S1.** The parent's `declared_modules()` still reads `.sv` text. Run on the same
  forms:
  - It agrees with this census on a plain header, a split header and an attribute on the
    line before.
  - It does not count an attribute on the header line, a comment before the name,
    `macromodule` or `(* blackbox *)`. Listing such a module passes both gates.
  - It names `module automatic X` as `automatic`.
  - It counts a module in an inactive `` `ifdef ``. This gate refuses that module in
    `tops`, so a parent budget record would be needed.

  No module here has any of these forms today.
- **R449-2 S2.** The hosted `suites` job has no yosys, so `elab_bounds.sh` prints
  `YOSYS SKIP` there. Its class check still kills `$error` and `$warning`.

**Gates at `b6f17f2`.**

- Processor, pinned Verilator 5.050:
  - `./scripts/run_suites.sh` rc 0: 33 suites, 1,020,253 checks, 0 failing.
  - `lint_hdl.sh` rc 0, 41 of 41. `make check` and `gen_matrix.py --check` rc 0.
  - `./syn/yosys/run.sh` rc 0: three runs with jemalloc and three with
    `YOSYS_MALLOC=none` (42 OK, parsed once, XILINX OK, identical verdicts), plus one
    under yosys 0.33.
  - `--selftest-alloc`: PASS.
- Parent consumers at milan-fpga `1269cdaf` + c8 + p2 + c10, in a scratch copy, with the
  processor gitlink at `b6f17f2`: the 17 gates above, all rc 0. That includes
  `check_rtl_source_lists.py` (42/42 tops, 0 recorded), its self-test (50 of 50),
  `check_sh_idiom.py` (the parent's scanner finds nothing in `run.sh`: 56% of it is inside
  functions) and `xvlog_gate.py --check` (run alone).
- Every other parent command that opens `run.sh` or a budget is rc 0:
  - `check_sh_idiom.py --selftest`;
  - `check_hygiene.py --check` and `--selftest`;
  - `check_todo_ownership.py` and `--selftest`;
  - `measure_fail_fast.py --check` and `--selftest`;
  - `check_entity_shape.py --self-test`;
  - `xvlog_gate.py --selftest`.
- The three parent patches are unchanged from round 2.

## Round 3b

Merge only, as assigned on #25 (5972322274). `39298e03` is a `git merge --no-ff` of
`main` `c4cb84ff` (PR #150, lane P1), parents `b6f17f2` and `c4cb84ff`. No follow-up
commit was needed.

**The merge.**

- One conflict, `tb/nvm_port/README.md:105-106`: both sides had moved the same two
  citations. They are re-derived at the merge: the writer's `frame_ok_w` at
  `KL_aecp_nvm_writer.sv:549-552` (P1's file) and the shadow instance at
  `protocol_processor_top.sv:2731` (this PR's reorder +1, P1's port comments +5).
- The other four files both sides changed (`protocol_processor_top.sv`,
  `tb/pp_top/sim_main.cpp`, `tb/pp_top/README.md`, `09_verification.md`) merged cleanly.
  The merge's diff against each parent has exactly the other side's changed lines, so
  both sides stand whole: this PR's declaration reorder and moved citations, and P1's name
  stage, D3 contract amendment and D3KR cuts.
- RTL: against `main`, the merge changes only this PR's two files (the top's reorder and
  the port's guard). Against round 3's head it changes exactly P1's RTL. The merge itself
  changes no logic, port or parameter meaning, and P1 added no module.
- Every line citation into a file both sides changed, and every `KL_pp_nvm_port.sv`
  citation, was checked at the merge against the text it names. Only the two conflicted
  ones moved. This body's citations follow (`README.md:1138`, `:2731`).
- Every ROM was regenerated at the base, both sides and the merge: `ucode.hex`,
  `ltn_rom.hex` and both descriptor images with their maps are byte-identical at all four.
  Neither side changed a generator.

**Re-measured at the merge** (pinned Verilator 5.050):

| Gate | Result |
|---|---|
| `./scripts/run_suites.sh` | rc 0: 33 suites, 1,021,449 checks = P1's recorded 1,021,423 + this PR's 26; `tb/pp_top` 10,416 = 10,390 + 26 |
| `lint_hdl.sh`; `make check`; `gen_matrix.py --check` | rc 0: 41 of 41; 1,114 links; 94 rows, 0 untested |
| `./syn/yosys/run.sh`, with jemalloc and with `YOSYS_MALLOC=none` | rc 0: 42 of 42 tops (P1 added none), the census from yosys's own list, `all.v parsed 1 time(s)`, XILINX OK; identical verdict lines |
| `tb/nvm_port/elab_bounds.sh` | rc 0: 4 ELAB OK, 6 GUARD OK, YOSYS OK |
| `make -C tb/nvm_port figures` | rc 0: all measured figures agree with the tree |
| `aecp_dispatch_mutants.py` | 4 controls PASS, 40 of 40 KILLED, this PR's three NSD arms among them |
| `aecp_mutants.py` | 5 controls PASS, 55 of 55 KILLED |
| `d3_mutants.py` (D3, D3V, D3KR, AD7 to AD9) | 6 goldens PASS, 110 of 110 KILLED |
| `notify_mutants.py` | 5 goldens PASS, 40 of 40 KILLED |
| `ctr_mutants.py` | control PASS, 17 of 17 KILLED |
| `acmp_mutants.py` | 3 goldens PASS, 19 of 19 KILLED |
| `gsi_mutants.py` | golden and restored PASS, 20 of 20 failed by their named checks |
| `name_wr_mutant.py` | golden and restored PASS, the mutant killed |
| `tb/adp_engine`, `tb/maap`, `tb/srp_top` `mutants.py` | 30 of 30 KILLED; 29 of 29 runs (27 arms); 78 KILLED, 11 controls PASS |

Every failing-check count equals its README record, arm for arm, P1's moved counts
included, so no record changes.

**Out-of-context** (Vivado 2026.1, `main` `c4cb84ff` against the merge, nothing else
running): the netlists (19,658,600 bytes) differ only in the `// Date` line, and the
utilization reports are identical. `Synth 8-6901` goes from 51 to 7. The reorder is still
netlist-neutral.

**Parent consumer set** at milan-fpga dev `1269cdaf`, in a fresh scratch copy, with the
processor at `39298e03`. PR #150 states that `parent-adoption-p2-p1-1269cdaf.patch`
replaces the p2 patch for P1's adoption, so this run applies c8, then **p2-p1**, then c10
(unchanged). All 17 gates are rc 0, as are their self-tests and the other parent commands
that open `run.sh` or a budget:

- The two p2 patches differ only in the parent's D3 page. The ten light gates give the
  same verdicts with either.
- Gate 5 counts 1,759 processor ports. The extra three are P1's internal ports, and the
  top keeps its 213.
- Gate 16 passes at this dev revision: T30 INTERNAL LAW measures 8.739 media ticks, inside
  8 < d/T <= 9. P1's two gate-16 failures (milan-fpga #643) were measured at dev `bbf704ec`.
- `check_doc_paths.py` (not one of the 17) still flags the p2 page's row W13, as in round
  2; p2-p1 keeps that row.

Supersedes #26, which can be closed when this merges.

