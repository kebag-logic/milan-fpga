[A518]
Closes #25
Closes #17
Closes #37
Relates to #22

Lane C10 (tooling): the four items of the assignment on #25, in their order. This PR
supersedes PR #26, whose branch `25-cover-every-module-and-stop-reparsing` is merged here
with `--no-ff`, its two commits kept. The lane adds no logic. Item 2 is an elaboration
guard. Item 3 is a reorder whose synthesized netlist, and so its out-of-context cost, is
unchanged. Item 4 adds a test arm. No port changed, no parameter changed its meaning, and
the microprogram is unchanged.

## 1. #25: every `hdl/` module is a Yosys top, and the design is parsed once

- **Merge** (`5c20350`). One conflict, in `syn/yosys/run.sh`. It is resolved to the
  branch's structure (the census, the allocator selection, the elaboration step) plus
  `main`'s `pipefail`, its sv2v-line comment and the three modules `main` gained since
  (`KL_aecp_desc_mem_guard`, `KL_pp_nvm_mgr_arb`, `KL_pp_acmp_lsn_admit`). `tops` now
  names all **42** declared modules, and the branch's census refuses a declared module
  with no top, and a top that names no declared module.
- **Parsed once** (`b5e3b97`). One yosys reads `all.v` once (`read_verilog -defer`),
  keeps it with `design -save`, and elaborates each top from a `design -load` of it, with
  the same `hierarchy -check; proc; opt_clean` as before. PR #26's 16-way pool, with one
  parse per top, is replaced. Each top's step is bracketed by two markers on stderr, so a
  failing top is named, with the log's first ERROR line. A fresh run then resumes at the
  next top, so a red gate still gives every top a verdict, in inventory order. A green
  gate parses exactly once, and says so (`YOSYS 42 tops, all.v parsed 1 time(s)`). A
  parse failure names the module of `all.v` that holds the cited line.
- The `synth_xilinx` / `select -assert-count 6 t:RAMB36E1` regression is unchanged and
  passes.

**Red on a broken new top, naming it.** Each case is a scratch copy, with an instance of
an undeclared module planted before the module's `endmodule`:

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

At `main`, `KL_pp_dispatch` instantiates `KL_pp_dispatch_fifo`, so five of the six were
uncovered, not six.

**Wall time and top count**, end to end (sv2v, elaboration and the XILINX regression).
Each run was alone on the same host, three interleaved rounds, median:

| Revision | Tops | Median of three | Rounds |
|---|---:|---:|---|
| `main` `f4167536` (one yosys per top, full re-parse) | 36 | **88.80 s** | 83.30, 90.51, 88.80 |
| PR #26's pool, as merged (`5c20350`) | 42 | 30.00 s | 28.70, 30.00, 30.04 |
| **this head (parsed once)** | **42** | **35.97 s** | 35.97, 34.24, 36.57 |
| this head, `YOSYS_MALLOC=none` | 42 | 48.12 s | 51.22, 48.12, 45.66 |

The elaboration step alone, on one staged `all.v`, takes 50.89 s for `main`'s 36
per-top runs and 10.00 s parsed once for 42 tops. The verdict lines are identical across
the merge, the head and the head on the system allocator; only the new `parsed` line
differs.

## 2. #17: `MAX_PAYLOAD_P` above 65527 fails elaboration, naming the bound

`KL_pp_nvm_port.sv:192-200`: `if (MAX_PAYLOAD_P > 65527) begin : g_maxp_check
$fatal(1, "KL_pp_nvm_port: MAX_PAYLOAD_P=%0d is above 65527: 8 + it overflows dev_len_o",
...)`. This is `KL_pp_acmp_listener.sv:344-347`'s `$fatal(1, ...)`, placed at module scope
like the port's own `MEM_TIMEOUT_CYC_P` guard and every other elaboration guard in
`hdl/`. That placement was measured, not assumed:

| `MAX_PAYLOAD_P` = 65528 | in an `initial` block (the precedent's placement) | at module scope (this change) |
|---|---|---|
| Verilator 5.050 lint and build | rc 0: built, stops only at time 0 | rc 1, `%Warning-USERFATAL ... MAX_PAYLOAD_P=65528 is above 65527 ...` |
| sv2v + Yosys 0.66 | rc 1 | rc 1, at the guard's line (Yosys prints no `$display` text) |
| Vivado 2026.1 `synth_design -rtl` | rc 1 | rc 1, `[Synth 8-6058] Synth Error: KL_pp_nvm_port: MAX_PAYLOAD_P=65528 is above 65527 ...` |

At 65527 all three elaborate. `tb/nvm_port/elab_bounds.sh`, which `make` in `tb/nvm_port`
runs, now also lints 1024 and 65527 clean, and refuses 65528, 65535 and 2^32 - 1 by name
and bound. Five mutants each turn it red: the guard deleted, the bound moved to 65528, the
bound moved to `>= 65527`, the message without the bound, and the `initial` placement.
The guard moves the port's lines down by ten. The nvm_port figures gate caught that in its
line-keyed ARMS table, and `54f9411` moves the table and the three line ranges cited in
comments with it.
The top does not override the parameter, so this is elaboration-only: the OOC cost is
unchanged (below).

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

`syn/ooc/protocol_processor_ooc.tcl`, Vivado 2026.1, each run alone, base `f4167536` and
head (the head's `hdl/` is `34b5246`'s):

| Resource | Base | Head | Delta |
|---|---:|---:|---:|
| Slice LUTs | 30,658 | 30,658 | 0 |
| Registers | 31,944 | 31,944 | 0 |
| LUT as distributed RAM | 1,222 | 1,222 | 0 |
| F7 / F8 muxes | 1,482 / 57 | 1,482 / 57 | 0 |
| RAMB36 / RAMB18 / DSP | 23 / 2 / 4 | 23 / 2 / 4 | 0 |

Equal, as required, and the netlist itself is identical. Both builds have the same OOC
slack, so this makes no timing claim.

## Validation

All with the pinned Verilator 5.050, at the head:

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | 33 suites, **1,020,253** checks, 0 failing. `tb/pp_top` 9,196 to 9,222 (+26: NSD's 13 in the default and line builds). `main` swept on the same host: 1,020,227, and `tb/pp_top` is the only suite whose tally differs |
| `./scripts/lint_hdl.sh` | 0 | 41 of 41 |
| `make check` | 0 | 41 mermaid + 18 wavedrom blocks, 1,105 links, 115 REQ rows, 17 GAP findings, 94 module rows 0 untested, 28 parameters |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `./syn/yosys/run.sh` | 0 | 42 of 42 `YOSYS OK`, parsed once, `YOSYS XILINX OK` |
| `./syn/yosys/run.sh --selftest-alloc` | 0 | PASS |
| `make -C tb/nvm_port figures` | 0 | all measured figures agree with the tree (160 builds) |
| `aecp_dispatch_mutants.py --jobs 6` | 0 | 4 controls PASS, 40 of 40 KILLED |
| `aecp_mutants.py --jobs 6` | 0 | 5 controls PASS, 55 of 55 KILLED |
| `tb/srp_top`, `tb/maap`, `tb/adp_engine` `mutants.py --jobs 6` | 0, 0, 0 | 90, 32, 32 checks, 0 FAIL |

The five campaigns are the HDL workflow's own; they ran at `8473c04`, and only
`tb/pp_top/README.md` and `tb/nvm_port/` have changed since, which none of them builds.

**Parent consumer set (16)** at milan-fpga dev `1269cdaf`, in a scratch copy: a `git
archive` of dev (984 index entries, tree identical), gptp-processor `5dce647a` and
verilog-axis `48ff7a7e` at their pins, and protocol-processor at this head with its gitlink
recorded. `parent-adoption-c8-cdf49d1a.patch`, then `parent-adoption-p2-cdf49d1a.patch`,
were each applied after a clean `git apply --check`:

| # | Command | c8 + p2 | + c10 | Result |
|---:|---|---:|---:|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | 0, 0 | 0, 0 | every ratchet held: long function 0 <= 0, build without warnings 0 <= 0, long module 10 <= 10 |
| 3 | `check_rtl_source_lists.py` | **1** | 0 | c8 + p2: six `STALE RECORD`, one per new top; + c10: `protocol-processor 42/42 tops, 0 recorded` |
| 4 | `pp_srcs.py --check --selftest` | 0 | 0 | 46 sources derived, self-test passed |
| 5 | `check_port_contracts.py` | 0 | 0 | processor 1,756 ports, unchanged; undocumented 111 <= 111 |
| 6, 7 | `measure_naming.py --check`, `measure_test_evidence.py --check` | 0, 0 | 0, 0 | 96 recorded; 72 <= 77, 0 <= 0 unexplained DUT readers |
| 8 | `docs_check.py` | 0 | 0 | 0 findings |
| 9 | `xvlog_gate.py --check` (alone, last) | **1** | 0 | c8 + p2: `BANK IT: protocol_processor_top.sv\|VRFC 10-3380\|srp_class_a_prio_w no longer occurs`; + c10: `PASS (3 finding(s) == ratchet)` |
| 10, 11 | `sw/builder/test_builder.py`, `lint_rtl.py --check` | 0, 0 | -, 0 | all gates pass except gate 11, not run (it needs a local build tree, as before); 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j16` | 0 | - | 606, 646, 606 and 311 checks, 0 failures |
| 13, 14 | `make -C tb/verilator/nvm_cosim lint`, `quick` | 0, 0 | - | pass; 315 of 315 |
| 15 | `make -C tb/verilator/milan_dp -j16 VERILATOR_JOBS=3` | 0 | - | 9 RESULT: PASS; the mutant arms caught |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | 0 | - | 0 failures; 5 of 5 leg-defect arms caught |

With the two named patches, gates 3 and 9 fail **by the parent's design**, on this PR's
two intended effects. The parent's tops budget says the pin bump that names its six
modules as tops deletes their lines, and its xvlog ratchet fails on a finding that no
longer occurs until the fix is banked. `parent-adoption-c10-1269cdaf.patch` (2,764 bytes,
after c8 then p2) is exactly that bookkeeping: it deletes the six budget lines and
regenerates `scripts/xvlog.budget` with a normal `xvlog_gate.py` run. With it, gates 1-9
and 11 re-ran rc 0. Gates 10 and 12-16 read neither file, so their results stand.

## Parent-visible list

1. **No port, parameter or register change** of `protocol_processor_top`.
   `KL_pp_shadow` needs no edit.
2. **Adopting this head needs `parent-adoption-c10-1269cdaf.patch`** after c8 and p2: the
   six `processor_yosys_tops.budget` lines go, and the xvlog ratchet banks
   `protocol_processor_top.sv`. `KL_pp_shadow` synthesis drops the 44 `Synth 8-6901`
   warnings from that file; 7 remain, in the three files #22 still names.
3. `KL_pp_nvm_port` refuses `MAX_PAYLOAD_P` above 65527 at elaboration. Nothing in the
   parent sets it.
4. The ROM generators are unchanged from `main`, so the ROM digests are `main`'s, and the
   OOC netlist is identical to `main`'s.
5. Processor documents the parent reads: 09 §8.1 (clock_source row) and §8.6 (one new
   row). F01.5, F08.1, the integrator guide and diagram 21 are unchanged.

## Not done here

- #22's three other files and the integrator-side `Synth 8-6901` count (hence "Relates to").
- #25's side note on pinning yosys and sv2v in the `portability` workflow. It is not in that
  issue's acceptance, and the workflow is unchanged.

Supersedes #26, which can be closed when this merges.
