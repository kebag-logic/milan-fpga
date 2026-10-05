"""R500-3 probe: a slot whose every boot read fails, for good. The store must
not deadlock: boot returns, AECP is released once, the service loop keeps
stepping for a long run with changes and console commits, nothing is erased
or written, and the condition is reported (unread bit, HELD phase, dirty).
Reset is the only exit: the held state repeats on every faulted boot and
ends on the first clean one. Model port, one shape. Usage:
probe_held.py <repo> <workdir> [config-stem]"""
import sys
from pathlib import Path
repo, work = Path(sys.argv[1]), Path(sys.argv[2])
stem = sys.argv[3] if len(sys.argv) > 3 else "endstation_ax7101_1x1_tdm8"
sys.path.insert(0, str(repo / "sw/firmware/ctrl_nvm/test"))
import nvm_bench  # noqa: E402
import nvm_checks as C  # noqa: E402
from nvm_checks_write import _one_change  # noqa: E402

inputs = nvm_bench.shape_inputs(repo / "configs" / f"{stem}.yaml", work / "in")
b = nvm_bench.make_bench(inputs, work / "store")
bad = []


def run(what, *args):
    f = []
    r = C.go(b, "", f, *args)
    s = r.s
    print(f"{what}: terminal={s['terminal']} auth={s['auth']} seq={s['seq']} vd_a={s['vd_a']} "
          f"vd_b={s['vd_b']} unread={s['unread']} read_faults={s['read_faults']} phase={s['phase']} "
          f"releases={s['releases']} steps={s['steps']} calls={s['calls']} dirty={s['dirty']} "
          f"stale={s['stale']} erases={s['erases']} programs={s['programs']} ok={s['ok']} "
          f"commit_tries={s['commit_tries']} commit_refused={s['commit_refused']} "
          f"max_call_us={s['max_call_us']} now_ms={s['now_ms']}")
    bad.extend(f"{what}: contract {x}" for x in f)
    return s


def need(what, ok):
    print(f"  {'OK ' if ok else 'BAD'} {what}")
    if not ok:
        bad.append(what)


rid, new = _one_change(b, 41)
_r2, new2 = _one_change(b, 42)
churn = [w for k in range(20) for w in ("--set", f"{rid}:{(new if k % 2 else new2).hex()}",
                                         "--run-ms", "2500", "--commit-try")]
for label, slots, dead, want_auth, want_term in (
        ("A valid 5, B blank, B dead", ["--slot-a", b.file("a5.bin", b.assemble(b.frames, 5))],
         C.SLOT_B, 0, C.T_COMPLETE),
        ("A valid 5, B valid 6, B (newer) dead",
         ["--slot-a", b.file("a5.bin", b.assemble(b.frames, 5)),
          "--slot-b", b.file("b6.bin", b.assemble(b.frames, 6))], C.SLOT_B, 0, C.T_COMPLETE),
        ("A dead, B blank", [], C.SLOT_A, -1, C.T_BLANK)):
    if not slots:
        slots = ["--blank"]
    for boot in range(3):
        s = run(f"{label}, faulted boot {boot}", *slots, "--boot-fault",
                f"read-fail-at:1000000:0:{dead:#x}", "--boot", *churn)
        need("boot returned, AECP released once", s["releases"] == 1)
        need("the loop kept stepping (50 s of service)", s["calls"] >= 400_000 and s["now_ms"] >= 50_000)
        need("held and reported", s["phase"] == C.P_HELD and s["unread"] != 0 and s["read_faults"] >= 3
             and s["dirty"] == 1)
        need("nothing erased or programmed, every console commit refused",
             s["erases"] == 0 and s["programs"] == 0 and s["commit_refused"] == s["commit_tries"] == 20)
        need("the readable slot applied", s["auth"] == want_auth and s["terminal"] == want_term)
    s = run(f"{label}, clean boot", *slots, "--boot", "--set", f"{rid}:{new.hex()}", "--until-idle")
    need("a clean boot ends the hold and commits", s["phase"] == C.P_IDLE and s["unread"] == 0
         and s["ok"] == 1)
print("PROBE_HELD", "FAIL" if bad else "PASS", len(bad))
sys.exit(1 if bad else 0)
