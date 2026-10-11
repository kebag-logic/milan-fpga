"""R584-9: write the helper-rebinding mutants into copies of a checkout's pin-proof modules.

Usage: python3 -I make_rebind_mutants.py <checkout> <form>; edits that checkout (a disposable copy) in place.
Forms:
  E1b  ctrl_build.py: a function run at import that declares `global git` and defines a nested `def git`, routing
       every git command without stdin through the harness's runner (ctrl_build.run) with the helper's environment
  E2b  ctrl_build.py: a self-import that sets ctrl_build.git to such an adapter, its __name__ set to "git"
  E6   ctrl_pin.py: the same adapter assigned to ctrl_build.git at the end of ctrl_pin.py
  E7   ctrl_build.py: os.walk, a name of the pin proof's vocabulary, rebound to a function that starts git through
       the harness's runner before walking
Each keeps the helper's environment (git_env), so the pin's verdicts do not change; only the launch route does."""
import sys
from pathlib import Path

root, form = Path(sys.argv[1]), sys.argv[2]
build = root / "sw/firmware/ctrl/test/ctrl_build.py"
pin = root / "sw/firmware/ctrl/test/ctrl_pin.py"
ANCHOR = "\n\ndef stack_gitlink("
PLANTS = {
    "E1b": (build, '''

def configure() -> None:
    """Route the pin proof's git through the harness's runner."""
    global git
    helper = git

    def git(directory: Path, *args: str, stdin: str | None = None) -> GitRun:
        if stdin is not None:
            return helper(directory, *args, stdin=stdin)
        res = run(["git", "-C", str(directory), *args], env=git_env())
        return GitRun(res.returncode, res.stdout, res.stderr)


configure()
'''),
    "E2b": (build, '''

def plain(directory: Path, *args: str, stdin: str | None = None) -> GitRun:
    """git through the harness's runner, with the helper's environment."""
    if stdin is not None:
        return HELPER_FN(directory, *args, stdin=stdin)
    res = run(["git", "-C", str(directory), *args], env=git_env())
    return GitRun(res.returncode, res.stdout, res.stderr)


HELPER_FN = git
plain.__name__ = "git"
import ctrl_build  # noqa: E402
ctrl_build.git = plain
'''),
    "E7": (build, '''

WALK = os.walk


def walk(top: str) -> object:
    """os.walk, after a git command started through the harness's runner."""
    run(["git", "-C", str(top), "status", "--porcelain"])
    return WALK(top)


os.walk = walk
'''),
}
if form in PLANTS:
    path, plant = PLANTS[form]
    text = path.read_text(encoding="utf-8")
    assert text.count(ANCHOR) == 1
    path.write_text(text.replace(ANCHOR, plant + ANCHOR, 1), encoding="utf-8")
elif form == "E6":
    pin.write_text(pin.read_text(encoding="utf-8") + '''

import ctrl_build  # noqa: E402


def plain(directory: Path, *args: str, stdin: str | None = None) -> object:
    """git through the harness's runner, with the helper's environment."""
    if stdin is not None:
        return git(directory, *args, stdin=stdin)
    res = fw_gtest.run(["git", "-C", str(directory), *args], env=git_env())
    return ctrl_build.GitRun(res.returncode, res.stdout, res.stderr)


ctrl_build.git = plain
''', encoding="utf-8")
else:
    raise SystemExit(f"unknown form {form}")
