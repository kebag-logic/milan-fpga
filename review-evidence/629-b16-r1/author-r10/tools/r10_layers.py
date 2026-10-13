#!/usr/bin/env python3
"""Lane B16, round 10: what each of round 10's two rules catches on its own (offline, documents only).

usage: <parser python> r10_layers.py <check_b16_figures.py> <findings.md> <packet root> <scratch dir> <out.json>

Writes two copies of the check into the scratch directory, each with one rule taken out by replacing its one
statement: "no position" without the refusal of a block holding a node with no start line, and "conservation"
without the comparison of a block's rendered digits with those the check read. Then runs the check and both
copies on the unchanged page and on altered copies, each appending to a line or prefixing it so that no line
moves: a bare e-mail address before a figure on the introduction's second covered line, in the index row's
lane B16 part, on the second line of the section's first paragraph and in the last cell of a row of its first
table; and an entity or a backslash escape just before the index row's lane B16 part. For each run it records
the exit status and what the check names MARKUP or UNCOVERED, with the line and the reason. Nothing on the
bench is read or written.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

CHECK, PAGE, PACKET, SCRATCH, OUT = (Path(a).resolve() for a in sys.argv[1:6])
REPO = PAGE.parents[2]
CUT = {"no position": ("bad_start = sl < 1", "bad_start = False and sl < 1"),
       "conservation": ("                if not leaf[3] and sorted(", "                if False and sorted(")}


def main() -> int:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    src = CHECK.read_text(encoding="utf-8")
    checks = {"both rules": CHECK}
    for name, (old, new) in CUT.items():
        assert src.count(old) == 1, old
        checks[f"without {name}"] = SCRATCH / f"without-{name.replace(' ', '-')}.py"
        checks[f"without {name}"].write_text(src.replace(old, new, 1), encoding="utf-8")
    text = PAGE.read_text(encoding="utf-8").split("\n")
    index = (PAGE.parent / "README.md").read_text(encoding="utf-8").split("\n")
    intro = next(i for i, x in enumerate(text) if x.startswith("In lane B16, the operator tried the reference peer's"))
    para = next(i for i, x in enumerate(text) if x.startswith("The loopback did not form. The peer's listener"))
    cell = next(i for i, x in enumerate(text) if x.startswith("| Restore | Done | See [B16: bench as left]"))
    row = next(i for i, x in enumerate(index) if x.startswith("| [" + PAGE.name + "]"))
    a = "Lane B16, `5603c353`:"
    cases = [("the unchanged page", None, None, None),
             ("an e-mail address before a figure on the introduction's second covered line", "page", intro + 1,
              lambda x: x + " Write to x@example.com 7 ppm."),
             ("an e-mail address before a figure in the index row's lane B16 part", "index", row,
              lambda x: x[:-2] + "; write to x@example.com 7 ppm. |"),
             ("an e-mail address before a figure on the second line of the section's first paragraph", "page", para + 1,
              lambda x: x + " x@example.com 7 ppm."),
             ("an e-mail address before a figure in the last cell of a row of the section's first table", "page", cell,
              lambda x: x[:-2] + " x@example.com 7 ppm. |"),
             ("an entity just before the index row's lane B16 part", "index", row, lambda x: x.replace(a, "&amp; " + a, 1)),
             ("a backslash escape just before the index row's lane B16 part", "index", row,
              lambda x: x.replace(a, "\\* " + a, 1))]
    out = []
    for i, (name, doc, line, edit) in enumerate(cases):
        d = SCRATCH / f"case{i}" / "docs" / "findings"
        d.mkdir(parents=True, exist_ok=True)
        page, ix = list(text), list(index)
        if doc:
            (page if doc == "page" else ix)[line] = edit((page if doc == "page" else ix)[line])
        (d / PAGE.name).write_text("\n".join(page), encoding="utf-8")
        (d / "README.md").write_text("\n".join(ix), encoding="utf-8")
        runs = {}
        for cname, chk in checks.items():
            p = subprocess.run([sys.executable, "-I", str(chk), str(d / PAGE.name), str(PACKET), str(d / "r.tsv"),
                                str(d / "c.tsv"), "--repo", str(REPO)], capture_output=True, text=True, timeout=600)
            named = [x.split(" | ")[0] for x in p.stdout.splitlines() if x.split(" ")[0] in ("MARKUP", "UNCOVERED")]
            runs[cname] = dict(rc=p.returncode, named=named)
        out.append(dict(case=name, document=doc and ("README.md" if doc == "index" else PAGE.name),
                        line=None if line is None else line + 1, runs=runs))
        print(name, {k: (v["rc"], [x[:70] for x in v["named"]]) for k, v in runs.items()})
    OUT.write_text(json.dumps(dict(note="Lane B16 round 10: the check with both of round 10's rules, and copies of it "
                                        "with each taken out, on the unchanged page and on altered copies; offline, "
                                        "no bench action", cut={k: v[0].strip() for k, v in CUT.items()}, cases=out),
                              indent=1, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
