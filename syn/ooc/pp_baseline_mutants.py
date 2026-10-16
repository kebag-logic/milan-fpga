#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Prove that the baseline self-test detects removed enforcement points."""

import ast
from pathlib import Path
import subprocess
import shutil
import sys
import tempfile


MUTANTS = {
    "absolute-file recipe import broken": ('sys.path.insert(0, str(Path(__file__).resolve().parent))\n', ''),
    "split dispatch ignored": ('    if args.placement != "all-fabric":\n', '    if False:\n'),
    "split pre-route census omitted": (
        'commands[0] + pp_placement.census_tcl(placement)', 'commands[0]'),
    "split final census omitted": (
        'pp_placement.census_tcl(placement, report=True) + REPORTS', 'REPORTS'),
    "split timing assumes wrapper": ('pp_placement.scope_timing_tcl() + "\\nquit\\n"', 'SCOPE_TIMING + "\\nquit\\n"'),
    "split ROM error promotion omitted": (' + prefix + ROM_ERROR + "# Add constraints"',
                                         ' + prefix + "# Add constraints"'),
    "split retained AECP ROM skipped": (
        'placement == "f0-f4" and parameter == "PP_TROM_HEX_P"',
        'placement == "f0-f4" and parameter.startswith("PP_")'),
    "split selection marker omitted": ('script = pp_placement.MARKER + placement + "\\n" + prefix', 'script = prefix'),
    "present removed-protocol ROM unchecked": ("        if removed and not matches:\n", "        if removed:\n"),
    "split synthesis command count unchecked": (
        '    if len(commands) != 1:\n        raise ValueError("selected placement requires',
        '    if False:\n        raise ValueError("selected placement requires'),
    "split synthesis-only endpoint runs implementation": (
        '    marker = "# Add pre-optimize commands" if synthesis_only else "# Bitstream generation"\n'
        "    endpoint, _ = split_once(rest, marker)\n    script = pp_placement",
        '    marker = "# Bitstream generation"\n    endpoint, _ = split_once(rest, marker)\n    script = pp_placement'),
    "synthesis worker cap ignored": ("    if args.single_thread_synthesis:\n", "    if False:\n"),
    "synthesis worker cap enabled by default": ("    if args.single_thread_synthesis:\n", "    if True:\n"),
    "ROM error promotion": ("    prefix += ROM_ERROR\n", "    pass\n"),
    "readmemh inventory equality": (
        '    if expected != {Path(row["path"]).name for row in inputs}:\n',
        "    if False:\n"),
    "empty SRAM requirement": (
        "inputs.append(image_record(path, 0, None))",
        "inputs.append(image_record(path, None, None))"),
    "parameter ROM depth": (
        "inputs.append(image_record(Path(matches[0]), count,",
        "inputs.append(image_record(Path(matches[0]), None,"),
    "generated ROM depth": (
        "inputs.append(image_record(path, int(words), int(width)))",
        "inputs.append(image_record(path, None, int(width)))"),
    "generated ROM width": (
        "inputs.append(image_record(path, int(words), int(width)))",
        "inputs.append(image_record(path, int(words), None))"),
    "parameter ROM width": (
        "                                   package_number(text, width)))\n",
        "                                   None))\n"),
    "image and geometry ambiguity": (
        "        if len(matches) != 1 or len(packages) != 1:\n", "        if False:\n"),
    "image binding uniqueness": (
        "        if len(matches) != 1 or len(packages) != 1:\n",
        "        if len(packages) != 1:\n"),
    "geometry package uniqueness": (
        "        if len(matches) != 1 or len(packages) != 1:\n",
        "        if len(matches) != 1:\n"),
    "geometry declaration uniqueness": (
        "    if len(hits) != 1:\n", "    if False:\n"),
    "microcode address depth": (
        "            count = 1 << count\n", "            count = count\n"),
    "outside repository guard": (
        "    if output.is_relative_to(root):\n", "    if False:\n"),
    "image depth": (
        "    if words is not None and len(tokens) != words:\n", "    if False:\n"),
    "image width": (
        "    if width is not None and any(len(word) != (width + 3) // 4 for word in tokens):\n",
        "    if False:\n"),
    "hexadecimal image words": (
        '    if not all(re.fullmatch(r"[0-9a-fA-F]+", word) for word in tokens):\n',
        "    if False:\n"),
    "attribution constraint loading": (
        '        prefix += "read_xdc baseline_boundary.xdc\\n"\n', "        pass\n"),
    "attribution boundary preservation": (
        '        constraint = "set_property KEEP_HIERARCHY TRUE [get_cells milan_datapath/pp_shadow]\\n"\n',
        '        constraint = "set_property KEEP_HIERARCHY FALSE [get_cells milan_datapath/pp_shadow]\\n"\n'),
    "wrapper declaration equality": (
        "    if set(values) != set(declarations):\n", "    if False:\n"),
    "empty parameter block": ("    if not values:\n", "    if False:\n"),
    "duplicate parameter": ("        if name in values:\n", "        if False:\n"),
    "integrated output directory": (
        "    if log is None and output != gateware:\n", "    if False:\n"),
    "attribution integrated endpoint": (
        "        if log is not None:\n", "        if False:\n"),
    "CLI integrated endpoint": (
        "    if args.integrated_log and (args.synthesis_only or args.attribution_only):\n",
        "    if False:\n"),
    "single synthesis command": ("        if len(commands) != 1:\n", "        if False:\n"),
    "image pathname characters": (
        "                if any(char in value for char in '{}\"\\n'):\n", "                if False:\n"),
    "template marker uniqueness": ("    if text.count(marker) != 1:\n", "    if False:\n"),
    "unfiltered hierarchy report": (
        " -hierarchical_min_primitive_count 0 -file baseline_hierarchy.rpt\n",
        " -file baseline_hierarchy.rpt\n"),
    "integrated clock ignored": (
        "    if not integrated:\n", "    if True:\n"),
    "integrated clock frequency check": (
        "    if not isinstance(hertz, int) or hertz <= 0:\n", "    if False:\n"),
    "integrated clock period": (
        '    return f"create_clock -period {1e9 / hertz:.3f} -name clk [get_ports clk_i]\\n"\n',
        '    return f"create_clock -period {1e9 / hertz / 2:.3f} -name clk [get_ports clk_i]\\n"\n'),
    "CLI integrated clock endpoint": (
        "    if args.integrated_clock and not args.integrated_log:\n", "    if False:\n"),
}


def main() -> None:
    """Run a positive control and require every single mutant to fail."""
    pristine = Path(__file__).with_name("pp_baseline.py")
    source = pristine.read_text()
    with tempfile.TemporaryDirectory(prefix="pp-baseline-mutants-") as tmp:
        for name, change in [("control", None), *MUTANTS.items()]:
            changed = source
            if change is not None:
                old, new = change
                if source.count(old) != 1:
                    raise AssertionError(f"mutation is not unique: {name}")
                changed = source.replace(old, new)
            ast.parse(changed)
            target = Path(tmp) / name / "syn/ooc/pp_baseline.py"
            target.parent.mkdir(parents=True)
            target.write_text(changed)
            for sibling in ("pp_placement.py", "pp_placement_selftest.py"):
                shutil.copy2(pristine.with_name(sibling), target.with_name(sibling))
            result = subprocess.run([sys.executable, "-B", str(target), "--selftest"],
                                    capture_output=True, text=True, timeout=60)
            if (result.returncode == 0) != (change is None):
                raise AssertionError(f"{name}: rc={result.returncode}\n"
                                     f"{result.stdout}\n{result.stderr}")
            if change is None and "placement recipe: legacy parity" not in result.stdout:
                raise AssertionError("the control passed without running the placement recipe controls")
            print(f"{name}: rc={result.returncode} PASS")


if __name__ == "__main__":
    main()
