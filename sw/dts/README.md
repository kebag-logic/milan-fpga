# `sw/dts/` — platform-convergent device tree for the Milan NIC

The `kl,dma-ether` device-tree node splits into an **invariant contract** (compatible,
`reg-names`/`interrupt-names` ordering, `kl,txq-cnt`/`kl,shaped-queues`, `phy-mode`,
`kl,ptp`, sizes) and a few **platform holes** (reg bases, IRQ number(s),
`interrupt-parent`, phy-handle/reset, mac address). The addresses differ completely
per host — csr `0x9000_0000` + DMA `0xf0002800` on the fully-FPGA LiteX build vs csr
`0x43c00000` + DMA `0x40410000` on Zynq — and the interrupt *model* differs too (LiteX
has ONE aggregate PLIC line; Zynq has four GIC lines).

So the overlay is **generated** from a small, platform-neutral **intermediate
representation (IR) JSON**. The invariant part lives once in the generator; each
platform provides only its IR. Adding a future SoC never touches the generator, the
schema, or the binding.

```
 platform build ──extract──▶ ir/milan-dt.<plat>.json ──gen──▶ milan-nic.<plat>.dtsi ──validate──▶ overlay onto base .dts
   (LiteX csr.json /            (canonical IR;                  (invariant template)     (dtc + binding)
    hand for Zynq)               schema: milan-dt.schema.json)
```

## Files

| File | Role |
|------|------|
| [`milan_dt.py`](milan_dt.py) | the tool: `extract` (csr.json → IR), `gen` (IR → `.dtsi`), `validate` (dtc). |
| [`milan-dt.schema.json`](milan-dt.schema.json) | JSON Schema for the IR (the stable, platform-neutral contract). |
| [`boards/ax7101.json`](boards/ax7101.json) | board values not in the gateware (mac, phy addr, reset-gpio, shaped-queues, ptp, intc label). |
| [`ir/milan-dt.litex.json`](ir/milan-dt.litex.json) | LiteX/NaxRiscv IR — **extracted from a `--full` build's `csr.json`**. |
| [`ir/milan-dt.zynq.json`](ir/milan-dt.zynq.json) | Zynq-7000 IR — hand-authored (demonstrates convergence). |
| `milan-nic.litex.dtsi` / `milan-nic.zynq.dtsi` | **generated** overlays (do not edit; edit the IR + regenerate). |
| [`bindings/kl,dma-ether.yaml`](bindings/kl,dma-ether.yaml) | normative binding — the validation oracle. |
| `milan.dtsi` | deprecated pointer to the generated files. |

## Fully-FPGA flow (FR-DT-08)

```sh
# 1. build the SoC with the CSR JSON exported
./../litex/milan_soc.py --full --csr-json build/csr.json     # (or any --full build dir)

# 2. base tree from LiteX, then the NIC overlay from the same csr.json
litex_json2dts_linux build/csr.json > base.dts
./milan_dt.py extract --platform litex build/csr.json --board boards/ax7101.json > ir/milan-dt.litex.json
./milan_dt.py gen ir/milan-dt.litex.json > milan-nic.litex.dtsi
./milan_dt.py validate milan-nic.litex.dtsi

# 3. overlay + compile
cat milan-nic.litex.dtsi >> base.dts
dtc -I dts -O dtb base.dts -o milan.dtb
```

For Zynq, the base tree comes from the Vivado export (the retired `device-tree-xlnx`
path) and the overlay from `gen ir/milan-dt.zynq.json`.

## Adding a new platform (the convergence contract)

1. Produce an IR JSON that conforms to [`milan-dt.schema.json`](milan-dt.schema.json):
   fill `reg` (csr + dma-tx/rx/ts base+size), `interrupts` (a list — one `{name,num}`
   for a single-cell PLIC line, or `{name,cells:[…]}` for a multi-cell GIC line),
   `interrupt_parent`, and the board bits (`phy`, `mac_address`, `ptp`, `queues`).
   - If the platform emits a LiteX-style `csr.json`, reuse `extract --platform litex`.
   - Otherwise write a small extractor (or hand-author the IR, like the Zynq one).
2. `./milan_dt.py gen ir/milan-dt.<plat>.json > milan-nic.<plat>.dtsi` and `validate`.

The generator, schema, and binding are unchanged — that is the point.

## Notes

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
     [`../../docs/REGISTER_MAP.md`](../../docs/reference/REGISTER_MAP.md) → DMA registers.
  2. **The `dma-*` ranges are sub-page (28 B) inside the shared LiteX CSR bus** that
     other LiteX peripherals (uart/timer/soc-controller) also occupy. Map them with
     `devm_ioremap` (non-exclusive), not `devm_ioremap_resource` (which does an exclusive
     `request_mem_region` and can clash with the LiteX soc-controller/syscon); or map the
     whole `milan_dma` block once. On Zynq the DMA was a standalone plain-MMIO `axi_dma`
     block, so neither point applies there — the caveat is LiteX-specific.
