#!/usr/bin/env python3
"""collect3.py RECEIPTS HEAD10: round 3's receipts outside identity/: the sweep at HEAD, the gates and planted
defects at HEAD, the harness images and input carry at HEAD, the tools. Host paths are replaced by placeholders,
then each text is passed through the publication's privacy scrub, so the archive publishes it unchanged."""
import re
import sys
from pathlib import Path

sys.path.insert(0, "<home>/milan-fpga-management/2026-09-23")
import privacy  # noqa: E402

R, H = Path(sys.argv[1]), sys.argv[2]
S = Path("<scratch>")
L = S / "logs2"
SANITISE = (("<train-scratch>", "<train-scratch>"), (str(S), "<scratch>"),
            ("<lane>", "<lane>"), ("<home>", "<home>"), ("<host-tools>", "<host-tools>"),
            ("<host-tmp>", "<host-tmp>"), ("<host-data>", "<host-data>"))


def put(rel, text, header=None):
    for old, new in SANITISE:
        text = text.replace(old, new)
    if header:
        text = header.rstrip("\n") + "\n" + text
    if len(text.encode()) > 190_000:
        lines = text.splitlines()
        text = "\n".join(lines[:400] + [f"[... {len(lines) - 800} lines cut to keep the receipt under 200 KB ...]"]
                         + lines[-400:]) + "\n"
    data = privacy.scrub_redact(text.encode())
    dst = R / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(data)


def drop_software(text):
    kept = [line for line in text.splitlines() if not re.match(r"\s+only (A|B): software/", line)]
    return "\n".join(kept) + "\n"


short = H[:8]
put(f"f1/rsweep-{short}.txt", drop_software((L / f"rsweep-{H}.log").read_text()),
    f"# rsweep2.sh in a fresh clone of {short}: yosys_sweep.py shapes, soc_sweep.py export of every SoC variant "
    "(LiteX venv, pinned RV32 SDK), then the missing-image control and the comparison with base 59b09884")
put(f"f1/axilite-xdc-{short}.txt", (L / f"axilite-xdc-{H}.txt").read_text())
put(f"gates/plants-{short}.txt", (L / f"plants-{H}.txt").read_text())
put(f"gates/round-checks-{short}.txt", (L / f"r2checks-{H}.log").read_text(),
    f"# quick.sh over checks/r2.tsv (the sweep and yosys self-tests, the diagram regeneration, the harness argv "
    f"checks, solution docs, doc paths) on a clean clone at {short}")
put(f"gates/docswf-{short}.txt", (L / f"docswf-{H}.log").read_text(),
    f"# the docs workflow's 103 commands (docswf4.tsv: the removed lane interpreter replaced by the system one, the four Markdown-renderer rows on the pinned Markdown venv), "
    f"quick.sh on a clean clone at {short}; one line per check: name, rc, its last line")
for p in ("1x1", "8x8"):
    put(f"gates/inputs-carry-{p}-{short}.txt", (L / f"inputs-carry-{p}-{H}.txt").read_text())
put(f"s1/harness-images-{short}.txt", "".join((S / "meas5" / p / "hashes.txt").read_text() for p in ("1x1", "8x8-1if")),
    f"# hbuild2.sh at {short}: each arm's ctrl_app.elf sha256 and its group partition line (legs.py build)")
for name in ("plants3.py", "build3.py", "publish_check.py", "collect3.py", "rsweep2.sh", "rsweep.sh", "quick.sh",
             "hbuild2.sh", "carry2.sh", "index2.py"):
    put(f"tools/{name}", (S / "bin" / name).read_text())
for name in ("docswf4.tsv", "r2.tsv"):
    put(f"tools/{name}", (S / "checks" / name).read_text())
print("collected")
