"""Run the in-tree property check (_fuzz_units + _fuzz_check) over a fresh seed range.

usage: python3 -I probe_fuzz.py <torture_campaign.py> <frames> <seed_start> <seed_end> <jobs> <out.json>
Counts violations (any AssertionError from _fuzz_check), verdicts and allowances.
"""
import json
import multiprocessing
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import probe_lib  # noqa: E402

MOD = T = FRAMES = None


def init(path, frames):
    global MOD, T, FRAMES
    MOD = probe_lib.load(path)
    T = probe_lib.case(MOD)
    FRAMES = frames


def one(seed):
    units = T._fuzz_units(FRAMES, seed)
    try:
        verdict, allowed = T._fuzz_check(FRAMES, units)
        return seed, verdict, sorted(allowed), None
    except AssertionError as error:
        return seed, None, [], str(error)[:600]
    except Exception as error:  # a grader crash is also a finding
        return seed, None, [], "EXC " + type(error).__name__ + ": " + str(error)[:500]


def main():
    path, frames, lo, hi, jobs, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), \
        int(sys.argv[5]), sys.argv[6]
    with multiprocessing.Pool(jobs, initializer=init, initargs=(path, frames)) as pool:
        rows = pool.map(one, range(lo, hi), chunksize=16)
    verdicts, allow, bad = {}, {}, []
    for seed, verdict, allowed, error in rows:
        if error:
            bad.append({"seed": seed, "error": error})
            continue
        verdicts[verdict] = verdicts.get(verdict, 0) + 1
        for a in allowed:
            allow[a] = allow.get(a, 0) + 1
    result = {"frames": frames, "seeds": [lo, hi], "verdicts": verdicts, "allowances": allow,
              "violations": len(bad), "first_violations": bad[:20]}
    with open(out, "w") as fh:
        json.dump(result, fh, indent=1, sort_keys=True)
    print(json.dumps({k: result[k] for k in ("frames", "seeds", "verdicts", "allowances", "violations")}))


if __name__ == "__main__":
    main()
