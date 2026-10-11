#!/usr/bin/env python3
"""Composition probe for #696 on the merge-train candidate.

The candidate's hdl/milan/milan_datapath.sv carries this PR's two new KL_maap
connections (port_operational_i, realtime_ns_i) beside M6's datapath hunks.
The datapath elaboration flags waive PINMISSING, so a connection dropped by a
merge compiles silently. Each probe rewrites one exact-once anchor in a scratch
copy of the candidate datapath, builds the suite's real-datapath MAAP harness
(tb/verilator/maap/sim_integration.cpp) against it with the suite's own source
list and flags, and requires the named check to fail. A clean control through
the same route must pass. No checkout file is written; builds live under the
scratch directory given.

usage: probe_datapath_wiring.py <repo> <scratch-dir> <probe-name|clean> [...]
"""
import os
import subprocess
import sys
from pathlib import Path

LINK = "    .port_operational_i (eff_link_w),\n"
CLOCK = "    .realtime_ns_i     (ptp_now_w[31:0]),\n"
PROBES = {
    "clean": (None, None, None),
    "link_tied_high": (LINK, "    .port_operational_i (1'b1),\n",
                       "M5 datapath: link return starts four fresh PROBEs"),
    "link_dropped": (LINK, "",
                     "M5 datapath: link return starts four fresh PROBEs"),
    "clock_dropped": (CLOCK, "",
                      "M3 datapath: fixed PHC time pair claims different first offsets"),
}


def main() -> int:
    repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    suite = repo / "tb/verilator/maap"
    rel_dp = "../../../hdl/milan/milan_datapath.sv"
    env = dict(os.environ, MAKEFLAGS="")
    srcs = subprocess.run(["make", "-s", "--no-print-directory", "-C", "../milan_dp",
                           "print-srcs"], cwd=suite, env=env, capture_output=True,
                          text=True, check=True).stdout.split()
    flags = subprocess.run(["make", "-s", "--no-print-directory", "-C", "../milan_dp",
                            "print-dp-vflags", "VERILATOR_JOBS=2"], cwd=suite, env=env,
                           capture_output=True, text=True, check=True).stdout.strip()
    if srcs.count(rel_dp) != 1:
        print(f"source list names the datapath {srcs.count(rel_dp)} times")
        return 2
    original = (suite / rel_dp).read_text()
    verdicts = 0
    for name in sys.argv[3:]:
        anchor, replacement, failure = PROBES[name]
        work = scratch / name
        work.mkdir(parents=True, exist_ok=True)
        source = original
        if anchor is not None:
            if original.count(anchor) != 1:
                print(f"[BAD] {name}: anchor occurs {original.count(anchor)} times")
                verdicts += 1
                continue
            source = original.replace(anchor, replacement)
        dp = work / "milan_datapath.sv"
        dp.write_text(source)
        mdir = work / "obj"
        mdir.mkdir(exist_ok=True)
        for gen, out in (("protocol-processor/hdl/acmp/rom/gen_ltn_rom.py", "ltn_rom.hex"),
                         ("protocol-processor/hdl/aecp/ucode/gen_ucode.py", "ucode.hex")):
            subprocess.run([sys.executable, str(repo / gen), "-o", str(mdir / out)],
                           check=True, capture_output=True)
        cmd = (f"verilator +incdir+../../../configs/generated/endstation_ax7101_1x1_tdm8 "
               f"{flags} --Mdir {mdir} -GMAAP_CLK_HZ_P=10000 -GN_STREAMS=1 "
               f"-GTALKER_WIRE_CHANS_P=8 -GAUDIO_IF_SLOTS_P=8 -GAUDIO_IF_MASTER_P=1 "
               f"-GLOOPBACK_P=1 -GI2SPB_P=0 -GLPF_P=0 "
               + " ".join(str(dp) if s == rel_dp else s for s in srcs)
               + " sim_integration.cpp -o maap_integration")
        build = subprocess.run(cmd, shell=True, cwd=suite, capture_output=True, text=True)
        (work / "build.log").write_text(build.stdout + build.stderr)
        if build.returncode:
            print(f"[BAD] {name}: build rc={build.returncode}")
            verdicts += 1
            continue
        run = subprocess.run([str(mdir / "maap_integration")], cwd=mdir,
                             capture_output=True, text=True)
        out = run.stdout + run.stderr
        (work / "run.log").write_text(out)
        fails = [line for line in out.splitlines() if line.startswith("[FAIL]")]
        if failure is None:
            ok = run.returncode == 0 and " 0 failures" in out
        else:
            ok = run.returncode == 1 and f"[FAIL] {failure}" in out
        tag = "CONTROL-PASS" if failure is None and ok else ("CAUGHT" if ok else "ESCAPED")
        print(f"[{tag}] {name}: rc={run.returncode}; failing checks: {fails}")
        print("  " + (out.strip().splitlines() or [""])[-1])
        verdicts += 0 if ok else 1
    return 1 if verdicts else 0


if __name__ == "__main__":
    sys.exit(main())
