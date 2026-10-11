"""R584-9: the census given a ctrl_build.py whose helper name is bound only by assignment (the def renamed).
Usage: python3 -I helper_value_only_probe.py <checkout>. Writes nothing."""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
from ctrl_pin import PROOF, ROOT, census, git_env  # noqa: E402

texts = {p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8") for p in PROOF}
k = "sw/firmware/ctrl/test/ctrl_build.py"
assert texts[k].count("\ndef git(") == 1
texts[k] = texts[k].replace("\ndef git(", "\ndef git_run(").replace(
    "\n\n\ndef stack_gitlink(", "\n\n\ngit = git_run\n\n\ndef stack_gitlink(", 1)
try:
    print("census findings:", census(texts, git_env()))
except Exception as exc:  # the probe reports what the census does, whatever it raises
    print(f"census raised {type(exc).__name__}: {exc}")
