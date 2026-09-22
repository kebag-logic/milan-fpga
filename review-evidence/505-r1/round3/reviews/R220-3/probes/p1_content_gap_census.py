#!/usr/bin/env python3
"""p1 (R220-3): content-gap census over every `run:` step of the four
workflow files, at the tree given by --root (a disposable `git archive`
copy of the head under review).

For each run step, content levers are applied on an in-memory copy of the
parsed world and the real `check()` of that tree's scripts/ci_events.py is
called. A lever is ACCEPTED when check() returns no finding, i.e. that
content edit would leave `ci_events.py --check` green.

Levers (applied to the step's normalized lines, re-joined with LF; a
whitespace-only re-join is reported separately as the reformat control):
  true           body replaced by `true`
  append         `echo r220-tamper` appended as a new last line
  prepend        `set +e` prepended as a new first line
  or-true-N      ` || true` appended to normalized line N
  drop-N         normalized line N deleted (multi-line bodies only)
  sub-N          normalized line N replaced by `true`
  swap-N         lines N and N+1 swapped (distinct adjacent lines only)
Plus, for any line equal to `exit 1`, `exit1-to-true-N` (line -> `true`,
same as sub-N but named for the F3 edit).

Output: JSON with one record per run step: file, job, index, name, class,
number of levers, accepted lever names, reformat-control result.
Class is `carrier` (docs.yml / elaborate.yml), `rtl7` (RTL_STEP_LISTS
jobs), `sibling` (RTL_SIBLING_STEP_LISTS jobs and the fast verdict).
"""
import argparse
import copy
import json
import sys

sys.dont_write_bytecode = True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    sys.path.insert(0, f"{args.root}/scripts")
    import ci_events as ce  # noqa: E402  (the tree under test)
    import pathlib

    pristine = ce.parse_world(ce.read_tree(pathlib.Path(args.root)))
    base = ce.check(pristine)
    assert not base.findings, base.findings
    rtl7 = set(ce.RTL_STEP_LISTS)
    sibling = set(ce.RTL_SEQUENCE_PINS) - rtl7

    def classify(path, jid):
        if path in (ce.DOCS, ce.ELABORATE):
            return "carrier"
        if (path, jid) in rtl7:
            return "rtl7"
        if (path, jid) in sibling:
            return "sibling"
        return "unrecorded"

    def accepted(path, jid, idx, body):
        world = copy.deepcopy(pristine)
        ce.jobs(world[path])[jid]["steps"][idx]["run"] = body
        return not ce.check(world).findings

    records = []
    for path in ce.WORKFLOWS:
        for jid, job in ce.jobs(pristine[path]).items():
            raw_steps = job.get("steps") or []
            for idx, step in enumerate(raw_steps):
                if not isinstance(step, dict) or not isinstance(step.get("run"), str):
                    continue
                lines = ce.normalize_script(step["run"])
                join = lambda ls: "\n".join(ls) + "\n"  # noqa: E731
                levers = [("true", join(["true"])),
                          ("append", join(lines + ["echo r220-tamper"])),
                          ("prepend", join(["set +e"] + lines))]
                for n, line in enumerate(lines, 1):
                    levers.append((f"or-true-{n}", join(
                        lines[:n - 1] + [line + " || true"] + lines[n:])))
                    if len(lines) > 1:
                        levers.append((f"drop-{n}", join(lines[:n - 1] + lines[n:])))
                    levers.append((f"sub-{n}", join(lines[:n - 1] + ["true"] + lines[n:])))
                    if line == "exit 1":
                        levers.append((f"exit1-to-true-{n}", join(
                            lines[:n - 1] + ["true"] + lines[n:])))
                    if n < len(lines) and lines[n] != line:
                        sw = list(lines)
                        sw[n - 1], sw[n] = sw[n], sw[n - 1]
                        levers.append((f"swap-{n}", join(sw)))
                acc = [name for name, body in levers
                       if accepted(path, jid, idx, body)]
                records.append({
                    "file": path, "job": jid, "step": idx + 1,
                    "name": step.get("name"), "class": classify(path, jid),
                    "normalized_lines": len(lines),
                    "levers": len(levers), "accepted": acc,
                    "reformat_control_clean": accepted(path, jid, idx, join(lines)),
                })
    summary = {}
    for r in records:
        s = summary.setdefault(r["class"], {"run_steps": 0, "fully_refused": 0,
                                            "some_accepted": 0, "all_accepted": 0})
        s["run_steps"] += 1
        if not r["accepted"]:
            s["fully_refused"] += 1
        elif len(r["accepted"]) == r["levers"]:
            s["all_accepted"] += 1
        else:
            s["some_accepted"] += 1
    out = {"root": args.root, "pristine_items": base.checked,
           "summary": summary, "steps": records}
    pathlib.Path(args.out).write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(summary, indent=1))
    for r in records:
        if r["accepted"] and r["class"] != "rtl7":
            print("NON-RTL7 ACCEPTS:", r["file"], r["job"], r["step"], r["name"],
                  f"{len(r['accepted'])}/{r['levers']}", r["accepted"])


if __name__ == "__main__":
    main()
