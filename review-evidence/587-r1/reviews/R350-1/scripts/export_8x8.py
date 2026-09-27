# Recipe "Export the shipping builds" restricted to ax8x8 (verbatim logic).
import json, os, shlex, subprocess
from pathlib import Path
root = Path(os.environ["REPO"]); work = Path(os.environ["WORK"])
python = os.environ["LITEX_PYTHON"]
for shape in ("ax8x8",):
    preview = (work / f"{shape}-dry-run.log").read_text()
    lines = [l for l in preview.splitlines() if "exec python3 milan_soc.py " in l]
    assert len(lines) == 1
    argv = shlex.split(lines[0].split("exec python3 ", 1)[1])
    argv.remove("--build")
    argv[argv.index("--output-dir") + 1] = str(work / shape)
    (work / f"{shape}-argv.json").write_text(json.dumps(argv, indent=2))
    with (work / f"{shape}-elaboration.log").open("w") as log:
        subprocess.run([python, *argv], cwd=root / "sw/litex",
                       stdout=log, stderr=subprocess.STDOUT, check=True)
