#!/usr/bin/env python3
"""Round 3 delta checks: syntax delta, the banner arms' real line numbers, the digest table, natural duplicates.

Usage: delta_checks_r787_3.py PRIOR.py HEAD.py REPO WORKDIR
"""
from __future__ import annotations

import ast
import difflib
import hashlib
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile

GROUP = 'grouped.setdefault(lanes[finding.page], []).append((finding, line))'


def names(path: pathlib.Path) -> dict[str, str]:
    """Each top-level name's dumped syntax, docstrings included."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out = {}
    for node in tree.body:
        name = getattr(node, "name", None)
        if name is None and isinstance(node, (ast.Assign, ast.AnnAssign)):
            target = node.targets[0] if isinstance(node, ast.Assign) else node.target
            name = getattr(target, "id", None)
        if name:
            out[name] = ast.dump(node)
    return out


def function(path: pathlib.Path, name: str) -> list[str]:
    """One function, unparsed with one needle or arm per line, so layout cannot show."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    node = next(n for n in tree.body if getattr(n, "name", None) == name)
    return ast.unparse(node).replace("), (", "),\n(").split("\n")


def load(path: pathlib.Path):
    """The module at `path`, without running its main."""
    spec = importlib.util.spec_from_file_location("inventory_under_probe", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def table_digests(repo: pathlib.Path) -> None:
    """Every path and sha256 pair of the command table against the bytes of that path."""
    table = json.loads((repo / "ci/image/command-table.json").read_text(encoding="utf-8"))
    pairs: list[tuple[str, str]] = []

    def walk(node: object) -> None:
        """Collect each object key naming a repository path whose value holds a sha256."""
        if isinstance(node, dict):
            for key, value in node.items():
                if isinstance(value, dict) and isinstance(value.get("sha256"), str) and "/" in key:
                    pairs.append((key, value["sha256"]))
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(table)
    bad = []
    missing = []
    for path, digest in pairs:
        target = repo / path
        if not target.is_file():
            missing.append(path)
        elif hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            bad.append(path)
    print(f"command table: {len(pairs)} path digests, {len(bad)} wrong, {len(missing)} not in this clone")
    print("  wrong:", bad[:10])
    print("  absent:", missing[:10])
    print("  docs_inventory entry present:", any(p == "scripts/docs_inventory.py" for p, _ in pairs))


def banner_lines(head: pathlib.Path) -> None:
    """Where the two banner arms really put their banner."""
    module = load(head)
    banner = "\n> Superseded by [A](A.md).\n"
    for label, pad in (("read arm", 10), ("not-read arm", 11)):
        with tempfile.TemporaryDirectory() as scratch:
            root = pathlib.Path(scratch)
            assert module.fixture(root) is None
            module.append("docs/guides/B.md", "\n" * pad + banner)(root)
            lines = (root / "docs/guides/B.md").read_text(encoding="utf-8").split("\n")
            print(f"{label}: banner on line {lines.index('> Superseded by [A](A.md).') + 1}")


def natural_duplicates(head: pathlib.Path, work: pathlib.Path) -> None:
    """A copy filed under both its own lane and its origin's lane, in `located` order."""
    source = head.read_text(encoding="utf-8")
    assert source.count(GROUP) == 1
    variants = {
        "LD4 a copy filed in its own lane and its origin's lane": (
            'for page in dict.fromkeys((finding.page, finding.origin or finding.page)):\n'
            '            grouped.setdefault(lanes[page], []).append((finding, line))'),
        "LD5 a copy filed in its origin's lane as well, origin first": (
            'for page in dict.fromkeys((finding.origin or finding.page, finding.page)):\n'
            '            grouped.setdefault(lanes[page], []).append((finding, line))'),
    }
    for index, (name, text) in enumerate(variants.items()):
        target = work / f"dup{index}" / "scripts" / "docs_inventory.py"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(source.replace(GROUP, text), encoding="utf-8")
        done = subprocess.run([sys.executable, "-I", str(target), "--selftest"], capture_output=True, text=True,
                              check=False, cwd=work)
        state = "SURVIVED" if done.returncode == 0 else "KILLED"
        first = next((line[15:110] for line in done.stdout.splitlines() if line.startswith("selftest: FAIL")),
                     done.stderr.strip()[-120:])
        print(f"{state} rc={done.returncode} {name} :: {first!r}")


def main() -> int:
    """Run the checks."""
    prior, head = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    repo, work = pathlib.Path(sys.argv[3]), pathlib.Path(sys.argv[4])
    before, after = names(prior), names(head)
    same = [n for n in before if after.get(n) == before[n]]
    print(f"identical top-level names: {len(same)}; changed: {sorted(n for n in before if n not in same)}; "
          f"added {sorted(set(after) - set(before))}")
    for name in ("control", "copy_controls", "selftest"):
        print(f"--- layout-free diff of {name}")
        for line in difflib.unified_diff(function(prior, name), function(head, name), lineterm="", n=0):
            if not line.startswith(("---", "+++", "@@")):
                print(line[:260])
    banner_lines(head)
    table_digests(repo)
    natural_duplicates(head, work)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
