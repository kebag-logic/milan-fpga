"""Real filename bytes across fresh Python filesystem encodings (#423).

The normal containment self-test owns these controls. UTF-8 and ASCII need
no installed locale. Strict UTF-8, Latin-1 and Big5 use an existing locale or
a disposable localedef output; unavailable locale data is explicitly NOT RUN,
never reported passed. Big5 is not injective (a1 fe re-encodes as a2 41), so
the same controls also run in this process with the checker's filesystem codec
replaced by Big5, which needs no locale at all.
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
from unittest.mock import patch

from merge_containment_selftest_scratch import quiet_git, scratch

NAMES = (b"\xc3\xa9.txt", b"raw-\xff", b"\xe2\x82\xac.txt", b"\xa1\xfe.txt",
         b":(exclude)tab\tcrlf\r\nend\n")
#! Unchanged files named as a lossy transport would misname a changed one:
#! Latin-1 turns UTF-8 c3 a9 into e9, and Big5 turns a1 fe into a2 41.
ALIASES = (b"\xe9.txt", b"\xa2\x41.txt")
OLD = b"".join(f"line {i:02d}\r\n".encode() for i in range(40)) + b"raw-\xff\r\n"
CHANGED = OLD.replace(b"line 05", b"source 05 \xff \xc3\xa9 \xa1\xfe")
EXTENDED = CHANGED.replace(b"line 35", b"later 35")
LOSSY_NAME = b"\xa1\xfe"
#! Rows per child: the encoding witness, ten per name, then the real-stdout
#! control's stream witness and three report assertions.
CHILD_ROWS = 1 + 10 * len(NAMES) + 4


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


def _init():
    _raw("init", "-q", "-b", "main")
    _raw("config", "user.name", "Fixture")
    _raw("config", "user.email", "fixture@example.invalid")
    _raw("config", "commit.gpgsign", "false")


def _histories(name):
    """Create four distinct histories beside unchanged aliases."""
    def tree(content: bytes, control: bytes) -> str:
        """Keep every differently encoded alias unchanged in every tree."""
        return _tree({name: content, b"control": control,
                      **{alias: b"unchanged alias\n" for alias in ALIASES}})

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


def _controls(mc, proof, case):
    """CLI verdicts and helper measurements for every name, in this process."""
    for name in NAMES:
        prefix = name.hex()
        original, linear, missing, retained, branch, reverted, extended = _histories(name)
        label = proof.path_label(name)
        for kind, source, target, want in (
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
            case(prefix + "-" + kind, [rc, words.split()[0]], want)
            if kind == "merge-reverted":
                case(prefix + "-unproved-path", label in words, True)
            if kind == "merge-retained":
                case(prefix + "-retention-proof", "raw no-op retention" in words, True)
        paths, error = mc._commit_paths(linear)
        case(prefix + "-enumerated-bytes",
             [error, sorted(path.hex() for path in paths)], [None, [name.hex()]])
        case(prefix + "-postimage", list(mc._same_patch_postimage(linear, original)),
             [False, None])
        expected_oid = _raw("hash-object", "--stdin", data=CHANGED).strip().decode("ascii")
        entry = proof._tree_entry(linear, name)
        case(prefix + "-entry", list(entry) if entry else None,
             ["100644", "blob", expected_oid])
        # Independent raw transport catches a mismatched inverse after _git
        # changes, including CRLF and invalid UTF-8 patch payload bytes.
        patch_bytes = _raw("show", *mc.RAW_DIFF_FLAGS, "--format=medium", "--binary",
                           "--full-index", "--no-renames", linear).rstrip(b"\n")
        identity = _raw("patch-id", "--verbatim", data=patch_bytes).split()[0].decode("ascii")
        case(prefix + "-patch-bytes", list(mc._verbatim_patch_id(linear)), [identity, None])


def _stdout_control(case, checker, proof, stream):
    """Three targets through a real process stdout in this locale.

    The stranded target's note names every changed file.  A report printed
    raw names once, so a strict UTF-8 stdout aborted it at that line.
    """
    original = _commit(_tree({name: OLD for name in NAMES}), [], "original")
    source = _commit(_tree({name: CHANGED for name in NAMES}), [original], "source")
    target = _commit(_tree({b"unrelated": OLD, **{name: OLD for name in NAMES}}),
                     [original], "unrelated work")
    for ref, oid in (("main", target), ("pr", source), ("aa-ok", original),
                     ("zz-later", original)):
        _raw("update-ref", "refs/heads/" + ref, oid)
    env = {key: value for key, value in os.environ.items() if key != "PYTHONIOENCODING"}
    witness = subprocess.run((sys.executable, "-c", "import codecs, sys; print("
                              "codecs.lookup(sys.stdout.encoding).name, sys.stdout.errors)"),
                             env=env, capture_output=True)
    case("stdout-stream", witness.stdout.decode("ascii").split(), list(stream))
    result = subprocess.run((sys.executable, "-B", str(checker), "--no-fetch", "--base", "main",
                             "aa-ok", "pr", "zz-later"), env=env, capture_output=True)
    lines = result.stdout.splitlines()
    verdicts = [line.split()[0].decode("ascii", "replace") for line in lines[:3] if line.strip()]
    case("stdout-verdicts", [result.returncode, verdicts, result.stderr.decode("ascii", "replace")],
         [1, ["contained", "STRANDED", "contained"], ""])
    case("stdout-ascii-report", result.stdout.isascii(), True)
    case("stdout-names", [proof.path_label(name).encode("ascii") in result.stdout
                          for name in NAMES], [True] * len(NAMES))


def _child(expected_encoding, stream):
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
    _init()
    _controls(mc, proof, case)
    _stdout_control(case, Path(mc.__file__), proof, stream)
    return rows


class _Big5Os:
    """The os module, except that its filesystem codec is Big5."""

    def __getattr__(self, name):
        return getattr(os, name)

    @staticmethod
    def fsdecode(data: bytes | str) -> str:
        """Decode as Big5 with surrogateescape, as a Big5 locale would."""
        return data.decode("big5", "surrogateescape") if isinstance(data, bytes) else data

    @staticmethod
    def fsencode(text: str | bytes) -> bytes:
        """Encode as Big5 with surrogateescape, as a Big5 locale would."""
        return text.encode("big5", "surrogateescape") if isinstance(text, str) else text


def _in_process_big5_cases(fx, directory):
    """Every host runs the lossy-codec transport, with or without locales."""
    import merge_containment_git as transport
    import merge_containment_replay as proof

    mc, lossy = fx.mc, _Big5Os()
    label = "locale-big5-in-process-"

    def case(name: str, got: object, want: object) -> None:
        """Report through the suite's own counter."""
        fx.case(label + name, got, want, "Big5 filesystem codec in this process")

    case("codec-lossy", lossy.fsencode(lossy.fsdecode(LOSSY_NAME)), b"\xa2\x41")
    work = Path(directory) / "big5-in-process"
    work.mkdir()
    cwd = os.getcwd()
    try:
        os.chdir(work)
        _init()
        #! Only the transport decodes today.  create=True: a change that brings
        #! the codec back into either other module is measured through it too.
        with patch.object(transport, "os", lossy), \
                patch.object(mc, "os", lossy, create=True), \
                patch.object(proof, "os", lossy, create=True):
            _controls(mc, proof, case)
            _lossy_output_cases(mc, transport, case)
    finally:
        os.chdir(cwd)


def _lossy_output_cases(mc, transport, case):
    """Decoded Git output that cannot re-encode is refused, never measured."""
    lossy = _raw("hash-object", "-w", "--stdin", data=LOSSY_NAME + b"\n").strip()
    kept = _raw("hash-object", "-w", "--stdin", data=b"raw-\xff\n").strip()
    case("git-lossy-output", list(mc._git("cat-file", "blob", lossy.decode("ascii"))),
         [transport.RC_LOSSY_OUTPUT, ""])
    case("git-reversible-output", list(mc._git("cat-file", "blob", kept.decode("ascii"))),
         [0, "raw-\udcff"])
    # With no operand the current branch name comes from Git; a name the
    # codec cannot keep is a refusal, not a lookup of some other branch.
    _raw("update-ref", b"refs/heads/" + LOSSY_NAME, "main")
    _raw("symbolic-ref", "HEAD", b"refs/heads/" + LOSSY_NAME)
    try:
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
            rc = mc.main([str(Path(mc.__file__)), "--no-fetch", "--base", "main"])
        case("git-lossy-head-branch", [rc, output.getvalue()], [mc.RC_CANNOT_RUN, ""])
    finally:
        #! Git removes the ref and its reflog by their bytes.  shutil.rmtree
        #! names files through the parent's codec and fails under Big5.
        _raw("symbolic-ref", "HEAD", "refs/heads/main")
        _raw("update-ref", "-d", b"refs/heads/" + LOSSY_NAME)


def _codeset(locale_name):
    """The normalized codeset of a locale name: en_US.ISO-8859-1 -> iso88591."""
    language, _, rest = locale_name.partition(".")
    codeset = rest.split("@")[0].lower().replace("-", "").replace("_", "")
    return language, codeset


def _locale_env(directory, env, codeset, source, charmap):
    """An installed locale for codeset, else a disposable localedef output."""
    installed = {key: value for key, value in env.items() if key != "LOCPATH"}
    if shutil.which("locale"):
        result = subprocess.run(("locale", "-a"), capture_output=True, env=installed)
        for name in result.stdout.decode("ascii", "ignore").splitlines():
            language, found = _codeset(name)
            #! C.UTF-8 gives Python a surrogateescape stdout, not a strict one.
            if found == codeset and language not in ("C", "POSIX"):
                return dict(installed, LC_ALL=name), None
    if not shutil.which("localedef"):
        return None, f"localedef unavailable and no {charmap} locale installed"
    locale_root = Path(directory) / "locales"
    locale_root.mkdir(exist_ok=True)
    name = f"{source}.{charmap}"
    result = subprocess.run(("localedef", "--no-archive", "-i", source, "-f", charmap,
                             str(locale_root / name)), capture_output=True)
    if result.returncode:
        return None, f"localedef exit {result.returncode}: {result.stderr!r}"
    return dict(env, LOCPATH=str(locale_root), LC_ALL=name), None


def locale_cases(fx: object) -> None:
    """Report every child comparison through the existing suite's counter."""
    with scratch(fx.leftovers) as directory:
        env = dict(os.environ, PYTHONCOERCECLOCALE="0", PYTHONUTF8="0",
                   PYTHONIOENCODING="utf-8:backslashreplace", LC_ALL="C",
                   GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        # (label, filesystem encoding, stdout codec and error handler, env)
        environments = [("utf-8", "utf-8", ("utf-8", "surrogateescape"),
                         dict(env, PYTHONUTF8="1")),
                        ("ascii", "ascii", ("ascii", "surrogateescape"), env)]
        for label, codeset, source, charmap, encoding in (
                ("utf-8-strict", "utf8", "en_US", "UTF-8", "utf-8"),
                ("iso8859-1", "iso88591", "en_US", "ISO-8859-1", "iso8859-1"),
                ("big5", "big5", "zh_TW", "BIG5", "big5")):
            child_env, unavailable = _locale_env(directory, env, codeset, source, charmap)
            if child_env is None:
                print(f"  NOT RUN locale-{label}: {unavailable}")
            else:
                environments.append((label, encoding, (encoding, "strict"), child_env))
        for label, encoding, stream, child_env in environments:
            work = Path(directory) / label
            work.mkdir()
            result = subprocess.run((sys.executable, "-B", str(Path(__file__).resolve()),
                                     "--child", encoding, *stream), cwd=work, env=child_env,
                                    capture_output=True)
            prefix = "locale-" + label
            fx.case(prefix + "-process", result.returncode, 0,
                    "fresh Python: " + repr(result.stderr) if result.returncode else
                    "fresh Python completed the raw-name controls")
            if result.returncode:
                continue
            rows = json.loads(result.stdout)
            fx.case(prefix + "-population", len(rows), CHILD_ROWS,
                    "encoding witness plus CLI, path, entry, patch and stdout controls")
            for name, got, want in rows:
                fx.case(prefix + "-" + name, got, want,
                        "actual filesystem encoding and literal Git filename bytes")
        _in_process_big5_cases(fx, directory)


if __name__ == "__main__":
    if len(sys.argv) != 5 or sys.argv[1] != "--child":
        raise SystemExit("Run check_merge_containment.py --selftest")
    with quiet_git():
        print(json.dumps(_child(sys.argv[2], sys.argv[3:]), ensure_ascii=True))
