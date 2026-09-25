"""Boot the generated CPU model to a bounded, observed BIOS prompt."""
import os
import re
from pathlib import Path
import selectors
import subprocess
import time

gateware = Path("$VALIDATION_STORAGE/559-a307-cpu-preflight/soc/gateware")
with subprocess.Popen(["obj_dir/Vsim"], cwd=gateware, stdin=subprocess.DEVNULL,
                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
    selector = selectors.DefaultSelector()
    selector.register(proc.stdout, selectors.EVENT_READ)
    deadline = time.monotonic() + 300
    output = bytearray()
    passed = False
    while time.monotonic() < deadline:
        for key, _ in selector.select(timeout=1):
            data = os.read(key.fileobj.fileno(), 65536)
            output.extend(data)
            print(data.decode(errors="replace"), end="", flush=True)
        if b"litex>" in re.sub(rb"\x1b\[[0-9;]*m", b"", output):
            passed = True
            break
        if proc.poll() is not None:
            break
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
    print("\nPRODUCT_CPU_BOOT:", "PASS" if passed else "FAILED", flush=True)
    raise SystemExit(0 if passed else 1)
