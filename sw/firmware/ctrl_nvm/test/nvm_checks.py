# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""nvm_checks.py - the named checks of the saved-state store's host suite.

Each check is one function of a `Bench` and a flash port ("" for the host
flash model, "--litespi" for the on-chip LiteSPI implementation over the
command-master model) and returns its findings. Every verdict is taken here,
against scripts/nvm_klj2.py (the reference encoder and decoder), the recorded
vectors of tb/verilator/nvm_backend and the runner's counters, never against
the C store's own idea of the bytes. Every run is also held to the port
contract (`contract`), whatever the check is about.
"""

from __future__ import annotations

import struct
import sys
import zlib
from collections.abc import Callable
from pathlib import Path

from nvm_bench import JOURNAL, ROOT, SLOT, Bench, Run, default_payload, read_state

sys.path.insert(0, str(ROOT / "sw/firmware/nvm_hosttest"))

from nvm_contract import (KLJ2_HDR, REC_HDR, VD_BLANK, VD_CRC, VD_LEN, VD_OK,  # noqa: E402
                          VD_VER)
from nvm_klj2 import crc16_ccitt, frame_record, rid_of_key                      # noqa: E402
from nvm_shape import inventory                                                 # noqa: E402
import test_nvm_firmware as hosttest                                            # noqa: E402

T_COMPLETE, T_BLANK, T_DEFAULTS, T_CLOSED = 1, 2, 3, 4
C_APPLY, C_SETTLE, C_MODEL, C_STAGE = 1, 2, 3, 5
PAGE = 256
STEP_BYTES = 256
#: The longest one service call may hold the loop, in model time: the link
#: time of one 256-byte read-back or page program and its command bytes, the
#: command master's CSR accesses at 40 ns each, and one stalled wait given up
#: (README, "The service bound"). CPU work costs no model time.
CALL_BOUND_US = 1000
TABLE_DIR = ROOT / "tb/verilator/nvm_backend"
LITESPI = "--litespi"
SLOT_A = JOURNAL["offset"]
SLOT_B = SLOT_A + SLOT


def contract(b: Bench, r: Run, allow: tuple[str, ...] = ()) -> list[str]:
    """The port contract every run keeps: the journal only, never the
    authoritative slot, no program across a page or while busy, pages in
    ascending order, the step bound, the state port's order, one call's
    latency, and on the LiteSPI port a write enable before every PP and SE."""
    s = r.s
    zero = ["outside", "protected", "pagewrap", "while_busy", "descending", "sm_order", "bad",
            "ls_no_wel", "ls_short", "ls_refused", "ls_unknown", "ls_hung"]
    found = [f"invariant {k}={s.get(k)}" for k in zero if k not in allow and s.get(k) != 0]
    if s.get("step_max", 0) > s.get("step_bound", 0):
        found.append(f"invariant step_max={s.get('step_max')} > step_bound={s.get('step_bound')}")
    if s.get("max_call_us", 0) > CALL_BOUND_US:
        found.append(f"invariant max_call_us={s.get('max_call_us')} > {CALL_BOUND_US}")
    found += [f"runner {x}" for x in r.fails]
    return found


def go(b: Bench, port: str, found: list[str], *args: str, allow: tuple[str, ...] = ()) -> Run:
    """Run `args` on `port`, adding any contract finding to `found`."""
    r = b.run(*((port,) if port else ()), *args)
    found += contract(b, r, allow)
    return r


def expect(found: list[str], ok: bool, what: str) -> None:
    """Record `what` unless `ok`."""
    if not ok:
        found.append(what)


def rid_payloads(b: Bench, blob: bytes) -> dict[int, bytes]:
    """record id -> payload of every FRAMED record klj2_decode applies."""
    vd, applied = b.decode(blob)
    if vd != VD_OK:
        return {}
    return {rid_of_key(k, b.donor.base): v for k, v in applied.items()}


def state_matches(b: Bench, path: Path, saved: dict[int, bytes]) -> list[str]:
    """The state model holds exactly `saved` (valid) and the image default
    (not valid) for every other record of the shape."""
    state = read_state(path)
    bad = []
    for rid, fr in b.frames.items():
        plen = len(fr) - REC_HDR
        want = (1, saved[rid]) if rid in saved else (0, default_payload(rid, plen))
        if state.get(rid) != want:
            bad.append(rid)
    return [f"state of records {[hex(x) for x in bad[:6]]} ({len(bad)} in all) "
            f"differs from the slot"] if bad else []


def reseal(blob: bytes) -> bytes:
    """Recompute the CRC-32 trailer after an edit above it."""
    return blob[:-4] + struct.pack("<I", zlib.crc32(blob[:-4]) & 0xFFFF_FFFF)


def binding_ids(b: Bench) -> list[int]:
    """The record ids of the binding walk (D3 section 8.1 step 4)."""
    return sorted(rid for g, _i, rid, _p, _b in _inventory(b) if g == "BINDING")


def d3_ids(b: Bench) -> list[int]:
    """The record ids of the D3 walk: every other record."""
    return sorted(set(b.frames) - set(binding_ids(b)))


def stage_seq(b: Bench, name: str) -> int:
    """The sequence word of a dumped stage."""
    return struct.unpack_from("<I", (b.work / name).read_bytes(), 8)[0]


def changed_frames(b: Bench, seed: int) -> tuple[dict[int, bytes], dict[int, bytes]]:
    """The first record of every group with a new payload: (frames, payloads)."""
    firsts, seen = {}, set()
    for g, i, rid, plen, _b in sorted(_inventory(b), key=lambda t: t[2]):
        if g not in seen:
            seen.add(g)
            firsts[rid] = bytes((rid * 29 + j * 5 + seed) & 0xFF for j in range(plen))
    frames = dict(b.frames)
    frames.update({rid: frame_record(rid, p, b.donor.layout) for rid, p in firsts.items()})
    return frames, firsts


def _inventory(b: Bench) -> list[tuple]:
    """The shape's inventory rows with an id."""
    return [row for row in inventory(b.shape, b.donor.base) if row[2] is not None]


def set_args(payloads: dict[int, bytes]) -> list[str]:
    """--set words for every record in `payloads`."""
    out = []
    for rid, p in payloads.items():
        out += ["--set", f"{rid}:{p.hex()}"]
    return out


def pages(b: Bench) -> int:
    """Page programs one commit of this shape issues."""
    return -(-len(b.assemble(b.frames, 0)) // PAGE)


# ---- the boot path --------------------------------------------------------

def check_blank_boot(b: Bench, port: str) -> list[str]:
    """A blank board boots BLANK, releases AECP once, applies nothing, and
    stages the all-erased container the Python encoder writes."""
    f: list[str] = []
    r = go(b, port, f, "--blank", "--boot", "--dump-stage", "stage.bin")
    s = r.s
    expect(f, s["terminal"] == T_BLANK and s["vd_a"] == VD_BLANK and s["vd_b"] == VD_BLANK
           and s["releases"] == 1 and s["sm_releases"] == 1 and s["sm_applies"] == 0
           and s["auth"] == -1 and s["phase"] == 1, f"blank boot state: {s}")
    staged = (b.work / "stage.bin").read_bytes()
    expect(f, staged == b.assemble(b.erased_frames(), 0),
           "the staged blank container differs from nvm_klj2.py's")
    return f


def check_golden_restore(b: Bench, port: str) -> list[str]:
    """A golden slot is chosen, every record is applied in the D3 order (the
    settle step once, between the maps and the names) and the state equals
    what klj2_decode reads out of the same bytes."""
    f: list[str] = []
    golden = b.assemble(b.frames, 5)
    r = go(b, port, f, "--slot-b", b.file("g.bin", golden), "--boot", "--dump-state", "st.txt")
    s = r.s
    expect(f, s["terminal"] == T_COMPLETE and s["auth"] == 1 and s["seq"] == 5
           and s["vd_a"] == VD_BLANK and s["vd_b"] == VD_OK and s["applied"] == len(b.frames)
           and s["refused"] == 0 and s["blank"] == 0 and s["sm_settles"] == 1
           and s["releases"] == 1, f"golden restore state: {s}")
    f += state_matches(b, b.work / "st.txt", rid_payloads(b, golden))
    return f


def check_erased_records(b: Bench, port: str) -> list[str]:
    """An erased record applies nothing and keeps its image default; the
    framed ones beside it are applied (section 6.1, the erased-record rule)."""
    f: list[str] = []
    erased = b.erased_frames()
    half = {rid: (erased[rid] if n % 2 == 0 else fr)
            for n, (rid, fr) in enumerate(sorted(b.frames.items()))}
    img = b.assemble(half, 3)
    r = go(b, port, f, "--slot-a", b.file("h.bin", img), "--boot", "--dump-state", "st.txt")
    n_erased = (len(b.frames) + 1) // 2
    expect(f, r.s["terminal"] == T_COMPLETE and r.s["blank"] == n_erased
           and r.s["applied"] == len(b.frames) - n_erased, f"erased-record counts: {r.s}")
    f += state_matches(b, b.work / "st.txt", rid_payloads(b, img))
    return f


def check_newer_wins(b: Bench, port: str) -> list[str]:
    """The newer accepted slot wins, by the wrap-safe compare of section 7,
    and its records are the ones applied; on equal sequences slot A wins, as
    in the shipping writer (milan_baremetal.c nvm_pick_slot)."""
    f: list[str] = []
    frames, _ = changed_frames(b, 0x2B)
    for seq_a, seq_b, want in ((9, 10, 1), (10, 9, 0), (0xFFFF_FFFF, 0, 1), (0, 0xFFFF_FFFF, 0),
                               (7, 7, 0)):
        imgs = (b.assemble(b.frames, seq_a), b.assemble(frames, seq_b))
        r = go(b, port, f, "--slot-a", b.file("a.bin", imgs[0]),
               "--slot-b", b.file("b.bin", imgs[1]), "--boot", "--dump-state", "st.txt")
        expect(f, r.s["auth"] == want and r.s["terminal"] == T_COMPLETE,
               f"seq A {seq_a:#x} B {seq_b:#x}: chose {r.s['auth']}, want {want}")
        f += state_matches(b, b.work / "st.txt", rid_payloads(b, imgs[want]))
    return f


def _torn(blob: bytes, at: int) -> bytes:
    """`blob` with one bit flipped at `at`, its trailer left as it was."""
    return blob[:at] + bytes([blob[at] ^ 0x80]) + blob[at + 1:]


def check_torn_falls_back(b: Bench, port: str) -> list[str]:
    """A torn newer slot falls back to the older one, whose records apply."""
    f: list[str] = []
    older = b.assemble(b.frames, 9)
    newer = _torn(b.assemble(b.frames, 10), KLJ2_HDR + 3)
    r = go(b, port, f, "--slot-a", b.file("a.bin", older), "--slot-b", b.file("b.bin", newer),
           "--boot", "--dump-state", "st.txt")
    expect(f, r.s["auth"] == 0 and r.s["seq"] == 9 and r.s["vd_b"] == VD_CRC
           and r.s["terminal"] == T_COMPLETE, f"torn newer slot: {r.s}")
    f += state_matches(b, b.work / "st.txt", rid_payloads(b, older))
    return f


def check_both_torn_blank(b: Bench, port: str) -> list[str]:
    """Two torn slots boot on the defaults, naming the failure."""
    f: list[str] = []
    a = _torn(b.assemble(b.frames, 9), KLJ2_HDR + 9)
    bb = _torn(b.assemble(b.frames, 10), KLJ2_HDR + 3)
    r = go(b, port, f, "--slot-a", b.file("a.bin", a), "--slot-b", b.file("b.bin", bb),
           "--boot", "--dump-state", "st.txt")
    expect(f, r.s["terminal"] == T_BLANK and r.s["last"] == VD_CRC and r.s["sm_applies"] == 0
           and r.s["releases"] == 1, f"two torn slots: {r.s}")
    f += state_matches(b, b.work / "st.txt", {})
    return f


def parity_extra(b: Bench) -> list[tuple[str, bytes]]:
    """Refusals the shipping suite's table does not carry: a framed record
    whose length runs past the record area, an extra record past the shape's
    last, and a container longer than the stage whose CRC closes."""
    full = b.assemble(b.frames, 3)
    last = max(b.frames)
    off = KLJ2_HDR + b.offsets()[last]
    fr = b.frames[last]
    hdr = fr[:4] + struct.pack(">H", 0x4000)
    over = full[:off] + hdr + struct.pack(">H", crc16_ccitt(hdr + fr[REC_HDR:])) + full[off + 8:]
    extra = dict(b.frames)
    extra[0xFF] = frame_record(0xFF, b"\x01\x02\x03\x04", b.donor.layout)
    body = full[KLJ2_HDR:-4] + bytes(100)
    head = full[:16] + struct.pack("<I", KLJ2_HDR + len(body) + 4) + full[20:KLJ2_HDR]
    return [("framed record overruns the area", reseal(over)),
            ("one record past the shape's last", b.assemble(extra, 3)),
            ("longer than the stage, CRC closing", reseal(head + body + bytes(4)))]


def check_verdict_parity(b: Bench, port: str) -> list[str]:
    """For every section 6.2 refusal, both faces of the erased-record rule and
    a blank slot, the store's verdict equals klj2_decode's for the same bytes
    (the shipping writer suite's table, plus parity_extra)."""
    f: list[str] = []
    cases = hosttest.parity_cases(b) + parity_extra(b)
    for n, (label, blob) in enumerate(cases):
        want = b.decode(blob)[0] if len(blob) <= SLOT else VD_LEN
        r = go(b, port, f, "--slot-a", b.file(f"p{n}.bin", blob), "--boot")
        expect(f, r.s["vd_a"] == want, f"parity: {label}: store {r.s['vd_a']}, klj2_decode {want}")
    return f


def check_wrong_version_falls_back(b: Bench, port: str) -> list[str]:
    """A newer slot of another major version is refused VD_VER, never
    reinterpreted, and the older slot is offered."""
    f: list[str] = []
    older = b.assemble(b.frames, 3)
    for major in (1, 3):
        newer = b.assemble(b.frames, 4)
        newer = reseal(newer[:4] + struct.pack("<I", major << 16) + newer[8:])
        r = go(b, port, f, "--slot-a", b.file("a.bin", older), "--slot-b", b.file("b.bin", newer),
               "--boot")
        expect(f, r.s["vd_b"] == VD_VER and r.s["auth"] == 0 and r.s["seq"] == 3,
               f"major {major}: {r.s}")
    return f


def check_read_flip_at_stage(b: Bench, port: str) -> list[str]:
    """The chosen slot is read again and judged again in RAM: a bit the read
    flips after the slot was judged is never applied; the other slot is."""
    f: list[str] = []
    older = b.assemble(b.frames, 3)
    frames, _ = changed_frames(b, 0x41)
    newer = b.assemble(frames, 4)
    # two reads judge each slot (the header, then the container); the fifth
    # read re-stages slot B
    r = go(b, port, f, "--slot-a", b.file("a.bin", older), "--slot-b", b.file("b.bin", newer),
           "--boot-fault", "read-flip:1:4", "--boot", "--dump-state", "st.txt")
    expect(f, r.s["cause"] == C_STAGE and r.s["auth"] == 0 and r.s["seq"] == 3
           and r.s["vd_b"] == VD_LEN and r.s["terminal"] == T_COMPLETE, f"flipped re-stage: {r.s}")
    f += state_matches(b, b.work / "st.txt", rid_payloads(b, older))
    return f


def _two_slots(b: Bench, seq_a: int, seq_b: int) -> tuple[bytes, bytes]:
    """Slot A holds the golden records at seq_a, slot B others at seq_b, so
    which slot was applied shows in every group."""
    frames, _ = changed_frames(b, 0x37)
    return b.assemble(b.frames, seq_a), b.assemble(frames, seq_b)


def _consistent(b: Bench, f: list[str], r: Run, imgs: tuple[bytes, bytes], seqs: tuple[int, int],
                what: str) -> None:
    """The slot the store names is the one applied, under the sequence it
    holds: published SEQ = staged SEQ = that slot's own, and the state is its
    records."""
    auth = r.s["auth"]
    expect(f, r.s["terminal"] == T_COMPLETE and auth in (0, 1), f"{what}: {r.s}")
    if auth not in (0, 1):
        return
    expect(f, r.s["seq"] == seqs[auth] == stage_seq(b, "stage.bin"),
           f"{what}: slot {auth} holds seq {seqs[auth]:#x}, published {r.s['seq']:#x}, "
           f"staged {stage_seq(b, 'stage.bin'):#x}")
    f += [f"{what}: {x}" for x in state_matches(b, b.work / "st.txt", rid_payloads(b, imgs[auth]))]


def check_read_flip_boot(b: Bench, port: str) -> list[str]:
    """A bit a boot read flips in a slot's sequence word (bit 3 of byte 8:
    5 reads as 13) never selects a slot on that word: on every
    read that covers it, of either slot, across the wrap, the store applies
    one slot's own records under that slot's own sequence, and a flip in the
    OLDER slot never displaces the newer one."""
    f: list[str] = []
    for seq_a, seq_b in ((5, 6), (6, 5), (0xFFFF_FFFF, 0), (0, 0xFFFF_FFFF)):
        imgs = _two_slots(b, seq_a, seq_b)
        newer = 0 if ((seq_a - seq_b) & 0xFFFF_FFFF) < 0x8000_0000 else 1
        for slot, base in ((0, SLOT_A), (1, SLOT_B)):
            for k in range(3):
                what = f"seq A {seq_a:#x} B {seq_b:#x}, flip in slot {slot} read {k}"
                r = go(b, port, f, "--slot-a", b.file("a.bin", imgs[0]),
                       "--slot-b", b.file("b.bin", imgs[1]),
                       "--boot-fault", f"read-flip-at:1:{k}:{base + 8:#x}", "--boot",
                       "--dump-stage", "stage.bin", "--dump-state", "st.txt")
                _consistent(b, f, r, imgs, (seq_a, seq_b), what)
                expect(f, slot == newer or r.s["auth"] == newer,
                       f"{what}: the older slot's flipped word displaced the newer: {r.s}")
    return f


def check_read_alias_at_stage(b: Bench, port: str) -> list[str]:
    """The re-stage read of the chosen slot answering from the other slot (an
    address line stuck) is caught by its sequence: the bytes are valid but
    not the chosen slot's, so the other slot is offered and applied under its
    own sequence."""
    f: list[str] = []
    imgs = _two_slots(b, 6, 5)
    # reads 0-3 judge the two slots; read 4 re-stages slot A
    r = go(b, port, f, "--slot-a", b.file("a.bin", imgs[0]), "--slot-b", b.file("b.bin", imgs[1]),
           "--boot-fault", "read-alias:1:4", "--boot", "--dump-stage", "stage.bin",
           "--dump-state", "st.txt")
    _consistent(b, f, r, imgs, (6, 5), "aliased re-stage")
    expect(f, r.s["auth"] == 1 and r.s["cause"] == C_STAGE and r.s["vd_a"] == VD_LEN,
           f"aliased re-stage: {r.s}")
    return f


def check_read_fail_boot(b: Bench, port: str) -> list[str]:
    """A slot whose read fails is refused VD_LEN (rule 4), the newer one
    included, and the older is applied; a re-stage read that fails offers
    the other slot."""
    f: list[str] = []
    imgs = _two_slots(b, 5, 6)
    for skip, cause in ((3, 0), (4, C_STAGE)):
        r = go(b, port, f, "--slot-a", b.file("a.bin", imgs[0]),
               "--slot-b", b.file("b.bin", imgs[1]), "--boot-fault", f"read-fail:1:{skip}",
               "--boot", "--dump-stage", "stage.bin", "--dump-state", "st.txt")
        _consistent(b, f, r, imgs, (5, 6), f"read {skip} failed")
        expect(f, r.s["auth"] == 0 and r.s["vd_b"] == VD_LEN and r.s["cause"] == cause,
               f"read {skip} failed: {r.s}")
    return f


def _golden_boot(b: Bench, port: str, f: list[str], *knobs: str) -> Run:
    """Boot a golden slot B under the state-model knobs given."""
    return go(b, port, f, "--slot-b", b.file("g.bin", b.assemble(b.frames, 5)), *knobs,
              "--boot", "--dump-state", "st.txt")


def _bindings_saved(b: Bench) -> dict[int, bytes]:
    """The golden slot's bindings: what a D3 roll-back leaves applied."""
    saved = rid_payloads(b, b.assemble(b.frames, 5))
    return {rid: saved[rid] for rid in binding_ids(b)}


def check_apply_fault_rolls_back(b: Bench, port: str) -> list[str]:
    """A value rule that cannot be judged aborts the D3 walk and rolls every
    D3 value back to its image default: DEFAULTS, AECP released. The binding
    walk ran first and its bindings stay applied (D3 section 8.6)."""
    f: list[str] = []
    rid = d3_ids(b)[len(d3_ids(b)) // 2]
    r = _golden_boot(b, port, f, "--apply-fault", str(rid))
    expect(f, r.s["terminal"] == T_DEFAULTS and r.s["cause"] == C_APPLY
           and r.s["sm_rollbacks"] == 1 and r.s["sm_unbinds"] == 0
           and r.s["bind_terminal"] == T_COMPLETE and r.s["releases"] == 1
           and r.s["phase"] == 1, f"apply fault: {r.s}")
    f += state_matches(b, b.work / "st.txt", _bindings_saved(b))
    return f


def check_settle_fault_rolls_back(b: Bench, port: str) -> list[str]:
    """A formats-against-maps judgement that cannot be made rolls the D3
    walk back too, and leaves the bindings applied."""
    f: list[str] = []
    r = _golden_boot(b, port, f, "--settle-fault")
    expect(f, r.s["terminal"] == T_DEFAULTS and r.s["cause"] == C_SETTLE
           and r.s["sm_rollbacks"] == 1 and r.s["sm_unbinds"] == 0
           and r.s["releases"] == 1, f"settle fault: {r.s}")
    f += state_matches(b, b.work / "st.txt", _bindings_saved(b))
    return f


def check_binding_walk(b: Bench, port: str) -> list[str]:
    """The binding walk is its own unit (D3 section 8.1 step 4, 8.6): a
    binding whose rule cannot be judged fails that walk whole, nothing
    preloaded, and the D3 walk still restores every other record; a walk
    whose preloads cannot be dropped ends CLOSED. The state model polices
    that every binding precedes the D3 walk."""
    f: list[str] = []
    golden = b.assemble(b.frames, 5)
    saved = rid_payloads(b, golden)
    last = binding_ids(b)[-1]
    r = _golden_boot(b, port, f, "--apply-fault", str(last))
    expect(f, r.s["bind_terminal"] == T_DEFAULTS and r.s["bind_cause"] == C_APPLY
           and r.s["sm_unbinds"] == 1 and r.s["terminal"] == T_COMPLETE
           and r.s["sm_rollbacks"] == 0 and r.s["releases"] == 1, f"binding fault: {r.s}")
    f += state_matches(b, b.work / "st.txt",
                       {rid: p for rid, p in saved.items() if rid not in binding_ids(b)})
    r = _golden_boot(b, port, f, "--apply-fault", str(last), "--unbind-fault")
    expect(f, r.s["bind_terminal"] == T_CLOSED and r.s["terminal"] == T_CLOSED
           and r.s["releases"] == 0 and r.s["phase"] == 0, f"binding undo fault: {r.s}")
    return f


def check_rollback_fault_closes(b: Bench, port: str) -> list[str]:
    """A roll-back that fails ends CLOSED: AECP is never released and the
    writer never runs, so a later change reaches no slot."""
    f: list[str] = []
    rid = max(b.frames)
    plen = len(b.frames[rid]) - REC_HDR
    r = go(b, port, f, "--slot-b", b.file("g.bin", b.assemble(b.frames, 5)),
           "--apply-fault", str(d3_ids(b)[2]), "--rollback-fault", "--boot",
           "--set", f"{rid}:{bytes(plen).hex()}", "--run-ms", "3000")
    expect(f, r.s["terminal"] == T_CLOSED and r.s["releases"] == 0 and r.s["sm_releases"] == 0
           and r.s["phase"] == 0 and r.s["erases"] == 0, f"rollback fault: {r.s}")
    return f


def check_model_unproven_closes(b: Bench, port: str) -> list[str]:
    """No entity model to judge against: CLOSED, nothing applied, AECP held."""
    f: list[str] = []
    r = _golden_boot(b, port, f, "--not-ready")
    expect(f, r.s["terminal"] == T_CLOSED and r.s["cause"] == C_MODEL and r.s["releases"] == 0
           and r.s["sm_applies"] == 0 and r.s["phase"] == 0, f"unproven model: {r.s}")
    return f


def check_refused_keeps_default(b: Bench, port: str) -> list[str]:
    """A value its rule refuses keeps its image default and the walk goes on
    to apply every later record (section 8.3)."""
    f: list[str] = []
    rids = sorted(b.frames)
    refuse = [rids[1], rids[len(rids) // 2]]
    golden = b.assemble(b.frames, 5)
    r = go(b, port, f, "--slot-b", b.file("g.bin", golden), "--refuse", str(refuse[0]),
           "--refuse", str(refuse[1]), "--boot", "--dump-state", "st.txt")
    expect(f, r.s["terminal"] == T_COMPLETE and r.s["refused"] == 2
           and r.s["applied"] == len(rids) - 2, f"refusals: {r.s}")
    saved = {k: v for k, v in rid_payloads(b, golden).items() if k not in refuse}
    f += state_matches(b, b.work / "st.txt", saved)
    return f


BOOT_CHECKS: dict[str, Callable[[Bench, str], list[str]]] = {
    "blank_boot": check_blank_boot,
    "golden_restore": check_golden_restore,
    "erased_records": check_erased_records,
    "newer_wins": check_newer_wins,
    "torn_falls_back": check_torn_falls_back,
    "both_torn_blank": check_both_torn_blank,
    "verdict_parity": check_verdict_parity,
    "wrong_version_falls_back": check_wrong_version_falls_back,
    "read_flip_at_stage": check_read_flip_at_stage,
    "read_flip_boot": check_read_flip_boot,
    "read_alias_at_stage": check_read_alias_at_stage,
    "read_fail_boot": check_read_fail_boot,
    "apply_fault_rolls_back": check_apply_fault_rolls_back,
    "settle_fault_rolls_back": check_settle_fault_rolls_back,
    "binding_walk": check_binding_walk,
    "rollback_fault_closes": check_rollback_fault_closes,
    "model_unproven_closes": check_model_unproven_closes,
    "refused_keeps_default": check_refused_keeps_default,
}

#: The checks whose subject is the media face run on both ports; the rest
#: read through the port only to boot, and the LiteSPI port reads through the
#: memory map, where the flash model's read faults do not reach.
BOTH = ("", LITESPI)
DIRECT = ("",)
READ_FAULTS = ("read_flip_at_stage", "read_flip_boot", "read_alias_at_stage", "read_fail_boot")
BOOT_PORTS = {name: (DIRECT if name in READ_FAULTS else BOTH) for name in BOOT_CHECKS}
