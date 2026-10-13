"""Run only the round-5 monitor arms of a given act_ci.py, timing them (scratch driver)."""
import importlib.util, sys, time, pathlib
path = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("act_ci_r5", path)
act = importlib.util.module_from_spec(spec)
sys.modules["act_ci_r5"] = act
spec.loader.exec_module(act)
which = sys.argv[2] if len(sys.argv) > 2 else "masked"
fixture = act.selftest_fixture()
tally = act.SelftestTally()
start = time.monotonic()
if which == "window":
    run = act.ValidatedRun(fixture.pr, fixture.repository, fixture.base)
    act.selftest_act_signal_window(tally, fixture, run)
else:
    with act.temporary_run_directory(False) as root:
        layout = act.make_layout(root, fixture.pr)
        docker = act.selftest_docker_fixture(layout)
        if which == "interrupt":
            act.selftest_interrupt_probe_signal_window(tally, docker)
        else:
            getattr(act, f"selftest_job_cpu_monitor_{which}")(tally, docker)
print(f"failures={tally.failures} seconds={time.monotonic() - start:.1f}", flush=True)

sys.exit(int(bool(tally.failures)))
