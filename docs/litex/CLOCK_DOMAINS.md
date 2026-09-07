# Clock domains, resets, and crossings

This guide maps the reference SoC's actual clock wiring.
It distinguishes clock sources, reset domains, and protocol time.

Baseline: `911bc57e`, the `dev` tip of 2026-09-06.
Every claim below was checked against that source.

Example configuration: [AX7101 1x1 TDM8](../../configs/endstation_ax7101_1x1_tdm8.yaml).
Rates below describe this configuration unless stated otherwise.

This is an implementation map, not CDC sign-off.
[REQ-CSR-03](../../REQUIREMENTS.md#3-csr-plane) remains the crossing requirement.

## Contents

- **[Clock tree](#clock-tree)** -- Follow physical sources and derived clocks.
- **[Domain inventory](#domain-inventory)** -- Find frequencies, consumers, and clock aliases.
- **[Audio variants](#audio-variants)** -- Separate nominal rates from synthesized rates.
- **[Reset ownership](#reset-ownership)** -- Understand reset scope and recovery ordering.
- **[Crossing map](#crossing-map)** -- Locate bus, packet, audio, and control crossings.
- **[gPTP timestamp boundaries](#gptp-timestamp-boundaries)** -- Locate timestamp capture relative to MAC buffering.
- **[Constraints and verification](#constraints-and-verification)** -- Check implementation evidence without assuming CDC safety.
- **[Known gaps](#known-gaps)** -- Find the recorded contradictions and their owners.
- **[Source index](#source-index)** -- Find the owning code and related contracts.

## Clock tree

Arrows below mean clock derivation, not data flow.
Rates are nominal, before oscillator tolerance or servo adjustment.

```text
AX7101 board oscillator: 200 MHz
  |
  +-- main PLL
        +-- sys: 100 MHz
        |     +-- audio pre-PLL --> audio_ref --> audio MMCM
        |                                          +-- audio: ~24.576 MHz
        |                                          +-- audio_tdm: optional
        +-- milan: 50 MHz
        |     +-- axis_clk = gtx_clk = CPU cpu_clk
        +-- sys4x: 400 MHz              [DDR3]
        +-- sys4x_dqs: 400 MHz, +90 deg [DDR3]
        +-- idelay: 200 MHz             [delay calibration; MMCM PSCLK]

Ethernet PHY RXC: 125 MHz               [independent board input]
  +-- eth_rx --> GMII receive registers
  +-- eth_tx --> GMII transmit registers --> forwarded GTX pad clock
                                            [180 deg option enabled]
```

The PHC does **not** use the PHY's 125 MHz clock.
`gtx_clk` is a legacy datapath port name.

`sys` and `milan` share a PLL source.
Their crossings still use asynchronous interfaces and timing exceptions.

Ethernet RXC is independent of the main PLL.
Losing RXC also stops this GMII transmit clock.

Source: [`_CRG` and `MilanMAC`](../../sw/litex/milan_soc.py).

## Domain inventory

| Clock/domain | Example rate | Source | Main consumers |
|---|---:|---|---|
| `clk200` | 200 MHz | Differential board oscillator | Main PLL |
| `sys` | 100 MHz | Main PLL | LiteX interconnect, CSR bridges, ROM/SRAM, UART, SPI controller, LiteDRAM controller, CPU wrapper's `litex_clk` |
| `milan` | 50 MHz | Main PLL | Datapath, Milan CSR decoder, protocol engines, PHC, CPU `cpu_clk` |
| `sys4x` | 400 MHz | Main PLL | DDR3 PHY serialization |
| `sys4x_dqs` | 400 MHz, +90 degrees | Main PLL | DDR3 PHY DQS timing |
| `idelay` | 200 MHz | Main PLL | IDELAYCTRL reference; audio MMCM phase-control clock |
| `audio_ref` | 31.081081 MHz, plan A | Audio pre-PLL from `sys` | Audio MMCM input; intermediate net, not a Migen domain |
| `audio` | 24.575739 MHz, plan A | Audio MMCM output 0 | TDM8 master, enabled I2S paths, CRF/audio clock measurement |
| `audio_tdm` | Absent in TDM8 | Optional audio MMCM output 1 | TDM16/TDM32 master |
| `eth_rx` | 125 MHz at 1 Gb/s | PHY RXC through BUFG | GMII RX registers |
| `eth_tx` | 125 MHz at 1 Gb/s | Same PHY RXC through BUFG | GMII TX registers; forwarded GTX pad clock |

Logical aliases do not introduce another oscillator:

| Name | Clock equality | Reset distinction |
|---|---|---|
| `axis_clk` | Selected `milan_cd`: `milan` here | `axis_resetn = ~ResetSignal(milan_cd)` |
| `gtx_clk` | Same selected `milan_cd` | `gtx_resetn = axis_resetn` here |
| CPU `cpu_clk` | `milan` when `with_cpu_clk` is selected; the shipping choice, kept by [#364](https://github.com/kebag-logic/milan-fpga/issues/364) after a measured comparison with `sys` | CPU wrapper owns its internal reset synchronization |
| CPU `litex_clk` | `sys` | Wrapper receives `sys` reset plus CPU reset request |
| `macdp` | `milan_cd`, when distinct from `sys` | Milan reset extended by MAC `reinit` |
| `macsys` | `sys` | System reset extended by MAC `reinit` |
| `maceth_rx`, `maceth_tx` | `eth_rx`, `eth_tx` respectively | PHY-domain resets extended by `eth_rst` |
| `clk_audio_i` | `audio` | RTL audio blocks receive `axis_resetn`; see reset caveat |
| `clk_tdm_i` | `audio` for TDM8; `audio_tdm` for TDM16/32 | TDM master synchronizes its incoming reset locally |
| `i_ps_clk` | `idelay` here; `sys` without DDR/Ethernet | Servo synchronizes its incoming reset locally |

Without a selected Milan clock, `milan_cd` becomes `sys`.
The explicit Milan stream and AXI-Lite crossings then disappear.

This does not establish a complete alternate product recipe.

The CPU does not necessarily run at the system-bus rate.

Here, CPU execution is 50 MHz.
The system bus runs at 100 MHz.

Other interface clocks are not extra `_CRG` domains:

- JTAG TCK clocks programming/debug access, not the Milan datapath.
- SPI SCK is generated by the system-clocked SPI controller.
- Software-driven MDC and UART baud timing also originate in `sys`.

## Audio variants

The requested audio rate is nominal, not mathematically exact.
The explicit integer PLL/MMCM recipe determines its initial frequency.

Values below assume the reference 100 MHz audio input.

| Selection | Pre-PLL output | MMCM multiplier/dividers | Actual initial output |
|---|---|---|---|
| Plan A: I2S or TDM8 | `100 MHz × 23 / (2 × 37)` | `×34 /43` | `audio = 24,575,738.529 Hz`, about -10.64 ppm |
| Plan B: TDM16 | `100 MHz × 23 / (2 × 67)` | `×63 /44`; second output `/22` | `audio = 24,575,983.718 Hz`; `audio_tdm = 49,151,967.436 Hz` |
| Plan B: TDM32 | Same as TDM16 | `×63 /44`; second output `/11` | Same `audio`; `audio_tdm = 98,303,934.871 Hz` |

Plan B's initial error is about -0.66 ppm.
The media servo steers enabled MMCM outputs together.

These calculated values are not measured board frequencies.

TDM uses 32-bit slots at nominal 48 kHz:

| Geometry | Nominal master input | Nominal BCLK | Frame rate |
|---|---:|---:|---:|
| TDM8 | 24.576 MHz, existing `audio` | 12.288 MHz | 48 kHz |
| TDM16 | 49.152 MHz, `audio_tdm` | 24.576 MHz | 48 kHz |
| TDM32 | 98.304 MHz, `audio_tdm` | 49.152 MHz | 48 kHz |

- Master BCLK/FSYNC are divided outputs, not new internal clocks.
- `KL_tdm_capture_master` uses clock enables on `clk_tdm_i`.
- Slave TDM instead clocks registers from external `tdm_bclk_i`.
- That external clock is another domain requiring integration constraints.
- The example configuration exposes capture, not physical TDM rendering.

Three different meanings of “time” coexist:

- **PHC:** numeric nanoseconds, advanced on the Milan clock.
- **Audio clock:** physical MMCM output, steered by media recovery.
- **Media tick:** a datapath pulse, not a separate clock net.

Changing the PHC increment does not retune the main PLL.
At 50 MHz, its nominal increment is 20 ns/tick.

## Reset ownership

Equal-frequency domains can still have independent reset lifetimes.

| Reset scope | Assertion source | Release/ownership |
|---|---|---|
| Main PLL | Active-low board reset button | `_CRG`; outputs require PLL lock |
| PLL output domains | Main PLL unlock | LiteX `create_clkout` reset synchronization, per output clock |
| CPU core | Wrapper's system/CPU reset request | Generated VexiiRiscv wrapper; inspect the exact generated core |
| `axis_resetn`, `gtx_resetn` | Selected Milan-domain reset | Identical inverted reset net in this integration |
| `audio`, `audio_tdm` Migen domains | Audio MMCM unlock | `AsyncResetSynchronizer`, released on each audio clock |
| Audio MMCM reset | `audio_mmcm_rst` from the media servo | Servo owns MMCM repair/control sequencing |
| `eth_rx`, `eth_tx` | PHY initialization/software reset, or guard `eth_rst` | PHY wrapper; asynchronous assertion, local synchronous release |
| `maceth_rx`, `maceth_tx` | Corresponding Ethernet reset OR `eth_rst` | MAC shadow-domain reset synchronizers |
| `macsys`, `macdp` | Corresponding system/Milan reset OR `reinit` | MAC shadow-domain reset synchronizers |

The audio-domain reset signals are not automatically RTL resets.
`add_milan_datapath()` passes audio clocks, not `ResetSignal("audio")`.

Several audio modules synchronize incoming `axis_resetn` locally.
Other audio-clocked processes use it directly.

For example, inspect `zf_audio_div` in
[`milan_datapath`](../../hdl/milan/milan_datapath.sv).
Do not infer MMCM-unlock coverage for every audio register.

Link recovery preserves the Milan datapath and CPU clocks.
Its reset sequence is:

```text
Ethernet clock outage
  -> hold MAC/PHY-side fabric resets
  -> wait for both Ethernet clocks to resume
  -> settle: release eth_rst after 1,048,576 clean cycles (20.97 ms)
  -> release reinit after 2,097,152 clean cycles (41.94 ms)
  -> resume MAC traffic
```

The `link_guard` instance in the [datapath](../../hdl/milan/milan_datapath.sv) passes no override.
It runs on `axis_clk`, the Milan clock at 50 MHz here.

| Guard constant | Cycles | Duration at 50 MHz | Meaning |
|---|---:|---:|---|
| `DEAD_CYC_C` | 4,096 | 81.92 us | No-transition window that declares an Ethernet clock dead |
| `ETH_REL_CYC_C` (`SETTLE_CYC_C / 2`) | 1,048,576 | 20.97 ms | `eth_rst` release point inside the settle hold |
| `SETTLE_CYC_C` | 2,097,152 | 41.94 ms | Full `reinit` hold after both clocks return |

Constants: [`KL_link_guard`](../../hdl/common/KL_link_guard.sv) parameters and `ETH_REL_CYC_C`.

The guard's comments say 21 ms and 41 us.
Those are the 100 MHz figures; [#374](https://github.com/kebag-logic/milan-fpga/issues/374) owns them.

- Both FIFO reset sides must converge before resuming traffic.
- Per-domain reset release can differ by several clock cycles.
- Clock-liveness toggle registers are deliberately `reset_less`.
- Resetting those observers through the guard creates a deadlock.
- Guard `eth_rst` does not reset the physical PHY chip.
- Physical PHY reset remains a separate initialization/software action.

See [`KL_link_guard`](../../hdl/common/KL_link_guard.sv) and
the [reset timing diagram](../diagrams/wd_linkguard_reset.svg).

## Crossing map

This table identifies important integration paths, not every register.
Conditional paths exist only when their features are elaborated.

| Path | From → to | Implemented crossing / caveat |
|---|---|---|
| Milan CSR transactions | `sys` ↔ `milan` | `milan_axil_cdc`: LiteX `AXILiteClockDomainCrossing` |
| Descriptor-memory requests and responses | `milan` ↔ `sys` | `descmem_req_cdc`, `descmem_rsp_cdc` |
| Response and record-image memory channels | `milan` ↔ `sys` | `respmem_*_cdc`, `nvmmem_*_cdc`; separate request, response, write, completion streams |
| MAC TX stream | `macdp` → `macsys` | `mac_tx_cdc`; reset-extended shadow domains |
| MAC RX stream | `macsys` → `macdp` | `mac_rx_cdc`; reset-extended shadow domains |
| MAC core TX/RX streams | `macsys` → `maceth_tx`; `maceth_rx` → `macsys` | LiteEth internal stream FIFOs plus width conversion |
| CPU peripheral/DMA interfaces | CPU clock ↔ `sys` | Generated CPU wrapper's supported CDC; distinct from dedicated DDR port |
| CPU dedicated DDR AXI port | CPU clock (`milan`) → `sys` LiteDRAM port | `cross_cpu_memory_ports()`: one LiteX `AXIClockDomainCrossing` per memory bus, added by [#359](https://github.com/kebag-logic/milan-fpga/issues/359)'s fix; before it the port was connected straight and the board stalled when the BIOS returned the DRAM to the controller |
| Link, duplex and speed levels | `sys` → Milan | Migen `MultiReg` on `link_status.link_up` and `full_duplex`; `speed` is synchronized by RTL `mac_speed_cdc` |
| CSR IRQ | none | `o_irq_csr` is left unconnected in `add_milan_datapath()`; firmware polls, and no CPU event-manager ABI exists |
| MAC event pulses | `macsys` → Milan | `KL_mac_rmon_events`, using `cdc_pulse` |
| Ethernet liveness/activity toggles | `eth_rx`/`eth_tx` → Milan | Reset-less source toggles; synchronization inside `KL_link_guard` |
| PHC commands and snapshots | `axis_clk` ↔ `gtx_clk` | `ptp_csr_sync` retained, but both clock ports alias Milan here |
| Capture sample pairs | Audio/master TDM or external slave BCLK → Milan | `cdc_pair_fifo` in the selected capture module |
| Playback/render samples | Milan → audio or external slave BCLK | `cdc_pair_fifo` in enabled I2S playback / TDM render |
| Audio events and fill ticks | Audio → Milan | `cdc_pulse`, including `zf_tick_cdc` |
| MMCM phase-command batches | Milan → `i_ps_clk` | Servo `cdc_handshake`; phase runner waits for `PSDONE` |
| MMCM DRP commands/replies | Milan → MMCM DCLK interface | DCLK equals Milan; no separate DRP clock domain |

`_axis_dp_cdc` supplies the named packet/memory stream crossings.
Each uses a 16-beat buffered asynchronous FIFO here.

LiteEth's internal FIFOs have separate dependency-owned settings.

The CPU DDR path is crossed since #359's fix:

- `cross_cpu_memory_ports()` wraps each CPU memory bus in an `AXIClockDomainCrossing`.
- That crossing runs from `milan` to `sys`.
- The CPU wrapper already crossed its peripheral bus and DMA.
- The memory bus was not crossed before the fix.
- LiteX labels every interface's `clock_domain` by default.
- The label proved nothing; the asynchronous FIFO count did.
- `sw/litex/test_cpu_memory_port_cdc.py` drives the hook on a stand-in CPU.

See the generated [CDC census](../diagrams/cdc_census.svg).
Its [generator](../diagrams/cdc_census.gen.py) inventories recognized primitive call sites.

It does not prove the absence of unprotected crossings.
It also includes retained and conditional RTL, beyond this configuration.

## gPTP timestamp boundaries

The PHC and fabric gPTP engine share the Milan clock.
The engine reads `ptp_now_w` directly, without a PHC-bus CDC.

Keep `gtx_clk` and `axis_clk` equal in this integration.
Moving `gtx_clk` to PHY RXC alone breaks that assumption.

`ptp_csr_sync` does not protect those direct live-PHC consumers.

Current TX path:

```text
Milan 50 MHz                         macsys 100 MHz        maceth_tx 125 MHz
TX arbitration
  -> AXIS first-beat stamp
  -> mac_tx_cdc -------------------> tx_sf PacketFIFO
                                      -> LiteEth TX CDC -> width/framing
                                                          -> GMII registers
                                                          -> PHY -> wire
```

Current RX path:

```text
Wire -> PHY -> GMII RX 125 MHz -> LiteEth framing/width conversion
  -> LiteEth RX CDC -> macsys 100 MHz -> mac_rx_cdc
  -> Milan 50 MHz -> RX filter -> fabric gPTP first-beat stamp
```

- TX captures PHC time at the first accepted AXIS beat.
- RX captures PHC time at the first accepted tap beat.
- Neither timestamp is a PHY-pad or wire-SFD timestamp.
- TX `tx_sf` is a 512-word, eight-frame store-and-forward buffer.
- Each payload word carries eight bytes in this configuration.
- Its wait depends on frame completion and queued traffic.
- A fixed offset cannot remove variable queueing latency.

Issue [#360](https://github.com/kebag-logic/milan-fpga/issues/360)
tracks the TX timestamp reference-plane defect.
Peer delay alone cannot identify an external inline-device fault.

The retained latency CSRs do not repair this path.
In VERSION `0x0002_0057`, `0x540`/`0x544` are readable, inert scratch:

- `PTP_INGRESS_LAT` and `PTP_EGRESS_LAT` are plain RW shadow words.
- A read returns the last written value.
- No timestamp path consumes them at this VERSION.
- Source: `is_plain_rw` and `shadow_mem` in [`milan_csr`](../../hdl/common/csr/milan_csr.sv).

See the [register map](../reference/REGISTER_MAP.md) and
[timestamp scope note](../../REQUIREMENTS.md#4-time-synchronization-and-timestamping).

## Constraints and verification

Inspect generated constraints for the exact configuration and dependencies.
Clock labels alone do not establish safe data transfer.

- `_CRG` requests exact main-PLL output ratios with `margin=0`.
- It false-paths `sys`↔`milan` and selected audio crossings.
- GMII RXC has an explicit 8 ns input-clock period.
- GMII↔system/Milan paths receive 8 ns datapath-only maximum delays.
- Those asynchronous paths also receive hold-only false paths.
- Do not replace those bounds with blanket clock-group exclusions.
- DDR's 4× clocks remain related PHY timing clocks.
- Audio's explicit two-stage ratios follow the selected plan.

The tracked `constraints/` directory is not a build input:

- [`rgmii.xdc`](../../constraints/rgmii.xdc) carries RGMII and MDIO pin properties only.
- [`ila.xdc`](../../constraints/ila.xdc) is empty.
- No build script or platform file references either file.

For an implemented candidate, inspect these Vivado reports:

```tcl
report_clocks
report_clock_interaction
report_cdc
check_timing
report_timing_summary
```

Check the generated netlist alongside those reports:

- Resolve logical aliases to physical clock nets.
- Trace CPU peripheral, DMA, and DDR interfaces separately.
- Verify every asynchronous multibit path's transfer contract.
- Verify synchronized reset release in each consuming domain.
- Exercise clock stoppage and reset during active transfers.
- Check timestamp capture under MAC backpressure and queued frames.

Record configuration, source/dependency revisions, and implementation settings.
A timing pass is not CDC or gPTP compliance evidence.

The [testing guide](../testing/TESTING.md) defines the required evidence.

## Known gaps

Recorded, not repaired; each has an owner elsewhere.

- **FR-CLK-02 names a clock the design does not use.** The [requirements ledger](../reference/FR_NFR.md) requires a fixed 125 MHz PHC clock. It cites `REQ-PTP-07`, which covers atomic state publication. The reference SoC clocks the PHC from `milan` at 50 MHz. The requirement text and its cross-reference are the gap.
- **FR-CLK-05 requires GMII SFD timestamps.** The same ledger marks it MET. Neither stamp here is a pad or wire-SFD stamp. [#360](https://github.com/kebag-logic/milan-fpga/issues/360) owns the reconciliation.
- **TX timestamps** are taken at the first accepted AXIS beat. That beat precedes a store-and-forward buffer and two crossings. [#360](https://github.com/kebag-logic/milan-fpga/issues/360) owns the reference plane.
- **Source comments carry the 100 MHz guard figures.** They state 21 ms settling and 41 us detection. They sit in `KL_link_guard.sv`, `milan_datapath.sv` and `milan_soc.py`. This configuration runs the guard at 50 MHz. [#374](https://github.com/kebag-logic/milan-fpga/issues/374) owns the comment text.
- **Audio-domain resets are not uniform.** Some audio-clocked processes take `axis_resetn` directly. Others synchronize it locally. MMCM-unlock resets cover the Migen domains, not every RTL register.
- **CPU memory-port crossing evidence is netlist evidence.** LiteX's `clock_domain` label proved nothing; the asynchronous FIFO count did. Any CPU wrapper or bus change needs that measurement again.

## Source index

| Authority | What to inspect |
|---|---|
| [SoC integration](../../sw/litex/milan_soc.py) | `_CRG`, `add_milan_datapath`, `_axis_dp_cdc`, `MilanMAC`, `MilanSoC` |
| [AX7101 platform](../../sw/litex/platforms/alinx_ax7101.py) | Board clock, GMII pads, TDM pins, board input constraint |
| [Example configuration](../../configs/endstation_ax7101_1x1_tdm8.yaml) | System/Milan clocks, PHY choice, audio geometry |
| [Datapath](../../hdl/milan/milan_datapath.sv) | Clock/reset ports, PHC wiring, gPTP taps, selected audio modules |
| [gPTP TX stamp](../../hdl/ieee8021as/gptp_plane/KL_gptp_txstamp.sv) | First-accepted-beat timestamp capture and frame association |
| [gPTP wrapper](../../hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv) | RX timestamp capture and fabric engine clock |
| [Audio actuator](../../hdl/ieee1722/crf/KL_mmcm_drp_servo.sv) | Audio measurement, DRP, phase-command crossing, local resets |
| [TDM master](../../hdl/ieee1722/aaf/KL_tdm_capture_master.sv) | Clock-enable serialization and sample-pair FIFO |
| [Link guard](../../hdl/common/KL_link_guard.sv) | Clock observation and MAC recovery reset sequence |
| [SoC reproducibility](LITEX_SOC.md#7-reproducibility---versions) | Required LiteX/LiteEth/CPU revisions and generated artifacts |

Dependency code also owns important clock/reset details.
Inspect the recorded LiteEth PHY/MAC and generated CPU wrapper.

Do not substitute an arbitrary upstream revision for build evidence.
