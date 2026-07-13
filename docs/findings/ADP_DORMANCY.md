# ADP advertiser dormancy — silicon incident, forensics & fix (2026-07-13)

## Incident
During post-hwts re-certification of the Milan control plane, the Arty (:02)
vanished from ADP discovery: 35 s of `tcpdump ether proto 0x22f0` on pw0 showed
only the AX7101 (:01), while the same capture minutes after the session wrap-up
had shown both. **gPTP was unaffected the whole time** (pw0 stayed SLAVE at
offset ~6 ns under the Arty's HW-timestamped GM) — so the board, link, MAC and
driver-DMA TX path were all healthy; only the fabric-autonomous ADP TX had
stopped.

## Forensics chain (what ruled what out)
1. CSR readback: `ADP_CTRL=0x1F01` (enabled, valid_time 31), EID intact —
   config untouched.
2. `A_ADP_STATUS` (available_index) **frozen** across a 20 s window (advertise
   period is well inside it) — no ADPDUs being started.
3. AECP 0x648/0x64C read cmd=48/resp=48 and ACMP 0x650 read 5/5 — **balanced**.
   `resp_count` bumps only when the final beat drains through the (zero-buffer,
   combinational) arbiter chain into the MAC, so balanced counters prove no
   control responder was mid-frame and **no adp_tx_arbiter lock was held**.
   That killed the leading theory (mux wedged by a source that dropped tvalid
   mid-frame) — additionally each TX source was audited: advertiser, AECP
   builder, ACMP responder all stream-to-completion; the AECP builder bubbles
   between beats but cannot abandon a frame.
4. Discriminating experiment: `ADP_CTRL` enable toggled 0->1. A locked arbiter
   cannot be released by a CSR pulse — but the advertiser CAME BACK instantly
   (index 0xBC -> 0xC4, :02 back on the wire, periodic cadence resumed). So the
   serialiser was idle and **`available_r` was 0: the entity had silently
   departed** and only the enable-edge (`adp_link_up_p`) could re-arm it.
5. What can clear `available_r`: `link_down_i | shutdown_i`. On the fully-FPGA
   SoC `i_link_up` is **constant 1** (milan_soc.py `i_i_link_up=1`), so
   link_down is structurally impossible. `shutdown_i` = `ADP_CMD[1]` — and
   NOTHING in the software stack writes 0x640 (boot script writes 0x600-0x61C
   once; kl-eth touches MAC/PHC/ring groups only). The dominant CSR write
   stream (ptp4l gettime -> `A_PTP_CMD` 0x520 wdata=0x4) carries bit2, which
   cannot assert the bit1 depart strobe even if misrouted.
6. A reset is excluded (index was 0xBC, not 0); a real link blip is excluded
   (gPTP never faulted, and with i_link_up tied 1 no edge can be generated).

**Verdict: the dormancy is real and reproducible in effect, its trigger is not
retroactively provable.** Remaining candidates: a flop upset of `available_r`
itself, or a one-shot AXI-write anomaly presenting address 0x640+bit1. Neither
left a witness — which is exactly what the fix changes.

## Fix (commit `adp: SILICON BUG - ...`, all sim-gated)
1. **Dormancy self-re-arm** (`adp_advertiser.sv`): an ENABLED entity on a LIVE
   link must never stay silent. New `link_level_i` input (the raw link level,
   distinct from the edge pulses); if `!available_r && enable_i &&
   link_level_i` persists for 2 ticks, the advertiser re-arms and sends
   ENTITY_AVAILABLE (index keeps incrementing monotonically — la_avdecc/Hive
   accept that across a depart/return). Operator silence still has honest
   levers: enable=0 or link down, both gate the re-arm. Heal time ~2 s vs the
   62 s discovery validity — controllers never see the entity expire.
2. **Diagnostic witnesses** (`A_ADP_DIAG` 0x668, RO):
   `[7:0] depart_cnt` (depart events actually taken), `[15:8] rearm_cnt`
   (dormancy self-heals), `[17:16] last depart source {shutdown, link_down}`.
   The next occurrence identifies itself: **rearm_cnt advancing while
   depart_cnt stands still = state upset (no depart event ever fired);
   depart_cnt advancing with src=shutdown = the 0x640 write path is real** and
   the bus needs hunting.
3. **ADP tick divider now tracks `MILAN_CLK_FREQ_HZ`** (was hardcoded 100 M
   cycles): the Arty's 50 MHz datapath ticked every 2 s, stretching the
   re-advertise period to 62 s = EXACTLY the 2*valid_time validity horizon with
   zero margin (an unlucky capture window read as "not advertising"; controllers
   sat at the expiry edge). Both assemblies (milan_datapath + legacy milan_top)
   fixed.

## Gates
- `tb/verilator/adp`: 246 checks PASS — new cases: cmd-depart, dormancy
  self-re-arm (2 ticks -> AVAILABLE + rearm_cnt), periodic resumes after heal,
  re-arm gated by link level (departed-link-down stays silent) and by enable
  (disabled stays silent, re-enable self-heals), DIAG counts/src.
- `tb/verilator/milan_dp`: 43 checks PASS — CSR-level depart witness
  (DEPARTING frame on the MAC + DIAG 0x00020001), dormant-silent, and the
  exact bench recovery (enable toggle) re-advertising without a new depart
  count.
- `tb/verilator/cls`: the randomized classifier reference model was missing
  the 2026-07-13 gPTP fast-path (0x88F7 -> GPTP_CLASS in PCP mode too) — 7.5 %
  of 200 k random frames mismatched; taught + 200024 checks PASS. (Latent gap
  from the fast-path commit, caught by this regression sweep.)
- Yosys portability: 20/20 tops PASS.

## Re-certification context (what this session was doing when it hit)
Both boards run same-day gateware (Arty asl_hwts5, AX eto_hwts_ax2). The AX
re-certified clean on the new stack: `milan_controller.py` 31/31 and la_avdecc
enum-probe **IEEE17221=1 Milan=1 verdict CLEAN, 0 complaints**. The Arty's :02
was mid-certification when the dormancy was caught (its +2 index during the
probes = discover responses that died against the dormant state — see chain
above).

## Bench state / recovery one-liner
Until a board runs post-fix gateware, the manual recovery for a dormant
advertiser is the enable toggle (Arty console):
`devmem 0x90000600 32 0x1F00; devmem 0x90000600 32 0x1F01`
