#!/usr/bin/env python3
"""R357-1 probe: regenerate every artifact of the five tracked configs.

Usage: probe_artifacts.py <tree-root> <outdir> <manifest.json>

Runs endstation_builder.build() for each configs/endstation_*.yaml into
<outdir>/<name>/, adds the AEM descriptor image and map from
avdecc/gen_aemi_image.py, the sweep fragment text and the interface params,
and re-runs --write-rtl for the owner of the tracked RTL header (the config
its `Source :` line names). build() rewrites the tracked per-config headers
in <tree-root>, so run this only against a disposable copy, then use
`git status` in that copy to see whether tracked outputs changed.
Writes a sha256/size manifest of every file under <outdir>/<name>/ plus the
counts per config.
"""
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
outdir = Path(sys.argv[2]).resolve()
manifest_path = Path(sys.argv[3]).resolve()
sys.path.insert(0, str(root / "sw/builder"))
spec = importlib.util.spec_from_file_location(
    "endstation_builder", root / "sw/builder/endstation_builder.py")
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)

tracked_hdr = (root / B.ADP_SHAPE_REL).read_text()
owner_src = re.search(r"Source\s*:\s*(\S+)", tracked_hdr).group(1)

manifest = {}
for cfg_path in sorted((root / "configs").glob("endstation_*.yaml")):
    res = B.build(str(cfg_path), str(outdir),
                  write_rtl=(B.load_config(str(cfg_path))["source"] == owner_src))
    name = res["cfg"]["name"]
    d = outdir / name
    (d / "sweep_opts.sh.txt").write_text(res["sweep_opts"])
    (d / "interface_params.json").write_text(
        json.dumps(res["interface_params"], sort_keys=True, indent=2) + "\n")
    subprocess.run([sys.executable, str(root / "avdecc/gen_aemi_image.py"),
                    "--overlay", str(d / "aem_overlay.json"),
                    "-o", str(d / "aem_desc.bin"), "-m", str(d / "aem_desc.map")],
                   check=True, capture_output=True, cwd=root)
    dc = res["overlay"]["descriptor_counts"]
    manifest[name] = {
        "counts": {k: dc[k] for k in ("AUDIO_UNIT", "CLOCK_DOMAIN", "CONTROL")},
        "wrote_rtl_header": res["cfg"]["source"] == owner_src,
        "files": {str(p.relative_to(d)): {
            "bytes": p.stat().st_size,
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in sorted(d.rglob("*")) if p.is_file()},
    }
    print(name, manifest[name]["counts"], len(manifest[name]["files"]), "files",
          "(rtl owner)" if manifest[name]["wrote_rtl_header"] else "", flush=True)
manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
