"""R237-5 F2's verification: pages nested 1200 deep (block quotes, list
levels) through both SHIPPED gates in a disposable repository built from
`git archive <rev> scripts tools/markdown`. The base commit holds the gate
only; the head adds docs/DEEP.md (headings around the deep block, one of
them carrying an em dash, with a Contents block copying it).
Usage: deep_pages_gates.py <python-with-lock> <source-repo> <workdir> <rev>"""
import shutil, subprocess, sys
from pathlib import Path

py, src, work, rev = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
EM = "—"
DEEP = {"block quotes 1200 deep": ">" * 1200 + " x\n",
        "list levels 1200 deep": "".join("  " * i + "- x\n" for i in range(1200))}
env = {"PATH": "/usr/bin:/bin", "HOME": str(work), "GIT_CONFIG_NOSYSTEM": "1",
       "PYTHONDONTWRITEBYTECODE": "1"}
tar = subprocess.run(["git", "-C", str(src), "archive", rev, "scripts", "tools/markdown"],
                     capture_output=True, check=True).stdout
print("source:", subprocess.run(["git", "-C", str(src), "rev-parse", rev], capture_output=True, text=True).stdout.strip())
for name, deep in DEEP.items():
    repo = work / name.split()[0]
    shutil.rmtree(repo, ignore_errors=True); repo.mkdir(parents=True)
    subprocess.run(["tar", "-x", "-C", str(repo)], input=tar, check=True)

    def git(*a):
        return subprocess.run(["git", "-c", "user.name=probe", "-c", "user.email=probe@example.invalid", *a],
                              cwd=repo, env=env, capture_output=True, text=True, check=True).stdout
    git("init", "-q", "--initial-branch=main"); git("add", "-A"); git("commit", "-qm", "base")
    base = git("rev-parse", "HEAD").strip()
    page = ("# Page\n\n## Contents\n\n- **[Alpha](#alpha)** -- a.\n- **[Beta](#beta)** -- b.\n"
            f"- **[Old {EM} heading](#old--heading)** -- c.\n\n## Alpha\n\n## Beta\n\n" + deep
            + f"\n## Old {EM} heading\n")
    (repo / "docs").mkdir()
    (repo / "docs/DEEP.md").write_text(page); git("add", "-A"); git("commit", "-qm", "head")
    print(f"===== {name}")
    for argv in (["scripts/gen_toc.py", "--check"], ["scripts/check_em_dash.py", "--base", base]):
        res = subprocess.run([py, *argv], cwd=repo, env=env, capture_output=True, text=True)
        tail = (res.stdout + res.stderr).strip().splitlines()
        print(f"  {' '.join(argv[:2])}: rc={res.returncode}")
        for line in tail[-3:]:
            print(f"      {line[:200]}")
    shutil.rmtree(repo)
