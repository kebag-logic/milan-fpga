#!/usr/bin/env python3
"""[R238] bounded mutants of the head walk, each in a disposable worktree.

Each mutant is one exact edit of scripts/gen_toc.py (the old text must occur
exactly once) applied inside a fresh detached worktree of the SCRATCH clone
at the head commit; the tracked review checkout is never touched. Both
shipped self-tests run against the mutant and every failing arm or guard
they print is recorded, so a mutant caught only by a structural guard is
distinguishable from one caught by a behavioural I437 arm.
"""
import json
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent
CLONE = OUT / "scratch" / "clone-head"
WORK = OUT / "scratch" / "mutants"
HEAD = "65df1df50a80cd5f540a93d8f0cfabc97da3da75"

CALL = "para, item_context = _list_paragraph_after(line, out[-1], para, prev, item_context)"
BLANK_RET = "return after, None if context and context[1] else context"
COL_TEST = "if context and _indent_columns(line) >= context[0]:"
HELD_RET = "return HELD if after == PARAGRAPH else after, (context[0], False)"
ITEM_PICK = "item = LIST_ITEM_RE.match(line) if label == TEXT and after == HELD else None"
PAD_TEST = "if not item.group(2) or column - marker_end > 4:"
ITEM_RET = "return after, (column, not bool(item.group(2)))"
LAZY = "if para == HELD and after == HELD:\n        return after, context"
FINAL = "        return after, context\n    return after, None\n"

MUTANTS = {
    "M01 drop the context": (CALL, "para, item_context = _paragraph_after(line, out[-1], para, prev), None"),
    "M02 forget the context at every blank": (BLANK_RET, "return after, None"),
    "M03 strict column": (COL_TEST, "if context and _indent_columns(line) > context[0]:"),
    "M04 blanket indentation": (COL_TEST, "if context and _indent_columns(line) >= 1:"),
    "M05 fixed column two": ("column = len(prefix.expandtabs(4))", "column = 2"),
    "M06 characters, not columns": ("column = len(prefix.expandtabs(4))", "column = len(prefix)"),
    "M07 no W+1 for code padding": (PAD_TEST, "if not item.group(2):"),
    "M08 four columns count as code padding": (PAD_TEST, "if not item.group(2) or column - marker_end >= 4:"),
    "M09 empty item never ends at a blank": (BLANK_RET, "return after, context"),
    "M10 empty flag never clears": (HELD_RET, "return HELD if after == PARAGRAPH else after, context"),
    "M11 empty item uses its padding": (PAD_TEST, "if column - marker_end > 4:"),
    "M12 nested item replaces the outer column": (COL_TEST, "if context and _indent_columns(line) >= context[0] and not LIST_ITEM_RE.match(line):"),
    "M13 sibling keeps the stale column": (ITEM_RET, "return after, context or (column, not bool(item.group(2)))"),
    "M14 no lazy hold": (LAZY, "if False:\n        return after, context"),
    "M15 context never released": (FINAL, "        return after, context\n    return after, context\n"),
    "M16 markers read inside blocks": (ITEM_PICK, "item = LIST_ITEM_RE.match(line)"),
    "M17 noninterrupting item opens a context": (ITEM_PICK, "item = LIST_ITEM_RE.match(line) if label == TEXT and after in (HELD, PARAGRAPH) else None"),
    "M18 resumed paragraph not held": (HELD_RET, "return after, (context[0], False)"),
    # Candidate repair of finding F2, NOT a defect: a dedented block quote or
    # footnote definition releases the item. Expected to SURVIVE, which shows
    # no arm holds that property in either direction.
    "N01 dedented quote/footnote releases the item (F2 repair)": (
        "if para == HELD and after == HELD:",
        "if para == HELD and after == HELD and not (BLOCK_QUOTE_RE.match(line) or FOOTNOTE_DEFINITION_RE.match(line)):"),
}


def run(name: str, old: str, new: str) -> dict:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", name)[:40]
    tree = WORK / slug
    if tree.exists():
        subprocess.run(["git", "-C", str(CLONE), "worktree", "remove", "--force", str(tree)],
                       capture_output=True)
        shutil.rmtree(tree, ignore_errors=True)
    subprocess.run(["git", "-C", str(CLONE), "worktree", "add", "-q", "--detach", str(tree), HEAD],
                   check=True, capture_output=True)
    src = tree / "scripts" / "gen_toc.py"
    text = src.read_text()
    if text.count(old) != 1:
        return {"mutant": name, "error": f"old text occurs {text.count(old)} times"}
    src.write_text(text.replace(old, new, 1))
    result = {"mutant": name}
    for key, cmd in (("toc", ["python3", "-B", "scripts/gen_toc.py", "--selftest"]),
                     ("emdash", ["python3", "-B", "scripts/check_em_dash.py", "--selftest"])):
        proc = subprocess.run(cmd, cwd=tree, capture_output=True, text=True, timeout=900)
        out = proc.stdout + proc.stderr
        result[f"{key}_exit"] = proc.returncode
        result[f"{key}_tail"] = out.strip().splitlines()[-1] if out.strip() else ""
        result[f"{key}_i437"] = sorted(set(re.findall(r"\[(I437[^\]]*)\]", out)))
        result[f"{key}_guards"] = [l.strip() for l in out.splitlines() if "GUARD" in l]
        result[f"{key}_other_fail"] = sorted({m for m in re.findall(r"FAIL \[([^\]]*)\]", out)
                                              if not m.startswith("I437")})
    subprocess.run(["git", "-C", str(CLONE), "worktree", "remove", "--force", str(tree)],
                   capture_output=True)
    return result


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(lambda kv: run(kv[0], *kv[1]), MUTANTS.items()))
    (OUT / "receipts" / "mutants.json").write_text(json.dumps(results, indent=1))
    lines = ["mutant | toc exit | emdash exit | I437 arms named (toc) | guards (toc) | "
             "non-I437 failures (toc) | I437 named (emdash)"]
    for r in results:
        if "error" in r:
            lines.append(f"{r['mutant']} | ERROR {r['error']}")
            continue
        lines.append(f"{r['mutant']} | {r['toc_exit']} | {r['emdash_exit']} | "
                     f"{len(r['toc_i437'])} | {len(r['toc_guards'])} | "
                     f"{len(r['toc_other_fail'])} | {len(r['emdash_i437'])}")
    (OUT / "receipts" / "mutants-table.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
