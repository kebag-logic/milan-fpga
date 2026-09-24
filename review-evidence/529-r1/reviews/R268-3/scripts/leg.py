#!/usr/bin/env python3
"""Build and/or run one tb/verilator/milan_dp leg from its own `make -n run`
recipe line, in a given tree, with a bounded Verilator job count.

usage: leg.py TREE LEG {build|run|both} [--jobs N] [--verilator PATH]
              [--tag TAG] [--out DIR] [-- EXTRA RUN ARGS...]

LEG is the obj_* suffix: nxn, nxndv, nxn8, nxn4c, notify.
The build writes obj_<LEG>/ in TREE; the run writes <out>/<tag>-<LEG>.log
with a header naming the tree head, datapath and harness sha256.
"""
import argparse, hashlib, os, re, subprocess, sys, time

ap = argparse.ArgumentParser()
ap.add_argument("tree"); ap.add_argument("leg")
ap.add_argument("what", choices=["build", "run", "both"])
ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--verilator",
                default="$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator")
ap.add_argument("--tag", default="head")
ap.add_argument("--out", default=".")
ap.add_argument("rest", nargs="*")
a = ap.parse_args()

bench = os.path.join(a.tree, "tb/verilator/milan_dp")
env = dict(os.environ)

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def recipe():
    out = subprocess.run(["make", "-n", "run", "VERILATOR=" + a.verilator,
                          "VERILATOR_JOBS=%d" % a.jobs], cwd=bench, env=env,
                         capture_output=True, text=True, check=True).stdout
    joined = re.sub(r"\\\n", " ", out).splitlines()
    pat = re.compile(r"--Mdir obj_%s(\s|$)" % re.escape(a.leg))
    hits = [l for l in joined if pat.search(l)]
    if len(hits) != 1:
        sys.exit("expected one recipe line for obj_%s, found %d" % (a.leg, len(hits)))
    return hits[0]

binary = {"nxn": "Vmilan_dp_nxn", "nxndv": "Vmilan_dp_nxndv", "nxn8": "Vmilan_dp_nxn8",
          "nxn4c": "Vmilan_dp_nxn4c", "notify": "Vmilan_dp_notify"}[a.leg]

if a.what in ("build", "both"):
    for pre in ("ltn_rom.hex", "ucode.hex", "gptp_ucode.hex"):
        if not os.path.exists(os.path.join(bench, pre)):
            subprocess.run(["make", pre], cwd=bench, check=True)
    if a.leg == "nxndv" and not os.path.isdir(os.path.join(bench, "gen_divergent")):
        subprocess.run(["python3", "gen_divergent_shape.py"], cwd=bench, check=True)
    subprocess.run(["rm", "-rf", "obj_" + a.leg], cwd=bench, check=True)
    line = recipe()
    t = time.time()
    r = subprocess.run(line, shell=True, cwd=bench, env=env,
                       capture_output=True, text=True)
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "%s-%s.build.log" % (a.tag, a.leg)), "w") as f:
        f.write("recipe: %s\nexit %d  %.0f s\n" % (line[:400], r.returncode, time.time() - t))
        f.write(r.stdout[-4000:]); f.write(r.stderr[-8000:])
    if r.returncode:
        sys.exit("build failed: obj_%s (see %s-%s.build.log)" % (a.leg, a.tag, a.leg))

if a.what in ("run", "both"):
    exe = os.path.join(bench, "obj_" + a.leg, binary)
    t = time.time()
    r = subprocess.run([exe] + a.rest, cwd=bench, env=env, capture_output=True, text=True)
    txt = r.stdout + r.stderr
    fails = [l for l in txt.splitlines() if "[FAIL]" in l]
    tally = [l for l in txt.splitlines() if l.startswith("checks:") or l.startswith("RESULT:")]
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=a.tree, capture_output=True,
                          text=True).stdout.strip()
    os.makedirs(a.out, exist_ok=True)
    p = os.path.join(a.out, "%s-%s.log" % (a.tag, a.leg))
    with open(p, "w") as f:
        f.write("tree-head %s\nleg obj_%s args %s\n" % (head, a.leg, " ".join(a.rest)))
        f.write("datapath-sha256 %s\n" % sha(os.path.join(a.tree, "hdl/milan/milan_datapath.sv")))
        f.write("harness-sha256 %s\n" % sha(os.path.join(bench, "sim_nxn.cpp")))
        f.write("exit %d  wall %.0f s\n" % (r.returncode, time.time() - t))
        f.write("fail-lines %d\n" % len(fails))
        for l in fails: f.write("  " + l + "\n")
        f.write("tally-lines:\n")
        for l in tally[-3:]: f.write("  " + l + "\n")
        f.write("---- full output ----\n"); f.write(txt)
    print("%s obj_%s exit=%d fails=%d %s" % (a.tag, a.leg, r.returncode, len(fails),
                                             " | ".join(t.strip() for t in tally[-2:])))
