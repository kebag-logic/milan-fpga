Original file: tools/fixture_sizes.py
Original size: 1844 bytes
Original sha256: b7bb9104da6e4e6d5612dcd5328c80fd697589c3a485c3bd00cc19d480556395

#!/usr/bin/env python3
"""fixture_sizes.py <clone> <ledger-out> <out>: the size fixture's split image at each point, and its two labelled
harness arms (answering-every-port, valid-destinations) at 8x8/2if, linked through the CPU budget harness's own
build.firmware() on each shape's split export's flash map (ledger.sh's), with the ledgered point where build.py names
one; print each image's rom/sram need and planned RAMB36 from its link report."""
import json, sys
from pathlib import Path
clone, ledger, out = (Path(a).resolve() for a in sys.argv[1:4])
sys.path.insert(0, str(clone / "tb/verilator/ctrl_service_budget"))
import build as builder  # noqa: E402
rows = []
for shape, n_if, variant in (("endstation_ax7101_1x1_tdm8", 1, "none"), ("endstation_ax7101_1x1_tdm8", 2, "none"),
                             ("endstation_ax7101_8x8", 1, "none"), ("endstation_ax7101_8x8", 2, "none"),
                             ("endstation_ax7101_8x8", 2, "answering-every-port"),
                             ("endstation_ax7101_8x8", 2, "valid-destinations")):
    where = out / f"{shape}-if{n_if}-{variant}"
    fmap = ledger / shape / "split-soc/flash-map"
    try:
        builder.firmware(where, shape, n_if, variant=variant, flash_map=fmap)
        log = json.loads((where / "image.log").read_text())
        s = log["split"]
        rows.append(f"{shape} if{n_if} {variant}: rom {s['rom']['bytes']:,} B in {sum(s['rom']['banks']):,}, "
                    f"sram {s['sram']['bytes']:,} B, {s['tiles']} RAMB36 (budget {s['budget_tiles']})")
    except Exception as e:  # report and go on: a refused plan is a result too
        tail = (where / "image.log").read_text()[-600:] if (where / "image.log").exists() else ""
        rows.append(f"{shape} if{n_if} {variant}: REFUSED {type(e).__name__}: {e} | {tail}")
    print(rows[-1], flush=True)
