#!/usr/bin/env python3
"""whole_gate_plant.py <packet> <base-gtree> <probe-json> <name>...

For each named probe of <probe-json> (patch_probe_hook.py's format), copy the
shared clone, plant the probe into the SHIPPING firmware file itself (which is
already AEM-first, so gate 1b's aem_first() is the identity on it), and run
the whole test_baremetal_profile_contract() uninstrumented. RETURNED means the
entire gate function accepted that firmware. <= 8 jobs at once."""
import json, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

P, G = Path(sys.argv[1]), Path(sys.argv[2])
probes = {p[0]: p for p in json.load(open(sys.argv[3]))}
V = "static int aem_loaded;\n"
O = "static void nvm_boot(void)\n{\n"

def job(name):
    probe = probes[name]
    t = P / "scratch" / f"w_{name}"
    shutil.rmtree(t, ignore_errors=True)
    subprocess.run(["cp", "-a", str(G), str(t)], check=True)
    fw = t / "sw/firmware/milan_baremetal/milan_baremetal.c"
    text = fw.read_text(encoding="utf-8")
    pairs = ([[V, V + probe[2]], [O, O + probe[3]]] if probe[1] == "nvm"
             else probe[2])
    for old, new in pairs:
        if old == new:
            continue
        assert text.count(old) == 1, (name, old)
        text = text.replace(old, new)
    fw.write_text(text, encoding="utf-8")
    log = P / "whole" / f"{name}.log"
    subprocess.run(["timeout", "2400", str(P / "scripts/run_gate.sh"), str(t), str(log)],
                   capture_output=True)
    out = log.read_text(errors="replace")
    if "R412 GATE FUNCTION RETURNED" in out:
        return f"{name}: RETURNED (whole gate function accepted the planted firmware)"
    last = [l for l in out.splitlines() if l.startswith("AssertionError")]
    return f"{name}: FAILED :: {(last[-1] if last else out[-400:])[:900]}"

(P / "whole").mkdir(exist_ok=True)
with ThreadPoolExecutor(max_workers=8) as ex:
    for line in ex.map(job, sys.argv[4:]):
        print(line, flush=True)
