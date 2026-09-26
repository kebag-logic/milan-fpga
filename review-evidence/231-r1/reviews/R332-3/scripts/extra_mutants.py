#!/usr/bin/env python3
"""Reviewer probe: remove enforcement lines not in the maintained mutant list
and record whether `pp_baseline.py --selftest` detects each removal.
usage: extra_mutants.py <path/to/syn/ooc/pp_baseline.py>"""
import ast, subprocess, sys, tempfile
from pathlib import Path

MUTANTS = {
    "inventory image/geometry ambiguity guard": (
        "        if len(matches) != 1 or len(packages) != 1:\n", "        if False:\n"),
    "package geometry declaration uniqueness": (
        "    if len(hits) != 1:\n        raise ValueError(f\"expected one decimal declaration of {name}\")\n",
        "    if False:\n        raise ValueError(f\"expected one decimal declaration of {name}\")\n"),
    "microcode depth 1<<UPC_W_C": ("            count = 1 << count\n", "            count = count\n"),
    "wrapper declaration equality": (
        "    if set(values) != set(declarations):\n", "    if False:\n"),
    "empty parameter block": ("    if not values:\n", "    if False:\n"),
    "integrated output directory guard": (
        "    if log is None and output != gateware:\n", "    if False:\n"),
    "attribution requires integrated build": (
        "        if log is not None:\n            raise ValueError(\"attribution requires an integrated build\")\n",
        "        pass\n"),
    "CLI integrated-endpoint exclusivity": (
        "    if args.integrated_log and (args.synthesis_only or args.attribution_only):\n",
        "    if False:\n"),
    "single synth_design command": ("        if len(commands) != 1:\n", "        if False:\n"),
    "image pathname character guard": (
        "                if any(char in value for char in '{}\"\\n'):\n", "                if False:\n"),
    "split_once uniqueness": ("    if text.count(marker) != 1:\n", "    if False:\n"),
    "ROM_ERROR severity text": (
        'ROM_ERROR = "set_msg_config -id {Synth 8-4445} -new_severity ERROR\\n"',
        'ROM_ERROR = "set_msg_config -id {Synth 8-4445} -new_severity WARNING\\n"'),
    "ROM_ERROR placed after synthesis": (
        "    prefix += ROM_ERROR\n", "    rest = rest.replace('synth_design ', ROM_ERROR + 'synth_design ', 1)\n"),
    "KEEP_HIERARCHY on wrong cell": (
        '        constraint = "set_property KEEP_HIERARCHY TRUE [get_cells milan_datapath/pp_shadow]\\n"\n',
        '        constraint = "set_property KEEP_HIERARCHY TRUE [get_cells milan_datapath]\\n"\n'),
    "hexadecimal-only ROM check scoped to non-empty": (
        '    if not all(re.fullmatch(r"[0-9a-fA-F]+", word) for word in tokens):\n',
        '    if tokens and not re.fullmatch(r"[0-9a-fA-F]+", tokens[0]):\n'),
}

def main():
    source = Path(sys.argv[1]).read_text()
    with tempfile.TemporaryDirectory(prefix="r332-extra-mutants-") as tmp:
        for name, change in [("control", None), *MUTANTS.items()]:
            changed = source
            if change:
                old, new = change
                assert source.count(old) == 1, f"not unique: {name}"
                changed = source.replace(old, new)
            ast.parse(changed)
            target = Path(tmp) / name.replace(" ", "_").replace("/", "_") / "syn/ooc/pp_baseline.py"
            target.parent.mkdir(parents=True)
            target.write_text(changed)
            r = subprocess.run([sys.executable, "-B", str(target), "--selftest"],
                               capture_output=True, text=True, timeout=120)
            verdict = ("control-pass" if r.returncode == 0 else "CONTROL-FAIL") if change is None \
                else ("killed" if r.returncode != 0 else "SURVIVED")
            print(f"{name}\trc={r.returncode}\t{verdict}")

main()
