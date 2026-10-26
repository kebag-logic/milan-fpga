#!/usr/bin/env python3
"""R699-3's delta mutants V07, V09 and V13, ported to the round-4 lines they target.

Usage: python3 -I port_r3_mutants.py <export root> <work dir>

Round 4 replaced the three source lines these mutants anchor on. Each port
keeps the original defect and states its new anchor:
  V07 per-word hold release removed: the per-word check is now `keeps()`.
  V09 return needs the exact mask: a return is now decided by the resumed
      track; the port again demands that the window's body carry the mask,
      so a body of returned words releases the hold, as the original did.
  V13 half-block candidate dropped: the twin offsets are now built as `pair`.
Each is KILLED when the planner self-test of the mutated copy exits non-zero.
"""
import pathlib
import subprocess
import sys

root, work = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
PORTS = (
    ("V07 per-word hold release removed",
     "if slot.image is not None and not slot.image.keeps(index, word):",
     "if False and slot.image is not None:"),
    ("V09 return needs the exact mask",
     "elif back is not None and abs(back) <= abs(final):",
     "elif back is not None and abs(back) <= abs(final) and "
     "_audio_image_mask(image.tag, image.base, image.start, body) == image.mask:"),
    ("V13 half-block candidate dropped",
     "pair = (near, near - AUDIO_BLOCK_FRAMES) if delta == AUDIO_BLOCK_FRAMES // 2 else (near,)",
     "pair = (near,)"),
)
text = (root / "tb/tools/torture_campaign.py").read_text(encoding="utf-8")
for number, (name, old, new) in enumerate(PORTS):
    if text.count(old) != 1:
        print(f"INVALID: {name} (anchor count {text.count(old)})", flush=True)
        continue
    here = work / f"p{number}"
    here.mkdir(parents=True, exist_ok=True)
    (here / "torture_campaign.py").write_text(text.replace(old, new), encoding="utf-8")
    run = subprocess.run([sys.executable, "-B", str(here / "torture_campaign.py"), "--self-test"],
                         capture_output=True, text=True, timeout=600, check=False)
    failing = sorted({line.split(" ")[1] for line in run.stderr.splitlines() if line.startswith(("FAIL: ", "ERROR: "))})
    print(f"{'KILLED' if run.returncode else 'SURVIVED'}: {name} rc={run.returncode} by {failing[:4]}", flush=True)
