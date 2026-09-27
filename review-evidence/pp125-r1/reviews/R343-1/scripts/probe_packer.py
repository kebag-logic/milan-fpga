#!/usr/bin/env python3
"""Probe the processor descriptor packer against the enforcement statements of
docs/architecture/07_memory_maps.md section 3.1 (PR #126).

Usage: probe_packer.py <path/to/gen_desc_image.py> <path/to/example_milan_8.json>

Every probe starts from a fresh copy of the example model, applies one change
and calls build(). Each row prints the expected outcome (the statement the
document makes) and the observed outcome; exit status is the number of rows
whose observation disagrees with the expectation. Accepted probes also verify
that the mutated bytes survive into the packed image, so an accepted row is not
the result of the packer silently normalising the mutation.
"""
import copy
import importlib.util
import json
import sys


def load_packer(path):
    spec = importlib.util.spec_from_file_location("gen_desc_image_probe", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def find(model, typ, idx=0, cfg=0):
    for d in model["descriptors"]:
        if d["type"] == typ and d.get("index", 0) == idx and d.get("configuration", 0) == cfg:
            return d
    raise KeyError((typ, idx, cfg))


def as_bytes_form(P, desc, body):
    """Replace a descriptor's input with the literal-hex form of `body`."""
    for k in ("fields", "pad_to"):
        desc.pop(k, None)
    desc["bytes"] = body.hex()


def u16(b, off, v):
    b[off:off + 2] = v.to_bytes(2, "big")


def main():
    P = load_packer(sys.argv[1])
    base = json.load(open(sys.argv[2], encoding="utf-8"))
    rows = []

    def probe(name, expect, mutate):
        m = copy.deepcopy(base)
        needle = mutate(P, m)
        try:
            img, _ = P.build(m)
            got = "accepted"
            if needle is not None and needle not in img:
                got = "accepted-but-mutation-not-in-image"
        except P.ImageError as exc:
            got = "refused: " + str(exc)
        ok = got.split(":")[0] == expect
        rows.append((ok, name, expect, got))

    # ---- controls ---------------------------------------------------------
    probe("control: pristine example", "accepted", lambda P, m: None)

    def au_bytes(P, m, edit, pad=None):
        d = find(m, "AUDIO_UNIT")
        b = bytearray(P.descriptor_bytes(d))
        edit(b)
        as_bytes_form(P, d, bytes(b))
        return bytes(b)

    probe("control: AUDIO_UNIT bytes form, 144/2/152", "accepted",
          lambda P, m: au_bytes(P, m, lambda b: None))

    def line_bound(n):
        def mut(P, m):
            d = find(m, "AUDIO_UNIT")
            d["pad_to"] = n
            return None
        return mut
    probe("boundary: AUDIO_UNIT padded to 576 (line buffer)", "accepted", line_bound(576))

    # ---- statements: the packer rejects ... -------------------------------
    probe("enforced: descriptor 577 bytes > 576 line buffer", "refused", line_bound(577))

    def index_gap(P, m):
        find(m, "CLOCK_SOURCE")["index"] = 1
        find(m, "CLOCK_SOURCE", 1)["fields"][1]["value"] = 1
    probe("enforced: per-type index gap (CLOCK_SOURCE [1])", "refused", index_gap)

    def cfg_gap(P, m):
        d = copy.deepcopy(find(m, "CLOCK_SOURCE"))
        d["configuration"] = 2
        m["descriptors"].append(d)
    probe("enforced: configuration gap (cfg {0,2})", "refused", cfg_gap)

    def dup(P, m):
        m["descriptors"].append(copy.deepcopy(find(m, "CLOCK_SOURCE")))
    probe("enforced: duplicate (cfg,type,index) key", "refused", dup)

    def name_bind(P, m):
        d = find(m, "AUDIO_UNIT")
        d["fields"][2]["string"] = "Audio Unit X"
    probe("enforced: inline object_name differs from name table", "refused", name_bind)

    def key_fields(field, value):
        def mut(P, m):
            find(m, "AUDIO_UNIT")["fields"][field]["value"] = value
        return mut
    probe("enforced: body type != key, fields form", "refused", key_fields(0, "0x0003"))
    probe("enforced: body index != key, fields form", "refused", key_fields(1, 1))

    def key_bytes(off, v):
        return lambda P, m: au_bytes(P, m, lambda b: u16(b, off, v))
    probe("enforced: body type != key, bytes form", "refused", key_bytes(0, 0x0003))
    probe("enforced: body index != key, bytes form", "refused", key_bytes(2, 1))

    # ---- statements: the packer does NOT enforce L10 / L6 -----------------
    probe("not enforced L10: sampling_rates_offset 143", "accepted",
          key_bytes(140, 143))

    def au_rates(count, words, trunc=0):
        def edit(b):
            u16(b, 142, count)
            del b[144:]
            for w in words:
                b += w.to_bytes(4, "big")
            if trunc:
                del b[-trunc:]
        return lambda P, m: au_bytes(P, m, edit)
    probe("not enforced L10: count 9, length 144+36", "accepted",
          au_rates(9, [48000] * 9))
    probe("boundary L10: count 8, length 144+32", "accepted",
          au_rates(8, [48000] * 8))
    probe("not enforced L10: count 3 but two words (length 152)", "accepted",
          au_rates(3, [48000, 96000]))
    probe("not enforced L10: count 2, one byte short (length 151)", "accepted",
          au_rates(2, [48000, 96000], trunc=1))

    def cd_list(count, lst):
        def mut(P, m):
            d = find(m, "CLOCK_DOMAIN")
            b = bytearray(P.descriptor_bytes(d))
            u16(b, 74, count)
            del b[76:]
            for s in lst:
                b += s.to_bytes(2, "big")
            as_bytes_form(P, d, bytes(b))
            return bytes(b)
        return mut
    probe("not enforced L6: clock_sources list [1,0]", "accepted", cd_list(2, [1, 0]))
    probe("not enforced L6: clock_sources list [1] count 1", "accepted", cd_list(1, [1]))

    # ---- informational: F07.2 / #122 -------------------------------------
    def zero_cluster_port(P, m):
        body = bytearray(20)
        u16(body, 0, 0x000E)          # STREAM_PORT_INPUT, index 0
        # clock_domain 0, flags 0, controls 0/0, clusters 0/0, maps 0/0
        m["descriptors"].append({"configuration": 0, "type": "STREAM_PORT_INPUT",
                                 "index": 0, "bytes": bytes(body).hex()})
        return bytes(body)
    probe("info F07.2: STREAM_PORT_INPUT number_of_clusters=0 packs (no waiver)",
          "accepted", zero_cluster_port)

    bad = 0
    for ok, name, expect, got in rows:
        bad += not ok
        print(f"{'PASS' if ok else 'MISMATCH'} | {name} | expect {expect} | {got}")
    print(f"rows {len(rows)} mismatches {bad}")
    return bad


if __name__ == "__main__":
    sys.exit(main())
