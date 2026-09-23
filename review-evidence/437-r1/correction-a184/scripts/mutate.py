#!/usr/bin/env python3
"""Named mutations: each removes one property; both selftests must fail at
the arms that hold it. Runs in scratch copies of the lane's scripts/ only.

Usage: mutate.py OUT.json
Each mutation is (name, file, old, new, expected arm names). `old` must occur
exactly once. The unmodified copy must pass both selftests first. At most
four mutants run at once.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

LANE = Path("$LANES/437-container-paragraph-scopes")
G, C, F1, FC = ("gen_toc.py", "gen_toc_container_cases.py",
                "gen_toc_family_one.json", "gen_toc_comment_shapes.json")
UPDATE = "        if out[-1] in (HTML, COMMENT) or (out[-1] == TEXT and COMMENT_OPEN in line):\n"
ASSIGN = "            rendered_comment = _comment_after(line, rendered_comment)\n"
MUTATIONS = [
    # --- the rendered-comment flag (#516 shapes) ---
    ("comment-never-opens", G, ASSIGN,
     "            rendered_comment = rendered_comment and _comment_after(line, rendered_comment)\n",
     ["rendered #516 resumed tag column 0 open", "rendered type-6 block leaves comment open",
      "recorded #516 resumed tag column 0 open"]),
    ("raw-html-lines-ignored", G, UPDATE,
     "        if out[-1] == COMMENT or (out[-1] == TEXT and COMMENT_OPEN in line):\n",
     ["rendered #516 resumed tag column 1 attribute", "rendered type-1 pre leaves comment open",
      "recorded #516 first tag column 0 open"]),
    ("no-prose-relabel", G, "        out[-1], prev = COMMENT if hidden else out[-1], line\n",
     "        out[-1], prev = out[-1], line\n",
     ["rendered #516 resumed tag column 0 close", "rendered top-level tag leaves comment open",
      "recorded #516 resumed tag column 0 close"]),
    ("raw-lines-never-close", G, ASSIGN,
     "            rendered_comment = rendered_comment or _comment_after(line, False)\n",
     ["rendered closed by a later type-6 block", "rendered closed by a later type-7 block",
      "rendered closed by a later type-1 block", "rendered closed by a type-2 block",
      "recorded closed by a later type-6 block"]),
    ("escaped-arrow-closes", G, UPDATE,
     "        if out[-1] in (HTML, COMMENT) or COMMENT_OPEN in line or COMMENT_CLOSE in line:\n",
     ["rendered prose arrow closes nothing", "rendered heading arrow closes nothing",
      "rendered code span arrow closes nothing", "rendered fenced arrow closes nothing",
      "rendered indented arrow closes nothing", "recorded prose arrow closes nothing"]),
    ("prose-comment-ignored", G, UPDATE, "        if out[-1] in (HTML, COMMENT):\n",
     ["rendered closed by an inline comment", "rendered closed by a comment in a heading",
      "recorded closed by an inline comment"]),
    ("code-opener-counts", G, UPDATE,
     "        if out[-1] in (HTML, COMMENT) or COMMENT_OPEN in line:\n",
     ["rendered fenced opener opens nothing", "rendered indented opener opens nothing",
      "recorded fenced opener opens nothing"]),
    ("abrupt-comment-not-empty", G, '            scan, inside = scan[at + len("<!"):], True\n',
     "            scan, inside = scan[at + len(COMMENT_OPEN):], True\n",
     ["rendered abrupt empty comment in a block", "rendered abrupt dash comment in a block",
      "rendered abrupt empty comment line", "rendered abrupt empty comment inline",
      "recorded abrupt empty comment in a block"]),
    # --- family one, against the recorded shape set ---
    ("item-context-dropped", G,
     "        para, item_context = _list_paragraph_after(line, out[-1], para, prev, item_context)\n",
     "        para, _ = _list_paragraph_after(line, out[-1], para, prev, item_context)\n",
     ["rendered bullet at column, inline tag outside", "rendered star at column, unknown tag outside",
      "rendered bullet at column, b tag outside", "recorded bullet at column, inline tag outside"]),
    ("tag-inside-opens", G, "                opening_para = PARAGRAPH\n", "                opening_para = HELD\n",
     ["rendered bullet at column, inline tag inside", "rendered ordered at column, unknown tag inside",
      "recorded star past column, unknown tag inside"]),
    ("content-column-fixed-at-two", G, "        column = len(prefix.expandtabs(4))\n", "        column = 2\n",
     ["rendered two-digit ordered below column, inline tag outside",
      "rendered two-digit ordered below column, unknown tag outside",
      "recorded two-digit ordered below column, inline tag outside"]),
    ("content-column-fixed-at-three", G, "        column = len(prefix.expandtabs(4))\n", "        column = 3\n",
     ["rendered two-digit ordered below column, inline tag outside",
      "rendered two-digit ordered below column, unknown tag outside",
      "rendered bullet at column, unknown tag outside"]),
    ("blank-forgets-item", G, "        return after, None if context and context[1] else context\n",
     "        return after, None\n",
     ["rendered bullet at column, inline tag outside", "rendered bullet after two blanks, inline tag outside",
      "rendered ordered at column, unknown tag outside", "recorded task at column, inline tag outside"]),
    # --- the recorded receipts themselves ---
    ("response-byte-altered", F1, None, None, None),
    ("recorded-headings-altered", FC, None, None, None),
    ("page-without-request", F1, None, None, None),
]


def failing(text: str) -> list[str]:
    names = re.findall(r"FAIL \[(?:I437 )?([^\]]*)\]", text)
    names += re.findall(r"\[I437 ([^\]]*)\] expected findings", text)
    names += re.findall(r"\[I437 ([^\]]*)\] absent base heading", text)
    return names


def run(tmp: Path) -> dict:
    out = {}
    for tool, args in (("toc", ["gen_toc.py", "--selftest"]), ("emdash", ["check_em_dash.py", "--selftest"])):
        p = subprocess.run([sys.executable, "-B", *args], cwd=tmp / "scripts", capture_output=True, text=True)
        out[tool] = {"exit": p.returncode, "failing": failing(p.stdout + p.stderr),
                     "tail": (p.stdout + p.stderr).strip().splitlines()[-1:]}
    return out


def mutate(spec: tuple) -> dict:
    name, fname, old, new, expected = spec
    with tempfile.TemporaryDirectory(prefix=f"a184.mut.{name}.") as d:
        tmp = Path(d)
        shutil.copytree(LANE / "scripts", tmp / "scripts")
        path = tmp / "scripts" / fname
        src = path.read_text()
        if name == "response-byte-altered":
            doc = json.loads(src)
            shape = next(s for s in doc["shapes"] if s["name"] == "ordered at column, inline tag outside")
            shape["response_bytes"] = shape["response_bytes"].replace(">Real<", ">Reel<")
            expected = ["receipt ordered at column, inline tag outside"]
            new_src = json.dumps(doc, indent=1, sort_keys=True) + "\n"
        elif name == "recorded-headings-altered":
            doc = json.loads(src)
            shape = next(s for s in doc["shapes"] if s["name"] == "closed by an inline comment")
            shape["headings"] = [[2, "Real"]]
            expected = ["receipt closed by an inline comment", "rendered closed by an inline comment",
                        "recorded closed by an inline comment"]
            new_src = json.dumps(doc, indent=1, sort_keys=True) + "\n"
        elif name == "page-without-request":
            doc = json.loads(src)
            shape = next(s for s in doc["shapes"] if s["name"] == "bullet at column, inline tag outside")
            shape["page"] = shape["page"].replace("  text", "   text")
            expected = ["receipt bullet at column, inline tag outside"]
            new_src = json.dumps(doc, indent=1, sort_keys=True) + "\n"
        else:
            if src.count(old) != 1:
                return {"name": name, "error": f"old text occurs {src.count(old)} times"}
            new_src = src.replace(old, new)
            if expected is None:
                shape = json.loads(new_src)["shapes"][0]["name"]
                expected = [f"receipt {shape}"]
        path.write_text(new_src)
        res = run(tmp)
    all_failing = set(res["toc"]["failing"]) | set(res["emdash"]["failing"])
    missing = [e for e in expected if e not in all_failing]
    return {"name": name, "file": fname, "old": old, "new": new, "expected": expected,
            "missing_expected": missing, **res,
            "killed": res["toc"]["exit"] != 0 and not missing}


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="a184.mut.clean.") as d:
        shutil.copytree(LANE / "scripts", Path(d) / "scripts")
        clean = run(Path(d))
    print("clean copy:", clean["toc"]["tail"], clean["emdash"]["tail"])
    assert clean["toc"]["exit"] == 0 and clean["emdash"]["exit"] == 0
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(mutate, MUTATIONS))
    for r in results:
        if "error" in r:
            print("ERROR", r["name"], r["error"])
            continue
        print(f"{r['name']:30s} killed={r['killed']} toc_exit={r['toc']['exit']} "
              f"emdash_exit={r['emdash']['exit']} toc_fail={len(r['toc']['failing'])} "
              f"emdash_fail={len(r['emdash']['failing'])} missing={r['missing_expected']}")
    Path(sys.argv[1]).write_text(json.dumps({"clean": clean, "mutations": results}, indent=1) + "\n")
    return 0 if all(r.get("killed") for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
