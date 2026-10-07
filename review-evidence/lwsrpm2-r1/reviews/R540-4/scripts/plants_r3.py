#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Reviewer plant campaign for lwSRP PR #12 round 5 (R540-4).

Each plant edits one copy of the reviewed sources in scratch, builds the unit
runner in the selected profile, records the failing named tests, and also runs
the reviewer probe against the planted sources. The checkout is never edited.

Usage: plants_r3.py --checkout DIR --cgreen PREFIX --probe probe_r3.c --work DIR
                    --out JSON [--jobs N] [--only ID,...] [--patch FILE]
"""
import argparse
import concurrent.futures as cf
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

MAD = "src/core/mrp_mad.c"
TESTS = "tests/unit/review_test.c"

FLUSH = ("        if (ev == MRP_EVENT_FLUSH) {\n"
         "            /* The topology API cannot report refusal. Retain its withdrawal. */\n"
         "            ai->reg = MRP_REG_STATE_LV;\n"
         "            shlan_timer_arm(&ai->leave_timer, 1u);\n"
         "        }\n")

# (id, file, old, new, intent)
PLANTS = [
    ("p01-flush-timer-leave-time", MAD, "            shlan_timer_arm(&ai->leave_timer, 1u);\n        }\n        if (ev == MRP_EVENT_LEAVETIMER)",
     "            shlan_timer_arm(&ai->leave_timer, priv_of(app)->ports[port_id].leave_cs);\n        }\n        if (ev == MRP_EVENT_LEAVETIMER)",
     "Flush retry delayed to the full Leave time"),
    ("p02-flush-keeps-in", MAD, "            ai->reg = MRP_REG_STATE_LV;\n            shlan_timer_arm(&ai->leave_timer, 1u);\n        }\n        if (ev == MRP_EVENT_LEAVETIMER)",
     "            shlan_timer_arm(&ai->leave_timer, 1u);\n        }\n        if (ev == MRP_EVENT_LEAVETIMER)",
     "Flush failure keeps IN; leavetimer! in IN is ignored"),
    ("p03-flush-no-timer", MAD, "            ai->reg = MRP_REG_STATE_LV;\n            shlan_timer_arm(&ai->leave_timer, 1u);\n        }\n        if (ev == MRP_EVENT_LEAVETIMER)",
     "            ai->reg = MRP_REG_STATE_LV;\n        }\n        if (ev == MRP_EVENT_LEAVETIMER)",
     "Flush failure enters LV without arming the retry"),
    ("p04-flush-silent-mt", MAD, "            ai->reg = MRP_REG_STATE_LV;\n            shlan_timer_arm(&ai->leave_timer, 1u);\n        }\n        if (ev == MRP_EVENT_LEAVETIMER)",
     "            ai->reg = MRP_REG_STATE_MT;\n        }\n        if (ev == MRP_EVENT_LEAVETIMER)",
     "Flush failure drops the registration without indication"),
    ("p05-flush-only-from-lv", MAD, "        if (ev == MRP_EVENT_FLUSH) {\n",
     "        if (ev == MRP_EVENT_FLUSH && previous == MRP_REG_STATE_LV) {\n",
     "Flush retention only when the source was already LV"),
    ("p06-replace-skip-leave-timer", MAD,
     "                if (r >= 0) {\n                    r = deliver_event_changed(rc->app, rc->ps, old,\n                                              MRP_EVENT_LEAVETIMER, rc->port_id, false);\n                }\n",
     "", "Replacement delivers rLv! only"),
    ("p07-replace-unguarded-timer", MAD, "                if (r >= 0) {\n                    r = deliver_event_changed(rc->app, rc->ps, old,\n                                              MRP_EVENT_LEAVETIMER",
     "                if (true) {\n                    r = deliver_event_changed(rc->app, rc->ps, old,\n                                              MRP_EVENT_LEAVETIMER",
     "Replacement overwrites an rLv! failure with the leavetimer! result"),
    ("p08-replace-continue", MAD, "                    rc->error = r;\n                    return;\n                }\n            }\n        }\n    }",
     "                    rc->error = r;\n                }\n            }\n        }\n    }",
     "Replacement failure continues to the new Join"),
    ("p09-replace-in-only", MAD, "if (old != ai && old->reg != MRP_REG_STATE_MT &&",
     "if (old != ai && old->reg == MRP_REG_STATE_IN &&",
     "Replacement ignores old registrations in LV"),
    ("p10-replace-no-value-restore", MAD,
     "                if (r < 0) {\n                    if (previous) {\n                        memcpy(ai->attr_val, previous_value, sizeof(previous_value));\n                    }\n                    rc->error = r;",
     "                if (r < 0) {\n                    rc->error = r;",
     "Replacement failure keeps the refreshed value of an existing new-type instance"),
    ("p11-replace-no-error", MAD, "                    rc->error = r;\n                    return;\n                }\n            }\n        }\n    }",
     "                    return;\n                }\n            }\n        }\n    }",
     "Replacement failure records no receive error (map_error remains)"),
    ("p12-leavetimer-retry-2cs", MAD, "        if (ev == MRP_EVENT_LEAVETIMER) {\n            shlan_timer_arm(&ai->leave_timer, 1u);",
     "        if (ev == MRP_EVENT_LEAVETIMER) {\n            shlan_timer_arm(&ai->leave_timer, 2u);",
     "Timer withdrawal retry delayed by one tick"),
    ("p13-flush-no-leaveall", MAD, "        la_event(app, ps, MRP_EVENT_LEAVEALLTIMER, port_id); /* §10.7.5.22 */",
     "        (void)0;", "Flush no longer requests LeaveAll"),
    ("p14-receive-stop-final-event", MAD, "    int r = deliver_event_changed(rc->app, rc->ps, ai, ev, rc->port_id, changed_in);\n    if (r < 0 && previous) {",
     "    int r = deliver_event_changed(rc->app, rc->ps, ai, ev, rc->port_id, changed_in);\n    priv->map_error = 0;\n    if (r < 0 && previous) {",
     "Final event failure is neither stopped nor reported"),
    ("p15-flush-arm-zero", MAD, "            ai->reg = MRP_REG_STATE_LV;\n            shlan_timer_arm(&ai->leave_timer, 1u);",
     "            ai->reg = MRP_REG_STATE_LV;\n            shlan_timer_arm(&ai->leave_timer, 0u);",
     "Flush retry armed with zero centiseconds"),
    ("y01-stop-guard-removed", MAD, "    if (rc->error || priv->map_error) {\n        return;\n    }\n    if (priv->filter",
     "    if (priv->filter", "Receive continues after any earlier failure"),
    ("y01b-stop-map-error-only", MAD, "if (rc->error || priv->map_error) {", "if (priv->map_error) {",
     "Receive continues after a source-instance allocation failure"),
    ("y02-publish-ignores-mask", MAD, "        if (!(ports & (1u << work->port_id))) {",
     "        if (false && !(ports & (1u << work->port_id))) {", "Publication ignores the policy mask"),
    ("y02b-publish-adds-source", MAD, "    while (head) {\n        struct mrp_map_work *work = head;\n        head = head->next;\n        if (!(ports",
     "    ports |= 1u << src_port;\n    while (head) {\n        struct mrp_map_work *work = head;\n        head = head->next;\n        if (!(ports",
     "Publication also targets the source port"),
    ("y07-no-policy-reserves", MAD, "    if (join ? !app->ops->map_join : !app->ops->map_leave) {\n        return 0;\n    }\n", "",
     "Applications without policy still reserve"),
    ("y07b-no-leave-policy-reserves", MAD, "    if (join ? !app->ops->map_join : !app->ops->map_leave) {",
     "    if (join && !app->ops->map_join) {", "Withdrawal without leave policy still reserves"),

]


def sh(cmd, cwd, env, log, timeout=300):
    r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
    with open(log, "a") as f:
        f.write("$ " + " ".join(map(str, cmd)) + f"\n{r.stdout}{r.stderr}\nrc={r.returncode}\n")
    return r.returncode, r.stdout + r.stderr


def run_one(args, pid, path, old, new, intent, profile, patch=None):
    work = Path(args.work) / profile / pid
    if work.exists():
        shutil.rmtree(work)
    src = work / "source"
    src.mkdir(parents=True)
    root = Path(args.checkout)
    for name in ["CMakeLists.txt", "src", "tests"]:
        p = root / name
        if p.is_dir():
            shutil.copytree(p, src / name, ignore=shutil.ignore_patterns("__pycache__"))
        else:
            shutil.copy2(p, src / name)
    log = work / "run.log"
    rec = {"id": pid, "profile": profile, "intent": intent}
    if patch is None:
        target = src / path
        text = target.read_text()
        n = text.count(old)
        rec["matches"] = n
        if n != 1:
            rec["status"] = "TARGET-COUNT-%d" % n
            return rec
        target.write_text(text.replace(old, new))
    else:
        rc, out = sh(["patch", "-p1", "-i", str(Path(patch).resolve())], src, os.environ.copy(), log)
        if rc:
            rec["status"] = "PATCH-FAILED"
            return rec
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = str(Path(args.cgreen) / "lib")
    milan = "ON" if profile == "milan" else "OFF"
    b = work / "build"
    rc, _ = sh(["cmake", "-S", str(src), "-B", str(b), "-DCMAKE_BUILD_TYPE=Debug",
                f"-DCMAKE_PREFIX_PATH={args.cgreen}", f"-DLWSRP_MILAN={milan}"], src, env, log)
    if rc == 0:
        rc, _ = sh(["cmake", "--build", str(b), "--parallel", "2"], src, env, log)
    if rc:
        rec["status"] = "BUILD-FAILED"
        return rec
    rc, out = sh([str(b / "unit_tests")], src, env, log)
    rec["suite_rc"] = rc
    rec["failing_tests"] = sorted(set(re.findall(r"Failure: \S+ -> (\S+)", out)))
    m = re.search(r'Completed "main": (\d+) pass', out)
    rec["suite_summary"] = out.strip().splitlines()[-1] if out.strip() else ""
    probe = work / "probe"
    rc, out = sh(["cc", "-std=c11", "-g", "-O1", f"-DLWSRP_MILAN={1 if milan == 'ON' else 0}",
                  "-fsanitize=address,undefined", f"-I{src}/src/include", f"-I{src}/src", args.probe,
                  f"{src}/src/ports/timer.c", f"{src}/src/core/mrp_mad.c", f"{src}/src/core/mrp_pdu.c",
                  f"{src}/src/modules/msrp.c", "-o", str(probe)], src, env, log)
    if rc:
        rec["probe"] = "PROBE-BUILD-FAILED"
    else:
        rc, out = sh([str(probe)], src, env, log, timeout=600)
        rec["probe_rc"] = rc
        m = re.search(r"checks (\d+) failures (\d+)", out)
        rec["probe_checks"] = m.group(0) if m else "no summary"
        g = re.search(r"cases with observer gaps (\d+)", out)
        rec["probe_observer_gap_cases"] = int(g.group(1)) if g else None
        rec["probe_first_failures"] = [l for l in out.splitlines() if l.startswith("FAIL")][:3]
    rec["status"] = "KILLED" if rec["suite_rc"] != 0 else "SURVIVED"
    return rec


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--checkout", required=True)
    ap.add_argument("--cgreen", required=True)
    ap.add_argument("--probe", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--only", default="")
    ap.add_argument("--patch", default=None, help="apply one patch instead of the plant list")
    args = ap.parse_args()
    args.probe = str(Path(args.probe).resolve())
    jobs = []
    if args.patch:
        for prof in ("default", "milan"):
            jobs.append(("patch-" + Path(args.patch).stem, None, None, None, "patch", prof, args.patch))
    else:
        only = set(filter(None, args.only.split(",")))
        for pid, path, old, new, intent in PLANTS:
            if only and pid not in only:
                continue
            for prof in ("default", "milan"):
                jobs.append((pid, path, old, new, intent, prof, None))
    results = []
    with cf.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        futs = [ex.submit(run_one, args, *j) for j in jobs]
        for f in cf.as_completed(futs):
            r = f.result()
            results.append(r)
            print(f"{r['id']:34s} {r['profile']:8s} {r['status']:10s} tests={r.get('failing_tests')} "
                  f"probe={r.get('probe_checks')} gaps={r.get('probe_observer_gap_cases')}", flush=True)
    results.sort(key=lambda r: (r["id"], r["profile"]))
    Path(args.out).write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
