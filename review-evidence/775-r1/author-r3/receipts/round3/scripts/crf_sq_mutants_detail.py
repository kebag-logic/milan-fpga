#!/usr/bin/env python3
"""crf_sq_mutants_detail.py <clone> <out>: the two #775 CRF mutants of mutants.py,
planted the same way (one anchor, exactly once) and run through `make unit-build`,
listing EVERY failed check, not only the named one mutants.py requires. Evidence
only; the gate verdict is mutants.py's."""
import subprocess, sys
from pathlib import Path

clone, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
here = clone / "tb/verilator/crf_rx"
sys.path.insert(0, str(here))
import mutants  # noqa: E402

src = (clone / "hdl/ieee1722/crf/KL_crf_rx.sv").read_text()
for name, anchor, repl, named in mutants.UNIT_MUTANTS:
    if not name.startswith("offformat_"):
        continue
    assert src.count(anchor) == 1, name
    work = out / name
    work.mkdir(exist_ok=True)
    rtl = work / f"{name}.sv"
    rtl.write_text(src.replace(anchor, repl))
    mdir = Path("<scratch>/crf-sq-detail") / name
    b = subprocess.run(["make", "-s", "-C", str(here), "unit-build", f"RX_RTL={rtl}",
                        f"UNIT_MDIR={mdir}"], capture_output=True, text=True)
    r = subprocess.run([str(mdir / "Vcrf_rx_sim")], capture_output=True, text=True, cwd=here)
    fails = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("[FAIL]")]
    named_lines = [l for l in fails if not l.startswith("[FAIL] pdu#")]
    pdu_lines = len(fails) - len(named_lines)
    diff = subprocess.run(["diff", "-u", str(clone / "hdl/ieee1722/crf/KL_crf_rx.sv"), str(rtl)],
                          capture_output=True, text=True).stdout
    (work / "plant.diff").write_text(diff)
    (work / "result.txt").write_text(
        f"build rc={b.returncode} run rc={r.returncode}\nnamed check required: {named}\n"
        f"named check failed: {any(named in l for l in named_lines)}\n"
        f"{len(named_lines)} named failures, {pdu_lines} per-PDU replica-compare failures\n"
        + "\n".join(named_lines) + "\n" + r.stdout.splitlines()[-1] + "\n")
    rtl.unlink()
    print((work / "result.txt").read_text())
