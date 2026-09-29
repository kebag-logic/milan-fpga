#!/usr/bin/env python3
"""Reproduce the #599 page's seed CRC row from the three seed build directories.

Claim (docs/findings/599_394_E1_LINK_CYCLES.md, identity table): the QSPI
payload CRC32 over 3,825,788 bytes is d84bce7b for the `eto` seed; `eppo`
reads bf44ccc9 and `asl` reads 809fcffa. Round 1 archived only the `eto` and
`eppo` lines (r1/identity/expected-crc.txt); this adds `asl`.

It runs the round-1 tool r1/tools/expected_crc.py unchanged (its SHA-256 is
printed and must equal the round-1 manifest) over the builder's seed
directories build_ax7101_<seed>_tdm8dev13eda870 of dev 13eda870. Only the
directory names are printed. The directories are tied to dev 13eda870 by
their names; the images were not rebuilt here.

usage: extract_seed_crc.py <eto-dir> <eppo-dir> <asl-dir>
"""
import contextlib
import hashlib
import importlib.util
import io
import re
import sys
from pathlib import Path

PACKET = Path(__file__).resolve().parent.parent
TOOL = PACKET / "r1" / "tools" / "expected_crc.py"
CLAIM = {"eto": "d84bce7b", "eppo": "bf44ccc9", "asl": "809fcffa"}


def main():
    man = dict(reversed(x.split(None, 1)) for x in (PACKET / "r1" / "MANIFEST.sha256").read_text().splitlines()
               if x.strip())
    digest = hashlib.sha256(TOOL.read_bytes()).hexdigest()
    same = man.get("tools/expected_crc.py") == digest
    print(f"TOOL r1/tools/expected_crc.py {digest} {'= round-1 manifest' if same else 'MISMATCH'}")
    if not same:
        sys.exit(2)
    spec = importlib.util.spec_from_file_location("expected_crc", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    dirs = sys.argv[1:4]
    sys.argv = ["expected_crc.py"] + dirs
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = mod.main()
    out = buf.getvalue()
    print(out, end="")
    got = {}
    for block in out.split("== ")[1:]:
        name = block.split()[0]
        seed = re.match(r"build_ax7101_(\w+?)_tdm8dev13eda870$", name).group(1)
        m = re.search(r"bitpay\s+len=\s*(\d+) crc32=([0-9a-f]{8})", block)
        got[seed] = (int(m.group(1)), m.group(2))
    ok = rc == 0 and all(got.get(s) == (3825788, c) for s, c in CLAIM.items())
    for s, c in CLAIM.items():
        print(f"seed {s:5s} payload {got.get(s)} claim {c}")
    print("CLAIM eto d84bce7b, eppo bf44ccc9, asl 809fcffa:", "REPRODUCED" if ok else "NOT REPRODUCED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
