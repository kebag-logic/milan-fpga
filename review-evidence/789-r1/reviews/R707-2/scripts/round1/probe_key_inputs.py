#!/usr/bin/env python3
"""Plant edits that do, or do not, change the Yosys the tool job builds, and read the generated tool key.

Usage: probe_key_inputs.py <exported-head-tree> <receipt-dir>

The tool key is read from the generated `yosys-tool` cache step with its runtime
expressions resolved the way the hosted runner resolves them: `env.YOSYS_VERSION`
from the generated workflow's top-level env, `runner.os` as Linux. A cache entry
is served by exact key, so two builds that resolve to one key are
indistinguishable to the consumer's restore. Each row records whether the edit
changes the built tool (by construction of the edit) and whether the key moved.
"""
import copy
import importlib
import json
import pathlib
import re
import sys

TOOL, CONSUMER, BUILD = "yosys-tool", "yosys-elaboration", "Build Yosys from source on cache miss"


def resolved_key(workflow: dict) -> str:
    """The tool cache key with its expressions resolved as on a hosted Linux runner."""
    step = next(s for s in workflow["jobs"][TOOL]["steps"] if s.get("name") == "Cache the pinned Yosys build")
    key = step["with"]["key"]
    key = key.replace("${{ env.YOSYS_VERSION }}", workflow["env"]["YOSYS_VERSION"])
    key = re.sub(r"\$\{\{\s*runner\.os\s*\}\}", "Linux", key)
    assert "${{" not in key, key
    return key


def tool_build(workflow: dict) -> dict:
    """The generated tool job's build step and the environment it runs under."""
    job = workflow["jobs"][TOOL]
    return {"workflow_env": workflow.get("env"), "job_env": job.get("env"),
            "build": next(s for s in job["steps"] if s.get("name") == BUILD)["run"]}


def main() -> int:
    tree, receipts = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve()
    sys.path.insert(0, str(tree / "scripts"))
    gen = importlib.import_module("ci_gate_workflows")
    install = importlib.import_module("ci_install_workflows")
    template = gen.load_template(tree, "rtl-fast")
    pristine = gen.generate("rtl-fast", template)
    base_key, base_build = resolved_key(pristine), tool_build(pristine)

    def edit_build(old: str, new: str):
        def apply(t: dict) -> None:
            step = next(s for s in t["jobs"][CONSUMER]["steps"] if s.get("name") == BUILD)
            assert step["run"].count(old) == 1, old
            step["run"] = step["run"].replace(old, new)
        return apply

    def edit_env(name: str, value: str):
        def apply(t: dict) -> None:
            t["env"][name] = value
        return apply

    def edit_consumer_env(name: str, value: str):
        def apply(t: dict) -> None:
            t["jobs"][CONSUMER].setdefault("env", {})[name] = value
        return apply

    def edit_runs_on(t: dict) -> None:
        t["jobs"][CONSUMER]["runs-on"] = "ubuntu-22.04"

    def edit_other_job(t: dict) -> None:
        step = next(s for s in t["jobs"][CONSUMER]["steps"] if s.get("name") == "Elaborate the integration-heavy tops")
        step["run"] = step["run"].replace("--top KL_gptp_shadow", "--top KL_gptp_shadow --top KL_pp_shadow")

    cases = [
        # label, changes the built tool?, template edit
        ("pinned version v0.66 -> v0.67 (workflow env)", True, edit_env("YOSYS_VERSION", "v0.67")),
        ("source commit asserted by the build step", True, edit_build("86f2ddebce7e98ce7cacc27e8a5c14cb53b51b51\"",
                                                                      "0000000000000000000000000000000000000000\"")),
        ("build recipe: ENABLE_PLUGINS 0 -> 1", True, edit_build("ENABLE_PLUGINS := 0", "ENABLE_PLUGINS := 1")),
        ("build recipe: one more apt package", True, edit_build("zlib1g-dev python3", "zlib1g-dev python3 libffi-dev")),
        ("runner image ubuntu-24.04 -> ubuntu-22.04", True, edit_runs_on),
        ("workflow env gains CXXFLAGS=-O0 (Makefile: CXXFLAGS := $(CXXFLAGS) ...)", True, edit_env("CXXFLAGS", "-O0")),
        ("workflow env gains CXXSTD=c++23 (Makefile: export CXXSTD ?= c++20)", True, edit_env("CXXSTD", "c++23")),
        ("yosys-elaboration job env gains CXXFLAGS=-O0", False, edit_consumer_env("CXXFLAGS", "-O0")),
        ("edit outside the recipe (elaboration tops)", False, edit_other_job),
        ("workflow env gains an unrelated name", False, edit_env("UNRELATED_NAME", "1")),
    ]
    rows = []
    for label, changes_tool, apply in cases:
        changed = copy.deepcopy(template)
        apply(changed)
        out = gen.generate("rtl-fast", changed)
        key, build = resolved_key(out), tool_build(out)
        rows.append({"edit": label, "changes_built_tool": changes_tool,
                     "tool_build_inputs_changed": build != base_build, "key_changed": key != base_key, "key": key})
    # A generator-side transform of the build body (the install-cache rewrite), with the template unchanged.
    original = install.package_steps

    def rewritten(step: dict, index: int) -> list[dict]:
        out = original(step, index)
        for s in out:
            if s.get("name") == BUILD:
                s["run"] = s["run"].replace("install -y --no-install-recommends", "install -y")
        return out
    install.package_steps = rewritten
    try:
        out = gen.generate("rtl-fast", copy.deepcopy(template))
    finally:
        install.package_steps = original
    rows.append({"edit": "install-cache transform drops --no-install-recommends from the generated build (template unchanged)",
                 "changes_built_tool": True, "tool_build_inputs_changed": tool_build(out) != base_build,
                 "key_changed": resolved_key(out) != base_key, "key": resolved_key(out)})
    receipts.mkdir(parents=True, exist_ok=True)
    (receipts / "key_inputs.json").write_text(json.dumps({"pristine_key": base_key, "rows": rows}, indent=1) + "\n")
    print("pristine key:", base_key)
    for row in rows:
        stale = row["changes_built_tool"] and not row["key_changed"]
        print(("STALE-SERVED " if stale else "ok           ") + "tool-changes=" + str(row["changes_built_tool"])
              + " build-inputs-changed=" + str(row["tool_build_inputs_changed"]) + " key-changed="
              + str(row["key_changed"]) + "  " + row["edit"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
