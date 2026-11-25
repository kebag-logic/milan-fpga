#!/usr/bin/env python3
"""The harness image against the merge head's ledger image: identity.py BUILD_DIR LEDGER_ELF.

Prints the sha256 of BUILD_DIR/image/ctrl_app.elf as hashed now, the hash build.json records for it
(`build:image/ctrl_app.elf`), build.json's variant, and the sha256 of LEDGER_ELF; then SAME or DIFFERENT.
"""
import hashlib
import json
import sys
from pathlib import Path

build, ledger = Path(sys.argv[1]), Path(sys.argv[2])
spec = json.loads((build / "build.json").read_text())
recorded = next((v for k, v in spec.items() if isinstance(v, dict) and "build:image/ctrl_app.elf" in v), {})
recorded = recorded.get("build:image/ctrl_app.elf", "MISSING")
elf = Path(spec.get("elf", build / "image/ctrl_app.elf"))
now = hashlib.sha256(elf.read_bytes()).hexdigest()
led = hashlib.sha256(ledger.read_bytes()).hexdigest()
print(f"build {build.name}: variant {spec.get('variant')}, shape {spec.get('shape')}, interfaces {spec.get('interfaces')}")
print(f"  harness ELF {elf}: sha256 {now}")
print(f"  build.json records             {recorded}")
print(f"  ledger ELF  {ledger}: sha256 {led}")
print(f"  harness = ledger: {'SAME' if now == led == recorded else 'DIFFERENT'}")
