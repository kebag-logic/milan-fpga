# Verilator verification harnesses

Runnable, self-checking [Verilator](https://verilator.org) harnesses for the
Milan TSN NIC. They need **only** `verilator >= 5.0` and a C++17 compiler — no
Xilinx tools — because they target the pure-RTL blocks (no XPM/DSP primitives are
instantiated). Each exits `0` on pass / non-zero on failure, so they drop
straight into CI.

| Harness | DUT | What it proves | Run |
|---------|-----|----------------|-----|
| [`cbs/`](cbs) | `credit_based_shaper.sv` | 802.1Qav credit math (runtime config): bit-exact vs a cycle-accurate fixed-point replica, bounded vs an ideal continuous model, and the accrual/drain/reset/recovery, strict-priority bypass, back-pressure accrual and live-reconfig behaviours (87 k checks). | `cd cbs && make` |
| [`shaper_core/`](shaper_core) | `traffic_shaping_core.sv` | Multi-queue arbiter (`REQ-VER-02`): grant exclusivity, tlast-held grants, strict-priority order, unshaped bypass, credit depletion — vs an independent arbiter model (61 k checks). | `cd shaper_core && make` |
| [`cls/`](cls) | `traffic_class_map.sv` | 802.1Q classification (`REQ-VER-03`): PCP→regen→TC→queue, untagged default priority, legacy EtherType fallback — vs a reference over 200 k random configs. | `cd cls && make` |
| [`ptp/`](ptp) | `timestamp_counter.sv` | PTP hardware clock: nominal rate, adjfine (fractional carry), settime, adjtime, gettime snapshot, disable — vs a 128-bit accumulator model (201 k checks). | `cd ptp && make` |
| [`ptp_sync/`](ptp_sync) | `ptp_csr_sync.sv` | CSR↔PHC CDC: settime/adjtime command-pulse ↔ payload alignment, one pulse per command, rate-config passthrough, gettime snapshot return path. | `cd ptp_sync && make` |
| [`csr/`](csr) | `milan_csr.sv` | AXI4-Lite CSR: reset values, RO/RW/W1C, IRQ mask+event, hardware-set-beats-W1C, PTP command strobes + TOD-valid snapshot, stats snapshot, output wiring (46 checks). | `cd csr && make` |
| [`adp/`](adp) | `adp_advertiser.sv` | ADP transmit (IEEE 1722.1 / Milan v1.2, `REQ`/FR-DISC-01..04): byte-exact 82-byte ADPDU decoded like a controller — Ethernet/subtype/cdl/fields, AVAILABLE vs DEPARTING, `available_index` bump-on-change/hold-on-readvertise, advertise timer, back-pressure integrity (121 checks). | `cd adp && make` |
| [`adp_tx/`](adp_tx) | `adp_tx_arbiter.sv` | 2-input AXIS packet arbiter merging the ADP stream into the MAC TX: no frame interleave, per-source in-order byte-exact delivery, round-robin fairness, back-pressure integrity (26 checks). | `cd adp_tx && make` |
| [`classifier/`](classifier) | `traffic_classifier.sv` | Full classifier after the `xpm_fifo_axis`→`axis_fifo` (Forencich) swap — proves it now Verilates; lossless in-order byte-exact passthrough + `tdest` stable per frame, under back-pressure (6 checks). Needs `third_party/verilog-axis`. | `cd classifier && make` |
| [`queues/`](queues) | `traffic_queues.sv` | Per-queue buffering after the `axis_switch` IP + `xpm_fifo_axis` → Forencich `axis_demux`/`axis_fifo`/`axis_arb_mux` swap (T1.3): per-queue `tdest` routing, grant suppression (no drain w/o grant), `queue_has_data`, byte-exact per-queue delivery (11 checks). | `cd queues && make` |
| [`tcam/`](tcam) | `tcam.sv` | Ternary CAM dest-MAC database (`REQ-MAC-02`): exact + wildcard/range match, priority among overlaps, multi-hit vector, add/remove/update entries, clean miss (19 checks). | `cd tcam && make` |
| [`rx_filter/`](rx_filter) | `rx_mac_filter.sv` | TCAM-driven RX dest-MAC filter (`REQ-MAC-02`): whitelist/blacklist, ternary range accept, mask exclusion, cut-through byte-exact forwarding of accepted frames (14 checks). | `cd rx_filter && make` |
| [`cdc/`](cdc) | `cdc_pulse.sv` + `cdc_handshake.sv` | Open CDC primitives that replaced `xpm_cdc_*` (T1.4): across two *independent* clocks — every source pulse yields one dest pulse; each value crosses byte-exact with req/ack (16 checks). | `cd cdc && make` |
| [`datapath/`](datapath) | `traffic_controller_802_1q.sv` | **End-to-end** de-Xilinx'd 802.1Q TX datapath (T1.5): classifier → Forencich per-queue FIFOs → CBS shaper. VLAN frames in → byte-exact egress, PCP→queue routing (exact `tdest`), all 4 queues, strict-priority + CBS modes, burst (15 checks). | `cd datapath && make` |
| [`milan_dp/`](milan_dp) | `milan_datapath.sv` | **Whole-wrapper integration** (§A.9 PS-less datapath the LiteX SoC instantiates): drive the AXI4-Lite CSR slave to read `ID="MILN"` (**M-A2**), VERSION, CAP bits; program the classifier over the CSR (readback); push a frame TX-DMA-port → MAC-port and MAC-port → RX-DMA-port, both byte-exact through classify→CBS→PTP→ADP-arbiter and PTP-RX→dest-MAC-filter (11 checks). | `cd milan_dp && make` |

```sh
# run everything
for d in cbs shaper_core cls ptp ptp_sync csr adp adp_tx classifier queues tcam rx_filter cdc datapath milan_dp; do ( cd "$d" && make clean >/dev/null && make ) || exit 1; done
```

## Conventions

* `cbs_ver_wrap.sv` / (CSR uses flat ports) expose internal DUT state to the C++
  harness via cross-module references so the *arithmetic/registers* are checked,
  not just the top-level outputs.
* Reference models (`cbs/cbs_ref_model.h`) and BFMs (`csr/sim_main.cpp`) are
  independent re-implementations of the spec — a DUT/model mismatch fails the run.
* When you extend a DUT, extend its harness in the same commit. The CSR harness
  is the executable form of [`docs/REGISTER_MAP.md`](../../docs/REGISTER_MAP.md).

## Notes

* The XPM/vendor IP is **gone** (Forencich open cores, see
  [`docs/OPEN_SOURCE_MIGRATION.md`](../../docs/OPEN_SOURCE_MIGRATION.md)): `hdl/` is
  XPM-free (T1.2 FIFOs, T1.3 switch/mux, T1.4 CDC). `traffic_classifier`,
  `traffic_queues`, `traffic_controller_802_1q` and `ptp_ts_top` all Verilate.
* Device portability is proven separately by the open Yosys synthesis check in
  [`syn/yosys/`](../../syn/yosys) (generic + Lattice ECP5).
* Still vendor-gated (T2): `milan_top` (MAC RGMII SelectIO cells + the Zynq PS block
  design).
