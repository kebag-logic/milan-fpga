#!/usr/bin/env python3
"""Undo each round-3 generator fix in a disposable export, regenerate, and run --selftest.
Usage: mutants.py <clean-export> <work-dir> <out.tsv> <deps-dir> [jobs]"""
import concurrent.futures as cf
import os
import re
import shutil
import subprocess
import sys

src, work, out, deps = sys.argv[1:5]
jobs = int(sys.argv[5]) if len(sys.argv) > 5 else 16
PAGE, TEST = "scripts/register_page.py", "scripts/register_selftest.py"
OLD_TABLE = '''    live = [leaf for _, leaf in reg.views if not leaf_constant(leaf, model)]
    rows = [[model.wording.conditions(conds), leaf_text(leaf, len(live) == 1, model)] for conds, leaf in reg.views]
    return table(["When", "A read returns"], rows)
'''
NEW_TABLE = re.compile(r"    live = \[leaf for _, leaf in reg\.views if not leaf_constant\(leaf, model\)\]\n.*?    return table\(\[\"When\", \"A read returns\"\], rows\)\n", re.S)
M = [
 # name, file, old, new, the control that must fail
 ("baseline", None, None, None, None),
 ("reserved_refusal_removed", PAGE, 'if fl.name == "RESERVED" and "W" in fl.access and any(note.startswith("writes:") for note in fl.notes):', 'if False:', "reserved bits"),
 ("reserved_refusal_access_off", PAGE, 'fl.name == "RESERVED" and "W" in fl.access', 'fl.name == "RESERVED" and "Z" in fl.access', "reserved bits"),
 ("reserved_refusal_note_off", PAGE, 'note.startswith("writes:") for note in fl.notes', 'note.startswith("nothing:") for note in fl.notes', "reserved bits"),
 ("table_refusal_removed", PAGE, 'if TABLE_DELIMITER_RE.search(text):', 'if False:', "Markdown table"),
 ("table_regex_dead", PAGE, 'r"^\\s*\\|?\\s*:?-+:?\\s*\\|"', 'r"^NEVER$"', "Markdown table"),
 ("table_site_plain_undone", PAGE, 'out += [note_prose(item), ""]', 'out += [page_links(item), ""]', "Markdown table"),
 ("table_site_text_undone", PAGE, 'out += [note_prose(item["text"]), ""]', 'out += [page_links(item["text"]), ""]', "Markdown table"),
 ("table_site_intro_undone", PAGE, 'out += [note_prose(para), ""]', 'out += [page_links(para), ""]', "Markdown table"),
 ("table_site_pair_undone", PAGE, "note_prose(' '.join(item[1:]))", "page_links(' '.join(item[1:]))", "Markdown table"),
 ("read_rows_old_flat_table", PAGE, "@TABLE", OLD_TABLE, "read-table"),
 ("read_impossible_off", PAGE, "if equal.setdefault(signal, unparse(node[3])) != unparse(node[3]):", "if False:", "read-table"),
 ("read_no_merge", PAGE, "merged.add((value, care & ~bit))", "pass", "read-table"),
 ("read_polarity_flipped", PAGE, "[(found[name], bool(term >> n & 1))", "[(found[name], not (term >> n & 1))", "read-table"),
 ("read_last_match_not_first", PAGE, "leaf = next(leaf for conds, leaf in views if", "leaf = next(leaf for conds, leaf in reversed(views) if", "read-table"),
 ("read_any_other_wrong_value", PAGE, 'rows.append(["any other case", other])', 'rows.append(["any other case", "`0xFFFFFFFF`"])', "read-table"),
 ("read_any_other_row_dropped", PAGE, 'rows.append(["any other case", other])', 'pass', "read-table"),
 ("read_arm_or_check_off", TEST, 'if " or " in when or len(set(terms)) < len(terms):', 'if False:', "read-table"),
]


def run(args, cwd):
    env = dict(os.environ, PYTHONPATH=deps)
    return subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True, timeout=540)


def one(m):
    name, rel, old, new, want = m
    d = os.path.join(work, name)
    shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(src, d, symlinks=True)
    if rel:
        path = os.path.join(d, rel)
        text = open(path, encoding="utf-8").read()
        if old == "@TABLE":
            mutated, count = NEW_TABLE.subn(lambda _: new, text)
            if not count:
                return f"{name}\tNOT-APPLIED\t\t\t"
        else:
            if old not in text:
                return f"{name}\tNOT-APPLIED\t\t\t"
            mutated = text.replace(old, new)
        open(path, "w", encoding="utf-8").write(mutated)
    w = run(["python3", "scripts/gen_register_reference.py", "--write"], d)
    s = run(["python3", "scripts/gen_register_reference.py", "--selftest"], d)
    fails = [l.strip()[5:] for l in s.stdout.splitlines() if l.strip().startswith("FAIL ")]
    open(os.path.join(work, name + ".log"), "w", encoding="utf-8").write(w.stdout + w.stderr + s.stdout + s.stderr)
    named = "" if want is None else ("yes" if any(want.lower() in f.lower() for f in fails) else "no")
    verdict = s.stdout.strip().splitlines()[-1] if s.stdout.strip() else ""
    shutil.rmtree(d, ignore_errors=True)
    return f"{name}\twrite_rc={w.returncode}\tselftest_rc={s.returncode}\texpected_control_failed={named}\t{verdict}\t{'; '.join(fails)[:300]}"


with cf.ThreadPoolExecutor(jobs) as pool:
    rows = list(pool.map(one, M))
open(out, "w", encoding="utf-8").write("\n".join(rows) + "\n")
print("\n".join(rows))
