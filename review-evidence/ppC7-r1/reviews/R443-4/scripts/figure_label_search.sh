#!/usr/bin/env bash
# Search every figure source and render for a removed op, adapter, counter block or tick.
# Usage: figure_label_search.sh <repo-root>
set -u
root=${1:?repo root}
cd "$root" || exit 2
pat='adapter|counters? subsystem|counter[ -]?banks?|counter block|to SMs / counters|READ_AS_PATH|AS_CAPABLE_CHANGE|PATH_CHANGE|INPUT_CONFIGURE|INPUT_ENABLE|INPUT_DISABLE|INPUT_START|INPUT_STOP|SET_INPUT_FORMAT|SET_OUTPUT_FORMAT|OUTPUT_SET_PT_OFFSET|OUTPUT_STATUS|GET_MCR_DEFAULTS|MC_LOCKED|MC_UNLOCKED|gm_changed_tick|adp_gm_tick|mclk\.[A-Z_]+|avtp\.[A-Z_]+|gptp\.[A-Z_]+|counter-mask ROM|mask ROM'
echo "## draw.io sources: every value= label"
for f in docs/diagrams/src/*.drawio; do
  python3 - "$f" "$pat" <<'PY'
import re, sys, html
f, pat = sys.argv[1], sys.argv[2]
for n, line in enumerate(open(f, encoding="utf-8"), 1):
    for v in re.findall(r'value="([^"]*)"', line):
        t = re.sub(r"<[^>]+>", " ", html.unescape(html.unescape(v))).replace("\n", " ")
        t = " ".join(t.split())
        if re.search(pat, t, re.I) or re.search(r"counter", t, re.I):
            print(f"{f}:{n}: {t}")
PY
done
echo "## every committed SVG/PNG-adjacent SVG (draw.io exports, hand-authored, wavedrom): text content"
for f in docs/diagrams/*.svg docs/diagrams/wavedrom/*.svg; do
  # every text line naming a counter is listed too, for reading by eye
  # strip tags to the visible text, then search
  python3 - "$f" "$pat" <<'PY'
import re, sys, html
f, pat = sys.argv[1], sys.argv[2]
s = open(f, encoding="utf-8").read()
s = re.sub(r"<[^>]+>", "\n", s)
for line in s.splitlines():
    t = html.unescape(line).strip()
    if t and (re.search(pat, t, re.I) or re.search(r"\bcounters?\b|subsystem|banks?\b", t, re.I)):
        print(f"{f}: {t}")
PY
done
echo "## mermaid fences in docs"
python3 - "$pat" <<'PY'
import re, sys, pathlib
pat = sys.argv[1]
for p in sorted(pathlib.Path("docs").rglob("*.md")):
    inside = False
    for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip().startswith("```mermaid"):
            inside = True; continue
        if inside and line.strip().startswith("```"):
            inside = False; continue
        if inside and re.search(pat, line, re.I):
            print(f"{p}:{n}: {line.strip()}")
PY
echo "## end"
