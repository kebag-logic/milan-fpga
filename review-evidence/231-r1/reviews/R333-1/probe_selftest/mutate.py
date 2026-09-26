#!/usr/bin/env python3
"""Apply one named mutation to a copy of syn/ooc/pp_baseline.py and run --selftest.

usage: mutate.py <pristine pp_baseline.py> <workdir>
Each mutant removes one enforcement point; a mutant that still passes the
self-test marks enforcement the self-test does not guard.
"""
import shutil
import subprocess
import sys
from pathlib import Path

MUTANTS = {
    "drop_rom_error_promotion": ("    prefix += ROM_ERROR\n", "    pass\n"),
    "drop_readmemh_set_check": (
        "    if expected != {Path(row[\"path\"]).name for row in inputs}:\n",
        "    if False:\n"),
    "skip_param_rom_geometry": (
        "        inputs.append(image_record(Path(matches[0]), count,\n",
        "        inputs.append(image_record(Path(matches[0]), None,\n"),
    "drop_output_outside_repo_check": (
        "    if output.is_relative_to(root):\n", "    if False:\n"),
    "control_width_check_removed": (
        "    if width is not None and any(len(word) != (width + 3) // 4 for word in tokens):\n",
        "    if False:\n"),
}


def main() -> None:
    """Run the pristine self-test and every mutant; print pass/fail rows."""
    pristine, work = Path(sys.argv[1]), Path(sys.argv[2])
    work.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, (old, new) in [("pristine", (None, None)), *MUTANTS.items()]:
        text = pristine.read_text()
        if old is not None:
            if text.count(old) != 1:
                rows.append(f"{name}\tNOT-APPLIED")
                continue
            text = text.replace(old, new)
        target = work / name / "syn" / "ooc" / "pp_baseline.py"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
        r = subprocess.run([sys.executable, "-B", str(target), "--selftest"],
                           capture_output=True, text=True)
        verdict = "selftest PASS (mutant survives)" if r.returncode == 0 else "selftest FAIL (mutant killed)"
        if name == "pristine":
            verdict = f"rc={r.returncode}"
        rows.append(f"{name}\t{verdict}")
    shutil.rmtree(work)
    print("\n".join(rows))


if __name__ == "__main__":
    main()
