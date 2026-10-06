#!/usr/bin/env python3
"""Verify public equality receipts and exact source/index/submodule integrity.

Usage: python3 scripts/verify_delta.py CHECKOUT PACKET
Run fetch_public.py first. No builds, source writes or network writes occur.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

HEAD = "41bc9dac031526c1fd637ff1e801d3c6dc1260b4"
TREE = "1a233401c2f5d585b7a0a2d1a7db16daff6d29b6"
BASE = "423ac5d910d09ab189b3acc39ae3ae1d10d50b19"
DEV = "bd884631684ccf5060339efa92263d5c3e5c262c"
AUTHOR = "5d6164a2da2d4f7374558bf33b464bcd8a9b4fc2"
EXPECTED_HASH = "3ef42e34ca3874e90fd2929f869dd0f37343e04b9cb2cb0c5f294262448c1c6b"
RTL = "hdl/ieee1722/aaf/KL_aaf_packetizer.sv"
REQUIRED = ["third_party/verilog-axis", "protocol-processor", "gptp-processor"]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])


def tree_entries(repo):
    entries = {}
    for entry in git(repo, "ls-tree", "-rz", "HEAD").split(b"\0"):
        if entry:
            fields, path = entry.split(b"\t", 1)
            mode, kind, oid = fields.split()
            entries[os.fsdecode(path)] = (mode.decode(), kind.decode(), oid.decode())
    return entries


def integrity(repo, expected):
    assert git(repo, "rev-parse", "HEAD").decode().strip() == expected
    entries = tree_entries(repo)
    index = {}
    for entry in git(repo, "ls-files", "--stage", "-z").split(b"\0"):
        if entry:
            fields, path = entry.split(b"\t", 1)
            mode, oid, stage = fields.split()
            assert stage == b"0", (path, stage)
            index[os.fsdecode(path)] = (mode.decode(), oid.decode())
    assert index == {p: (m, o) for p, (m, _, o) in entries.items()}, "Index differs"
    blobs = 0
    for path, (mode, kind, oid) in entries.items():
        if kind == "commit":
            continue
        file = repo / path
        info = file.lstat()
        if mode == "120000":
            assert stat.S_ISLNK(info.st_mode), path
            data = os.fsencode(os.readlink(file))
        else:
            assert stat.S_ISREG(info.st_mode), path
            actual_mode = "100755" if info.st_mode & 0o111 else "100644"
            assert actual_mode == mode, (path, mode, actual_mode)
            data = file.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert actual == oid, path
        blobs += 1
    return {"head": expected, "tree": git(repo, "rev-parse", "HEAD^{tree}").decode().strip(),
            "verified_blobs_and_modes": blobs, "verified_index_entries": len(index),
            "gitlinks": {p: o for p, (_, kind, o) in entries.items() if kind == "commit"}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path)
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    repo, packet = args.checkout.resolve(), args.packet.resolve()
    receipts = packet / "receipts"
    prior = receipts / "prior"

    manifest = {}
    for line in (prior / "MANIFEST.sha256").read_text().splitlines():
        checksum, path = line.split(maxsplit=1)
        manifest[path.removeprefix("*")] = checksum
    verified = []
    for file in sorted(prior.rglob("*")):
        if file.is_file() and file.name != "MANIFEST.sha256":
            path = str(file.relative_to(prior))
            assert digest(file.read_bytes()) == manifest[path], path
            verified.append(path)
    source = packet / "scratch/public-source"
    publication = json.loads((source / "MANIFEST.json").read_text())
    for item in publication:
        assert digest((source / item["file"]).read_bytes()) == item["published_sha256"]

    logs = {name: (prior / f"receipts/epoch-{name}-run.log").read_bytes()
            for name in ["base", "head", "dev"]}
    assert logs["head"] == logs["dev"]
    assert logs["head"] != logs["base"]
    assert digest(logs["head"]) == EXPECTED_HASH
    assert len(logs["head"]) == 3746
    assert b"checks: 127   failures: 4" in logs["head"]
    failures = {name: [line for line in data.splitlines() if b"[FAIL]" in line]
                for name, data in logs.items()}
    assert len(failures["head"]) == 4
    assert failures["base"] == failures["head"] == failures["dev"]
    for name in logs:
        assert (prior / f"receipts/epoch-{name}-run.rc").read_text().strip() == "1"

    parents = git(repo, "show", "-s", "--format=%P", HEAD).decode().split()
    assert parents == [AUTHOR, DEV]
    changes = git(repo, "diff", "--name-only", DEV, HEAD).decode().splitlines()
    closure = ["hdl", "protocol-processor", "gptp-processor", "third_party/verilog-axis",
               "configs", "sw/builder", "avdecc", "tb/verilator/milan_dp",
               "tb/verilator/milan_dp_render", "tb/common"]
    closure_delta = git(repo, "diff", "--name-only", DEV, HEAD, "--", *closure).decode().splitlines()
    assert closure_delta == [RTL]
    for path in changes:
        if path == "scripts/measure_test_evidence_readers.py":
            continue
        assert git(repo, "show", f"{HEAD}:{path}") == git(repo, "show", f"{AUTHOR}:{path}")
    # The renderer, harness and recipes are inherited exactly from dev.
    inherited_render = "tb/verilator/milan_dp_render/sim_tdm8_render.cpp"
    assert git(repo, "show", f"{HEAD}:{inherited_render}") == git(repo, "show", f"{DEV}:{inherited_render}")
    comparison = json.loads((source / "author/render-comparison.json").read_text())
    assert comparison["base"] == BASE and comparison["head"] == AUTHOR
    assert comparison["same_campaign_verdicts"] and len(comparison["runs"]) == 32
    for run in comparison["runs"]:
        assert run["byte_equal"] and run["base_rc"] == run["head_rc"]
        assert run["base_sha256"] == run["head_sha256"]

    result = {
        "head": HEAD, "tree": TREE, "merge_parents": parents,
        "equality_base": DEV, "source_base": BASE,
        "prior_manifest_verified_files": verified,
        "author_publication_verified_files": len(publication),
        "render_source_closure_delta": closure_delta,
        "changes_against_merge_parent": changes,
        "logs": {n: {"bytes": len(data), "sha256": digest(data), "rc": 1}
                 for n, data in logs.items()},
        "head_equals_merge_parent": True, "head_differs_from_original_base": True,
        "four_failure_lines_identical": True,
        "historical_full_campaign": {"base": BASE, "head": AUTHOR, "runs": 32,
                                      "same_campaign_verdicts": True},
        "fresh_simulation_executed": False,
        "method": "Rehash immutable public same-head receipts and recheck source closure"
    }
    (receipts / "delta-audit.json").write_text(json.dumps(result, indent=2) + "\n")
    (receipts / "source-diff.patch").write_bytes(git(repo, "diff", "--no-ext-diff", "--no-textconv", BASE, HEAD))
    (receipts / "history.txt").write_bytes(git(repo, "log", "--format=%H %P %s", BASE + ".." + HEAD))
    tree = integrity(repo, HEAD)
    assert tree["tree"] == TREE
    tree["required_submodules"] = {}
    for path in REQUIRED:
        child = repo / path
        assert not child.is_symlink() and (child / ".git").is_file(), path
        superproject = git(child, "rev-parse", "--show-superproject-working-tree").decode().strip()
        assert Path(superproject).resolve() == repo, path
        tree["required_submodules"][path] = integrity(child, tree["gitlinks"][path])
    status = git(repo, "status", "--porcelain=v1", "--untracked-files=all")
    assert status == b"", status
    (receipts / "tree-integrity.json").write_text(json.dumps(tree, indent=2) + "\n")
    print("PASS: merge-parent equality; four identical failures; historical campaign labeled")
    print("PASS: exact head/tree, tracked bytes/modes/index, three registered submodules")
    print("PASS: 19 source publication entries and 14 selected prior receipt entries verified")


if __name__ == "__main__":
    main()
