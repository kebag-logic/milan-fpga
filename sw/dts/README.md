# `sw/dts/` — device-tree contract (bindings) for the Milan NIC

> **GENERATION RETIRED — 2026-07-26.** The `kl,dma-ether` and `kl,milan-pcm`
> nodes are emitted by **`sw/builder/endstation_builder.py`** (`emit_dt_overlay`)
> from the declarative end-station config in `configs/`. Its output byte-matches
> both deployed trees and is gated by `sw/builder/test_builder.py` gates 19a/19b.
> `milan_dt.py extract` / `gen` now **exit 2 with a pointer**; `validate` stays
> and is the binding check.
>
> **Why, with the numbers.** Fed the *current* deployed build's `csr.json`
> (`build_ax8x8_rxq1fix_eppo`), the old generator emitted **four** reg windows
> with no `phy` (deployed: **five**, `phy` = `0xf0003800`/`0xc` — the MDIO
> bit-bang window `ethtool mdio1` uses), a `dma-rx` size of **0x68** (the
> min/max span of the `milan_dma_rx_*` CSRs) where the deployed trees and the
> driver ABI use **0x40**, a single-string `compatible`, and no `dma-coherent`
> / `kl,rsc-clk-mhz` / PCM node / reserved-memory node. The DT window is a
> **driver ABI constant, not a CSR span**, so no `csr.json`-derived rule can
> produce it — making the old generator agree would mean copying `sw/builder`'s
> window table into a second place, which is the drift class being closed (same
> shape as the 2026-07-22 RMON tie-off and the 2026-07-24 `rx-queues` bug).
> The checked-in `ir/*.json` and `milan-nic.*.dtsi` are two memory-map
> generations stale (`0xf00028xx`) and are kept only as historical artifacts.

What lives here now is the **contract**, not a second implementation: the
bindings, and a checker that holds any overlay to them.

```
 configs/endstation_*.yaml ──endstation_builder──▶ overlay .dtsi ──milan_dt.py validate──▶ dtc + bindings/*.yaml
```

## Contents

- **[Files](#files)** — Which files are still normative and which are wreckage. The two `bindings/*.yaml` and `milan_dt.py validate` are live; the `ir/*.json`, the generated `milan-nic.*.dtsi` and `boards/ax7101.json` are two memory-map generations stale and marked do-not-deploy.
- **[Fully-FPGA flow](#fully-fpga-flow)** — The four commands from end-station config to `.dtb`, and the trick that keeps the binding honest: `validate` also eats a complete deployed `.dts`, so the shipping tree is checked against the same schema.
- **[Adding a new platform](#adding-a-new-platform)** — Short: add the shape to `configs/`, extend the bindings. Worth knowing that `additionalProperties: false` is enforced, so an undeclared property is a hard failure rather than a silent pass.
- **[Notes](#notes)** — The driver caveats, and they are the reason to open this page: the LiteX build splits `csr` and `dma-*` across two windows; both are native-endian `readl`, but the `dma-*` 64-bit `base` has its MS word at the *lower* address, so a native 64-bit access swaps the halves; and the 28-byte sub-page `dma-*` ranges need `devm_ioremap`, not `devm_ioremap_resource`.

## Files

| File | Role |
|------|------|
| [`bindings/kl,dma-ether.yaml`](bindings/kl,dma-ether.yaml) | **normative binding** for the NIC node — rewritten 2026-07-26 against both deployed trees (5 reg windows incl. `phy`, `dma-coherent`, `kl,rsc-clk-mhz`, the two-string `compatible`). |
| [`bindings/kl,milan-pcm.yaml`](bindings/kl,milan-pcm.yaml) | Retired PCM/ALSA binding history (#259); no supported product exposes the `snd-kl-milan` node. |
| [`milan_dt.py`](milan_dt.py) | `validate <dts\|dtsi>` (dtc + binding check, works on an overlay OR a complete tree) and `selftest`. `extract`/`gen` retired. |
| [`milan-dt.schema.json`](milan-dt.schema.json) | IR schema — historical, only the retired generator consumed it. |
| [`boards/ax7101.json`](boards/ax7101.json) | historical board values (carries the wrong `rgmii-id` for a GMII board). |
| [`ir/milan-dt.litex.json`](ir/milan-dt.litex.json) / [`ir/milan-dt.zynq.json`](ir/milan-dt.zynq.json) | historical IRs (stale `0xf00028xx` map). |
| `milan-nic.litex.dtsi` / `milan-nic.zynq.dtsi` | historical generated overlays — **do not deploy**. |
| `milan.dtsi` | deprecated pointer. |

## Fully-FPGA flow

```sh
# 1. node + PCM node + reserved-memory, from the end-station config
python3 sw/builder/endstation_builder.py configs/endstation_ax7101_8x8.yaml

# 2. base tree from LiteX, overlay on top
litex_json2dts_linux build/csr.json > base.dts
python3 sw/dts/milan_dt.py validate <generated>/milan-nic.dtsi
cat <generated>/milan-nic.dtsi >> base.dts
dtc -I dts -O dtb base.dts -o milan.dtb
```

`validate` also accepts a complete deployed `.dts` — that is how the binding is
kept honest:

```sh
python3 sw/dts/milan_dt.py validate <bench-repo>/fpga/dts/milan_ax7101_vexii.dts
python3 sw/dts/milan_dt.py selftest       # negative controls for the checker
```

## Adding a new platform

Add its shape to `configs/` and let `sw/builder/endstation_builder.py` emit the
node; extend the bindings here if the platform needs a property they do not
declare (`additionalProperties: false` is enforced, so an undeclared property is
a hard failure, not a silent pass).

## Notes

- The first two notes below describe the retired IR generator and are kept
  only to explain the historical artifacts in `ir/`.
- IR addresses may be ints or hex strings (`"0x40410000"`) — hand-authored IRs use hex.
- `address_cells` (default 1) controls 32- vs 64-bit `reg` cells; all current platforms
  fit in 32 bits.
- The LiteX build exposes a single aggregate NIC interrupt (`milan_interrupt`, the
  `milan` EventManager); the driver demuxes via `milan_csr` `IRQ_STATUS`. The Zynq IR
  models four discrete GIC lines. Both are valid under the binding (`interrupts` minItems 1).

- **Caveat — on the LiteX build the `csr` and `dma-*` `reg` entries are in two different
  windows** (`0x9000_0000` AXI-Lite vs the `0xf000_0000` LiteX CSR bus). This is *not*
  an issue for the device tree itself — `reg` is a list of independent ranges and the
  driver `ioremap`s each `reg-name` separately, so split/non-contiguous windows are
  normal. It *is* a driver caveat in two ways:
  1. **Different register layout per window.** Both windows are **native-endian** 32-bit
     MMIO (`readl`/`writel` — do *not* set a `big-endian` node property or use `ioread32be`;
     that would byte-swap and corrupt). The difference is multi-word *word* order: on the
     LiteX `dma-*` window the 64-bit `base` is two 32-bit words with the **MS word at the
     lower address** (`config_csr_ordering_big` = word order, not byte order), so a native
     64-bit access to `base` swaps its halves → wrong DMA address. Full detail in
     [`../../docs/reference/REGISTER_MAP.md`](../../docs/reference/REGISTER_MAP.md) → DMA registers.
  2. **The `dma-*` ranges are sub-page (28 B) inside the shared LiteX CSR bus** that
     other LiteX peripherals (uart/timer/soc-controller) also occupy. Map them with
     `devm_ioremap` (non-exclusive), not `devm_ioremap_resource` (which does an exclusive
     `request_mem_region` and can clash with the LiteX soc-controller/syscon); or map the
     whole `milan_dma` block once. On Zynq the DMA was a standalone plain-MMIO `axi_dma`
     block, so neither point applies there — the caveat is LiteX-specific.
