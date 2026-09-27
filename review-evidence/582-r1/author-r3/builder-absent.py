"""Run the complete builder bank with cross compiler probes hidden."""
from pathlib import Path
import runpy
import json
import subprocess
import sys
from unittest.mock import patch

root = Path.cwd().resolve()
sys.path.insert(0, str(root / "sw/builder"))
real_run = subprocess.run
cross = {str(Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc"),
         "riscv64-elf-gcc", "riscv32-unknown-elf-gcc"}
hidden = set()
host_probes = []

def absent(argv, **kwargs):
    if str(argv[0]) in cross:
        hidden.add(str(argv[0]))
        raise FileNotFoundError("deliberately absent RV32 candidate")
    if str(argv[0]) in ("cc", "gcc") and any(Path(str(arg)).name == "probe.c" for arg in argv):
        host_probes.append([str(arg) for arg in argv])
    return real_run(argv, **kwargs)

with patch.object(subprocess, "run", side_effect=absent), \
        patch.object(sys, "argv", ["sw/builder/test_builder.py"]):
    result = runpy.run_path(str(root / "sw/builder/test_builder.py"), run_name="__main__")
assert hidden == cross, (hidden, cross)
assert any("THREE INSTRUMENTS" in why for _, why, _ in result["SKIPPED"])
Path(__file__).with_name("absent-audit.json").write_text(json.dumps({
    "hidden_selectors": sorted(hidden), "host_probe_count": len(host_probes),
    "not_run": result["SKIPPED"]}, indent=2) + "\n")
print("Compiler-absent full bank: all three cross selectors hidden; stand-down registered")
