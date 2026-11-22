#!/usr/bin/env python3
"""Plant one reviewer probe (a disposable source mutation) into an already copied tree: each (old, new) must occur
exactly once in the file.

Usage: python3 -I make_probe.py <tree-root> <probe-name>
"""
import sys
from pathlib import Path

C = "sw/firmware/ctrl/srp/srp_mbx.c"
H = "sw/firmware/ctrl/srp/srp_mbx.h"
PROBES = {
    # the count also counts the participant's own Talker declarations (the Applicant test dropped)
    "own-declared-counted": (C, "        (SRP_UNDECLARED_APPL >> status->appl & 1u) != 0u && !bound_stream(i,id)) {\n",
                             "        !bound_stream(i,id)) {\n"),
    # the count also counts a bound StreamID's Talkers
    "bound-counted": (C, "        (SRP_UNDECLARED_APPL >> status->appl & 1u) != 0u && !bound_stream(i,id)) {\n",
                      "        (SRP_UNDECLARED_APPL >> status->appl & 1u) != 0u && (bound_stream(i,id) || true)) {\n"),
    # one past the bound kept
    "bound-plus-one": (C, "    if (*count >= SRP_KEPT_TALKERS) {\n        return false;\n",
                       "    if (*count > SRP_KEPT_TALKERS) {\n        return false;\n"),
    # a bound StreamID's registration held as well
    "hold-bound-too": (C, "    if (registered && !bound && h == NULL && m->held_count < SRP_HELD_STREAMS) {\n",
                       "    if (registered && h == NULL && m->held_count < SRP_HELD_STREAMS) {\n"),
    # the filter counts a newly kept Talker but does not list it, so its refresh is counted again
    "kept-unlisted": (C, "    memcpy(kept[*count].stream_id.bytes,stream_id,8);\n    kept[(*count)++].kind = kind;\n",
                      "    (*count)++;\n"),
    # the kept list matched on kind alone, whatever the StreamID
    "any-stream-kept": (C, "        if (kept[n].kind == kind && same(kept[n].stream_id.bytes,stream_id,8)) {\n",
                        "        if (kept[n].kind == kind) {\n"),
    # the bound one short of the inputs
    "bound-one-short": (H, "#define SRP_KEPT_TALKERS CTRL_SRP_SINKS\n", "#define SRP_KEPT_TALKERS (CTRL_SRP_SINKS - 1u)\n"),
    # an unbound StreamID's indication owes the walk again (the base's schedule): a load-only change
    "unbound-walks": (C, "    i->stale = i->stale || bound;\n", "    i->stale = true;\n"),
}

root = Path(sys.argv[1])
path, old, new = PROBES[sys.argv[2]]
target = root / path
text = target.read_text()
assert text.count(old) == 1, (sys.argv[2], text.count(old))
target.write_text(text.replace(old, new))
print("planted", sys.argv[2], "in", path)
