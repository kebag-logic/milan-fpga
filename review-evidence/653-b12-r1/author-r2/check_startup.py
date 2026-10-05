"""Recompute startup receipts and exercise header bit/rollover controls.
Usage: python3 -B check_startup.py PACKET_DIRECTORY
"""
import copy
import csv
import json
import sys
from pathlib import Path
from startup_decode import analyze, delta32, header

p = Path(sys.argv[1])
doc = json.loads((p / "startup-headers.json").read_text())
result = analyze(doc)
assert result == json.loads((p / "startup-analysis.json").read_text())
old = {r["cycle"]: r for f in p.glob("wire-receipts-*.json") for r in json.loads(f.read_text())}
polls = list(csv.DictReader((p / "short-polls.csv").open()))
expected = {
    "BAAF0300-2": (3644145645, 3620532816, -23612829, 20227033, 29880, 278656, 318532),
    "BAAF0900-5": (289243013, 810612109, 521369096, 20407250, 29947, 878672, 418654),
    "BAAF0300-1": (3452644691, 3452769690, 124999, 222566994),
    "BAAF0900-4": (3685205858, 3685330857, 124999, 20091409),
}
for r in result["cycles"]:
    name = r["cycle"]
    first = r["decoded"]
    a, b, step, interval, *times = expected[name]
    assert first[0]["avtp_timestamp"] == a and first[1]["avtp_timestamp"] == b
    assert r["timestamp_steps_ns"][0] == step and r["bind_to_first_pdu_tap_ns"] == interval
    assert r["sequence_consecutive"]
    assert all(x["tv"] == 1 and x["tu"] == x["mr"] == x["sp"] == x["version"] == 0 and x["sv"] == 1 for x in first)
    assert all(124999 <= x <= 125020 for x in r["timestamp_steps_ns"][1:])
    assert [(x["record"], x["tap_ns"], x["sequence"]) for x in first] == [(x["i"], x["tns"], x["seq"]) for x in old[name]["first_twelve_pdus"]]
    if times:
        assert [r[k] for k in ("bind_submit_to_nonzero_us", "nonzero_to_unbind_submit_us", "nonzero_to_callback_us")] == times
        actual = next(x for x in polls if x["cycle"] == name and x["phase"] != "pre-bind" and (int(x["EARLY"]) or int(x["LATE"])))
        assert int(actual["response_us"]) == r["first_nonzero"]["response_us"]
        assert actual["utc"] == r["first_nonzero"]["utc"]
        assert float(actual["since_bind_command_ms"]) * 1000 == times[0]
controls = []
base = bytearray.fromhex(doc["cycles"][0]["first_twelve_pdus"][0]["avtp_header"])
for field, offset, mask, expected_value in (("tv", 1, 1, 0), ("tu", 3, 1, 1), ("mr", 1, 8, 1), ("sp", 22, 16, 1)):
    h = base.copy(); h[offset] ^= mask
    assert header(h.hex())[field] == expected_value
    controls.append(field + " bit change detected")
assert delta32(20, 0xfffffff0) == 36
assert delta32(0xfffffff0, 20) == -36
controls += ["forward timestamp rollover", "reverse timestamp rollover"]
try:
    header(base[:-1].hex())
except ValueError:
    controls.append("truncated header rejected")
else:
    raise AssertionError("truncated header accepted")
mutant = copy.deepcopy(doc)
h = bytearray.fromhex(mutant["cycles"][0]["first_twelve_pdus"][0]["avtp_header"])
h[12:16] = (3620532816 - 125000).to_bytes(4, "big")
mutant["cycles"][0]["first_twelve_pdus"][0]["avtp_header"] = h.hex()
assert analyze(mutant)["cycles"][0]["timestamp_steps_ns"][0] != expected["BAAF0300-2"][2]
controls.append("planted regular timestamp removes measured discontinuity")
print(json.dumps(dict(passed=True, cycles=4, headers=48, original_first_pdu_receipts_matched=48, earliest_nonzero_polls_matched=2, controls=controls), indent=2))
