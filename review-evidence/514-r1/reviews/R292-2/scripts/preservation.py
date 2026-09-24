"""Check that every prior self-test case line survives verbatim and in order."""
import sys
prev = [l for l in open(sys.argv[1]).read().splitlines() if l.startswith("  ok ")]
head = [l for l in open(sys.argv[2]).read().splitlines() if l.startswith("  ok ")]
i = 0
for h in head:
    if i < len(prev) and h == prev[i]:
        i += 1
fails = [l for l in open(sys.argv[2]).read().splitlines() if l.startswith("  FAIL")]
print("prev ok cases", len(prev), "head ok cases", len(head), "prev matched in order", i, "head FAIL lines", len(fails))
added = [h for h in head if h not in set(prev)]
print("added", len(added))
print("\n".join(added))
sys.exit(0 if i == len(prev) and not fails else 1)
