[A270] REVIEW READY
Commit: a21cd3585abdd3cdf4ac5774a048361a66fed043 (branch `387-media-rebase`, local, not pushed; five one-line commits on `a9636e0f`)

Changed (assignment 5818091077, items 1-5):
1. **Wire boundary.** `KL_media_clock_restart.sv:236-238`: a streaming talker that has adopted a level no reported PDU has carried yet (`hold_r == 0`) keeps it as its target on a request, so the request merges. The merge line at `:230` is unchanged.
   - The banner (`:55-92`), the `GM_LOSS_RECOVERY.md` pending row and the PR text state the wire boundary. They also state where the engine measures it: the transmitted-PDU feed, the one the hold and MEDIA_RESET count.
   - tkdiag: T17 now expects one toggle and one MEDIA_RESET on talker 0 as well, because the step lands after its adoption and before any PDU at that level. The new T18 grades a step after the first PDU at the adopted level: a second toggle, counted twice.
   - `mcr_mutants.py` plants four engine defects, adding a window that ends at the adoption and one that stays open for the whole hold. T12 and T15 send one talker-1 PDU so their per-stream-hold checks still grade a hold.
2. **settime** (R277-3 F2). `sim_main.cpp:1028-1072` grades the leg's software settime as one more `mr` toggle and one MEDIA_RESET, in `obj_dir`, `obj_nolpf` and `obj_ax1x1` (233/233/230). `settime_no_mr` and the CRF-gated step are controls on a new option-off leg of `gmstep_mutants.py`, in the explicit `gmstep-mutants` campaign.
3. **Render stage.** `KL_render_setpoint.sv` banner and `recentre_p_i` spec name the PHC step and the settled clock-source change. Comment only.
4. **Margin.** The exact-head hosted shard 4/5 at `a9636e0f` (job 107720800104, candidate merge `1e3a115`) measured the `milan_dp` window at 2264.9 s, which leaves 435 s (16%) of 2700 s. Dev `57456af9` measured 2133.3 s. `CI_WORKFLOWS.md` records these next to the unchanged budget, and the PR text states the margin from them.
5. **Suggestions.** The PR status, the INTERNAL-source citation, the measurement next to the budget, and both runners now rebuild a stale clean binary.

Validation (all rc 0, never piped; Verilator 5.050, eight jobs):
- **`milan_dp` default `run`.** It ran as its 47 recipe commands from `make clean`, in six chunks, with every exit code recorded: 9781 checks, 0 failures. It ran at `c14f96ed`; the head differs by one README line.
- **gmstep.** gmstep passes 48/48. `make gmstep-mutants` gives 13/13: both positive legs and all eleven controls caught.
- **tkdiag.** 96/96, and mcr_mutants 5/5.
- **Full builder.** With the pinned SDK: ALL GATES PASS EXCEPT 1 NOT RUN (gate 11 report), 224/224 mutations. Without a compiler: EXCEPT 2 NOT RUN, 189/189.
- **Docs.** `docs_check` passes in both CI modes. `check_em_dash --base 57456af9`, `check_doc_style`, `gen_toc --check` and `check_doc_paths` pass.
- **Static.** `gen_module_matrix --check`, `xvlog_gate --check`, `check_rtl_source_lists`, `check_cpp_idiom` and `check_py_idiom` pass. `behave` passes 344 scenarios, and `git diff --check` is clean.
- **Extra.** `measure_test_evidence --check`, `lint_rtl --check` (90 <= 90), `test_firmware_compiler --absent` and the Yosys `milan_datapath` elaborate smoke all pass.

Reviewer probes, re-run unchanged:
- R276 `probe_pending_boundary.sh`: tkdiag 96/96, talker 0 one toggle.
- R276 `probe_step_gated_by_crf.sh`: killed, 233 checks with 2 failures.
- R277 D3/D4: pending=0 and one toggle, where the previous head gave 2.
- R277 base engine: killed, P1 = 21 and P4 = 21.
- R277 `plant.py`: `settime_no_mr`, `adjtime_no_mr` and `step_gated_by_source` are all killed in the option-off leg. `settime_no_mr` survived there before. On the gmstep leg it still survives 48/0, because that leg issues no settime.
- Every previously killed mutant still dies.
- Not run as-is: R276's builder clone script and R277's `cp -a` wrappers need a second git checkout, which this round may not create. Instead, `plant.py` ran unchanged and the same make recipe built the planted file. The builder banks cover F1.

Acceptance criteria: acceptance 3 is met digitally at this head, except for the open question below. Acceptance 4 stays the #117 bench step after merge.

Open risks/questions:
- **Decision requested.** R277-3's property probe P1 is NOT clean. It flags 10 requests over seeds 2, 3, 5 and 6; seeds 1 and 4 are clean, and P2-P4 are clean on all six.
  - A print-only copy places every one 0-3 cycles after the first launch at the adopted level. That is inside the probe's 3-cycle launch-to-report latency.
  - The engine sees a PDU only when the feed reports it. At such a request, its inputs are the same as in D3. So no engine on the existing ports can meet both D3/D4 = 1 and P1 in that model.
  - The same residue exists in hardware: a talker latches `mr` at launch (`KL_aaf_packetizer.sv:616`, `KL_crf_tx.sv:502`) and reports the PDU after sending it.
  - Options: (a) rule the feed report as "launched" and grade P1 there (implemented); or (b) add launch strobes from both talkers as new engine ports, with the probe driving them.
- **Margin.** 435 s hosted. Whether the three gmstep controls stay in the default `run` is a maintainer decision.

Packet: this round's output directory (`HANDOFF.md`, `PR-BODY.md`, `receipts/`, `MANIFEST.sha256`).
