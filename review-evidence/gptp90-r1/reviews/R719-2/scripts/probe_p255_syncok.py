#!/usr/bin/env python3
"""Reviewer probe: sync-ok under a priority1 255 grandmaster whose Sync stops.

Usage: probe_p255_syncok.py <tree> <verilator>

<tree> is a disposable extraction of the repository (never a tracked
checkout). The probe appends one phase to the end of the engine harness's
priority1 255 pass: wait for mastership, elect a better priority1 255 peer,
feed it usable Sync/Follow_Up pairs at 125 ms with an Announce every
second, then stop Sync while the Announces continue, and print the published
flags at each step. It then builds the harness with <verilator> and runs only
the priority1 255 pass. Output lines start with "R719PROBE".
"""
import pathlib
import subprocess
import sys

PROBE = r'''
  // ---- reviewer probe: sync-ok under a priority1 255 grandmaster ----
  void r719_probe_p255_syncok() {
    const uint64_t G = 0x0000000000000105ull;
    const uint64_t SRC = 0x0000000000000106ull;
    uint16_t aseq = 0x9101, sseq = 0x9201;
    pd_mode = PD_NORMAL;
    bool m = wait_flags(FL_AMGM, FL_AMGM, 8000000ull);
    printf("R719PROBE start master=%d flags=%x\n", m ? 1 : 0,
           static_cast<unsigned>(dut->pub_flags_o));
    send_announce(aseq++, 255, G, 1, SRC, {G, SRC}, phc() + 100);
    run(2000);
    printf("R719PROBE elected flags=%x gm=%016llx\n",
           static_cast<unsigned>(dut->pub_flags_o),
           static_cast<unsigned long long>(dut->pub_gm_id_o));
    auto interval = [&](bool sync, bool ann) {
      uint64_t spent = 0;
      if (sync) {
        const uint64_t local = phc() + 150;
        const uint16_t seq = sseq++;
        Frame f = ptp(0x0, seq, 0, 0x0208, 10, SRC);
        f.ts(0);
        send_frame(f.b, local);
        run(1000);
        run_svc(1000);
        Frame g = follow_up(seq, 0, local - static_cast<uint64_t>(pdm.d), SRC);
        send_frame(g.b, local + 1000 * 500);
        run(1000);
        spent += 3000 + f.b.size() + g.b.size();
      }
      if (ann) {
        send_announce(aseq++, 255, G, 1, SRC, {G, SRC}, phc() + 100);
        spent += 8000;
      }
      if (spent < 250000) run_svc(250000 - spent);
    };
    for (int k = 0; k < 16; k++) interval(true, k % 8 == 3);
    printf("R719PROBE after 2 s of usable Sync flags=%x gm=%016llx\n",
           static_cast<unsigned>(dut->pub_flags_o),
           static_cast<unsigned long long>(dut->pub_gm_id_o));
    for (int s = 1; s <= 4; s++) {
      for (int k = 0; k < 8; k++) interval(false, k == 3);
      printf("R719PROBE %d s after Sync stopped flags=%x gm=%016llx "
             "syncok=%d\n", s, static_cast<unsigned>(dut->pub_flags_o),
             static_cast<unsigned long long>(dut->pub_gm_id_o),
             (dut->pub_flags_o & FL_SYNCOK) ? 1 : 0);
    }
  }
'''


def main() -> int:
    tree = pathlib.Path(sys.argv[1]).resolve()
    verilator = sys.argv[2]
    eng = tree / "tb/verilator/engine"
    src = (eng / "sim_main.cpp").read_text()
    anchor = "  void run_the_self_publication_phases() {"
    assert src.count(anchor) == 1, "anchor"
    body_start = src.index(anchor)
    body_end = src.index("\n  }\n", body_start)
    src = (src[:body_end] + "\n    r719_probe_p255_syncok();" + src[body_end:])
    src = src.replace(anchor, PROBE + "\n" + anchor, 1)
    (eng / "sim_main.cpp").write_text(src)
    gen = tree / "hdl/ucode/gen_gptp_ucode.py"
    (eng / "p1run").mkdir(exist_ok=True)
    subprocess.run([sys.executable, "-I", str(gen), "--clk-hz", "2000000",
                    "--cease-ms", "3000", "--p1", "255", "-o",
                    str(eng / "p1run/gptp_ucode.hex")], check=True,
                   stdout=subprocess.DEVNULL)
    mk = (eng / "Makefile").read_text()
    mk += "\nr719probebuild:\n\t$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vengine_sim\n"
    (eng / "Makefile").write_text(mk)
    with open(eng / "build.log", "w") as log:
        subprocess.run(["make", "-C", str(eng), f"VERILATOR={verilator}",
                        "r719probebuild"], check=True, stdout=log,
                       stderr=subprocess.STDOUT)
    r = subprocess.run(["../obj_dir/Vengine_sim", "+not-gm-capable"],
                       cwd=eng / "p1run", capture_output=True, text=True)
    for line in r.stdout.splitlines():
        if line.startswith("R719PROBE") or "checks:" in line:
            print(line)
    print(f"R719PROBE rc={r.returncode}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
