"""Count every dynmap_mutants.py edit pattern in the merged sources (exactly once each)."""
import sys
sys.path.insert(0, sys.argv[1])
import dynmap_mutants as m
bad = 0
for mut in m.MUTATIONS:
    leg, name, edits = mut[:3]
    src = m.SHADOW_RTL if (len(mut) > 4 and mut[4] == "shadow") else m.DP_RTL
    text = src.read_text()
    for pat, _ in edits:
        c = text.count(pat)
        if c != 1:
            bad += 1
            print(f"BAD {c}x {leg} {name!r} in {src.name}")
print(f"{len(m.MUTATIONS)} mutants checked, {bad} bad anchors")
