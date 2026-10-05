"""Sweep slowed-master patterns the suite does not run (TX, RX and drain;
count, skip and polls) on the LiteSPI port and report the longest service
call against the asserted CALL_BOUND_US. Usage:
probe_bound_sweep.py <repo> <workdir> <config-stem> <jobs>"""
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
repo, work, stem, jobs = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], int(sys.argv[4])
sys.path.insert(0, str(repo / "sw/firmware/ctrl_nvm/test"))
import nvm_bench  # noqa: E402
import nvm_checks as C  # noqa: E402
from nvm_checks_write import _one_change, P_PROGRAM, P_ERASE, P_PROGRAM_WAIT  # noqa: E402
inputs = nvm_bench.shape_inputs(repo / "configs" / f"{stem}.yaml", work / "in")
b = nvm_bench.make_bench(inputs, work / "store")
g = b.file("g.bin", b.assemble(b.frames, 5))
rid, new = _one_change(b, 30)
cases = []
for phase in (P_PROGRAM, P_ERASE, P_PROGRAM_WAIT):
    for kind in ("tx", "rx", "drain"):
        for count in (1, 2, 4, 8, 11, 12, 13, 14, 16, 40, 999999):
            for skip in (0, 1, 7, 130, 250):
                for polls in (64, 1000, 2047, 3900, 3990, 4000, 4050, 4094, 4095):
                    cases.append((phase, f"{kind}:{count}:{skip}:{polls}"))


def one(c):
    phase, stall = c
    r = b.run("--litespi", "--slot-b", g, "--boot", "--protect-auth", "--set", f"{rid}:{new.hex()}",
              "--until-phase", str(phase), "--ls-stall", stall, "--run-ms", "4000")
    return phase, stall, r.s["max_call_us"], r.s["ls_hung"]


with ThreadPoolExecutor(jobs) as ex:
    res = list(ex.map(one, cases))
res.sort(key=lambda x: -x[2])
for phase, stall, us, hung in res[:12]:
    print(f"{stem} phase={phase} stall={stall} max_call_us={us} hung={hung}")
worst = res[0][2]
print(f"{stem} cases={len(res)} worst={worst} bound={C.CALL_BOUND_US} "
      f"{'WITHIN' if worst <= C.CALL_BOUND_US else 'EXCEEDS'} hung_any={any(h for *_, h in res)}")
