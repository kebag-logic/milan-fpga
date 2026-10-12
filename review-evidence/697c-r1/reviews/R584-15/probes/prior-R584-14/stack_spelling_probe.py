# Reviewer probe (R584-14): the stack's allowlist (ctrl_build.configured) against the spellings that pass the
# superproject's refused keys (superproject_spelling_probe.py). Each case: a fresh clone of the stack at the pin,
# with every object loose and the pinned src/ tree's object removed (ctrl_pin_store.keyed(..., missing=True)),
# then the case's text appended to its own config file, then the head's ctrl_build.stack_pin.
# Usage: python3 -I stack_spelling_probe.py <clone-root> <work-dir>
import shutil
import sys
from pathlib import Path

root, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_build  # noqa: E402
from ctrl_build import Refusal, stack_pin  # noqa: E402
from ctrl_pin_env import Scene, answer  # noqa: E402
import ctrl_pin_store  # noqa: E402

PIN = answer(root, "ls-files", "--stage", "--", "third_party/tsn-c-stack").split()[1]
CASES = {
    "T0-clean": "",
    "T1-no-subsection-promisor-url-rewrite-ext":
        '[remote]\n\tpromisor = true\n[url "ext::{ext}"]\n\tinsteadOf =\n[protocol "ext"]\n\tallow = always\n',
    "T2-empty-subsection-promisor": '[remote ""]\n\tpromisor = true\n',
}
print(f"git: {answer(root, 'version').strip()}", flush=True)
for name, body in CASES.items():
    own = work / name
    if own.exists():
        shutil.rmtree(own)
    own.mkdir(parents=True)
    stack = own / "stack"
    answer(own, "clone", "--quiet", "--no-hardlinks", str(root / "third_party/tsn-c-stack"), str(stack))
    answer(stack, "-c", "advice.detachedHead=false", "checkout", "--quiet", PIN)
    s = Scene(stack, PIN, own)
    if body:
        ctrl_pin_store.keyed(s, (), True)
        ext = own / "extserver"
        ext.write_text('#!/bin/sh\necho "$0 $*" >> "$(dirname "$0")/ran"\nexit 1\n', encoding="utf-8")
        ext.chmod(0o755)
        with open(stack / ".git/config", "a", encoding="utf-8") as f:
            f.write(body.format(ext=ext))
    try:
        verdict = f"ACCEPTED {stack_pin(stack, PIN)}"
    except Refusal as exc:
        verdict = f"REFUSED: {exc}"
    ran = sum(len(p.read_text().splitlines()) for p in own.rglob("ran"))
    print(f"{name}: {verdict} RAN={ran}", flush=True)
