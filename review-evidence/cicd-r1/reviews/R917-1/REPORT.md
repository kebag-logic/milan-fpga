[R917] NEGATIVE - exact head fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f

# R917-1: internal cleared-context review of PR #1001 (Relates to #998)

Head `fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f`, tree `6aa4a42135fc7615a344aba1935eac8133bdf54b`.
Delta reviewed: `300da99beed5bb1c77e4b04af0bb4f9369856e0d..fcbc31f3` (three commits, 12 files: four
`probes.vlt`, four suite Makefiles, `ci/image/command-table.json`, `docs/testing/TESTING.md`,
`scripts/run_all_suites.sh`, `tb/verilator/ctrl_service_budget/build.py`).

**Verdict: NEGATIVE, on one open MINOR (F1, Docs): a figure the PR body states for the -O3 lever does not match
the packet's own receipts.** Everything the brief named as the central risk came out clean in my independent
checks. Each of the four suites has a complete probe list, with write access exactly where the harness writes. None
of the four models contains a defaulted input port. Every suite log at the head matches the base after
normalisation. Planted mutants are caught by the same check names. ccache cannot change a verdict. F1 is a
text-only fix to one figure, and the code needs no change.

## 1. What was reconstructed (public state only)

- AGENTS.md, CONTRIBUTING.md (one-line commits with no trailers, PR template, self-test evidence in a PR comment)
  and docs/testing/TESTING.md section 1 (the sweep).
- #998 body. Scope: measured speed-ups that leave every verdict identical. Out of scope: RTL, firmware, owner bounds,
  test expectations and graded figures. AC1 requires CPU/wall evidence and byte-identical suite output against the
  base for every adopted change. AC2 requires every hosted job to stay within 30 min with margin.
  The Issue has no comments, so it records no further scope decision.
- #996 (the defaulted-port hazard), #999 and #1000, all filed by the lane and all open.
- The PR body. The evidence packet `review-evidence/cicd-r1` at `9b89b4b5`: author REPORT.md, REVIEW-READY.md and
  receipts/. I downloaded the packet blob by blob into disposable scratch and used it as data only.
- The PR has no review, no review comment and no evidence comment. Its only comments are the two review-start
  notices, so this round has **no prior public finding to resolve or retain**. The manager has posted no evidence
  comment on the Issue or the PR yet.
- Toolchain (`receipts/toolchain.txt`): pinned Verilator 5.050, wrapper sha256 `905795b9...`, `verilator_bin`
  `44898b22...`, `verilated.mk` `698f5874...`. Also g++ 16.2.1, GNU make 4.4.1 and ccache 4.14.1.

## 2. Independent checks (the brief's items 1-6)

All runs used my own scripts (`scripts/`). The trees were disposable copies of the base and head. Each run had 2
pinned CPUs and the hosted job budgets: `VERILATOR_JOBS=SIM_JOBS=2`,
`MAKEFLAGS=-j1 --no-print-directory`, and Verilator's `-j 0` rewritten to `-j 2` by `scripts/vwrap.sh`, which
changes no other argument. Host load was 110-160 throughout, so wall times are for orientation only.

### 2.1 Probe-list completeness and read/write privilege: CLEAN

`scripts/probe_check.py OBJDIR harness.cpp` extracts every `__DOT__` identifier from the harness sources,
including the alias `root->` and the static `::` parameter members. It classifies each one as written or read and
looks it up in the generated scope table (`varInsert ... VLVF_PUB_RD|VLVF_PUB_RW`) of the model that was actually
built. A written name must be `PUB_RW`. I ran it over all nine builds of the four suites at the head and at the
base (`receipts/probe_check.txt`). It found **0 uncovered names**:

| Build (head) | Names | Written (must be RW) | Result |
|---|---:|---|---|
| crf_rx `obj_dir` (sim_main.cpp) | 3 | `pdu_count_o`, `fmt_err_o`: RW | ok |
| crf_rx `obj_talker` (sim_talker_step.cpp) | 6 | none | ok (incl. the wire `tick_p_w`) |
| crf_rx `obj_discontinuity` | 0 | | ok |
| mmcm_servo `obj_phc` (sim_phc_step.cpp) | 9 | none | ok (incl. `u_tick_cdc__DOT__sync`, matched through `-module "cdc_pulse"`) |
| aaf_clock_meter `obj_servo` (sim_servo.cpp) | 4 | none | ok (matched through the parameter clone `KL_mmcm_drp_servo__pi1`) |
| aaf_clock_meter `obj_dir` (sim_main.cpp) | 1 | none | ok: `g5_v_r` is public through the RTL metacomment at `hdl/ieee1722/crf/KL_aaf_clock_meter.sv:345`, not through probes.vlt (see R1c) |
| maap `obj_dir` (sim_main.cpp) | 4 | `lfsr_r`: RW | ok (`PROBE_MIN_MS_C`, `POOL_SIZE_C` static members present) |

No token pasting (`##`) and no VPI or scope lookups appear in the harness sources or in their shared headers
(`tb/common/verilator_harness.hpp`, `mmcm_servo/mmcm_model.h`). No mutant driver adds internal names to its
harness replicas. Each driver builds through the suite's own Makefile with `make -C <suite>`, so the relative
`probes.vlt` resolves. A build that cannot find it fails, and every driver states that a compiler error never
counts as a kill.

**Control (P3).** I weakened a copy of the head crf_rx list: `tout_r` dropped, and both RW entries downgraded to
`public_flat_rd` (`receipts/probes/p3.probes.diff`). The copy still compiles. `probe_check.py` flags all three
names (`receipts/probes/p3.probe_check.txt`). The harness fails 63 checks, `[G1-a0..b3]` among them, because the
preload writes are lost. It does **not** notice the missing `tout_r` read: `[UNB-d1]` still passes
(`receipts/probes/p3.run.log`). This confirms the central risk the brief named: a list can compile and still be
incomplete. Today's lists are known to be complete because of a static check like this one; a test run would not
show it (S1).

### 2.2 Defaulted-input-port hazard (#996): CLEAN for all four suites

- **Reproduced.** The author's minimal case under the pinned tool prints `port 0 net 255 reg 0` in the plain build
  and `port 134 net 121 reg 134` under `--public-flat-rw`. The plain build's generated
  `Vtop___024root__0__Slow.cpp:18` contains `vlSelfRef.pcm_chans_i = 0U;` (`receipts/portdef_repro.txt`).
- **Census.** `scripts/portdef_census.py` runs Verilator's `--json-only` on each model exactly as the Makefile
  elaborates it, then reports every INPUT that carries an initialiser (`receipts/portdef_census.txt`). Results:
  crf_rx unit, crf_rx talker (5 modules), mmcm_servo phc (3), aaf servo (5) and maap all report **none**. Both
  controls fire: the repro's `sub.chans_i` and `KL_crf_tx.transit_c_i`. None of the 11 defaulted ports #996 lists
  sits in any of the four suites' models.
- **Mechanism.** `scripts/topinput_writes.py` flags any generated statement that assigns a top-level input. It
  fires on the repro's plain build and stays silent on the flat build. Over all nine builds of the four suites,
  at the base and at the head, it reports **none** (`receipts/topinput_writes.txt`).

### 2.3 Whole-suite log identity, base vs head: IDENTICAL for all four; planted mutants caught by the same names

`scripts/logcmp.py` removes only host text: the tree path, Verilator's three build-statistics lines, make's
directory chatter and temporary-directory suffixes. On each Verilator command echo, the base's `--public-flat-rw`
is rewritten to `probes.vlt`, so the rest of that command line is still compared byte for byte. Nothing else is
masked: no numbers and no times. Sanitised logs are in `receipts/logs/`; comparisons are in `receipts/identity/`.

| Suite (`make -C tb/verilator/<suite>`, default target incl. mutants) | Base rc / head rc | Compared lines | Result | CPU s user+sys, base -> head (orientation only) |
|---|---|---:|---|---|
| crf_rx (incl. the 23-mutant campaign) | 0 / 0 | 2633 | IDENTICAL | 1536.9 -> 1023.3 (-33 %) |
| mmcm_servo (default `run`) | 0 / 0 | 427 | IDENTICAL | 1910.6 -> 1114.2 (-42 %) |
| aaf_clock_meter (38/38 mutants) | 0 / 0 | 138 | IDENTICAL | 1836.4 -> 1246.1 (-32 %) |
| maap (65 mutant checks, git-backed clones with submodules at their gitlinks) | 0 / 0 | 390 | IDENTICAL | 1901.9 -> 1826.8 (-4 %) |
| maap `make coverage` (95 % gate) | 0 / 0 | 278 | IDENTICAL, 100.0 % (225/225) both | |

My first maap pass ran in a copy without git metadata, and its integration mutants could not derive the
protocol-processor source list (`git ls-files`). That is a limit of my copy, not of the PR. I discarded that pass
and reran maap in local clones at both commits.

Reviewer-planted mutants were built through the suites' own targets with an RTL override, so no tracked file was
edited (`receipts/probes/`, diffs in `{base,head}.p{1,2}.rtl.diff`):

- **P1** (crf_rx `KL_crf_rx.sv:516`: `fmt_err_o` pegs at 255, the old 8-bit law). Caught at both commits by
  `[G1-b2]` and `[G1-b3]` plus the per-PDU replica checks, 15714 checks with 29 failures. The two run logs are
  **byte-identical**.
- **P2** (maap `KL_maap.sv:202`: the PROBE draw folds `lfsr_r` in place of `lfsr_next_w`). Caught at both commits
  by `M4 B.3.4 every seed pair 2^i apart draws different first probe intervals`. The two run logs are
  **byte-identical**.
- **mmcm_servo `make slew-mutants`.** This is the only mutant campaign that rebuilds the changed `phc_step_build`,
  and the sweep does not run it. At the head: `checks: 10 failures: 0`, every mutant with its named rejection
  (`receipts/slew_prefix.txt`). See the base note in Limits.

### 2.4 ccache cannot change a verdict: CLEAN

- Only verilated.mk reads `OBJCACHE`. It prefixes the compiler (`$(OBJCACHE) $(CXX) ...`, verilated.mk lines
  290-307, and the generated per-file testbench rule, e.g. `Vcrf_talker_wrap.mk:63`). `git grep` finds no other
  consumer in the tree. I tested the exact bytes of `scripts/run_all_suites.sh:131-133` in four cases
  (`receipts/objcache_logic.txt`). Unset with ccache on PATH gives `ccache`. Unset without ccache leaves it unset.
  `OBJCACHE=` stays empty. A preset value is kept.
- The workflows and `ci/image` contain no ccache. Hosted shards run on bare `ubuntu-24.04` (`rtl.yml`). The
  boundary gate (`sw/firmware/ctrl/test/ctrl_boundary.py`) and its compiler capture are untouched by the delta. It
  runs as its own rtl-fast job (`rtl-fast.yml:1220`, `:1357`) outside the sweep. Hosted `firmware-boundary` at
  this head: success.
- **Verdict identity.** I ran crf_rx's mutant campaign at the head without ccache (526.5 CPU s), then with
  `OBJCACHE=ccache` and a private cache directory, cold (279.2 s, **-47.0 %**, 64 % hits) and warm (262.7 s).
  All three logs are IDENTICAL, 23/23 (`receipts/ccache_crf_rx_mutants.txt`). This reproduces the -47 % in the
  commit message, the runner comment and the PR body.

### 2.5 Budget harness `OPT_FAST=-O3`: CLEAN on mechanism and receipts (not rerun, see Limits)

- `make -n -B` on a generated Verilator makefile shows the change does what the comment says. The testbench rule
  ends `... -O2 ... $(OPT_FAST)`, so the default `-Os` wins and the command-line `OPT_FAST=-O3` makes it `-O3`. The
  model rule puts `$(OPT_FAST)` first, so the suite's `-CFLAGS` level still wins. `build.py:765` already passes
  `-O3` in `-CFLAGS` and to Verilator, so the model's level is unchanged.
- The compile is ISO `-std=c++17` (no fp-contract) with no `-ffast-math` and no `-march`, so the optimisation level
  cannot change floating-point results.
- The packet's `budget/outputs.md5` gives the same md5 `f1630111...` for all 7 runs of the 2.8 MB output (-Os x3,
  -O2, -O3 x3), and `4a5c0c06...` for all 8 earlier runs.
- Paired CPU from `budget/*.perf`: -4.9 / -2.6 / -2.5 %, which matches "-2.5..-5 %" (`receipts/packet_figures.txt`).
  The L1d figure does not: see F1.

### 2.6 PR-body figures against the packet (`scripts/packet_figures.py`, `receipts/packet_figures.txt`)

The probes CPU figures match `ab/*.perf`: -37.4 / -25.9 / -26.6 / -9.8 %. So do talker_step instructions -49.1 %
and L1i misses -99.56 % (`talker/*.perf`), and 23.66 + 21.06 % ico in `talker/perf-report-flat.txt`. The shard
replicas match: 18068 + 487 checks (`shards/*/out`). The hosted estimates are consistent with the packet REPORT
section 4 arithmetic: crf_rx 17.2 x 0.52-0.63, and about 16 runner-min summed.

One exact-head hosted data point: Verilator shard 9/19 (maap__2 + aaf_clock_meter) completed in 14.1 min with 487
checks PASS (`receipts/hosted_shard9_excerpt.txt`). The PR estimates ~14.5 min. The remaining figures are F1 and
S2.

## 3. Findings

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

## 4. Per-lens results at fcbc31f3

```text
[R917] PASS Conformance - #998 AC1 vs receipts/identity/*.txt, receipts/ccache_crf_rx_mutants.txt, packet budget/outputs.md5; git diff 300da99b..fcbc31f3 --stat - every adopted lever is measured and its output identical against the base; the delta touches no RTL, firmware, bound, expectation or graded figure; AC2 is not claimed (Relates to #998; firmware-boundary and shard 1 untouched)
[R917] PASS RTL - receipts/portdef_census.txt, receipts/topinput_writes.txt, receipts/probe_check.txt (generated *__Syms__Slow.cpp of nine builds at both commits) - no defaulted input in any of the four models; no generated write to a top input; every probed variable public with the right privilege in the model actually built (incl. parameter clones); no RTL file in the delta
[R917] PASS Robustness - scripts/run_all_suites.sh:131-133 (receipts/objcache_logic.txt); mutants.py/slew_mutants.py build paths (make -C <suite>, compile error never a kill); receipts/probes/p3.*; receipts/identity/maap_coverage.txt - OBJCACHE unset/empty/preset/absent behave as documented; a missing probes.vlt fails loudly; a weakened RW entry is caught by [G1]; an unwritable ccache directory fails closed (S3)
[R917] PASS Tests - receipts/identity/{crf_rx_mmcm_servo,mmcm_servo,aaf_clock_meter,maap,maap_coverage}.txt; receipts/probes/{base,head}.p{1,2}.run.log; receipts/slew_prefix.txt - existing campaigns (crf_rx 23, aaf 38, maap 65, mmcm slew 10 at head) and two reviewer-planted mutants are caught by the same check names at base and head; no test or expectation changed
[R917] MINOR Docs - PR body Description row 3; packet author/REPORT.md 3.1 and 4 - L1d -7..-9 % does not match budget/*.perf (F1)
```

Docs, the clean part: TESTING.md lines 166-177 match the reproduced hazard and the runner's behaviour. The seven
command-table patterns (`/commands/verilator/patterns[42,43,48,49,90,113,125]`) mirror the changed Makefile
argument lists. The commits are one line with no trailers. The added lines contain no lane label, review round,
reviewer ID, issue-comment ID, private name or tool name. Docs stays UNCLEAN until F1 is fixed.

## 5. Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #998 body/AC; diff stat; identity, ccache and md5 receipts | R917-1 | fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f |
| RTL | CLEAN | port-default census; top-input write scan; scope tables of 9 builds x 2 commits | R917-1 | fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f |
| Robustness | CLEAN | run_all_suites.sh:121-133; mutant drivers; P3 control; maap coverage; ccache failure mode | R917-1 | fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f |
| Tests | CLEAN | 4 whole-suite base/head identities; P1, P2; slew-mutants at head; ccache mutant identity | R917-1 | fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f |
| Docs | UNCLEAN (F1 open) | TESTING.md 166-177; probes.vlt/Makefile/runner/build.py comments; PR body; packet REPORT and receipts; command-table | R917-1 | fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f |

F1 is fixed in the PR body and the packet REPORT, neither of which is a tracked file at this head. Docs can be
re-covered once the corrected text is published. A fix confined to that prose does not un-cover the other four
lenses. R1 goes to the residue checklist and does not hold any lens.

## 6. Real limits

- **I did not rerun the CPU budget harness.** It needs the product LiteX tree, the CPU netlist and the RV32 SDK.
  Item 2.5 rests on the mechanism check above and the packet's md5 receipts. I started the portable
  `run.py --self-test`, but it did not finish within my 580 s cap. It does not exercise the changed make argv, so
  I draw no conclusion from it.
- **The base mmcm_servo `make slew-mutants` did not finish within this round.** The head's campaign completed
  10/10. The base log's first 9 lines match the head's (`receipts/slew_prefix.txt`). This campaign is outside the
  default sweep.
- **I ran no shard replica (`run_all_suites.sh --ci-pieces --shard`).** My suite runs call the suite Makefiles
  directly. The runner's only change, the OBJCACHE lines, was tested in isolation on its exact bytes. The author's
  shard replicas ran on `32e8ed4f`, whose tree differs from the head's in one TESTING.md sentence.
- **My CPU ratios come from a host at load 110-160.** They are unpaired and serve as orientation only: maap came
  out at -4 % against the author's paired -10 %. The decision figures are the author's paired perf counters.
- **`ci_tool_inventory.py --check` cannot run here** because no pinned shfmt is available. It is red at the base
  (#1000). `ci/image/tool-inventory.json` records a command-table sha256 (`c9bd5d35...`) that matches neither the
  base (`c68792bb...`) nor the head (`5057457d...`).
- **The hosted run at this head was still in progress** (`receipts/hosted_checks_snapshot.txt`). I read only
  completed contexts: shard 9 and firmware-boundary passed. I made no hosted or act acceptance and claim no manager
  source bank.
- **Review clone integrity was verified after all probes** (`receipts/clone_integrity.txt`): HEAD and tree are
  exact, the index and worktree are clean with nothing ignored or untracked, the index entries (mode, blob, path)
  equal the HEAD tree, and all six submodule gitlinks are unchanged. Every probe ran in disposable copies under
  `scratch/`.

## 7. Pending manager duties

- Carry R1 (a-f) to the residue checklist.
- Route F1 to the author, then to a Docs re-cover round.
- Consider filing S4 as a new Issue.
- Post the evidence comment the PR template requires.
- Build and validate the current-dev merge candidate (live dev `e275d795`; source base `300da99b`) with the builder
  and native banks, and link the receipts.
- Accept the exact-head hosted contexts (`rtl-fast`, all 19 Verilator shards, Yosys) once they complete.
- Physical calibration was NOT RUN, and field skips are not hardware proof.
- The second (external) positive review is still required.

R917-1 FINISHED
