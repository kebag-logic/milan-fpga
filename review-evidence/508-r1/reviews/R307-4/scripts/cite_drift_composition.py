#!/usr/bin/env python3
"""Composition citation-drift probe.

For every unpinned `path:line` / `path#Lline` citation in the candidate tree
that points into a file the merge's two sides changed (either side), compare
the cited line's text in the candidate with the text the SAME citation named
in each parent that already carried it. A citation whose candidate text
differs from EVERY carrying parent's was moved by the merge itself: neither
source review saw that state (DRIFT). One whose candidate text equals some
carrying parent's shows a state that source head already had (INHERITED).

Processor-submodule targets are read through each side's own gitlink.

Usage: cite_drift_composition.py <clone> <base> <parent1> <parent2> <candidate>
Exit 1 when any citation drifted under the merge.
"""
import re
import subprocess
import sys
from pathlib import Path

CITE = re.compile(
    r"(?<![\w/.-])((?:\.\./|\./)*[\w][\w./-]*\.(?:sv|svh|cpp|h|hpp|c|py|md|sh|v|tcl|mk|txt|yml|yaml))"
    r"(?::|#L)(\d+)(?:[-–]L?(\d+))?")
PINNED = re.compile(r"/blob/[0-9a-f]{7,40}/")
TEXT_EXT = (".md", ".sv", ".svh", ".cpp", ".h", ".c", ".py", ".sh", ".txt",
            "Makefile", ".yml", ".tcl")


def git(clone: Path, *args: str) -> str:
    """stdout of a git command in `clone` (empty on failure)."""
    out = subprocess.run(["git", "-C", str(clone), *args], capture_output=True,
                         text=True, check=False)
    return out.stdout if out.returncode == 0 else ""


def blob_lines(clone: Path, rev: str, path: str) -> list[str] | None:
    """Lines of `path` at `rev`, following the processor gitlink."""
    if path.startswith("protocol-processor/"):
        pin = git(clone, "rev-parse", f"{rev}:protocol-processor").strip()
        text = git(clone / "protocol-processor", "show",
                   f"{pin}:{path[len('protocol-processor/'):]}")
    else:
        text = git(clone, "show", f"{rev}:{path}")
    return text.splitlines() if text else None


def main() -> int:
    """Scan, compare, report."""
    clone = Path(sys.argv[1])
    base, p1, p2, cand = sys.argv[2:6]
    changed: set[str] = set()
    for side in (p1, p2):
        changed |= set(git(clone, "diff", "--name-only", base, side).split())
    pp_changed = set()
    for side in (p1, p2):
        a = git(clone, "rev-parse", f"{base}:protocol-processor").strip()
        b = git(clone, "rev-parse", f"{side}:protocol-processor").strip()
        if a != b:
            pp_changed |= {"protocol-processor/" + f for f in git(
                clone / "protocol-processor", "diff", "--name-only", a, b).split()}
    targets = changed | pp_changed
    by_base: dict[str, list[str]] = {}
    for t in targets:
        by_base.setdefault(Path(t).name, []).append(t)
    files = [f for f in git(clone, "ls-tree", "-r", "--name-only", cand).split()
             if f.endswith(TEXT_EXT)]
    drift, same, checked = [], 0, 0
    inherited = []
    for f in files:
        text = git(clone, "show", f"{cand}:{f}")
        for ln, line in enumerate(text.splitlines(), 1):
            for m in CITE.finditer(line):
                if PINNED.search(line[:m.start()][-60:]):
                    continue
                raw, lo = m.group(1), int(m.group(2))
                hi = int(m.group(3)) if m.group(3) else lo
                if raw.startswith(("../", "./")):
                    tgt = str((Path(f).parent / raw).resolve().relative_to(
                        clone.resolve())) if (clone / Path(f).parent / raw).exists() else None
                    cands = [tgt] if tgt in targets else []
                elif raw in targets:
                    cands = [raw]
                else:
                    cands = by_base.get(Path(raw).name, []) if "/" not in raw else [
                        t for t in targets if t.endswith("/" + raw)]
                if len(cands) != 1:
                    continue
                tgt = cands[0]
                checked += 1
                cl = blob_lines(clone, cand, tgt)
                if cl is None or hi > len(cl):
                    drift.append((f, ln, m.group(0), tgt, "candidate: beyond EOF", ""))
                    continue
                now = cl[lo - 1:hi]
                seen = {}
                for par in (p1, p2):
                    ptext = git(clone, "show", f"{par}:{f}")
                    if m.group(0) not in ptext:
                        continue
                    pl = blob_lines(clone, par, tgt)
                    seen[par[:8]] = pl[lo - 1:hi] if pl and hi <= len(pl) else None
                if not seen:
                    continue
                if any(v == now for v in seen.values()):
                    same += 1
                    inherited.extend(
                        (f, ln, m.group(0), tgt, f"differs at {k}") for k, v in seen.items()
                        if v != now)
                else:
                    drift.append((f, ln, m.group(0), tgt,
                                  "candidate text differs from every carrying parent",
                                  f"parents={seen!r:.200} now={now!r:.160}"))
    for d in inherited:
        print("INHERITED (the candidate shows exactly one source head's state)", *d, sep=" | ")
    for d in drift:
        print("DRIFT", *d, sep=" | ")
    print(f"citations into changed files checked: {checked}; parent-carried citation "
          f"sites whose candidate text equals some carrying parent's: {same} "
          f"(of which {len(inherited)} differ at the other parent); "
          f"drifted by the merge itself: {len(drift)}")
    return 1 if drift else 0


if __name__ == "__main__":
    sys.exit(main())
