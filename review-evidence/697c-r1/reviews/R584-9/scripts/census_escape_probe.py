"""R584-9 census probe: run ctrl_pin.census on the checkout's pin-proof modules, its standing controls, and
planted forms.  Usage: python3 -I census_escape_probe.py <checkout>.  Writes nothing; prints one line per case.
A case's 'census findings: []' means the census accepted the planted text."""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_pin  # noqa: E402
from ctrl_pin import PROOF, ROOT, census, census_arms, git_env, proof_census  # noqa: E402

print("clean census findings:", proof_census())
for what, _spoil, check, needle in census_arms():
    accepted, detail = check()
    print(f"[{'ESCAPED' if accepted else 'refused'}] standing control: {what}: {detail}")

texts = {p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8") for p in PROOF}
BUILD, PIN = "sw/firmware/ctrl/test/ctrl_build.py", "sw/firmware/ctrl/test/ctrl_pin.py"
ANCHOR = "\n\ndef stack_gitlink("

ADAPTER = '''

def plain(directory: Path, *args: str, stdin: str | None = None) -> GitRun:
    """git through the harness's runner, with the helper's environment."""
    res = run(["git", "-C", str(directory), *args], env=git_env())
    return GitRun(res.returncode, res.stdout, res.stderr)
'''

CASES = {
    # the helper's name bound again from inside a function, run at import
    "E1 global rebinding of the helper in ctrl_build.py": (BUILD, ADAPTER + '''

def configure() -> None:
    """Route the pin proof's git through the runner."""
    global git
    git = plain


configure()
'''),
    # the helper's name bound again on the module object, through a self-import
    "E2 self-import attribute rebinding in ctrl_build.py": (BUILD, ADAPTER + '''

import ctrl_build  # noqa: E402
ctrl_build.git = plain
'''),
    # a facility of CPython's own, outside the listed names (stated limit)
    "E3 _posixsubprocess import outside the helper": (BUILD, '''

import _posixsubprocess  # noqa: E402
FORK = _posixsubprocess.fork_exec
'''),
    "E4 multiprocessing outside the helper": (BUILD, '''

import multiprocessing  # noqa: E402
POOL = multiprocessing.Pool
'''),
    "E5 a C library's system by subscript outside the helper": (BUILD, '''

import ctypes  # noqa: E402
LIBC_SYSTEM = ctypes.CDLL(None)["system"]
'''),
}

for name, (rel, plant) in CASES.items():
    t = dict(texts)
    if t[rel].count(ANCHOR) != 1:
        print(f"[anchor?] {name}")
        continue
    t[rel] = t[rel].replace(ANCHOR, plant + ANCHOR, 1)
    print(f"{name}: census findings: {census(t, git_env())}")

# E6: the same rebinding planted in ctrl_pin.py (the other pin-proof module)
t = dict(texts)
t[PIN] = t[PIN] + '''

import ctrl_build  # noqa: E402


def plain(directory, *args, stdin=None):
    """git through the harness's runner."""
    return fw_gtest.run(["git", "-C", str(directory), *args], env=git_env())


ctrl_build.git = plain
'''
print(f"E6 attribute rebinding of ctrl_build.git from ctrl_pin.py: census findings: {census(t, git_env())}")
