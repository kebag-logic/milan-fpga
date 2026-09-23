#!/usr/bin/env python3
"""Reviewer probe: graceful cancellation of the real sweep while the PR's own
self-tests run inside it (the cancellation preflight, or the gptp_shadow
lifecycle test). Checks exit, timing, owned identities, later suite, summary,
and whether those tests' temporary trees survive in TMPDIR.

Usage: probe_nested_phase.py SOURCE_CLONE WORKDIR RECEIPT.json PHASE SIGNAL
  PHASE: preflight | lifecycle     SIGNAL: TERM | INT
"""
import json, os, shutil, signal, subprocess, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_campaign import integrity, tree, alive, present, stat_of, referencing, wait_for, kill_identity, VERILATOR  # noqa: E402
import probe_nested  # noqa: E402

SOURCE = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
RECEIPT = Path(sys.argv[3]).resolve()
PHASE, SIG = sys.argv[4], signal.Signals["SIG" + sys.argv[5]]
probe_nested.SOURCE = SOURCE


def main():
    base = WORK / f"{PHASE}-{SIG.name}"
    repo, probe = probe_nested.prepare(base)
    before = integrity(repo, base / "integrity-before.json")
    env = dict(os.environ)
    for k in ("SUITE_TIMEOUT", "SUITE_SWEEP_LOCK"):
        env.pop(k, None)
    tmp = probe / "tmp"
    env.update(TMPDIR=str(tmp), VERILATOR=VERILATOR, VERILATOR_JOBS="8", PYTHONDONTWRITEBYTECODE="1")
    out = open(probe / "entry.out", "wb")
    p = subprocess.Popen(["bash", str(repo / "scripts/run_all_suites.sh"), str(base / "logs")], cwd=repo, env=env,
                         stdout=out, stderr=subprocess.STDOUT, process_group=0)
    prefix = "suite-cancellation-" if PHASE == "preflight" else "mutant-lifecycle-"

    def in_phase():
        dirs = [d for d in tmp.iterdir() if d.name.startswith(prefix)]
        # several fixtures already created inside the test's tree
        return dirs and sum(1 for _ in dirs[0].iterdir()) >= 6
    assert wait_for(lambda: in_phase() or p.poll() is not None, 300), "phase never reached"
    assert p.poll() is None, (probe / "entry.out").read_text()
    census = tree(p.pid)
    tdirs = [str(d) for d in tmp.iterdir()]
    t0 = time.monotonic()
    fd = os.pidfd_open(p.pid)
    signal.pidfd_send_signal(fd, SIG)
    os.close(fd)
    try:
        status = p.wait(timeout=90)
    except subprocess.TimeoutExpired:
        status = "NO-EXIT-90s"
    secs = round(time.monotonic() - t0, 2)
    out.close()
    time.sleep(2.0)
    text = (probe / "entry.out").read_text()
    left = sorted(x.name for x in tmp.iterdir())
    rec = dict(phase=PHASE, signal=SIG.name, exit=status, exit_seconds=secs, tmp_at_signal=[Path(d).name for d in tdirs],
               tmp_left_after=left,
               tmp_left_file_count={n: sum(1 for _ in (tmp / n).rglob("*")) for n in left},
               census_size=len(census),
               census_live_after={str(k): v["comm"] for k, v in census.items() if alive(k, v["start"])},
               census_zombie_after={str(k): v["comm"] for k, v in census.items()
                                    if present(k, v["start"]) and stat_of(k)["state"] == "Z"},
               processes_referencing_tmp_after=referencing(tmp),
               sentinel_ran=(probe / "ran-zz_sentinel").exists(),
               summary_printed=any(l.startswith("suites:") for l in text.splitlines()),
               output_tail=text[-700:])
    after = integrity(repo, base / "integrity-after.json")
    rec["caller_tracked_state_unchanged"] = before == after
    for k, v in census.items():
        kill_identity(k, v["start"])
    results = json.loads(RECEIPT.read_text()) if RECEIPT.exists() else []
    results = [r for r in results if (r["phase"], r["signal"]) != (PHASE, SIG.name)] + [rec]
    RECEIPT.write_text(json.dumps(results, indent=1) + "\n")
    print(json.dumps({k: rec[k] for k in ("phase", "signal", "exit", "exit_seconds", "tmp_left_after", "tmp_left_file_count",
                                          "census_live_after", "sentinel_ran", "summary_printed",
                                          "caller_tracked_state_unchanged")}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
