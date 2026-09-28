// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe adapter (R377-2): runs the round-1 reviewer probes P1-P6
// (probes/r1/probe_cases.hpp, unchanged) at the round-2 head.
struct R377Round1Probes {
  int& checks;
  int& fails;
  void run_all() { run_reviewer_probes(checks, fails); }
};
