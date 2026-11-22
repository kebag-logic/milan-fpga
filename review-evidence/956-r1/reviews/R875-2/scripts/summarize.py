"""summarize.py <log>...: per log, failed tests, OK count, and request-to-wire extremes of the phase probes."""
import re, sys
for p in sys.argv[1:]:
    t = open(p, errors="replace").read()
    ok = re.findall(r"^\[       OK \] (\S+)", t, re.M)
    fail = sorted(set(re.findall(r"^\[  FAILED  \] (\S+) \(", t, re.M)))
    print(f"== {p}: OK {len(ok)} FAILED {fail}")
    for kind in ("held", "free"):
        v = [int(x) for x in re.findall(rf"PROBE {kind} phase \d+ if\d: request-to-wire (\d+)", t)]
        if v:
            print(f"   ReviewerPhase {kind}: n={len(v)} min {min(v)} max {max(v)} ms")
    v = [int(x) for x in re.findall(r"PROBE P4 .*request-to-wire (\d+)", t)]
    if v:
        print(f"   P4 off-centisecond: n={len(v)} min {min(v)} max {max(v)} ms")
    for m in re.findall(r"^(PROBE (?:P[123]|step5).*)$", t, re.M):
        print("  ", m)
    ev = [n for n in ok if n.startswith("EveryPhase/")]
    if ev:
        print(f"   EveryPhase instances OK: {len(ev)}")
    for n in ok:
        if "Reset" in n or "JoinTimerRunning" in n or "AtTheLatest" in n or "ABuildPaused" in n:
            print("   OK", n)
