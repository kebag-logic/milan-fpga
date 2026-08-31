# System integrator guide

Use this path when embedding the datapath.

## Contents

- **[Understand the boundary](#understand-the-boundary)** — Identify every required interface.
- **[Connect clocks and reset](#connect-clocks-and-reset)** — Preserve documented domain assumptions.
- **[Follow boot order](#follow-boot-order)** — Load state before enabling protocols.
- **[Verify integration](#verify-integration)** — Prove real wiring and failures.

## Understand the boundary

`milan_datapath` is the primary integration boundary.

```mermaid
flowchart LR
    CPU[RV32I firmware] --> CSR[AXI4-Lite CSR]
    DMA[Memory engines] <--> DP[milan_datapath]
    CSR --> DP
    DP <--> MAC[Ethernet MAC]
    DP --> IRQ[Interrupt controller]
    DP <--> DESC[Descriptor memory]
    DP <--> RESP[Response memory]
    DP --> PCM[PCM DMA]
    DP <--> PLAY[Playback memory]
    DP <--> AUDIO[Audio interfaces]
    DP --> IDENTIFY[Identify output]
    DP <--> MMCM[MMCM controls]
```

<!-- solution-memory-faces:start -->
| Interface group | RTL prefix | Direction | Integration responsibility |
|---|---|---|---|
| Clocks and resets | `axis_*`, `gtx_*`, `clk_*` | Host to datapath | Preserve declared domains and sequencing |
| AXI4-Lite CSR | `s_axi_*` | Host to datapath | Map the stable CSR window |
| TX DMA stream | `s_axis_tx_*` | Memory to datapath | Preserve AXI-Stream handshakes |
| RX DMA stream | `m_axis_rx_*` | Datapath to memory | Accept complete frames safely |
| Timestamp stream | `m_axis_ts_*` | Datapath to memory | Drain metadata without loss |
| PCM DMA stream | `m_axis_pcm_*` | Datapath to memory | Preserve stream identity and framing |
| MAC streams | `m_axis_mac_tx_*`, `s_axis_mac_rx_*` | Bidirectional | Preserve final-boundary backpressure |
| Descriptor memory | `desc_mem_*` | Datapath read master | Serve the generated entity image |
| Response memory | `resp_mem_*` | Datapath read-write master | Complete every accepted operation |
| Playback memory | `pb_mem_*` | Datapath read master | Serve PCM ring fetches |
| MAC control and status | `o_mac_*`, `i_mac_*` | Bidirectional | Provide honest capabilities and controls |
| Interrupt | `o_irq_*` | Datapath to host | Route and acknowledge events |
| Identify output | `o_identify` | Datapath to board | Route the requested visual indication |
| MMCM controls | `o_mmcm_*`, `i_mmcm_*` | Bidirectional | Bridge DRP and phase-shift handshakes |
| Audio pins | `i2s_*`, `tdm_*` | Bidirectional | Match selected interface geometry |
<!-- solution-memory-faces:end -->

Read the existing [integration contract](../integration/INTEGRATION_GUIDE.md).

Read the stable [register map](../reference/REGISTER_MAP.md).

## Connect clocks and reset

- Identify every clock source.
- Keep domain names explicit.
- Use approved crossing primitives.
- Constrain asynchronous paths deliberately.
- Sequence reset release correctly.
- Preserve resetless liveness observers.
- Never add direct cross-domain assignments.

Use the generated [CDC census](../diagrams/cdc_census.svg).

Use the [CDC handshake timing](../diagrams/wd_cdc_handshake.svg).

## Follow boot order

```mermaid
sequenceDiagram
    participant Host as Host operator
    participant Boot as Boot firmware
    participant Memory as Shared memory
    participant CSR as Milan CSR
    participant Entity as Protocol plane
    Boot->>CSR: Verify CSR identity
    Boot->>CSR: Disable entity operation
    Boot->>CSR: Configure fabric controls
    Boot->>Memory: Load descriptor image
    Boot->>Memory: Verify image checksum
    Boot->>Entity: Enable verified entity
    Host->>Boot: Run milan_status
    Boot->>CSR: Read live status
    CSR-->>Boot: Return status registers
    Boot-->>Host: Print explicit status
```

- Verify CSR identity first.
- Disable entity operation before configuration.
- Configure generated fabric values.
- Load the descriptor image afterward.
- Verify its checksum before advertising.
- Enable only the verified entity.
- Confirm live status afterward.
- gPTP remains independent from entity enablement.

Missing memory bridges cause misleading protocol failures.

Never tie response interfaces silently.

## Verify integration

- Read the identification register.
- Confirm the reported version.
- Exercise one CSR write.
- Read that value back.
- Send one frame each direction.
- Apply downstream backpressure.
- Reset during active traffic.
- Stall descriptor memory.
- Stall response memory.
- Verify timeout behavior.
- Confirm interrupt clearing.
- Run the integrated Verilator suite.

```sh
make -C tb/verilator/milan_dp
```

Activate the documented [LiteX environment](../litex/LITEX_SOC.md#7-reproducibility---versions).

```sh
python3 sw/litex/test_pp_mem_bridge.py
python3 sw/litex/test_pp_boot_bus_freeze.py
```

The raw harness cannot prove SoC bridge wiring.

Run SoC evidence after every bridge change.

Read the complete [simulation procedure](../testing/SIMULATION.md#section-33-the-scripted-path-used-to-capture-the-evidence).

Build the softcore simulator once.

```sh
python3 sw/litex/milan_sim.py --xlen 32 --non-interactive \
  --output-dir build_milan_sim
```

Press Ctrl-C after the first `litex>` prompt.

Run the cached simulator with scripted input.

```sh
cd build_milan_sim/gateware
{ sleep 4; printf 'mem_read 0x90000000 16\n'; sleep 5; } \
  | ./obj_dir/Vsim | tee /tmp/milan-id.log
grep -F '4e 4c 49 4d' /tmp/milan-id.log
```

The byte sequence proves the `MILN` identification word.

Then run the required complete gates.
