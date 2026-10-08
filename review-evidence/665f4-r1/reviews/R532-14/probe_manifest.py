#!/usr/bin/env python3
"""Reviewer probe: run the act runner's submodule-manifest arms in isolation.

Usage: python3 -I probe_manifest.py <act_ci.py copy> <mutation-id> <scratch-dir>

The runner file is read as text only. A fixed list of reviewed top-level
definitions is extracted by AST (after an optional exact-text mutation) and
executed in a fresh module. The runner's process launcher is replaced by a
reviewer-owned `capture` with the same contract (stdout stripped, nonzero exit
is Refusal); every git command runs locally with protocol.allow=never and no
network, credential, Docker or act path. Prints one line per arm and a final
`RESULT <mutation> failures=<n> crashed=<0|1>` line.
"""
from __future__ import annotations

import ast
import contextlib
import io
import os
import pathlib
import subprocess
import sys
import traceback
import types

NAMES = {
    "SHA_RE", "SAFE_PATH", "MAX_GITMODULES_BYTES", "TRUSTED_SUBMODULES",
    "REQUIRED_SUBMODULES", "Refusal", "SelftestTally", "expect_refusal",
    "require_tool", "git_environment", "git_prefix", "git_capture",
    "expected_file", "expected_submodule_config", "validate_submodule_manifest",
    "initialize_required_submodules", "selftest_submodule_manifest",
    "selftest_lwsrp_manifest",
}

# Exact (old, new) text replacements; each must match exactly once.
MUTATIONS: dict[str, list[tuple[str, str]]] = {
    "none": [],
    # Production manifest defects.
    "P1-manifest-omits-lwsrp": [(
        '    (\n        "third_party/lwSRP",\n        "third_party/lwSRP",\n'
        '        "https://github.com/kebag-logic/lwSRP.git",\n    ),\n', "")],
    "P2-manifest-wrong-url": [(
        '        "https://github.com/kebag-logic/lwSRP.git",\n    ),\n)',
        '        "https://github.com/kebag-logic/lwSRP",\n    ),\n)')],
    "P3-manifest-wrong-path": [(
        '        "third_party/lwSRP",\n        "third_party/lwSRP",\n',
        '        "third_party/lwSRP",\n        "third_party/lwsrp",\n')],
    "P4-required-includes-external": [(
        'for name, path, _url in TRUSTED_SUBMODULES if name != "external"',
        'for name, path, _url in TRUSTED_SUBMODULES')],
    "P5-required-omits-lwsrp": [(
        'for name, path, _url in TRUSTED_SUBMODULES if name != "external"',
        'for name, path, _url in TRUSTED_SUBMODULES '
        'if name not in ("external", "third_party/lwSRP")')],
    "P6-required-reorders": [(
        'for name, path, _url in TRUSTED_SUBMODULES if name != "external"\n)',
        'for name, path, _url in TRUSTED_SUBMODULES if name != "external"\n)[::-1]')],
    # Validator defects.
    "V1-ignore-extra-config": [(
        "    if actual != expected:\n        missing",
        "    if {k: actual.get(k) for k in expected} != expected:\n        missing")],
    "V2-ignore-missing-config": [(
        "    if actual != expected:\n        missing",
        "    if {k: expected.get(k) for k in actual} != actual:\n        missing")],
    "V3-ignore-url-values": [(
        "    if actual != expected:\n        missing",
        "    if {k: v for k, v in actual.items() if not k.endswith('.url')} != "
        "{k: v for k, v in expected.items() if not k.endswith('.url')} "
        "or actual.keys() != expected.keys():\n        missing")],
    "V4-ignore-path-values": [(
        "    if actual != expected:\n        missing",
        "    if {k: v for k, v in actual.items() if not k.endswith('.path')} != "
        "{k: v for k, v in expected.items() if not k.endswith('.path')} "
        "or actual.keys() != expected.keys():\n        missing")],
    "V5-no-repeat-check": [(
        "        if key in actual:\n            raise Refusal",
        "        if False:\n            raise Refusal")],
    "V6-no-gitlink-check": [(
        "    if actual_gitlinks != expected_gitlinks or len(gitlinks) != len(actual_gitlinks):",
        "    if False:")],
    "V7-gitlink-subset-only": [(
        "    if actual_gitlinks != expected_gitlinks or len(gitlinks) != len(actual_gitlinks):",
        "    if not actual_gitlinks <= expected_gitlinks:")],
    "V8-gitlink-superset-only": [(
        "    if actual_gitlinks != expected_gitlinks or len(gitlinks) != len(actual_gitlinks):",
        "    if not actual_gitlinks >= expected_gitlinks:")],
    "V9-ssh-allowed": [(
        '        "protocol.https.allow=always",\n    ]',
        '        "protocol.https.allow=always",\n        "-c",\n'
        '        "protocol.ssh.allow=always",\n    ]')],
    # Test-the-test: defects in the new arms themselves.
    "T1-plant-noop": [(
        "            if label == \"drops lwSRP\":\n"
        "                candidate_config.pop(f\"submodule.third_party/lwSRP.{suffix}\")\n"
        "            else:\n"
        "                candidate_config[f\"submodule.third_party/lwSRP-extra.{suffix}\"] = (\n"
        "                    value + \"-extra\" if suffix == \"path\" else value\n"
        "                )\n",
        "            pass\n")],
    "T2-extra-stanza-refused-incidentally": [(
        "        (\"adds another lwSRP\", manifest + stanza.replace(\"third_party/lwSRP\", "
        "\"third_party/lwSRP-extra\"),\n",
        "        (\"adds another lwSRP\", manifest + stanza.replace(\"third_party/lwSRP\", "
        "\"third_party/lwSRP-extra\") + \"\\tupdate = none\\n\",\n")],
    "T3-drop-variant-also-drops-gitlink": [(
        "        (\"drops lwSRP\", manifest.replace(stanza, \"\"), gitlinks),",
        "        (\"drops lwSRP\", manifest.replace(stanza, \"\"), gitlinks[:-1]),")],
    "T4-drop-variant-drops-nothing": [(
        "              '\\turl = https://github.com/kebag-logic/lwSRP.git\\n')",
        "              '\\turl = https://github.com/kebag-logic/lwSRP\\n')")],
    "T5-redirect-variant-redirects-nothing": [(
        "        (\"redirects lwSRP\", manifest.replace(\"https://github.com/kebag-logic/lwSRP.git\",",
        "        (\"redirects lwSRP\", manifest.replace(\"https://github.com/kebag-logic/lwSRP.gitX\",")],
    "T6-fixture-derived-from-manifest": [(
        "    manifest = (\n        (\"external\", \"external\", \"git@github.com:kebag-logic/fpga-avb-ethernet.git\"),",
        "    manifest = TRUSTED_SUBMODULES\n    _unused = (\n        (\"external\", \"external\", \"git@github.com:kebag-logic/fpga-avb-ethernet.git\"),")],
}

COMBINED = {
    # The pre-fix shape: manifest omits lwSRP and the fixture is derived from it.
    "C1-omit-lwsrp-with-derived-fixture": ["P1-manifest-omits-lwsrp", "T6-fixture-derived-from-manifest"],
}


def capture(command, *, cwd, description, env=None):
    """Reviewer-owned launcher with the runner's capture() contract."""
    try:
        result = subprocess.run(list(command), cwd=cwd, env=dict(env or {}),
                                capture_output=True, text=True, timeout=300, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise MODULE.Refusal(f"cannot run {description}: {exc}") from exc
    if result.returncode != 0:
        detail = result.stderr.strip().splitlines()
        raise MODULE.Refusal(f"{description} failed{': ' + detail[-1] if detail else ''}")
    return result.stdout.strip()


MODULE: types.ModuleType


def build(source: str) -> types.ModuleType:
    tree = ast.parse(source)
    picked = []
    for node in tree.body:
        targets = []
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            targets = [node.name]
        elif isinstance(node, ast.Assign):
            targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
        if set(targets) & NAMES:
            picked.append(ast.get_source_segment(source, node))
    found = set()
    for seg in picked:
        found |= {n for n in NAMES if f"def {n}(" in seg or f"class {n}" in seg or seg.startswith(n)}
    missing = NAMES - found
    if missing:
        raise SystemExit(f"extraction missing {sorted(missing)}")
    module = types.ModuleType("act_manifest_probe")
    sys.modules[module.__name__] = module
    header = ("from __future__ import annotations\nimport contextlib, io, os, pathlib, re, shutil, stat, sys\n"
              "from unittest import mock\nfrom typing import Callable, Mapping, Sequence\n")
    exec(compile(header + "\n\n".join(picked), "<extracted act_ci>", "exec"), module.__dict__)
    module.capture = capture
    return module


def main() -> int:
    path, mutation, scratch = pathlib.Path(sys.argv[1]), sys.argv[2], pathlib.Path(sys.argv[3]).resolve()
    source = path.read_text(encoding="utf-8")
    for step in COMBINED.get(mutation, [mutation]):
        for old, new in MUTATIONS[step]:
            count = source.count(old)
            if count != 1:
                print(f"MUTATION-NOT-APPLIED {step} matches={count}")
                return 3
            source = source.replace(old, new)
    global MODULE
    MODULE = build(source)
    repo = scratch / "repo"
    repo.mkdir(parents=True)
    env = MODULE.git_environment(scratch)

    def test_git(*args):
        return capture([*MODULE.git_prefix(), "-C", str(repo), *args], cwd=repo, env=env,
                       description="probe git")

    test_git("init", "--quiet")
    test_git("config", "user.name", "probe")
    test_git("config", "user.email", "probe@example.invalid")
    (repo / "README").write_text("x\n", encoding="utf-8")
    test_git("add", "README")
    test_git("commit", "--quiet", "-m", "base")
    fixture = types.SimpleNamespace(repo=repo, test_git=test_git)
    tally = MODULE.SelftestTally()
    crashed = 0
    try:
        MODULE.selftest_submodule_manifest(tally, fixture)
    except BaseException:  # an unguarded Refusal aborts the arm group, a failure
        crashed = 1
        print("CRASH " + traceback.format_exc().strip().splitlines()[-1])
    print(f"RESULT {mutation} failures={tally.failures} crashed={crashed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
