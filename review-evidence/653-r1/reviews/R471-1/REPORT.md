[R471] NEGATIVE - exact head 77ea6cb46cc3f746a14fa717c5e49a4485fb071e

# R471-1: external review of PR #655 (Relates #653)

- Round: R471-1, external independent reviewer, cleared context.
- Exact head: `77ea6cb46cc3f746a14fa717c5e49a4485fb071e`, tree `6aab682e4390fc3f5c5cdb25cea1c8baba1a46ee`.
- Source base: `fea346e76c2a57ed5cd131af8fc68dfeff57f877`.
- Live `dev` when this round ended: `6c22d3cad7c8c24ed3f0c5eab535922a3428c8d5`. PR #650 moved it during the round (see pending manager duties).
- Scope: the re-scope ruling (issuecomment-5980290102), items 1 to 4, plus the reproduction of the two failing gates.
- Order read: AGENTS.md, CONTRIBUTING.md, docs/README.md, the #653 body, the lane comment, the author's STOP, the ruling and REVIEW READY. Then REQUIREMENTS.md (REQ-VER-06), the full diff `fea346e7..77ea6cb4` and its four commits, and the public evidence tree `c4b00e84:review-evidence/653-r1`.
- Prior public review findings on PR #655: none. The PR's only earlier comments are the two review-start notices. I read them after finishing my own pass over the diff.

## Verdict

**NEGATIVE.** The RTL fix, the standing tests and the area figure hold up. I reproduced each of them at the exact head with the pinned simulator.

Two MINOR documentation findings stay open, so the Docs lens is unclean:

- The authoritative design page still says that an unbound followed source's lock falls 100 ms later. For CRF it now falls at the unbind.
- The CHANGELOG states the wire order without saying it was shown in simulation only, while the hardware report on that order is still open.

One RESIDUE (two stale line pointers) is recorded with its exact fix. Conformance, RTL, Robustness and Tests are clean at this head.

## What I checked, per focus item

### (1) The CRF fix (`hdl/ieee1722/crf/KL_crf_rx.sv`)

**The new arm.**
- `:395` defines `w_bind_fall_w = !en_i && en_q`. It reuses the existing `en_q`, so no new register is added.
- `:627-631`: on a bind fall while locked, `locked_o` falls, `cnt_unlocked_o` gets +1 and `dirty_p_o` pulses.
- This matches the AAF rule at `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:857`. There, a bind fall while locked sets `sil_pend_r`, and the silence walk writes MEDIA_UNLOCKED +1 at `:607-611`.

**The 100 ms silence path.**
- `:538-545` is unchanged. It still unlocks a bound input that goes silent (unit check `[UNB-d0]`).
- After an unbind it finds `locked_o` low and counts nothing (`[UNB-b1]`, `[UNB-b2]`).
- When the timeout and the unbind land on one edge, both arms write the same non-blocking `cnt_unlocked_o + 1`, so the event counts once (`[UNB-d2]`, `[UNB-d4]`).
- The bind-rise wipe (`:641-696`) remains the last writer of `locked_o` and the tallies. Rise and fall are mutually exclusive by construction. My probe P8, which moves the arm below the wipe, is equivalent: 14287/0.

**STREAM_INTERRUPTED.**
- `w_hit` is gated by `en_i` (`:314`), so an unbound input accepts no PDU. `w_ev_si_w` (`:391`) cannot fire.
- Checked by `[UNB-a6]`, `[UNB-b3]`, the milan_dp U3/U4 checks, and my probe P6.

**The earlier lock fall, and its effect on the followed-CRF clock path.**
- `en_i = cfg_crf_en | acmpl1_bound` (`hdl/milan/milan_datapath.sv`, the `crf_rx` instance). The fall therefore happens only when the ACMP bind and the bench CSR lever are both low, which matches the REGISTER_MAP text.
- `crf_locked_w` feeds three consumers:
  - `CRF_CTRL[31]` (`.i_crf_locked`, `milan_datapath.sv:2661`);
  - the 4.4.4.3 restart request `mcr_restart_p_w` (`:3229-3232`), gated by `crf_clk_selected_r`;
  - the servo reference lock `ref_locked_w` (`:5745-5746`). On that fall the servo enters HOLDOVER (`hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:574`).
- With a followed CRF input selected, an unbind now produces its one restart request and its HOLDOVER at the unbind, instead of up to 100 ms later.
- The number of requests per unbind is unchanged: exactly one falling edge. The timeout after it finds the lock already down, and a rebind within 100 ms no longer produces the edge either, because the lock is already low.
- `rate_valid_o` already fell at the unbind (its `en_i` term, `:409-410`). So before this change the servo saw "locked, rate invalid" for up to 100 ms. After it, the lock and the rate validity agree.
- I judge this effect to be intended, benign and consistent with IEEE 1722-2016 4.4.4.3: the unbind is the disruption. It is documented in the datapath comment (`:3174-3176`), the REGISTER_MAP `0x738` row and TOC line, and the design page's evidence table (`MEDIA_CLOCK_FOLLOWING.md:297`) and meter note (`:994-996`). The design page's lock-loss rule is not updated: see R471-F1.

### (2) The `[UNB]` section and its controls

- `tb/verilator/milan_dp/sim_nxn.cpp:2293-2630` grades both inputs, AAF 0 and CRF 1:
  - U1: the response is SUCCESS;
  - U2: a push reporting the unlock reaches A and B, and the earliest one leaves after the response's last byte;
  - U3: the source pair as the response leaves, GET_COUNTERS right after it (1/1/0), and every later push equal;
  - U4: 10.5 M cycles later, 1/1/0.
- A single serial MAC TX trunk carries both frames, so last-byte order equals frame order.
- The leg reran at 421 checks, 0 failures. Both trace lines match the PR table exactly (CRF: MEDIA_UNLOCKED +200, response +277, pushes +2294 / +3057; AAF: +204, +277, +2294 / +3057).
- `make unb-mutants` reran at 6/6. Mutant failure counts: 4, 2, 2, 2, 2, each of 421. Each catch named its required checks, and its named holds still passed.
- In the crf_rx suite, the re-pinned `[5t-g3]` still pins all ten tallies exactly across the unbind. It now expects MEDIA_UNLOCKED +1, and `[5t-g3b]` adds the equality. My probe P1 (the arm deleted, the dev behaviour) fails `[5t-g3]` and `[5t-g3b]`. So the re-pin is the behaviour change and tightens the check. It is not a weakening.
- My own seven unit fault probes (`scripts/crf_probes.py`, crf_rx unit suite) were all caught:
  - P1: arm deleted, 8 failures;
  - P2: lock guard removed, 3;
  - P3: no Table 5.22 pulse, 1;
  - P4: lock kept, 4;
  - P5: +2, 7;
  - P6: STREAM_INTERRUPTED also counted, 4;
  - P7: timeout counts without the lock guard, 418.
  - The equivalence probe P8 passes, 14287/0.

### (3) Area

- Yosys `ooc.sh KL_crf_rx` with `OOC_SHAPE=configs/generated/endstation_ax7101_1x1_tdm8`, rerun at both commits:
  - dev: 433 LUT, 544 FF, 1 RAMB18;
  - head: 368 LUT, 544 FF, 1 RAMB18.
  - This matches the PR exactly.
- Vivado is not installed on this host, so I could not rerun it. I inspected the published reports `vivado-util-KL_crf_rx-{dev,head}.rpt` (Vivado v2026.1, xc7a100tfgg484-2, the binding generics in `vivado-crf_ooc.tcl`, which match `milan_datapath.sv:67` and `:245` defaults):
  - Slice LUTs 373 to 352;
  - Slice Registers 544 to 544;
  - 1 RAMB18 each.
- Both are within the ruling's 30 LUT / 60 FF bound. FF is unchanged on both instruments.

### (4) The stale line pointer

- The PR body corrects #653's `:597-605`. At dev, `:533-537` is the silence-timeout unlock and `:619-670` is the bind-rise arm. At head these are `:540-545`, `:641-696`, and the new arm `:627-631`. I verified each against both blobs.

### The two failing gates: real dev defects, not tool-version artifacts, and not caused by this PR

**`make -C tb/verilator/milan_dp_gptp`.**
- Results: dev `fea346e7` with pinned 5.050, head with 5.050 and dev with the host's 5.052 each gave 139 checks and 3 failures. The failures are "audio sample order, no duplicates or gaps" got=2 twice, and "all monitored audio sample ordering errors" got=5.
- dev against head: the 241 kept simulation-output lines are identical.
- dev 5.050 against dev 5.052: identical.
- The hosted nightly bracket with pinned 5.050 (`receipts/nightly_bracket.txt`):
  - `1269cdaf`, `cdf49d1a` and `e4b771f9`: 139 checks, 0 in-suite failures;
  - `241f9184`: 139 checks, 3 failures, the same three checks with the same values.
- The only hdl/configs/submodule/milan_dp-tb change in that bracket is PR #634 (`bbf704ec`, #629). The cause is not narrowed further inside it.

**`make -C tb/verilator/milan_dp_render tdm8render-mutants`.**
- head 5.050, dev 5.050 and dev 5.052: each 32 checks, 28 PASS, 4 FAIL, with identical verdict lines. The failures are:
  - the clean `--epoch-only` leg;
  - its two clean controls;
  - the "uncounted repeat" mutant, which survives.
- The clean `--epoch-only` leg run directly is identical at dev and head: 114 checks, 4 failures, all T30 CRF recentre checks ("fired the settled-grid trigger ONCE" and its three companions, got=0).
- At `241f9184`, before #648, the campaign already reads 28 checks with 24 PASS and the same 4 FAIL. These failures therefore predate #648. I did not bracket further.

Neither gate is in a required hosted PR context: Physical gPTP is nightly only and was skipped at this head, and tdm8render-mutants is an explicit campaign. Both need their own Issue (manager duty).

## Findings

### R471-F1: MINOR, Docs

- **Where:** `docs/design/MEDIA_CLOCK_FOLLOWING.md:1059-1060`, "Lock loss, holdover and restart", rule 1.
- **Authority/evidence:**
  - Rule 1 says: "The selected measurement's `locked` falls after 100 ms with no accepted PDU: the stream stopped, **was unbound** or STOPPED, or was rejected." The section opens with "The same rules apply to either kind of followed source" (`:1057`).
  - At this head, a followed CRF input's lock falls at the unbind's own edge (`KL_crf_rx.sv:627-631`). The servo's HOLDOVER (`KL_mmcm_drp_servo.sv:574` via `milan_datapath.sv:5745-5746`) and the 4.4.4.3 restart request (`milan_datapath.sv:3229-3232`) start then.
  - The PR updated the evidence table (`:297`) and the meter note (`:994-996`) but left this rule.
  - The bench record names this section as the declared behaviour (`docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1640-1647`, "Declared: Lock falls 100 ms after the last PDU").
- **Impact:** the authoritative design contract for the followed-CRF clock path misstates when an unbind drops the lock, starts HOLDOVER and requests the restart. A later bench lane graded against it would declare the wrong timing. AGENTS.md section 6, Docs: "Changed contracts are reflected in authoritative docs".
- **Required outcome:** rule 1, or a sentence beside it, states the following:
  - a followed CRF input's lock falls at the unbind, counting one MEDIA_UNLOCKED (#653);
  - a followed AAF input's meter lock still falls at its own 100 ms timeout.
  - Rules 2 to 4 are then checked to still read true for both sources. Dated bench records are left as recorded.
- **Verification:** reread the section at the corrected head against `KL_crf_rx.sv` and `KL_aaf_clock_meter.sv`; the docs gates pass.

### R471-F2: MINOR, Docs

- **Where:** `CHANGELOG.md:50`, "The UNBIND_RX response still leaves before the counters push."
- **Authority/evidence:**
  - The order is shown only in simulation (the `[UNB]` trace).
  - #653's hardware report of the opposite order remains open for a capture at the DUT's port (ruling issuecomment-5980290102). That is why the PR says "Relates to #653".
  - The PR body and the bench README qualify the claim as simulation. The release-facing changelog states it as a device fact.
- **Impact:** a release reader is told that #653's acceptance 1 holds on the device when it has not been shown there. This is a conformance claim, so under the owner rule it is not RESIDUE.
- **Required outcome:** the changelog line states that the order is shown in simulation, and that the hardware order reported in #653 awaits the bench capture. For example: "In simulation the UNBIND_RX response still leaves before the counters push; the hardware order in #653 awaits a bench capture."
- **Verification:** read the line at the corrected head; the docs gates pass.

### R471-F3: RESIDUE, Docs

- **Where:** `docs/design/MEDIA_CLOCK_FOLLOWING.md:964` and `:1499`.
- **Evidence:** this PR shifts `KL_crf_rx.sv` by 5 and then 7 lines. Commit `77ea6cb4` says it updates the design page's KL_crf_rx line pointers, and it updated `:298` and `:759`. It missed two citations of the same lines:
  - `:964` "`KL_crf_rx`'s rules (`:390-403`)", the rate-history restart rules at dev;
  - `:1499` "restarts on any sequence gap (`:398-400`)".
  - At head those lines are `:397-410` and `:405-407`.
- **Exact fix:**
  - `:964`: change `(`:390-403`)` to `(`:397-410`)`;
  - `:1499`: change `(`:398-400`)` to `(`:405-407`)`.
- This is a citation only. It changes no claim, figure, test or code.

### R471-S1: SUGGESTION, Tests

No root-level test grades a followed CRF input's unbind with CRF selected. `tb/verilator/milan_dp_mclk/sim_mclk.cpp` counts `mcr_restart_p_w` but never unbinds, and the gmstep leg does not either. A check would make the newly earlier consumers (item 1) regression-protected: one restart request at the unbind, none at the timeout after it, and HOLDOVER entered. It is optional, because the fall itself and its single edge are pinned at the unit and root counter level.

### R471-S2: SUGGESTION, Tests

`tb/verilator/milan_dp/unb_mutants.py` builds and runs its five mutants serially and has no `--jobs`. A `--jobs N` option, like `tdm8_render_mutants.py --law-boundary`, would cut the campaign's wall time.

### Examined, not findings

- With the bench lever `CRF_CTRL[0]` held, an ACMP unbind does not drop `en_i`, so the unlock waits for the timeout. This is pre-existing, documented in the REGISTER_MAP row ("enable and ACMP bind both low"), and nothing under `sw/` writes `0x738`.
- The response-before-push order rests on structure, not only on margin. The listener queues the response before the debounced bind level can fall, and ACMP holds the top class on the processor's single TX stream (the published STOP analysis). The order mutant shows that the checks catch a reversal.

## Clean-lens results (findings format)

- `[R471] PASS Conformance` (`KL_crf_rx.sv:314,395,538-545,627-631`; `KL_avtp_rx_monitor_ctx.sv:607-611,857`; notify leg at 77ea6cb4): checked against Milan v1.2 5.3.8.10 Table 5.6 and ruling items 1 to 4.
  - Pair 1/1 as the response leaves, 1/1/0 right after it and past both timeouts, STREAM_INTERRUPTED 0.
  - The response precedes every unlock push on AAF 0 and CRF 1.
  - Ruling item 4 is verified against both blobs.
  - The hardware order stays open as a manager bench item, as the PR states.
- `[R471] PASS RTL` (`KL_crf_rx.sv:393-395,538-545,627-631,641-696`; `milan_datapath.sv:2661,3229-3232,5745-5746`; `KL_mmcm_drp_servo.sv:574`):
  - non-blocking last-writer ordering, the edge reusing `en_q`, 32-bit wrap, one consumer edge per unbind; probe P8 is equivalent;
  - lint gate 90 <= 90 with no KL_crf_rx finding;
  - Yosys OOC 433 to 368 LUT, FF 544 = 544. Vivado reports 373 to 352 LUT, FF 544 = 544.
- `[R471] PASS Robustness` (`tb/verilator/crf_rx/sim_main.cpp` `[UNB-a..e]`, `[5t-g3]`; probes P2, P4, P7, P8): covers
  - an unbind of a settling, unlocked input (no count);
  - the unbind and the timeout on one edge (one count);
  - a stopped input still holding its lock (one count);
  - the talker streaming, gaps included, to the unbound input (no STREAM_INTERRUPTED);
  - the rebind wipe;
  - a bound silence (still unlocks);
  - a repeated unbind (no edge, no count).
- `[R471] PASS Tests` (`tb/verilator/crf_rx`, `tb/verilator/milan_dp` notify and `unb_mutants.py`, `scripts/crf_probes.py`):
  - crf_rx 16567/0 (unit 14287, discontinuity 2201, talker_step 69, mutants 10);
  - notify 421/0; unb-mutants 6/6 with the named breaks and holds;
  - my seven fault probes were all caught and the equivalence probe passed;
  - `[5t-g3]` is tightened, not weakened (P1 fails it).
- `[R471] UNCLEAN Docs`: R471-F1 and R471-F2 are open, and R471-F3 is RESIDUE. Examined:
  - `CHANGELOG.md:11,41-58`;
  - `docs/design/MEDIA_CLOCK_FOLLOWING.md`: every `KL_crf_rx` pointer, plus `:297`, `:964`, `:994-996`, `:1057-1060` and `:1499`;
  - `docs/reference/REGISTER_MAP.md:188`, `:851`;
  - `docs/testing/TESTING.md:273`, `:311-313`;
  - the `[UNB]` section of `tb/verilator/milan_dp/README.md`, whose figures I reproduced;
  - `scripts/measure_test_evidence.py:669-673`;
  - `hdl/milan/milan_datapath.sv:3174-3176`;
  - the PR body.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_crf_rx.sv:314,395,538-545,627-631`; `KL_avtp_rx_monitor_ctx.sv:607-611,857`; notify leg 421/0 with U1 to U4 on AAF 0 and CRF 1; ruling items 1 to 4; PR body pointers against both blobs | R471-1 | 77ea6cb46cc3f746a14fa717c5e49a4485fb071e |
| RTL | CLEAN | `KL_crf_rx.sv:393-395,538-545,627-631,641-696`; `milan_datapath.sv:2661,3229-3232,5745-5746`; `KL_mmcm_drp_servo.sv:574`; lint gate; Yosys OOC at dev and head; Vivado reports (inspected, not rerun) | R471-1 | 77ea6cb46cc3f746a14fa717c5e49a4485fb071e |
| Robustness | CLEAN | `tb/verilator/crf_rx/sim_main.cpp` `[UNB-a..e]`, `[5t-g3]`; probes P2, P4, P7, P8 | R471-1 | 77ea6cb46cc3f746a14fa717c5e49a4485fb071e |
| Tests | CLEAN | crf_rx 16567/0; notify 421/0; `unb_mutants.py` 6/6 (4, 2, 2, 2, 2 of 421); `crf_probes.py` 7 caught + 1 equivalent; `[5t-g3]` re-pin | R471-1 | 77ea6cb46cc3f746a14fa717c5e49a4485fb071e |
| Docs | UNCLEAN (F1, F2 MINOR open; F3 RESIDUE) | `CHANGELOG.md`; `MEDIA_CLOCK_FOLLOWING.md`; `REGISTER_MAP.md`; `TESTING.md`; `milan_dp/README.md`; `measure_test_evidence.py`; PR body | R471-1 | 77ea6cb46cc3f746a14fa717c5e49a4485fb071e |

Coverage note: F1 and F2 are documentation-only. A correction confined to `docs/design/MEDIA_CLOCK_FOLLOWING.md` and `CHANGELOG.md` touches no artifact in the four clean lenses' scope. The re-review states whether they still bank at the corrected head.

## Real limits

- Vivado is not available on this host. The Vivado area is read from the published reports, not reproduced. The Yosys area is reproduced.
- I did not run the full parent, processor, gPTP, Yosys (`run.sh`) or builder banks, the docs-workflow gates, behave, xvlog, act, or the candidate merge. The manager's published static, builder and native banks are the source evidence for those.
- Of the suites that build `KL_crf_rx`, I reran crf_rx, the milan_dp notify leg with unb-mutants, milan_dp_gptp and milan_dp_render tdm8render-mutants. I did not rerun the default milan_dp sweep (11877), aaf_clock_meter, milan_dp_mclk, pp_shadow or capture_coherence. Hosted `verilator-suites` is green at this head.
- The followed-CRF consumer effect (item 1) is judged from the RTL. No simulation of a followed CRF unbind with CRF selected exists, and I wrote none (S1).
- The milan_dp_gptp bracket rests on hosted nightly logs and artifacts. The render bracket stops at `241f9184`. Neither is bisected to a single commit.
- Simulation only: physical calibration NOT RUN. No bench capture, and no hardware proof of the wire order.
- One early crf_rx run shared a log with a duplicate launch and was stopped. Its log, `receipts/head_crf.log`, is not listed and is not evidence. The clean rerun is `receipts/crf_rx_head.log`.
- The pinned simulator's install path is redacted to `<pinned-5.050-root>` in published receipts. Each build's report line prints its identity: "Verilator 5.050 2026-07-01 rev v5.050".

## Pending manager duties

- Carry R471-F3 (RESIDUE) to the residue checklist with its exact fix.
- After F1 and F2 are corrected, schedule a re-review at the new head.
- Live `dev` moved from `fea346e7` to `6c22d3ca` during this round (PR #650: `syn/resmap/*`, `docs/findings/649_*`, `docs/findings/README.md`; no file overlaps this PR). The candidate merge must be built and validated against the live tip.
- File Issues for the two dev defects:
  - milan_dp_gptp: 3 audio sample-order failures in the PR #634 bracket, hosted nightly at `241f9184`;
  - tdm8render-mutants: 28/32, four T30 CRF recentre failures in the clean `--epoch-only` leg, already at `241f9184`.
- The #653 bench capture at the DUT's port and acceptance 4 (20 controller connect/disconnect cycles).
- Hosted and act acceptance at the exact head. At the time of `receipts/hosted_checks_at_head.txt`, every executed hosted job had succeeded and "Physical gPTP (nightly and manual)" was skipped.

## Receipts

Every receipt is listed in `MANIFEST.sha256`:

- `receipts/runs_summary.txt`: every run's tally and rc.
- Raw logs in `receipts/`.
- `receipts/nightly_bracket.txt`.
- `receipts/hosted_checks_at_head.txt`.
- `receipts/clone_integrity.txt`: the review clone is unmodified. HEAD and tree are exact, the index sha256 is equal before and after, the status is clean including ignored files, the four gitlinks are at their pinned values, and the submodule worktrees are clean.
- Portable scripts:
  - `scripts/mk_tree.sh`: disposable shared clones at a revision;
  - `scripts/run_bg.sh` and `scripts/wait_rc.sh`;
  - `scripts/crf_probes.py`: the seven fault probes and one equivalence probe;
  - `scripts/cmp_sim_output.py`.

R471-1 FINISHED
