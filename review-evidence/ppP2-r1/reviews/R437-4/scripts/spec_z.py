# R437-4: the Z plants as the head's figures gate carries them
# (tb/nvm_port/deadline_rows.py DRAIN_PLANTS, read from the exact head by
# git show in the --repo clone, so this run is independent of the gate's driver),
# under pristine and coincident completion at 100, 37 and 20, and the
# randomized harness at 1, 2, 3 and 37.
import subprocess, types
_src = subprocess.run(["git", "-C", REPO, "show",
                       "3957814550f164d72bfaad5d28cd0e7cac0ecaaf:tb/nvm_port/deadline_rows.py"],
                      check=True, capture_output=True, text=True).stdout
_m = types.ModuleType("deadline_rows_head")
exec(compile(_src, "deadline_rows.py", "exec"), _m.__dict__)
PROBES = {}
for _name, _pairs in _m.DRAIN_PLANTS:
    if _name.startswith("Z"):
        PROBES[_name] = [("RTL", o, n) for o, n in _pairs]
RUNS = []
for _p in list(PROBES):
    for _mdl in ("pristine", "coincident completion"):
        for _t in (100, 37, 20):
            RUNS.append((_p, _mdl, _t))
    for _t in (1, 2, 3, 37):
        RUNS.append(("FZ:" + _p, "pristine", _t))
PROBES.update({"FZ:" + k: v for k, v in list(PROBES.items())})
