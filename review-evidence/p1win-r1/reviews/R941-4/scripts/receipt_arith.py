"""receipt_arith.py: recompute the derived figures of the round-4 board receipts from their own primary numbers
(si0-report.txt epoch and UTC times; fail-8x8-input0.txt per-attempt table). No input files: the primary numbers are
copied below with the receipt line they come from, so a reader can check each against the receipt."""
from datetime import datetime, timezone
def utc(s): return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=timezone.utc).timestamp()
b = 1795687230.218                                  # si0-report.txt:6 bind response
print("si0-report")
print(f"  declared before bind      {1795687229.213 - b:+.3f}  (receipt t-1.005)")
off, on = utc("2026-11-26T10:00:31.769") - b, utc("2026-11-26T10:00:42.845") - b   # :10, :15
print(f"  relay off                 {off:.3f}  (t+1.551)   relay on {on:.3f} (t+12.627)")
wd = 1795687233.286 - b                             # :13
print(f"  withdraw                  {wd:.3f}  (t+3.068); after return 2.067: {wd-2.067:.3f} (1.001); after last frame 1.782: {wd-1.782:.3f} (1.286)")
print(f"  withdraw after cut issued {wd-1.000:.3f}  (the drain counts from the command's return, not the issue)")
print(f"  last frame after relay off {1.782-off:.3f}; return after relay off {2.067-off:.3f}; durable before last frame {1.782-0.586:.3f} (1.196)")
d = 1795687247.025 - b                              # :18
print(f"  declaration               {d:.3f}; after relay on {d-on:.3f} (4.18); after test ref (on-0.56) {d-on+0.56:.2f} (4.74)")
print(f"  probe response after declaration {1795687250.999-1795687247.025:.3f} (3.974); after relay on {1795687250.999-b-on:.3f}")
print("fail-8x8-input0 (cut, relay off, return, withdraw, last frame, probe, relay on, own declaration)")
rows = [(1.000, 1.488, 1.870, 1.870, 1.907, 1.909, 11.477, 22.548, 11.68),
        (22.550, 23.130, 23.571, 23.571, 23.572, 23.572, 33.164, 44.201, 11.63),
        (44.203, 44.836, 45.431, 45.431, 45.021, 44.438, 54.977, 65.994, 11.56)]
for n, (c, o, r, w, l, p, pon, dec, stated) in enumerate(rows, 1):
    print(f"  attempt {n}: return-off {r-o:.3f}; last-off {l-o:.3f}; last-return {l-r:+.3f}; probe-withdraw {p-w:+.4f}; "
          f"probe-cut {p-c:+.3f}; probe before off {o-p:+.3f}; decl-probe {dec-p:.2f}; "
          f"decl after relay on {dec-pon:.3f} vs stated {stated} (difference {stated-(dec-pon):.3f})")
