"""Link the image and export the harness's test SoC for one CPU geometry, without verilating.

usage: export_only.py CHECKOUT BUILD_DIR SHAPE N_IF FETCH_L1 [CPU_REGIONS]
"""
import json
import sys
from pathlib import Path

checkout, build_dir, shape, n_if, fetch_l1 = sys.argv[1:6]
cpu_regions = sys.argv[6] if len(sys.argv) > 6 else 'cover'
harness = Path(checkout) / 'tb/verilator/ctrl_service_budget'
sys.path.insert(0, str(harness))
import build as builder  # noqa: E402
import split_soc  # noqa: E402
out = Path(build_dir).resolve()
out.mkdir(parents=True, exist_ok=True)
elf = out / 'image/ctrl_app.elf'
if not elf.is_file():
    elf = builder.firmware(out, shape, int(n_if))
spec = split_soc.build(out, shape, elf, int(n_if), cpu_regions, fetch_l1)
print(json.dumps({k: spec[k] for k in ('netlist', 'vexii_args', 'fetch_l1', 'fetch_l1_geometry')}, indent=1))
