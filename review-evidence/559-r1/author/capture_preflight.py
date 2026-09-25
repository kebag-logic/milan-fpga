"""Run the product fixture in the foreground to its terminal capture marker."""
import os
from pathlib import Path
import selectors
import subprocess
import time

gateware = Path('$VALIDATION_STORAGE/559-a307-product-preflight/endstation_ax7101_8x8/gateware')
with subprocess.Popen(['obj_dir/Vsim'], cwd=gateware, stdin=subprocess.PIPE,
                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
    selector = selectors.DefaultSelector()
    selector.register(proc.stdout, selectors.EVENT_READ)
    deadline = time.monotonic() + 1800
    output = bytearray()
    passed = False
    while time.monotonic() < deadline:
        for key, _ in selector.select(timeout=1):
            data = os.read(key.fileobj.fileno(), 65536)
            output.extend(data)
            print(data.decode(errors='replace'), end='', flush=True)
        if b'CAPTURE_DONE' in output:
            passed = b'ok=1' in output and b'mismatches=0' in output
            break
        if b'CAPTURE_FAILED' in output or proc.poll() is not None:
            break
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
    print('\nPRODUCT_CAPTURE_PREFLIGHT:', 'PASS' if passed else 'FAILED', flush=True)
    raise SystemExit(0 if passed else 1)
