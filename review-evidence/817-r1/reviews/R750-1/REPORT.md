[R750] POSITIVE - exact head 6cfb27dacafb2e5b693412db3342ca0fccc9c0bc

# R750-1: external review of PR #821 (#817), servo reset synchroniser cut

- Scope: whole PR, `dev` 1e80128f0a467b58bf884b7d9bf62e013a2fb141 .. head 6cfb27dacafb2e5b693412db3342ca0fccc9c0bc (tree 0fa85222108a0bc0f4b47fe01552bf44c5de757d), two commits: a7ff491a (the change) and 6cfb27da (docs plus one test docstring).
- Role: cleared-context external reviewer. The task was rebuilt from public state: AGENTS.md, CONTRIBUTING.md, docs/README.md, the #817 issue body, PR metadata (`gh pr view --json title,body,headRefOid,baseRefName,baseRefOid,files,commits`), the source at head and dev, and the author's public evidence packet (`review-evidence/817-r1` at 414795304a97868ff26cf2dcc5b547c99537fb51).
- Verdict and ledger were written before any PR or issue comment was read. Prior public findings are dealt with in the section "Prior public findings" at the end.
- Open findings: none at MINOR or above. Two SUGGESTIONs (S1, S2) and two observations for the manager (O1, O2).

## What the change is (as read from the source)

- `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:1292-1298`: `(* ASYNC_REG = "TRUE" *)` on `psrst_sync_r[1:0]`, the two-flop chain that samples `rst_n` (milan domain) into `ps_clk_i`. Stage 1 drives `psrst_n_w`, which is the synchronous reset of the PS runner (`:1327-1334`) and the destination reset of `u_batch_hs` (`:1302-1312`). No logic change.
- `sw/litex/clock_constraints.tcl:21-59`: `kl_servo_reset_sync_constraints <milan net>`. It resolves the milan clock through `kl_net_clock`, which refuses anything but one clock. It finds `*mmcm_servo/psrst_sync_r_reg*` and refuses a count other than two. It refuses either stage without a strict-true `ASYNC_REG`. It classifies the stages by structure (D driven by the other stage = stage 1) and refuses anything but one first and one second stage. It refuses a destination clock set that is not exactly one clock, or that is the milan clock. Then it emits exactly `set_false_path -from <milan clock> -to <stage0>/D`.
- `sw/litex/clock_constraints.py:31-48`: `_source_hooks` sources the Tcl once. `add_servo_reset_constraints` adds the hook with the milan PLL output resolved through the namespace.
- `sw/litex/milan_soc.py:279-281,3120-3123`: `_CRG.milan_pll_clk = pll.clkouts[-1].clk` is set beside `cd_milan`. The hook is installed where the audio-MMCM servo boundary is wired, unless `media_clock_servo` is pruned. `audio_mmcm_rst` exists only under `if milan_clk_freq:` (`:264`, `:397`), so `milan_pll_clk` exists wherever the hook is installed. The prune key matches `MCSERVO_P` (`:683`), which gates `g_mmcm_servo` (`hdl/milan/milan_datapath.sv:7321`).
- Tests: `sw/builder/test_clock_constraints.py:164-248` (stub netlist: the exact cut, both stage orders, and each refusal), `sw/builder/test_shipping_clock_constraints.py:98-111` (exactly one hook naming `clocks[1]`, the Tcl sourced once, `synth < source < hook < opt`).
- Docs: `docs/litex/CLOCK_DOMAINS.md:92,237,378-380`, `docs/integration/BUILDING.md:618-621`, `docs/testing/RUNNING_TESTS.md:190-191,197`.

## Focus checks

### (1) Exactly one endpoint, one source clock, no other exception change

- Routed exception list: dev 25, head 26. They differ by exactly one row: `[get_clocks -of_objects [get_nets milansoc_crg_clkout1]] | * | [get_pins {milan_datapath/g_mmcm_servo.mmcm_servo/psrst_sync_r_reg[0]/D}] | false | false` (`route-a7ff491a/exceptions-diff-vs-dev.txt`; row 26 of `route-a7ff491a/alinx_ax7101_exceptions.rpt:349`). Setup and hold are both cut, from one clock to one pin.
- Ignored-exception reports: 382 lines each. They are byte-identical apart from the date line and the output path in the command line (my diff of `post-route-dev/exceptions_ignored.rpt` against `post-route-head/exceptions_ignored.rpt`).
- The XDC is identical. The build Tcl gains exactly one line, `kl_servo_reset_sync_constraints milansoc_crg_clkout1` (`constraints-text/*.diff`). The generated Verilog differs only in its dates and in the order of module-tree comment lines.
- The other milan→PS endpoints, the 16 `u_batch_hs` endpoints, keep their 5.000 ns requirement and have no exception at head. Only `psrst_sync_r_reg[0]/D` moves to `False Path` (my diff of `post-route-{dev,head}/milan_ps_endpoints.tsv`, endpoint/requirement/exception columns).
- The route ran at a7ff491a. `git diff --stat a7ff491a 6cfb27da` touches only three docs and the docstring of `test_shipping_clock_constraints.py` (I verified the docstring-only diff). No build input differs, so that route is the head's route.
- Result: met.

### (2) The synchroniser, and the reset it carries

- Structure: at head both stages carry `ASYNC_REG=1` and share one slice: `SLICE_X3Y16` AFF and A5FF (`post-route-head/crossing.txt`). At dev they had no attribute (`SLICE_X0Y4`). I independently confirmed that the attribute is new at head and survives the repository's sv2v→Yosys lowering. `select -list KL_mmcm_drp_servo/a:ASYNC_REG` lists `psrst_sync_r` at head and not at dev (`receipts/yosys-asyncreg-{head,dev}.log`). The servo lints with 0 warnings at head and at dev (`receipts/lint-servo-*.log`).
- The reset is a level. The servo's `rst_n` is `axis_resetn = ~ResetSignal(milan_cd)` (`sw/litex/milan_soc.py:854`). That is the output of the milan domain's reset synchroniser (`FDPE_3`, the timing startpoint in `crossing.txt`): it asserts asynchronously and releases only on milan edges. So any assertion lasts at least about one 20 ns milan period, which is four 5 ns PS-clock periods. Route delay shifts the edges but does not shorten the level, so stage 0 samples it.
- Open risk 2, the unbounded route (11.368 ns max / 5.971 ns min in this route, 2.671 ns at dev). I judged it against the servo's own protocol:
  - **Release.** `cdc_handshake` carries requests as a toggle *level* (`hdl/common/cdc_handshake.sv:47-69`). A `req_tog` flip made while the destination is still in reset is still held when the destination's `req_sync` comes out of reset, so a late PS-side release cannot lose a batch. The source also sends nothing until a measurement window produces a command, and that takes milliseconds. Release skew is therefore harmless.
  - **Assertion.** The only order-sensitive case is a source `req_tog` cleared from 1 to 0 by reset while the destination is still running. That reads as one request edge carrying `data_hold = 0`, which would be one fine-phase step (`:1352-1363`).
    - After the cleared toggle is captured in `req_sync[0]` (PS edge E1), the step needs five more PS edges: `req_sync[1]`, `dest_req_r`, `pend_v_r`, `P_EN_S`, `ps_en_o`. So `ps_en_o` cannot rise before E6 = E1 + 25 ns. E1 is at the earliest about 3 ns after `rst_n` asserts, so the earliest absolute step is about 28 ns after `rst_n`.
    - The PS-side reset applies its synchronous clear at edge F3, two edges after stage 0 captures it at F1. That is at most 11.4 + 3×5 ≈ 26.4 ns after `rst_n` in this route.
    - Taking each side's worst phase independently leaves at least about 1.6 ns. Both events count the same PS edges, and the step is suppressed whenever F1 ≤ E4. That holds while the reset route stays under about 15 ns plus E1's offset, roughly 18 ns. So the edge-aligned margin is about 6.6 ns of further route growth.
    - The spurious step cannot occur in this route. If a placement ever lost the race, the effect is one ~1/56-VCO-period phase step during a reset, after which the servo re-acquires from IDLE. That is not a held fault.
  - **Conclusion.** `set_max_delay -datapath_only` is not required. The issue's Fix paragraph names `set_false_path` into the first flop with ASYNC_REG on both flops as an accepted alternative. A bound would turn the reset-ordering margin above into a checked property instead of a placement outcome; that is recorded as S2, optional.
- Result: met.

### (3) Refusals and hook presence are killed by planted mutants; one shipping hook

- My campaign (`scripts/tcl_mutants.py`, `receipts/tcl-mutants/`) planted 17 mutants in disposable copies of `clock_constraints.tcl` and ran the stub test (`scripts/servo_stub_driver.py`, `-I -B`, with an import-only LiteX stand-in) on each. The unmutated control passes, and so does the head itself (`receipts/stub-test-head.{log,rc}`, rc 0).
- **Killed (16 of 17):**
  - the cut: removed; widened (`-from` dropped); moved to stage 1; setup-only; aimed at the cell rather than the pin;
  - the stage-count check dropped;
  - the ASYNC_REG check: dropped; narrowed to the last-listed cell; loosened to "any non-empty value";
  - the chain check: dropped; first-only;
  - the clock check: dropped; distinct-only; count-only;
  - the source clock taken unchecked;
  - the stage filter widened.
- **Survived (1):** K08, the ASYNC_REG check narrowed to the *first-listed* cell. The stub plants a missing attribute only on `psrst_sync_r_reg[1]`, so a check that skips stage 0 is not detected. This is recorded as S1. It is not a missing check in the gate: the shipped hook checks both stages, its removal is killed (K07 here, M4 in the author's packet), and the vendor-side live run on dev's real netlist refused on `psrst_sync_r_reg[0]` (`live-hook-dev-netlist/live-lines.txt`: `LIVE-DEV rc=1 ... psrst_sync_r_reg[0] lacks ASYNC_REG`, then `LIVE-ATTR rc=0` with the cut applied).
- **Hook presence.** I could not run it: the review host has no LiteX/VexiiRiscv elaboration environment (see Limits). I read the assertion at `test_shipping_clock_constraints.py:99-101`. `servo == ["kl_servo_reset_sync_constraints <clocks[1]>"]` requires exactly one hook naming the actual milan PLL output object, so a removed, duplicated or renamed hook fails it. Lines `102-106` require one `source` and `synth < source < hook < opt`. The author's receipts show the hook-call-removed mutant (M1) and the hook-skipped-with-servo-present mutant (M5) KILLED by exactly that assertion. They also show all four shipping elaborations (1x1 TDM8 and 8x8, e1 and e2) printing `kl_servo_reset_sync_constraints milansoc_crg_clkout1 PASS` at 6cfb27da (`constraint-check/test_clock_constraints-6cfb27da.log`, rc 0).
- **Kill mechanism.** Errors in tclsh on stdin go to stderr while the script continues, so the "PASS" line can still print. The test asserts `returncode == 0 and not result.stderr`, and that is what kills the cut mutants. I confirmed this from the mutant logs. The gate is not vacuous.
- Result: met.

### (4) The CDC-report criterion ("The CDC report lists the crossing as safe")

- At head, `report_cdc` for the milan→PS pair reads `Info milansoc_crg_clkout1 milansoc_crg_clkout4 Safely Timed None 17 17 0 0 0`. The pair's 17 endpoints include `psrst_sync_r_reg[0]/D`: Safe 17, Unsafe 0, Unknown 0 (`post-route-head/cdc_milan_ps_summary.rpt`). The whole-design CDC summary and its 269 detail rows are identical to dev's (`route-a7ff491a/signoff-cdc-rows-vs-dev.txt`).
- As worded, the criterion is met: the report lists the crossing and lists it as safe.
- It does not discriminate: dev lists the same pair the same way.
- The stricter reading, a structural `CDC-3` row in the shipped report, needs a clock-level exception between the milan and PS clocks. That would change the 16 handshake endpoints and breach the criterion "No other path's constraint changes". The literal reading is the only one consistent with both criteria. The author published that reading in the PR body.
- The diagnostic (an in-memory asynchronous clock-group declaration, never shipped) classifies this endpoint as `CDC-3 1-bit synchronized with ASYNC_REG property` at head, against `CDC-2 ... missing ASYNC_REG property` at dev (`cross-probe-{head,dev}/diag_async_cdc_details.rpt`). So the structure is CDC-safe.
- Result: met as worded. The reading is listed for a maintainer to confirm (O2). It is not a finding.

### (5) Suites and rtl-fast

- **My runs at head**, on a `git archive` export of 6cfb27da with scoped Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`; wrapper sha256 905795b9...):
  - `mmcm_servo`: all four stages of its `run` target, as separate binaries: unit 109, rails 8, phc_step 113, slew 90 = 320 checks, 0 failures. This equals the author's tally of 320.
  - `mmcm_servo_autorepair`: 47 checks, 0 failures.
  - `crf_tx`: 129, 0 failures.
  - `media_nco`: 410, 0 failures.
  - `follow_ring`: rc 0.
  - `aaf_clock_meter`: `run` passed, with 465 + 6 = 471 checks and 0 failures, matching the author. Its `mutants` stage completed 25 of 36 rejections, all `[PASS]` and none `[FAIL]`, before my wall-clock cap under host contention (rc 124). See Limits.
- **Author receipts at 6cfb27da**:
  - the 17 servo-compiling suites: all rc 0 with `suite_tally --verdict`, 73,367 checks, 0 failures (`suites/tally.txt`). A first `mbx` rc 2 is explained in the packet and reproduced by its log: `mutants-quick` parsed `make[1]: Entering directory` without `--no-print-directory`. The rerun with CI's MAKEFLAGS gives rc 0, 6 of 6 mutants caught.
  - rtl-fast A/B replay: rc 0, `failed jobs: none`, head 6cfb27da.
  - Yosys `tops: 60 pass: 60 fail: 0`.
  - docs gates: rc 0.
- I enumerated the suites whose Makefiles name the servo or `milan_datapath` myself and found 14. The other three in the author's 17 (`crf_tx`, `media_grid_align`, `media_nco`) are a superset, not a gap.
- Result: met on the author's receipts, with partial independent reproduction.

### Timing (acceptance 5)

- Route-1x1 at ExtraPostPlacementOpt, recipe unchanged: WNS +0.166 ns slow / +1.481 ns fast, WHS +0.055 ns slow / +0.020 ns fast, 0 failing endpoints at every corner (`route-a7ff491a/corner-table.md`). This meets the BUILDING section 5 floor (WNS ≥ +0.03 ns, WHS ≥ 0) at every corner.
- The implementation-log gate passes (`check_implementation_log.log`). Route status shows 0 nets with routing errors.
- `pp_resource_gate --endpoint route-1x1` exits 1 on WNS alone (0.44 → 0.166). Under #818 a fall from the record is a warning, and the record is re-recorded once after the release merges (manager rule). So it is not a finding.

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE.

**S1 - SUGGESTION - Tests - `sw/builder/test_clock_constraints.py:225-228` - the ASYNC_REG refusal is planted on one stage only**
- Authority/evidence: AGENTS.md section 6, `Tests` ("each new test can fail for the defect it claims to detect"); `docs/testing/RUNNING_TESTS.md:197` ("checks ... each of its refusals"). Mutant K08 (check narrowed to the first-listed cell) survives (`receipts/tcl-mutants/K08-asyncreg-check-first-listed-cell-only.log`, rc 0). The refusal itself is killed by removal (K07, author M4), and the stage-0 case has vendor-run evidence (`live-hook-dev-netlist/live-lines.txt`).
- Impact: none today, because the shipped hook checks both stages. A future edit that narrows the check would pass the stub test.
- Suggested outcome: plant `async(...)` FALSE/empty on `psrst_sync_r_reg[0]` as well as on `[1]`, for example by looping over both stages.
- Verification: K08 is killed (`scripts/tcl_mutants.py`).

**S2 - SUGGESTION - Robustness, RTL - `sw/litex/clock_constraints.tcl:57-58` - the reset arrival is unbounded**
- Authority/evidence: the author's open risk 2. The 11.368 ns route here against 2.671 ns at dev (`post-route-*/crossing.txt`). The ordering analysis in focus check (2).
- Impact: none required. The handshake's toggle level makes release order harmless. Assertion order has margin in this route: at least about 1.6 ns taking each side's worst phase independently, about 6.6 ns once the shared PS edges are counted. The worst case is one fine-phase step during a reset.
- Suggested outcome, optional: add `set_max_delay -datapath_only` (one PS period or one milan period) beside the cut, so that the margin is checked by STA.
- Verification: `report_exceptions -to` the pin shows the bound, and the route meets it.

**O1 - observation, out of scope (candidate new Issue, not a finding against this PR)**
- `KL_mmcm_drp_servo.sv:533-537`: the audio-domain reset synchroniser `arst_sync_r`, with the same `{arst_sync_r[0], rst_n}` pattern, carries no ASYNC_REG. The delta does not touch it. Whether its crossing is cut depends on the existing audio clock constraints. The whole-design CDC report already lists 8 pre-existing `CDC-2 ... missing ASYNC_REG` rows, identical at dev and head.

**O2 - observation for the manager/maintainer**
- Confirm the CDC-criterion reading in focus check (4) on #817.

## Lens coverage (reviewer-owned ledger)

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #817 acceptance (all five bullets) against `route-a7ff491a/{exceptions-diff-vs-dev.txt,alinx_ax7101_exceptions.rpt,corner-table.md}`, `post-route-{dev,head}/{crossing.txt,crossing_setup.rpt,exceptions_ignored.rpt,milan_ps_endpoints.tsv,cdc_milan_ps_summary.rpt}`, `constraints-text/*.diff`, `cross-probe-*/diag_async_cdc_details.rpt`; the issue's Fix paragraph (false path + ASYNC_REG on both flops allowed) | R750-1 | 6cfb27dacafb2e5b693412db3342ca0fccc9c0bc |
| RTL | CLEAN | `KL_mmcm_drp_servo.sv:533-570,1289-1378`, `hdl/common/cdc_handshake.sv:38-84`, `hdl/milan/milan_datapath.sv:7321-7340`, `milan_soc.py:240-300,380-420,854,3099-3123`; servo lint 0 warnings head and dev; Yosys `a:ASYNC_REG` head vs dev; routed placement and attribute (`post-route-head/crossing.txt`) | R750-1 | 6cfb27dacafb2e5b693412db3342ca0fccc9c0bc |
| Robustness | CLEAN | Reset assertion/release ordering against the toggle handshake (focus check 2); refusal paths of `clock_constraints.tcl:21-59` (count, attribute, chain, clock pair, missing clock), all exercised by 16 killed mutants; pruned-servo and no-milan-clock install paths (`milan_soc.py:264,397,3122`); `_source_hooks` single source | R750-1 | 6cfb27dacafb2e5b693412db3342ca0fccc9c0bc |
| Tests | CLEAN | `test_clock_constraints.py:164-248` (stub test run at head, rc 0; 17-mutant campaign, 16 killed, 1 SUGGESTION); `test_shipping_clock_constraints.py:95-111` (read; author M1/M5 kills and 4 shipping PASS lines at 6cfb27da); servo suites run at head (`receipts/suites/`); author 17-suite tally, rtl-fast A/B, Yosys 60/60 | R750-1 | 6cfb27dacafb2e5b693412db3342ca0fccc9c0bc |
| Docs | CLEAN | `docs/litex/CLOCK_DOMAINS.md:92,237,376-380`, `docs/integration/BUILDING.md:606-629`, `docs/testing/RUNNING_TESTS.md:185-200` against the Tcl and the evidence; comment-rule scan of every added line (no lane/round/reviewer labels); commit messages one line, no trailers; author docs gates rc 0 | R750-1 | 6cfb27dacafb2e5b693412db3342ca0fccc9c0bc |

## Real limits

- I ran no vendor implementation. The routed, exception, CDC and timing figures are the author's published receipts, read and cross-checked here, not reproduced.
- I did not run the shipping LiteX elaboration (`test_shipping_clock_constraints.py`): the host has no LiteX/VexiiRiscv environment, and installing one is outside this review's allowance. Hook presence rests on reading the assertion and on the author's M1/M5 receipts.
- Of the 17 suites I reproduced only `mmcm_servo` (all four binaries), `mmcm_servo_autorepair`, `crf_tx`, `media_nco`, `follow_ring` and `aaf_clock_meter` `run`. The rest rest on the author's receipts. `aaf_clock_meter` `mutants` stopped at 25 of 36 (all passing so far) on my wall clock under host contention. A detached run was not permitted in this session.
- Hosted check runs at this exact head, listed after the verdict was written (`receipts/hosted-check-runs-6cfb27da.txt`): 58 contexts, 57 `success` (including `rtl-fast`, `verilator-suites`, `yosys-portability`, `yosys-elaboration`, `verilator-lint`, `elaborate`). One context is `skipped`, `Physical gPTP (nightly and manual)`, and it is not executed evidence. I did not open job logs, so I did not confirm whether the builder member that runs `test_clock_constraints.py` executed or declared a LiteX skip in hosted CI. The manager owns hosted/act acceptance.
- No manager source bank ran at this head, and none is claimed.
- Physical calibration was NOT RUN. Field skips are not hardware proof. No hardware was used.
- Every probe ran on exports or copies under the packet's `scratch/`; my own bytecode was removed from the clone after the first driver run. At the end, the clone is at HEAD 6cfb27da, tree 0fa85222, with zero status lines (ignored files included). The index mode/blob/path digest equals the HEAD tree's. The initialised submodules sit at their gitlinks (`receipts/clone-integrity.txt`).

## Pending manager duties

- Validate the current-dev merge candidate (builder and native banks; live dev 1e80128f0a467b58bf884b7d9bf62e013a2fb141), and own hosted/act acceptance.
- Record the WNS warning under #818. Re-record the area record once after the last release merge.
- Have a maintainer confirm the CDC-criterion reading (O2). Optionally file O1 as a new Issue, and carry S1/S2 to the author.

## Prior public findings

I wrote this section after the verdict, findings and ledger above were on disk. The PR thread then held three public comments: two review-start notices and the internal round R749-1 (`POSITIVE`, exact head 6cfb27da). There are no review objects or review-thread comments. R749-1 recorded no BLOCKER, MAJOR, MINOR or RESIDUE, and two SUGGESTIONs. At this head:

- **R749 S-1** (Tests, Robustness): no committed control covers the pruned-servo branch at `milan_soc.py:3120-3123`.
  - **Retained, as a SUGGESTION.** The head is unchanged, and the shipping test elaborates only servo-present shapes.
  - I agree with the impact assessment. A regressed guard would make a `--no-media-clock-servo` build fail loudly in the hook (`expected two servo reset synchronizer flops`). It would not produce a wrong bitstream.
  - I did not reproduce its pruned-elaboration receipts (no LiteX here).
- **R749 S-2** (RTL, Robustness): the unbounded cut.
  - **Retained.** It is the same item as S2 here, and the same optional outcome.
  - R749 quotes the assertion-race margin as about 1.6 ns; focus check (2) above quotes about 6.6 ns. Both are correct. The 1.6 ns figure takes each side's worst PS phase independently. The 6.6 ns figure counts edges, because both events are on the same PS clock edges.
  - Both agree the step cannot occur in this route, and that the worst case is one zero-count phase step during a reset.
- **S1 here** (ASYNC_REG refusal planted on one stage, surviving mutant K08) does not appear in R749-1. It is new in this round.

No prior finding is open at MINOR or above. The verdict stands.

R750-1 FINISHED
