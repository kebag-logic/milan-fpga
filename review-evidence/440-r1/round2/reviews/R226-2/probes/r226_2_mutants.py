#!/usr/bin/env python3
"""R226-2 mutation sensitivity on disposable copies of one tree's scripts/.

Usage: python3 -B r226_2_mutants.py <tree-root> <r226-1-probes-dir> <outdir> [set]

set: "all" (default) = the public R226-1 mutants (R00-R27, X01-X04) plus the
R226-2 closer-only widening variants (W*) and residual-name probes (Z*);
"closer" = R15, R16, X04 and the W*/Z*/X01* closer-name mutants only.

Each mutant is applied to a fresh temporary copy of <tree-root>/scripts (never
to a tracked file); each textual edit must match exactly once. Both
self-tests run with `python3 -B`; exit status and EVERY failing line (FAIL /
GUARD / "- [" problem lines) are kept, plus the arm names they cite. The
input tree digest is checked before and after.
"""
import difflib
import hashlib
import json
import re
import runpy
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SRC = Path(sys.argv[1]).resolve() / "scripts"
R1 = Path(sys.argv[2]).resolve()
OUT = Path(sys.argv[3]).resolve()
WHICH = sys.argv[4] if len(sys.argv) > 4 else "all"
OUT.mkdir(parents=True, exist_ok=True)

lib = runpy.run_path(str(R1 / "r226_mutants.py"), run_name="r226_mutants_lib")
T, E, CLOSE = lib["T"], lib["E"], lib["CLOSE"]
R1_MUTANTS = list(lib["MUTANTS"])
# X01-X04 exactly as the public r226_mutants_extra.py spells them
X_MUTANTS = [
    ("X01-raw-html-tags-plus-title-both-sites",
     [(T, 'RAW_HTML_TAGS = ("pre", "script", "style", "textarea")',
          'RAW_HTML_TAGS = ("pre", "script", "style", "textarea", "title")')]),
    ("X02-closer-any-ascii-tag-name", [(T, CLOSE, 'return bool(re.search(r"</[a-z]+>", line, ASCII_FOLD))')]),
    ("X03-length-strictly-longer", [(T, lib["LEN"], "len(m.group(1)) > len(delim)")]),
    ("X04-closer-add-xmp", [(T, CLOSE, CLOSE.replace('"|".join(RAW_HTML_TAGS)', '"|".join(RAW_HTML_TAGS + ("xmp",))'))]),
]

STILL = '        return (TEXT if _type_1_end(line) else HTML), "", tag'
OPENS = "        closed = _type_1_end(line)"


def closer_add(name: str) -> list:
    return [(T, CLOSE, CLOSE.replace('"|".join(RAW_HTML_TAGS)', f'"|".join(RAW_HTML_TAGS + ("{name}",))'))]


W_MUTANTS = []
for name in ("div", "title", "xmp"):
    W_MUTANTS += [
        (f"W-{name}-later-line-site-only",
         [(T, STILL, f'        return (TEXT if _type_1_end(line) or re.search(r"</{name}>", line, ASCII_FOLD) else HTML), "", tag')]),
        (f"W-{name}-opening-line-site-only",
         [(T, OPENS, f'        closed = _type_1_end(line) or bool(re.search(r"</{name}>", line, ASCII_FOLD))')]),
        (f"W-{name}-literal-alternation-no-RAW_HTML_TAGS",
         [(T, CLOSE, f'return bool(re.search(r"</(?:pre|script|style|textarea|{name})>", line, ASCII_FOLD))')]),
        (f"X01-{name}-raw-html-tags-plus-{name}-both-sites",
         [(T, 'RAW_HTML_TAGS = ("pre", "script", "style", "textarea")',
              f'RAW_HTML_TAGS = ("pre", "script", "style", "textarea", "{name}")')]),
    ]
Z_MUTANTS = [(f"Z-closer-add-{name}", closer_add(name))
             for name in ("iframe", "noscript", "plaintext", "noembed", "noframes",
                          "listing", "p", "span", "code", "pre2", "b")]

if WHICH == "closer":
    keep = {"R15-closer-add-div", "R16-closer-add-title"}
    MUTANTS = [m for m in R1_MUTANTS if m[0] in keep] + [X_MUTANTS[3]] + W_MUTANTS + Z_MUTANTS
else:
    MUTANTS = R1_MUTANTS + X_MUTANTS + W_MUTANTS + Z_MUTANTS

ARM = re.compile(r"\[(I440[^\]]*|[^\]]+)\]")


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
        with tempfile.TemporaryDirectory(prefix="r226-2.mut.") as tmp:
            dst = Path(tmp) / "scripts"
            shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__"))
            texts, patch = {}, []
            for fname, old, new in edits:
                texts.setdefault(fname, (dst / fname).read_text())
                assert texts[fname].count(old) == 1, (mid, fname, old, texts[fname].count(old))
                texts[fname] = texts[fname].replace(old, new)
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
                (OUT / f"{mid}.{script}.log").write_text(log + f"\nexit={res.returncode}\n")
                fails = [l.strip() for l in log.splitlines()
                         if l.strip().startswith(("FAIL [", "GUARD ", "- ["))]
                names = []
                for l in fails:
                    m = ARM.search(l)
                    names.append(m.group(1) if m else l[:100])
                summary = [l for l in log.splitlines() if "selftest" in l or "FATAL" in l]
                rec["runs"][script] = {"exit": res.returncode, "failing": len(fails),
                                       "I440_failing": sum("I440" in n for n in names),
                                       "non_I440_failing": sum("I440" not in n for n in names),
                                       "failing_names": names, "summary": summary[-2:]}
            records.append(rec)
            print(mid, {s: (r["exit"], r["I440_failing"], r["non_I440_failing"])
                        for s, r in rec["runs"].items()}, flush=True)
    after = tree_digest(SRC)
    (OUT / "results.json").write_text(json.dumps({
        "tree": str(SRC.parent), "set": WHICH,
        "input_scripts_sha256_before": before, "input_scripts_sha256_after": after,
        "mutants": records}, indent=1, ensure_ascii=True) + "\n")
    with open(OUT / "summary.tsv", "w") as fh:
        fh.write("mutant\tgen_toc_exit\tgen_toc_I440_fail\tgen_toc_other_fail\t"
                 "em_dash_exit\tem_dash_I440_fail\tem_dash_other_fail\n")
        for r in records:
            g, e = r["runs"][T], r["runs"][E]
            fh.write(f"{r['id']}\t{g['exit']}\t{g['I440_failing']}\t{g['non_I440_failing']}\t"
                     f"{e['exit']}\t{e['I440_failing']}\t{e['non_I440_failing']}\n")
    assert before == after, "input tree changed"
    print("input scripts unchanged:", before)


if __name__ == "__main__":
    main()
