"""Export bounded startup headers from retained B12 captures.
Usage: python3 -B project_startup.py RAW_DIRECTORY OUTPUT_DIRECTORY
All reads are offline. Stream IDs and Ethernet identities are excluded.
"""
import datetime
import hashlib
import json
import struct
import sys
from pathlib import Path
from startup_decode import analyze


def digest(path):
    data = path.read_bytes()
    return dict(file=path.name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest())


def frames(path):
    with path.open("rb") as f:
        assert f.read(24)[:4] == bytes.fromhex("d4c3b2a1")
        index = 0
        while True:
            h = f.read(16)
            if not h:
                return
            assert len(h) == 16
            sec, usec, size, original = struct.unpack("<4I", h)
            data = f.read(size)
            assert len(data) == size and len(data) >= 42
            index += 1
            port, hi, lo = struct.unpack("<3I", data[8:20])
            ethernet = data[28:]
            offset = 14
            ether_type = ethernet[12:14]
            if ether_type == bytes.fromhex("8100"):
                offset = 18
                ether_type = ethernet[16:18]
            yield index, (hi << 32) | lo, port, ether_type, ethernet[offset:]


def project(raw):
    cases = []
    for cycle, kind in (("BAAF0300-2", "EARLY"), ("BAAF0900-5", "LATE"), ("BAAF0300-1", "clean control"), ("BAAF0900-4", "clean control")):
        result_path = raw / f"{cycle}-result.json"
        result = json.loads(result_path.read_text())
        events = result["events"]
        plain = raw / f"653-b12-B-AAF-{cycle}-plain.pcap"
        media = raw / f"653-b12-B-AAF-{cycle}-vlan.pcap"
        # Match the bind to the DUT talker and input selected by this cycle.
        plan = result["plan"]
        commands = [(i, t, port, a) for i, t, port, et, a in frames(plain) if et == bytes.fromhex("22f0") and a[0] == 0xfc and a[1] & 15 == 6 and a[20:28].hex() == "020000fffe000001" and int.from_bytes(a[36:38], "big") == plan["ti"] and int.from_bytes(a[38:40], "big") == plan["li"]]
        assert len(commands) == 1
        i, anchor, port, command = commands[0]
        # Neutral identifiers retain fields, lengths and match relationships.
        safe_command = bytearray(command)
        safe_command[4:12] = bytes(8)
        safe_command[12:20] = bytes.fromhex("0000000000000001")
        safe_command[20:28] = bytes.fromhex("0000000000000002")
        safe_command[28:36] = bytes.fromhex("0000000000000003")
        safe_command[40:46] = bytes(6)
        initial = []
        types = {}
        for n, t, direction, et, a in frames(media):
            types[et.hex()] = types.get(et.hex(), 0) + 1
            if t < anchor or et != bytes.fromhex("22f0") or a[0] != 2 or direction != 3:
                continue
            assert len(a) >= 24 and a[4:10].hex() == "020000000001" and int.from_bytes(a[10:12], "big") == plan["ti"]
            if len(initial) < 12:
                h = bytearray(a[:24]); h[4:12] = bytes(8)
                initial.append(dict(record=n, tap_ns=t, port=direction, avtp_header=h.hex()))
        bind = next(x for x in events if x["ev"] == "bind")
        unbind = next(x for x in events if x["ev"] == "unbind")
        polls = [dict(phase=x["phase"], send_us=x["t_cmd"], response_us=x["t_rsp"], utc=datetime.datetime.fromtimestamp(x["t_rsp"]/1e6, datetime.timezone.utc).isoformat(), status=x["status"], counters=x["counters"]) for x in events if x["ev"] == "poll"]
        callbacks = [x for x in events if x["ev"] == "hive_rule" and x.get("increments")]
        controller = dict(bind_submit_us=bind["t_cmd"], unbind_submit_us=unbind["t_cmd"], polls=polls, callback_us=callbacks[0]["t"] if callbacks else None)
        cases.append(dict(cycle=cycle, classification=kind, sources=[digest(x) for x in (plain, media, result_path)], bind_command=dict(record=i, tap_ns=anchor, port=port, acmp_header=safe_command.hex()), first_twelve_pdus=initial, media_ether_types=types, controller=controller))
    return dict(schema="b12-startup-v2", projection="Original first 24 AVTP bytes with bytes 4:12 (stream identity) zeroed. Ethernet and audio payload excluded. Bind ACMP identity fields replaced consistently by neutral tokens; all timing and status bytes preserved.", gptp_correlation=dict(status="NOT RUN", reason="Retained cycle captures select EtherType 0x22f0. No gPTP Sync/Follow_Up or measured mapping from the tap clock to gPTP time is retained. Absolute presentation lead/lag at the listener and timestamp fault ownership cannot be determined."), cycles=cases)


if __name__ == "__main__":
    raw, out = map(Path, sys.argv[1:])
    doc = project(raw)
    (out / "startup-headers.json").write_text(json.dumps(doc, indent=2) + "\n")
    (out / "startup-analysis.json").write_text(json.dumps(analyze(doc), indent=2) + "\n")
    print("Exported", len(doc["cycles"]), "cycles; 48 independently decodable headers")
