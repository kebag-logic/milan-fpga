#!/usr/bin/env python3
"""collect2.py RECEIPTS: copy round 2's receipts (outside identity/) from the scratch logs into RECEIPTS, host paths
replaced by placeholders, each a text file under 200 KB (long logs cut to their head and tail, the cut stated)."""
import re
import sys
from pathlib import Path

R = Path(sys.argv[1])
S = Path("<scratch>")
L = S / "logs2"
SANITISE = (("<train-scratch>", "<train-scratch>"), (str(S), "<scratch>"),
            ("<lane>", "<lane>"), ("<home>", "<home>"), ("<host-tools>", "<host-tools>"),
            ("<host-tmp>", "<host-tmp>"), ("<host-data>", "<host-data>"))


def clean(text):
    for old, new in SANITISE:
        text = text.replace(old, new)
    return text


def put(rel, text, header=None):
    dst = R / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    text = clean(text)
    if header:
        text = header.rstrip("\n") + "\n" + text
    if len(text.encode()) > 190_000:
        lines = text.splitlines()
        text = "\n".join(lines[:400] + [f"[... {len(lines) - 800} lines cut to keep the receipt under 200 KB ...]"]
                         + lines[-400:]) + "\n"
    dst.write_text(text)


def drop_software(text):
    """cmp_export.py lists build-tree object files that differ by name only (their path is in it): counted, not listed."""
    kept = [line for line in text.splitlines() if not re.match(r"\s+only (A|B): software/", line)]
    return "\n".join(kept) + "\n"


SWEEP = ("# rsweep.sh{2} in a fresh clone of {0}: yosys_sweep.py shapes, then soc_sweep.py export of every SoC variant "
         "(LiteX venv, pinned RV32 SDK){1}\n")
put("f1/rsweep-59b09884-base.txt", (L / "rsweep-base.log").read_text(), SWEEP.format("base 59b09884", "", ""))
put("f1/rsweep-62477be4-reproduction.txt", (L / "rsweep-h0.log").read_text()
    + "\n# the ship export's own log, its last lines:\n"
    + "\n".join((S / "work/rs-h0/soc/ship/export.log").read_text().splitlines()[-6:]) + "\n",
    SWEEP.format("round 1's head 62477be4", ": the reproduction of R880-1-F1", ""))
put("f1/rsweep-59f91d9f.txt", drop_software((L / "rsweep-f1.log").read_text()),
    SWEEP.format("the fixing head 59f91d9f", "; then the missing-image control and the comparison with base", "2"))
put("f1/rsweep-a9da4c48.txt", drop_software((L / "rsweep-a9da4c4814.log").read_text()),
    SWEEP.format("a9da4c48 (the final head but for one generated docs page)",
                 "; then the missing-image control and the comparison with base", "2"))
put("f1/exports-a9da4c48.json", (S / "work/rs-a9da4c4814/soc/exports.json").read_text())
put("f1/axilite-xdc-a9da4c48.txt", (L / "axilite-xdc-a9da4c4814.txt").read_text())
put("f1/yosys-shapes-59b09884-vs-62477be4.txt", (L / "yosys-shapes-59b09884-vs-62477be4.txt").read_text())
put("s1/harness-argv-a9da4c48.txt", (L / "harness-argv-a9da4c4814.txt").read_text())
for name, label in (("meas-bench", "8c5e2b4f"), ("meas2", "2f985971"), ("meas3", "a9da4c48")):
    text = "".join((S / name / p / "hashes.txt").read_text() for p in ("1x1", "8x8-1if"))
    put(f"s1/harness-images-{label}.txt", text, f"# hbuild2.sh at {label}: each arm's ctrl_app.elf sha256 and its "
                                               f"group partition line (legs.py build)")
put("gates/plants-9413958c.txt", (L / "plants-9413958c66.txt").read_text())
for name, label in (("r2checks-a9da4c4814", "a9da4c48"), ("r2checks-2f985971fc", "2f985971")):
    put(f"gates/round2-checks-{label}.txt", (L / f"{name}.log").read_text(),
        f"# quick.sh over checks/r2.tsv (this round's checks) on a clean clone at {label}")
for name, label, what in (("docswf-9413958c66", "9413958c", "the docs workflow's 103 commands"),
                          ("docswf-2f985971fc", "2f985971", "the docs workflow's 103 commands"),
                          ("quick-2f985971fc", "2f985971", "the quick list's 58 commands")):
    if (L / f"{name}.log").is_file():
        put(f"gates/{name.split('-')[0]}-{label}.txt", (L / f"{name}.log").read_text(),
            f"# {what}, quick.sh on a clean clone at {label}; one line per check: name, rc, its last line")
for p in ("1x1", "8x8"):
    for h in ("2f985971fc", "a9da4c4814"):
        put(f"gates/inputs-carry-{p}-{h[:8]}.txt", (L / f"inputs-carry-{p}-{h}.txt").read_text())
for name in ("rsweep.sh", "rsweep2.sh", "quick.sh", "clone.sh", "bgunit.sh", "hbuild2.sh", "carry2.sh", "collect2.py",
             "index2.py", "env.sh", "fwenv.sh"):
    put(f"tools/{name}", (S / "bin" / name).read_text())
for name in ("q.tsv", "docswf2.tsv", "r2.tsv"):
    put(f"tools/{name}", (S / "checks" / name).read_text())
print("collected")
