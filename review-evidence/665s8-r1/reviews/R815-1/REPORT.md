[R815] NEGATIVE - exact head bfb2df37079f0172d6e94841ea5b9bd084e3ee06

Internal cleared-context review R815-1 of issue #868 / PR #879 (`665-s8-wire-timing` -> `dev-soft-core`).
Exact head `bfb2df37079f0172d6e94841ea5b9bd084e3ee06`, tree `c39da4934203695af6af8d00b3f16dd80c8eab8c`, source base `dev-soft-core` `1d6bf5556ae28764361d85012b86394eb467d294`.
All five lenses were applied. Four MINOR findings are open: F1 (Conformance, Tests, Docs), F2 (Tests, Docs), F3 (Tests, Robustness) and F4 (Robustness, Docs). So the verdict is NEGATIVE, and only RTL is covered clean.
One RESIDUE (R1) and one SUGGESTION (S1) do not affect the verdict.

## Scope as reconstructed

- Issue #868 acceptance 1 to 5 (frozen body).
- The round 2 ruling on the issue (issuecomment-6755260058):
  - 8x8/2if by option (a), testbench and recipe only;
  - CI runs the 1x1 short paths, and a local campaign of 4 seeded units to the second ANNOUNCE covers announce and advertise;
  - item 3: the draws run at S2b's composed load, with each distribution reported with and without it;
  - the egress-past-reserve plant must fail;
  - round 1's probe gaps are graded;
  - `ctrl_service_hooks` is #869.
- Authorities:
  - Milan v1.2 Table 5.26 and Table 5.50, as `docs/reference/FR_NFR.md` 3.4.1 states them;
  - IEEE 1722-2016 B.3.4.1/B.3.4.2. The sequencing was checked against `third_party/tsn-c-stack/src/maap.c:125-143`: the final probe expiry sends its PROBE and the ANNOUNCE in one pass, so three probe intervals per acquisition is the complete set;
  - FR_NFR 3.4.1's 240 ms AECP bound, and H-ACMP, H-AECP, H-MAAP and H-ADP;
  - `sw/firmware/ctrl/maap/README.md:43-50`;
  - `sw/firmware/ctrl/app/ctrl_app.h:51-56`: the timer slots are ADP 0, ACMP N and MAAP 2N, and the grader's slots match.
- Prior public review findings on this PR: none existed at this head. There are no PR reviews, no inline comments, and only the two review-start comments; the issue carries no reviewer findings. Nothing had to be resolved or retained.

## What this review executed (receipts in this packet)

| Check | Result | Receipt |
|---|---|---|
| `run.py --self-test` at head | rc 0, `33 controls, 0 failed` | `receipts/selftest.log`, `.rc` |
| Regrade of the published unloaded logs (1x1, 8x8/2if) with the head's grader | 0 findings each. `results.json` is byte-identical to the published one, and the log digests equal the author's published sha256 | `receipts/regrade/`, `scripts/regrade_published.py` |
| milan_dp split leg at base `1d6bf555` and at head, with the pinned Verilator 5.050 | build and run rc 0 at both. `split.out` is identical, sha256 `14b57a6d...`, equal to the author's receipt. The default `make -n build-split` command lines are identical | `receipts/split/` |
| The head's split top at 8x8/2if (`SPLIT_SHAPE=endstation_ax7101_8x8 SPLIT_STREAMS=8 SPLIT_IF=2`) | build rc 0. Warning classes and counts are identical to the 1x1 builds: no new class | `receipts/split/warn-*.txt`, `split-head.build-split8.rc` |
| `make twin` at base and at head | rc 0 at both. `fabric.json`, `split.json` and `report.json` are byte-identical, and their hashes equal the author's receipt | `receipts/split/twin-*.sha256` |
| `make split-cdc` at head | rc 0, 13 checks, 0 failures | `receipts/split/split-cdc-head.*` |
| `ci_gate_workflows.py --check`, `ci_events.py --check` and `--selftest` | rc 0. Events OK at 2,432 contract items; self-test PASS at 5,779 arms | `receipts/ci/` |
| `docs_check.py`, `check_em_dash.py --base 1d6bf555`, `gen_toc.py --check`, `git diff --check`, the SV/C++/Python/shell idiom gates, `check_feature_status.py` | rc 0 each | `receipts/docs/` |
| Fault probes of the grader and harness | see F1 to F4 | `receipts/probes/`, `scripts/probe_*.py`, `scripts/load_delivery.py` |
| The review clone after every probe | HEAD, index tree and worktree all equal `c39da493...`. No index flags. Each gitlink equals its checkout, and the checkouts are clean | `receipts/integrity/review-clone.txt` |

## Findings

### F1 MINOR - Conformance, Tests, Docs - the composed load's MAAP records are missing from almost every loaded burst after the first ANNOUNCE

- **Location.**
  - `tb/verilator/ctrl_wire_timing/wire_main.cpp:476-479` (the echo history) and `:496-500` (an echo skipped);
  - `tb/verilator/ctrl_wire_timing/README.md:111` and `:115`;
  - `tb/verilator/ctrl_wire_timing/wire_scenario.py:29-32`;
  - `sw/firmware/ctrl/maap/README.md:49`.
- **Authority and evidence.** Ruling item 3 requires the draws at "the other windows' traffic and timers as S2b's model loads them". The harness states two things about the MAAP records:
  - its only MAAP deviation is that the echoes "before the first ANNOUNCE ... are skipped" (README:111);
  - "an ADP deadline's [burst] is MAAP's and SRP's" (README:115).

  The echo source is one 64-frame history per interface, holding every protocol sent at the MAC (`wire_main.cpp:476-479`). The CPU budget harness keys its history by channel (`tb/verilator/ctrl_service_budget/sim_main.cpp:219-221`). So in the wire harness an ANNOUNCE drops out of the history within about two draws of traffic, and every later MAAP echo is skipped.

  Measured from the published `results.json` load blocks (`receipts/probes/load-delivery.log`):
  - campaign unit 2's draw bursts delivered 49 of 4,788 MAAP records: 21 of 2,394 in the ACMP bursts and 28 of 2,394 in the AECP bursts;
  - unit 3's draw bursts delivered 56 of 4,788;
  - every ADP deadline offer of every loaded run skipped all 7 of its MAAP records. That is 2 offers per 16-draw run and 12 per campaign unit, so those bursts were SRP only.

  In the 16-draw runs the skipping falls before the first ANNOUNCE, where the stated deviation covers it.
- **Impact.** Two sets of loaded figures were measured under a lighter load than the one stated: no MAAP records, and so none of the DEFENDs those records cause.
  - the loaded campaign units' ACMP and AECP draws over about 33 s after the first ANNOUNCE;
  - the ADP advertise periods and egress under their deadline bursts.

  The README, the PR and the closed MAAP note all describe the load as carrying those records. The margins are wide (the campaign's worst ACMP transaction is 5.4 ms and its worst AEM response 6.7 ms), so no bound is predicted to flip. But the measurement condition that ruling item 3 requires is not the one delivered, and the text says it is.
- **Required outcome.** One of these:
  - the MAAP echo finds interface 0's last ANNOUNCE whenever one has been sent, as the CPU budget harness's per-channel history does, and the loaded campaign units, with any loaded figure that depends on them, are measured again;
  - the deviation is stated with its delivered counts and accepted by the ruling's owner.
- **Verification.**
  - In a loaded campaign unit's `results.json`, the skipped MAAP echoes are only those of offers made before the first ANNOUNCE.
  - A stimulus or self-test control shows the echo is found after unrelated traffic has filled the history window.

### F2 MINOR - Tests, Docs - deadline loads that never reach the MAC are counted as offered load

- **Location.**
  - `tb/verilator/ctrl_wire_timing/wire_main.cpp:307-312` and `:509`;
  - `tb/verilator/ctrl_wire_timing/wire_grade.py:217-221` and `:590`;
  - `tb/verilator/ctrl_wire_timing/README.md:88`, `:168-173` and `:224-229`;
  - the PR body's "load offers" columns.
- **Evidence.** Every arm of a triggered slot prints its `LOAD` line at the arm, and queues its frames to be offered from the deadline less 200 us. A deadline past the run's end is never reached, so its frames are never offered. They are still counted in `results.json`'s `load.offers` and `load.frames`, which the grader describes as "the frames offered" and the README as "each load offered".

  From the published results (`receipts/probes/load-delivery.log`):
  - each loaded 16-draw run, at 1x1 and at 8x8/2if, counts 1,999 load frames. With its 64 draw frames that is 2,063, against 1,951 received at the MAC and the bench, so 112 frames were never offered:
    - two MAAP offers: the probe arm that the final probe expiry cancels, and the announce arm 31.9 s out;
    - one ADP offer: the 5,000 ms advertise arm.
  - campaign units 2 and 3 each have 72 frames that were never offered.

  So "load offers: maap 5, adp 2" stands for 3 MAAP and 1 ADP deadline bursts actually in the loop at an expiry. In the campaign, the cancelled probe arm's burst is delivered but meets no expiry.
- **Impact.** The stated load in `results.json`, the README tables and the PR overstates the delivered load and the number of timer expiries measured under load.
- **Required outcome.** For each load, the result reports the offers and frames that reached the MAC inside the run, or it separates armed triggers from delivered bursts and from expiries met. The tables say which.
- **Verification.** For every loaded run, the delivered load frames plus four per draw equal `SUMMARY` `rx_frames` + `bench_rx`.

### F3 MINOR - Tests, Robustness - the grade does not require each draw's PROBE_TX, nor any advertise period in a campaign unit

- **Location.** `tb/verilator/ctrl_wire_timing/wire_grade.py:399-403`, and `:551-585` (`REQUIRED` and the count checks).
- **Evidence.**
  - **A missing PROBE_TX.** `scripts/probe_missing_probe_tx.py` removes one draw's PROBE_TX transaction from the published unloaded logs: its commit, its KL_mbx egress, its MAC frame, the talker's answer and that transaction's ACMP-slot arms. The head's grader then reports 0 findings in all three cases: 1x1 with k=0, 1x1 with k=3, and 8x8/2if with k=3.
    - `acmp.probe_tx` falls to n=15 with no finding.
    - `acmp.bind_to_probe_tx` silently pairs the bind with the next draw's PROBE_TX, about 100.9 ms later.
  - **No re-advertising.** `scripts/probe_no_advertise.py` takes the self-test's clean campaign-shaped log and removes ADP's periodic advertising. Graded with two ANNOUNCEs, it gives 0 findings, with `adp.advertise_period` n=0.
  - `REQUIRED` lists neither path, and the count checks cover only BIND_RX commands, AEM commands and ANNOUNCEs.
- **Impact.** Two regressions would pass:
  - a bind that causes no PROBE_TX (item 1's second path) would pass the CI step;
  - an entity that stops advertising (item 3's advertise period, graded only in the campaign) would pass a campaign unit.
- **Required outcome.** The grade finds both cases, each with a self-test control:
  - a draw whose bind is not followed by its own PROBE_TX before the next draw, or a PROBE_TX count different from the draws;
  - at `announces > 1`, an absent `adp.advertise_period` sample.
- **Verification.** Both probes above are found by their own words.

### F4 MINOR - Robustness, Docs - `--reuse-build` accepts a stale model after the split top, the datapath RTL or the firmware changes

- **Location.** `tb/verilator/ctrl_wire_timing/wire_build.py:22-23` (the docstring) and `:169-179` (`inputs()`).
- **Evidence.** `inputs()` records these files:
  - the built ELF and the split archive;
  - the CPU half's export sources;
  - `wire_main.cpp`, `wire_soc.py`, `wire_build.py`, `flash.hpp` and `wire_config.hpp`.

  It does not record `tb_split_top.sv`, the datapath and KL_mbx RTL that the split recipe builds, `milan_dp/Makefile`, or the firmware sources.

  `scripts/probe_reuse_stale.py`, run on a disposable checkout with every change restored, changes one file of each kind:
  - `tb_split_top.sv`, `KL_mbx.sv`, `KL_ctrl_split.sv`, `maap_mbx.c` and `milan_dp/Makefile` are each ACCEPTED, so the stale build is reused;
  - the recorded `KL_mbx_wb.sv` is refused, so the probe is not vacuous.

  The docstring says "Every input the model is built from, or reads when it runs, is recorded ... so a reused build is refused when any changed". That is not true. The sibling CPU budget harness records the firmware source trees.
- **Impact.** A campaign unit or a reviewer that reuses a build at a later head silently runs the old model, and the PR's validation commands use `--reuse-build`.
- **Required outcome.** The reuse record covers the split top's and the firmware's sources. Otherwise, the docstring and the README state exactly what is recorded, and the PR's reuse commands are confined to one head.
- **Verification.** The probe's five changes are refused.

### R1 RESIDUE - `tb/verilator/ctrl_wire_timing/wire_scenario.py:18` - a review round named in a source comment

- `THE LOAD (#868, the round 2 ruling):` names a review round, which the owner's comment rule forbids in source comments.
- Exact fix: `THE LOAD (#868, its ruling on the load):`.
- The README's link to the ruling is on a harness page, not in a source comment, so it is not counted here.

### S1 SUGGESTION - `tb/verilator/ctrl_wire_timing/run.py:74-76`, with `:177` and `:187`

- On the `--point` and `--campaign` paths, a refused stimulus raises out of `main()`: a traceback and exit 1, instead of the documented refusal exit 2. Only `--ci` catches it.
- The head's own scenario never reaches this (self-test control `clean-loaded-script`).
- Catching `ValueError` there would keep the exit-code contract.

## Per-lens results

- **Conformance - UNCLEAN (F1).** Applied to items 1 to 5, against the clauses and the published figures:
  - **Item 1.** The worst ACMP transaction is 17.651 ms, at 8x8/2if under load: 182.3 ms inside Table 5.26's 200 ms. It was measured at both points, without and with the load.
  - **Item 2.**
    - The probe intervals are 512.9 to 583.7 ms, strictly inside B.3.4.2.
    - The four announce intervals are 31,956.5 to 31,958.2 ms, inside B.3.4.1.
    - The worst interval error is 1.672 ms, and the egress over 36 timer-driven frames is 0.264 to 2.455 ms. Both are under the 11 ms reserve, and the closed MAAP note's numbers recompute from the published results.
  - **Item 3.**
    - The advertise periods are 5,363.0 to 8,387.6 ms. The grader checks that every advertise arm is exactly 5,000 ms and that every delay is drawn in 0 to 4,000 ms.
    - The worst AECP response is 20.567 ms, against 240 ms.
  - **Item 4.** Both plants are graded on every run's log, and the self-test carries both.
  - **Item 5.** `wire-timing` is a job of the existing `rtl-fast` workflow, with `timeout-minutes: 30` (`.github/workflows/rtl-fast.yml:1379`). The verdict requires it, and `scripts/ci_events.py:2646` pins it. Its hosted wall time is pending (see the limits).
  - **Ruling item 3** is not met as stated: F1.
- **RTL - CLEAN.**
  `[R815] PASS RTL - tb/verilator/milan_dp/tb_split_top.sv:360-438, tb/verilator/milan_dp/Makefile:852-881 at bfb2df3707 - checked against ruling item 1 and KL_mbx.sv:497-503/660 (fw_send_o/fw_ack_p_i contract); see the notes below`

  - **Interface 0.** At one interface the composition is unchanged: the split leg's and the twin's outputs are byte-identical base vs head, and their build command lines are identical.
  - **The receive mux.** It holds `rx_if_i` for a frame, gives interface 0 priority at a frame's start, and loses no byte.
  - **Transmit.** Steered by `tx_if_o`.
  - **The commit acknowledgement.** One pulse at `MBX_FACE_ACK_CYCLES_C`, identical to `ctrl_service_budget/split_soc.py:213-224`.
  - **The interfaces past the first.** Their windows and face events are held idle. Everything is in the sys domain with no new crossing, and `split-cdc` gives 13 of 13.
  - **Widths.** Correct for `MBX_IF_W_C` and `N_STREAMS_P`.
  - **The 8x8/2if build.** It builds with no new warning class.
  - **Scope.** No production RTL, `milan_soc.CtrlMailbox` or `sw/mailbox/mailbox.yaml` change appears in the diff.
- **Robustness - UNCLEAN (F3, F4).** Also applied:
  - truncated and incomplete logs, and logs with no tally, are refused;
  - the time limit becomes a failed tally;
  - an unsettled host boundary throws;
  - censoring is confined to commands the log ends within the bound of;
  - a refused stimulus is caught on the CI path; S1 covers the other paths.
- **Tests - UNCLEAN (F1, F2, F3).** Also applied:
  - the 33 self-test controls, each caught by its own words;
  - the two plants on real logs;
  - the regrade of the published logs, byte-identical;
  - the attribution of the PROBE_TX handling, checked on a real log: the unbind cancels the slot rather than arming it, so no later arm stands in for an unhandled answer.
- **Docs - UNCLEAN (F1, F2, F4).** Also applied:
  - the harness README, the milan_dp README, CI_WORKFLOWS.md and the MAAP note, against the code and the published figures;
  - the docs, em-dash, TOC and idiom gates, rc 0;
  - the comment rule, where R1 is the only new instance.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | issue #868 body, ruling issuecomment-6755260058, FR_NFR.md 3.4.1/3.4.2, maap/README.md:43-50, tsn-c-stack maap.c:125-143, ctrl_app.h:51-56, wire_grade.py, wire_scenario.py, published results.json of all 8 runs | R815-1 | bfb2df37079f0172d6e94841ea5b9bd084e3ee06 |
| RTL | CLEAN | tb_split_top.sv, milan_dp/Makefile, KL_mbx.sv fw_send/ack, KL_ctrl_split.sv, the split leg, twin, split-cdc and 8x8 builds at base and head | R815-1 | bfb2df37079f0172d6e94841ea5b9bd084e3ee06 |
| Robustness | UNCLEAN (F3, F4) | run.py, wire_build.py, wire_grade.py, wire_main.cpp, the probes in receipts/probes | R815-1 | bfb2df37079f0172d6e94841ea5b9bd084e3ee06 |
| Tests | UNCLEAN (F1, F2, F3) | wire_selftest.py (33 controls), the plants, the regrade of the published logs, the probes, ci_events check and self-test | R815-1 | bfb2df37079f0172d6e94841ea5b9bd084e3ee06 |
| Docs | UNCLEAN (F1, F2, F4) | ctrl_wire_timing/README.md, milan_dp/README.md, CI_WORKFLOWS.md, maap/README.md, the PR body, the docs gates | R815-1 | bfb2df37079f0172d6e94841ea5b9bd084e3ee06 |

## Real limits

- **The harness was not built or run here.** Its CPU half needs the product LiteX tree and the CPU generator, which this review's environment did not provide. So the measured figures rest on the author's published receipts.
- **Two of the eight runs were cross-checked.** The two unloaded logs are published, and they regrade byte for byte at this head. The loaded logs are published only as digests, so their figures were not regraded independently. F1 and F2 rest on their published `results.json` counts and on the code.
- **The local campaign was not repeated.** No full parent, PP, gPTP, Yosys or builder bank was run, and no Docker or act run.
- **No physical calibration was run.** This is simulation evidence only, and no hardware claim is made or implied.
- **MAAP's interval draws are fixed by the boot**, as the PR states. So the four announce intervals are four phases of one drawn value, and the boundary draws (511 and 589 ms, 30,011 and 31,989 ms) are not exercised at the wire.

## Pending manager duties

- **The hosted run.** Item 5's hosted wall time and verdict for the exact-head `rtl-fast` / `wire-timing` job. At this review's end `rtl-fast` was still queued (`receipts/integrity/hosted-runs-at-review-end.json`). The author's gate pass recorded 2,317 s for the step on contended CPUs, beyond the job's 30-minute timeout, so the hosted figure decides it.
- **The merge candidate.** Validation against live `dev` `45c0b56c1f4a8a52878815fdcb1359d18e2c5b1c` at the merge turn, with the builder and native banks.
- **Ruling item 3.** The author's open question (deadline bursts that leave out the ACMP and AECP records) needs a decision, and F1 bears on the same item.
- **The residue checklist.** Carry R1.

R815-1 FINISHED
