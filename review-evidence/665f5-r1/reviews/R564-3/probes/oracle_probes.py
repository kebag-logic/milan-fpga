# Reviewer probes of the round-3 wire oracle change (PR #700).
# Usage: python3 -I -B oracle_probes.py <repo-root> <wire-output-dir> <scratch-dir>
# Grades the recorded wire log with the head oracle (baseline), with the head oracle on
# planted observation edits, and with the pre-round-3 latency expectation restored.
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

OLD_RULE = ('        assert number(reply, 62, 4) == (67890 if status else number(request, 62, 4)), '
            '"SET requested or current latency"\n')
NEW_BLOCK_START = "        requested_latency = number(request, 62, 4)\n"
NEW_BLOCK_END = '        assert number(reply, 62, 4) == expected_latency, "SET requested or current latency"\n'


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def grade(oracle, rows, descriptors):
    try:
        oracle.grade(rows, descriptors)
    except AssertionError as error:
        return f"REJECT: {error}"
    return "ACCEPT"


def main() -> int:
    repo, wire, scratch = (Path(p).resolve() for p in sys.argv[1:4])
    scratch.mkdir(parents=True, exist_ok=True)
    source = repo / "sw/firmware/ctrl/test/aecp_wire_oracle.py"
    head = load(source, "oracle_head")
    text = source.read_text()
    start, end = text.index(NEW_BLOCK_START), text.index(NEW_BLOCK_END) + len(NEW_BLOCK_END)
    (scratch / "oracle_old_rule.py").write_text(text[:start] + OLD_RULE + text[end:])
    old = load(scratch / "oracle_old_rule.py", "oracle_old")
    results = {}
    failures = 0
    for log in sorted(wire.glob("wire-if*.log")):
        rows = [json.loads(line[5:]) for line in log.read_text().splitlines() if line.startswith("WIRE ")]
        descriptors = head.image_rows(wire / "aecp_entity_gen.h")
        n = head.number

        def req(r):
            return bytes.fromhex(r["request"])

        def set_rows(rs, pred):
            return [r for r in rs if r["kind"] == "command" and n(req(r), 36) == 14 and pred(n(req(r), 42, 4))]

        nosub = set_rows(rows, lambda f: not f & 0x20000000)
        withsub = set_rows(rows, lambda f: f & 0x20000000 and f != 0x60000000)
        census = {"set_rows": len(set_rows(rows, lambda f: True)), "nosub_rows": len(nosub),
                  "nosub_request_latency": [n(req(r), 62, 4) for r in nosub],
                  "nosub_core_latency": [n(bytes.fromhex(r["core"][0]), 62, 4) for r in nosub]}

        def plant(edit):
            import copy
            mutant = copy.deepcopy(rows)
            edit(mutant)
            return mutant

        def edit_core(pred_rows, offset, value, size=4):
            def f(m):
                r = pred_rows(m)[0]
                frame = bytearray.fromhex(r["core"][0])
                frame[offset:offset + size] = value.to_bytes(size, "big")
                r["core"][0] = frame.hex()
            return f

        def edit_request_latency(value):
            def f(m):
                r = set_rows(m, lambda fl: not fl & 0x20000000)[0]
                frame = bytearray.fromhex(r["request"])
                frame[62:66] = value.to_bytes(4, "big")
                r["request"] = frame.hex()
            return f

        def echo(m):
            r = set_rows(m, lambda fl: not fl & 0x20000000)[0]
            frame = bytearray.fromhex(r["core"][0])
            frame[62:66] = bytes.fromhex(r["request"])[62:66]
            r["core"][0] = frame.hex()

        def flag_set(m):
            r = set_rows(m, lambda fl: not fl & 0x20000000)[0]
            frame = bytearray.fromhex(r["core"][0])
            frame[42] |= 0x20
            r["core"][0] = frame.hex()

        cases = {
            "baseline/head-oracle": (head, rows, "ACCEPT"),
            "baseline/pre-round3-rule": (old, rows, "REJECT: SET requested or current latency"),
            "nosub-core-echoes-request": (head, plant(echo), "REJECT: SET requested or current latency"),
            "nosub-core-latency-off-by-one": (head, plant(edit_core(
                lambda m: set_rows(m, lambda fl: not fl & 0x20000000), 62, 67891)),
                "REJECT: SET requested or current latency"),
            "nosub-core-sets-latency-valid": (head, plant(flag_set), "REJECT: SET response validity"),
            "subcommand-core-latency-not-echoed": (head, plant(edit_core(
                lambda m: set_rows(m, lambda fl: fl & 0x20000000 and fl != 0x60000000), 62, 67891)),
                "REJECT: SET requested or current latency"),
            "nosub-stimulus-equals-current": (head, plant(edit_request_latency(67890)),
                                              "REJECT: no-subcommand stimulus distinguishes current latency"),
        }
        out = {"census": census}
        for name, (oracle, rs, expected) in cases.items():
            got = grade(oracle, rs, descriptors)
            ok = got == expected
            failures += not ok
            out[name] = {"expected": expected, "observed": got, "ok": ok}
            print(f"[{'ok' if ok else 'FAIL'}] {log.parent.name}/{log.name} {name}: {got}")
        results[f"{log.parent.name}/{log.name}"] = out
    (scratch / "oracle_probes.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({k: v["census"] for k, v in results.items()}, indent=1))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
