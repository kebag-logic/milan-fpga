#!/usr/bin/env python3
"""artifacts.py <repo> <outdir> <label>: every builder artifact of every tracked config, at both placements,
written to <outdir>/<label>/<config>/<placement>/ with a JSON receipt of sizes and sha256 (no host paths).

Captured per config and placement: the builder's readable artifact set (_write_artifact_dir), the AEM image set
(_entity_model_image), the shape include, the firmware's generated AEM header (aecp_entity.emit), and the packed
descriptor image's summary (descriptor count, name entries, image bytes, entity_model_id)."""
import hashlib
import json
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve() / sys.argv[3]
sys.path.insert(0, str(repo / "sw/builder"))
sys.path.insert(0, str(repo / "sw/firmware/ctrl/aecp"))
import endstation_builder as builder  # noqa: E402
import aecp_entity  # noqa: E402

receipt = {}
for config in sorted((repo / "configs").glob("endstation_*.yaml")):
    for placement in ("all-fabric", "split"):
        art = builder._derive_artifacts(config, placement)
        base = out / config.stem / placement
        directory, _ = builder._write_artifact_dir(art, base)
        for name, data in builder._entity_model_image(art.cfg, art.overlay).items():
            (directory / name).write_bytes(data if isinstance(data, bytes) else data.encode())
        (directory / "adp_shape_defaults.gen.svh").write_text(art.adp_svh)
        if placement == "split":
            cfg_path = config
            hdr = aecp_entity.emit(cfg_path) if art.cfg["control"]["placement"] == "split" else None
            if hdr is not None:
                (directory / "aecp_entity_gen.h").write_text(hdr)
        files = {f.name: dict(bytes=f.stat().st_size, sha256=hashlib.sha256(f.read_bytes()).hexdigest())
                 for f in sorted(directory.iterdir()) if f.is_file()}
        receipt[f"{config.stem}/{placement}"] = dict(
            files=files, model_id=art.cfg["entity"]["entity_model_id"],
            counts=art.overlay.get("descriptor_counts"),
            clusters_in=[p["clusters"] for p in art.cfg["ports_in"]],
            clusters_out=[p["clusters"] for p in art.cfg["ports_out"]])
        print(config.stem, placement, art.cfg["entity"]["entity_model_id"],
              [p["clusters"] for p in art.cfg["ports_in"]], flush=True)
(out / "receipt.json").write_text(json.dumps(receipt, indent=1, sort_keys=True) + "\n")
