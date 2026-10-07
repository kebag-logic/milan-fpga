#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Reviewer-owned plants: each replaces one exact-once snippet in a scratch copy,
builds the unit target (optionally with sanitizers) and records whether the
author's suites detect it. Usage: plants.py SRC WORK PREFIX MILAN(OFF|ON) JOBS"""
import concurrent.futures as cf, json, os, shutil, subprocess, sys
from pathlib import Path

SRC, WORK, PREFIX, MILAN, JOBS = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4], int(sys.argv[5])
MAD, PDU, MSRP, MVRP = "src/core/mrp_mad.c", "src/core/mrp_pdu.c", "src/modules/msrp.c", "src/modules/mvrp.c"
# (label, file, old, new, sanitize)
PLANTS = [
    ("y01-no-map-error-stop", MAD, "if (rc->error || priv->map_error) {", "if (rc->error) {", False),
    ("y02-publish-ignores-policy", MAD, "        if (!(ports & (1u << work->port_id))) {", "        if (false && !(ports & (1u << work->port_id))) {", False),
    ("y03-no-pending-tx-rollback", MAD, "        ai->pending_tx = pending_from;\n", "", False),
    ("y04-list-skip-known-later", PDU, "if (unknown && msrp) {", "if ((unknown || later) && msrp) {", False),
    ("y05-list-skip-to-pdu-end", PDU, "            off = end;\n            continue;", "            off = len;\n            continue;", False),
    ("y06-reserve-misses-last-port", MAD, "p < priv_of(app)->n_ports && p < 32u; ++p) {\n        struct mrp_map_work *work = shlan_calloc", "p + 1u < priv_of(app)->n_ports && p < 32u; ++p) {\n        struct mrp_map_work *work = shlan_calloc", False),
    ("y07-no-policy-still-reserves", MAD, "    if (join ? !app->ops->map_join : !app->ops->map_leave) {\n        return 0;\n    }\n", "", True),
    ("y08-failure-returns-zero", MAD, "        return mapped;\n    }\n\n    switch (e->timer)", "        return 0;\n    }\n\n    switch (e->timer)", False),
    ("y09-changed-rjoinin-only", MAD, "if (changed && (ev == MRP_EVENT_RJOININ || ev == MRP_EVENT_RJOINMT)) {", "if (changed && (ev == MRP_EVENT_RJOININ)) {", False),
    ("y10-changed-any-event", MAD, "if (changed && (ev == MRP_EVENT_RJOININ || ev == MRP_EVENT_RJOINMT)) {", "if (changed) {", False),
    ("y11-changed-key-only", MAD, "memcmp(previous->attr_val, attr_val, attr_store_len(rc->app->ops, attr_type)) != 0;", "memcmp(previous->attr_val, attr_val, 8) != 0;", False),
    ("y12-publish-leaks-unselected", MAD, "        if (!(ports & (1u << work->port_id))) {\n            shlan_free(work);\n            continue;", "        if (!(ports & (1u << work->port_id))) {\n            continue;", True),
    ("y13-reserve-partial-leak", MAD, "            while (head) {\n                struct mrp_map_work *next = head->next;\n                shlan_free(head);\n                head = next;\n            }\n            priv_of(app)->map_error", "            priv_of(app)->map_error", True),
    ("y14-no-replay-after-publish", MAD, "        map_publish(app, port_id, ai->attr_type, ai->attr_val, join, reserved);\n        map_replay_all(app);", "        map_publish(app, port_id, ai->attr_type, ai->attr_val, join, reserved);", False),
]

def run(label, file, old, new, sanitize):
    w = WORK / label
    if w.exists():
        shutil.rmtree(w)
    src = w / "source"
    src.mkdir(parents=True)
    for n in ["CMakeLists.txt", "src", "tests"]:
        p = SRC / n
        (shutil.copytree if p.is_dir() else shutil.copy2)(p, src / n)
    path = src / file
    text = path.read_text()
    count = text.count(old)
    if count != 1:
        return {"label": label, "status": f"TARGET-COUNT-{count}"}
    path.write_text(text.replace(old, new))
    flags = "-fsanitize=address,undefined -fno-omit-frame-pointer -g" if sanitize else ""
    b = w / "build"
    env = dict(os.environ, LD_LIBRARY_PATH=str(PREFIX / "lib"))
    cfg = subprocess.run(["cmake", "-S", str(src), "-B", str(b), "-DCMAKE_BUILD_TYPE=Debug" if sanitize else "-DCMAKE_BUILD_TYPE=Release",
                          f"-DCMAKE_PREFIX_PATH={PREFIX}", f"-DLWSRP_MILAN={MILAN}", f"-DCMAKE_C_FLAGS={flags}",
                          f"-DCMAKE_EXE_LINKER_FLAGS={flags}", f"-DCMAKE_SHARED_LINKER_FLAGS={flags}"],
                         capture_output=True, text=True, env=env)
    bld = subprocess.run(["cmake", "--build", str(b), "--parallel", "2"], capture_output=True, text=True, env=env)
    if cfg.returncode or bld.returncode:
        (w / "build.log").write_text(cfg.stdout + cfg.stderr + bld.stdout + bld.stderr)
        return {"label": label, "status": "BUILD-FAIL"}
    env["ASAN_OPTIONS"] = "detect_leaks=1"
    t = subprocess.run([str(b / "unit_tests")], capture_output=True, text=True, env=env, timeout=300)
    out = t.stdout + t.stderr
    (w / "unit.log").write_text(out)
    failing = sorted({l.split("->")[2].strip() for l in out.splitlines() if "Failure:" in l and l.count("->") >= 2} |
                     {l.split("->")[2].strip() for l in out.splitlines() if "Exception:" in l and l.count("->") >= 2})
    san = "ERROR: AddressSanitizer" in out or "ERROR: LeakSanitizer" in out or "runtime error" in out
    status = "KILLED" if t.returncode != 0 else "SURVIVED"
    return {"label": label, "status": status, "rc": t.returncode, "failing": failing, "sanitizer": san,
            "tail": out.strip().splitlines()[-1] if out.strip() else ""}

with cf.ThreadPoolExecutor(JOBS) as ex:
    results = list(ex.map(lambda p: run(*p), PLANTS))
for r in results:
    print(json.dumps(r))
