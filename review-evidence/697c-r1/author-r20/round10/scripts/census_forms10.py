"""Census over planted forms (round 10): each form is put in place of an anchor of a pin-proof module, or added
at its end; the census must name the planted line. Usage: census_forms10.py <checkout>"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
sys.dont_write_bytecode = True
import ctrl_build  # noqa: E402
import ctrl_pin  # noqa: E402

B, P = "ctrl_build.py", "ctrl_pin.py"
TREE = ctrl_pin.TREE_READ
GITLINK = 'entry = git(root, "ls-files", "--stage", "--", rel).stdout.split()'
HEAD = 'head = git(stack, "rev-parse", "HEAD").stdout.strip()'
LEGACY = '    held = {new: old for new, old in LEGACY.items() if (ctrl / old).is_file()}'
FORMS = [
    ("import subprocess as sp, used in stack_pin", B, TREE, 'import subprocess as sp\n    tree = sp.run(["git", "ls-tree", pin])'),
    ("__import__ of subprocess", B, TREE, 'tree = __import__("subprocess").run(["git", "ls-tree", pin])'),
    ("importlib", B, TREE, 'import importlib\n    tree = importlib.import_module("subprocess").run(["git"])'),
    ("getattr(os, computed)", B, TREE, 'tree = getattr(os, "sys" + "tem")("git ls-tree")'),
    ("os.popen", B, HEAD, 'head = os.popen("git rev-parse HEAD").read().strip()'),
    ("os.execvp", B, HEAD, 'os.execvp("git", ["git", "rev-parse", "HEAD"])'),
    ("os.posix_spawn", B, HEAD, 'os.posix_spawn("/usr/bin/git", ["git"], {})'),
    ("os.spawnlp", B, HEAD, 'os.spawnlp(os.P_WAIT, "git", "git")'),
    ("pty.spawn", B, HEAD, 'import pty\n    pty.spawn(["git", "rev-parse", "HEAD"])'),
    ("asyncio create_subprocess_exec", B, HEAD, 'import asyncio\n    asyncio.create_subprocess_exec("git")'),
    ("from asyncio import create_subprocess_shell", B, HEAD, 'from asyncio import create_subprocess_shell as c\n    c("git")'),
    ("fw_gtest.run in stack_pin (another module's runner)", B, TREE, 'tree = fw_gtest.run(["git", "-C", str(stack), "ls-tree", "-r", "-t", "-z", "--full-tree", pin])'),
    ("shutil.os.system outside the proof (legacy_stack)", B, LEGACY, '    shutil.os.system("git status")\n' + LEGACY),
    ("sys.modules lookup", B, TREE, 'tree = sys.modules["subprocess"].run(["git"])'),
    ("a generator's frame globals", B, TREE, 'tree = (i for i in ()).gi_frame.f_globals["fw_gtest"].run(["git"])'),
    ("from os import system", B, HEAD, 'from os import system\n    system("git rev-parse HEAD")'),
    ("eval of a string", B, HEAD, 'head = eval("run([\'git\'])")'),
    ("compile of a string", B, HEAD, 'head = compile("x", "y", "exec")'),
    ("a module constant bound to the runner, used by stack_pin", B, TREE, 'tree = RUNNER(["git", "ls-tree", pin])'),
    ("the helper's name bound again", B, None, 'git = run\n'),
    ("a new module function using fw_gtest, called by stack_pin", B, TREE, 'tree = reader(stack, pin)'),
    ("a lambda parameter shadowing run", B, TREE, 'tree = (lambda run: run)(0) or run(["git", "ls-tree", pin])'),
    ("the runner as a default argument", B, 'def stack_pin(stack: Path = STACK, pin: str | None = None) -> str:', 'def stack_pin(stack: Path = STACK, pin: str | None = None, r=fw_gtest.run) -> str:'),
    ("os.environ changed in stack_pin", B, HEAD, 'os.environ["GIT_NO_REPLACE_OBJECTS"] = "0"\n    ' + HEAD),
    ("from ctrl_pin import run inside stack_pin", B, TREE, 'from ctrl_pin import run as tool\n    tree = tool(["git", "ls-tree", pin])'),
    ("subprocess in a ctrl_pin.py function", P, None, 'def planted() -> None:\n    import subprocess\n    subprocess.run(["git", "status"])\n'),
    ("a star import", B, None, 'from os import *\n'),
    ("a class method using fw_gtest, used by stack_pin", B, TREE, 'tree = Reader().read(stack, pin)'),
]
EXTRA = {
    "a module constant bound to the runner, used by stack_pin": "\nRUNNER = fw_gtest.run\n",
    "a new module function using fw_gtest, called by stack_pin":
        '\n\ndef reader(stack: Path, pin: str) -> object:\n    """A reader."""\n    return fw_gtest.run(["git", "-C", str(stack), "ls-tree", pin])\n',
    "a class method using fw_gtest, used by stack_pin":
        '\n\nclass Reader:\n    """A reader."""\n\n    def read(self, stack: Path, pin: str) -> object:\n        """Read."""\n        return fw_gtest.run(["git", "-C", str(stack), "ls-tree", pin])\n',
}
texts = {p.relative_to(ctrl_build.ROOT).as_posix(): p.read_text(encoding="utf-8") for p in ctrl_pin.PROOF}
print("clean:", ctrl_pin.census(texts, ctrl_build.git_env()))
bad = 0
for what, rel, old, new in FORMS:
    key = f"sw/firmware/ctrl/test/{rel}"
    text = texts[key]
    if old is not None:
        assert text.count(old) == 1, (what, text.count(old))
    at = len(text) if old is None else text.index(old)
    line = text[:at].count("\n") + 1
    planted = text[:at] + new + text[at + len(old or ""):] + EXTRA.get(what, "")
    found = ctrl_pin.census({**texts, key: planted}, ctrl_build.git_env())
    lines = range(line, line + new.count("\n") + 1)
    named = [f for f in found if any(f.startswith(f"{key}:{n} ") for n in lines)]
    bad += not named
    print(f"[{'REFUSED' if named else 'ESCAPED'}] {what}:", *(named or found), sep="\n    ")
print(f"{len(FORMS) - bad} of {len(FORMS)} refused at the planted line")
# The stated limit: a function of another module that starts a process, where the pin decision does not reach it.
LIMITS = [
    ("the harness's runner in legacy_stack, which the pin decision does not reach", B, LEGACY,
     '    run(["git", "-C", str(ctrl), "status"])\n' + LEGACY),
    ("fw_gtest.run in ctrl_pin.py's mirror", P, '    listed = git(directory, "ls-files", "-z", "--cached", "--others", "--exclude-standard", ".")',
     '    fw_gtest.run(["git", "-C", str(directory), "status"])\n    listed = git(directory, "ls-files", "-z", "--cached", "--others", "--exclude-standard", ".")'),
]
for what, rel, old, new in LIMITS:
    key = f"sw/firmware/ctrl/test/{rel}"
    text = texts[key]
    assert text.count(old) == 1, (what, text.count(old))
    found = ctrl_pin.census({**texts, key: text.replace(old, new)}, ctrl_build.git_env())
    print(f"[{'NOT SEEN, the stated limit' if not found else 'REFUSED'}] {what}:", *found, sep="\n    ")
sys.exit(1 if bad else 0)
