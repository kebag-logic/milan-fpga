#!/usr/bin/env python3
"""Reviewer probe: derive a probe copy of tb/verilator/engine/sim_main.cpp.

usage: make_probe_harness.py IN_SIM_MAIN OUT_SIM_MAIN

Adds, without changing any existing check:
  * PROBE-INV: a per-commit invariant over the whole suite. After the first
    cold-boot commit no commit may name grandmaster 0; a commit naming
    thisClock must carry exactly {thisClock} (count 1, zero tail); a count
    of 0 or 1 must carry a zero tail.
  * PROBE-COLD: prints the cycle and time (2 MHz model clock) of the first
    commit after the cold release, and the outward GM/count sampled 1000
    cycles after the release.
  * PROBE-WARM-RETAINED (new final phase): a better peer A wins, the plane
    takes a warm reset while A is the retained best record, A is silent, and
    a peer B that is worse than A but better than this plane announces.
    802.1AS-2020 port vectors do not survive a reset, so B is the expected
    grandmaster. The phase reports what is committed.
"""
import sys

src = open(sys.argv[1], encoding="utf-8").read()


def sub(old, new, count=1):
    global src
    if src.count(old) != count:
        sys.exit(f"pattern count {src.count(old)} != {count}: {old[:60]!r}")
    src = src.replace(old, new)


# --- per-commit invariant, sampled where the harness samples commits ------
sub("      commit_snaps.push_back(s);\n",
    "      commit_snaps.push_back(s);\n"
    "      if (probe_cold_seen) {\n"
    "        bool tail0 = true;\n"
    "        for (unsigned k = 0; k < PATH_TAIL_SLOTS; k++) tail0 &= s.tail[k] == 0;\n"
    "        if (s.gm == 0) { probe_gm0++; printf(\"PROBE-INV gm0 commit at cyc %llu count %u\\n\", (unsigned long long)cyc, s.count); }\n"
    "        if (s.gm == OUR_CID && !(s.count == 1 && tail0)) { probe_self_bad++; printf(\"PROBE-INV self commit with count %u tail0 %d at cyc %llu\\n\", s.count, tail0, (unsigned long long)cyc); }\n"
    "        if (s.count <= 1 && !tail0) { probe_tail_bad++; printf(\"PROBE-INV count %u with nonzero tail at cyc %llu\\n\", s.count, (unsigned long long)cyc); }\n"
    "        probe_commits++;\n"
    "      } else if (dut->rst_n && s.gm != 0) {\n"
    "        probe_cold_seen = true;\n"
    "        printf(\"PROBE-COLD first nonzero-GM commit at cyc %llu, %llu cycles after release = %.4f s; gm %016llx count %u\\n\", (unsigned long long)cyc, (unsigned long long)(cyc - probe_release_cyc), (cyc - probe_release_cyc) / 2.0e6, (unsigned long long)s.gm, s.count);\n"
    "      } else if (dut->rst_n) {\n"
    "        probe_pre_commits++;\n"
    "        printf(\"PROBE-COLD zero-GM commit before thisClock at cyc %llu count %u\\n\", (unsigned long long)cyc, s.count);\n"
    "      }\n"
    "      if (probe_cold_seen && probe_cold_first_cyc == 0) probe_cold_first_cyc = cyc;\n")

sub("  std::vector<PubSnap> commit_snaps;\n",
    "  std::vector<PubSnap> commit_snaps;\n"
    "  bool probe_cold_seen = false;\n"
    "  uint64_t probe_release_cyc = 0, probe_cold_first_cyc = 0;\n"
    "  uint64_t probe_gm0 = 0, probe_self_bad = 0, probe_tail_bad = 0;\n"
    "  uint64_t probe_commits = 0, probe_pre_commits = 0;\n")

sub("    dut->rst_n = 1;\n    cold_boot_mark = commit_snaps.size();\n",
    "    dut->rst_n = 1;\n    cold_boot_mark = commit_snaps.size();\n"
    "    probe_release_cyc = cyc;\n")

# outward value 1000 cycles after the cold release, before the first beat
sub("  void publish_thisclock_before_any_peer() {\n",
    "  void publish_thisclock_before_any_peer() {\n"
    "    printf(\"PROBE-COLD harness at cyc %llu (%.4f s after release) when 1d grades\\n\", (unsigned long long)cyc, (cyc - probe_release_cyc) / 2.0e6);\n")

# a final phase after #82 phase 35
sub("    return_to_thisclock_around_a_winning_peer();\n",
    "    return_to_thisclock_around_a_winning_peer();\n"
    "    probe_warm_reset_with_a_retained_record();\n"
    "    printf(\"PROBE-INV commits graded %llu: gm0 %llu, self-path bad %llu, tail bad %llu; zero-GM commits before thisClock %llu\\n\", (unsigned long long)probe_commits, (unsigned long long)probe_gm0, (unsigned long long)probe_self_bad, (unsigned long long)probe_tail_bad, (unsigned long long)probe_pre_commits);\n"
    "    expect(\"PROBE-INV no commit names GM 0 after thisClock\", probe_gm0, 0);\n"
    "    expect(\"PROBE-INV every thisClock commit carries {thisClock}\", probe_self_bad, 0);\n"
    "    expect(\"PROBE-INV count 0/1 commits carry a zero tail\", probe_tail_bad, 0);\n")

sub("  //! A #75 policy probe uses wire frames and watches every output edge.\n",
    "  void probe_warm_reset_with_a_retained_record() {\n"
    "    const uint64_t GMA = 0x0065A0FFFE0000A1ull, SRCA = 0x0065A0FFFE0000A3ull;\n"
    "    const uint64_t GMB = 0x0065A0FFFE0000B1ull, SRCB = 0x0065A0FFFE0000B3ull;\n"
    "    pd_mode = PD_NORMAL;\n"
    "    wait_flags(FL_ASCAP, FL_ASCAP, 9000000);\n"
    "    size_t m = commit_snaps.size();\n"
    "    send_announce(0x6501, 0, GMA, 1, SRCA, {GMA, SRCA}, phc() + 100);\n"
    "    printf(\"PROBE-WARM A announce: %zu commits, last gm %016llx count %u\\n\", commit_snaps.size() - m, commit_snaps.size() > m ? (unsigned long long)commit_snaps.back().gm : 0ull, commit_snaps.size() > m ? commit_snaps.back().count : 0);\n"
    "    expect(\"PROBE-WARM peer A elected\", commit_snaps.size() > m ? commit_snaps.back().gm : 0, GMA);\n"
    "    m = commit_snaps.size();\n"
    "    warm_reset();\n"
    "    printf(\"PROBE-WARM after warm reset: %zu commits, first gm %016llx count %u\\n\", commit_snaps.size() - m, commit_snaps.size() > m ? (unsigned long long)commit_snaps[m].gm : 0ull, commit_snaps.size() > m ? commit_snaps[m].count : 0);\n"
    "    expect(\"PROBE-WARM warm reset publishes thisClock\", commit_snaps.size() > m ? commit_snaps[m].gm : 0, OUR_CID);\n"
    "    wait_flags(FL_ASCAP, FL_ASCAP, 9000000);\n"
    "    m = commit_snaps.size();\n"
    "    send_announce(0x6502, 1, GMB, 1, SRCB, {GMB, SRCB}, phc() + 100);\n"
    "    const uint64_t got = commit_snaps.size() > m ? commit_snaps.back().gm : 0;\n"
    "    printf(\"PROBE-WARM B announce after reset: %zu commits, last gm %016llx (A=%016llx B=%016llx self=%016llx) parent %016llx count %u flags %x\\n\", commit_snaps.size() - m, (unsigned long long)got, (unsigned long long)GMA, (unsigned long long)GMB, (unsigned long long)OUR_CID, commit_snaps.size() > m ? (unsigned long long)commit_snaps.back().parent : 0ull, commit_snaps.size() > m ? commit_snaps.back().count : 0, commit_snaps.size() > m ? commit_snaps.back().flags : 0);\n"
    "    for (int beat = 0; beat < 3; beat++) {\n"
    "      run_svc(2000000);\n"
    "      m = commit_snaps.size();\n"
    "      send_announce(0x6503 + beat, 1, GMB, 1, SRCB, {GMB, SRCB}, phc() + 100);\n"
    "      printf(\"PROBE-WARM B announce %d s later: outward gm %016llx parent %016llx flags %x, %zu commits\\n\", beat + 1, (unsigned long long)dut->pub_gm_id_o, (unsigned long long)dut->pub_parent_id_o, dut->pub_flags_o, commit_snaps.size() - m);\n"
    "    }\n"
    "    expect(\"PROBE-WARM a peer B better than this plane is elected after the reset\", dut->pub_gm_id_o, GMB);\n"
    "  }\n\n"
    "  //! A #75 policy probe uses wire frames and watches every output edge.\n")

open(sys.argv[2], "w", encoding="utf-8").write(src)
print("probe harness written")
