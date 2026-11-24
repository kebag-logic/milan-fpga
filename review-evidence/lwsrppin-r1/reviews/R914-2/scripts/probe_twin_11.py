#!/usr/bin/env python3
"""Independent table, capacity and self-test census probes; no checkout writes."""
from pathlib import Path
import sys
import types

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "tb/verilator/milan_dp"))
import twin_mrp as m

src = Path(m.__file__).read_text()
calls = []
def record(frame, event, arg):
    if event == "call" and frame.f_code.co_name == "check" and frame.f_code.co_filename == m.__file__:
        calls.append(frame.f_locals["name"])
sys.setprofile(record)
failed = m.selftest()
sys.setprofile(None)
print("selftest failures:", failed)
print("actual named checks:", len(calls), calls)
print("advertised success:", [line.strip() for line in src.splitlines() if "OK (10 checks)" in line])
assert len(calls) == len(set(calls)) == 11

expected = dict(zip(m.STATES, "LO VP VN VN VP VP LO LO LO VP VP LO".split()))
count = 0
for application in ("MSRP", "MVRP"):
    part = m.Participant(application, m.REGISTRAR[application], True)
    for state in m.STATES:
        for registrar in m.REGISTRARS:
            normal = m.opportunity(True, (state, registrar), part)
            full = m.opportunity(True, (state, registrar), part, True)
            omitted = (None, (expected[state], "LV" if registrar == "IN" else registrar))
            assert full == normal + [omitted]
            assert m.opportunity(False, (state, registrar), part, True) == m.transmit(False, (state, registrar), part)
            count += 1
print("table probes:", count, "Applicant/Registrar/application combinations passed")
assert [m.vector_octets("MSRP", k) for k in (1, 2, 3, 4)] == [28, 37, 12, 7]
assert m.vector_octets("MVRP", 1) == 5
print("independent minimum vectors: MSRP 28/37/12/7, MVRP 5")

# Exercise the real decoder-to-observation path, including MAC padding.
header = bytes(12) + bytes.fromhex("88f5")
first = m.Sent(0, header + bytes.fromhex("000102000100016c00000000"), 14)
for n, expected_full in ((297, False), (298, True)):
    vectors = b"".join((0x2001 if k == 0 else 1).to_bytes(2, "big") +
                       (1000+k).to_bytes(2, "big") + bytes([108]) for k in range(n))
    frame = m.Sent(1000, header + bytes.fromhex("000102") + vectors + bytes(4) + bytes(20), 14)
    cap = m.Capture("split", 2000, {}, [], {"MVRP": [first, frame]}, -1)
    seen = m.observations(cap, "MVRP")[(1, "0001")][-1]
    assert seen.sent is None and seen.leave_all and seen.full == expected_full
    assert m.mrpdu_octets("MVRP", frame) == 7 + 5*n
    print("decoded omission:", 7 + 5*n, "octets; full=", seen.full)

mutations = {
    "drop-txlaf": ("if leave_all and full:", "if False:"),
    "drop-listener-fourpacked": ('(1 if application == "MSRP" and kind == 3 else 0)', "0"),
    "capacity-off-by-one": ("MRPDU_ROOM = 1500", "MRPDU_ROOM = 1499"),
    "mvrp-endmark-missing": ("return offset + 2 - s.at", "return offset - s.at"),
    "extra-applicant-rla": ("outcomes = transmit(leave_all, config, part)",
        'outcomes = [(sent, step("rLA!", moved, part)) for sent, moved in transmit(leave_all, config, part)] if leave_all else transmit(False, config, part)'),
}
for name, (before, after) in mutations.items():
    assert src.count(before) == 1
    module = types.ModuleType("probe_" + name.replace("-", "_"))
    sys.modules[module.__name__] = module
    exec(compile(src.replace(before, after), name, "exec"), module.__dict__)
    failures = module.selftest()
    print("mutation", name, "caught by", failures)
    assert failures
print("five independent grade mutations caught")
