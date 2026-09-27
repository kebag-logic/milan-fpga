#!/usr/bin/env python3
"""Derive each shape's AEM flash image and generated shape outputs from one tree.

Usage: aem_probe.py <tree> <pp-desc-dir> <out-dir>
Mirrors milan_soc.build_desc_image without importing LiteX, so the harness's
measured AEM bytes can be compared across the source base and the candidate.
"""
import hashlib
import json
import sys
from pathlib import Path

tree, desc, out = (Path(a).resolve() for a in sys.argv[1:4])
sys.path[:0] = [str(tree / 'sw/builder'), str(tree / 'avdecc'), str(desc)]
import endstation_builder as eb  # noqa: E402
import gen_aem_store as aem  # noqa: E402
import gen_desc_image as img  # noqa: E402
import gen_aemi_image as join  # noqa: E402

result = {}
for shape in ('endstation_ax7101_1x1_tdm8', 'endstation_ax7101_8x8'):
    art = eb._derive_artifacts(str(tree / 'configs' / (shape + '.yaml')))
    gen, _ = eb._write_artifact_dir(art, str(out / shape))
    ovl = json.loads((Path(gen) / 'aem_overlay.json').read_text())
    model = aem.build_model(aem.spec_from_overlay(ovl))
    blob, _report = img.build(join.model_to_document(model, join.identity_from_overlay(ovl)), 576)
    c = art.cfg['constraints']
    result[shape] = dict(aem_bytes=len(blob), aem_sha256=hashlib.sha256(blob).hexdigest(),
                         adp_svh_sha256=hashlib.sha256(art.adp_svh.encode()).hexdigest(),
                         milan_clk_hz=c['milan_clk_hz'], sys_clk_hz=c['sys_clk_hz'])
print(json.dumps(result, indent=1, sort_keys=True))
