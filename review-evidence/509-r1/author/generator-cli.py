"""Reproduce every documented generator CLI boundary in temporary storage."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path.cwd()
receipts = Path(__file__).resolve().parent
expected = json.loads((receipts / "descriptor-audit.json").read_text())
results = []
with (receipts / "generator-cli.log").open("w") as log:
    with tempfile.TemporaryDirectory(prefix="509-generator-", dir="$VALIDATION_STORAGE") as scratch:
        work = Path(scratch)
        for item in expected["configurations"]:
            config = Path(item["config"])
            build = work / config.stem
            overlay = build / config.stem / "aem_overlay.json"
            binary = work / (config.stem + ".bin")
            commands = [
                [sys.executable, "sw/builder/endstation_builder.py", str(config), "-o", str(build)],
                [sys.executable, "avdecc/gen_aem_store.py", "--overlay", str(overlay),
                 "--out-dir", str(work / (config.stem + "-store"))],
                [sys.executable, "avdecc/gen_aemi_image.py", "--overlay", str(overlay),
                 "-o", str(binary), "-m", str(binary.with_suffix(".map")),
                 "--json", str(binary.with_suffix(".json"))],
            ]
            for command in commands:
                log.write(json.dumps(command) + "\n")
                log.flush()
                subprocess.run(command, cwd=root, stdout=log, stderr=subprocess.STDOUT,
                               check=True, timeout=7200)
            actual = binary.read_bytes()
            digest = hashlib.sha256(actual).hexdigest()
            assert len(actual) == item["image_bytes"]
            assert digest == item["sha256"], (config, digest, item["sha256"])
            results.append(dict(config=str(config), image_bytes=len(actual), sha256=digest,
                                generator_commands=3, exit_code=0))
            print(config, len(actual), digest, flush=True)
(receipts / "generator-cli.json").write_text(json.dumps(results, indent=2) + "\n")
print("All five CLI image hashes match the independent decoded audit.", flush=True)
