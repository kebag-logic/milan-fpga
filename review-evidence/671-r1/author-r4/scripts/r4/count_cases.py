"""Count check 13's cases and check every window meets every manner: python count_cases.py TREE BODY"""
import sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]) / "sw/firmware/nvm_hosttest"))
import read_fault_cases as RF
body = int(sys.argv[2])
run = RF.fault_cases(body)
print(f"cases {len(run)}")
def manner(c):
    if c.fault[0] != "--read-fault":
        return c.fault[0]
    off = int(c.fault[1].split(":")[1])
    return {0: "magic", 0x0B: "seq"}.get(off, "body")
keys = Counter((c.restart, c.older, c.valid, c.fault[1][0] == c.valid, c.skip, c.count, manner(c)) for c in run)
assert all(v == 1 for v in keys.values()), "a case repeats"
beyond = 0
for restart in (True, False):
    for older, faulted, manners, seqs in RF.GROUPS:
        for valid in "ab":
            slot = valid if faulted == "valid" else "ba"["ab".index(valid)]
            own = faulted == "valid"
            clean = RF.expect(RF.FaultCase(valid, older, seqs[0], ("--read-fault", f"{slot}:0:0:0"), 0, 0, restart)).reads
            bound = RF.BOOT_READ_BOUND - int(restart)
            ws = RF.windows(bound)
            got = {(k[4], k[5]) for k in keys if k[:4] == (restart, older, valid, own)}
            assert got == set(ws), (restart, older, valid, own)
            bytewise = [m for m in manners if not m.startswith("--")]
            for w in ws:
                for m in bytewise:
                    assert (restart, older, valid, own, w[0], w[1], m) in keys, (w, m)
            n = sum(1 for k in keys if k[:4] == (restart, older, valid, own))
            beyond += len(ws) * len(manners) - n
            print(f"  restart={restart!s:<5} older={older!s:<5} valid={valid} faulted={faulted:<5}: clean boot {clean} reads, full bound {bound}, "
                  f"{len(ws)} windows x {len(manners)} manners = {len(ws) * len(manners)}, run {n}")
print(f"every window meets every byte manner; {beyond} cases beyond the detection limit not run")
m = Counter((c.older, "valid" if c.fault[1][0] == c.valid else "other", manner(c)) for c in run)
for k, v in sorted(m.items()):
    print(f"  older={k[0]!s:<5} faulted={k[1]:<5} manner={k[2]:<13}: {v}")
s = Counter((c.older, c.seq) for c in run)
print("  sequences:", {f"{'both' if k[0] else 'one'}:{k[1]:#x}": v for k, v in sorted(s.items())})
print(f"restart cases {sum(c.restart for c in run)}, cold {sum(not c.restart for c in run)}")
held = sum(1 for c in run if RF.expect(c).unread)
unst = sum(1 for c in run if RF.expect(c).unstaged)
print(f"cases the model holds: {held}; with a re-stage that did not read back: {unst}")
print("reads distribution:", sorted(Counter(RF.expect(c).reads for c in run).items()))
