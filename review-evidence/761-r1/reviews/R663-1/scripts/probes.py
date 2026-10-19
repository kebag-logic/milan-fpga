#!/usr/bin/env python3
"""Reviewer fault probes for PR #767 at 4191b098 (disposable; never edits a checkout).

Usage: probes.py <tree> <workdir> <probe>...   probes: aaf_eng aaf_both crf_stop mclk_ungated
  <tree>    a copy of the reviewed head (git-backed for mclk_ungated)
  <workdir> scratch directory for mutated sources and builds
Each probe plants ONE edit by exact anchor (the anchor must occur once), rebuilds
through the suite's own Makefile recipe and prints the harness [FAIL] lines.
Exit status is 0 when every probe built and ran; the verdict per probe is in
the printed summary (CAUGHT = the harness failed, SURVIVED = it passed).
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
ENGINE = "hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv"
REF = "tb/verilator/avtp_rxmon/reference/KL_avtp_rx_monitor_ctx_ref.sv"
UNBIND_CLEAR = "        if (bind_fall_i[s]) sil_si_r[s] <= 1'b0;\n"
CRF = "hdl/ieee1722/crf/KL_crf_rx.sv"
DP = "hdl/milan/milan_datapath.sv"


def plant(src: Path, dst: Path, anchor: str, repl: str) -> None:
    text = src.read_text()
    if text.count(anchor) != 1:
        raise SystemExit(f"anchor count {text.count(anchor)} in {src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text.replace(anchor, repl))


def run(cmd, cwd, log: Path) -> int:
    with log.open("w") as fh:
        return subprocess.run(cmd, cwd=cwd, stdout=fh, stderr=subprocess.STDOUT,
                              check=False).returncode


def report(name: str, logs: list[Path], rcs: list[int]) -> str:
    fails = []
    for log in logs:
        fails += [l.strip() for l in log.read_text(errors="replace").splitlines()
                  if l.strip().startswith("[FAIL]") or "FAIL" in l[:8]]
    verdict = "CAUGHT" if any(rcs) else "SURVIVED"
    print(f"== {name}: {verdict} rcs={rcs}")
    for f in fails[:12]:
        print(f"   {f[:200]}")
    if len(fails) > 12:
        print(f"   ... {len(fails) - 12} more failure lines")
    return verdict


def lockstep(name: str, eng: Path, ref: Path | None) -> str:
    """Build the lockstep harness at N=1/N=8 through its own recipe.

    The Makefile names the frozen reference by a relative path, so a probe
    that also edits the reference runs from a private copy of the whole tree.
    """
    root = TREE
    if ref is not None:
        root = WORK / f"{name}_tree"
        if root.exists():
            shutil.rmtree(root)
        shutil.copytree(TREE, root, symlinks=True,
                        ignore=shutil.ignore_patterns("obj_*", "__pycache__", ".git"))
        shutil.copy(ref, root / REF)
    tb = root / "tb/verilator/avtp_rxmon"
    mk = ["make", f"RXMON_SRC={eng}", f"LS_MDIR={WORK}/{name}_obj_ls", "lockstep-build"]
    blog = WORK / f"{name}.build.log"
    rc = run(mk, tb, blog)
    if rc:
        print(f"== {name}: BUILD FAILED rc={rc} (see {blog})")
        return "BUILD-FAILED"
    rcs, logs = [], []
    for n in (1, 8):
        log = WORK / f"{name}.N{n}.log"
        rcs.append(run([f"{WORK}/{name}_obj_ls{n}/Vavtp_rxmon_lockstep"], tb, log))
        logs.append(log)
    return report(name, logs, rcs)


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MAKEFLAGS", "")
    out = {}
    for probe in sys.argv[3:]:
        if probe == "aaf_eng":       # unbind no longer cancels a pending silence mark (engine only)
            eng = WORK / "aaf_eng.sv"
            plant(TREE / ENGINE, eng, UNBIND_CLEAR, "")
            out[probe] = lockstep(probe, eng, None)
        elif probe == "aaf_both":    # the same edit in engine AND frozen reference
            eng = WORK / "aaf_both.sv"
            ref = WORK / "aaf_both_ref.sv"
            plant(TREE / ENGINE, eng, UNBIND_CLEAR, "")
            plant(TREE / REF, ref, UNBIND_CLEAR, "")
            out[probe] = lockstep(probe, eng, ref)
        elif probe == "crf_stop":    # a STOPPED CRF sink's timeout counts STREAM_INTERRUPTED
            rtl = WORK / "crf_stop.sv"
            plant(TREE / CRF, rtl,
                  "if (en_i && !stop_i) cnt_intr_o <= cnt_intr_o + 32'd1;",
                  "if (en_i) cnt_intr_o <= cnt_intr_o + 32'd1;")
            mdir = WORK / "obj_crf_stop"
            blog = WORK / "crf_stop.build.log"
            rc = run(["make", "unit-build", f"RX_RTL={rtl}", f"UNIT_MDIR={mdir}"],
                     TREE / "tb/verilator/crf_rx", blog)
            if rc:
                out[probe] = "BUILD-FAILED"; print(f"== {probe}: BUILD FAILED"); continue
            log = WORK / "crf_stop.run.log"
            rc = run([str(mdir / "Vcrf_rx_sim")], TREE / "tb/verilator/crf_rx", log)
            out[probe] = report(probe, [log], [rc])
        elif probe == "mclk_ungated":  # the CRF lock-GAIN request escapes the clock-source gate
            rtl = WORK / "mclk_ungated_dp.sv"
            plant(TREE / DP, rtl,
                  "        & ((tkd_crflk_q_r ^ crf_locked_w) | crf_mr_toggle_p_w))\n",
                  "        & ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w))\n"
                  "       | (~tkd_crflk_q_r & crf_locked_w)\n")
            mdir = WORK / "obj_mclk_ungated"
            blog = WORK / "mclk_ungated.build.log"
            here = TREE / "tb/verilator/milan_dp_mclk"
            rc = run(["make", "mclk-build", f"MUT_DP_SRC={rtl}", f"MCLK_MDIR={mdir}",
                      "VERILATOR_JOBS=8"], here, blog)
            if rc:
                out[probe] = "BUILD-FAILED"; print(f"== {probe}: BUILD FAILED"); continue
            procs, logs = [], []
            for mode in ("a", "c", "b"):   # the three clean legs, concurrently
                log = WORK / f"mclk_ungated.{mode}.log"
                fh = log.open("w")
                procs.append((subprocess.Popen(
                    [str(mdir / "Vmilan_dp_mclk"), f"--{mode}", "+MCLK_MUT=0"],
                    cwd=here, stdout=fh, stderr=subprocess.STDOUT), fh))
                logs.append(log)
            rcs = []
            for proc, fh in procs:
                rcs.append(proc.wait())
                fh.close()
            out[probe] = report(probe, logs, rcs)
        else:
            raise SystemExit(f"unknown probe {probe}")
    print("SUMMARY", " ".join(f"{k}={v}" for k, v in out.items()))
    return 1 if any(v == "BUILD-FAILED" for v in out.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
