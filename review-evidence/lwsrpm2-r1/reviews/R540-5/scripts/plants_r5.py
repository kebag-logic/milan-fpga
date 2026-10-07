# SPDX-License-Identifier: Apache-2.0
"""Reviewer plants: copy the checkout, apply one mutation, build both profiles,
run the unit runner and the reviewer probe, and record which named tests fail."""
import argparse, json, re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

MAD = "src/core/mrp_mad.c"
FLUSH_ARM = ("            ai->flush_pending = true;\n            ai->reg = MRP_REG_STATE_LV;\n"
             "            shlan_timer_arm(&ai->leave_timer, 1u);\n")
PLANTS = {
    # Reviewer-owned mutations.
    "timer-path-two-tick": (MAD, "        if (ev == MRP_EVENT_LEAVETIMER) {\n            shlan_timer_arm(&ai->leave_timer, 1u);",
                            "        if (ev == MRP_EVENT_LEAVETIMER) {\n            shlan_timer_arm(&ai->leave_timer, 2u);"),
    "flush-no-timer": (MAD, FLUSH_ARM, "            ai->flush_pending = true;\n            ai->reg = MRP_REG_STATE_LV;\n"),
    "refresh-before-flush": (MAD, "        /* Withdraw the saved value before any receive can refresh it. */\n",
                             "        memcpy(previous->attr_val, attr_val, attr_store_len(rc->app->ops, attr_type));\n"),
    "continue-after-retry-failure": (MAD, "            rc->error = r;\n            return;\n        }\n    }\n    bool changed_in",
                                     "            rc->error = r;\n        }\n    }\n    bool changed_in"),
    "pending-only-from-in": (MAD, "            ai->flush_pending = true;", "            ai->flush_pending = previous == MRP_REG_STATE_IN;"),
    "clear-only-on-flush-event": (MAD, "    if (e->ind == REG_IND_LV) {\n        ai->flush_pending = false;",
                                  "    if (e->ind == REG_IND_LV && ev == MRP_EVENT_FLUSH) {\n        ai->flush_pending = false;"),
    "replacement-skips-pending": (MAD, "if (old != ai && old->reg != MRP_REG_STATE_MT &&",
                                  "if (old != ai && old->reg != MRP_REG_STATE_MT && !old->flush_pending &&"),
    "flush-every-lv-recovery": (MAD, "if (previous && previous->flush_pending) {",
                                "if (previous && (previous->flush_pending || previous->reg == MRP_REG_STATE_LV)) {"),
    "retry-only-declarations": (MAD, "if (previous && previous->flush_pending) {",
                                "if (previous && previous->flush_pending && (attr_event == MRP_ATTR_EVENT_NEW || "
                                "attr_event == MRP_ATTR_EVENT_JOININ || attr_event == MRP_ATTR_EVENT_JOINMT)) {"),
    "flush-leaveall-request": (MAD, "        la_event(app, ps, MRP_EVENT_LEAVEALLTIMER, port_id); /* \u00a710.7.5.22 */\n", "        (void)0; /* Plant: no LeaveAll request. */\n"),
    # Sample of the author's named reversals, re-run by this driver.
    "S-pending-flush": (MAD, "            ai->flush_pending = true;", "            ai->flush_pending = false;"),
    "S-flush-before-refresh": (MAD, "if (previous && previous->flush_pending) {", "if (false && previous && previous->flush_pending) {"),
    "S-flush-deadline": (MAD, "ai->reg = MRP_REG_STATE_LV;\n            shlan_timer_arm(&ai->leave_timer, 1u);",
                         "ai->reg = MRP_REG_STATE_LV;\n            shlan_timer_arm(&ai->leave_timer, 2u);"),
    "S-flush-observer": (MAD, "        observe(app, ai, ev, port_id, appl_from, reg_from);\n        return r;", "        return r;"),
    "S-replacement-lv": (MAD, "if (old != ai && old->reg != MRP_REG_STATE_MT &&", "if (old != ai && old->reg == MRP_REG_STATE_IN &&"),
    "S-receive-instance-stop": (MAD, "if (rc->error || priv->map_error) {", "if (priv->map_error) {"),
    "S-flush-completion": (MAD, "        ai->flush_pending = false;", "        /* Plant: retain completed withdrawal. */"),
    "S-replacement-leave-timer": (MAD, "                if (r >= 0) {\n                    r = deliver_event_changed(rc->app, rc->ps, old,\n"
                                  "                                              MRP_EVENT_LEAVETIMER, rc->port_id, false);\n                }\n", ""),
}


def run(cmd, cwd, env=None, log=None):
    r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=600)
    if log:
        Path(log).write_text(" ".join(map(str, cmd)) + "\n" + r.stdout + r.stderr)
    return r.returncode, r.stdout + r.stderr


def one(name, src, work, prefix, probe):
    path, old, new = PLANTS[name]
    d = work / name
    if d.exists():
        shutil.rmtree(d)
    (d / "src").mkdir(parents=True)
    tree = d / "src"
    for n in ["CMakeLists.txt", "src", "tests"]:
        p = src / n
        (shutil.copytree if p.is_dir() else shutil.copy2)(p, tree / n)
    f = tree / path
    text = f.read_text()
    count = text.count(old)
    rec = {"plant": name, "file": path, "target_count": count}
    if count != 1:
        rec["result"] = "TARGET-NOT-UNIQUE"
        return rec
    f.write_text(text.replace(old, new))
    env = dict(**__import__("os").environ, LD_LIBRARY_PATH=str(prefix / "lib"))
    for prof, m in (("OFF", "0"), ("ON", "1")):
        b = d / ("build-" + prof)
        rc, _ = run(["cmake", "-S", str(tree), "-B", str(b), "-DCMAKE_BUILD_TYPE=Debug",
                     f"-DCMAKE_PREFIX_PATH={prefix}", f"-DLWSRP_MILAN={prof}"], d, env, d / f"configure-{prof}.log")
        rc_b, _ = run(["cmake", "--build", str(b), "--parallel", "2"], d, env, d / f"build-{prof}.log")
        rec[f"build_{prof}"] = rc_b
        if rc or rc_b:
            continue
        rc_u, out = run([str(b / "unit_tests")], d, env, d / f"unit-{prof}.log")
        failed = sorted(set(re.findall(r"Failure: \w+ -> (\w+)", out)))
        rec[f"unit_{prof}"] = {"rc": rc_u, "failing_tests": failed, "failure_lines": out.count("Failure:")}
        rc_p, out = run(["sh", str(probe), str(tree), str(d / "probe"), m], d, env, d / f"probe-{prof}.log")
        rec[f"probe_{prof}"] = {"rc": rc_p, "summary": (out.strip().splitlines() or [""])[-1]}
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, required=True)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--prefix", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    a.src, a.work, a.prefix = a.src.resolve(), a.work.resolve(), a.prefix.resolve()
    probe = Path(__file__).resolve().parent / "run_probe.sh"
    with ThreadPoolExecutor(a.jobs) as ex:
        names = [n for n in PLANTS if not a.only or n in a.only.split(",")]
        recs = list(ex.map(lambda n: one(n, a.src, a.work, a.prefix, probe), names))
    a.out.write_text(json.dumps(recs, indent=1) + "\n")
    for r in recs:
        u = [r.get(f"unit_{p}", {}) for p in ("OFF", "ON")]
        pr = [r.get(f"probe_{p}", {}) for p in ("OFF", "ON")]
        print(r["plant"], r.get("result", ""), "build", r.get("build_OFF"), r.get("build_ON"),
              "| unit rc", [x.get("rc") for x in u], "| probe rc", [x.get("rc") for x in pr])
        for p, x in zip(("OFF", "ON"), u):
            print("   ", p, "failing:", x.get("failing_tests"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
