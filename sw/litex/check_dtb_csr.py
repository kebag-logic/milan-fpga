#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
#
# check_dtb_csr.py [--expected-xlen 32|64] <dtb-or-dts> <csr.csv>
# — refuse a stale or wrong-architecture device tree at flash time.
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
#   kl,milan-pcm reg[0] covers every milan_dma_pcm_* register (when present)
#   kl,milan-pcm reg[2] covers every milan_dma_pb_* register (when present)
#   litex,spiflash reg[0] == the csr.csv spiflash bank base (when both have it)
# With --expected-xlen, every cpu@N node must also carry the matching
# riscv,isa width and Linux MMU type (RV32/sv32 or RV64/sv39).  This applies to
# a standalone DTB and to the FDT carved from an OpenSBI fw_jump binary.
#
# Exit 0 = every applicable check passed; exit 1 = mismatch (stale dtb); exit 2 = usage.
import argparse
import csv
import tempfile
import re
import subprocess
import sys

MILAN_CSR_BASE = 0x9000_0000


FDT_MAGIC = b"\xd0\x0d\xfe\xed"


def decompile(path):
    """Normalized dts text for a .dts, a .dtb, or ANY binary embedding an FDT.

    The embedded case is the one that matters most: the LiteX BIOS jumps to
    OpenSBI with a1=0, so the fdt OpenSBI carries (FW_FDT_PATH) is the ONLY
    device tree the kernel ever sees - the flash "dtb" slot is decorative on
    this boot path. Gate the opensbi image, not just the slot file.
    """
    blob = open(path, "rb").read()
    off = blob.find(FDT_MAGIC)
    if off < 0:
        # dts source: compile first so multi-group `reg = <..>, <..>` and
        # include/label sugar come back as one flat cell list.
        with tempfile.NamedTemporaryFile(suffix=".dtb") as tmp:
            out = subprocess.run(["dtc", "-I", "dts", "-O", "dtb", "-o", tmp.name, path],
                                 capture_output=True, text=True)
            if out.returncode != 0:
                sys.exit("check_dtb_csr: dtc failed on %s: %s" % (path, out.stderr.strip()))
            return decompile(tmp.name)
    size = int.from_bytes(blob[off + 4:off + 8], "big")
    if off > 0:
        print("check_dtb_csr: using the FDT embedded at +0x%x in %s (%d B)"
              % (off, path, size))
    with tempfile.NamedTemporaryFile(suffix=".dtb") as tmp:
        tmp.write(blob[off:off + size])
        tmp.flush()
        out = subprocess.run(["dtc", "-I", "dtb", "-O", "dts", tmp.name],
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


def node_reg_after_compatible(dts, compatible):
    """reg cells of the node that declares `compatible`, for DEEP nodes.

    ``node_reg_cells`` above scans balanced bodies and tolerates ONE level of
    children; the LiteSPI node is three deep (``spiflash`` > ``flash@0`` >
    ``partitions`` > ``partition@N``) so that scanner never sees it and
    silently returns None - a gate that quietly checks nothing.  This one
    anchors on the compatible string and takes the first ``reg`` that follows
    it BEFORE any child node opens, which is by construction the node's own.
    """
    m = re.search(r'compatible\s*=\s*[^;]*"%s"[^;]*;' % re.escape(compatible), dts)
    if not m:
        return None
    tail = dts[m.end():]
    stop = tail.find("{")
    r = re.search(r"\breg\s*=\s*([^;]*);", tail if stop < 0 else tail[:stop])
    if not r:
        return None
    return [int(c, 0) for c in re.findall(r"0x[0-9a-fA-F]+|\b\d+\b", r.group(1))]


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


def prefixed_window_errors(regs, prefix, win, label):
    """Return every CSR named by ``prefix`` that lies outside ``win``.

    Checking only the first register proves the base but not the size.  A
    shortened DT window still lets the driver map the first word while later
    capability/status registers fall outside the resource it was given.
    """
    return [
        "%s 0x%x/+0x%x does not cover %s @ 0x%x"
        % (label, win[0], win[1], name, addr)
        for name, addr in sorted(regs.items())
        if name.startswith(prefix) and not contains(win, addr)
    ]


def _property_strings(text, name):
    """Return every quoted string in assignments to one exact DTS property."""
    values = []
    pattern = r"(?:^|\s)%s\s*=\s*([^;]*);" % re.escape(name)
    for match in re.finditer(pattern, text, re.M):
        values.extend(re.findall(r'"([^"]*)"', match.group(1)))
    return values


def cpu_identity_errors(dts, expected_xlen):
    """Return CPU ISA/MMU mismatches for the requested Linux boot width."""
    if expected_xlen not in (32, 64):
        raise ValueError("expected_xlen must be 32 or 64")
    # DTC flattens labels but preserves cpu@N nodes.  Permit one nested child
    # (the per-hart interrupt-controller) while keeping each CPU's properties
    # scoped to that node rather than accepting an unrelated global string.
    node_re = re.compile(
        r"(?:^|\s)cpu@[^\s{]+\s*\{((?:[^{}]|\{[^{}]*\})*)\};", re.S)
    cpus = list(node_re.finditer(dts))
    if not cpus:
        return ["device tree has no cpu@N node to prove its RISC-V width"]

    wanted_isa = f"rv{expected_xlen}"
    wanted_mmu = {32: "riscv,sv32", 64: "riscv,sv39"}[expected_xlen]
    bad = []
    for index, match in enumerate(cpus):
        body = match.group(1)
        isa = _property_strings(body, "riscv,isa")
        if not isa:
            isa = _property_strings(body, "riscv,isa-base")
        if len(isa) != 1:
            bad.append(
                f"cpu[{index}] needs exactly one riscv,isa/riscv,isa-base string")
        elif not isa[0].lower().startswith(wanted_isa):
            bad.append(
                f"cpu[{index}] ISA {isa[0]!r} is not {wanted_isa} for the "
                f"compiled RV{expected_xlen} SoC")

        mmu = _property_strings(body, "mmu-type")
        if len(mmu) != 1:
            bad.append(f"cpu[{index}] needs exactly one mmu-type string")
        elif mmu[0].lower() != wanted_mmu:
            bad.append(
                f"cpu[{index}] mmu-type {mmu[0]!r} is not {wanted_mmu!r} "
                f"for the compiled RV{expected_xlen} SoC")
    return bad


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-xlen", type=int, choices=(32, 64))
    parser.add_argument("artifact")
    parser.add_argument("csr_csv")
    args = parser.parse_args(argv)
    dts = decompile(args.artifact)
    regs = csr_registers(args.csr_csv)

    cells = node_reg_cells(dts, "kl,dma-ether")
    if cells is None:
        sys.exit("check_dtb_csr: no kl,dma-ether node in %s" % args.artifact)
    wins = [(cells[i], cells[i + 1]) for i in range(0, len(cells) - 1, 2)]

    # (window index, csr.csv register names that must fall inside it)
    contract = [
        (0, []),  # Milan CSR block, checked against the fixed base below
        (1, ["milan_dma_tx_base", "milan_dma_tx_bd_base"]),
        (2, ["milan_dma_rx_base", "milan_dma_rx_bd_base"]),
        (3, ["milan_dma_ts_base"]),
    ]
    bad = (cpu_identity_errors(dts, args.expected_xlen)
           if args.expected_xlen is not None else [])
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
    if pcm and len(pcm) >= 2:
        bad += prefixed_window_errors(
            regs, "milan_dma_pcm_", (pcm[0], pcm[1]),
            "kl,milan-pcm reg[0]")
    # task #31 playback window: kl,milan-pcm reg[2] must BE the pb CSR block
    # (first register = milan_dma_pb_cap). Checked whenever both sides carry
    # it; a DT with a pb-dma window against a gateware without the block (or
    # vice versa) is the same stale-dtb corruption class as the kl-eth case.
    if pcm and len(pcm) >= 6 and "milan_dma_pb_cap" not in regs:
        bad.append("kl,milan-pcm declares a pb-dma window but csr.csv has no "
                   "milan_dma_pb_cap (gateware built without --aaf-playback?)")
    if pcm and len(pcm) >= 6 and "milan_dma_pb_cap" in regs \
       and pcm[4] != regs["milan_dma_pb_cap"]:
        bad.append("kl,milan-pcm reg[2] 0x%x != milan_dma_pb_cap 0x%x"
                   % (pcm[4], regs["milan_dma_pb_cap"]))
    if pcm and len(pcm) >= 6:
        bad += prefixed_window_errors(
            regs, "milan_dma_pb_", (pcm[4], pcm[5]),
            "kl,milan-pcm reg[2]")
    if pcm and len(pcm) < 6 and "milan_dma_pb_cap" in regs:
        bad.append("gateware has the playback CSR block (milan_dma_pb_cap) "
                   "but kl,milan-pcm has no pb-dma reg window")

    # litex,spiflash: the LiteSPI bank base.  Same stale-window failure class
    # as kl,dma-ether above, and worse in one way - the LiteSPI MASTER port at
    # bank+0x10 is a WRITE path to the boot flash.  A device tree naming the
    # wrong bank points every future mtd/spi-nor driver at whatever CSRs
    # actually live there (on the AX7101 map, `sdram`), and it is the same
    # window `acmp-persist` writes saved bindings through.  This node was
    # added by hand rather than regenerated from a build's csr.json, so it is
    # exactly the case the gate exists for.  Checked whenever both sides carry
    # it; absent on either side is not an error (builds without --with-spiflash
    # have no bank, and older trees have no node).
    spi = node_reg_after_compatible(dts, "litex,spiflash")
    if spi and "spiflash_master_cs" in regs:
        base = regs["spiflash_master_cs"] - 0x10   # master block is bank+0x10
        win = (spi[0], spi[1] if len(spi) > 1 else 0)
        if spi[0] != base:
            bad.append("litex,spiflash reg[0] 0x%x != the csr.csv spiflash "
                       "bank base 0x%x (spiflash_master_cs 0x%x - 0x10)"
                       % (spi[0], base, regs["spiflash_master_cs"]))
        elif not contains(win, regs["spiflash_master_cs"]):
            bad.append("litex,spiflash reg[0] 0x%x/+0x%x does not cover "
                       "spiflash_master_cs @ 0x%x"
                       % (win[0], win[1], regs["spiflash_master_cs"]))

    if bad:
        print("check_dtb_csr: STALE device tree vs %s:" % args.csr_csv)
        for b in bad:
            print("  - " + b)
        sys.exit(1)
    arch = (f" and CPU identity is RV{args.expected_xlen}"
            if args.expected_xlen is not None else "")
    print("check_dtb_csr: OK — %s windows match %s%s"
          % (args.artifact, args.csr_csv, arch))


if __name__ == "__main__":
    main()
