# LiteX ecosystem patches

`apply.sh` applies the small product-required deltas to the active LiteX
environment. It discovers each source tree through the selected Python
interpreter and is safe to run again after dependency updates.

The series contains:

- `0002-liteeth-gmii-tx-clk-invert.patch`: expose the AX7101 GMII transmit
  clock phase control used by `milan_soc.py --gtx-tx-invert`.
- `0007-liteeth-gmii-rx-capture.patch`: capture RX pads without reset.
  Sample reset alongside data and valid, then mask their outputs.
  This preserves synchronous reset behavior and the existing latency.
  Reset logic cannot precede the input flops through control-set remapping.
  RX-error remains unused; MII has no required RX IOB capture.
- `0004-vexiiriscv-baremetal-variant.patch`: add the cacheless, machine-mode
  RV32I Vexii variant and publish an MMU constant only when one exists.
- `0005-vexiiriscv-cacheless-litex.patch`: connect the cacheless instruction and
  data buses plus the dedicated protocol-memory port to the LiteX bus fabric.
- `0006-bios-dispatch-hook.patch`: call a weak product hook after every
  console line, before parsing built-in, unknown or empty input.
  Bare-metal firmware overrides it for heartbeat and PHY service.
  Its required link marker rejects firmware builds missing this patch.
  Long built-in bodies still need their own internal service opportunities.

Usage:

```sh
./apply.sh
./apply.sh --reverse
PYTHON=/path/to/venv/bin/python3 ./apply.sh
```

If an upstream revision changes a patched hunk, `apply.sh` stops at that patch.
Refresh the diff against the newly pinned source tree, then rerun the builder's
toolchain-patch gate before committing it.

At any re-pin of LiteX or of the VexiiRiscv generator, also run the split
CPU's region-decode checks (#791), from the repository root, with the
prerequisites in `tb/verilator/ctrl_region_decode/README.md`. The split SoC's
exact fetch and load decode depends on LiteX's VexiiRiscv naming its netlist
through its own naming step and generating it from the region list that step
leaves, which `sw/litex/test_ctrl_memory.py` grades on a stand-in CPU and on
the split export. `tb/verilator/ctrl_region_decode` runs the generated CPU at
each region's edges and reads its decode at every address; no workflow runs
it:

```sh
python3 sw/litex/test_ctrl_memory.py
python3 -B tb/verilator/ctrl_region_decode/run.py --build-dir /tmp/region-decode-self --self-test
```

If the series text changes without an upstream change - `0005` had a
comment-only rewrite on 2026-08-30 - a tree patched with the previous text can
neither reverse the new patch nor take it again, and gate 23h reports that tree
as not upstream plus this series. Migrate such a tree by reversing the previous
text first, then applying the current series (run from this directory):

```sh
old=$(git log -1 --format=%H --diff-filter=M -- 0005-vexiiriscv-cacheless-litex.patch)~1
tree=$(python3 -c 'import pythondata_cpu_vexiiriscv as m, os; print(os.path.dirname(os.path.dirname(m.__file__)))')
git show "$old:sw/litex/patches/0005-vexiiriscv-cacheless-litex.patch" | git -C "$tree" apply --reverse
./apply.sh
```

A fresh environment (`scripts/ci_litex_env.py`, the one CI builds) needs no
migration.
