"""Regenerate every builder artifact for the five shipped configurations."""
import hashlib
import json
from pathlib import Path
import sys

root = Path.cwd()
sys.path.insert(0, str(root / "sw/builder"))
import endstation_builder as eb

phase = sys.argv[1]
scratch = Path("$VALIDATION_STORAGE/400-403-a322")
packet = (Path.home() / "milan-fpga-management/2026-09-23/400-403-a322")
dest = scratch / phase
dest.mkdir(exist_ok=False)
configs = sorted((root / "configs").glob("endstation_*.yaml"))
assert len(configs) == 5
for config in configs:
    result = eb.build(str(config), str(dest))
    directory = dest / result["cfg"]["name"]
    # build() writes the config shape beside the tracked configurations.
    # Capture that emitted copy as well as every file under the output root.
    for key in ("cfg_adp_shape_svh", "rtl_csr_defaults_svh"):
        if key in result["paths"]:
            (directory / (key + ".svh")).write_bytes(
                Path(result["paths"][key]).read_bytes())
    # The optional per-board fragment is rendered by the same build. Keep
    # each config's bytes separately without changing board ownership.
    (directory / "sweep_opts.sh").write_text(result["sweep_opts"])
    print(config.relative_to(root), len(list(directory.rglob("*"))), "artifacts")
records = [dict(path=str(path.relative_to(dest)), size=path.stat().st_size,
                sha256=hashlib.sha256(path.read_bytes()).hexdigest())
           for path in sorted(dest.rglob("*")) if path.is_file()]
(packet / (phase + "-artifacts.json")).write_text(json.dumps(records, indent=2) + "\n")
print(phase, len(configs), "configs;", len(records), "artifact files")
