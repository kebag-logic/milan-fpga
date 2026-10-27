"""Check every unit probe_reach.py reports against the round-8 coverage rule, independently of the planner.

A unit is covered on a channel when some DUT listing on that channel has a sample span overlapping
[first word - 63, last word + 63]. The span is the one probe_reach.py prints: located_within, or the listed
sample, widened to the listing's words for every class but dropped and repeated. The rule's third clause:
a unit inside a constant-mask excursion on the same channel may be covered by that excursion's listing alone,
so each covered unit is also classed by what covers it:

- "own": a covering listing begins within [first - 63, last + 63] (never the case for a reported unit);
- "excursion": a covering listing on the excursion's channel also covers the excursion's words;
- "other": covered, by neither.

usage: python3 -I classify_reach.py <reach.jsonl>...
Prints one JSON summary per file; "uncovered" must be 0.
"""
import json
import sys

GUARD = 63


def overlaps(span, low, high):
    return span[0] <= high and span[1] >= low


def classify(row):
    units = row["units"]
    first, last = row["at"], row["at"] + row["n"] - 1
    low, high = first - GUARD, last + GUARD
    covering = [r for r in row["reaching"] if overlaps(r[3], low, high)]
    if not covering:
        return "uncovered"
    if any(low <= r[3][0] <= high for r in covering):
        return "own"
    kind, at, chans, n = units[0]
    inside = kind == "run" and row["channel"] in chans and at <= first and last <= at + n - 1 and row["unit"] != 0
    if inside and any(overlaps(r[3], at, at + n - 1) for r in covering):
        return "excursion"
    return "other"


def main():
    for path in sys.argv[1:]:
        counts, kinds, verdicts = {}, {}, {}
        with open(path) as fh:
            for line in fh:
                row = json.loads(line)
                if row.get("summary"):
                    reported = row["units_reached_only_by_a_listing_starting_before_first_minus_63"]
                    continue
                cls = classify(row)
                counts[cls] = counts.get(cls, 0) + 1
                kinds[f"{cls}:{row['kind']}"] = kinds.get(f"{cls}:{row['kind']}", 0) + 1
                verdicts[row["verdict"]] = verdicts.get(row["verdict"], 0) + 1
        print(json.dumps({"file": path.rsplit("/", 1)[-1], "reported": reported,
                          "uncovered": counts.get("uncovered", 0), "covered_by": counts,
                          "by_kind": dict(sorted(kinds.items())), "verdicts": verdicts}, sort_keys=True))


if __name__ == "__main__":
    main()
