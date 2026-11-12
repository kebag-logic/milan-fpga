"""Per-build executable lines of one source in kept gcov data, and the lines only some builds instrument.
Usage: python3 -I gcov_lines.py <keep dir> <source suffix> <gcda basename>"""
import gzip, json, subprocess, sys
from pathlib import Path
keep, suffix, base = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
per = {}
for gcda in sorted(keep.rglob(base)):
    out = subprocess.run(["gcov", "--json-format", "--stdout", str(gcda)], capture_output=True, cwd=gcda.parent)
    lines = set()
    for chunk in out.stdout.decode().splitlines():
        if not chunk.strip():
            continue
        for f in json.loads(chunk)["files"]:
            if f["file"].endswith(suffix):
                lines |= {l["line_number"] for l in f["lines"]}
    per[str(gcda.parent.relative_to(keep))] = lines
union = set().union(*per.values())
print(f"union {len(union)} lines over {len(per)} builds")
for name, lines in per.items():
    print(f"  {len(lines):4d}  {name}")
for ln in sorted(union):
    have = [n for n, l in per.items() if ln in l]
    if len(have) < len(per):
        print(f"line {ln}: instrumented in {len(have)} of {len(per)}: {', '.join(have) if len(have) <= 4 else '(many)'}")
