#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probes: build the stack's adp_tests on a copy of the exact head with one planted change each.
Usage: stack_probes.py REPO OUTDIR JOBS"""
import json, subprocess, sys, os, shutil
from concurrent.futures import ThreadPoolExecutor
repo, out, jobs = sys.argv[1], sys.argv[2], int(sys.argv[3])
GM = "\tif (a->enabled && a->state == ADP_STATE_WAITING) {\n\t\tenter_delay(a, ADP_DRAW_DELAY);"
RX = "\ttimer_stop(a);                                                  // Milan v1.2 5.6.3.5.4\n\tenter_delay(a, ADP_DRAW_DELAY);"
PLANTS = [
    ("control-no-change", "src/adp.c", None, None),
    ("gm-change-draws-link-up-kind", "src/adp.c", GM, GM.replace("ADP_DRAW_DELAY", "ADP_DRAW_LINK_UP")),
    ("gm-change-draws-startup-kind", "src/adp.c", GM, GM.replace("ADP_DRAW_DELAY", "ADP_DRAW_STARTUP")),
    ("discover-draws-link-up-kind", "src/adp.c", RX, RX.replace("ADP_DRAW_DELAY", "ADP_DRAW_LINK_UP")),
    ("startup-draws-link-up-kind", "src/adp.c", "enter_delay(a, ADP_DRAW_STARTUP);", "enter_delay(a, ADP_DRAW_LINK_UP); "),
    ("link-up-range-one-second", "include/adp.h", "#define ADP_DELAY_LINK_UP_MAX_MS 500u", "#define ADP_DELAY_LINK_UP_MAX_MS 1000u"),
    ("startup-range-one-second", "include/adp.h", "#define ADP_DELAY_STARTUP_MAX_MS 500u", "#define ADP_DELAY_STARTUP_MAX_MS 1000u"),
    ("delay-range-half-second", "include/adp.h", "#define ADP_DELAY_MAX_MS 4000u", "#define ADP_DELAY_MAX_MS 500u  "),
]
env = dict(os.environ)
def one(p):
    name, path, old, new = p
    d = os.path.join(out, name); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    subprocess.run(f"git -C {repo} archive HEAD | tar -x -C {d}", shell=True, check=True)
    if old is not None:
        f = os.path.join(d, path); s = open(f).read()
        assert s.count(old) == 1, (name, s.count(old)); open(f, "w").write(s.replace(old, new))
    log = open(os.path.join(d, "probe.log"), "w")
    rc = subprocess.run(["cmake", "-S", d, "-B", d + "/b", "-DCMAKE_BUILD_TYPE=Debug"], stdout=log, stderr=subprocess.STDOUT).returncode
    if rc == 0:
        rc = subprocess.run(["cmake", "--build", d + "/b", "-j2", "--target", "adp_tests"], stdout=log, stderr=subprocess.STDOUT).returncode
    if rc != 0:
        return {"plant": name, "build_rc": rc}
    r = subprocess.run([d + "/b/adp_tests"], capture_output=True, text=True)
    failed = sorted({l.split()[-1] for l in r.stdout.splitlines() if l.startswith("[  FAILED  ]") and "." in l and "ms)" in l})
    msgs = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith(("A0", "A3", "A9", "A18", "A20", "A2", "A4", "valid discovery"))]
    open(os.path.join(d, "adp_tests.out"), "w").write(r.stdout)
    return {"plant": name, "build_rc": 0, "test_rc": r.returncode, "verdict": "caught" if r.returncode else "SURVIVED", "failed_tests": failed, "messages": msgs[:12]}
with ThreadPoolExecutor(jobs) as ex:
    res = list(ex.map(one, PLANTS))
print(json.dumps(res, indent=1))
