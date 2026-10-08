"""Shared setup: argv[1] = candidate checkout, argv[2] = pinned lwSRP checkout, argv[3] = output dir."""
import sys
from pathlib import Path
REPO = Path(sys.argv[1]).resolve()
LWSRP = Path(sys.argv[2]).resolve()
OUT = Path(sys.argv[3]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(REPO / "sw/firmware/ctrl/test"))
