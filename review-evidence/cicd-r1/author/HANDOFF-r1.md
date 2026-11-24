# [A839] CICD improvement — round 1 handoff

Status (2026-11-24 12:25 CET): ROUND 1 DONE. 3 commits, validated; REPORT.md, REVIEW-READY.md, PR-BODY.md and
receipts/INDEX.md written. Not pushed, no PR, no comments (as instructed). Lane clean at the head below; the
scratch worktrees are removed (git worktree list shows only the lane).

Head: fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f (cicd-verilator-perf, on the train head 300da99b):
- 427b7f4f  probes.vlt in place of --public-flat-rw: crf_rx, mmcm_servo, aaf_clock_meter, maap
            (+ the seven command-table Verilator patterns, TESTING.md)
- f09c9a0f  run_all_suites.sh: OBJCACHE=ccache where ccache is installed (local sweeps / native bank; hosted has none)
- fcbc31f3  ctrl_service_budget/build.py: testbench at -O3 (OPT_FAST) with its model
The hosted-shard replicas ran at 32e8ed4f, the same tree but one TESTING.md sentence (git diff 32e8ed4f fcbc31f3 =
docs only); 32e8ed4f is no longer on the branch.

Results (REPORT.md has the tables; receipts/identity.txt every comparison):
- Kept levers change no verdict: crf_rx, mmcm_servo, aaf_clock_meter, maap whole-suite logs byte-identical to
  300da99b (mutants included); CPU -37 / -26 / -27 / -10 %.
- Hosted-shard replicas (run_all_suites.sh --ci-pieces --shard N/19, 4 CPUs, loaded host): base shards 7 and 11
  each lost a suite to the 1800 s guard (mmcm_servo, crf_rx: exit 92); head shards 7, 9, 11 passed every suite
  (1058, 487, 18068 checks) with identical logs and case receipts. Hosted estimate: shard 11 28.6 -> ~20-22 min,
  shard 7 23.1 -> ~18.6, shard 9 18.2 -> ~14.5; the slowest hosted job becomes shard 1 (26.4 min, untouched).
- The owner's speed-over-size premise does not hold: the models already compile at -O2 (-O3 budget/gPTP legs);
  only the testbench was -Os, and -O2/-O3 there moves instructions < 1 % and costs compile time => not applied
  centrally (budget harness only). Model -O3: 0-6 %, inside the noise => not applied.
- ccache: crf_rx mutants -47 % CPU cold, avtp_rxmon -65 % cold (both identical). Hosted needs ccache installed.

**For the manager, outside this lane (worth its own Issue, REPORT 5.1):** Verilator 5.050/5.054 writes a defaulted
input port's default (`input wire [7:0] x = '0`) into the CONNECTED net at time zero when the port is not public;
a top-level input the harness set before its first eval() then stays at the default. Silent under -Wall. This
broke follow_ring when --public-flat-rw was dropped (lb_wire_chans_i tied to the top input pcm_chans_i). 11
defaulted inputs exist (KL_chan_map_capture 8, KL_crf_tx, KL_aaf_packetizer, protocol_processor_top); milan_datapath
ties its ones to internal, re-driven nets, so its suites are probably unaffected, but a census of wrappers that tie
one to a top-level input needs an owner. Minimal repro: receipts/bisect/portdef/.

Other findings for Issues: firmware-boundary is 93 % serial builder compiles (job split, REPORT 5.2);
ci_tool_inventory.py --check is red at the base (13+ stale hashes incl. run_all_suites.sh, REPORT 5.3).

Round-2 candidates (REPORT 4): ccache on the hosted runner; media_phase probes.vlt once 5.1 is settled (-66 %);
preflight once per head; firmware-boundary split; milan_dp --threads (its models are L1d-bound, IPC ~0.9-1.2);
per-suite model -O3 on a quiet host.

Session note: commands longer than the 10-minute foreground limit (suite and shard runs) ran as background tasks of
this session and were waited on; all of them finished before this handoff.

REVIEW READY fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f
