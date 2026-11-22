[R883] NEGATIVE - exact head 8167b70d89d2a913a07c3b1187f4f2469109eebc

# R883-2: internal review of PR #966 (issue #884), round 3 delta

- **Head:** `8167b70d89d2a913a07c3b1187f4f2469109eebc`, tree `66ceef5f516a9804f09a06bb8d02339730cbb02a`.
- **Delta reviewed:** `f15b3a7d..8167b70d`, 9 commits, 27 files.
- **Earlier context:** the PR diff `59b09884..8167b70d`.
- **Method:** I did my own pass over the delta before reading the earlier public findings (R884-1 issuecomment-7074604747, R883-1 issuecomment-7075220700). I then re-checked each of those findings at its cause, using that reviewer's own probe.
- **Lenses:** all five were applied: Conformance, RTL, Robustness, Tests, Docs.
- **Why NEGATIVE:** two MAJOR findings are open.
  - **F1** is R883-1-F1, retained in part. A PHC step of a few hundred µs still takes the grandmaster's port out of asCapable for 2 to 4 s at a 10 ms turnaround.
  - **F2** is new. Two hosted end-station builder assertions fail at this exact head, and the PR causes both.
- Every other earlier finding is resolved at its cause.

## Findings

### R883-2-F1: MAJOR. Lenses: Conformance, Robustness, Tests, Docs. A slave step inside the rate envelope's span still drops the far port's asCapable (R883-1-F1, retained in part)

**Where**
- `sw/firmware/ctrl/gptp/gptp.c:397`: the envelope `mag > (s4 >> GPTP_NRR_ENVELOPE_SHIFT)` (244 ppm of the window's span) is the only guard against a step of the responder's clock between exchanges.
- `gptp.c:434`: the turnaround bound only catches a step that falls inside one exchange's t2..t3.
- `gptp.c:523`: `pd_own_step` repairs only the stepping port's own side.
- `sw/firmware/ctrl/test/test_gptp.cpp:1107-1132`: the step matrix only uses steps of 100 ms, 1 s and TAI scale. All of these are far outside the envelope.
- `docs/design/GPTP_SOFTWARE.md:117` claims "a step on either side of the link never reaches a delay or a rate and asCapable holds across it".
- The PR body says "Each finding is fixed at its cause".

**Authority**
- IEEE 802.1AS-2020 11.2.19.3.3 and 11.2.19.3.4 (neighborRateRatio and neighborPropDelay over a LocalClock that is never stepped).
- 11.2.2 and 10.2.5.1 (asCapable).
- Milan v1.2 4.2.6.1.1 (800 ns neighborPropDelayThresh).
- 802.1AS-2011 B.2.3 (a 10 ms turnaround is allowed; the suite's own matrix uses it).
- R883-1-F1's required outcome: "asCapable stays up across a step on either side of the link". Its impact text names "a locked step over 100 µs".

**Mechanism**
- The port steps at 20 µs at link-up and at 100 µs when locked (`gptp.h:83-84`).
- The window spans about 2 to 3 s of exchanges, so the envelope only rejects a peer step larger than about 0.5 to 0.7 ms.
- A step between the two passes as a rate of up to about 240 ppm. The delay error is rtt × ratio error / 2, which is about 1 µs at a 10 ms turnaround.
- That error crosses the 800 ns threshold (`gptp.c:455`) for 2 to 4 s. The grandmaster then stops Sync, and the slave leaves its grandmaster.

**Evidence** (reviewer probes on the suite's own `Net` fixture, at this head; `scripts/run_probes.sh`)
- **The suite's own `step_across_the_link`** (`receipts/probe_matrix_ext-head.log`):
  - B behind A by 300 µs or by 400 µs at a 10 ms turnaround, and B ahead by 400 µs at 10 ms, each fail "the grandmaster's port fell from asCapable across the slave's step" (down_ms 4000).
  - Each also fails "the slave left its grandmaster after it first followed it" (367 ticks).
  - B ahead by 475 µs at 5 ms fails the same way (3000 ms).
  - 150 µs at 10 ms passes. The suite's five own cases pass.
- **R883-1's own outage table, adapted only for the fixture's `turn_ns`** (`receipts/r883-1-outage-and-step-probes-head.log`):
  - Its six original rows now read 0 ms on both ports, so the fix holds for those rows.
  - Rows added at 300 µs and 400 µs (both directions, 10 ms turnaround) reproduce the original defect's signature exactly: "A 4000 ms, B 0 ms; role changes A 3 B 4; B grandmaster changes 4".
  - The 300 µs row at a 1 ms turnaround is clean.
- **A sweep of initial offsets ±25 to ±600 µs at 1, 5 and 10 ms turnarounds** (`receipts/probe_midstep_sweep-head.log`):
  - At 10 ms, the grandmaster's port is out of asCapable for 2,000 to 4,000 ms with B 225 to 425 µs behind A, and for 3,000 to 4,000 ms with B 275 to 525 µs ahead.
  - At 5 ms, it is out for 3,000 ms at 475 µs ahead.
  - At 1 ms, there is no outage.
  - In every failing row the slave's verdict drops for 260 ms, against the 130 ms baseline.
- The suite under UBSan with these probes reports 0 runtime errors (`receipts/test_gptp-ubsan-head-with-probes.log`). The remaining defect is the rate, not overflow.

**Impact**
- The probes reproduce the outage R883-1-F1 described for a step whose size a deployment does not choose, at the turnaround the suite itself qualifies:
  - the grandmaster stops Sync and Announce for 2 to 4 s;
  - the slave changes grandmaster four times;
  - `gptp_grandmaster_id`, the verdict and the discontinuity count each flip.
- A step of a few hundred µs at link-up or after a grandmaster change is one of these.
- The design page and the PR state that the defect is gone.

**Required outcome**
- No exchange whose times straddle either port's step reaches neighborRateRatio or neighborPropDelay, whatever the step's size above the step thresholds.
- asCapable holds across such a step at turnarounds up to 10 ms.
- One way, not prescribed: stamp Pdelay on a stepless LocalClock, for example the PHC less this port's accumulated steps, as 11.2.19.3.3 assumes.
- The step matrix includes steps between the locked threshold and the envelope's span, in both directions, each with a planted defect it kills.
- The page and PR claims match what is proven.

**Verification**
- `scripts/run_probes.sh` passes every probe row: 0 ms out of asCapable and no grandmaster change.
- The extended matrix is in the suite, and its plants are killed under `gptp_mutants.py`.

### R883-2-F2: MAJOR. Lenses: Tests, RTL, Docs. Two hosted end-station builder assertions fail at this head, and the PR causes both

**Where**
- `sw/builder/test_builder.py:11329` pins `"gptp_adj_w": 4` in the datapath PHC nets' sole-driver reference census.
  - `hdl/milan/milan_datapath.sv:9364` adds a fifth live reference, `assign gptp_adj_w = '0;` in the software arm.
- `sw/builder/test_builder.py:18095`, gate 1c ("fabric ownership is the product default and only config value"), asserts that `'self._gptp_owner = "software"'` is absent from the SoC source.
  - `sw/litex/milan_soc.py:3701` adds that line.
- Both lines come from `4cd82cdf`, which is in this PR before the reviewed delta.
- No public ruling, handoff or PR text mentions either gate.

**Evidence**
- Exact-head hosted jobs (`receipts/hosted-builder-assertions-8167b70d.txt`, `receipts/hosted-failed-steps-8167b70d.txt`):
  - `elaborate-gates-0`, "Elaboration gates, leg 0 of 2": `AssertionError: datapath PHC nets must retain sole-driver reference ownership: gptp_adj_w must have exactly 4 live references, found 5`.
  - `docs-gates-1`, "End-station builder gates, leg 0 of 2": the same assertion.
  - `docs-gates-2`, "End-station builder gates, leg 1 of 2": the assertion at `test_gptp_product_default_and_legacy_option`, `test_builder.py:18095`.
- The `docs-check` and `elaborate` aggregates then fail "Require every gate exactly once".
- `receipts/builder-census-gptp_adj_w.txt`:
  - 4 references and no software-owner line at base `59b09884` and at `4cd82cdf^`;
  - 5 references and the line at `4cd82cdf`, `f15b3a7d` and `8167b70d`.
- The author's gate table lists no builder-gate result.

**Authority**
- AGENTS.md section 6, Tests ("Existing regressions remain green") and RTL ("Existing module/interface contracts remain valid").
- Section 7: hosted evidence on the current head.
- Section 8: never weaken a test solely to obtain a pass.
- #884's ruling of 2026-11-21, item 6, puts `--sw-gptp` on this line. So the gate's contract and the ruling now disagree. That needs a public resolution, not a silent edit.

**Impact**
- A required hosted context is red at the exact head because of the PR.
- The datapath PHC net's pinned driver set has changed, and no gate re-proves it.
- A cold reader of the PR evidence cannot see either failure.

**Required outcome**
- The builder gates pass at the head.
- The census and gate 1c state the contract under the ruling, with a reason. For example: the software arm's tie-off is exclusive with the plane arm; fabric stays the product default; `--sw-gptp` is the opt-in owner on this line.
- This is recorded publicly, not by loosening a count without a reason.
- The PR's gate table names the builder legs.

**Verification**
- `python3 sw/builder/test_builder.py --require-elaboration --require-rv32` (both legs) passes at the new head.
- The hosted `elaborate-gates-*` and `docs-gates-*` builder legs succeed on it.

### Residue (wording only; does not affect the verdict)

- **R883-2-R1** `tb/verilator/mbx/tb_cdc_pub.sv:18`: a source comment names a reviewed head ("the ordering that tore at f15b3a7d").
  - Exact fix: "(the ordering that tears a crossing of the live words)".
- **R883-2-R2** `tb/verilator/mbx/cdc_pub_mutants.py:48`: a source comment names a review ("the defect #966's first review found:").
  - Exact fix: "the defect REQ-PTP-07 forbids:".

### Suggestions (optional; no lens)

- **S1** `gptp.c:734`: `tlv_ok ? (int32_t)get32(tlv + 10) >> 9 : 0` comes after the early return on `!tlv_ok`, so the ternary is dead. `(int32_t)get32(tlv + 10) >> 9` alone says the same.
- **S2** `tb/verilator/mbx/README.md:53` and `:58`: the durable README names a head and "#966's review". Stating the ordering itself would age better.
- **S3** `receipts/gates-8167b70d/xvlog-8167b70d.log`: it records the slot and time but not the head it analysed. Printing `git rev-parse HEAD` in the receipt would bind it. The verdict is unaffected, because `hdl/` is byte-identical from `09c5934a` to `8167b70d`.
- **S4** `tb_cdc_pub.sv`: a random phase offset between the two clocks, and a reset of the datapath clock alone, would widen the bench. The RTL reasoning below holds without them.

## Earlier findings: resolved or retained at this head

| Finding | State | Evidence at this head |
|---|---|---|
| R884-1-F1 publication tear | **Resolved** | See note 1 |
| R884-1-F2 Sync alone renews the deadline | **Resolved** | See note 2 |
| R884-1-F3 late second responder | **Resolved** | See note 3 |
| R884-1-F4 Follow_Up without TLV | **Resolved** | See note 4 |
| R884-1-F5 xvlog skip shown as PASS | **Resolved** | See note 5 |
| R883-1-F1 PHC step corrupts the rate | **Retained in part, as R883-2-F1** | See note 6 |
| R883-1-F2 split-sw in no gate | **Resolved** | `make -C tb/verilator/milan_dp ci-list` ends with `split-sw` (`receipts/milan_dp-ci-list-head.txt`); `TAIL_CASES` is in `RUN_CASES` and in `run` |
| R883-1-F3 stale routes on the design page | **Resolved** | See note 7 |
| R883-1-F4 three-call HAL | **Resolved** | `GPTP_SOFTWARE.md` and the PR body say three calls; `gptp.h` `struct gptp_hal` has three |
| R883-1-S1 null to memcmp/memcpy | Taken | `gptp.c:185-191`; the `null-path-compared` plant is killed under UBSan |
| R883-1-S2 to S5 | Not taken (optional) | No lens |

**Notes to the table**

1. **R884-1-F1.**
   - **RTL at the cause.** `KL_mbx_cdc.sv:476-516`: the bank is captured from `m_pub_gptp_i` on a GEN change and sent from `gptp_bank_r`.
   - **Latch edge.** `gptp_latch_w` mirrors `cdc_handshake`'s own `src_send && !src_send_d` latch edge (`cdc_handshake.sv`), so a commit on that edge stays dirty.
   - **Ordering.** A commit made in flight is sent next; an overtaken commit is not sent.
   - **My runs with the pinned Verilator 5.050:**
     - `run-cdc-pub`: 53 checks, 0 failures (`receipts/run-cdc-pub-head.log`);
     - the same bench on `f15b3a7d`'s crossing: 12 failures, the reviewed ordering among them (`receipts/tb_cdc_pub-on-base-crossing.log`);
     - `cdc_pub_mutants.py`: 5 of 5 caught (`receipts/cdc_pub_mutants-head.log`);
     - R884-1's `probe_publication.sv`: count 2, torn 0, in both the control and the overlapping case (`receipts/r884-1-probe_publication*-head.log`).
   - **Host model.** `mbx_model.c:1409` snapshots at the GEN-moving write, which is the bank's content. `MbxModelGptp.TheSnapshotIsTheLastCommitWhole` holds it to that.
   - **Integration.** The author's `split-sw` receipts show 152/0 on the new crossing and the old crossing's `0x2222222233333333`.
   - **Route.** The author's 8x8/1if `--sw-gptp` routes at `9d753fa0` meet #818's floor on all three directives (ExtraTimingOpt WNS +0.220, WHS +0.056). `hdl/` is unchanged from `9d753fa0` to head except the generated README-tests files.
2. **R884-1-F2.**
   - `gptp.c:619`: the deadline is renewed only when a pair is consumed.
   - `gptp.c:703`: a Sync alone renews nothing.
   - The followUpReceiptTimeout discards the pending Sync (`gptp.c:1000`).
   - R884-1's `probe_protocol.c` reports 0 failed assertions (`receipts/r884-1-probe_protocol-head.log`), for both priority1 248 and priority1 255.
3. **R884-1-F3.**
   - `pd_multi` (`gptp.c:313`) counts each request once, for a second clock identity (8-octet compare), before or after the first Follow_Up.
   - `pd_send` (`gptp.c:334`) ends the run on a request answered by one clock or by none.
   - The probe shows multi_run 1, 2, 3 and ceased by the third request.
4. **R884-1-F4.**
   - `fu_tlv_ok` checks plen >= 76, type 3, length 28, 00-80-C2, subtype 1 before any use.
   - `gptp_port_rx` bounds plen to the frame.
   - The probe shows used=0 and sync_ok=0.
5. **R884-1-F5.**
   - The author's `gates-8167b70d/SUMMARY.txt` keeps xvlog at rc 124.
   - The author's re-run at head shows 90 + 52 files and 0 findings.
   - The `09c5934a` run passed with the same `hdl/`.
   - The PR body names the timeout and the re-run.
6. **R883-1-F1.**
   - **Fixed:**
     - overflow-free arithmetic (`pd_rate`, `gptp.c:377-409`);
     - the own-step void (`gptp.c:523`);
     - the turnaround bound;
     - every row of R883-1's table, now 0 ms;
     - 15 regression tests fail on `f15b3a7d`'s port (`receipts/test_gptp-head-suite-on-base-port.log`: 37 pass, 15 fail, matching the author's claim).
   - **Not fixed:** steps inside the envelope's span (F1 above).
7. **R883-1-F3.**
   - `GPTP_SOFTWARE.md` names `9d753fa0` and the plane's `40bd7738`.
   - Its figures equal the author's route receipts: 38,183 LUT; ExtraTimingOpt +0.220/+0.056; AltSpreadLogic_high +0.174/+0.056; ExtraPostPlacementOpt +0.154/+0.026.

## Clean results and evidence, per lens

```text
[R883] PASS RTL - hdl/milan/mailbox/KL_mbx_cdc.sv:476-516 vs hdl/common/cdc_handshake.sv source latch - committed bank, latch-edge priority, in-flight and overtaken commits, reset; run-cdc-pub 53/0, base crossing 12 fail, 5/5 plants (receipts/run-cdc-pub-head.log, tb_cdc_pub-on-base-crossing.log, cdc_pub_mutants-head.log). Lens UNCLEAN by F2 only.
[R883] PASS Conformance (sub-items; lens UNCLEAN by F1) - gptp.c:313-339,603-620,700-740,774-805,995-1010 vs 802.1AS-2020 10.2.8.2.1(c), 11.2.14, 11.4.4.1/Table 11-10, 11.4.4.3, Milan v1.2 4.2.6.2.3/4.2.6.2.5 - R884-1 probe_protocol.c 0 failed (receipts/r884-1-probe_protocol-head.log).
[R883] PASS Conformance (sub-items) - sw/mailbox/mailbox.yaml GPTP_STATE doc and its three generated copies - doc-only, no field/offset/channel/version moved; gen_mailbox.py --check --crosscheck 0 findings (receipts/gen_mailbox-check-head.log).
[R883] PASS Robustness (sub-items; lens UNCLEAN by F1) - gptp.c:377-409,434,523-534 - 64-bit spans unsigned, quotient bounded under 2^20, own-step void; UBSan 0 runtime errors over the suite and 5 extra probes (receipts/test_gptp-ubsan-head-with-probes.log).
[R883] PASS Tests (sub-items; lens UNCLEAN by F1, F2) - test_gptp.cpp at head 52/52 (scratch build); gptp_mutants.py 40/40 killed with --jobs 16 (receipts/gptp_mutants-head.log); 15 of 52 fail on f15b3a7d's port (receipts/test_gptp-head-suite-on-base-port.log); split-sw in ci-list.
[R883] PASS Docs (sub-items; lens UNCLEAN by F1, F2) - GPTP_SOFTWARE.md routes, HAL, crossing text vs receipts; MAILBOX_CONTRACT.md regenerated sentence; tb/verilator/mbx/README.md item 6; MODULE_MATRIX regenerated.
```

**Service-budget conditions of round 2b** (author receipts; checked against what changed since)
- Firmware, harness and `hdl/` are unchanged from `64a473be` to head, except `gptp_mutants.py` and the generated README-tests.
- `egress_ledger.py --point 8x8-1if`: PASS. `backlog-owed.service.acmp.last.if0` is 62.411 ms, at or under 62.62.
- Turnaround: 0.223 ms (8x8/1if) and 0.309 ms (8x8/2if), at or under 10 ms.
- Flood: 490 stamped, 0 unstamped, 0 egress lost, lock kept.
- 0 of 5,142 and 0 of 5,197 passes over the share.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | gptp.[ch] delta; mailbox.yaml doc edit and generated copies; 802.1AS-2020 10.2.8.2.1, 11.2.14, 11.2.19.3.3/4, 11.4.4; Milan v1.2 4.2.6.1.1, 4.2.6.2.3, 4.2.6.2.5; R884-1 probe_protocol.c | R883-2 | 8167b70d89d2a913a07c3b1187f4f2469109eebc |
| RTL | UNCLEAN (F2) | KL_mbx_cdc.sv gptp_pub_send; cdc_handshake.sv; milan_datapath.sv:9364 against test_builder.py:11329; milan_soc.py:3701 against test_builder.py:18095; route receipts at 9d753fa0 | R883-2 | 8167b70d89d2a913a07c3b1187f4f2469109eebc |
| Robustness | UNCLEAN (F1) | step and turnaround sweep (144 rows); UBSan over the suite and probes; malformed Follow_Up and multi-responder orderings; crossing reset and GEN wrap | R883-2 | 8167b70d89d2a913a07c3b1187f4f2469109eebc |
| Tests | UNCLEAN (F1, F2) | test_gptp.cpp, gptp_mutants.py (40/40), tb_cdc_pub.sv and cdc_pub_mutants.py (53/0, 5/5), model_suite.cpp, milan_dp Makefile and sim_split.cpp, fw_gtest.py UBSan arm, hosted builder legs | R883-2 | 8167b70d89d2a913a07c3b1187f4f2469109eebc |
| Docs | UNCLEAN (F1, F2) | GPTP_SOFTWARE.md, MAILBOX_CONTRACT.md, mbx README, milan_dp README, DOCUMENTATION_AUDIT.md, MODULE_MATRIX.md, PR body, HANDOFF-r3 | R883-2 | 8167b70d89d2a913a07c3b1187f4f2469109eebc |

## Real limits

- No full parent, PP, gPTP, Yosys or builder bank was run here, by the role's rules.
  - Sweep, firmware-gate, closed-loop, TSU, census, Yosys, harness and route results are the author's published receipts at the heads they name. I checked them against what changed since, and I did not re-execute them.
- I did not re-run `split-sw`. Its receipts are the author's, and `hdl/` and the bench are unchanged since `8121e098`.
- F2's cause comes from the hosted job logs and from textual counts. I did not run `test_builder.py` locally.
- I did not consult the actual standards texts again in this round. The clause readings for the delta follow the earlier rounds' consultation and the code's own citations.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- No manager source bank exists at this head, and none is claimed.

## Pending manager duties

- Hosted and act acceptance at the exact head. At `8167b70d`:
  - `verilator-suites`, `yosys-portability`, `docs-check` and `elaborate` concluded failure;
  - most shards were cancelled by the fail-fast job after the builder failures (`receipts/hosted-check-runs-8167b70d.txt`);
  - "Physical gPTP" was skipped.
- The current-dev merge candidate (base `59b09884`, live dev `e275d795`), with builder and native banks, at the merge turn.
- The residue checklist: R883-2-R1 and R883-2-R2.

## Reproduction

- `scripts/run_probes.sh <clone> <packet>`: the firmware probes. Builds go to `scratch/`, and no tracked file is written.
- `scripts/census_gptp_adj.sh <clone> <revs...>`: the F2 counts.
- `scripts/verify_integrity.sh`: the clone check.
- After all probes, the clone is at exact head and tree. Index stage 0 equals the tree, every tracked blob's bytes and mode equal HEAD's, status is empty, and the six gitlinks are as recorded (`receipts/clone_integrity.txt`).

R883-2 FINISHED
