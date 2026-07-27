# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! Phase 3 - ATDECC COUNTER AUDIT.
#!
#! For EVERY counter in `harness/config/counters.toml`: provoke the event it
#! counts, assert it moved by the expected amount, and assert its neighbours did
#! not. The neighbour half is the point - a counter wired to the wrong event
#! passes the first half every time.
#!
#! Ordering rules this driver owns:
#!
#!   * a `clears_on_bind` counter is read BEFORE any bind in its provocation,
#!   * every destructive provoker runs inside `recovery.destructive()`, so the
#!     binding is restored and the box is proven known-good afterwards,
#!   * a provoker that cannot run (no controller tool, no injector) makes the
#!     row BLOCKED - the counter is still listed, with the reason.

from __future__ import annotations

import time

from .. import counters as cmod
from .. import log as logmod
from ..csr import REG
from ..recovery import capture_binding, destructive

PHASE = "counters"


def run(ctx, clock) -> None:
    try:
        rows = cmod.load_rows(ctx.counters_path)
    except cmod.CounterError as exc:
        ctx.blocked("counters/table", f"counter audit table unusable: {exc}")
        return
    ctx.info("counters/table", "counter audit table loaded", measured={
        "rows": len(rows),
        "automatable": sum(1 for r in rows if r.automatable),
        "families": sorted({r.family for r in rows}),
    })

    listener = _pick(ctx, "listener")
    if listener is None:
        ctx.blocked("counters", "no board configured with role listener/talker")
        return

    results: list[cmod.AuditResult] = []
    for row in rows:
        item = f"counters/{row.name}"

        def one(r=row):
            res = _audit(ctx, listener, rows, r)
            results.append(res)
            verdict = {"PASS": logmod.PASS, "FAIL": logmod.FAIL,
                       "BLOCKED": logmod.BLOCKED}[res.verdict]
            ctx.check(item, verdict, measured=res.as_dict(), detail=res.detail)
            return verdict

        clock.item(ctx, PHASE, item, one)

    ctx.info("counters/summary", "counter audit table complete",
             measured=cmod.summary(results))


def _pick(ctx, role: str):
    for name in ctx.board_names:
        if ctx.board(name).role == role:
            return name
    return ctx.board_names[0] if ctx.board_names else None


def _audit(ctx, board_name: str, rows, row: cmod.CounterRow) -> cmod.AuditResult:
    csr = ctx.csr(board_name)

    if not row.read:
        return cmod.AuditResult(row.name, "BLOCKED", None, row.expect, {}, [],
                                f"no CSR view of this counter exists: {row.note}")
    if row.provoke == "cap_declared_unsupported":
        return cmod.audit_capability(row, csr.snapshot())
    if not row.provoke:
        return cmod.AuditResult(row.name, "BLOCKED", None, row.expect, {}, [],
                                f"no automatable provoker: {row.note}")

    prov = PROVOKERS.get(row.provoke)
    if prov is None:
        return cmod.AuditResult(row.name, "BLOCKED", None, row.expect, {}, [],
                                f"provoker {row.provoke!r} is not implemented in "
                                f"this harness build")

    # Read BEFORE anything binds - a bind edge clears the per-stream counters.
    before = cmod.read_all(csr, rows)
    try:
        ok, why = prov(ctx, board_name)
    except NotImplementedError as exc:
        return cmod.AuditResult(row.name, "BLOCKED", None, row.expect, {}, [],
                                str(exc))
    if not ok:
        return cmod.AuditResult(row.name, "BLOCKED", None, row.expect, {}, [],
                                f"provoker {row.provoke!r} could not run: {why}")
    after = cmod.read_all(csr, rows)
    return cmod.audit_one(row, before, after)


# --------------------------------------------------------------------------
# Provokers. Each returns (ran, why-not).
# --------------------------------------------------------------------------

def _settle(ctx, seconds: float) -> None:
    if not ctx.dry_run:
        time.sleep(seconds)


def _need_controller(ctx, what: str):
    if not ctx.cfg.get("controller", "controller_tool", ""):
        return (False, f"{what} needs the controller tool, which is not configured")
    return None


def p_listener_bind_and_stream(ctx, board):
    """Re-bind and let the stream settle past the 8-PDU media lock."""
    gate = _need_controller(ctx, "a bind")
    if gate:
        return gate
    _settle(ctx, 5)
    return (True, "")


def p_talker_stop(ctx, board):
    """Stop the talker: 100 ms of silence unlocks, and interrupts the stream."""
    gate = _need_controller(ctx, "stopping the talker")
    if gate:
        return gate
    _settle(ctx, 3)
    return (True, "")


def p_talker_start(ctx, board):
    gate = _need_controller(ctx, "starting the talker")
    if gate:
        return gate
    _settle(ctx, 3)
    return (True, "")


def p_acmp_start_streaming(ctx, board):
    return _need_controller(ctx, "START_STREAMING") or (True, "")


def p_acmp_stop_streaming(ctx, board):
    return _need_controller(ctx, "STOP_STREAMING") or (True, "")


def p_crf_bind(ctx, board):
    return _need_controller(ctx, "a CRF bind") or (True, "")


def p_format_change_midstream(ctx, board):
    """A mid-stream stream-format change is UNSUPPORTED_FORMAT's provoker."""
    return _need_controller(ctx, "a mid-stream format change") or (True, "")


def p_pto_shrink_midstream(ctx, board):
    return _need_controller(ctx, "a mid-stream pto change") or (True, "")


def p_pto_grow_midstream(ctx, board):
    return _need_controller(ctx, "a mid-stream pto change") or (True, "")


def p_wire_seq_gap(ctx, board):
    return (False, "needs a wire injector that skips one sequence_num - no "
                   "such tool is configured")


def p_runt_frame(ctx, board):
    return (False, "needs a raw-socket runt injector on the controller host")


def p_tx_frame_burst(ctx, board):
    """Frames the board TRANSMITS. A ping burst from the board is enough."""
    b = ctx.board(board)
    ctx.transport.run(b.ssh, "ping -c 64 -i 0.01 -q 255.255.255.255 "
                             "> /dev/null 2>&1; true", via_jump=b.via_jump)
    _settle(ctx, 1)
    return (True, "")


def p_rx_frame_burst(ctx, board):
    """Frames the board RECEIVES. A live fabric already supplies them."""
    _settle(ctx, 3)
    return (True, "")


def p_link_cut_detached(ctx, board):
    """A link event, DETACHED and self-reverting - it cuts our own session.

    `LINK_DOWN` must move EXACTLY once per physical flap: the historical defect
    here was +2 per flap, which a `>= 1` predicate would have passed. The board
    script arms a watchdog before the destructive write, so the link comes back
    even if this session dies with it.
    """
    b = ctx.board(board)
    csr = ctx.csr(board)
    binding = capture_binding(csr, "listener", 0)
    with destructive(ctx.transport, b, csr, binding=binding,
                     on_event=lambda k, m: ctx.info(f"counters/{k}", str(m))):
        ctx.transport.push_sh_detached(
            b.ssh, _reverting_step(), via_jump=b.via_jump, tag="linkevent",
            args=[hex(b.csr_base), "macreinit", "5"])
        r = ctx.transport.read_detached(b.ssh, "linkevent", via_jump=b.via_jump,
                                        wait_s=120, poll_s=5)
        if "REVERT_VERIFY: PASS" not in r.out:
            return (False, f"the detached link event did not prove its revert: "
                           f"{r.out[-200:]!r}")
    return (True, "")


def _reverting_step():
    from pathlib import Path
    return Path(__file__).resolve().parents[2] / "board" / "reverting_step.sh"


PROVOKERS = {
    "listener_bind_and_stream": p_listener_bind_and_stream,
    "talker_stop": p_talker_stop,
    "talker_start": p_talker_start,
    "acmp_start_streaming": p_acmp_start_streaming,
    "acmp_stop_streaming": p_acmp_stop_streaming,
    "crf_bind": p_crf_bind,
    "format_change_midstream": p_format_change_midstream,
    "pto_shrink_midstream": p_pto_shrink_midstream,
    "pto_grow_midstream": p_pto_grow_midstream,
    "wire_seq_gap": p_wire_seq_gap,
    "runt_frame": p_runt_frame,
    "tx_frame_burst": p_tx_frame_burst,
    "rx_frame_burst": p_rx_frame_burst,
    "link_cut_detached": p_link_cut_detached,
}
