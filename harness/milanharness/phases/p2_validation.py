# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! Phase 2 - VALIDATION. Every `es-N.M` item, plus the BDD conformance suite.
#!
#! **Every registered item gets a row in the run, implemented or not.** A stub
#! reports `BLOCKED: not-implemented` with its reason, so the report can never
#! quietly cover 22 items and call the campaign complete. That visibility is the
#! reason the registry exists.
#!
#! The item registry itself lives outside this repository (its procedures and
#! pass criteria are private). When it is not configured, this phase reports one
#! clean BLOCKED and moves on - it does not crash, and it does not invent items.

from __future__ import annotations

import re
import shlex
from pathlib import Path

from .. import log as logmod

PHASE = "validation"
REPO = Path(__file__).resolve().parents[3]


def run(ctx, clock) -> None:
    clock.item(ctx, PHASE, "validation/bdd-conformance", lambda: _bdd(ctx))

    if ctx.registry is None:
        ctx.blocked("validation/items",
                    f"item registry unavailable: {ctx.registry_error}")
        return

    tally = ctx.registry.tally()
    ctx.info("validation/items", "item registry loaded", measured=tally)

    for item in ctx.registry:
        clock.item(ctx, PHASE, item.id, lambda it=item: _item(ctx, it))

    ctx.info("validation/items", "item sweep complete", measured={
        "rows": tally["total"],
        "implemented": tally["implemented"],
        "not_implemented": tally["not_implemented"],
    })


def _item(ctx, item) -> str:
    from .. import runners as runmod

    if not item.implemented:
        ctx.blocked(item.id, f"not-implemented ({item.status})"
                             + (f": {item.note}" if item.note else ""),
                    measured={"group": item.group, "area": item.area,
                              "mapping": item.mapping, "status": item.status})
        return logmod.BLOCKED
    fn = runmod.ITEM_RUNNERS.get(item.runner)
    if fn is None:
        ctx.blocked(item.id,
                    f"registry names runner {item.runner!r}, which this harness "
                    f"build does not provide",
                    measured={"runner": item.runner})
        return logmod.BLOCKED
    return fn(ctx, item)


def _bdd(ctx) -> str:
    """`cd tests && behave -f plain` - 113 scenarios, offline, no DUT needed.

    A missing `behave` is BLOCKED, not FAILED: the device did not do anything
    wrong, the host is missing a tool.
    """
    tests = REPO / "tests"
    if not (tests / "environment.py").is_file():
        ctx.blocked("validation/bdd-conformance",
                    f"no behave suite at {tests}")
        return logmod.BLOCKED
    behave = ctx.cfg.get("exec", "behave", "") or "behave"
    r = ctx.transport.local(
        ["sh", "-c", f"cd {shlex.quote(str(tests))} && {shlex.quote(behave)} -f plain"],
        timeout=int(ctx.cfg.phase_timeouts.get("item", 600)))
    if r.rc == 127:
        ctx.blocked("validation/bdd-conformance",
                    f"{behave!r} not on PATH (set [exec].behave to the venv's "
                    f"behave - see harness/README.md)")
        return logmod.BLOCKED
    tail = r.out.strip().splitlines()[-6:]
    stats = _parse_behave(r.out)
    verdict = logmod.PASS if (r.ok and stats.get("scenarios_failed", 1) == 0) \
        else logmod.FAIL
    ctx.check("validation/bdd-conformance", verdict, measured=stats,
              detail="\n".join(tail))
    return verdict


#: behave's summary lines, e.g. "113 scenarios passed, 0 failed, 0 skipped".
_SUMMARY_RE = re.compile(
    r"^(?P<total>\d+)\s+(?P<noun>features?|scenarios?|steps?)\s+"
    r"(?P<rest>.*)$")
_PART_RE = re.compile(r"(\d+)\s+(passed|failed|skipped|undefined|error(?:ed)?)")


def _parse_behave(text: str) -> dict:
    """Pull behave's own tallies out of its plain formatter summary."""
    out: dict[str, int] = {}
    for line in text.splitlines():
        m = _SUMMARY_RE.match(line.strip())
        if not m:
            continue
        noun = m.group("noun").rstrip("s") + "s"
        out[f"{noun}_total"] = int(m.group("total"))
        for count, word in _PART_RE.findall(m.group("rest")):
            out[f"{noun}_{word}"] = int(count)
    return out
