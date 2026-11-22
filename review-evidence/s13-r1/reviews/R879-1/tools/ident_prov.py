#!/usr/bin/env python3
"""ident_prov.py CLONE SHAPE OUT: the provisional platform image of one shape in one clone, built with the clone's
own split-boot helpers (tb/verilator/ctrl_split_boot/run.py: the flash port map from the CPU budget harness's
build.flash_map, the bare-metal runtime archives, the image linked against the fixture CSR map). Prints the image's
path and the two runtime archives' paths, one per line."""
import importlib.util
import sys
from pathlib import Path

clone, shape, out = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3]).resolve()
spec = importlib.util.spec_from_file_location("sb_run", clone / "tb/verilator/ctrl_split_boot/run.py")
sb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sb)
assert sb.ROOT == clone, (sb.ROOT, clone)
sys.path.insert(0, str(sb.BUDGET))
import build as budget_build  # noqa: E402

out.mkdir(parents=True, exist_ok=True)
fm = budget_build.flash_map(out / "split-soc/flash-map", shape)
archives = sb.runtime(out)
prov = sb.image(out, "image-provisional", (shape, 1), sb.ImageMaps(sb.PROVISIONAL, fm), archives)
print(prov)
print(archives[0])
print(archives[1])
