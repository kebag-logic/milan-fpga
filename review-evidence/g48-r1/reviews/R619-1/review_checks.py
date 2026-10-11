#!/usr/bin/env python3
"""Reproduce focused documentation review checks without editing the checkout."""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

HEAD = "7cc9c492145dd9e7c5c0e1d4695a261ea8025850"
TREE = "fba21199f65fb1fc9963314495f74a5c42309b18"
BASE = "bd466e60074539a7147e3d1613c9dcb0f93e2544"
PARENT = "ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5"
PREFIX = "https://github.com/kebag-logic/milan-fpga/blob/"
URL = re.compile(re.escape(PREFIX) + r"([^/)]+)/([^#)\s]+)#L(\d+)(?:-L(\d+))?")
OFF = re.compile(r"default(?:s|ed)?[\s`*_-]*(?:to[\s`*_-]*)?(?:off|disabled|0)\b|(?:off|disabled)[\s`*_-]+by[\s`*_-]+default", re.I)
CHANGED = {"README.md", "docs/INTEGRATION.md", "docs/MANAGER.md", "docs/SOURCE_EVIDENCE.md", "docs/history/v1/PROJECT_STATUS.md"}


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])


def integrity(repo):
    assert git(repo, "rev-parse", "HEAD").decode().strip() == HEAD
    assert git(repo, "rev-parse", "HEAD^{tree}").decode().strip() == TREE
    assert git(repo, "diff", "--raw", "HEAD") == b""
    assert git(repo, "diff", "--cached", "--raw", "HEAD") == b""
    assert git(repo, "status", "--porcelain=v1") == b""
    entries = []
    links = []
    for record in git(repo, "ls-tree", "-rz", "HEAD").split(b"\0"):
        if not record:
            continue
        metadata, rawpath = record.split(b"\t", 1)
        mode, kind, oid = metadata.decode().split()
        name = os.fsdecode(rawpath)
        path = repo / name
        if mode == "160000":
            links.append({"path": name, "oid": oid})
            assert git(path, "rev-parse", "HEAD").decode().strip() == oid
            continue
        data = os.fsencode(os.readlink(path)) if mode == "120000" else path.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert actual == oid, name
        actual_mode = "120000" if path.is_symlink() else ("100755" if path.stat().st_mode & 0o111 else "100644")
        assert actual_mode == mode, name
        entries.append({"path": name, "mode": mode, "blob": oid, "sha256": hashlib.sha256(data).hexdigest()})
    expected_index = git(repo, "ls-tree", "-r", "HEAD").decode().splitlines()
    index = git(repo, "ls-files", "--stage").decode().splitlines()
    assert [x.replace(" blob ", " ").replace(" commit ", " ") for x in expected_index] == [x.replace(" 0\t", "\t") for x in index]
    assert not links and not (repo / ".gitmodules").exists()
    return {"head": HEAD, "tree": TREE, "clean": True, "tracked_count": len(entries), "required_gitlinks": links, "index_matches_tree": True, "entries": entries}


def citations(pages, authorities):
    found = []
    for name, body in pages.items():
        for number, line in enumerate(body.splitlines(), 1):
            for m in URL.finditer(line):
                revision, path, begin, end = m.groups()
                assert revision == PARENT, (name, number, "wrong parent revision")
                target = authorities / path.replace("/", "__")
                assert target.is_file(), (name, number, "missing target", path)
                lines = target.read_text().splitlines()
                start, stop = int(begin), int(end or begin)
                assert 1 <= start <= stop <= len(lines), (name, number, "invalid line range")
                found.append({"source": name, "line": number, "claim": line, "url": m.group(), "target": path, "first": start, "last": stop, "excerpt": "\n".join(f"{i}: {lines[i-1]}" for i in range(start, stop+1))})
    assert len(found) == 31, len(found)
    assert len({x["url"] for x in found}) == 14
    return found


def stale(pages):
    return [(name, body.count("\n", 0, match.start()) + 1, match.group())
            for name, body in pages.items() if not name.startswith("docs/history/")
            for match in OFF.finditer(body)]


def audit(repo, packet):
    receipts = packet / "receipts"
    identity = integrity(repo)
    (receipts / "integrity.json").write_text(json.dumps(identity, indent=2) + "\n")
    changed = set(git(repo, "diff", "--name-only", BASE, HEAD).decode().splitlines())
    assert changed == CHANGED, changed
    assert git(repo, "rev-list", "--count", f"{BASE}..{HEAD}").decode().strip() == "1"
    subject = git(repo, "show", "-s", "--format=%B", HEAD).decode().strip()
    assert len(subject.splitlines()) == 1
    subprocess.run(["git", "-C", str(repo), "diff", "--check", BASE, HEAD], check=True)
    pages = {name: (repo / name).read_text() for name in git(repo, "ls-files", "*.md").decode().splitlines()}
    current = [name for name in pages if not name.startswith("docs/history/")]
    assert not stale(pages)
    found = citations(pages, receipts / "authorities")
    (receipts / "citations.json").write_text(json.dumps(found, indent=2) + "\n")
    print(f"PASS: {len(found)} parent citations, {len({x['url'] for x in found})} exact targets")
    print(f"PASS: {len(current)} current Markdown pages scanned; no default-off claim")
    print("Current page set: " + ", ".join(current))
    note_start = "> Integration note (2026-10-11, issue #48):"
    historical = "docs/history/v1/PROJECT_STATUS.md"
    old = git(repo, "show", f"{BASE}:{historical}").decode()
    new = pages[historical]
    start = new.index(note_start)
    end = new.index("\n\n", start) + 2
    assert new[:start] + new[end:] == old
    print("PASS: dated history differs only by forward note; original bytes retained")
    for phrase in ["defaults off", "defaults to off", "default-off", "disabled by default", "default disabled", "defaults to 0", "defaults\noff"]:
        mutant = dict(pages)
        mutant["README.md"] += "\nParent GPTP_PLANE_EN_P " + phrase + ".\n"
        assert stale(mutant), phrase
        print("DETECTED stale-default mutation: " + repr(phrase))
    victim = found[0]["url"]
    for label, replacement in [
        ("wrong revision", victim.replace(PARENT, BASE)),
        ("missing file", victim.replace("milan_datapath.sv", "missing.sv")),
        ("zero line", victim.replace("#L73", "#L0")),
        ("past EOF", victim.replace("#L73", "#L999999")),
    ]:
        mutant = dict(pages)
        mutant[found[0]["source"]] = mutant[found[0]["source"]].replace(victim, replacement, 1)
        try:
            citations(mutant, receipts / "authorities")
        except AssertionError:
            print("DETECTED citation mutation: " + label)
        else:
            raise AssertionError(label + " escaped")
    # A valid line number can still cite unrelated text; retain that limit explicitly.
    mutant = dict(pages)
    mutant[found[0]["source"]] = mutant[found[0]["source"]].replace(victim, victim.replace("#L73", "#L1"), 1)
    try:
        citations(mutant, receipts / "authorities")
    except AssertionError:
        print("Valid-but-wrong anchor also changes the expected target inventory; semantic inspection still required")
    print("LIMIT: line resolution alone cannot establish semantic support; inspect every unique excerpt")
    print(f"PASS: {len(changed)} Markdown-only files; one single-line commit subject: {subject}")
    print(f"PASS: {identity['tracked_count']} tracked blobs and modes match; index matches; zero nested gitlinks")


def gates(repo, packet, jobs):
    def run(target):
        tmp = packet / "scratch" / target
        tmp.mkdir(parents=True, exist_ok=True)
        env = dict(os.environ, TMPDIR=str(tmp), PYTHONDONTWRITEBYTECODE="1")
        command = ["make", "-j16", target]
        with (packet / "receipts" / (target + ".log")).open("w") as stream:
            stream.write("Command: " + " ".join(command) + "\nHead: " + HEAD + "\n")
            stream.flush()
            result = subprocess.run(command, cwd=repo, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=300)
        (packet / "receipts" / (target + ".rc")).write_text(str(result.returncode) + "\n")
        return target, result.returncode
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(jobs, 2)) as executor:
        results = list(executor.map(run, ["docs", "diagrams-check"]))
    for target, rc in results:
        print(f"{target}: rc {rc}")
        assert rc == 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["audit", "gates", "integrity"])
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--packet", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--jobs", type=int, default=2)
    args = parser.parse_args()
    assert 1 <= args.jobs <= 16
    args.repo, args.packet = args.repo.resolve(), args.packet.resolve()
    if args.mode == "gates":
        gates(args.repo, args.packet, args.jobs)
    elif args.mode == "audit":
        audit(args.repo, args.packet)
    else:
        result = integrity(args.repo)
        (args.packet / "receipts" / "final-integrity.json").write_text(json.dumps(result, indent=2) + "\n")
        print(f"PASS: exact head/tree; {result['tracked_count']} raw blobs/modes; index; zero nested gitlinks; clean worktree")


if __name__ == "__main__":
    main()
