"""Project retained protocol readbacks without entity or transport identities.

Usage: python3 project_restore.py RAW_DIRECTORY OUTPUT_DIRECTORY
Only local files are read. Source hashes bind the projection to retained files.
"""
import hashlib
import json
import re
import struct
import sys
from pathlib import Path
from restore_compare import inventory, validate


def project(raw, endpoint):
    observations, sources = [], []
    for stem in ("census", "dut-descs", "peer-descs"):
        path = raw / f"{stem}-{endpoint}.jsonl"
        data = path.read_bytes()
        sources.append(dict(file=path.name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
        for line, text in enumerate(data.decode().splitlines(), 1):
            row = json.loads(text)
            what = row.get("what", "")
            role = row.get("role")
            if what.startswith(("rx-state-", "tx-state-")):
                role = what.split("-")[2]
                key = what
                value = dict(connections=row["conn_count"])
                expected_index = inventory()[key][4]
                assert row["listener_uid" if what.startswith("rx-") else "talker_uid"] == expected_index
                # No effective binding exists at count zero. Endpoint IDs and
                # stale transport fields are intentionally not exported.
            elif row.get("cmd") in ("GET_STREAM_FORMAT", "GET_CLOCK_SOURCE", "GET_AUDIO_MAP"):
                key = f"census-clock-{role}" if what == "clock" else what
                if key not in inventory():
                    continue
                payload = bytes.fromhex(row["payload"])
                assert len(payload) >= 4
                dt, idx = struct.unpack(">HH", payload[:4])
                expected = inventory()[key]
                assert (dt, idx) == expected[3:]
                if row["cmd"] == "GET_STREAM_FORMAT":
                    assert len(payload) == 12
                    value = dict(format=payload[4:12].hex())
                elif row["cmd"] == "GET_CLOCK_SOURCE":
                    assert len(payload) == 8
                    value = dict(source=int.from_bytes(payload[4:6], "big"))
                else:
                    assert len(payload) >= 12
                    page, pages, count = struct.unpack(">HHH", payload[4:10])
                    assert len(payload) == 12 + 8 * count
                    value = dict(map_index=page, number_of_maps=pages, number_of_mappings=count, mappings=[list(struct.unpack(">4H", payload[i:i+8])) for i in range(12, len(payload), 8)])
            else:
                continue
            expected = inventory()[key]
            assert role == expected[0]
            observations.append(dict(observation=key, role=role, category=expected[1], command=expected[2], descriptor_type=expected[3], descriptor_index=expected[4], status=row["status"], value=value, source_file=path.name, source_line=line))
    doc = dict(schema="b12-restore-v2", endpoint=endpoint, sources=sources, projection="Complete effective values for the 43 assigned observations. Entity, controller, transport and descriptor-name identities omitted; reserved bytes excluded. No effective value or response status redacted.", observations=observations)
    validate(doc, endpoint)
    return doc


if __name__ == "__main__":
    raw, out = map(Path, sys.argv[1:])
    for endpoint in ("start", "end"):
        doc = project(raw, endpoint)
        (out / f"restore-{endpoint}.json").write_text(json.dumps(doc, indent=2) + "\n")
        print(endpoint, len(doc["observations"]), "successful observations")
