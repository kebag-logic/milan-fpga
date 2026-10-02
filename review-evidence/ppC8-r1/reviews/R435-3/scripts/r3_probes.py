#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Round-3 delta probes of the descriptor model lint (reviewer-owned).

usage: r3_probes.py TREE [BASE_TREE]

TREE is an extraction of the processor repository at the head under review;
BASE_TREE (optional) one at the previous round's head, used only to compare
milan_min.json's model digest. Each probe edits a copy of milan_min.json
(bodies normalised to literal bytes) with this script's own layout helpers,
not the gate's, and records whether build() packs it or which checks refuse
it, beside the table text that decides it:
  IEEE 1722.1-2021 7.2.6 Table 7-8: formats_offset 138, N <= 46,
      redundant_offset 138+8N, R <= 8, redundant_streams 2*R octets.
  Milan v1.2 Annex C Table C.1: formats_offset 136, N <= 47,
      redundant_offset 136+8N, R <= 8, redundant_streams 2*R octets.
  IEEE 1722.1-2021 7.2: a descriptor is at most 508 octets.
Nothing in TREE is written. Exit 1 if any probe is unexpected.
"""
import copy
import importlib.util
import json
import struct
import sys
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
DESC = TREE / "hdl/aecp/desc"
sys.path.insert(0, str(TREE / "tb/desc_store"))
import lint_mutations as mut  # noqa: E402  (body/store/put/add helpers only)


def load(tree: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, tree / "hdl/aecp/desc/gen_desc_image.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gdi = load(TREE, "gdi_head")
MIN = json.loads((DESC / "milan_min.json").read_text(encoding="utf-8"))


def normalised(model):
    out = copy.deepcopy(model)
    for row in out["descriptors"]:
        row["bytes"] = gdi.descriptor_bytes(row).hex()
        row["type"] = gdi._type_code(row["type"])
        for key in ("fields", "pad_to"):
            row.pop(key, None)
        if row["type"] != mut.ENTITY:
            row.pop("name_index", None)
    return out


def outcome(model, **kw):
    try:
        _, report = gdi.build(model, **kw)
        return "PACK", report
    except gdi.ImageError as exc:
        lines = str(exc).splitlines()
        checks = sorted({ln.split(":")[0] for ln in lines})
        return "REFUSE " + "; ".join(checks), "\n".join(lines)


RESULTS = []


def probe(name, expect, basis, model, detail=None, **kw):
    got, text = outcome(model, **kw)
    if expect == "PACK":
        ok = got == "PACK"
    else:
        ok = got.startswith("REFUSE") and expect.split(" ", 1)[1] in got
        if ok and detail is not None:
            ok = detail in text
    RESULTS.append((name, expect, got, "as-expected" if ok else "UNEXPECTED", basis, text))


S_IN0, S_IN1, S_OUT0 = (mut.STREAM_INPUT, 0, 0), (mut.STREAM_INPUT, 1, 0), (mut.STREAM_OUTPUT, 0, 0)


def formats_of(model, at):
    data = mut.body(model, *at)
    off, n = struct.unpack_from(">HH", data, 82)
    return n, data[off:off + 8 * n]


def relay(model, at, *, offset=136, n=None, words=None, streams=(), red_off=None, red_cnt=None,
          extra=b""):
    """Lay a stream out again from scratch: the 136-octet head of Table 7-8/C.1,
    a 2-octet timing field when offset is 138, the formats, then the tail."""
    data = mut.body(model, *at)
    cur_n, cur_words = formats_of(model, at)
    if words is None:
        words = cur_words
    if n is None:
        n = len(words) // 8
    head = bytearray(data[:136])
    struct.pack_into(">HH", head, 82, offset, n)
    struct.pack_into(">H", head, 132, offset + 8 * n if red_off is None else red_off)
    struct.pack_into(">H", head, 134, len(streams) if red_cnt is None else red_cnt)
    timing = bytes(offset - 136) if offset > 136 else b""   # 138: Table 7-8's timing
    mut.store(model, at, bytes(head) + timing + bytes(words)
              + b"".join(struct.pack(">H", s) for s in streams) + extra)


base = normalised(MIN)
n_out, w_out = formats_of(base, S_OUT0)
word_out = w_out[:8]

TBL78 = "IEEE 1722.1-2021 Table 7-8"
TBLC1 = "Milan v1.2 Annex C Table C.1"

# --- A. positives the ruling and both tables allow
m = copy.deepcopy(base)
for at in (S_IN0, S_IN1, S_OUT0):
    relay(m, at)
probe("A1 every stream in Annex C, R=0", "PACK", TBLC1 + "; Milan 5.3.3.4 'may use ... for any'", m)

m = copy.deepcopy(base)
relay(m, S_OUT0, streams=(0,))
probe("A2 Annex C output, R=1 (index not paired: pair rules are not linted, 07 3.1)", "PACK",
      TBLC1 + "; ruling 5956187186: pair rules on the Not linted list", m)

m = copy.deepcopy(base)
relay(m, S_OUT0, streams=tuple(range(8)))
probe("A3 Annex C output, R=8 (cap value)", "PACK", TBLC1 + " R max 8", m)

m = copy.deepcopy(base)
relay(m, S_IN0, streams=(1,))
relay(m, S_IN1, streams=(0,))
probe("A4 Annex C input pair, each naming the other, R=1", "PACK",
      TBLC1 + "; Milan 'Redundant Pair' definition", m)

m = copy.deepcopy(base)
relay(m, S_OUT0, words=word_out * 46)
probe("A5 Annex C output, N=46, R=0 (504 octets)", "PACK", TBLC1 + "; 508-octet 7.2 maximum", m)

m = copy.deepcopy(base)
relay(m, S_OUT0, words=word_out * 46, streams=(0, 0))
probe("A6 Annex C output, N=46, R=2 (508 octets, the 7.2 maximum)", "PACK",
      TBLC1 + "; 508-octet 7.2 maximum", m)

m = copy.deepcopy(base)
relay(m, S_OUT0, offset=138)
probe("A7 control: Table 7-8 relaid by this script, R=0", "PACK", TBL78, m)

# --- B. inconsistent or out-of-bound layouts stay refused
m = copy.deepcopy(base)
relay(m, S_OUT0, words=word_out * 46, streams=(0, 0, 0))
probe("B1 Annex C N=46 R=3 (510 octets)", "REFUSE L12", "IEEE 7.2 508 octets", m)

m = copy.deepcopy(base)
relay(m, S_OUT0, words=word_out * 47)
probe("B2 Annex C N=47 R=0 (512 octets; C.1 says N<=47 but 7.2 caps at 508)", "REFUSE L4 format-count",
      "IEEE 7.2 508 octets; 07 3.1 N<=46", m)

m = copy.deepcopy(base)
relay(m, S_OUT0, streams=tuple(range(9)))
probe("B3 Annex C R=9", "REFUSE L4 stream-layout", TBLC1 + " R max 8", m, detail="above 8")

m = copy.deepcopy(base)
relay(m, S_OUT0, offset=138, streams=(0,))
probe("B4 Table 7-8 with R=1 tail of consistent length", "REFUSE L4 stream-layout",
      "Milan 5.3.3.4: redundant-pair streams shall use Annex C", m, detail="Table 7-8 layout")

m = copy.deepcopy(base)
relay(m, S_OUT0, red_off=138 + 8 * n_out)
probe("B5 Annex C with Table 7-8's redundant_offset", "REFUSE L4 stream-layout",
      TBLC1 + " redundant_offset 136+8N", m, detail=f"redundant_offset {138 + 8 * n_out}")

m = copy.deepcopy(base)
relay(m, S_OUT0, offset=138, red_off=136 + 8 * n_out)
probe("B6 Table 7-8 with Annex C's redundant_offset", "REFUSE L4 stream-layout",
      TBL78 + " redundant_offset 138+8N", m, detail=f"redundant_offset {136 + 8 * n_out}")

m = copy.deepcopy(base)
relay(m, S_OUT0, red_cnt=1)
probe("B7 Annex C counting R=1, tail absent", "REFUSE L4 stream-layout", TBLC1 + " 2*R tail", m,
      detail="make")

m = copy.deepcopy(base)
relay(m, S_OUT0, extra=bytes(2))
probe("B8 Annex C, R=0 with two stray tail octets", "REFUSE L4 stream-layout", TBLC1, m, detail="make")

m = copy.deepcopy(base)
relay(m, S_OUT0, streams=(0,), extra=bytes(2))
probe("B9 Annex C, R=1 with two stray tail octets", "REFUSE L4 stream-layout", TBLC1, m, detail="make")

m = copy.deepcopy(base)
data = mut.body(m, *S_OUT0)
struct.pack_into(">H", data, 82, 136)
mut.store(m, S_OUT0, bytes(data))
probe("B10 Table 7-8 body with only formats_offset changed to 136", "REFUSE L4 stream-layout",
      "offset/length disagree", m)

m = copy.deepcopy(base)
data = mut.body(m, *S_OUT0)
struct.pack_into(">H", data, 82, 137)
mut.store(m, S_OUT0, bytes(data))
probe("B11 formats_offset 137", "REFUSE L4 stream-layout", "neither table", m, detail="formats_offset 137")

m = copy.deepcopy(base)
relay(m, S_OUT0, offset=140)
probe("B12 list moved to 140, offsets consistent", "REFUSE L4 stream-layout", "neither table", m,
      detail="formats_offset 140")

m = copy.deepcopy(base)
relay(m, S_OUT0, red_cnt=0x8000)
probe("B13 Annex C R=0x8000 (huge), no tail", "REFUSE L4 stream-layout", TBLC1 + " R max 8", m,
      detail="above 8")

# --- C. the other L4 checks read the list through formats_offset in Annex C
m = copy.deepcopy(base)
relay(m, S_IN0)
mut.put(m, S_IN0, 74, 0x0123456789ABCDEF, 8)
probe("C1 Annex C input whose current_format is outside its list", "REFUSE L4 current-format",
      "Milan 5.3.3.4 current_format in list", m)

m = copy.deepcopy(base)
relay(m, S_OUT0, words=bytes(w_out) + struct.pack(">Q", mut.CRF))
probe("C2 Annex C output listing AAF and CRF", "REFUSE L4 format-family", "Milan 5.3.3.4", m)

m = copy.deepcopy(base)
relay(m, S_OUT0, words=word_out * 47)          # 47 at 136 must still be counted
probe("C3 format-count reads N from an Annex C list", "REFUSE L4 format-count", "07 3.1 N<=46", m,
      detail="above 46")

# --- D. the digest: milan_min's recorded value, and a layout change moves it
recorded = json.loads((DESC / "model_ids.json").read_text(encoding="utf-8"))["models"]
_, rep = gdi.build(MIN)
digest_line = [ln for ln in rep.splitlines() if "digest" in ln.lower()]
print("milan_min digest lines at TREE:", digest_line)
print("model_ids.json at TREE:", recorded)
if len(sys.argv) > 2:
    gbase = load(Path(sys.argv[2]).resolve(), "gdi_base")
    _, rep_b = gbase.build(json.loads((Path(sys.argv[2]) / "hdl/aecp/desc/milan_min.json").read_text()))
    same = [ln for ln in rep_b.splitlines() if "digest" in ln.lower()] == digest_line
    print("milan_min digest identical to BASE_TREE:", same)
    if not same:
        RESULTS.append(("D0 milan_min digest vs base", "same", "differs", "UNEXPECTED", "assignment", ""))


def digest_of(model):
    try:
        _, report = gdi.build(model)
    except gdi.ImageError as exc:
        return ["refused: " + str(exc).splitlines()[0]]
    return [ln for ln in report.splitlines() if "model digest" in ln.lower() or "digest:" in ln.lower()]


m = copy.deepcopy(base)
relay(m, S_OUT0)
d_annex = digest_of(m)
d_base = digest_of(base)
moved = d_annex != d_base
RESULTS.append(("D1 Annex C relayout moves the digest (structure, IEEE 6.2.2.8)", "moves",
                "moves" if moved else "same", "as-expected" if moved else "UNEXPECTED", "6.2.2.8", ""))
annex = bytes(mut.body(m, *S_OUT0))
redm = copy.deepcopy(base)
relay(redm, S_OUT0, streams=(0,))
annex_r = bytes(mut.body(redm, *S_OUT0))


def same_digest(data, at):
    edited = bytearray(data)
    edited[at] ^= 0x5A
    md = gdi.model_lint.model_digest
    return md({0: {mut.STREAM_OUTPUT: {0: data}}}) == md({0: {mut.STREAM_OUTPUT: {0: bytes(edited)}}})


for what, data, at, want in (("current_format first octet", annex, 74, True),
                             ("current_format last octet", annex, 81, True),
                             ("formats_offset", annex, 83, False),
                             ("first format octet at 136", annex, 136, False),
                             ("redundant_streams[0] octet", annex_r, len(annex_r) - 1, False)):
    got = same_digest(data, at)
    RESULTS.append((f"D2 Annex C {what}: digest {'kept' if want else 'moves'}", str(want), str(got),
                    "as-expected" if got == want else "UNEXPECTED", "IEEE 6.2.2.8", ""))

# --- E. loader: model_lint gets the packer's loader
lint = gdi.model_lint
ok = getattr(lint, "beside", None) is getattr(gdi, "_beside", object())
RESULTS.append(("E1 model_lint.beside is gen_desc_image._beside", "True", str(ok),
                "as-expected" if ok else "UNEXPECTED", "R435-2 S1", ""))
mods = [k for k in sys.modules if k in ("model_lint", "model_rules")]
RESULTS.append(("E2 no model_lint/model_rules in sys.modules", "[]", str(mods),
                "as-expected" if not mods else "UNEXPECTED", "S3 round 2", ""))

bad = 0
for name, expect, got, verdict, basis, text in RESULTS:
    bad += verdict == "UNEXPECTED"
    print(f"{verdict:12} {name}\n             expect {expect}; got {got}; basis {basis}")
    if text and got != "PACK":
        for ln in text.splitlines()[:4]:
            print("             | " + ln)
print(f"{len(RESULTS)} probes, {bad} unexpected")
sys.exit(1 if bad else 0)
