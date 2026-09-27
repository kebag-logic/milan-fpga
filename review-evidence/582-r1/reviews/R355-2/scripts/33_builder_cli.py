#!/usr/bin/env python3
"""Reviewer probe: the real builder CLI on planted clock variants, base vs head.

Usage: 33_builder_cli.py <tree> <label> <scratch-dir>
Each variant is written to scratch, built with --write-fragment into a fresh
output directory, and recorded with rc, the last diagnostic line and whether
any output or fragment was written.
"""
import copy
import hashlib
import subprocess
import sys
from pathlib import Path

import yaml

TREE, LABEL, X = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
X.mkdir(parents=True, exist_ok=True)
frag_dir = TREE / "configs/generated"


def frag_state():
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(frag_dir.glob("sweep_opts_*.sh"))}


def variant(name, mutate, expect):
    raw = yaml.safe_load((TREE / f"configs/{name}.yaml").read_text())
    raw = copy.deepcopy(raw)
    mutate(raw)
    return raw, expect


def c(**kw):
    return lambda r: r["board"]["constraints"].update(kw)


CASES = [
    ("8x8 at 100 MHz (#565 observation)", "endstation_ax7101_8x8", c(milan_clk_hz=100_000_000), "refuse"),
    ("1x1 at 80 MHz (former ROM variant)", "endstation_ax7101_1x1_tdm8", c(milan_clk_hz=80_000_000), "refuse"),
    ("arty_4x4 at 50000001", "endstation_arty_4x4", c(milan_clk_hz=50_000_001), "refuse"),
    ("arty_current at 49999999", "endstation_arty_current", c(milan_clk_hz=49_999_999), "refuse"),
    ("arty_8ch at 25 MHz", "endstation_arty_8ch", c(milan_clk_hz=25_000_000), "refuse"),
    ("1x1 flashboot none at 100 MHz", "endstation_ax7101_1x1_tdm8", c(milan_clk_hz=100_000_000, flashboot="none"), "refuse"),
    ("1x1 milan equals sys at 100 MHz", "endstation_ax7101_1x1_tdm8", c(milan_clk_hz=100_000_000, sys_clk_hz=100_000_000), "refuse"),
    ("1x1 milan and sys both 50 MHz", "endstation_ax7101_1x1_tdm8", c(milan_clk_hz=50_000_000, sys_clk_hz=50_000_000), "record"),
    ("1x1 milan as float 50000000.0", "endstation_ax7101_1x1_tdm8", c(milan_clk_hz=50_000_000.0), "record"),
    ("1x1 milan as float 50000000.9", "endstation_ax7101_1x1_tdm8", c(milan_clk_hz=50_000_000.9), "record"),
    ("1x1 milan omitted", "endstation_ax7101_1x1_tdm8", lambda r: r["board"]["constraints"].pop("milan_clk_hz"), "refuse-any"),
    ("1x1 unchanged", "endstation_ax7101_1x1_tdm8", lambda r: None, "accept"),
]
bad = 0
before = frag_state()
for i, (label, name, mutate, expect) in enumerate(CASES):
    raw, _ = variant(name, mutate, expect)
    cfg = X / f"{LABEL}-{i:02d}.yaml"
    cfg.write_text(yaml.safe_dump(raw))
    out = X / f"{LABEL}-{i:02d}-out"
    proc = subprocess.run([sys.executable, "sw/builder/endstation_builder.py", str(cfg), "-o", str(out), "--write-fragment"],
                          cwd=TREE, capture_output=True, text=True, timeout=600)
    last = (proc.stdout + proc.stderr).strip().splitlines()[-1:] or [""]
    wrote = out.exists() and any(out.rglob("*"))
    frag_changed = frag_state() != before
    if frag_changed:
        before = frag_state()
    ok = {"refuse": proc.returncode != 0 and "baremetal clock:" in last[0] and not wrote,
          "refuse-any": proc.returncode != 0 and not wrote,
          "accept": proc.returncode == 0,
          "record": True}[expect]
    bad += not ok
    print(f"[{LABEL}] {'ok ' if ok else 'BAD'} rc={proc.returncode} wrote={wrote} fragment-changed={frag_changed} "
          f"expect={expect} {label} :: {last[0][:150]}")
print(f"[{LABEL}] {len(CASES)} cases, {bad} unexpected")
sys.exit(1 if bad else 0)
