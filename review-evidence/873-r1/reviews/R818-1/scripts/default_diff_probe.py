"""Differential probe: the base and head runners on the same default command lines.

Loads one act_ci.py (argv[1]) as a module, against the shipping worktree argv[2],
and prints JSON: for each case the act command the runner builds (ports, temp
paths and tokens normalised), the replay concurrency over the shipping workflows,
the selected ranges, and every --cpu-ranges refusal text. Run once per runner
and diff the two outputs. Usage: python3 -I default_diff_probe.py <act_ci.py> <worktree> [extra argv...]
"""
import contextlib, contextvars, dataclasses, importlib.util, json, os, pathlib, re, sys
from unittest import mock

path, worktree, extra = sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3:]
spec = importlib.util.spec_from_file_location("act_ci_probe", path)
m = importlib.util.module_from_spec(spec)
sys.modules["act_ci_probe"] = m
spec.loader.exec_module(m)

def fake(tp):
    vals = {}
    for f in dataclasses.fields(tp):
        if f.default is not dataclasses.MISSING or f.default_factory is not dataclasses.MISSING:
            continue
        name = f.name
        vals[name] = 1 if "number" in name else ("a" * 40 if "sha" in name or "oid" in name else "x")
    return tp(**vals)

out = {}
def refusal(fn):
    try:
        return ["ok", fn()]
    except m.Refusal as exc:
        return ["REFUSED", str(exc)]

with mock.patch.object(os, "cpu_count", return_value=128):
    parser = m.build_argument_parser()
    cases = {
        "4x16": "0-15,16-31,32-47,48-63",
        "4x12 fallback": "0-11,12-23,24-35,36-47",
        "mixed 16+12": "0-15,24-35",
        "one range": "0-15",
        "8x16 booked": "0-15,16-31,32-47,48-63,64-79,80-95,96-111,112-127",
    }
    for item in filter(None, os.environ.get("PROBE_RANGES", "").split(";")):
        label, ranges = item.split("=", 1)
        cases[label] = ranges
    bad = [None, "", "0-7", "0-5", "1-16", "0-15,12-23", "0-15,0-15", "128-143", "00-15", "0-15,", "-1-14",
           "0-7,8-15", "12-17", "0-31", "4-15"] + [x for x in os.environ.get("PROBE_BAD", "").split(";") if x]
    pr = fake(m.PullRequest)
    for label, ranges in cases.items():
        argv = ["--pr", "1", "--cpu-ranges", ranges, *extra]
        args = parser.parse_args(argv)
        ctx = contextvars.copy_context()
        def body():
            if hasattr(m, "JOB_GEOMETRY"):
                m.JOB_GEOMETRY.set(m.job_geometry_arguments(args.jobs, args.job_cpus, args.job_memory))
            m.BOOKED_CPU_RANGES.set(m.parse_cpu_ranges(args.cpu_ranges))
            conc = m.replay_container_concurrency(worktree, tuple(m.WORKFLOWS))
            sel = refusal(lambda: list(m.job_cpu_ranges(0, conc)))
            with m.temporary_run_directory(False) as root:
                layout = m.make_layout(root, pr)
                fx = m.selftest_docker_fixture(layout)
                cmd = m.build_act_command(["act"], "rtl-full", layout, fx.port, fx.boundary)
                text = " ".join(cmd).replace(str(root), "<ROOT>").replace(str(fx.port), "<PORT>")
            return {"concurrency": conc, "selected": sel, "command": text}
        out[label] = refusal(lambda: ctx.run(body))
    for raw in bad:
        args = parser.parse_args(["--pr", "1", *extra] + ([] if raw is None else ["--cpu-ranges", raw]))
        ctx = contextvars.copy_context()
        def body2():
            if hasattr(m, "JOB_GEOMETRY"):
                m.JOB_GEOMETRY.set(m.job_geometry_arguments(args.jobs, args.job_cpus, args.job_memory))
            return list(m.parse_cpu_ranges(args.cpu_ranges))
        out["ranges " + repr(raw)] = refusal(lambda: ctx.run(body2))
    oom = m.SlotMemory.__dataclass_fields__ if hasattr(m.SlotMemory, "__dataclass_fields__") else {}
print(json.dumps(out, indent=1, sort_keys=True))
