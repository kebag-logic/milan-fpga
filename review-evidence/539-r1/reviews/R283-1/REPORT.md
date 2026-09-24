[R283] NEGATIVE - exact head f49b57a60ae4ce72e7a1a9ea8e5db13f1ca838ed

Round R283-1, external independent review of issue #539 / PR #547, cleared context.
Head `f49b57a60ae4ce72e7a1a9ea8e5db13f1ca838ed`, tree `52329eb1f29ffbc774a23da9a3c6e062514ee9e3`,
source base `26d855a9176d63625e6635a029a0c44e3d57ce9a` (4 commits, 7 files, +672/-22).
Lenses applied: Conformance, RTL, Robustness, Tests, Docs. One open MINOR (Tests) makes the
verdict NEGATIVE; the other four lenses are covered clean at this head.

## Summary

The fix is correct and I reproduced it independently. At the base RTL, a locked +150 us PHC step
at mid-window is committed: window error +150040, integrator +15680 to +90700 (+30.62 to +177.15
ppm), written rate +130.65 ppm, and LOCKED drops to ACQUIRE a window later. The whole pre-fix
sweep matches the PR table, for example +100 us to +128.32 ppm, -150 us to -115.82 ppm, and 524 us
to the +200 ppm clamp, while 525 us and 1 s are discarded. So does the fixed behaviour: the 150 us
trace holds +15680 to +15700, the 113-check step suite passes, and all seven of the author's
one-line mutants fail their stated arms with the stated counts (66, 53, 19, 1, P3+U11, 1, P4).
Four more mutants of my own also fail: a one-cycle-late verdict, a one-cycle-early verdict, a
forward-only detector and a 25 us threshold. The +31 LUT figure reproduces exactly.

I judge the author's reading of acceptance 2 (detect the step where it lands in `ptp_now_i` rather
than wire the plane's pulse) sound. The plane's `phc_step_we_o` reaches the PHC as one `cmd_adjust`,
applied in one cycle. The per-cycle advance of the PHC is otherwise bounded far below the
detector's 4096 ns threshold, and the pinned plane's smallest step is 20 us.

The finding is about test evidence, not the RTL. The new U11 arm says in its check label that it
covers the 1024 ppm guard's resync path. With the resync branch removed, every U11 line (and the
whole unit and step suites) is byte-identical. See F1.

## Findings

### F1 - MINOR - lenses: Tests
- **Artifact:** `tb/verilator/mmcm_servo/sim_main.cpp:413` (check `[U11] >= 5 windows discarded (the resync path included)`), with the same claim at `:23` (`U11 ... discards, resyncs, holds`), `:395-396` and `:399` (`the 1024 ppm guard and its resync`). The PR body echoes it: "gives 6 discards and the resync".
- **Authority/evidence:** AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect." U11 is new in this PR. Mutant `no_resync` forces `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:605` (`if (disc_run_r == 2'(DISC_MAX_C - 1))`) false, so the resync never fires. U11 still reports `discards=6`, the same trim envelope and all checks ok (`receipts/probes/mut_no_resync_unit.log` against `receipts/probes/head_unit.log`). The step suite passes too (`mut_no_resync_phc.log`). The same mutant survives the base harness (`base_mut_no_resync_unit.log`), so the missing arm predates this PR. The claim that U11 covers it is new.
- **Why Tests only:** the RTL resync behaviour is unchanged and I read it as correct (see the RTL and Robustness lines). The authoritative docs describe it correctly (`docs/design/TIME_SYNC.md:113`). The defect is a check whose label claims coverage it cannot detect.
- **Impact:** a later change that breaks or removes the DISC_MAX_C resync ("a sustained slew can never wedge the servo", `KL_mmcm_drp_servo.sv:49-52`) stays green, while the suite's own output says that path is proven. A cold reviewer reading the check label would bank coverage that does not exist.
- **Required outcome:** one of the following.
  - (a) An arm that fails when the resync branch is removed. The resync shifts the next window boundary by the re-base tick, which can be observed; the step harness already reads `win_valid_r` and `tick_cnt_r` through its public build.
  - (b) Withdraw the resync claim from the U11 label and comments and from the PR text, and record the resync path as unproved (a new Issue if it is to be proved).
- **Verification:** re-run `scripts/probe.sh <tree> <wd> no_resync unit` (and `... phc`). Under (a), at least one arm must FAIL. Under (b), the check label and comments no longer claim the resync, as shown in the diff.

### Suggestions (optional, do not affect coverage)
- **S1 - SUGGESTION - Tests - `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:655,658`:** "The discard streak restarts with the new baseline" (`disc_run_r <= '0` on a step) has no failing arm. Mutant `no_streak_reset` survives both harnesses. It only acts through the resync, so an F1(a) arm could cover it too.
- **S2 - SUGGESTION - Tests - `KL_mmcm_drp_servo.sv:460,667`; `docs/reference/REGISTER_MAP.md:1884`:** two tally rules have no arm. Saturation at 63 is documented, and so is counting only a step that lands in an open window ("one a PHC step landed in"). Mutants `no_saturate` and `step_ignores_valid` survive both harnesses.
- **S3 - SUGGESTION - RTL, Docs - `KL_mmcm_drp_servo.sv:296-301`:** the comment says a legitimate per-cycle advance "stays below 256 ns on any clock". The per-cycle addend is `incr_i + adj_i` (`hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv:144-145`), both Q8.24 in 32 bits, so the true bound is below 384 ns. The 4096 ns margin is unaffected.

## Lens results (clean lines carry their evidence)

```text
[R283] PASS Conformance - issue #539 acceptance 1-3; KL_mmcm_drp_servo.sv:444-460,648-668; receipts/probes/repro_trace*.log, head_phc.log, mutation_table.txt; hosted_check_runs.tsv - Acc 1: a locked 150 us step under CRF selection reproduced at base RTL with the integrator traced (+15680 -> +90700), plus the sweep 21 us/100 us/-150 us/524 us/525 us/1 s. Acc 2: first alternative met; every P1 size from 21 us to +/-1 s holds the integrator within 512 units with LOCKED and one discard. The detection-at-ptp_now reading covers the plane's pulse: gptp_step_we_w -> eff_ptp_adjust_w (milan_datapath.sv:2742-2743) -> ptp_csr_sync -> timestamp_counter cmd_adjust, applied in one cycle (timestamp_counter.sv:160-170); the pinned plane's smallest step is 20 us (gptp-processor gen_gptp_ucode.py:378) > 4096 ns. Acc 3: failing arms for the step discard (det_off, no_abandon, no_squash, uncond_squash), the guard (guard_off: P3/U11) and the rate path (guard32: P4), all re-run clean. Every required hosted context at this head completed success (physical gPTP skipped by design). #545/#546 are filed and open. No port change, so no milan_datapath.sv edit is needed.
[R283] PASS RTL - KL_mmcm_drp_servo.sv:439-460,548-668,902; receipts/ooc_servo_{base,head}.txt, lint_rtl_check.txt - ptp_jump_r is set on the edge that stages the first stepped sample into ptp_q_r, so the verdict and the sample agree (a late and an early verdict mutant both fail P2). Case analysis: a step with no sequence in flight squashes a boundary that snapshotted it (P2a); a sequence in flight closed on a pre-step sample and commits (P2b); an abandon inside the last tick re-bases (P2c); a coincident S4 guard hit and step count 2, the step's writes win and pp_run is not re-armed. In a re-base cycle (win_valid low) the next tick bases on post-step time. 32-bit wrap: exact below 2^31 ns, a backward step wraps large, and the alias near k*2^32 ns falls to the 1024 ppm guard (documented at :74-77). Synchronous reset on ptp_jump_r; ptp_q_r's lack of reset is masked by win_valid_r. No CDC added. Area: 831->862 LUT, 789->790 FF, 140->150 CARRY4, DSP 1 (reproduced). The lint ratchet passes (90<=90) with no finding in the servo.
[R283] PASS Robustness - KL_mmcm_drp_servo.sv:444-460,497-546,648-668; timestamp_counter.sv:142-170; KL_crf_rx.sv:25,476; receipts/probes/head_*.log - Checked: both signs; the minimum and maximum of the frozen range (21 us..1 s, below 4096 ns undetected by design); boundary positions (P2a/b/c); repeated steps (the U10 storm; a second step before the re-base is absorbed uncounted); reset and IDLE clear the tally; HOLDOVER abandons and counts; VERIFY/REPAIR/FAULT/IDLE are unaffected (window block gated). False steps: the PHC advance per cycle is incr+adj (<384 ns) except for cmd_load/cmd_adjust, so no legitimate time movement trips 4096 ns on any CRF datapath leg. crf_rate_i is talker-timestamp only (KL_crf_rx.sv:25,476), so a local step cannot leak through the rate input. The pruned build (MCSERVO_P=0) is unaffected.
[R283] UNCLEAN Tests - see F1. Also examined: sim_phc_step.cpp (P0-P4, each P2 arm asserts it landed), the U10 envelope rewrite, the new U11, the Makefile targets, and 15 independent mutants (receipts/mutation_table.txt).
[R283] PASS Docs - docs/design/TIME_SYNC.md:112-113; docs/reference/REGISTER_MAP.md:1884; docs/testing/TESTING.md:481; KL_mmcm_drp_servo.sv:54-77,296-302 - The TIME_SYNC rows match the RTL (step window discarded, trim/integrator held; >1024 ppm discarded, four in a row re-base). The 0x8F8 row corrects the former "[15:9] reserved" to [9] reserved plus [15:10] tally (saturating, cleared in IDLE), matching status_o at :905. The TESTING row names the step suite and the trace target. The PR text's figures (LUT/FF/CARRY4, check counts, pre-fix table) reproduce. There is no U+2014 in added lines (check_em_dash 0 findings, 57/57 arms). git diff --check is clean and all four commits are one line. No stale in-tree doc found; the GM_LOSS_RECOVERY row lives on #540's lane.
```

On the U10 rewrite (a Tests judgement, not a finding): the base check fails at this head, trim 1519 to 1579, |d|=60 against a limit of 48 (`receipts/probes/head_rtl_base_tb_unit.log`). The base RTL's own steady state spans the same 1499..1579 band (`base_unit.log`), so this is the re-base moving the sampling phase, not a regression. The replacement checks every post-step sample and still rejects the recorded pre-guard 540 kick. The silicon-scale step property is proved far more tightly by P1 (1 ppm integrator bound).

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #539 body, comments and acceptance 1-3; milan_datapath.sv:2738-2833,5485-5515; timestamp_counter.sv:142-170; gen_gptp_ucode.py:378; repro and head traces; hosted check runs | R283-1 | f49b57a60ae4ce72e7a1a9ea8e5db13f1ca838ed |
| RTL | CLEAN | KL_mmcm_drp_servo.sv full diff and FSM/window/PI context; OOC area base/head; lint ratchet; KL_crf_rx.sv:328-335 path comparison | R283-1 | f49b57a60ae4ce72e7a1a9ea8e5db13f1ca838ed |
| Robustness | CLEAN | step sign/size/position/repetition/reset/state gating; PHC false-step bound; crf_rate independence; pruned build | R283-1 | f49b57a60ae4ce72e7a1a9ea8e5db13f1ca838ed |
| Tests | UNCLEAN (F1) | sim_phc_step.cpp, sim_main.cpp U10/U11, Makefile; 7 author and 8 reviewer mutants on both harnesses; base-harness cross-runs | R283-1 | f49b57a60ae4ce72e7a1a9ea8e5db13f1ca838ed |
| Docs | CLEAN | TIME_SYNC.md, REGISTER_MAP.md, TESTING.md rows; RTL header; PR body figures; em-dash, diff-check and commit form | R283-1 | f49b57a60ae4ce72e7a1a9ea8e5db13f1ca838ed |

## Prior public review findings

None to resolve or retain. When this round started and again when it was finalised (after the verdict and ledger above were written), PR #547 carried only the two review-start notices. It had no review bodies and no review-thread comments, and issue #539 carries no review finding (`receipts/pr547_comments_at_start.txt`, `receipts/pr547_comments_at_finalise.txt`, `receipts/issue539_comments.txt`).

## Real limits

- I did not run Vivado timing. The detector puts a 32-bit subtract and compare on the live `ptp_now_i` net, which the file itself stages elsewhere for timing (`:435-438`). The PR's comparison to `KL_crf_rx.sv:328-335` (an existing 32-bit subtract and two compares on the same `axis_clk` net) holds by reading, but it is not a measurement.
- I did not run `milan_dp` myself (aclk or tdm8render). The CRF-leg `A_MCSRV_STAT = 0x33` is the author's public log, and the hosted Verilator shards (including the dedicated milan_dp shard) succeeded at this head. False-step safety on the datapath legs rests on the structural bound above, not on an asserted datapath check: the aclk leg asserts only state 3.
- Physical calibration was NOT RUN, and skipped field or physical contexts are not hardware proof. All results here are Verilator 5.050 simulation with a behavioural MMCM model.
- The out-of-scope classes remain open by design. At this head a 100 us slew at 200 ppm still moves the integrator +30.62 to +80.66 ppm with ACQUIRE (`head_slew_100000.log`, #545), and the talker's own step is #546.
- The first mutation batch overlapped a re-run and was discarded. Every mutant verdict above comes from clean foreground re-runs. The host was heavily loaded, so runtimes are not representative.
- The reproduction commit's harness is trace-only, so `repro_phc.log` is a usage exit, not a verdict. The reproduction evidence is the `repro_trace*` logs.

## Pending manager duties

- Build and validate the candidate merge against live `dev` 615b5a5d7de01b23f15502e3732c6f2cb81ce74b (source base 26d855a9), and own hosted/act acceptance.
- Route F1 to the author and schedule a re-review of the answering head. Any change under `tb/verilator/mmcm_servo/` un-covers Tests, and an RTL change un-covers RTL, Robustness and Conformance.
- Coordinate the stale `GM_LOSS_RECOVERY.md` row with #540, whichever lands second.

## Reproduce

From this packet, with a tree exported at the exact head (and one at the base, and one at c16cd61e for the pre-fix traces) under `scratch/`:
`VERILATOR=<pinned Verilator 5.050> BASE_TREE=<base tree> sh scripts/batch.sh scripts/<jobs file>`; the mutants are named in `scripts/mutate.py`, and each refuses unless its edit matches exactly once. The area figures come from `sh scripts/ooc_servo.sh <tree> <out>`. Receipts are listed in `MANIFEST.sha256`.

R283-1 FINISHED
