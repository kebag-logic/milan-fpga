#!/usr/bin/env python3
"""Plant every copy-rule self-test arm on a real page of a tree copy and run the production check.

usage: python3 -I plant_arms.py <tree> <jobs> <scratch>
Arms are read from the selftest source by parsing the for-loop tuples, so nothing is retyped.
Exit shape per arm: PASS-ARM / FAIL-ARM / XFAIL-ARM, expected, rc, whether a 'restates' finding appeared.
"""
import ast, re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
tree, jobs, scratch = Path(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3])
source = (tree / "scripts/check_docs.py").read_text()
fn = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == "selftest")
sub_table = {"rto": "SYNC_RTO_MS_C", "follow_up": "FU_RTO_MS_C", "cease": "CEASE_MS_C"}
arms = []
def lit(node):
    try:
        return ast.literal_eval(node)
    except Exception:
        return None
for loop in ast.walk(fn):
    if not isinstance(loop, ast.For) or not isinstance(loop.iter, ast.Tuple):
        continue
    names = [t.id for t in loop.target.elts] if isinstance(loop.target, ast.Tuple) else []
    body = ast.get_source_segment(source, loop)
    for row in loop.iter.elts:
        if not isinstance(row, ast.Tuple):
            continue
        vals = [lit(e) for e in row.elts]
        if names[:2] == ["label", "text"] and "copy_findings" in body and len(vals) == 2:
            arms.append(("pass", vals[0], vals[1], None))
        elif names[:3] == ["label", "copy", "name"]:
            name = lit(row.elts[2]) or sub_table.get(getattr(row.elts[2], "id", ""))
            arms.append(("fail", vals[0], vals[1], name))
        elif names[:3] == ["label", "page", "copy"]:
            if vals[1] == "docs/GUIDE.md" and vals[2] is not None:
                arms.append(("xfail", vals[0], vals[2], None))
print(f"arms pass={sum(a[0]=='pass' for a in arms)} fail={sum(a[0]=='fail' for a in arms)} xfail={sum(a[0]=='xfail' for a in arms)}")
def worker(args):
    index, (kind, label, text, name) = args
    work = scratch / f"plant{index}"
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(tree, work, ignore=shutil.ignore_patterns(".git", "obj_dir", "__pycache__"))
    page = work / "docs/GLOSSARY.md"
    page.write_text(page.read_text() + "\n" + text + "\n")
    run = subprocess.run([sys.executable, "-B", "scripts/check_docs.py"], cwd=work, capture_output=True, text=True)
    out = run.stdout + run.stderr
    found = re.findall(r"restates (\w+)", out)
    shutil.rmtree(work)
    if kind == "fail":
        ok = run.returncode != 0 and name in found
    else:
        ok = not found
    return f"{'OK ' if ok else 'BAD'} {kind:5} rc={run.returncode} found={sorted(set(found))} want={name} | {label}"
with ThreadPoolExecutor(jobs) as pool:
    results = list(pool.map(worker, enumerate(arms)))
print("\n".join(results))
print("BAD count", sum(r.startswith("BAD") for r in results))
