"""Re-run the author's published planted defects (mutants.json old/new pairs) on the clean head.

Each pair is applied to a copy of the committed runner only if `old` occurs exactly
once; the flat 0555 install's --selftest runs inside sbx.sh. The FAIL lines are
compared with the author's recorded ones. Usage:
python3 -I replay_author_mutants.py <mutants.json> <clean> <out> <sbx.sh> [jobs]
"""
import concurrent.futures, json, pathlib, re, subprocess, sys
spec, clean, out, sbx = sys.argv[1:5]
jobs = int(sys.argv[5]) if len(sys.argv) > 5 else 12
items = json.load(open(spec))
source = (pathlib.Path(clean) / "scripts/act_ci.py").read_text()
def run(item):
    d = pathlib.Path(out) / item["mutant"]; d.mkdir(parents=True, exist_ok=True)
    n = source.count(item["old"])
    if n != 1:
        return item["mutant"], f"NOT-APPLIED ({n}x)", [], item.get("fails", [])
    t = d / "act_ci.py"
    if t.exists(): t.chmod(0o644)
    t.write_text(source.replace(item["old"], item["new"])); t.chmod(0o555)
    subprocess.run([sbx, str(d / "run"), clean, sys.executable, "-I", str(t), "--selftest", "--worktree", clean])
    rc = (d / "run.rc").read_text().strip()
    log = (d / "run.log").read_text(errors="replace")
    fails = ["FAIL " + re.sub(r"^\s*FAIL\s+", "", l) for l in log.splitlines() if re.match(r"^\s*FAIL\s", l)]
    last = log.strip().splitlines()[-1] if log.strip() else ""
    return item["mutant"], f"{'KILLED' if rc != '0' or fails else 'SURVIVED'} rc={rc} last={last[:100]!r}", fails, item.get("fails", [])
with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
    for name, verdict, fails, theirs in pool.map(run, items):
        norm = lambda xs: sorted(re.sub(r"(line |:)[0-9]{4,5}\b", r"\1N", x) for x in xs)
        same = "same FAIL set as the author's receipt" if norm(fails) == norm(theirs) else f"FAIL set differs (mine {len(fails)}, theirs {len(theirs)})"
        print(f"{name}: {verdict}; {len(fails)} FAIL; {same}")
        for f in fails[:4]: print("    " + f[:200])
