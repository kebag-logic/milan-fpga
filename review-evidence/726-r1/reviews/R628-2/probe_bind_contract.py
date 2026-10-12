#!/usr/bin/env python3
"""Plant bind-era defects into a disposable export of the head and run the
R629-1 reproduction scenario against each. Usage: probe_bind_contract.py <clone> <scratch> <reproduce_contract.py>"""
import subprocess, sys, shutil
from pathlib import Path
clone, scratch, repro = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
RX = "hdl/ieee1722/crf/KL_crf_rx.sv"
PLANTS = {
    "clean": None,
    "drop-frames-rx-wipe": ("        pdu_count_o    <= '0;\n", ""),
    "drop-seq-err-wipe": ("        seq_err_o      <= '0;\n", ""),
    "drop-uf-flag-wipe": ("        iv_uf_r  <= 1'b0;\n        iv_sm_r  <= 1'b0;\n        iv_mr_r  <= 1'b0;\n        iv_tu_r  <= 1'b0;\n        iv_lt_r  <= 1'b0;\n        iv_et_r  <= 1'b0;\n        //! MEDIA_LOCKED",
                          "        iv_sm_r  <= 1'b0;\n        iv_mr_r  <= 1'b0;\n        iv_tu_r  <= 1'b0;\n        iv_lt_r  <= 1'b0;\n        iv_et_r  <= 1'b0;\n        //! MEDIA_LOCKED"),
    "wipe-on-any-edge": ("wire w_bind_rise_w = en_i && !en_q;", "wire w_bind_rise_w = en_i != en_q;"),
    "drop-lock-drop": ("        locked_o <= 1'b0;\n        //! the wipe is itself", "        //! the wipe is itself"),
}
results = []
for name, plant in PLANTS.items():
    tree = scratch / name
    if tree.exists(): shutil.rmtree(tree)
    tree.mkdir(parents=True)
    arc = subprocess.run(["git", "-C", str(clone), "archive", "HEAD", "tests", "tb/tools", "hdl", "docs", "scripts"], capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(tree)], input=arc, check=True)
    if plant:
        f = tree / RX; t = f.read_text(); old, new = plant
        assert t.count(old) == 1, (name, t.count(old)); f.write_text(t.replace(old, new))
    r = subprocess.run([sys.executable, str(repro), str(tree)], capture_output=True, text=True)
    (scratch / f"{name}.log").write_text(r.stdout + r.stderr)
    ok = (r.returncode == 0) if plant is None else (r.returncode != 0 and "ASSERT FAILED" in (r.stdout + r.stderr))
    results.append((name, r.returncode, "PASS" if ok else "UNEXPECTED"))
    print(f"{name}: rc={r.returncode} -> {'expected' if ok else 'UNEXPECTED'}")
sys.exit(0 if all(x[2] == "PASS" for x in results) else 1)
