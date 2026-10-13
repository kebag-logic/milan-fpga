"""The stated limit, shown: a plant that rebinds sys.audit in ctrl_pin.py, so the subprocess module's own (Python)
audit call is skipped, and a Git command started by the harness's runner where the pin is decided. On an interpreter
whose _posixsubprocess.fork_exec raises no audit event (CPython before 3.14) nothing names the start; on 3.14 the
hook refuses it. And the same runner bypass without the rebinding, refused on both.
Usage: python3 -I limit_probe.py <checkout>"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
sys.dont_write_bytecode = True
import ctrl_pin  # noqa: E402

texts = {p.relative_to(ctrl_pin.ROOT).as_posix(): p.read_text(encoding="utf-8") for p in ctrl_pin.PROOF}
build, pin = "sw/firmware/ctrl/test/ctrl_build.py", "sw/firmware/ctrl/test/ctrl_pin.py"
bypass = 'tree = run(["git", "-C", str(stack), "ls-tree", "-r", "-t", "-z", "--full-tree", pin])'
assert texts[build].count(ctrl_pin.TREE_READ) == 1
plain = dict(texts, **{build: texts[build].replace(ctrl_pin.TREE_READ, bypass)})
rebound = dict(plain, **{pin: texts[pin] + "sys.audit = lambda *args: None\n"})
print(sys.version.split()[0], "runner bypass:", ctrl_pin.exercised(plain))
print(sys.version.split()[0], "runner bypass with sys.audit rebound:", ctrl_pin.exercised(rebound))
