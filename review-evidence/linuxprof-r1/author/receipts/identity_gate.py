#!/usr/bin/env python3
"""FPGA artifact identity capture for milan-fpga #983 (lane-local tool, not committed).

For every tracked configs/endstation_*.yaml, at its own placement and at the
split placement recipe, run the builder's build() into OUT, then the AEM image
(_entity_model_image) and the firmware generators (adp_entity.py,
aecp_entity.py, srp_entity.py, ctrl_plat_gen.py policy), and write a manifest
of sha256 per artifact. Also hashes the tracked generated files the builder
owns (configs/generated/**, hdl/common/gen, hdl/common/csr/gen).

usage: identity_gate.py REPO OUT MANIFEST
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

repo, out, manifest = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3])
sys.path.insert(0, str(repo / "sw/builder"))
import endstation_builder as eb  # noqa: E402

rows = {}


def put(label, data):
    rows[label] = hashlib.sha256(data).hexdigest()


configs = sorted(p.relative_to(repo) for p in (repo / "configs").glob("endstation_*.yaml"))
assert len(configs) == 5, configs
for cfg_rel in configs:
    for placement in (None, "split"):
        tag = f"{cfg_rel.stem}@{placement or 'own'}"
        dest = out / tag
        dest.mkdir(parents=True, exist_ok=True)
        r = eb.build(str(cfg_rel), str(dest), placement=placement)
        for f in sorted((dest / cfg_rel.stem).rglob("*")):
            if f.is_file():
                put(f"{tag}/build/{f.relative_to(dest)}", f.read_bytes())
        cfg = r["cfg"]
        for name, content in eb._entity_model_image(cfg, r["overlay"]).items():
            put(f"{tag}/image/{name}", content if isinstance(content, bytes) else content.encode())
    for tool, args in (("sw/firmware/ctrl/adp/adp_entity.py", []),
                       ("sw/firmware/ctrl/aecp/aecp_entity.py", []),
                       ("sw/firmware/ctrl/srp/srp_entity.py", []),
                       ("sw/firmware/ctrl/plat/ctrl_plat_gen.py", ["policy"])):
        o = out / f"{cfg_rel.stem}.{Path(tool).stem}.h"
        subprocess.run([sys.executable, "-B", tool, *args, str(cfg_rel), "-o", str(o)], cwd=repo, check=True)
        put(f"{cfg_rel.stem}/gen/{Path(tool).name}", o.read_bytes())

tracked = subprocess.run(["git", "ls-files", "configs/generated", "hdl/common/gen", "hdl/common/csr/gen"],
                         cwd=repo, check=True, capture_output=True, text=True).stdout.split()
for t in sorted(tracked):
    put(f"tracked/{t}", (repo / t).read_bytes())
status = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=repo, check=True,
                        capture_output=True, text=True).stdout
manifest.write_text(json.dumps({"artifacts": rows, "tracked_status": status}, indent=1, sort_keys=True) + "\n")
print(f"{len(rows)} artifacts; tracked status after the builds: {'clean' if not status else status!r}")
