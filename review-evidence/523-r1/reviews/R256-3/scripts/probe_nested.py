#!/usr/bin/env python3
"""Reviewer probe: the real sweep entry containing the real gPTP shadow campaign.

Usage: probe_nested.py SOURCE_CLONE WORKDIR RECEIPT.json ARM...
  ARM is one of TERM, INT, TERM-group, KILL, HUP.
A disposable copy of SOURCE_CLONE (exact head, pinned submodules) keeps the
real driver, owner, tally, selector, the real gptp_shadow Makefile and every
campaign input. In that copy only: every other suite directory is removed, a
`zz_sentinel` suite is added after gptp_shadow, and the slow unrelated
preflight self-tests are replaced by bounded stubs (the campaign never reads
them). The signal is sent while a real compile runs in the campaign's private
scratch. Checks: exit, sentinel, summary, reaped identities, processes naming
the private tree, private tree removal, caller tracked state.
"""
import json, os, shutil, signal, subprocess, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_campaign import (integrity, tree, alive, present, stat_of, referencing, wait_for,  # noqa: E402
                            kill_identity, VERILATOR)

SOURCE = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
RECEIPT = Path(sys.argv[3]).resolve()
ARMS = sys.argv[4:]
COMPILERS = ("cc1plus", "verilator_bin", "g++", "c++")


def prepare(base):
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True)
    repo = base / "repo"
    shutil.copytree(SOURCE, repo, symlinks=True)
    for suite in (repo / "tb/verilator").iterdir():
        if suite.is_dir() and suite.name != "gptp_shadow" and (suite / "Makefile").exists():
            shutil.rmtree(suite)
    probe = base / "probe"
    (probe / "tmp").mkdir(parents=True)
    sentinel = repo / "tb/verilator/zz_sentinel/Makefile"
    sentinel.parent.mkdir()
    sentinel.write_text(f"all:\n\t@echo executed > '{probe}/ran-zz_sentinel'\n\t@echo '1 checks: 1 PASS, 0 FAIL'\n")
    for name in ("check_merge_containment", "check_results_fresh",
                 "xvlog_gate", "check_merge_review_integrity"):
        (repo / f"scripts/{name}.py").write_text("print('bounded prerequisite stub')\n")
    (repo / "syn/yosys/check_list_hermetic.sh").write_text("#!/usr/bin/env bash\nexit 0\n")
    return repo, probe


def arm(name):
    base = WORK / ("nested-" + name)
    repo, probe = prepare(base)
    before = integrity(repo, base / "integrity-before.json")
    env = dict(os.environ)
    for k in ("SUITE_TIMEOUT", "SUITE_SWEEP_LOCK"):
        env.pop(k, None)
    env.update(TMPDIR=str(probe / "tmp"), VERILATOR=VERILATOR, VERILATOR_JOBS="8", PYTHONDONTWRITEBYTECODE="1")
    out = open(probe / "entry.out", "wb")
    p = subprocess.Popen(["bash", str(repo / "scripts/run_all_suites.sh"), str(base / "logs")], cwd=repo, env=env,
                         stdout=out, stderr=subprocess.STDOUT, process_group=0)
    foreign = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(900)"], start_new_session=True)
    foreign_start = stat_of(foreign.pid)["start"]

    def private_dirs():
        return [d for d in (probe / "tmp").iterdir() if d.name.startswith("gptp-shadow-mutants-")]

    def compiling():
        t = tree(p.pid)
        return private_dirs() and any(v["comm"] in COMPILERS for v in t.values())
    assert wait_for(lambda: compiling() or p.poll() is not None, 400), "campaign compile never observed"
    assert p.poll() is None, (probe / "entry.out").read_text()
    time.sleep(1.0)
    census = tree(p.pid)
    private = private_dirs()[0]
    shell = [k for k, v in census.items() if v["comm"] == "bash" and stat_of(k)["ppid"] == p.pid][0]
    rec = dict(arm=name, private=str(private), census={str(k): v for k, v in census.items()},
               census_comms=sorted({v["comm"] for v in census.values()}))
    sig = signal.Signals["SIG" + name.split("-")[0]]
    t0 = time.monotonic()
    if name.endswith("-group"):
        os.killpg(p.pid, sig)
    else:
        fd = os.pidfd_open(p.pid)
        signal.pidfd_send_signal(fd, sig)
        os.close(fd)
    try:
        rec["exit"] = p.wait(timeout=90)
    except subprocess.TimeoutExpired:
        rec["exit"] = "NO-EXIT-90s"
    rec["exit_seconds"] = round(time.monotonic() - t0, 3)
    at_exit = (probe / "entry.out").read_text()
    rec["output_at_exit"] = at_exit[-800:]
    graceful = sig in (signal.SIGINT, signal.SIGTERM)
    rec["shell_gone_within_5s"] = wait_for(lambda: not alive(shell, census[shell]["start"]), 5)
    timeline = [(round(time.monotonic() - t0, 2), alive(foreign.pid, foreign_start))]
    if not graceful:
        # The in-flight suite may finish (documented); wait for it, bounded.
        def done():
            now = alive(foreign.pid, foreign_start)
            if now != timeline[-1][1]:
                timeline.append((round(time.monotonic() - t0, 2), now))
            return not any(alive(k, v["start"]) for k, v in census.items()) and not referencing(private)
        rec["inflight_finished_within_420s"] = wait_for(done, 420)
        time.sleep(3.0)
    timeline.append((round(time.monotonic() - t0, 2), alive(foreign.pid, foreign_start)))
    out.close()
    final = (probe / "entry.out").read_text()
    rec["output_after_exit"] = final[len(at_exit):]
    rec["sentinel_ran"] = (probe / "ran-zz_sentinel").exists()
    rec["summary_printed"] = any(l.startswith("suites:") or l.startswith("logs:") for l in final.splitlines())
    rec["census_live_after"] = {str(k): v["comm"] for k, v in census.items() if alive(k, v["start"])}
    rec["census_zombie_after"] = {str(k): v["comm"] for k, v in census.items()
                                  if present(k, v["start"]) and stat_of(k)["state"] == "Z"}
    rec["processes_referencing_private_after"] = referencing(private)
    rec["private_exists_after"] = private.exists()
    rec["tmp_after"] = sorted(x.name for x in (probe / "tmp").iterdir())
    gs = base / "logs/gptp_shadow.log"
    rec["gptp_shadow_log_tail"] = gs.read_text()[-500:] if gs.exists() else None
    after = integrity(repo, base / "integrity-after.json")
    rec["caller_tracked_state_unchanged"] = before == after
    rec["foreign_untouched"] = alive(foreign.pid, foreign_start)
    rec["foreign_returncode"] = foreign.poll()
    rec["foreign_state"] = stat_of(foreign.pid)
    rec["foreign_timeline"] = timeline
    rec["lock_owner_file_left"] = (repo / ".run_all_suites.lock.owner").exists()
    probs = []
    if rec["sentinel_ran"]:
        probs.append("later suite ran")
    if rec["summary_printed"]:
        probs.append("completed summary")
    if not rec["caller_tracked_state_unchanged"]:
        probs.append("caller tracked state changed")
    if not rec["foreign_untouched"]:
        probs.append("foreign process touched")
    if graceful:
        if rec["exit"] != 128 + sig:
            probs.append(f"exit {rec['exit']}")
        if rec["census_live_after"] or rec["census_zombie_after"] or rec["processes_referencing_private_after"]:
            probs.append("owned processes survived")
        if rec["private_exists_after"] or rec["tmp_after"]:
            probs.append("private work left")
        if rec["lock_owner_file_left"]:
            probs.append("lock owner left")
    else:
        if rec["exit"] != -sig:
            probs.append(f"exit {rec['exit']}")
        if not rec["shell_gone_within_5s"]:
            probs.append("sweep shell outlived entry")
        if rec["output_after_exit"]:
            probs.append("output after caller saw exit")
    rec["problems"] = probs
    for k, v in census.items():
        kill_identity(k, v["start"])
    foreign.kill(); foreign.wait()
    return rec


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    results = json.loads(RECEIPT.read_text()) if RECEIPT.exists() else []
    for name in ARMS:
        rec = arm(name)
        results = [r for r in results if r["arm"] != name] + [rec]
        RECEIPT.write_text(json.dumps(results, indent=1, sort_keys=True) + "\n")
        print(f"nested-{name:11s} exit={rec['exit']!s:5s} t={rec['exit_seconds']:6.2f}s sentinel={rec['sentinel_ran']} "
              f"summary={rec['summary_printed']} live={sorted(rec['census_live_after'].values())} "
              f"private_left={rec['private_exists_after']} tmp={rec['tmp_after']} caller_unchanged={rec['caller_tracked_state_unchanged']} "
              f"inflight_done={rec.get('inflight_finished_within_420s')} problems={rec['problems']}", flush=True)
    bad = [r["arm"] for r in results if r["problems"]]
    print("PROBLEM ARMS (cumulative):", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
