#!/usr/bin/env python3
"""R564-4: rebuild the published freestanding runtime archives from the public
runtime-provenance.json recipe, verifying every source hash first and every
output archive hash afterwards.

Usage: r564_4_runtime.py PROVENANCE OUT --picolibc D --compiler-rt D --litex-software D --sdk D
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("provenance", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--picolibc", type=Path, required=True)
    ap.add_argument("--compiler-rt", type=Path, required=True)
    ap.add_argument("--litex-software", type=Path, required=True)
    ap.add_argument("--sdk", type=Path, required=True)
    a = ap.parse_args()
    scratch = a.out.resolve()
    subs = {"$PICOLIBC": str(a.picolibc.resolve()), "$COMPILER_RT": str(a.compiler_rt.resolve()),
            "$LITEX_SOFTWARE": str(a.litex_software.resolve()), "$F5_SCRATCH": str(scratch),
            "$RV32_SDK": str(a.sdk.resolve())}

    def expand(s: str) -> str:
        for k, v in subs.items():
            s = s.replace(k, v)
        return s

    p = json.loads(a.provenance.read_text())
    (scratch / "runtime-freestanding").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path(subs["$LITEX_SOFTWARE"]) / "libc/picolibc-minimal.h",
                    scratch / "runtime-freestanding/picolibc.h")
    report = {"sources": [], "outputs": [], "commands": 0}
    outputs = []
    for rec in p["files"]:
        path = Path(expand(rec["path"]))
        if rec["path"].startswith("$F5_SCRATCH") and path.suffix == ".a":
            outputs.append((path, rec))
            continue
        got = sha(path)
        report["sources"].append({"path": rec["path"], "match": got == rec["sha256"]})
        if got != rec["sha256"]:
            print(f"SOURCE MISMATCH {rec['path']}", file=sys.stderr)
            (scratch / "runtime-report.json").write_text(json.dumps(report, indent=2) + "\n")
            return 1
    for command in p["commands"]:
        subprocess.run([expand(c) for c in command], check=True, timeout=120)
        report["commands"] += 1
    ok = True
    for path, rec in outputs:
        got = sha(path)
        report["outputs"].append({"path": rec["path"], "size": path.stat().st_size, "sha256": got,
                                  "published_sha256": rec["sha256"], "match": got == rec["sha256"]})
        ok &= got == rec["sha256"]
    (scratch / "runtime-report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report["outputs"], indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
