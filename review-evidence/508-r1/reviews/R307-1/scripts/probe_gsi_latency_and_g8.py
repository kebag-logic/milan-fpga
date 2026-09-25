#!/usr/bin/env python3
"""Reviewer probe (R307-1, PR #560): instrument a DISPOSABLE copy of
tb/verilator/milan_dp/sim_nxn.cpp.

1. After G6, sink 0's registered Talker Failed is re-declared (JoinIn) with
   ONLY its AccumulatedLatency changed. The processor's #113 latency-only
   notification should push exactly one GET_STREAM_INFO for sink 0 to each
   registered controller, none for sink 1, and the push must equal the
   solicited answer. Checks are tagged [PROBE-LAT].
2. G8's withdrawal push count (the leg checks only ">= 1") is printed per
   controller and per sink, tagged [PROBE-G8].

Usage: probe_gsi_latency_and_g8.py <path to a scratch copy of sim_nxn.cpp>
The file is rewritten in place; never point it at a tracked checkout.
"""
import sys
from pathlib import Path

p = Path(sys.argv[1])
t = p.read_text()

def sub(old, new):
    global t
    n = t.count(old)
    if n != 1:
        sys.exit(f"pattern found {n} times: {old[:60]!r}")
    t = t.replace(old, new)

# per-sink latency, default the leg's 500000
sub("    std::array<unsigned, kGsiSinks> gsi_tf_code{};\n",
    "    std::array<unsigned, kGsiSinks> gsi_tf_code{};\n"
    "    std::array<uint32_t, kGsiSinks> gsi_tf_lat{{500000u, 500000u}};\n")
sub("        gsi_put(f, 42, 500000, 4);                   // AccumulatedLatency\n",
    "        gsi_put(f, 42, gsi_tf_lat[z], 4);            // AccumulatedLatency (probe)\n")

# latency-only phase after G6
sub("            snprintf(tag, sizeof tag, \"[GSI] G6 sink %d unchanged refresh\", s);\n"
    "            gsi_ck_pushes(tag, s, 0);\n"
    "        }\n",
    "            snprintf(tag, sizeof tag, \"[GSI] G6 sink %d unchanged refresh\", s);\n"
    "            gsi_ck_pushes(tag, s, 0);\n"
    "        }\n"
    "        notify_clear();\n"
    "        gsi_tf_lat[0] = 750000u;\n"
    "        gsi_declare(0, kGsiSink[0].bridge, kGsiSink[0].code, 1);\n"
    "        gsi_ms(kGsiWinMs);\n"
    "        {\n"
    "            const std::vector<uint8_t> g = gsi_ck_pushes(\"[PROBE-LAT] sink 0 latency-only change\", 0, 1);\n"
    "            gsi_ck_failure(\"[PROBE-LAT] sink 0 latency-only change\", g, true, kGsiSink[0].bridge, kGsiSink[0].code);\n"
    "            gsi_ck_state(\"[PROBE-LAT] sink 0 latency-only change\", g, kPbCompleted, 0);\n"
    "            gsi_ck_pushes(\"[PROBE-LAT] sink 1 quiet on sink 0's latency\", 1, 0);\n"
    "        }\n")

# G8 push counts
sub("        const long pushes = notify_count(0x000F, &CTL_B, 0x0005, 0);\n",
    "        const long pushes = notify_count(0x000F, &CTL_B, 0x0005, 0);\n"
    "        printf(\"  [PROBE-G8] withdrawal pushes: sink0->A %ld sink0->B %ld sink1->A %ld sink1->B %ld\\n\",\n"
    "               notify_count(0x000F, &CTL_A, 0x0005, 0), pushes,\n"
    "               notify_count(0x000F, &CTL_A, 0x0005, 1), notify_count(0x000F, &CTL_B, 0x0005, 1));\n")
p.write_text(t)
print("probe planted")

# 3. (appended) list every unsolicited GET_STREAM_INFO(sink 0) to B in G8:
#    its cycle, probing_status, acmp_status, MSRP_FAILURE_VALID, code, bridge.
t = p.read_text()
sub("        const std::vector<uint8_t> last = notify_last(0x000F, CTL_B, 0x0005, 0);\n"
    "        const std::vector<uint8_t> w = gsi_get(CTL_B, 0);\n",
    "        for (size_t i = 0; i < uns_log.size(); i++) {\n"
    "            const std::vector<uint8_t>& f = uns_log[i];\n"
    "            if (!aecp_is_unsolicited(f) || notify_cmd(f) != 0x000F || !notify_to(f, CTL_B)) continue;\n"
    "            if (f.size() < 94 || f[39] != 0x05 || f[41] != 0) continue;\n"
    "            printf(\"  [PROBE-G8] push cycle %ld pbsta %u acmpsta %u fvalid %u code %u bridge %016llx\\n\",\n"
    "                   uns_log_when[i], gsi_pb(f), gsi_as(f), gsi_flag(f, 42, 0x08), gsi_code(f),\n"
    "                   static_cast<unsigned long long>(gsi_bridge(f)));\n"
    "        }\n"
    "        const std::vector<uint8_t> last = notify_last(0x000F, CTL_B, 0x0005, 0);\n"
    "        const std::vector<uint8_t> w = gsi_get(CTL_B, 0);\n")
p.write_text(t)
print("G8 content listing planted")
