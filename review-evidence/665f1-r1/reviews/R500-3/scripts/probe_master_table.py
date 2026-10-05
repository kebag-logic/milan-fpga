"""Re-run the command-master cases of README "The service bound" table with
the lane's own scenario runner (the same arguments as port_stall and
port_deadline) and print each run's longest service call. Usage:
probe_master_table.py <repo> <workdir> <config-stem>"""
import sys
from pathlib import Path
repo, work, stem = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
sys.path.insert(0, str(repo / "sw/firmware/ctrl_nvm/test"))
import nvm_bench  # noqa: E402
import nvm_checks as C  # noqa: E402
from nvm_checks_write import _one_change, _value, P_PROGRAM, P_ERASE, P_ERASE_WAIT  # noqa: E402
inputs = nvm_bench.shape_inputs(repo / "configs" / f"{stem}.yaml", work / "in")
b = nvm_bench.make_bench(inputs, work / "store")
g = b.file("g.bin", b.assemble(b.frames, 5))
rid, new = _one_change(b, 29)
head = ["--litespi", "--slot-b", g, "--boot", "--protect-auth", "--set", f"{rid}:{new.hex()}"]
cases = [
    ("two TX waits slowed 4000", [*head, "--until-phase", str(P_PROGRAM), "--ls-stall", "tx:2:0:4000", "--until-idle"]),
    ("two RX waits slowed 4000", [*head, "--until-phase", str(P_PROGRAM), "--ls-stall", "rx:2:0:4000", "--until-idle"]),
    ("two drains slowed 4000", [*head, "--until-phase", str(P_PROGRAM), "--ls-stall", "drain:2:0:4000", "--until-idle"]),
    ("TX stalled for good in one wait", [*head, "--until-phase", str(P_PROGRAM), "--ls-stall", "tx:1:10:0", "--until-idle"]),
    ("a drain that never empties", [*head, "--until-phase", str(P_PROGRAM), "--ls-stall", "drain:1:0:0", "--until-idle"]),
    ("a master that never answers", [*head, "--until-phase", str(P_ERASE), "--ls-stall", "tx:99999:0:0", "--run-ms", "10000"]),
]
rid30, new30 = _one_change(b, 30)
head30 = ["--litespi", "--slot-b", g, "--boot", "--protect-auth", "--set", f"{rid30}:{new30.hex()}",
          "--until-phase", str(P_PROGRAM)]
cases += [
    ("ten TX waits slowed", [*head30, "--ls-stall", "tx:10:0:4000", "--until-idle"]),
    ("twelve TX waits slowed", [*head30, "--ls-stall", "tx:12:0:4000", "--until-idle"]),
    ("every TX wait slowed", [*head30, "--ls-stall", "tx:999999:0:4000", "--run-ms", "10000"]),
    ("every RX wait slowed (not in the suite)", [*head30, "--ls-stall", "rx:999999:0:4000", "--run-ms", "10000"]),
    ("every drain slowed (not in the suite)", [*head30, "--ls-stall", "drain:999999:0:4000", "--run-ms", "10000"]),
    ("every TX wait slowed by 63 reads (not in the suite)", [*head30, "--ls-stall", "tx:999999:0:63", "--run-ms", "10000"]),
    ("every TX wait slowed by 4095 reads (not in the suite)", [*head30, "--ls-stall", "tx:999999:0:4095", "--run-ms", "10000"]),
]
worst = 0
for what, args in cases:
    r = b.run(*args)
    s = r.s
    worst = max(worst, s["max_call_us"])
    print(f"{stem} | {what} | max_call_us={s['max_call_us']} ok={s['ok']} failed={s['failed']} "
          f"first={s['first']} stalled={s['ls_stalled']} max_withheld={s['ls_max_withheld']} "
          f"hung={s['ls_hung']} calls={s['calls']}")
print(f"{stem} worst={worst} bound={C.CALL_BOUND_US} {'WITHIN' if worst <= C.CALL_BOUND_US else 'EXCEEDS'}")
