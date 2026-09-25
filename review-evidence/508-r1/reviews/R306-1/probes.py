#!/usr/bin/env python3
"""Reviewer-owned disposable probes for PR #560 / issue #508 at 6a9828c1.

Each probe plants one edit in a COPY of the processor hdl/ tree (kind "pp")
or temporarily in tb/verilator/milan_dp/sim_nxn.cpp (kind "tb", restored
byte-for-byte afterwards), rebuilds the timed obj_notify leg through the
suite's own `make notify-build` recipe with VERILATOR_JOBS=8, runs it, and
records the tally and the failing check names.

Usage: python3 probes.py <clone root> <scratch dir> <receipt dir> [name ...]
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
SCRATCH = Path(sys.argv[2]).resolve()
RECEIPTS = Path(sys.argv[3]).resolve()
DP = ROOT / "tb/verilator/milan_dp"
PP_HDL = ROOT / "protocol-processor/hdl"
PP_TOP = Path("top/protocol_processor_top.sv")
NXN = DP / "sim_nxn.cpp"

PROBES = {
    # the listener status change no longer reaches the notify OR
    "P1_no_status_push": ("pp", [(
        "          || lstn_gsi_changed_r[k]\n", "")]),
    # every listener record write announces, changed or not (a fabricated transition)
    "P2_fabricated_push": ("pp", [(
        "            (lstn_gsi_status_r[lstn_recwr_sink_w] != lstn_gsi_status_w);",
        "            1'b1;")]),
    # processor #113 reverted: a latency-only change no longer pushes
    "P3_revert_latency_notify": ("pp", [(
        "          || srp_evt_tk_fail_chg_w[k] || srp_evt_tk_latency_chg_w[k];",
        "          || srp_evt_tk_fail_chg_w[k];")]),
    # G6's refresh carries a different AccumulatedLatency and nothing else
    # (from G6 on, every Talker Failed the bridge sends carries 600000 ns)
    "P4_latency_only_refresh": ("tb", [
        ("    static constexpr uint64_t kGsiBridgeB = 0x0F1E2D3C4B5A6978ull;\n",
         "    static constexpr uint64_t kGsiBridgeB = 0x0F1E2D3C4B5A6978ull;\n"
         "    bool gsi_lat_hi = false;\n"),
        ("        gsi_put(f, 42, 500000, 4);                   // AccumulatedLatency\n",
         "        gsi_put(f, 42, gsi_lat_hi ? 600000 : 500000, 4);\n"),
        ("        notify_clear();\n        for (int s = 0; s < kGsiSinks; s++)\n"
         "            gsi_declare(s, kGsiSink[s].bridge, kGsiSink[s].code, 1);\n",
         "        notify_clear();\n        gsi_lat_hi = true;\n        for (int s = 0; s < kGsiSinks; s++)\n"
         "            gsi_declare(s, kGsiSink[s].bridge, kGsiSink[s].code, 1);\n")]),
    # G8 graded as exactly one push (the README's "every transition pushes
    # exactly one") instead of at least one: measures the withdrawal's count
    "P6_g8_exactly_one": ("tb", [(
        "        ck(\"[GSI] G8 sink 0 withdrawn: the withdrawal pushed\", static_cast<long>(pushes >= 1), 1);\n",
        "        ck(\"[GSI] G8 sink 0 withdrawn: the withdrawal pushed\", pushes, 1);\n")]),
    # the harness never starts the boot restore walk
    "P5_no_restore_walk": ("tb", [(
        "    prove_the_identity_and_provision_the_entity_id();\n    start_the_boot_restore_walk();\n",
        "    prove_the_identity_and_provision_the_entity_id();\n")]),
}


def build_and_run(name, pp_dir, mdir):
    log = RECEIPTS / f"probe_{name}.log"
    b = subprocess.run(
        ["make", "-s", "-C", str(DP), "-o", "ltn_rom.hex", "-o", "ucode.hex",
         "notify-build", f"PP_DIR={pp_dir}", f"NOTIFY_MDIR={mdir}",
         "VERILATOR_JOBS=8"], capture_output=True, text=True, check=False)
    if b.returncode != 0:
        log.write_text(b.stdout + b.stderr)
        return f"{name}: BUILD FAILED rc={b.returncode}"
    r = subprocess.run([str(mdir / "Vmilan_dp_notify")], cwd=str(DP),
                       capture_output=True, text=True, check=False)
    out = r.stdout + r.stderr
    log.write_text(out)
    fails = [ln.strip() for ln in out.splitlines() if ln.strip().startswith("[FAIL]")]
    tally = [ln for ln in out.splitlines() if ln.startswith("checks:")]
    head = "; ".join(fails[:6])
    return f"{name}: rc={r.returncode} {tally[-1] if tally else 'no tally'} first-fails: {head}"


def main():
    names = sys.argv[4:] or list(PROBES)
    results = []
    for name in names:
        kind, edits = PROBES[name]
        work = SCRATCH / f"probe_{name}"
        if work.exists():
            shutil.rmtree(work)
        work.mkdir(parents=True)
        pp_dir = PP_HDL
        backup = None
        if kind == "pp":
            pp_dir = work / "pp_hdl"
            shutil.copytree(PP_HDL, pp_dir)
            text = (pp_dir / PP_TOP).read_text()
        else:
            backup = NXN.read_bytes()
            text = backup.decode()
        ok = True
        for old, new in edits:
            if text.count(old) != 1:
                results.append(f"{name}: PATTERN MATCHED {text.count(old)} TIMES - not planted")
                ok = False
                break
            text = text.replace(old, new)
        try:
            if ok:
                if kind == "pp":
                    (pp_dir / PP_TOP).write_text(text)
                else:
                    NXN.write_text(text)
                results.append(build_and_run(name, pp_dir, work / "obj"))
        finally:
            if backup is not None:
                NXN.write_bytes(backup)
    summary = "\n".join(results) + "\n"
    (RECEIPTS / "probes_summary.txt").write_text(summary)
    print(summary)


if __name__ == "__main__":
    main()
