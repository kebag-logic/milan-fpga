"""Run owner_stated_seconds from a scripts tree with every listing checked, not stopping at the first red.

Usage: python3 -I probe_all_listings.py <tree-with-scripts/> [--classify]

For each listing it prints GREEN or RED. With --classify it also prints, from the census clocks the
listing was asked for, the pass that resumed the shell (from the SIGCONT event), how many passes up to
and including it were at or past grace (2 s), the clock of the pass after the resume, and the clock of
the first census that lists a descendant new since the first census.
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
classify = "--classify" in sys.argv
sys.path.insert(0, str(tree / "scripts"))
path = tree / "scripts/test_suite_cancellation.py"
src = path.read_text()
old_assert = ("        assert events == stated, f\"{words}'s stated seconds were not kept on the owner's clock:"
              " {events}\"\n")
assert src.count(old_assert) == 1, "assert line moved"
src = src.replace(old_assert, "        RESULTS.append((words, events == stated, events, stated))\n")
old_call = "            events = starved_cleanup(owner, listing, names, stated, reaped)\n"
assert src.count(old_call) == 1, "call line moved"
src = src.replace(old_call, "            try:\n"
                            "                events = starved_cleanup(owner, listing, names, stated, reaped)\n"
                            "            except AssertionError as exc:\n"
                            "                events = [('raised', str(exc))]\n")
g = {"__name__": "probe", "__file__": str(path), "RESULTS": []}
exec(compile(src, str(path), "exec"), g)
CLOCKS = []
real_starved = g["starved_cleanup"]


def recording(owner, listing, names, stated, reaped=lambda _c: set()):
    seen = []

    def wrapped(clock):
        out = listing(clock)
        seen.append((clock, set(out)))
        return out
    events = real_starved(owner, wrapped, names, stated, reaped)
    CLOCKS.append(seen)
    return events


g["starved_cleanup"] = recording
g["owner_stated_seconds"]()
red = 0
for index, (words, ok, events, stated) in enumerate(g["RESULTS"]):
    red += not ok
    line = f"{'GREEN' if ok else 'RED  '} {words}"
    if classify:
        seen = CLOCKS[index]
        first = seen[0][1] if seen else set()
        conts = [e[0] for e in events if len(e) == 3 and e[1] == "SIGCONT"]
        if conts:
            at = conts[0]
            clocks = [c for c, _ in seen]
            n = clocks.index(at) + 1
            past = sum(1 for c in clocks[:n] if c >= 2)
            after = clocks[n] if n < len(clocks) else None
            line += f" | resume clock {at!r} pass {n} past-grace-pass-ordinal {past} next-pass {after!r}"
        new = [c for c, pids in seen if pids - first]
        if new:
            line += f" | first new-descendant census at {new[0]!r} ({'inside' if new[0] < 2 else 'past'} grace)"
    print(line)
    if not ok:
        print(f"      events {events}\n      stated {stated}")
print(f"listings {len(g['RESULTS'])} red {red}")
