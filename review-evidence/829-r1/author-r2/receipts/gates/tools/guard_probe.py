"""Plant a guard value on the MII build, report which named checks fail. Restores the source."""
import subprocess, sys
sys.dont_write_bytecode = True
sys.path.insert(0, 'tb/verilator/gptp_txts')
import mutants as m
path = m.PLANE / "KL_gptp_txret.sv"
old = "RECON_NEED_CYC_C = TXTS_CORR_NS_P / DP_TICK_NS_P + 15;"
assert m.tracked_clean(path)
for g in (203, 202, 200, 195, 190, 189, 188, 187, 186, 185, 180, 170, 150, 64):
    new = old if g == 203 else f"RECON_NEED_CYC_C = {g};  // PROBE"
    assert m.apply_control(path, old, new)
    out = m.run_suite("run-mii")
    m.restore(path)
    assert m.tracked_clean(path)
    fails = [l.strip() for l in out.splitlines() if "[FAIL]" in l]
    res = [l.strip() for l in out.splitlines() if l.startswith("RESULT")]
    print(f"guard={g}: {res[0] if res else 'no result'}; " + ("; ".join(fails) if fails else "no failed check"), flush=True)
