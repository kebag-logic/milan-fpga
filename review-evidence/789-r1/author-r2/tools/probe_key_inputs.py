#!/usr/bin/env python3
"""The rtl-fast tool key under one edit at a time, resolved as the hosted runner resolves it.

Usage: python3 -I probe_key_inputs.py <tree> <out.json>

<tree>'s scripts/ goes first on sys.path. Each row plants one edit in memory (a template edit, a
wrapped transform, or a changed repository file under hashFiles) and resolves the generated tool
key: `env.YOSYS_VERSION` from the workflow env, `runner.os` as Linux, and `hashFiles(...)` as the
runner computes it (SHA-256 over the concatenated SHA-256 digests of the named files). A row whose
edit changes what the build runs, under an unchanged key, is STALE-SERVED.
"""

import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from unittest.mock import patch


def main() -> int:
    tree, out = Path(sys.argv[1]), Path(sys.argv[2])
    sys.path.insert(0, str(tree / "scripts"))
    import ci_gate_workflows as gw
    import ci_install_workflows
    import ci_runtime_workflows

    template = gw.load_template(tree, "rtl-fast")
    tool, consumer, build = gw.FAST_TOOL_JOB, gw.FAST_TOOL_CONSUMER, gw.YOSYS_BUILD_STEPS[1]

    def resolve(workflow: dict, files: dict[str, bytes]) -> str:
        """The tool key with every expression evaluated."""
        step = next(s for s in workflow["jobs"][tool]["steps"] if s.get("name") == gw.YOSYS_BUILD_STEPS[0])
        key = step["with"]["key"]

        def hashed(match: re.Match) -> str:
            digests = b"".join(hashlib.sha256(files.get(path, (tree / path).read_bytes())).digest()
                               for path in sorted(re.findall(r"'([^']*)'", match.group(1))))
            return hashlib.sha256(digests).hexdigest()

        key = re.sub(r"\$\{\{ hashFiles\(([^)]*)\) \}\}", hashed, key)
        return key.replace("${{ env.YOSYS_VERSION }}", str(workflow["env"]["YOSYS_VERSION"])).replace(
            "${{ runner.os }}", "Linux")

    def key_of(changed: dict | None = None, files: dict[str, bytes] | None = None) -> str:
        return resolve(gw.generate("rtl-fast", template if changed is None else changed), files or {})

    def with_template(edit) -> dict:
        changed = copy.deepcopy(template)
        edit(changed)
        return changed

    def step(changed: dict, name: str) -> dict:
        return next(s for s in changed["jobs"][consumer]["steps"] if s.get("name") == name)

    def replaced(name: str, old: str, new: str):
        def edit(changed: dict) -> None:
            body = step(changed, name)
            assert body["run"].count(old) == 1, (name, old)
            body["run"] = body["run"].replace(old, new)
        return edit

    def wrapped(module, attribute: str, edit) -> str:
        original = getattr(module, attribute)

        def rewritten(*args):
            result = original(*args)
            edit(result)
            return result

        with patch.object(module, attribute, rewritten):
            return key_of()

    def install_rewrite(workflow: dict) -> None:
        body = next(s for s in workflow["jobs"][tool]["steps"] if s.get("name") == build)
        body["run"] = body["run"].replace("make -C /tmp/yosys-src config-gcc",
                                          "make -C /tmp/yosys-src config-clang", 1)

    def budget_export(budget: dict) -> None:
        budget["run"] = budget["run"].replace("} >> \"$GITHUB_ENV\"",
                                              "  printf 'CXXFLAGS=%s\\n' -O0\n} >> \"$GITHUB_ENV\"")

    def after_build(workflow: dict) -> None:
        steps = workflow["jobs"][tool]["steps"]
        at = [s.get("name") for s in steps].index(build) + 1
        steps.insert(at, {"name": "Touch the built tree", "id": "touch", "run": "touch /opt/yosys/planted\n"})

    script = (tree / "scripts/ci_install_cache.py").read_bytes()
    pristine = key_of()
    rows = []

    def row(label: str, build_input: bool, compute) -> None:
        try:
            key = compute()
        except ValueError as exc:
            rows.append({"edit": label, "build_input": build_input, "outcome": "REFUSED", "words": str(exc)})
            return
        changed = key != pristine
        outcome = ("key-changed" if changed else
                   ("STALE-SERVED" if build_input else "key-unchanged (as intended)"))
        rows.append({"edit": label, "build_input": build_input, "key_changed": changed, "outcome": outcome,
                     "key": key})

    row("edit outside the build (elaborate one more top)", False, lambda: key_of(with_template(
        replaced("Elaborate the integration-heavy tops", "--top KL_gptp_shadow",
                 "--top KL_gptp_shadow --top KL_pp_shadow"))))
    row("yosys-elaboration's if (schedules the tool job only)", False, lambda: key_of(with_template(
        lambda t: t["jobs"][consumer].update({"if": "${{ needs.changes.outputs.rtl == 'true' && !cancelled() }}"}))))
    row("pinned version v0.66 -> v0.67", True, lambda: key_of(with_template(
        lambda t: t["env"].update({"YOSYS_VERSION": "v0.67"}))))
    row("asserted source commit", True, lambda: key_of(with_template(replaced(
        build, "86f2ddebce7e98ce7cacc27e8a5c14cb53b51b51", "0" * 40))))
    row("recipe: ENABLE_PLUGINS := 1", True, lambda: key_of(with_template(replaced(
        build, "ENABLE_PLUGINS := 0", "ENABLE_PLUGINS := 1"))))
    row("recipe: one more apt package", True, lambda: key_of(with_template(replaced(
        build, "zlib1g-dev python3", "zlib1g-dev python3 libffi-dev"))))
    row("runner image ubuntu-22.04", True, lambda: key_of(with_template(
        lambda t: t["jobs"][consumer].update({"runs-on": "ubuntu-22.04"}))))
    row("workflow env CXXFLAGS: -O0", True, lambda: key_of(with_template(
        lambda t: t["env"].update({"CXXFLAGS": "-O0"}))))
    row("workflow env CXXSTD: c++23", True, lambda: key_of(with_template(
        lambda t: t["env"].update({"CXXSTD": "c++23"}))))
    row("workflow env, a new unrelated name (make still reads it)", True, lambda: key_of(with_template(
        lambda t: t["env"].update({"UNRELATED_NAME": "1"}))))
    row("yosys-elaboration job env CXXFLAGS: -O0", True, lambda: key_of(with_template(
        lambda t: t["jobs"][consumer].update({"env": {"CXXFLAGS": "-O0"}}))))
    row("install transform rewrites the build (config-clang)", True,
        lambda: wrapped(ci_install_workflows, "generate", install_rewrite))
    row("job budget step exports CXXFLAGS", True,
        lambda: wrapped(ci_runtime_workflows, "cpu_budget_step", budget_export))
    row("scripts/ci_install_cache.py content edited", True, lambda: key_of(
        files={"scripts/ci_install_cache.py": script + b"# planted\n"}))
    row("a step between the build and the cache save", True,
        lambda: wrapped(ci_runtime_workflows, "generate", after_build))
    out.write_text(json.dumps({"pristine": pristine, "rows": rows}, indent=1) + "\n")
    print("pristine", pristine)
    for item in rows:
        print(item["outcome"], "|", item["edit"], "|", item.get("words", item.get("key")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
