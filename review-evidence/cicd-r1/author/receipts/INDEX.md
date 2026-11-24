# [A839] round 1 receipts (text only, uncompressed)

Raw logs, perf.data files and build trees stay in the lane's scratch (runs/); everything a reviewer needs to
re-check a figure in REPORT.md is here.

| Path | What it holds | REPORT section |
|---|---|---|
| identity.txt | every verdict-identity comparison, regenerated from the raw logs with tools/logcmp.py | 3, 4.1 |
| ab/VARIANT.SUITE.{perf,time,verdict,cmd} | per-suite perf-stat CSV (task-clock, cycles, instructions, cache, L1d, L1i, branch), /usr/bin/time, suite_tally --verdict, the command; VARIANT base = 300da99b, o2/o3 = testbench OPT_FAST forced, pub = probes.vlt, base2/m3 = model -O2/-O3 pair | 3.1, 3.2, 3.5 |
| talker/ts_{flat,vlt,vltO2,vltO3}.{perf,time}, outputs.md5 | crf_rx talker_step alone: --public-flat-rw vs probes.vlt (+ -O2/-O3); four outputs md5-identical | 3.2 |
| talker/perf-report-{flat,vltO2}.txt | perf record, top symbols, the two talker builds | 2.1 |
| budget/*.perf, *.time, outputs.md5 | CPU budget harness 8x8/1if bench, testbench -Os/-O2/-O3, three paired runs; every output md5 | 3.1 |
| prof/*.comm.txt, *.sym.txt, *.time | whole-suite perf record attribution by process and symbol: avtp_rxmon, nvm_cosim, milan_dp_gm_steps | 2, 3.3 |
| prof/milan_dp-gptp-60s.{sym.txt,perf} | milan_dp gPTP leg, 60 s: symbols and counters (IPC 0.93, L1d 4.9 %) | 4 (#10) |
| fwb/timeline.log, time.txt, perf.txt | firmware-boundary job command with per-line timestamps, /usr/bin/time -v, counters | 2.3 |
| ccache/{nocc,cold,warm}.time, verdicts.txt, cold.stats | crf_rx mutants and avtp_rxmon with and without ccache | 3.3, 4.1 |
| pre/*.perf, cancellation-verdicts.txt | preflight self-test timings; test_suite_cancellation before/after the runner change | 2.4 |
| bisect/follow_ring-pullin-bisect.txt, base-vs-probes-pullin.diff, *.vlt | follow_ring module bisect and the failing diff | 5.1 |
| bisect/portdef/*.sv, *.cpp | minimal reproduction of the defaulted-input-port initialisation | 5.1 |
| shards/ | hosted-shard replica summaries (out, time, perf per run) | 4.1 |
| tools/ | the scratch scripts that produced all of the above (absuite.sh, shard.sh, profsuite.sh, logcmp.py, perftab.py, receipts.sh, ...) | all |
