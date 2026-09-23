#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer receipt script: compare the Run B bytes the donor tests transcribe
with the capture itself.

Usage: compare_test_bytes.py <donor tree> <original tap-runB.pcap>

- tb/srp_decoder/sim_main.cpp test P: the 109-byte array `p` must equal the
  switch's header-stripped LeaveAll MRPDU at 47.029619 s.
- tb/srp_encoder/sim_main.cpp test L2: the three kSwitch* LeaveAll-only
  message constants (head + zero count), each followed by the AttributeList
  EndMark, plus the MRPDU EndMark, must equal the switch's LeaveAll MRPDU at
  10.429430 s after its ProtocolVersion and Domain message.
"""
import re
import sys
import importlib.util
from pathlib import Path

here = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("runb", here / "runb_msrp_check.py")
runb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runb)

tree = Path(sys.argv[1])
pcap = sys.argv[2]

pdus = {}
t0 = None
for _i, t, _off, fr in runb.records(pcap):
    if t0 is None:
        t0 = t
    m = runb.mrpdu(fr)
    if m and m[0] == "3c:c0:c6:fe:02:11":
        msgs, end = runb.walk(m[1])
        if end and any(v[0] == 1 for (_t, _a, _l, vs) in msgs for v in vs):
            pdus[round(t - t0, 6)] = m[1][:end]

fail = 0
src = (tree / "tb/srp_decoder/sim_main.cpp").read_text()
body = src.split("the_run_b_switch_leave_all_strobes_each_type_ahead_of_its_events() {", 1)[1]
arr = body.split("const std::vector<uint8_t> p = {", 1)[1].split("};", 1)[0]
arr = re.sub(r"//[^\n]*", "", arr)
p = bytes(int(x, 16) for x in re.findall(r"0x([0-9a-fA-F]{2})", arr))
cap = pdus[47.029619]
ok = p == cap
fail += not ok
print(f"decoder P: {len(p)} B transcribed, {len(cap)} B captured at 47.029619 s: "
      f"{'IDENTICAL' if ok else 'DIFFERENT'}")

src = (tree / "tb/srp_encoder/sim_main.cpp").read_text()
tail = b""
for name in ("kSwitchTalkerAdv", "kSwitchTalkerFail", "kSwitchListener"):
    m = re.search(name + r"\s*=\s*\{\{([^}]*)\}\s*,\s*(\d+)\}", src)
    head = bytes(int(x, 16) for x in re.findall(r"0x([0-9a-fA-F]{2})", m.group(1)))
    tail += head + bytes(int(m.group(2))) + b"\x00\x00"
tail += b"\x00\x00"
cap = pdus[10.42943]
dom_end = 1 + 13        # ProtocolVersion + the Domain message (4 + 2 + 4 + 1 + 2)
ok = cap[dom_end:] == tail and cap[1] == 4
fail += not ok
print(f"encoder L2: {len(tail)} B of LeaveAll-only tail vs the capture at 10.429430 s "
      f"after its Domain message: {'IDENTICAL' if ok else 'DIFFERENT'}")
sys.exit(1 if fail else 0)
