#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Emit every builder artifact and the descriptor image for the shipping
1x1/1if and 8x8/1if configs from one exported tree, and hash them.

Usage: identity.py <tree> <out-dir> [enable]
Run once per tree (base, head); compare the two JSON files with
compare_identity.py. With "enable", the head tree is also built with
input_loopback_lane: true (legacy loopback lane off), as a sanity control
that the option does change the emitted artifacts.
"""
import copy
import hashlib
import json
import sys
from pathlib import Path

import yaml

tree, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
enable = len(sys.argv) > 3 and sys.argv[3] == "enable"
sys.path[:0] = [str(tree / "sw/builder"), str(tree / "avdecc"),
                str(tree / "protocol-processor/hdl/aecp/desc")]
import endstation_builder as eb  # noqa: E402
import gen_aem_store  # noqa: E402
import gen_aemi_image  # noqa: E402
import gen_desc_image  # noqa: E402


def image(overlay):
    model = gen_aem_store.build_model(gen_aem_store.spec_from_overlay(overlay))
    document = gen_aemi_image.model_to_document(model, gen_aemi_image.identity_from_overlay(overlay))
    return gen_desc_image.build(document, 576)[0]


def digest_dir(d):
    return {str(p.relative_to(d)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(d.rglob("*")) if p.is_file()}


records = {}
out.mkdir(parents=True, exist_ok=True)
for name in ("endstation_ax7101_1x1_tdm8", "endstation_ax7101_8x8"):
    variants = [("default", None)]
    if enable:
        variants.append(("enabled", True))
    for label, value in variants:
        raw = yaml.safe_load((tree / "configs" / (name + ".yaml")).read_text())
        if value is not None:
            fab = raw["audio_interface"]["cluster_mapping"].setdefault("fabric", {})
            fab.update(input_loopback_lane=True, loopback_lane=False)
        cfgdir = out.parent / "idcfg" / label
        cfgdir.mkdir(parents=True, exist_ok=True)
        # The config's own pathname is part of some artifacts, so every
        # variant uses one fixed file name under its own directory.
        path = cfgdir / (name + ".yaml")
        if value is None:
            path.write_bytes((tree / "configs" / (name + ".yaml")).read_bytes())
        else:
            path.write_text(yaml.safe_dump(raw))
        art = eb._derive_artifacts(path)
        dest = out.parent / "idart" / label
        dest.mkdir(parents=True, exist_ok=True)
        written, _ = eb._write_artifact_dir(art, dest)
        (Path(written) / "sweep_opts.sh").write_text(art.sweep)
        files = digest_dir(Path(written))
        blob = image(art.overlay)
        records[f"{name}/{label}"] = dict(
            files=files, aem_image_sha256=hashlib.sha256(blob).hexdigest(),
            aem_image_bytes=len(blob), argv=list(art.argv),
            model_id=art.overlay.get("model_id"))
        print(name, label, len(files), "files, image", len(blob), "bytes", flush=True)
(out / "identity.json").write_text(json.dumps(records, indent=1, sort_keys=True) + "\n")
