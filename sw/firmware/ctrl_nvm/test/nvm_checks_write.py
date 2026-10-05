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

from nvm_bench import SLOT, Bench, Run
from nvm_checks import (BOTH, CALL_BOUND_US, DIRECT, LITESPI, LS_CALL_US, NOMINAL_CALL_US,
                        P_HELD, P_IDLE, READ_TRIES, SLOT_A, SLOT_B, STEP_BYTES, T_COMPLETE,
                        TABLE_DIR, changed_frames, expect, go, pages, reseal, rid_payloads,
                        set_args, state_matches)
from nvm_contract import (KLJ2_HDR, REC_HDR, VD_ERASE, VD_LEN, VD_OK, VD_PROGRAM, VD_SHAPE,
                          VD_VERIFY)

T_BLANK = 2
#: The write path's phases (nvm_store.h enum nvm_phase).
P_CAPTURE, P_SEAL, P_ERASE, P_ERASE_WAIT, P_PROGRAM, P_PROGRAM_WAIT = 2, 3, 4, 5, 7, 8
#: The port's no-progress bound on one wait (plat/nvm_flash_litespi.c
#: LS_POLL_MAX), and a drain's one extra read.
POLL_MAX = 4096
MS = 1000


def _slot(b: Bench, name: str) -> bytes:
    """A dumped slot."""
    return (b.work / name).read_bytes()


def _padded(blob: bytes) -> bytes:
    """`blob` as a slot holds it: the rest of the erase block erased."""
    return blob + b"\xff" * (SLOT - len(blob))


def _value(b: Bench, rid: int, seed: int) -> bytes:
    """A payload for record rid that no golden frame carries."""
    plen = len(b.frames[rid]) - REC_HDR
    return bytes((rid * 13 + j * 11 + seed) & 0xFF for j in range(plen))


def _one_change(b: Bench, seed: int) -> tuple[int, bytes]:
    """The last record of the shape with a new payload."""
    rid = max(b.frames)
    return rid, _value(b, rid, seed)


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


def _after_mark(r: Run, k: int) -> int | None:
    """The k-th erase's start, in us after the run's last mark."""
    return r.erases[k] - r.marks[-1] if len(r.erases) > k and r.marks else None


def _in(value: int | None, lo: int, hi: int) -> bool:
    """lo <= value <= hi, and a value at all."""
    return value is not None and lo <= value <= hi


def check_debounce(b: Bench, port: str) -> list[str]:
    """DR2a: a change commits after the 1,000 ms first-dirty window and not
    before, and a second change inside the window does not extend it. A
    change the running capture takes leaves no window behind it, so the next
    change gets its own full window: a change to the last record, and one to
    the very record the capture examines next; a change the capture has
    passed opens one of its own."""
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
    first = min(b.frames)
    # the capture has latched nothing yet: it takes a change to the last
    # record, and one to the first, the record it examines next
    for taken in (rid, first):
        r = go(b, port, f, "--slot-b", g, "--boot", "--set-pattern", "1",
               "--until-phase", str(P_CAPTURE), "--set", f"{taken}:{_value(b, taken, 1).hex()}",
               "--until-idle", "--run-ms", "5000", "--mark",
               "--set", f"{taken}:{_value(b, taken, 2).hex()}", "--until-idle")
        expect(f, r.s["ok"] == 2 and _in(_after_mark(r, 1), 1000 * MS, 1050 * MS),
               f"a change after a commit that took one mid-capture (record {taken:#x}): erase "
               f"{_after_mark(r, 1)} us after it, want 1,000 to 1,050 ms: {r.s}")
    # the capture is over: a change now waits for a window of its own
    r = go(b, port, f, "--slot-b", g, "--boot", "--set", f"{rid}:{new.hex()}",
           "--until-phase", str(P_SEAL), "--mark", "--set", f"{first}:{_value(b, first, 9).hex()}",
           "--until-idle")
    expect(f, r.s["ok"] == 2 and _in(_after_mark(r, 1), 1000 * MS, 1050 * MS),
           f"a change after the capture: erase {_after_mark(r, 1)} us after it, "
           f"want 1,000 to 1,050 ms: {r.s}")
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
    keeps the change in flight, marks the claim stale, retries at most three
    times 1,000 ms apart and then stops, recording the abandoned set; the
    authoritative slot is untouched."""
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
               and s["dirty"] == 0 and s["pending"] == 1 and s["ok"] == 0
               and s["abandoned"] == 1 and s["abandoned_vd"] == verdict, f"{mode}: {s}")
        expect(f, _slot(b, "b.bin") == _padded(golden), f"{mode}: the authoritative slot changed")
        if not hang:
            gaps = [y - x for x, y in zip(r.erases, r.erases[1:])]
            expect(f, len(r.erases) == 3 and all(g >= 1_000_000 for g in gaps),
                   f"{mode}: attempts at {r.erases} us, want three at least 1,000 ms apart")
    return f


def check_recovers_after_failure(b: Bench, port: str) -> list[str]:
    """A third attempt that succeeds clears the stale claim; after exhaustion,
    a changed value is a new work set and commits once the media answers. The
    stale claim heals (FASTCONNECT section 9.2), also when the change left
    after the recovering commit set the value it already had and DR2b writes
    nothing; the record of the abandoned set does not heal."""
    f: list[str] = []
    g = b.file("g.bin", b.assemble(b.frames, 5))
    rid, new = _one_change(b, 5)
    r = go(b, port, f, "--slot-b", g, "--boot", "--fault", "erase-stuck:2",
           "--set", f"{rid}:{new.hex()}", "--until-idle")
    gaps = [y - x for x, y in zip(r.erases, r.erases[1:])]
    expect(f, r.s["ok"] == 1 and r.s["failed"] == 2 and r.s["stale"] == 0
           and r.s["last"] == VD_OK and r.s["first"] == VD_OK and r.s["attempts"] == 0
           and len(r.erases) == 3 and all(g >= 1_000_000 for g in gaps), f"third attempt: {r.s}")
    # the first attempt fails; the same value is set again while the retry
    # writes, so the retry's commit leaves it dirty and DR2b suppresses it
    r = go(b, port, f, "--slot-b", g, "--boot", "--fault", "program-drop:1",
           "--set", f"{rid}:{new.hex()}", "--until-phase", str(P_ERASE_WAIT),
           "--until-phase", str(P_IDLE), "--until-phase", str(P_ERASE_WAIT),
           "--set", f"{rid}:{new.hex()}", "--until-idle")
    expect(f, r.s["ok"] == 1 and r.s["failed"] == 1 and r.s["skipped"] == 1 and r.s["stale"] == 0
           and r.s["dirty"] == 0 and r.s["pending"] == 0, f"a repeated value after recovery: {r.s}")
    _rid, new2 = _one_change(b, 6)
    r = go(b, port, f, "--slot-b", g, "--boot", "--fault", "program-drop:99999",
           "--set", f"{rid}:{new.hex()}", "--run-ms", "15000", "--fault", "none:0",
           "--set", f"{rid}:{new2.hex()}", "--until-idle", "--dump-slot-a", "a.bin")
    expect(f, r.s["ok"] == 1 and r.s["failed"] == 3 and r.s["exhausted"] == 0
           and r.s["stale"] == 0 and r.s["abandoned"] == 1 and r.s["abandoned_vd"] == VD_VERIFY,
           f"new work set after exhaustion: {r.s}")
    expect(f, rid_payloads(b, _slot(b, "a.bin")[:len(b.assemble(b.frames, 0))]).get(rid) == new2,
           "the new work set is not in the slot")
    return f


def check_dr2c_unchanged_set(b: Bench, port: str) -> list[str]:
    """DR2c: an unchanged captured work set gets three attempts in all. A
    change call that leaves the value as it was, made every 5 s for 60 s,
    buys no fourth, and neither does the medium healing; a value that really
    changes is a new set, commits, and leaves the abandoned set's record."""
    f: list[str] = []
    g = b.file("g.bin", b.assemble(b.frames, 5))
    rid, new = _one_change(b, 21)
    touches = [w for _ in range(12) for w in ("--touch", str(rid), "--run-ms", "5000")]
    r = go(b, port, f, "--slot-b", g, "--boot", "--protect-auth", "--fault", "program-drop:99999",
           "--set", f"{rid}:{new.hex()}", "--run-ms", "5000", *touches, "--fault", "none:0",
           "--touch", str(rid), "--run-ms", "3000")
    s = r.s
    expect(f, s["failed"] == 3 and s["erases"] == 3 and s["ok"] == 0 and s["exhausted"] == 1
           and s["withheld"] == 13 and s["abandoned"] == 1, f"unchanged set held: {s}")
    newer = _value(b, rid, 22)
    r = go(b, port, f, "--slot-b", g, "--boot", "--fault", "program-drop:99999",
           "--set", f"{rid}:{new.hex()}", "--run-ms", "5000", "--fault", "none:0",
           "--set", f"{rid}:{newer.hex()}", "--until-idle", "--dump-slot-a", "a.bin")
    s = r.s
    expect(f, s["ok"] == 1 and s["failed"] == 3 and s["erases"] == 4 and s["stale"] == 0
           and s["abandoned"] == 1 and s["abandoned_vd"] == VD_VERIFY,
           f"a changed set after exhaustion: {s}")
    expect(f, rid_payloads(b, _slot(b, "a.bin")[:len(b.assemble(b.frames, 0))]).get(rid) == newer,
           "the changed set is not in the slot")
    return f


def check_dr2c_console(b: Bench, port: str) -> list[str]:
    """DR2c binds the console too: a commit asked for inside a failed
    attempt's backoff is refused and the retry still waits 1,000 ms; asked
    for after the set is exhausted, it writes nothing while the set is
    unchanged, and a changed set commits."""
    f: list[str] = []
    g = b.file("g.bin", b.assemble(b.frames, 5))
    rid, new = _one_change(b, 23)
    r = go(b, port, f, "--slot-b", g, "--boot", "--fault", "program-drop:1",
           "--set", f"{rid}:{new.hex()}", "--until-phase", str(P_PROGRAM_WAIT), "--run-ms", "200",
           "--commit-try", "--run-ms", "300", "--commit-try", "--until-idle")
    gap = r.erases[1] - r.fail_at[0] if len(r.erases) > 1 and r.fail_at else None
    expect(f, r.s["commit_tries"] == 2 and r.s["commit_refused"] == 2 and r.s["failed"] == 1
           and r.s["ok"] == 1 and _in(gap, 1000 * MS, 1050 * MS),
           f"console inside the backoff: retry {gap} us after the failure: {r.s}")
    tries = [w for _ in range(5) for w in ("--commit-try", "--run-ms", "1500")]
    newer = _value(b, rid, 24)
    r = go(b, port, f, "--slot-b", g, "--boot", "--protect-auth", "--fault", "program-drop:99999",
           "--set", f"{rid}:{new.hex()}", "--run-ms", "5000", *tries, "--fault", "none:0",
           "--commit-try", "--run-ms", "1500", "--set", f"{rid}:{newer.hex()}", "--commit-try",
           "--until-idle")
    s = r.s
    expect(f, s["commit_tries"] == 7 and s["commit_refused"] == 0 and s["withheld"] == 6
           and s["failed"] == 3 and s["ok"] == 1 and s["erases"] == 4 and s["abandoned"] == 1,
           f"console after exhaustion: {s}")
    return f


def _fails_then_recovers(b: Bench, port: str, f: list[str], fault: str, verdict: int,
                         seed: int) -> None:
    """With `fault` armed after boot, the first attempt fails with `verdict`
    and nothing commits before the backoff ends; run on, the retry commits
    the change into the other slot and the authority was never touched."""
    g = b.file("g.bin", b.assemble(b.frames, 5))
    rid, new = _one_change(b, seed)
    head = ["--slot-b", g, "--boot", "--protect-auth", "--fault", fault, "--set", f"{rid}:{new.hex()}"]
    r = go(b, port, f, *head, "--run-ms", "1500")
    expect(f, r.s["failed"] == 1 and r.s["first"] == verdict and r.s["ok"] == 0,
           f"{fault}: want the first failure {verdict}: {r.s}")
    r = go(b, port, f, *head, "--until-idle", "--dump-slot-a", "a.bin")
    expect(f, r.s["failed"] == 1 and r.s["ok"] == 1 and r.s["auth"] == 0 and r.s["seq"] == 6,
           f"{fault}: no recovery: {r.s}")
    expect(f, rid_payloads(b, _slot(b, "a.bin")[:len(b.assemble(b.frames, 0))]).get(rid) == new,
           f"{fault}: the retried change is not in the slot")


def check_verify_tail(b: Bench, port: str) -> list[str]:
    """The read-back covers the whole container to the trailer: a dropped
    LAST page fails the attempt VD_VERIFY, the authority stays, and the retry
    commits."""
    f: list[str] = []
    _fails_then_recovers(b, port, f, f"program-drop:1:{pages(b) - 1}", VD_VERIFY, 25)
    return f


def check_blankcheck_tail(b: Bench, port: str) -> list[str]:
    """The blank check covers the whole container span to its last byte: an
    erase that leaves the last byte programmed fails VD_ERASE before any page
    is programmed, and the retry commits."""
    f: list[str] = []
    last = len(b.assemble(b.frames, 0)) - 1
    _fails_then_recovers(b, port, f, f"erase-stuck:1:0:{last}", VD_ERASE, 26)
    return f


def check_media_verdicts(b: Bench, port: str) -> list[str]:
    """Each failure is named by the step that met it, not a later one: a
    read that fails in the blank check is VD_ERASE and in the read-back
    VD_VERIFY, never passed over; a program or erase the port refuses is
    VD_PROGRAM or VD_ERASE. Each attempt is retried and the retry commits."""
    f: list[str] = []
    n = pages(b)
    for fault, verdict in ((f"read-fail:1:{n // 2}", VD_ERASE),
                           (f"read-fail:1:{n + n // 2}", VD_VERIFY),
                           ("program-refuse:1:2", VD_PROGRAM), ("erase-refuse:1", VD_ERASE)):
        _fails_then_recovers(b, port, f, fault, verdict, 27)
    return f


def check_time_base(b: Bench, port: str) -> list[str]:
    """The windows and deadlines run on the port's local counter, never the
    PHC: a gPTP step of 60 s either way in the debounce window, the backoff,
    an erase and a program changes no elapsed time, and the counter's wrap
    (2^32 clocks, 42.9 s) does not either. Every time is graded on the
    model's own clock, which no step moves."""
    f: list[str] = []
    g = b.file("g.bin", b.assemble(b.frames, 5))
    rid, new = _one_change(b, 28)
    change = ["--slot-b", g, "--boot", "--set", f"{rid}:{new.hex()}"]
    hang = ("while_busy", "ls_refused")
    for step in ("-60000", "60000"):
        r = go(b, port, f, "--slot-b", g, "--boot", "--mark", "--set", f"{rid}:{new.hex()}",
               "--run-ms", "500", "--phc-step", step, "--run-ms", "1000")
        expect(f, _in(_after_mark(r, 0), 1000 * MS, 1050 * MS),
               f"PHC {step} ms in the window: erase {_after_mark(r, 0)} us after the change")
        r = go(b, port, f, *change, "--fault", "program-drop:1", "--run-ms", "1200",
               "--phc-step", step, "--run-ms", "2000")
        gap = r.erases[1] - r.fail_at[0] if len(r.erases) > 1 and r.fail_at else None
        expect(f, _in(gap, 1000 * MS, 1050 * MS),
               f"PHC {step} ms in the backoff: retry {gap} us after the failure")
        r = go(b, port, f, *change, "--fault", "erase-hang:1", "--run-ms", "1500",
               "--phc-step", step, "--run-ms", "5000", allow=hang)
        took = r.fail_at[0] - r.erases[0] if r.fail_at and r.erases else None
        expect(f, _in(took, 3500 * MS, 3510 * MS),
               f"PHC {step} ms in an erase: timed out {took} us after it, want 3,500 ms")
        r = go(b, port, f, *change, "--fault", "program-hang:1", "--until-phase",
               str(P_PROGRAM_WAIT), "--mark", "--run-ms", "20", "--phc-step", step,
               "--run-ms", "200", allow=hang)
        took = r.fail_at[0] - r.marks[0] if r.fail_at and r.marks else None
        expect(f, _in(took, 49 * MS, 51 * MS),
               f"PHC {step} ms in a program: timed out {took} us after it, want 50 ms")
    r = go(b, port, f, "--slot-b", g, "--boot", "--run-ms", "42500", "--mark",
           "--set", f"{rid}:{new.hex()}", "--run-ms", "1500")
    expect(f, _in(_after_mark(r, 0), 1000 * MS, 1050 * MS),
           f"a window across the counter's wrap: erase {_after_mark(r, 0)} us after the change")
    return f


def check_port_stall(b: Bench, port: str) -> list[str]:
    """Every wait on the command master is bounded: two waits of one page
    program slowed by 4,000 status reads each (TX, RX or a drain) still
    complete; a master that stops answering in one wait (TX, RX, or a
    receive side that never drains) fails the call within LS_POLL_MAX reads,
    chip select released, so the step returns, the attempt fails under the
    step's verdict, the authority is untouched and the retry commits; a
    master that never answers exhausts the set while the loop keeps
    running. The case that slows every wait is port_deadline's."""
    f: list[str] = []
    golden = b.assemble(b.frames, 5)
    g = b.file("g.bin", golden)
    rid, new = _one_change(b, 29)
    head = ["--slot-b", g, "--boot", "--protect-auth", "--set", f"{rid}:{new.hex()}"]
    cut = ("ls_short", "while_busy", "ls_refused")
    for stall in ("tx:2:0:4000", "rx:2:0:4000", "drain:2:0:4000"):
        r = go(b, port, f, *head, "--until-phase", str(P_PROGRAM), "--ls-stall", stall,
               "--until-idle")
        expect(f, r.s["failed"] == 0 and r.s["ok"] == 1 and r.s["ls_stalled"] == 2
               and r.s["ls_max_withheld"] == 4000, f"slow master {stall}: {r.s}")
    for phase, stall, verdict in ((P_PROGRAM, "tx:1:10:0", VD_PROGRAM),
                                  (P_PROGRAM, "rx:1:200:0", VD_PROGRAM),
                                  (P_PROGRAM, "drain:1:0:0", VD_PROGRAM),
                                  (P_ERASE, "tx:1:3:0", VD_ERASE),
                                  (P_ERASE_WAIT, "rx:1:0:0", VD_ERASE)):
        r = go(b, port, f, *head, "--until-phase", str(phase), "--ls-stall", stall,
               "--run-ms", "100", "--dump-slot-b", "b.bin", allow=cut)
        # the port gives up after LS_POLL_MAX reads; a drain reads once more
        expect(f, r.s["failed"] == 1 and r.s["first"] == verdict and r.s["ls_stalled"] == 1
               and r.s["ls_max_withheld"] == POLL_MAX + stall.startswith("drain"),
               f"stalled master {stall}: {r.s}")
        expect(f, _slot(b, "b.bin") == _padded(golden), f"{stall}: the authoritative slot changed")
        r = go(b, port, f, *head, "--until-phase", str(phase), "--ls-stall", stall,
               "--until-idle", allow=cut)
        expect(f, r.s["failed"] == 1 and r.s["ok"] == 1, f"{stall}: no recovery: {r.s}")
    r = go(b, port, f, *head, "--until-phase", str(P_ERASE), "--ls-stall", "tx:99999:0:0",
           "--run-ms", "10000", "--dump-slot-b", "b.bin", allow=cut)
    expect(f, r.s["failed"] == 3 and r.s["exhausted"] == 1 and r.s["first"] == VD_ERASE
           and r.s["calls"] >= 90_000 and r.s["max_call_us"] <= CALL_BOUND_US,
           f"dead master: {r.s}")
    expect(f, _slot(b, "b.bin") == _padded(golden), "dead master: the authoritative slot changed")
    return f


def check_port_deadline(b: Bench, port: str) -> list[str]:
    """No call is still waiting on the master past the port's deadline,
    LS_CALL_US of timer0 time, even when the master keeps progressing inside
    every wait. Ten waits slowed by 4,000 status reads each (1.6 ms in one
    page program) and the call completes. Twelve, the slow part ending just
    before the deadline, and the call completes past it at the ready pace,
    within CALL_BOUND_US. Every wait slowed by 4,000 reads, none of them
    reaching LS_POLL_MAX, and each page program fails at the deadline: the
    attempt fails VD_PROGRAM, the authority is untouched, three attempts are
    spent and the loop keeps running; once the master is well, a changed
    value commits. Every call stays within CALL_BOUND_US of model time."""
    f: list[str] = []
    golden = b.assemble(b.frames, 5)
    g = b.file("g.bin", golden)
    rid, new = _one_change(b, 30)
    head = ["--slot-b", g, "--boot", "--protect-auth", "--set", f"{rid}:{new.hex()}",
            "--until-phase", str(P_PROGRAM)]
    r = go(b, port, f, *head, "--ls-stall", "tx:10:0:4000", "--until-idle")
    expect(f, r.s["ok"] == 1 and r.s["failed"] == 0 and r.s["ls_stalled"] == 10
           and 1600 <= r.s["max_call_us"] < LS_CALL_US, f"ten slowed waits: {r.s}")
    r = go(b, port, f, *head, "--ls-stall", "tx:12:0:4000", "--until-idle")
    expect(f, r.s["ok"] == 1 and r.s["failed"] == 0 and r.s["ls_stalled"] == 12
           and LS_CALL_US < r.s["max_call_us"] <= CALL_BOUND_US, f"twelve slowed waits: {r.s}")
    r = go(b, port, f, *head, "--ls-stall", "tx:999999:0:4000", "--run-ms", "10000",
           "--dump-slot-b", "b.bin", "--ls-stall", "none:0",
           "--set", f"{rid}:{_value(b, rid, 31).hex()}", "--until-idle", allow=("ls_short",))
    expect(f, r.s["failed"] == 3 and r.s["abandoned_vd"] == VD_PROGRAM and r.s["abandoned"] == 1
           and r.s["ok"] == 1 and r.s["ls_max_withheld"] == 4000
           and LS_CALL_US <= r.s["max_call_us"] <= CALL_BOUND_US and r.s["calls"] >= 50_000,
           f"every wait slowed: {r.s}")
    expect(f, _slot(b, "b.bin") == _padded(golden), "every wait slowed: the authority changed")
    return f


#: Sequences the generation restart meets differently: a tie with 1, an
#: ordinary one, the half-range point and the wrap.
AUTH_SEQS = (1, 5, 0x8000_0000, 0xFFFF_FFFF)


def _authority_case(b: Bench, port: str, f: list[str], x: int, seq: int,
                    case: tuple[str, bool]) -> None:
    """Slot x valid at seq, the other blank, the case's fault armed at boot
    (held: whether it must hold the writer); a change; then a clean reboot,
    a change, its commit and a clean reboot."""
    fault, held = case
    frames, _ = changed_frames(b, 0x60 + x)
    img = b.assemble(frames, seq)
    saved = rid_payloads(b, img)
    rid, new = _one_change(b, 32)
    _rid, new2 = _one_change(b, 33)
    what = f"slot {'AB'[x]} at {seq:#x}, {fault}"
    console = ["--run-ms", "3000", "--commit-try"] if held else []
    r = go(b, port, f, "--slot-a" if x == 0 else "--slot-b", b.file("x.bin", img),
           "--boot-fault", fault, "--boot", "--dump-state", "st0.txt", "--set", f"{rid}:{new.hex()}",
           "--until-idle", *console, "--dump-slot-a", "a1.bin", "--dump-slot-b", "b1.bin")
    s = r.s
    if held:
        expect(f, s["unread"] == 1 << x and s["phase"] == P_HELD and s["terminal"] == T_BLANK
               and s["vd_" + "ab"[x]] == VD_LEN and s["ok"] == 0 and s["erases"] == 0
               and s["programs"] == 0 and s["dirty"] == 1 and s["commit_refused"] == 1,
               f"{what}: the writer is not held: {s}")
    else:
        expect(f, s["unread"] == 0 and s["terminal"] == T_COMPLETE and s["ok"] == 1
               and s["auth"] == 1 - x and s["seq"] == (seq + 1) & 0xFFFF_FFFF,
               f"{what}: the slot was not read again and applied: {s}")
    f += [f"{what}: at boot: {e}" for e in state_matches(b, b.work / "st0.txt", {} if held else saved)]
    # whatever the store reported committed, a clean reboot restores
    durable = {**saved, **({rid: new} if s["ok"] else {})}
    want_seq = (seq + (1 if s["ok"] else 0)) & 0xFFFF_FFFF
    r = go(b, port, f, "--slot-a", str(b.work / "a1.bin"), "--slot-b", str(b.work / "b1.bin"),
           "--boot", "--dump-state", "st1.txt", "--set", f"{rid}:{new2.hex()}", "--until-idle",
           "--dump-slot-a", "a2.bin", "--dump-slot-b", "b2.bin")
    expect(f, r.s["seq"] == (want_seq + 1) & 0xFFFF_FFFF and r.s["ok"] == 1 and r.s["unread"] == 0,
           f"{what}: the change after a clean reboot: {r.s}")
    f += [f"{what}: clean reboot: {e}" for e in state_matches(b, b.work / "st1.txt", durable)]
    r = go(b, port, f, "--slot-a", str(b.work / "a2.bin"), "--slot-b", str(b.work / "b2.bin"),
           "--boot", "--dump-state", "st2.txt")
    expect(f, r.s["seq"] == (want_seq + 1) & 0xFFFF_FFFF and r.s["terminal"] == T_COMPLETE,
           f"{what}: the reboot after that commit: {r.s}")
    f += [f"{what}: last reboot: {e}"
          for e in state_matches(b, b.work / "st2.txt", {**durable, rid: new2})]


def check_authority_unknown(b: Bench, port: str) -> list[str]:
    """#665 decision 2: a slot refused by a media read fault leaves the
    authority unknown, so nothing is committed until reset. One slot valid
    and the other blank, both ways round, at sequence 1, 5, 0x80000000 and
    0xFFFFFFFF. The valid slot's reads failing NVM_READ_TRIES times: the
    boot is BLANK, the writer HELD, a change is reported dirty, nothing is
    erased or written and the console is refused; a clean reboot restores
    the slot. Two failed reads, one read flipping a bit unreported, or one
    read answering from the blank slot (so the valid one reads blank): the
    slot is read again and applied, and the change commits at the next
    sequence. Either way a later change commits and a clean reboot restores
    it with every other value, and nothing reported committed is lost on a
    clean reboot."""
    f: list[str] = []
    for x in (0, 1):
        # a blank slot stands on two header reads, a valid one on its header
        # and its container; slot A is judged first
        first = 0 if x == 0 else 2
        body = f"{(SLOT_A, SLOT_B)[x] + 0x100:#x}"
        for seq in AUTH_SEQS:
            for case in ((f"read-fail:{READ_TRIES}:{first}", True),
                         (f"read-fail:{READ_TRIES - 1}:{first}", False),
                         (f"read-flip-at:1:0:{body}", False),
                         (f"read-alias:1:{first}", False)):
                _authority_case(b, port, f, x, seq, case)
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
    NOMINAL_CALL_US of model time, and the loop keeps running through a 3 s
    erase (one status poll per call)."""
    f: list[str] = []
    r = go(b, port, f, "--slot-b", b.file("g.bin", b.assemble(b.frames, 5)), "--boot",
           "--times", "3000:1000", "--set-pattern", "1", "--until-idle")
    s = r.s
    maxplen = max(len(fr) for fr in b.frames.values()) - REC_HDR
    want = max(STEP_BYTES, 2 * maxplen + 6)
    expect(f, s["ok"] == 1 and s["step_max"] == want == s["step_bound"],
           f"step bytes {s['step_max']}, want {want} (bound {s['step_bound']})")
    expect(f, s["max_call_us"] <= NOMINAL_CALL_US and s["calls"] >= 3_000_000 // 100
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
    "dr2c_unchanged_set": check_dr2c_unchanged_set,
    "dr2c_console": check_dr2c_console,
    "verify_tail": check_verify_tail,
    "blankcheck_tail": check_blankcheck_tail,
    "media_verdicts": check_media_verdicts,
    "refused_slot_kept": check_refused_slot_kept,
    "service_bound": check_service_bound,
    "powercut": check_powercut,
    "vector_round_trip": check_vector_round_trip,
    "time_base": check_time_base,
    "port_stall": check_port_stall,
    "port_deadline": check_port_deadline,
    "port_guard": check_port_guard,
    "authority_unknown": check_authority_unknown,
}

#: The flash model's read and refusal faults reach the store through the
#: model's port only (LiteSPI reads are memory-mapped and its refusals are
#: the guard's); the PHC, timer0 and the command master exist on the LiteSPI
#: port only.
WRITE_PORTS = {name: BOTH for name in WRITE_CHECKS}
for _name in ("media_verdicts", "authority_unknown"):
    WRITE_PORTS[_name] = DIRECT
for _name in ("time_base", "port_stall", "port_deadline", "port_guard"):
    WRITE_PORTS[_name] = (LITESPI,)
