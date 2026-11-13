# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Steps for aecp_owed_notices.feature: AECP's owed-notice queue (#894), an offline model of its rules.

Each rule the model applies is pinned to the shipped firmware text that makes it (RULES): the step that reads the
rules fails a scenario whose rule the source no longer states. The model then plays the scenario: a command's response
is committed in its record's turn and its notice, when it fits a slot, joins the queue's tail; a poll sends the
queue's oldest notice to every registered controller but its requester, each at that recipient's next sequence_id,
then a notice waiting in the response buffer; AECP is not ready while a notice waits there or the queue is full.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING

from behave import given, then, when  # pylint: disable=no-name-in-module

if TYPE_CHECKING:  # behave is a test-only dependency; the annotation is lazy
    from behave.runner import Context

ROOT = Path(__file__).resolve().parents[2]
AECP_C = ROOT / "sw/firmware/ctrl/aecp/aecp.c"
AECP_H = ROOT / "sw/firmware/ctrl/aecp/aecp.h"
AECP_MBX_H = ROOT / "sw/firmware/ctrl/aecp/aecp_mbx.h"

#: Each rule and the firmware text that makes it.
RULES = {
    "ready only while the queue has a slot": (AECP_C, "(a->owed_count == 0u || a->owed_count < a->cfg.owed_slots)"),
    "a record's turn commits its response, the notice to the queue": (AECP_C,
                                                                     "(a->cfg.queue != NULL && a->cfg.queue->owe(a))"),
    "the response before any notice": (AECP_C, "return respond(a) || notices(a, drains);"),
    "the queue's oldest notice first": (AECP_C, "struct aecp_owed *o = &a->cfg.owed[a->owed_head];"),
    "its requester left out": (AECP_C, "r->controller == requester"),
    "each recipient's next sequence_id": (AECP_C, "++r->sequence;"),
    "a longer notice stays in the response buffer": (AECP_C, "a->response_bytes > AECP_OWED_BYTES"),
    "the slot's length": (AECP_H, "#define AECP_OWED_BYTES 552u"),
    "the depth at one interface": (AECP_MBX_H,
                                   "#define AECP_MBX_OWED_SLOTS (MBX_N_IF == 1u ? MBX_CH_AECP_RATE_BURST : 0u)"),
}


class OwedModel:
    """The queue's rules, played: frames on the wire as (kind, command, recipient, sequence_id)."""

    def __init__(self, depth: int, slot_bytes: int, controllers: list[str]) -> None:
        """A queue of `depth` slots of `slot_bytes`, the controllers registered, each at its first sequence_id."""
        self.depth, self.slot_bytes = depth, slot_bytes
        self.controllers = controllers
        self.sequence = {c: 0x100 for c in controllers}
        self.queue: list[tuple[str, str]] = []      # (command, requester)
        self.held: tuple[str, str] | None = None    # a notice waiting in the response buffer
        self.response_owed: tuple[str, str] | None = None
        self.wire: list[tuple[str, str, str, int]] = []

    def ready(self) -> bool:
        """Whether AECP takes the next command: no response owed, no notice held, the queue with a slot."""
        return self.held is None and self.response_owed is None and (not self.queue or len(self.queue) < self.depth)

    def command(self, name: str, requester: str, notice_bytes: int) -> bool:
        """A state-changing command taken, if AECP is ready: whether it was."""
        if not self.ready():
            return False
        if notice_bytes <= self.slot_bytes and len(self.queue) < self.depth:
            self.wire.append(("response", name, requester, 0))
            self.queue.append((name, requester))
        else:
            self.response_owed = (name, requester)
            self.held = (name, requester)
        return True

    def _notify(self, name: str, requester: str) -> None:
        for c in self.controllers:
            if c != requester:
                self.wire.append(("notice", name, c, self.sequence[c]))
                self.sequence[c] += 1

    def poll(self) -> None:
        """One poll: the response owed, then the queue's oldest notice, else the one the response buffer holds."""
        if self.response_owed is not None:
            self.wire.append(("response", *self.response_owed, 0))
            self.response_owed = None
        if self.queue:
            self._notify(*self.queue.pop(0))
        elif self.held is not None:
            self._notify(*self.held)
            self.held = None

    def drain(self) -> None:
        """Polls until nothing is owed."""
        for _ in range(64):
            self.poll()


@given("AECP's owed-notice rules read from the shipped firmware")
def step_rules(context: Context) -> None:
    """Given: AECP's owed-notice rules read from the shipped firmware."""
    missing = [rule for rule, (path, text) in RULES.items() if text not in path.read_text(encoding="utf-8")]
    assert not missing, f"the firmware no longer states: {missing}"
    burst = re.search(r"- name: aecp\b.*?burst: (\d+)", (ROOT / "sw/mailbox/mailbox.yaml").read_text(encoding="utf-8"),
                      re.S)
    context.depth = int(burst[1]) if burst else 16
    context.slot = int(re.search(r"#define AECP_OWED_BYTES (\d+)u", AECP_H.read_text(encoding="utf-8"))[1])


@given("controllers A, B and C registered for unsolicited notifications")
def step_controllers(context: Context) -> None:
    """Given: controllers A, B and C registered for unsolicited notifications."""
    context.model = OwedModel(context.depth, context.slot, ["A", "B", "C"])


@when("A sends a state-changing command and B sends one before any notice leaves")
def step_back_to_back(context: Context) -> None:
    """When: A sends a state-changing command and B sends one before any notice leaves."""
    m = context.model
    assert m.command("set-A", "A", 110)
    assert m.ready(), "(c) a command's notice owed in the queue does not hold the next command"
    assert m.command("set-B", "B", 110)
    m.drain()


@then("the wire carries A's response, then B's response, then the notices")
def step_order(context: Context) -> None:
    """Then: the wire carries A's response, then B's response, then the notices."""
    wire = context.model.wire
    assert wire[0][:3] == ("response", "set-A", "A") and wire[1][:3] == ("response", "set-B", "B"), wire[:2]
    assert all(kind == "notice" for kind, *_ in wire[2:]), "(b) only notices follow the responses"


@then("C receives A's notice before B's, at consecutive sequence_ids")
def step_fifo(context: Context) -> None:
    """Then: C receives A's notice before B's, at consecutive sequence_ids."""
    to_c = [(name, seq) for kind, name, who, seq in context.model.wire if kind == "notice" and who == "C"]
    assert [name for name, _ in to_c] == ["set-A", "set-B"], to_c
    assert to_c[1][1] == to_c[0][1] + 1, to_c


@then("A receives only B's notice and B only A's")
def step_requester(context: Context) -> None:
    """Then: A receives only B's notice and B only A's."""
    wire = context.model.wire
    assert [n for k, n, who, _ in wire if k == "notice" and who == "A"] == ["set-B"]
    assert [n for k, n, who, _ in wire if k == "notice" and who == "B"] == ["set-A"]


@when("commands fill the owed-notice queue at its depth")
def step_fill(context: Context) -> None:
    """When: commands fill the owed-notice queue at its depth."""
    m = context.model
    for n in range(m.depth):
        assert m.command(f"set-{n}", "AB"[n % 2], 110), n


@then("AECP is not ready for the next command")
def step_full(context: Context) -> None:
    """Then: AECP is not ready for the next command."""
    assert not context.model.ready()
    assert not context.model.command("one-more", "A", 110)


@then("one notice sent frees one slot and AECP is ready again")
def step_freed(context: Context) -> None:
    """Then: one notice sent frees one slot and AECP is ready again."""
    context.model.poll()
    assert len(context.model.queue) == context.model.depth - 1 and context.model.ready()


@when("A sends a state-changing command and B sends one whose notice is longer than a slot")
def step_long(context: Context) -> None:
    """When: A sends a state-changing command and B sends one whose notice is longer than a slot."""
    m = context.model
    assert m.command("set-A", "A", 110)
    assert m.command("map-B", "B", context.slot + 14)
    assert not m.ready(), "a longer notice waits in the response buffer, the next command with it"
    context.before_poll = list(m.wire)
    m.drain()


@then("B's response is held until the poll and precedes B's notice")
def step_long_response(context: Context) -> None:
    """Then: B's response is held until the poll and precedes B's notice."""
    assert [w[:3] for w in context.before_poll] == [("response", "set-A", "A")]
    wire = context.model.wire
    response = wire.index(next(w for w in wire if w[:2] == ("response", "map-B")))
    assert all(i > response for i, w in enumerate(wire) if w[:2] == ("notice", "map-B"))


@then("C receives A's notice before B's")
def step_long_fifo(context: Context) -> None:
    """Then: C receives A's notice before B's."""
    to_c = [name for kind, name, who, _ in context.model.wire if kind == "notice" and who == "C"]
    assert to_c == ["set-A", "map-B"], to_c
