#!/usr/bin/env python3
"""R272-6: S's verdict and the `keeps` reader's answer on given texts, in
gate 1b's own namespace (hook before `subset_note = assert_subset_refuses()`,
every cross compiler hidden), optionally after count-checked --patch files;
and, with --gcc, what that compiler keeps of each text at -std=gnu99 -E -P,
one file per text. Usage: reader_eval.py --tree <repo> --texts <json list of
[label, text]> --out <json> [--gcc <compiler>] [--patch <json> ...]"""
import argparse, json, re, subprocess, sys, tempfile, types
from pathlib import Path
from unittest.mock import patch

ANCHOR = "    subset_note = assert_subset_refuses()\n"
INT_RE = re.compile(r"\bint\s+(\w+)\s*;", re.ASCII)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", type=Path, required=True)
    ap.add_argument("--texts", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--gcc")
    ap.add_argument("--patch", type=Path, action="append", default=[])
    a = ap.parse_args()
    tree = a.tree.resolve()
    path = tree / "sw/builder/test_builder.py"
    src = path.read_text(encoding="utf-8")
    for pf in a.patch:
        for old, new in json.loads(pf.read_text(encoding="utf-8")):
            assert src.count(old) == 1, old
            src = src.replace(old, new, 1)
    assert src.count(ANCHOR) == 1
    src = src.replace(ANCHOR, "    if _R272_HOOK is not None:\n"
                      "        return _R272_HOOK(locals())\n" + ANCHOR, 1)
    texts = json.loads(a.texts.read_text(encoding="utf-8"))
    rows = []

    def hook(ns):
        for label, text in texts:
            try:
                ns["assert_within_lexical_subset"](text)
                s = "admitted"
            except AssertionError as exc:
                s = "refused: " + str(exc)[:120]
            try:
                r = ns["lexer_readers"]["keeps"](text)
            except Exception as exc:
                r = ["EXC", type(exc).__name__]
            rows.append({"label": label, "text": text, "S": s,
                         "reader": r})
    sys.path.insert(0, str(tree / "scripts"))
    sys.path.insert(0, str(tree / "sw/builder"))
    mod = types.ModuleType("test_builder")
    mod.__file__ = str(path)
    mod._R272_HOOK = hook
    sys.modules["test_builder"] = mod
    exec(compile(src, str(path), "exec"), mod.__dict__)
    import test_firmware_compiler as tfc
    with tempfile.TemporaryDirectory() as tmp:
        with (Path(tmp) / "a.jsonl").open("w") as st:
            au = tfc.CompilerAudit(st, None)
            with patch.object(subprocess, "run", side_effect=au.invoke), \
                    patch.object(sys, "argv", [str(path)]), \
                    patch.object(mod, "OUT", Path(tmp)), \
                    patch.object(mod, "SKIPPED", []):
                mod.test_baremetal_profile_contract()
    if a.gcc:
        for row in rows:
            with tempfile.TemporaryDirectory() as tmp:
                f = Path(tmp) / "t.c"
                f.write_bytes(row["text"].encode("utf-8", "surrogateescape"))
                run = subprocess.run([a.gcc, "-std=gnu99", "-E", "-P", str(f)],
                                     capture_output=True)
            row["gcc"] = None if run.returncode else list(INT_RE.findall(
                run.stdout.decode("utf-8", "replace")))
    for row in rows:
        row["reader"] = None if row["reader"] is None else list(row["reader"])
        print(json.dumps({k: row[k] for k in row if k != "text"}))
    a.out.write_text(json.dumps(rows, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
