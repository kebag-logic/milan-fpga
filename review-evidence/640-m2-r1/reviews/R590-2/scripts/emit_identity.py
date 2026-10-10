#!/usr/bin/env python3
"""R590-2: emit the lane test's three benches (every framing flag a port) from
the head's milan_soc and from the head's milan_soc with the round-2 product
delta reverted (the read port's `mode=READ_FIRST`, i.e. the measured
4177835c form), through LiteX's and migen's emitters, and compare.

Usage: emit_identity.py CLONE LITEX_PYTHON SCRATCH OUTDIR
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mutants import plant  # noqa: E402

OLD = '        array_read = array.get_port(clock_domain="read", mode=READ_FIRST)\n'
NEW = '        array_read = array.get_port(clock_domain="read")\n'


def main():
    clone, python, scratch, out = (Path(a) for a in sys.argv[1:5])
    out.mkdir(parents=True, exist_ok=True)
    reverted = plant(clone, scratch / "emit-reverted", OLD, NEW)
    emit_dir = scratch / "emit"
    lane = clone / "sw/litex/test_retained_cdc_storage.py"
    robust = Path(__file__).resolve().parent / "robustness.py"
    for tag, soc_dir in (("head", clone / "sw/litex"), ("reverted", reverted)):
        proc = subprocess.run([python, "-B", str(robust), str(soc_dir), "--lane-test", str(lane),
                               "--emit-dir", str(emit_dir), "--tag", tag, "--emit-only"],
                              capture_output=True, text=True)
        print(f"emit {tag}: rc {proc.returncode} {proc.stdout.strip()} {proc.stderr.strip()[-300:]}")
    lines = []
    for emitter in ("litex", "migen"):
        for bench in ("mac_tx", "mac_rx", "csr_aw"):
            a = (emit_dir / f"head-{emitter}-{bench}.v").read_bytes()
            b = (emit_dir / f"reverted-{emitter}-{bench}.v").read_bytes()
            lines.append(f"{emitter} {bench}: {'IDENTICAL' if a == b else 'DIFFERS'} "
                         f"({len(a)} vs {len(b)} bytes)")
    (out / "emit_identity.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
