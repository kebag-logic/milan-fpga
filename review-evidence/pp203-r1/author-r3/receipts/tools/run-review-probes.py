#!/usr/bin/env python3
"""run-review-probes.py TREE OUT VERILATOR: the reviewers' probes, unchanged, on copies of TREE.
R731: probes/window-after-notification-round.patch (patch -p1), section RBT's probe run only.
R732: post-departure-probe.patch (git apply), and the non-advertising probe made exactly as
run-probes.py makes it (the same method text, the same two string insertions). Each run's log
and rc go to OUT."""
import pathlib, re, shutil, subprocess, sys
TREE, OUT, VL = (pathlib.Path(a).resolve() for a in sys.argv[1:4])
MG = pathlib.Path("<mgmt>")
R731 = MG / "pp203-r731-1"
R732 = MG / "pp203-r732-2"
OUT.mkdir(parents=True, exist_ok=True)
SCR = OUT / "scratch"

def fresh(name):
    d = SCR / name
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(TREE, d, ignore=shutil.ignore_patterns("obj_dir", ".git"))
    return d

def run(name, args, cwd):
    with (OUT / f"{name}.log").open("w") as f:
        r = subprocess.run(args, cwd=cwd, stdout=f, stderr=subprocess.STDOUT)
    (OUT / f"{name}.rc").write_text(f"{r.returncode}\n")
    print(name, r.returncode, flush=True)
    return r.returncode

# R731 window probe
d = fresh("r731-window")
assert run("r731-window-apply", ["patch", "-p1", "-i", str(R731 / "probes/window-after-notification-round.patch")], d) == 0
run("r731-window", ["make", "reboot", f"VERILATOR={VL}"], d / "tb/pp_top")
# R732 post-departure probe
d = fresh("r732-post-departure")
assert run("r732-post-departure-apply", ["git", "apply", str(R732 / "post-departure-probe.patch")], d) == 0
run("r732-post-departure", ["make", "reboot", f"VERILATOR={VL}"], d / "tb/pp_top")
# R732 non-advertising probe, made as run-probes.py makes it
src = (R732 / "run-probes.py").read_text()
method = re.search(r"method = '''(.*?)'''", src, re.S).group(1).replace("\\\\n", "\\n")
d = fresh("r732-nonadvertising")
f = d / "tb/pp_top/sim_main.cpp"
original = f.read_text()
anchor = "  // ---- RBT9: nothing on tx_* from the final DEPARTING to a delayed reset -----"
assert original.count(anchor) == 1
changed = original.replace(anchor, method + "\n" + anchor)
assert changed.count("    every_slot_taken_at_the_shutdown();") == 1
changed = changed.replace("    every_slot_taken_at_the_shutdown();",
                          "    every_slot_taken_at_the_shutdown();\n    nonadvertising_pending_frame_probe();", 1)
f.write_text(changed)
run("r732-nonadvertising", ["make", "reboot", f"VERILATOR={VL}"], d / "tb/pp_top")
shutil.rmtree(SCR)
