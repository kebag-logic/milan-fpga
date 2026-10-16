#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Bind the isolated runtime reader and its helpers to the audited runner bytes."""

import argparse
import hashlib
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
FILES = ("ci_local_manifest.py", "ci_manifest.py", "ci_workflow_plan.py")


def main() -> int:
    """Regenerate only the designated digest block, or refuse any stale pin."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    block = "# BEGIN EVIDENCE HELPER PINS\nEVIDENCE_HELPERS = {\n"
    for name in FILES:
        digest = hashlib.sha256(ROOT.joinpath(name).read_bytes()).hexdigest()
        block += f'    "{name}": "{digest}",\n'
    block += "}\n# END EVIDENCE HELPER PINS"
    path = ROOT / "act_ci.py"
    original = path.read_text()
    changed, count = re.subn(r"# BEGIN EVIDENCE HELPER PINS.*?# END EVIDENCE HELPER PINS",
                            lambda _match: block, original, flags=re.DOTALL)
    if count != 1:
        raise ValueError("runner must contain exactly one helper pin block")
    if args.check:
        if original != changed:
            print("runtime evidence helper pins are stale")
            return 1
    else:
        path.write_text(changed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
