"""Run only the focused offline tool-path arms on in-memory source mutations."""
import contextlib
import io
from pathlib import Path
import sys
import types

path = Path("scripts/act_ci.py").resolve()
source = path.read_text(encoding="utf-8")
cases = [
    ("control", None, None, 0),
    ("resolve-lookup-again", "return str(pathlib.Path(found).absolute())",
     "return str(pathlib.Path(found).resolve())", 2),
    ("resolve-uplink-launch-again", '        require_tool("pasta"),',
     '        str(pathlib.Path(require_tool("pasta")).resolve()),', 1),
    ("preserve-every-tool-name", "    return str(pathlib.Path(found).resolve())\n\n\ndef capture(",
     "    return str(pathlib.Path(found).absolute())\n\n\ndef capture(", 1),
]
for label, before, after, expected in cases:
    variant = source
    if before is not None:
        assert source.count(before) == 1, (label, "mutation does not apply exactly once")
        variant = source.replace(before, after, 1)
    module = types.ModuleType("act_ci_path_unit")
    module.__file__ = str(path)
    sys.modules[module.__name__] = module
    exec(compile(variant, str(path), "exec"), module.__dict__)
    tally = module.SelftestTally()
    transcript = io.StringIO()
    with contextlib.redirect_stdout(transcript):
        module.selftest_host_tool_paths(tally)
    print(f"{label}: failures={tally.failures}, expected={expected}")
    print(transcript.getvalue(), end="")
    assert tally.failures == expected, label
print("PASS: control clean; 3/3 path mutations killed")
