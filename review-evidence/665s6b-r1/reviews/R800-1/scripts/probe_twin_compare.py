#!/usr/bin/env python3
"""probe_twin_compare.py TREE CAPTURES - probes of TREE's twin comparison on the unplanted captures.

CAPTURES holds fabric.json and split.json as `make twin` wrote them. Each probe edits the comparison's
modules in memory only (never a file) and says what the comparison then finds:
  * the baseline: 0 findings;
  * every F5 ledger row a real difference: each half's selection fails the other half's predicate, and the
    two selections differ;
  * the notices of the AECP owner's rows 5 and 6 equal across the halves (no row, no finding);
  * CONTROLLER_AVAILABLE's sequence_id per controller in each half, and the mutants of its rules:
    sequence_id byte-compared; gaps refused; responses not matched;
  * each OWED_GRADES row removed in turn: the fabric's grade findings it covered must appear;
  * each of the two #860 rows' asserted trace changed by one character: the row must stop holding.
Prints one line per probe and "probe_twin_compare: PASS" or "FAIL"; exit 0 only on PASS.
"""
import dataclasses
import importlib
import sys
from pathlib import Path

tree, caps = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree / "tb/verilator/milan_dp"))
import twin_compare as tc  # noqa: E402
import twin_decode as td  # noqa: E402
import twin_grades as tg  # noqa: E402

ok = True


def say(cond, what):
    global ok
    ok &= bool(cond)
    print(f"[{'ok' if cond else 'FAIL'}] {what}", flush=True)


def run():
    fab, spl = td.load(caps / "fabric.json"), td.load(caps / "split.json")
    return fab, spl, tc.compare(fab, spl)


fab, spl, base = run()
say(base["findings"] == [], f"baseline: {len(base['findings'])} findings, {len(base['notes'])} notes")
kinds = sorted({n.split("]")[0] + "]" for n in base["notes"]})
say(set(kinds) <= {"[TAIL]", "[LEDGER]", "[OWED]"}, f"baseline notes are only {kinds}")

hf = tc.Half(fab.frames.get("AECP", []), tc.msrp_attributes(fab.frames.get("MSRP", [])), fab)
hs = tc.Half(spl.frames.get("AECP", []), tc.msrp_attributes(spl.frames.get("MSRP", [])), spl)
for row in tc.LEDGER:
    f, s = row.select(hf), row.select(hs)
    real = not row.fabric(hs, s) and not row.split(hf, f) and tc.normalized(f) != tc.normalized(s)
    say(real and row.fabric(hf, f) and row.split(hs, s), f"ledger row {row.name}: holds, and is a real difference")

# rows 5 and 6: the started-state GET_STREAM_INFO notice of STREAM_INPUT 0 and the LOCK_ENTITY release notice
for key, what in (((0x000F, (5, 0)), "row 5: STREAM_INPUT 0 GET_STREAM_INFO notices"),
                  ((0x0001, (0, 0)), "row 6: LOCK_ENTITY notices")):
    nf = [td.without_seq(s) for s in tc.notices(hf, *key)]
    ns = [td.without_seq(s) for s in tc.notices(hs, *key)]
    say(nf and nf == ns, f"{what}: {len(nf)} in each half, equal without sequence_id")
lock = [s for s in tc.notices(hf, 0x0001, (0, 0))]
say(any(s.data[s.at + 24 + 3] & 1 for s in lock), "row 6: a fabric LOCK_ENTITY notice carries flags UNLOCK (1)")

_, mf = tg.grade_commands(fab)
_, ms = tg.grade_commands(spl)
print(f"  CONTROLLER_AVAILABLE ids: fabric {mf['controller_available_ids']}, split {ms['controller_available_ids']}")
say(any(len(v) > 1 and any(b - a > 1 for a, b in zip(v, v[1:])) for v in ms["controller_available_ids"].values()),
    "the split's ids to one controller have a gap (so 'gaps allowed' is load-bearing)")

# mutant: the entity's commands byte-compared with their sequence_id
saved = tc.COMMANDS
tc.COMMANDS = dataclasses.replace(saved, body=lambda s: s.data)
_, _, r = run()
tc.COMMANDS = saved
say(any("AECP command" in f for f in r["findings"]), f"mutant sequence_id byte-compared: {len(r['findings'])} "
    f"finding(s), e.g. {r['findings'][:1]}")

# mutant: gaps refused (strictly +1)
src = Path(tg.__file__).read_text()
mut = src.replace("if not 0 < (b - a) % 65536 < 32768]", "if (b - a) % 65536 != 1]")
assert mut != src
ns = {}
exec(compile(mut, tg.__file__, "exec"), ns)
found, _ = ns["grade_commands"](spl)
say(found, f"mutant gaps refused: the split's grade finds {found[:1]}")

# mutant: responses matched to nothing (count compare kept): drop the id comparison by swapping the responses
found_f, _ = tg.grade_commands(fab)
say(not found_f, "the fabric's CONTROLLER_AVAILABLE grade is clean as built")

# each OWED_GRADES row removed in turn
saved = tc.OWED_GRADES
for k, row in enumerate(saved):
    tc.OWED_GRADES = saved[:k] + saved[k + 1:]
    _, _, r = run()
    say(r["findings"] and all(row.covers(f) for f in r["findings"]),
        f"row {row.name} removed: {len(r['findings'])} finding(s), each one it covered, e.g. {r['findings'][:1]}")
tc.OWED_GRADES = saved

# each #860 row's asserted trace changed by one character
for k, row in enumerate(saved):
    if row.owed_to.startswith("#860"):
        tc.OWED_GRADES = saved[:k] + (dataclasses.replace(row, says=row.says.replace("x1 from", "x2 from", 1)),) \
            + saved[k + 1:]
        _, _, r = run()
        say(any(f"owed row {row.name} does not hold" in f for f in r["findings"]),
            f"row {row.name}'s trace changed: {r['findings'][:1]}")
tc.OWED_GRADES = saved

print(f"probe_twin_compare: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
