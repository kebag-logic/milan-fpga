import pathlib,subprocess,sys
root=pathlib.Path("/tmp/502-a345")
tb=root/"export/tb/verilator/pp_shadow"
probe=tb/"r328_probe_main.cpp"
probe.write_bytes(subprocess.check_output(["git","show","104c8a54:tb/verilator/pp_shadow/sim_main.cpp"]))
subprocess.run(["patch","--batch",str(probe),str(root/"probe_main.patch")],check=True)
# Preserve the published patch's literal redacted include unchanged.
compat=tb/"$REVIEWS/r328-1-502/tb/common/verilator_harness.hpp"
compat.parent.mkdir(parents=True,exist_ok=True)
compat.write_bytes((root/"export/tb/common/verilator_harness.hpp").read_bytes())
for leg,command in (
    ("static",["make","run-base","SIM_ARGS=--pending-only",f"BUILD_DIR={root}/r328-oracle/static"]),
    ("dynamic",["make","run-pending",f"PENDING_BUILD_DIR={root}/r328-oracle/dynamic"]),
):
    (root/"r328-oracle").mkdir(exist_ok=True)
    result=subprocess.run([sys.executable,str(root/"gate.py"),"r328-oracle-"+leg,*command,"CPP=r328_probe_main.cpp"],cwd=tb)
    if result.returncode: sys.exit(result.returncode)
