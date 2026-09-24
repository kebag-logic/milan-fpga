"""Optional linear retention examples for #514, through the shipped CLI.

Historical verdicts remain separate. Each negative content example also runs
against a source mutant that bypasses this arm's T measurement. The same
expected verdict and exit reject that mutant; no oracle calls the predicate.
"""

import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import merge_containment_replay as proof
from merge_containment_selftest_replay import MOD, _History
from merge_containment_selftest_retention import _commit, _tree
from merge_containment_selftest_scratch import scratch


SOURCE = MOD.replace("line 05", "source 05").replace("line 20", "source 20").encode()
ORIGINAL = MOD.encode()
EXTENSION = SOURCE.replace(b"line 35", b"extension 35")


def _blob(data, mode="100644"):
    return mode, data


def _examples(old_oid, new_oid):
    """Independent input/output cases, including mode and kind boundaries."""
    original, source = _blob(ORIGINAL), _blob(SOURCE)
    link_old, link_new = _blob(b"old", "120000"), _blob(b"new", "120000")
    pin_old, pin_new = _blob(old_oid, "160000"), _blob(new_oid, "160000")
    return (
        ("exact-retention", (original, source, source), True),
        ("exact-reversion", (original, source, original), False),
        ("partial-reversion", (original, source,
                               _blob(SOURCE.replace(b"source 20", b"line 20"))), False),
        ("legitimate-extension", (original, source, _blob(EXTENSION)), True),
        ("intentional-supersession", (original, source,
                                      _blob(SOURCE.replace(b"source 05", b"replacement 05"))), False),
        ("mode-loss", (original, _blob(SOURCE, "100755"), source), False),
        ("later-mode-change", (original, source, _blob(EXTENSION, "100755")), True),
        ("file-kind-change", (original, source, _blob(SOURCE, "120000")), False),
        ("symlink-identity", (link_old, link_new, link_new), True),
        ("symlink-reversion", (link_old, link_new, link_old), False),
        ("gitlink-identity", (pin_old, pin_new, pin_new), True),
        ("gitlink-reversion", (pin_old, pin_new, pin_old), False),
        ("binary-unmeasurable", (_blob(b"old\0data"), _blob(b"source\0data"),
                                   _blob(b"later\0data")), False),
        ("deletion-retained", (original, None, None), True),
        ("deletion-reverted", (original, None, original), False),
    )


def _history(history, entries):
    """Linear exact replay, followed by an independently specified tip."""
    trees = [_tree({"work": entry, "control": _blob(control)})
             for entry, control in zip(entries, (b"unrelated\n", b"unrelated\n", b"later\n"))]
    initial = _commit(history, trees[0], [], "initial")
    source = _commit(history, trees[1], [initial], "source")
    replay = _commit(history, trees[1], [initial], "replay")
    tip = _commit(history, trees[2], [replay], "later intent is not evidence")
    history._git("update-ref", "refs/heads/pr", source)
    history._git("update-ref", "refs/heads/main", tip)
    return initial, source, tip


def _observed(result):
    rc, output = result
    words = [line.split()[0] for line in output.splitlines()
             if "current retention:" in line]
    return rc, words


def _mutant(fx, args, before, after):
    """Run the actual CLI with one guard edited in a disposable copy."""
    sources = Path(__file__).resolve().parent
    with scratch(fx.leftovers) as directory:
        target = Path(directory)
        for name in ("check_merge_containment.py", "merge_containment_git.py",
                     "merge_containment_replay.py"):
            data = (sources / name).read_bytes()
            if name == "merge_containment_replay.py":
                if data.count(before) != 1:
                    raise RuntimeError("linear retention mutant needs one guard location")
                data = data.replace(before, after)
            (target / name).write_bytes(data)
        result = subprocess.run((sys.executable, "-B", "-I",
                                 str(target / "check_merge_containment.py"), *args),
                                capture_output=True, text=True, errors="backslashreplace")
    return result.returncode, result.stdout


def _check(fx, name, retained, mutation=True):
    args = ["--no-fetch", "--base", "main", "pr"]
    rc, output = fx.run(args)
    fx.case("linear-" + name + "-historical", (rc, "contained" in output), (0, True),
            "existing landing verdict remains contained/0")
    args.append("--current-retention")
    result = fx.run(args)
    expected = (0, ["retained"]) if retained else (1, ["UNKNOWN"])
    fx.case("linear-" + name, _observed(result), expected,
            "separate current retention verdict AND process exit")
    fx.case("linear-" + name + "-landing", "contained" in result[1], True,
            "the optional result does not replace historical landing")
    if not retained:
        fx.case("linear-" + name + "-claim", "historical inclusion only" in output, True,
                "the default replay diagnostic names its historical claim")
        fx.case("linear-" + name + "-path", "'work'" in result[1], True,
                "unproved current path is named")
        if mutation:
            mutant = _mutant(fx, args,
                              b"missing = _retained_at_tip(source, target, git)", b"missing = []")
            fx.case("linear-mutant-" + name, _observed(mutant), (0, ["retained"]),
                    "bypassing T is rejected by this example's UNKNOWN/1 oracle")
            fx.case("linear-kills-" + name, _observed(mutant) != expected, True,
                    "the negative example fails against the new arm's mutant")
    return result


def _measurement_cases(fx):
    saved = proof._git_bytes

    def fail(*args: object) -> tuple[int, bytes]:
        """Inject one unavailable raw object measurement, keeping Git history real."""
        if args[0] == "cat-file":
            return 128, b""
        return saved(*args)

    with patch.object(proof, "_git_bytes", fail):
        result = _check(fx, "missing-object-measurement", False, mutation=False)
        with patch.object(proof, "_retained_at_tip", return_value=[]):
            mutant = fx.run(["--no-fetch", "--base", "main", "pr", "--current-retention"])
        fx.case("linear-kills-measurement-mutant", _observed(mutant), (0, ["retained"]),
                "bypassing T while the same object read fails violates the UNKNOWN/1 oracle")
    fx.case("linear-measurement-diagnostic", "cat-file failed (exit 128)" in result[1], True,
            "measurement failure is explicit, never a retained certificate")


def _scope_cases(fx, history, initial, source):
    """Unsupported histories and missing H cannot become optional passes."""
    args = ["--no-fetch", "--current-retention", "--base", "main", "pr"]
    # Ancestry proves landing but supplies no source-only replay range.
    history._git("update-ref", "refs/heads/main", source)
    result = fx.run(args)
    fx.case("linear-ancestry-unsupported", _observed(result), (1, ["UNKNOWN"]),
            "an empty source-only range is explicitly unsupported")
    fx.case("linear-ancestry-diagnostic", "unsupported" in result[1], True,
            "ancestry alone supplies no current-retention baseline")
    mutant = _mutant(fx, args,
                      b'return False, "unsupported: needs a nonempty whitespace-exact linear replay"',
                      b'return True, "unsupported: needs a nonempty whitespace-exact linear replay"')
    fx.case("linear-kills-ancestry-mutant", _observed(mutant), (0, ["retained"]),
            "the ancestry example rejects certifying an unsupported history")
    # A merge-shaped source with identical current entries passes the old
    # path arm, but is outside this optional linear arm's scope.
    tree = history._git("rev-parse", source + "^{tree}")
    merge = _commit(history, tree, [initial, source], "redundant merge")
    history._git("update-ref", "refs/heads/pr", merge)
    history._git("update-ref", "refs/heads/main", _commit(history, tree, [initial], "exact replay"))
    result = fx.run(args)
    fx.case("linear-merge-unsupported", _observed(result), (1, ["UNKNOWN"]),
            "this optional arm never generalizes the source topology")
    mutant = _mutant(fx, args, b"if int(merges) != 0:", b"if False:")
    fx.case("linear-kills-shape-mutant", _observed(mutant), (0, ["retained"]),
            "the unsupported merge example rejects the removed shape guard")
    # Two linear commits squashed to one have exact current entries but no H.
    intermediate = _commit(history, _tree({"control": _blob(b"unrelated\n")}),
                           [initial], "delete first")
    split = _commit(history, tree, [intermediate], "restore and change")
    history._git("update-ref", "refs/heads/pr", split)
    result = fx.run(args)
    fx.case("linear-squash-unsupported", _observed(result), (1, ["UNKNOWN"]),
            "exact endpoint equality does not stand in for distinct replay evidence")
    mutant = _mutant(fx, args, b"matched, error = replay(source, target)",
                      b"matched, error = True, None")
    fx.case("linear-kills-history-mutant", _observed(mutant), (0, ["retained"]),
            "the squash example rejects bypassing the optional arm's H guard")


def _cli_cases(fx, source, tip):
    args = ["--no-fetch", "--base", "main", "pr", "--current-retention"]
    for extra in (["--current-retention"], ["--selftest"]):
        fx.case("linear-cli-refuses-" + extra[0], fx.run([*args, *extra])[0], 2,
                "malformed optional invocation is refused")
    fx.mc._git("update-ref", "refs/heads/good", tip)
    # The ancestral target is unsupported while pr retains its replay.
    result = fx.run([*args, "good"])
    fx.case("linear-cli-multiple", _observed(result), (1, ["retained", "UNKNOWN"]),
            "one unresolved optional result makes the whole command fail")
    with patch.object(fx.mc, "_merged_pr_targets",
                      return_value=([("#1 pr", source, None)], None)):
        result = fx.run(["--no-fetch", "--base", "main", "--merged-prs", "1",
                         "--current-retention"])
    fx.case("linear-cli-sweep", _observed(result), (0, ["retained"]),
            "the optional arm reaches merged-PR targets too")


def linear_retention_cases(fx: object) -> None:
    """Run the new arm's executable policy, refusal and mutation controls."""
    cwd = os.getcwd()
    with scratch(fx.leftovers) as directory:
        try:
            os.chdir(directory)
            history = _History()
            history._git("init", "-q", "-b", "main")
            empty = _tree({})
            old_oid = _commit(history, empty, [], "old pin")
            new_oid = _commit(history, empty, [old_oid], "new pin")
            for name, entries, retained in _examples(old_oid, new_oid):
                _history(history, entries)
                result = _check(fx, name, retained)
                if name == "binary-unmeasurable":
                    fx.case("linear-binary-diagnostic", "raw merge-file failed" in result[1], True,
                            "binary overlap is reported as an unmeasurable raw merge")
            initial, source, tip = _history(history, (_blob(ORIGINAL), _blob(SOURCE), _blob(EXTENSION)))
            _measurement_cases(fx)
            _cli_cases(fx, source, tip)
            _scope_cases(fx, history, initial, source)
        finally:
            os.chdir(cwd)
