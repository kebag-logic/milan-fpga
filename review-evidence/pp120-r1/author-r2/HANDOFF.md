# [A334] Round 2 handoff

Status: review ready. All repository gates and all 12 prescribed consumer commands returned rc 0.

Repository: `Mister-M-alt/protocol-processor-control-plane-avb-milan`  
Origin confirmed: `https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git`  
Branch: `120-name-wr-export`  
Starting head: `691f1d2b3a73705a50a8f827e2bb16837dc0dcdc`  
Final head: `a9b7874d415d935949becd7ccfd58799927efb08`  
Commit: `Clarify name-write contracts and split acceptance scenarios`

Assignment: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/120#issuecomment-5845451831

## Changes

1. `tb/pp_top/sim_main.cpp:9593`: introduce `NameWritePhase`; counting (`:9602`), SET/readback (`:9614`), accepted writes (`:9642`), refusals (`:9650`) and stall/abort recovery (`:9698`) are short helpers. `run_name_writes` at `:9744` retains boot setup and the scenario order. Commands, assertions and tally output are preserved.
2. `tb/pp_top/name_wr_mutant.py:14` and `:23`: document both public functions. Remove the process deadline; the completed simulation, return status and required named failures determine the verdict. DUT-cycle budgets remain in the harness.
3. `hdl/aecp/KL_aecp_desc_store.sv:185`: document the accepted live name lane, clock edge, qualifying request signals and boot exclusion.
4. `hdl/aecp/KL_aecp_engine.sv:529`: document the direct store event separately from the existing effect-strobe bundle. The trailing comment on the added port had interrupted that bundle; restoring it removes all ten newly undocumented engine ports.
5. `hdl/top/protocol_processor_top.sv:648`: retain the complete standalone contract for the exported event, removing the short trailing comment that obscured it in the shared parser.
6. `tb/pp_top/pp_top_wrap.sv:321` and `:325`: document both the exported event and the independent RAM-enable observation, with explicit clock, acceptance, boot and handshake semantics.

All four assignment items are complete. No RTL tokens changed after comment/whitespace removal. The focused pre/post output is byte-identical: **85 checks, zero failures**. The full suite retains **1,014,722 checks, zero failures**. The mutation campaign builds all three variants: golden and restored return 0; decode returns 1 with the required multi-lane, locked and aborted-write failures. The campaign itself returns 0.

## Consumer setup and results

The private clone was made with `git clone -q --no-hardlinks $LANES/pp120-parent-consumer /tmp/pp120-consumer-check`, checked out at `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`, and given the supplied `pp120-parent-open-port.patch`. Its processor gitlink was staged at the final head above; no parent commit was made. The local consumer dependency copies were initialized at their pins: gPTP `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, AXIS `48ff7a7e2ef782cf778d47910cf85835c64b1bce`.

The commands below are exactly the argv following each env prefix in the supplied consumer JSON. They ran from that clone, in the prescribed order, with the supplied environment and pinned simulator version 5.050. Every command ran in the foreground without an output pipeline. [Setup evidence](consumer-setup.log) records the base, staged gitlink and patch hash.

| No. | Command | rc | Evidence |
| ---: | --- | ---: | --- |
| 01 | `python3 scripts/check_cpp_idiom.py` | 0 | [01.log](consumer/01.log) |
| 02 | `python3 scripts/check_py_idiom.py` | 0 | [02.log](consumer/02.log) |
| 03 | `python3 scripts/xvlog_gate.py --check` | 0 | [03.log](consumer/03.log) |
| 04 | `python3 scripts/check_rtl_source_lists.py` | 0 | [04.log](consumer/04.log) |
| 05 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | [05.log](consumer/05.log) |
| 06 | `python3 sw/builder/test_builder.py` | 0 | [06.log](consumer/06.log) |
| 07 | `make -C tb/verilator/pp_shadow -j8` | 0 | [07.log](consumer/07.log) |
| 08 | `python3 scripts/check_port_contracts.py` | 0 | [08.log](consumer/08.log) |
| 09 | `python3 scripts/measure_naming.py --check` | 0 | [09.log](consumer/09.log) |
| 10 | `python3 scripts/measure_test_evidence.py --check` | 0 | [10.log](consumer/10.log) |
| 11 | `python3 scripts/docs_check.py` | 0 | [11.log](consumer/11.log) |
| 12 | `python3 scripts/lint_rtl.py --check` | 0 | [12.log](consumer/12.log) |

Consumer findings resolved: processor undocumented ports are **111 <= 111**, with no new undocumented debt; unexplained DUT-source readers are **0 <= 0** and wall-clock-dependent suite files are **3 <= 3**. The integration suite passes all three builds, each with 402 checks and zero failures.

Coverage limit: command 06 returns 0 but reports one utilization-calibration arm not run because its external implementation report is absent. No hardware work was performed; this result does not claim coverage of that arm.

Setup recovery: the first attempt to initialize every submodule stopped on the unavailable local `external` repository, leaving two cloned dependencies without working files. The three available consumer dependencies were fully checked out from their local copies, then all 12 commands were restarted. The incomplete attempt is retained separately in `consumer-incomplete-checkout/`; the table above and `consumer/results.json` are the final complete run. No source or gate was altered for this repair.

## Repository gate table

All commands below returned rc 0. Logs are relative to this evidence directory.

| Command | rc | Evidence |
| --- | ---: | --- |
| `make -C tb/pp_top gsi-build` | 0 | [name-build.log](name-build.log) |
| `./obj_dir/Vpp_top_sim --name-writes-only` | 0 | [name-run.log](name-run.log) |
| `make check` | 0 | [make-check.log](make-check.log) |
| `scripts/run_suites.sh` | 0 | [suites.log](suites.log) |
| `scripts/lint_hdl.sh` | 0 | [lint.log](lint.log) |
| `syn/yosys/run.sh` | 0 | [yosys.log](yosys.log) |
| `python3 scripts/check-integrator-params.py` | 0 | [params.log](params.log) |
| `python3 scripts/check-links.py` | 0 | [links.log](links.log) |
| `python3 scripts/check-matrix.py` | 0 | [matrix.log](matrix.log) |
| `python3 scripts/render-wavedrom.py --check` | 0 | [wavedrom.log](wavedrom.log) |
| `make stale` | 0 | [stale.log](stale.log) |
| `python3 scripts/gen_matrix.py --check` | 0 | [modmatrix.log](modmatrix.log) |
| `git fetch --no-tags origin refs/pull/13/head` | 0 | [history.log](history.log) |
| `make -C tb/nvm_port figures` | 0 | [figures.log](figures.log) |
| `python3 tb/pp_top/name_wr_mutant.py --output name-mutation/` | 0 | [name-mutation.log](name-mutation.log) |
| `git diff --check` | 0 | [diff-check.log](diff-check.log) |

The focused simulation runs from `tb/pp_top`; the other repository commands run from the repository root. The mutation output argument above is shown relative to this evidence directory. The historical figure gate completed 46 builds with every measured figure matching the documentation. The synthesis gate includes the engine memory-mapping assertions. Both working-tree and committed-change whitespace checks passed.

## Final state

- The repository worktree is clean, with one local commit beyond the supplied head. Its message is one line, with no body or trailers.
- The throwaway consumer clone and both temporary orchestration scripts were deleted; see [cleanup.log](cleanup.log).
- `PR-BODY.md` contains the full current PR body with the requested first line and Round 2 update, including the coverage limit and `Closes #120`.
- No push, PR edit, merge, parent-repository commit or hardware operation was performed.
- Final state checks are recorded in [final-verification.log](final-verification.log).
