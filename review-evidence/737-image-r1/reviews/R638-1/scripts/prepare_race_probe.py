#!/usr/bin/env python3
"""Drive build.prepare's download pool over two lock rows that share one staged filename.

usage: prepare_race_probe.py <exact-head tree>
No network: urlopen is replaced by a slow in-memory stream with the right bytes.
"""
import hashlib, io, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(sys.argv[1]) / "ci/image"))
import build

payload = b"x" * (4 * 1024 * 1024)
row = {"tool": "dup", "size": len(payload), "sha256": hashlib.sha256(payload).hexdigest(), "url": "https://example.invalid/a"}

class Slow(io.BytesIO):
    def read(self, n=-1):
        time.sleep(0.01)
        return super().read(min(n, 65536) if n and n > 0 else 65536)
    def __enter__(self): return self
    def __exit__(self, *a): return False

outcomes = {"pass": 0, "refused": 0}
for trial in range(10):
    with tempfile.TemporaryDirectory() as d:
        target = Path(d) / "maven" / "same-name.jar"
        with patch("urllib.request.urlopen", side_effect=lambda *a, **k: Slow(payload)):
            with ThreadPoolExecutor(max_workers=4) as pool:
                try:
                    list(pool.map(lambda pair: build.verified_download(*pair), [(row, target), (dict(row, tool="dup2"), target)]))
                    outcomes["pass"] += 1
                except (OSError, ValueError) as error:
                    outcomes["refused"] += 1
                    last = f"{type(error).__name__}: {error}".replace(d, "<tmp>")
print(outcomes)
if outcomes["refused"]:
    print("example:", last)
