#!/usr/bin/env python3
"""Run the existing S10/MP integration checks with no-round and clean RTL.

Usage: check_top_retry.py DONOR SCRATCH
Only SCRATCH is written. The selection main calls the unchanged case methods.
"""
import shutil
import subprocess
import sys
from pathlib import Path


MAIN = r'''
int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  const milan::tb::Model<Vpp_top_wrap> instance;
  H h(instance.get());
  Suite setup(h);
  setup.load_descriptor_image();
  h.reset();
  setup.boot_restore_over_blank_nvm();
  h.d->link_up_i = 1;
  h.d->entity_enable_i = 1;
  h.run_ms(300);
  Msg dom{4, 4, false, {Vec{false, 2, fv_domain(5, 2, 5),
                              {EV_JOININ, EV_JOININ}, {}}}};
  h.feed(mrpdu_frame(true, T1_MAC, {dom}));
  h.run_ms(20);
  setup.maap_face_and_the_da_gate();
  InternalMaapPhase{h}.run();
  printf("%d checks: %d PASS, %d FAIL\n", h.checks, h.checks-h.fails, h.fails);
  return h.fails ? 1 : 0;
}
'''


def main() -> int:
    """Require the exact updated integration assertions to kill the defect."""
    donor, scratch = [Path(arg).resolve() for arg in sys.argv[1:]]
    for folder in ("hdl", "tb/pp_top", "tb/common"):
        shutil.copytree(donor / folder, scratch / folder, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("obj*", "__pycache__", "*.hex"))
    cpp = scratch / "tb/pp_top/sim_main.cpp"
    original = cpp.read_text()
    cpp.write_text(original[:original.rindex("int main(")] + MAIN)
    rtl = scratch / "hdl/acmp/KL_acmp_talker.sv"
    source = rtl.read_text()
    anchor = "retry_tick_w ? cfg_src_en_i : '0"
    assert source.count(anchor) == 1
    for variant in ("baseline", "no_round", "restored"):
        rtl.write_text(source.replace(anchor, "'0") if variant == "no_round" else source)
        with (scratch / f"{variant}-build.log").open("w") as log:
            build = subprocess.run(["make", "gsi-build"], cwd=scratch / "tb/pp_top",
                                   stdout=log, stderr=subprocess.STDOUT,
                                   timeout=900, check=False)
        if build.returncode:
            raise RuntimeError(f"{variant}: build failed, not a killed mutant")
        run = subprocess.run(["./obj_dir/Vpp_top_sim"], cwd=scratch / "tb/pp_top",
                             capture_output=True, text=True, timeout=900, check=False)
        (scratch / f"{variant}-run.txt").write_text(run.stdout + run.stderr)
        print(f"{variant}: rc={run.returncode}\n{run.stdout}", flush=True)
        if variant == "no_round":
            assert run.returncode == 1
            assert "FAIL: S10: exactly one ALLOC_DA for every enabled source" in run.stdout
            assert "FAIL: MP3: first PROBE_TX_RESPONSE succeeds after acquisition bound" in run.stdout
        else:
            assert run.returncode == 0
    print("PASS: updated S10 and MP3 assertions kill the no-round defect; clean controls rc 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
