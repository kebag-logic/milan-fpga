#!/usr/bin/env python3
"""Focused disposable controls; no network, hardware or checkout writes.

Usage: python3 offline_probes.py EVIDENCE_ROOT SCRATCH_DIRECTORY
All generated captures, executables and comparator inputs stay in SCRATCH_DIRECTORY.
"""
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import sys

sys.dont_write_bytecode = True


def main():
    evidence, scratch = map(Path, sys.argv[1:])
    author = evidence / "author"
    scratch.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location("bench_wire", author / "wire.py")
    wire = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(wire)
    controller, talker, listener = (n.to_bytes(8, "big") for n in (1, 2, 3))

    def acmp(mt, seq=19, status=0):
        p = bytearray(56)
        p[0:4] = bytes([0xfc, mt, status << 3, 44])
        p[12:20], p[20:28], p[28:36] = controller, talker, listener
        p[48:50] = seq.to_bytes(2, "big")
        return bytes(p)

    def counters(mu, unsolicited=True, ctl=controller, idx=0):
        p = bytearray(160)
        p[0:4] = bytes([0xfb, 1, 0, 148])
        p[4:12], p[12:20] = listener, ctl
        p[22:24] = (0x8029 if unsolicited else 0x29).to_bytes(2, "big")
        p[24:28] = struct.pack(">HH", 5, idx)
        p[28:32] = (4095).to_bytes(4, "big")
        p[32:40] = struct.pack(">II", 1, mu)
        return bytes(p)

    def capture(name, pdus, tap=True, origin=10000000000):
        path = scratch / (name + ".pcap")
        blob = bytearray(struct.pack("<IHHIIII", 0xa1b2c3d4, 2, 4, 0, 0, 65535, 1))
        for i, p in enumerate(pdus):
            tns = origin + i * 10000
            frame = bytes(12) + bytes.fromhex("22f0") + p
            if tap:
                prefix = bytearray(28)
                struct.pack_into("<III", prefix, 8, 2, tns >> 32, tns & 0xffffffff)
                frame = prefix + frame
            sec, nsec = divmod(tns, 1000000000)
            blob += struct.pack("<IIII", sec, nsec // 1000, len(frame), len(frame)) + frame
        path.write_bytes(blob)
        return path, tap

    def grade(paths):
        return wire.analyze(paths, listener.hex(), 0, controller.hex())["wire"]

    controls = [
        ("response-first", [counters(0), acmp(8), acmp(9), counters(1)], "RESPONSE_FIRST"),
        ("reversed", [counters(0), acmp(8), counters(1), acmp(9)], "COUNTERS_FIRST"),
        ("missing-push", [counters(0), acmp(8), acmp(9)], "NO_UNLOCK_PUSH"),
        ("prior-unlock", [counters(0), counters(1), acmp(8), acmp(9)], "NO_UNLOCK_PUSH"),
        ("foreign-controller", [counters(0), acmp(8), acmp(9), counters(1, ctl=bytes(8))], "NO_UNLOCK_PUSH"),
        ("foreign-input", [counters(0), acmp(8), acmp(9), counters(1, idx=1)], "NO_UNLOCK_PUSH"),
        ("foreign-sequence", [counters(0), acmp(8), acmp(9, seq=20), counters(1)], None),
        ("solicited-baseline", [counters(0, unsolicited=False), acmp(8), acmp(9), counters(1)], "RESPONSE_FIRST"),
    ]
    for name, pdus, expected in controls:
        g = grade([capture(name, pdus)])
        observed = g["order"] if g else None
        assert observed == expected
        print(json.dumps({"control": name, "observed": observed, "expected": expected, "result": "PASS"}))
    paths = [capture("clock-one-no-push", [counters(0), acmp(8), acmp(9)], origin=20000000000),
             capture("clock-two-complete", [counters(0), acmp(8), acmp(9), counters(1)], tap=False, origin=1700000000000000000)]
    g = grade(paths)
    assert g["capture"] == "clock-two-complete.pcap" and g["response_unlock_us"] == 10
    print(json.dumps({"control": "unrelated-capture-clocks", "selected": g["capture"], "interval_us": g["response_unlock_us"], "result": "PASS"}))
    g = grade([capture("error-status", [counters(0), acmp(8), acmp(9, status=2), counters(1)])])
    assert g["status"] == 2
    print(json.dumps({"control": "response-status-preservation", "observed_status": g["status"], "result": "PASS"}))

    def stream(seq):
        return bytes([2, 0x81, seq, 0]) + talker + bytes(12)
    for name, sequence, expected in (("arbitrary-initial-sequence", [119, 120, 121], 0),
                                     ("sequence-wrap", [255, 0, 1], 0),
                                     ("missing-sequence", [119, 121], 1),
                                     ("repeated-sequence", [119, 119], 1)):
        path = capture(name, [stream(n) for n in sequence])
        analyzed = wire.analyze([path], listener.hex(), 0, controller.hex())
        gaps = sum(x["gaps"] for x in analyzed["streams"])
        assert gaps == expected
        print(json.dumps({"control": name, "observed_gaps": gaps, "expected_gaps": expected, "result": "PASS"}))

    rule = (author / "rule_controls.cpp").read_text()
    start = rule.index("static std::string errorUpdate")
    end = rule.index("\nclass Obs") if "\nclass Obs" in rule else rule.index("\n\n\nint main")
    function = rule[start:end].strip()
    for filename in ("probe.cpp", "probe_phase.cpp"):
        text = (author / filename).read_text()
        assert function == text[text.index("static std::string errorUpdate"):text.index("\nclass Obs")].strip()
    print(json.dumps({"rule_controls_use_actual_probe_function": True}))
    for name, code, expected in (("rule-original", rule, 0),
                                 ("rule-inverted", rule.replace('conn=="Connected"', 'conn!="Connected"'), 1)):
        src, binary = scratch / (name + ".cpp"), scratch / name
        src.write_text(code)
        subprocess.run(["c++", "-std=c++17", "-pthread", str(src), "-o", str(binary)], check=True, timeout=60, capture_output=True)
        r = subprocess.run([str(binary)], capture_output=True, text=True, timeout=15)
        assert r.returncode == expected
        print(json.dumps({"control": name, "exit": r.returncode, "expected_exit": expected, "stdout": r.stdout.strip(), "result": "PASS"}))

    # Execute the published comparator unchanged except for its scratch input root.
    source = (author / "restore_compare.py").read_text()
    fixture = scratch / "restore-inputs"
    fixture.mkdir(exist_ok=True)
    adapted = source.replace("RAW=Path('/tmp/653-b12/raw')", "RAW=Path(" + repr(str(fixture)) + ")")
    assert adapted != source
    comparator = scratch / "restore_compare.py"
    comparator.write_text(adapted)
    def rows(status=0):
        values = []
        for role, nb, nf, nm, nc in (("dut", 4, 4, 2, 2), ("peer", 14, 14, 2, 1)):
            for i in range(nb):
                values.append({"role": role, "what": f"rx-state-{role}-{i}", "status": status, "conn_count": 0})
            for cmd, count, payload in (("GET_STREAM_FORMAT", nf, "000000000205022001006000"),
                                        ("GET_AUDIO_MAP", nm, "0000000000000000"),
                                        ("GET_CLOCK_SOURCE", nc, "000000000001")):
                for i in range(count):
                    values.append({"role": role, "what": f"{cmd}-{role}-{i}", "cmd": cmd, "status": status, "payload": payload})
        return values
    good = rows()
    changed = json.loads(json.dumps(good))
    changed[4]["payload"] = "000000000205022002006000"
    cases = (("equal-success", good, good, 0),
             ("changed-format", good, changed, 1),
             ("equal-failed-readbacks", rows(status=1), rows(status=1), 0),
             ("empty-readbacks", [], [], 0))
    for name, before, after, actual_expected in cases:
        for phase, contents in (("start", before), ("end", after)):
            for stem in ("census", "peer-descs", "dut-descs"):
                data = contents if stem == "census" else []
                (fixture / f"{stem}-{phase}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in data))
        r = subprocess.run([sys.executable, str(comparator)], capture_output=True, text=True, timeout=15)
        observed = json.loads(r.stdout)
        assert r.returncode == actual_expected
        print(json.dumps({"control": name, "exit": r.returncode,
                          "pass_restore": observed["pass_restore"],
                          "observation_count": sum(x["observations"] for x in observed["rows"]),
                          "evaluation": "DEFECT: invalid evidence accepted" if name in ("equal-failed-readbacks", "empty-readbacks") else "PASS"}))


if __name__ == "__main__":
    main()
