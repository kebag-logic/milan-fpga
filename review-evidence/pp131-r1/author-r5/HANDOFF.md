# [A435] Round 5 handoff: processor #131 / PR #132

Status: **all four round-5 items done in the assigned order; no STOP** (item 3 shows the arbiter
behaving exactly as its banner permits).

Head `9dce84ea60857de74457f74b5bf08d89bd3ba408` on branch `131-d3-core-scalars` (round-4
head `84572585`, base `c951a9ff`). One commit this round; not pushed; the PR is not edited
(PR-BODY.md carries a Round 5 section and the corrected consolidated list).

Assignment: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/131#issuecomment-5883464746 ·
TAKEN https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/131#issuecomment-5883469814 ·
REVIEW READY https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/131#issuecomment-5884424686 ·
reviews R390-4 (PR #132, 5883190182) and R391-4 (5883463400) · bank note 5880274287 ·
parent #70 scope record 5880276193.

## Commits (one-line subjects, assigned order)

| Item | Commit | Subject |
|---|---|---|
| 1 R390-4 F1 | (PR body and `parent_edits.py`) | the nightly `ax1x1gptp` harness in the `PP_CTRL[1]` obligation |
| 2 R391-4 F1 | (PR body and `parent_edits.py`) | the timed leg keeps its `[AECP-WTMO]` arm; the retired degrade arm named |
| 3 R390-4 S1 = R391-4 S1 | `9dce84e` | Grade the arbiter's own contract where neither manager reaches it: a WRITE presented with an abort completes undrained, an abort drains only its own manager's READ, and after a WRITE an issue-cycle abort still drains |
| 4 R390-4 S2 | (PR body and `parent_edits.py`) | the image-less legs name CLOSED; `wr_chg_o` on a named no-connect |

`8457258..9dce84e`: 6 files, +216 / -23, no file under `hdl/` or `syn/` (`git diff 8457258
9dce84e -- hdl syn` is empty). Line numbers below are at `9dce84e`; parent line numbers are
at dev `eaa88a32`.

## Items: change and proof

**1. The nightly gPTP harness (R390-4 F1).**
- The finding holds: `tb/verilator/milan_dp/sim_ax1x1gptp.cpp` (target `ax1x1gptp`, run by
  `milan_dp_gptp/Makefile:9`, the nightly physical job) serves `obj_ax1x1gptp/aemi.bin` from
  reset (`:918`, `:353-375`), grades GET_AVB_INFO and GET_AS_PATH (`:771-787`, `:935-938`) and
  never writes `PP_CTRL` (`0x920`).
- The edit (`parent_edits.py:113-133`): the top of `Harness::configure()` (`:671`), which
  follows every `reset()` (`run()` `:922` and the mid-run reset `:984`), writes `PP_CTRL[1]`, polls
  `PP_STAT[2]` for up to 400 x 64 clocks and checks `[BOOT] PP_STAT[2] the restore walk
  sequenced`, before any other CSR write and before the first AECP command (the
  pre-acquisition GET_AVB_INFO). The image is served from reset, so the walk starts after it.
- Measured in a scratch parent at dev `eaa88a32`, every declared edit applied,
  `make -C tb/verilator/milan_dp ax1x1gptp`: rc 0, **139 checks, 0 failures** (the harness's 137 plus the two boots'
  walk checks), 16.992510280 s simulated (849,625,514 clocks at 50 MHz), 3,246.9 s wall for
  the build and run on a heavily loaded host (`receipts/ax1x1gptp-84572585.txt`).
- Control, the same parent without this one edit: `make` rc 2, 137 checks, **15 failures**: every GET_AVB_INFO
  check (the pre-acquisition three and the acquired five) and all seven GET_AS_PATH checks,
  each unanswered (length 0); every other check passes, so nothing else rests on the walk.
- At the final head (`9dce84e`, a fresh scratch parent): rc 0, 139 checks, 0 failures, the same simulated duration,
  3,277.1 s wall (`gates-gptp` in GATES.md); then `milan_dp_gptp`'s own step, `python3 verify_abort.py`,
  rc 0 on that binary: setup abort 6/6, no-TX accounting 20/20, no-Pdelay accounting 14/14
  (`receipts/milan_dp_gptp-9dce84e.txt`), so the whole nightly suite passes with the edit.

**2. The wedged-memory arm in the timed leg (R391-4 F1).**
- The declared `sim_nxn.cpp` edit (`parent_edits.py:229-298`) no longer calls
  `prove_a_wedged_response_memory_reports_and_heals()` from `run()` after the image arm
  (round 4's placement, after `if (prove_the_shipped_descriptor_image_enumerates()) return`,
  which the timed leg never reaches). It calls it inside
  `prove_the_shipped_descriptor_image_enumerates()` right after
  `grade_the_first_descriptors_on_the_wire()` (parent `:2465`), that is after the restore
  (started in `grade_the_image_header_and_the_side_port()`, parent `:2505`) and before the
  `#ifdef NOTIFY_TIMED_TB` return, in every leg.
- `notify` (the shipping 1x1 shape): 378 of 378, the six `[AECP-WTMO]` checks printed and
  passing, the heal answering SUCCESS (`receipts/r391-4-parent-notify-9dce84e.txt`, from
  R391-4's own `parent_scratch.sh` with this packet's `parent_edits.py`). R391-4 measured 381
  at base `c951a9ff`, unedited: 378 + 5 retired degrade checks - 2 hold checks. `nxn`: 1,841 of
  1,841 (R391-4: 1,844 at base), nxndv 1,843, nxn8 3,521, nxn4c 1,841,
  each with its six `[AECP-WTMO]` checks passing (30 in the `milan_dp` log: five legs x six).
- The PR body now states that the `[AECP]` no-descriptor-memory degrade arm (5 checks) is
  retired in every `sim_nxn` leg, and why: with no image AECP is held from reset (contract
  section 8.1, steps 1, 6 and 9) and CLOSED keeps holding it; the two hold checks replace it.

**3. The arbiter's own contract (R390-4 S1 = R391-4 S1), `9dce84e`.** No RTL change.
- Harness (`tb/acmp_nvm/sim_main.cpp`): manager 1 gains a WRITE (`:311-324`: the framed
  bytes it streams once granted, a byte per accepted cycle, `:754`), an abort held from its
  strobe to its op's end (`m1_abort_hold`), and an abort presented alone in every cycle the
  binding walk's READ strobe is out (`m1_abort_on_m0`, `:642-651`); the monitor records the
  grant's intent (`:751`) and counts the walk's READ issues with and without manager 1's
  abort (`:759-762`). `m1_op` (`:2575`) presents one op. Wrap taps
  (`tb/acmp_nvm/acmp_nvm_wrap.sv:86-89`, `:541-544`): the arbiter's issue and intent
  (`arb_req_o`, `arb_we_o`), the binding manager's registered strobe and intent
  (`mgr_req_o`, `mgr_we_o`). Test bench only.
- `check_n11_the_arbiters_own_contract()` (`:2597`), three arms, each on its own reset:
  - **N11a** (`:2602`) a manager-1 WRITE presented with its abort, the abort held to the
    write's end: issued as a commit, never drained, every one of the record's 28 bytes taken,
    done (not err), one ERASE and one WRITE of region 0x33, the record byte-exact in the
    device, the device idle.
  - **N11b** (`:2621`) manager 1's abort, alone, in the issue cycle of each of the walk's
    READs: 8 of 8 READs issued with it, none drained, no leak, no binding-manager abort, the
    walk completes as saved (`l_walk_ok`), nothing written.
  - **N11c** (`:2639`) after a completed manager-1 WRITE (the arbiter's `we_r` then 1), a
    manager-1 READ abandoned in its issue cycle: drained from issue + 1, bytes moved in the
    drain, nothing reaching manager 1, the device idle; then manager 1's next READ completes.
- STOP check: the head's arbiter passes all three (`tb/acmp_nvm` 359 of 359), exactly as its
  banner (`KL_pp_nvm_mgr_arb.sv:38-65`) states: only reads are abandoned, an abort presented
  while a WRITE is owned is ignored, and the issue-cycle arm takes the strobe's own manager,
  its own abort and its own `we`. **No STOP.**
- Mutants (`tb/pp_top/d3_mutants.py:365-398`, the head's arm text in `ARMS` `:74`), all
  `ACMP_NVM`, all KILLED from the tree (see Negative controls). README rows
  (`tb/acmp_nvm/README.md:343-347`), the N11 description (`:213-226`), 359 checks (`:8`); 09
  section 8.2 row (`docs/architecture/09_verification.md:192`) and 81 controls (`:200-201`);
  `tb/pp_top/README.md:664-669`.

**4. The scratch-parent refinements (R390-4 S2).**
- (a) The image-less legs (`parent_edits.py:190-228`): the wait still ends on either
  terminal, and the check now names the terminal the legs reach: `PP_STAT the restore walk
  ended CLOSED (no AEM image: busy 0, done 0, fail 1)` (`sim_main.cpp`: main, nolpf, ax1x1)
  and `[RENDER-BIND] PP_STAT the restore walk ended CLOSED (...)` (`sim_aclk.cpp`: aclk).
  Measured: `ax1x1` 231/231, `aclk` 190/190 (focused runs at `84572585`); the full `milan_dp`
  sweep at the head: main 234, nolpf 234, ax1x1 231 and aclk 190, 0 failures, each printing its
  CLOSED check.
- (b) = item 2.
- (c) `cosim_top.sv` (`parent_edits.py:50-75`): `.wr_chg_o (wr_chg_nc_w)` with
  `logic wr_chg_nc_w;`, the file's convention for the store's 23 other unused outputs, each of
  which lint reports as UNUSEDSIGNAL. A new output costs one warning either way: base
  (`c951a9ff` gitlink) 84 warnings (1 SYNCASYNCNET, 54 UNUSEDPARAM, 29 UNUSEDSIGNAL); with
  the edits 85 (30 UNUSEDSIGNAL), 0 PINMISSING, 0 PINCONNECTEMPTY, rc 0.

## Section 15.2 table and sweep

All 37 rows remain applied. [TABLE-15.2.md](TABLE-15.2.md) adds a round-5 column: 3 rows
updated (9: 09 section 8.2; 28: the `acmp_nvm` README and wrap; 29: the `pp_top` README), 34
unchanged. Named sweep at the head (the round-1 `sweep_reconcile.py`, unchanged): **704
matching lines, 357 rewritten or added by this lane, 347 with a location-specific scope
reason, 0 unreviewed** ([SWEEP.md](SWEEP.md), 133 KB). The one new match is N11b's
`restore_fail_o` line (`tb/acmp_nvm/sim_main.cpp:2630`); the README's `359 checks` line was
already this lane's, and the other changes only move line numbers.

## Negative controls

[MUTANTS.md](MUTANTS.md) lists all 81 controls from the full campaign at the head, with
suite, named assertions, failing-check count, first failing message and the README equality.
The round-5 additions and the one re-measured count:

| Control | Defect planted (`KL_pp_nvm_mgr_arb.sv:157-160`) | Named assertion(s) that fail | Failing checks |
|---|---|---|---:|
| `issue_arm_cross_intent` (R390-4, R391-4) | the issue-cycle term takes either manager's abort | `N11b manager 1's abort in the issue cycle of each of the walk's READs` | 1 |
| `issue_arm_ignores_we` (R390-4) | the issue-cycle term drops `!mX_we_i`, so a WRITE strobe with an abort arms the drain | `N11a a manager-1 WRITE presented with its abort` | 1 |
| `issue_arm_write_too` (R391-4) | the same defect, in R391-4's own text | `N11a a manager-1 WRITE presented with its abort` | 1 |
| `issue_arm_stale_we` (R391-4) | the issue cycle judged by the previous operation's `we_r` | `N11a a manager-1 WRITE presented with its abort` (after reset `we_r` is 0, so the WRITE is drained), `N11c a manager-1 READ abandoned in its issue cycle after a WRITE` (after the WRITE `we_r` is 1, so the READ's abort is lost and the port waits for ever) | 3 |
| `owned_arm_write_too` (this lane) | the owned term drops `!we_r`, so an abort while a WRITE is owned cuts it | `N11a a manager-1 WRITE presented with its abort` | 1 |
| `drain_misses_issue_cycle_m1` (round 4, re-measured) | the round-3 arbiter: no issue-cycle arm | `N10 a manager-1 READ abandoned in its issue cycle` (and now N11c too) | 4 (was 2) |

How each is killed, from the failing messages at the head
([receipts/d3_mutants-results-9dce84e.json](receipts/d3_mutants-results-9dce84e.json)):
a drained WRITE never reaches manager 1's `wready`, so the port collects eight copies of the
first byte, refuses the header as UNFRAMED before any device traffic, and the drain swallows
the err: manager 1 takes 0 (or 1) of 28 bytes and never sees an end. A cross-intent drain takes
the walk's first header READ from the binding manager, which then fails the walk on its
per-wait deadline.

The reviewers' own scripts at `9dce84e` (receipts):
- R390-4 `r390_4_mutants.py` (HEAD set to `9dce84e` in a scratch copy), its four issue-cycle
  edits (`r390-4-issue-mutants-9dce84e.txt`): `issue_arm_cross_intent` and
  `issue_arm_ignores_we` pass the D3 section, as that reviewer found, and are now KILLED by
  `tb/acmp_nvm` (N11b; N11a) and by the reviewer's unit probe; `issue_arm_one_clock_late` is
  KILLED by D3R18, N10, N11c and the unit probe; `issue_arm_m1_dropped` passes the D3 section,
  as that reviewer found, and is KILLED by N10 and N11c and the unit probe.
- R390-4 arbiter unit probe (`r390-4-arb-unit-9dce84e.txt`): 9 of 9 at the head.
- R390-4 arbiter monitor over `tb/acmp_nvm` (`r390-4-arb-monitor-acmp_nvm-9dce84e.txt`): the
  inputs round 4 counted at 0 are now presented: a WRITE strobe with manager 1's abort 1,
  manager 0's READ strobe with manager 1's abort 8, an abort while a WRITE is owned 45 cycles,
  manager-1 issue-cycle READ aborts 2 (N10, N11c). The one input this bench cannot present is
  a manager-1 grant with manager 0's abort: the real binding manager raises its abort only
  while it owns or strobes its own READ, so the arbiter cannot grant manager 1 then (the
  reviewer's unit probe case F covers it).
- R391-4 `run_r391_4.sh ... acmp <mutant>` for its six issue-cycle edits
  (`r391-4-acmp-mutants-9dce84e.txt`): golden 359/359; `issue_arm_stale_we` 3 failing (N11a,
  N11c), `issue_arm_cross_intent` 1 (N11b), `issue_arm_write_too` 1 (N11a),
  `issue_arm_m0_only` 4 (N10, N11c), `issue_arm_one_clock_late` 2 (N10, N11c);
  `issue_arm_m1_only` passes this suite, as in round 4 (D3R18 in `tb/pp_top` kills it).
- R390-4 E1/E2 (`run_probe_r3.sh`, unchanged) and R391-4 D1 (`run_r391_4.sh ... d1`) at the
  head: identical line for line to each reviewer's own round-4 head receipt
  (`r390-4-probe-e1-e2-9dce84e.txt`, `r391-4-d1-9dce84e.txt`): E1 aligned drains and the
  later SET persists; D1's five arms +4, +545, +44, +4,105, +545.
- R391-4 `parent_scratch.sh ... dp notify` with this packet's `parent_edits.py`
  (`r391-4-parent-notify-9dce84e.txt`): 378 of 378, six `[AECP-WTMO]` checks.

## DR3a measurements (ratified values, enforced)

`./obj_dir/Vpp_top_sim --dr3a` at `9dce84e` (the `tb/pp_top` default build from the gate
clone): **byte-identical to round 4's receipt** (`cmp` against `dr3a-8457258.txt`), as it must
be with no file under `hdl/` changed ([receipts/dr3a-9dce84e.txt](receipts/dr3a-9dce84e.txt)).
Clocks are `clk_i` cycles from `restore_go_i`; the wrap's clock is nominally 1,000,001 Hz, so
RS_TMO = 20,001 and AGG = 1,000,001 clocks. At 50 MHz a cycle is 20 ns, at 100 MHz 10 ns.

| Path | Terminal | go to release | go to terminal (cycles) | 50 MHz | 100 MHz |
|---|---|---:|---:|---:|---:|
| erased device, DRAM 31 | COMPLETE | 122 | 1,286 | 25.7 µs | 12.9 µs |
| nine records, DRAM 31 | COMPLETE | 122 | 1,989 | 39.8 µs | 19.9 µs |
| erased device, DRAM 143 | COMPLETE | 122 | 1,734 | 34.7 µs | 17.3 µs |
| nine records, DRAM 143 | COMPLETE | 122 | 2,661 | 53.2 µs | 26.6 µs |
| pass 0 DEVICE error | DEFAULTS (2) | 122 | 813 | 16.3 µs | 8.1 µs |
| pass 1 rule fetch error, roll-back | DEFAULTS (6) | 122 | 1,554 | 31.1 µs | 15.5 µs |
| pass 1 fetch 16,000 late, roll-back on debt | DEFAULTS (6) | 122 | 17,539 | 350.8 µs | 175.4 µs |
| NVM silent from its first read | DEFAULTS (3) | 20,003 | 40,006 = 2 x RS_TMO + 4 | 2 x 20 ms | 2 x 20 ms |
| image refused (magic) | CLOSED (7) | 122 | 164 | 3.3 µs | 1.6 µs |
| descriptor memory silent | CLOSED (7) | 122 | 8,188 | 163.8 µs | 81.9 µs |
| every grant 200 inside the per-wait deadline | DEFAULTS (3) | 158,530 | 1,000,000 (= AGG) | 1,000 ms | 1,000 ms |
| every READ byte just inside the per-wait deadline | DEFAULTS (3) | 1,000,002 | 1,000,004 (AGG + 4) | 1,000 ms + 80 ns | 1,000 ms + 40 ns |

The paths the checks place against the bound are unchanged too (`tb/pp_top` 7,888 of 7,888,
D3 133 of 133, at this head), in clocks after the bound's own clock: D3R18 +4 (80 ns at
50 MHz, 40 ns at 100 MHz), D3R19 +546 and +272 (10.9 / 5.5 µs and 5.4 / 2.7 µs), D3R20 +1
(20 / 10 ns), D3R21 +5 (100 / 50 ns). Longest waits unchanged: healthy D3 405 / 853 cycles
(DRAM 31 / 143), binding 12; the DR2a producer share 50,028 bench cycles = the 500-tick window
+ 28. The integrator's bounded wait stays 1,000 ms plus two per-wait deadlines plus a few
clocks (1,060 ms a margin).

## DR4 scalar-stage contribution

No synthesized file changed (`git diff 8457258 9dce84e -- hdl syn` is empty). Measured
again anyway, in one session: Vivado 2026.1 out-of-context synthesis with the head's
`syn/ooc/protocol_processor_ooc.tcl` over `git archive` trees of base `c951a9ff` and head
`9dce84e`, the shipping 1x1 shape (`-tclargs <src> 1 1`), part `xc7a100tfgg484-2`
([receipts/dr4-ooc-1x1-9dce84e.txt](receipts/dr4-ooc-1x1-9dce84e.txt)).

| Shape | Base `c951a9f` LUT / FF / BRAM / DSP | Head `9dce84e` | Lane 1 (head - base) | Round-5 increment | Writer `u_d3` LUT / FF | Binding `u_nvm_shadow` LUT / FF |
|---|---|---|---|---|---|---|
| 1x1 (shipping) | 21,675 / 23,710 / 16.5 / 4 | 22,706 / 24,269 / 16.5 / 4 | **+1,031 LUT / +559 FF / 0 BRAM / 0 DSP** | 0 / 0 | 790 / 479 | 689 / 1,268 (base 638 / 1,221) |

The absolute totals equal round 4's for both trees. Against the ruled scalar-core ceiling for
lanes 1-2 (2,500 LUT / 1,400 FF / 0 BRAM / 0 DSP), lane 1 uses 1,031 / 559, leaving 1,469 /
841 for lane 2. Synthesis WNS at the 10 ns constraint: -5.970 ns (base), -5.165 ns (head),
synthesis estimates only. The 8x8 diagnostic was not re-run (round 4: +842 / +502; no source
changed since). Post-place and the 8x8 post-place obligation stay lane 2's (open, not
waived).

## Parent-visible changes (for the pin-adoption lane)

The corrected consolidated list is PR-BODY.md "Round 5". Round 5 changes on the parent side:
- **No processor port, parameter or behaviour change** (no RTL change).
- `ax1x1gptp` joins the `PP_CTRL[1]` harness obligation; it is outside the consumer set.
- The `sim_nxn.cpp` edit keeps the wedged-memory arm in every leg, the timed `notify` leg
  included; the retired `[AECP]` degrade arm (5 checks) and its two replacing hold checks are
  stated.
- The image-less legs' check names CLOSED; `wr_chg_o` sits on a named no-connect.
- `parent_edits.py` applies at dev `eaa88a32` (the round-4 edits applied unchanged there, as
  both reviewers found); it now edits 12 parent files (round 4: 11, plus
  `sim_ax1x1gptp.cpp`).

## Suites and gates

[GATES.md](GATES.md) has every command with rc, seconds, log size and SHA-256, run by
[gates.py](gates.py) with the pinned Verilator 5.050 wrapper (clean processor clone at
`9dce84e`; scratch parents at dev `eaa88a32` with this packet's `parent_edits.py`).

| Tree | Entry point | rc |
|---|---|---:|
| processor | `./scripts/run_suites.sh` (33 suites, 1,016,035 checks, 0 failing; `tb/pp_top` 7,888, `tb/acmp_nvm` 359) | 0 |
| processor | `./scripts/lint_hdl.sh` | 0 |
| processor | `make -j1 check` (lint, WaveDrom, links 968, matrices, params 26/26/26, stale) | 0 |
| processor | `python3 scripts/gen_matrix.py --check` | 0 |
| processor | `./syn/yosys/run.sh` | 0 |
| processor | `make -C tb/nvm_port figures` (PR #13 history fetched read-only first) | 0 |
| processor | `git diff --check c951a9ff HEAD` | 0 |
| processor | `python3 tb/pp_top/d3_mutants.py` (81 of 81 KILLED, goldens PASS, 81 README counts equal) | 0 |
| processor | `make -C tb/srp_top mutants` (64 checks, coverage 49/49) | 0 |
| parent | the manager's 16 commands (C++ and Python idiom, xvlog, RTL source lists, `pp_srcs`, builder tests, `pp_shadow`, port contracts, naming, evidence classifier, docs, `lint_rtl`, `nvm_cosim` lint and quick, `milan_dp`, `milan_dp_render`) | **16 of 16 rc 0** |
| parent | `make -C tb/verilator/milan_dp ax1x1gptp` (outside the consumer set) | 0 (139/139) |

`git status` of the lane is empty; the processor gate clone was clean after the gates.

## Notes for review

1. **One arbiter input stays ungraded in the tree, by construction.** N11 drives manager 1
   only, as the assignment scopes it; manager 0 is the real binding manager. That manager
   raises its abort only in `H_RS_STREAM`, while it owns or strobes its own READ, so the
   arbiter can never grant manager 1 in a cycle manager 0 presents an abort. A mutant that
   takes manager 0's abort in manager 1's issue term *only* would pass every in-tree suite.
   `issue_arm_cross_intent` edits both terms, and N11b kills it through manager 0's term.
   R390-4's unit probe case F grades the other half on the arbiter alone. The binding
   manager's own behaviour makes that input unreachable in the product.
2. **`owned_arm_write_too` goes beyond the four named mutants.** N11a holds the abort to the
   write's end, so it also grades the owned half of the banner rule ("an abort presented while
   a WRITE is owned is ignored"). No in-tree manager presented that input before N11 either;
   the control proves the check is real. `issue_arm_ignores_we` (R390-4) and
   `issue_arm_write_too` (R391-4) are the same defect in two texts; both are kept, as named.
3. **N11b presents manager 1's abort without a request.** It is presented in exactly the
   cycles the binding manager's registered READ strobe is out. The arbiter issues that READ
   in the same cycle (the banner's one rule), and the monitor counts it: 8 of the walk's 8 READ
   issues carried the abort.
4. **`ax1x1gptp` starts the walk in `configure()`, that is on both of its boots.** The
   harness resets the datapath mid-run. Only the first boot sends AECP, but the firmware
   starts the walk on every boot, so the edit does too. That adds two passing checks (137 to
   139). The measured wall time (about 3,230 s for the run) is inflated: the host's load
   average was 40 to 50 during it. The nightly budget is 5,400 s for the whole
   `milan_dp_gptp` suite.
5. **The untimed `sim_nxn` legs now run the `[AECP-WTMO]` arm earlier.** It moves from after
   the whole-model walk to before it, inside the image arm. The arm heals within itself (its
   last check is the heal), so the whole-model walk after it meets a healthy station:
   `nxn` 1,841 of 1,841 at the head, the same count as round 4's placement.
6. **The pp_top-based reviewer probes are identical because no RTL changed.** E1/E2 and D1 were
   rerun and match their round-4 receipts line for line. R391-4's 17,406-run P9 sweep was
   not rerun (RTL unchanged).
7. R390-4 S2(c) is taken as far as it can go: any termination of a new output costs one
   lint warning in `cosim_top.sv`'s `-Wall` lint. The named no-connect keeps the file's own
   convention.

## Packet

HANDOFF.md, PR-BODY.md (Round 5 section; the consolidated list moved there and corrected),
TABLE-15.2.md, SWEEP.md with `sweep_reconcile.py`, MUTANTS.md with `mutants_table.py`,
GATES.md with `gates.py`, `gates_table.py` and `run_logged.py`, `parent_edits.py` (the
declared parent edits, applied to scratch parents only) with `mk_parent.sh` (the scratch
parent recipe), and `receipts/`:
- `parent-edits.diff` (the 12-file diff the script makes at dev `eaa88a32`; it equals the
  applied text in the gate parent);
- `ax1x1gptp-84572585.txt` (with and without the edit) and `milan_dp_gptp-9dce84e.txt`;
- `d3_mutants-results-9dce84e.json` (the full campaign), `dr3a-9dce84e.txt`,
  `dr4-ooc-1x1-9dce84e.txt`;
- the reviewer reruns: `r390-4-issue-mutants-9dce84e.txt`, `r390-4-arb-unit-9dce84e.txt`,
  `r390-4-arb-monitor-acmp_nvm-9dce84e.txt`, `r390-4-probe-e1-e2-9dce84e.txt`,
  `r391-4-acmp-mutants-9dce84e.txt`, `r391-4-d1-9dce84e.txt`,
  `r391-4-parent-notify-9dce84e.txt`.

Logs, synthesis reports, scratch parents and clones stay under `$VALIDATION_STORAGE/a435` (not
copied; log sizes and hashes in GATES.md). No file in the packet exceeds 200 KB.
