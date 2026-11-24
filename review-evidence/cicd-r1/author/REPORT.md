# [A839] CICD improvement, round 1: measurements and ranked levers

**Summary.** The models were never at -Os: every suite's `-CFLAGS -O2` overrides Verilator's default for the model
and runtime; only the testbench C++ was at -Os, and moving it to -O2/-O3 changes nothing measurable except compile
time (not applied, except the CPU budget harness: -2.5..-5 %). Model -O3 is 0-6 %, inside the noise (not applied).
The profile pointed elsewhere: `--public-flat-rw` makes Verilator re-evaluate the whole input-combinational network
every eval (45 % of crf_rx talker_step's cycles; L1i-bound). Replacing it with per-suite probes.vlt files cuts
crf_rx -37 %, mmcm_servo -26 %, aaf_clock_meter -27 %, maap -10 % CPU with byte-identical logs, and on local
hosted-shard replicas the base shards 7 and 11 lost a suite to the 1800 s guard while the head shards finished every
suite. Estimated hosted shard 11 (the 28.6-min slowest): ~20-22 min. ccache cuts mutant and multi-build suites
47-65 % CPU even on a cold cache (adopted where installed; hosted needs an install). The same probe experiment found
a silent Verilator hazard (5.1): a defaulted input port's default is written into the connected net at time zero
when the port is optimised, which broke follow_ring; follow_ring and media_phase keep --public-flat-rw. Three
commits: 427b7f4f, f09c9a0f, fcbc31f3.

Head measured: 300da99b (train head of PR #988). Host: AMD EPYC 9554P VM, 96 vCPU, load 70-110 from other
lanes throughout, so wall times are inflated and noisy; every A/B pair ran CONCURRENTLY on disjoint 4-CPU
sets (the hosted runner's size) with the hosted job budgets (CI_BUILD_JOBS=VERILATOR_JOBS=SIM_JOBS=4,
MAKEFLAGS=-j1 --no-print-directory), and the decision figures are perf counters (task-clock, instructions,
cycles), which load moves far less than wall time. Toolchain: pinned Verilator 5.050, g++ 16.1.1, make 4.4.1
(4.3, the hosted runner's, checked for the MAKEFLAGS behaviour). Raw data: /data-2/milan/tmp/cicd-a839/runs/.

Verdict identity rule used throughout: the suite's whole log is compared after removing ONLY host-dependent
text (Verilator build-statistics lines and warning text, make directory chatter, compiler command echoes, the
scratch tree path, temp-dir names, PIDs); every check line, figure and verdict must be byte-identical. No
time or number masking. Suites whose legs run in parallel (follow_ring) interleave lines nondeterministically;
those are compared as a multiset of tokens, which still catches any changed number or verdict word
(bin/logcmp.py).

## 1. What the builds actually do (from the generated Makefiles, not assumed)

| Setting | Value at 300da99b | Evidence |
|---|---|---|
| OPT_FAST / OPT_SLOW / OPT_GLOBAL defaults | -Os / (none) / -Os | pinned `include/verilated.mk` |
| Model files (`$(VK_OBJS_FAST)`), runtime (`$(VK_GLOBAL_OBJS)`) | `$(CXX) $(OPT_FAST) $(CXXFLAGS) $(CPPFLAGS)`: the suite's `-CFLAGS -O2` comes LATER and wins | verilated.mk compile rules |
| Testbench C++ (`sim_main.cpp` etc., the generated per-file rule) | `$(CXX) $(CXXFLAGS) $(CPPFLAGS) $(OPT_FAST)`: **-Os comes last and wins** | generated `V*.mk`, e.g. talker_step: `-std=c++17 -O2 -Os -c -o sim_talker_step.o` |
| Effective model level | -O2 in 116 of 121 build sites; -O3 in the budget harnesses and milan_dp's gPTP legs | static census + hosted logs (manager's shard map) |
| --threads / --trace / --x-assign / --x-initial | none / none (one suite) / default fast / default unique | census over all suite Makefiles and drivers |
| --public-flat-rw | 6 suites: crf_rx, mmcm_servo, follow_ring, aaf_clock_meter, media_phase, maap | census |
| ccache | not used anywhere: OBJCACHE empty, ccache not installed on the hosted runner or in the CI image | verilated.mk `OBJCACHE ?=`, workflows, ci/image/Dockerfile |
| Hosted runner | ubuntu-24.04, 4 vCPU, GNU make 4.3 | rtl.yml |

## 2. Where the time goes

### 2.1 Simulation (perf record, crf_rx talker_step, the single longest simulation: 75 % of crf_rx)

With `--public-flat-rw` (as shipped):

| Share of user cycles | Symbol |
|---:|---|
| 23.7 % | `___ico_sequent__TOP__0` (input-combinational settle) |
| 21.1 % | `___eval_ico` |
| 9.3 % | `___nba_sequent__TOP__7` |
| 8.2 % | `___eval_triggers_vec__ico` |
| 6.2 % | `___eval_phase__act` |
| 4.5 % | `pthread_mutex_trylock` (runtime, per eval) |
| 4.0 % | `VlDeleter::deleteAll` (runtime, per eval) |
| 2.4 % | the harness's own `event()` |

With only the probed signals public (probes.vlt), the ico settle work is gone; what is left is the model's
sequential logic and the pinned runtime's per-`eval()` bookkeeping: `pthread_mutex_trylock` 10.6 %,
`VlDeleter::deleteAll` 6.6 %, `VerilatedThreadMsgQueue::flush` 5.8 %, `Verilated::endOfEval` 4.4 % (about 28 %
together). `eval_step()` calls `deleteAll()` (a mutex lock) and `endOfEval()` unconditionally on every eval; that
cost is inherent to the pinned runtime and is only reducible by fewer `eval()` calls in the harness, which is out of
this round's scope. The testbench C++ is 2-4 % of cycles in every simulation profiled: the simulations are
model-bound, which is why the testbench optimisation level barely moves them (section 3).

### 2.2 Builds

Small model (crf_rx talker_step), one core: Verilator runtime `verilated.cpp` 7.2 s, `verilated_threads.cpp`
2.7 s, `verilated_dpi.cpp` 1.7 s; the generated model 2.1 s; the testbench 1.4 s. The runtime, identical for every
build of the same flags, is 77 % of a small model's compile CPU and is recompiled by every build and every mutant.

### 2.3 firmware-boundary (`ctrl_boundary.py --require-rv32 --selftest --without verilator`), local, 4 CPUs

It runs no Verilator. Timeline (seconds from start; the gate runs its builders one after another):

| Phase | Seconds | Share |
|---|---:|---:|
| `fw_rv32_selftest.py --require-rv32` | 16 | 1 % |
| `test_ctrl_firmware.py --require-rv32 --build-only --jobs 4` (host `g++ -std=c++20 -O1 -g` over every shape) | 1366 | 50 % |
| `test_ctrl_nvm.py --build-only` | 166 | 6 % |
| `fw_coverage.py --build-only` | 631 | 23 % |
| `stream_counter_f5.py --build-only` x2, `test_ctrl_memory.py` | 94 | 3 % |
| judging the 4326-invocation capture, the 100+ boundary controls, pin controls, stack gate | 474 | 17 % |
| **total** | **2747** (hosted: 25.8 min) | |

`/usr/bin/time`: 3061 s user + 449 s sys over 2747 s wall = **127 % CPU on the 4 CPUs it was given**. On the
hosted runner the same 3510 CPU-s in 25.8 min is ~2.3 of 4 cores busy. The time is the firmware builders' own
compiles, run serially, each internally parallel to 4 jobs but with long serial tails. Those compiler invocations
are what the gate judges, so neither their flags nor a compiler wrapper (ccache) may change without the gate's own
review; the safe levers are structural (section 4, not implemented this round).

### 2.4 Preflight (every shard)

| Gate | Wall | CPU (user+sys) | Nature |
|---|---:|---:|---|
| test_suite_cancellation.py | 69.8 s | 38.8 s | real signals against owner-stated second windows (grace 2 s, verdict 14 s, vanishing 24 s ...): half of it is deliberate waiting |
| check_merge_containment.py --selftest | 56.7 s | 54.8 s | throwaway git repositories; sys-heavy |
| xvlog_gate.py --selftest | 35.2 s | 35.1 s | pure Python |

## 3. Lever measurements

Columns: wall s (contended host, for orientation only), CPU s = perf task-clock over the whole suite including
its builds and mutants, instructions and cycles in units of 10^12, IPC, L1d load misses (rate of loads), the
`cache-misses` generic event (rate of `cache-references`), L1i load misses, branch misses. base = 300da99b as
committed; o2/o3 = testbench OPT_FAST forced to -O2/-O3; pub = probes.vlt in place of --public-flat-rw.

### 3.1 Testbench -Os -> -O2 / -O3 (the owner's speed-over-size directive)

| run | wall s | CPU s | instr T | cycles T | IPC | L1d misses G (rate) | cache-misses M (rate) | L1i misses M | identity vs base |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| crf_rx base | 1937 | 1870 | 10.12 | 4.77 | 2.12 | 24.00 (0.535 %) | 11908 (7.58 %) | 3432 | |
| crf_rx o2 | 1963 | 1897 | 10.13 | 4.80 | 2.11 | 24.67 (0.551 %) | 12253 (7.66 %) | 3988 | IDENTICAL (2609 lines) |
| crf_rx o3 | 1505 | 1670 | 10.17 | 4.34 | 2.34 | 26.79 (0.603 %) | | | IDENTICAL |
| media_phase base | 1450 | 3251 | 22.58 | 8.45 | 2.67 | 8.31 (0.124 %) | 3208 (3.47 %) | 2277 | |
| media_phase o2 | 1168 | 3240 | 22.40 | 8.51 | 2.63 | 7.44 (0.113 %) | 3124 (3.52 %) | 3147 | IDENTICAL (611) |
| media_phase o3 | 1198 | 3168 | 22.41 | 8.44 | 2.66 | 7.85 (0.119 %) | | | IDENTICAL |
| gptp_plane base | 1209 | 1176 | 8.05 | 3.06 | 2.63 | 3.10 (0.079 %) | 1134 (6.66 %) | 556 | |
| gptp_plane o2 | 1210 | 1189 | 7.98 | 3.11 | 2.57 | 2.87 (0.073 %) | 1060 (5.93 %) | 390 | IDENTICAL (39) |
| gptp_plane o3 | 1468 | 1238 | 7.98 | 3.20 | 2.50 | 2.81 (0.072 %) | | | IDENTICAL |
| follow_ring base | 1206 | 4376 | 21.90 | 11.31 | 1.94 | 10.92 (0.111 %) | 4246 (0.65 %) | 18072 | |
| follow_ring o2 | 1245 | 4457 | 22.02 | 11.53 | 1.91 | 11.77 (0.119 %) | 4564 (0.66 %) | 47789 | IDENTICAL (token multiset, 5792) |
| aaf_clock_meter base | 1653 | 1950 | 10.58 | 5.03 | 2.10 | 36.83 (0.762 %) | 18995 (11.61 %) | 3980 | |
| aaf_clock_meter o2 | 1649 | 2010 | 10.81 | 5.20 | 2.08 | 41.22 (0.835 %) | 20232 (11.68 %) | 4400 | IDENTICAL (122) |
| mmcm_servo base | 1958 | 1938 | 14.66 | 5.12 | 2.86 | 3.48 (0.058 %) | 1538 (3.60 %) | 799 | |
| mmcm_servo o2 | 1882 | 1862 | 14.59 | 4.91 | 2.97 | 3.53 (0.059 %) | 1530 (3.56 %) | 1075 | IDENTICAL (389) |
| budget 8x8/1if bench, tb -Os (3 paired runs) | 260 | 254 / 257 / 256 | 0.74 | 0.68 | 1.09-1.10 | 3.65-3.95 (1.17-1.26 %) | | 3616-3738 | |
| budget, tb -O2 | 257 | 254 | 0.73 | 0.68 | 1.08 | 3.96 (1.289 %) | | 4087 | md5 identical (2.8 MB log) |
| budget, tb -O3 (3 paired runs) | 248 | 242 / 250 / 250 | 0.73 | 0.64-0.67 | 1.09-1.14 | 3.37-3.46 (1.10-1.13 %) | | 3456-3761 | md5 identical |

Reading: the testbench optimisation level does not change the work: instructions stay within +-1 % on every suite
(the models dominate: the harness is 2-4 % of talker_step's cycles and 0.4 % of milan_dp's), and the cycle
differences track the host load at the time of each batch, not the flag (o3 ran in a later, differently loaded
window). It costs compile time: milan_dp's 614 KB `sim_nxn.cpp` compiles in 8.7 s at -Os, 13.9 s at -O2, 12.8 s
at -O3, and it is compiled once per nxn case. Only the CPU budget harness, whose large `sim_main.cpp` runs a
memory model per access, gains, consistently in three paired runs: -O3 2.5-5 % less CPU and 7-9 % fewer L1d
misses, -O2 nothing. Decision: OPT_FAST is set for the budget harness only (commit 3); the central sweep is left
at Verilator's default, because applying it there measured as compile cost with no run-time return.

The models themselves are not at -Os: every suite's `-CFLAGS "-O2"` (or -O3) lands after OPT_FAST in the model and
runtime rules. Model -O2 -> -O3: see 3.5.

### 3.2 `--public-flat-rw` -> probes.vlt (only the signals each harness touches)

| run | wall s | CPU s | instr T | cycles T | IPC | L1d misses G (rate) | cache-misses M (rate) | L1i misses M | identity vs base |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| talker_step alone, --public-flat-rw | 1266 | 1083 | 7.29 | 2.85 | 2.56 | 0.61 (0.018 %) | 97 (0.37 %) | **1399** | |
| talker_step alone, probes | 741 | **573** | 3.71 | 1.50 | 2.47 | 0.31 (0.018 %) | 26 (0.89 %) | **6** | md5 identical |
| talker_step, probes + tb/model -O3 | 799 | 549 | 3.58 | 1.43 | 2.50 | 0.29 (0.018 %) | 26 (0.66 %) | 6 | md5 identical |
| crf_rx suite, probes | 1008 | **1170** (-37 %) | 6.52 | 2.99 | 2.18 | 22.66 (0.799 %) | 11710 (13.82 %) | 1880 | IDENTICAL (2609) |
| mmcm_servo suite, probes | 1470 | **1437** (-26 %) | 10.03 | 3.75 | 2.68 | 3.28 (0.077 %) | 1419 (6.09 %) | 376 | IDENTICAL (389) |
| aaf_clock_meter suite, probes | 1128 | **1431** (-27 %) | 6.91 | 3.64 | 1.90 | 37.13 (1.218 %) | 19141 (14.14 %) | 3017 | IDENTICAL (122) |
| maap suite, probes | 1525 | **2051** (-10 %) | 7.68 | 5.14 | 1.49 | 103.23 (3.560 %) | | | IDENTICAL (382; one make `rm` echo dropped) |
| media_phase suite, probes | 436 | **1112** (-66 %) | 6.87 | 2.86 | 2.40 | 5.96 (0.190 %) | 2840 (8.31 %) | 501 | IDENTICAL (611) -- NOT adopted, see 5.1 |
| follow_ring suite, probes | 457 (rc 2) | | | | | | | | **43 FAILURES** -- dropped, see 5.1 |

Locality: the lever removes work rather than reshuffling it, so absolute misses fall with it. On talker_step,
the one simulation measured in isolation, L1i misses fall 1399 M -> 6 M (-99.6 %: the --public-flat-rw model's
hot code did not fit the 32 KB L1i), L1d misses -49 %, cache-misses -73 %; per-access miss RATES are unchanged
or higher and IPC falls slightly (2.56 -> 2.47) because the cheap, cache-friendly ico re-evaluation is what went.
The whole-suite rows include the suites' C++ compiles (each suite's cache-misses are mostly cc1plus), so their
rates mix compile and simulation; their CPU columns are the decision figures.

A probe missing from probes.vlt still COMPILES (Verilator keeps the variable in the root structure whether or
not it is public), so a compile is no proof the list is complete; each list was taken from every `__DOT__` and
`rootp->` name in the harness sources (including macros such as media_phase's `R(n)`) and written public_flat_rw
only where the harness writes (crf_rx's [G1] preloads, maap's LFSR preload).

### 3.3 ccache (OBJCACHE)

| crf_rx `mutants.py` (23 rebuild-and-run cases) | wall s | CPU s (user) | result |
|---|---:|---:|---|
| no cache (today, hosted and local) | 377 | 498 | 23/23, log IDENTICAL |
| ccache, cold cache (first use in a job) | 247 | 262 (-47 %) | 23/23, IDENTICAL |
| ccache, warm cache | 219 | 229 (-54 %) | 23/23, IDENTICAL |

Within one run the mutants share the Verilator runtime (verilated*.cpp, ~11.6 CPU-s per build) and the unchanged
testbench, so even a cold cache hits 66 % of compiles. avtp_rxmon's whole-suite profile is 94.8 % `cc1plus`
(eight builds plus five mutant drivers): the hosted suites are as much compile-bound as simulation-bound.

### 3.4 Rebuild census

Echoed Verilator builds in the eight profiled suites: 19, none with an identical command line; mutant builds are
quiet (make -s) and differ by construction (a planted RTL edit). So the avoidable recompilation is not repeated
models but the per-build Verilator runtime and unchanged testbench/model objects, which is what ccache recovers.
A runtime configuration file in place of -G/-D parameters would not help the measured suites: their -G values
change what the RTL elaborates (clock rates, shapes, window sizes), and the -D testbench defines only mirror them
(`derive-never-mirror` rule in the Makefiles), so the same RTL is never rebuilt for a pure testbench value.

### 3.5 Model -O2 -> -O3 (the suite's `-CFLAGS`, which is what decides the model's level)

| run (paired, concurrent) | wall s | CPU s | instr T | cycles T | IPC | L1d misses G (rate) | identity |
|---|---:|---:|---:|---:|---:|---:|---|
| media_phase, model -O2 (as committed) | 1784 | 3538 | 22.52 | 9.12 | 2.47 | 8.51 (0.126 %) | |
| media_phase, model -O3 | 1454 | 3318 (-6 %) | 22.17 | 8.72 | 2.54 | 11.76 (0.177 %) | IDENTICAL (605) |
| gptp_plane, model -O2 | 1435 | 1222 | 8.05 | 3.19 | 2.52 | 3.55 (0.090 %) | |
| gptp_plane, model -O3 | 1418 | 1225 (+0 %) | 8.05 | 3.21 | 2.51 | 3.45 (0.087 %) | IDENTICAL (35) |
| talker_step, model+tb -O2 -> -O3 (3.2) | | 569 -> 549 (-4 %) | 3.66 -> 3.58 | 1.48 -> 1.43 | | | md5 identical |
| milan_dp__0 (gPTP legs already -O3), tb -O2 | 3515 | 5005 (+1.5 % vs base 4932) | 15.37 | 13.05 | 1.18 | 285.8 (4.36 %) | IDENTICAL (4243 + case receipt) |

-O3 is worth 0-6 % on these models, inside about twice this host's paired-run noise, and it raises L1d misses
where it helps (media_phase +38 %: more unrolled code over the same state). Not adopted this round: the owner's
"whichever measures faster" is -O2 by a margin this host cannot resolve, at a lower compile cost. A per-suite pass
with repeated paired runs on a quiet host is the way to settle the 4-6 % cases (crf_rx, media_phase).

## 4. Ranked table

Hosted estimate = the hosted suite time on 300da99b (manager's shard map, run 45326076983) times the measured local
CPU ratio (head / base) of the same suite; shard estimate = the shard's hosted time less the suites' savings. The
local hosted-shard replicas (run_all_suites.sh --ci-pieces --shard N/19, 4 pinned CPUs, base and head side by
side) are in 4.1.

| # | Lever | Status | Speedup (measured) | Hosted effect (estimate) | Verdict identity | Risk |
|---:|---|---|---|---|---|---|
| 1 | probes.vlt in place of --public-flat-rw: crf_rx, mmcm_servo, aaf_clock_meter, maap | **commit 427b7f4f** | CPU -37 / -26 / -27 / -10 % | crf_rx 17.2 -> ~10.8 min, mmcm_servo 17.3 -> ~12.8, aaf_clock_meter 12.5 -> ~9.2, maap pieces 18.7 -> ~16.8 runner-min; **shard 11 28.6 -> ~20-22 min** (the local replica's crf_rx ratio, <=0.52, gives ~20; the direct A/B CPU ratio 0.63 gives ~21.7), shard 7 23.1 -> ~18.6, shard 9 18.2 -> ~14.5; ~16 runner-min per run; the slowest hosted job becomes shard 1 (26.4 min, untouched) | whole-suite logs byte-identical (normalised only for host text), mutants included | low: the four models contain no input port with a default value (5.1), so the one known way an optimised build diverges cannot apply; every harness `__DOT__`/`rootp->` name is listed |
| 2 | ccache through OBJCACHE in run_all_suites.sh | **commit f09c9a0f** | crf_rx mutants CPU -47 % cold, -54 % warm | none on hosted today (no ccache on the runner or in the CI image); local sweeps, act replay on this host and the native bank only | crf_rx mutants identical | low: content-addressed cache; a caller's OBJCACHE (empty included) wins |
| 3 | budget harness testbench -O3 (OPT_FAST in build.py's make) | **commit fcbc31f3** | CPU -2.5..-5 %, L1d misses -7..-9 % (3 paired runs) | none (not a hosted job); CPU budget rounds | 2.8 MB output md5-identical in all runs | low |
| 4 | probes.vlt for media_phase | measured, NOT adopted | CPU -66 %, instructions -70 % | 12.4 -> ~4.2 min; shard 5 14.2 -> ~6 | identical | blocked on 5.1: its wrappers connect two defaulted ports (to internal, re-driven nets, so probably safe; adopt once 5.1 is settled) |
| 5 | probes.vlt for follow_ring | DROPPED | (suite 457 s vs 1206 s, but wrong) | -- | **43 failures** | changes the simulated DUT (5.1) |
| 6 | central testbench OPT_FAST (-O2/-O3) for every suite | measured, NOT adopted | instructions +-1 %, CPU within noise on 7 suites | slightly negative: +4-5 s compile per large testbench (milan_dp sim_nxn.cpp x4 cases) | identical everywhere | none semantically; no return |
| 7 | ccache on the hosted runner (install + actions/cache keyed by toolchain and inputs) | recommended | avtp_rxmon is 95 % cc1plus; mutants -47 % even cold | compile-bound suites and every mutant bank; needs a pinned installer entry, the command table and the tool inventory (which is red at the base, 5.3) | -- | medium (workflow + inventory work) |
| 8 | preflight self-tests once per head (one job; shards check its SHA) | recommended | -- | ~80 s off every shard, ~25 runner-min per run | -- | medium: required-context and cancellation-contract design |
| 9 | split firmware-boundary's builder capture across two jobs (ctrl_boundary already takes repeatable --capture) | recommended | the job is 93 % builder compiles run serially at 127 % CPU of 4 | 25.8 -> ~14 min max job | -- | medium: the gate's capture semantics are what it proves |
| 10 | milan_dp model: --threads 2 per case with --jobs 2 per piece | to measure (round 2) | gPTP leg is L1d-bound: IPC 0.93, 4.9 % L1d miss rate, harness 0.4 % | the 23-min milan_dp__0 is now the slowest piece after #1 | -- | thread scheduling is deterministic in Verilator, but needs the same identity proof |
| 11 | model -O3 in the heaviest Makefiles | see 3.5 | | | | |

### 4.1 Hosted-shard replicas (local)

`scripts/run_all_suites.sh LOGS --ci-pieces --shard N/19` from a worktree at the base (300da99b) and one at the
head (32e8ed4f, the same tree as fcbc31f3 but one TESTING.md sentence), side by side, each on 4 pinned CPUs with
rtl.yml's job budgets; the preflight self-tests included. "head, no ccache" sets `OBJCACHE=` (empty), which the
runner keeps: the hosted runner's situation. Per-suite seconds from the suite logs' completion times. The host was
at load 95-128 throughout, so absolute times run 1.3-2x the hosted ones; the ratios are the information.

| Shard (hosted) | Run | Wall s | CPU s | Result | Per suite (s) |
|---|---|---:|---:|---|---|
| 11 (28.6 min) | base | >2690 | | **exit 92: crf_rx TIMEOUT at its 1800 s guard** | maap__3 490, crf_rx >1801 (killed), media_grid_align 399 |
| 11 | head, no ccache | 1958 | 1803 | 3/3 PASS, 18068 checks | maap__3 384, crf_rx 932, media_grid_align 356 |
| 11 | head, ccache | 1788 | 1294 | 3/3 PASS, 18068 checks | maap__3 218, crf_rx 897, media_grid_align 364 |
| 9 (18.2 min) | base | 2255 | 2279 | 2/2 PASS, 487 checks | maap__2 397, aaf_clock_meter 1610 |
| 9 | head, ccache | 1274 | 990 | 2/2 PASS, 487 checks | maap__2 184, aaf_clock_meter 802 |
| 7 (23.1 min) | base | >2586 | | **exit 92: mmcm_servo TIMEOUT at its 1800 s guard** | pp_shadow__0 785, mmcm_servo >1801 (killed) |
| 7 | head, no ccache | 2135 | 1803 | 2/2 PASS, 1058 checks | pp_shadow__0 602, mmcm_servo 1308 |

Identity through the runner: maap__3 (base vs both heads), media_grid_align, maap__2, aaf_clock_meter and
pp_shadow__0 logs IDENTICAL; the maap__3 and maap__2 case receipts IDENTICAL with timing/identity keys removed; the head's crf_rx
log through the runner IDENTICAL to the base's direct `make -C tb/verilator/crf_rx` log, and the head's mmcm_servo
log likewise to the base's direct mmcm_servo log (the base runner killed both at their guard on this host, so that
is the comparison available). On this loaded host the base shards 7 and 11 each lost a suite to the 1800 s guard,
the local image of the hosted near-timeouts; the head shards finished every suite.

ccache within one cold job, the hosted case once ccache is installed: avtp_rxmon (eight builds, five mutant
drivers, 95 % cc1plus) CPU 1588 -> 548 s (-65 %), wall 968 -> 783 s, 72 % hits, log IDENTICAL (3201 lines).

## 5. Findings for their own Issues

### 5.1 Verilator initialises the net connected to a defaulted input port with the default (silent, -Wall clean)

Pinned 5.050 and system 5.054 both. For an ANSI input port with a default value (`input wire [7:0] x = '0`),
whenever the port is not public Verilator emits the default as an `eval_static` assignment to the CONNECTED net
(`vlSelfRef.pcm_chans_i = 0U;` in the generated `__Slow.cpp`). A net the design re-drives recovers at the first
settle; a top-level input the harness set before its first `eval()` is overwritten and stays at the default.
`--public-flat-rw` (or making that one port public) prevents it. Removing the default value prevents it.

Minimal repro (receipts/bisect/portdef/internal.sv, tb3.cpp, tb4.cpp): `pcm_chans_i = 0x86` set before the first
eval, three instances wired straight to it, through `~`, and through a flop:

| build | prints | expected |
|---|---|---|
| plain | `port 0 net 255 reg 0` | `port 134 net 121 reg 134` |
| --public-flat-rw | `port 134 net 121 reg 134` | same |
| plain, input set after the first eval (tb4.cpp) | `port 134 net 121 reg 134` | same |

How it surfaced: follow_ring with probes.vlt fails 43 of 97 checks (pullin case: render_slips_o 1 -> 7234, the stream
off its presentation law). Bisect by module (only all of KL_chan_map_capture or all of follow_ring_wrap public
restores byte-identical output), then by variable (209 plain names in 8 groups, then 3s, then 1): `lb_wire_chans_i`
alone restores it. follow_ring_wrap.sv:340 ties it to the top input `pcm_chans_i`; with the bug the per-stream channel
count reads 0, which KL_chan_map_capture maps to 2 channels.

The tree has 11 defaulted input ports: KL_chan_map_capture.sv (8: tdm_close_ns_i, lb_tdata_i, lb_tvalid_i,
lb_tlast_i, lb_tuser_i, lb_wire_chans_i, lb_flush_i, lb_recentre_i), KL_crf_tx.sv transit_c_i, KL_aaf_packetizer.sv
stream_id_i, protocol_processor_top.sv rx_if_index_i. Exposure is any build without --public-flat-rw where one is
tied to a top-level input (or another net nothing re-drives). milan_datapath ties its KL_chan_map_capture ports to
internal nets, so its suites are probably unaffected, but nobody has checked every wrapper; that census, and the
decision (drop the defaults, or forbid tying them to top inputs, or a Verilator upstream report), belong in an Issue.
Until then the rule in TESTING.md keeps probes.vlt out of any suite whose model has a defaulted input.

### 5.2 firmware-boundary runs its builders serially

25.8 min hosted, 93 % of it the builders' own compiles at ~2.3 of 4 cores. ctrl_boundary already accepts several
`--capture DIR`; a job split (builders' captures in parallel jobs, the judging job taking all captures) is the
structural lever. It belongs to the gate's owners because the capture is what the gate proves.

### 5.3 The CI tool inventory is red at the base head

`python3 scripts/ci_tool_inventory.py --check` (with the pinned shfmt) refuses at 300da99b: 13+ declared scripts
whose sha256 no longer matches (first sw/builder/endstation_builder.py; run_all_suites.sh too, stale since
2026-11-08), then an uncensused `exec` in endstation_builder.py and an unclassified `git ls-files` in
sw/builder/test_builder.py. No PR workflow runs it, so it has been rotting silently. This round updates the command
table's Verilator patterns for the four Makefiles it changes and leaves the stale hashes to that Issue; the check
can neither pass nor fail on this change until the inventory is repaired.

### 5.4 Per-eval runtime overhead

With the model trimmed, ~28 % of talker_step's cycles are the pinned runtime's per-`eval()` bookkeeping
(`VlDeleter::deleteAll`'s mutex, `Verilated::endOfEval`'s queue flush). Only fewer `eval()` calls per simulated
edge in the harnesses would reduce it; that is a harness change with its own proof burden.
