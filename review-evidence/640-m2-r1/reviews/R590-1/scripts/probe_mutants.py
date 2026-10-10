#!/usr/bin/env python3
# Reviewer probe (R590-1, #640 lane M2): plant defects into scratch copies of
# sw/litex/milan_soc.py and require test_retained_cdc_storage.py (run with
# --soc-dir <copy> --no-controls) to fail the named checks.
#
#   probe_mutants.py <repo> <scratch-dir> <python> [jobs]
#
# The repository is never written: each mutant is a tree of symlinks to the
# checkout except the one planted milan_soc.py, as the test's own controls do.
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO, SCRATCH, PY = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
JOBS = int(sys.argv[4]) if len(sys.argv) > 4 else 8
TEST = REPO / "sw/litex/test_retained_cdc_storage.py"

# (name, product text, planted text, {(array, check), ...} that must FAIL)
MUTANTS = (
    # re-applied author controls (independently re-planted here)
    ("A-read-address-ahead",
     "            array_read.adr.eq(read.adr),\n",
     "            array_read.adr.eq(read.adr + 1),\n",
     {("mac_tx", "order"), ("mac_rx", "order"), ("csr_w", "order"), ("csr_r", "order")}),
    ("A-mac-reset-one-side",
     '    return {"sys": "macsys", milan_cd: "macdp"}\n',
     '    return {"sys": "macsys"}\n',
     {("mac_tx", "reset"), ("mac_rx", "reset")}),
    ("A-storage-half-depth",
     '        array = Memory(bits, storage.depth, name="storage")\n',
     '        array = Memory(bits, storage.depth // 2, name="storage")\n',
     {("mac_tx", "depth"), ("mac_rx", "depth"), ("csr_w", "depth"), ("csr_r", "depth")}),
    # reviewer's own planted defects
    ("R-concat-order-swapped",
     "    core.comb += read.dat_r.eq(Cat(*pieces))\n",
     "    core.comb += read.dat_r.eq(Cat(*reversed(pieces)))\n",
     {("mac_tx", "lockstep"), ("mac_rx", "lockstep"), ("csr_w", "lockstep"), ("csr_r", "lockstep")}),
    ("R-flags-never-written",
     "            array_write.we.eq(write.we),\n",
     "            array_write.we.eq(write.we if ram_style == \"block\" else 0),\n",
     {("mac_tx", "lockstep"), ("mac_rx", "lockstep"), ("csr_w", "lockstep"), ("csr_r", "lockstep")}),
    ("R-flags-write-address-off",
     "            array_write.adr.eq(write.adr),\n",
     "            array_write.adr.eq(write.adr + (ram_style == \"distributed\")),\n",
     {("mac_tx", "lockstep"), ("mac_rx", "lockstep"), ("csr_w", "lockstep"), ("csr_r", "lockstep")}),
    ("R-async-read-port",
     '        array_read = array.get_port(clock_domain="read")\n',
     '        array_read = array.get_port(async_read=True, clock_domain="read")\n',
     {("mac_tx", "lockstep"), ("mac_rx", "lockstep"), ("csr_w", "lockstep"), ("csr_r", "lockstep")}),
    ("R-styles-swapped",
     '    for bits, ram_style in ((payload_bits, "block"),\n'
     '                            (_FIFO_FRAMING_BITS, "distributed")):\n',
     '    for bits, ram_style in ((payload_bits, "distributed"),\n'
     '                            (_FIFO_FRAMING_BITS, "block")):\n',
     {("mac_tx", "storage"), ("mac_rx", "storage"), ("csr_w", "storage"), ("csr_r", "storage")}),
    ("R-b-channel-also-converted",
     '    _payload_in_block_ram(by_name["r"])\n',
     '    _payload_in_block_ram(by_name["r"])\n    _payload_in_block_ram(by_name["b"])\n',
     {("csr_b", "storage")}),
    ("R-mac-dp-side-not-reinit",
     '    return {"sys": "macsys", milan_cd: "macdp"}\n',
     '    return {"sys": "macsys", milan_cd: milan_cd}\n',
     {("mac_tx", "reset"), ("mac_rx", "reset")}),
    ("R-csr-w-r-swapped-roles",
     '    _payload_in_block_ram(by_name["w"])\n',
     '    _payload_in_block_ram(by_name["aw"])\n',
     {("csr_w", "storage"), ("csr_aw", "storage")}),
)


def planted(name, old, new):
    src = (REPO / "sw/litex/milan_soc.py").read_text(encoding="utf-8")
    if src.count(old) != 1:
        return None, f"anchor occurs {src.count(old)} times"
    root = SCRATCH / name
    for parent, keep in ((REPO, "sw"), (REPO / "sw", "litex"), (REPO / "sw/litex", "milan_soc.py")):
        target = root / parent.relative_to(REPO)
        target.mkdir(parents=True, exist_ok=True)
        for entry in parent.iterdir():
            if entry.name not in (keep, "__pycache__") and not (target / entry.name).exists():
                (target / entry.name).symlink_to(entry)
    (root / "sw/litex/milan_soc.py").write_text(src.replace(old, new), encoding="utf-8")
    return root / "sw/litex", None


def run(mutant):
    name, old, new, must = mutant
    soc_dir, err = planted(name, old, new)
    if err:
        return name, None, err, must, set()
    log = SCRATCH / f"{name}.log"
    p = subprocess.run([PY, "-B", str(TEST), "--soc-dir", str(soc_dir), "--no-controls"],
                       capture_output=True, text=True, timeout=1800)
    log.write_text(p.stdout + "\n--- stderr ---\n" + p.stderr, encoding="utf-8")
    failed = {tuple(l.split()[1:3]) for l in p.stdout.splitlines()
              if l.startswith("VERDICT ") and l.endswith(" FAIL")}
    return name, p.returncode, None, must, failed


def main():
    SCRATCH.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=JOBS) as pool:
        results = list(pool.map(run, MUTANTS))
    missed = 0
    for name, rc, err, must, failed in results:
        if err:
            print(f"PROBE {name}: NOT-PLANTED ({err})")
            missed += 1
            continue
        caught = rc == 1 and must <= failed
        missed += not caught
        print(f"PROBE {name}: {'DETECTED' if caught else 'SURVIVED'} rc={rc} "
              f"required={sorted(' '.join(m) for m in must)} "
              f"failed={sorted(' '.join(f) for f in failed)}")
    print(f"PROBES {len(results) - missed}/{len(results)} detected")
    return 1 if missed else 0


if __name__ == "__main__":
    sys.exit(main())
