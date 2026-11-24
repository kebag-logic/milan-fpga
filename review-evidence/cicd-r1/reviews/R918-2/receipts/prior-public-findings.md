Source: https://github.com/kebag-logic/milan-fpga/pull/1001#issuecomment-7131916838


**F1 - MINOR - lenses: Docs - PR body "Description" table, row 3 ("L1d misses -7..-9 %"); packet
`author/REPORT.md` 3.1 and 4 (row 3) - the -O3 lever's L1d-miss figure does not match its receipts.**
Authority/evidence: the packet's `receipts/budget/{base,base-2,base-3,tbO3,tbO3-2,tbO3-3}.perf`, field
`L1-dcache-load-misses`: 3.947 / 3.742 / 3.654 G -> 3.374 / 3.411 / 3.457 G. Paired, that is -14.5 / -8.8 / -5.4 %,
and the mean is -9.7 %. No pairing or range of these files gives -7..-9 %. The brief's item 6 and the AGENTS.md
section 6 Docs lens require a cold reviewer to be able to reproduce the PR's figures from its evidence. Owner rule:
a defect that changes a figure is not RESIDUE.
Impact: a stated measurement understates the spread its own data shows. No verdict or code is affected.
Required outcome: the PR body and the packet REPORT state the figures the receipts give (for example "L1d misses
-5..-15 % paired, -10 % mean"), or the packet publishes the receipts that give -7..-9 %.
Verification: `python3 -I scripts/packet_figures.py <packet>/author/receipts` and compare with the corrected text.

**R1 - RESIDUE - lenses: Docs - wording only; no figure, code or verdict changes.** Exact fixes:

- **a.** This delta makes stale two comments in `tb/verilator/crf_rx/sim_main.cpp`: line 1382 "(--public-flat-rw
  keeps every signal writable)" and lines 1392-1393 "the rootp name --public-flat-rw exposes". Change them to
  "(probes.vlt makes these flops writable)" and "the rootp name probes.vlt exposes". In
  `tb/verilator/mmcm_servo/sim_phc_step.cpp:37`, change "read through --public-flat-rw" to "read through
  probes.vlt".
- **b.** `tb/verilator/maap/probes.vlt:3-4` says "(in place of --public-flat-rw, see the Makefile)", but
  `tb/verilator/maap/Makefile` has no probes.vlt comment. Either drop "see the Makefile", or add the one-line
  reason the other three Makefiles give.
- **c.** `tb/verilator/aaf_clock_meter/probes.vlt:4` says "sim_main.cpp and sim_servo.cpp read them", but only the
  servo build (`SERVO_FLAGS`) loads this file. sim_main.cpp's `g5_v_r` is public through
  `KL_aaf_clock_meter.sv:345`. Change it to "sim_servo.cpp reads them; g5_v_r is also public through its RTL
  metacomment, which the meter build (sim_main.cpp) relies on".
- **d.** `docs/testing/TESTING.md:171` "lists exactly those in its suite's `probes.vlt`" reads as the only
  mechanism, but the tree also uses `observe.vlt`, `ptoff_public.vlt`, `*_probes.vlt` and RTL metacomments.
  Change it to "makes public exactly those, in a `.vlt` such as the suite's `probes.vlt`".
- **e.** The comment rule asks for reasons with issue IDs. The new TESTING.md hazard text (lines 174-177) and the
  new comments in the four Makefiles, the four probes.vlt files, `run_all_suites.sh:125-130` and `build.py:778-779`
  cite neither #998 nor #996. Add "(#996)" to the hazard sentences and "(#998)" to the speed-up comments.
- **f.** The PR body says the hazard "needs its own Issue", but #996 is filed, as the PR's first line says. Its
  "a minimal reproduction and the bisect are in the evidence comment" points at a comment that does not exist. The
  reproduction is in `review-evidence/cicd-r1/author/receipts/bisect/` and in #996. Replace the sentence with that
  path.

**S1 - SUGGESTION - Tests, Robustness.** Add a static probe-list check like `scripts/probe_check.py`, as a
suite-local self-check or as a sweep preflight that compares the harness's `__DOT__` names with the generated
scope table. Control P3 shows that a dropped read probe compiles and passes silently.

**S2 - SUGGESTION - Docs.** Packet `receipts/ccache/{nocc,cold}.time` hold 1587.52 / 547.52 user s, which are
avtp_rxmon's figures (packet REPORT 4.1), while `warm.time` holds crf_rx's 229.32. So the crf_rx 498 -> 262 s
headline has no time receipt in the packet. The headline is true (2.4 reproduces -47.0 %). Publish the crf_rx
files under distinct names.

**S3 - SUGGESTION - Robustness, Docs.** With ccache installed and an unwritable cache directory, every compile
fails (`ccache: error: Failed to create directory ...`, rc 1). The sweep would then fail closed on a host that
passed before. Record the opt-out (`OBJCACHE=`) and the writable-`CCACHE_DIR` requirement in TESTING.md and in the
runner's `Environment:` header (`run_all_suites.sh:37-46`), which does not list `OBJCACHE`.

**S4 - SUGGESTION (a new Issue for the manager, not a finding against this head).** The packet's
`ab/pub.follow_ring.verdict` says follow_ring's make exited 0 while its log tallied 43 failures ("VERDICT
CONTRADICTED"). That is a masked exit code in a suite this PR does not touch. The sweep's tally catches it.

