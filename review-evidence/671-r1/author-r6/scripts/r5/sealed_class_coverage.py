"""Which sequences check 13's generated cases give the R603-4 class: in one
slot's judgement, exactly two sealed (distinct, CRC-closing, refused) faulty
reads and then a clean read that stands, per entry path, layout,
orientation and faulted slot. Replays the reference model's read schedule
(read_fault_cases.expect), not the firmware.
python3 -I sealed_class_coverage.py REPO"""
import sys
from collections import defaultdict
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
sys.dont_write_bytecode = True
sys.path.insert(0, str(repo / "sw/firmware/nvm_hosttest"))
import read_fault_cases as rfc


def judgements(case):
    """Each slot's judgement reads as the model answers them: 'F' faulty, 'C' clean."""
    clean = {case.valid.upper(): "OK", case.other.upper(): "OK" if case.older else "BLANK"}
    slot = case.fault[1][0].upper()
    reads = 0 if case.restart else 1
    out = {}
    for s in "AB":
        seen, trace = [], ""
        for _ in range(rfc.READ_TRIES):
            faulty = s == slot and case.skip <= reads < case.skip + case.count
            reads += 1
            got = ("REFUSED", reads) if faulty else (clean[s],)
            trace += "F" if faulty else "C"
            if got[0] == "OK" or got in seen:
                break
            seen.append(got)
        out[s] = trace
    return slot, out


cover = defaultdict(set)
for c in rfc.fault_cases(1000):
    if c.fault[0] != "--read-sealed":
        continue
    slot, trace = judgements(c)
    if trace[slot] == "FFC":
        role = "newer/valid" if slot == c.valid.upper() else "older"
        manner = "entity" if c.fault[1].split(":")[1] == "20" else "record area"
        cover[("restart" if c.restart else "cold boot", "both valid" if c.older else "other blank",
               f"slot {slot} faulted ({role})", manner)].add(c.seq)
missing = 0
for key in sorted(cover):
    full = set(rfc.BOTH_VALID_SEQS if key[1] == "both valid" else rfc.FAULT_SEQS)
    gap = full - cover[key]
    missing += bool(gap)
    print(" / ".join(key) + ": " + ", ".join(hex(x) for x in sorted(cover[key]))
          + (f"  MISSING {', '.join(hex(x) for x in sorted(gap))}" if gap else "  (every sequence)"))
print(f"{len(cover)} combinations, {missing} missing a sequence")
sys.exit(1 if missing or len(cover) != 24 else 0)
