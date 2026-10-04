[R470] POSITIVE - exact head 77ea6cb46cc3f746a14fa717c5e49a4485fb071e

# R470-1 internal cleared-context review: issue #653 / PR #655

- **Head:** `77ea6cb46cc3f746a14fa717c5e49a4485fb071e`, tree `6aab682e4390fc3f5c5cdb25cea1c8baba1a46ee`, base dev `fea346e76c2a57ed5cd131af8fc68dfeff57f877`. Four commits. Processor pin `631eeb34`, gPTP pin `5dce647a` and verilog-axis pin `48ff7a7e` are unchanged.
- **Scope reconstructed from public state:**
  - AGENTS.md and CONTRIBUTING.md;
  - the #653 body;
  - the lane comment, the executor's STOP and the re-scope ruling (issuecomment-5980290102);
  - the REVIEW READY comment and the PR #655 body;
  - the diff `fea346e7..77ea6cb4` with its history;
  - the public evidence tree `c4b00e84:review-evidence/653-r1`.
- **Lenses applied:** all five (Conformance, RTL, Robustness, Tests, Docs), each with its own artifacts below.
- **Prior public findings:** at the start of this round, PR #655 carried two review-start notices and no review findings. The #653 thread carries no review findings either. Nothing is carried forward to resolve or retain.

## Verdict basis

There is no BLOCKER, MAJOR or MINOR. There is one RESIDUE (a stale line pointer in prose) and one SUGGESTION. All five lenses are covered clean at the exact head.

## Findings

### R470-1-F1 RESIDUE - Docs - `docs/design/MEDIA_CLOCK_FOLLOWING.md:1499` - one KL_crf_rx line pointer was not moved with the rest

- **Authority/evidence:**
  - The last commit re-pointed the design page's `KL_crf_rx.sv` references after the +7 line shift at `:391-392`.
  - The same sequence-gap reference was updated at `:759`, from `(:398-400)` to `(:405-407)`. The second copy, at `:1499` ("Its rate also restarts on any sequence gap (`:398-400`)"), still carries the dev numbers.
  - At the head, `KL_crf_rx.sv:398-400` is the tu/era comment. `rate_break_w` is at `:405-406`.
- **Impact:** a reader following the pointer lands three lines into a comment instead of on the rate-break term. No measurement, figure, verdict, test, code or clause claim changes.
- **Required outcome:** at `docs/design/MEDIA_CLOCK_FOLLOWING.md:1499`, replace `(:398-400)` with `(:405-407)`, matching `:759`.
- **Verification:** `sed -n 405,407p hdl/ieee1722/crf/KL_crf_rx.sv` shows the `rate_break_w` sequence-gap term.

### R470-1-S1 SUGGESTION - Tests, RTL - `hdl/milan/milan_datapath.sv:3229-3232`, `:5745-5746` - no executable check grades the followed-CRF consumers at an unbind

- **Evidence:**
  - `crf_locked_w` now falls at the unbind. When CRF is the selected media clock, this drives two consumers:
    - `mcr_restart_p_w`, the 4.4.4.3 restart request, through `tkd_crflk_q_r & ~crf_locked_w`;
    - `ref_locked_w`, which moves the servo from LOCKED to HOLDOVER (`KL_mmcm_drp_servo.sv:574`).
  - At dev, both events happened at the 100 ms timeout, or at a rebind's wipe if that came first.
  - By reading, the count is unchanged: one restart per unbind of a locked followed input, and none at the later timeout because `locked_o` is already low.
  - The servo's trim effect is also unchanged. At dev, `rate_valid_o` already fell at the unbind (`KL_crf_rx.sv:409-410` includes `en_i`), so PI had no valid sample. HOLDOVER now freezes `u` explicitly, up to 100 ms earlier.
  - The change is documented: `milan_datapath.sv:3174-3176`, `REGISTER_MAP.md:851`, `CHANGELOG.md:41-58` and the PR body.
  - No check pins the new unbind-time behaviour of these two consumers. The existing silence-path mr checks still pass (manager native banks).
- **Impact:** none observed. A later change could double the restart at unbind plus timeout, and no check would catch it.
- **Suggested outcome (optional):** a check, with the CRF source selected, that an unbind of the locked followed CRF input requests exactly one restart at the unbind and none at the timeout after it.

## The judgments requested

1. **CRF fix (`hdl/ieee1722/crf/KL_crf_rx.sv:394-395`, `:627-631`)**
   - **Bind fall while locked.** `w_bind_fall_w = !en_i && en_q` reuses the existing `en_q`, so no flop is added. While locked, the arm drops `locked_o`, adds one to `cnt_unlocked_o` and pulses `dirty_p_o`. This is the AAF rule at `KL_avtp_rx_monitor_ctx.sv:857`.
   - **Same edge as the timeout.** The timeout arm (`:540-545`) writes the identical `cnt_unlocked_o + 1`, so the event counts once.
   - **Silence path.** A bound input that goes silent still unlocks through `:540-545`. After an unbind the timeout finds `locked_o` low and counts nothing.
   - **No accept on the fall cycle.** `w_hit` (`:314`) is gated by `en_i`, so no accept or lock rise can land on the fall cycle.
   - **Last writer.** The bind-rise wipe (`:641-696`) stays the last writer. A one-cycle low pulse on `en_i` therefore ends at 0/0, which is consistent.
   - **STREAM_INTERRUPTED.** It cannot move, because `en_i` low accepts no PDU.
   - **CSR lever.** `en_i = cfg_crf_en | acmpl1_bound` (`milan_datapath.sv:5625`), so an unbind with the CSR lever held is not a fall. `REGISTER_MAP.md:851` states this ("enable and ACMP bind both low").
   - **Consumers of the earlier fall.** These are `CRF_CTRL[31]` (`i_crf_locked`, `milan_datapath.sv:2661`), the restart request and the servo lock input. The change is intended and documented. Its effect on the followed-CRF clock path is analysed in S1: the same events, at most 100 ms earlier, with an unchanged count.
2. **Tests**
   - **The [UNB] section.** It is at `tb/verilator/milan_dp/sim_nxn.cpp:2293-2630` and runs in the timed `obj_notify` leg.
     - It grades the order on the MAC TX trunk for AAF 0 and CRF 1 (U2).
     - It grades the pair as the response's handshake edge completes: the TX capture precedes `hi()`, and `unb_watch()` samples right after it.
     - It grades GET_COUNTERS right after the response and every later push (U3), and the pair past both timeouts with the talker still streaming (U4).
     - Reproduced: 421/0, with trace lines identical to the PR table (CRF MEDIA_UNLOCKED +200, response +277, pushes +2294 / +3057).
   - **The campaign.** `make unb-mutants` reproduced 6/6. The tallies are 4, 2, 2, 2 and 2 failures of 421, each with the named breaks failing and the named holds passing.
   - **Reviewer probes.**
     - Seven CRF defects planted in copies against the unit harness were all caught: the arm removed, an unlocked unbind counted, the lock kept, no dirty pulse, STREAM_INTERRUPTED counted, a same-edge double count, and MEDIA_LOCKED moved.
     - The AAF bind-fall unlock removed in a copy is caught by the AAF U3 checks (2 of 421). The AAF half of the invariant is graded too, not only the order.
   - **`[5t-g3]`.** The re-pin is the behaviour change, not a weakening. It still asserts every one of the ten totals, with MEDIA_UNLOCKED at exactly +1. The new `[5t-g3b]` asserts LOCKED = UNLOCKED. With the dev arm (probe p1), both fail together with `[UNB-a1..a5]`, `[UNB-b2]` and `[UNB-e1]`.
3. **Area**
   - **Yosys `ooc.sh KL_crf_rx` (AX 1x1 TDM8 shape), reproduced here:** dev 433 LUT / 544 FF / 1 RAMB18, head 368 LUT / 544 FF / 1 RAMB18. FF are unchanged and the result is under the 30 LUT / 60 FF bound.
   - **Vivado OOC 373 -> 352 LUT, 544 FF:** not re-run, because no Vivado is available to this review. The published reports (`vivado-util-KL_crf_rx-{dev,head}.rpt`, xc7a100tfgg484-2, generics `CLK_FREQ_HZ_P = IVAL_CYC_P = 100000000` = the datapath binding at `milan_datapath.sv:67`, `:245`) state those figures. They do not record the source digest.
4. **Stale pointer**
   - The PR body's correction is accurate. At dev, `:597-605` is the rate-ring update, `:533-536` is the silence-timeout unlock and `:619-670` is the bind-rise wipe. At the head, these are `:540-545`, `:641-696` and the new arm at `:627-631`.
   - The #653 body itself still cites `:597-605`. The ruling assigned the correction to the PR body, and it is there.
5. **The two gates reported failing at dev are real dev defects, not tool-version artifacts, and this lane does not cause them.** The pinned Verilator was verified as `Verilator 5.050 2026-07-01 rev v5.050`. The host default is 5.052.
   - **`milan_dp_gptp` (physical):**
     - Head with 5.050, dev with 5.050 and dev with 5.052 each end rc 2 at 139 checks / 3 failures. Two are "audio sample order, no duplicates or gaps" (got 2) and one is "all monitored audio sample ordering errors" (got 5).
     - The 224 simulation-output lines are byte-identical across all three (sha256 `0d4c1b12...`).
     - The hosted nightly with 5.050 on dev `241f9184`, an ancestor of `fea346e7`, reports the same 139 / 3 (run 37184411090).
     - The three earlier nightlies (`e4b771f9`, `cdf49d1a`, `1269cdaf`) timed out at 139 / 0. So the failure first shows in `1269cdaf..241f9184`, which changes `milan_datapath.sv` and `milan_dp` sources.
   - **`milan_dp_render` `make tdm8render-mutants`:**
     - Head with 5.050, dev with 5.050 and dev with 5.052 each give rc 2 and 28/32, with the same four FAIL lines: the clean ship leg in `--epoch-only`, its two arrival-skew clean controls, and the surviving "uncounted repeat" mutant.
     - The clean `--epoch-only` leg run directly gives 114 checks / 4 failures in all three: the four T30 CRF recentre checks. Its stdout is byte-identical across all three (sha256 `8f6ebaae...`).
   - Both need their own Issue (manager duty).

## Lens coverage, one line per clean lens

```text
[R470] PASS Conformance — hdl/ieee1722/crf/KL_crf_rx.sv:394-395,:627-631,:540-545,:641-696 at 77ea6cb4; receipts/head-notify.log [UNB] U1-U4 — the unbind of a locked CRF input scores one MEDIA_UNLOCKED at the bind fall, so Table 5.6 (Milan v1.2 5.3.8.10) reads LOCKED = UNLOCKED as the UNBIND_RX response leaves (1/1) and after it, STREAM_INTERRUPTED 0 at the response and past both timeouts; the response precedes every unlock push on AAF and CRF (+277 vs +2294/+3057); ruling items 1-4 met, PR says "Relates to #653" as ruled
[R470] PASS RTL — hdl/ieee1722/crf/KL_crf_rx.sv:314,:394-395,:530-545,:627-631,:641-696; hdl/milan/milan_datapath.sv:2661,:3189-3232,:5596-5653,:5745-5746; hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:554-590 — single-clock edge detect on the existing en_q, no new flop, no port/parameter/register change; last-writer order against the timeout and the bind-rise wipe; w_hit gated by en_i; consumer effects analysed (S1); Yosys OOC 433->368 LUT, 544 FF unchanged (receipts/{dev,head}-ooc-crf_rx.log); lint 90 <= 90 with 5.050 (receipts/head-lint_rtl-5050.log)
[R470] PASS Robustness — tb/verilator/crf_rx/sim_main.cpp:1476-1601 [UNB-a..e] and receipts/probe-crf-unit.log — unbind of locked, unlocked and stopped-locked inputs, unbind on the timeout's own edge, a talker streaming with gaps into the unbound input, silence while bound; reset clears en_q so no spurious fall; a one-cycle en_i low pulse ends 0/0 via the rise wipe; seven planted CRF defects (p1-p7) each caught by the unit harness
[R470] PASS Tests — tb/verilator/milan_dp/sim_nxn.cpp:2293-2630, tb/verilator/milan_dp/unb_mutants.py, tb/verilator/crf_rx/sim_main.cpp:1036-1070 — notify 421/0, unb-mutants 6/6 with tallies 4/2/2/2/2 of 421 (receipts/head-unb-mutants.log), crf_rx suite 14287+2201+69+10 = 16567/0 (receipts/head-crf_rx.log), the reviewer AAF probe caught by the AAF U3 checks (receipts/probe-aaf-unbind-notify.log); [5t-g3] re-pin fails against the dev arm (p1), so it is the behaviour change, not a weakening; test-evidence ratchet PASS and selftest 101/101
[R470] PASS Docs — CHANGELOG.md:11,:41-58; docs/reference/REGISTER_MAP.md:188,:851; docs/design/MEDIA_CLOCK_FOLLOWING.md:295-299,:494,:516,:531,:632,:759,:973-997,:1496-1499; docs/testing/TESTING.md:273,:311-313; tb/verilator/milan_dp/README.md:75,:93,:656-715,:1073; hdl/milan/milan_datapath.sv:3174-3176; PR #655 body — each pointer checked against the head bytes; trace and mutant tables match the reproduced runs; docs_check 0 findings, check_doc_style OK; the one stale pointer is RESIDUE F1 (does not un-cover the lens under the 2026-10-02 owner rule)
```

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_crf_rx.sv` unbind, timeout and wipe arms; the [UNB] U1-U4 run; #653 body, ruling 5980290102, Milan v1.2 5.3.8.10 Table 5.6 as quoted in the RTL headers and issue | R470-1 | `77ea6cb46cc3f746a14fa717c5e49a4485fb071e` |
| RTL | CLEAN | `KL_crf_rx.sv:314,394-395,530-545,627-631,641-696`; `milan_datapath.sv:2661,3189-3232,5596-5653,5745-5746`; `KL_mmcm_drp_servo.sv:554-590`; Yosys OOC dev/head; lint (5.050) | R470-1 | `77ea6cb46cc3f746a14fa717c5e49a4485fb071e` |
| Robustness | CLEAN | crf_rx `[UNB-a..e]`; reviewer probes p1-p7; notify U4 with the talker streaming | R470-1 | `77ea6cb46cc3f746a14fa717c5e49a4485fb071e` |
| Tests | CLEAN | `sim_nxn.cpp` [UNB]; `unb_mutants.py` 6/6; crf_rx 16567/0; the AAF probe; `[5t-g3]` and `[5t-g3b]`; `measure_test_evidence.py --check` and `--selftest` | R470-1 | `77ea6cb46cc3f746a14fa717c5e49a4485fb071e` |
| Docs | CLEAN (RESIDUE F1 carried) | CHANGELOG, REGISTER_MAP, MEDIA_CLOCK_FOLLOWING, TESTING, the milan_dp README, the datapath comment, the PR body; `docs_check.py`, `check_doc_style.py` | R470-1 | `77ea6cb46cc3f746a14fa717c5e49a4485fb071e` |

## Executed here (all at the exact head unless marked dev; pinned 5.050 unless marked 5.052)

| Run | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/milan_dp notify` | rc 0, 421 / 0, both trace lines | `receipts/head-notify.log` |
| `make -C tb/verilator/milan_dp unb-mutants` | rc 0, 6 checks: 6 PASS | `receipts/head-unb-mutants.log` |
| `make -C tb/verilator/crf_rx` | rc 0: unit 14287/0, discontinuity 2201/0, talker_step 69/0, mutants 10/0 | `receipts/head-crf_rx.log` |
| reviewer CRF unit probes p1-p7 (copies) | 7 / 7 caught | `receipts/probe-crf-unit.log`, `scripts/crf_unit_probes.py` |
| reviewer AAF bind-fall probe, notify leg (copy) | rc 2, 421 / 2: AAF U3 at and right after the response | `receipts/probe-aaf-unbind-notify.log`, `scripts/aaf_unbind_probe.sh` |
| `syn/yosys/ooc.sh KL_crf_rx`, dev and head | 433 -> 368 LUT, 544 -> 544 FF, 1 RAMB18 | `receipts/{dev,head}-ooc-crf_rx.log` |
| `scripts/lint_rtl.py --check` (5.050 and host) | PASS 90 <= 90 | `receipts/head-lint_rtl-5050.log`, `receipts/head-lint_rtl.log` |
| `docs_check.py`, `check_doc_style.py` | rc 0, 0 findings / OK | `receipts/head-docs_check.log`, `receipts/head-check_doc_style.log` |
| `measure_test_evidence.py --check`, `--selftest` | PASS; 101 / 101 | `receipts/head-measure_test_evidence-*.log` |
| `milan_dp_gptp`: head 5.050, dev 5.050, dev 5.052 | rc 2, 139 / 3 each, identical | `receipts/{head,dev}-gptp-505*.log`, `receipts/dev-vs-head-comparison.txt` |
| `tdm8render-mutants`: head 5.050, dev 5.050, dev 5.052 | rc 2, 28 / 32 each, identical FAIL lines | `receipts/{head,dev}-tdm8r-mutants-505*.log` |
| clean ship leg `--epoch-only`: head, dev, dev 5.052 | rc 1, 114 / 4 each, byte-identical | `receipts/*-r-epoch-only-clean.log` |
| hosted CI at the head (read-only) | rtl-fast, elaborate, docs success; rtl-full Yosys 4/4 and Verilator 4/5 shards success, one shard still running at read time; Physical gPTP skipped (not executed) | `receipts/hosted-ci-at-head.txt` |
| hosted nightly physical gPTP on dev (read-only) | 139 / 3 at `241f9184` with 5.050 | `receipts/hosted-nightly-physical-gptp.txt` |
| clone state after probes | HEAD and tree exact; index == tree (mode, blob, path); 0 untracked or ignored; gitlinks `631eeb34` / `5dce647a` / `48ff7a7e` / `efeb541a` | `receipts/clone-state-final.txt` |

## Real limits

- **Vivado.** The Vivado OOC figure was not re-run (no Vivado here). The Yosys delta was reproduced. The Vivado reports are taken as published.
- **Em-dash gate.** `check_em_dash.py` could not run locally: the pinned Markdown renderer is not installed, and no shared install is allowed. The hosted `docs` workflow at this head completed successfully.
- **Not run:**
  - the full `milan_dp` default sweep and the other touched suites: pp_shadow, milan_dp_render default, milan_dp_mclk, capture_coherence, aaf_clock_meter;
  - the gsi, crflic, gmstep and render-csr campaigns;
  - `syn/yosys/run.sh`, xvlog, behave and the builder bank.

  These are covered by the manager's source banks at this head, per the public evidence.
- **Spec text.** No Milan or IEEE specification text was available locally. Clause readings rest on the quotations in the RTL headers, the issue and the ruling.
- **Not hardware proof.** This is simulation only. No physical calibration or bench capture was run, and field skips are not hardware proof. #653's reported hardware order is unconfirmed either way.
- **Hosted CI.** Read-only, and one `rtl-full` Verilator shard was still in progress when read. The hosted Physical gPTP context was skipped, not executed.

## Pending manager duties

- Carry RESIDUE F1 (`MEDIA_CLOCK_FOLLOWING.md:1499`, `(:398-400)` -> `(:405-407)`) to the residue checklist.
- File Issues for the two dev defects:
  - `milan_dp_gptp`: 139 / 3 audio sample order. It first shows in `1269cdaf..241f9184`.
  - `tdm8render-mutants`: 28 / 32. The four T30 CRF recentre checks fail in the `--epoch-only` clean ship leg, and "uncounted repeat" survives.
- Bench items, which keep #653 open:
  - a capture of one disconnect at the DUT's port, with a reversed-order control;
  - acceptance 4, a 20-connect controller session.
- Hosted and act acceptance at the exact head. That includes the still-running `rtl-full` shard and the exact-head `verilator-suites` and `yosys-portability` contexts.
- Candidate-merge validation against live dev (`fea346e7` at review time), and post-merge containment.
- The second (external) review. Merge authorization stays with the maintainer.

R470-1 FINISHED
