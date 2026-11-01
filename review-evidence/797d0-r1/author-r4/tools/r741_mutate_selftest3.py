#!/usr/bin/env python3
"""Apply single mutants to the cross-page search in scripts/docs_inventory.py and run --selftest on each, 16 at a time.
Usage: python3 -I mutate_selftest3.py GENERATOR WORKDIR. KILLED = --selftest rc != 0."""
import subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
gen, work = Path(sys.argv[1]).read_text(encoding="utf-8"), Path(sys.argv[2])
M = [
 ("search-disabled", "for finding in findings + copies(findings, texts):", "for finding in findings:"),
 ("no-line-markers", 'LINE_MARKER_RE.sub("", unicodedata.normalize("NFKC", text))', 'unicodedata.normalize("NFKC", text)'),
 ("no-inline-markup", 'INLINE_MARKUP_RE.sub("", LINE_MARKER_RE.sub("", unicodedata.normalize("NFKC", text)))', 'LINE_MARKER_RE.sub("", unicodedata.normalize("NFKC", text))'),
 ("no-nfkc", 'unicodedata.normalize("NFKC", text)', 'text'),
 ("no-casefold", '" ".join(plain.split()).casefold()', '" ".join(plain.split())'),
 ("no-whitespace-collapse", '" ".join(plain.split()).casefold()', 'plain.strip().casefold()'),
 ("no-left-boundary", 'left = r"(?<!\\w)" if needle[:1].isalnum() else ""', 'left = ""'),
 ("no-right-boundary", 'right = r"(?!\\w)" if needle[-1:].isalnum() else ""', 'right = ""'),
 ("line-off-by-one", 'bisect_right(flat[1], match.start())', 'bisect_right(flat[1], match.start()) + 1'),
 ("drop-also", 'for statement in (finding.quote, *finding.also):', 'for statement in (finding.quote,):'),
 ("drop-quote", 'for statement in (finding.quote, *finding.also):', 'for statement in finding.also:'),
 ("no-held-check", 'if any(needle in words or words in needle for words in held.get(path, [])):', 'if False:'),
 ("held-one-way-a", 'if any(needle in words or words in needle for words in held.get(path, [])):', 'if any(words in needle for words in held.get(path, [])):'),
 ("held-one-way-b", 'if any(needle in words or words in needle for words in held.get(path, [])):', 'if any(needle in words for words in held.get(path, [])):'),
 ("rows-not-updated", '                rows.add((finding.ident, path))\n', ''),
 ("held-not-updated", '                held.setdefault(path, []).append(needle)\n', ''),
 ("recording-page-searched", 'if (finding.ident, path) in rows or carried_line(flat, statement) is None:', 'if carried_line(flat, statement) is None:'),
 ("copy-loses-origin", 'origin=finding.page))', '))'),
 ("copy-rows-use-exact-locate", 'carried_line(flatten(text), f.quote) if f.origin else locate(text, f.quote)', 'locate(text, f.quote)'),
 ("origin-rows-use-search", 'carried_line(flatten(text), f.quote) if f.origin else locate(text, f.quote)', 'carried_line(flatten(text), f.quote)'),
 ("source-loses-copy-text", 'return f"Copy of the {finding.ident} statement on `{finding.origin}`. {finding.source}"', 'return finding.source'),
 ("audit-page-searched", 'texts = {path: "\\n".join(OWN_HEAD) if path == OUTPUT\n             else (tree.root / path).read_text(encoding="utf-8", errors="replace") for path in paths}', 'texts = {path: (tree.root / path).read_text(encoding="utf-8", errors="replace") if (tree.root / path).exists() else "" for path in paths}'),
 ("also-not-validated", 'if not isinstance(also, list) or not all(isinstance(value, str) and value.strip() for value in also):', 'if False:'),
 ("also-empty-allowed", 'isinstance(value, str) and value.strip() for value in also', 'isinstance(value, str) for value in also'),
 ("blank-line-not-a-break", 'flat += normal_form(line) + " "', 'flat += (normal_form(line) + " ") if line.strip() else ""'),
 ("cited-at-dropped", 'f"Findings cite source lines at dev `{cited_at}` and its submodule pins."', '"Findings cite source lines."'),
 ("copies-only-at-recording-order", 'needle = normal_form(statement)\n            for path, flat in flats.items():', 'needle = normal_form(statement)\n            for path, flat in list(flats.items())[:-1]:'),
]
def one(m):
    name, a, b = m
    if a not in gen:
        return name, "NOT-APPLICABLE"
    d = work / name / "scripts"; d.mkdir(parents=True, exist_ok=True)
    (d / "docs_inventory.py").write_text(gen.replace(a, b, 1), encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", str(d / "docs_inventory.py"), "--selftest"], capture_output=True, text=True, timeout=500)
    tail = (r.stdout + r.stderr).strip().split("\n")[0][:150]
    return name, ("KILLED" if r.returncode else "SURVIVED") + f" rc={r.returncode} {tail}"
with ThreadPoolExecutor(16) as p:
    for name, verdict in p.map(one, M):
        print(f"{name}\t{verdict}")
