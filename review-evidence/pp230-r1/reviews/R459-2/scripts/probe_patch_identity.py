#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Is each R458-1 probe (its published probes.py PROBES table, imported, not
run) the same edit as the committed tb/srp_top/mutations patch of that name?
Applies both to the exact head's hdl/srp and compares the edited file bytes.

usage: probe_patch_identity.py PROBES_PY HEAD_TREE
"""
import importlib.util
import pathlib
import shutil
import subprocess
import sys
import tempfile


def main():
    spec = importlib.util.spec_from_file_location("probes", sys.argv[1])
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    head = pathlib.Path(sys.argv[2])
    bad = 0
    for name, (rel, edits) in mod.PROBES.items():
        src = (head / rel).read_text()
        s = src
        for a, b in edits:
            assert s.count(a) == 1, (name, a)
            s = s.replace(a, b)
        with tempfile.TemporaryDirectory() as t:
            t = pathlib.Path(t)
            shutil.copytree(head / "hdl", t / "hdl")
            patch = head / "tb/srp_top/mutations" / f"{name}.patch"
            r = subprocess.run(["git", "apply", str(patch)], cwd=t, capture_output=True, text=True)
            same = r.returncode == 0 and (t / rel).read_text() == s
        bad += not same
        print(f"{name}: {'same edit as the committed patch' if same else 'DIFFERENT'}")
    print(f"{len(mod.PROBES)} probes, {bad} differ")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
