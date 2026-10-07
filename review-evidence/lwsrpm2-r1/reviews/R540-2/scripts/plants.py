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
    ("x01-no-commit-replay", MAD, "    map_replay(app, port_id);\n    ps->join_wait = ps->join_cs;", "    ps->join_wait = ps->join_cs;", False),
    ("x02-no-poll-replay", MAD, "    map_replay(app, port_id);\n    if (!ps->prepared_pdu &&", "    if (!ps->prepared_pdu &&", False),
    ("x03-no-registrar-rollback", MAD, "        ai->reg = previous;\n", "", False),
    ("x04-no-leavetimer-retry", MAD, "            shlan_timer_arm(&ai->leave_timer, 1u);\n", "", False),
    ("x05-drop-map-error", MAD, "ctx.error ? ctx.error : priv->map_error;", "ctx.error;", False),
    ("x06-partial-publish", MAD, "            priv_of(app)->map_error = -SHLAN_ERROR_NO_MEMORY;\n            return -SHLAN_ERROR_NO_MEMORY;",
     "            priv_of(app)->map_error = -SHLAN_ERROR_NO_MEMORY;\n            return 0;", False),
    ("x07-zero-attr-length-accepted", PDU, "|| !alen ||", "||", False),
    ("x08-vid-off-by-one", MVRP, "offset > MVRP_VID_MAX - vid", "offset > MVRP_VID_MAX + 1 - vid", False),
    ("x09-rjoinmt-lv-join-only", MAD, "    /* MRP_EVENT_RJOINMT — same entry as RJOININ for Registrar */\n    {\n        _RE(REG_IND_NONE, REG_TIMER_NONE, MRP_REG_STATE_IN),\n        _RE(REG_IND_NONE, REG_TIMER_STOP, MRP_REG_STATE_IN),",
     "    /* MRP_EVENT_RJOINMT — same entry as RJOININ for Registrar */\n    {\n        _RE(REG_IND_NONE, REG_TIMER_NONE, MRP_REG_STATE_IN),\n        _RE(REG_IND_JOIN, REG_TIMER_STOP, MRP_REG_STATE_IN),", False),
    ("x10-lv-no-timer-stop", MAD, "_RE(REG_IND_NONE, REG_TIMER_STOP, MRP_REG_STATE_IN),  /* LV: Stop; IN         */",
     "_RE(REG_IND_NONE, REG_TIMER_NONE, MRP_REG_STATE_IN),  /* LV: Stop; IN         */", False),
    ("x11-dangling-tail", MAD, "        shlan_free(work);\n    }\n    ps->map_tail = NULL;", "        shlan_free(work);\n    }", True),
    ("x12-destroy-leaks-queue", MAD, "        struct mrp_map_work *work = priv->ports[p].map_head;\n        while (work) {",
     "        struct mrp_map_work *work = NULL;\n        while (work) {", True),
    ("x13-map-value-not-copied", MAD, "memcpy(work->value, value, attr_store_len(app->ops, type));", "(void)value;", False),
    ("x14-later-known-type-skip", PDU, "if (unknown || (later && unknown_event))", "if (unknown || later)", False),
    ("x15-domain-vid-ignored", MSRP, "d->vid = be16_get(buf + 2);", "d->vid = 0;", False),
    ("x16-changed-in-map-dropped", MAD, "        (void)map_apply_join(rc->app, rc->port_id, attr_type, ai->attr_val);\n", "", False),
    ("x17-replay-ignores-retention", MAD, "    if (ps->prepared_pdu || ps->in_send) {\n        return;\n    }\n    while (ps->map_head)", "    while (ps->map_head)", False),
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
