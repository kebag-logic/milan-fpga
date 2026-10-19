#!/usr/bin/env python3
"""Plant one RTL mutant at a time in a committed scratch parent snapshot and
run one milan_dp leg (default `gptp`), to show a companion check fails.

usage: parent_mut_dp.py <parent-tree> <logdir> <target> <arm> [<arm> ...]

Arms are named below; each is an exact-text replacement in one RTL file (the
engine texts are the lane's engine mutants.py texts). After each arm the
mutated file is restored with `git checkout` in the repository that owns it,
and the tree is checked clean. Writes <logdir>/<arm>.log and appends one
"<arm> rc=<n> secs=<s> fails=<k>" line to <logdir>/rc.txt.
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

ENGINE = "gptp-processor/hdl/top/KL_gptp_engine.sv"
CLKV = "hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv"
GENERATOR = "gptp-processor/hdl/ucode/gen_gptp_ucode.py"
ARMS = {
    "control": None,
    "no-thisclock": (
        ENGINE,
        "  wire       path_append_w = (ann_pub_count_clamped_w != 4'd0) &&\n"
        "                             (ann_pub_count_clamped_w != 4'd8);\n",
        "  wire       path_append_w = 1'b0;\n"),
    "appended-source": (
        ENGINE,
        "                    pub_path_r[64*pk +: 64] <= rom_clock_id_w;\n",
        "                    pub_path_r[64*pk +: 64] <= frame_cid_r;\n"),
    "reset-gm-zero": (
        ENGINE,
        "      pub_gm_r        <= rom_clock_id_w;\n",
        "      pub_gm_r        <= 64'd0;\n"),
    "first-gm-no-hold": (
        CLKV,
        "                     (fabric_disc_p_i | (gm_id_i != gm_r)));\n",
        "                     (fabric_disc_p_i | ((gm_id_i != gm_r) &&\n"
        "                                         (gm_r != 64'd0))));\n"),
    "hold-never-armed": (
        CLKV,
        "      if (disc_p_w)                 hold_r <= HOLD_W_C'(HOLD_MAX_C);\n",
        "      if (disc_p_w)                 hold_r <= '0;\n"),
    "become-no-syncok": (
        GENERATOR,
        "    e_flags(p, andm=FL_ASCAP_C, orm=FL_AMGM_C | FL_SYNCOK_C)\n",
        "    e_flags(p, andm=FL_ASCAP_C, orm=FL_AMGM_C)\n"),
    "self-keeps-departed-gm": (
        GENERATOR,
        "    p.emit(\"WRST\", ra=RC, imm=RG_PUB | 0, fmt=FMT_Q)\n"
        "    p.emit(\"WRST\", ra=RC, imm=RG_PUB | 1, fmt=FMT_Q)\n",
        "    p.emit(\"WRST\", ra=RC, imm=RG_PUB | 1, fmt=FMT_Q)\n"),
}


def git(repo: Path, *argv: str) -> str:
    """Run git in `repo` after checking that `repo` is its own top level."""
    top = subprocess.run(["git", "-C", str(repo), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, check=True).stdout.strip()
    assert Path(top) == repo.resolve(), (top, repo)
    return subprocess.run(["git", "-C", str(repo), *argv], capture_output=True,
                          text=True, check=True).stdout


def owner(tree: Path, rel: str) -> tuple[Path, str]:
    """The repository holding `rel` and the path inside it."""
    if rel.startswith("gptp-processor/"):
        return tree / "gptp-processor", rel.split("/", 1)[1]
    return tree, rel


def main() -> int:
    tree, logdir, target = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    logdir.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env["PATH"] = ("<pinned-tools>:<home>/.local/bin:"
                   "/usr/local/sbin:/usr/local/bin:/usr/bin:/bin")
    env["TMPDIR"] = "<scratch>/tmpdir"
    assert git(tree, "status", "--porcelain") == "", "tree not clean"
    obj = {"gptp": "obj_gptp", "gptp-lat": "obj_gptplat",
           "ax1x1gptp": "obj_ax1x1gptp"}[target]
    for name in sys.argv[4:]:
        arm = ARMS[name]
        if arm is not None:
            path = tree / arm[0]
            text = path.read_text()
            assert text.count(arm[1]) == 1, name
            path.write_text(text.replace(arm[1], arm[2]))
        subprocess.run(["rm", "-rf", str(tree / "tb/verilator/milan_dp" / obj)],
                       check=True)
        start = time.time()
        log_path = logdir / f"{name}.log"
        with open(log_path, "w", encoding="utf-8") as log:
            rc = subprocess.run(["make", "-C", "tb/verilator/milan_dp", target,
                                 "VERILATOR_JOBS=8"], cwd=tree, env=env,
                                stdout=log, stderr=subprocess.STDOUT).returncode
        if arm is not None:
            repo, rel = owner(tree, arm[0])
            git(repo, "checkout", "--", rel)
        assert git(tree, "status", "--porcelain") == "", "tree not restored"
        fails = sum(1 for line in log_path.read_text().splitlines()
                    if line.startswith("FAIL ") or line.startswith("  [FAIL]"))
        line = f"{name} rc={rc} secs={int(time.time() - start)} fails={fails}"
        with open(logdir / "rc.txt", "a", encoding="utf-8") as f:
            f.write(line + "\n")
        print(line, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
