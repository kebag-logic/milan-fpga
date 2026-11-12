#!/usr/bin/env python3
"""adapter_mutants.py TREE OUTDIR - the reviewer's own plants on the ACMP adapter's redelivery (bfe7a9d6), each
run against the scratch copy's acmp arm (run_acmp_arm.py). Each plant is applied, the arm run, and the file
restored byte for byte. A plant is CAUGHT when any test other than the reviewer probes (ProbeP...) fails; probe results are
reported beside it. An optional third argument names the plants to run (comma-separated).
A control run with no plant must pass every test but may fail the probe only if the probe itself fails."""
import re
import subprocess
import sys
from pathlib import Path

tree, out = Path(sys.argv[1]), Path(sys.argv[2])
ONLY = set(sys.argv[3].split(",")) if len(sys.argv) > 3 else None  # optional plant names
src = tree / "sw/firmware/ctrl/acmp/acmp_mbx.c"
HERE = Path(__file__).resolve().parent
POLL = ("\tconst unsigned owed = m->acmp.owed_count;\n\t(void)acmp_poll(&m->acmp);\n"
        "\tif (m->acmp.owed_count < owed) {\n\t\tredeliver(m);\n\t}\n")
PLANTS = {
    "control-no-plant": None,
    # an empty kept record offered whenever a send freed a slot (len 0 reaches acmp_rx)
    "empty-kept-offered": ("\tif (m->kept.len != 0u) {\n\t\tif (!acmp_rx(", "\tif (true) {\n\t\tif (!acmp_rx("),
    # after a decline the redelivery takes the next record anyway, which overwrites the kept command
    "redelivery-past-a-decline": (
        "\tfor (unsigned k = 0; k < ACMP_MBX_REDELIVER_RECORDS && m->kept.len == 0u; ++k) {",
        "\tfor (unsigned k = 0; k < ACMP_MBX_REDELIVER_RECORDS; ++k) {"),
    # the redelivery runs before the send that frees the slot, not after it
    "redelivery-before-the-send": (
        POLL,
        "\tconst unsigned owed = m->acmp.owed_count;\n\tif (owed != 0u) {\n\t\tredeliver(m);\n\t}\n"
        "\t(void)acmp_poll(&m->acmp);\n"),
    # a refused record does not end the redelivery (the loop's own receive service continues after one)
    "redelivery-continues-after-a-refusal": (
        "\t\tif (st != MBX_STATUS_OK) {\n\t\t\tl->stats.rx_bad += st == MBX_STATUS_BAD;\n\t\t\treturn;\n\t\t}",
        "\t\tif (st != MBX_STATUS_OK) {\n\t\t\tl->stats.rx_bad += st == MBX_STATUS_BAD;\n"
        "\t\t\tif (st == MBX_STATUS_BAD) {\n\t\t\t\tcontinue;\n\t\t\t}\n\t\t\treturn;\n\t\t}"),
    # the redelivery takes two records at most
    "redelivery-two-records": (
        "\tfor (unsigned k = 0; k < ACMP_MBX_REDELIVER_RECORDS && m->kept.len == 0u; ++k) {",
        "\tfor (unsigned k = 0; k < 2u && m->kept.len == 0u; ++k) {"),
}
orig = src.read_bytes()
for name, plant in PLANTS.items():
    if ONLY is not None and name not in ONLY:
        continue
    text = orig.decode()
    if plant is not None:
        old, new = plant
        assert text.count(old) == 1, name
        src.write_text(text.replace(old, new, 1))
    try:
        p = subprocess.run([sys.executable, "-I", str(HERE / "run_acmp_arm.py"), str(tree), str(out / name)],
                           capture_output=True, text=True, cwd=tree)
    finally:
        src.write_bytes(orig)
    log = p.stdout + p.stderr
    (out / f"{name}.log").write_text(log)
    allf = sorted(set(re.findall(r"\[  FAILED  \] (\S+)", log)))
    fails = [f for f in allf if not f.startswith("AcmpMailbox.ProbeP")]
    pf = [f for f in allf if f.startswith("AcmpMailbox.ProbeP")]
    probe = ("probes FAILED: " + ", ".join(pf)) if pf else "probes passed"
    if "REFUSED" in log or p.returncode not in (0, 1):
        res = f"REFUSED/BUILD rc {p.returncode}"
    else:
        res = ("CAUGHT by " + ", ".join(fails)) if fails else ("ESCAPED" if plant else "PASS (control)")
    print(f"{name}: {res}; {probe}; arm rc {p.returncode}", flush=True)
assert src.read_bytes() == orig
print("restored", src)
