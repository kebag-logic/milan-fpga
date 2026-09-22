"""Real filename bytes across fresh Python filesystem encodings (#423).

The normal containment self-test owns these controls. UTF-8 and ASCII need
no installed locale. Latin-1 uses an existing locale or a disposable localedef
output; unavailable locale data is explicitly NOT RUN, never reported passed.
Fixtures use raw mktree records, independently of the checker's path decoder.
"""

import codecs
import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from merge_containment_selftest_scratch import quiet_git, scratch

NAMES = (b"\xc3\xa9.txt", b"raw-\xff", b"\xe2\x82\xac.txt",
         b":(exclude)tab\tcrlf\r\nend\n")
OLD = b"".join(f"line {i:02d}\r\n".encode() for i in range(40)) + b"raw-\xff\r\n"
CHANGED = OLD.replace(b"line 05", b"source 05 \xff \xc3\xa9")
EXTENDED = CHANGED.replace(b"line 35", b"later 35")


def _raw(*args, data=None):
    """Fixture plumbing transports raw bytes, not production helpers."""
    result = subprocess.run(("git", "--no-replace-objects", *args),
                            input=data, capture_output=True)
    if result.returncode:
        raise RuntimeError(f"fixture Git failed: {args!r}: {result.stderr!r}")
    return result.stdout


def _tree(entries):
    records = []
    for name, content in entries.items():
        oid = _raw("hash-object", "-w", "--stdin", data=content).strip()
        records.append(b"100644 blob " + oid + b"\t" + name + b"\0")
    return _raw("mktree", "-z", data=b"".join(records)).strip().decode("ascii")


def _commit(tree, parents, label):
    args = ["commit-tree", tree, "-m", label]
    for parent in parents:
        args.extend(("-p", parent))
    return _raw(*args).strip().decode("ascii")


def _histories(name):
    """Create four distinct histories with an unchanged Latin-1 alias."""
    def tree(content: bytes, control: bytes) -> str:
        """Keep the differently encoded alias unchanged in every tree."""
        return _tree({name: content, b"control": control,
                      b"\xe9.txt": b"unchanged alias\n"})

    original = _commit(tree(OLD, OLD), [], "original")
    source_tree = tree(CHANGED, OLD)
    linear = _commit(source_tree, [original], "linear source")
    missing = _commit(tree(OLD, EXTENDED), [original], "unrelated work")
    retained = _commit(tree(CHANGED, EXTENDED), [original], "retained work")
    merge = _commit(source_tree, [original, linear], "redundant merge")
    final_tree = tree(CHANGED, CHANGED)
    branch = _commit(final_tree, [merge], "source control edit")
    replay = _commit(source_tree, [original], "replay first")
    replay_final = _commit(final_tree, [replay], "replay second")
    reverted = _commit(tree(OLD, EXTENDED), [replay_final], "revert named file")
    extended = _commit(tree(CHANGED, EXTENDED), [replay_final], "distant extension")
    return original, linear, missing, retained, branch, reverted, extended


def _child(expected_encoding):
    """Run actual CLI aggregation and helper measurements in this process."""
    import check_merge_containment as mc
    import merge_containment_replay as proof

    rows = []

    def case(name: str, got: object, want: object) -> None:
        """Return comparisons to the parent suite's actual failure counter."""
        rows.append([name, got, want])

    actual = codecs.lookup(sys.getfilesystemencoding()).name
    case("filesystem-encoding", actual, expected_encoding)
    if actual != expected_encoding:
        return rows
    _raw("init", "-q", "-b", "main")
    _raw("config", "user.name", "Fixture")
    _raw("config", "user.email", "fixture@example.invalid")
    _raw("config", "commit.gpgsign", "false")
    for name in NAMES:
        prefix = name.hex()
        original, linear, missing, retained, branch, reverted, extended = _histories(name)
        path = os.fsdecode(name)
        for label, source, target, want in (
                ("linear-missing", linear, missing, [1, "STRANDED"]),
                ("linear-retained", linear, retained, [0, "contained"]),
                ("merge-reverted", branch, reverted, [1, "UNKNOWN"]),
                ("merge-retained", branch, extended, [0, "contained"])):
            _raw("update-ref", "refs/heads/pr", source)
            _raw("update-ref", "refs/heads/main", target)
            output = io.StringIO()
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
                rc = mc.main([str(Path(mc.__file__)), "--no-fetch", "--base", "main", "pr"])
            words = output.getvalue()
            case(prefix + "-" + label, [rc, words.split()[0]], want)
            if label == "merge-reverted":
                case(prefix + "-unproved-path", repr(path) in words, True)
            if label == "merge-retained":
                case(prefix + "-retention-proof", "raw no-op retention" in words, True)
        paths, error = mc._commit_paths(linear)
        case(prefix + "-enumerated-bytes",
             [error, sorted(os.fsencode(p).hex() for p in paths)], [None, [name.hex()]])
        case(prefix + "-postimage", list(mc._same_patch_postimage(linear, original)),
             [False, None])
        expected_oid = _raw("hash-object", "--stdin", data=CHANGED).strip().decode("ascii")
        entry = proof._tree_entry(linear, path)
        case(prefix + "-entry", list(entry) if entry else None,
             ["100644", "blob", expected_oid])
        # Independent raw transport catches a mismatched inverse after _git
        # changes, including CRLF and invalid UTF-8 patch payload bytes.
        patch = _raw("show", *mc.RAW_DIFF_FLAGS, "--format=medium", "--binary",
                     "--full-index", "--no-renames", linear).rstrip(b"\n")
        identity = _raw("patch-id", "--verbatim", data=patch).split()[0].decode("ascii")
        case(prefix + "-patch-bytes", list(mc._verbatim_patch_id(linear)), [identity, None])
    return rows


def _latin1_env(directory, env):
    """Use a measured locale without changing any installed locale."""
    if shutil.which("locale"):
        result = subprocess.run(("locale", "-a"), capture_output=True)
        for name in result.stdout.decode("ascii", "ignore").splitlines():
            if "88591" in name.lower().replace("-", ""):
                return dict(env, LC_ALL=name), None
    if not shutil.which("localedef"):
        return None, "localedef unavailable and no Latin-1 locale installed"
    locale_root = Path(directory) / "locales"
    locale_root.mkdir()
    result = subprocess.run(("localedef", "--no-archive", "-i", "en_US", "-f",
                             "ISO-8859-1", str(locale_root / "en_US.ISO-8859-1")),
                            capture_output=True)
    if result.returncode:
        return None, f"localedef exit {result.returncode}: {result.stderr!r}"
    return dict(env, LOCPATH=str(locale_root), LC_ALL="en_US.ISO-8859-1"), None


def locale_cases(fx: object) -> None:
    """Report every child comparison through the existing suite's counter."""
    with scratch(fx.leftovers) as directory:
        env = dict(os.environ, PYTHONCOERCECLOCALE="0", PYTHONUTF8="0",
                   PYTHONIOENCODING="utf-8:backslashreplace", LC_ALL="C",
                   GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        latin1, unavailable = _latin1_env(directory, env)
        environments = [("utf-8", dict(env, PYTHONUTF8="1")), ("ascii", env)]
        if latin1 is not None:
            environments.append(("iso8859-1", latin1))
        else:
            print(f"  NOT RUN locale-iso8859-1: {unavailable}")
        for encoding, child_env in environments:
            work = Path(directory) / encoding
            work.mkdir()
            result = subprocess.run((sys.executable, "-B", str(Path(__file__).resolve()),
                                     "--child", encoding), cwd=work, env=child_env,
                                    capture_output=True)
            label = "locale-" + encoding
            fx.case(label + "-process", result.returncode, 0,
                    "fresh Python: " + repr(result.stderr) if result.returncode else
                    "fresh Python completed the raw-name controls")
            if result.returncode:
                continue
            rows = json.loads(result.stdout)
            fx.case(label + "-population", len(rows), 1 + 10 * len(NAMES),
                    "encoding witness plus CLI, path, entry and patch controls")
            for name, got, want in rows:
                fx.case(label + "-" + name, got, want,
                        "actual filesystem encoding and literal Git filename bytes")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "--child":
        raise SystemExit("Run check_merge_containment.py --selftest")
    with quiet_git():
        print(json.dumps(_child(sys.argv[2]), ensure_ascii=True))
