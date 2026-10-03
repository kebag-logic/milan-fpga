#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Prove that the resource gate's self-test detects each removed enforcement point."""

import ast
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


MUTANTS = {
    "identity comparison": ("    if changed:\n", "    if False:\n"),
    "endpoint kind comparison": ('    if candidate["kind"] != base["kind"]:\n', "    if False:\n"),
    "identical-input refusal": (
        '    if candidate["inputs_sha256"] == base["inputs_sha256"] and candidate["figures"] != base["figures"]:\n',
        "    if False:\n"),
    "identical-input figures": ('candidate["figures"] != base["figures"]:\n',
                                'candidate["figures"]["LUT"] != base["figures"]["LUT"]:\n'),
    "resource tolerance": ("    if after - before > tolerance:\n", "    if False:\n"),
    "resource tolerance boundary": ("    if after - before > tolerance:\n", "    if after - before >= tolerance:\n"),
    "timing floor": ("        if after < floor:\n", "        if False:\n"),
    "timing floor boundary": ("        if after < floor:\n", "        if after <= floor:\n"),
    "timing fall": ("        if before - after > tolerance:\n", "        if False:\n"),
    "timing fall boundary": ("        if before - after > tolerance:\n", "        if before - after >= tolerance:\n"),
    "ceiling": ('        if candidate["figures"][figure] > ceiling:\n', "        if False:\n"),
    "ceiling boundary": ('        if candidate["figures"][figure] > ceiling:\n',
                         '        if candidate["figures"][figure] >= ceiling:\n'),
    "verdict status": ("        status = status if ok else 1\n", "        status = status\n"),
    "standalone RAMB36": ('"ooc": ("LUT", "FF", "RAMB36", "RAMB18", "DSP")}', '"ooc": ("LUT", "FF", "RAMB18", "DSP")}'),
    "standalone DSP": ('"ooc": ("LUT", "FF", "RAMB36", "RAMB18", "DSP")}', '"ooc": ("LUT", "FF", "RAMB36", "RAMB18")}'),
    "improvement report": ("    if improved:\n", "    if False:\n"),
    "improvement threshold": ('        if gain > entry["tolerance"][figure]:\n',
                              '        if gain >= entry["tolerance"][figure]:\n'),
    "improvement direction": ("        gain = after - before if figure in TIMING else before - after\n",
                              "        gain = before - after\n"),
    "Slice row": ('"Slice": "SLICE",\n', "\n"),
    "row agreement": ("        if len(values) != 1:\n", "        if not values:\n"),
    "count format": ('        if not re.fullmatch(r"\\d+(\\.5)?", value):\n', "        if False:\n"),
    "count format decimals": ('r"\\d+(\\.5)?"', 'r"\\d+(\\.\\d+)?"'),
    "header uniqueness": ("    if len(hits) != 1:\n", "    if not hits:\n"),
    "one timing summary": ("    if len(blocks) != 2:\n", "    if len(blocks) < 2:\n"),
    "timing value row": ("    if heads is None or heads + 2 >= len(lines):\n", "    if heads is None:\n"),
    "timing columns": (
        '    if len(names) != len(values) or len(names) < 5 or names[0] != "WNS(ns)" or names[4] != "WHS(ns)":\n',
        "    if False:\n"),
    "timed endpoints": ("    if not paths or not all(value.isdigit() and int(value) > 0 for value in paths):\n",
                        "    if False:\n"),
    "finite slack": ("    if not all(math.isfinite(value) for value in slack.values()):\n", "    if False:\n"),
    "tool build": ('    tool = re.match(r"(.+? Build \\d+)", header(report, "Tool Version"))\n',
                   '    tool = re.match(r"(.+?) Build \\d+", header(report, "Tool Version"))\n'),
    "design identity": ('"design": header(report, "Design"), ', '"design": "", '),
    "design state identity": ('"state": header(report, "Design State"),', '"state": "",'),
    "flow commands": ('    flow = [GENERICS.sub("", INCLUDES.sub("", match.group(0))).strip()\n',
                      '    flow = [GENERICS.sub("", INCLUDES.sub("", match.group(0)))[:12]\n'),
    "flow create_project": ('r"^(create_project|', 'r"^('),
    "flow set_param": ("|set_param|", "|"),
    "flow synth_design": ("|synth_design|", "|"),
    "flow opt_design": ("|opt_design|", "|"),
    "flow place_design": ('|place_design"', '"'),
    "flow phys_opt_design": ('r"|phys_opt_design|', 'r"|'),
    "flow route_design": ("|route_design|", "|"),
    "flow kl_timing_grade_configure": ("|kl_timing_grade_configure)", ")"),
    "standalone clock": ('re.findall(r"-period (\\S+)", clock.read_text()) if clock.is_file() else []}',
                         "[]}"),
    "generated-file normalization": ('            text = re.sub(r"//[^\\n]*", "", data.decode(errors="replace"))\n',
                                     '            text = data.decode(errors="replace")\n'),
    "generated-file roots": ('                text = text.replace(root, f"$ROOT{index}")\n', "                pass\n"),
    "one generated top": ("    if len(generated) != 1 or len(repository) != 1:\n",
                          "    if not generated or not repository:\n"),
    "read source presence": ("        if not path.is_file():\n", "        if False:\n"),
    "include directory presence": ("            if not folder.is_dir():\n", "            if False:\n"),
    "include headers": (
        '            headers += sorted(path for path in folder.iterdir() if path.suffix in (".svh", ".vh"))\n',
        "            headers += []\n"),
    "generic inputs": ("    for generic in GENERICS.findall(script):\n", "    for generic in []:\n"),
    "image inputs": ("    for image in sorted(images, key=lambda row: Path(row[\"path\"]).name):\n",
                     "    for image in []:\n"),
    "image manifest shape": ("    if not isinstance(images, list) or not all(", "    if False and all("),
    "recipe script uniqueness": ("    if len(kinds) != 1:\n", "    if not kinds:\n"),
    "census header": ('    if not lines or lines[0] != "cell\\tprimitive":\n', "    if False:\n"),
    "route status of a route": ('    if kind != "route":\n', "    if True:\n"),
    "one route status report": ("    if len(reports) != 1:\n", "    if not reports:\n"),
    "route status counts": ("        if not value.isdigit():\n", "        if False:\n"),
    "routing-error row": ('    if len(counts.get("nets with routing errors", [])) != 1:\n', "    if False:\n"),
    "routable and routed rows": ("    if len(routable) != len(routed):\n", "    if False:\n"),
    "routing errors fail": ('("routing errors" in label or "unrouted" in label)', '("unrouted" in label)'),
    "unrouted nets fail": ('("routing errors" in label or "unrouted" in label)', '("routing errors" in label)'),
    "partly routed nets fail": ("    if sum(routed) != sum(routable):\n", "    if False:\n"),
    "incomplete route fails": ("    if unrouted:\n", "    if False:\n"),
    "complete route reported": (
        '        lines.append("route status: complete, no unrouted net and no routing error")\n', "        pass\n"),
    "check reads the route status": (
        '        unrouted = routing(directory, candidate["kind"]) if args.command == "check" else []\n',
        "        unrouted = []\n"),
    "refusal exit status": ('        print(f"NOT COMPARABLE: {error}")\n        return 2\n',
                            '        print(f"NOT COMPARABLE: {error}")\n        return 0\n'),
    "kind from the directory": ("        candidate = record(directory, kind_of(directory))\n",
                                '        candidate = record(directory, "route")\n'),
    "unreadable baseline": ('raise Refusal(f"baseline {path} is unreadable: {error}") from error', "raise"),
    "baseline endpoints table": (
        '    if not isinstance(baseline, dict) or not isinstance(baseline.get("endpoints"), dict):\n',
        "    if False:\n"),
    "check validates its endpoint": (
        '        problems = entry_problems(args.endpoint, entry) if args.command == "check" else []\n',
        "        problems = []\n"),
    "check-baseline exit status": ("            return 2 if problems else 0\n", "            return 0\n"),
    "baseline record presence": ("    if not isinstance(base, dict):\n", "    if False:\n"),
    "baseline record completeness": ('    if (base.get("kind") not in GATED',
                                     '    if False and (base.get("kind") not in GATED'),
    "baseline tolerance": (
        '            if not entry.get("tolerance", {}).get(figure, -1) >= 0:\n', "            if False:\n"),
    "baseline floor presence": ('            if figure in TIMING and figure not in entry.get("floor", {}):\n',
                                "            if False:\n"),
    "baseline floor value": ('            elif figure in TIMING and figures[figure] < entry["floor"][figure]:\n',
                             "            elif False:\n"),
    "baseline route ceiling": ('            if figure not in entry.get("ceiling", {}):\n', "            if False:\n"),
    "baseline ceiling figure": ("            if figure not in figures:\n", "            if False:\n"),
    "baseline ceiling": ("            elif figures[figure] > ceiling:\n", "            elif False:\n"),
    "malformed policy": ("    except (KeyError, TypeError, AttributeError) as error:\n",
                         "    except KeyError as error:\n"),
    "budget table compared": ("                if held.get(figure) != table[name][field].get(figure):\n",
                              "                if False:\n"),
    "budget endpoints compared": ("        if name not in table or name not in endpoints:\n", "        if False:\n"),
    "one budget table": ("    if len(starts) != 1:\n", "    if not starts:\n"),
    "budget row shape": ("        if len(cells) != len(COLUMNS) + 1 or name is None or name[1] in table:\n",
                         "        if False:\n"),
    "budget cell values": ('            if value is None and cell != "-":\n', "            if False:\n"),
    "unreadable budget page": ("    except (OSError, ValueError, Refusal) as error:\n",
                               "    except (ValueError, Refusal) as error:\n"),
}


def main() -> None:
    """Run a positive control and require every single mutant to fail the self-test."""
    here = Path(__file__).resolve().parent
    source = (here / "pp_resource_gate.py").read_text()
    with tempfile.TemporaryDirectory(prefix="pp-resource-gate-mutants-") as tmp:
        for name, change in [("control", None), *MUTANTS.items()]:
            changed = source
            if change is not None:
                old, new = change
                if source.count(old) != 1:
                    raise AssertionError(f"mutation is not unique: {name}")
                changed = source.replace(old, new)
            ast.parse(changed)
            folder = Path(tmp) / name.replace(" ", "_")
            folder.mkdir()
            for sibling in ("pp_baseline_rank.py", "pp_resource_gate_selftest.py"):
                shutil.copy2(here / sibling, folder / sibling)
            (folder / "pp_resource_gate.py").write_text(changed)
            result = subprocess.run([sys.executable, "-B", str(folder / "pp_resource_gate.py"), "--selftest"],
                                    capture_output=True, text=True, timeout=120)
            if (result.returncode == 0) != (change is None):
                raise AssertionError(f"{name}: rc={result.returncode}\n{result.stdout}\n{result.stderr}")
            print(f"{name}: rc={result.returncode} PASS")
    print(f"resource gate mutants: control passes, all {len(MUTANTS)} mutants fail")


if __name__ == "__main__":
    main()
