#!/usr/bin/env python3
"""Focused receipt, argument, and workflow-accounting probes; no source edits or full banks."""
import contextlib, copy, importlib.util, io, json, os, pathlib, subprocess, sys, tempfile
sys.dont_write_bytecode = True
ROOT = pathlib.Path(sys.argv[1]).resolve()
OUT = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("isolation", ROOT / "scripts/ci_toolcache_isolation.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
rows = []
def record(case, **values):
    rows.append({"case": case, **values})
    print("PASS", case)
with tempfile.TemporaryDirectory(dir=OUT / "scratch", prefix="delta-") as tmp:
    tmp = pathlib.Path(tmp)
    good = {"gates": [{"gate": g, "verdict": "pass", "not_run": []} for g in m.GATES]}
    receipt = tmp / "receipt.json"
    def judge(case, payload, rc=0, refusal=True):
        if payload is None:
            receipt.unlink(missing_ok=True)
        else:
            receipt.write_text(json.dumps(payload))
        status, problems = m.checks("probe", rc, receipt)
        assert bool(problems) == refusal, (case, status, problems)
        record(case, status=status, problems=problems)
        return status, problems
    judge("complete receipt", good, refusal=False)
    for gate in m.GATES:
        data = copy.deepcopy(good)
        next(r for r in data["gates"] if r["gate"] == gate)["not_run"] = [["arm", "missing litex_boards", "no_litex"]]
        status, problems = judge("NOT RUN " + gate, data)
        assert any(gate in p and "missing litex_boards" in p for p in problems)
        data["gates"] = [r for r in data["gates"] if r["gate"] != gate]
        _, problems = judge("missing check " + gate, data)
        assert any(gate in p for p in problems)
    judge("missing receipt", None)
    judge("nonzero exit despite complete receipt", good, rc=7)
    receipt.write_text("{")
    try:
        m.checks("probe", 0, receipt)
    except json.JSONDecodeError:
        record("malformed receipt refuses with error")
    else:
        raise AssertionError("malformed receipt passed")
    home = tmp / "home"
    home.mkdir()
    real_receipt = OUT / "missing-dependency-driver.json"
    real_receipt.unlink(missing_ok=True)
    env = dict(os.environ, HOME=str(home), PYTHONDONTWRITEBYTECODE="1")
    for k in ("MILAN_LITEX_PYTHON", "PYTHONPATH", "PYTHONHOME"):
        env.pop(k, None)
    run = subprocess.run([sys.executable, "-B", str(ROOT / "sw/builder/test_builder.py"),
                          "--gates", ",".join(m.GATES), "--receipt", str(real_receipt)],
                         cwd=ROOT, env=env, capture_output=True, text=True)
    (OUT / "missing-dependency-driver.log").write_text(run.stdout + run.stderr)
    assert run.returncode == 0, run.stderr
    status, problems = m.checks("missing-dependency", run.returncode, real_receipt)
    assert all(status[g].startswith("NOT RUN:") for g in m.GATES), status
    assert all(any(g in p for p in problems) for g in m.GATES), problems
    record("real selected builder checks: exit zero but named NOT RUN refusal", status=status, problems=problems)
    saved = sys.argv
    for absolute in (False, True):
        def form(name):
            p = tmp / name
            return str(p) if absolute else os.path.relpath(p)
        (tmp / "sdk").mkdir(exist_ok=True)
        sys.argv = [str(ROOT / "scripts/ci_toolcache_isolation.py"),
                    "--python", form("python"), "--work", form("work"),
                    "--pip-cache", form("pip"), "--report", form("report.json"),
                    "--rv32-sdk", form("sdk"), "--tool-dir", form("tools"), "--gate-legs"]
        args = m.arguments()
        for key in ("python", "work", "pip_cache", "report", "rv32_sdk"):
            assert getattr(args, key).is_absolute(), key
        assert all(p.is_absolute() for p in args.tool_dir)
        assert args.work == tmp / "work"
        assert args.rev == "2e83841675e4e1439c413c9ca11b4a123898a60e"
        record("argument boundary " + ("absolute" if absolute else "relative"), all_paths_absolute=True, rev=args.rev)
    sys.argv = saved
    for absolute in (False, True):
        work = tmp / ("bad-abs" if absolute else "bad-rel")
        arg = str(work) if absolute else os.path.relpath(work)
        run = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/ci_toolcache_isolation.py"),
                              "--python", "missing-python", "--work", arg, "--rev", "nonexistent-r637-ref"],
                             capture_output=True, text=True, cwd=ROOT)
        assert run.returncode == 2 and "not a commit" in run.stderr and not work.exists()
        record("actual CLI bad revision with " + ("absolute" if absolute else "relative") + " --work", rc=run.returncode, no_work_created=True)
    jobs = m.yaml.safe_load((ROOT / m.WORKFLOW).read_text())["jobs"]
    for name in m.LEGS:
        job = jobs[name]
        assert m.PRIVATE_STEP in [s["name"] for s in m.window(job, False)]
        assert m.PRIVATE_STEP not in [s["name"] for s in m.window(job, True)]
        assert any(s["name"].startswith("Elaboration gates, leg ") for s in m.tail(job))
        for section, selector, target in (("setup", lambda j:m.window(j, False), m.LAST_STEP),
                                         ("tail", m.tail, m.BUDGET_STEP)):
            bad = copy.deepcopy(job)
            next(s for s in bad["steps"] if s.get("name") == target)["run"] = True
            try:
                selector(bad)
            except ValueError as e:
                assert target in str(e)
                record(name + " nontext " + section + " named refusal")
            else:
                raise AssertionError("nontext script accepted")
        record(name + " current setup, shared control, and tail accounted", modules=m.modules(job))
    current = (ROOT / m.WORKFLOW).read_bytes()
    old = subprocess.check_output(["git", "show", "c48bfe38:" + m.WORKFLOW], cwd=ROOT)
    assert old == current
    record("generated workflow byte-identical to previously reviewed head")
(OUT / "probe-delta.json").write_text(json.dumps(rows, indent=2) + "\n")
print(f"PASS: {len(rows)} focused checks")
