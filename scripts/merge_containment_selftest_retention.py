"""Bounded real-history controls for the #423 raw-retention boundary.

All successes traverse the shipped CLI with real distinct replay commits.
Fault injection targets only plumbing failures, never supplies a proof.
Repeated-block probes exercise selected alignments, not all possible merges.
"""

import os
import subprocess
from pathlib import Path
from unittest.mock import patch

import merge_containment_replay as proof
from merge_containment_selftest_replay import MOD, _History
from merge_containment_selftest_scratch import scratch


def _raw(*args, data):
    result = subprocess.run(("git", "--no-replace-objects", *args),
                            input=data, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f"fixture git {args}: {result.stderr!r}")
    return result.stdout.strip().decode("ascii")


def _tree(entries):
    records = []
    for name, entry in entries.items():
        if entry is None:
            continue
        mode, data = entry
        kind = {"160000": "commit", "040000": "tree"}.get(mode, "blob")
        oid = data if kind != "blob" else _raw("hash-object", "-w", "--stdin", data=data)
        records.append(f"{mode} {kind} {oid}\t".encode()
                       + name.encode("utf-8", "surrogateescape") + b"\0")
    return _raw("mktree", "-z", data=b"".join(records))


def _commit(history, tree, parents, label):
    args = ["commit-tree", tree, "-m", label]
    for parent in parents:
        args.extend(("-p", parent))
    return history._git(*args)


def _history(history, path, entries):
    """One real redundant merge; two replay commits; a later tip edit."""
    original, source, current = entries
    control = MOD.encode()
    changed = control.replace(b"line 05", b"source 05")
    extended = changed.replace(b"line 35", b"later 35")
    initial_tree = _tree({path: original, "control": ("100644", control)})
    initial = _commit(history, initial_tree, [], "initial")
    a_tree = _tree({path: source, "control": ("100644", control)})
    a = _commit(history, a_tree, [initial], "source A")
    merge = _commit(history, a_tree, [initial, a], "redundant merge")
    source_tree = _tree({path: source, "control": ("100644", changed)})
    branch = _commit(history, source_tree, [merge], "source C")
    replay_a = _commit(history, a_tree, [initial], "replay A")
    replay_c = _commit(history, source_tree, [replay_a], "replay C")
    tip_tree = _tree({path: current, "control": ("100644", extended)})
    tip = _commit(history, tip_tree, [replay_c], "later extension")
    history._git("update-ref", "refs/heads/pr", branch)
    history._git("update-ref", "refs/heads/main", tip)
    return initial, branch, tip


def _check(fx, name, expected, path=None):
    rc, output = fx.run(["--no-fetch", "--base", "main", "pr"])
    lines = [line.split() for line in output.splitlines() if line.strip()]
    fx.case("retention-" + name, (rc, lines[0][0] if lines else "no verdict"),
            expected, "real Git history: exit AND verdict")
    if expected == (0, "contained"):
        fx.case("retention-" + name + "-proof", "raw no-op retention" in output,
                True, "acceptance requires both historical replay and raw retention")
    if path is not None:
        # _tree fixes the filename bytes independently of the process locale.
        literal_path = os.fsdecode(path.encode("utf-8", "surrogateescape"))
        fx.case("retention-" + name + "-path", repr(literal_path) in output, True,
                "the unproved literal path is named without decoding loss")


def _text_entries(original, source, current):
    return tuple(("100644", data) for data in (original, source, current))


def _entry_cases(history):
    """File types, absence and modes are independent of blob similarity."""
    old = MOD.encode()
    source = old.replace(b"line 05", b"source 05")
    extended = source.replace(b"line 35", b"later 35")
    empty_tree = _tree({})
    oid1 = _commit(history, empty_tree, [], "gitlink 1")
    oid2 = _commit(history, empty_tree, [oid1], "gitlink 2")
    oid3 = _commit(history, empty_tree, [oid2], "gitlink 3")
    child_tree = _tree({"child": ("100644", source)})
    regular = ("100644", source)
    return (
        ("symlink-identical", (("120000", b"old"), ("120000", b"new"), ("120000", b"new")), True),
        ("symlink-changed", (("120000", b"old"), ("120000", b"new"), ("120000", b"later")), False),
        ("symlink-to-file", (("120000", b"old"), ("120000", source), regular), False),
        ("file-to-symlink", (("100644", old), regular, ("120000", source)), False),
        ("file-to-tree", (("100644", old), regular, ("040000", child_tree)), False),
        ("gitlink-identical", (("160000", oid1), ("160000", oid2), ("160000", oid2)), True),
        ("gitlink-changed", (("160000", oid1), ("160000", oid2), ("160000", oid3)), False),
        ("gitlink-to-file", (("160000", oid1), ("160000", oid2), regular), False),
        ("mode-lost", (("100644", old), ("100755", source), ("100644", extended)), False),
        ("mode-retained", (("100644", old), ("100755", source), ("100755", extended)), True),
        ("later-mode-only", (("100644", old), regular, ("100755", extended)), True),
        ("addition-identical", (None, regular, regular), True),
        ("addition-edited", (None, regular, ("100644", extended)), False),
        ("deletion-retained", (("100644", old), None, None), True),
        ("deletion-restored", (("100644", old), None, ("100644", old)), False),
    )


def _path_and_format_cases(fx, history):
    old = MOD.encode()
    source = old.replace(b"line 05", b"source 05")
    extended = source.replace(b"line 35", b"later 35")
    for path in (":(exclude)magic", "tab\tnewline\nend\n", "crlf\r\npath", "raw-\udcff"):
        _history(history, path, _text_entries(old, source, extended))
        _check(fx, "literal-" + ascii(path), (0, "contained"))
        _history(history, path, _text_entries(old, source, old + b"extension\n"))
        _check(fx, "literal-revert-" + ascii(path), (1, "UNKNOWN"), path)
    crlf = tuple(data.replace(b"\n", b"\r\n") for data in (old, source, extended))
    _history(history, "crlf", _text_entries(*crlf))
    _check(fx, "crlf-exact", (0, "contained"))
    _history(history, "crlf", _text_entries(crlf[0], crlf[1], extended))
    _check(fx, "crlf-normalized-tip", (1, "UNKNOWN"), "crlf")
    # Invalid UTF-8 blob bytes also stay raw; only NUL makes Git call it binary.
    non_utf8 = tuple(data + b"\xff\n" for data in (old, source, extended))
    _history(history, "raw-bytes", _text_entries(*non_utf8))
    _check(fx, "raw-blob-bytes", (0, "contained"))


def _alignment_cases(fx, history):
    """Sixteen real histories: partial deletions/edits in repeated blocks."""
    for repeats in (2, 3, 5, 8):
        old = b"a\nb\nc\n" * repeats + b"end\n"
        for deleting in (False, True):
            lines = old.splitlines(keepends=True)
            first, second = 1, 3 * (repeats - 1) + 1
            source = b"".join((b"" if deleting else b"changed\n")
                              if i in (first, second) else line
                              for i, line in enumerate(lines))
            restored = b"".join((b"" if deleting else b"changed\n")
                                if i == second else line
                                for i, line in enumerate(lines)) + b"append\n"
            for current, accepted in ((source + b"append\n", True), (restored, False)):
                name = f"blocks-{repeats}-{deleting}-{accepted}"
                _history(history, "repeated", _text_entries(old, source, current))
                expected = (0, "contained") if accepted else (1, "UNKNOWN")
                _check(fx, name, expected, None if accepted else "repeated")


def _hostile_cases(fx, history):
    history._git("config", "merge.ours.driver", "touch driver-ran; true")
    history._git("config", "diff.quiet.textconv", "touch textconv-ran; true")
    history._git("config", "filter.quiet.clean", "touch filter-ran; cat")
    history._git("config", "merge.renormalize", "true")
    history._git("config", "merge.conflictStyle", "diff3")
    history._git("config", "core.autocrlf", "true")
    history._git("config", "core.filemode", "false")
    history._git("config", "diff.algorithm", "patience")
    Path(".gitattributes").write_text("* merge=ours diff=quiet filter=quiet text eol=lf\n")
    old = MOD.encode()
    source = old.replace(b"line 05", b"source 05")
    for current, accepted in ((source.replace(b"line 35", b"later 35"), True),
                              (old + b"extension\n", False)):
        _history(history, "hostile", _text_entries(old, source, current))
        _check(fx, f"hostile-{accepted}", (0, "contained") if accepted else (1, "UNKNOWN"))
    fx.case("retention-hostile-no-drivers",
            any(Path(name).exists() for name in ("driver-ran", "textconv-ran", "filter-ran")),
            False, "raw measurements never invoked configured drivers or filters")
    # Git validates each configured style before applying the final override.
    # An invalid value is therefore an unmeasurable command, even for retained
    # bytes. The decision requires UNKNOWN on measurement failure.
    _history(history, "hostile", _text_entries(old, source, source.replace(b"line 35", b"later 35")))
    history._git("config", "merge.conflictStyle", "invalid-style")
    _check(fx, "invalid-config", (1, "UNKNOWN"), "hostile")
    Path(".gitattributes").unlink()


def _fault_cases(fx, history):
    """Real missing objects plus injected malformed/failed Git measurements."""
    old = MOD.encode()
    source = old.replace(b"line 05", b"source 05")
    _history(history, "fault", _text_entries(old, source, source.replace(b"line 35", b"later 35")))
    raw_git = proof._git_bytes
    failures = (("ls-tree", (128, b"")), ("ls-tree", (0, b"malformed\0")),
                ("diff", (128, b"")), ("diff", (0, b"")),
                ("cat-file", (128, b"")), ("merge-file", (129, b"")),
                ("merge-file", (-9, b"")))
    for index, (command, result) in enumerate(failures):
        def fail(*args: str) -> tuple[int, bytes]:
            """Fail only the targeted raw measurement."""
            return result if command in args else raw_git(*args)
        with patch.object(proof, "_git_bytes", fail):
            _check(fx, f"command-{command}-{index}", (1, "UNKNOWN"))
    with patch.object(proof, "_git_bytes", side_effect=OSError("planted execution error")):
        _check(fx, "execution-error", (1, "UNKNOWN"))
    with patch.object(proof.tempfile, "TemporaryDirectory", side_effect=OSError("planted storage error")):
        _check(fx, "temporary-storage-error", (1, "UNKNOWN"), "fault")
    _graph_fault_cases(fx)
    oid = history._git("rev-parse", "main:fault")
    object_path = Path(".git/objects") / oid[:2] / oid[2:]
    raw = object_path.read_bytes()
    try:
        object_path.unlink()
        _check(fx, "missing-blob", (1, "UNKNOWN"))
    finally:
        object_path.write_bytes(raw)
    _check(fx, "restored-blob", (0, "contained"))


def _graph_fault_cases(fx):
    git = fx.mc._git
    conditions = (
        (lambda args: args[:3] == ("rev-list", "--min-parents=2", "--parents"), (128, "")),
        (lambda args: args[:3] == ("rev-list", "--parents", "--max-count=1"), (128, "")),
        (lambda args: args[:2] == ("merge-base", "--all"), (128, "")),
        (lambda args: args[:2] == ("merge-base", "--all"), (0, "")),
        (lambda args: args[:2] == ("merge-base", "--all"), (0, "a\nb")),
    )
    for index, (condition, result) in enumerate(conditions):
        def fail(*args: str) -> tuple[int, str]:
            """Fail only the targeted graph measurement."""
            return result if condition(args) else git(*args)
        with patch.object(fx.mc, "_git", fail):
            _check(fx, f"graph-error-{index}", (1, "UNKNOWN"))


def retention_cases(fx: object) -> None:
    """Exercise the bounded controls under the default self-test owner."""
    for object_format in ("sha1", "sha256"):
        with scratch(fx.leftovers) as directory:
            cwd = os.getcwd()
            try:
                os.chdir(directory)
                history = _History()
                history._git("init", "-q", "-b", "main", "--object-format=" + object_format)
                if object_format == "sha256":
                    old = MOD.encode()
                    source = old.replace(b"line 05", b"source 05")
                    _history(history, "format", _text_entries(old, source, source + b"append\n"))
                    _check(fx, "sha256", (0, "contained"))
                    _history(history, "format", _text_entries(old, source, old + b"append\n"))
                    _check(fx, "sha256-revert", (1, "UNKNOWN"), "format")
                    continue
                for name, entries, accepted in _entry_cases(history):
                    _history(history, "entry", entries)
                    expected = (0, "contained") if accepted else (1, "UNKNOWN")
                    _check(fx, name, expected, None if accepted else "entry")
                _path_and_format_cases(fx, history)
                _alignment_cases(fx, history)
                _fault_cases(fx, history)
                _hostile_cases(fx, history)
            finally:
                os.chdir(cwd)
