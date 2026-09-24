#!/usr/bin/env python3
"""Drop each member of gen_toc_renderer._OWN_ELEMENT in turn (disposable
copies) and run gen_toc.py --selftest and check_em_dash.py --selftest.
Usage: mutate_own_element.py <tree> <workdir> <python>"""
import shutil, subprocess, sys
from pathlib import Path
tree, work, py = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
OLD = ('_OWN_ELEMENT = ("block_quote", "list", "heading", "code_block",\n'
       '                "thematic_break", "table")')
env = {"PATH": "/usr/bin:/bin", "HOME": str(work), "TMPDIR": str(work),
       "PYTHONDONTWRITEBYTECODE": "1", "GIT_CONFIG_NOSYSTEM": "1",
       "GIT_AUTHOR_NAME": "m", "GIT_AUTHOR_EMAIL": "m@example.invalid",
       "GIT_COMMITTER_NAME": "m", "GIT_COMMITTER_EMAIL": "m@example.invalid"}
for kind in ("block_quote", "list", "heading", "code_block", "thematic_break", "table"):
    copy = work / f"own-{kind}"
    shutil.rmtree(copy, ignore_errors=True); copy.mkdir(parents=True)
    for part in ("scripts", "tools"):
        shutil.copytree(tree / part, copy / part)
    p = copy / "scripts/gen_toc_renderer.py"; src = p.read_text()
    assert src.count(OLD) == 1
    kinds = [k for k in ("block_quote", "list", "heading", "code_block", "thematic_break", "table") if k != kind]
    p.write_text(src.replace(OLD, f"_OWN_ELEMENT = {tuple(kinds)!r}"))
    out = []
    for script in ("scripts/gen_toc.py", "scripts/check_em_dash.py"):
        r = subprocess.run([py, script, "--selftest"], cwd=copy, env=env, capture_output=True, text=True)
        out.append(f"{script.split('/')[1]} rc={r.returncode} {(r.stdout + r.stderr).strip().splitlines()[-1][:90]}")
    killed = any(" rc=0 " not in o for o in out)
    print(f"drop {kind!r}: {'KILLED' if killed else 'SURVIVES'} | " + " | ".join(out))
    shutil.rmtree(copy)
