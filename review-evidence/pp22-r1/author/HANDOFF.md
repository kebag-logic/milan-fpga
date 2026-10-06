# Issue 22 declaration ordering handoff

Status: REVIEW READY. Role: author. Branch: `pp22-decl-order`.
Base: `e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8`.
Head: `2139f3dc10161b456dfbd51d2f73a63f9164e041`.
Commit subject: `Move packet-engine declarations above their first use`.
One-line subject, no body or trailers. Local commit only; no push or pull request creation.

## Assignment and provenance

The origin URL was verified as the assigned processor repository; starting HEAD and branch matched the assignment and the worktree was clean. Read the processor README, both edited modules, the full issue and its three pre-existing comments, including exact assignment comment `6008772151`, and the declaration moves in PRs 149 and 153. TAKEN was posted as comment `6008785364`. No existing issue or pull request comment was edited or deleted.

Only declaration moves are permitted in the processor. The change contains exactly four existing declaration lines moved within their modules, plus their existing separating blank line. Both modules' complete line multisets are unchanged. Ports, parameters, registers, executable statements and declaration initializers are unchanged. No stop condition was triggered.

The original issue includes a vendor synthesis warning criterion. This assignment explicitly prohibits vendor synthesis and implementation, so neither was run. The review body uses `Relates to #22`; it does not claim that unmeasured acceptance item.

## Declaration inventory

| File | Declarations | Base line | Head line |
|---|---|---:|---:|
| `hdl/packet_engine/KL_pp_originator.sv` | `cancel_hit_w` | 236 | 188 |
| `hdl/packet_engine/KL_pp_originator.sv` | `cancel_ix_w` | 237 | 189 |
| `hdl/packet_engine/KL_pp_rx_validator.sv` | `fifo_ne_w`, `fifo_full_w`, `vq_ne_w`, `vq_full_w` | 621 | 232 |
| `hdl/packet_engine/KL_pp_rx_validator.sv` | `push_w`, `vd_push_w`, `vd_val_w`, `rd_fire_w`, `retire_w` | 623 | 233 |

Grouped declaration statements remain intact. `vq_full_w` shares the validator's first-use site with `vd_push_w`. Originator first uses move from lines 194/195 to 197/198; the validator's first use moves from line 383 to 385.

## Patch-context search and mutation planting

Before editing, the following command ran separately for each complete declaration line in the table. All four returned 1, meaning no fixed-string match; no patch context needed a refresh.

```sh
git grep -n -F -- '<entire declaration line>' 'tb/**/*.patch' 'tb/**/*.py'
```

The source-name search identified and the author read:

- `tb/maap/mutations/validator-maap-version-1-only.patch`
- `tb/pp_top/notify_mutants.py`
- `tb/pp_top/acmp_mutants.py`
- `tb/pp_top/d3_mutants.py`

After the move, every tracked patch passed `git apply --check`; each exact-text arm was planted independently in fresh scratch files through its table's own `plant()` function. No edit-count refusal occurred.

| Population | Planting checks | Passed |
|---|---:|---:|
| `tb/**/*.patch` | 277 | 277 |
| notification table | 56 | 56 |
| ACMP table | 33 | 33 |
| D3 table | 110 | 110 |
| Total | 476 | 476 |

These are planting results, not mutation-kill claims. The four affected originator arms and four validator arms retain their original exact source text. No test or mutant file changed.

## Execution environment and isolation

Pinned Verilator 5.050 was exported in `VERILATOR` and placed before the host default in PATH. Processor runs inherited `MAKEFLAGS=-j16`; direct make invocations use `-j16`. Parent heavy builds limit translation/build workers to two where supported; the shadow build uses a scratch make include to replace only `--build -j 0` with `--build -j 2`. Two independent parent heavy consumers run concurrently, alongside the builder, analysis and light gates. Processor base/head gates also run concurrently, each with its own log and return-code file. No suite or gate command was piped.

Scratch root: `$VALIDATION_STORAGE/pp22-a546`. Processor suite/lint/matrix/portability inputs are plain `git archive` exports, not additional checkouts; `make check` runs in the real lane at the respective revision. Generated products, dependencies, large logs and lowered netlists stay under the scratch root. The processor worktree contains only committed source. All commands remain supervised by foreground runners; no work is detached. No hardware, bench, flashing, vendor synthesis or implementation was used.

## Processor gates and records

| Command | Base rc | Head rc | Comparison |
| --- | --- | --- | --- |
| `scripts/run_suites.sh` | 0 | 0 | byte-identical log |
| `scripts/lint_hdl.sh` | 0 | 0 | byte-identical log |
| `make -j16 check` | 0 | 0 | identical records (sorted; concurrent recipe order varies) |
| `python3 scripts/gen_matrix.py --check` | 0 | 0 | byte-identical log |
| `syn/yosys/run.sh` | 0 | 0 | identical 42 top verdicts, census and memory-mapping verdict |

| Suite | Base checks | Head checks | Result |
| --- | --- | --- | --- |
| acmp_listener | 3111 | 3111 | identical |
| acmp_nvm | 388 | 388 | identical |
| acmp_talker | 1342 | 1342 | identical |
| adp_engine | 1348 | 1348 | identical |
| aecp_notify | 45 | 45 | identical |
| ca_originator | 16 | 16 | identical |
| desc_mem_guard | 78 | 78 | identical |
| desc_store | 586 | 586 | identical |
| dispatch | 211 | 211 | identical |
| dyn_state | 118 | 118 | identical |
| event_router | 81 | 81 | identical |
| lsn_admit | 18 | 18 | identical |
| maap | 196 | 196 | identical |
| nvm_port | 1219 | 1219 | identical |
| originator | 107 | 107 | identical |
| pp_top | 10444 | 10444 | identical |
| prng | 76 | 76 | identical |
| release_merge | 18 | 18 | identical |
| resp_buf | 64 | 64 | identical |
| rx_slots | 130 | 130 | identical |
| rx_validator | 555 | 555 | identical |
| scoreboard | 3705 | 3705 | identical |
| side_port | 368 | 368 | identical |
| srp_admission | 991231 | 991231 | identical |
| srp_decoder | 190 | 190 | identical |
| srp_encoder | 581 | 581 | identical |
| srp_stream_fsms | 1219 | 1219 | identical |
| srp_top | 2200 | 2200 | identical |
| timer_map | 1360 | 1360 | identical |
| timer_service | 48 | 48 | identical |
| tx_arbiter | 66 | 66 | identical |
| tx_slots | 95 | 95 | identical |
| ucpu | 437 | 437 | identical |

base: `suites: 1021651 checks total, 0 failing`.

head: `suites: 1021651 checks total, 0 failing`.

Per-build retained records (`checks failures`, build order):

| Suite | Base | Head | Comparison |
| --- | --- | --- | --- |
| acmp_nvm | 372 0; 16 0 | 372 0; 16 0 | identical |
| aecp_notify | 41 0; 4 0 | 41 0; 4 0 | identical |
| nvm_port | 393 0; 393 0; 393 0; 10 0; 10 0; 10 0; 10 0 | 393 0; 393 0; 393 0; 10 0; 10 0; 10 0; 10 0 | identical |
| pp_top | 9956 0; 20 0; 178 0; 231 0; 56 0; 3 0 | 9956 0; 20 0; 178 0; 231 0; 56 0; 3 0 | identical |

## Yosys statistics

Independent flow: all derived processor sources through `sv2v`, then `read_verilog -defer all.v; hierarchy -check -top <module>; proc; opt_clean; stat -json`. ROM inputs were generated into each statistics directory. All three full JSON outputs are byte-identical at base and head, including every cell-type count and every reached parameterized module. This is additional to the required complete portability gate, which also checks memory mapping.

| Scope | Metric | Base | Head |
| --- | --- | --- | --- |
| KL_pp_originator | num_wires | 1493 | 1493 |
| KL_pp_originator | num_wire_bits | 12312 | 12312 |
| KL_pp_originator | num_pub_wires | 84 | 84 |
| KL_pp_originator | num_pub_wire_bits | 719 | 719 |
| KL_pp_originator | num_ports | 45 | 45 |
| KL_pp_originator | num_port_bits | 272 | 272 |
| KL_pp_originator | num_memories | 7 | 7 |
| KL_pp_originator | num_memory_bits | 1248 | 1248 |
| KL_pp_originator | num_processes | 0 | 0 |
| KL_pp_originator | num_cells | 1483 | 1483 |
| KL_pp_originator | num_submodules | 0 | 0 |
| KL_pp_rx_validator | num_wires | 870 | 870 |
| KL_pp_rx_validator | num_wire_bits | 10606 | 10606 |
| KL_pp_rx_validator | num_pub_wires | 158 | 158 |
| KL_pp_rx_validator | num_pub_wire_bits | 1783 | 1783 |
| KL_pp_rx_validator | num_ports | 38 | 38 |
| KL_pp_rx_validator | num_port_bits | 484 | 484 |
| KL_pp_rx_validator | num_memories | 2 | 2 |
| KL_pp_rx_validator | num_memory_bits | 592 | 592 |
| KL_pp_rx_validator | num_processes | 0 | 0 |
| KL_pp_rx_validator | num_cells | 840 | 840 |
| KL_pp_rx_validator | num_submodules | 0 | 0 |
| protocol_processor_top | num_wires | 2680 | 2680 |
| protocol_processor_top | num_wire_bits | 59784 | 59784 |
| protocol_processor_top | num_pub_wires | 1050 | 1050 |
| protocol_processor_top | num_pub_wire_bits | 26051 | 26051 |
| protocol_processor_top | num_ports | 212 | 212 |
| protocol_processor_top | num_port_bits | 7161 | 7161 |
| protocol_processor_top | num_memories | 8 | 8 |
| protocol_processor_top | num_memory_bits | 1536 | 1536 |
| protocol_processor_top | num_processes | 0 | 0 |
| protocol_processor_top | num_cells | 2010 | 2010 |
| protocol_processor_top | num_submodules | 33 | 33 |
| top hierarchy total | num_wires | 41447 | 41447 |
| top hierarchy total | num_wire_bits | 445441 | 445441 |
| top hierarchy total | num_pub_wires | 6017 | 6017 |
| top hierarchy total | num_pub_wire_bits | 133051 | 133051 |
| top hierarchy total | num_ports | 1881 | 1881 |
| top hierarchy total | num_port_bits | 40223 | 40223 |
| top hierarchy total | num_memories | 390 | 390 |
| top hierarchy total | num_memory_bits | 403846 | 403846 |
| top hierarchy total | num_processes | 0 | 0 |
| top hierarchy total | num_cells | 59534 | 59534 |
| top hierarchy total | num_submodules | 33 | 33 |

## Per-file xvlog analysis

The parent's `pp_srcs.py` derived list exactly matches the 46 measured paths and their order. Each revision uses a fresh work directory, packages first, and a separate `xvlog -sv --work work <source>` invocation for every file. All 46 head return codes are zero. Diagnostic totals: base 2 `VRFC 10-3380` and 2 `VRFC 10-8530`; head 0 and 0. The base fails only the two expected modules, naming `cancel_hit_w` and `vd_push_w`.

| File | Base rc | Base 3380/8530 | Head rc | Head 3380/8530 |
| --- | --- | --- | --- | --- |
| `hdl/acmp/pp_acmp_pkg.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/adp/pp_adp_pkg.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/aecp/ucpu_pkg.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/common/pp_pkg.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/srp/srp_pkg.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/acmp/KL_acmp_nvm_shadow.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/acmp/KL_acmp_talker.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/acmp/KL_pp_acmp_listener.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/acmp/KL_pp_acmp_lsn_admit.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/adp/KL_adp_engine.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/aecp/KL_aecp_ca_originator.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/aecp/KL_aecp_desc_mem_guard.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/aecp/KL_aecp_desc_store.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/aecp/KL_aecp_dyn_state.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/aecp/KL_aecp_engine.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/aecp/KL_aecp_notify.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/aecp/KL_aecp_nvm_writer.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/aecp/KL_aecp_resp_buf.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/aecp/KL_aecp_ucpu.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/common/KL_pp_prng.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/common/KL_pp_timer_service.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/maap/KL_pp_maap.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/packet_engine/KL_pp_dispatch.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/packet_engine/KL_pp_event_router.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/packet_engine/KL_pp_normalizer.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/packet_engine/KL_pp_nvm_mgr_arb.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/packet_engine/KL_pp_nvm_port.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/packet_engine/KL_pp_originator.sv` | 1 | 1/1 | 0 | 0/0 |
| `hdl/packet_engine/KL_pp_release_merge.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/packet_engine/KL_pp_rx_slots.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/packet_engine/KL_pp_rx_validator.sv` | 1 | 1/1 | 0 | 0/0 |
| `hdl/packet_engine/KL_pp_scoreboard.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/packet_engine/KL_pp_side_port.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/packet_engine/KL_pp_trace_ring.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/packet_engine/KL_pp_tx_arbiter.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/packet_engine/KL_pp_tx_slots.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/srp/KL_srp_admission.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/srp/KL_srp_decoder.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/srp/KL_srp_domain.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/srp/KL_srp_encoder.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/srp/KL_srp_listener_fsm.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/srp/KL_srp_talker_fsm.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/srp/KL_srp_top.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/srp/KL_srp_vlan.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/top/KL_mrp_strip.sv` | 0 | 0/0 | 0 | 0/0 |
| `hdl/top/protocol_processor_top.sv` | 0 | 0/0 | 0 | 0/0 |

## Scratch parent and consumer set

Clone at parent dev `28f9666feab2b2ba287643c63ed3a16b1e0bb863`, under `parent/` in the scratch root. Processor submodule and staged index gitlink are at the head above. The other initialized submodules remain at their recorded pins: timing processor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` (exact pin verification is recorded in the final integrity receipt) and AXIS dependency `48ff7a7e2ef782cf778d47910cf85835c64b1bce`; the external leaf is not needed and remains uninitialized.

The supplied `parent-adoption-148-6c22d3ca.patch` applied first with `git apply`, followed by `parent-adoption-22-28f9666f.patch`. The latter removes only the two remaining budget findings and changes the section count from two to zero. The budget and gate source were read before execution. No parent commit or push. Submodule top-level identities are verified before invoking Git there and before each consumer starts. The parent analysis gate reports zero findings across 73 parent sources and 52 pinned processor sources, exactly matching the zero budget.

| Consumer | Command | rc | Seconds |
| --- | --- | --- | --- |
| 01_cpp | `python3 scripts/check_cpp_idiom.py` | 0 | 30.987 |
| 02_py | `python3 scripts/check_py_idiom.py` | 0 | 92.463 |
| 03_sources | `python3 scripts/check_rtl_source_lists.py` | 0 | 36.498 |
| 04_pp_sources | `python3 scripts/pp_srcs.py --check --selftest` | 0 | 22.992 |
| 05_ports | `python3 scripts/check_port_contracts.py` | 0 | 36.837 |
| 06_naming | `python3 scripts/measure_naming.py --check` | 0 | 15.845 |
| 07_evidence | `python3 scripts/measure_test_evidence.py --check` | 0 | 84.575 |
| 08_docs | `python3 scripts/docs_check.py` | 0 | 19.507 |
| 09_xvlog | `python3 scripts/xvlog_gate.py --check` | 0 | 313.787 |
| 10_builder | `python3 sw/builder/test_builder.py` | 0 | 1490.867 |
| 11_lint | `python3 scripts/lint_rtl.py --check` | 0 | 68.671 |
| 12_shadow | `make -j16 -C tb/verilator/pp_shadow -f Makefile -f <scratch>/limits.mk` | 0 | 427.774 |
| 13_nvm_lint | `make -j16 -C tb/verilator/nvm_cosim lint` | 0 | 47.838 |
| 14_nvm_quick | `make -j16 -C tb/verilator/nvm_cosim quick` | 0 | 184.971 |
| 15_datapath | `make -j16 -C tb/verilator/milan_dp VERILATOR_JOBS=2` | 0 | 2216.178 |
| 16_render | `make -j16 -C tb/verilator/milan_dp_render VERILATOR_JOBS=2 MUTANT_JOBS=2` | 0 | 786.713 |
| 17_shell | `python3 scripts/check_sh_idiom.py` | 0 | 0.614 |

Builder limitations reported by the gate:

- 1 GATE ARM(S) DID NOT RUN - this verdict does not cover them:
- [gate 11] real report not on disk (reference report) - the calibration gate needs the mf48 build tree
- ALL GATES PASS EXCEPT 1 NOT RUN

Retained parent simulation records (shape guards are reported, not counted as coverage):

| Consumer | Records |
| --- | --- |
| 12_shadow | pp_shadow: 606 checks, 0 failures; pp_shadow: 606 checks, 0 failures; pp_shadow: 646 checks, 0 failures; pp_shadow: 311 checks, 0 failures |
| 14_nvm_quick | nvm_cosim: 315 checks: 315 PASS, 0 FAIL (0 not expressible) |
| 15_datapath | == gmstep: checks: 104   failures: 0 ==; 182 checks: 182 PASS, 0 FAIL; 182 checks: 182 PASS, 0 FAIL; milan_datapath: 236 checks, 0 failures; milan_datapath: guarded and NOT run in this shape: 1; checks: 421   failures: 0; checks: 416   failures: 0; checks: 1961   failures: 0; checks: 1961   failures: 0; checks: 3746   failures: 0; checks: 1961   failures: 0; milan_datapath: 236 checks, 0 failures; milan_datapath: guarded and NOT run in this shape: 1; checks: 33   failures: 0; milan_datapath: 233 checks, 0 failures; milan_datapath: guarded and NOT run in this shape: 5; 6 checks: 6 PASS, 0 FAIL; 6 checks: 6 PASS, 0 FAIL |
| 16_render | == tdm8_render: checks: 65   failures: 0 ==; == tdm8_render: checks: 245   failures: 0 ==; 5 checks: 5 PASS, 0 FAIL (--leg-defects: the arms that need no elaboration; the gateware and shape mutants are the tdm8render-mutants target) |

Final integrity receipt: `final-integrity.json`. The processor tree is clean and matches the head; both exports preserve all 556 tracked blobs, and the scratch parent differs only by the staged processor gitlink and the two prescribed patches.

## Reproduction and retained evidence

Scratch scripts: `run_phase.py`, `stats.py`, `analyse_processor.py`, `run_parent.py`, `verify_final.py`, and `limits.mk`. Each completed command has a `.log`, `.rc`, and command/time `.json` under `logs/base`, `logs/head`, or `logs/parent`. Per-file analysis logs and the statistics work products live beneath each processor phase. No file over 200 KB is copied into the delivery directory; large artifacts are recorded by size and sha256 below.

| Scratch-relative artifact | Bytes | sha256 |
| --- | --- | --- |
| patch-context-before.json | 906 | 6500483f6eafaa3a7fc91e02f9d51568e6d0acaf025c1f3fcbef57737cb90782 |
| planting-head.json | 49239 | 4ca7b6d4f03597dd70dd824d4dc9ca2088bd634ddb7dffa64c466a415b13b29a |
| source-integrity.json | 430 | 90b54d19f7085e423e33d922b5b869c7020e142921fa2352642a75da34e2dc2e |
| final-integrity.json | 5040 | 626e7ca1ddd2271a054cb73b7930bc6ffbff0f63d2fd4421de0044f01b11beea |
| logs/base/check.log | 410 | bbde74fce3ceddddc8c010cc97204f79279463b32aadfd5babdfdf67cd51d7f1 |
| logs/base/lint.log | 1056 | 9a3703ba1ec6767b277e9d5102c94a93fe107454da19d13cab518ba312cd1e81 |
| logs/base/matrix.log | 33 | 7a2c98136a0892f195fa6a08ad82dfe7e36e8a81d0732cb304584f31e966e097 |
| logs/base/stats.log | 286 | a3a01698f357f7ca6c71865b7a73d03d43061172711db31c3e6ee47ab12e3430 |
| logs/base/suites.log | 1750 | 299897e701fa15cbc20b6007e1566749c48499ace9118db456ef35d48f409f69 |
| logs/base/xvlog.log | 4119 | 631d8c0eb79f9ad954c0a73aca55cc0e2bc8eb95e4e2614e5f2c0abd44421e55 |
| logs/base/yosys.log | 3548 | 5918894aeb86257a2ba105f0914f534c8ab77338863151178375bed543a51a82 |
| logs/head/check.log | 410 | 56f2ef6b9b21505c4671b3069a68acfe2daa81400e29e38bc6fb713a4f83d11c |
| logs/head/lint.log | 1056 | 9a3703ba1ec6767b277e9d5102c94a93fe107454da19d13cab518ba312cd1e81 |
| logs/head/matrix.log | 33 | 7a2c98136a0892f195fa6a08ad82dfe7e36e8a81d0732cb304584f31e966e097 |
| logs/head/stats.log | 286 | 9cccf778a229a9f56a289480a385c3504780d0fec03b687ff4299dc9ab48357b |
| logs/head/suites.log | 1750 | 299897e701fa15cbc20b6007e1566749c48499ace9118db456ef35d48f409f69 |
| logs/head/xvlog.log | 4119 | 6f0d79dc84a5bebfcfb31da7af5e6b355a526ff4b82c0f9cc228e683a1424123 |
| logs/head/yosys.log | 3548 | 5918894aeb86257a2ba105f0914f534c8ab77338863151178375bed543a51a82 |
| logs/parent/01_cpp.log | 315 | 20d9e296340ae6319c913211b7a2b7d63b6cc89798c011092c87908916634810 |
| logs/parent/02_py.log | 461 | 51652f142f99dd13b062bd2051192a89a45a962f40ddde1b22b4ddbe9f9bc936 |
| logs/parent/03_sources.log | 153 | ed979d7e26c3cd7a6f14364c11994089b77632424d04252613eeed458ebc8a95 |
| logs/parent/04_pp_sources.log | 955 | fad5e1b9dd5f465b7fcb2334e2abe6c6db44be93b5bb12afb3a35f3ebf432e1a |
| logs/parent/05_ports.log | 421 | b04fbab06614655f710f529fa8d2cdbd59073e9a63f179b308734b9e21f35c23 |
| logs/parent/06_naming.log | 36608 | db23d3d49d070f855b77fbe71e83f3cc24b00ae81d2c288082eb016ac2820e77 |
| logs/parent/07_evidence.log | 13902 | bb9aadc07a14eb4e219e87fa681571c7886f1ef0be545cbae69d099b66fd7f44 |
| logs/parent/08_docs.log | 127 | 6a6b0baa714d34c94d863882cab86a5eac8309164fc1a6c99cb5659f049510ee |
| logs/parent/09_xvlog.log | 721 | 0b429de4cd82331716b088e634d7c56c0b1845db6f1c811ca8299a407fc5526e |
| logs/parent/10_builder.log | 101612 | d1b95ebfd29ac4ff6e713d39f1f3cb320452b3038f7b2edd49e599648ba9a5e7 |
| logs/parent/11_lint.log | 14186 | 9087b44973869192bcab894931d990c7976fb895a8d92b6c243c555087f69d6e |
| logs/parent/12_shadow.log | 276102 | 0b39124fdbae2e063972f38341937f9bbec5b0d29bf6f6a91341e96060e5ab2c |
| logs/parent/13_nvm_lint.log | 29863 | 4f1e06ab4a5cc433736817c5456cab2714eff9a5787b706614345b22a631f966 |
| logs/parent/14_nvm_quick.log | 392 | 6c4912bdea9f1179027a4539d615d3f210261f69388f1ed89a167192969c832a |
| logs/parent/15_datapath.log | 1951700 | c83c68b4b9b3c7093f60257c995b43c730a0d3c5461a2bedfd96f0c2ce530a15 |
| logs/parent/16_render.log | 156106 | 23edcb91124d2872339992399ed02a137a92afd01bc26b2b84349b5655664e50 |
| logs/parent/17_shell.log | 235 | 7ace602f03fa0e411862de119cff9d337583f1f2170d920dff65a0e0f39ee6d9 |
| logs/base/statistics/KL_pp_originator.json | 2045 | 102354aa0632d5ca1fa83cf6c72f36cdb3f6a9a2524c5dc55114d5ff87b52298 |
| logs/base/statistics/KL_pp_originator.log | 62744 | 7259dabc2719aa7af0854610202d46ed18d6ab609a311c4c2de4eed84caa13fc |
| logs/base/statistics/KL_pp_rx_validator.json | 2427 | b48ab8257a5d01221d8df24ec2138e12f0572f385ef4f657a0427af7554a2dda |
| logs/base/statistics/KL_pp_rx_validator.log | 47442 | 80b6082cfca46bbeb7c38cb5ad7459361ce08440b3076e533921d2c9818219c3 |
| logs/base/statistics/all.v | 759318 | a4bd8685f950eeeb33651b1cfd36a5006cb4d57e2c69cd938982eccbb290c783 |
| logs/base/statistics/ltn_rom.hex | 6138 | 23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956 |
| logs/base/statistics/protocol_processor_top.json | 47371 | c19429cb06a6aa5f47e0f4b5fd53ac4d5bd390ba1f4d83b752ccbc14a35793e6 |
| logs/base/statistics/protocol_processor_top.log | 7402315 | d090df7ab337c38b8cc28b57bf44f51df61d2a587b7930d3da1698105e231cbb |
| logs/base/statistics/ucode.hex | 26624 | 518b900c4a5650902c3ea9125941e434857ba2f379b6c92268a67fef459d37f8 |
| logs/base/xvlog/table.json | 5180 | b742a4d4f93d8ddca9cc8932d7d1c787312351a6b4dc07fcbac79fd3565bcb25 |
| logs/head/statistics/KL_pp_originator.json | 2045 | 102354aa0632d5ca1fa83cf6c72f36cdb3f6a9a2524c5dc55114d5ff87b52298 |
| logs/head/statistics/KL_pp_originator.log | 62744 | bbdf94df34ecf65f6e320782972c3064be79196f93dd56a901b345b345f46649 |
| logs/head/statistics/KL_pp_rx_validator.json | 2427 | b48ab8257a5d01221d8df24ec2138e12f0572f385ef4f657a0427af7554a2dda |
| logs/head/statistics/KL_pp_rx_validator.log | 47441 | c792347d375b0001646755456042c236e233c42362e055ec8ff4250381dab7c4 |
| logs/head/statistics/all.v | 759318 | 5ddcb0f4cc8e84c72ae430c777354f3dd5c25fde40cef04c032534c9e3d297b3 |
| logs/head/statistics/ltn_rom.hex | 6138 | 23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956 |
| logs/head/statistics/protocol_processor_top.json | 47371 | c19429cb06a6aa5f47e0f4b5fd53ac4d5bd390ba1f4d83b752ccbc14a35793e6 |
| logs/head/statistics/protocol_processor_top.log | 7402317 | 30b042e8501e0d7d7890fbaf03c7012eff4478422dfb34328e49f0c556d88c46 |
| logs/head/statistics/ucode.hex | 26624 | 518b900c4a5650902c3ea9125941e434857ba2f379b6c92268a67fef459d37f8 |
| logs/head/xvlog/table.json | 5180 | 94d84f6ea7b25c5f892c8a00728740b77371b4a508cdeaf3f15fb13af7ef6456 |

Delivery patches:

| File | Bytes | sha256 |
| --- | --- | --- |
| parent-adoption-148-6c22d3ca.patch | 966 | bbd0301dc7e576f51f92d24c8d140eda0666f9c6699806649365110e7ecfea83 |
| parent-adoption-22-28f9666f.patch | 447 | 8acf2b12f4cd67ffff19cc668c9d74cbf77f203f116a13f3f22db4e08b28e94f |

## Acceptance and handoff

- Declaration-only processor diff and context planting: met.
- Identical complete statistics and all-source analysis: met.
- Full processor gate and record comparison: met.
- Parent consumer set and zero-finding ratchet: met.
- Original issue vendor synthesis warning criterion: not measured, prohibited by this lane's assignment. `Relates to #22` is used accordingly.

Final integrity checks passed. The local head is ready for review; the required final status comment is the last action.
