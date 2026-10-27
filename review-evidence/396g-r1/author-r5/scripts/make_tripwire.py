#!/usr/bin/env python3
"""Write a tripwire copy of the planner: any unbalanced reading, or the balance guard firing, raises.

Usage: python3 -I make_tripwire.py <torture_campaign.py> <copy's tb/tools dir>

Every probe run against the copy then shows, by its return code and a
`TRIPWIRE` line, whether a reading that does not balance was ever formed or
the guard behind it ever fired. Nothing else changes.
"""
import sys
from pathlib import Path

source, target = Path(sys.argv[1]), Path(sys.argv[2])
text = source.read_text(encoding="utf-8")
EDITS = (
    ("            return (balance and _audio_net(events) != final, *self._score(events, arms))",
     "            if balance and _audio_net(events) != final:\n"
     "                raise RuntimeError(\"TRIPWIRE: an unbalanced reading\")\n"
     "            return (balance and _audio_net(events) != final, *self._score(events, arms))"),
    ("                events = [self._unbalanced(track, window, found)]",
     "                raise RuntimeError(\"TRIPWIRE: the balance guard fired\")"),
)
for old, new in EDITS:
    assert text.count(old) == 1, old
    text = text.replace(old, new)
target.mkdir(parents=True, exist_ok=True)
(target / "torture_campaign.py").write_text(text, encoding="utf-8")
print("tripwire copy written")
