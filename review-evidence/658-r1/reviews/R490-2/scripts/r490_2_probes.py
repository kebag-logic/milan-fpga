#!/usr/bin/env python3
"""R490-2 disposable probes of the #658 boot window, on the [DYNMAP] leg.

Each probe plants one edit in a COPY of hdl/milan/milan_datapath.sv, rebuilds
the dynmap leg through the leg's own recipe (the helpers of the repository's
tb/verilator/milan_dp/dynmap_mutants.py) and runs it. The verdict is the
leg's own: KILLED when it reports a failure, SURVIVED when it passes, and any
other outcome is printed as such; a death by signal is NOT-EVIDENCE. The
failing check lines are listed. The leg's generated inputs (ltn_rom.hex,
ucode.hex) must already exist: the recipe is run with them kept unmade.

Usage: r490_2_probes.py <repo> <workdir> <probe-id> [<probe-id> ...]
"""

import sys
from pathlib import Path

REPO = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(REPO / "tb/verilator/milan_dp"))
import dynmap_mutants as dm  # noqa: E402

HOLD = "&& !amap_boot_busy_w && !aecp_locked"
CAP_RAM = ("(!aecp_odmap_wr_p_w && !amap_edit_txn_active_r\n"
           f"                     {HOLD}")
REN_RAM = ("(!aecp_dmap_wr_p_w && !amap_edit_txn_active_r\n"
           f"                     {HOLD}")
OUT_ST = (f"          {HOLD}\n"
          "          && cfg_chmap_wr_en && cfg_chmap_wr_side")
IN_ST = (f"          {HOLD}\n"
         "          && cfg_chmap_wr_en && !cfg_chmap_wr_side")
REWIND = ("        amap_boot_last_r <= 1'b1;\n"
          "        amap_boot_k_r    <= '0;\n")
WAIT = "  assign pp_amap_edit_wait_w = amap_boot_busy_w;"


def unheld(site: str, term: str = "&& !aecp_locked") -> tuple[str, str]:
    return (site, site.replace(HOLD, term))


PROBES = {
    "Q1": ("capture RAM site of the CSR hold removed alone",
           [unheld(CAP_RAM)], "SURVIVED (equivalent on the shipping shape)"),
    "Q2": ("render RAM site of the CSR hold removed alone",
           [unheld(REN_RAM)], "SURVIVED (equivalent on the shipping shape)"),
    "Q3": ("both RAM sites of the CSR hold removed",
           [unheld(CAP_RAM), unheld(REN_RAM)],
           "SURVIVED (equivalent on the shipping shape)"),
    "Q4": ("the store sites hold only while the window is open, not in the sweep",
           [unheld(IN_ST, "&& !amap_boot_r && !aecp_locked"),
            unheld(OUT_ST, "&& !amap_boot_r && !aecp_locked")], "KILLED"),
    "Q5": ("the edit face waits only while the window is open, not in the sweep",
           [(WAIT, "  assign pp_amap_edit_wait_w = amap_boot_r;")], "KILLED"),
    "Q6": ("the terminal does not rewind the cursor: the sweep starts mid-lap",
           [(REWIND, "        amap_boot_last_r <= 1'b1;\n")], "informative"),
    "Q7": ("the sweep after the terminal starts at key 5, skipping keys 0..4",
           [(REWIND, "        amap_boot_last_r <= 1'b1;\n"
                     "        amap_boot_k_r    <= 3'd5;\n")], "KILLED"),
}


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    dm.DP_RTL = REPO / "hdl/milan/milan_datapath.sv"
    rc = 0
    for pid in sys.argv[3:]:
        name, edits, expect = PROBES[pid]
        dp = dm.plant(name, edits, WORK, pid)
        if dp is None:
            print(f"{pid} NOT PLANTED: {name}")
            rc = 1
            continue
        exe = dm.build("dynmap", dp, WORK / f"obj_{pid}")
        if exe is None:
            print(f"{pid} DID NOT COMPILE: {name}")
            rc = 1
            continue
        code, out = dm.run_leg("dynmap", exe)
        (WORK / f"{pid}.log").write_text(out)
        reason, failed = dm.log_reports_failure(out)
        fails = [ln.strip() for ln in out.splitlines() if ln.strip().startswith("[FAIL]")]
        tally = [ln.strip() for ln in out.splitlines() if "checks" in ln and "fail" in ln.lower()][-1:]
        if code < 0:
            verdict = f"NOT-EVIDENCE (died by signal {-code})"
        elif code == 0 and not failed:
            verdict = "SURVIVED"
        elif failed:
            verdict = "KILLED"
        else:
            verdict = f"rc {code} with no harness verdict"
        print(f"{pid} {verdict} (expected {expect}): {name}; rc {code}; {reason}; "
              f"{len(fails)} [FAIL] lines; tally {tally}")
        for ln in fails:
            print(f"    {ln}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
