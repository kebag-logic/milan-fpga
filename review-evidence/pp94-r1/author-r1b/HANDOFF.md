[A250] Author handoff — PR #110 / issue #94, round 1b

Head: `cc077a6ffe20585d20b116f008e07189ba1bb7f8`  
Branch: `94-desc-mem-guard`  
Starting head: `4f525eb55b310d6b9bc2f1a000254cb2dd483665`  
Repository: `$LANES/pp94-desc-mem-guard`  
Parent consumer: `$LANES/pp94-parent-consumer`  
Parent commit: `5b2415f4e4eb8580c5512024f6c454ec482afd1b`  
Date: 2026-09-24

Implemented the three repairs in the
[round 1b assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/110#issuecomment-5811722803).
The parent Rules 11 and 12 were read in `docs/development/CODE_QUALITY.md`.
Original failures are preserved as [C++](parent-before-01.log),
[Python](parent-before-02.log), and [parent build](parent-before-07.log).

The guard keeps `debt_o` as its own documented D3 interface. There is no
`desc_mem_debt_o` port on `protocol_processor_top`. The product-top bench observes
`u_dut.u_desc_mem_guard.debt_o`; the parent instantiation needs no edit.
Guard/store RTL and all product-top stimulus and assertions are unchanged,
[verified against the starting head](preserved-contracts.txt).
The complete round diff is [round-1b.diff](round-1b.diff), and the updated diagram
was rendered and inspected: [descriptor-fetch.png](descriptor-fetch.png).

## Every flagged item: before and after

All C++ locations below refer to `tb/desc_mem_guard/sim_main.cpp` at the starting
head `4f525eb55b310d6b9bc2f1a000254cb2dd483665`. The original scanner sites are
saved in [before-findings.txt](before-findings.txt). The final local scan is
[after-local-findings.json](after-local-findings.json); the parent gates below
scan the complete consumed tree.

| C-style cast | Before | After (Rule 11 ES.49/ES.48) |
|---|---|---|
| 1, line 150 | `(unsigned long long)first.data` | `static_cast<unsigned long long>(first.data)` |
| 2, line 150 | `(unsigned long long)second.data` | `static_cast<unsigned long long>(second.data)` |
| 3, line 151 | `(unsigned long long)INPUT0` | `static_cast<unsigned long long>(INPUT0)` |
| 4, line 151 | `(unsigned long long)INPUT1` | `static_cast<unsigned long long>(INPUT1)` |
| 5, line 178 | `(unsigned long long)h.delayed_accept` | `static_cast<unsigned long long>(h.delayed_accept)` |
| 6, line 178 | `(unsigned long long)h.delayed_first` | `static_cast<unsigned long long>(h.delayed_first)` |
| 7, line 179 | `(unsigned long long)h.delayed_end` | `static_cast<unsigned long long>(h.delayed_end)` |
| 8, line 179 | `(unsigned long long)presented` | `static_cast<unsigned long long>(presented)` |
| 9, line 204 | `(unsigned long long)h.accepted` | `static_cast<unsigned long long>(h.accepted)` |
| 10, line 205 | `(unsigned long long)h.terminal` | `static_cast<unsigned long long>(h.terminal)` |

| File-scope mutable finding | Before | After (Rule 11 I.2) |
|---|---|---|
| Line 13 (one declaration, two counters) | `static int checks = 0, fails = 0;` | Separate `int checks = 0;` and `int fails = 0;` members of `TestResults`; `main` owns a local instance and passes it by reference to each case and harness. No mutable global or static-local replacement. |

| Multi-declarator finding | Before | After (Rule 11 ES.10) |
|---|---|---|
| 1, line 13 | `static int checks = 0, fails = 0;` | `int checks = 0;` and `int fails = 0;` in the owned result object |
| 2, line 26 | `bool valid = false, err = false;` | `bool valid = false;` and `bool err = false;` |
| 3, line 47 | `bool stuck, error;` | `bool stuck;` and `bool error;` |
| 4, line 50 | `uint64_t cycle = 0, accepted = 0, terminal = 0;` | Three separate `uint64_t` declarations, each initialized to zero |
| 5, line 51 | `uint64_t delayed_accept = 0, delayed_first = 0, delayed_end = 0;` | Three separate `uint64_t` declarations, each initialized to zero |
| 6, line 53 | `bool stuck_next = false, error_next = false;` | `bool stuck_next = false;` and `bool error_next = false;` |

The same new harness also had `unsigned beats, index;` and
`unsigned held_cycles = 0, overlap_accepts = 0;`. Both now use one declaration
per name, although the scanner did not include those unsigned declarations in
its six findings. Member order, initialization, stimulus, checks and output stay
the same. The full guard runtime output is
[byte-identical before and after](guard-runtime-comparison.txt).

| Python finding | Before | After (Rule 12) |
|---|---|---|
| `tb/desc_mem_guard/mutate.py:9`, unannotated public function | `def main():` | `def main() -> int:` |
| Same function, undocumented public function | No docstring | `Read CLI options and return 0 only when the completed byte check kills the mutant.` |

The controller still rejects build failures, crashes, a different assertion, or
an incomplete scenario; its return-code and exact wrong-byte checks are unchanged.

| Integration finding | Before | After |
|---|---|---|
| Parent build reports missing pin `desc_mem_debt_o` | `protocol_processor_top` exports a new debt output absent from the parent instantiation | Top-level output removed. The guard retains its own `debt_o` D3 port, connected to the local `desc_mem_debt_nc_w` tap. |
| Preserve product-top debt checks | Bench binds a product-top output | Bench assigns its observation output from `u_dut.u_desc_mem_guard.debt_o`. All five debt assertions and all product-top stimulus remain byte-for-byte unchanged. |
| Document the selected D3 seam | Architecture catalog, integrator guide and diagram claim a current top-level debt output | Catalog row removed; memory contract, integrator guide, bench README and diagram state that D3 will route the guard port to the top together with parent consumer changes. |

## Processor repository gate table

Every gate runs as a foreground subprocess, with a 7,200-second outer timeout and
no pipeline. [gates.jsonl](gates.jsonl) records the exact arguments, working
directory, return code and duration; [run_gate.py](run_gate.py) captures full logs.
Commands below run from the processor repository, except area which runs in the
output directory's `area/` directory.

| Command | rc | Result | Log |
|---|---:|---|---|
| `bash scripts/run_suites.sh` | 0 | 32 suites; 15,894 checks; zero failing (before repair) | [before-suites.log](before-suites.log) |
| `make -C tb/desc_mem_guard baseline` | 2 | Expected failure: 17 PASS / 1 FAIL; completed wrong-byte assertion; simulation rc 1 | [baseline-late.log](baseline-late.log) |
| `make -C tb/desc_mem_guard` | 0 | 77 PASS / 0 FAIL; includes never-ending burst, resets and handshake cases | [guard-suite.log](guard-suite.log) |
| `tb/desc_mem_guard/obj_dir/Vguard_sim --late-only` | 0 | 18 PASS / 0 FAIL; complete correct bytes and recovery | [guard-late.log](guard-late.log) |
| `python3 tb/desc_mem_guard/mutate.py --output $MANAGEMENT/2026-09-23/pp94-a250` | 0 | Control passes: hold-deleted simulation rc 1 / make rc 2, exact completed wrong-byte assertion detected | [mutant-controller.log](mutant-controller.log) |
| `bash scripts/run_suites.sh` | 0 | 32 suites; 15,894 checks; zero failing; output identical to pre-change sweep | [after-suites.log](after-suites.log) |
| `./scripts/lint_hdl.sh` | 0 | All RTL modules pass, including the guard and product top | [hdl-lint.log](hdl-lint.log) |
| `make check` | 0 | 41 Mermaid + 18 WaveDrom blocks; 838 links; 115 REQ rows / 17 GAP findings; 92 matrix rows / zero untested; exports current | [docs-check.log](docs-check.log) |
| `./syn/yosys/run.sh` | 0 | All 35 listed tops elaborate; engine target RAM inference assertions pass | [portability.log](portability.log) |
| `make -C tb/nvm_port figures` | 0 | 46 builds; all measured figures match documentation | [nvm-figures.log](nvm-figures.log) |
| `$WORKSPACE_HOME/Xilinx/2026.1/Vivado/bin/vivado -mode batch -source $LANES/pp94-desc-mem-guard/syn/ooc/desc_mem_guard_ooc.tcl -nojournal -log ooc.log` | 0 | 4 LUTs; 1 flip-flop; no RAM or DSP | [area.log](area.log) |
| `git diff --check` | 0 | No whitespace errors | [diff-check.log](diff-check.log) |

The full sweep output is [byte-identical](suite-comparison.txt) before and after.
The guard's full runtime output is also [byte-identical](guard-runtime-comparison.txt).
The never-ending burst returns five later locate errors, at most 4,102 cycles
against the 4,160-cycle bound, with debt retained and no extra accepted request.
The late burst is accepted at cycle 80, first responds at 6,080 and terminates at
6,083; the third locate is presented at 4,185 and held for 1,895 cycles without
an overlapping acceptance. The baseline and mutant complete the same scenario
and fail only the expected byte assertion.

Area reports: [util.rpt](area/util.rpt), [util_hier.rpt](area/util_hier.rpt),
[timing.rpt](area/timing.rpt), [ooc.log](area/ooc.log). Reference part:
`xc7a100tfgg484-2`, 10 ns OOC clock, all guard ports retained. The T9 estimate was
5 LUTs / 1 flip-flop; measured area is 4 / 1. The OOC timing report warns that
`HD.CLK_SRC` is unset; no routed timing or hardware validation is claimed.

## Parent repository gate table

The prescribed local fetch and detached checkout completed with rc 0:
[parent-submodule-update.log](parent-submodule-update.log).
No files were copied into the parent. Its submodule is at the final head.
The commands below run in `$LANES/pp94-parent-consumer`.

| Command | rc | Result | Log |
|---|---:|---|---|
| `python3 scripts/check_cpp_idiom.py` | 2 | REFUSED before scan: checkout differs from parent index gitlink | [parent-cpp-idiom.log](parent-cpp-idiom.log) |
| `python3 scripts/check_py_idiom.py` | 2 | REFUSED before scan: checkout differs from parent index gitlink | [parent-py-idiom.log](parent-py-idiom.log) |
| `python3 scripts/xvlog_gate.py --check` | 2 | REFUSED before scan: checkout differs from parent index gitlink | [parent-xvlog.log](parent-xvlog.log) |
| `python3 scripts/check_rtl_source_lists.py` | 0 | 106 files; all four consumer lists complete; 35/41 native tops with six recorded omissions | [parent-rtl-source-lists.log](parent-rtl-source-lists.log) |
| `python3 scripts/pp_srcs.py --check --selftest` | 0 | 45 tracked sources derived; self-test passes; no duplicated build source list | [parent-pp-srcs.log](parent-pp-srcs.log) |
| `make -C tb/verilator/pp_shadow -j8` | 0 | 371 checks; zero failures; RESULT: PASS | [parent-shadow.log](parent-shadow.log) |

### Pending permission: parent index pin

The parent commit and index still pin the starting head `4f525eb5`. Moving only
the submodule checkout produces a `+` status, which `scripts/code_quality_scope.py`
rejects before either idiom scan. `scripts/xvlog_gate.py` likewise requires its
index gitlink to match the checked-out source population; lines 666 onward
explicitly document that the index, rather than HEAD, is authoritative.
It also strips `GIT_INDEX_FILE` overrides, so a separate temporary index cannot
satisfy the actual gate. No gate or budget was altered or bypassed.

Permission has been requested to stage only the new parent gitlink temporarily,
run the gates, then restore the original index entry. This is outside the supplied
checkout-only exception, so it has not been done. Until approved and re-run, the
three rc 2 refusals are not passes and the requested all-green parent proof is
incomplete. A REVIEW READY comment has not been posted.

## Deferred to the D3 lane

D3 routes the guard's own `debt_o` to `protocol_processor_top` together with the
parent consumer changes. The D3 writer, restorable-owner hold, deadline-to-CLOSED
policy, 5,000/16,000-cycle rollback cases, stage-1-only/full-slot rollback cases and
owner-release mutant remain deferred. Store-only reset coverage proves only the
debt-retention seam, not rollback implementation or validation.

## Delivery state

One local commit with one subject line, no body or trailers:
`Keep descriptor debt on guard and fix parent idiom findings`.
No push, PR edit, merge, parent commit/push, delegation or hardware action was
performed. The processor working tree is clean. The parent source tree is
unchanged apart from the allowed submodule checkout and gate-generated build
artifacts. The final parent gitlink scan proof awaits the permission described
above. [PR-BODY.md](PR-BODY.md) is a full replacement body with the current gate
limitation stated explicitly.
