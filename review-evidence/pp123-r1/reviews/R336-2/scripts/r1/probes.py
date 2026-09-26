#!/usr/bin/env python3
"""Reviewer-owned bypass probes for the body/key check.

Usage: probes.py <base-tree> <head-tree> <scratch-dir> <out.json>

Each case is a kl-aem-image model aimed at one input path (pad_to, name_index,
grouped/mixed-length runs, several configurations, ENTITY, duplicates, key
spellings, out-of-range keys, CLI options). Every case is packed by build() and
by the command line at base and at head. At head, a case marked "refuse" must
raise ImageError whose text is the body/key diagnostic naming cfg, key and body,
and the CLI must return 1 with no image or map; a case marked "accept" must pack,
byte-identical to base.
"""
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

BASE, HEAD, SCRATCH = (Path(a).resolve() for a in sys.argv[1:4])
OUT = Path(sys.argv[4])
GEN = "hdl/aecp/desc/gen_desc_image.py"


def load(tree, tag):
    spec = importlib.util.spec_from_file_location(tag, tree / GEN)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def d(cfg, typ, idx, body_hex=None, fields=None, **extra):
    desc = {"configuration": cfg, "type": typ, "index": idx, **extra}
    if fields is not None:
        desc["fields"] = fields
    else:
        desc["bytes"] = body_hex
    return desc


def model(descs, names=()):
    return {"format": "kl-aem-image", "version": 1, "names": list(names),
            "descriptors": descs}


def named_body(typ, idx, name):
    raw = name.encode()[:64]
    return f"{typ:04x}{idx:04x}" + (raw + b"\0" * (64 - len(raw))).hex()


def entity(idx_in_body=0, typ_in_body=0):
    body = bytearray(312)
    body[0:2] = typ_in_body.to_bytes(2, "big")
    body[2:4] = idx_in_body.to_bytes(2, "big")
    body[48:48 + 3] = b"ent"
    body[180:180 + 3] = b"grp"
    return d(0, "ENTITY", 0, body.hex(), name_index=0)


C = "0014"  # AUDIO_CLUSTER
CASES = [
    # (name, model, expect, cli extra args, expected diagnostic fragment)
    ("legal-bytes", model([d(0, "AUDIO_CLUSTER", 0, "00140000cafe")]), "accept", [], None),
    ("legal-fields-4byte-value",
     model([d(0, "AUDIO_CLUSTER", 0, fields=[{"size": 4, "value": "0x00140000"}])]), "accept", [], None),
    ("legal-fields-bytes-field",
     model([d(0, "AUDIO_CLUSTER", 0, fields=[{"size": 4, "bytes": "0014 0000"}])]), "accept", [], None),
    ("legal-string-field-at-0",
     model([d(0, 0x4142, 0, fields=[{"size": 2, "string": "AB"}, {"size": 2}])]), "accept", [], None),
    ("legal-short-body-padded",
     model([d(0, "AUDIO_CLUSTER", 0, "0014", pad_to=8)]), "accept", [], None),
    ("pad_to-zero-body-type-mismatch",
     model([d(0, "AUDIO_CLUSTER", 0, "", pad_to=8)]), "refuse", [],
     "cfg 0 directory key type 0x0014 index 0 disagrees with body type 0x0000 index 0"),
    ("pad_to-fields-empty-mismatch",
     model([d(0, "AUDIO_CLUSTER", 0, fields=[], pad_to=16)]), "refuse", [],
     "body type 0x0000 index 0"),
    ("named-group-index-mismatch",
     model([d(0, "AUDIO_CLUSTER", 0, named_body(0x14, 0, "a"), name_index=0),
            d(0, "AUDIO_CLUSTER", 1, named_body(0x14, 7, "b"), name_index=1)],
           names=["a", "b"]), "refuse", [],
     "cfg 0 directory key type 0x0014 index 1 disagrees with body type 0x0014 index 7"),
    ("name_index-minus1-type-mismatch",
     model([d(0, "AUDIO_CLUSTER", 0, "00150000", name_index=-1)]), "refuse", [],
     "body type 0x0015 index 0"),
    ("invalid-name_index-still-body-first",
     model([d(0, "AUDIO_CLUSTER", 0, "00150000", name_index=70000)]), "refuse", [],
     "body type 0x0015 index 0"),
    ("mixed-length-runs-second-run-mismatch",
     model([d(0, "STREAM_INPUT", 0, "00050000" + "00" * 136),
            d(0, "STREAM_INPUT", 1, "00050001" + "00" * 144),
            d(0, "STREAM_INPUT", 2, "00050009" + "00" * 144)]), "refuse", [],
     "cfg 0 directory key type 0x0005 index 2 disagrees with body type 0x0005 index 9"),
    ("second-config-mismatch",
     model([d(0, "AUDIO_CLUSTER", 0, "00140000"),
            d(1, "AUDIO_CLUSTER", 0, "00140000"),
            d(2, "AUDIO_CLUSTER", 0, "00240000")]), "refuse", [],
     "cfg 2 directory key type 0x0014 index 0 disagrees with body type 0x0024 index 0"),
    ("entity-body-index-mismatch", model([entity(idx_in_body=1)], names=["ent", "grp"]),
     "refuse", [], "cfg 0 directory key type 0x0000 index 0 disagrees with body type 0x0000 index 1"),
    ("entity-legal", model([entity()], names=["ent", "grp"]), "accept", [], None),
    ("duplicate-mismatch-refused-by-body-first",
     model([d(0, "AUDIO_CLUSTER", 0, "00140000"),
            d(0, "AUDIO_CLUSTER", 0, "00140001")]), "refuse", [],
     "index 0 disagrees with body type 0x0014 index 1"),
    ("key-type-over-16-bit", model([d(0, 0x10014, 0, "00140000")]), "refuse", [],
     "directory key type 0x10014 index 0 disagrees with body type 0x0014 index 0"),
    ("key-index-over-16-bit", model([d(0, "AUDIO_CLUSTER", 0x10000, "00140000")]), "refuse", [],
     "index 65536 disagrees with body type 0x0014 index 0"),
    ("key-index-negative", model([d(0, "AUDIO_CLUSTER", "-1", "0014ffff")]), "refuse", [],
     "index -1 disagrees with body type 0x0014 index 65535"),
    ("key-type-hex-with-space", model([d(0, " 0x0014", 0, "00140000")]), "accept", [], None),
    ("line-bytes-small-still-body-first",
     model([d(0, "AUDIO_CLUSTER", 0, "00150000" + "00" * 600)]), "refuse", ["--line-bytes", "8"],
     "body type 0x0015 index 0"),
    ("mismatch-in-first-of-many",
     model([d(0, "AUDIO_CLUSTER", i, f"0014{(i if i else 5):04x}") for i in range(4)]), "refuse", [],
     "index 0 disagrees with body type 0x0014 index 5"),
]


def run_build(mod, m, extra):
    lb = int(extra[1]) if extra[:1] == ["--line-bytes"] else 576
    try:
        img, rep = mod.build(json.loads(json.dumps(m)), lb)
        return {"ok": True, "image": img, "map": rep}
    except mod.ImageError as exc:
        return {"ok": False, "kind": "ImageError", "msg": str(exc)}
    except Exception as exc:  # noqa: BLE001 - recorded, never hidden
        return {"ok": False, "kind": type(exc).__name__, "msg": str(exc)}


def run_cli(tree, m, extra):
    with tempfile.TemporaryDirectory(dir=SCRATCH) as tmp:
        t = Path(tmp)
        (t / "m.json").write_text(json.dumps(m))
        p = subprocess.run([sys.executable, "-B", str(tree / GEN), "-i", str(t / "m.json"),
                            "-o", str(t / "o.bin"), "-m", str(t / "o.map"), *extra],
                           capture_output=True, text=True, timeout=60)
        return {"rc": p.returncode, "stderr": p.stderr.strip()[-300:],
                "bin": (t / "o.bin").read_bytes() if (t / "o.bin").exists() else None,
                "map_written": (t / "o.map").exists()}


def main():
    base, head = load(BASE, "gen_base"), load(HEAD, "gen_head")
    rows, bad = [], 0
    for name, m, expect, extra, frag in CASES:
        hb, bb = run_build(head, m, extra), run_build(base, m, extra)
        hc, bc = run_cli(HEAD, m, extra), run_cli(BASE, m, extra)
        if expect == "accept":
            ok = (hb["ok"] and bb["ok"] and hb["image"] == bb["image"]
                  and hc["rc"] == 0 and hc["bin"] == hb["image"])
        else:
            ok = (not hb["ok"] and hb["kind"] == "ImageError" and "disagrees with body" in hb["msg"]
                  and frag in hb["msg"] and hb["msg"].startswith("cfg ")
                  and hc["rc"] == 1 and hc["bin"] is None and not hc["map_written"]
                  and hc["stderr"] == f"gen_desc_image: {hb['msg']}")
        bad += not ok
        rows.append({"case": name, "expect": expect, "pass": ok,
                     "head_build": hb.get("msg", "packed %d bytes" % len(hb.get("image", b""))),
                     "head_cli_rc": hc["rc"], "head_cli_wrote_image": hc["bin"] is not None,
                     "head_cli_wrote_map": hc["map_written"],
                     "base_build": (bb.get("kind", "") + ": " + bb["msg"]) if not bb["ok"]
                     else "packed %d bytes" % len(bb["image"]),
                     "base_cli_rc": bc["rc"]})
        print(f"{'PASS' if ok else 'FAIL'}  {name:42} head: {rows[-1]['head_build'][:70]}"
              f" | base: {rows[-1]['base_build'][:40]}")
    OUT.write_text(json.dumps(rows, indent=1) + "\n")
    print(f"{len(rows) - bad}/{len(rows)} probes as expected")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
