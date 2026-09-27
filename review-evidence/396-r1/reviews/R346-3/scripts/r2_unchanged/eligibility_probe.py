#!/usr/bin/env python3
"""R346-2 probe: CLI eligibility and timing threading at the head under review.

Usage: python3 -B eligibility_probe.py <repo-root>
Runs the planner CLI read-only and prints, per case, the exit code and each
release step's release_eligible / topology_explicit / timing fields.
"""
import json, subprocess, sys
root = sys.argv[1]
DUT = "entity=0011223344556677,mac=001122334455,talkers=2,listeners=2,crf_out=2,crf_in=2"
PEER = "entity=8899aabbccddeeff,mac=8899aabbccdd,talker_index_set=0|2,listener_index_set=0|2,crf_out=3,crf_in=3"
BASE = ["--plan", "--areas", "soak,power", "--json"]
cases = {
    "explicit defaults": ["--dut", DUT, "--peer", PEER],
    "explicit restore-bound 600": ["--dut", DUT, "--peer", PEER, "--restore-bound-s", "600"],
    "explicit restore-bound 3600 margin 1": ["--dut", DUT, "--peer", PEER, "--restore-bound-s", "3600", "--boot-margin-s", "1"],
    "explicit restore-bound 29": ["--dut", DUT, "--peer", PEER, "--restore-bound-s", "29"],
    "explicit boot-margin 10000": ["--dut", DUT, "--peer", PEER, "--boot-margin-s", "10000"],
    "explicit interval 60": ["--dut", DUT, "--peer", PEER, "--soak-interval-s", "60"],
    "explicit interval 61": ["--dut", DUT, "--peer", PEER, "--soak-interval-s", "61"],
    "explicit interval 604800": ["--dut", DUT, "--peer", PEER, "--soak-interval-s", "604800"],
    "explicit items clock_source": ["--dut", DUT, "--peer", PEER, "--persisted-items", "clock_source"],
    "explicit items stream_binding,x": ["--dut", DUT, "--peer", PEER, "--persisted-items", "stream_binding,x"],
    "fixture topology": [],
    "dut uses entity_id alias": ["--dut", DUT.replace("entity=", "entity_id="), "--peer", PEER],
    "dut missing mac": ["--dut", DUT.replace("mac=001122334455,", ""), "--peer", PEER],
    "peer missing crf_in": ["--dut", DUT, "--peer", PEER.replace(",crf_in=3", "")],
    "dut aaf overlaps crf (talkers=3,crf_out=2)": ["--dut", DUT.replace("talkers=2", "talkers=3"), "--peer", PEER],
    "peer listener set overlaps crf": ["--dut", DUT, "--peer", PEER.replace("listener_index_set=0|2", "listener_index_set=0|3")],
    "restore-bound 0": ["--restore-bound-s", "0"],
    "boot-margin -1": ["--boot-margin-s", "-1"],
    "restore-bound nan-string": ["--restore-bound-s", "x"],
    "power only, explicit, interval 120": ["--areas", "power", "--dut", DUT, "--peer", PEER, "--soak-interval-s", "120"],
}
for name, extra in cases.items():
    argv = BASE + extra
    if "--areas" in extra:
        argv = ["--plan", "--json"] + extra
    r = subprocess.run([sys.executable, "-B", "tb/tools/torture_campaign.py", *argv],
                       cwd=root, capture_output=True, text=True)
    line = f"{name:45s} rc={r.returncode}"
    if r.returncode == 0:
        for s in json.loads(r.stdout):
            a = s["args"]
            line += (f" | {s['sid']}: eligible={a['release_eligible']} explicit={a['topology_explicit']}"
                     + (f" restore={a['restore_bound_s']} obs={a['boot_observation_s']}" if s['area'] == 'power' else
                        f" interval={a['interval_s']}"))
    else:
        line += " | " + (r.stderr.strip().splitlines() or [""])[-1][:140]
    print(line)
