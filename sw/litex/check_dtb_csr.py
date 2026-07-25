#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
#
# check_dtb_csr.py <dtb-or-dts> <csr.csv>  — refuse a stale device tree at flash time.
#
# The kl-eth driver maps its kl,dma-ether reg windows BY INDEX, so a device tree
# compiled against an older CSR layout lands every host-DMA register access on a
# wrong-but-writable CSR: readback matches what was written, the ring/ts engines
# never arm, and host TX+RX are dead at the wire while the fabric plane streams
# fine (silicon post-mortem 2026-07-25, a July-5 dtb flashed onto a July-25 SoC).
#
# Window contract checked against the build's csr.csv:
#   reg[0]  the Milan CSR block (contains 0x90000000)
#   reg[1]  contains milan_dma_tx_base  and milan_dma_tx_bd_base
#   reg[2]  contains milan_dma_rx_base  and milan_dma_rx_bd_base
#   reg[3]  contains milan_dma_ts_base
#   kl,milan-pcm reg[0] == milan_dma_pcm_base   (when both sides have it)
#
# Exit 0 = every applicable check passed; exit 1 = mismatch (stale dtb); exit 2 = usage.
import csv
import tempfile
import re
import subprocess
import sys

MILAN_CSR_BASE = 0x9000_0000


def decompile(path):
    """Return normalized device-tree source text for a .dtb or .dts input."""
    with open(path, "rb") as f:
        magic = f.read(4)
    if magic != b"\xd0\x0d\xfe\xed":
        # dts source: compile first so multi-group `reg = <..>, <..>` and
        # include/label sugar come back as one flat cell list.
        with tempfile.NamedTemporaryFile(suffix=".dtb") as tmp:
            out = subprocess.run(["dtc", "-I", "dts", "-O", "dtb", "-o", tmp.name, path],
                                 capture_output=True, text=True)
            if out.returncode != 0:
                sys.exit("check_dtb_csr: dtc failed on %s: %s" % (path, out.stderr.strip()))
            return decompile(tmp.name)
    out = subprocess.run(["dtc", "-I", "dtb", "-O", "dts", path],
                         capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit("check_dtb_csr: dtc failed on %s: %s" % (path, out.stderr.strip()))
    return out.stdout


def node_reg_cells(dts, compatible):
    """reg cells (list of ints) of the first node whose compatible mentions `compatible`."""
    # Node bodies with up to one level of child nodes (e.g. a future mdio child).
    for m in re.finditer(r"\{((?:[^{}]|\{[^{}]*\})*)\}", dts, re.S):
        body = re.sub(r"\{[^{}]*\}", "", m.group(1))  # drop child bodies
        if compatible not in body:
            continue
        r = re.search(r"\breg\s*=\s*([^;]*);", body)
        if r:
            return [int(c, 0) for c in re.findall(r"0x[0-9a-fA-F]+|\b\d+\b", r.group(1))]
    return None


def csr_registers(path):
    regs = {}
    with open(path, newline="") as f:
        for row in csv.reader(f):
            if len(row) >= 3 and row[0] == "csr_register":
                regs[row[1]] = int(row[2], 0)
    return regs


def contains(win, addr):
    off, ln = win
    return off <= addr < off + ln


def main():
    if len(sys.argv) != 3:
        sys.exit(2)
    dts = decompile(sys.argv[1])
    regs = csr_registers(sys.argv[2])

    cells = node_reg_cells(dts, "kl,dma-ether")
    if cells is None:
        sys.exit("check_dtb_csr: no kl,dma-ether node in %s" % sys.argv[1])
    wins = [(cells[i], cells[i + 1]) for i in range(0, len(cells) - 1, 2)]

    # (window index, csr.csv register names that must fall inside it)
    contract = [
        (0, []),  # Milan CSR block, checked against the fixed base below
        (1, ["milan_dma_tx_base", "milan_dma_tx_bd_base"]),
        (2, ["milan_dma_rx_base", "milan_dma_rx_bd_base"]),
        (3, ["milan_dma_ts_base"]),
    ]
    bad = []
    if len(wins) <= max(i for i, _ in contract):
        bad.append("kl,dma-ether has %d reg windows, contract needs %d"
                   % (len(wins), max(i for i, _ in contract) + 1))
        wins += [(0, 0)] * 8
    if not contains(wins[0], MILAN_CSR_BASE):
        bad.append("reg[0] %s does not cover the Milan CSR base 0x%x"
                   % (wins[0], MILAN_CSR_BASE))
    for idx, names in contract[1:]:
        for name in names:
            if name not in regs:
                bad.append("csr.csv is missing %s (wrong csr.csv?)" % name)
            elif not contains(wins[idx], regs[name]):
                bad.append("reg[%d] 0x%x/+0x%x does not cover %s @ 0x%x"
                           % (idx, wins[idx][0], wins[idx][1], name, regs[name]))

    pcm = node_reg_cells(dts, "kl,milan-pcm")
    if pcm and "milan_dma_pcm_base" in regs and pcm[0] != regs["milan_dma_pcm_base"]:
        bad.append("kl,milan-pcm reg[0] 0x%x != milan_dma_pcm_base 0x%x"
                   % (pcm[0], regs["milan_dma_pcm_base"]))

    if bad:
        print("check_dtb_csr: STALE device tree vs %s:" % sys.argv[2])
        for b in bad:
            print("  - " + b)
        sys.exit(1)
    print("check_dtb_csr: OK — %s windows match %s" % (sys.argv[1], sys.argv[2]))


if __name__ == "__main__":
    main()
