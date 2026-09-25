"""Exercise the fixture VID domain under normal and optimized Python."""
from pathlib import Path
import subprocess
import sys
import tempfile
import yaml

script = Path.cwd() / "tb/common/gen_declaration_fixture.py"
valid = (1, 73, 4094)
invalid = (-1, 0, 2, 4095, True, 1.0, "73", None)
with tempfile.TemporaryDirectory(prefix="fixture-guard-") as temp:
    root = Path(temp)
    for index, value in enumerate((*valid, *invalid)):
        fixture = root / f"case-{index}.yaml"
        fixture.write_text(yaml.safe_dump(dict(
            base="configs/endstation_arty_current.yaml", emitter_srp_vid=value)))
        normal_headers = {}
        for optimized in (False, True):
            out = root / f"out-{index}"
            command = [sys.executable, *(["-O"] if optimized else []),
                       str(script), str(fixture), str(out)]
            result = subprocess.run(command, capture_output=True, text=True, timeout=120)
            if index < len(valid):
                assert result.returncode == 0, result.stderr
                headers = {path.name: path.read_bytes() for path in (out / "gen").iterdir()}
                if optimized:
                    assert headers == normal_headers, value
                else:
                    normal_headers = headers
            else:
                assert result.returncode != 0, (value, optimized)
                assert "ValueError: emitter_srp_vid must be" in result.stderr
                assert not (out / "gen").exists()
            print(repr(value), "optimized=" + str(optimized),
                  "accepted" if result.returncode == 0 else "refused")
print("PASS: 6 accepted runs, 16 explicit refusals; valid headers identical")
