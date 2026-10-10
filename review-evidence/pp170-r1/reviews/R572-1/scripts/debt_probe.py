#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Disposable probe: is omitted descriptor-debt protection visible on NAMES?

Builds two isolated copies of a processor export (golden, and the author's
`rollback_ignores_debt` edit from tb/pp_top/d3_mutants.py) with one extra
selection `debt` added to tb/name_state/sim_main.cpp: every name record of the
population is saved, a rate record is seeded, and the AUDIO_UNIT descriptor
fetch answers LATE cycles late (the D3R10 shape), so pass 1 aborts (cause 6)
and rolls back while the guard still owes the abandoned burst. After the
terminal every name entry and GET_NAME must hold the image default, both
ENTITY names must be served by READ_DESCRIPTOR, and a later SET_NAME of the
last ordinal must save and read back.

Usage: debt_probe.py --root <export> --output <new dir> [--verilator V] [--late N ...]
"""
import argparse, json, re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

PROBE = r'''
  void debt_probe(int late) {
    fresh();
    for (const auto& n : named) seed(uint8_t(0x80 + n.ordinal), name_record(n.ordinal, n.name));
    seed(0x02, d3_record(0x02, 96000, 4));
    // the AUDIO_UNIT descriptor's address, read from the image's index map
    const uint32_t ioff = rd32(&image[12]);
    const uint16_t nent = uint16_t((image[8] << 8) | image[9]);
    uint32_t au = 0;
    for (uint16_t e = 0; e < nent; ++e) {
      const uint8_t* p = &image[ioff + 16u * e];
      if (((p[2] << 8) | p[3]) == 0x0002) au = DESC_BASE + rd32(p + 8);
    }
    x.dram_late_at = au;
    x.dram_late_cycles = late;
    const Boot b = boot(8 * RS_TMO);
    x.dram_late_at = 0;
    x.d->link_up_i = 1;
    printf("DEBT late %d: au 0x%08x done %ld closed %ld fail %u cause %u rb %u\n", late, au,
           b.done, b.closed, unsigned(x.d->restore_fail_o), unsigned(x.d->rs_cause_o),
           unsigned(x.d->restore_rb_o));
    bool entries = true, gets = true;
    for (const auto& n : named) {
      std::vector<uint8_t> got;
      for (unsigned lane = 0; lane < 8; lane++) {
        x.d->dbg_name_lane_i = n.ordinal * 8 + lane; x.d->eval();
        for (int byte = 7; byte >= 0; byte--) got.push_back(uint8_t(x.d->dbg_name_o >> (byte * 8)));
      }
      entries = entries && got == defaults[n.ordinal];
      gets = gets && get_reads(n, defaults[n.ordinal]);
    }
    CHECK(b.done >= 0 && x.d->restore_rb_o, "DEBT %d premise: rolled back to DEFAULTS", late);
    CHECK(entries && gets, "DEBT %d names: every entry and GET_NAME at the image default after the roll-back", late);
    CHECK(entity_reads(defaults[0], defaults[1]), "DEBT %d names: READ_DESCRIPTOR serves both image ENTITY names", late);
    const auto& last = named.back();
    const bool set = set_name(last, last.name);
    x.idle(4 * WINDOW);
    const auto want = name_record(last.ordinal, last.name);
    CHECK(set && get_reads(last, last.name)
              && std::equal(want.begin(), want.end(), x.nv_mem[0x80 + last.ordinal].begin()),
          "DEBT %d names: a later SET_NAME of the last ordinal saves and reads back", late);
  }
'''


def make_tree(root, work, mutate):
    tree = work / "source"
    skip = shutil.ignore_patterns("obj*", "*.hex", "__pycache__")
    for d in ("hdl", "tb/common", "tb/pp_top", "tb/name_state"):
        shutil.copytree(root / d, tree / d, ignore=skip)
    sim = tree / "tb/name_state/sim_main.cpp"
    s = sim.read_text()
    anchor = "  void measure_names() {"
    assert s.count(anchor) == 1
    s = s.replace(anchor, PROBE + anchor)
    sel = '  else if (selection == "all") names.run();\n'
    assert s.count(sel) == 1
    s = s.replace(sel, sel + '  else if (selection.rfind("debt", 0) == 0) names.debt_probe(std::stoi(selection.substr(4)));\n')
    sim.write_text(s)
    if mutate:
        w = tree / "hdl/aecp/KL_aecp_nvm_writer.sv"
        t = w.read_text()
        old = "          if (rb_min_r && !desc_debt_i) ws_r <= W_RELOC;\n"
        assert t.count(old) == 1
        w.write_text(t.replace(old, "          if (rb_min_r) ws_r <= W_RELOC;\n"))
    return tree


def one(args, name, mutate):
    work = args.output / name
    work.mkdir(parents=True)
    tree = make_tree(args.root, work, mutate)
    sys.path.insert(0, str(tree / "tb/name_state"))
    import run as harness
    import fixture as fx
    binary = harness.build(tree, work, args.verilator)
    out = {}
    for aaf in (1, 8):
        image = work / f"names-{aaf}.bin"
        image.write_bytes(fx.packer(tree).build(fx.fixture(aaf), lint=False)[0])
        for late in args.late:
            r = subprocess.run([str(binary), str(image), str(aaf), f"debt{late}"], cwd=work,
                               text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            (work / f"debt-{aaf}-{late}.log").write_text(r.stdout)
            out[f"{aaf}x{aaf}/late{late}"] = {
                "rc": r.returncode,
                "tally": (re.search(r"\d+ checks: \d+ PASS, \d+ FAIL", r.stdout) or [None])[0],
                "status": [l for l in r.stdout.splitlines() if l.startswith(("DEBT", "FAIL"))]}
    print(name, json.dumps(out, indent=1), flush=True)
    return name, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--verilator", default="verilator")
    ap.add_argument("--late", type=int, nargs="*", default=[5000, 16000])
    args = ap.parse_args()
    args.root = args.root.resolve(); args.output = args.output.resolve()
    args.output.mkdir(parents=True, exist_ok=False)
    with ThreadPoolExecutor(2) as pool:
        res = dict(pool.map(lambda a: one(args, *a), (("golden", False), ("rollback_ignores_debt", True))))
    (args.output / "results.json").write_text(json.dumps(res, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
