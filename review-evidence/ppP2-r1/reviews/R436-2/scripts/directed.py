#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer-owned directed checks R436d-f (R436-2), injected into probe copies
of tb/nvm_port only, never proposed as the PR's code, and run against the head
RTL and against the planted defects the PR's 343 checks pass (Q1, Q9), plus
D26 and Q2 for contrast. `make -s run`: both builds, at 100 and at 37.

  R436d  a backend without erase semantics answers the ERASE on its grant, then
         grants the WRITE exactly TMO cycles after the request shows: legal, so
         the commit must be served (the latched S_WEWAIT cycle owes nothing).
  R436e  the device presents a withheld payload byte on the (TMO + 1)-th owed
         cycle, the manager having dropped rready on the one cycle the count
         sat at its bound: legal, so the restore must be served (a paused cycle
         never ends the operation).
  R436f  the same with the pause one owed cycle later, so the device is one
         owed cycle late: DEADLINE (the boundary control for R436e).

usage: directed.py <head export> <out dir> [--jobs N]
"""
import argparse
import concurrent.futures as cf
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import plant                     # noqa: E402  (the plant definitions)
import rerun_round1 as rr        # noqa: E402  (the copy-edit-make driver)

SIM = "tb/nvm_port/sim_main.cpp"
ANCHOR = "  a_short_command_is_a_device_error();\n  every_operation_got_what_it_was_owed();"
CODE = r"""  a_short_command_is_a_device_error();
  { // [R436-2] reviewer-owned directed checks on the pause (not part of the PR)
    fresh_reset();
    h.deadline_ok = true;
    const std::vector<uint8_t> rr = frame(2, pattern(40, 0x3D));
    CHECK(h.commit(2, rr) == 0, "R436 setup: region 2 committed");
    // (d) ERASE answered on its grant, WRITE granted TMO cycles after its request
    h.gnt_done_on_erase = true;
    int rc = silenced(true, rr, SIL_GNT, 1, TMO);
    h.gnt_done_on_erase = false;
    CHECK(rc == 0 && h.done_pulses == 1 && h.err_pulses == 0 && h.sent == rr
              && h.gnt_done_pairs == 1,
          "R436d an ERASE answered on its own grant, then the WRITE granted %d cycles "
          "after its request: the latched terminal owes nothing and the commit is "
          "served (rc %d, cause %d, pairs %d)", TMO, rc, h.last_cause, h.gnt_done_pairs);
    // (e)/(f) a withheld payload byte released after `owed` owed cycles, with
    // rready dropped for the one cycle that follows them
    for (int late = 0; late < 2; ++late) {
      fresh_reset();
      h.ops.clear();
      h.arm_silence(SIL_BYTE, 1, -1, 10);
      h.clear_capture();
      h.m_mode = 2; h.m_stall = 0;
      h.start(false, 2);
      for (long g = 0; h.rbytes.size() < 18 && g < kOpTimeoutCycles; ++g) h.tick();
      for (int i = 0; i < TMO + late; ++i) h.tick();
      const bool pulsed_early = (h.done_pulses + h.err_pulses) > 0;
      h.m_stall = 1;
      h.tick();
      h.sil_block = false;
      rc = h.run_op();
      if (late == 0) {
        CHECK(!pulsed_early && rc == 0 && h.done_pulses == 1 && h.err_pulses == 0
                  && h.rbytes == rr,
              "R436e a payload byte on the (TMO + 1)-th owed cycle, rready dropped on "
              "the cycle the count sat at its bound: a paused cycle never ends the "
              "operation and the restore is served (rc %d, cause %d, %zu bytes)",
              rc, h.last_cause, h.rbytes.size());
      } else {
        CHECK(rc == 1 && h.err_pulses == 1 && h.last_cause == 3,
              "R436f the same byte one owed cycle later: DEADLINE (rc %d, cause %d)",
              rc, h.last_cause);
      }
    }
    fresh_reset();
    h.deadline_ok = false;
  }
  every_operation_got_what_it_was_owed();"""

CASES = {
    "head": [],
    "Q1": plant.PLANTS["Q1-wewait-latched-owes"],
    "Q9": plant.PLANTS["Q9-verdict-on-paused-cycle"],
    "Q2": plant.PLANTS["Q2-rhwait-latched-owes"],
    "D26": plant.PLANTS["D26"],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("head"); ap.add_argument("out")
    ap.add_argument("--jobs", type=int, default=6)
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    rr.MODELS["directed"] = [(SIM, ANCHOR, CODE)]
    rr.MODELS["directed+coincident"] = [(SIM, ANCHOR, CODE)] + rr.MODELS["coincident"]
    jobs = []
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for name, edits in CASES.items():
            e = [(rr.RTL, o, n) for o, n in edits]
            for m in ("directed", "directed+coincident"):
                jobs.append(ex.submit(rr.run, Path(a.head), None, out, name, e, m, False))
        lines = []
        for f in jobs:
            tag, res, fails = f.result()
            lines.append(f"{tag}: {res}" + "".join(f"\n    {x}" for x in fails[:8]))
    (out / "SUMMARY.txt").write_text("\n".join(sorted(lines)) + "\n")
    print("\n".join(sorted(lines)))


if __name__ == "__main__":
    main()
