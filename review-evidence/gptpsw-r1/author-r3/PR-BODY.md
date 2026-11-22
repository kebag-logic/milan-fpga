## gPTP in the split firmware on the optimisation line (#884, #665 F6)

Refs #884, #665, #872, #962. Implements the owner's decision of 2026-11-21 (#872) with the rulings of #884
issuecomment-7067495546 and issuecomment-7072401468 applied. Does not close #884: the bench qualification (ruling
item 3 of the first) is owed.

### What it does

- **Firmware owns gPTP** under `milan_soc.py --sw-gptp` (`GPTP_SW_EN_P`): one IEEE 802.1AS-2020 end station port
  an interface (`sw/firmware/ctrl/gptp/gptp.c`), fixed-point, no heap, behind a three-call HAL (send a frame, adjust
  the rate, step the time); the mailbox adapter (`gptp_mbx.c`) publishes each port from the callback that ran it,
  with no poll.
- **The fabric keeps the timestamps and the PHC**: `KL_gptp_tsu` keeps the plane's stamp points and corrections; the
  ingress stamp rides with its frame as an eight-octet trailer from a stamp FIFO in step with the split tap's frame
  FIFO (`KL_ctrl_split`, `GPTP_P`), so no stamp of a delivered frame is lost.
- **Mailbox contract 2.5, additive:** channel `gptp` (5), event `TIMESTAMP` (9, egress, not coalesced, credit-flowed,
  naming no hart), and a three-word gPTP publication an interface (`GPTP_GM_LO`, `GPTP_GM_HI`, `GPTP_STATE`).
- **The publication crosses whole**: `KL_mbx_cdc` copies the three words into a committed bank the cycle after
  `GEN` moves and crosses that bank, never the live words, so an update begun while a crossing is in flight reaches
  no delivered snapshot (REQ-PTP-07).
- **The gptp channel's admission burst is derived, seven an interface** (`sw/mailbox/mailbox.yaml`, stated in
  MAILBOX_CONTRACT.md): the worst legitimate coincidence of the 802.1AS message kinds in one 10 ms refill window.
  A full-duplex port receives seven kinds from its one peer (IEEE 802.1AS-2020 Tables 11-5 and 10-8), each at most
  once in 10 ms at Milan v1.2 Table 4.1's intervals and 802.1AS's 30 % tolerance (10.7.2.2, 10.7.2.3, 10.7.2.5).
  The model scales it by the interfaces: 7 at one, 14 at two.
- **The status block is narrowed** under `--sw-gptp`: parent, peer delay and path trace stay in firmware, which
  answers GET_AVB_INFO's gPTP fields and GET_AS_PATH from the snapshot it published and raises their changes;
  REGISTER_MAP regenerated.
- **The platform image composes gPTP** (`ctrl_plat_image.py --with-gptp`, `CTRL_PLAT_GPTP`) on the CSR's PTP block.
- **Memory debt ledgered**: the 8x8 gPTP images at 59.0, 64.0 and 62.0 RAMB36; the platform's 8x8/1if entry
  re-measured at 58.5 under contract 2.5.
- **The fabric plane stays buildable**; nothing of it is deleted.
- **One MAC.** The product split SoC has one MAC, so its build has one PHC, one launch observer, one timestamp unit
  and one control tap. The replication per MAC is built and proven at two interfaces in the closed loop. The second
  MAC is #962.

### Corrections after the first reviews (R884-1, R883-1)

Each finding is fixed at its cause, each reviewer's probe is now a regression test that fails at `f15b3a7d`, and
every earlier planted defect is still caught.

- **The publication tear (R884-1-F1).** The crossing read the live words when it was free, so an update begun while
  a commit crossed reached it. It now crosses the bank committed at the `GEN` write. Its own bench,
  `tb/verilator/mbx/tb_cdc_pub.sv`, runs at a datapath clock under and over the mailbox's: 53 checks, 12 of which
  fail on the old crossing, the reviewed ordering among them. Five planted defects are each caught. `split-sw`
  carries the reviewed ordering end to end (the old crossing gives `0x2222222233333333`), and the host model is
  held to the same orderings.
- **Sync without Follow_Up (R884-1-F2).** The sync receipt deadline now restarts only when a Sync and its Follow_Up
  are consumed as a pair (802.1AS-2020 10.2.8.2.1 c), so a master sending Sync alone, with or without Announce, is
  aged in its 375 ms, for a grandmaster-capable port and for one that never is.
- **The late second responder (R884-1-F3).** Each Pdelay_Req counts toward Milan v1.2 4.2.6.2.5's cease once, when
  a second clock identity answers it, whether before or after the first responder's Follow_Up; a request answered by
  one clock, or by none, ends the run. One clock answering twice is not asCapable (10.2.5.1 c) and does not cease.
- **A Follow_Up without its information TLV (R884-1-F4)** is refused (11.4.4.1, 11.4.4.3): absent, cut short, or
  of another type, length, organization or subtype. A further TLV after it is still accepted.
- **A PHC step on either side of the link (R883-1-F1).** This port's own step voids the exchange in flight,
  restarts its rate window and completes no response it owes. A rate window outside 2^-12 (244 ppm, above the
  200 ppm two in-tolerance clocks can differ by, B.1.1) holds the responder's step and restarts. A turnaround
  longer than its round trip is no measurement. The arithmetic is overflow-free for any 64-bit time difference,
  and asCapable now holds across a step at TAI scale and at 100 ms and 1 s offsets, at 1 ms and 10 ms turnarounds.
  The port's suite runs under UndefinedBehaviorSanitizer as a new gate arm (`gptp_ubsan`), clean.
- **`split-sw` in a gate (R883-1-F2):** it is `milan_dp`'s last case (`ci-list`), hosted leg 2.
- **The design page (R883-1-F3, F4)** states the routes of this head's RTL with the head they ran at, and the
  three-call HAL.

### Evidence

- gPTP port (`sw/firmware/ctrl/test/test_gptp.cpp`): 52 tests, also clean under UBSan; 40 planted defects all
  killed.
- Closed loop (`tb/verilator/gptp_sw`), two interfaces and two peers: each port locks its own PHC within 100 ns in
  about 2.5 s and holds it; as grandmaster each peer locks to it; bursts of 32 Pdelay_Req past the derived burst
  leave all 490 delivered event messages stamped, with no egress record lost and the lock kept. 48 checks;
  14 planted defects all killed.
- Timestamp unit bench (`tb/verilator/gptp_tsu`): both stamp points, the trailer read where the mailbox reads it, an
  80-frame flood; 36 checks; 24 planted defects all killed.
- The publication crossing (`tb/verilator/mbx`, `run-cdc-pub`): 53 checks; 5 planted defects all killed.
- Service budget at the derived burst: Pdelay turnaround 0.309 ms at 8x8/2if and 0.223 ms at 8x8/1if, against
  10 ms; composed maximum 1.655 ms and 1.634 ms inside THE SHARE (2.0 ms); no pass over the share (0 of 5,197 and
  of 5,142); the burst's last record by 7.853 ms. gPTP takes 0.31 % of the CPU.
- Held egress: `egress_ledger.py --point 8x8-1if` PASS, every held row within its ledger figure, among them
  `backlog-owed.service.acmp.last.if0` at 62.411 ms against 62.62 ms. The ledger exists at 8x8/1if only. At
  8x8/2if the held row is 62.460 ms; the tool cannot pass there on the 1if figures, with gPTP or without it (the
  AECP row's last instance falls on interface 1), so a 2if ledger is the ledger owner's to derive.
- Synthesis: the narrowing saves 3,049 FF.
- Routed `--sw-gptp` 8x8/1if with the gPTP image, at `9d753fa0` (the RTL and firmware of the head): all three
  placement directives meet #818's floor at every corner, ExtraTimingOpt at WNS +0.220 ns, WHS +0.056 ns,
  AltSpreadLogic_high at +0.174 / +0.056 ns, ExtraPostPlacementOpt at +0.154 / +0.026 ns. Against the plane at the
  same directive (routed at `40bd7738`): −5.0k LUT, −5.4k FF, −6 DSP, equal block RAM.
- Local gates, each at the head it names:
  - the full Verilator sweep at `333dc7c5`: 66 of 67 suites, 0 in-suite failures; `tsn_fuzz` failed there only
    on its traceability-matrix check, regenerated in `09c5934a`, where `tsn_fuzz` passes with and without the
    tsn-gen field campaigns (164 and 675 pass);
  - the 73 docs, idiom and rtl-fast gates: 73 of 73 at `09c5934a`, none skipped, xvlog executed (Vivado 2026.1's
    front end, 142 files, 0 findings); at `8167b70d`, whose one later change is the gPTP campaign's Python, 72 of
    73 in the run, its xvlog timing out on a busy Vivado slot, then xvlog re-run alone there: executed, 0 findings;
  - the firmware gate's four shards (the control campaign 826 of 826 caught; the `gptp`, `gptp_ubsan` and
    `gptp_rv32` arms), Yosys portability (64 tops), the publication census with its self-test, `split-cdc`, and
    the harness legs at `64a473be`, whose later commits touch tests and documents only.

### Owed, not in this PR

- **The census `GPTP_SW_EN_P` shape**, before this line merges onward. The census owner rules the rows the sw build
  ties off, and this lane applies the shape. The rows:
  - E rows `o_ctl_avb_chg_p`, `o_ctl_asp_chg_p`: constant 0 under `GPTP_SW_EN_P`, since the firmware raises those
    changes;
  - M rows `i_ctl_gptp_pub` (three words an interface; `GPTP_STATE` bits 11 to 15 reserved and unread, its `GEN`
    consumed in `KL_mbx_cdc`), `i_ctl_gptp_pub_p`, `i_ctl_ts_take`: read only under the sw build
    (`census_split.GPTP_SW_ONLY`);
  - `o_ctl_ts_valid`, `o_ctl_ts_data`: tied 0 under the plane, driven by the timestamp unit under the sw build;
  - the plane's `gptp_pub_*` parent, peer-delay and path nets: tied 0 under the sw build;
  - `KL_ctrl_split` with `GPTP_P`: the stamp FIFO and the ingress trailer.
- **The bench qualification** of #884.
- **The second MAC**: #962.
