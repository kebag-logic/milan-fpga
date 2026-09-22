"""P4: can the new generic #407 body finding satisfy a pre-existing arm?

For every HEAD arm that is NOT a carrier-script-407 body arm (the 590 base
arms plus the 56 round-1 continue-on-error arms), apply the arm and split
HEAD's findings into those the #407 comparison produced (findings of the
real checker minus findings of the checker with check_carrier_script
stubbed) and the rest. An arm whose expected fragment is matched ONLY by a
generic #407 finding would keep passing if its specialized check were
deleted: the generic comparison would mask that specialized control.

Then, per specialized content check, stub it at BASE and at HEAD and count
the base arms that miss; a lower count at HEAD would be masking.
"""
from __future__ import annotations

import copy
import json
import sys

from common import BASE, HEAD, load_module, world_at

SPECIALIZED = ("check_carrier_gate_step", "check_named_carrier_gate_step",
               "check_scope_step", "check_builder_dependencies",
               "_check_builder_sv2v", "check_env_files", "check_contract_step",
               "check_default_branch_step")


def main() -> int:
    head = load_module(HEAD, "head_p4")
    base = load_module(BASE, "base_p4")
    w0 = world_at(head, HEAD)
    wb = world_at(base, BASE)
    real = head.check
    orig = head.check_carrier_script
    report = {"generic_only_matches": [], "per_function": {}}
    arms = [a for a in head._mutations(w0)
            if not (a[0].startswith("carrier-script-407") and not a[0].endswith("continue-on-error"))]
    report["non_body_arms"] = len(arms)
    for name, mutate, want in arms:
        w = copy.deepcopy(w0)
        mutate(w)
        full = real(w).findings
        head.check_carrier_script = lambda *a, **k: None
        try:
            rest = head.check(w).findings
        finally:
            head.check_carrier_script = orig
        generic = [f for f in full if f not in rest]
        by_rest = any(want in f for f in rest)
        by_generic = any(want in f for f in generic)
        if by_generic and not by_rest:
            report["generic_only_matches"].append(name)
        elif by_generic:
            report.setdefault("matched_by_both", []).append(name)
    # Per specialized function: base arms that miss when it is stubbed.
    base_arms = {n for n, _, _ in base._mutations(wb)}
    for fn in SPECIALIZED:
        counts = {}
        for label, mod, world in (("base", base, wb), ("head", head, w0)):
            if not hasattr(mod, fn):
                counts[label] = "absent"
                continue
            saved = getattr(mod, fn)
            setattr(mod, fn, lambda *a, **k: None)
            try:
                misses = mod._run_mutations(lambda w: mod.check(w).findings, world)
            finally:
                setattr(mod, fn, saved)
            names = sorted(m.split("]")[0][1:] for m in misses)
            counts[label] = sorted(n for n in names if n in base_arms)
        b, h = counts["base"], counts["head"]
        report["per_function"][fn] = {
            "base_arms_missing_at_base": len(b) if isinstance(b, list) else b,
            "base_arms_missing_at_head": len(h) if isinstance(h, list) else h,
            "masked_at_head": sorted(set(b) - set(h)) if isinstance(b, list) and isinstance(h, list) else None,
        }
    json.dump(report, open(sys.argv[1], "w"), indent=1)
    print(json.dumps({k: (v if k != "matched_by_both" else len(v)) for k, v in report.items()}, indent=1))
    bad = report["generic_only_matches"] or any(v["masked_at_head"] for v in report["per_function"].values())
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
