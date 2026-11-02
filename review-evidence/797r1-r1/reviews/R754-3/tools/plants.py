#!/usr/bin/env python3
"""Plant description edits in a disposable export; report --write, --check and the prose gate.
Usage: plants.py <clean-export> <work-dir> <out.tsv> <deps-dir>"""
import concurrent.futures as cf
import json
import os
import shutil
import subprocess
import sys

src, work, out, deps = sys.argv[1:5]
W = "word " * 25 + "end."
def strobes(name, text=""):
    def f(d):
        d["registers"]["PP_NVM_STAT"]["split"]["PP_NVM_CSR_RDATA"][-2:] = [["1:0", name, text]]
    return f
def undo_data(d):
    strobes("RESERVED")(d)
def note(value):
    def f(d):
        d["registers"]["ETH_GUARD"]["notes"] = [value]
    return f
def purpose(d):
    d["registers"]["ETH_GUARD"]["purpose"] = "| Note |\n|---|\n| " + W + " |"
def field(d):
    d["registers"]["ETH_GUARD"]["fields"] = {k: "| Note |\n|---|\n| x |" for k in d["registers"]["ETH_GUARD"].get("fields", {})}
P = [
 ("control_no_plant", lambda d: None),
 ("data_undone_reserved_pp_nvm_stat", undo_data),
 ("reserved_renamed_RSVD_empty", strobes("RSVD")),
 ("reserved_renamed_UNUSED_prose", strobes("UNUSED", "Unused bits; stored and read back, drive nothing.")),
 ("note_table_trailing_pipe", note("| Note |\n|---|\n| " + W + " |")),
 ("note_table_no_trailing_pipe", note("| Note\n|---\n| " + W)),
 ("note_table_colon_no_trailing_pipe", note("| Note\n|:--\n| " + W)),
 ("note_table_two_col_no_outer_pipe", note("Note | More\n--- | ---\n" + W + " | x")),
 ("note_text_item_table", note({"text": "| Note |\n|---|\n| " + W + " |"})),
 ("note_pair_table", note(["Topic", "| Note |\n|---|\n| " + W + " |"])),
 ("note_heading_intro_table", note({"heading": "Topic", "intro": ["| Note |\n|---|\n| " + W + " |"], "rows": []})),
 ("register_purpose_table", purpose),
 ("field_text_table", field),
]
def run(args, cwd):
    return subprocess.run(args, cwd=cwd, env=dict(os.environ, PYTHONPATH=deps), capture_output=True, text=True, timeout=300)
def one(item):
    name, plant = item
    d = os.path.join(work, name)
    shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(src, d, symlinks=True)
    path = os.path.join(d, "scripts/register_descriptions.json")
    data = json.load(open(path, encoding="utf-8"))
    plant(data)
    json.dump(data, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    w = run(["python3", "scripts/gen_register_reference.py", "--write"], d)
    c = run(["python3", "scripts/gen_register_reference.py", "--check"], d)
    s = run(["python3", "scripts/check_doc_style.py"], d)
    msg = (w.stdout + w.stderr).strip().splitlines()
    shutil.rmtree(d, ignore_errors=True)
    return f"{name}\twrite_rc={w.returncode}\tcheck_rc={c.returncode}\tstyle_rc={s.returncode}\t{(msg[-1] if msg else '')[:150]}"
with cf.ThreadPoolExecutor(13) as pool:
    rows = list(pool.map(one, P))
open(out, "w", encoding="utf-8").write("\n".join(rows) + "\n")
print("\n".join(rows))
