#!/usr/bin/env python3
"""adapter_mutants.py TREE OUTDIR - reviewer's own plants on the ACMP adapter's kept command, each run against
the scratch copy's acmp arm (run_acmp_arm.py). Each plant is applied, the arm run, and the file restored byte for
byte. A plant is CAUGHT when any test other than the reviewer probe (ProbeP1...) fails."""
import re
import subprocess
import sys
from pathlib import Path

tree, out = Path(sys.argv[1]), Path(sys.argv[2])
src = tree / "sw/firmware/ctrl/acmp/acmp_mbx.c"
HERE = Path(__file__).resolve().parent
PLANTS = {
    # the kept record offered before the poll that frees its slot, not after it
    "kept-offered-before-the-poll": (
        "\tconst unsigned owed = m->acmp.owed_count;\n\t(void)acmp_poll(&m->acmp);\n"
        "\tif (m->kept.len != 0u && m->acmp.owed_count < owed &&\n"
        "\t    acmp_rx(&m->acmp, m->kept.interface, m->kept.frame, m->kept.len)) {\n\t\tm->kept.len = 0u;\n\t}\n",
        "\tconst unsigned owed = m->acmp.owed_count;\n"
        "\tif (m->kept.len != 0u && owed != 0u &&\n"
        "\t    acmp_rx(&m->acmp, m->kept.interface, m->kept.frame, m->kept.len)) {\n\t\tm->kept.len = 0u;\n\t}\n"
        "\t(void)acmp_poll(&m->acmp);\n"),
    # the poll offers an empty kept record whenever a send freed a slot (len 0 reaches acmp_rx)
    "empty-kept-offered": (
        "\tif (m->kept.len != 0u && m->acmp.owed_count < owed &&",
        "\tif (m->acmp.owed_count < owed &&"),
}
orig = src.read_bytes()
res = {}
for name, (old, new) in PLANTS.items():
    text = orig.decode()
    assert text.count(old) == 1, name
    src.write_text(text.replace(old, new, 1))
    try:
        p = subprocess.run([sys.executable, "-I", str(HERE / "run_acmp_arm.py"), str(tree), str(out / name)],
                           capture_output=True, text=True, cwd=tree)
    finally:
        src.write_bytes(orig)
    log = p.stdout + p.stderr
    (out / f"{name}.log").write_text(log)
    fails = sorted(set(re.findall(r"\[  FAILED  \] (\S+)", log)) - {"AcmpMailbox.ProbeP1LaterKeptCommandBehindNoAnswerFramesAndATimerProbe"})
    refused = "REFUSED" in log
    res[name] = "REFUSED (build)" if refused else ("CAUGHT by " + ", ".join(fails) if fails else "ESCAPED")
    print(f"{name}: {res[name]}", flush=True)
assert src.read_bytes() == orig
print("restored", src)
