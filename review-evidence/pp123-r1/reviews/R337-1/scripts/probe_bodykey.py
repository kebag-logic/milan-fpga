#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probes of the descriptor body/directory-key check.

Usage: probe_bodykey.py GENERATOR  -> prints one JSON line per probe and a
summary; exit 0 when every probe's observed outcome matches its expectation for
the revision named by --expect {head,base}.

Each probe is a small, otherwise-legal model so that only the body/key relation
decides acceptance. Every probe is run through build() AND the CLI; the CLI
must return 1 and leave no image/map on refusal, 0 and write both on accept,
and the CLI image must equal build()'s.
"""
import argparse
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def load(path):
    spec = importlib.util.spec_from_file_location("gdi_probe", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def doc(descs, names=None):
    d = {"format": "kl-aem-image", "version": 1, "descriptors": descs}
    if names is not None:
        d["names"] = names
    return d


def b(key, idx, body_hex, **kw):
    d = {"type": key, "index": idx, "bytes": body_hex}
    d.update(kw)
    return d


def f(key, idx, fields, **kw):
    d = {"type": key, "index": idx, "fields": fields}
    d.update(kw)
    return d


def named_body(t, i, name, total=72):
    nm = name.encode()[:64].ljust(64, b"\0")
    return (t.to_bytes(2, "big") + i.to_bytes(2, "big") + nm).ljust(total, b"\0").hex()


def entity_body(t=0, i=0, ename="E", gname="G"):
    body = bytearray(244)
    body[0:2] = t.to_bytes(2, "big")
    body[2:4] = i.to_bytes(2, "big")
    body[48:112] = ename.encode().ljust(64, b"\0")
    body[180:244] = gname.encode().ljust(64, b"\0")
    return body.hex()


# (name, model, expect_head, expect_base, message_fragment_on_head_refusal)
# expect: "accept" / "refuse" / "crash" (non-ImageError exception)
PROBES = [
    # --- the legal pair and the two single mismatches, both forms
    ("legal_bytes", doc([b("AUDIO_CLUSTER", 0, "0014 0000 cafe")]), "accept", "accept", None),
    ("legal_fields", doc([f("AUDIO_CLUSTER", 0, [{"size": 2, "value": 0x14}, {"size": 2, "value": 0}])]),
     "accept", "accept", None),
    ("type_bytes", doc([b("AUDIO_CLUSTER", 0, "0015 0000 cafe")]), "refuse", "accept",
     "cfg 0 directory key type 0x0014 index 0 disagrees with body type 0x0015 index 0"),
    ("index_bytes", doc([b("AUDIO_CLUSTER", 0, "0014 0001 cafe")]), "refuse", "accept",
     "cfg 0 directory key type 0x0014 index 0 disagrees with body type 0x0014 index 1"),
    ("type_fields", doc([f("AUDIO_CLUSTER", 0, [{"size": 2, "value": 0x15}, {"size": 2, "value": 0}])]),
     "refuse", "accept", "body type 0x0015 index 0"),
    ("index_fields", doc([f("AUDIO_CLUSTER", 0, [{"size": 2, "value": 0x14}, {"size": 2, "value": 1}])]),
     "refuse", "accept", "body type 0x0014 index 1"),
    # --- endianness and single-byte discrimination
    ("type_little_endian_bytes", doc([b("AUDIO_CLUSTER", 0, "1400 0000")]), "refuse", "accept", "body type 0x1400"),
    ("index_little_endian_bytes", doc([b("AUDIO_CLUSTER", 0, "0014 0000"), b("AUDIO_CLUSTER", 1, "0014 0100")]),
     "refuse", "accept", "index 1 disagrees with body type 0x0014 index 256"),
    ("type_high_byte_only", doc([b(0x1234, 0, "1334 0000")]), "refuse", "accept", "body type 0x1334"),
    ("type_low_byte_only", doc([b(0x1234, 0, "1235 0000")]), "refuse", "accept", "body type 0x1235"),
    # --- other field shapes that still assemble the first four bytes
    ("fields_one_u32_legal", doc([f("AUDIO_CLUSTER", 0, [{"size": 4, "value": "0x00140000"}])]), "accept", "accept", None),
    ("fields_one_u32_bad", doc([f("AUDIO_CLUSTER", 0, [{"size": 4, "value": "0x00140002"}])]), "refuse", "accept",
     "body type 0x0014 index 2"),
    ("fields_split_bytes_bad", doc([f("AUDIO_CLUSTER", 0, [{"size": 1, "bytes": "00"}, {"size": 0},
                                                           {"size": 1, "bytes": "15"}, {"size": 2}])]),
     "refuse", "accept", "body type 0x0015"),
    ("fields_string_type_bad", doc([f("AUDIO_CLUSTER", 0, [{"size": 4, "string": "AB"}])]), "refuse", "accept",
     "body type 0x4142"),
    ("fields_absent_zero_body_bad", doc([f("AUDIO_CLUSTER", 0, [{"size": 4}])]), "refuse", "accept",
     "body type 0x0000 index 0"),
    # --- pad_to cannot manufacture agreement except where zeros ARE the key
    ("pad_to_short_body_legal", doc([b("AUDIO_CLUSTER", 0, "0014", pad_to=8)]), "accept", "accept", None),
    ("pad_to_empty_body_nonzero_key", doc([b("AUDIO_CLUSTER", 0, "", pad_to=8)]), "refuse", "accept",
     "body type 0x0000 index 0"),
    ("pad_to_empty_fields_nonzero_key", doc([{"type": "AUDIO_CLUSTER", "pad_to": 8}]), "refuse", "accept",
     "body type 0x0000"),
    ("pad_to_type_ok_index_bad", doc([b("AUDIO_CLUSTER", 0, "0014 0000"), b("AUDIO_CLUSTER", 1, "0014", pad_to=4)]),
     "refuse", "accept", "index 1 disagrees with body type 0x0014 index 0"),
    # --- grouped descriptors: the mismatch sits in the middle / a later run
    ("group_middle_bad", doc([b("AUDIO_MAP", i, f"0017{j:04x}00") for i, j in ((0, 0), (1, 2), (2, 2))]),
     "refuse", "accept", "index 1 disagrees with body type 0x0017 index 2"),
    ("mixed_length_run_bad", doc([b("STREAM_INPUT", 0, "0005 0000 aa"), b("STREAM_INPUT", 1, "0005 0001 aabb"),
                                  b("STREAM_INPUT", 2, "0006 0002 aabb")]),
     "refuse", "accept", "type 0x0005 index 2 disagrees with body type 0x0006 index 2"),
    ("second_config_bad", doc([b("AUDIO_MAP", 0, "0017 0000"), dict(b("AUDIO_MAP", 0, "0017 0001"), configuration=1)]),
     "refuse", "accept", "cfg 1 directory key type 0x0017 index 0"),
    ("swapped_pair_bad", doc([b("AUDIO_MAP", 0, "0017 0001"), b("AUDIO_MAP", 1, "0017 0000")]), "refuse", "accept",
     "index 0 disagrees with body type 0x0017 index 1"),
    ("body_claims_other_type_same_pair", doc([b("AUDIO_MAP", 0, "0014 0000"), b("AUDIO_CLUSTER", 0, "0017 0000")]),
     "refuse", "accept", "disagrees"),
    # --- name_index handling: a named group, named ENTITY
    ("named_group_legal", doc([f("AUDIO_CLUSTER", i, [{"size": 72, "bytes": named_body(0x14, i, n)}], name_index=i)
                               for i, n in ((0, "a"), (1, "b"))], names=["a", "b"]), "accept", "accept", None),
    ("named_group_index_bad", doc([f("AUDIO_CLUSTER", i, [{"size": 72, "bytes": named_body(0x14, j, n)}],
                                     name_index=i) for i, j, n in ((0, 0, "a"), (1, 0, "b"))], names=["a", "b"]),
     "refuse", "accept", "index 1 disagrees with body type 0x0014 index 0"),
    ("named_minus1_type_bad", doc([b("AUDIO_CLUSTER", 0, "0015 0000", name_index=-1)]), "refuse", "accept",
     "body type 0x0015"),
    ("entity_legal", doc([b("ENTITY", 0, entity_body(), name_index=0)], names=["E", "G"]), "accept", "accept", None),
    ("entity_type_bad", doc([b("ENTITY", 0, entity_body(t=1), name_index=0)], names=["E", "G"]), "refuse", "accept",
     "type 0x0000 index 0 disagrees with body type 0x0001 index 0"),
    # --- key spellings; out-of-range keys can never agree with a u16 body
    ("key_hexstr_legal", doc([b("0x0017", "0x0", "0017 0000")]), "accept", "accept", None),
    ("key_decstr_bad", doc([b("23", "0", "0017 0001")]), "refuse", "accept", "index 1"),
    ("key_type_over_u16", doc([b(0x10017, 0, "0017 0000")]), "refuse", "crash", "type 0x10017"),
    ("key_index_negative", doc([b("AUDIO_MAP", -1, "0017 ffff")]), "refuse", "refuse", "index -1"),
]


def run(gen_path, mod, model, tmp):
    out = {}
    try:
        img, rep = mod.build(model)
        out["build"] = "accept"
    except mod.ImageError as exc:
        out["build"] = "refuse"; out["msg"] = str(exc); img = rep = None
    except Exception as exc:  # noqa: BLE001 - reported, not hidden
        out["build"] = "crash"; out["msg"] = f"{type(exc).__name__}: {exc}"; img = rep = None
    src = tmp / "m.json"; ib = tmp / "i.bin"; im = tmp / "i.map"
    for p in (ib, im):
        if p.exists():
            p.unlink()
    src.write_text(json.dumps(model))
    r = subprocess.run([sys.executable, "-B", str(gen_path), "-i", str(src), "-o", str(ib), "-m", str(im)],
                       capture_output=True, text=True, timeout=60)
    out["cli_rc"] = r.returncode
    out["cli_stderr"] = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else ""
    out["cli_wrote"] = [p.name for p in (ib, im) if p.exists()]
    out["cli_image_equals_build"] = (img is not None and ib.exists() and ib.read_bytes() == img
                                     and im.read_text() == rep)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("generator")
    ap.add_argument("--expect", choices=("head", "base"), required=True)
    a = ap.parse_args()
    gen = Path(a.generator).resolve()
    mod = load(gen)
    bad = 0
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        for name, model, eh, eb, frag in PROBES:
            want = eh if a.expect == "head" else eb
            o = run(gen, mod, model, tmp)
            ok = o["build"] == want
            if want == "accept":
                ok = ok and o["cli_rc"] == 0 and o["cli_image_equals_build"]
            elif want == "refuse":
                ok = ok and o["cli_rc"] == 1 and o["cli_wrote"] == [] and \
                    o["cli_stderr"] == f"gen_desc_image: {o['msg']}"
                if a.expect == "head" and frag:
                    ok = ok and frag in o["msg"]
            else:
                ok = ok and o["cli_rc"] != 0
            bad += not ok
            print(json.dumps({"probe": name, "expect": want, "ok": ok, **o}, sort_keys=True))
    print(f"SUMMARY {a.expect}: {len(PROBES)} probes, {len(PROBES) - bad} as expected, {bad} unexpected")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
