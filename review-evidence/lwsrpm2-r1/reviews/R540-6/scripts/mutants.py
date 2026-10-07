# SPDX-License-Identifier: Apache-2.0
"""Internal reviewer mutations of the round-7 snapshot mechanism.

Each mutant copies the exact-head sources into scratch, applies one textual
change, builds in the selected profile, and runs the unit runner, the
internal probe, and the external cross-port probe. A mutant is KILLED when
it compiles and at least one check fails. The checkout is never modified.
"""
import argparse, concurrent.futures, os, pathlib, shutil, subprocess, sys

PACKET = pathlib.Path(__file__).resolve().parents[1]
SCRATCH = PACKET / "scratch"
RECEIPTS = PACKET / "receipts" / "mutants"
SRC = pathlib.Path(os.environ["REVIEW_SOURCE"]).resolve()
EXTERNAL = SCRATCH / "ev/reviews/R541-5/scripts/probe.c"
F = "src/core/mrp_mad.c"
MUTANTS = [
    ("m1-snapshot-in-only", F, "            if (!ai->flush_pending) {\n                memcpy(ai->flush_value",
     "            if (!ai->flush_pending && previous == MRP_REG_STATE_IN) {\n                memcpy(ai->flush_value"),
    ("m2-no-snapshot-copy", F, "                memcpy(ai->flush_value, ai->attr_val, attr_store_len(app->ops, ai->attr_type));\n", ""),
    ("m3-reserve-applicant-value", F, "map_reserve(app, ai->attr_type, ind_value,", "map_reserve(app, ai->attr_type, ai->attr_val,"),
    ("m4-clear-only-on-timer", F, "    if (e->ind == REG_IND_LV) {\n        ai->flush_pending = false;",
     "    if (e->ind == REG_IND_LV && ev != MRP_EVENT_FLUSH) {\n        ai->flush_pending = false;"),
    ("m5-identity-only-snapshot", F, "memcpy(ai->flush_value, ai->attr_val, attr_store_len(app->ops, ai->attr_type));",
     "memcpy(ai->flush_value, ai->attr_val, 8);"),
    ("m6-timer-failure-resnapshots", F, "        if (ev == MRP_EVENT_LEAVETIMER) {\n            shlan_timer_arm(&ai->leave_timer, 1u);",
     "        if (ev == MRP_EVENT_LEAVETIMER) {\n            if (ai->flush_pending) { memcpy(ai->flush_value, ai->attr_val, attr_store_len(app->ops, ai->attr_type)); }\n            shlan_timer_arm(&ai->leave_timer, 1u);"),
    ("m7-receive-retry-resnapshots", F, "    if (previous && previous->flush_pending) {\n",
     "    if (previous && previous->flush_pending) {\n        memcpy(previous->flush_value, previous->attr_val, attr_store_len(rc->app->ops, attr_type));\n"),
    ("m8-local-join-resnapshots", F, "        memcpy(a->attr_val, val, attr_store_len(ops, type));\n        return a;",
     "        memcpy(a->attr_val, val, attr_store_len(ops, type));\n        if (a->flush_pending) { memcpy(a->flush_value, val, attr_store_len(ops, type)); }\n        return a;"),
    ("m9-policy-applicant-value", F, "map_publish(app, port_id, ai->attr_type, ind_value, join, reserved);",
     "map_publish(app, port_id, ai->attr_type, ai->attr_val, join, reserved);"),
]
# Prior-round suggestion plants, rerun at this head.
PRIOR = [
    ("p1-replacement-skips-pending", F, "            if (old != ai && old->reg != MRP_REG_STATE_MT &&",
     "            if (old != ai && old->reg != MRP_REG_STATE_MT && !old->flush_pending &&"),
    ("p2-flush-leaveall-request", F, "        la_event(app, ps, MRP_EVENT_LEAVEALLTIMER, port_id); /* §10.7.5.22 */\n", "        (void)0;\n"),
]


def run(log, args, cwd, env=None, timeout=300):
    r = subprocess.run(list(map(str, args)), cwd=cwd, env=env, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    log.write(f"$ {' '.join(map(str, args))}\nrc={r.returncode}\n{r.stdout[-6000:]}\n")
    return r.returncode, r.stdout


def mutant(name, path, old, new, mode):
    work = SCRATCH / "mutants" / f"{name}-{mode}"
    if work.exists():
        shutil.rmtree(work)
    src = work / "source"
    src.mkdir(parents=True)
    for item in ["CMakeLists.txt", "src", "tests"]:
        p = SRC / item
        (shutil.copytree if p.is_dir() else shutil.copy2)(p, src / item)
    target = src / path
    text = target.read_text()
    if text.count(old) != 1:
        return name, mode, "TARGET-MISSING", ""
    target.write_text(text.replace(old, new))
    prefix = SCRATCH / "prefix"
    env = os.environ | {"LD_LIBRARY_PATH": str(prefix / "lib")}
    build = work / "build"
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    with open(RECEIPTS / f"{name}-{mode}.log", "w") as log:
        if run(log, ["cmake", "-S", src, "-B", build, "-DCMAKE_BUILD_TYPE=Debug",
                     f"-DCMAKE_PREFIX_PATH={prefix}", f"-DLWSRP_MILAN={mode}"], src, env)[0]:
            return name, mode, "CONFIGURE-FAIL", ""
        if run(log, ["cmake", "--build", build, "--parallel", "2"], src, env)[0]:
            return name, mode, "BUILD-FAIL", ""
        killers = []
        rc, out = run(log, [build / "unit_tests"], src, env)
        if rc:
            failed = sorted({l.split(" -> ")[2] for l in out.splitlines() if l.count(" -> ") >= 3 and "Failure" in l})
            killers.append("units:" + ",".join(failed[:6]))
        common = ["cc", "-std=c11", f"-I{src}/src/include", f"-I{src}/src", f"-I{src}/tests/unit"]
        link = [src / "tests/unit/fault_alloc.c", f"-L{build}", f"-Wl,-rpath,{build}", "-lshlan"]
        own, ext = work / "own-probe", work / "ext-probe"
        if run(log, common + [PACKET / "scripts/r540_6_probe.c"] + link + ["-o", own], src, env)[0] == 0:
            rc, out = run(log, [own], src, env)
            if rc:
                killers.append("internal-probe")
        if run(log, common + [EXTERNAL] + link + ["-o", ext], src, env)[0] == 0:
            rc, out = run(log, [ext, "cross-port"], src, env)
            if rc:
                killers.append("external-cross-port")
            rc, out = run(log, [ext], src, env)
            if rc:
                killers.append("external-broad")
    return name, mode, "KILLED" if killers else "SURVIVED", " ".join(killers)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--set", choices=["round7", "prior"], default="round7")
    args = ap.parse_args()
    chosen = MUTANTS if args.set == "round7" else PRIOR
    jobs = [(m, mode) for m in chosen for mode in ["OFF", "ON"]]
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(args.jobs, 8)) as pool:
        results = list(pool.map(lambda j: mutant(*j[0], j[1]), jobs))
    for name, mode, status, why in sorted(results):
        print(f"{status} {name} {mode} {why}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
