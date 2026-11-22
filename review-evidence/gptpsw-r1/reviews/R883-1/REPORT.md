[R883] NEGATIVE - exact head f15b3a7d2bf1ba84d14140a4cda8a193d2e6b1c9

# R883-1: internal review of PR #966 (issue #884, #665 F6, optimisation line #872)

- **Head:** `f15b3a7d2bf1ba84d14140a4cda8a193d2e6b1c9`, tree `44de68bf9dfc3534963fc1e11a6a86477c669ff1`.
- **Base:** `59b098841b1e2826aaf7a38b557faa5345f91c82` (33 commits).
- **Role:** internal reviewer, cleared context.
- **Lenses:** all five applied: Conformance, RTL, Robustness, Tests, Docs.
- **Verdict: NEGATIVE.** One MAJOR finding (F1) and two MINOR findings (F2, F3) are open. There is also one RESIDUE (F4) and five SUGGESTIONs.
- **Clean lenses:** RTL only. Conformance, Robustness, Tests and Docs are unclean.
- **Not counted:** bench qualification is owed by ruling and is not a finding. Neither is the 2if egress-ledger question.

Scope was reconstructed from:
- AGENTS.md and CONTRIBUTING.md.
- docs/README.md.
- The issue body.
- The rulings: #884 issuecomment-7067495546 (round 1) and issuecomment-7072401468 (round 2b), and #872's owner decision of 2026-11-21.
- The diff and its history.
- The public evidence tree `dc64b04a` `review-evidence/gptpsw-r1` (author-r1, author-r2, HANDOFF-r2 including round 2b).

**Prior public findings.** Before this pass, PR #966 carried no review findings, only the two review-start notices. The issue thread holds author reports and manager rulings, no review findings. Nothing is retained or resolved from an earlier round.

## Findings

### F1 - MAJOR - Conformance, Robustness, Tests - a PHC step corrupts neighborRateRatio for the next three exchanges, overflowing int64, and drops asCapable for 3 to 4 s on the far side of the link

**Where:**
- `sw/firmware/ctrl/gptp/gptp.c:364-383`: the neighborRateRatio window.
- `gptp.c:378`: `(d3 - d4) * (1ll << 32)`.
- `gptp.c:387`: the delay that uses it.
- `gptp.c:493-503`: the servo's step branch. It resets the servo's own rate memory (`have_prev`, `seeded`) but not the Pdelay window `pd.w3/w4/w_n` or the delay history `pd.d/d_n`.

**Authority:**
- IEEE 802.1AS-2020 11.2.19.3.3 (neighborRateRatio from the responder's and the initiator's elapsed times) and 11.2.19.3.4 (neighborPropDelay from it).
- 11.2.2 asCapable.
- B.1.1: each LocalClock within ±100 ppm, so a valid |neighborRateRatio − 1| is at most about 200 ppm.
- The standard takes the Pdelay timestamps on a LocalClock that is never stepped.
- In this design the PHC is both the stamp clock and the clock the servo steps (`phc_step`). So is a peer's PHC in most implementations.
- Nothing removes a step from the window. Nothing bounds the ratio. The product of a step of more than 2.1 s and 2^32 is signed int64 overflow (C11 6.5p5, undefined).

**Evidence** (reviewer probes, reproducible with `probes/run_probes.sh`; output in `probes/run_probes.out`):
- The unmodified 34-test suite under UBSan reports `gptp.c:378:34: runtime error: signed integer overflow: 999997002853 * 4294967296` in `Net.SlaveLocksToTheGrandmaster`.
- The suite still passes, because its simulated peer answers a Pdelay_Req within about a microsecond. That makes the delay error, rtt × (NRR error)/2, a few hundred ns.
- With the peer's turnaround modelled, the grandmaster port's neighborRateRatio after the slave's first lock step reads −0.49 (TAI-scale offset) or −0.37 (1000 s).
- Its neighborPropDelay then reads −122 µs, −242 µs or −2.43 ms, and it drops asCapable:

| Case (two ports, the suite's `Net` model) | Grandmaster port not asCapable after first rising | Slave port not asCapable | Slave's grandmaster changes in 30 s |
|---|---:|---:|---:|
| TAI-scale grandmaster vs PHC at 0, 0.2 ms turnaround (this port's own measured 0.186 ms) | 4,000 ms | 0 | 4 |
| same, 1 ms turnaround | 4,000 ms | 0 | 4 |
| same, 10 ms turnaround (802.1AS-2011 B.2.3) | 4,000 ms | 0 | 4 |
| 1 s initial offset, 1 ms turnaround | 3,000 ms | 4,000 ms | 5 |
| 100 ms initial offset, 1 ms turnaround | 4,000 ms | 4,000 ms | 5 |
| control: 10 µs initial offset, 1 ms turnaround | 0 | 0 | 2 |

**Impact:**
- As grandmaster, against a real slave peer that steps its clock on first lock, the port stops sending Sync and Announce for 3 to 4 s. The peer's sync times out, and the peer may elect itself.
- As slave, its own step of 0.1 to 2 s causes the same outage on its own port.
- The same happens after every later step: a grandmaster change to a clock seconds apart, or a locked step over 100 µs.
- Each outage flips gptp_grandmaster_id, the clock validity verdict and the discontinuity count, and raises AVB_INFO notices.
- The overflow is undefined behaviour on the RV32IM build too.
- No committed bench can see this:
  - the GoogleTest `Net` peer answers in about 1 µs;
  - the closed loop (`tb/verilator/gptp_sw/sim_main.cpp:510-520`) answers in 20 µs;
  - the closed loop's master-run peers start only 5 and 9 ms off (`:730-731`).

**Required outcome:**
- No exchange whose times straddle the port's own PHC step enters the rate window or the delay history.
- A ratio outside the physically possible envelope restarts the window instead of feeding neighborPropDelay. That covers a peer's step, which the port cannot see.
- The computation is free of signed overflow for any 64-bit timestamp difference.
- asCapable stays up across a step on either side of the link.

**Verification:**
- Host tests in both roles, with a responder turnaround of at least 1 ms and at 10 ms, an initial offset of at least 100 ms and one at TAI scale.
- They require asCapable to stay up and no extra grandmaster change after it first rises.
- Each has a planted defect that the test kills.
- The suite runs clean under `-fsanitize=undefined`.

### F2 - MINOR - Tests - `milan_dp split-sw`, the one check of the product datapath's `--sw-gptp` wiring, is run by no gate

**Where:**
- `tb/verilator/milan_dp/Makefile:764`: `ORDINARY_CASES` has `split`, not `split-sw`, so `run`/`ci-list` and the sweep never build it.
- `Makefile:941-952`: the target exists.
- `.github/workflows/rtl-fast.yml:729`: runs `split-cdc` only.

**Authority:** AGENTS.md section 6, Tests lens: "Real integration wiring is tested where practical"; "Existing regressions remain green".

**Evidence:**
- `split-sw` is the only bench that elaborates `milan_datapath`'s `g_gptp_sw` block. That covers the unit wired to `rx_axis_fabric`, the narrowed `GPTP_STATE` decode onto `gptp_pub_*`, the trailer through the datapath's `KL_ctrl_split`, and the detectors gated off.
- The closed loop instantiates `KL_gptp_tsu` and `KL_ctrl_split` directly (`tb/verilator/gptp_sw/Makefile:14-16`).
- The handoff states it: "`split-sw` is not a default case, so the sweep does not run it; run by hand".
- I ran it at head: 151 checks, 0 failures (`receipts/split_sw.log`).
- The PR's "67 of 67 suites" does not include it.

**Impact:** a later change can break the shipped `--sw-gptp` datapath wiring with every gate green.

**Required outcome:** a required gate runs `split-sw` at every head (a `milan_dp` case or a workflow step), or a recorded ruling says why not.

**Verification:** `make -C tb/verilator/milan_dp ci-list` names it, or a workflow step runs it, and its receipt is in the sweep's.

### F3 - MINOR - Docs - the design page's routed fit and timing are an earlier head's, before the burst change reached the RTL

**Where:** `docs/design/GPTP_SOFTWARE.md:153-154`.

**What the page says:**
- "all three placement directives meet #818's floor ... the best AltSpreadLogic_high at WNS +0.237 ns, WHS +0.023 ns (ExtraTimingOpt +0.152 ns, ExtraPostPlacementOpt +0.098 ns)";
- the plane "at the same head".

**What the receipts say:**
- Those are round 2's routes at `40bd7738`, with burst 16 (`author-r2/receipts/route/`).
- `0bb83b9d` changed the gptp burst in the generated `KL_mbx_pkg.sv` that `KL_mbx_rx` reads. The author re-routed at `62fcd154` (`author-r2/receipts/round2b/route/`):
  - AltSpreadLogic_high WNS +0.230 / WHS +0.015 ns, 38,265 LUT;
  - ExtraPostPlacementOpt +0.205 / +0.013 ns, 38,178 LUT;
  - ExtraTimingOpt was not re-run.
- The PR body states the head's figures. The authoritative design page does not, and it names no head.

**Impact:** a stale timing figure, and a claim (three directives meet the floor) that no route of the head's RTL supports.

**Required outcome:** the page states the routes of the head's RTL with the head they ran at. It claims only the directives routed there, and it names the plane comparison's own head.

**Verification:** the page's figures equal `round2b/route/*.txt`, or a later receipt at the PR head.

### F4 - RESIDUE - Docs - the HAL is three calls, not four

**Where:** `docs/design/GPTP_SOFTWARE.md:129`: "The HAL is four calls: send a frame, adjust the rate, step the time, and the time base." The PR body says "behind a four-call HAL".

**Evidence:** `struct gptp_hal` (`sw/firmware/ctrl/gptp/gptp.h:97-107`) has three calls (`send`, `phc_adjfine`, `phc_step`). Time enters through `gptp_port_tick`, not the HAL.

**Exact fix:**
- Page: "The HAL is three calls: send a frame, adjust the rate and step the time."
- PR body: "behind a three-call HAL".

This is pure wording: no code, figure, test or verdict changes.

### Suggestions (optional; they affect no lens)

- **S1** `sw/firmware/ctrl/gptp/gptp.c:185,189`: `pub_set_path(p, NULL, 0)` passes NULL to `memcmp`/`memcpy` with n 0. UBSan flags it (`receipts/ubsan_suite.log`), and it is undefined in C11 7.24.1. Fix: pass an empty static array, or skip the calls when n is 0.
- **S2** `hdl/milan/milan_datapath.sv:80,9346`: the parameter is documented "exclusive of GPTP_PLANE_EN_P", but only `milan_soc.py:1036` enforces it. With both set, the plane elaborates while `KL_ctrl_split` appends zero-stamp trailers and the AVB_INFO/AS_PATH detectors are off. An elaboration `$error` would hold the contract for any instantiation.
- **S3** `milan_datapath.sv` `g_gptp_sw` (`GW_STATE_C = (32'h28 - 32'h20) / 4`, `gw_state_w[8]`, `[9]`, `[10]`, `[19:16]`) decodes `GPTP_STATE` by literal bit positions. `KL_mbx_cdc` uses the generated `MBX_GPTP_STATE_*_C`. Deriving the decode from the same package would stop a future layout change from leaving the decode behind.
- **S4** `hdl/milan/mailbox/KL_mbx_cdc.sv` `ts_send`: the credit's correctness rests on the free pulse arriving no earlier than `u_ts`'s acknowledge.
  - That holds today: the free toggles at least two sys cycles after the acknowledge toggle, and both cross equal-depth synchronisers.
  - If the free ever led, a take in the same cycle as a late `ts_rcv` would leave `ts_send_r` low with `ts_busy_r` high, and the record path would stall.
  - Gating `d_ts_take_p_o` on `!ts_send_r` as well removes the dependence.
- **S5** `hdl/milan/mailbox/KL_mbx_rx.sv:737-748`: the gptp bucket, 7 × interfaces, is per channel and shared by the interfaces. At two interfaces, a flooding peer on one can take the other's tokens. This is worth weighing with #962. The existing channels share their buckets the same way.

## Clean results and evidence, per lens

```text
[R883] PASS RTL - hdl/ieee8021as/gptp_tsu/KL_gptp_tsu.sv:162-183 vs hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:386-399 - the ingress stamp is the PHC on the first accepted beat less INGRESS_LAT, the plane's point and expression; the event test reads the DA at beat 0 and EtherType 0x88F7, majorSdoId 1 and messageType 0-3 at beat 1 lanes 4-6
[R883] PASS RTL - KL_gptp_tsu.sv:119-131,222-296 - egress TXTS_CORR_NS_C = (45+2+1-1)*8 + 2*20 + 20/2 = 426 ns at GMII; history guard, 200 ppm envelope (same rounding as gptp_addend_of_ppm), delta/abort/generation qualify OK; FIFO full-and-pop writes the slot being read only at the edge after the read
[R883] PASS RTL - hdl/milan/KL_ctrl_split.sv:146-400 with third_party/verilog-axis/rtl/axis_fifo.v:261-300 - the stamp is held at the last beat and committed the next cycle unless status_overflow, which axis_fifo raises only the cycle after a dropped frame's tlast, so the stamp FIFO and the frame FIFO hold the same frames; the room test counts the held stamp; a refused frame is marked bad at beat 1 and counted; trailer MSB first, popped on its last byte
[R883] PASS RTL - hdl/milan/mailbox/KL_mbx_cdc.sv:469-531, KL_mbx_evt.sv:183-290,432-436, hdl/common/cdc_handshake.sv - the publication crosses only on a GEN move (latched one cycle after the GEN write, words final); the TIMESTAMP record is one in flight with its credit returned on KL_mbx's take; uncoalesced, posted after the timer slot; both crossings are approved primitives
[R883] PASS RTL - hdl/milan/milan_datapath.sv g_gptp_sw (diff hunk 9343-9433) vs sw/mailbox/mailbox.yaml:444-458 - AS_CAPABLE bit 8, SYNC_OK 9, SLEW 10, DISC [19:16] decoded onto gptp_pub_flags_w[2]/[3] as clock validity reads them (:2400-2401); parent/pdelay/path tied 0; detectors gated by !GPTP_SW_EN_P (:10332-10333)
[R883] PASS RTL - generated files - gen_mailbox.py --check --crosscheck: 0 findings; --selftest: 0 failed (receipts/gen_check.log, gen_selftest.log); mbx_contract.h base vs head: no define removed or changed but the per-channel tables extended, MBX_N_CH 5->6, minor 4->5 (additive)
[R883] PASS RTL - scripts/lint_rtl.py --check at head with pinned Verilator 5.050: PASS 89 <= 89 (receipts/lint_rtl.log); tb/verilator/gptp_tsu at head: 36 checks 0 failures, tsu_mutants.py 24/24 killed; milan_dp split-sw 151 checks 0 failures
[R883] PASS Conformance (sub-items; lens UNCLEAN by F1) - gptp.c:206-284,561-624,871-899 - BMCA vector order and comparison, stepsRemoved 255 and own-GM discards, path trace TLV bounds and append (10.3.9.23), Announce fields and ptpTimescale; two-step Sync/Follow_Up with csro 2^-41 -> 2^-32 (>>9) and syncReceiptTime pd*(1+csro); responder Pdelay_Resp/FU fields; lost-response rule (5th consecutive lost clears; Figure 11-8 RESET, allowedLostResponses 3); late response 15.006181 ms (docs/reference/STRICTER_READINGS.md:107); cease after 3 multi-answered; Milan intervals and timeouts (gptp.h:69-93)
[R883] PASS Conformance (sub-items) - gptp.c:450-537 - servo: recurrence o(k+2) = (2-gKp-gKi)o(k+1) - (1-gKp)o(k) with a double root at 0.6 gives gKp 0.64, gKi 0.16 (GKP_Q16 41943, GKI_Q16 10486); Kp = 0.64*2^24/ticks in Q16; seeding u = q32*1e9/(clk*256) checked; step thresholds 20/100 us; 200 ppm clamp; #75 slew level
[R883] PASS Conformance (sub-items) - sw/mailbox/mailbox.yaml:1314-1325 - the burst 7 an interface is derived from the seven message kinds (802.1AS-2020 Tables 11-5, 10-8) at most once in 10 ms at Milan Table 4.1 intervals with the 30 % tolerance, not fitted; author receipts round2b/harness: turnaround 0.186/0.266 ms <= 10 ms, composed max 1.638/1.633 ms <= 2.0 ms, egress_ledger 8x8-1if PASS with acmp.last.if0 62.535 <= 62.62 ms; harness inputs unchanged after f828861c (git diff --stat f828861c..f15b3a7d: the design page and gptp_sw/Makefile only)
[R883] PASS Conformance (sub-items) - gptp_mbx.c:59-121, aecp_face.c:205-213,343-348 vs milan_datapath.sv:6864-6875 - GET_AVB_INFO's gPTP fields and GET_AS_PATH answered from the published snapshot; AVB_INFO raised on GM/pdelay/domain/asCapable and AS_PATH on the served path, the fabric detectors' terms; AS_CAPABLE flag bit 0x01
[R883] PASS Robustness (sub-items; lens UNCLEAN by F1) - gptp.c:569-596,747-756, gptp_mbx.c:128-153 - Announce TLV length bounded by plen; plen bounded by the frame; short and foreign records counted; closed-loop flood at head: 977 handed out, 490 received stamped, 0 unstamped, 0 egress records lost, lock 2.9 s (receipts/gptp_sw_flood.log); TSU flood T2: 64 kept with stamps, 16 refused and counted
[R883] PASS Tests (sub-items; lens UNCLEAN by F1, F2) - at head: gptp GoogleTests 34/34 (also under UBSan/ASan); gptp_mutants.py 25/25 killed (receipts/gptp_mut.log); closed loop slave 30, master 13, flood 5 = 48 checks 0 failures; harness self-test 1,017 checks, 298/298 mutants caught (receipts/harness_selftest.log); RV32IM audit of gptp.c: text 11,674 B, undefined only __ashldi3/__ashrdi3/__lshrdi3 and memory functions, no float, libm or multiply/divide helper (probes/rv32_audit.out)
[R883] PASS Docs (sub-items; lens UNCLEAN by F3) - REGISTER_MAP regenerated in the change: gen_register_reference.py --check fresh (receipts/gate_regref.log); docs_check 0 findings, gen_toc --check and --verify-anchors OK, doc paths, doc style, gPTP docs, docs inventory, module matrix fresh (receipts/gate_*.log); FR_NFR NFR-SCOUT-03 states the 10 ms bound and THE SHARE per the ruling; no new comment-rule residue in the source delta (lane, round, reviewer or comment IDs: none added in non-doc files)
```

Checks against the brief that hold, beyond the lines above:
- The plane stays buildable and nothing of it is deleted: `g_gptp_plane` is intact and `milan_soc.py:1036` refuses `--sw-gptp` with the plane.
- One MAC, with #962 as the second.
- Memory debt is ledgered under the loose-BRAM rule (`sw/litex/ctrl_memory.py:269-289`: 59.0, 64.0, 62.0 RAMB36).
- The −3,049 FF saving is from synthesis (author S3 receipt at `0e476c94`; the burst constant does not touch the narrowed hierarchy).
- The census `GPTP_SW_EN_P` shape is stated as owed, per ruling item 3.

## Completion ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | gptp.c/gptp.h against 802.1AS-2020 and Milan v1.2; mailbox.yaml gptp channel and GPTP_* block; gptp_mbx.c; aecp_face.c; author harness receipts | R883-1 | f15b3a7d2bf1ba84d14140a4cda8a193d2e6b1c9 |
| RTL | CLEAN | KL_gptp_tsu.sv, KL_ctrl_split.sv, KL_mbx_cdc.sv, KL_mbx_evt.sv, KL_mbx_rx.sv buckets, milan_datapath.sv g_gptp_sw, generated contract, lint, gptp_tsu and split-sw benches | R883-1 | f15b3a7d2bf1ba84d14140a4cda8a193d2e6b1c9 |
| Robustness | UNCLEAN (F1) | the step and timestamp-discontinuity paths (probes), malformed and short frames, the floods, FIFO-full paths | R883-1 | f15b3a7d2bf1ba84d14140a4cda8a193d2e6b1c9 |
| Tests | UNCLEAN (F1, F2) | test_gptp.cpp, gptp_mutants.py, tb/verilator/gptp_sw, tb/verilator/gptp_tsu, milan_dp split-sw and its gating, harness self-test | R883-1 | f15b3a7d2bf1ba84d14140a4cda8a193d2e6b1c9 |
| Docs | UNCLEAN (F3; F4 RESIDUE) | GPTP_SOFTWARE.md, REGISTER_MAP.md, FR_NFR.md, MAILBOX_CONTRACT.md via the generator, docs gates | R883-1 | f15b3a7d2bf1ba84d14140a4cda8a193d2e6b1c9 |

## Real limits

- **Harness self-test.** `tb/verilator/ctrl_service_budget/run.py --self-test` was re-run at the head in a scratch copy:
  - rc 0, 1,017 PASS lines, 298 of 298 mutants caught, "self-test: 0 failures";
  - `receipts/harness_selftest.log`, CONTROL lines dropped;
  - one earlier attempt was stopped and restarted on a fresh log, and only the restarted run is the receipt.
- **Not run by this round:**
  - the full Verilator sweep;
  - Yosys portability;
  - the firmware gate and its four self-test shards;
  - the publication census;
  - `gptp_sw_mutants.py` (14 plants);
  - the mbx suites;
  - `plat_ledger.py` and `test_ctrl_memory.py`;
  - the 8x8 and 8x8-1if `--with-gptp` harness legs and `egress_ledger.py`;
  - synthesis and route.

  For those this review reads the author's published receipts at the heads they name. No manager source bank ran at this head, and none is claimed.
- **RV32 toolchain.** The RV32IM object audit used a host riscv32 GCC 14 toolchain through `MILAN_RV32_CC`, with the gate's own `SPLIT_RV32_FLAGS`, not necessarily the CI-pinned SDK.
- **Probe model.** F1's probes use the suite's own `Net` model of two ports and two PHCs, with only the responder's turnaround added. They are not the closed loop or hardware.
- **No hardware.** Physical calibration was not run. Field skips are not hardware proof.

## Pending manager duties

- The current-dev merge candidate (live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`) with the builder and native banks at the merge turn.
- Hosted and act acceptance.
- Carrying F4 to the residue checklist.
- The bench qualification owed by #884's ruling item 3.
- The census `GPTP_SW_EN_P` shape owed to the census owner (ruling of 2026-11-22, item 3).
- The 2if egress ledger, owed to its owner.

R883-1 FINISHED
