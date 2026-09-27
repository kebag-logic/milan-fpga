#!/usr/bin/env python3
"""R358-1 probe: regenerate the 1x1 TDM8 AEM image from source and compare it to
the identity and enumeration evidence of the issue 117 headless enumeration.

usage: probe_aem_identity.py <repo_root> <packet_author_dir>

Read-only on the repository: imports the builder, writes nothing into the tree.
Checks:
  1. the builder's aem_desc.bin for configs/endstation_ax7101_1x1_tdm8.yaml has
     the size and SHA-256 the assignment and findings page cite;
  2. ENTITY / CONFIGURATION bytes read over AECP (identity-aecp.jsonl, 4-byte
     configuration/reserved prefix removed) equal the image's descriptor rows;
  3. the descriptor type/index inventory the image declares equals every
     run-N.inventory.json and the 41 / 14 claim;
  4. the three run-N.entity.json library verdicts are exactly IEEE17221+MILAN.
"""
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

root, author = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw" / "builder"))
sys.path.insert(0, str(root / "avdecc"))
import endstation_builder as builder  # noqa: E402

CITED_AEM = "9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404"
NAMES = {0: "ENTITY", 1: "CONFIGURATION", 2: "AUDIO_UNIT", 5: "STREAM_INPUT",
         6: "STREAM_OUTPUT", 9: "AVB_INTERFACE", 10: "CLOCK_SOURCE",
         12: "LOCALE", 13: "STRINGS", 14: "STREAM_PORT_INPUT",
         15: "STREAM_PORT_OUTPUT", 16: "EXTERNAL_PORT_INPUT",
         17: "EXTERNAL_PORT_OUTPUT", 18: "INTERNAL_PORT_INPUT",
         19: "INTERNAL_PORT_OUTPUT", 20: "AUDIO_CLUSTER", 23: "AUDIO_MAP",
         26: "CONTROL", 36: "CLOCK_DOMAIN"}
fails = []


def check(cond, msg):
    print(("OK   " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)


cfg_path = root / "configs" / "endstation_ax7101_1x1_tdm8.yaml"
cfg = builder.load_config(cfg_path)
overlay = builder.emit_aem_overlay(cfg)
out = builder._entity_model_image(cfg, overlay)
blob = out["aem_desc.bin"]
h = hashlib.sha256(blob).hexdigest()
print(f"config {cfg_path.relative_to(root)} aem bytes={len(blob)} sha256={h}")
check(len(blob) == 7352 and h == CITED_AEM, "builder AEM image equals the cited 7,352-byte image")

# descriptor rows from the same document the image is packed from
for d in (root / "avdecc", root / "protocol-processor" / "hdl" / "aecp" / "desc"):
    sys.path.insert(0, str(d))
import gen_aem_store as aem  # noqa: E402
import gen_aemi_image as join  # noqa: E402
doc = join.model_to_document(aem.build_model(aem.spec_from_overlay(overlay)),
                             join.identity_from_overlay(overlay))
rows = {(r["type"], r["index"]): bytes.fromhex(r["bytes"]) for r in doc["descriptors"]}
inv = defaultdict(list)
for (t, i) in rows:
    inv[NAMES.get(t, f"TYPE_{t}")].append(i)
inv = {k: sorted(v) for k, v in sorted(inv.items())}
print("image inventory", json.dumps({k: len(v) for k, v in inv.items()}),
      "total", sum(map(len, inv.values())), "types", len(inv))
check(sum(map(len, inv.values())) == 41 and len(inv) == 14, "image declares 41 descriptors across 14 types")
for n in (1, 2, 3):
    run_inv = json.loads((author / f"run-{n}.inventory.json").read_text())
    check(run_inv == inv, f"run-{n}.inventory.json equals the image inventory (types and indices)")

# AECP identity bytes vs image rows and vs image offsets 0x110 / 0x248
lines = [json.loads(x) for x in (author / "identity-aecp.jsonl").read_text().splitlines()]
reads = {x["req"]: bytes.fromhex(x["payload"]) for x in lines if x.get("cmd") == "READ_DESCRIPTOR"}
for req, key, off in (("0000000000000000", (0, 0), 0x110), ("0000000000010000", (1, 0), 0x248)):
    got = reads[req][4:]
    check(got == rows[key], f"AECP {NAMES[key[0]]} ({len(got)} B) equals the image descriptor row")
    check(blob[off:off + len(got)] == got, f"AECP {NAMES[key[0]]} equals image bytes at 0x{off:x}")
ent = reads["0000000000000000"][4:]
print("entity_id", ent[4:12].hex(), "model", ent[12:20].hex())
check(ent[4:12].hex() == "020000fffe000001" and ent[12:20].hex() == "001bc5c40236ba0e", "entity and model IDs as cited")

# library verdicts and per-run inventories recomputed from the dumps themselves
for n in (1, 2, 3):
    j = json.loads((author / f"run-{n}.entity.json").read_text())
    check(j["compatibility_flags"] == ["IEEE17221", "MILAN"] and j["compatibility_events"] == [],
          f"run-{n} library flags exactly IEEE17221+MILAN, no compatibility events")
    found = defaultdict(list, ENTITY=[0])

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k.endswith("_descriptors") and isinstance(v, list):
                    for d in v:
                        found[k.removesuffix("_descriptors").upper()].append(d["_index (informative)"])
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(j["entity_model"])
    check({k: sorted(v) for k, v in sorted(found.items())} == inv, f"run-{n} dump inventory recomputed equals the image inventory")
    st = j["statistics"]
    check(all(st[k] == 0 for k in ("aecp_retry_counter", "aecp_timeout_counter", "aecp_unexpected_response_counter")),
          f"run-{n} AECP retries/timeouts/unexpected all zero")
print("RESULT", "FAIL" if fails else "PASS", len(fails))
sys.exit(1 if fails else 0)
