#!/usr/bin/env python3
"""Copy one gate run's logs into a receipts directory: every file under 200 KB as it is, and for a larger one
its last 60,000 bytes from a line start as NAME.tail, with its full size and sha256 in large-files.txt.
The runner's own log is copied as runner.log. For the firmware campaign (ctrl_firmware.log) the full log's
verdict lines are tallied in ctrl_firmware-tally.txt: each plant's "[ok]" and "[ESCAPED]" lines, each plant's
first reddened test, and the driver's verdict.

Usage: collect_gates.py GATE_OUT_DIR RUNNER_LOG RECEIPTS_DIR
"""
import hashlib
import shutil
import sys
from pathlib import Path

LIMIT = 200_000
TAIL = 60_000

src, runner, dst = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
dst.mkdir(parents=True, exist_ok=True)
large = []
for path in sorted(p for p in src.iterdir() if p.is_file()):
    data = path.read_bytes()
    if len(data) < LIMIT:
        shutil.copyfile(path, dst / path.name)
        continue
    tail = data[-TAIL:]
    tail = tail[tail.find(b'\n') + 1:]
    (dst / f'{path.name}.tail').write_bytes(tail)
    large.append(f'{path.name}\t{len(data)}\t{hashlib.sha256(data).hexdigest()}')
if large:
    (dst / 'large-files.txt').write_text('file\tbytes\tsha256\n' + '\n'.join(large) + '\n')
shutil.copyfile(runner, dst / 'runner.log')
firmware = src / 'ctrl_firmware.log'
if firmware.is_file():
    lines = firmware.read_text(errors='replace').splitlines()
    verdicts = [line for line in lines if line.startswith('test_ctrl_firmware:')]
    (dst / 'ctrl_firmware-tally.txt').write_text(
        f'[ok] lines: {sum(line.lstrip().startswith("[ok]") for line in lines)}\n'
        f'[ESCAPED] lines: {sum("[ESCAPED]" in line for line in lines)}\n'
        f"'first: [FAIL]' lines (each plant's first reddened test): {sum('first: [FAIL]' in line for line in lines)}\n"
        f'verdict: {verdicts[-1] if verdicts else "none"}\n')
print(f'{dst}: copied {sum(1 for _ in src.iterdir()) - len(large)} logs, kept {len(large)} as tails')
