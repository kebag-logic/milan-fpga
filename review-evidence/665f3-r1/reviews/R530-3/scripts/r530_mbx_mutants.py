#!/usr/bin/env python3
"""[R530] R530-3: reviewer-planted interface mix-ups in KL_mbx_rx's bound-talker term, run through
tb/verilator/mbx/mutants.py's own plant/build/run (VERILATOR from the environment).
usage: r530_mbx_mutants.py TREE WORKDIR"""
import pathlib, sys
from concurrent.futures import ThreadPoolExecutor
tree, work = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree / 'tb/verilator/mbx'))
import mutants as m  # noqa: E402
F = "KL_mbx_rx.sv"
LIVE = "live_w[e] = fok_w && en_r[int'(fif_w) * int'(NB_C) + e] && !owed_r[int'(fif_w) * int'(NB_C) + e];"
ARMS = [
    m.Arm("r530-live-en-of-interface-0", F, LIVE,
          "live_w[e] = fok_w && en_r[e] && !owed_r[int'(fif_w) * int'(NB_C) + e];", 0, "Q13", 2),
    m.Arm("r530-compare-interface-0-identities", F,
          "eq_w[e]   = rx_data_i == c_tap_w[int'(fif_w) * int'(NB_C) + e];",
          "eq_w[e]   = rx_data_i == c_tap_w[e];", 0, "Q", 2),
    m.Arm("r530-if-latched-every-byte", F, "if (cnt_r == 11'd0) if_r <= rx_if_i;", "if_r <= rx_if_i;", 0, "Q", 1),
    m.Arm("r530-if-latched-every-byte-if2", F, "if (cnt_r == 11'd0) if_r <= rx_if_i;", "if_r <= rx_if_i;", 0, "Q", 2),
    m.Arm("r530-host-entry-ignores-interface", F,
          "assign hk_w   = KW_C'(int'(bnd_if_i) * int'(NB_C) + int'(bnd_entry_i));",
          "assign hk_w   = KW_C'(int'(bnd_entry_i));", 0, "Q", 2),
    m.Arm("r530-no-table-index-not-refused", F,
          "assign {fok_w, fif_w} = (int'(if_r) < int'(MBX_N_IF_C)) ? {1'b1, if_r} : '0;",
          "assign {fok_w, fif_w} = {1'b1, if_r};", 0, "Q13", 2),
    m.Arm("r530-verdict-presented-interface-axil-if2", F,
          "assign {fok_w, fif_w} = (int'(if_r) < int'(MBX_N_IF_C)) ? {1'b1, if_r} : '0;",
          "assign {fok_w, fif_w} = (int'(rx_if_i) < int'(MBX_N_IF_C)) ? {1'b1, rx_if_i} : '0;", 1, "Q22", 2),
]
with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(lambda a: m.run_arm(a, work), ARMS))
for arm, caught, detail in results:
    # caught here means: exit 1 and a failing line containing the needle (the check family)
    print(f"[{'CAUGHT' if caught else 'ESCAPED'}] {arm.name} (ifs {arm.ifs}, host {arm.host}): {detail}")
