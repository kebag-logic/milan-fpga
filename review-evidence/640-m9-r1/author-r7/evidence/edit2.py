"""Round 7, commit 2: residue R757-6 RR11 and R758-6-R1, combined."""
import sys
p = "$LANES/640-mark2-charter/docs/design/MARK_II_STREAM_ENGINES.md"
s = open(p, encoding="utf-8").read()
for old, new in [
 ("A margin under 125 µs lapses the head every packet.\nInterleaved copies can then land one sample apart.\n\n[Open design item 3]",
  "Both copies' margins under about 125 µs lapse every head.\nThe threshold carries the conversion error, so it is approximate.\n\nInterleaved copies can then land one sample apart.\n[Open design item 3]"),
 ("A margin under 125 µs lapses the head before the next packet, so rule 2 places every packet by its own time. When first arrival",
  "A margin under about 125 µs on both networks lapses the head before the next packet, so rule 2 places every packet by its own time. The threshold carries the conversion error: within that error of 125 µs, only some packets lapse. When first arrival"),
]:
    n = s.count(old)
    if n != 1:
        sys.exit(f"expected one match, got {n}: {old[:80]!r}")
    s = s.replace(old, new)
open(p, "w", encoding="utf-8").write(s)
