#!/usr/bin/env python3
"""Finalize receipts and publication allowlist from the exact candidate checkout."""
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

PACKET = Path(__file__).resolve().parent
HEAD = "fa1294279c42f181b6f43c6e6bd812039798705c"


def main():
    report = (PACKET / "REPORT.md").read_text()
    assert report.splitlines()[0] == "[R500] POSITIVE - exact head " + HEAD
    assert report.splitlines()[-1] == "R500-5 FINISHED"
    assert "SKELETON" not in report
    results = json.loads((PACKET / "gate-results.json").read_text())
    assert len(results) == 13 and all(row["rc"] == 0 for row in results)
    for script in PACKET.glob("*.py"):
        ast.parse(script.read_text(), filename=script.name)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", GIT_NO_REPLACE_OBJECTS="1")
    with (PACKET / "final-integrity.log").open("wb") as log:
        result = subprocess.run([sys.executable, str(PACKET / "audit_checkout.py")],
                                env=env, stdout=log, stderr=subprocess.STDOUT, timeout=60)
    (PACKET / "final-integrity.rc").write_text(str(result.returncode) + "\n")
    assert result.returncode == 0
    sys.path.insert(0, str(Path.cwd() / "scripts"))
    from docs_check import scrub_files
    names = sorted(path.name for path in PACKET.iterdir()
                   if path.is_file() and path.name != "MANIFEST.sha256")
    findings, count = scrub_files(PACKET, names)
    receipt = f"Publication privacy scan: {count} text files, {len(findings)} findings\n"
    (PACKET / "publication-privacy.log").write_text(receipt + "\n".join(findings))
    assert not findings, findings
    names = sorted(path.name for path in PACKET.iterdir()
                   if path.is_file() and path.name != "MANIFEST.sha256")
    manifest = "".join(hashlib.sha256((PACKET / name).read_bytes()).hexdigest()
                       + "  " + name + "\n" for name in names)
    (PACKET / "MANIFEST.sha256").write_text(manifest)
    checked = subprocess.run(["sha256sum", "--check", "MANIFEST.sha256"],
                             cwd=PACKET, capture_output=True, text=True, check=True)
    assert len(checked.stdout.splitlines()) == len(names)
    print(f"PASS: {len(names)} publishable files, every manifest digest verified")
    print(receipt.strip())
    print("Final exact-byte, mode, index and required-gitlink audit: PASS")
    print("REPORT.md sha256: " + hashlib.sha256((PACKET / "REPORT.md").read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
