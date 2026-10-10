#!/usr/bin/env python3
"""R590-2 reviewer mutation probes for the M2 lane test.

Each probe plants one defect (independent of the test's own controls) into a
scratch copy of sw/litex/milan_soc.py and runs the head's lane test against it
with --no-controls. A probe is CAUGHT when the test exits 1 and every
(array, check) named as expected appears among its FAIL verdicts.

Usage: mutants.py CLONE LITEX_PYTHON SCRATCH OUTDIR [--jobs N]
"""
import argparse
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

LOOP_STYLES = ('    for bits, ram_style in ((payload_bits, "block"),\n'
               '                            (_FIFO_FRAMING_BITS, "distributed")):\n')

# (name, product text, planted text, {array: check that must fail} or None
#  meaning "any failure", description)
PROBES = (
    ("cat-order-swapped",
     "    core.comb += read.dat_r.eq(Cat(*pieces))\n",
     "    core.comb += read.dat_r.eq(Cat(*reversed(pieces)))\n",
     {"mac_tx": "lockstep", "mac_rx": "lockstep", "csr_w": "lockstep", "csr_r": "lockstep"},
     "read word reassembled with flags below the payload"),
    ("split-write-enable-always",
     "            array_write.we.eq(write.we),\n",
     "            array_write.we.eq(1),\n",
     None,
     "both split arrays written every write-domain cycle"),
    ("csr-aw-instead-of-w",
     '    _payload_in_block_ram(by_name["w"])\n',
     '    _payload_in_block_ram(by_name["aw"])\n',
     {"csr_w": "storage", "csr_aw": "storage"},
     "the CSR helper places AW instead of W"),
    ("ram-style-dropped",
     '        array.attr = {("ram_style", ram_style)}\n',
     '        array.attr = set()\n',
     {"mac_tx": "storage", "csr_w": "storage"},
     "no ram_style attribute on either split array"),
    ("ram-styles-swapped",
     LOOP_STYLES,
     LOOP_STYLES.replace('"block"', '"TMP"').replace('"distributed"', '"block"')
                .replace('"TMP"', '"distributed"'),
     {"mac_tx": "storage", "mac_rx": "storage", "csr_w": "storage", "csr_r": "storage"},
     "payload tagged distributed, flags tagged block"),
    ("payload-slice-shifted",
     "            array_write.dat_w.eq(write.dat_w[lsb:lsb + bits]),\n",
     "            array_write.dat_w.eq(write.dat_w[lsb + 1:lsb + 1 + bits]),\n",
     {"mac_tx": "lockstep", "mac_rx": "lockstep", "csr_w": "lockstep", "csr_r": "lockstep"},
     "split arrays store the write word one bit off"),
    ("read-address-from-write-side",
     "            array_read.adr.eq(read.adr),\n",
     "            array_read.adr.eq(write.adr),\n",
     {"mac_tx": "lockstep", "mac_rx": "lockstep", "csr_w": "lockstep", "csr_r": "lockstep"},
     "split arrays read at the write pointer"),
    ("flags-async-read",
     '        array_read = array.get_port(clock_domain="read", mode=READ_FIRST)\n',
     '        array_read = (array.get_port(clock_domain="read", async_read=True)\n'
     '                      if ram_style == "distributed" else\n'
     '                      array.get_port(clock_domain="read", mode=READ_FIRST))\n',
     {"mac_tx": "lockstep", "mac_rx": "lockstep", "csr_w": "lockstep", "csr_r": "lockstep"},
     "framing flags read one cycle earlier than the payload"),
    ("mac-rx-call-removed",
     "            _payload_in_block_ram(self.mac_rx_cdc)\n",
     "            pass\n",
     {"mac_rx": "storage"},
     "MilanMAC places only mac_tx_cdc"),
    ("split-depth-doubled",
     '        array = Memory(bits, storage.depth, name="storage")\n',
     '        array = Memory(bits, storage.depth * 2, name="storage")\n',
     {"mac_tx": "storage", "mac_rx": "storage", "csr_w": "storage", "csr_r": "storage"},
     "split arrays twice the pointer range (function-neutral, area-wasting)"),
    ("split-write-in-read-domain",
     '        array_write = array.get_port(write_capable=True, clock_domain="write")\n',
     '        array_write = array.get_port(write_capable=True, clock_domain="read")\n',
     {"mac_tx": "lockstep", "mac_rx": "lockstep", "csr_w": "lockstep", "csr_r": "lockstep"},
     "split arrays written in the read clock"),
    ("csr-r-not-placed",
     '    _payload_in_block_ram(by_name["r"])\n',
     '    pass\n',
     {"csr_r": "storage"},
     "the CSR helper leaves R stock"),
)


def plant(clone: Path, scratch: Path, old: str, new: str) -> Path:
    src = (clone / "sw/litex/milan_soc.py").read_text(encoding="utf-8")
    if src.count(old) != 1:
        raise ValueError(f"anchor occurs {src.count(old)} times")
    for parent, keep in ((clone, "sw"), (clone / "sw", "litex"),
                         (clone / "sw/litex", "milan_soc.py")):
        target = scratch / parent.relative_to(clone)
        target.mkdir(parents=True, exist_ok=True)
        for entry in parent.iterdir():
            if entry.name not in (keep, "__pycache__"):
                (target / entry.name).symlink_to(entry)
    (scratch / "sw/litex/milan_soc.py").write_text(src.replace(old, new), encoding="utf-8")
    return scratch / "sw/litex"


def run_probe(args, probe):
    name, old, new, must, _ = probe
    scratch = Path(args.scratch) / f"mutant-{name}"
    if scratch.exists():
        shutil.rmtree(scratch)
    soc_dir = plant(Path(args.clone), scratch, old, new)
    proc = subprocess.run([args.python, "-B", str(Path(args.clone) / "sw/litex/test_retained_cdc_storage.py"),
                           "--soc-dir", str(soc_dir), "--no-controls"],
                          capture_output=True, text=True, timeout=3600,
                          env={"PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1",
                               "HOME": str(Path.home()),
                               "TMPDIR": args.scratch})
    (Path(args.out) / f"{name}.log").write_text(proc.stdout + "\n--- stderr ---\n" + proc.stderr)
    failed = sorted({" ".join(l.split()[1:3]) for l in proc.stdout.splitlines()
                     if l.startswith("VERDICT ") and l.endswith(" FAIL")})
    if must is None:
        caught = proc.returncode == 1 and bool(failed)
    else:
        caught = proc.returncode == 1 and all(f"{a} {c}" in failed for a, c in must.items())
    shutil.rmtree(scratch)
    return {"probe": name, "rc": proc.returncode, "failed": failed,
            "expected": must, "caught": caught}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clone"); ap.add_argument("python"); ap.add_argument("scratch"); ap.add_argument("out")
    ap.add_argument("--jobs", type=int, default=6)
    args = ap.parse_args()
    Path(args.out).mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(lambda p: run_probe(args, p), PROBES))
    for r, p in zip(results, PROBES):
        r["description"] = p[4]
        print(f"[{'CAUGHT' if r['caught'] else 'MISSED'}] {r['probe']}: rc {r['rc']}; fails: {', '.join(r['failed']) or 'nothing'}")
    (Path(args.out) / "results.json").write_text(json.dumps(results, indent=1))
    missed = [r["probe"] for r in results if not r["caught"]]
    print(f"probes: {len(results)} caught: {len(results) - len(missed)} missed: {missed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
