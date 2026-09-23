#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""R227-3 disposable resolver fault probes over exact-head copies.

Each probe copies a pristine exact-head tree, applies exact-string edits to
sw/builder/test_builder.py (each must apply exactly once), and runs the real
gate 1b through sw/builder/test_firmware_compiler.py in absent mode (literal
resolver controls, which run on every machine) or with the adopted SDK mapped
through the audited selector (compiled mutants and plants). A probe is KILLED
when the gate fails with an AssertionError naming the expected control, and
SURVIVED when it reaches the planted stop marker or passes.

Usage: probe_mutants.py <base-tree> <work-dir> <receipt-dir> <sdk> ID...
"""
import concurrent.futures
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

PACKET = Path(__file__).resolve().parents[1]
TB = "sw/builder/test_builder.py"
STOP_LITERAL = (
    "    range_control_note = (\n",
    "    raise SystemExit('R227-3-PROBE-STOP literal resolver controls passed')\n"
    "    range_control_note = (\n")
PLANTS = (
    "    #: ---- and the verifier's CONTROL and DATA flow, which no positional\n",
    "    import sys as _r227_sys\n"
    f"    _r227_sys.path.insert(0, {str(PACKET / 'scripts')!r})\n"
    "    import r227_plants\n"
    "    r227_plants.run(dict(locals()))\n"
    "    raise SystemExit('R227-3-PLANTS-DONE')\n"
    "    #: ---- and the verifier's CONTROL and DATA flow, which no positional\n")

STORE_VALUE = ('    if mnem == "sw" or mnem.startswith("amoswap."):\n'
               '        return state.get(args[-2])\n')
MIRROR = ('        if rv32_store_bytes(mnem) is not None or \\\n'
          '                (rv32_memory_operand(args) and not rv32_is_load(mnem)) or \\\n'
          '                mnem in ("call", "jal", "jalr", "tail", "jr", "ret"):\n')
STALE_ASSERT = ('        assert reported[-1:] and isinstance(reported[-1], Rv32Where) and \\\n'
                '            reported[-1].kind == "unplaced", \\\n'
                '            f"after {label} the RV32 resolver still placed')
NEUTRAL_STALE = (STALE_ASSERT, STALE_ASSERT.replace("assert reported", "assert True or reported", 1))
CLASS_ASSERT = "        assert reported == words, \\\n"
NEUTRAL_CLASS = (CLASS_ASSERT, "        assert True or reported == words, \\\n")
REACH_ASSERT = "        assert any(csr_base <= word < csr_base + csr_size\n"
NEUTRAL_REACH = (REACH_ASSERT, "        assert True or any(csr_base <= word < csr_base + csr_size\n")
UNCLASS_ASSERT = "    assert all(len(stores) == 1 and isinstance(stores[0], Rv32Where) and\n"
NEUTRAL_UNCLASS = (UNCLASS_ASSERT, UNCLASS_ASSERT.replace("assert all", "assert True or all", 1))
FOOT_ASSERT = "        assert placed == [want] and start + 63 < csr_base == want.hi, \\\n"
NEUTRAL_FOOT = (FOOT_ASSERT, FOOT_ASSERT.replace("assert placed", "assert True or placed", 1))
FALLBACK = ('    if rv32_memory_operand(args) and not rv32_is_load(mnem):\n'
            '        _rv32_forget_symbols(state)\n'
            '        return ("store", (Rv32Where("unclassified", f"{mnem} {ops}"), None))\n')
TABLE = ('RV32_STORE_BYTES = {"sb": 1, "sh": 2, "sw": 4,\n'
         '                    "fsh": 2, "fsw": 4, "fsd": 8, "fsq": 16}\n')
RD_CLEAR = ('            #: ordinary spelling.\n'
            '            state.set(args[0], None)\n')

#: id -> (what it reverts, mode, edits, expected control fragment)
PROBES = {
    "M0-none": ("no edit: the literal controls must pass to the stop marker",
                "literal", [], None),
    "M1-subword-keeps-value": (
        "R227-2-F1: sb/sh store their register as the slot's whole word",
        "literal", [(STORE_VALUE, STORE_VALUE.replace(
            'mnem == "sw"', 'mnem in ("sw", "sh", "sb")', 1))],
        "at a frame slot's own offset"),
    "M2-no-forget-frame": (
        "R227-2-F1/R228-F5: a store through a stack address forgets no slot",
        "literal", [("            _rv32_forget_frame(state)\n"
                     '            return ("store", (Rv32Where("stack"), value))\n',
                     '            return ("store", (Rv32Where("stack"), value))\n')],
        "through a pointer to a frame slot"),
    "M3-no-frame-overlap": (
        "R228-F4: a frame store forgets no overlapped neighbouring slot",
        "literal", [("            _rv32_forget_overlap(state.mem, (base,), offset, width)\n", "")],
        "an fsd over a frame slot"),
    "M4-mirror-int-first-term": (
        "R227-2-F2: slot mirror first term back to integer stores only",
        "literal", [(MIRROR, MIRROR.replace("rv32_store_bytes(mnem) is not None",
                                            'mnem in ("sw", "sh", "sb")', 1))],
        "between the slot's load and the bltu"),
    "M5-mirror-no-memop-term": (
        "R227-2-F2: slot mirror loses the memory-operand fail-closed term",
        "literal", [(MIRROR, MIRROR.replace(
            "                (rv32_memory_operand(args) and not rv32_is_load(mnem)) or \\\n", "", 1))],
        "an amocas.w through a pointer to the slot"),
    "M45-mirror-pre-pr": (
        "R227-2-F2: slot mirror reverted to the base's integer-only test",
        "literal", [(MIRROR, '        if mnem in ("sw", "sh", "sb") or \\\n'
                     '                mnem in ("call", "jal", "jalr", "tail", "jr", "ret"):\n')],
        "between the slot's load and the bltu"),
    "M6-range-first-byte": (
        "R227-2-F2/R228-F4: ranged store placed by first bytes only",
        "literal", [("            placed = _rv32_range_bounded(held.lo + offset,\n"
                     "                                         held.hi + offset + width - 1)\n",
                     "            placed = _rv32_range_add(held, offset)\n")],
        "not as its footprint"),
    "M7-any-amo-writes-rs2": (
        "R227-2-F2: every AMO and SC treated as writing its rs2",
        "literal", [(STORE_VALUE, STORE_VALUE.replace(
            'mnem.startswith("amoswap.")', "RV32_ATOMIC_STORE_RE.match(mnem)", 1))],
        "handed a placed address"),
    "M7b-sc-writes-rs2": (
        "R227-2-F2: SC treated as writing its rs2",
        "literal", [(STORE_VALUE, STORE_VALUE.replace(
            'mnem.startswith("amoswap.")', 'mnem.startswith(("amoswap.", "sc."))', 1))],
        "an sc.w into a static"),
    "M8-amo-rd-kept": (
        "R227-2-F2: an AMO's rd keeps its old value",
        "literal", [(RD_CLEAR, "            #: ordinary spelling.\n            pass\n")],
        "an AMO writing its base register"),
    "M9-footprint-first-word": (
        "R228-F4: a store is judged at its first word only",
        "literal", [("    return [address & RV32_MASK] + [word & RV32_MASK for word in further]\n",
                     "    return [address & RV32_MASK]\n")],
        "not the words it writes"),
    "M10-no-sym-overlap": (
        "R228-F4: a static store forgets no overlapped word",
        "literal", [('            _rv32_forget_overlap(state.mem, ("sym", held.name), at, width)\n', "")],
        "the RV32 resolver still placed the next store"),
    "M11-no-class-fallback": (
        "R228-F1: memory-addressing unknown mnemonics are stepped over",
        "literal", [(FALLBACK, "")], "UNCLASSIFIED store"),
    "M12-no-other-loads": (
        "R228-F1: FP and LR loads no longer recognised as loads",
        "literal", [('    r"^(?:fl[hwdq]|lr\\.w(?:\\.(?:aq|rl|aqrl))?)$")\n', '    r"^(?!)$")\n')],
        "reported a load as a store"),
    "M13-memop-needs-disp": (
        "R228-S4: memory operand recognised only with a displacement",
        "literal", [('RV32_MEM_BASE_RE = re.compile(r"\\(\\s*([a-z0-9]+)\\s*\\)$")\n',
                     'RV32_MEM_BASE_RE = re.compile(r"-?\\d+\\(\\s*([a-z0-9]+)\\s*\\)$")\n')],
        "UNCLASSIFIED store"),
    "M14-no-fsw": (
        "R228-F1: fsw dropped from the store table",
        "literal", [(TABLE, TABLE.replace('"fsw": 4, ', "", 1))],
        "the fsw store class"),
    "M15-overlap-low-boundary": (
        "boundary: a slot ending exactly at the store's first byte",
        "literal", [("key[-1] + 3 >= start]", "key[-1] + 3 > start]")], None),
    "M16-overlap-high-boundary": (
        "boundary: a slot starting exactly at the store's last byte",
        "literal", [("key[-1] <= start + width - 1 and", "key[-1] < start + width - 1 and")], None),
    "M17-footprint-boundary": (
        "boundary: last byte computed one short",
        "literal", [("((address + width - 1) & ~3) + 4", "((address + width - 2) & ~3) + 4")], None),
    "M18-stores-first-only": (
        "R228-F4: a multi-word observation keeps only its first word",
        "literal", [('                seen["stores"].extend((block, word) for word in payload)\n',
                     '                seen["stores"].append((block, payload[0]))\n')],
        "not the words it writes"),
    "M21-amoswap-unknown": (
        "positive arm: amoswap no longer leaves its rs2",
        "literal", [(STORE_VALUE, STORE_VALUE.replace(
            ' or mnem.startswith("amoswap.")', "", 1))],
        "stale-word probes cannot tell a rewrite"),
    "C1-compiled-subword": (
        "M1 with its literal control neutralised: the compiled union mutants must still refuse",
        "compiled", [(STORE_VALUE, STORE_VALUE.replace(
            'mnem == "sw"', 'mnem in ("sw", "sh", "sb")', 1)), NEUTRAL_STALE],
        "mutation passed the boot-contract gate"),
    "C2-compiled-pointer-rewrite": (
        "M2 with its literal control neutralised: the compiled pointer mutants must still refuse",
        "compiled", [("            _rv32_forget_frame(state)\n"
                      '            return ("store", (Rv32Where("stack"), value))\n',
                      '            return ("store", (Rv32Where("stack"), value))\n'), NEUTRAL_STALE],
        "mutation passed the boot-contract gate"),
    "C3-compiled-fp-classes": (
        "pre-R228-F1 classes (no fsw/fsd, no fallback), literal controls neutralised",
        "compiled", [(TABLE, TABLE.replace('"fsw": 4, "fsd": 8, ', "", 1)),
                     (FALLBACK, ""), NEUTRAL_CLASS, NEUTRAL_REACH, NEUTRAL_UNCLASS,
                     NEUTRAL_FOOT, NEUTRAL_STALE],
        "the resolver accepted the"),
    "M10b-sym-overlap-width-4": (
        "R228-F4 (RM11): static overlap width fixed at 4",
        "literal", [('            _rv32_forget_overlap(state.mem, ("sym", held.name), at, width)\n',
                     '            _rv32_forget_overlap(state.mem, ("sym", held.name), at, 4)\n')],
        "reloaded at its second"),
    "FIX1-plants-frame-lw-only": (
        "information only: frame loads read the slot on lw alone, as statics do; plants re-asked",
        "plants", [("        elif base in RV32_FRAME_REGS and held is None:\n"
                    "            state.set(args[0], state.mem.get((base, offset)))\n",
                    "        elif base in RV32_FRAME_REGS and held is None and mnem == \"lw\":\n"
                    "            state.set(args[0], state.mem.get((base, offset)))\n")], None),
    "P-plants": ("no resolver edit: R227-3 compiled plants, resolver alone and whole gate",
                 "plants", [], None),
    "P-plants-M15": ("M15 with the R227-3 plants: the top-byte plants must flip to ACCEPTED",
                     "plants", [("key[-1] + 3 >= start]", "key[-1] + 3 > start]")], None),
    "C4-compiled-M15": ("M15 in the complete compiled gate: does any control fail?",
                        "compiled", [("key[-1] + 3 >= start]", "key[-1] + 3 > start]")],
                        "mutation passed the boot-contract gate"),
}


def run_probe(pid, base, work, receipts, sdk):
    what, mode, edits, expect = PROBES[pid]
    tree = work / pid
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(base, tree, symlinks=True)
    path = tree / TB
    text = path.read_text()
    applied = []
    stops = [STOP_LITERAL] if mode == "literal" else ([PLANTS] if mode == "plants" else [])
    for old, new in list(edits) + stops:
        count = text.count(old)
        assert count == 1, f"{pid}: edit anchor occurs {count} times: {old[:80]!r}"
        text = text.replace(old, new, 1)
        applied.append({"old": old, "new": new})
    path.write_text(text)
    log = receipts / f"{pid}.log"
    argv = ["python3", "-u", "sw/builder/test_firmware_compiler.py"]
    audit = str(work / f"{pid}.argv.jsonl")
    argv += (["--absent", "--audit", audit] if mode == "literal" else
             ["--sdk-destination", str(sdk), "--audit", audit])
    env = dict(os.environ, R227_PLANTS_OUT=str(receipts / f"{pid}.plants.json"))
    started = time.time()
    with log.open("w") as out:
        try:
            proc = subprocess.run(argv, cwd=tree, env=env, stdout=out,
                                  stderr=subprocess.STDOUT, timeout=570)
            code = proc.returncode
        except subprocess.TimeoutExpired:
            code = "timeout"
    elapsed = round(time.time() - started)
    body = log.read_text(errors="replace")
    stopped = "R227-3-PROBE-STOP" in body or "R227-3-PLANTS-DONE" in body
    passed = "GATE 1b PASS" in body
    last_error = ""
    for line in body.splitlines():
        if "Error" in line or "SystemExit" in line:
            last_error = line.strip()
    if mode == "plants":
        verdict = "PLANTS-DONE" if stopped else "PLANTS-FAILED"
    elif stopped or passed:
        verdict = "SURVIVED"
    elif expect and expect in body and code not in (0, "timeout"):
        verdict = "KILLED"
    else:
        verdict = "OTHER"
    record = {"id": pid, "reverts": what, "mode": mode, "exit": code,
              "elapsed_s": elapsed, "verdict": verdict, "expected": expect,
              "last_error_line": last_error[:600], "edits": applied}
    (receipts / f"{pid}.json").write_text(json.dumps(record, indent=1) + "\n")
    shutil.rmtree(tree)
    return record


def main():
    base, work, receipts, sdk = (Path(arg) for arg in sys.argv[1:5])
    ids = sys.argv[5:]
    work.mkdir(parents=True, exist_ok=True)
    receipts.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(run_probe, pid, base, work, receipts, sdk): pid
                   for pid in ids}
        for future in concurrent.futures.as_completed(futures):
            rec = future.result()
            print(f"{rec['id']}: {rec['verdict']} exit={rec['exit']} "
                  f"{rec['elapsed_s']}s :: {rec['last_error_line'][:220]}", flush=True)


if __name__ == "__main__":
    main()
