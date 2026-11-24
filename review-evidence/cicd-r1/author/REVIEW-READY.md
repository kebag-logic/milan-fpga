[A839] REVIEW READY
Commit: fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f (branch cicd-verilator-perf, on the train head 300da99bee; eventual base dev-soft-core)

Commits (one-line subjects, no trailers):
- 427b7f4fe3117a830523f30dfd680e385ad7b56c  Make only the probed signals public in crf_rx, mmcm_servo, aaf_clock_meter and maap, in place of --public-flat-rw: the same logs for 10-37 % less CPU
- f09c9a0fc99098cb48aa9d2386399ceb079a278b  Let the suite sweep compile through ccache where it is installed, so mutant rebuilds reuse the Verilator runtime and the testbench: crf_rx's mutants 47 % less CPU, the same results
- fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f  Compile the CPU budget harness's testbench at -O3 with its model, past Verilator's -Os default for it: 2.5-5 % less CPU on the 8x8/1if fixture, the same output

Changed:
- tb/verilator/{crf_rx,mmcm_servo,aaf_clock_meter,maap}/Makefile: `--public-flat-rw` -> `probes.vlt`; new
  probes.vlt per suite listing exactly the internal signals the harness touches (public_flat_rw where the harness
  writes: crf_rx pdu_count_o/fmt_err_o, maap lfsr_r; public_flat_rd elsewhere). follow_ring and media_phase keep
  --public-flat-rw (REPORT 5.1).
- ci/image/command-table.json: the seven Verilator argument patterns of those builds follow the Makefiles.
- scripts/run_all_suites.sh: `OBJCACHE=ccache` when ccache is on PATH and the caller set no OBJCACHE.
- tb/verilator/ctrl_service_budget/build.py: `OPT_FAST=-O3` on its `make -f Vsim.mk` (testbench level).
- docs/testing/TESTING.md section 1: the ccache behaviour, the probes.vlt rule and the defaulted-port hazard.
No RTL, firmware, owner bound, test expectation or graded figure changed.

Validation (exact commands; host: 96 vCPU EPYC VM under load 95-128 from other lanes; every timing pair concurrent
on disjoint 4-CPU sets with the hosted job budgets; pinned Verilator 5.050):
1. Whole-suite identity, base 300da99b vs the change, `make -C tb/verilator/<suite>` (VERILATOR_JOBS=SIM_JOBS=4,
   MAKEFLAGS=-j1 --no-print-directory), logs compared after removing only host text (bin/logcmp.py):
   crf_rx IDENTICAL (2609 lines), mmcm_servo IDENTICAL (389), aaf_clock_meter IDENTICAL (122),
   maap IDENTICAL (382; one make `rm` echo of an intermediate file dropped). CPU -37 / -26 / -27 / -10 %.
2. Hosted-shard replicas through the real runner, `scripts/run_all_suites.sh LOGS --ci-pieces --shard N/19`,
   base worktree at 300da99b vs head worktree at 32e8ed4f (= fcbc31f3's tree but one TESTING.md sentence):
   - shard 11, head without ccache (OBJCACHE= , the hosted case): 3/3 PASS, 18068 checks, 1958 s wall;
     base: crf_rx TIMEOUT at its 1800 s guard (exit 92) on this host; maap__3 and media_grid_align logs and the
     maap__3 case receipt IDENTICAL; head crf_rx log IDENTICAL to the base direct run (2606 lines).
   - shard 11 head with ccache: 3/3 PASS, 1788 s wall.
   - shard 9 head (ccache): 2/2 PASS, 487 checks, 1274 s vs base 2255 s; maap__2 and aaf_clock_meter logs and
     the maap__2 receipt IDENTICAL.
   - shard 7, head without ccache: 2/2 PASS, 1058 checks, 2135 s wall; base: mmcm_servo TIMEOUT at its 1800 s
     guard (exit 92); pp_shadow__0 log IDENTICAL; head mmcm_servo log IDENTICAL to the base direct run (386 lines).
   The runner's own preflight self-tests (test_suite_cancellation, suite_tally, suite_shards,
   check_merge_containment, check_results_fresh, check_list_hermetic, xvlog_gate, check_merge_review_integrity)
   passed in every head shard; `python3 scripts/test_suite_cancellation.py` also passed on the runner as committed.
3. ccache: crf_rx `python3 mutants.py` no cache 498 CPU-s, cold 262, warm 229; 23/23 and logs IDENTICAL.
4. Budget harness: the committed make argv on a copy of the 8x8/1if native model builds a Vsim byte-identical to
   the measured -O3 variant; its 2.8 MB output md5 f1630111e1f8 equals the -Os, -O2 and -O3 runs (3 paired runs:
   CPU 254/257/256 s -> 242/250/250 s).
5. Gates at fcbc31f3: check_em_dash --base 300da99bee (pinned renderer) 0 findings over 10 added lines;
   check_doc_style OK; check_hygiene --check PASS; check_sh_idiom, check_py_idiom within budget; check_doc_paths OK;
   check_rtl_source_lists OK; check_port_contracts, check_wire_accountability, check_entity_shape PASS;
   check_tied_inputs PASS.
Not run: the full local sweep (run_all_suites.sh with no shard) and syn/yosys/run.sh — the manager's native bank
covers the sweep; no RTL or Yosys input changed. `ci_tool_inventory.py --check` cannot run green at the base (REPORT
5.3), so neither before nor after is evidence.

Acceptance (the round's brief): kept levers change no verdict (above); measured per suite and per shard (REPORT 3,
4.1); hosted estimate per changed job: shard 11 28.6 -> ~20-22 min, shard 7 23.1 -> ~18.6, shard 9 18.2 -> ~14.5, the
pieces of maap ~-10 % each (shards 3, 8, 9, 11); rtl-fast firmware-boundary unchanged (not touched, REPORT 5.2).
The central testbench OPT_FAST was measured and NOT applied (no return, extra compile: REPORT 3.1).

Open risks/questions:
- REPORT 5.1 (Verilator initialises the net on a defaulted input port when the port is optimised): needs its own
  Issue and an owner census of wrappers that tie such a port to a top-level input.
- The command table's script hashes are stale at the base for 13+ scripts, run_all_suites.sh among them; this
  change does not refresh them (REPORT 5.3).
