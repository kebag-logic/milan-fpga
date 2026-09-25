#!/usr/bin/env python3
"""R246-1: does sim_nxn's builder call rewrite a TRACKED shape header?

Usage: python3 builder_premise_probe.py <checkout> <receipt.json>

Runs from <checkout>/tb/verilator/milan_dp exactly the generator commands
sim_nxn.cpp:run_the_image_generators issues (same relative argv, private -o),
for the three configs sim_nxn.cpp selects, and records for each:
  * the cfg["source"] the builder derives (its _repo_relative), and whether
    _write_shape_copies' `source_parts[0] == "configs"` branch is taken;
  * mtime_ns and sha256 of the tracked configs/generated/<cfg>/gen header
    before and after, and where the builder actually wrote the header.
Use a disposable checkout: if the premise were true the tracked file would be
rewritten (same bytes expected).
"""
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

CONFIGS = ("endstation_ax7101_8x8", "endstation_arty_4x4", "endstation_ax7101_1x1_tdm8")


def ident(path: Path) -> dict:
    st = path.stat()
    return dict(mtime_ns=st.st_mtime_ns, sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def main() -> int:
    root, receipt = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
    suite = root / "tb/verilator/milan_dp"
    derive = subprocess.run(
        [sys.executable, "-c",
         "import sys; from pathlib import Path; sys.path.insert(0, '../../../sw/builder');"
         "import endstation_builder as eb;"
         "print('\\n'.join(eb._repo_relative(Path(f'../../../configs/{c}.yaml')) for c in sys.argv[1:]))",
         *CONFIGS], cwd=suite, capture_output=True, text=True, check=True).stdout.split()
    rows = []
    for cfg, source in zip(CONFIGS, derive):
        tracked = root / "configs/generated" / cfg / "gen/adp_shape_defaults.svh"
        before = ident(tracked)
        with tempfile.TemporaryDirectory(prefix="r246-builder-") as tmp:
            bld = Path(tmp) / "builder"
            build = subprocess.run(
                f"python3 ../../../sw/builder/endstation_builder.py "
                f"'../../../configs/{cfg}.yaml' -o '{bld}'", shell=True, cwd=suite,
                capture_output=True, text=True)
            private = sorted(str(p.relative_to(bld)) for p in bld.rglob("adp_shape_defaults.svh"))
        after = ident(tracked)
        rows.append(dict(config=cfg, derived_source=source,
                         takes_tracked_branch=Path(source).parts[0] == "configs",
                         builder_rc=build.returncode, tracked_header=str(tracked.relative_to(root)),
                         tracked_before=before, tracked_after=after,
                         tracked_rewritten=before["mtime_ns"] != after["mtime_ns"],
                         header_written_privately_at=private))
    receipt.write_text(json.dumps(rows, indent=1) + "\n")
    for row in rows:
        print(f"{row['config']}: source={row['derived_source']} tracked-branch={row['takes_tracked_branch']} "
              f"rc={row['builder_rc']} tracked-rewritten={row['tracked_rewritten']} "
              f"private={row['header_written_privately_at']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
