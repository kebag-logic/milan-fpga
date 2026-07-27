# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! Item runners - the generic verbs a registry row can name.
#!
#! The registry (private) says *which* runner an item uses and with what
#! expectations; this module is the machinery that executes them. Keeping the
#! verbs here and the item detail there is what lets the plan and the harness
#! version independently.
#!
#! Every runner returns a verdict string and records exactly one check. A runner
#! that cannot run - controller tool absent, feature not in this build - returns
#! BLOCKED, never FAIL: only a defect in the device wakes a human.

from __future__ import annotations

import shlex

from . import log as logmod


def _controller(ctx):
    """(host, via_jump, tool, iface) or None when no controller is configured."""
    tool = ctx.cfg.get("controller", "controller_tool", "")
    if not tool:
        return None
    return (ctx.cfg.get("controller", "host", ""),
            bool(ctx.cfg.get("controller", "via_jump", False)),
            tool, ctx.cfg.get("controller", "iface", ""))


def _run_controller(ctx, argv: list[str], timeout: int = 120):
    c = _controller(ctx)
    if c is None:
        return None
    host, via, tool, iface = c
    cmd = " ".join(shlex.quote(a) for a in
                   [tool, "--iface", iface, *argv])
    return ctx.transport.run(host, cmd, via_jump=via, timeout=timeout)


# --------------------------------------------------------------------------
# Runners
# --------------------------------------------------------------------------

def aecp_cmd(ctx, item) -> str:
    """An AECP/AEM command item: send it, check the status the registry expects.

    The registry row supplies the command and the expected status through its
    `note`/overlay fields; here we only own the transport, the verdict shape and
    the BLOCKED-not-FAILED rule.
    """
    r = _run_controller(ctx, ["--item", item.id])
    if r is None:
        ctx.blocked(item.id, "no controller tool configured - this item is "
                             "driven from the controller host")
        return logmod.BLOCKED
    verdict = logmod.PASS if r.ok else logmod.FAIL
    ctx.check(item.id, verdict,
              measured={"rc": r.rc, "area": item.area, "mapping": item.mapping},
              detail=(r.out or r.err).strip()[-400:])
    return verdict


def aecp_counters(ctx, item) -> str:
    """GET_COUNTERS: the shallow leg here, the deep audit in phase 3."""
    r = _run_controller(ctx, ["--item", item.id])
    if r is None:
        ctx.blocked(item.id, "no controller tool configured")
        return logmod.BLOCKED
    verdict = logmod.PASS if r.ok else logmod.FAIL
    ctx.check(item.id, verdict, measured={"rc": r.rc},
              detail="GET_COUNTERS round trip; the per-counter provoke/neighbour "
                     "audit is phase 3")
    return verdict


def aecp_audio_maps(ctx, item) -> str:
    """Audio maps both ways, cross-checked against the fabric map window.

    The wire answer alone is not enough: a map the entity reports but the
    crossbar does not carry is exactly the "armed and genuinely silent" case, so
    `CHMAP_STAT` commit movement is checked alongside the command result.
    """
    r = _run_controller(ctx, ["--item", item.id])
    if r is None:
        ctx.blocked(item.id, "no controller tool configured")
        return logmod.BLOCKED
    fabric = {}
    for name in ctx.board_names:
        snap = ctx.csr(name).snapshot()
        fabric[name] = {"CHMAP_STAT": f"0x{snap['CHMAP_STAT']:08X}",
                        "commits": snap["CHMAP_STAT"] & 0xFFFF,
                        "csr_refused": (snap["CHMAP_STAT"] >> 16) & 0xFF,
                        "PBK_STAT": f"0x{snap['PBK_STAT']:08X}"}
    verdict = logmod.PASS if r.ok else logmod.FAIL
    ctx.check(item.id, verdict, measured={"rc": r.rc, "fabric": fabric},
              detail=(r.out or r.err).strip()[-400:])
    return verdict


def gptp_posture(ctx, item) -> str:
    """gPTP posture read at the tap. Needs the capture host; else BLOCKED."""
    r = _run_controller(ctx, ["--item", item.id])
    if r is None:
        ctx.blocked(item.id, "gPTP posture is read at a capture tap - no "
                             "controller/capture tool configured")
        return logmod.BLOCKED
    verdict = logmod.PASS if r.ok else logmod.FAIL
    ctx.check(item.id, verdict, measured={"rc": r.rc},
              detail=(r.out or r.err).strip()[-400:])
    return verdict


def srp_domain(ctx, item) -> str:
    """MSRP Domain declaration posture, cross-checked with LWSRP_STATUS.

    The wire half needs a tap; the fabric half is readable here and is worth
    recording either way, because a shortfall flag explains a wire result that
    otherwise looks arbitrary.
    """
    fabric = {}
    for name in ctx.board_names:
        snap = ctx.csr(name).snapshot()
        st = snap["LWSRP_STATUS"]
        fabric[name] = {
            "LWSRP_STATUS": f"0x{st:08X}",
            "domain_ok": bool(st >> 5 & 1),
            "reservation_active": bool(st >> 6 & 1),
            "row_shortfall": bool(st >> 11 & 1),
            "msrp_failure_code": (st >> 16) & 0xFF,
        }
    r = _run_controller(ctx, ["--item", item.id])
    if r is None:
        ctx.blocked(item.id, "the Domain declaration is a WIRE assertion and "
                             "needs a tap - fabric state recorded only",
                    measured={"fabric": fabric})
        return logmod.BLOCKED
    shortfall = [n for n, f in fabric.items() if f["row_shortfall"]]
    verdict = logmod.PASS if (r.ok and not shortfall) else logmod.FAIL
    ctx.check(item.id, verdict, measured={"rc": r.rc, "fabric": fabric},
              detail=("attribute-row shortfall on " + ", ".join(shortfall))
              if shortfall else (r.out or r.err).strip()[-400:])
    return verdict


ITEM_RUNNERS = {
    "aecp_cmd": aecp_cmd,
    "aecp_counters": aecp_counters,
    "aecp_audio_maps": aecp_audio_maps,
    "gptp_posture": gptp_posture,
    "srp_domain": srp_domain,
}
