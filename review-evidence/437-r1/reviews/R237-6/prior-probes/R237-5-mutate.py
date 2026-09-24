#!/usr/bin/env python3
"""Disposable mutation probes of the head walk and renderer binding.

Usage: mutate.py <tree> <workdir> <python>

Each mutant is one exact string replacement in one file (the old string
must occur exactly once). The mutated copy lives under <workdir>/<name>;
`gen_toc.py --selftest` and `check_em_dash.py --selftest` are run there
with <python>, and the verdict is KILLED when either exits non-zero. The
first failing arm names are printed. The source tree is never modified.
"""
import shutil
import subprocess
import sys
from pathlib import Path

R, G = "scripts/gen_toc_renderer.py", "scripts/gen_toc.py"
MUTANTS = [
    ("M01 positions left quoted for the HTML parse", R,
     "    head, *rest = html.split(f' {POSITION}=\"')",
     "    return html\n    head, *rest = html.split(f' {POSITION}=\"')"),
    ("M02 position-attribute guard removed", R,
     "    if POSITION in text:\n        return Rendered((), ())",
     "    if False:\n        return Rendered((), ())"),
    ("M03 tight-list paragraphs given an element", R,
     "out += _nodes(bound, child, bare=holder == \"tight\")",
     "out += _nodes(bound, child, bare=False)"),
    ("M04 raw HTML / indented code extent from reported end line", G,
     "    if node.kind == \"html_block\" or (node.kind == \"code_block\"\n"
     "                                     and not node.fenced):",
     "    if False:"),
    ("M05 swallowed blocks not marked COMMENT", G,
     "        if node.element and node.position not in shown:",
     "        if False:"),
    ("M06 heading element tag not checked against level", G,
     "        if node is None or tag != f\"h{node.level}\":",
     "        if node is None:"),
    ("M07 ATX label from rendered text", G,
     "        if node.last == node.first:",
     "        if False:"),
    ("M08 html5lib release not checked", R,
     'PINNED = {"cmarkgfm": "2025.10.22", "html5lib": "1.1"}',
     'PINNED = {"cmarkgfm": "2025.10.22"}'),
    ("M09 tagfilter extension dropped", R,
     'EXTENSIONS = ("table", "strikethrough", "autolink", "tagfilter", "tasklist")',
     'EXTENSIONS = ("table", "strikethrough", "autolink", "tasklist")'),
    ("M10 table extension dropped", R,
     'EXTENSIONS = ("table", "strikethrough", "autolink", "tagfilter", "tasklist")',
     'EXTENSIONS = ("strikethrough", "autolink", "tagfilter", "tasklist")'),
    ("M11 footnotes option dropped", R,
     "lib.CMARK_OPT_SOURCEPOS | lib.CMARK_OPT_UNSAFE\n"
     "               | lib.CMARK_OPT_FOOTNOTES | lib.CMARK_OPT_GITHUB_PRE_LANG",
     "lib.CMARK_OPT_SOURCEPOS | lib.CMARK_OPT_UNSAFE\n"
     "               | lib.CMARK_OPT_GITHUB_PRE_LANG"),
    ("M12 comment block read as raw HTML", G,
     "\"html_block\": COMMENT if node.literal.lstrip(\" \").startswith(\n"
     "                     \"<!--\") else HTML}",
     "\"html_block\": HTML}"),
    ("M13 lone carriage return not a renderer line end", G,
     "        if char == \"\\n\" or (char == \"\\r\" and text[at + 1:at + 2] != \"\\n\"):",
     "        if char == \"\\n\":"),
    ("M14 bundled cmark-gfm release not checked", R,
     "    if core != CMARK_GFM:",
     "    if False:"),
    ("M15 table not an own-element block", R,
     "_OWN_ELEMENT = (\"block_quote\", \"list\", \"heading\", \"code_block\",\n"
     "                \"thematic_break\", \"table\")",
     "_OWN_ELEMENT = (\"block_quote\", \"list\", \"heading\", \"code_block\",\n"
     "                \"thematic_break\")"),
    ("M16 (candidate fix, expect SURVIVES) guard made case-insensitive", R,
     "    if POSITION in text:\n        return Rendered((), ())",
     "    if POSITION in text.lower():\n        return Rendered((), ())"),
    ("M17 unsafe option dropped (raw HTML omitted)", R,
     "lib.CMARK_OPT_SOURCEPOS | lib.CMARK_OPT_UNSAFE\n",
     "lib.CMARK_OPT_SOURCEPOS\n"),
]


def main() -> int:
    tree, work, py = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    env = {"PATH": "/usr/bin:/bin", "HOME": str(work), "TMPDIR": str(work),
           "PYTHONDONTWRITEBYTECODE": "1", "GIT_CONFIG_NOSYSTEM": "1",
           "GIT_AUTHOR_NAME": "m", "GIT_AUTHOR_EMAIL": "m@example.invalid",
           "GIT_COMMITTER_NAME": "m", "GIT_COMMITTER_EMAIL": "m@example.invalid"}
    for name, path, old, new in MUTANTS:
        copy = work / name.split()[0]
        if copy.exists():
            shutil.rmtree(copy)
        copy.mkdir(parents=True)
        for part in ("scripts", "tools"):
            shutil.copytree(tree / part, copy / part)
        src = (copy / path).read_text()
        if src.count(old) != 1:
            print(f"{name}: NOT APPLIED (old string occurs {src.count(old)} times)")
            continue
        (copy / path).write_text(src.replace(old, new))
        verdicts = []
        for script in ("scripts/gen_toc.py", "scripts/check_em_dash.py"):
            res = subprocess.run([py, script, "--selftest"], cwd=copy, env=env,
                                 capture_output=True, text=True, check=False)
            lines = (res.stdout + res.stderr).splitlines()
            fails = [l.strip() for l in lines if "FAIL [" in l or l.strip().startswith("- [")
                     or "GUARD" in l or "Traceback" in l or "Error" in l]
            tail = lines[-1] if lines else ""
            verdicts.append((script.split("/")[1], res.returncode, len(fails), fails[:3], tail))
        killed = any(rc != 0 for _, rc, _, _, _ in verdicts)
        print(f"{name}: {'KILLED' if killed else 'SURVIVES'}")
        for script, rc, n, fails, tail in verdicts:
            print(f"    {script} rc={rc} failing-lines={n} :: {tail[:120]}")
            for f in fails:
                print(f"        {f[:160]}")
        shutil.rmtree(copy)
    return 0


if __name__ == "__main__":
    sys.exit(main())
