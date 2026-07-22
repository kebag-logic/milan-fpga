# Verilator verification harnesses

Runnable, self-checking [Verilator](https://verilator.org) harnesses for the
Milan TSN NIC — **25 suites** (one per subdirectory; the directory listing is
the authoritative count). They need **only** `verilator >= 5.0`, a C++17
compiler and the `third_party/verilog-axis` submodule
(`git submodule update --init third_party/verilog-axis`) — no Xilinx tools —
because they target the pure-RTL blocks (no XPM/DSP primitives are
instantiated). Each exits `0` on pass / non-zero on failure, so they are
CI-ready (note: no CI is wired up in this repo yet — see
[`docs/testing/TESTING.md`](../../docs/testing/TESTING.md)).

| Harness | DUT | What it proves | Run |
|---------|-----|----------------|-----|
| [`cbs/`](cbs) | `credit_based_shaper.sv` | 802.1Qav credit math (runtime config): bit-exact vs a cycle-accurate fixed-point replica, bounded vs an ideal continuous model, and the accrual/drain/reset/recovery, strict-priority bypass, back-pressure accrual and live-reconfig behaviours (87 k checks). | `cd cbs && make` |
| [`shaper_core/`](shaper_core) | `traffic_shaping_core.sv` | Multi-queue arbiter (`REQ-VER-02`): grant exclusivity, tlast-held grants, strict-priority order, unshaped bypass, credit depletion — vs an independent arbiter model (61 k checks). | `cd shaper_core && make` |
| [`cls/`](cls) | `traffic_class_map.sv` | 802.1Q classification (`REQ-VER-03`): PCP→regen→TC→queue, untagged default priority, legacy EtherType fallback — vs a reference over 200 k random configs. | `cd cls && make` |
| [`ptp/`](ptp) | `timestamp_counter.sv` | PTP hardware clock: nominal rate, adjfine (fractional carry), settime, adjtime, gettime snapshot, disable — vs a 128-bit accumulator model (201 k checks). | `cd ptp && make` |
| [`ptp_sync/`](ptp_sync) | `ptp_csr_sync.sv` | CSR↔PHC CDC: settime/adjtime command-pulse ↔ payload alignment, one pulse per command, rate-config passthrough, gettime snapshot return path. | `cd ptp_sync && make` |
| [`csr/`](csr) | `milan_csr.sv` | AXI4-Lite CSR: reset values, RO/RW/W1C, IRQ mask+event, hardware-set-beats-W1C, PTP command strobes + TOD-valid snapshot, stats snapshot, output wiring (check count printed at run time). | `cd csr && make` |
| [`adp/`](adp) | `adp_advertiser.sv` | ADP transmit (IEEE 1722.1 / Milan v1.2, `REQ`/FR-DISC-01..04): byte-exact 82-byte ADPDU decoded like a controller — Ethernet/subtype/cdl/fields, AVAILABLE vs DEPARTING, `available_index` bump-on-change/hold-on-readvertise, advertise timer, back-pressure integrity (121 checks). | `cd adp && make` |
| [`adp_tx/`](adp_tx) | `adp_tx_arbiter.sv` | 2-input AXIS packet arbiter merging the ADP stream into the MAC TX: no frame interleave, per-source in-order byte-exact delivery, round-robin fairness, back-pressure integrity (26 checks). | `cd adp_tx && make` |
| [`classifier/`](classifier) | `traffic_classifier.sv` | Full classifier after the `xpm_fifo_axis`→`axis_fifo` (Forencich) swap — proves it now Verilates; lossless in-order byte-exact passthrough + `tdest` stable per frame, under back-pressure (6 checks). Needs `third_party/verilog-axis`. | `cd classifier && make` |
| [`queues/`](queues) | `traffic_queues.sv` | Per-queue buffering after the `axis_switch` IP + `xpm_fifo_axis` → Forencich `axis_demux`/`axis_fifo`/`axis_arb_mux` swap (T1.3): per-queue `tdest` routing, grant suppression (no drain w/o grant), `queue_has_data`, byte-exact per-queue delivery (11 checks). | `cd queues && make` |
| [`tcam/`](tcam) | `tcam.sv` | Ternary CAM dest-MAC database (`REQ-MAC-02`): exact + wildcard/range match, priority among overlaps, multi-hit vector, add/remove/update entries, clean miss (19 checks). | `cd tcam && make` |
| [`rx_filter/`](rx_filter) | `rx_mac_filter.sv` | TCAM-driven RX dest-MAC filter (`REQ-MAC-02`): whitelist/blacklist, ternary range accept, mask exclusion, cut-through byte-exact forwarding of accepted frames (14 checks). | `cd rx_filter && make` |
| [`cdc/`](cdc) | `cdc_pulse.sv` + `cdc_handshake.sv` | Open CDC primitives that replaced `xpm_cdc_*` (T1.4): across two *independent* clocks — every source pulse yields one dest pulse; each value crosses byte-exact with req/ack (16 checks). | `cd cdc && make` |
| [`datapath/`](datapath) | `traffic_controller_802_1q.sv` | **End-to-end** de-Xilinx'd 802.1Q TX datapath (T1.5): classifier → Forencich per-queue FIFOs → CBS shaper. VLAN frames in → byte-exact egress, PCP→queue routing (exact `tdest`), all 4 queues, strict-priority + CBS modes, burst (15 checks). | `cd datapath && make` |
| [`milan_dp/`](milan_dp) | `milan_datapath.sv` | **Whole-wrapper integration** (§A.9 PS-less datapath the LiteX SoC instantiates): drive the AXI4-Lite CSR slave to read `ID="MILN"` (**M-A2**), VERSION, CAP bits; program the classifier over the CSR (readback); push a frame TX-DMA-port → MAC-port and MAC-port → RX-DMA-port, both byte-exact through classify→CBS→PTP→ADP-arbiter and PTP-RX→dest-MAC-filter (11 checks). | `cd milan_dp && make` |
| [`avtp_stream/`](avtp_stream) | `avtp_stream_parser.sv` | IEEE 1722 AVTP stream-header monitor (the S1 AVTP-engine foundation): stream-id / presentation-time / subtype / `tv` extraction against a programmable stream-match table, accept + reject cases, untagged and VLAN-tagged frames (21 checks). | `cd avtp_stream && make` |
| [`controller_rate/`](controller_rate) | `traffic_controller_802_1q.sv` | **Gating regression** for the CBS interference TX-wedge ([`docs/findings/CBS_DATAPATH_BUG.md`](../../docs/findings/CBS_DATAPATH_BUG.md)): back-to-back frames landing in *different* queues must each come out byte-exact — catches classifier `tdest` mis-timing / parse-FSM desync. | `cd controller_rate && make` |
| [`lwsrp_tx/`](lwsrp_tx) | `KL_lwsrp_tx.sv` | lwSRP applicant TX (802.1Q MSRP/MVRP, Milan v1.2 §5.6): byte-exact MSRP Domain/TalkerAdvertise + MVRP VID MRPDUs decoded like a bridge (endmark walk), NEW/JOININ/LV lifecycle, LeaveAll turn, back-pressure (363 checks). | `cd lwsrp_tx && make` |
| [`lwsrp_rx/`](lwsrp_rx) | `KL_lwsrp_rx.sv` | lwSRP receive chain (tap → packet FIFO → streaming walker → registrar) vs hand-built bridge MRPDUs: the **+k multi-value vector trap**, four-packed Ready/AskingFailed gating, leave-timer expiry, LeaveAll storms, domain boundary, TalkerFailed capture, truncation/garbage recovery (75 checks). Needs `third_party/verilog-axis`. | `cd lwsrp_rx && make` |
| [`lwsrp/`](lwsrp) | `KL_lwsrp_top.sv` | Whole lwSRP engine end-to-end at a 10 kHz scaled clock: declare cadence over ≥2 JoinTimes, reservation activation with **slope-before-gate** ordering, **gate-before-slope** teardown, 75 % TSpec refusal, LeaveAll turn + prompt re-declare (36 checks). | `cd lwsrp && make` |
| [`lwsrp_ctx/`](lwsrp_ctx) | `KL_lwsrp_top.sv` (`N_CTX_P=4`) | N-attribute context table: **golden N=1 byte-equivalence** with zero rows provisioned, CRF-listener row via the request/grant port (Ready follows the TA registration, TalkerFailed code readback), extra talker row's 25-B TalkerAdvertise FirstValue from the record RAM, **multi-attribute single-MRPDU packing**, one bridge vector covering several contexts at different +k, add/remove LV withdraw, LeaveAll aging across contexts (61 checks). Needs `third_party/verilog-axis`. | `cd lwsrp_ctx && make` |
| [`acmp_lstn/`](acmp_lstn) | `KL_acmp_lstn_ctx.sv` + `KL_acmp_listener.sv` | Milan v1.2 ACMP **listener** engine at a 10 kHz scaled clock (pipewire acmp-milan-v12.c contract), two executables: the 2-sink compatibility wrapper byte-identical regression (BIND_RX → response + PROBE_TX ladder 200 ms ×2 → 4 s retry, probe-response settle, SRP transitions, ADP watch + age-out, rebind rules, UNBIND, GET_RX_STATE payloads — 126 checks) and the N=4 mixed-policy context core (shared SM + context RAM, one timer wheel over simultaneous ladders, per-context sid policy derive/explicit, occupied-sink rebind, unbind isolation, table req/grant port — 100 checks). | `cd acmp_lstn && make` |
| [`acmp/`](acmp) | `KL_acmp_tlkr_ctx.sv` + `KL_acmp_responder.sv` | Milan v1.2 ACMP **talker** side, two executables: the 1-source compatibility wrapper byte-identical regression (PROBE_TX/DISCONNECT_TX/GET_TX_STATE/GET_TX_CONNECTION response tables, 15 s probe window, listener hold — 72 checks) and the N=4 source-context core (per-uid probe windows on ONE shared 1 s sweep, per-source stream params, TALKER_UNKNOWN_ID beyond N — 47 checks). | `cd acmp && make` |
| [`tdm/`](tdm) | `KL_tdm_capture.sv` + `KL_aaf_packetizer.sv` | Item-4 TDM front-end family: TDM16 slave deserializer slot alignment under BOTH documented frame-sync modes (1-bclk pulse + data delay 1, 50%-duty long fsync + delay 0, armed edge detection), then capture → packetizer with TCTX-chans pair-slot partitioning — a 234-byte 8-channel AAF PDU and a 90-byte stereo PDU byte-exact vs hand-built references (1722-2016 7.3.3/7.3.4/7.3.5), two epochs (seq/ts chains). | `cd tdm && make` |

```sh
# run everything (glob — never hand-list suites, lists go stale)
for d in */ ; do ( cd "$d" && make clean >/dev/null && make ) || exit 1; done
```

## Conventions

* `cbs_ver_wrap.sv` / (CSR uses flat ports) expose internal DUT state to the C++
  harness via cross-module references so the *arithmetic/registers* are checked,
  not just the top-level outputs.
* Reference models (`cbs/cbs_ref_model.h`) and BFMs (`csr/sim_main.cpp`) are
  independent re-implementations of the spec — a DUT/model mismatch fails the run.
* When you extend a DUT, extend its harness in the same commit. The CSR harness
  is the executable form of [`docs/reference/REGISTER_MAP.md`](../../docs/reference/REGISTER_MAP.md).

## Notes

* The XPM/vendor IP is **gone** (Forencich open cores, see
  [`docs/integration/OPEN_SOURCE_MIGRATION.md`](../../docs/integration/OPEN_SOURCE_MIGRATION.md)): `hdl/` is
  XPM-free (T1.2 FIFOs, T1.3 switch/mux, T1.4 CDC). `traffic_classifier`,
  `traffic_queues`, `traffic_controller_802_1q` and `ptp_ts_top` all Verilate.
* Device portability is proven separately by the open Yosys synthesis check in
  [`syn/yosys/`](../../syn/yosys) (generic + Lattice ECP5).
* Still vendor-gated (T2): `milan_top` (MAC RGMII SelectIO cells + the Zynq PS block
  design).
