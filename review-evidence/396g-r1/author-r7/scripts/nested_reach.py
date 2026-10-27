"""Grade the nested fuzz family of one planner (<family.py>, its _fuzz_nested) with another planner's grader
(<grader.py>), over a seed range at one capture length: the family planner's checks run with only
_sweep_grade taken from the grader planner.

For each composition: the verdict; whether the excursion's channel is first listed more than 63 samples after the
excursion's first word ("late", R699-6 F1's shape); and the family planner's own _fuzz_check bound, run with the
grader planner grading ("violation").

usage: python3 -I -B nested_reach.py <family.py> <grader.py> <frames> <lo> <hi> <jobs> <out.json>
"""
import json
import multiprocessing
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "r699-6-packet", "scripts"))
import probe_lib  # noqa: E402

FAMILY = GRADER = FRAMES = None


def init(family, grader, frames):
    global FAMILY, GRADER, FRAMES
    import importlib.util
    spec = importlib.util.spec_from_file_location("family_planner", family)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    FAMILY = probe_lib.case(module)
    GRADER = probe_lib.case(probe_lib.load(grader))
    FAMILY._sweep_grade = GRADER._sweep_grade
    FRAMES = frames


def one(seed):
    units = FAMILY._fuzz_nested(FRAMES, seed)
    run = units[0]
    verdict, detail, _ = GRADER._sweep_grade(FRAMES, [event for unit in units for event in unit[4]])
    first = min((e["capture_index"] for e in detail["events"] if e["attribution"] == "dut"
                 and e["channel"] == run[2][0] and e["capture_index"] >= run[1] - 63), default=None)
    late = first is None or first - run[1] > 63
    slip_inside = any(u[0] == "slip" for u in units[1:])
    try:
        FAMILY._fuzz_check(FRAMES, units)
        violation = None
    except AssertionError as error:
        violation = str(error)[:300]
    return {"seed": seed, "verdict": verdict, "late": late, "slip_inside": slip_inside,
            "mask": run[4][0]["mask"], "length": run[3], "violation": violation}


def main():
    family, grader, frames, lo, hi, jobs, out = (sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]),
                                                 int(sys.argv[5]), int(sys.argv[6]), sys.argv[7])
    with multiprocessing.Pool(jobs, initializer=init, initargs=(family, grader, frames)) as pool:
        rows = pool.map(one, range(lo, hi), chunksize=8)
    verdicts = {}
    for row in rows:
        verdicts[row["verdict"]] = verdicts.get(row["verdict"], 0) + 1
    result = {"frames": frames, "seeds": [lo, hi], "verdicts": verdicts,
              "slip_inside": sum(r["slip_inside"] for r in rows),
              "late": sum(r["late"] for r in rows), "late_seeds": [r for r in rows if r["late"]][:20],
              "violations": sum(1 for r in rows if r["violation"]),
              "violation_rows": [r for r in rows if r["violation"]][:20]}
    with open(out, "w") as fh:
        json.dump(result, fh, indent=1, sort_keys=True)
    print(json.dumps({k: result[k] for k in ("frames", "seeds", "verdicts", "slip_inside", "late", "violations")}))


if __name__ == "__main__":
    main()
