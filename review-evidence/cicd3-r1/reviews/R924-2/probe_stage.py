#!/usr/bin/env python3
"""R924: reproduce lock aliases and refused roots in disposable directories."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

PACKET = Path(__file__).resolve().parent
CLONE = Path(sys.argv[1]).resolve()
SCRATCH = PACKET / "scratch"
HOLDER = r'''
import importlib.util,json,os,sys,tempfile
from pathlib import Path
spec=importlib.util.spec_from_file_location("stage",sys.argv[1])
stage=importlib.util.module_from_spec(spec);spec.loader.exec_module(stage)
tempfile.tempdir=None
with stage.directory("review-",parent=sys.argv[2] or None) as p:
    marker=Path(p)/sys.argv[3];marker.write_text(sys.argv[3])
    print(json.dumps({"path":p,"real":str(Path(p).resolve())}),flush=True)
    sys.stdin.readline()
    print(json.dumps({"survived":marker.exists() and marker.read_text()==sys.argv[3]}),flush=True)
'''


def start(module, parent, tmp, token):
    return subprocess.Popen([sys.executable, "-c", HOLDER, str(module), str(parent or ""), token],
                            env={**os.environ, "TMPDIR": str(tmp), "PYTHONDONTWRITEBYTECODE": "1"},
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def finish(proc):
    output, error = proc.communicate("release\n", timeout=10)
    assert proc.returncode == 0, error
    return json.loads(output), error


def collision(module, root, alias):
    tmp1, tmp2, parent = root / "tmp1", root / "tmp2", root / "parent"
    for p in (tmp1, tmp2, parent):
        p.mkdir(mode=0o700)
    if alias:
        tmp2.rmdir(); tmp2.symlink_to(tmp1)
        parent = None
    first = start(module, parent, tmp1, "first")
    a = json.loads(first.stdout.readline())
    second = start(module, parent, tmp2, "second")
    b = json.loads(second.stdout.readline())
    # Release the first while the second still holds, detecting both empty and cleanup collisions.
    alive_a, err_a = finish(first)
    alive_b, err_b = finish(second)
    return {"same_physical_slot": a["real"] == b["real"], "first_survived": alive_a["survived"],
            "second_survived": alive_b["survived"], "stderr": err_a + err_b}


def main():
    result = {"reviewer": "R924", "heads": {}}
    with tempfile.TemporaryDirectory(dir=SCRATCH, prefix="stage-probe-") as name:
        root = Path(name)
        for rev in ("13e6d869", "9c625393"):
            module = root / (rev + ".py")
            module.write_bytes(subprocess.check_output(["git", "show", rev + ":scripts/mutant_stage.py"], cwd=CLONE))
            rows = {}
            for label, alias in (("different_tmpdirs_same_parent", False), ("tmpdir_alias", True)):
                case = root / (rev + label); case.mkdir()
                rows[label] = collision(module, case, alias)
            result["heads"][rev] = rows
        for row in result["heads"]["13e6d869"].values():
            assert row["same_physical_slot"] and not row["first_survived"], row
        for row in result["heads"]["9c625393"].values():
            assert not row["same_physical_slot"] and row["first_survived"] and row["second_survived"], row
        refused = {}
        for label in ("symlink", "writable", "file", "nonsticky"):
            case = root / label; case.mkdir(mode=0o700)
            stage_root = case / f"milan-mutant-stage-{os.getuid()}"
            outside = root / (label + "-outside"); outside.mkdir()
            sentinel = outside / "sentinel"; sentinel.write_text("untouched")
            if label == "symlink": stage_root.symlink_to(outside)
            if label == "writable": stage_root.mkdir(); stage_root.chmod(0o777)
            if label == "file": stage_root.write_text("untouched")
            if label == "nonsticky": case.chmod(0o777)
            proc = start(root / "9c625393.py", None, case, "owner")
            chosen = json.loads(proc.stdout.readline())
            survived, error = finish(proc)
            assert "random private directory" in error, error
            assert survived["survived"] and sentinel.read_text() == "untouched"
            assert not Path(chosen["real"]).is_relative_to(stage_root.resolve())
            refused[label] = {"fallback": True, "own_marker_survived": True, "outside_unchanged": True}
        result["refused_roots"] = refused
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
