#!/usr/bin/env python3
"""Second plant set. Usage: plants2.py <clean-export> <work-dir> <out.tsv> <deps-dir>"""
import json, os, shutil, subprocess, sys
src, work, out, deps = sys.argv[1:5]
W = "word " * 25 + "end."
P = [("note_when_item_table", {"when": {"LPF_P": 0}, "text": "| Note |\n|---|\n| " + W + " |"}),
     ("note_table_row_without_leading_pipe", "| Note\n|---\n" + W)]
rows = []
for name, value in P:
    d = os.path.join(work, name); shutil.rmtree(d, ignore_errors=True); shutil.copytree(src, d, symlinks=True)
    path = os.path.join(d, "scripts/register_descriptions.json"); data = json.load(open(path, encoding="utf-8"))
    data["registers"]["ETH_GUARD"]["notes"] = [value]
    json.dump(data, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    env = dict(os.environ, PYTHONPATH=deps)
    w = subprocess.run(["python3", "scripts/gen_register_reference.py", "--write"], cwd=d, env=env, capture_output=True, text=True)
    s = subprocess.run(["python3", "scripts/check_doc_style.py"], cwd=d, env=env, capture_output=True, text=True)
    first = (w.stdout + w.stderr).strip().splitlines()[0][:110]
    rows.append(f"{name}\twrite_rc={w.returncode}\tstyle_rc={s.returncode}\t{first}")
    shutil.rmtree(d, ignore_errors=True)
open(out, "w", encoding="utf-8").write("\n".join(rows) + "\n"); print("\n".join(rows))
