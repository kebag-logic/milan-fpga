#!/usr/bin/env python3
"""Read-only M5 delta checks; usage: verify_delta.py REPO PR_JSON."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

sys.dont_write_bytecode = True
HEAD = "2bef9e50489a60f216a8073a9f5ea0645752b33f"
TREE = "9777e890c07850052a0d9134cdb22388a651c5f1"
BASE = "6bfeeb132fa0b1ad8a5b957446c66a498e633af7"
REQUIRED = ("protocol-processor", "gptp-processor", "third_party/verilog-axis")


def git(repo, *args):
    return subprocess.check_output(
        ["git", "--no-replace-objects", "-C", str(repo), *args],
        env={**os.environ, "GIT_NO_REPLACE_OBJECTS": "1"})


def blob_oid(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def verify_tree(repo, revision):
    expected = {}
    links = {}
    count = 0
    for entry in git(repo, "ls-tree", "-rz", "--full-tree", revision).split(b"\0"):
        if not entry:
            continue
        header, name = entry.split(b"\t", 1)
        mode, kind, oid = header.decode().split()
        expected[name] = (mode, oid, "0")
        path = repo / os.fsdecode(name)
        if kind == "commit":
            links[os.fsdecode(name)] = oid
            continue
        info = path.lstat()
        if mode == "120000":
            assert stat.S_ISLNK(info.st_mode), os.fsdecode(name)
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode), os.fsdecode(name)
            actual_mode = "100755" if info.st_mode & 0o111 else "100644"
            assert actual_mode == mode, os.fsdecode(name)
            data = path.read_bytes()
        assert blob_oid(data) == oid, os.fsdecode(name)
        count += 1
    actual = {}
    for entry in git(repo, "ls-files", "--stage", "-z").split(b"\0"):
        if not entry:
            continue
        header, name = entry.split(b"\t", 1)
        assert name not in actual, "multiple index stages"
        actual[name] = tuple(header.decode().split())
    assert actual == expected, "index differs from committed tree"
    print(f"PASS tracked bytes, filesystem modes, index: {count} blobs; {len(links)} gitlinks")
    return links


def check_body(body):
    # The entire body must have no obsolete, unqualified resource figure.
    assert not re.search(r"38,?436|\b396\b", body), "obsolete resource figure"
    for heading in ("## Status", "## Known limitations / out of scope", "## Composition repair"):
        section = body.split(heading, 1)[1].split("\n## ", 1)[0]
        assert all(x in section for x in ("38,784", "744", "38,040")), heading


def main():
    repo = Path(sys.argv[1]).resolve()
    pr = json.loads(Path(sys.argv[2]).read_text())
    assert git(repo, "rev-parse", "HEAD").decode().strip() == HEAD
    assert git(repo, "rev-parse", "HEAD^{tree}").decode().strip() == TREE
    assert pr["head"]["sha"] == HEAD
    assert pr["base"]["sha"] == BASE
    print(f"PASS source head {HEAD}; tree {TREE}; published head and base match")
    links = verify_tree(repo, HEAD)
    for name in REQUIRED:
        sub = repo / name
        assert (sub / ".git").is_file(), f"not a registered submodule: {name}"
        assert git(sub, "rev-parse", "HEAD").decode().strip() == links[name]
        verify_tree(sub, links[name])
        print(f"PASS required submodule {name}: {links[name]}")
    original = git(repo, "show", "e8454e2751d05b02ee8e5a571857589ab358ab86:hdl/common/csr/milan_csr.sv")
    frozen = (repo / "tb/verilator/csr/milan_csr_ref.sv").read_bytes()
    normalized = frozen.replace(b"module milan_csr_ref #(", b"module milan_csr #(")
    assert original == normalized
    print("PASS frozen oracle equals original blob after module-name normalization; sha256 " + hashlib.sha256(original).hexdigest())
    spec = importlib.util.spec_from_file_location("lockgen", repo / "tb/verilator/csr/gen_lockstep.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.checked_reference(frozen.decode())
    try:
        module.checked_reference(frozen.decode() + "\n// planted drift\n")
    except SystemExit:
        print("PASS negative control: reference-byte drift rejected")
    else:
        raise AssertionError("reference-byte drift accepted")
    dut = (repo / "hdl/common/csr/milan_csr.sv").read_text()
    for n in (1, 8):
        params = dict(NUM_QUEUES=5, ADDR_WIDTH=16, GPTP_PLANE_EN_P=1,
                      MILAN_CLK_FREQ_HZ_P=50000000, CHMAP_RDBK_P=3,
                      PPS_P=0, PPS_WIDTH_CYC_P=50000,
                      N_LISTENERS_P=n, N_TALKERS_P=n, SRP_LSN0_ROW_P=2*n)
        ports = module.ports(dut, params)
        assert ports == module.ports(frozen.decode(), params)
        print(f"PASS interface identity at {n}x{n}: {len(ports)} ports")
    assert 37957 + (200 - 34) + (600 - 121) + (600 - 418) == 38784
    assert 38784 - 38040 == 744
    plan = (repo / "docs/design/MARK_II_AREA_PLAN.md").read_text().splitlines()
    for line in (699, 960, 1048, 1106):
        print(f"PLAN {line}: {plan[line-1]}")
    assert all(x in plan[1105] for x in ("M2 (34)", "M5 (121)", "M6 (418)", "38,784", "744", "38,040"))
    check_body(pr["body"])
    print("PASS entire PR body: obsolete resource figures absent; all three current sections agree")
    bad = pr["body"].replace("38,784, 744 over 38,040", "38,436, 396 over 38,040", 1)
    assert bad != pr["body"]
    try:
        check_body(bad)
    except AssertionError:
        print("PASS negative control: obsolete PR figure rejected")
    else:
        raise AssertionError("obsolete PR figure accepted")
    git(repo, "diff", "--check", BASE, HEAD)
    assert not git(repo, "status", "--porcelain", "--untracked-files=no")
    print("PASS diff whitespace and final tracked status")


if __name__ == "__main__":
    main()
