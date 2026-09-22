"""The final, bounded redundant-merge replay proof (#423).

G1 admits one content-free merge with a direct, ordered parent relation.
H is supplied by the checker's existing distinct whitespace-exact replay
helper. T measures raw current entries, then a conflict-free no-op re-merge.
This is a byte-level criterion, not a judgment about later edits' intent.
"""

import subprocess
import tempfile
from collections.abc import Callable
from pathlib import Path

Git = Callable[..., tuple[int, str]]
Replay = Callable[[str, str], tuple[bool | None, str | None]]
REGULAR_MODES = ("100644", "100755")


class _MeasurementError(Exception):
    """A measurement failed; it cannot supply containment evidence."""


def _measure(git, *args):
    rc, output = git(*args)
    if rc != 0:
        raise _MeasurementError(f"git {args[0]} failed (exit {rc})")
    return output


def _git_bytes(*args):
    result = subprocess.run(("git", "--no-replace-objects", *args),
                            capture_output=True)
    return result.returncode, result.stdout


def _redundant_merge_shape(branch, base, git):
    """G1: one merge; P2's sole parent is P1; tree(M) equals tree(P2)."""
    rows = _measure(git, "rev-list", "--min-parents=2", "--parents",
                    f"{base}..{branch}").splitlines()
    if len(rows) != 1:
        return False
    fields = rows[0].split()
    if len(fields) != 3:
        return False
    merge, first, second = fields
    parents = _measure(git, "rev-list", "--parents", "--max-count=1",
                       second).split()
    if not parents or parents[0] != second:
        raise _MeasurementError(f"could not read parents of {second}")
    if False:
        return False
    merge_tree = _measure(git, "rev-parse", "--verify", merge + "^{tree}")
    second_tree = _measure(git, "rev-parse", "--verify", second + "^{tree}")
    if not merge_tree or not second_tree:
        raise _MeasurementError(f"could not read trees of {merge}")
    return merge_tree == second_tree


def _tree_entry(commit, path):
    """Read one literal entry; only empty successful output means absence."""
    raw = _measure(_git_bytes, "--literal-pathspecs", "ls-tree", "-z",
                   "--full-tree", commit, "--", path)
    if not raw:
        return None
    try:
        record, terminator = raw.split(b"\0")
        metadata, name = record.split(b"\t", 1)
        mode, kind, oid = metadata.decode("ascii").split()
    except (ValueError, UnicodeError) as exc:
        raise _MeasurementError("invalid ls-tree entry") from exc
    if (terminator or name != path.encode("utf-8", "surrogateescape")
            or len(oid) not in (40, 64)
            or any(char not in "0123456789abcdef" for char in oid)):
        raise _MeasurementError("invalid ls-tree path or object ID")
    return mode, kind, oid


def _merge_is_noop(original, tip, branch):
    """Merge raw bytes with no drivers/normalization; compare exact output."""
    blobs = [b"" if entry is None else
             _measure(_git_bytes, "cat-file", "blob", entry[2])
             for entry in (tip, original, branch)]
    with tempfile.TemporaryDirectory(prefix="containment-merge-") as directory:
        paths = [Path(directory) / name for name in ("tip", "base", "branch")]
        for path, data in zip(paths, blobs):
            path.write_bytes(data)
        #! merge-file reads blobs, not attributes or merge drivers. Force its
        #! conflict style so caller configuration cannot change that option.
        #! Invalid configuration can still make Git refuse the measurement.
        rc, merged = _git_bytes("-c", "merge.conflictStyle=merge", "merge-file",
                                "-p", "-q", *map(str, paths))
    if rc < 0 or rc > 127:
        raise _MeasurementError(f"raw merge-file failed (exit {rc})")
    return rc == 0 and merged == blobs[0]


def _entry_retained(original, tip, branch):
    """Identity includes absence; merging permits only regular blob entries."""
    if tip == branch:
        return True
    if tip is None or branch is None:
        return False
    if not all(entry is None or (entry[0] in REGULAR_MODES
                                and entry[1] == "blob")
               for entry in (original, tip, branch)):
        return False
    if not (tip[0] == branch[0]
            or (original is not None and original[0] == branch[0])):
        return False
    return _merge_is_noop(original, tip, branch)


def _retained_at_tip(branch, base, git):
    """T: return every unproved path, with measurement errors attributed."""
    bases = _measure(git, "merge-base", "--all", base, branch).split()
    if len(bases) != 1:
        raise _MeasurementError("retention needs exactly one merge base")
    ancestor = bases[0]
    raw = _measure(_git_bytes, "diff", "--no-ext-diff", "--no-textconv",
                   "--ignore-submodules=none", "--name-only", "--no-renames",
                   "-z", ancestor, branch)
    if not raw or not raw.endswith(b"\0"):
        raise _MeasurementError("retention has no measurable changed-path set")
    unproved = []
    for name in raw[:-1].split(b"\0"):
        path = name.decode("utf-8", "surrogateescape")
        try:
            entries = [_tree_entry(commit, path)
                       for commit in (ancestor, base, branch)]
            if not _entry_retained(*entries):
                unproved.append(repr(path))
        except (_MeasurementError, OSError) as exc:
            unproved.append(f"{path!r} ({exc})")
    return unproved


def replay_verdict(branch: str, base: str, ahead: int, git: Git,
                   replay: Replay) -> tuple[bool | None, int | None, str] | None:
    """G1 + H + T, called only after the pre-existing arms decline."""
    historical = False
    try:
        if not _redundant_merge_shape(branch, base, git):
            return None
        historical, error = replay(branch, base)
        if historical is None:
            raise _MeasurementError(error)
        if not historical:
            return None
        unproved = _retained_at_tip(branch, base, git)
    except (_MeasurementError, OSError) as exc:
        context = "historical replay proved; " if historical else ""
        return (None, None, f"{context}redundant-merge proof unmeasurable: {exc}")
    if unproved:
        return (None, None, f"historical whitespace-exact replay in {base}; "
                "current retention unproved on: " + ", ".join(unproved))
    return (True, ahead, f"historical whitespace-exact replay across one "
            f"redundant merge; raw no-op retention at {base} "
            f"({ahead} not ancestors)")
