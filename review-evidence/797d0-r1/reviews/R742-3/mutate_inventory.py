#!/usr/bin/env python3
"""Mutate a scratch copy of the inventory generator; each mutant must fail its own --selftest.

Usage: python3 -I mutate_inventory.py REPO SCRATCH_DIR
"""
import concurrent.futures as cf, re, subprocess, sys
from pathlib import Path
repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
src = (repo / "scripts/docs_inventory.py").read_text(encoding="utf-8")
M = {
 "search disabled": ("    for finding in findings + copies(findings, texts):", "    for finding in findings:"),
 "also not searched": ("for statement in (finding.quote, *finding.also):", "for statement in (finding.quote,):"),
 "quote not searched": ("for statement in (finding.quote, *finding.also):", "for statement in finding.also:"),
 "no left boundary": ('left = r"(?<!\\w)" if needle[:1].isalnum() else ""', 'left = ""'),
 "no right boundary": ('right = r"(?!\\w)" if needle[-1:].isalnum() else ""', 'right = ""'),
 "no casefold": ('return " ".join(plain.split()).casefold()', 'return " ".join(plain.split())'),
 "markup kept": ('plain = INLINE_MARKUP_RE.sub("", LINE_MARKER_RE.sub("", unicodedata.normalize("NFKC", text)))',
                 'plain = LINE_MARKER_RE.sub("", unicodedata.normalize("NFKC", text))'),
 "line markers kept": ('plain = INLINE_MARKUP_RE.sub("", LINE_MARKER_RE.sub("", unicodedata.normalize("NFKC", text)))',
                       'plain = INLINE_MARKUP_RE.sub("", unicodedata.normalize("NFKC", text))'),
 "quote marker only": (r'LINE_MARKER_RE = re.compile(r"^\s*(?:>\s*)*(?:[-*+]\s+|\d+\.\s+)?")', r'LINE_MARKER_RE = re.compile(r"^\s*(?:>\s*)*")'),
 "list marker only": (r'LINE_MARKER_RE = re.compile(r"^\s*(?:>\s*)*(?:[-*+]\s+|\d+\.\s+)?")', r'LINE_MARKER_RE = re.compile(r"^\s*(?:[-*+]\s+|\d+\.\s+)?")'),
 "ordered marker dropped": (r'(?:[-*+]\s+|\d+\.\s+)?")', r'(?:[-*+]\s+)?")'),
 "backtick kept": ('INLINE_MARKUP_RE = re.compile(r"[`*]")', 'INLINE_MARKUP_RE = re.compile(r"[*]")'),
 "star kept": ('INLINE_MARKUP_RE = re.compile(r"[`*]")', 'INLINE_MARKUP_RE = re.compile(r"[`]")'),
 "no NFKC": ('unicodedata.normalize("NFKC", text)', 'text'),
 "blank line joins": ('flat += normal_form(line) + " "', 'flat += normal_form(line) + (" " if line.strip() else "")'),
 "line off by one": ('return bisect_right(flat[1], match.start()) if match else None', 'return bisect_right(flat[1], match.start()) + 1 if match else None'),
 "held check removed": ('                if any(needle in words or words in needle for words in held.get(path, [])):\n                    continue\n', ''),
 "held one way a": ('needle in words or words in needle', 'needle in words'),
 "held one way b": ('needle in words or words in needle', 'words in needle'),
 "copies not held": ('                held.setdefault(path, []).append(needle)\n', ''),
 "second spelling second row": ('                rows.add((finding.ident, path))\n', ''),
 "archive skipped": ('for path, text in texts.items()}\n    held', 'for path, text in texts.items() if not path.startswith(ARCHIVE_PREFIX)}\n    held'),
 "root pages skipped": ('for path, text in texts.items()}\n    held', 'for path, text in texts.items() if "/" in path}\n    held'),
 "audit page searched": ('"\\n".join(OWN_HEAD) if path == OUTPUT\n             else (tree.root / path).read_text(encoding="utf-8", errors="replace")', '(tree.root / path).read_text(encoding="utf-8", errors="replace") if (tree.root / path).is_file() else ""'),
 "copy row loses origin": ('finding.source, finding.correction,\n                                     origin=finding.page))', 'finding.source, finding.correction))'),
 "origin not named": ('return f"Copy of the {finding.ident} statement on `{finding.origin}`. {finding.source}"', 'return finding.source'),
 "copy located by exact line": ('carried_line(flatten(text), f.quote) if f.origin else locate(text, f.quote)', 'locate(text, f.quote)'),
 "status rule off": ('if page_findings and state == "current":', 'if False:'),
 "status check off": ('    broken = current_with_findings(actual)\n', '    broken = []\n'),
 "also shape unchecked": ('if not isinstance(also, list) or not all(isinstance(value, str) and value.strip() for value in also):', 'if False:'),
}
def run(item):
    name, (old, new) = item
    if src.count(old) < 1:
        return name, "NOT APPLIED", ""
    d = scratch / re.sub(r"\W+", "_", name); d.mkdir(parents=True, exist_ok=True)
    (d / "docs_inventory.py").write_text(src.replace(old, new), encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", "-B", str(d / "docs_inventory.py"), "--selftest"], capture_output=True, text=True, timeout=500)
    return name, r.returncode, (r.stdout.strip().split("\n") or [""])[0][:120]
with cf.ThreadPoolExecutor(14) as ex:
    res = list(ex.map(run, M.items()))
for name, rc, line in res:
    print(f"{'KILLED  ' if rc == 1 else 'SURVIVED' if rc == 0 else 'OTHER   '} rc={rc} {name}: {line}")
print("killed", sum(r[1] == 1 for r in res), "survived", sum(r[1] == 0 for r in res), "other", sum(r[1] not in (0, 1) for r in res))
