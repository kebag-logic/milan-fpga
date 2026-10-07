#!/usr/bin/env python3
"""Match each measured object size to the README row with the same BSS."""
import argparse
from pathlib import Path
import re
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("repo", type=Path)
args = parser.parse_args()
packet = Path(__file__).resolve().parent
repo = args.repo.resolve()
assert (packet / "ctrl-nvm.rc").read_text().strip() == "0"
log = (packet / "ctrl-nvm.log").read_text()
assert "OK across 5 shape(s), 435 tests" in log
assert "SKIPPED" not in log and "REFUSED" not in log and "[FAIL]" not in log
pattern = r"rv32 at (\d+) Hz: text=(\d+) data=(\d+) bss=(\d+) stage=(\d+) payload=(\d+) chunk=(\d+) store=(\d+) clock=(\d+) \(bytes\)"
measured = [tuple(map(int, m)) for m in re.findall(pattern, log)]
assert len(measured) == 5
by_bss = {m[3]: m for m in measured}
assert len(by_bss) == 5
path = "sw/firmware/ctrl_nvm/README.md"
old = subprocess.check_output(["git", "-C", str(repo), "show", "34475e77:" + path]).decode()
new = (repo/path).read_text()
old_lines, new_lines = old.splitlines(), new.splitlines()
assert len(old_lines) == len(new_lines)
rows = []
for number, (before, after) in enumerate(zip(old_lines,new_lines),1):
    if before == after:
        continue
    a = [s.strip() for s in before.strip("|").split("|")]
    b = [s.strip() for s in after.strip("|").split("|")]
    assert after.startswith("| `endstation_") and len(b) == 11
    assert a[:-1] == b[:-1]
    assert int(a[-1].replace(",","")) + 4 == int(b[-1].replace(",",""))
    values = [int(s.replace(",","")) for s in b[1:]]
    clock, records, container, stage, payload, chunk, state, counters, bss, text = values
    measurement = by_bss[bss]
    measured_clock, measured_text, measured_data, *measured_buffers = measurement
    # README has no data column; compare only the quantities it claims.
    assert (measured_clock, measured_text, *measured_buffers) == (clock,text,bss,stage,payload,chunk,state,counters), (b,measurement)
    rows.append((number,b[0].strip("`"),bss,text))
assert len(rows) == 5
changed = subprocess.check_output(["git","-C",str(repo),"diff","--name-only","34475e77","HEAD"]).decode().splitlines()
assert changed == [path]
assert subprocess.check_output(["git","-C",str(repo),"rev-list","--count","34475e77..HEAD"]).strip() == b"1"
assert subprocess.check_output(["git","-C",str(repo),"rev-parse","HEAD^"]).strip() == b"34475e774dfe1c92c81fa51293668e64dc95fa85"
print("PASS delta: one commit; one README; exactly five text cells; each +4; other bytes unchanged")
print("PASS gate: 435 tests across five shapes, zero skips; five RV32 object builds")
print("README line | shape | bss | measured text | README text")
for line,shape,bss,text in rows:
    print(f"{line} | {shape} | {bss} | {text} | {text}")
print("PASS all five rows matched by unique BSS, with clock and buffer dimensions also equal")
