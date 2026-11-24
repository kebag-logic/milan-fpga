#!/usr/bin/env python3
"""Run only scripts/suite_preflight_controls.py's controls, through the same
disposable fixture test_suite_cancellation.py's main() gives them.

usage: python3 -I run_preflight_controls.py REPO
"""

import sys
import tempfile
from pathlib import Path


def main() -> int:
    repo = Path(sys.argv[1]).resolve()
    sys.path.insert(0, str(repo / "scripts"))
    import test_suite_cancellation as harness
    import suite_preflight_controls
    from owned_process import OwnedProcesses  # the same owner main() installs
    with tempfile.TemporaryDirectory(prefix="r-preflight-controls-") as directory:
        with OwnedProcesses():
            suite_preflight_controls.run(Path(directory), harness)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
