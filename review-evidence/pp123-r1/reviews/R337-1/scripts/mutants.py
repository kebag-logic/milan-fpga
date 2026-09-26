#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Apply one mutant at a time to a COPY of the head tree and run the PR's own
generator tests (tb/desc_store/test_gen_desc_image.py) plus `make
generator-check`. Usage: mutants.py HEAD_TREE WORK_DIR

Every mutant must be killed (a non-zero test exit). The unmutated control must
pass. Prints one JSON line per mutant: failing test names and exit codes.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

GEN = "hdl/aecp/desc/gen_desc_image.py"
CHECK = '''        body_type = int.from_bytes(body[0:2], "big")
        body_index = int.from_bytes(body[2:4], "big")
        if (body_type, body_index) != (typ, idx):
'''

MUTANTS = {
    "control": [],
    # the author's mutant: remove the comparison and its ImageError entirely
    "author_remove_check": [(re.compile(
        r'        body_type = int.from_bytes\(body\[0:2\], "big"\)\n.*?f"index \{body_index\}"\)\n',
        re.S), "")],
    "type_only": [('if (body_type, body_index) != (typ, idx):', 'if body_type != typ:')],
    "index_only": [('if (body_type, body_index) != (typ, idx):', 'if body_index != idx:')],
    "low_bytes_only": [('int.from_bytes(body[0:2], "big")', 'body[1]'),
                       ('int.from_bytes(body[2:4], "big")', 'body[3]'),
                       ('if (body_type, body_index) != (typ, idx):',
                        'if (body_type, body_index) != (typ & 0xFF, idx & 0xFF):')],
    "little_endian": [('int.from_bytes(body[0:2], "big")', 'int.from_bytes(body[0:2], "little")'),
                      ('int.from_bytes(body[2:4], "big")', 'int.from_bytes(body[2:4], "little")')],
    "offset_shift": [('int.from_bytes(body[0:2], "big")', 'int.from_bytes(body[1:3], "big")'),
                     ('int.from_bytes(body[2:4], "big")', 'int.from_bytes(body[3:5], "big")')],
    "bytes_form_only": [('if (body_type, body_index) != (typ, idx):',
                         'if "bytes" in desc and (body_type, body_index) != (typ, idx):')],
    "fields_form_only": [('if (body_type, body_index) != (typ, idx):',
                          'if "bytes" not in desc and (body_type, body_index) != (typ, idx):')],
    "first_descriptor_only": [('if (body_type, body_index) != (typ, idx):',
                               'if not groups and (body_type, body_index) != (typ, idx):')],
    "message_drops_cfg": [('f"cfg {cfg} directory key type', 'f"cfg 0 directory key type')],
    "message_key_body_swapped": [('f"cfg {cfg} directory key type 0x{typ:04X} index {idx} "',
                                  'f"cfg {cfg} directory key type 0x{body_type:04X} index {body_index} "')],
    "wrong_exception": [('            raise ImageError(\n                f"cfg {cfg} directory key',
                         '            raise ValueError(\n                f"cfg {cfg} directory key')],
    "compare_raw_key_spelling": [('if (body_type, body_index) != (typ, idx):',
                                  'if (body_type, body_index) != (typ, idx) and '
                                  'isinstance(desc["type"], str) and desc["type"] in TYPES:')],
}


def mutate(src, edits):
    for old, new in edits:
        if isinstance(old, re.Pattern):
            src, n = old.subn(new, src)
        else:
            n = src.count(old)
            src = src.replace(old, new)
        if n != 1:
            raise SystemExit(f"mutation site count {n} for {old!r}")
    return src


def main():
    head, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    orig = (head / GEN).read_text()
    assert CHECK in orig
    bad = 0
    for name, edits in MUTANTS.items():
        tree = work / name
        if tree.exists():
            shutil.rmtree(tree)
        shutil.copytree(head / "hdl/aecp/desc", tree / "hdl/aecp/desc")
        shutil.copytree(head / "tb/desc_store", tree / "tb/desc_store")
        (tree / GEN).write_text(mutate(orig, edits))
        t = subprocess.run([sys.executable, "-B", "test_gen_desc_image.py"], cwd=tree / "tb/desc_store",
                           capture_output=True, text=True, timeout=600)
        failed = sorted(set(re.findall(r"^(?:FAIL|ERROR): (test_\w+)", t.stderr, re.M)))
        m = subprocess.run(["make", "generator-check"], cwd=tree / "tb/desc_store",
                           capture_output=True, text=True, timeout=600)
        tail = [ln for ln in t.stderr.splitlines() if ln.startswith(("Ran ", "OK", "FAILED"))]
        killed = t.returncode != 0 and m.returncode != 0
        ok = (not killed) if name == "control" else killed
        bad += not ok
        print(json.dumps({"mutant": name, "tests_rc": t.returncode, "make_generator_check_rc": m.returncode,
                          "failed_tests": failed, "unittest_tail": tail,
                          "verdict": ("control passes" if name == "control" else
                                      "killed" if killed else "SURVIVED"), "ok": ok}))
    print(f"SUMMARY: {len(MUTANTS)} runs, {bad} unexpected")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
