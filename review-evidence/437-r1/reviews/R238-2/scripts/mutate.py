#!/usr/bin/env python3
"""Reviewer-designed source mutations of the #437 walk, each applied to a
disposable copy of the head's scripts/ and scored by BOTH shipped self-tests.

Usage: mutate.py <head-scripts-root> <scratch-dir> <out.json> [jobs]
A mutation is (id, file, exact old text, new text); the old text must occur
exactly once. The shipped bytes are never touched: every copy is under
<scratch-dir>/mut/<id>/.
"""
import concurrent.futures
import json
import os
import shutil
import subprocess
import sys

MUTATIONS = [
    ("C01 quote never consumes its optional space", "gen_toc_containers.py",
     'return at + 1 if text[at:at + 1] == " " else at', "return at"),
    ("C02 blank line continues an empty item", "gen_toc_containers.py",
     "return len(text) if box.filled and _blank(rest) else None",
     "return len(text) if _blank(rest) else None"),
    ("C03 whitespace-only line continues a footnote", "gen_toc_containers.py",
     "return at if not text else None", "return at if _blank(text) else None"),
    ("C04 footnote continues at two columns", "gen_toc_containers.py",
     "    if lead >= TAB_STOP:\n        return at + TAB_STOP", "    if lead >= 2:\n        return at + 2"),
    ("C05 indented line is never lazy", "gen_toc_containers.py",
     "    if _lead(rem) >= TAB_STOP:\n        return True", "    if _lead(rem) >= TAB_STOP:\n        return False"),
    ("C06 type 3-5 opener is lazy", "gen_toc_containers.py",
     "LIST_ITEM_RE, RAW_3_5_RE)", "LIST_ITEM_RE)"),
    ("C07 footnote opener is lazy", "gen_toc_containers.py",
     "    starts = (ATX_HEADING_RE, THEMATIC_BREAK_RE, BLOCK_QUOTE_RE,\n              FOOTNOTE_DEFINITION_RE, ",
     "    starts = (ATX_HEADING_RE, THEMATIC_BREAK_RE, BLOCK_QUOTE_RE,\n              "),
    ("C08 four columns of padding make code", "gen_toc_containers.py",
     "or padding > TAB_STOP else", "or padding >= TAB_STOP else"),
    ("C09 empty item keeps its padding", "gen_toc_containers.py",
     "return end + 1 if not item.group(2) or padding > TAB_STOP",
     "return end + 1 if padding > TAB_STOP"),
    ("C10 any item interrupts a paragraph", "gen_toc_containers.py",
     "interrupting = para == PARAGRAPH and not opened", "interrupting = False"),
    ("C11 any ordinal interrupts a paragraph", "gen_toc_containers.py",
     "item.group(2) and int(item.group(1) or 1) == 1)):", "item.group(2))):"),
    ("C12 no lazy continuation", "gen_toc_containers.py",
     "if state == TEXT and para == PARAGRAPH and _lazy(rem):", "if False:"),
    ("C13 footnote content read in place", "gen_toc_containers.py",
     "noted = any(box.kind == NOTE for box in walk.stack)", "noted = False"),
    ("C14 indented comment opener starts a block", "gen_toc_containers.py",
     "if state == COMMENT and (label == TEXT or _lead(rem) > 3):",
     "if state == COMMENT and label == TEXT:"),
    ("C15 types 3-5 not raw", "gen_toc_containers.py",
     "raw = RAW_3_5_RE.match(rem) if (label, state) == (TEXT, TEXT) else None", "raw = None"),
    ("C16 tabs expand to eight", "gen_toc_containers.py",
     "text = line.expandtabs(TAB_STOP)", "text = line.expandtabs(8)"),
    ("C17 types 3-5 never end", "gen_toc_containers.py",
     'state, tag = (TEXT, "") if tag in rem else (HTML, tag)', "state, tag = HTML, tag"),
    ("C18 blank line never continues an item", "gen_toc_containers.py",
     "return len(text) if box.filled and _blank(rest) else None", "return None"),
    ("H01 only --> closes", "gen_toc_html.py",
     'HTML_COMMENT_END_RE = re.compile(r"--!?>")', 'HTML_COMMENT_END_RE = re.compile(r"-->")'),
    ("H02 no abrupt empty comment", "gen_toc_html.py",
     'HTML_ABRUPT_END_RE = re.compile(r"-?>")', 'HTML_ABRUPT_END_RE = re.compile(r"(?!)")'),
    ("H03 tag filter ignored", "gen_toc_html.py",
     "        elif HTML_FILTERED_RE.match(raw, mark.start()):\n            at = mark.start() + 1\n", ""),
    ("H04 quoted attribute value not skipped", "gen_toc_html.py",
     r'''r"(?:\"[^\"]*(?:\"|\Z)|'[^']*(?:'|\Z)|(?:(?!%(s)s)[^>])*))?)*(?:>|\Z)"''',
     r'''r"(?:(?:(?!%(s)s)[^>])*))?)*(?:>|\Z)"'''),
    ("H05 declaration is no bogus comment", "gen_toc_html.py",
     r'r"(?P<comment><!--)|<!(?!--)[^>]*(?:>|\Z)|', r'r"(?P<comment><!--)|'),
    ("H06 processing instruction is no bogus comment", "gen_toc_html.py",
     r'|<\?[^>]*(?:>|\Z)"', '"'),
    ("H07 code span not skipped", "gen_toc_html.py",
     "            at = closer.end() if closer else at\n", ""),
    ("H08 escape not honoured", "gen_toc_html.py",
     r'r"\\%(esc)s|(?P<ticks>`+)', r'r"(?P<ticks>`+)'),
    ("H09 every line its own paragraph", "gen_toc_html.py",
     "if text and not (scope.text is not None and scope.cont):", "if text:"),
    ("H10 raw run read per line", "gen_toc_html.py",
     "if raw and scope.raw is None:", "if raw:"),
    ("H11 lowercase declaration is inline HTML", "gen_toc_html.py",
     '"decl": _cc("declaration name")', '"decl": _cc("tag name")'),
    ("H12 raw lines never hide", "gen_toc_html.py",
     "            raw.append(scope.raw)\n", "            pass\n"),
    ("B01 no container end for blocks", "gen_toc.py",
     "owner not in scope.held_by or (prose and not scope.plain)):", "(prose and not scope.plain)):"),
    ("B02 prose comment never ends early", "gen_toc.py",
     "owner not in scope.held_by or (prose and not scope.plain)):", "owner not in scope.held_by):"),
    ("B03 hidden lines not relabelled", "gen_toc.py",
     "out[-1] = COMMENT if hidden and out[-1] == TEXT else out[-1]", "pass"),
    ("B04 container gate ignored", "gen_toc.py",
     "label, state, delim, tag = _opens(line, para, state, scope.gate)",
     "label, state, delim, tag = _opens(line, para, state)"),
    ("B05 empty comment opens", "gen_toc.py",
     'scan, inside = scan[at + len("<!"):], True', "scan, inside = scan[at + len(COMMENT_OPEN):], True"),
]


def run(args):
    ident, name, old, new, root, scratch = args
    slug = ident.split()[0]
    where = os.path.join(scratch, "mut", slug)
    shutil.rmtree(where, ignore_errors=True)
    shutil.copytree(root, where)
    path = os.path.join(where, "scripts", name)
    text = open(path, encoding="utf-8").read()
    if text.count(old) != 1:
        return {"mutation": ident, "error": f"old text occurs {text.count(old)} times"}
    open(path, "w", encoding="utf-8").write(text.replace(old, new))
    env = dict(os.environ, TMPDIR=os.path.join(scratch, "tmp"))
    out = {"mutation": ident, "file": name}
    for label, script in (("toc", "gen_toc.py"), ("em_dash", "check_em_dash.py")):
        proc = subprocess.run([sys.executable, "-B", f"scripts/{script}", "--selftest"], cwd=where,
                              capture_output=True, text=True, env=env, timeout=900)
        lines = (proc.stdout + proc.stderr).splitlines()
        fails = [line for line in lines if "FAIL" in line or "expected" in line or "I437" in line]
        out[label] = {"exit": proc.returncode, "tail": lines[-1:] if lines else [],
                      "failing_lines": len(fails), "first": fails[:3]}
    shutil.rmtree(where, ignore_errors=True)
    return out


def main():
    root, scratch, out_path = sys.argv[1:4]
    jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    work = [(ident, name, old, new, root, scratch) for ident, name, old, new in MUTATIONS]
    with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
        results = list(pool.map(run, work))
    json.dump(results, open(out_path, "w"), indent=1)
    for r in results:
        if "error" in r:
            print(r["mutation"], "ERROR", r["error"])
        else:
            print(f"{r['mutation']}: toc={r['toc']['exit']} em_dash={r['em_dash']['exit']}")


if __name__ == "__main__":
    main()
