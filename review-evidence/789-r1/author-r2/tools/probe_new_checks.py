#!/usr/bin/env python3
"""Run each control of the round-2 fast-tool self-test on its own, against one tree's generator.

Usage: python3 -I probe_new_checks.py <tree> <controls-module> <out.json>

<tree> supplies the generator, the transforms and the template (its scripts/ goes first on sys.path);
<controls-module> is the new scripts/ci_fast_tool_selftest.py, loaded by path, so its imports
resolve to <tree>'s generator. Each control's outcome is PASS or FAIL with the exception's words.
"""

import contextlib
import importlib.util
import io
import json
import sys
from pathlib import Path


def main() -> int:
    tree, module_path, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    sys.path.insert(0, str(tree / "scripts"))
    spec = importlib.util.spec_from_file_location("fast_tool_controls_probe", module_path)
    controls = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(controls)
    template = controls.load_template(controls.ROOT, "rtl-fast")
    generated = controls.generate("rtl-fast", template)
    derived = controls.gate_graph("rtl-fast", template)["jobs"]

    def pristine_findings() -> None:
        found = controls.fast_tool_findings(template, generated)
        assert found == [], found

    def pristine_retention() -> None:
        found = controls.fast_tool_retention(template, derived)
        assert found == [], found

    rows = []
    for name, run in (("pristine fast_tool_findings", pristine_findings),
                      ("pristine fast_tool_retention", pristine_retention),
                      ("fast_tool_planted", lambda: controls.fast_tool_planted(template, generated)),
                      ("fast_tool_retention_planted", lambda: controls.fast_tool_retention_planted(template, derived)),
                      ("fast_tool_key_inputs", lambda: controls.fast_tool_key_inputs(template, generated)),
                      ("fast_tool_template_refusals", lambda: controls.fast_tool_template_refusals(template)),
                      ("fast_tool_controls (whole)", controls.fast_tool_controls)):
        printed = io.StringIO()
        try:
            with contextlib.redirect_stdout(printed):
                run()
        except Exception as exc:  # each control is judged on its own; record why it failed
            rows.append({"control": name, "result": "FAIL", "why": type(exc).__name__ + ": " + str(exc)[:600]})
        else:
            rows.append({"control": name, "result": "PASS", "printed": len(printed.getvalue().splitlines())})
    out.write_text(json.dumps(rows, indent=1) + "\n")
    for row in rows:
        print(row["result"], row["control"], "--", row.get("why", str(row.get("printed")) + " lines printed"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
