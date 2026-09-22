import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import time

root = Path("/tmp/milan-504-a160-7_lvwnpb")
url = "https://toolchains.bootlin.com/downloads/releases/toolchains/riscv32-ilp32d/tarballs/riscv32-ilp32d--glibc--stable-2025.08-1.tar.xz"
size = 102597892
parts = 6
def fetch(index):
    start, end = size * index // parts, size * (index + 1) // parts - 1
    path = root / f"part{index}"
    argv = ["curl", "--fail", "--silent", "--show-error", "--location", "--retry", "4", "--retry-all-errors", "--max-time", "45", "--range", f"{start}-{end}", "--output", str(path), url]
    if path.exists() and path.stat().st_size == end - start + 1:
        return {"argv": argv, "exit": 0, "bytes": path.stat().st_size, "reused_completed_range": True}
    begin = time.time()
    result = subprocess.run(argv)
    record = {"argv": argv, "exit": result.returncode, "elapsed_seconds": time.time() - begin, "bytes": path.stat().st_size}
    assert result.returncode == 0 and path.stat().st_size == end - start + 1, record
    print(json.dumps(record), flush=True)
    return record
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    records = list(pool.map(fetch, range(parts)))
with (root / "verified-download.tar.xz").open("wb") as output:
    for index in range(parts):
        with (root / f"part{index}").open("rb") as source:
            while block := source.read(1024 * 1024):
                output.write(block)
archive = root / "verified-download.tar.xz"
with archive.open("rb") as source:
    digest = hashlib.file_digest(source, "sha256").hexdigest()
assert digest == "d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f", digest
Path(__file__).with_suffix(".json").write_text(json.dumps({"parts": records, "archive": str(archive), "bytes": archive.stat().st_size, "sha256": digest}, indent=2) + "\n")
print("Verified archive:", archive, digest, flush=True)
