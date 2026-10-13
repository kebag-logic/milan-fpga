"""Exercise hostile-environment and disconnected-history mutations in a disposable job."""
import importlib.util
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile

shipping = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(shipping / "scripts"))
import ci_scope_history as history
runner = runpy.run_path(str(shipping / "scripts/act_ci.py"))
for label, control, envname in (
    ("classifier", history.environment_control, "fixture_environment"),
    ("runner", runner["scope_fixture_environment_control"], "scope_fixture_environment"),
):
    namespace = control.__globals__
    original = namespace[envname]
    for poison in ("signing", "gitdir"):
        def leaky(root):
            import os
            clean = original(root)
            keys = ("GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM", "GIT_CONFIG_COUNT") if poison == "signing" else ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")
            if poison == "signing":
                clean.pop("GIT_CONFIG_COUNT", None)
                clean.pop("GIT_CONFIG_NOSYSTEM", None)
            clean.update({key: value for key, value in os.environ.items() if key in keys})
            return clean
        namespace[envname] = leaky
        try:
            try:
                caught = not control(shipping, poison)
            except (subprocess.CalledProcessError, FileNotFoundError):
                caught = True
            assert caught, (label, poison)
            print(f"PASS {label}: leaking {poison} is rejected")
        finally:
            namespace[envname] = original
with tempfile.TemporaryDirectory(prefix="scope-wiring-control-") as raw:
    root = Path(raw)
    (root / "scripts").mkdir()
    text = (shipping / "scripts/ci_scope.py").read_text()
    needle = "failures += history_selftest(ROOT)"
    assert text.count(needle) == 1
    (root / "scripts/ci_scope.py").write_text(text.replace(needle, "pass"))
    tally = runner["SelftestTally"]()
    runner["selftest_scope_history_wiring"](tally, root)
    assert tally.failures > 0
    print("PASS disconnected history call is rejected by the independent runner guard")
print("extra controls: PASS")
