# Issue #120 handoff

Status: donor implementation committed and all donor gates pass. Full issue acceptance is NOT met: the unmodified parent strict suite and lint reject its omitted output connection, and parent edits are prohibited.
Role: author [A329].
Branch: `120-name-wr-export`.
Base: `0922e43408f891fc0b84a84691df86b4fd0f1c0d`.
Head: `691f1d2b3a73705a50a8f827e2bb16837dc0dcdc`.
Origin verified: `https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git`.

## Scope

Export `aecp_name_wr_o` from actual descriptor-store live name write acceptance. Preserve all existing behavior and NVM mark timing. Document the contract and prove accepted, multi-beat, refused, aborted and out-of-range cases, including a decode-driven mutant.

## Change list

- `hdl/aecp/KL_aecp_desc_store.sv`: export the existing accepted live name-lane enable.
- `hdl/aecp/KL_aecp_engine.sv`, `hdl/top/protocol_processor_top.sv`: pass acceptance to the one new top output, without registers or changed effects.
- `docs/guides/integrator.md`, `docs/architecture/02_interfaces.md`: document the accepting edge, per-lane meaning, refusal/abort behavior and unchanged completion mark.
- `tb/pp_top/`: independent lane-count/readback tests, per-cycle RAM-enable timing check, decode-driven mutation runner.

File references:

| File:line | Change |
| --- | --- |
| `hdl/aecp/KL_aecp_desc_store.sv:185` | Internal output; acceptance assignment at line 454 and RAM enable at line 542 |
| `hdl/aecp/KL_aecp_engine.sv:530` | Engine output; store connection at line 1625 |
| `hdl/top/protocol_processor_top.sv:648` | Clock/acceptance/open-connection contract and the only new top output; engine connection at line 3470 |
| `docs/guides/integrator.md:318` | Integrator contract |
| `docs/architecture/02_interfaces.md:547` | Top contract table and live-write/completion distinction |
| `tb/pp_top/pp_top_wrap.sv:321` | Export and independent actual-RAM-enable tap |
| `tb/pp_top/sim_main.cpp:1175` | Per-edge sample; acceptance scenarios start at line 9593 |
| `tb/pp_top/Makefile:61` | Focused test entry; also in default suite |
| `tb/pp_top/name_wr_mutant.py:14` | Foreground build/run, exact decode substitution, required named failures, golden/restored controls |
| `tb/pp_top/README.md:25` | Coverage, reproduction and mutation contract |
| `tb/desc_mem_guard/wrap.sv:41` | Connect the unused store export in the existing strict read-only harness |

## Tests and mutation

| Check | Result | Evidence |
| --- | --- | --- |
| Golden focused acceptance tests | PASS: 85 checks, 0 failures | `name-writes.log` |
| One changed lane / eight changed lanes / unchanged name | PASS: 1 / 8 / 0 pulses, exact readback, single-cycle width and mark ordering | `mutant/golden-run.log` |
| Lock, semantic-index, descriptor, configuration, unnamed and short-body refusals | PASS: 0 pulses | `mutant/golden-run.log` |
| Held fetch then release | PASS: 0 pulses while held, 8 on accepted lanes | `mutant/golden-run.log` |
| Watchdog abort and late-response recovery | PASS: 0 pulses or marks; previous name retained | `mutant/golden-run.log` |
| Boot/read/idle controls and RAM acceptance edge alignment | PASS | `mutant/golden-run.log` |
| Decode-driven mutant | PASS: build rc 0, simulation rc 1 with 34 failed checks; required EIGHT, LOCKED and ABORT count checks fail; golden/restored 85/85 | `mutant/results.json` |

## Area

Complete default-shape `protocol_processor_top`, all ports present, identical conversion and `synth_xilinx -family xc7` recipes on base and changed RTL:

| Resource | Before | After | Delta |
| --- | ---: | ---: | ---: |
| LUT primitives | 66,461 | 66,439 | -22 |
| Estimated logic cells | 52,202 | 52,195 | -7 |
| Registers | 32,462 | 32,462 | 0 |
| RAMB36 / RAMB18 | 16 / 1 | 16 / 1 | 0 |
| Distributed RAM32M / RAM64M | 1,645 / 3 | 1,645 / 3 | 0 |
| DSP | 4 | 4 | 0 |
| Output buffers | 5,450 | 5,451 | +1 |

This is synthesis mapping, not placed area or hardware timing. Small LUT variation is not a logic-saving claim. See `area.json` and `area-before.log` / `area-after.log`. Source conversion and ROMs remain in temporary build directories, outside this output directory.

## Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| make check | PASS rc 0, including final contract wording | `final-make-check.log` |
| scripts/run_suites.sh | PASS rc 0, 1,014,722 checks, zero failing suites; pp_top 7,751 checks | `suites-final.log` |
| scripts/lint_hdl.sh | PASS rc 0 | `lint.log` |
| Repository Yosys gate | PASS rc 0 | `yosys.log` |
| python3 scripts/gen_matrix.py --check | PASS rc 0, 92 rows, 0 untested | `matrix.log` |
| python3 scripts/check-integrator-params.py | PASS rc 0, all 24 parameters | `parameters.log` |
| Workflow documentation gates | PASS rc 0, including NVM figures after required historical PR ref fetch | `docs-matrix.log`, `wavedrom.log`, `stale.log`, `nvm-figures-with-history.log` |
| python3 scripts/check-links.py | PASS rc 0, 915 links | `links.log` |
| git diff --check | PASS rc 0 | `diff-check.log` |
| Parent consumer Yosys, output omitted | PASS rc 0, both integration tops | `consumer-yosys.log` |
| Parent datapath ax1x1, output omitted | PASS rc 0, 231 checks | `consumer-milan-ax1x1.log` |
| Parent consumer strict suite and lint, output omitted | BLOCKED: rc 2 / rc 1; new output raises PINMISSING and parent edits are prohibited | `consumer-pp-shadow.log`, `consumer-lint.log` |

## Parent compatibility

Parent source export: `kebag-logic/milan-fpga` at the prerequisite report head `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`; gPTP `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. Sources and builds live outside this output directory. No additional checkout was created.

With the new donor output omitted by the parent, both integration tops pass the parent elaboration gate and `make -C tb/verilator/milan_dp ax1x1` passes 231 checks. `make -C tb/verilator/pp_shadow` fails with exactly one fatal PINMISSING warning at `hdl/milan/KL_pp_shadow.sv:1072`. Parent lint reports three findings against a two-finding budget, the added one being the same missing pin. An explicit open `.aecp_name_wr_o()` in a temporary validation export was requested, but no authorization was received. The original no-parent-edits constraint is retained. There is no claim that the strict consumer gates passed; these remain the acceptance gap. No parent source has been changed. `consumer-source-audit.json` compares every exported parent HDL file with the pinned archive.

## Validation environment and reproduction

Simulation/lint version 5.052; synthesis version 0.66; source conversion v0.0.13. The repository requires simulation >=5.050. Commands run in the foreground, without a pipeline around any gate; each `.rc` file is the command result. The gate wrapper gives each process up to four hours and directs output to a log. Temporary build copies do not reside in this directory.

Area recipe (both sides): all HDL converted together, packages first and sorted; generate the existing two ROM images; `read_verilog all.v; hierarchy -check -top protocol_processor_top; synth_xilinx -family xc7 -top protocol_processor_top; stat`. The base was measured in this checkout before editing. Converted-source and ROM digests are in `area-inputs.json`; ROM digests match. The area counts include the complete hierarchy, not just the top's own cells.

The first `nvm_port figures` invocation lacked the historical PR #13 lineage required in `.github/workflows/hdl.yml`. It failed its source-form provenance checks. The workflow's `git fetch --no-tags origin refs/pull/13/head` succeeded, and the unchanged gate passed with rc 0. Both logs are retained.

## Delivery

Local commit: `691f1d2b3a73705a50a8f827e2bb16837dc0dcdc` — `Export accepted live name writes at processor top`. One-line subject, no body or trailers. Worktree clean; both worktree and base-to-head whitespace checks pass. `PR-BODY.md` is ready locally and explicitly records the consumer acceptance gap.

`REVIEW-COMMENT.md` contains the final authorized notification for issue #120, with this head and the consumer blocker. Its posted URL is recorded in `review-comment.url` when the post succeeds.

No push, PR operation, merge, additional checkout, hardware operation or parent source edit was performed. The initial donor sweep failed only because the existing descriptor-memory guard test wrapper omitted the new internal store output; that connection was fixed and the full sweep rerun successfully. Initial failed logs remain for audit.

Review-ready notification posted: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/120#issuecomment-5845319119
Stopped after the authorized issue notification.
