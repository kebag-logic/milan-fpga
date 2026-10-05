"""Validate the complete B12 effective-state inventory before comparing it.

Usage: python3 restore_compare.py restore-start.json restore-end.json
No device access. Inputs are role-safe projections of retained responses.
"""
import hashlib
import json
import sys
from pathlib import Path


def inventory():
    expected = {}
    for role, inputs, outputs in (("dut", 2, 2), ("peer", 10, 4)):
        for kind, dt, count in (("rx", 5, inputs), ("tx", 6, outputs)):
            for idx in range(count):
                expected[f"{kind}-state-{role}-{idx}"] = (role, "bindings", "GET_RX_STATE" if kind == "rx" else "GET_TX_STATE", dt, idx)
                expected[f"format-{role}-{dt}-{idx}"] = (role, "formats", "GET_STREAM_FORMAT", dt, idx)
        for dt in (14, 15):
            expected[f"map-{role}-0x{dt:04x}-0-0"] = (role, "maps", "GET_AUDIO_MAP", dt, 0)
        expected[f"census-clock-{role}"] = (role, "clocks", "GET_CLOCK_SOURCE", 36, 0)
    expected["clock-dut"] = ("dut", "clocks", "GET_CLOCK_SOURCE", 36, 0)
    assert len(expected) == 43
    return expected


def require(condition, message):
    if not condition:
        raise ValueError(message)


def uint(value, bits=16):
    return type(value) is int and 0 <= value < (1 << bits)


def validate(doc, endpoint):
    require(type(doc) is dict and doc.get("schema") == "b12-restore-v2", "invalid schema")
    require(doc.get("endpoint") == endpoint, "wrong endpoint")
    records = doc.get("observations")
    require(type(records) is list and len(records) == 43, "expected 43 observations")
    expected, found = inventory(), {}
    for row in records:
        require(type(row) is dict, "malformed observation")
        key = row.get("observation")
        require(type(key) is str and key in expected, "unexpected observation")
        require(key not in found, "duplicate observation: " + key)
        role, cat, cmd, dt, idx = expected[key]
        require((row.get("role"), row.get("category"), row.get("command"), row.get("descriptor_type"), row.get("descriptor_index")) == expected[key], "wrong descriptor identity: " + key)
        require(type(row["descriptor_type"]) is int and type(row["descriptor_index"]) is int, "invalid descriptor identity")
        status = row.get("status")
        require((type(status) is int and status == 0) if cat == "bindings" else status == "SUCCESS", "unsuccessful response: " + key)
        val = row.get("value")
        require(type(val) is dict, "missing effective value: " + key)
        if cat == "bindings":
            require(set(val) == {"connections"} and uint(val["connections"]), "invalid binding: " + key)
        elif cat == "formats":
            require(set(val) == {"format"} and type(val["format"]) is str, "missing format: " + key)
            require(len(val["format"]) == 16 and all(c in "0123456789abcdef" for c in val["format"]), "truncated or malformed format: " + key)
        elif cat == "clocks":
            require(set(val) == {"source"} and uint(val["source"]), "invalid source: " + key)
        else:
            require(set(val) == {"map_index", "number_of_maps", "number_of_mappings", "mappings"}, "incomplete map: " + key)
            require(val["map_index"] == 0 and type(val["map_index"]) is int, "unexpected map page")
            require(val["number_of_maps"] == 1 and type(val["number_of_maps"]) is int, "incomplete map pages")
            require(uint(val["number_of_mappings"]) and type(val["mappings"]) is list and len(val["mappings"]) == val["number_of_mappings"], "truncated map")
            for mapping in val["mappings"]:
                require(type(mapping) is list and len(mapping) == 4 and all(uint(x) for x in mapping), "malformed mapping")
        found[key] = {k: row[k] for k in ("role", "category", "command", "descriptor_type", "descriptor_index", "status", "value")}
    require(set(found) == set(expected), "missing observation")
    require(found["clock-dut"]["value"] == found["census-clock-dut"]["value"], "conflicting source observations")
    return found


def compare(start, end):
    before, after = validate(start, "start"), validate(end, "end")
    require(before == after, "effective state changed")
    require(all(r["value"]["connections"] == 0 for r in before.values() if r["category"] == "bindings"), "bindings remain")
    rows = []
    for role in ("dut", "peer"):
        for cat in ("bindings", "formats", "maps", "clocks"):
            def group(pop):
                return {k: v for k, v in pop.items() if v["role"] == role and v["category"] == cat}
            a, b = group(before), group(after)
            digest = lambda x: hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            rows.append(dict(role=role, category=cat, observations=len(a), all_success=True, equal=a == b, start_sha256=digest(a), end_sha256=digest(b)))
    return dict(pass_restore=True, expected_observations=43, all_streams_unbound=True, rows=rows)


def main():
    try:
        require(len(sys.argv) == 3, "provide start and end projections")
        result = compare(*(json.loads(Path(p).read_text()) for p in sys.argv[1:]))
    except (ValueError, TypeError, KeyError, OSError) as exc:
        print(json.dumps(dict(pass_restore=False, reason=str(exc)), indent=2))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
