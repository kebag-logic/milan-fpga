"""Decode sanitized 24-byte AAF headers and startup timing receipts.

Usage: python3 -B startup_decode.py startup-headers.json
The tap and controller clocks remain independent. No device access.
"""
import json
import sys
from pathlib import Path


def header(h):
    a = bytes.fromhex(h)
    if len(a) != 24 or a[0] != 2 or a[4:12] != bytes(8):
        raise ValueError("expected sanitized 24-byte AAF header")
    return dict(sequence=a[2], tv=a[1] & 1, tu=a[3] & 1, mr=(a[1] >> 3) & 1, sv=a[1] >> 7, version=(a[1] >> 4) & 7, avtp_timestamp=int.from_bytes(a[12:16], "big"), sp=(a[22] >> 4) & 1)


def delta32(new, old):
    return ((new - old + (1 << 31)) % (1 << 32)) - (1 << 31)


def analyze(doc):
    out = []
    for case in doc["cycles"]:
        frames = case["first_twelve_pdus"]
        if len(frames) != 12:
            raise ValueError("expected twelve headers")
        decoded = [dict(record=f["record"], tap_ns=f["tap_ns"], **header(f["avtp_header"])) for f in frames]
        # Header steps only. Never subtract AVTP time from a tap timestamp.
        steps = [delta32(b["avtp_timestamp"], a["avtp_timestamp"]) for a, b in zip(decoded, decoded[1:])]
        gaps = [b["tap_ns"] - a["tap_ns"] for a, b in zip(decoded, decoded[1:])]
        c = case["controller"]
        polls = c["polls"]
        nonzero = [x for x in polls if x["phase"] != "pre-bind" and (x["counters"]["EARLY"] or x["counters"]["LATE"])]
        first = nonzero[0] if nonzero else None
        row = dict(cycle=case["cycle"], classification=case["classification"], decoded=decoded, sequence_consecutive=all(b["sequence"] == (a["sequence"] + 1) % 256 for a, b in zip(decoded, decoded[1:])), timestamp_steps_ns=steps, tap_spacing_ns=gaps, bind_to_first_pdu_tap_ns=decoded[0]["tap_ns"]-case["bind_command"]["tap_ns"], first_nonzero=first, gptp_correlation="NOT RUN", correlation_reason=doc["gptp_correlation"]["reason"])
        if first:
            row.update(bind_submit_to_nonzero_us=first["response_us"]-c["bind_submit_us"], nonzero_to_unbind_submit_us=c["unbind_submit_us"]-first["response_us"], nonzero_to_callback_us=c["callback_us"]-first["response_us"])
        out.append(row)
    return dict(cycles=out)


if __name__ == "__main__":
    print(json.dumps(analyze(json.loads(Path(sys.argv[1]).read_text())), indent=2))
