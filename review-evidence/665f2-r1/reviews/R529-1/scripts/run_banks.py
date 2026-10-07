#!/usr/bin/env python3
"""Run independent review banks concurrently; all children joined before exit."""
import argparse, concurrent.futures, json, os, pathlib, subprocess, time
p = argparse.ArgumentParser()
p.add_argument("source", type=pathlib.Path)
p.add_argument("packet", type=pathlib.Path)
p.add_argument("--verilator", required=True)
a = p.parse_args(); source = a.source.resolve(); packet = a.packet.resolve()
scratch = packet / "scratch"; receipts = packet / "receipts"
scratch.mkdir(exist_ok=True); receipts.mkdir(exist_ok=True)
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE="1", VERILATOR=a.verilator, CTRL_RV32_CC="riscv64-elf-gcc")
commands = {
 "ctrl-baseline": ["python3", "sw/firmware/ctrl/test/test_ctrl_firmware.py", "--require-rv32", "--build-dir", str(scratch / "baseline")],
 "coverage": ["python3", "sw/firmware/gtest/fw_coverage.py", "--check", "--jobs", "4", "--keep", str(scratch / "coverage")],
 "differential": ["python3", "sw/firmware/ctrl/test/maap_differential.py", "--keep", str(scratch / "differential")],
}
def normalize(t):
 return t.replace(str(source), "<source>").replace(str(packet), "<packet>").replace(str(pathlib.Path.home()), "<home>")
def bank(pair):
 name, argv = pair; start = time.monotonic()
 raw = scratch / (name + ".raw.log")
 with raw.open("w") as f:
  result = subprocess.run(argv, cwd=source, env=env, stdout=f, stderr=subprocess.STDOUT, timeout=570)
 elapsed = round(time.monotonic() - start, 3)
 (receipts / (name + ".log")).write_text(normalize(raw.read_text()))
 record = {"argv": [normalize(x) for x in argv], "rc": result.returncode, "seconds": elapsed}
 (receipts / (name + ".rc.json")).write_text(json.dumps(record, indent=2)+"\n")
 print(name, record, flush=True)
 return result.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
 results = list(executor.map(bank, commands.items()))
raise SystemExit(int(any(results)))
