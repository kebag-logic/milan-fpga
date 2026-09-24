#!/usr/bin/env python3
"""Reviewer probe: forged-position pages through the shipped em-dash gate.

For every spelling of the renderer's position attribute a page can carry,
build a page whose em-dash heading GitHub hides (a raw `<!--` left open in a
block quote, the #516 family) and whose forged element carries that
heading's source position. Then, in a disposable git repository holding
only one tree's `scripts/` and `tools/markdown/`:

  base commit: the page with a Contents block the GENERATOR TREE writes
               (the tree before the correction lists the hidden heading)
  head commit: the same page, only the hidden heading's description changed

and run that tree's `scripts/check_em_dash.py --base <base>`. A forged
position that still works shows as `exempt >= 1`. `headings()` of the page
is recorded under each tree too.

Usage: forge_e2e.py PYTHON GEN_TREE GATE_TREE [GATE_TREE...] OUT_DIR
(trees are `git archive <rev> scripts tools/markdown` extractions).
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

HIDDEN = "## Secret — x"


def forgery(kind: str, pos: str) -> list[str]:
    """Lines that put `pos` on an h2 element the page wrote, per spelling.
    Every variant has the same line count (4), so positions stay put."""
    raw = {
        "lower-raw": f'<h2 data-sourcepos="{pos}"></h2>',
        "upper-raw": f'<h2 DATA-SOURCEPOS="{pos}"></h2>',
        "mixed-raw": f'<h2 Data-SourcePos="{pos}"></h2>',
        "mixed-raw-unquoted": f'<h2 dAtA-sOuRcEpOs={pos}></h2>',
    }
    if kind in raw:
        return [raw[kind], "", "x", ""]
    text = {
        "charref-dec": f"&#100;ata-sourcepos={pos} z",
        "charref-hex": f"&#x64;ata-sourcepos={pos} z",
        "charref-upper": f"&#68;ATA-SOURCEPOS={pos} z",
        "charref-hyphen": f"data&#45;sourcepos={pos} z",
        "charref-all": "".join(f"&#{ord(c)};" for c in "data-sourcepos")
                       + f"={pos} z",
        "escape": f"data\\-sourcepos={pos} z",
        "escape-upper": f"DATA\\-SOURCEPOS={pos} z",
        "control-benign": f"data-sourcepo={pos} z",
    }[kind]
    # A raw tag left open in a single-quoted value (a type-6 HTML block
    # ended by the blank line), then a paragraph whose leading quote closes
    # the value: the paragraph's decoded text is read as attributes.
    return ["<h2 title='", "", "'" + text, ""]


def page(kind: str, pos: str, contents: list[str] | None) -> str:
    head = ["# Probe", ""]
    if contents:
        head += contents + ([""] if contents[-1] else [])
    body = ["## Alpha", "", "Text.", "", "## Beta", "", "Text.", "",
            "## Gamma", "", "Text.", ""]
    body += forgery(kind, pos)
    body += ["> <!--", "", HIDDEN, "", "Tail.", ""]
    return "\n".join(head + body)


def hidden_pos(text: str) -> str:
    lines = text.split("\n")
    n = lines.index(HIDDEN) + 1
    return f"{n}:1-{n}:{len(HIDDEN.encode())}"


def run(cmd, cwd, check=True):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit(f"{cmd} rc {r.returncode}\n{r.stdout}\n{r.stderr}")
    return r


HELPER = r"""
import json, sys
sys.path.insert(0, sys.argv[1] + "/scripts")
import gen_toc
text = open(sys.argv[2], encoding="utf-8").read()
items = gen_toc.plan(text)
out = {"headings": gen_toc.headings(text),
       "refusals": [list(r) for r in gen_toc.refusals(text)],
       "block": gen_toc.render(items, {}, "--") if items else None}
print(json.dumps(out))
"""


def ask(py: str, tree: Path, path: Path) -> dict:
    r = run([py, "-c", HELPER, str(tree), str(path)], cwd=path.parent)
    return json.loads(r.stdout)


def build_page(py: str, gen_tree: Path, kind: str, work: Path) -> str:
    """The base page: its Contents block as the generator tree writes it,
    with the forged position matching the hidden heading at that layout."""
    probe = work / "probe.md"
    contents = None
    for _ in range(4):
        text = page(kind, "0:0-0:0", contents)
        text = page(kind, hidden_pos(text), contents)
        probe.write_text(text, encoding="utf-8")
        block = ask(py, gen_tree, probe)["block"]
        if block is None:
            return text
        block = [l.replace("TODO describe this section", "old words")
                 for l in block]
        if block == contents:
            return text
        contents = block
    return text


def e2e(py: str, gate_tree: Path, text: str, repo: Path) -> dict:
    if repo.exists():
        shutil.rmtree(repo)
    repo.mkdir(parents=True)
    shutil.copytree(gate_tree / "scripts", repo / "scripts")
    shutil.copytree(gate_tree / "tools", repo / "tools")
    (repo / "docs").mkdir()
    env_git = ["git", "-c", "user.name=probe", "-c", "user.email=p@x",
               "-c", "commit.gpgsign=false"]
    run(["git", "init", "-q", "-b", "main"], repo)
    (repo / "docs/probe.md").write_text(text, encoding="utf-8")
    run(["git", "add", "-A"], repo)
    run(env_git + ["commit", "-qm", "base"], repo)
    base = run(["git", "rev-parse", "HEAD"], repo).stdout.strip()
    lines = text.split("\n")
    changed = [l.replace("old words", "new words") if "Secret" in l else l
               for l in lines]
    edited = changed != lines
    if not edited:  # no Contents entry for it: add an em dash to a label
        changed = [l + " — x" if l == "## Gamma" else l for l in lines]
    (repo / "docs/probe.md").write_text("\n".join(changed), encoding="utf-8")
    run(["git", "add", "-A"], repo)
    run(env_git + ["commit", "-qm", "head"], repo)
    r = run([py, "scripts/check_em_dash.py", "--base", base], repo,
            check=False)
    tail = (r.stdout.strip().splitlines() or [""])[-1]
    exempt = None
    if "mirrored label(s) exempt" in tail:
        exempt = int(tail.split(" mirrored")[0].rsplit(",", 1)[1].strip())
    return {"rc": r.returncode, "summary": tail, "exempt": exempt,
            "entry_edited": edited, "stdout": r.stdout, "stderr": r.stderr}


def main() -> int:
    py, gen_tree, *gates, out = sys.argv[1:]
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    kinds = ["lower-raw", "upper-raw", "mixed-raw", "mixed-raw-unquoted",
             "charref-dec", "charref-hex", "charref-upper", "charref-hyphen",
             "charref-all", "escape", "escape-upper", "control-benign"]
    report = {}
    for kind in kinds:
        work = out / "pages" / kind
        work.mkdir(parents=True, exist_ok=True)
        text = build_page(py, Path(gen_tree), kind, work)
        (work / "probe.md").write_text(text, encoding="utf-8")
        entry = {"page_sha": __import__("hashlib").sha256(
            text.encode()).hexdigest()}
        for gate in gates:
            g = Path(gate)
            asked = ask(py, g, work / "probe.md")
            res = e2e(py, g, text, out / "repos" / f"{kind}-{g.name}")
            entry[g.name] = {"headings": asked["headings"],
                             "refusals": asked["refusals"],
                             "gate": {k: res[k] for k in
                                      ("rc", "summary", "exempt",
                                       "entry_edited")},
                             "findings": res["stdout"].splitlines()[:-1]}
        report[kind] = entry
        line = [kind]
        for gate in gates:
            e = entry[Path(gate).name]
            hid = any("Secret" in h[1] for h in e["headings"])
            line.append(f"{Path(gate).name}: hidden-listed={hid} "
                        f"refused={len(e['refusals'])} rc={e['gate']['rc']} "
                        f"exempt={e['gate']['exempt']}")
        print(" | ".join(line), flush=True)
    (out / "forge_e2e.json").write_text(json.dumps(report, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
