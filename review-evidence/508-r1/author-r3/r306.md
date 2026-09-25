[R306] NEGATIVE - exact head 6a9828c172aa4d5d8ee49725e357a10bae2caa52

# R306-1 internal review: issue #508 / PR #560

- Head `6a9828c172aa4d5d8ee49725e357a10bae2caa52`, tree `e43b64d9421ce0892f1bc620de942fc1f1fe50f8` (re-verified in the review clone before and after every probe).
- Source base `573f0052a0e4412e81f0845438fcec2086ce5d55`; merged dev `c266432dcb0cdd464205823a3d82cad260eedde2` (merge commit `cec6b99da7b26ce9962bcf9a6c05161c9f99439a`).
- Processor gitlink `990f96526bb89356c963a260ebbdcf2a77e6623a`; gPTP `e5dcea6e351a`; verilog-axis `48ff7a7e2ef7`.
- Role: internal independent reviewer, cleared context, round R306-1. All five lenses applied.

Verdict: NEGATIVE. The shipped RTL change, the processor seam, the harness restore-walk adaptation and the `nvm_cosim` transcription are correct, and every executable claim I re-ran reproduced. Four MINOR findings stay open:

- F1 and F2 are documentation defects the re-pin introduced: a CHANGELOG entry duplicated into a historical section, and processor line citations left aimed at `a8f8ce81`.
- F3 is a test gap at the G8 withdrawal, where the README's "exactly one push" is false.
- F4 is frozen acceptance criterion 2, whose wording has no recorded maintainer decision.

None needs an RTL change.

## Reconstruction

Sources read, in order:

- `AGENTS.md`, `CONTRIBUTING.md` (sections 1-3 and 5), `docs/README.md`.
- The issue #508 body and its comments: 5819498419 (round-1 assignment), 5822002238 (round-1 handoff), 5822047670 (decision: option 1, processor #116, re-pin rules, `nvm_boot()` early return to #495), 5824708827 (round-2 assignment) and 5825445388 (round-2 handoff).
- The PR #560 body and the review-start comment 5825475961.
- Processor authorities at `990f9652`: `hdl/top/protocol_processor_top.sv` (GSI owner read, answer mux, `stri_events`), `docs/architecture/05_acmp_engine.md` sections 6.1 and 6.4 (listener states and pbsta mapping), and `KL_srp_listener_fsm.sv` (`msrp_fail_code_o` gating).
- Parent authorities: `hdl/milan/milan_datapath.sv`, `hdl/milan/KL_pp_shadow.sv`, the firmware `nvm_boot()`/`nvm_restore_walk()`, and the #495 checklist.
- Diffs: `573f0052..6a9828c1` (48 files) and the lane-only part `c266432d..6a9828c1` (28 files), with first-parent history of 13 lane commits plus the merge.

I read no private author material and no other reviewer's report before this verdict and ledger were written. The concurrent external report is addressed in the addendum at the end.

## Findings

### F1 - MINOR - Docs - `CHANGELOG.md:113-116` - processor #116/#113 entries duplicated into the historical `09f9bf38` section

- **Authority/evidence.** The section "Unreleased - licence and LeaveAll scope" records the move to processor pin `09f9bf38` (processor issue 106), at `CHANGELOG.md:110`. The re-pin commit `e9f8ea5aa` inserted four lines into it at 113-116:
  - "Processor issue 116: ..."
  - "No behavior or external port changes..."
  - "Processor issue 113: latency-only input changes now push GET_STREAM_INFO"
  - "Unchanged refreshes stay silent..."

  The same four lines are correct at `CHANGELOG.md:51-54`, in the new "processor pin 990f9652" section. Neither `c266432dc:CHANGELOG.md` nor the merge result `cec6b99da:CHANGELOG.md` carries them, so the merge resolution is clean and the re-pin commit introduced the defect.
- **Impact.** The changelog says the `09f9bf38` pin already carried #116 and #113. Those merged far later in processor history, as `265d6762` and `990f9652`. That is a false release record, in the exact artifact the round-2 assignment required to be correct.
- **Required outcome.** The four lines appear once, in the `990f9652` section only. The `09f9bf38` section's body returns to its dev `c266432d` content.
- **Verification.**
  - `grep -c 'Processor issue 116' CHANGELOG.md` and `grep -c 'Processor issue 113' CHANGELOG.md` each give 1.
  - The "licence and LeaveAll scope" section is byte-equal to the same section at `c266432d`.
  - `check_em_dash --base c266432d` and `gen_toc --check` stay green.

### F2 - MINOR - Docs - `hdl/milan/milan_datapath.sv:6603-6604`, `hdl/milan/milan_datapath.sv:6683-6684`, `tb/verilator/pp_shadow/sim_main.cpp:2849` - processor line citations stale at the adopted pin

- **Authority/evidence.** Round 1 re-aimed these citations at `a8f8ce81`. Processor #113 (`265d6762..990f9652`) then added lines to `hdl/srp/KL_srp_top.sv` and `hdl/srp/KL_srp_listener_fsm.sv`, and round 2 did not move the citations. At `990f9652`:
  - `KL_srp_top.sv:210` is `src_fail_bridge_o`; `tk_reg_state_o` is now 211.
  - `KL_srp_listener_fsm.sv:842-843` is `vl_pend_r`/`vl_vid_r` bookkeeping. The `status_map` driver of `tk_reg_state_o` is now 851-852.
  - `KL_srp_top.sv:450` is a comment; `assign sr_adm_fsm_w` is now 451.
  - `KL_srp_top.sv:785-796` and `871-874` are each shifted by two lines (now 787-798 and 873-876).

  `cite_drift.py` measured the drift (`receipts/cite_drift.txt`). I read the two ranges it does not parse across line breaks by hand. The other citations in the same banners (`KL_srp_admission.sv`, `KL_srp_talker_fsm.sv`) are unaffected: those files did not change after `a8f8ce81`. The one other drifting citation the tool reports, `sw/litex/milan_soc.py:2123`, was already stale at dev's `09f9bf38` and is not this lane's.
- **Impact.** Two places send a reader to the wrong processor lines:
  - the datapath banner that justifies the #530 transmit gate and the #472 code decode;
  - the pp_shadow comment behind the `tk_reg_state` code decode.

  Nothing gates line citations in RTL or C++ comments (`check_doc_paths` checks Markdown only), so they stay wrong silently.
- **Required outcome.** Every processor line citation this PR touched resolves, at `990f9652`, to the construct it names.
- **Verification.** For each citation, the cited lines at `990f9652` hold the text the round-1 citation named at `a8f8ce81`.

### F3 - MINOR - Tests, Docs, Conformance - `tb/verilator/milan_dp/sim_nxn.cpp:2173-2174`, `tb/verilator/milan_dp/README.md:477,481`, `tb/verilator/milan_dp/sim_nxn.cpp:1667` - the G8 withdrawal's pushes are ungraded, and "exactly one push" is false there

- **Authority/evidence.** Acceptance 4 requires that the notification path "does not announce a fabricated transition". The README (`:481`) and the section banner (`sim_nxn.cpp:1667`) say every transition pushes exactly one GET_STREAM_INFO to each controller. G8 checks much less:
  - it asserts only `pushes >= 1`;
  - it counts controller B only;
  - it compares only the last push to the solicited answer.

  My probe P6 changed that assertion to `== 1`, and the leg fails there alone: `[GSI] G8 sink 0 withdrawn: the withdrawal pushed got=0x2 exp=0x1` (`receipts/probe_P6_g8_exactly_one.log`, 1 of 345). So the withdrawal pushes twice. That is plausibly the registrar's withdrawal followed by the settlement teardown to PASSIVE, but the leg never grades the first push's content and sets no upper bound. A third, fabricated push at withdrawal would pass.
- **Impact.** The one phase with two real changes is also the one phase where acceptance 4's "no fabricated transition" is not shown. The README also claims a property the leg measurably lacks.
- **Required outcome.**
  - G8 grades the exact number of pushes to each registered controller.
  - Each push is tied to a named change, and its content is graded against the state it announces. Where a push's content cannot be observed, the leg shows why.
  - The README (`:477`, `:481`) and the banner (`sim_nxn.cpp:1667`) state the withdrawal's count.
- **Verification.** Plant an extra GET_STREAM_INFO push at withdrawal, for example a duplicated `srp_evt_tk_unreg_w` term in a processor copy; a named G8 check fails. `make gsi-mutants` and the clean leg stay green.

### F4 - MINOR - Conformance - issue #508 acceptance 2 - frozen wording "PASSIVE after bind" not met as written, with no recorded decision

- **Authority/evidence.** Acceptance 2 requires "PASSIVE after bind". The adopted processor behaves differently:
  - A bind goes straight to `PRB_W_RESP`, which reports ACTIVE (2) (`protocol-processor/docs/architecture/05_acmp_engine.md` F05.2 `UNBOUND --> PRB_W_RESP: BIND_RX`, and the pbsta table in section 6.1).
  - PASSIVE is `PRB_W_AVAIL` only: reached after an unanswered retry with no discovered talker, or on a boot-restored binding.

  G1 grades ACTIVE at bind and G3 grades PASSIVE after the retry (`sim_nxn.cpp` `gsi_g1_g2_sink0_probes_unanswered`, `gsi_g3_retries_fall_to_passive`). My Conformance reading agrees with the processor: a Milan v1.2 bind sends its fast-connect probe at once (5.5.3.5.3, the processor's REQ-ACMP-013).

  But `AGENTS.md` section 4 freezes acceptance criteria and requires a public change when one is wrong. The executors recorded the difference in 5822002238, 5825445388 and the PR body, and asked review to "retain the distinction". No amended reading is recorded: not in the maintainer decisions 5822047670 and 5824708827, and not in any later comment.
- **Impact.** A cold completion check cannot mark criterion 2 met as worded. The ledger would rest on an executor's interpretation of a frozen criterion, which `AGENTS.md` section 2 forbids choosing privately.
- **Required outcome.** A maintainer decision on #508 does one of two things. It records that criterion 2 is met by ACTIVE at bind and PASSIVE after an unanswered retry with no discovered talker, as G1 and G3 grade. Or it amends the criterion. No code or test change is needed.
- **Verification.** The decision comment exists and cites G1/G3; the re-reviewing round re-reads it.

### Suggestions (optional; they do not affect coverage)

- **S1 (Docs)** - `tb/verilator/milan_dp_render/sim_tdm8_render.cpp:1419-1426`: the restore-walk doc block sits above `boot_the_entity()`, which now has two stacked `//!` blocks. `start_the_boot_restore_walk()` at `:1438` has none. Move the first block to the helper it describes.
- **S2 (Tests)** - `start_the_boot_restore_walk()` is repeated almost verbatim in `sim_main.cpp:256`, `sim_aclk.cpp:1137`, `sim_nxn.cpp:2283` and `sim_tdm8_render.cpp:1438`. One shared helper would keep the firmware boot contract in a single place.
- **S3 (Docs)** - "without it the 1x1 leg fails 24 checks" (`tb/verilator/milan_dp/README.md:511`, `docs/limitations/TROUBLESHOOTING.md:1073`) names neither the leg nor the pin it was measured at. For comparison, my probe P5 on `obj_notify` fails 122 of 344.

## Verified claims (focus items)

| Claim | Result | Evidence |
|---|---|---|
| The gitlink is the processor's merged main | yes | Compare `990f9652...main` is `identical` (0 ahead, 0 behind). PRs 109, 110, 111, 114, 115 and 117 are all merged, as `008edbb`, `939c143`, `7a47f57`, `a8f8ce8`, `990f965` and `265d676` (`receipts/pp_pin_on_main.txt`). |
| The `rom_digests` rows come from the repository tool | yes | `cd syn/yosys && ./ooc.sh --record-rom-digests` rc 0. The rewritten ledger is byte-identical to the head's (`receipts/rom_record.log`); the file was restored with its mode. The `990f9652` ucode digest equals `09f9bf38`'s, so "images unchanged" holds. |
| SUBMODULES, diagram and CHANGELOG pin text | pin text correct; F1 open | `SUBMODULES.md:25` pins `990f9652...`. The drawio and svg name `990f96526bb8`. `check_submodule_docs`: 4 exact gitlinks. `check_diagram_pngs`: 6 source-bound rasters. |
| The adopted-change table covers #109 #110 #111 #114 #116 #113 with correct parent effects | yes | `SUBMODULES.md:31-38`. #116 changes only comments in `hdl` (a `KL_aecp_desc_mem_guard.sv` port comment and three `protocol_processor_top.sv` comments) plus test-driver deadlines, with no port change. #113 adds an internal `srp_evt_tk_latency_chg_w` term to `stri_events`; no `input`/`output` line of `protocol_processor_top.sv` changes between `265d6762` and `990f9652`. |
| The datapath no longer answers selectors 5/7 or the failure-code byte | yes | `milan_datapath.sv:4776-4800`. For an input, selector 4 returns `{dmac,16'd0}` or zero. Selector 5 answers outputs only. The selector-7 arm is gone, so selector 7 falls to `default: 64'd0`. The processor (`protocol_processor_top.sv:3095-3124`) suppresses `gsi_req_o` for input selectors 5/7 and replaces selector 4 `[15:0]` with `{code,8'd0}`. The code is gated at source (`KL_srp_listener_fsm.sv:858`); the bridge is gated on FAILED after a full-width index check. Output answers are unchanged: the deleted arm gave outputs zero, as `default` does. |
| `[GSI]` grades the processor fields for two sinks; tie-to-zero, wrong-sink and approximation mutants fail | yes | Clean `make notify`: 345/0 (`receipts/notify_clean.log`). `gsi_mutants.py`: 8/8, each named check failing (`receipts/gsi_mutants.log`). Failures per mutant: tie-bridge 7, selector 5 to parent 7, tie-code 7, code byte to parent 7, tie-status 17, wrong sink 30, approximation 10. |
| The notify path detects changes and invents none | yes, except G8 (F3) | P1 drops `lstn_gsi_changed_r` from `stri_events`: 33 failures, starting with the G1 push counts. P2 announces every record write: 8 failures, starting with the G1 duplicate probe (`receipts/probes_summary_P1-P5.txt`). |
| Every harness that binds a sink starts the restore walk | yes | `sim_main.cpp:2651`; `sim_nxn.cpp:2210,7899`; `sim_aclk.cpp:1165`; `sim_tdm8_render.cpp` via `boot_the_entity()` for T1 and the multi-stream binds; `pp_shadow` already drives `restore_go`. No other processor harness sends listener ACMP: `sim_crf_licence` plays the talker side only, and `sim_gptp`, `sim_gmstep`, `sim_prune` and `sim_ax1x1gptp` send none. P5 (walk never started) gives 122 failures, with no BIND_RX response and no PROBE_TX, which confirms the processor #109 hold. |
| `nvm_cosim` wires the arbiter, cause, abort and deadline as the top does | yes | `cosim_top.sv:253-371` against `protocol_processor_top.sv:2437-2600` at the pin: `m0_*` wired, `m1_*` tied idle, `p_*` wired, `m0_err_cause_o` to `nvm_err_cause_i`, `nvm_abort_o` to `m0_abort_i`. `RS_TMO_CYC_P` is `CLK_HZ_P/32'd50`, the default of `NVM_RS_TMO_CYC_P`. `make -C tb/verilator/nvm_cosim`: 465/465 checks, 39/39 mutants (`receipts/nvm_cosim.log`). |
| The merge resolutions keep both sides | yes | Every line either side added to the five conflicted files, relative to `573f0052`, is present in `cec6b99da` (`receipts/merge_keep_both.txt`). Two apparent exceptions are unions: the `.PHONY` line at `Makefile:202` carries every target of both, and the README measurement rows became one table whose "dev c266432d record" column carries dev's counts (`README.md:832-848`, read by hand). |
| Whether the latency notification reaches a milan_dp check | it does not, as the handoff states | P3 reverts processor #113 in a copy: 345/0, so no check sees it. P4 changes only AccumulatedLatency in G6's refresh: exactly the four G6 push counts fail (0 to 1), so the leg could observe the notification but nothing drives it (`receipts/probes_summary_P1-P5.txt`). |
| `check_port_contracts`, `measure_naming --check`, `measure_test_evidence --check` | all rc 0 | Allowances unchanged: processor 111 <= 111; naming 96 recorded; wall-clock 3 <= 3 (`receipts/gates_summary.txt`). |
| Redundancy path | not narrowed | The RTL change is selector arms and comments, with no port-count or single-port assumption. The GSI leg's 1x1-shape guard is test-only. |

These gates also returned rc 0 at the head:

- `pp_srcs --check --selftest`, `check_rtl_source_lists`, `lint_rtl --check` (90 <= 90);
- `docs_check`, `check_doc_style`, `check_doc_paths`, `gen_module_matrix --check`;
- `check_cpp_idiom`, `check_py_idiom`, `measure_test_evidence --selftest` (101/101);
- `check_em_dash --base c266432d` and `gen_toc --check` (both with the pinned renderer in a disposable venv);
- `git diff --check 573f0052 HEAD`.

Suite results: `pp_shadow` 371/0, `milan_dp aclk` 144/0, `milan_dp_render` 152/0, 60/0 and 5/5.

Hosted checks at the exact head, read only (`receipts/hosted_check_runs.tsv`):

- 21 check runs are `success`, including `rtl-fast`, `verilator-suites`, the five Verilator shards, `yosys-portability`, the four Yosys shards, `docs-check`, `docs-check-no-git`, `bdd-conformance` and `full-ci-gate`.
- One is `skipped`: "Physical gPTP (nightly and manual)". That context was skipped, not executed.

## Per-lens coverage lines

```text
[R306] PASS RTL - hdl/milan/milan_datapath.sv:4391-4800,6579-6700 and hdl/milan/KL_pp_shadow.sv:293-301,386-391 at 6a9828c1 - selector 4/5/7 arms, widths and default path checked against protocol_processor_top.sv:3055-3150 at 990f9652 (index checked before narrowing, bridge gated on FAILED, code gated at KL_srp_listener_fsm.sv:858); no net left unused (gsi_tkfail_w, gsi_bnd_w, pp_cd_srp_snk_fail_code_w still consumed); output answers unchanged; no clock, reset or CDC change; restore_go_i contract matches milan_datapath.sv:7557 and the firmware nvm_restore_walk(); nvm_cosim transcription equals the top's NVM wiring; lint 90 <= 90
[R306] PASS Robustness - tb/verilator/milan_dp/sim_nxn.cpp [GSI] G0/G6/G10 and probe P5 at 6a9828c1 - a missing descriptor answers NO_SUCH_DESCRIPTOR with a zero cdl-68 body; a reset clears both sinks; an unchanged refresh and a duplicate probe announce nothing; an out-of-range index is handled before narrowing (processor top :3107); without a walk the listener stays held (P5, 122 failures), and the silent-device walk deadline is CLK_HZ_P/50 in both the top and nvm_cosim; the firmware early-return path is publicly tracked in #495 and unreachable from a builder-accepted shape
```

The Conformance, Tests and Docs lenses were applied in full. Each is UNCLEAN only through F1-F4:

- **Conformance** confirmed acceptance 1, 3, 5 and 6 clean, and acceptance 2 apart from the F4 wording, as tabled above.
- **Tests** confirmed all seven mutants and probes P1-P5 fail their intended checks.
- **Docs** confirmed SUBMODULES, REGISTER_MAP `PP_CTRL`/`LWSRP`, INTEGRATION_GUIDE, TROUBLESHOOTING section 27, the compliance matrix and TESTING.md clean.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F3, F4) | issue #508 acceptance 1-6; processor top GSI owner/answer/`stri_events`; `05_acmp_engine.md` 6.1/6.4; `[GSI]` G0-G10; P3/P4 latency probes | R306-1 | `6a9828c172aa4d5d8ee49725e357a10bae2caa52` |
| RTL | CLEAN | `milan_datapath.sv` GSI block and SRP banners; `KL_pp_shadow.sv`; processor top at `990f9652`; `nvm_cosim/cosim_top.sv` against the top's NVM wiring; lint | R306-1 | `6a9828c172aa4d5d8ee49725e357a10bae2caa52` |
| Robustness | CLEAN | G0/G6/G10; P5 walk-hold probe; walk-deadline derivation; firmware `nvm_boot()` early return (#495) | R306-1 | `6a9828c172aa4d5d8ee49725e357a10bae2caa52` |
| Tests | UNCLEAN (F3) | `sim_nxn.cpp` `[GSI]`; `gsi_mutants.py` (8/8 re-run); probes P1-P6; `sim_main`/`sim_aclk`/`sim_tdm8_render` walk starts; `pp_shadow`, `nvm_cosim`, `aclk` and render re-runs; `measure_test_evidence` dispositions | R306-1 | `6a9828c172aa4d5d8ee49725e357a10bae2caa52` |
| Docs | UNCLEAN (F1, F2, F3) | CHANGELOG; SUBMODULES; diagram and manifest; REGISTER_MAP; INTEGRATION_GUIDE; TROUBLESHOOTING section 27; compliance matrix; TESTING.md; milan_dp README GSI section and measurement table; RTL/C++ comment citations | R306-1 | `6a9828c172aa4d5d8ee49725e357a10bae2caa52` |

## Limits

- **Banks not run.** I did not run the full parent, processor, gPTP, Yosys or builder banks, Docker/act, `act_ci` or its selftest, hardware, or physical calibration. The manager's source-validation banks and the hosted contexts are the evidence for those; I did not re-execute them. `xvlog_gate` was not run because this host has no Vivado.
- **Sweep not re-run.** The milan_dp default sweep was not re-run in full. I re-ran `obj_notify`, `gsi-mutants`, `aclk` and `milan_dp_render` only.
- **Clause text.** The Milan clause readings in F4 rest on the processor's cited architecture pages and clause numbers. The standard's own text was not available in this clone.
- **Job cap.** Two recipes used the simulator's built-in parallel C++ build (`-j 0`, up to 16 host threads): the `gsi_mutants.py` campaign and the `pp_shadow` build. Every run was sequential and in the foreground. All other builds were capped at 8, by `VERILATOR_JOBS=8` or `taskset -c 0-7`.
- **Renderer venv.** The pinned Markdown renderer was installed into a disposable venv under the packet's scratch directory, for `check_em_dash` and `gen_toc` only. Nothing was installed on the host.
- **Redaction.** Host-specific path prefixes in receipts were replaced with `<clone>`, `<packet>`, `<tool>` and `<VERILATOR_PREFIX>`.
- **Clone restored.** Probes edited only copies of the processor `hdl/` tree; `sim_nxn.cpp` was patched temporarily and restored byte for byte. After all probes and cleanup (`receipts/restore_verification.txt`):
  - the index tree is `e43b64d9...` and `git diff` is empty;
  - every tracked blob was re-hashed and matches;
  - gitlink modes and SHAs are as pinned;
  - the submodules are clean, with no ignored files.

## Pending manager duties

- Route F1-F4 to the executor. F4 needs a maintainer decision on #508, not a code change.
- At the merge turn, build and validate the final current-dev candidate (source base `573f0052`; live dev `c266432d` at review time), and own hosted/act acceptance. The Physical gPTP context was skipped at this head.
- After the fixes, re-cover:
  - Docs;
  - Tests, only if `sim_nxn.cpp` changes;
  - Conformance, once F3 and F4 close.

  RTL and Robustness stay covered unless a fix touches their scope.

## Addendum: prior and concurrent public findings at this head

I wrote this addendum after the verdict and ledger above, having read the concurrent external round `[R307]` (comment 5825730404) only at that point. It changes neither the verdict nor the ledger.

- **Round-1 author-declared BLOCKER (5822002238), decided in 5822047670: RESOLVED at this head.** It concerned three parent `docs-check` gates that refused processor content. Processor #116 (`265d6762`) fixed that content, and `check_port_contracts.py`, `measure_naming.py --check` and `measure_test_evidence.py --check` all return rc 0 here with unchanged allowances (`receipts/gates_summary.txt`).
- **[R307] F1 (MINOR, Docs, `CHANGELOG.md:113-116`): RETAINED.** Same defect as my F1.
- **[R307] F2 (MINOR, Conformance, acceptance 2): RETAINED.** Same defect as my F4.
- **[R307] S1 (SUGGESTION, Tests/Docs/Conformance, G8 push count): RETAINED as my F3, at MINOR.** The two rounds disagree on severity, and both readings stay on the record. I hold MINOR for two reasons. First, the suite README (`:481`) and the section banner state "exactly one" per transition, a property the leg measurably lacks at G8, so the document is wrong, not merely incomplete. Second, acceptance 4's "no fabricated transition" is left ungraded at that phase. [R307]'s extra observation is that both withdrawal pushes carry identical content, because the processor reads its owners live. That makes the second push a repeat of an unchanged state to the controller. It strengthens the case for grading G8's exact count and each push's content rather than weakening it. The Tests lens therefore stays UNCLEAN in this round's ledger.
- **[R307] S2 (SUGGESTION, Docs, `sim_tdm8_render.cpp:1419-1427`): RETAINED.** Same observation as my S1.
- **My F2 (stale processor line citations) was not reported by [R307]. RETAINED.**

R306-1 FINISHED
