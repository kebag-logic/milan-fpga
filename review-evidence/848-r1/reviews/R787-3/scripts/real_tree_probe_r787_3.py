#!/usr/bin/env python3
"""Real-tree probes for round 3: lane routing, the banner edges, and what the two lane survivors reach.

Usage: real_tree_probe_r787_3.py CLONE WORKDIR
CLONE is a disposable clone at the exact head; every edit is made there or in a copy under WORKDIR.
"""
from __future__ import annotations

import importlib.util
import pathlib
import re
import shutil
import subprocess
import sys

GROUP = 'grouped.setdefault(lanes[finding.page], []).append((finding, line))'
ARCH = '(r"docs/history/.*", "archive"),'


def load(path: pathlib.Path):
    """The module at `path`, without running its main."""
    spec = importlib.util.spec_from_file_location("inventory_under_probe", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def run(*argv: str, cwd: pathlib.Path) -> subprocess.CompletedProcess:
    """One command, captured."""
    return subprocess.run(list(argv), cwd=cwd, capture_output=True, text=True, check=False)


def lanes_of(script: pathlib.Path, out: pathlib.Path, cwd: pathlib.Path) -> dict[str, list[str]]:
    """The entries of each lane file a fresh --findings-dir run writes."""
    shutil.rmtree(out, ignore_errors=True)
    done = run(sys.executable, "-I", str(script), "--findings-dir", str(out), cwd=cwd)
    assert done.returncode == 0, done.stderr
    found = {}
    for page in sorted(out.glob("*.md")):
        found[page.stem] = re.findall(r"^## (D0-\d+): (.+?):(?:\d+|\?)$", page.read_text(encoding="utf-8"), re.M)
    return found


def report_routing(label: str, found: dict, module) -> None:
    """How many entries sit in the file of their page's lane."""
    wrong = 0
    total = 0
    for stem, entries in found.items():
        for _, page in entries:
            total += 1
            own = re.sub(r"[^a-z0-9]+", "-", module.first_match(module.LANES, page).lower()).strip("-")
            wrong += own != stem
    sizes = {stem: len(entries) for stem, entries in found.items()}
    print(f"{label}: files {len(found)} entries {total} outside their lane {wrong} sizes {sizes}")


def main() -> int:
    """Run the probes."""
    clone = pathlib.Path(sys.argv[1]).resolve()
    work = pathlib.Path(sys.argv[2]).resolve()
    work.mkdir(parents=True, exist_ok=True)
    script = clone / "scripts/docs_inventory.py"
    module = load(script)
    print("head", run("git", "rev-parse", "HEAD", cwd=clone).stdout.strip())
    print("unmodified --check rc", run(sys.executable, "-I", str(script), "--check", cwd=clone).returncode)

    report_routing("head", lanes_of(script, work / "lanes-head", clone), module)

    source = script.read_text(encoding="utf-8")
    assert source.count(GROUP) == 1 and source.count(ARCH) == 1
    mutants = {
        "LF8 archive filed in overview at filing": source.replace(GROUP, (
            'grouped.setdefault("overview and guides" if lanes[finding.page] == "archive" else lanes[finding.page], [])'
            '.append((finding, line))')),
        "LF9 archive routed to overview in the table": source.replace(ARCH, '(r"docs/history/.*", "overview and guides"),'),
    }
    for index, (name, text) in enumerate(mutants.items()):
        script.write_text(text, encoding="utf-8")
        checked = run(sys.executable, "-I", str(script), "--check", cwd=clone)
        print(f"{name}: --check rc {checked.returncode} :: {checked.stdout.splitlines()[0][:110]}")
        report_routing(name, lanes_of(script, work / f"lanes-m{index}", clone), module)
        script.write_text(source, encoding="utf-8")

    print("banner edges through status(), no page involved:")
    for line in (1, 14, 15, 16, 17):
        text = "\n" * (line - 1) + "> Superseded by [A](A.md).\n"
        print(f"  banner on line {line}: {module.status(text, 'docs/guides/B.md', {})[0]}")

    page = clone / "docs/guides/QUICKSTART.md"
    target = page if page.is_file() else next(p for p in sorted((clone / "docs").rglob("*.md"))
                                              if "history" not in str(p) and "AUDIT" not in p.name
                                              and p.read_text(encoding="utf-8").count("\n") > 40)
    original = target.read_text(encoding="utf-8")
    lines = original.split("\n")
    print("banner edges on real page", target.relative_to(clone))
    for line in (15, 16):
        changed = lines[:line - 1] + ["> Superseded by [A](A.md)."] + lines[line - 1:]
        target.write_text("\n".join(changed), encoding="utf-8")
        checked = run(sys.executable, "-I", str(script), "--check", cwd=clone)
        print(f"  inserted on line {line}: --check rc {checked.returncode}")
        target.write_text(original, encoding="utf-8")

    pages = run("git", "ls-files", "*.md", cwd=clone).stdout.split()
    saved = {path: (clone / path).read_bytes() for path in pages if (clone / path).is_file()}
    for path in saved:
        if path != module.OUTPUT:
            with (clone / path).open("a", encoding="utf-8") as handle:
                handle.write("Added line.\n")
    print("one line appended to", len(saved) - 1, "tracked pages: --check rc",
          run(sys.executable, "-I", str(script), "--check", cwd=clone).returncode)
    for path, data in saved.items():
        (clone / path).write_bytes(data)
    print("restored --check rc", run(sys.executable, "-I", str(script), "--check", cwd=clone).returncode)
    print("clone dirty entries", len(run("git", "status", "--short", cwd=clone).stdout.splitlines()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
