"""R272-5: dump the mutation table's labels and pins, and the accepted-case
labels, at the mutation-loop hook (probe_gate1b.py --anchor mutations), to
R272_LABELS_OUT, so two heads' tables can be compared entry by entry.
Grades nothing; returns no cases."""
import json
import os


def _pin(value):
    return list(value) if isinstance(value, tuple) else value


def cases(ns):
    table = [{"label": m[0], "pin": _pin(m[4]) if len(m) > 4 else None}
             for m in ns["mutations"]]
    out = {"mutations": table,
           "accepted": sorted(ns["accepted_cases"]),
           "subset_refusal_corpus": [e[0] for e in
                                     ns.get("subset_refusal_corpus", ())]}
    with open(os.environ["R272_LABELS_OUT"], "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, default=str)
    print(f"LABELS {len(table)} mutations, {len(out['accepted'])} accepted",
          flush=True)
    return ()
