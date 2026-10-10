#!/usr/bin/env python3
"""Reviewer mutation probes for sw/litex/test_retained_cdc_storage.py.

Usage: pinned_py.sh probe_mutants.py <repo checkout> <scratch dir> <jobs>

Each probe plants one defect into a scratch copy of sw/litex/milan_soc.py
(every other entry of the checkout is symlinked, as the lane test's own
controls do), runs the checkout's lane test against it with --no-controls,
and records which (array, check) verdicts FAIL. A probe is CAUGHT when the
test exits 1 and fails at least one listed expectation. Nothing in the
checkout is modified.
"""
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO, SCRATCH, JOBS = Path(sys.argv[1]).resolve(), Path(sys.argv[2]), int(sys.argv[3])
SOC = REPO / "sw/litex/milan_soc.py"
TEST = REPO / "sw/litex/test_retained_cdc_storage.py"

# (name, product text, planted text, [(array, check) any of which must fail])
PROBES = (
    ("framing-never-written",
     "            array_write.we.eq(write.we),\n",
     "            array_write.we.eq(write.we & (ram_style == \"block\")),\n",
     [("mac_tx", "lockstep"), ("mac_rx", "lockstep"), ("csr_w", "lockstep"), ("csr_r", "lockstep")]),
    ("pieces-order-swapped",
     "        pieces.append(array_read.dat_r)\n",
     "        pieces.insert(0, array_read.dat_r)\n",
     [("mac_tx", "lockstep"), ("mac_rx", "lockstep"), ("csr_w", "lockstep"), ("csr_r", "lockstep")]),
    ("lsb-not-advanced",
     "        lsb += bits\n",
     "        pass\n",
     [("mac_tx", "lockstep"), ("mac_rx", "lockstep"), ("csr_w", "lockstep"), ("csr_r", "lockstep")]),
    ("csr-wrong-channel-aw",
     '    _payload_in_block_ram(by_name["w"])\n',
     '    _payload_in_block_ram(by_name["aw"])\n',
     [("csr_w", "storage"), ("csr_aw", "storage")]),
    ("ram-style-swapped",
     '    for bits, ram_style in ((payload_bits, "block"),\n'
     '                            (_FIFO_FRAMING_BITS, "distributed")):\n',
     '    for bits, ram_style in ((payload_bits, "distributed"),\n'
     '                            (_FIFO_FRAMING_BITS, "block")):\n',
     [("mac_tx", "storage"), ("csr_w", "storage")]),
    ("read-port-in-write-domain",
     '        array_read = array.get_port(clock_domain="read", mode=READ_FIRST)\n',
     '        array_read = array.get_port(clock_domain="write", mode=READ_FIRST)\n',
     [("mac_tx", "lockstep"), ("mac_rx", "lockstep"), ("csr_w", "lockstep"), ("csr_r", "lockstep")]),
    ("read-port-async-latency-change",
     '        array_read = array.get_port(clock_domain="read", mode=READ_FIRST)\n',
     '        array_read = array.get_port(clock_domain="read", async_read=True)\n',
     [("mac_tx", "lockstep"), ("mac_rx", "lockstep"), ("csr_w", "lockstep"), ("csr_r", "lockstep")]),
    ("write-address-ahead",
     "            array_write.adr.eq(write.adr),\n",
     "            array_write.adr.eq(write.adr + 1),\n",
     [("mac_tx", "order"), ("mac_rx", "order"), ("csr_w", "order"), ("csr_r", "order")]),
    ("mac-rename-dropped",
     "            mac_cdc_rename = _mac_cdc_rename(milan_cd)\n",
     "            mac_cdc_rename = None\n",
     [("mac_tx", "reset"), ("mac_rx", "reset")]),
    ("mac-cdc-unbuffered",
     "                                     depth=_AXIS_CDC_DEPTH, buffered=True)\n"
     "    if rename: cdc = ClockDomainsRenamer(rename)(cdc)\n"
     "    setattr(host, name, cdc)\n"
     "    return _AxisDP(dp=cdc.sink, sys=cdc.source)\n",
     "                                     depth=_AXIS_CDC_DEPTH, buffered=False)\n"
     "    if rename: cdc = ClockDomainsRenamer(rename)(cdc)\n"
     "    setattr(host, name, cdc)\n"
     "    return _AxisDP(dp=cdc.sink, sys=cdc.source)\n",
     [("mac_tx", "depth"), ("mac_tx", "lockstep")]),
    ("csr-r-not-converted",
     '    _payload_in_block_ram(by_name["r"])\n',
     "    pass\n",
     [("csr_r", "storage")]),
)


def planted(name, old, new):
    source = SOC.read_text(encoding="utf-8")
    if source.count(old) != 1:
        return f"product text occurs {source.count(old)} times"
    root = SCRATCH / name
    for parent, keep in ((REPO, "sw"), (REPO / "sw", "litex"), (REPO / "sw/litex", "milan_soc.py")):
        target = root / parent.relative_to(REPO)
        target.mkdir(parents=True, exist_ok=True)
        for entry in parent.iterdir():
            if entry.name not in (keep, "__pycache__") and not (target / entry.name).exists():
                (target / entry.name).symlink_to(entry)
    (root / "sw/litex/milan_soc.py").write_text(source.replace(old, new), encoding="utf-8")
    run = subprocess.run([sys.executable, "-B", str(TEST), "--soc-dir", str(root / "sw/litex"),
                          "--no-controls"], capture_output=True, text=True, timeout=1800)
    (SCRATCH / f"{name}.log").write_text(run.stdout + run.stderr)
    return run


def one(probe):
    name, old, new, expect = probe
    run = planted(name, old, new)
    if isinstance(run, str):
        return f"[ERROR ] {name}: {run}"
    failed = sorted({tuple(l.split()[1:3]) for l in run.stdout.splitlines()
                     if l.startswith("VERDICT ") and l.endswith(" FAIL")})
    hit = [e for e in expect if e in failed]
    caught = run.returncode == 1 and bool(hit)
    tail = "" if run.returncode in (0, 1) else " | " + (run.stderr.strip().splitlines() or ["?"])[-1]
    return (f"[{'CAUGHT' if caught else 'MISSED'}] {name}: exit {run.returncode}, "
            f"expected-any {expect}, fails {' '.join('/'.join(f) for f in failed) or 'nothing'}{tail}")


SCRATCH.mkdir(parents=True, exist_ok=True)
with ThreadPoolExecutor(max_workers=JOBS) as pool:
    lines = list(pool.map(one, PROBES))
for line in lines:
    print(line)
print(f"probes {len(lines)}, caught {sum(l.startswith('[CAUGHT') for l in lines)}")
