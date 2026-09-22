"""P2: arm populations across base, round-1 head and HEAD.

* every base arm and every round-1 arm is still present at HEAD with the
  same expected fragment and the same mutation effect on the (identical)
  workflow world;
* labels are unique at each revision;
* HEAD's new #407 arms are exactly the per-line swallowing arms for every
  non-last line, one appended command per body and one reorder per
  multi-command body, each reason-pinned to job, step number, step name,
  line number and expected text, and each edit equal to an independently
  computed edit of the live body;
* the AC5 edit (docs-check step 34 line 1 `|| true`) and every bounded
  `--check` line has its own arm;
* every HEAD arm bites the real HEAD checker.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from collections import Counter

from common import BASE, HEAD, R1, load_module, world_at


def _canon(obj):
    """JSON-safe canonical form: PyYAML reads `on:` as True, so keys are
    rendered with repr to keep bool and str keys distinct and sortable."""
    if isinstance(obj, dict):
        return {repr(k): _canon(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_canon(v) for v in obj]
    return obj


def world_digest(world) -> str:
    return hashlib.sha256(json.dumps(_canon(world), sort_keys=True, default=repr)
                          .encode()).hexdigest()


def arms_of(mod, world):
    out = {}
    names = Counter()
    for name, mutate, want in mod._mutations(world):
        names[name] += 1
        w = copy.deepcopy(world)
        mutate(w)
        out[name] = (want, world_digest(w))
    dup = [n for n, k in names.items() if k > 1]
    return out, dup


def main() -> int:
    report = {}
    problems = []
    mods = {rev: load_module(rev) for rev in (BASE, R1, HEAD)}
    head = mods[HEAD]
    # The workflow files are byte-identical at the three revisions; each
    # module still derives its arms from its own revision's world.
    worlds = {rev: world_at(mods[rev], rev) for rev in mods}
    for rev in (BASE, R1):
        a = {k: v for k, v in worlds[rev].items() if k != head.POLICY}
        b = {k: v for k, v in worlds[HEAD].items() if k != head.POLICY}
        assert a == b, f"workflow worlds differ at {rev}"
    arms = {}
    for rev in mods:
        arms[rev], dup = arms_of(mods[rev], worlds[rev])
        report[f"arms_{rev[:8]}"] = len(arms[rev])
        report[f"duplicate_labels_{rev[:8]}"] = dup
        if dup:
            problems.append(f"duplicate labels at {rev[:8]}: {dup}")
    # For effect comparison use HEAD's world for all revisions: identical
    # workflows, and only the policy text differs, which no #407 arm edits.
    for rev in (BASE, R1):
        missing = sorted(set(arms[rev]) - set(arms[HEAD]))
        changed_want = sorted(n for n in set(arms[rev]) & set(arms[HEAD])
                              if arms[rev][n][0] != arms[HEAD][n][0])
        report[f"{rev[:8]}_arms_missing_at_head"] = missing
        report[f"{rev[:8]}_arms_with_changed_want"] = changed_want
        if missing or changed_want:
            problems.append(f"{rev[:8]} arms missing/changed at HEAD: "
                            f"{len(missing)}/{len(changed_want)}")
    # Mutation effect equality, evaluated on one common world.
    common_world = worlds[HEAD]
    eff = {}
    for rev in mods:
        eff[rev] = {}
        for name, mutate, want in mods[rev]._mutations(worlds[rev]):
            w = copy.deepcopy(common_world)
            try:
                mutate(w)
            except Exception as exc:  # noqa: BLE001
                eff[rev][name] = f"raised {exc!r}"
                continue
            # Compare only what the four workflow files became.
            eff[rev][name] = world_digest({k: v for k, v in w.items()
                                           if k != head.POLICY})
    for rev in (BASE, R1):
        diff = sorted(n for n in eff[rev] if n in eff[HEAD]
                      and eff[rev][n] != eff[HEAD][n])
        report[f"{rev[:8]}_arms_with_changed_effect"] = diff
        if diff:
            problems.append(f"{rev[:8]} arms with changed edit: {diff[:5]}")

    # New arms at HEAD relative to round 1.
    new = sorted(set(arms[HEAD]) - set(arms[R1]))
    new_r1 = sorted(set(arms[R1]) - set(arms[BASE]))
    report["new_at_r1"] = len(new_r1)
    report["new_at_head"] = len(new)
    levers = Counter(re.sub(r"^carrier-script-407 \S+ step \d+ ", "", n)
                     .split("-line-")[0] for n in new)
    report["new_at_head_by_lever"] = dict(levers)
    report["new_at_r1_by_lever"] = dict(Counter(
        re.sub(r"^carrier-script-407 \S+ step \d+ ", "", n) for n in new_r1))

    # Independent expected population at HEAD.
    expected_new = {}
    by_line_arm = {}
    for path, jids in ((head.DOCS, ("docs-check", "wire-accountability",
                                    "docs-check-no-git")),
                       (head.ELABORATE, ("elaborate",))):
        for jid in jids:
            for at, step in enumerate(common_world[path]["jobs"][jid]["steps"]):
                if not isinstance(step.get("run"), str):
                    continue
                lines = head.normalize_script(step["run"])
                what = f"job `{jid}` step {at + 1} (`{step['name']}`)"
                label = f"carrier-script-407 {jid} step {at + 1}"
                for k in range(len(lines) - 1):
                    edited = list(lines)
                    edited[k] = lines[k] + " || true"
                    expected_new[f"{label} or-true-line-{k + 1}"] = (
                        f"{what} script is not the canonical form: line {k + 1} "
                        f"must be {lines[k]!r}", "\n".join(edited), (path, jid, at))
                    by_line_arm[(jid, at + 1, k + 1)] = f"{label} or-true-line-{k + 1}"
                by_line_arm[(jid, at + 1, len(lines))] = f"{label} or-true"
                expected_new[f"{label} append-command"] = (
                    f"{what} script is not the canonical form: line {len(lines) + 1} "
                    f"must be None", "\n".join((*lines, "echo appended")), (path, jid, at))
                for k in range(len(lines) - 1):
                    if lines[k] != lines[k + 1]:
                        edited = list(lines)
                        edited[k], edited[k + 1] = edited[k + 1], edited[k]
                        expected_new[f"{label} reorder-lines"] = (
                            f"{what} script is not the canonical form: line {k + 1} "
                            f"must be {lines[k]!r}", "\n".join(edited), (path, jid, at))
                        break
    report["expected_new_population"] = len(expected_new)
    if set(expected_new) != set(new):
        problems.append("new-arm population differs from the independent "
                        f"expectation: extra={sorted(set(new) - set(expected_new))[:5]} "
                        f"missing={sorted(set(expected_new) - set(new))[:5]}")
    # Each new arm: same expected fragment and same edit as computed here.
    head_arms = {n: (m, w) for n, m, w in head._mutations(common_world)}
    for name, (want, run, (path, jid, at)) in expected_new.items():
        if name not in head_arms:
            continue
        mutate, got_want = head_arms[name]
        if got_want != want:
            problems.append(f"{name}: want {got_want!r} != {want!r}")
        w = copy.deepcopy(common_world)
        mutate(w)
        step = w[path]["jobs"][jid]["steps"][at]
        if step.get("run") != run:
            problems.append(f"{name}: edit differs")
        # Only that step's run changed.
        w2 = copy.deepcopy(w)
        w2[path]["jobs"][jid]["steps"][at]["run"] = common_world[path]["jobs"][jid]["steps"][at]["run"]
        if w2 != common_world:
            problems.append(f"{name}: edit touches more than one step's run")
    # Line completeness: every normalized line of every body has a swallowing arm.
    line_total = len(by_line_arm)
    have = sum(1 for n in by_line_arm.values() if n in arms[HEAD])
    report["line_swallow_arms_expected"] = line_total
    report["line_swallow_arms_present"] = have
    if have != line_total:
        problems.append(f"line-complete swallowing: {have}/{line_total}")
    # AC5 arm and bounded --check arms.
    ac5 = "carrier-script-407 docs-check step 34 or-true-line-1"
    report["ac5_arm"] = {"name": ac5, "present": ac5 in arms[HEAD],
                         "want": arms[HEAD].get(ac5, (None,))[0]}
    mutate, _ = head_arms[ac5]
    w = copy.deepcopy(common_world)
    mutate(w)
    report["ac5_arm"]["edited_run"] = w[head.DOCS]["jobs"]["docs-check"]["steps"][33]["run"]
    report["ac5_arm"]["present_at_r1"] = ac5 in arms[R1]
    check_lines = {}
    for (jid, stepno, lineno), name in sorted(by_line_arm.items()):
        step = common_world[head.DOCS if jid != "elaborate" else head.ELABORATE]["jobs"][jid]["steps"][stepno - 1]
        line = head.normalize_script(step["run"])[lineno - 1]
        if re.search(r" --check(?= |$)", line):
            check_lines[f"{jid} step {stepno} line {lineno}"] = {
                "line": line, "arm": name, "present_at_head": name in arms[HEAD],
                "present_at_r1": name in arms[R1]}
    report["bounded_check_lines"] = check_lines
    if not all(v["present_at_head"] for v in check_lines.values()):
        problems.append("a --check line lacks a swallowing arm")
    # Every HEAD arm bites the real HEAD checker (independent re-run).
    misses = head._run_mutations(lambda w: head.check(w).findings, common_world)
    report["head_arm_misses_real_checker"] = misses
    if misses:
        problems.append(f"{len(misses)} HEAD arms miss the real checker")
    report["problems"] = problems
    json.dump(report, open(sys.argv[1], "w"), indent=1, default=str)
    short = {k: v for k, v in report.items() if k not in ("bounded_check_lines",)}
    print(json.dumps(short, indent=1, default=str)[:6000])
    print("bounded --check lines:")
    for k, v in check_lines.items():
        print(f"  {k}: {v['arm']} head={v['present_at_head']} r1={v['present_at_r1']}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
