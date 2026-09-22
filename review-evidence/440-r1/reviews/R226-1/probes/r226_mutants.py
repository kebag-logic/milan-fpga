"""R226 independent mutation sensitivity on disposable copies of the head scripts.

Usage: python3 -B r226_mutants.py HEAD_SCRIPTS_DIR OUTDIR

Each mutant is applied to a fresh temporary copy of the head `scripts/` tree
(never to a tracked file). Both self-tests are run; every FAIL/GUARD line
and exit status is kept. Source SHA-256 of the input tree is checked before
and after, so the input tree is proven untouched.
"""
import difflib
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SRC = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
OUT.mkdir(parents=True, exist_ok=True)

TRAILER = 'and not m.group(2).strip(CLASSES["blank"]):  # CommonMark 4.5 trailer'
CLOSE = 'return bool(re.search(r"</(?:%s)>" % "|".join(RAW_HTML_TAGS), line, ASCII_FOLD))'
LEN = "len(m.group(1)) >= len(delim)"
SAME = 'm.group(1)[0] == delim[0] and '
TYPE6 = 'return (TEXT if not line.strip(CLASSES["blank"])\n                    else HTML), "", tag'
FENCE_TAIL = '        return TEXT, "", ""\n    return FENCE, delim, ""'
GIT_TEXT = ('out = subprocess.run(["git", "-C", str(repo), *args],\n'
            '                             capture_output=True, text=True,\n'
            '                             encoding="utf-8", errors="replace", env=env)')
GIT_BYTES = ('out = subprocess.run(["git", "-C", str(repo), *args],\n'
             '                             capture_output=True, env=env)\n'
             '        out = subprocess.CompletedProcess(out.args, out.returncode,\n'
             '            out.stdout.decode("utf-8", "replace"), out.stderr.decode("utf-8", "replace"))')

T = "gen_toc.py"
E = "check_em_dash.py"
MUTANTS = [
    # --- the combined pre-#440 semantics at both sites (revert of the fix)
    ("R00-base-semantics-both-sites", [
        (T, TRAILER, 'and not m.group(2).strip():'),
        (T, "def _type_1_end(line: str) -> bool:", "def _type_1_end(line: str, tag: str) -> bool:"),
        (T, CLOSE, 'return bool(re.search(r"</%s\\s*>" % tag, line, ASCII_FOLD))'),
        (T, "(TEXT if _type_1_end(line) else HTML)", "(TEXT if _type_1_end(line, tag) else HTML)"),
        (T, "closed = _type_1_end(line)", "closed = _type_1_end(line, tag)")]),
    # --- fence trailer site
    ("R01-trailer-plus-ff", [(T, TRAILER, 'and not m.group(2).strip(CLASSES["blank"] + "\\f"):')]),
    ("R02-trailer-plus-nbsp", [(T, TRAILER, 'and not m.group(2).strip(CLASSES["blank"] + "\\xa0"):')]),
    ("R03a-trailer-plus-zwsp-inline", [(T, TRAILER, 'and not m.group(2).strip(CLASSES["blank"] + "\\u200b"):')]),
    ("R03b-blank-class-body-plus-zwsp", [(T, '_BLANK = " \\t"', '_BLANK = " \\t\\u200b"')]),
    ("R04-trailer-python-rstrip", [(T, TRAILER, 'and not m.group(2).rstrip():')]),
    ("R05-trailer-first-char-only", [(T, TRAILER, 'and not m.group(2)[:1].strip(CLASSES["blank"]):')]),
    ("R06-trailer-space-only", [(T, TRAILER, 'and not m.group(2).strip(CLASSES["indent"]):')]),
    ("R07-trailer-ignored", [(T, TRAILER, 'and True:')]),
    ("R08-length-exact-only", [(T, LEN, "len(m.group(1)) == len(delim)")]),
    ("R09-length-ignored", [(T, LEN, "True")]),
    ("R10-fence-char-ignored", [(T, SAME, "")]),
    ("R11-fence-ended-by-type1-closer", [
        (T, FENCE_TAIL, '        return TEXT, "", ""\n    if _type_1_end(line):\n'
                        '        return TEXT, "", ""\n    return FENCE, delim, ""')]),
    # --- type-1 closer site
    ("R12-closer-word-boundary", [(T, CLOSE, CLOSE.replace(')>"', ')\\b"'))]),
    ("R13-closer-attributes", [(T, CLOSE, CLOSE.replace(')>"', ')[^>]*>"'))]),
    ("R14-closer-drop-textarea", [(T, CLOSE, CLOSE.replace('"|".join(RAW_HTML_TAGS)', '"|".join(RAW_HTML_TAGS[:3])'))]),
    ("R15-closer-add-div", [(T, CLOSE, CLOSE.replace('"|".join(RAW_HTML_TAGS)', '"|".join(RAW_HTML_TAGS + ("div",))'))]),
    ("R16-closer-add-title", [(T, CLOSE, CLOSE.replace('"|".join(RAW_HTML_TAGS)', '"|".join(RAW_HTML_TAGS + ("title",))'))]),
    ("R17-closer-end-of-line", [(T, CLOSE, CLOSE.replace(')>"', ')>$"'))]),
    ("R18-closer-lower-or-upper-only", [(T, CLOSE,
        'return bool(re.search(r"</(?:%s|%s)>" % ("|".join(RAW_HTML_TAGS), "|".join(RAW_HTML_TAGS).upper()), line))')]),
    ("R19-closer-ascii-case-sensitive", [(T, CLOSE, CLOSE.replace("ASCII_FOLD", "re.ASCII"))]),
    ("R20-closer-unicode-fold", [(T, CLOSE, CLOSE.replace("ASCII_FOLD", "re.IGNORECASE"))]),
    ("R21-closer-optional-slash", [(T, CLOSE, CLOSE.replace('r"</', 'r"</?'))]),
    ("R22-type6-ended-by-type1-closer", [
        (T, TYPE6, 'return (TEXT if not line.strip(CLASSES["blank"]) or _type_1_end(line)\n'
                   '                    else HTML), "", tag')]),
    ("R23-closer-requires-opener-name-prefix", [(T, CLOSE,
        'return bool(re.search(r"</(?:%s)>" % "|".join(RAW_HTML_TAGS), line, ASCII_FOLD)) and "</p" in line.lower()')]),
    # --- shipped readers and refusal
    ("R24-gate-git-reader-no-newline-translation", [(E, GIT_TEXT, GIT_BYTES)]),
    ("R25-generator-reader-no-newline-translation", [(T, "        text = md.read_text()\n        rel = md.relative_to(REPO)",
        '        text = md.read_bytes().decode("utf-8")\n        rel = md.relative_to(REPO)')]),
    ("R26-base-side-refusal-dropped", [(E, "    notes = [f\"{note}, so no Contents label copied from it is exempt\"\n"
                                          "             for note in refusal_notes(change.base_path, text)]",
                                       "    notes = []")]),
    ("R27-refused-drops-cr", [(T, 'REFUSED = ("\\v\\f\\r\\x1c', 'REFUSED = ("\\v\\f\\x1c')]),
]


def tree_digest(root: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(root.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts:
            h.update(str(p.relative_to(root)).encode() + b"\0" + p.read_bytes() + b"\0")
    return h.hexdigest()


def main() -> None:
    before = tree_digest(SRC)
    records = []
    for mid, edits in MUTANTS:
        with tempfile.TemporaryDirectory(prefix="r226.mut.") as tmp:
            dst = Path(tmp) / "scripts"
            shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__"))
            patch = []
            texts = {}
            for fname, old, new in edits:
                texts.setdefault(fname, (dst / fname).read_text())
                cur = texts[fname]
                assert cur.count(old) == 1, (mid, fname, old, cur.count(old))
                texts[fname] = cur.replace(old, new)
            for fname, text in texts.items():
                orig = (SRC / fname).read_text()
                (dst / fname).write_text(text)
                patch += difflib.unified_diff(orig.splitlines(True), text.splitlines(True),
                                              f"a/scripts/{fname}", f"b/scripts/{fname}")
            (OUT / f"{mid}.patch").write_text("".join(patch))
            rec = {"id": mid, "runs": {}}
            for script in (T, E):
                res = subprocess.run([sys.executable, "-B", str(dst / script), "--selftest"],
                                     capture_output=True, text=True, cwd=tmp, timeout=900)
                log = res.stdout + res.stderr
                (OUT / f"{mid}.{script}.log").write_text(log)
                fails = [l.strip() for l in log.splitlines()
                         if l.strip().startswith(("FAIL [", "GUARD ", "- ["))]
                i440 = [l for l in fails if "I440" in l]
                summary = [l for l in log.splitlines() if "selftest" in l or "FATAL" in l]
                rec["runs"][script] = {"exit": res.returncode, "failing_lines": len(fails),
                                       "I440_failing": len(i440),
                                       "non_I440_failing": len(fails) - len(i440),
                                       "first_I440": i440[:3], "first_other": [l for l in fails if "I440" not in l][:3],
                                       "summary": summary[-2:]}
            records.append(rec)
            print(mid, {s: (r["exit"], r["I440_failing"], r["non_I440_failing"]) for s, r in rec["runs"].items()},
                  flush=True)
    after = tree_digest(SRC)
    (OUT / "results.json").write_text(json.dumps({"input_tree_sha256_before": before,
                                                  "input_tree_sha256_after": after,
                                                  "mutants": records}, indent=1) + "\n")
    assert before == after, "input tree changed"
    print("input tree unchanged:", before)


if __name__ == "__main__":
    main()
