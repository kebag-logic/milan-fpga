# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""nvm_fixture.py - the oracle of the saved-state store's GoogleTest suite (#665 lanes F1 and FT).

For one shape, every container the tests load or compare a slot with, every
payload set a restore must leave, and the shape's facts, written into a
directory the test binary reads (nvm_suite.hpp, "the fixture"). Every byte
comes from scripts/nvm_klj3.py (klj3_assemble, frame_record3, klj3_decode):
the split placement's KLJ3 and layout 3 (#823). The refusal table is the
shipping writer's suite's, rule for rule, in that framing, with the rules
layout 3 adds. The all-fabric placement's KLJ2 container for the shape, the
one the store must refuse, comes from scripts/nvm_klj2.py; the recorded
vectors' records and offsets from tb/verilator/nvm_backend. None of it comes
from the C store.

An image is named by a recipe, which the tests spell:

    SET@SEQ[~AT | /majorK | /foreign]      parity/N

SET is the records: golden (the shape's frames), erased (every record
erased), half (every other record erased), changedXX (the first record of
every group with a new payload, seed 0xXX), oneN (the last record with the
value test seed N gives it), erased_oneN (the same over erased records) or
frames (the vector bench's frames). SEQ is the sequence in hex. ~AT flips bit
7 of byte AT and leaves the trailer as it was (a torn slot); /majorK rewrites
the format word's major version and /foreign the entity model id, both
resealed. parity/N is the N-th refusal of the verdict-parity table.
"""

from __future__ import annotations

import re
import struct
import sys
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from nvm_contract import KLJ2_HDR, VD_LEN, VD_OK, Donor, Ident          # noqa: E402
from nvm_klj2 import crc16_ccitt, frame_record, key_of_id, klj2_assemble, payload_bytes  # noqa: E402
from nvm_klj3 import (DHDR, HDR, KLD3_MAGIC, KLD3_VER, KLJ3_FMT_VER, KLJ3_FMT_VER_0, LAYOUT, PAGE, REC_HDR3,  # noqa: E402
                      delta_base, delta_end, erased_record3, frame_record3, inventory3, klj3_delta, record_places,
                      rid_of_key3)
from nvm_shape import binding_base, inventory, layout_version          # noqa: E402

from nvm_bench import JOURNAL, LEGACY, LEGACY_SLOT, SLOT, Bench        # noqa: E402
from flash_map import literal                                           # noqa: E402

REC_HDR = REC_HDR3

TABLE_DIR = ROOT / "tb/verilator/nvm_backend"
#: Sequences the authority checks meet the restart at (test_nvm_write.cpp kAuthSeqs).
AUTH_SEQS = (1, 5, 0x8000_0000, 0xFFFF_FFFF)
#: The sequence pairs of newer_wins and read_flip_boot.
NEWER_WINS = ((9, 10), (10, 9), (0xFFFF_FFFF, 0), (0, 0xFFFF_FFFF), (7, 7), (0xFFFF_FFFF, 0xFFFF_FFFF))
FLIP_PAIRS = ((5, 6), (6, 5), (0xFFFF_FFFF, 0), (0, 0xFFFF_FFFF))
#: The seeds of the test's one-record changes whose committed slot is compared.
ONE_SEEDS = (3, 6, 22, 25, 26, 27)
#: Every payload set a test compares a restored state with.
PAYLOAD_SETS = ("golden", "half", "changed2b", "changed41", "changed37", "changed5c", "changed60", "changed61",
                "bind7", "bind8", "bind9")
#: #1009's delta frames: the base sequences of the two slots, and the binding saves after them (seed, sequence,
#: the sequence of the slot the frame goes to).
DELTA_SAVES = ((7, 7, 5), (8, 8, 6), (9, 9, 7))

_RECIPE = re.compile(r"^(?P<set>golden|frames|erased_one|erased|half|changed|one|bind)(?P<seed>[0-9a-f]+)?"
                     r"@(?P<seq>[0-9a-f]+)(?:~(?P<at>\d+)|/major(?P<major>\d+)|/(?P<foreign>foreign)"
                     r"|/(?P<minor1>minor1))?$")


def reseal(blob: bytes) -> bytes:
    """Recompute the CRC-32 trailer after an edit above it."""
    return blob[:-4] + struct.pack("<I", zlib.crc32(blob[:-4]) & 0xFFFF_FFFF)


def value(b: Bench, rid: int, seed: int) -> bytes:
    """A payload for record rid that no golden frame carries (test_nvm_write.cpp value())."""
    plen = len(b.frames[rid]) - REC_HDR
    return bytes((rid * 13 + j * 11 + seed) & 0xFF for j in range(plen))


def _rows(b: Bench) -> list[tuple]:
    """The shape's inventory rows with an id."""
    return [row for row in inventory3(b.shape) if row[2] is not None]


def changed_frames(b: Bench, seed: int) -> tuple[dict[int, bytes], dict[int, bytes]]:
    """The first record of every group with a new payload: (frames, payloads)."""
    firsts, seen = {}, set()
    for g, _i, rid, plen, _b in sorted(_rows(b), key=lambda t: t[2]):
        if g not in seen:
            seen.add(g)
            firsts[rid] = bytes((rid * 29 + j * 5 + seed) & 0xFF for j in range(plen))
    frames = dict(b.frames)
    frames.update({rid: frame_record3(rid, p) for rid, p in firsts.items()})
    return frames, firsts


def binding_ids(b: Bench) -> list[int]:
    """The record ids of the binding walk (D3 section 8.1 step 4)."""
    return sorted(rid for g, _i, rid, _p, _b in _rows(b) if g == "BINDING")


def frameset(b: Bench, name: str, seed: int | None) -> dict[int, bytes]:
    """The records a recipe's SET names."""
    last = max(b.frames)
    if name in ("golden", "frames"):
        return dict(b.frames)
    if name == "erased":
        return b.erased_frames()
    if name == "half":
        erased = b.erased_frames()
        return {rid: (erased[rid] if n % 2 == 0 else fr) for n, (rid, fr) in enumerate(sorted(b.frames.items()))}
    if name == "changed" and seed is not None:
        return changed_frames(b, seed)[0]
    if name == "bind" and seed is not None:
        # #1009: the first binding record changed, what a BIND_RX saves
        frames = dict(b.frames)
        rid = binding_ids(b)[0]
        frames[rid] = frame_record3(rid, value(b, rid, seed))
        return frames
    if name in ("one", "erased_one") and seed is not None:
        frames = b.erased_frames() if name == "erased_one" else dict(b.frames)
        frames[last] = frame_record3(last, value(b, last, seed))
        return frames
    raise ValueError(f"no record set {name!r}")


def image(b: Bench, recipe: str) -> bytes:
    """The container a recipe names, from the reference encoder."""
    if recipe.startswith("parity/"):
        return parity(b)[int(recipe.split("/", 1)[1])][1]
    m = _RECIPE.match(recipe)
    if m is None:
        raise ValueError(f"not a recipe: {recipe!r}")
    name, seed = m.group("set"), m.group("seed")
    seed_value = None if seed is None else int(seed, 16 if name == "changed" else 10)
    # a slot's image is the previous minor (#1009), which every boot test reads as the old format; /minor1 is the
    # minor the store writes, what a commit is compared with
    ver = KLJ3_FMT_VER if m.group("minor1") else KLJ3_FMT_VER_0
    blob = b.assemble(frameset(b, name, seed_value), int(m.group("seq"), 16), ver=ver)
    if m.group("at"):
        at = int(m.group("at"))
        return blob[:at] + bytes([blob[at] ^ 0x80]) + blob[at + 1:]
    if m.group("major"):
        return reseal(blob[:4] + struct.pack("<I", int(m.group("major")) << 16) + blob[8:])
    if m.group("foreign"):
        return reseal(blob[:28] + struct.pack("<I", 0xDEAD_0002) + blob[32:])
    return blob


def klj2_container(b: Bench, seq: int) -> bytes:
    """The all-fabric placement's KLJ2 container of this shape and identity,
    as the shipping writer would leave it (scripts/nvm_klj2.py, the donor's
    binding base and layout read from the processor RTL)."""
    donor = Donor(base=binding_base(), layout=layout_version())
    frames = {r: frame_record(r, payload_bytes(g, i, r, p), donor.layout)
              for g, i, r, p, _b in inventory(b.shape, donor.base) if r is not None}
    return klj2_assemble(frames, donor, Ident(seq=seq, entity_id=b.ident.entity_id,
                                              model_id=b.ident.model_id))[0]


def parity_cases(b: Bench) -> list[tuple[str, bytes]]:
    """Every refusal of section 6.2 and the erased-record rule, as bytes: the
    shipping writer suite's table (sw/firmware/nvm_hosttest/test_nvm_firmware.py
    parity_cases) rule for rule in KLJ3 and layout 3, then the rules #823 adds:
    a KLJ2 container is the previous format, the reserved header byte is zero,
    and no id lies past the layout 3 space."""
    full = b.assemble(b.frames, 3)
    rids = sorted(b.frames)
    first, last = rids[0], rids[-1]
    offs = b.offsets()
    plen_last = len(b.frames[last]) - REC_HDR

    def with_frames(frames: dict[int, bytes], nrec: int | None = None) -> bytes:
        """The container for `frames`, its N_REC word overridden when asked."""
        blob = b.assemble(frames, 3)
        return patched(blob, 12, struct.pack("<I", nrec)) if nrec is not None else blob

    def id_rewritten(rid: int, new_rid: int) -> dict[int, bytes]:
        """The golden frames with record `rid` re-framed under `new_rid`, its
        crc16 recomputed so only the id is wrong."""
        fr = b.frames[rid]
        hdr = fr[:4] + struct.pack(">H", new_rid) + fr[6:8]
        frames = dict(b.frames)
        frames[rid] = hdr + struct.pack(">H", crc16_ccitt(hdr + fr[REC_HDR:])) + fr[REC_HDR:]
        return frames

    def reserved_set() -> bytes:
        """The first record with its reserved header byte set, its crc16 closing."""
        fr = b.frames[first]
        hdr = fr[:3] + b"\x01" + fr[4:8]
        frames = dict(b.frames)
        frames[first] = hdr + struct.pack(">H", crc16_ccitt(hdr + fr[REC_HDR:])) + fr[REC_HDR:]
        return b.assemble(frames, 3)

    erased = b.erased_frames()
    half = dict(b.frames)
    for rid in rids[::2]:
        half[rid] = erased[rid]
    torn_erased = dict(b.frames)
    torn_erased[last] = erased_record3(plen_last)[:-1] + b"\x00"
    trunc = dict(b.frames)
    del trunc[last]
    return [
        ("full image", full),
        ("every record erased", b.assemble(erased, 3)),
        ("every other record erased", b.assemble(half, 3)),
        ("bad magic", patched(full, 0, b"KLJ1")),
        ("major version 2", patched(full, 4, struct.pack("<I", 0x0002_0000))),
        ("IMG_LEN 43", patched(full, 16, struct.pack("<I", 43))),
        (f"IMG_LEN {SLOT + 1}", patched(full, 16, struct.pack("<I", SLOT + 1))),
        ("bad CRC", patched(full, KLJ2_HDR + 1, bytes([full[KLJ2_HDR + 1] ^ 1]), False)),
        ("foreign entity", patched(full, 20, struct.pack("<I", 0xDEAD_0001))),
        ("foreign model", patched(full, 28, struct.pack("<I", 0xDEAD_0002))),
        ("record layout off", patched(full, 36, struct.pack("<I", LAYOUT.layout + 1))),
        ("record magic", patched(full, KLJ2_HDR + offs[first], b"\x17\x23")),
        ("unknown record id", with_frames(id_rewritten(last, last + 1))),
        ("duplicate record id", with_frames(id_rewritten(last, last - 1))),
        ("truncated by one record", with_frames(trunc)),
        ("N_REC one too many", with_frames(b.frames, len(rids) + 1)),
        ("N_REC one too few", with_frames(b.frames, len(rids) - 1)),
        ("erased header, live payload", b.assemble(torn_erased, 3)),
        ("erased span short by one", with_frames({r: erased[r] for r in rids[:-1]})),
        ("the shipping writer's KLJ2 container", klj2_container(b, 3)),
        ("a KLJ2 magic over KLJ3 bytes", patched(full, 0, b"KLJ2")),
        ("the reserved header byte set", reserved_set()),
        (f"record id {LAYOUT.id_space}, past the layout 3 space",
         with_frames(id_rewritten(last, LAYOUT.id_space))),
    ]


def parity_extra(b: Bench) -> list[tuple[str, bytes]]:
    """Refusals the shipping suite's table does not carry: a framed record
    whose length runs past the record area, an extra record past the shape's
    last, and a container longer than the stage whose CRC closes."""
    full = b.assemble(b.frames, 3)
    last = max(b.frames)
    off = KLJ2_HDR + b.offsets()[last]
    fr = b.frames[last]
    hdr = fr[:6] + struct.pack(">H", 0x4000)
    over = full[:off] + hdr + struct.pack(">H", crc16_ccitt(hdr + fr[REC_HDR:])) + full[off + REC_HDR:]
    extra = dict(b.frames)
    extra[last + 1] = frame_record3(last + 1, b"\x01\x02\x03\x04")
    body = full[KLJ2_HDR:-4] + bytes(100)
    head = full[:16] + struct.pack("<I", KLJ2_HDR + len(body) + 4) + full[20:KLJ2_HDR]
    return [("framed record overruns the area", reseal(over)),
            ("one record past the shape's last", b.assemble(extra, 3)),
            ("longer than the stage, CRC closing", reseal(head + body + bytes(4)))]


def patched(blob: bytes, at: int, new: bytes, seal: bool = True) -> bytes:
    """`blob` with `new` written at `at`, its trailer recomputed unless the
    corruption under test is the trailer itself."""
    out = blob[:at] + new + blob[at + len(new):]
    return reseal(out) if seal else out


def long_container(b: Bench) -> bytes:
    """A container longer than the stage whose CRC closes (parity_extra's last)."""
    return parity_extra(b)[2][1]


def codec_cases(b: Bench) -> list[tuple[str, bytes, bool]]:
    """Refusals of nvm_klj2.c the parity table does not reach, each crafted
    for one test of the acceptance order: (label, bytes, whether the codec is
    asked as the store asks of a container longer than the stage, with only
    NVM_STAGE_BYTES of it loaded)."""
    full = b.assemble(b.frames, 3)
    rids = sorted(b.frames)
    first, last = rids[0], rids[-1]
    offs = b.offsets()
    erased = b.erased_frames()
    beyond = dict(b.frames)
    beyond[last + 1] = erased_record3(0)
    cut = b.assemble({**b.frames, last: erased[last]}, 3)
    cut_body = cut[KLJ2_HDR:-4][:-8]
    cut = reseal(cut[:16] + struct.pack("<I", KLJ2_HDR + len(cut_body) + 4) + cut[20:KLJ2_HDR] + cut_body + bytes(4))
    at_first = KLJ2_HDR + offs[first]
    short = {**b.frames, last: frame_record3(last, b.frames[last][REC_HDR:-1])}
    long = long_container(b)
    at_last = KLJ2_HDR + offs[last]
    stage = len(full) + REC_HDR
    overrun = long[:at_last + 6] + struct.pack(">H", stage + 8 - (at_last + REC_HDR)) + long[at_last + 8:]
    return [("an erased header past the shape's last record", b.assemble(beyond, 3), False),
            ("the last record erased, its span cut short of its payload", cut, False),
            ("a record of another layout_version", patched(full, at_first + 2, bytes([full[at_first + 2] ^ 1])), False),
            ("a record whose crc16 does not close",
             patched(full, at_first + REC_HDR, bytes([full[at_first + REC_HDR] ^ 1])), False),
            ("a known record one payload byte short", b.assemble(short, 3), False),
            ("the entity_id's high word foreign", patched(full, 24, struct.pack("<I", 0xDEAD_0003)), False),
            ("the entity_model_id's high word foreign", patched(full, 32, struct.pack("<I", 0xDEAD_0004)), False),
            ("longer than the stage, its CRC not closing", long[:-1] + bytes([long[-1] ^ 1]), False),
            ("longer than the stage, a record running past the loaded bytes", reseal(overrun), True)]


def parity(b: Bench) -> list[tuple[str, bytes]]:
    """The verdict-parity table: the shipping writer suite's refusals in KLJ3, and parity_extra."""
    return parity_cases(b) + parity_extra(b)


def verdict(b: Bench, blob: bytes) -> int:
    """klj3_decode's verdict on a slot holding `blob`: VD_LEN for one no slot can hold."""
    return b.decode(blob)[0] if len(blob) <= SLOT else VD_LEN


def rid_payloads(b: Bench, blob: bytes) -> dict[int, bytes]:
    """record id -> payload of every FRAMED record klj3_decode applies."""
    vd, applied = b.decode(blob)
    return {rid_of_key3(k): v for k, v in applied.items()} if vd == VD_OK else {}


def payload_set(b: Bench, name: str) -> dict[int, bytes]:
    """A payload set a restored state is compared with, decoded from its image."""
    if name.endswith("_firsts"):
        return changed_frames(b, int(name[len("changed"):-len("_firsts")], 16))[1]
    return rid_payloads(b, image(b, f"{name}@5"))


def main_images() -> list[str]:
    """Every image test_nvm_boot.cpp and test_nvm_write.cpp load or compare with."""
    names = ["erased@0", "golden@5", "golden@6", "half@3", "golden@9", "golden@a~43", "golden@9~49", "golden@3",
             "golden@4/major2", "golden@4/major4", "changed41@4", "erased@1", "changed5c@6", "golden@5/foreign",
             "erased_one7@1", "changed21@6"]
    names += [f"golden@{a:x}" for a, _ in NEWER_WINS] + [f"changed2b@{b:x}" for _, b in NEWER_WINS]
    names += [f"golden@{a:x}" for a, _ in FLIP_PAIRS] + [f"changed37@{b:x}" for _, b in FLIP_PAIRS]
    names += [f"one{seed}@6" for seed in ONE_SEEDS]
    names += [f"changed6{x}@{seq:x}" for x in (0, 1) for seq in AUTH_SEQS]
    # what the store writes (#1009's minor 1), each compared with a commit or the stage
    names += [f"{n}/minor1" for n in ("erased@0", "erased@1", "golden@6", "erased_one7@1", "changed5c@6", "one3@6",
                                      "one6@6", "one22@6")]
    names += [f"one{seed}@6/minor1" for seed in ONE_SEEDS]
    return sorted(set(names))


def table(stem: str) -> dict | None:
    """The recorded vector of a shape: header values and record rows."""
    path = TABLE_DIR / f"records_{stem}.txt"
    if not path.exists():
        return None
    head, rows = {}, {}
    for line in path.read_text().splitlines():
        if line.startswith("#") or not line.strip():
            continue
        tag, *rest = line.split()
        if tag == "rec":
            rows[int(rest[0], 16)] = (int(rest[1]), int(rest[2]), int(rest[3]))
        else:
            head[tag] = rest[0]
    return {"head": head, "rows": rows}


class Writer:
    """manifest.txt and its blob files (the format nvm_suite.cpp reads)."""

    def __init__(self, out: Path) -> None:
        """Start an empty fixture directory at `out`."""
        out.mkdir(parents=True, exist_ok=True)
        self.out = out
        self.lines: list[str] = []

    def num(self, name: str, v: int) -> None:
        """One number."""
        self.lines.append(f"num {name} {v}")

    def list(self, name: str, values: list[int]) -> None:
        """A list of numbers."""
        self.lines.append(f"list {name} {' '.join(map(str, values))}")

    def text(self, name: str, words: str) -> None:
        """A label."""
        self.lines.append(f"text {name} {words}")

    def blob(self, name: str, data: bytes) -> None:
        """One image, in a file of its own."""
        file = f"b{len(self.lines):04d}.bin"
        (self.out / file).write_bytes(data)
        self.lines.append(f"blob {name} {file}")

    def payloads(self, name: str, payloads: dict[int, bytes]) -> None:
        """record id -> payload, as [id u16 LE][length u16 LE][payload] records."""
        file = f"p{len(self.lines):04d}.bin"
        (self.out / file).write_bytes(b"".join(struct.pack("<HH", rid, len(p)) + p
                                               for rid, p in sorted(payloads.items())))
        self.lines.append(f"payloads {name} {file}")

    def close(self) -> None:
        """Write manifest.txt."""
        (self.out / "manifest.txt").write_text("\n".join(self.lines) + "\n")


def facts(w: Writer, b: Bench) -> None:
    """What every test reads about the shape, and the NAME block's ends under
    layout 3 as the reference reads them from nvm_layout3.h."""
    rids = sorted(b.frames)
    names = sorted(rid for g, _i, rid, _p, _b in _rows(b) if g == "NAME")
    w.list("rids", rids)
    w.list("plens", [len(b.frames[r]) - REC_HDR for r in rids])
    w.list("binding_ids", binding_ids(b))
    w.list("d3_ids", sorted(set(rids) - set(binding_ids(b))))
    w.num("img_len", len(b.assemble(b.frames, 0)))
    w.num("max_plen", max(len(fr) for fr in b.frames.values()) - REC_HDR)
    w.num("rec_hdr", REC_HDR)
    w.num("clock_hz", b.clock_hz)
    w.num("n_names", len(names))
    w.list("name_ids", names[:1] + names[-1:])
    w.num("name_block_first", LAYOUT.block("NAME").base)
    w.num("name_block_last", LAYOUT.block("NAME").last)
    w.num("id_space", LAYOUT.id_space)
    # the flash map as the SoC source holds it (FLASHBOOT_RESERVED), not as the
    # store's macros derive it: today's two slots and the store's own
    w.num("legacy_a", LEGACY["offset"])
    w.num("legacy_b", LEGACY["offset"] + LEGACY_SLOT)
    w.num("journal_a", JOURNAL["offset"])
    w.num("journal_b", JOURNAL["offset"] + SLOT)
    w.num("erase_block", literal("FLASH_ERASE_BLOCK"))


def resealed_frame(frame: bytes) -> bytes:
    """A delta frame with its trailer computed again over its bytes."""
    return frame[:-4] + struct.pack("<I", zlib.crc32(frame[:-4]) & 0xFFFF_FFFF)


def with_frames_after(base: bytes, frames: list[bytes]) -> bytes:
    """A slot's bytes: the container, erased bytes to its first frame's page, each frame on its own page."""
    out = bytearray(base) + bytes([0xFF]) * (delta_base(len(base)) - len(base))
    for frame in frames:
        out += frame + bytes([0xFF]) * ((-len(frame)) % PAGE)
    return bytes(out)


def delta_fixture(w: Writer, b: Bench) -> None:
    """#1009's delta frames: those the store must write for the binding saves of DELTA_SAVES and a console commit
    of nothing, the slots they leave, a slot whose frames fill its room, and the frames a boot must refuse or end
    its walk at, each named by what it plants."""
    rb = binding_ids(b)[0]
    expect = b.expect
    w.num("bind_rid", rb)
    base = image(b, "golden@5/minor1")
    w.num("delta_base", delta_base(len(base)))
    w.num("delta_end", delta_end(len(base)))
    kld = {}
    for seed, seq, prev in DELTA_SAVES:
        kld[seq] = klj3_delta(image(b, f"bind{seed}@{seq:x}/minor1"), [rb], expect, prev)
        w.blob(f"kld/bind{seed}@{seq}", kld[seq])
        w.blob(f"bind{seed}@{seq:x}/minor1", image(b, f"bind{seed}@{seq:x}/minor1"))
    w.blob("kld/empty@7", klj3_delta(image(b, "golden@7/minor1"), [], expect, 5))
    w.blob("golden@5/minor1", base)
    w.blob("golden@7/minor1", image(b, "golden@7/minor1"))
    w.blob("slot/g5+b7", with_frames_after(base, [kld[7]]))
    w.blob("slot/g6+b8", with_frames_after(image(b, "golden@6/minor1"), [kld[8]]))
    w.blob("slot/g5+b7+b9", with_frames_after(base, [kld[7], kld[9]]))
    # a chain that leaves less than two pages of room: empty frames, sequences two apart, each on its page
    chain, seq = [], 5
    while delta_base(len(base)) + PAGE * (len(chain) + 2) <= delta_end(len(base)):
        chain.append(klj3_delta(image(b, f"golden@{seq + 2:x}/minor1"), [], expect, seq))
        seq += 2
    w.blob("slot/g5+full", with_frames_after(base, chain))
    w.num("full_seq", seq)
    w.num("full_frames", len(chain))
    w.blob("slot/g5+e9", with_frames_after(base, [klj3_delta(image(b, "golden@9/minor1"), [], expect, 5)]))
    w.blob("slot/g5+b9", with_frames_after(base, [klj3_delta(image(b, "bind9@9/minor1"), [rb], expect, 5)]))
    # every record erased: a record still erased in the stage goes in no frame
    w.blob("erased@5/minor1", image(b, "erased@5/minor1"))
    w.blob("erased@6/minor1", image(b, "erased@6/minor1"))
    w.blob("kld/erased@7", klj3_delta(image(b, "erased@7/minor1"), [rb], expect, 5))
    d7 = kld[7]
    torn = bytearray(d7)
    torn[DHDR + 12] ^= 0x01
    w.blob("slot/g5+torn", with_frames_after(base, [bytes(torn)]))
    torn9 = bytearray(kld[9])
    torn9[DHDR + 12] ^= 0x01
    w.blob("slot/g5+b7+torn", with_frames_after(base, [d7, bytes(torn9)]))
    # a frame after another sequence; its result's trailer wrong; a span past the record area; a span inside the
    # container's header
    planted = {"prev4": (12, 4), "badcrc": (24, 0x0BAD_C0DE), "long": (20, delta_end(len(base))), "lowoff": (16, 8)}
    for name, (at, v) in planted.items():
        f = bytearray(d7)
        struct.pack_into("<I", f, at, v)
        w.blob(f"slot/g5+{name}", with_frames_after(base, [resealed_frame(bytes(f))]))
    # a frame whose CRC closes over a result whose binding record's crc16 does not
    bad = bytearray(image(b, "bind7@7/minor1"))
    at = record_places(expect)[rb][0]
    bad[at + REC_HDR3] ^= 0x01
    struct.pack_into("<I", bad, len(bad) - 4, zlib.crc32(bytes(bad[:-4])) & 0xFFFF_FFFF)
    w.blob("slot/g5+badrec", with_frames_after(base, [klj3_delta(bytes(bad), [rb], expect, 5)]))
    # a frame whose sequence is not newer; a span starting past the record area; another kind of frame
    for name, (at, v) in {"older": (8, 4), "highoff": (16, len(base)), "magic": (0, 0x33444C4C)}.items():
        f = bytearray(d7)
        struct.pack_into("<I", f, at, v)
        w.blob(f"slot/g5+{name}", with_frames_after(base, [resealed_frame(bytes(f))]))
    # frames filling the room to its last byte; and a frame longer than the room its page leaves
    brim, seq = [], 5
    while delta_base(len(base)) + PAGE * (len(brim) + 1) <= delta_end(len(base)):
        brim.append(klj3_delta(image(b, f"golden@{seq + 2:x}/minor1"), [], expect, seq))
        seq += 2
    w.blob("slot/g5+brim", with_frames_after(base, brim))
    w.num("brim_seq", seq)
    kept = brim[:-2]
    prev = 5 + 2 * len(kept)
    big = struct.pack("<7I", KLD3_MAGIC, KLD3_VER, prev + 2, prev, HDR, 600, 0) + base[HDR:HDR + 600]
    big += bytes((-len(big)) % 4)
    big += struct.pack("<I", zlib.crc32(big) & 0xFFFF_FFFF)
    w.blob("slot/g5+bigroom", with_frames_after(base, kept + [big]))
    w.num("bigroom_seq", prev)
    w.blob("golden@40/minor1", image(b, "golden@40/minor1"))
    w.num("bind_rid2", binding_ids(b)[1])
    # an erased header over a frame's span that is not erased: the blank check's to find
    stray = bytearray(with_frames_after(base, [])) + bytes([0xFF]) * PAGE
    stray[delta_base(len(base)) + 40] = 0x5A
    w.blob("slot/g5+stray", bytes(stray))


def write_fixture(b: Bench, out: Path) -> Path:
    """The fixture of test_nvm_boot.cpp and test_nvm_write.cpp for one shape."""
    w = Writer(out)
    facts(w, b)
    delta_fixture(w, b)
    for name in main_images():
        w.blob(name, image(b, name))
    cases = parity(b)
    for n, (label, blob) in enumerate(cases):
        w.blob(f"parity/{n}", blob)
        w.text(f"parity_label/{n}", label)
    w.list("parity_verdicts", [verdict(b, blob) for _l, blob in cases])
    codec = codec_cases(b)
    for n, (label, blob, _staged) in enumerate(codec):
        w.blob(f"codec/{n}", blob)
        w.text(f"codec_label/{n}", label)
    w.list("codec_verdicts", [verdict(b, blob) for _l, blob, _s in codec])
    w.list("codec_staged", [int(staged) for _l, _b, staged in codec])
    w.blob("long", long_container(b))
    w.num("long_verdict", verdict(b, long_container(b)))
    w.blob("long_crc", codec[7][1])
    w.num("long_crc_verdict", verdict(b, codec[7][1]))
    for name in PAYLOAD_SETS + ("changed5c_firsts",):
        w.payloads(name, payload_set(b, name))
    # today's journal: the shipping writer's KLJ2 container, refused VD_VER
    # wherever the store meets it (#823 decision 2)
    w.blob("klj2@5", klj2_container(b, 5))
    w.num("klj2_verdict", verdict(b, klj2_container(b, 5)))
    w.close()
    return out


def write_capacity_fixture(b: Bench, out: Path) -> Path:
    """The fixture of test_nvm_capacity.cpp: the shape built with the layout 3
    NAME block full, so its last name is the block's last id; its committed
    container, and the same container with one record past the block."""
    w = Writer(out)
    facts(w, b)
    golden = image(b, "golden@1/minor1")
    w.blob("golden@1/minor1", golden)
    w.blob("golden@3/minor1", image(b, "golden@3/minor1"))
    w.payloads("golden", rid_payloads(b, golden))
    last = max(b.frames)
    past = dict(b.frames)
    past[last + 1] = frame_record3(last + 1, bytes(64))
    w.blob("one_past@1", b.assemble(past, 1))
    w.num("one_past_verdict", verdict(b, b.assemble(past, 1)))
    w.close()
    return out


def write_vector_fixture(vb: Bench, out: Path) -> Path:
    """The fixture of test_nvm_vector.cpp: the vector bench's images and the
    recorded vector's record set in layout 3. tb/verilator/nvm_backend records
    the all-fabric RTL's KLJ2 container of the shape, and this store writes
    KLJ3 (#823), so the test holds the store to the same records with the same
    payload lengths: each recorded layout 2 id is read as its group and index
    (the donor's allocation) and given its layout 3 id. The offsets and the
    CRC-32 are the reference's KLJ3 container's."""
    tab = table(vb.stem)
    if tab is None:
        raise ValueError(f"{vb.stem}: tb/verilator/nvm_backend records no vector")
    w = Writer(out)
    facts(w, vb)
    w.blob("erased@6", image(vb, "erased@6"))
    want = image(vb, "frames@7/minor1")
    w.blob("frames@7/minor1", want)
    w.payloads("frames", rid_payloads(vb, want))
    head, rows = tab["head"], tab["rows"]
    base = binding_base()
    plen3 = {rid_of_key3(key_of_id(rid, base)): rows[rid][2] for rid in rows}
    ids = sorted(plen3)
    offs = vb.offsets()
    w.num("vector_imglen", len(want))
    w.num("vector_nrec", int(head["nrec"]))
    w.num("vector_crc32", zlib.crc32(want[:-4]) & 0xFFFF_FFFF)
    w.list("vector_rows_rid", ids)
    w.list("vector_rows_off", [offs.get(r, -1) for r in ids])
    w.list("vector_rows_flen", [REC_HDR + plen3[r] for r in ids])
    w.list("vector_rows_plen", [plen3[r] for r in ids])
    w.close()
    return out
