#!/usr/bin/env python3
"""soc_export.py TREE OUT SHAPE ELF: the split SoC's export as TREE's harness makes it (build.soc_export)."""
import sys
from pathlib import Path
tree, out, shape, elf = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], Path(sys.argv[4])
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import build  # noqa: E402
out.mkdir(parents=True, exist_ok=True)
print(build.soc_export(out, shape, elf))
