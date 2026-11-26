"""cuts.py LOG JUNIT: every power cut of a power-cycle run, in order of its `POWER off at` instant (the run's log), with
the scenario and STREAM_INPUT of the last BIND_RX before it (the junit report, which logs each bind with its time),
whether that bind came after the previous cut, and the durable reading the relay was asked for in its hold (the
log's request lines, by response time)."""
import calendar, html, re, sys, time
log = open(sys.argv[1], errors='replace').read()
jt = html.unescape(open(sys.argv[2], errors='replace').read())
binds, scen, inp = [], None, None
for m in re.finditer(r"Scenario: ([^\n]{0,95})|FOREACH STREAM_INPUT (\d+): start|BIND_RX STREAM_INPUT (\d+) <- T 0: SUCCESS at ([\d.]+)", jt):
    if m[1]: scen = m[1].strip()
    elif m[2]: inp = int(m[2])
    elif m[4]: binds.append((float(m[4]), scen, int(m[3])))
binds.sort()
reqs = {float(t): s for s, t in re.findall(r'^<compliance-lab-name>-RELAY-REQUEST durable (\d+):(\d+\.\d{3}) ', log, re.M)}
offs = [calendar.timegm(time.strptime(a, '%Y-%m-%dT%H:%M:%S')) + int(b) / 1000
        for a, b in re.findall(r'^POWER off at (\S+?)\.(\d{3})Z', log, re.M)]
prev = 0.0
for n, t in enumerate(offs, 1):
    before = [b for b in binds if b[0] < t]
    tb, sc, si = before[-1] if before else (None, None, None)
    new = tb is not None and tb > prev
    read = next((s for r, s in reqs.items() if tb is not None and abs(r - tb) < 0.002), None)
    print(f"cut {n:2d}: off {time.strftime('%H:%M:%S', time.gmtime(t))}Z, {t - tb:.3f} s after the last BIND_RX | {sc[:80]} | "
          f"STREAM_INPUT {si} | a bind since the previous cut: {new} | hold reading: {'yes' if new and read is not None else 'no'}")
    prev = t
