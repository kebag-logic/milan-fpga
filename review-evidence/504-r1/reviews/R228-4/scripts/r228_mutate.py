#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""R228-3 reviewer-owned mutation probes: does a control FAIL when one
load-bearing part of the change is reverted?

Usage: r228_mutate.py <disposable-tree> <mutation-id> <out-dir> [--sdk <prefix>]

Applies exactly one textual mutation (each anchor must match exactly once)
to a DISPOSABLE copy of the tree, runs the named control, records the exit
status and the first failure line, then restores the original bytes and
verifies their SHA-256. `literal` mutants stop gate 1b right after its
literal-assembly resolver controls, which run on every machine; `gate1b`
mutants run the whole gate 1b with the mapped SDK; `installer` and `audit`
mutants run the installer self-test and the compiler-audit self-test.
A mutant is KILLED when its control exits non-zero for a reason other than
the stop hook, and SURVIVES when the control still passes.
"""

import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

BUILDER = "sw/builder/test_builder.py"
INSTALLER = "scripts/ci_rv32_sdk.py"
AUDIT = "sw/builder/test_firmware_compiler.py"
STOP_ANCHOR = 'f"but stopped at {len(mirror_stops)} non-integer rewrites of it")\n'
STOP_HOOK = (STOP_ANCHOR +
             '    if os.environ.get("R228_STOP_AFTER_LITERALS"):\n'
             '        print("R228-LITERAL-CONTROLS-PASSED", flush=True)\n'
             '        raise SystemExit(0)\n')

#: id -> (kind, file, old, new, what the mutation reverts)
MUTATIONS = {
    "null-literal": ("literal", BUILDER, "RV32_MASK = 0xFFFF_FFFF\n",
                     "RV32_MASK = 0xFFFF_FFFF\n", "no change: stop hook only"),
    "null-installer": ("installer", INSTALLER, 'INSTALLER_REVISION = 1\n',
                       'INSTALLER_REVISION = 1\n', "no change"),
    "fp-classes": ("literal", BUILDER,
                   '"fsh": 2, "fsw": 4, "fsd": 8, "fsq": 16}', '}',
                   "FP store classes dropped from RV32_STORE_BYTES"),
    "atomic-classes": ("literal", BUILDER,
                       'r"^(?:amo(?:swap|add|xor|and|or|min|max|minu|maxu)|sc)\\.w"',
                       'r"^(?!)(?:amo(?:swap|add|xor|and|or|min|max|minu|maxu)|sc)\\.w"',
                       "AMO/SC no longer store classes"),
    "other-loads": ("literal", BUILDER,
                    'r"^(?:fl[hwdq]|lr\\.w(?:\\.(?:aq|rl|aqrl))?)$"',
                    'r"^(?!)(?:fl[hwdq]|lr\\.w(?:\\.(?:aq|rl|aqrl))?)$"',
                    "FP loads and LR no longer recognised as loads"),
    "unclassified-default": ("literal", BUILDER,
                             '    if rv32_memory_operand(args) and not rv32_is_load(mnem):\n'
                             '        _rv32_forget_symbols(state)\n'
                             '        return ("store", (Rv32Where("unclassified"',
                             '    if False:\n'
                             '        _rv32_forget_symbols(state)\n'
                             '        return ("store", (Rv32Where("unclassified"',
                             "class fail-closed default removed"),
    "memop-displacement": ("literal", BUILDER,
                           'RV32_MEM_BASE_RE = re.compile(r"\\(\\s*([a-z0-9]+)\\s*\\)$")',
                           'RV32_MEM_BASE_RE = re.compile(r"-?\\d+\\(\\s*([a-z0-9]+)\\s*\\)$")',
                           "memory operand must carry a numeric displacement"),
    "mirror-integer-only": ("literal", BUILDER,
                            '        if rv32_store_bytes(mnem) is not None or \\\n'
                            '                (rv32_memory_operand(args) and not rv32_is_load(mnem)) or \\\n',
                            '        if mnem in ("sw", "sh", "sb") or \\\n',
                            "mirror stops only at integer stores (base behaviour)"),
    "mirror-no-memop": ("literal", BUILDER,
                        '                (rv32_memory_operand(args) and not rv32_is_load(mnem)) or \\\n'
                        '                mnem in ("call"',
                        '                mnem in ("call"',
                        "mirror ignores unclassified memory writers"),
    "footprint-first-byte": ("literal", BUILDER,
                             '    return [address & RV32_MASK] + [word & RV32_MASK for word in further]',
                             '    return [address & RV32_MASK]',
                             "store judged at its first byte only"),
    "range-footprint": ("literal", BUILDER,
                        'held.hi + offset + width - 1)', 'held.hi + offset)',
                        "ranged store judged by first bytes only"),
    "sym-overlap": ("literal", BUILDER,
                    '            _rv32_forget_overlap(state.mem, ("sym", held.name), at, width)\n',
                    '', "static words overlapped by a store are not forgotten"),
    "frame-overlap": ("literal", BUILDER,
                      '            _rv32_forget_overlap(state.mem, (base,), offset, width)\n',
                      '', "frame words overlapped by a store are not forgotten"),
    "value-all-classes": ("literal", BUILDER,
                          '    if mnem == "sw" or mnem.startswith("amoswap."):\n'
                          '        return state.get(args[-2])\n    return None',
                          '    return state.get(args[-2])',
                          "every store class leaves its rs2 as the word"),
    "value-subword": ("literal", BUILDER,
                      '    if mnem == "sw" or mnem.startswith("amoswap."):',
                      '    if mnem in ("sw", "sh", "sb") or mnem.startswith("amoswap."):',
                      "sub-word stores leave their rs2 as the word (R227-2-F1 root)"),
    "value-amo-sc": ("literal", BUILDER,
                     '    if mnem == "sw" or mnem.startswith("amoswap."):',
                     '    if mnem == "sw" or mnem.startswith(("amo", "sc.")):',
                     "every AMO and SC leave rs2 as the word (R227-2-F2 root)"),
    "stack-forget-frame": ("literal", BUILDER,
                           '            _rv32_forget_frame(state)\n'
                           '            return ("store", (Rv32Where("stack"), value))',
                           '            return ("store", (Rv32Where("stack"), value))',
                           "store through a stack pointer keeps frame slots"),
    "atomic-rd": ("literal", BUILDER,
                  '            #: the value are read, because `amoswap.w a5,a5,0(a4)` is the\n'
                  '            #: ordinary spelling.\n'
                  '            state.set(args[0], None)\n',
                  '            #: the value are read, because `amoswap.w a5,a5,0(a4)` is the\n'
                  '            #: ordinary spelling.\n            pass\n',
                  "AMO/SC rd keeps its previous value"),
    "atomic-operand": ("literal", BUILDER,
                       '        place = RV32_MEM_RE.match(args[-1]) \\\n'
                       '            if len(args) == (3 if atomic else 2) else None',
                       '        place = RV32_MEM_RE.match(args[1]) \\\n'
                       '            if len(args) == 2 else None',
                       "atomic memory operand read at position 2"),
    "sym-overlap-width-4": ("literal", BUILDER,
                            '_rv32_forget_overlap(state.mem, ("sym", held.name), at, width)',
                            '_rv32_forget_overlap(state.mem, ("sym", held.name), at, 4)',
                            "static overlap judged over 4 bytes whatever the width (R228-F4 RM11)"),
    "frame-overlap-width-4": ("literal", BUILDER,
                              '_rv32_forget_overlap(state.mem, (base,), offset, width)',
                              '_rv32_forget_overlap(state.mem, (base,), offset, 4)',
                              "frame overlap judged over 4 bytes whatever the width (RM12)"),
    "overlap-last-byte": ("literal", BUILDER,
                          'key[-1] + 3 >= start]', 'key[-1] + 3 > start]',
                          "a store at a word's LAST byte leaves the word"),
    "overlap-first-byte": ("literal", BUILDER,
                           'key[-1] <= start + width - 1 and', 'key[-1] < start + width - 1 and',
                           "a word starting at the store's last byte is kept"),
    "stores-first-word": ("literal", BUILDER,
                          '                seen["stores"].extend((block, word) for word in payload)',
                          '                seen["stores"].append((block, payload[0]))',
                          "multi-word store reported at its first word only"),
    "census-isa-parse": ("gate1b", BUILDER,
                         'census_isa = set(re.findall(r"(?:^rv32|_)([a-z][a-z0-9]*?)\\d+p\\d+",\n'
                         '                                census_arch))',
                         'census_isa = set(re.findall(r"(?:^rv64|_)([A-Z][a-z0-9]*?)\\d+p\\d+",\n'
                         '                                census_arch))',
                         "census ISA mis-parsed: atomic compiled mutants silently skipped"),
    "overlap-last-byte-gate1b": ("gate1b", BUILDER,
                                 'key[-1] + 3 >= start]', 'key[-1] + 3 > start]',
                                 "overlap boundary at a word's last byte, whole gate"),
    "require-adoption": ("audit", BUILDER,
                         '        assert census_used["compiler"] == census_compilers[0], \\\n',
                         '        assert True or census_used["compiler"] == census_compilers[0], \\\n',
                         "--require-rv32 accepts an alternate compiler"),
    "require-instruments": ("audit", BUILDER,
                            '        assert not instruments_down, \\\n'
                            '            "--require-rv32: the hosted firmware instruments must run"',
                            '        assert True or not instruments_down, \\\n'
                            '            "--require-rv32: the hosted firmware instruments must run"',
                            "--require-rv32 accepts absent instruments"),
    "download-digest": ("installer", INSTALLER,
                        '    if actual != ARCHIVE_SHA256:\n'
                        '        raise ValueError(f"SDK archive digest mismatch: {actual}")',
                        '    if False:\n'
                        '        raise ValueError(f"SDK archive digest mismatch: {actual}")',
                        "download path extracts without the digest check (R228-1 F2 root)"),
    "digest-prefix": ("installer", INSTALLER,
                      '    if actual != ARCHIVE_SHA256:',
                      '    if actual[:63] != ARCHIVE_SHA256[:63]:',
                      "digest compared on a prefix only"),
    "provenance-drop-destination": ("installer", INSTALLER,
                                    ', "destination": str(destination)}', '}',
                                    "receipt no longer binds the destination (R228-1 F3 root)"),
    "provenance-drop-host": ("installer", INSTALLER,
                             '"host": host_identity(), ', '',
                             "receipt no longer binds the host (R228-1 F3 root)"),
    "installer-digest-constant": ("installer", INSTALLER,
                                  '"installer_sha256": digest(Path(__file__).resolve()),',
                                  '"installer_sha256": "0" * 64,',
                                  "receipt binds a constant instead of installer bytes"),
    "inventory-no-links": ("installer", INSTALLER,
                           '            records[relative] = {"link": os.readlink(path)}',
                           '            pass',
                           "inventory ignores symlinks"),
    "no-escape-check": ("installer", INSTALLER,
                        '    if not realpath.is_relative_to(destination):\n'
                        '        raise ValueError("compiler realpath escapes SDK destination")',
                        '    if False:\n'
                        '        raise ValueError("compiler realpath escapes SDK destination")',
                        "compiler realpath may leave the prefix"),
    "no-tools-check": ("installer", INSTALLER,
                       '    if receipt["tools"] != identify(destination):',
                       '    if False:',
                       "cached tool identity not re-measured"),
    "hit-skips-verify": ("installer", INSTALLER,
                         '    if destination.exists():\n        verify(destination)\n',
                         '    if destination.exists():\n',
                         "cache hit adopted without verification"),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    tree, ident, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    sdk = sys.argv[sys.argv.index("--sdk") + 1] if "--sdk" in sys.argv else None
    kind, rel, old, new, what = MUTATIONS[ident]
    target = tree / rel
    original = target.read_bytes()
    before = sha(target)
    text = original.decode()
    assert text.count(old) == 1, f"{ident}: anchor matches {text.count(old)} times"
    mutated = text.replace(old, new)
    env = None
    if kind == "literal":
        assert mutated.count(STOP_ANCHOR) == 1, "stop anchor lost"
        mutated = mutated.replace(STOP_ANCHOR, STOP_HOOK)
        env = {"R228_STOP_AFTER_LITERALS": "1"}
    audit = out / f"{ident}.jsonl"
    commands = {
        "literal": [sys.executable, AUDIT, "--absent", "--audit", str(audit)],
        "gate1b": [sys.executable, AUDIT, "--sdk-destination", str(sdk),
                   "--audit", str(audit)],
        "audit": [sys.executable, AUDIT, "--selftest"],
        "installer": [sys.executable, "scripts/ci_rv32_sdk_selftest.py"],
    }
    import os
    started = time.time()
    try:
        target.write_text(mutated)
        proc = subprocess.run(commands[kind], cwd=tree, capture_output=True,
                              text=True, env={**os.environ, **(env or {})})
    finally:
        target.write_bytes(original)
    assert sha(target) == before, f"{ident}: original bytes not restored"
    output = proc.stdout + proc.stderr
    stopped = "R228-LITERAL-CONTROLS-PASSED" in output
    failure = [line for line in output.splitlines()
               if "AssertionError" in line or line.startswith(("FAIL", "ERROR"))
               or "Error:" in line]
    killed = proc.returncode != 0 and not stopped
    record = {"id": ident, "kind": kind, "file": rel, "reverts": what,
              "returncode": proc.returncode, "stop_hook_reached": stopped,
              "verdict": "KILLED" if killed else "SURVIVED",
              "first_failure": failure[:3], "seconds": round(time.time() - started, 1),
              "restored_sha256": before}
    (out / f"{ident}.log").write_text(output)
    (out / f"{ident}.json").write_text(json.dumps(record, indent=1) + "\n")
    print(f"{ident}: {record['verdict']} rc={proc.returncode} "
          f"{(failure[:1] or [''])[0][:160]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
