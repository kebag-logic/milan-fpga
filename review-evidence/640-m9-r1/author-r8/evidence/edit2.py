"""Second round-8 commit: the sentence limit and the probe pointer's verb."""
import sys
p = "$LANES/640-mark2-charter/docs/design/MARK_II_STREAM_ENGINES.md"
s = open(p, encoding="utf-8").read()
for old, new in [("At 192 kHz they are 18.093 µs, without the packetizer.", "At 192 kHz, without the packetizer: 18.093 µs."),
                 (") sampled these cases.\n", ") reports these cases.\n")]:
    if s.count(old) != 1:
        sys.exit(f"expected one match: {old!r}")
    s = s.replace(old, new)
open(p, "w", encoding="utf-8").write(s)
