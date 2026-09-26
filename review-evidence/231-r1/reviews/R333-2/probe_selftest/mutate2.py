#!/usr/bin/env python3
"""Apply one named mutation to a copy of syn/ooc/pp_baseline.py and run --selftest.

usage: mutate2.py <pristine pp_baseline.py> <workdir>
Round-1 mutants (R1-*) are repeated unchanged. Round-2 mutants (R2-*) remove
further enforcement the page or recipe claims: generated-ROM and
parameter-ROM geometry, ambiguity refusals, directory and endpoint guards,
and the unfiltered hierarchy report. A mutant that still passes the
self-test marks enforcement the self-test does not guard.
"""
import shutil
import subprocess
import sys
from pathlib import Path

MUTANTS = {
    "R1-drop_rom_error_promotion": ("    prefix += ROM_ERROR\n", "    pass\n"),
    "R1-drop_readmemh_set_check": (
        "    if expected != {Path(row[\"path\"]).name for row in inputs}:\n",
        "    if False:\n"),
    "R1-skip_param_rom_geometry": (
        "        inputs.append(image_record(Path(matches[0]), count,\n",
        "        inputs.append(image_record(Path(matches[0]), None,\n"),
    "R1-drop_output_outside_repo_check": (
        "    if output.is_relative_to(root):\n", "    if False:\n"),
    "R1-control_width_check_removed": (
        "    if width is not None and any(len(word) != (width + 3) // 4 for word in tokens):\n",
        "    if False:\n"),
    "R2-generated_rom_depth_dropped": (
        "            inputs.append(image_record(path, int(words), int(width)))\n",
        "            inputs.append(image_record(path, None, int(width)))\n"),
    "R2-generated_rom_width_dropped": (
        "            inputs.append(image_record(path, int(words), int(width)))\n",
        "            inputs.append(image_record(path, int(words), None))\n"),
    "R2-param_rom_width_dropped": (
        "                                   package_number(text, width)))\n",
        "                                   None))\n"),
    "R2-param_rom_ambiguity_refusal_dropped": (
        "        if len(matches) != 1 or len(packages) != 1:\n", "        if False:\n"),
    "R2-package_declaration_ambiguity_dropped": (
        "    if len(hits) != 1:\n", "    if False:\n"),
    "R2-integrated_directory_guard_dropped": (
        "    if log is None and output != gateware:\n", "    if False:\n"),
    "R2-attribution_requires_integrated_dropped": (
        "        if log is not None:\n", "        if False:\n"),
    "R2-cli_attribution_endpoint_guard_dropped": (
        "    if args.integrated_log and (args.synthesis_only or args.attribution_only):\n",
        "    if False:\n"),
    "R2-unfiltered_hierarchy_report_dropped": (
        " -hierarchical_min_primitive_count 0 -file baseline_hierarchy.rpt\n",
        " -file baseline_hierarchy.rpt\n"),
    "R2-wrapper_parameter_set_equality_dropped": (
        "    if set(values) != set(declarations):\n", "    if False:\n"),
    "R2-duplicate_parameter_refusal_dropped": (
        "        if name in values:\n", "        if False:\n"),
    "R2-ooc_single_synth_command_dropped": (
        "    if len(commands) != 1:\n", "    if False:\n"),
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
                rows.append(f"{name}\tNOT-APPLIED (count {text.count(old)})")
                continue
            text = text.replace(old, new)
        target = work / name / "syn" / "ooc" / "pp_baseline.py"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
        r = subprocess.run([sys.executable, "-B", str(target), "--selftest"],
                           capture_output=True, text=True, timeout=120)
        verdict = ("selftest PASS (mutant survives)" if r.returncode == 0
                   else "selftest FAIL (mutant killed)")
        if name == "pristine":
            verdict = f"rc={r.returncode}"
        rows.append(f"{name}\t{verdict}")
    shutil.rmtree(work)
    print("\n".join(rows))


if __name__ == "__main__":
    main()
