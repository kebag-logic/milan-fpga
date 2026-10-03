#!/usr/bin/env python3
"""R457-1 probe: the tuple form of verdict() in tdm8_render_mutants.py.
A tuple is 'caught' only when EVERY named check failed; one missing name,
a pass, or a masked rc must not be 'caught'. usage: verdict_tuple_test.py <suite dir>
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import tdm8_render_mutants as m  # noqa: E402

names = m.LAW_SETTLED
assert len(names) == 18 and len(set(names)) == 18
tail = "\ntdm8_render: checks: 88 failures: {n}\n"


def out_with(failed):
    lines = [f"  [FAIL] {n}" for n in failed]
    lines += [f"  [PASS] {n}" for n in names if n not in failed]
    return "\n".join(lines) + tail.format(n=len(failed))


cases = [
    ("all 18 fail", 1, out_with(names), "caught"),
    ("17 of 18 fail", 1, out_with(names[:-1]), "not caught"),
    ("only the first fails", 1, out_with(names[:1]), "not caught"),
    ("none fail, rc 0", 0, out_with(()), "pass"),
    ("all fail but rc 0", 0, out_with(names), "not caught"),
]
# a prefix collision: "+1" is a prefix of "+130"? Names end with a fixed
# suffix, so check the substring match cannot be satisfied by a different phase
coll = [n for n in names for o in names if n != o and n in o]
ok = True
for label, rc, out, want in cases:
    got = m.verdict(rc, out, names)
    good = (got == want) if want in ("caught", "pass") else (got not in ("caught", "pass"))
    ok &= good
    print(f"{'OK ' if good else 'BAD'} {label}: {got!r}")
print(f"{'OK ' if not coll else 'BAD'} no name is a substring of another: {coll}")
ok &= not coll
# the runner's phase table against the leg's kLawPhases
src = (Path(sys.argv[1]) / "sim_tdm8_render.cpp").read_text()
import re  # noqa: E402
body = re.search(r"kLawPhases = \{([^}]*)\}", src).group(1)
leg = tuple(int(x) for x in re.findall(r"\d+", body))
same = leg == m.LAW_PHASES
print(f"{'OK ' if same else 'BAD'} kLawPhases {leg} == LAW_PHASES")
ok &= same
sys.exit(0 if ok else 1)
