#!/usr/bin/env python3
"""[R222] Hash every builder artifact of the five tracked configs at one root.

Usage: probe_artifacts.py <scratch-root> <outdir> <manifest.json>

Per config: the YAML bytes, load_config()'s normalized result, the AEM
overlay, every file _entity_model_image() returns (the packed aem_desc.bin
and its manifest), the AUDIO_UNIT descriptor's rate words read back out of
the packed image, and every file build() writes under <outdir>/<config>.
Paths inside <outdir> are recorded relative to it, and the scratch root is
replaced by '<ROOT>' in text before hashing so two roots compare.
"""
import hashlib
import importlib.util
import json
import struct
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
outdir = Path(sys.argv[2]).resolve()
manifest_path = Path(sys.argv[3])
sys.path.insert(0, str(root / "sw/builder"))
spec = importlib.util.spec_from_file_location(
    "test_builder", root / "sw/builder/test_builder.py")
tb = importlib.util.module_from_spec(spec)
sys.modules["test_builder"] = tb
spec.loader.exec_module(tb)
eb = tb.eb
assert Path(eb.__file__).resolve() == root / "sw/builder/endstation_builder.py"


def h(data) -> str:
    if isinstance(data, str):
        data = data.replace(str(root), "<ROOT>").encode()
    return hashlib.sha256(data).hexdigest()


result = {}
for name, path in tb.CONFIGS.items():
    row = {"yaml_sha256": h(path.read_bytes())}
    cfg = eb.load_config(str(path))
    row["load_config_sha256"] = h(json.dumps(cfg, sort_keys=True, default=str))
    row["audio_unit_rates_hz"] = cfg["clocking"]["audio_unit_rates_hz"]
    row["sampling_rate_hz"] = cfg["clocking"]["sampling_rate_hz"]
    row["entity_model_id"] = cfg["entity"]["entity_model_id"]
    overlay = eb.emit_aem_overlay(cfg)
    row["overlay_sha256"] = h(json.dumps(overlay, sort_keys=True, default=str))
    image = eb._entity_model_image(cfg, overlay)
    row["image_files"] = {k: h(v if isinstance(v, (bytes, str)) else
                               json.dumps(v, sort_keys=True, default=str))
                          for k, v in sorted(image.items())}
    desc = tb.image_descriptor(image["aem_desc.bin"], 0x0002)
    cur, off, cnt = struct.unpack_from(">IHH", desc, 136)
    row["image_audio_unit"] = {"current": cur, "offset": off, "count": cnt,
                               "rates": list(struct.unpack_from(f">{cnt}I", desc, off)),
                               "len": len(desc)}
    built = eb.build(str(path), str(outdir / name))
    files = {}
    for f in sorted((outdir / name).rglob("*")):
        if f.is_file():
            files[str(f.relative_to(outdir / name))] = h(
                f.read_text() if f.suffix in (".json", ".svh", ".sh", ".txt", ".md", ".v", ".yaml", ".hex")
                else f.read_bytes())
    row["build_files"] = files
    row["build_paths_outside_outdir"] = sorted(
        str(Path(p).relative_to(root)) for p in built["paths"].values()
        if p and not Path(p).resolve().is_relative_to(outdir))
    result[name] = row
manifest_path.write_text(json.dumps(result, indent=1, sort_keys=True))
for name, row in result.items():
    print(name, row["audio_unit_rates_hz"], row["image_audio_unit"],
          len(row["build_files"]), "build files;", "image",
          row["image_files"].get("aem_desc.bin"))
