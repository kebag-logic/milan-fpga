# R437-4: the round-3 drain plants on the randomized harness at bound 2, the one
# built bound spec_drain.py's harness runs (1, 3 and 37) leave out. The plant
# texts are spec_drain.py's, imported unchanged.
import os
_ns = {}
exec(open(os.path.join(os.path.dirname(os.path.abspath(SPEC_PATH)), "spec_drain.py")).read(), _ns)
PROBES = {k: v for k, v in _ns["PROBES"].items() if k.startswith("FZ:")}
RUNS = [(p, "pristine", 2) for p in PROBES]
