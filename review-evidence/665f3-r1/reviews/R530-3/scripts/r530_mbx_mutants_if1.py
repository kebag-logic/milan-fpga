#!/usr/bin/env python3
"""[R530] R530-3: the out-of-range-index mutant at one interface (index 1 has no table there)."""
import pathlib, sys
tree, work = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree / 'tb/verilator/mbx'))
import mutants as m  # noqa: E402
arm = m.Arm("r530-no-table-index-not-refused-if1", "KL_mbx_rx.sv",
            "assign {fok_w, fif_w} = (int'(if_r) < int'(MBX_N_IF_C)) ? {1'b1, if_r} : '0;",
            "assign {fok_w, fif_w} = {1'b1, if_r};", 0, "Q", 1)
a, caught, detail = m.run_arm(arm, work)
print(f"[{'CAUGHT' if caught else 'ESCAPED'}] {a.name} (ifs 1, host 0): {detail}")
