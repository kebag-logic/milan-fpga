#!/usr/bin/env python3
"""R591-1 reviewer mutation probes for PR #710 (issue #640 lane M2).

Each probe plants one textual defect into a scratch copy of
sw/litex/milan_soc.py (the rest of the tree is symlinked, as the lane's own
controls do), runs the lane test `sw/litex/test_retained_cdc_storage.py
--soc-dir <planted> --no-controls` against it, and records which named
VERDICT lines fail. The checkout itself is never modified.

Usage: r591_mutants.py REPO SCRATCH OUTDIR [--jobs N]
REPO is the clone at the head under review; the interpreter running this
script must be the pinned LiteX environment.
"""
import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# (name, old text, new text, {array: check expected to fail} or None when the
#  probe is expected to survive the lane test, i.e. a coverage-limit probe)
PROBES = (
    # re-applications of two of the lane's planted defects (own text)
    ("reapply-half-depth",
     '        array = Memory(bits, storage.depth, name="storage")\n',
     '        array = Memory(bits, storage.depth // 2, name="storage")\n',
     {"mac_tx": "depth", "mac_rx": "depth", "csr_w": "depth", "csr_r": "depth"}),
    ("reapply-read-ahead",
     "            array_read.adr.eq(read.adr),\n",
     "            array_read.adr.eq(read.adr + 1),\n",
     {"mac_tx": "order", "mac_rx": "order", "csr_w": "order", "csr_r": "order"}),
    # new reviewer probes
    ("framing-above-payload-swapped",
     "    core.comb += read.dat_r.eq(Cat(*pieces))\n",
     "    core.comb += read.dat_r.eq(Cat(*reversed(pieces)))\n",
     {"mac_tx": "lockstep", "mac_rx": "lockstep", "csr_w": "lockstep", "csr_r": "lockstep"}),
    ("read-port-in-write-domain",
     '        array_read = array.get_port(clock_domain="read")\n',
     '        array_read = array.get_port(clock_domain="write")\n',
     {"mac_tx": "lockstep", "mac_rx": "lockstep", "csr_w": "lockstep", "csr_r": "lockstep"}),
    ("mac-reset-datapath-side-only",
     '    return {"sys": "macsys", milan_cd: "macdp"}\n',
     '    return {milan_cd: "macdp"}\n',
     {"mac_tx": "reset", "mac_rx": "reset"}),
    ("framing-write-enable-dropped",
     "            array_write.we.eq(write.we),\n",
     "            array_write.we.eq(write.we & (ram_style == \"block\")),\n",
     {"mac_tx": "lockstep", "mac_rx": "lockstep", "csr_w": "lockstep", "csr_r": "lockstep"}),
    ("csr-aw-converted-too",
     '    _payload_in_block_ram(by_name["r"])\n',
     '    _payload_in_block_ram(by_name["r"])\n    _payload_in_block_ram(by_name["aw"])\n',
     {"csr_aw": "storage"}),
    # coverage-limit probe: the MilanMAC call site itself is not exercised
    ("milanmac-call-site-removed",
     "            _payload_in_block_ram(self.mac_tx_cdc)\n"
     "            _payload_in_block_ram(self.mac_rx_cdc)\n",
     "            pass\n",
     None),
)


def planted(repo: Path, scratch: Path, old: str, new: str) -> Path:
    source = (repo / "sw/litex/milan_soc.py").read_text(encoding="utf-8")
    if source.count(old) != 1:
        raise ValueError(f"anchor occurs {source.count(old)} times")
    for parent, keep in ((repo, "sw"), (repo / "sw", "litex"), (repo / "sw/litex", "milan_soc.py")):
        target = scratch / parent.relative_to(repo)
        target.mkdir(parents=True, exist_ok=True)
        for entry in parent.iterdir():
            if entry.name not in (keep, "__pycache__"):
                (target / entry.name).symlink_to(entry)
    (scratch / "sw/litex/milan_soc.py").write_text(source.replace(old, new), encoding="utf-8")
    return scratch / "sw/litex"


def run(repo: Path, scratch_root: Path, out: Path, probe) -> dict:
    name, old, new, expect = probe
    scratch = scratch_root / name
    soc_dir = planted(repo, scratch, old, new)
    proc = subprocess.run([sys.executable, "-B", str(repo / "sw/litex/test_retained_cdc_storage.py"),
                           "--soc-dir", str(soc_dir), "--no-controls"],
                          capture_output=True, text=True, timeout=1800)
    (out / f"{name}.log").write_text(proc.stdout + "\n--- stderr ---\n" + proc.stderr, encoding="utf-8")
    failed = sorted({" ".join(l.split()[1:3]) for l in proc.stdout.splitlines()
                     if l.startswith("VERDICT ") and l.endswith(" FAIL")})
    if expect is None:
        outcome = "SURVIVED (expected: coverage limit)" if proc.returncode == 0 else "DETECTED"
    else:
        missing = [f"{a} {c}" for a, c in expect.items() if f"{a} {c}" not in failed]
        outcome = "DETECTED" if proc.returncode == 1 and not missing else f"NOT-AS-EXPECTED missing={missing}"
    return {"probe": name, "rc": proc.returncode, "failed_verdicts": failed,
            "expected_failures": expect, "outcome": outcome}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", type=Path)
    ap.add_argument("scratch", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--jobs", type=int, default=8)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    a.scratch.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=a.jobs) as pool:
        results = list(pool.map(lambda p: run(a.repo.resolve(), a.scratch.resolve(), a.out, p), PROBES))
    (a.out / "mutants.json").write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8")
    bad = 0
    for r in results:
        print(f"{r['probe']}: rc {r['rc']} -> {r['outcome']}; fails: {', '.join(r['failed_verdicts']) or 'nothing'}")
        bad += r["outcome"].startswith("NOT-AS-EXPECTED")
    print(f"RESULT: {'PASS' if not bad else 'FAIL'} ({bad} probe(s) not as expected)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
