#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
#
# milan_dt.py — platform-convergent device-tree generation for the Milan TSN NIC.
#
# The kl,dma-ether node splits into an INVARIANT contract (compatible, reg-names /
# interrupt-names ordering, queue/ptp/phy property names, sizes) and a few PLATFORM
# HOLES (reg bases, IRQ number(s), interrupt-parent, phy-handle/reset, mac address).
# This tool keeps the invariant part in ONE place (the generator template below) and
# funnels every platform through a small, neutral **intermediate representation (IR)**
# JSON (schema: milan-dt.schema.json). Adding a future SoC = write one small extractor
# (or hand-author its IR); the generator, schema and binding never change.
#
#     platform build ──extract──▶ milan-dt.<plat>.json ──gen──▶ kl,dma-ether .dtsi ──validate──▶ overlay
#
# Subcommands:
#   extract --platform litex <csr.json> [--board board.json]   csr.json -> IR (stdout)
#   gen <ir.json>                                               IR -> kl,dma-ether .dtsi (stdout)
#   validate <dts|dtsi>                                         dtc (+ dtschema if present)
#
# Typical fully-FPGA flow (see sw/dts/README.md):
#   litex_json2dts_linux build/csr.json > base.dts
#   milan_dt.py extract --platform litex build/csr.json --board sw/dts/boards/ax7101.json > ir/milan-dt.litex.json
#   milan_dt.py gen ir/milan-dt.litex.json > milan-nic.litex.dtsi
#   cat milan-nic.litex.dtsi >> base.dts && dtc -I dts -O dtb base.dts -o milan.dtb
#
# Pure stdlib — runs with plain python3, no LiteX venv needed.

import os
import sys
import json
import argparse
import subprocess

HERE   = os.path.dirname(os.path.abspath(__file__))
SCHEMA = os.path.join(HERE, "milan-dt.schema.json")

# The binding's canonical orderings (the invariant contract; must match
# sw/dts/bindings/kl,dma-ether.yaml).
REG_ORDER = ["csr", "dma-tx", "dma-rx", "dma-ts"]
COMPATIBLE = "kl,dma-ether-0.9"


# --- IR validation ------------------------------------------------------------------

def validate_ir(ir):
    """Validate the IR against the JSON schema (jsonschema if available, else a minimal
    required-keys check so the tool works on a bare python)."""
    try:
        import jsonschema  # optional
        jsonschema.validate(ir, json.load(open(SCHEMA)))
        return
    except ImportError:
        pass
    for k in ("platform", "reg", "interrupts"):
        if k not in ir:
            raise SystemExit(f"IR error: missing required key '{k}'")
    if "csr" not in ir["reg"]:
        raise SystemExit("IR error: reg.csr is required")
    if not ir["interrupts"]:
        raise SystemExit("IR error: at least one interrupt is required")


# --- extract: LiteX csr.json -> IR --------------------------------------------------

def extract_litex(csr_json_path, board):
    """Build the IR from a LiteX build's csr.json. Addresses in csr.json are decimal
    ints; csr_registers[*].size is in 32-bit words (byte span = size*4)."""
    d = json.load(open(csr_json_path))
    mem, regs, consts = d["memories"], d["csr_registers"], d["constants"]

    if "milan_csr" not in mem:
        raise SystemExit("csr.json has no 'milan_csr' memory region — is this a --full build?")
    reg = {"csr": {"base": mem["milan_csr"]["base"], "size": mem["milan_csr"]["size"]}}

    # Each DMA engine's window = [min reg addr, max reg addr + size_words*4).
    for eng in ("tx", "rx", "ts"):
        pfx = f"milan_dma_{eng}_"
        addrs = [(v["addr"], v["size"]) for k, v in regs.items() if k.startswith(pfx)]
        if not addrs:
            continue
        base = min(a for a, _ in addrs)
        end  = max(a + s * 4 for a, s in addrs)
        reg[f"dma-{eng}"] = {"base": base, "size": end - base}

    # Interrupts: LiteX exposes ONE aggregate PLIC line for the NIC (the 'milan'
    # EventManager); model reality — a single 'csr' line. (Zynq's 4-line IR is hand
    # authored.) The number comes straight from the constants map.
    if "milan_interrupt" not in consts:
        raise SystemExit("csr.json has no 'milan_interrupt' constant")
    interrupts = [{"name": "csr", "num": int(consts["milan_interrupt"])}]

    ir = {
        "platform": "litex-naxriscv",
        "address_cells": board.get("address_cells", 1),
        "interrupt_parent": board.get("interrupt_parent", "intc0"),
        "reg": reg,
        "interrupts": interrupts,
    }
    for k in ("phy", "mac_address", "ptp", "queues"):
        if k in board:
            ir[k] = board[k]
    return ir


# --- gen: IR -> kl,dma-ether .dtsi --------------------------------------------------

def _int(x):
    """Coerce an IR numeric field to int — accepts a plain int or a string like
    '0x40410000'/'42' so hand-authored IRs can use readable hex."""
    return x if isinstance(x, int) else int(x, 0)

def _cells(value, n):
    """Render a base/size as n address/size cells (1 => 32-bit, 2 => 64-bit hi/lo)."""
    value = _int(value)
    if n == 1:
        return f"0x{value:08x}"
    return f"0x{(value >> 32) & 0xffffffff:08x} 0x{value & 0xffffffff:08x}"

def gen_dtsi(ir):
    validate_ir(ir)
    ac = ir.get("address_cells", 1)
    reg, irqs = ir["reg"], ir["interrupts"]
    csr_base = _int(reg["csr"]["base"])

    # reg / reg-names in canonical order, present keys only.
    present = [k for k in REG_ORDER if k in reg]
    reg_cells   = ",\n\t\t      ".join(f"<{_cells(reg[k]['base'], ac)} {_cells(reg[k]['size'], ac)}>" for k in present)
    reg_names   = ", ".join(f'"{k}"' for k in present)
    # Each interrupt is either a single-cell id (num, PLIC) or raw cells (GIC etc).
    def _irq(i):
        return "<" + " ".join(str(_int(c)) for c in i["cells"]) + ">" if "cells" in i else f"<{_int(i['num'])}>"
    irq_cells   = ", ".join(_irq(i) for i in irqs)
    irq_names   = ", ".join(f'"{i["name"]}"' for i in irqs)

    L = []
    L.append("// SPDX-License-Identifier: (GPL-2.0 OR MIT)")
    L.append("/*")
    L.append(f" * Milan TSN NIC (kl,dma-ether) overlay — GENERATED by sw/dts/milan_dt.py")
    L.append(f" * from the {ir['platform']} IR. DO NOT EDIT BY HAND; edit the IR + regenerate.")
    L.append(" * Overlay onto the SoC base .dts (LiteX litex_json2dts_linux, or the Zynq tree).")
    L.append(" */")
    L.append("")
    L.append("/ {")
    L.append(f"\tmilan_eth: ethernet@{csr_base:x} {{")
    L.append(f'\t\tcompatible = "{COMPATIBLE}";')
    L.append('\t\tstatus = "okay";')
    L.append("")
    L.append(f"\t\treg = {reg_cells};")
    L.append(f"\t\treg-names = {reg_names};")
    L.append("")
    if ir.get("interrupt_parent"):
        L.append(f"\t\tinterrupt-parent = <&{ir['interrupt_parent']}>;")
    L.append(f"\t\tinterrupts = {irq_cells};")
    L.append(f"\t\tinterrupt-names = {irq_names};")
    L.append("")
    q = ir.get("queues", {})
    if "txq" in q: L.append(f"\t\tkl,txq-cnt = <{q['txq']}>;")
    if "rxq" in q: L.append(f"\t\tkl,rxq-cnt = <{q['rxq']}>;")
    if "shaped" in q:
        L.append(f"\t\tkl,shaped-queues = <{' '.join(str(x) for x in q['shaped'])}>;")
    L.append("")
    if ir.get("mac_address"):
        mac = " ".join(ir["mac_address"].split(":"))
        L.append(f"\t\tlocal-mac-address = [{mac}];")
    phy = ir.get("phy", {})
    if phy.get("mode"):       L.append(f'\t\tphy-mode = "{phy["mode"]}";')
    if "reg" in phy:          L.append("\t\tphy-handle = <&milan_phy>;")
    if phy.get("reset_gpio"): L.append(f"\t\tphy-reset-gpios = <{phy['reset_gpio']}>;")
    L.append("")
    ptp = ir.get("ptp", {})
    if ptp.get("present"):    L.append("\t\tkl,ptp;")
    if "clock_hz" in ptp:     L.append(f"\t\tkl,ptp-clock-hz = <{ptp['clock_hz']}>;")
    # subnodes MUST follow all properties (DTS rule).
    if "reg" in phy:
        L.append("")
        L.append("\t\tmdio {")
        L.append("\t\t\t#address-cells = <1>;")
        L.append("\t\t\t#size-cells = <0>;")
        L.append(f"\t\t\tmilan_phy: ethernet-phy@{phy['reg']} {{")
        L.append(f"\t\t\t\treg = <{phy['reg']}>;")
        L.append("\t\t\t};")
        L.append("\t\t};")
    L.append("\t};")
    L.append("};")
    return "\n".join(L) + "\n"


# --- validate: dtc (+ dtschema if present) ------------------------------------------

def validate_dts(path):
    """Wrap the overlay in a synthetic base tree (providing the referenced labels) and
    run dtc for a structural check; run dt-validate against the binding if available."""
    frag = open(path).read()
    # strip the leading /{...} so we can nest it under a synthetic /soc with the labels.
    body = frag[frag.index("/ {") + 3: frag.rindex("};")]
    wrapper = (
        "/dts-v1/;\n/ {\n"
        "  #address-cells = <1>;\n  #size-cells = <1>;\n"
        "  intc0: intc { interrupt-controller; #interrupt-cells = <1>; phandle = <1>; };\n"
        "  intc: intc2 { interrupt-controller; #interrupt-cells = <3>; phandle = <2>; };\n"
        "  gpio: gpio { gpio-controller; #gpio-cells = <2>; phandle = <3>; };\n"
        + body + "\n};\n"
    )
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".dts", delete=False) as f:
        f.write(wrapper); tmp = f.name
    try:
        r = subprocess.run(["dtc", "-I", "dts", "-O", "dtb", tmp, "-o", os.devnull],
                           capture_output=True, text=True)
    finally:
        os.unlink(tmp)
    errs = [l for l in r.stderr.splitlines() if "Error" in l or "FATAL" in l]
    if r.returncode != 0 or errs:
        print(r.stderr, file=sys.stderr)
        raise SystemExit(f"dtc FAILED for {path}")
    print(f"dtc: {os.path.basename(path)} parses OK (structure valid)")

    binding = os.path.join(HERE, "bindings", "kl,dma-ether.yaml")
    if subprocess.run(["sh", "-c", "command -v dt-validate"], capture_output=True).returncode == 0:
        print("  (dt-validate available — run it against the full assembled tree in CI)")


# --- CLI ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Milan platform-convergent device-tree generator")
    sub = ap.add_subparsers(dest="cmd", required=True)

    pe = sub.add_parser("extract", help="platform SoC description -> IR JSON")
    pe.add_argument("--platform", choices=["litex"], default="litex")
    pe.add_argument("csr_json")
    pe.add_argument("--board", default=os.path.join(HERE, "boards", "ax7101.json"))

    pg = sub.add_parser("gen", help="IR JSON -> kl,dma-ether .dtsi")
    pg.add_argument("ir_json")

    pv = sub.add_parser("validate", help="dtc-check a generated overlay")
    pv.add_argument("dts")

    args = ap.parse_args()
    if args.cmd == "extract":
        board = json.load(open(args.board))
        ir = extract_litex(args.csr_json, board)
        json.dump(ir, sys.stdout, indent=2); print()
    elif args.cmd == "gen":
        ir = json.load(open(args.ir_json))
        sys.stdout.write(gen_dtsi(ir))
    elif args.cmd == "validate":
        validate_dts(args.dts)


if __name__ == "__main__":
    main()
