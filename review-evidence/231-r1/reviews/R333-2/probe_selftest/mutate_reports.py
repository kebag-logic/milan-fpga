#!/usr/bin/env python3
"""Mutate pp_baseline_rank.py / pp_baseline_mapping.py copies and run
pp_baseline_reports_selftest.py against each mutant.

usage: mutate_reports.py <syn/ooc directory> <workdir>
A mutant that still passes marks accounting the report self-test does not guard.
"""
import shutil
import subprocess
import sys
from pathlib import Path

MUTANTS = {
    "rank-non_additive_storage_check_dropped": ("pp_baseline_rank.py",
        '        if any(adjustment[field] for field in ("FF", "RAMB36", "RAMB18", "DSP")):\n',
        "        if False:\n"),
    "rank-own_row_not_renamed": ("pp_baseline_rank.py",
        '            name = "@own"\n', "            pass\n"),
    "rank-duplicate_row_refusal_dropped": ("pp_baseline_rank.py",
        "        if key in rows:\n", "        if False:\n"),
    "rank-ff_rank_uses_lut_order": ("pp_baseline_rank.py",
        "FF_rank=ff_order.index(key) + 1,", "FF_rank=position,"),
    "rank-missing_parent_refusal_dropped": ("pp_baseline_rank.py",
        "        if not children or parent not in rows:\n", "        if False:\n"),
    "mapping-blackbox_exclusion_dropped": ("pp_baseline_mapping.py",
        '               for flag in ("blackbox", "whitebox")):\n',
        '               for flag in ()):\n'),
    "mapping-multiplicity_dropped": ("pp_baseline_mapping.py",
        '            result.update(total(cell["type"]))\n',
        '            result.update(set(total(cell["type"])))\n'),
    "mapping-residual_row_dropped": ("pp_baseline_mapping.py",
        "    rows.append(dict(instance=\"@flattening_residual\", hierarchical_Yosys=flat - hierarchical_total,\n",
        "    rows.append(dict(instance=\"@flattening_residual\", hierarchical_Yosys=0,\n"),
    "mapping-lut_filter_includes_all": ("pp_baseline_mapping.py",
        'if re.fullmatch(r"LUT[1-6]", primitive))', 'if True)'),
}


def main() -> None:
    """Run the pristine report self-test, then each mutant copy."""
    source, work = Path(sys.argv[1]), Path(sys.argv[2])
    rows = []
    for name, change in [("pristine", None), *MUTANTS.items()]:
        target = work / name
        shutil.copytree(source, target, ignore=shutil.ignore_patterns("__pycache__"))
        if change is not None:
            filename, old, new = change
            path = target / filename
            text = path.read_text()
            if text.count(old) != 1:
                rows.append(f"{name}\tNOT-APPLIED (count {text.count(old)})")
                continue
            path.write_text(text.replace(old, new))
        result = subprocess.run([sys.executable, "-B", "pp_baseline_reports_selftest.py"],
                                cwd=target, capture_output=True, text=True, timeout=120)
        verdict = ("selftest PASS (mutant survives)" if result.returncode == 0
                   else "selftest FAIL (mutant killed)")
        if change is None:
            verdict = f"rc={result.returncode}"
        rows.append(f"{name}\t{verdict}")
    shutil.rmtree(work)
    print("\n".join(rows))


if __name__ == "__main__":
    main()
