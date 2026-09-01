# Verilator verification harnesses

Runnable, self-checking [Verilator](https://verilator.org) harnesses for the
Milan TSN NIC — one suite per subdirectory (the directory listing is
the authoritative count; prose numbers go stale).

They need **only** `verilator >= 5.050` (the CI pin; older 5.x cannot build every suite -- see [Section 7 of `docs/testing/TESTING.md`](../../docs/testing/TESTING.md#7-known-gaps-kept-honest)), a C++17
compiler and the `third_party/verilog-axis` submodule
(`git submodule update --init third_party/verilog-axis`) — no Xilinx tools —
because they target the pure-RTL blocks (no XPM/DSP primitives are
instantiated).

Each exits `0` on pass / non-zero on failure. Run the whole set with
`scripts/run_all_suites.sh` (exit status = number of failing suites); CI runs it
in the `rtl` workflow, and the docs/matrix/builder gates in the `docs` workflow
— see [`docs/testing/TESTING.md`](../../docs/testing/TESTING.md).

| Harness | DUT | What it proves | Run |
|---------|-----|----------------|-----|
| [`cbs/`](cbs) | `credit_based_shaper.sv` | 802.1Qav credit math (runtime config): bit-exact vs a cycle-accurate fixed-point replica, bounded vs an ideal continuous model, and the accrual/drain/reset/recovery, strict-priority bypass, back-pressure accrual and live-reconfig behaviours (87 k checks). | `cd cbs && make` |
| [`shaper_core/`](shaper_core) | `traffic_shaping_core.sv` | Multi-queue arbiter (`REQ-VER-02`): grant exclusivity, tlast-held grants, 802.1Q order (the higher queue index wins -- all 15 pairs), unshaped bypass, credit depletion -- vs an independent arbiter model. Plus **FQTSS** (802.1Q-2018 clause 34): Section 34.3.1 bandwidth availability over the package slope tables, and the MEASURED port share between a shaped SR class and unshaped best effort, its non-vacuity twin with CBS off, and gPTP's worst service gap under a saturating class A (1.5 M checks). | `cd shaper_core && make` |
| [`cls/`](cls) | `traffic_class_map.sv` | 802.1Q classification (`REQ-VER-03`): PCP→regen→TC→queue, untagged default priority, legacy EtherType fallback, reserved-DMAC validation of the gPTP fast path (`REQ-CLS-07`, with its spoof negatives), and the **DMAC-keyed control fast path** (`REQ-CLS-10`): the whole q2 protocol table, the gPTP/MSRP split at the shared `01-80-C2-00-00-0E`, AECP on the unicast arm, and four negatives — a tagged `0x22F0` still on the SR classes, an address with no table row (including the Bridge Group Address RSTP will use), a forged `0x22F0` to a foreign multicast, and `CLS_CTRL[2]=0` restoring VERSION `0x0011`. All vs a reference over 200 k random configs × 9 destination MACs. | `cd cls && make` |
| [`ptp/`](ptp) | `timestamp_counter.sv` | PTP hardware clock: nominal rate, adjfine (fractional carry), settime, adjtime, gettime snapshot, disable — vs a 128-bit accumulator model (201 k checks). | `cd ptp && make` |
| [`ptp_sync/`](ptp_sync) | `ptp_csr_sync.sv` | CSR↔PHC CDC: settime/adjtime command-pulse ↔ payload alignment, one pulse per command, rate-config passthrough, gettime snapshot return path. | `cd ptp_sync && make` |
| [`clkvalid/`](clkvalid) | `KL_ptp_clock_validity.sv` | The AVTP **`tu`** verdict every talker stamps. Product mode consumes the fabric owner's sync/asCapable/GM publication, detects discontinuity and applies the Milan holdover; verification-only option OFF is ownerless, holds `tu=1`, reports sync/asCapable zero and ignores every retired write. `CLKV_TUCNT` counts Milan Table 5.4 observation intervals. Both compressed behavioural timing and the shipping divider are covered. | `cd clkvalid && make` |
| [`csr/`](csr) | `milan_csr.sv` | AXI4-Lite CSR: reset values, RO/RW/W1C, IRQ mask+event, hardware-set-beats-W1C, PTP command strobes + TOD-valid snapshot, stats snapshot, output wiring (check count printed at run time). | `cd csr && make` |
| [`adp_tx/`](adp_tx) | `adp_tx_arbiter.sv` | 2-input AXIS packet arbiter merging the ADP stream into the MAC TX: no frame interleave, per-source in-order byte-exact delivery, round-robin fairness, back-pressure integrity (26 checks). | `cd adp_tx && make` |
| [`classifier/`](classifier) | `traffic_classifier.sv` | Full classifier after the `xpm_fifo_axis`→`axis_fifo` (Forencich) swap — proves it now Verilates; lossless in-order byte-exact passthrough, `tdest` correct+stable per frame under back-pressure, the DEI drop-eligibility sideband on `tuser[0]` (`REQ-CLS-05`, untagged negative), reserved-DMAC gating (`REQ-CLS-07`), the DMAC-keyed control fast path through the real parser (`REQ-CLS-10` — the q2 protocol table at line rate, the gPTP/MSRP split at one address, a tagged `0x22F0` staying on the SR classes, proof that `eth_type` is the **inner** type and not the TPID, and the no-row/`CLS_CTRL[2]=0` negatives) and a zero-idle line-rate burst with a stale-by-one-frame negative (`REQ-CLS-06`). Needs `third_party/verilog-axis`. | `cd classifier && make` |
| [`queues/`](queues) | `traffic_queues.sv` | Per-queue buffering after the `axis_switch` IP + `xpm_fifo_axis` → Forencich `axis_demux`/`axis_fifo`/`axis_arb_mux` swap (T1.3): per-queue `tdest` routing, grant suppression (no drain w/o grant), `queue_has_data`, byte-exact per-queue delivery (11 checks). | `cd queues && make` |
| [`tcam/`](tcam) | `tcam.sv` | Ternary CAM dest-MAC database (`REQ-MAC-02`): exact + wildcard/range match, priority among overlaps, multi-hit vector, add/remove/update entries, clean miss (19 checks). | `cd tcam && make` |
| [`rx_filter/`](rx_filter) | `rx_mac_filter.sv` | RX dest-MAC filter (`REQ-MAC-02`): TCAM whitelist/blacklist, ternary range accept, mask exclusion, cut-through byte-exact forwarding, plus the 802.3 station address filter — promisc, exact-match unicast, broadcast, allmulti, the 64-bucket multicast hash against an independent reference fold, and the precedence between all three layers. | `cd rx_filter && make` |
| [`cdc/`](cdc) | `cdc_pulse.sv` + `cdc_handshake.sv` | Open CDC primitives that replaced `xpm_cdc_*` (T1.4): across two *independent* clocks — every source pulse yields one dest pulse; each value crosses byte-exact with req/ack (16 checks). | `cd cdc && make` |
| [`mac_rmon/`](mac_rmon) | `KL_mac_rmon_events.sv` (two shapes: a MAC that checks FCS/preamble/bad-frame, and one that checks none) | The block that turns MAC-boundary facts into the `ethernet_events` pulse vector — the RMON "decorative ABI" fix. Per-frame derivation at the AXIS boundary across an asynchronous clock ratio (exactly one 1-cycle destination pulse per frame; mid-frame beats and a backpressured `tlast` count for nothing), good-vs-bad RX frames mutually exclusive, MAC error counters turned into pulses with a counter RESET (link-guard reinit) deliberately emitting none, and — the honesty half — `cap_o` tracking the parameters rather than the wish: the four MAC-internal lanes are never claimed, an unattached boundary reports cap 0 **and** stays silent, and the no-checks shape drops the three optional lanes from the mask (2 × 28 checks). | `cd mac_rmon && make` |
| [`datapath/`](datapath) | `traffic_controller_802_1q.sv` | **End-to-end** de-Xilinx'd 802.1Q TX datapath (T1.5): classifier → Forencich per-queue FIFOs → CBS shaper. VLAN frames in → byte-exact egress, PCP→queue routing (exact `tdest`), all 4 queues, strict-priority + CBS modes, burst (15 checks). | `cd datapath && make` |
| [`milan_dp/`](milan_dp) | `milan_datapath.sv` | Whole-wrapper integration: CSR identity/version, classifier programming, byte-exact memory/MAC paths, NxN routing and protocol-processor publication. Product-on gPTP checks cover BMCA/sync/pdelay, coherent GM/parent/path publication, CLOCK_DOMAIN counters/notifications and AAF/CRF `tu`; verification-only option OFF proves zero-owner, zero-publication, write-inert fail-safe behavior. Pruned and generated NxN shapes elaborate and retain their structural-zero contracts. | `cd milan_dp && make` |
| [`avtp_stream/`](avtp_stream) | `avtp_stream_parser.sv` | IEEE 1722 AVTP stream-header monitor (the S1 AVTP-engine foundation): stream-id / presentation-time / subtype / `tv` extraction against a programmable stream-match table, accept + reject cases, untagged and VLAN-tagged frames (21 checks). | `cd avtp_stream && make` |
| [`avtp_parser/`](avtp_parser) | `avtp_stream_parser.sv` + `KL_stream_table.sv`, at **five shapes** (`N_STREAMS` = 1 / 4 / 8, `BIG_ENDIAN=1`, and the table+parser pairing at N=8) | The listener **accept verdict** and, above all, its **reject leg**: `stream_id` byte order as lifted off the wire, the VLAN-tagged vs untagged offset with both mis-offset negatives, the subtype/`sv` gate swept, every table entry reachable at each N (entries 4..7 exist only at N=8), the compare's failure modes — byte-reversed arm, transposed `SID_LO`/`SID_HI`, one-bit-off, armed-but-disabled — each asserted as the exact `0x8B4` APRB signature (*PARSED climbs, MATCHED does not, the latch shows the wire value*), frame-stream integrity (one verdict per frame, back-to-back with no gap, backpressure, the 56-byte header floor), 600 randomised frames per shape against an independent model, and TRAP-1: any entry-0 window write detaches the ACMP alias for good (~10 660 checks). | `cd avtp_parser && make` |
| [`controller_rate/`](controller_rate) | `traffic_controller_802_1q.sv` | **Gating regression** for the CBS interference TX-wedge ([`docs/findings/CBS_DATAPATH_BUG.md`](../../docs/findings/CBS_DATAPATH_BUG.md)): back-to-back frames landing in *different* queues must each come out byte-exact — catches classifier `tdest` mis-timing / parse-FSM desync. | `cd controller_rate && make` |
| [`aes3/`](aes3) | `KL_aes3_tx.sv` + `KL_aes3_rx.sv` | Item-4 **AES3 / S-PDIF** biphase-mark ser/des: one encoder drives one line into FOUR receivers (24/20/16-bit words, professional and consumer channel-status dialects), so every difference observed is the parameter under test. Cold acquisition with **no external bit clock** — the unit interval is measured off the wire, X/Y/Z preambles are found by their illegal 3-UI run, and `locked_o` waits for `LOCK_BLOCKS_P` clean 192-frame blocks with **no pair emitted before it**; then sample-exact pairs in order, 20/16-bit truncation exactly where the standard says, channel status round-tripped and re-read in both dialects (the mismatch flag included), `V=1` counted without gagging the pair, a **real injected biphase violation** (two extra transitions on the line) dropping lock and self-re-locking, and transmitter underrun keeping the line legal while confessing the repeat (50 checks). | `cd aes3 && make` |
| [`tdm/`](tdm) | `KL_tdm_capture.sv` + `KL_aaf_packetizer.sv` | Item-4 TDM front-end family: TDM16 slave deserializer slot alignment under BOTH documented frame-sync modes (1-bclk pulse + data delay 1, 50%-duty long fsync + delay 0, armed edge detection), then capture → packetizer with TCTX-chans pair-slot partitioning — a 234-byte 8-channel AAF PDU and a 90-byte stereo PDU byte-exact vs hand-built references (1722-2016 7.3.3/7.3.4/7.3.5), two epochs (seq/ts chains). | `cd tdm && make` |

```sh
# run everything (glob — never hand-list suites, lists go stale)
for d in */ ; do ( cd "$d" && make clean >/dev/null && make ) || exit 1; done
```

### Suites without a row above (yet)

The table above is not complete — **`ls` is**. Run `ls tb/verilator/` for the
authoritative suite list; these have no prose row here:

[`aaf/`](aaf) · [`aaf_audio_loop/`](aaf_audio_loop) · [`aaf_latency_taps/`](aaf_latency_taps) · [`avtp_rxmon/`](avtp_rxmon) · [`chmap_capture/`](chmap_capture) · [`chmap_render/`](chmap_render) · [`crf_rx/`](crf_rx) · [`crf_tx/`](crf_tx) · [`eth_tx_reset/`](eth_tx_reset) · [`i2spb/`](i2spb) · [`ifg/`](ifg) · [`lat_history_ring/`](lat_history_ring) · [`link_guard/`](link_guard) · [`maap/`](maap) · [`mmcm_servo/`](mmcm_servo) · [`mmcm_servo_autorepair/`](mmcm_servo_autorepair) · [`pcmlpf/`](pcmlpf) · [`ptp_ts/`](ptp_ts) · [`tcam_csr/`](tcam_csr) · [`tdm_render/`](tdm_render) · [`tsn_fuzz/`](tsn_fuzz)

Rather than guess at what each proves, use the two authoritative sources: the
suite's own `README.md` where it has one, and
[`docs/traceability/MODULE_MATRIX.md`](../../docs/traceability/MODULE_MATRIX.md),
which is **generated** from the RTL tree and the TB Makefiles and lists, per
module, every testbench that compiles it.

> **2026-08-13 — thirteen suites were DELETED with the RTL they tested.**
> `aecp`, `aempatch`, `acmp`, `acmp_lstn`, `persist`, `adp`, `adp_advertise`,
> `adp_parser`, `lwsrp`, `lwsrp_ctx`, `lwsrp_rx`, `lwsrp_tx` and
> `lwsrp_switchpdu` covered this repository's own AECP/AEM, ACMP, ADP and
> lwSRP engines, all of which are gone: the protocol-processor submodule is
> the control plane now. The `csr` suite lost its `obj_live` leg (it wired the
> 0x800 window to those engines' context tables) and `tsn_fuzz` lost its
> `aecp`/`acmp`/`adp`/`legacy` campaigns, keeping only `aaf`. That is a real
> and large coverage loss on IEEE 1722.1: this repository no longer has any
> 1722.1 RTL of its own to test, and the processor's own campaigns live with
> the submodule.

Full sweep on 2026-07-27: **56/56 PASS, 2 062 281 checks, 0 failures**
(`scripts/run_all_suites.sh`, Verilator v5.050). The same tree immediately
before that round measured **55/55, 2 062 053** — so the whole delta is the new
that suite's checks, and a per-suite diff of the two sweeps shows one
differing row. (The example named `adp_parser`, a suite deleted 2026-08-13
with the RTL it tested; the tool-version trap it illustrates is unchanged.)

> **Those two totals are UNDER-COUNTS, kept as written because the delta
> argument above still holds.** On 2026-07-28 the aggregator was found to
> recognise only one of the **five** summary shapes this tree emits, so **29 of
> 57 suite logs contributed exactly zero** and two more were counted only in
> part. It also read `N checks: P PASS, F FAIL` as `P` rather than `N` — right
> only while those suites had no failures, i.e. an accounting check that could
> not fail. Corrected by `scripts/suite_tally.py`, which additionally **fails
> the sweep** on a log with no tally or with a tally in an unknown shape.
> Any figure quoted from before that date is low by roughly 1.8 %. That is part of how the round's
`axi_stream_if` `TDATA_WIDTH_P` 32 → 64 default change was shown to move no
elaboration (the other part being `syn/yosys/run.sh`, cell-for-cell identical
across all 47 tops).

## Conventions

* `cbs_ver_wrap.sv` / (CSR uses flat ports) expose internal DUT state to the C++
  harness via cross-module references so the *arithmetic/registers* are checked,
  not just the top-level outputs.
* Reference models (`cbs/cbs_ref_model.h`) and BFMs (`csr/sim_main.cpp`) are
  independent re-implementations of the spec — a DUT/model mismatch fails the run.
* When you extend a DUT, extend its harness in the same commit. The CSR harness
  is the executable form of [`docs/reference/REGISTER_MAP.md`](../../docs/reference/REGISTER_MAP.md).

## Notes

* The XPM/vendor IP is **gone**: `hdl/` uses Forencich open cores and is
  XPM-free across FIFOs, switch/mux, and CDC. `traffic_classifier`,
  `traffic_queues`, `traffic_controller_802_1q` and `ptp_ts_top` all Verilate.
* Device portability is proven separately by the open Yosys synthesis check in
  [`syn/yosys/`](../../syn/yosys) (generic + Lattice ECP5).
