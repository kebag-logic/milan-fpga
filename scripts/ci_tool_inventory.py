#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Derive CI installation requests from workflows and their installer inputs.

The generated inventory records requested pins, including explicitly unpinned
distribution and Python packages. The image source lock resolves those requests
to checksummed artifacts. An unknown installation command is a refusal.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import shlex
import sys

import yaml

from ci_command_table import Audit, Refusal, Runtime
from ci_syntax import SENSITIVE


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path("ci/image/tool-inventory.json")


def digest(data: bytes) -> str:
    """Hash an input without depending on its checkout location."""
    return hashlib.sha256(data).hexdigest()


def constants(path: Path) -> dict[str, str]:
    """Read literal constants; never execute a candidate installer."""
    result = {}
    for node in ast.parse(path.read_text()).body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
            for target in node.targets:
                if isinstance(target, ast.Name) and isinstance(node.value.value, str):
                    result[target.id] = node.value.value
    return result


def requirement_lines(path: Path) -> list[dict[str, object]]:
    """Read package requests and their supplied wheel checksums."""
    rows = []
    for line in path.read_text().replace("\\\n", " ").splitlines():
        words = shlex.split(line, comments=True)
        if not words:
            continue
        request = words[0]
        if request.startswith("git+https://"):
            source, pin = request.rsplit("@", 1)
            if not re.fullmatch(r"[0-9a-f]{40}", pin):
                raise Refusal(f"{path.name}: non-exact Git requirement")
            name = source.rsplit("/", 1)[1].removesuffix(".git")
            rows.append({"tool": name, "kind": "git", "pin": pin, "source": source[4:]})
        else:
            name, separator, pin = request.partition("==")
            if not separator or any(not w.startswith("--hash=sha256:") for w in words[1:]):
                raise Refusal(f"{path.name}: unsupported requirement {request}")
            rows.append({"tool": name.lower(), "kind": "pip", "pin": pin,
                         "sha256": sorted(w.split(":", 1)[1] for w in words[1:])})
    return rows


def package_words(words: list[str], root: Path) -> list[dict[str, object]]:
    """Enumerate pip requests, including every referenced requirements file."""
    result = []
    i = 0
    while i < len(words):
        word = words[i]
        if word in ("-r", "--requirement"):
            i += 1
            result.extend(requirement_lines(root / words[i]))
        elif word in ("--cache-dir", "--index-url"):
            i += 1
        elif word in ("--quiet", "-q", "--require-hashes"):
            pass
        elif word.startswith("-"):
            raise Refusal(f"unsupported pip option {word}")
        else:
            name, _, pin = word.partition("==")
            if not re.fullmatch(r"[\w.-]+", name):
                raise Refusal(f"unsupported pip request {word}")
            result.append({"tool": name.lower(), "kind": "pip", "pin": pin or None})
        i += 1
    return result


def expand(word: str, variables: dict[str, str]) -> str:
    """Resolve only literal workflow and shell installation variables."""
    value = re.sub(r"\$\{(\w+)\}|\$(\w+)",
                   lambda match: variables.get(match[1] or match[2], match[0]), word)
    return value


def shell_installs(run: str, env: dict[str, str], root: Path) -> list[dict[str, object]]:
    """Parse the installation commands actually used by these workflows."""
    result = []
    variables = dict(env)
    lines = run.replace("\\\n", " ").splitlines()
    for line in lines:
        assignment = re.fullmatch(r"\s*(\w+)=(.*)", line)
        if assignment:
            words = shlex.split(assignment[2], comments=True)
            if len(words) == 1:
                variables[assignment[1]] = expand(words[0], variables)
        words = shlex.split(line, comments=True)
        if words and words[0] == "sudo":
            words = words[1:]
        if words[:2] == ["apt-get", "install"]:
            for word in words[2:]:
                if word in ("-y", "--no-install-recommends"):
                    continue
                name, _, pin = word.partition("=")
                if not re.fullmatch(r"[a-z0-9][a-z0-9+.-]*", name):
                    raise Refusal(f"unsupported apt request {word}")
                result.append({"tool": name, "kind": "apt", "pin": pin or None})
        elif words[:4] == ["python3", "-m", "pip", "install"]:
            result.extend(package_words(words[4:], root))
        elif words[:2] == ["git", "clone"]:
            urls = [word for word in words if word.startswith("https://")]
            if len(urls) != 1:
                raise Refusal("clone needs exactly one public HTTPS source")
            url = urls[0]
            name = url.rsplit("/", 1)[1].removesuffix(".git")
            if "--branch" in words:
                pin = expand(words[words.index("--branch") + 1], variables)
            elif name == "tsn-gen":
                pin = variables.get("TSN_GEN_REV", "")
            else:
                raise Refusal(f"unrecognized clone pin for {name}")
            if not pin or "$" in pin:
                raise Refusal(f"unresolved clone pin for {name}")
            result.append({"tool": name, "kind": "git", "pin": pin, "source": url})
        elif words and words[0] in ("curl", "wget"):
            resolved = [expand(word, variables) for word in words]
            urls = [word for word in resolved if word.startswith("https://")]
            if len(urls) != 1 or "$" in urls[0]:
                raise Refusal("download needs one resolved public HTTPS source")
            url = urls[0]
            match = re.search(r"/([^/]+)/releases/download/([^/]+)/", url)
            if not match:
                raise Refusal(f"unrecognized release download {url}")
            result.append({"tool": match[1], "kind": "archive", "pin": match[2],
                           "source": url, "sha256": variables.get("sha256")})
        elif words[:2] == ['apt-get', 'update']:
            if words[2:] not in ([], ['-qq']):
                raise Refusal('unsupported apt update options')
        elif words:
            raise Refusal(f"unsupported installation command: {line.strip()}")
    return result


def job_images(body: dict) -> list[dict[str, object]]:
    """Record every job and service image, refusing moving or unresolved tags."""
    result = []
    images = [('container', body['container'])] if 'container' in body else []
    images.extend((f'service:{name}', value) for name, value in body.get('services', {}).items())
    for role, value in images:
        reference = value.get('image') if isinstance(value, dict) else value
        if not isinstance(reference, str) or not re.fullmatch(r'[^\s$]+@sha256:[0-9a-f]{64}', reference):
            raise Refusal(f'job {role} image requires an exact digest: {reference!r}')
        result.append({'tool': reference.split('@')[0], 'kind': 'image', 'pin': reference.split('@')[1],
                       'source': reference, 'role': role})
    return result


def derive(root: Path) -> dict[str, object]:
    """Derive tool requests with every installing job and step as provenance."""
    records: dict[str, dict[str, object]] = {}
    inputs = {}
    audit = Audit(root, inputs)
    audit.install_reader = shell_installs
    workflows = sorted((root / ".github/workflows").glob("*.yml"))
    if not workflows:
        raise Refusal("no workflows found")
    for workflow in workflows:
        relative = workflow.relative_to(root).as_posix()
        raw = workflow.read_bytes()
        doc = yaml.safe_load(raw)
        inputs[relative] = digest(raw)
        for job, body in doc["jobs"].items():
            if 'uses' in body:
                raise Refusal(f'unsupported reusable workflow at {relative}: job {job}')
            for row in job_images(body):
                key = json.dumps(row, sort_keys=True)
                records.setdefault(key, {**row, "installed_by": []})["installed_by"].append(
                    {"workflow": relative, "job": job, "step": row["role"], "index": -1})
            for index, step in enumerate(body.get("steps", [])):
                run = step.get("run", "")
                env = {**doc.get("env", {}), **body.get("env", {}), **step.get("env", {})}
                shell = step.get('shell', body.get('defaults', {}).get('run', {}).get(
                    'shell', doc.get('defaults', {}).get('run', {}).get('shell')))
                if shell is not None:
                    raise Refusal(f'uncensused workflow shell {shell!r} at {relative}')
                if set(env) & SENSITIVE:
                    raise Refusal(f'uncensused workflow environment {sorted(set(env) & SENSITIVE)} at {relative}')
                audit.requests = []
                audit.env = {k: Runtime(v) if isinstance(v, str) and '${{' in v else str(v)
                             for k, v in env.items()}
                audit.exported_env = dict(audit.env)
                working = step.get('working-directory', body.get('defaults', {}).get('run', {}).get(
                    'working-directory', doc.get('defaults', {}).get('run', {}).get('working-directory', '.')))
                if not isinstance(working, str) or '$' in working:
                    raise Refusal(f'unresolved workflow working-directory at {relative}: job {job}')
                audit.shell(run, relative, root / working)
                rows = audit.requests
                if "sw/litex/patches/apply.sh" in run:
                    for patch in sorted((root / "sw/litex/patches").glob("*.patch")):
                        inputs[patch.relative_to(root).as_posix()] = digest(patch.read_bytes())
                uses = step.get("uses", "")
                allowed_actions = ("actions/checkout@", "actions/cache@", "actions/upload-artifact@",
                                   "actions/download-artifact@", "actions/setup-python@")
                if uses and not uses.startswith(allowed_actions):
                    raise Refusal(f"unsupported action installation surface: {uses}")
                if uses.startswith("actions/"):
                    rows.append({"tool": "node", "kind": "runner", "pin": None})
                if re.search(r"\bgh\s+(?:api|pr|issue|run|workflow)\b", run):
                    rows.append({"tool": "gh", "kind": "runner", "pin": None})
                if uses.startswith("actions/setup-python@"):
                    rows.append({"tool": "python", "kind": "action",
                                 "pin": step["with"]["python-version"]})
                where = {"workflow": relative, "job": job,
                         "step": step.get("name", uses or str(index)), "index": index}
                for row in rows:
                    key = json.dumps(row, sort_keys=True)
                    records.setdefault(key, {**row, "installed_by": []})["installed_by"].append(where)
    audit.requests = []
    audit.env = {}
    audit.exported_env = {}
    for directory in ("tb/verilator",):
        for path in sorted((root / directory).rglob("*")):
            if path.is_file() and (path.name == "Makefile" or path.suffix == ".mk"):
                audit.script(path.relative_to(root).as_posix(), "suite recipe population", root)
    return {"schema": 2, "inputs": dict(sorted(inputs.items())),
            "residue": sorted(audit.residue),
            "tools": [records[key] for key in sorted(records)]}


def serialized(value: object) -> str:
    """Use one canonical, reviewable generated representation."""
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def main() -> int:
    """Generate or compare the installation inventory, failing on drift."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--write", action="store_true")
    modes.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        content = serialized(derive(args.root))
        target = args.root / OUTPUT
        if args.write:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
        elif not target.is_file() or target.read_text() != content:
            raise Refusal("tool inventory differs from workflow installation requests")
    except (OSError, ValueError, KeyError, yaml.YAMLError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    print("CI tool inventory matches workflow installation requests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
