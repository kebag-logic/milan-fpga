#!/usr/bin/env python3
"""Campaign 5: disposable fault probes on a copy of the exact head.

Each probe edits files in the copy, runs one focused check, records rc and
the tail of its output, and restores the edited files with `git checkout`.
Usage: c5_mutations.py <tree copy> <receipt dir> <probe set: builder|capacity|page>
"""
import json
import subprocess
import sys
from pathlib import Path

TREE, OUT, SET = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
OUT.mkdir(parents=True, exist_ok=True)
BUILDER = "sw/builder/endstation_builder.py"
RTL = "hdl/milan/KL_nvm_backend.sv"
PAGE = "docs/design/SAVED_STATE_FASTCONNECT.md"
CONTRACT = "scripts/nvm_contract.py"
GATE38 = ["python3", "-c", "import sys; sys.path.insert(0,'sw/builder'); import test_builder as t; "
          "t.test_name_count_fits_the_nvm_name_block()"]
GATE24 = ["python3", "-c", "import sys; sys.path.insert(0,'sw/builder'); import test_builder as t; "
          "t.test_d8_role_pools()"]
NVM = ["python3", "scripts/check_nvm_record_space.py"]


def edit(rel, old, new, count=1):
    p = TREE / rel
    text = p.read_text()
    assert text.count(old) == count, f"{rel}: anchor {old!r} occurs {text.count(old)} times"
    p.write_text(text.replace(old, new))


def run(cmd, timeout=1800):
    r = subprocess.run(cmd, cwd=TREE, capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout + r.stderr)


def restore():
    subprocess.run(["git", "checkout", "--", "."], cwd=TREE, check=True)
    st = subprocess.run(["git", "status", "--porcelain"], cwd=TREE, capture_output=True, text=True).stdout
    assert st == "", st


def probe(name, edits, cmd, want_red, grep=()):
    for e in edits:
        edit(*e)
    rc, text = run(cmd)
    restore()
    red = rc != 0
    hits = {g: (g in text) for g in grep}
    tail = "\n".join(text.strip().splitlines()[-6:])
    rec = {"probe": name, "rc": rc, "red": red, "want_red": want_red, "as_expected": red == want_red,
           "grep": hits, "tail": tail}
    (OUT / f"{name}.log").write_text(text)
    print(json.dumps(rec), flush=True)
    return rec


results = []
restore()
if SET == "builder":
    results.append(probe("b0_unmutated_gate38", [], GATE38, False))
    results.append(probe("b1_off_by_one_ge", [(BUILDER, "if aem_name_entries > capacity:", "if aem_name_entries >= capacity:")],
                         GATE38, True, ["128 writable names refused"]))
    results.append(probe("b2_capacity_mirrored_literal",
                         [(BUILDER, "    capacity, where = nvm_name_capacity()\n    if aem_name_entries",
                           "    capacity, where = 128, 'hdl/milan/KL_nvm_backend.sv:247'\n    if aem_name_entries")],
                         GATE38, True, ["stayed green"]))
    results.append(probe("b3_refusal_removed", [(BUILDER, "if aem_name_entries > capacity:", "if False:")],
                         GATE38, True, ["129 writable names accepted"]))
    results.append(probe("b4_refusal_without_capacity",
                         [(BUILDER, "saved-state backend holds {capacity} NAME records", "saved-state backend holds its NAME records")],
                         GATE38, True, ["does not name"]))
    results.append(probe("b5_write_before_derivation",
                         [(BUILDER, "    art = _derive_artifacts(config_path)\n    cfg = art.cfg\n    d, out",
                           "    Path(outdir).mkdir(parents=True, exist_ok=True)\n"
                           "    art = _derive_artifacts(config_path)\n    cfg = art.cfg\n    d, out")],
                         GATE38, True, ["came after writing"]))
    results.append(probe("b6_rtl_guard_on_literal",
                         [(RTL, "N_NAME_P > N_NAME_MAX_C) begin", "N_NAME_P > 128) begin")],
                         GATE38, True, ["not N_NAME_MAX_C"]))
    results.append(probe("b7_gate24_unmutated", [], GATE24, False))
    results.append(probe("b8_gate24_refusal_removed", [(BUILDER, "if aem_name_entries > capacity:", "if False:")],
                         GATE24, True))
elif SET == "capacity":
    # The capacity moved in the RTL only: the builder and the RTL guard follow it;
    # what do the record-space gate (nvm_contract ALLOC) and gate 38 say?
    mv = [(RTL, "N_NAME_MAX_C = 128;", "N_NAME_MAX_C = 100;")]
    results.append(probe("k1_rtl_cap100_gate38", mv, GATE38, True, ["declares 100 NAME records"]))
    results.append(probe("k2_rtl_cap100_nvm_record_space", mv, NVM, None))
    results.append(probe("k3_rtl_cap100_build_8x8", mv,
                         ["python3", BUILDER, "-o", "../c5k_out", "configs/endstation_ax7101_8x8.yaml"], True,
                         ["107 writable names", "100 NAME records"]))
    # The record-space gate's own NAME block moved: does anything tie it to the RTL?
    results.append(probe("k4_contract_name_block_100", [(CONTRACT, '"NAME":       (0x80, 128),', '"NAME":       (0x80, 100),')],
                         NVM, None, ["block reads 128"]))
elif SET == "page":
    row8 = "| `0x80` .. `0xFF` | user name | 128 | name ordinal | 39 | **107** |"
    results.append(probe("p0_unmutated", [], NVM, False))
    results.append(probe("p1_8x8_names_108", [(PAGE, row8, row8.replace("**107**", "**108**"))], NVM, True,
                         ["8x8 user name reads 108"]))
    results.append(probe("p2_8x8_cell_dropped", [(PAGE, row8, "| `0x80` .. `0xFF` | user name | 128 | name ordinal | 39 |")],
                         NVM, True))
    results.append(probe("p3_records_total", [(PAGE, "| **records** | | | | **54** | **164** |", "| **records** | | | | **54** | **165** |")],
                         NVM, True, ["records reads 165"]))
    results.append(probe("p4_name_row_deleted", [(PAGE, row8 + "\n", "")], NVM, True, ["no row for"]))
    results.append(probe("p5_header_changed", [(PAGE, "| ids | group | block | index | 1x1 | 8x8 |", "| ids | group | block | index | 1x1 | 8x8 | x |")],
                         NVM, True, ["no single allocation table"]))
    results.append(probe("p6_block_129", [(PAGE, row8, row8.replace("| 128 |", "| 129 |"))], NVM, True, ["block reads 129"]))
    results.append(probe("p7_extra_cell", [(PAGE, row8, row8 + " 999 |")], NVM, True))
    results.append(probe("p8_highest_id", [(PAGE, "`0xA6` | `0xEA`", "`0xA6` | `0xEB`")], NVM, True))
(OUT / f"results_{SET}.json").write_text(json.dumps(results, indent=1) + "\n")
print("done", SET)
