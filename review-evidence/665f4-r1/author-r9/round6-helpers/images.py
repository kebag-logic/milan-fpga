import os
import hashlib
import json
from pathlib import Path
import subprocess

root = Path(os.environ["SCRATCH"])
runtime = Path(os.environ["RUNTIME"])
provenance = json.loads((runtime / "provenance.json").read_text())
for entry in provenance["files"]:
    assert hashlib.sha256(Path(entry["path"]).read_bytes()).hexdigest() == entry["sha256"]
head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
reports = []
for shape in ("endstation_ax7101_1x1_tdm8", "endstation_ax7101_8x8"):
    for interfaces in (1, 2):
        output = root / f"image-{shape}-if{interfaces}"
        command = ["python3", "sw/firmware/ctrl/test/ctrl_image.py", "--config", f"configs/{shape}.yaml",
                   "--output", str(output), "--interfaces", str(interfaces), "--libc", str(runtime / "libc.a"),
                   "--compiler-runtime", str(runtime / "libcompiler_rt.a")]
        subprocess.run(command, check=True)
        report = json.loads((output / "size.json").read_text())
        report["head"] = head
        reports.append(report)
(root / "image-results.json").write_text(json.dumps(reports, indent=2) + "\n")
