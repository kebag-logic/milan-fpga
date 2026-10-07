# SPDX-License-Identifier: Apache-2.0
"""Reviewer probes: plant independent note 4/5 mutations in scratch exports of
the exact head, build each in both profiles concurrently, and record which
named tests fail. Usage: probe_mutations.py CHECKOUT CGREEN_PREFIX OUT"""
import concurrent.futures, json, os, subprocess, sys, tarfile, io, shutil
from pathlib import Path

src, prefix, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
MAD = "src/core/mrp_mad.c"
COND = ("(p2p && ev == MRP_EVENT_RJOININ &&\n         (ai->appl == MRP_APPL_STATE_VO || ai->appl == MRP_APPL_STATE_VP)) ||\n"
        "        (!p2p && ev == MRP_EVENT_RIN)")
PROBES = {
    "control-none": None,
    "drop-vo-from-note4": COND.replace("ai->appl == MRP_APPL_STATE_VO || ", ""),
    "note4-ignores-link-mode": COND.replace("(p2p && ev == MRP_EVENT_RJOININ", "(ev == MRP_EVENT_RJOININ"),
    "note5-ignores-link-mode": COND.replace("(!p2p && ev == MRP_EVENT_RIN)", "(ev == MRP_EVENT_RIN)"),
    "note4-inverted-link-mode": COND.replace("(p2p && ev == MRP_EVENT_RJOININ", "(!p2p && ev == MRP_EVENT_RJOININ"),
    # Carried suggestion: note 4 applied to every Applicant state (expected to survive).
    "note4-all-states": COND.replace("(ai->appl == MRP_APPL_STATE_VO || ai->appl == MRP_APPL_STATE_VP)", "true"),
}
NAMES = ["applicant_receive_conditions_follow_link_mode", "pending_applicant_joinin_obeys_note_four"]
archive = subprocess.run(["git", "-C", str(src), "archive", "HEAD"], check=True, capture_output=True).stdout
if out.exists():
    shutil.rmtree(out)
out.mkdir(parents=True)
env = dict(os.environ, LD_LIBRARY_PATH=str(prefix / "lib"))

def run(label, profile):
    work = out / f"{label}-{profile}"
    tarfile.open(fileobj=io.BytesIO(archive)).extractall(work / "src", filter="data")
    path = work / "src" / MAD
    text = path.read_text()
    assert COND in text, "probe target missing"
    if PROBES[label] is not None:
        path.write_text(text.replace(COND, PROBES[label]))
    log = []
    rc = 0
    for cmd in (["cmake", "-S", str(work / "src"), "-B", str(work / "b"), "-DCMAKE_BUILD_TYPE=Debug",
                 f"-DCMAKE_PREFIX_PATH={prefix}", f"-DLWSRP_MILAN={profile}"],
                ["cmake", "--build", str(work / "b"), "--parallel", "2"]):
        r = subprocess.run(cmd, capture_output=True, text=True, env=env)
        log.append(r.stdout + r.stderr)
        if r.returncode:
            return {"probe": label, "profile": profile, "build_rc": r.returncode}
    r = subprocess.run([str(work / "b" / "unit_tests")], capture_output=True, text=True, env=env, timeout=120)
    (work / "unit.log").write_text(r.stdout + r.stderr)
    return {"probe": label, "profile": profile, "build_rc": 0, "unit_rc": r.returncode,
            "summary": [l for l in r.stdout.splitlines() if l.startswith("Completed")],
            "failed_note_tests": [n for n in NAMES if n in r.stdout + r.stderr]}

with concurrent.futures.ThreadPoolExecutor(10) as pool:
    results = list(pool.map(lambda a: run(*a), [(l, p) for l in PROBES for p in ("OFF", "ON")]))
(out / "results.json").write_text(json.dumps(results, indent=2) + "\n")
for r in results:
    print(json.dumps(r))
