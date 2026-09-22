"""Shared helpers for R220-2 probes: load a ci_events.py revision as a module
from git (never from the working tree unless asked), and read a tree's
workflow/policy files from a git revision into memory.

All probes are read-only against the review clone: they read git objects
with `git show`/`git cat-file` and write only under the receipts directory
or a TemporaryDirectory.
"""
from __future__ import annotations

import atexit
import importlib.util
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

CLONE = pathlib.Path(os.environ.get("R220_CLONE", "$VALIDATION_STORAGE/reviews/r220-505-r2"))
BASE = "b17580b91deb11f3441dfc5d7f9fafe539d929b8"
R1 = "6af65a151663e1301f1983a6c9d22650a0b35da9"
HEAD = "ad62493186576144f9fa1568babad012bc9ad8ca"
SCRATCH_AC5 = "66ba210630ff7f412e5706427b3ea976ebee3ba2"

_TMP = tempfile.mkdtemp(prefix="r220-2-mods-")
atexit.register(shutil.rmtree, _TMP, ignore_errors=True)


def git(*args: str, text: bool = True) -> str | bytes:
    out = subprocess.run(["git", "-C", str(CLONE), *args], check=True,
                         capture_output=True)
    return out.stdout.decode("utf-8") if text else out.stdout


def show(rev: str, path: str) -> str:
    return git("show", f"{rev}:{path}")


def load_module(rev: str, name: str | None = None, source: str | None = None):
    """Import scripts/ci_events.py at `rev` (or the given source text) as a
    fresh module. ROOT inside the module is irrelevant: probes pass worlds
    or --root explicitly."""
    name = name or f"ci_events_{rev[:8]}"
    text = source if source is not None else show(rev, "scripts/ci_events.py")
    path = pathlib.Path(_TMP) / f"{name}.py"
    path.write_text(text, encoding="utf-8")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def tree_texts(mod, rev: str) -> dict[str, str]:
    """The files read_tree would return, read from git at `rev` instead of
    the working tree: every workflow file plus the policy page."""
    names = git("ls-tree", "-r", "--name-only", rev, "--", ".github/workflows").split()
    out = {n: show(rev, n) for n in names if n.endswith((".yml", ".yaml"))}
    out[mod.POLICY] = show(rev, mod.POLICY)
    return out


def world_at(mod, rev: str):
    return mod.parse_world(tree_texts(mod, rev))
