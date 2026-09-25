# HANDOFF — [A274] issue #508 (processor pin adoption + GET_STREAM_INFO seam)

Status: REVIEW READY posted (https://github.com/kebag-logic/milan-fpga/issues/508#issuecomment-5822002238) at head 35f0695815c202392b6b4806bb9f59dd110687ed (tree 95ee829d), with ONE BLOCKER that needs a decision (below). Not pushed; no PR (not allowed in this lane).

Lane: $LANES/508-pp-pin-adopt, branch 508-pp-pin-adopt, base dev 573f0052a0e4412e81f0845438fcec2086ce5d55 (head descends from it; 28 files, +1340/-116)
Processor pin: 09f9bf3846511f8388d995126502ed92eaa65213 -> a8f8ce810ddba1816cd129d0afcd71e6e02ade1b (ancestor check OK)
Tools: PATH=$VALIDATION_STORAGE/387b-manager-r2/pinned-tool-bin:$PATH (Verilator 5.050, docs-locked python3); every gate run in the foreground, output to a log file, never piped.

## Commits (one line, no body, no trailers)
| SHA | Subject |
|---|---|
| 4072d3894 | Pin the processor at a8f8ce81 and re-record its ROM digests |
| 0bf4bf961 | Start the restore walk in every milan_dp harness that binds a sink |
| 7740727ea | Leave STREAM_INPUT selectors 5 and 7 and the failure-code byte to the processor |
| a3164dd3c | Grade the processor-owned GET_STREAM_INFO fields in the timed milan_dp leg |
| 1595780dd | Document the processor-owned GET_STREAM_INFO fields and the per-boot restore walk |
| c018cba33 | Start the restore walk in the multi-stream render leg too |
| f597b34d8 | Wire the co-simulated NVM path as the processor top now wires it |
| b281c0ad1 | Boot the render leg's entity through one helper so the multi-stream phase stays under the function limit |
| 747497a42 | Record the dispositions of the three processor mutation campaigns the new pin adds |
| 35f069581 | Re-measure the milan_dp check counts at the #508 head |

## BLOCKER: three parent gates refuse processor content at a8f8ce81
All three run in the hosted `docs-check` required context. docs.yml is green on dev 573f0052 (hosted run), and every finding names a file or line new at the pin. Each gate's own rule forbids the parent from adding the identity or raising the ratchet, and the fix is processor-side, which this lane may not change.
| Gate | Finding | Processor source | Processor-side remedy |
|---|---|---|---|
| `scripts/check_port_contracts.py` (rc 1) | 7 new unjustified literal-bound connections: `protocol-processor:hdl/top/protocol_processor_top.sv:u_nvm_arb.{m1_req_i,m1_we_i,m1_rid_i,m1_wvalid_i,m1_wdata_i,m1_rready_i,m1_abort_i}` | PR #109 (manager 1 tied idle; the rationale sits above the declarations, not directly above the connection runs) | a rationale comment directly above each literal run |
| `scripts/measure_naming.py --check` (rc 1) | 2 new identities: `KL_aecp_desc_mem_guard:s_rsp_data_o` ("response bytes, unchanged"), `protocol_processor_top:srp_sr_admitted_o` (comment now quotes a latency in clocks) | PR #110, PR #114 | reword the two `//!` comments so they document no unit the name lacks |
| `scripts/measure_test_evidence.py --check` (rc 1) | wall-clock-dependent suite files 6 > ratchet 3: `protocol-processor/tb/desc_mem_guard/mutate.py`, `tb/pp_top/gsi_mutants.py`, `tb/srp_admission/mutants.py` (each passes `timeout=` to subprocess.run) | PR #110, #111, #114 | drop the host deadlines (the legs are cycle-bounded) |
Options: (1, recommended) a processor follow-up fixing the three, then re-pin this lane to the fixed main (only the gitlink, rom_digests row, SUBMODULES/diagram/CHANGELOG pin text move); (2) an explicit maintainer exception to add the identities and raise the wall-clock ratchet.
The parent-owned half of the third gate is fixed here: the three new processor DUT-source readers now carry dispositions (commit 747497a42), so `measure_test_evidence.py --selftest` passes (101/101).

## Adopted-change table (processor first-parent 09f9bf38..a8f8ce81)
| Processor merge | PR | Issues | Parent-visible effect | Parent adaptation |
|---|---|---|---|---|
| 008edbbf | #109 | #92, #93 | ACMP listener held from reset until the NVM walk ends; restore_go must start the walk on every boot; walk deadline NVM_RS_TMO_CYC_P (default CLK_HZ_P/50 = 20 ms); a device err or short header now fails the walk whole; new KL_pp_nvm_mgr_arb, nvm_err_cause, nvm_abort | milan_dp/milan_dp_render harnesses start the walk via PP_CTRL[1]; nvm_cosim transcription wires arbiter, cause, abort and deadline as the top does; wrapper, REGISTER_MAP PP_CTRL, INTEGRATION_GUIDE, TROUBLESHOOTING §27 document it; firmware nvm_boot() already starts it |
| 939c1433 | #110 | #94 | descriptor-memory guard inside the top; debt_o not exported | none (no port change) |
| 7a47f578 | #111 | #43, #49 | STREAM_INPUT selectors 5/7 answered internally (no gsi_req); selector 4 byte [15:8] replaced; new STREAM_INPUT notify terms | datapath gather for 5/7 and the input code byte removed; `[GSI]` section + `gsi_mutants.py` |
| a8f8ce81 | #114 | #112 | srp_sr_admitted_o drops at every accepted (re)declaration until evaluated; rounds meeting a pending declaration publish nothing | LWSRP_STATUS[9]/LWSRP_SLOPE docs and datapath comments updated; no gate reads them |

Ports/parameters (diff 09f9bf38..a8f8ce81 on hdl/top and docs/guides/integrator.md): one new top parameter NVM_RS_TMO_CYC_P (defaulted; KL_pp_shadow does not override). No top port added or removed. Port comments changed for restore_fail_o, srp_active_o, srp_sr_admitted_o, granted/sum slope, over_limit. Side-port register layout unchanged. ROM images unchanged.

## Consumer impact found and handled
- BOOT: unmodified 1x1 leg at the new pin = 230 checks, 24 FAIL (no PROBE_TX). milan_dp_render multi leg = 59 checks, 30 FAIL. Both pass once PP_CTRL[1] starts the walk.
- nvm_cosim: 3 FAIL (contract-8x8 R_power_cycle~B1/B2/B9, nothing restored) because cosim_top.sv left the shadow's new nvm_err_cause_i open (reads 0, so an UNFRAMED zero-byte record failed the whole walk) and did not transcribe the arbiter/abort/deadline. Wired as the top wires them: 465/465, 39/39 mutants.
- Stale processor line citations fixed (KL_srp_top.sv 207->210, 445/772-779/855-858 -> 450/785-796/871-874, KL_srp_listener_fsm 795-796 -> 842-843, KL_srp_admission 152-154/207-214 -> 187-190/261-266). milan_soc.py:2123 cites protocol_processor_top.sv:113, stale already at the old pin (line 120 there); left alone.
- FIRMWARE (report only): milan_baremetal.c nvm_boot() returns before nvm_restore_walk() when nvm_shape_consistent() fails. The check is constant per build and the builder refuses an inconsistent shape, so it is reachable only in an already broken build; at this pin such a build would advertise with a held listener. Candidate follow-up issue.

## ROM digest re-record command
`cd syn/yosys && ./ooc.sh --record-rom-digests` (rc 0). Adds two rows for a8f8ce81; ltn_rom 23cc67ee... and ucode 23605682... identical to 09f9bf38 (images unchanged; gptp row unchanged).

## Seam lineage (state owner -> selector -> response byte)
| Field | Milan | State owner (processor) | gsi selector | Who answers | AECPDU offset (frame byte) |
|---|---|---|---|---|---|
| probing_status | 5.3.8.6 | KL_pp_acmp_listener committed record `pbsta`, copied into `lstn_gsi_status_r` off the record write bus | 7 | processor, no gsi_req | @76 bits 7:5 (90) |
| acmp_status | 5.3.8.6 | same record, `acmpsta` | 7 | processor, no gsi_req | @76 bits 4:0 (90) |
| msrp_failure_code | 5.3.8.8 | KL_srp_listener_fsm registrar `snk_fail_code` | 4, byte [15:8] | processor replaces the byte; datapath leaves it 0 | @58 (72) |
| msrp_failure_bridge_id | 5.3.8.8 | registrar latch `snk_fail_bridge`, gated on `tk_reg_state == FAILED` after the index mux | 5 | processor, no gsi_req | @60..@67 (74..81) |
| MSRP_FAILURE_VALID, REGISTERING_FAILED, BOUND, REGISTERING | T5.9/T5.10 | class-D `srp_tk_reg_state`, `acmp_bound` | 0, 6 | datapath (unchanged) | @28 flags (42..45), @68 flags_ex (86..89) |

## Tests
| Leg | Result | Notes |
|---|---|---|
| obj_notify (timed, AX 1x1: AAF sink 0, CRF sink 1) with `[GSI]` | 345 / 0 | `[GSI]` adds 198 checks, G0..G10; 1 DUT LeaveAll re-declared inside the section |
| `[GSI]` G0 | DISABLED both sinks; STREAM_INPUT 2 = NO_SUCH_DESCRIPTOR, cdl 68, zero body | |
| `[GSI]` G1/G2 | bind -> ACTIVE/0 at once; duplicate probe pushes nothing; 2nd timeout -> ACTIVE/7; sink 1 refused -> ACTIVE/3 beside sink 0 ACTIVE/7 | |
| `[GSI]` G3/G4 | retries -> PASSIVE/0 (no talker discovered); unbind -> DISABLED; answered probes -> COMPLETED with the talker's stream_id | |
| `[GSI]` G5..G8 | Talker Failed: code 1 / bridge 0x0123456789ABCDEF (sink 0), code 2 / 0xFEDCBA9876543210 (sink 1); refresh silent; sink 1 change -> 8 / 0x0F1E2D3C4B5A6978, one push, sink 0 untouched; sink 0 withdrawal clears, tears down to PASSIVE | |
| `[GSI]` G9/G10 | STOP_STREAMING from A pushes STOP to B only, no GET_STREAM_INFO push; reset -> both DISABLED, nothing carried | |
| every transition | exactly one unsolicited GET_STREAM_INFO to each of A and B; push == solicited answer from byte 38 on | |

Acceptance note: #508 acceptance 2 says "PASSIVE after bind". The processor (PR 111, Milan 5.5.3.5.3 and 5.5.3.5.29) is ACTIVE at the bind (it probes at once) and PASSIVE after an unanswered probe's retry; graded as the processor behaves and stated in the PR body and README.

## Mutants (`make -C tb/verilator/milan_dp gsi-mutants`: 8/8 PASS, rc 0, 3 min 30 s; clean leg 345/345)
| # | Mutant | Planted in | Named check that fails | Failures |
|---|---|---|---|---|
| 1 | processor ties the bridge id to zero | processor top copy, sel 5 | G5 sink 0 Talker Failed: msrp_failure_bridge_id | 7/345 |
| 2 | selector 5 goes back to the datapath (answers 0 for inputs) | processor top copy | G5 sink 0 Talker Failed: msrp_failure_bridge_id | 7/345 |
| 3 | processor ties the failure code to zero | processor top copy, sel 4 | G5 sink 0 Talker Failed: msrp_failure_code | 7/345 |
| 4 | failure-code byte left to the datapath (0) | processor top copy, sel 4 | G5 sink 1 Talker Failed: msrp_failure_code | 7/345 |
| 5 | processor ties probing/ACMP status to zero | processor top copy, sel 7 | G2 sink 0 two probes unanswered: acmp_status | 17/345 |
| 6 | processor reads the other sink (index ^ 1) | processor top copy, gsi_sink_w | G5 sink 0 beside the other sink's failure: msrp_failure_bridge_id | 30/345 |
| 7 | datapath bound/settled approximation answers selector 7 again | processor top copy + datapath copy | G1 sink 0 bound: probing_status | 10/345 |
The submodule checkout is never edited: each processor mutant is written into a copied hdl/ tree that the recipe's PP_DIR points at.

## Gates (final head 35f06958 unless noted; all foreground, logs in /tmp/a274/logs)
| Gate | rc | Result |
|---|---|---|
| builder, pinned SDK (`/tmp/a274/full-builder-sdk.py`, identical to the 387b runner apart from its records path) | 0 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11: no mf48 board build tree); 239 compiler calls mapped to the SDK |
| builder, no RV32 compiler (PATH without riscv*, HOME without the native SDK, MILAN_LITEX_PYTHON=build venv) | 0 | ALL GATES PASS EXCEPT 2 NOT RUN (gate 1b compiled census, by design without RV32; gate 11) |
| make -C tb/verilator/pp_shadow (from clean) | 0 | 371 / 0 |
| milan_dp default `run` sweep, from clean, 31 commands in 4 chunks (at 1595780dd; no milan_dp input changed after) | 0 x31 | gptp 181/0, gptplat 181/0, obj_dir 231/0, notify 345/0, crflic 85/0, nxn 1709/0, nxndv 1711/0, nxn8 3137/0, nxn4c 1709/0, nolpf 231/0, prune 33/0, ax1x1 228/0, aclk 140/0, render_mutants 6/6 |
| make -C tb/verilator/milan_dp_render (from clean, at b281c0ad1) | 0 | 152/0, 60/0, leg-defects 5/5 |
| make -C tb/verilator/nvm_cosim (from clean, at f597b34d8) | 0 | 465/465, 39/39 mutants |
| make -C tb/verilator/milan_dp gsi-mutants (at a3164dd3c; datapath unchanged since) | 0 | 8/8 |
| python3 scripts/pp_srcs.py --check --selftest | 0 | |
| python3 scripts/docs_check.py (git) / (GIT_DIR=/nonexistent) | 0 / 0 | 0 findings; no-git walk 869 files |
| python3 scripts/check_feature_status.py (git / no git) | 0 / 0 | |
| check_em_dash --base 573f0052 | 0 | 0 findings over 168 added lines, 9 pages |
| check_doc_style | 0 | 22 documents |
| gen_toc --check | 0 | |
| check_doc_paths | 0 | 842 paths |
| docs/traceability/gen_module_matrix.py --check | 0 | 69 modules |
| xvlog_gate --check | 0 | 4 processor findings == ratchet, 0 hdl/ |
| check_rtl_source_lists | 0 | 106 files, 4/4 lists |
| check_cpp_idiom | 0 | every ratchet 0 |
| check_py_idiom | 0 | at budget |
| cd tests && behave --no-capture -f plain | 0 | 344 scenarios, 1739 steps |
| syn/yosys/run.sh, every top (all 54 read the derived processor list), shards 0..7 | 0 x8 | 54/54 PASS; tied-input and tap-purity PASS |
| git diff --check 573f0052..HEAD | 0 | |
| lint_rtl.py --check, check_sv_idiom, check_hygiene, gen_hdl_reference (--selftest 44/44 and build, pinned pyslang in /tmp venv) | 0 | extra |
| all other self-contained docs.yml / rtl-fast.yml python commands (83 listed) | 0 | except the three BLOCKER gates |
| check_port_contracts / measure_naming --check / measure_test_evidence --check | 1 / 1 / 1 | BLOCKER above |

Not run: milan_dp_gptp (scheduled physical suite, --physical-gptp, one process longer than the 10-minute foreground limit; its harness drives no ACMP listener command); elaborate.yml's `test_builder.py --require-elaboration`; act/hosted runs (no push).

## Open risks
- BLOCKER above (decision needed).
- Firmware nvm_boot() early return (report only).
- #551's cold-pipeline case not flipped here (#553 does it).
