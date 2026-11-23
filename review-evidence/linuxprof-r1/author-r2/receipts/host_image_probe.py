#!/usr/bin/env python3
"""Host images and the malformed-board boundary across revisions.

Usage: python3 -I -B host_image_probe.py REPO BOARD_YAML OUT_JSON
Loads each revision's builder blob as endstation_builder (tracked files are
not written). For the host example and the public board YAML: the AEM image
sha256 and length, the talker rows' MaxFrameSize. For the FPGA 1x1 with
board replaced by [], "" and ["ax7101"]: the outcome class and message.
"""
import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import types
from pathlib import Path

import yaml

repo, board, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3])
os.chdir(repo)
sys.path.insert(0, str(repo / "sw/builder"))
REVS = ("854bd7236792ce1adbd10c43b13a6a5002ad3bb6", "677d605f37c3a80654df1dd2cde053b57242845b",
        "66b4def34dcbc0d371ce4eb339d3d0226875befa")
rows = []
for rev in REVS:
    m = types.ModuleType("endstation_builder")
    m.__file__ = str(repo / "sw/builder/endstation_builder.py")
    sys.modules[m.__name__] = m
    exec(compile(subprocess.check_output(["git", "show", f"{rev}:sw/builder/endstation_builder.py"]),
                 m.__file__, "exec"), m.__dict__)
    fpga = yaml.safe_load((repo / "configs/endstation_ax7101_1x1_tdm8.yaml").read_text())
    for value in ([], "", ["ax7101"]):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bad.yaml"
            doc = copy.deepcopy(fpga)
            doc["board"] = value
            p.write_text(yaml.safe_dump(doc))
            try:
                m.load_config(str(p))
                outcome, msg = "accepted", ""
            except Exception as e:  # the class is the observation
                outcome, msg = type(e).__name__, str(e)
        rows.append(dict(revision=rev, case=f"board={value!r}", outcome=outcome, message=msg))
    if rev == REVS[0]:
        continue  # no host profile at the base
    for label, cfgp in (("host example", repo / "configs/host/endstation_host_example.yaml"),
                        ("board endstation_pb2_bridge.yaml", board)):
        cfg = m.load_config(str(cfgp))
        img = m._entity_model_image(cfg, m.emit_aem_overlay(cfg))["aem_desc.bin"]
        rows.append(dict(revision=rev, case=label, image_bytes=len(img),
                         image_sha256=hashlib.sha256(img).hexdigest(),
                         talker_max_frame_bytes=[r["max_frame_bytes"] for r in cfg["srp"]["rows"]
                                                 if r["direction"] == "talker"],
                         talker_formats=[t["formats"] for t in cfg["talkers"]]))
out.write_text(json.dumps(rows, indent=2) + "\n")
print(json.dumps(rows, indent=2))
