#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Timing probe for srp_top F5c (disposable export, harness-only prints).

Instruments a `git archive` export of COMMIT so the harness prints the
simulated time (now_ms_o) when each F5 step sees its own LeaveAll, at each
F5c talker-lane negative window, at the end of F5, and when the NEXT own
MSRP LeaveAll MRPDU after F5 appears. No RTL is touched and the probe's
tally is not a gate result: the extra wait changes later timing.

usage: f5c_timing_probe.py REPO COMMIT WORKDIR OUTFILE
env:   PINNED_VERILATOR (required), VL_JOBS (default 8)
"""
import io
import os
import shutil
import subprocess
import sys
import tarfile

SIM = "tb/srp_top/sim_main.cpp"
EDITS = [
    ('    CHECK(!f.empty(), "F5%s: own MSRP LeaveAll within 16 s", step);\n',
     '    CHECK(!f.empty(), "F5%s: own MSRP LeaveAll within 16 s", step);\n'
     '    printf("PROBE F5%s own LeaveAll seen at %u ms\\n", step, (unsigned)h.d->now_ms_o);\n'),
    ('    h.feed(mrpdu_body(true, {ta}), true);\n',
     '    printf("PROBE F5c TA negative window opens at %u ms\\n", (unsigned)h.d->now_ms_o);\n'
     '    h.feed(mrpdu_body(true, {ta}), true);\n'),
    ('    h.feed(mrpdu_body(true, {la_only(2, 34, false)}), true);\n',
     '    printf("PROBE F5c TF negative window opens at %u ms\\n", (unsigned)h.d->now_ms_o);\n'
     '    h.feed(mrpdu_body(true, {la_only(2, 34, false)}), true);\n'),
    ('    CHECK(h.malformed == 0, "F5: no PDU we fed was tolerance-discarded");\n  }\n',
     '    CHECK(h.malformed == 0, "F5: no PDU we fed was tolerance-discarded");\n'
     '    printf("PROBE F5 ends at %u ms\\n", (unsigned)h.d->now_ms_o);\n'
     '    {\n'
     '      auto nf = h.wait_frame(true, 16000, [](const std::vector<uint8_t>& fr) {\n'
     '        for (const PVec& v : parse_frame(fr).vecs) { if (v.la) return true; }\n'
     '        return false;\n'
     '      });\n'
     '      printf("PROBE next own LeaveAll after F5 at %u ms (%s)\\n",\n'
     '             (unsigned)h.d->now_ms_o, nf.empty() ? "none in 16 s" : "seen");\n'
     '    }\n'
     '  }\n'),
]


def main():
    repo, commit, work, outfile = sys.argv[1:5]
    dest = os.path.join(work, "f5c-probe")
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    data = subprocess.run(["git", "-C", repo, "archive", "--format=tar", commit],
                          check=True, capture_output=True).stdout
    with tarfile.open(fileobj=io.BytesIO(data)) as t:
        t.extractall(dest, filter="tar")
    p = os.path.join(dest, SIM)
    s = open(p, encoding="utf-8").read()
    for old, new in EDITS:
        n = s.count(old)
        if n != 1:
            raise SystemExit(f"anchor matched {n} times: {old[:50]!r}")
        s = s.replace(old, new)
    open(p, "w", encoding="utf-8").write(s)
    wrapper = os.path.join(os.path.dirname(os.path.abspath(__file__)), "verilator_capped.sh")
    os.environ.setdefault("VL_JOBS", "8")
    r = subprocess.run(["make", "-C", os.path.join(dest, "tb/srp_top"), f"VERILATOR={wrapper}"],
                       capture_output=True, text=True)
    out = [ln for ln in (r.stdout + r.stderr).splitlines()
           if ln.startswith("PROBE") or ln.startswith("FAIL") or " checks: " in ln]
    text = f"commit {commit}\nharness-only instrumentation of {SIM}; rc {r.returncode}\n" \
           + "\n".join(out) + "\n"
    open(outfile, "w").write(text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
