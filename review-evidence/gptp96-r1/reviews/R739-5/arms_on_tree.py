"""Plant every copy-rule self-test arm of the reviewed head on a real Current page.

usage: python3 -I arms_on_tree.py <repo-root> <scratch>
Reads the arm tables out of selftest() with ast, so the list is the head's own. Each arm's text is
appended to a Current page in an archive copy and the production check runs.
must-fail: a "restates <name>" finding is required. pass and expected-failure: no "restates" finding.
A closing paragraph first ends the page's last list item, so each arm starts outside any container.
The one expected-failure arm that embeds the fixture table is skipped here; tree_probes covers it.
"""
import ast
import concurrent.futures
import queue
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
SCRATCH = Path(sys.argv[2]).resolve()
PAGE = "docs/HDL_DEVELOPER.md"
JOBS = 16


def arm_tables():
    tree = ast.parse((ROOT / "scripts/check_docs.py").read_text(encoding="utf-8"))
    selftest = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "selftest")
    names = {"rto": "SYNC_RTO_MS_C", "follow_up": "FU_RTO_MS_C", "cease": "CEASE_MS_C"}
    arms, skipped = [], []
    for node in ast.walk(selftest):
        if not (isinstance(node, ast.For) and isinstance(node.iter, ast.Tuple) and isinstance(node.target, ast.Tuple)):
            continue
        target = [t.id for t in node.target.elts if isinstance(t, ast.Name)]
        if target == ["label", "text"]:
            kind = "pass"
        elif target == ["label", "copy", "name"]:
            kind = "must-fail"
        elif target == ["label", "page", "copy"]:
            kind = "expected-failure"
        else:
            continue
        for row in node.iter.elts:
            try:
                values = eval(compile(ast.Expression(row), "arm", "eval"), {"__builtins__": {}}, names)
            except NameError:
                skipped.append(ast.literal_eval(row.elts[0]))
                continue
            if kind == "pass" or kind == "must-fail":
                arms.append((kind, values[0], values[1], values[2] if kind == "must-fail" else ""))
            else:
                arms.append((kind, values[0], values[2], ""))
    return arms, skipped


def main():
    arms, skipped = arm_tables()
    trees = queue.Queue()
    archive = subprocess.run(["git", "-C", str(ROOT), "archive", "HEAD"], capture_output=True, check=True).stdout
    for index in range(JOBS):
        tree = SCRATCH / f"arm-tree-{index}"
        if tree.exists():
            shutil.rmtree(tree)
        tree.mkdir(parents=True)
        subprocess.run(["tar", "-x", "-C", str(tree)], input=archive, check=True)
        trees.put(tree)

    def run(arm):
        kind, label, text, name = arm
        tree = trees.get()
        target = tree / PAGE
        original = target.read_bytes()
        try:
            target.write_bytes(original + b"\nClosing paragraph here.\n\n" + text.encode("utf-8") + b"\n")
            done = subprocess.run([sys.executable, "-B", "scripts/check_docs.py"], cwd=tree, capture_output=True, text=True)
            out = done.stdout + done.stderr
        finally:
            target.write_bytes(original)
            trees.put(tree)
        if kind == "must-fail":
            good = f"restates {name}" in out and done.returncode != 0
        else:
            good = "restates" not in out
        return kind, label, done.returncode, good

    with concurrent.futures.ThreadPoolExecutor(JOBS) as pool:
        results = list(pool.map(run, arms))
    bad = 0
    counts = {}
    for kind, label, rc, good in results:
        counts[kind] = counts.get(kind, 0) + 1
        bad += not good
        print(f"{kind:17} rc={rc} {'as-stated' if good else 'DIFFERS'} | {label}")
    print(f"arms {counts}, skipped {skipped}, differ {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
