#!/usr/bin/env python3
"""Rerun both reviewers' gate-1b plant probes, unmodified, at one exported head.

usage: rerun_reviewer_probes.py <pristine-export> <work-dir> <receipt-dir>

For each plant of R413-2's plants.py (with instrument_builder.py and its run_gate1b.py,
R413_STOP_AFTER_BASELINE=1) and of R412-2's plants2.py (with early_stop.py and its
run_gate1b.py, R412_EARLY=1), this makes a hard-linked copy of the export whose firmware
and test_builder.py are fresh files, instruments and plants it with the reviewer's own
script, runs the reviewer's runner, and writes <receipt-dir>/<reviewer>_<plant>.log.
R413-2's forget-on-call arm (R413_FORCE_FORGET=1) is run once on the unplanted head.
Prints one line per probe: ACCEPTED (with kept) or REFUSED (with the refusal's pins).
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

pristine, work, receipts = (Path(arg).resolve() for arg in sys.argv[1:4])
PY = "$WORKSPACE_HOME/litex-milan/venv/bin/python"
R413 = Path("$REVIEWS/70L2-r413-2-packet/probes")
R412 = Path("$REVIEWS/70L2-r412-2-packet/scripts")
FIRMWARE = "sw/firmware/milan_baremetal/milan_baremetal.c"
BUILDER = "sw/builder/test_builder.py"
R413_PLANTS = ("none", "plain_write", "splice_write", "paste_write", "alias_write", "m_macro_set",
               "m_macro_addr", "m_macro_addr_sscanf", "asm_label_sscanf", "inline_asm_la",
               "alias_sscanf", "weakref_sscanf", "block_extern_sscanf")
R412_PLANTS = ("plain_write", "splice_write", "paste_write", "m_macro_set", "m_macro_addr",
               "m_macro_addr_sscanf", "alias_write", "alias_addr", "alias_decl_only",
               "static_alias_addr", "static_alias_write")
PINS = ("a store lands on aem_loaded's storage", "the linked image forms the full address",
        "another symbol of the linked image", "not a local object of the linked image",
        "an AUIPC of the linked image", "the address of aem_loaded is taken",
        "not a file-scope static of the compiled unit", "named in a second translation unit",
        "boot-unit asm allowlist rule")


def fresh_copy(name: str) -> Path:
    """A hard-linked copy of the export whose two edited files are its own."""
    copy = work / name
    if copy.exists():
        shutil.rmtree(copy)
    subprocess.run(["cp", "-al", str(pristine), str(copy)], check=True)
    for leaf in (FIRMWARE, BUILDER):
        (copy / leaf).unlink()
        shutil.copyfile(pristine / leaf, copy / leaf)
    return copy


def probe(label: str, steps: list[list[str]], runner: list[str], env: dict[str, str]) -> None:
    """Run the setup steps and the runner; write the receipt and print one line."""
    lines = []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", **env)
    for argv in steps:
        got = subprocess.run(argv, capture_output=True, text=True, check=True, env=env)
        lines.append(got.stdout.strip())
    got = subprocess.run(runner, capture_output=True, text=True, env=env)
    text = "\n".join(lines + [got.stdout.strip(), got.stderr.strip()[-2000:], f"rc={got.returncode}"])
    (receipts / f"{label}.log").write_text(text + "\n")
    refused = re.search(r"(?:GATE REFUSED|GATE1B REFUSED|forget-on-call REFUSED):(.*)", text)
    kept = re.search(r"kept=\s*(\[[^\]]*\]|None)", text)
    if refused:
        named = [pin for pin in PINS if pin in refused.group(1)]
        print(f"{label:34s} REFUSED rc={got.returncode} pins={named or refused.group(1)[:160]}")
    else:
        print(f"{label:34s} ACCEPTED rc={got.returncode} kept={kept.group(1) if kept else '?'}")


work.mkdir(parents=True, exist_ok=True)
receipts.mkdir(parents=True, exist_ok=True)
for plant in R413_PLANTS:
    copy = fresh_copy(f"r413_{plant}")
    probe(f"r413_{plant}",
          [["python3", str(R413 / "instrument_builder.py"), str(copy / BUILDER)],
           ["python3", str(R413 / "plants.py"), str(copy), plant]],
          [PY, str(R413 / "run_gate1b.py"), str(copy)],
          {"R413_STOP_AFTER_BASELINE": "1", "R413_HEAD_TREE": str(pristine)})
    shutil.rmtree(copy)
copy = fresh_copy("r413_none_forget")
probe("r413_none_forget",
      [["python3", str(R413 / "instrument_builder.py"), str(copy / BUILDER)]],
      [PY, str(R413 / "run_gate1b.py"), str(copy)],
      {"R413_STOP_AFTER_BASELINE": "1", "R413_FORCE_FORGET": "1"})
shutil.rmtree(copy)
for plant in R412_PLANTS:
    copy = fresh_copy(f"r412_{plant}")
    probe(f"r412_{plant}",
          [["python3", str(R412 / "early_stop.py"), str(copy)],
           ["python3", str(R412 / "plants2.py"), str(copy), plant]],
          [PY, str(R412 / "run_gate1b.py"), str(copy)],
          {"R412_EARLY": "1", "R412_ASM_OUT": str(work / f"r412_{plant}.s")})
    shutil.rmtree(copy)
