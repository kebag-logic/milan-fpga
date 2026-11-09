#!/usr/bin/env python3
"""Reviewer fault probes for issue #217 at an exact head.

probe.py REPO HEAD WORK NAME
Exports HEAD from REPO into WORK/NAME (git archive), applies the named
probe's edits (exact-string replacements, each required to match exactly
once) or restores base files, runs the probe's make targets with the pinned
simulator first on PATH, and prints one verdict line per target plus the
FAIL lines. Never touches REPO's working tree.
"""
import os, subprocess, sys
from pathlib import Path

BASE = "044cb25f"
ENG = "hdl/aecp/KL_aecp_engine.sv"
ADP = "hdl/adp/KL_adp_engine.sv"
TOP = "hdl/top/protocol_processor_top.sv"
UC = "hdl/aecp/ucode/gen_ucode.py"

PROBES = {
    # the base RTL under the head's benches: the defect reproduction
    "base-rtl": dict(base=[ENG, ADP, TOP, UC], targets=[("tb/pp_top", "avail-index")]),
    # the head unchanged, the same target: the positive control
    "head-control": dict(edits=[], targets=[("tb/pp_top", "avail-index"),
                                             ("tb/pp_top", "interfaces")]),
    # top serves interface 1's index to every command (the mirror of the author's arm)
    "top-serves-if1": dict(edits=[(TOP,
        "                             ? adp_last_aidx_w[32*aecp_cmd_if_r +: 32]\n"
        "                             : adp_last_aidx_w[31:0];",
        "                             ? adp_last_aidx_w[63:32]\n"
        "                             : adp_last_aidx_w[63:32];")],
        targets=[("tb/pp_top", "interfaces")]),
    # index built at the wrong octet (32 instead of 36)
    "aidx-offset-32": dict(edits=[(UC, "ENT_AIDX_OFF = 36 ", "ENT_AIDX_OFF = 32 ")],
        targets=[("tb/pp_top", "avail-index")]),
    # tail copy starts one lane late: octets 40..47 lost
    "tail-one-lane-late": dict(edits=[(UC, "ENT_AIDX_TAIL = 40 ", "ENT_AIDX_TAIL = 48 ")],
        targets=[("tb/pp_top", "avail-index")]),
    # rdent_r never cleared at the next command's load: sticky routing
    "rdent-sticky": dict(edits=[(ENG,
        "              rboot_r    <= rboot_w;\n              rdent_r    <= 1'b0;\n",
        "              rboot_r    <= rboot_w;\n")],
        targets=[("tb/pp_top", "counters"), ("tb/pp_top", "aecp-dispatch")]),
    # the same fault against every section of the default build
    "rdent-sticky-full": dict(edits=[(ENG,
        "              rboot_r    <= rboot_w;\n              rdent_r    <= 1'b0;\n",
        "              rboot_r    <= rboot_w;\n")],
        targets=[("tb/pp_top", "default-all-sections")]),
    # last index taken from the live next index at handoff (aidx_r, not the sample)
    "last-from-live-next": dict(edits=[(ADP,
        "      last_aidx_r[bld_done_if_w] <= bld_aidx_r;",
        "      last_aidx_r[bld_done_if_w] <= aidx_r[bld_done_if_w] + 32'd1;")],
        targets=[("tb/pp_top", "avail-index")]),
    # one interface's DEPARTING clears every interface's last index
    "departing-clears-all": dict(edits=[(ADP,
        "    end else if (bld_done_dep_w) begin\n      last_aidx_r[bld_done_if_w] <= 32'd0;",
        "    end else if (bld_done_dep_w) begin\n      for (int unsigned i = 0; i < N_IF_P; i++) last_aidx_r[i] <= 32'd0;")],
        targets=[("tb/adp_engine", "interfaces")]),
}


def main():
    repo, head, work, name = sys.argv[1:5]
    p = PROBES[name]
    tree = Path(work) / name
    tree.mkdir(parents=True, exist_ok=False)
    subprocess.run(f"git -C {repo} archive {head} | tar -x -C {tree}", shell=True, check=True)
    for f in p.get("base", []):
        data = subprocess.run(["git", "-C", repo, "show", f"{BASE}:{f}"], check=True,
                              capture_output=True).stdout
        (tree / f).write_bytes(data)
        print(f"restored {f} from {BASE}")
    for f, old, new in p.get("edits", []):
        path = tree / f
        s = path.read_text()
        n = s.count(old)
        if n != 1:
            print(f"PROBE-ERROR {name}: edit in {f} matched {n} times")
            sys.exit(3)
        path.write_text(s.replace(old, new))
        print(f"edited {f}")
    env = dict(os.environ)
    env["PATH"] = "$VALIDATION_TOOLS/pinned-verilator-5.050:" + env["PATH"]
    worst = 0
    for d, tgt in p["targets"]:
        if tgt == "default-all-sections":
            # the default build, every section of its run (no section flag)
            r = subprocess.run(["make", "-C", str(tree / d), "gsi-build"], env=env,
                               capture_output=True, text=True)
            out = r.stdout + r.stderr
            if r.returncode == 0:
                r = subprocess.run(["./obj_dir/Vpp_top_sim"], cwd=tree / d, env=env,
                                   capture_output=True, text=True)
                out += r.stdout + r.stderr
        else:
            r = subprocess.run(["make", "-C", str(tree / d), tgt], env=env,
                               capture_output=True, text=True)
            out = r.stdout + r.stderr
        (Path(work) / f"{name}.{d.replace('/', '_')}.{tgt}.log").write_text(out)
        tallies = [l for l in out.splitlines()
                   if ("checks" in l and ("FAIL" in l or "failures" in l))]
        fails = [l for l in out.splitlines() if l.lstrip().startswith("FAIL")]
        print(f"{name} {d} {tgt}: rc={r.returncode} tallies={tallies[-3:]} fail_lines={len(fails)}")
        for l in fails[:12]:
            print("    " + l[:260])
        worst = max(worst, r.returncode)
    sys.exit(worst)


if __name__ == "__main__":
    main()
