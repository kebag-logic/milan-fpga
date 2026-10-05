# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""nvm_checks_write.py - the write-path checks of the saved-state store's host suite.

The commit and its atomicity rules (docs/design/SAVED_STATE_FASTCONNECT.md
section 7; SAVED_STATE_MATERIALIZATION.md section 15.1 DR2a, DR2b, DR2c and
DR5), the power cut at every write step, the service bound, and the round
trip against the recorded vectors of tb/verilator/nvm_backend.
"""

from __future__ import annotations

import struct
import zlib
from collections.abc import Callable

from nvm_bench import SLOT, Bench
from nvm_checks import (BOTH, LITESPI, STEP_BYTES, TABLE_DIR, changed_frames, expect, go,
                        pages, reseal, rid_payloads, set_args, state_matches)
from nvm_contract import KLJ2_HDR, REC_HDR, VD_ERASE, VD_OK, VD_PROGRAM, VD_SHAPE, VD_VERIFY

T_BLANK = 2
CALL_BOUND_US = 1000


def _slot(b: Bench, name: str) -> bytes:
    """A dumped slot."""
    return (b.work / name).read_bytes()


def _padded(blob: bytes) -> bytes:
    """`blob` as a slot holds it: the rest of the erase block erased."""
    return blob + b"\xff" * (SLOT - len(blob))


def _one_change(b: Bench, seed: int) -> tuple[int, bytes]:
    """The last record of the shape with a new payload."""
    rid = max(b.frames)
    plen = len(b.frames[rid]) - REC_HDR
    return rid, bytes((rid * 13 + j * 11 + seed) & 0xFF for j in range(plen))


def check_first_commit_bytes(b: Bench, port: str) -> list[str]:
    """A console commit on a blank board writes slot A with the all-erased
    container at sequence 1, byte for byte as nvm_klj2.py writes it, in one
    erase and one program per page."""
    f: list[str] = []
    r = go(b, port, f, "--blank", "--boot", "--commit", "--dump-slot-a", "a.bin")
    s = r.s
    want = b.assemble(b.erased_frames(), 1)
    expect(f, s["ok"] == 1 and s["seq"] == 1 and s["auth"] == 0 and s["erases"] == 1
           and s["programs"] == pages(b), f"first commit: {s}")
    expect(f, _slot(b, "a.bin") == _padded(want), "the first container differs from nvm_klj2.py's")
    if port == LITESPI:
        expect(f, s["ls_se"] == 1 and s["ls_pp"] == pages(b)
               and s["ls_wren"] == s["ls_se"] + s["ls_pp"], f"LiteSPI command sequence: {s}")
    return f


def check_change_commit_bytes(b: Bench, port: str) -> list[str]:
    """A change to the first record of every group commits into the slot that
    is not authoritative, at the next sequence, byte for byte as nvm_klj2.py
    writes the same records; the authoritative slot is untouched; and a boot
    from the result applies exactly the changed values (the round trip)."""
    f: list[str] = []
    golden = b.assemble(b.frames, 5)
    frames, pay = changed_frames(b, 0x5C)
    r = go(b, port, f, "--slot-b", b.file("g.bin", golden), "--boot", "--protect-auth",
           *set_args(pay), "--until-idle", "--dump-slot-a", "a.bin", "--dump-slot-b", "b.bin")
    s = r.s
    want = b.assemble(frames, 6)
    expect(f, s["ok"] == 1 and s["seq"] == 6 and s["auth"] == 0 and s["stale"] == 0
           and s["dirty"] == 0 and s["pending"] == 0, f"change commit: {s}")
    expect(f, _slot(b, "a.bin") == _padded(want),
           "the committed container differs from nvm_klj2.py's for the same records")
    expect(f, _slot(b, "b.bin") == _padded(golden), "the authoritative slot changed")
    if port == LITESPI:
        expect(f, s["ls_se"] == 1 and s["ls_pp"] == pages(b), f"LiteSPI command sequence: {s}")
    r = go(b, port, f, "--slot-a", str(b.work / "a.bin"), "--slot-b", str(b.work / "b.bin"),
           "--boot", "--dump-state", "st.txt")
    expect(f, r.s["auth"] == 0 and r.s["seq"] == 6, f"boot after the commit: {r.s}")
    f += state_matches(b, b.work / "st.txt", rid_payloads(b, want))
    return f


def check_debounce(b: Bench, port: str) -> list[str]:
    """DR2a: a change commits after the 1,000 ms first-dirty window and not
    before, and a second change inside the window does not extend it."""
    f: list[str] = []
    g = b.file("g.bin", b.assemble(b.frames, 5))
    rid, new = _one_change(b, 1)
    _rid2, new2 = _one_change(b, 2)
    one = ["--slot-b", g, "--boot", "--set", f"{rid}:{new.hex()}"]
    r = go(b, port, f, *one, "--run-ms", "990")
    expect(f, r.s["erases"] == 0, f"an erase inside the debounce window: {r.s['erases']}")
    r = go(b, port, f, *one, "--run-ms", "990", "--run-ms", "60")
    expect(f, r.s["erases"] == 1, f"no erase 1,050 ms after the change: {r.s['erases']}")
    r = go(b, port, f, *one, "--run-ms", "500", "--set", f"{rid}:{new2.hex()}", "--run-ms", "560")
    expect(f, r.s["erases"] == 1, "a second change extended the first-dirty window")
    return f


def check_unchanged_no_erase(b: Bench, port: str) -> list[str]:
    """DR2b: a change that leaves every persisted value as the verified slot
    holds it erases nothing."""
    f: list[str] = []
    rid = max(b.frames)
    r = go(b, port, f, "--slot-b", b.file("g.bin", b.assemble(b.frames, 5)), "--boot",
           "--set", f"{rid}:{b.frames[rid][REC_HDR:].hex()}", "--until-idle")
    expect(f, r.s["erases"] == 0 and r.s["skipped"] == 1 and r.s["ok"] == 0
           and r.s["dirty"] == 0 and r.s["pending"] == 0, f"unchanged value: {r.s}")
    return f


def check_failed_commit_not_skipped(b: Bench, port: str) -> list[str]:
    """DR2b only suppresses what a VERIFIED slot holds: after a failed
    attempt, the retry writes the value again although the stage already
    carries it."""
    f: list[str] = []
    rid, new = _one_change(b, 3)
    r = go(b, port, f, "--slot-b", b.file("g.bin", b.assemble(b.frames, 5)), "--boot",
           "--fault", "program-drop:1", "--set", f"{rid}:{new.hex()}", "--until-idle",
           "--dump-slot-a", "a.bin")
    expect(f, r.s["failed"] == 1 and r.s["ok"] == 1 and r.s["last"] == VD_OK
           and r.s["skipped"] == 0, f"retry after a failed attempt: {r.s}")
    expect(f, rid_payloads(b, _slot(b, "a.bin")[:len(b.assemble(b.frames, 0))]).get(rid) == new,
           "the retried change is not in the slot")
    return f


FAILURES = (("erase-hang", VD_ERASE, True), ("erase-stuck", VD_ERASE, False),
            ("program-hang", VD_PROGRAM, True), ("program-drop", VD_VERIFY, False),
            ("program-flip", VD_VERIFY, False))


def check_media_failures(b: Bench, port: str) -> list[str]:
    """DR2c: an erase, program or read-back that fails names its verdict,
    returns the change to dirty, marks the claim stale, retries at most three
    times 1,000 ms apart and then stops; the authoritative slot is untouched."""
    f: list[str] = []
    golden = b.assemble(b.frames, 5)
    rid, new = _one_change(b, 4)
    for mode, verdict, hang in FAILURES:
        # a hung device stays busy: the attempts after the first are refused
        # at their erase, which the device and the command master both count
        r = go(b, port, f, "--slot-b", b.file("g.bin", golden), "--boot", "--protect-auth",
               "--fault", f"{mode}:99999", "--set", f"{rid}:{new.hex()}", "--run-ms", "20000",
               "--dump-slot-b", "b.bin", allow=("while_busy", "ls_refused") if hang else ())
        s = r.s
        expect(f, s["failed"] == 3 and s["exhausted"] == 1 and s["first"] == verdict
               and s["last"] == (VD_ERASE if hang else verdict) and s["stale"] == 1
               and s["dirty"] == 1 and s["pending"] == 0 and s["ok"] == 0, f"{mode}: {s}")
        expect(f, _slot(b, "b.bin") == _padded(golden), f"{mode}: the authoritative slot changed")
        if not hang:
            gaps = [y - x for x, y in zip(r.erases, r.erases[1:])]
            expect(f, len(r.erases) == 3 and all(g >= 1_000_000 for g in gaps),
                   f"{mode}: attempts at {r.erases} us, want three at least 1,000 ms apart")
    return f


def check_recovers_after_failure(b: Bench, port: str) -> list[str]:
    """A third attempt that succeeds clears the stale claim; after exhaustion,
    a new change is a new work set and commits once the media answers."""
    f: list[str] = []
    g = b.file("g.bin", b.assemble(b.frames, 5))
    rid, new = _one_change(b, 5)
    r = go(b, port, f, "--slot-b", g, "--boot", "--fault", "erase-stuck:2",
           "--set", f"{rid}:{new.hex()}", "--until-idle")
    gaps = [y - x for x, y in zip(r.erases, r.erases[1:])]
    expect(f, r.s["ok"] == 1 and r.s["failed"] == 2 and r.s["stale"] == 0
           and r.s["last"] == VD_OK and r.s["first"] == VD_OK and r.s["attempts"] == 0
           and len(r.erases) == 3 and all(g >= 1_000_000 for g in gaps), f"third attempt: {r.s}")
    _rid, new2 = _one_change(b, 6)
    r = go(b, port, f, "--slot-b", g, "--boot", "--fault", "program-drop:99999",
           "--set", f"{rid}:{new.hex()}", "--run-ms", "15000", "--fault", "none:0",
           "--set", f"{rid}:{new2.hex()}", "--until-idle", "--dump-slot-a", "a.bin")
    expect(f, r.s["ok"] == 1 and r.s["failed"] == 3 and r.s["exhausted"] == 0
           and r.s["stale"] == 0, f"new work set after exhaustion: {r.s}")
    expect(f, rid_payloads(b, _slot(b, "a.bin")[:len(b.assemble(b.frames, 0))]).get(rid) == new2,
           "the new work set is not in the slot")
    return f


def check_refused_slot_kept(b: Bench, port: str) -> list[str]:
    """DR5: with no slot accepted, a blank slot takes the first commit before
    a refused one, so a refused image is not erased merely for being refused."""
    f: list[str] = []
    golden = b.assemble(b.frames, 5)
    foreign = reseal(golden[:28] + struct.pack("<I", 0xDEAD_0002) + golden[32:])
    rid, new = _one_change(b, 7)
    r = go(b, port, f, "--slot-a", b.file("f.bin", foreign), "--boot",
           "--set", f"{rid}:{new.hex()}", "--until-idle", "--dump-slot-a", "a.bin",
           "--dump-slot-b", "b.bin")
    expect(f, r.s["terminal"] == T_BLANK and r.s["vd_a"] == VD_SHAPE and r.s["auth"] == 1
           and r.s["ok"] == 1, f"refused slot A: {r.s}")
    expect(f, _slot(b, "a.bin") == _padded(foreign), "the refused image was erased")
    expect(f, b.decode(_slot(b, "b.bin")[:len(golden)])[0] == VD_OK, "slot B does not decode")
    return f


def check_service_bound(b: Bench, port: str) -> list[str]:
    """Every service step is bounded and returns: no step touches more than
    one latched record or one 256-byte stretch, no call holds the loop past
    CALL_BOUND_US of link time, and the loop keeps running through a 3 s
    erase (one status poll per call)."""
    f: list[str] = []
    r = go(b, port, f, "--slot-b", b.file("g.bin", b.assemble(b.frames, 5)), "--boot",
           "--times", "3000:1000", "--set-pattern", "1", "--until-idle")
    s = r.s
    maxplen = max(len(fr) for fr in b.frames.values()) - REC_HDR
    want = max(STEP_BYTES, 2 * maxplen + 6)
    expect(f, s["ok"] == 1 and s["step_max"] == want == s["step_bound"],
           f"step bytes {s['step_max']}, want {want} (bound {s['step_bound']})")
    expect(f, s["max_call_us"] <= CALL_BOUND_US and s["calls"] >= 3_000_000 // 100
           and s["max_polls_call"] <= 3, f"the loop did not keep running: {s}")
    return f


def check_powercut(b: Bench, port: str) -> list[str]:
    """A power cut inside every media effect of a commit (the erase and every
    page program, at 0, 1/256, 1/2 and 255/256 of it) and during the
    read-back: the board boots the old values or the new ones exactly, never
    a mix, never touching the authoritative slot, and the next change
    commits. Three starting points: blank media, one slot, two slots."""
    f: list[str] = []
    older = b.file("o.bin", b.assemble(b.frames, 5))
    frames, _ = changed_frames(b, 0x21)
    newer = b.file("n.bin", b.assemble(frames, 6))
    effects = 1 + pages(b)
    for label, loads in (("blank media", ["--blank"]), ("one slot", ["--slot-a", older]),
                         ("two slots", ["--slot-a", older, "--slot-b", newer])):
        pc = go(b, port, f, *loads, "--powercut").powercut
        cases = 4 * effects + 1
        expect(f, pc.get("effects") == effects and pc.get("cases") == cases
               and pc.get("bad") == 0 and 1 <= pc.get("new", 0) <= 2
               and pc.get("old", 0) + pc.get("new", 0) == cases, f"power cut from {label}: {pc}")
    return f


def table_exists(stem: str) -> bool:
    """Whether tb/verilator/nvm_backend records a vector of this shape."""
    return (TABLE_DIR / f"records_{stem}.txt").exists()


def _table(stem: str) -> dict | None:
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


def _walk(blob: bytes) -> dict[int, tuple[int, int, int]]:
    """record id -> (area offset, framed length, payload length) of every frame."""
    out, pos = {}, KLJ2_HDR
    for _ in range(struct.unpack_from("<I", blob, 12)[0]):
        rid, plen = blob[pos + 3], struct.unpack_from(">H", blob, pos + 4)[0]
        out[rid] = (pos - KLJ2_HDR, REC_HDR + plen, plen)
        pos += REC_HDR + plen
    return out


def check_vector_round_trip(b: Bench, port: str) -> list[str]:
    """The round trip against the parent's recorded vector: the store, given
    the vector's records, commits the container tb/verilator/nvm_backend grades
    the RTL against (its length, CRC-32 and every record's offset), byte for
    byte as nvm_klj2.py assembles it, and boots it back to the same values."""
    vb = b.vector
    table = _table(b.stem)
    if vb is None or table is None:
        return []
    f: list[str] = []
    seed = vb.assemble(vb.erased_frames(), 6)
    r = go(vb, port, f, "--slot-a", vb.file("v6.bin", seed), "--boot", "--set-pattern", "0",
           "--commit", "--dump-slot-b", "v7.bin")
    want = vb.assemble(vb.frames, 7)
    got = _slot(vb, "v7.bin")[:len(want)]
    head = table["head"]
    expect(f, r.s["ok"] == 1 and r.s["seq"] == 7 and r.s["auth"] == 1, f"vector commit: {r.s}")
    expect(f, got == want, "the vector container differs from nvm_klj2.py's")
    expect(f, len(got) == int(head["imglen"]) and int(head["nrec"]) == len(table["rows"])
           and f"0x{zlib.crc32(got[:-4]) & 0xFFFF_FFFF:08X}" == head["crc32"],
           f"length or CRC-32 differs from the recorded vector {head}")
    expect(f, _walk(got) == table["rows"], "a record offset differs from the recorded vector")
    r = go(vb, port, f, "--slot-b", str(vb.work / "v7.bin"), "--boot", "--dump-state", "vst.txt")
    expect(f, r.s["applied"] == len(vb.frames), f"vector boot: {r.s}")
    f += state_matches(vb, vb.work / "vst.txt", rid_payloads(vb, want))
    return f


def check_port_guard(b: Bench, port: str) -> list[str]:
    """The LiteSPI port refuses to program or erase outside the journal."""
    f: list[str] = []
    r = go(b, port, f, "--port-guard")
    expect(f, r.guard == 0, f"the port took {r.guard} of 4 writes outside the journal")
    return f


WRITE_CHECKS: dict[str, Callable[[Bench, str], list[str]]] = {
    "first_commit_bytes": check_first_commit_bytes,
    "change_commit_bytes": check_change_commit_bytes,
    "debounce": check_debounce,
    "unchanged_no_erase": check_unchanged_no_erase,
    "failed_commit_not_skipped": check_failed_commit_not_skipped,
    "media_failures": check_media_failures,
    "recovers_after_failure": check_recovers_after_failure,
    "refused_slot_kept": check_refused_slot_kept,
    "service_bound": check_service_bound,
    "powercut": check_powercut,
    "vector_round_trip": check_vector_round_trip,
    "port_guard": check_port_guard,
}

WRITE_PORTS = {name: BOTH for name in WRITE_CHECKS}
WRITE_PORTS["port_guard"] = (LITESPI,)
