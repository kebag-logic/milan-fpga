#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Stage verified public inputs, build a tools stage, and record image identity."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tarfile
import time
import urllib.request


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
STAGES = ("system-tools", "gtest-tools", "python-tools", "litex-tools", "verilator-tools", "yosys-tools",
          "rv32-tools", "sv2v-tools", "sbt-tools", "oracle-tools", "node-tools", "gh-tools", "validation-tools")
GTEST = {"googletest", "libgtest-dev", "libgmock-dev"}
LAYER_ROOTS = {"verilator": ("verilator",), "yosys": ("yosys",), "rv32": ("rv32-sdk",),
               "sv2v": ("sv2v",), "oracle": ("tsn-gen",), "sbt": ("sbt",),
               "node": ("node",), "gh": ("gh",),
               "litex": ("migen", "litex", "litedram", "liteeth", "litespi", "litex-boards",
                         "pythondata-cpu-vexiiriscv", "VexiiRiscv")}


def sha256(path: Path) -> str:
    """Hash artifacts without loading toolchains into memory."""
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def canonical(value: object) -> bytes:
    """Use a stable encoding for recipe identities."""
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def validate_pins(pins: dict[str, object]) -> None:
    """Refuse a lock that diverges from any exact workflow installation request."""
    rows = pins["packages"] + pins["sources"]
    by_name = {row["tool"].lower(): row for row in rows}
    if len(by_name) != len(rows):
        raise ValueError("duplicate source tool")
    for row in rows:
        path = Path(row["filename"])
        if path.is_absolute() or ".." in path.parts or not re.fullmatch(r"[0-9a-f]{64}", row["sha256"]):
            raise ValueError(f"invalid source path or checksum: {row['tool']}")
        if not row["version"] or row["size"] <= 0:
            raise ValueError(f"missing source version or size: {row['tool']}")
    inventory = json.loads((HERE / "tool-inventory.json").read_text())
    for request in inventory["tools"]:
        if request["kind"] == "action":
            if request["pin"] not in ("3.12", "3.12.3"):
                raise ValueError("Python action no longer requests 3.12")
            continue
        row = by_name.get(request["tool"].lower())
        if row is None:
            raise ValueError(f"unresolved workflow tool: {request['tool']}")
        expected = request.get("pin")
        if expected and request["kind"] != "derived-git":
            if str(row["version"]).removeprefix("v") != str(expected).removeprefix("v"):
                raise ValueError(f"workflow version mismatch: {request['tool']}")
        expected_hash = request.get("sha256")
        if expected_hash and row["sha256"] not in (
                expected_hash if isinstance(expected_hash, list) else [expected_hash]):
            raise ValueError(f"workflow checksum mismatch: {request['tool']}")
    if not by_name["python3.12"]["version"].startswith("3.12.3-"):
        raise ValueError("CPython must remain 3.12.3")
    if (HERE / "Dockerfile").read_text().splitlines()[0] != f"FROM {pins['base']} AS system-tools":
        raise ValueError("Dockerfile base differs from the lock")


def recipe_digest() -> str:
    """Identify every immutable recipe input without using an output artifact."""
    return hashlib.sha256(canonical(recipe_inputs())).hexdigest()


def stage_file(source: Path, target: Path) -> None:
    """Reuse verified bytes, including downloads owned by another local user."""
    try:
        target.hardlink_to(source)
    except OSError:
        shutil.copyfile(source, target)


def validate_derived_pin(cache: Path, pins: dict[str, object]) -> None:
    """Read the CPU source pin from the checked LiteX source itself."""
    rows = {row["tool"]: row for row in pins["sources"]}
    with tarfile.open(cache / rows["litex"]["filename"]) as archive:
        members = [row for row in archive.getmembers()
                   if row.name.endswith("/litex/soc/cores/cpu/vexiiriscv/core.py")]
        if len(members) != 1:
            raise ValueError("LiteX archive has no unique CPU pin source")
        source = archive.extractfile(members[0]).read().decode()
    match = re.search(r'git_setup\("VexiiRiscv",[^\n]+"([0-9a-f]{40})"', source)
    if match is None or match[1] != rows["VexiiRiscv"]["version"]:
        raise ValueError("CPU source differs from the pin derived by the workflow")


def verified_download(row: dict[str, object], target: Path) -> None:
    """Accept only exact-size, exact-hash public artifacts, including cache hits."""
    if target.is_file() and target.stat().st_size == row["size"] and sha256(target) == row["sha256"]:
        return
    if not str(row["url"]).startswith("https://"):
        raise ValueError("source must use public HTTPS")
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + ".part")
    with urllib.request.urlopen(str(row["url"]), timeout=120) as response, temporary.open("wb") as stream:
        shutil.copyfileobj(response, stream, length=1024 * 1024)
    if temporary.stat().st_size != row["size"] or sha256(temporary) != row["sha256"]:
        temporary.unlink()
        raise ValueError(f"source digest mismatch: {row['tool']}")
    temporary.replace(target)


def recipe_inputs() -> dict[str, str]:
    """Bind pins, installers, smoke proof and the existing patch series."""
    files = [HERE / name for name in ("Dockerfile", "install.py", "sources.lock.json",
                                      "build.py", "smoke.py", "sbt-repositories")]
    files += [ROOT / "scripts/ci_rv32_sdk.py", ROOT / "scripts/ci_tool_inventory.py",
              HERE / "tool-inventory.json", ROOT / "sw/litex/patches/apply.sh"]
    files += sorted((ROOT / "sw/litex/patches").glob("*.patch"))
    return {path.relative_to(ROOT).as_posix(): sha256(path) for path in files}


def layer_sources(pins: dict[str, object], name: str) -> list[dict[str, object]]:
    """Follow each tool's public source closure into its own layer manifest."""
    selected = set(LAYER_ROOTS.get(name, ()))
    while True:
        expanded = selected | {row["tool"] for row in pins["sources"] if row.get("parent") in selected}
        if expanded == selected:
            break
        selected = expanded
    return [row for row in pins["sources"] if row["tool"] in selected or
            (name == "python" and row.get("kind") == "python") or
            (name == "sbt" and row.get("kind") == "maven")]


def prepare(work: Path, pins: dict[str, object]) -> tuple[Path, str]:
    """Populate a context from an allowlist; never export the checkout or home."""
    subprocess.run([sys.executable, str(ROOT / "scripts/ci_tool_inventory.py"), "--check"], check=True)
    validate_pins(pins)
    cache = work / "context"
    cache.mkdir(parents=True, exist_ok=True)
    rows = [(row, cache / "debs" / row["filename"]) for row in pins["packages"]]
    rows += [(row, cache / row["filename"]) for row in pins["sources"]]
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda pair: verified_download(*pair), rows))
    validate_derived_pin(cache, pins)
    inputs = recipe_inputs()
    recipe = hashlib.sha256(canonical(inputs)).hexdigest()
    context = work / "build-context"
    if context.exists():
        shutil.rmtree(context)
    context.mkdir()
    for name in ("system", "gtest"):
        packages = [row for row in pins["packages"] if (row["tool"] in GTEST) == (name == "gtest")]
        destination = context / f"debs-{name}"
        destination.mkdir()
        for row in packages:
            stage_file(cache / "debs" / row["filename"], destination / row["filename"])
        (context / f"{name}.sha256").write_text("".join(
            f"{row['sha256']}  debs/{row['filename']}\n" for row in packages))
    stage = context / "recipe"
    stage.mkdir(exist_ok=True)
    for name in ("install.py", "sources.lock.json", "smoke.py", "sbt-repositories"):
        shutil.copyfile(HERE / name, stage / name)
    for name in ("python", *LAYER_ROOTS):
        manifest = {"sources": layer_sources(pins, name)}
        if name == "sbt":
            manifest["sbt_boot"] = pins["sbt_boot"]
        (stage / f"{name}.lock.json").write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n")
        for row in manifest["sources"]:
            target = context / "tool-inputs" / name / row["filename"]
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                target.unlink()
            stage_file(cache / row["filename"], target)
    shutil.copyfile(ROOT / "scripts/ci_rv32_sdk.py", stage / "ci_rv32_sdk.py")
    shutil.copytree(ROOT / "sw/litex/patches", stage / "patches", dirs_exist_ok=True)
    shutil.copyfile(HERE / "Dockerfile", context / "Dockerfile")
    (context / ".dockerignore").write_text(
        "*\n!Dockerfile\n!*.sha256\n!debs-*/\n!debs-*/**\n"
        "!tool-inputs/\n!tool-inputs/**\n!recipe/\n!recipe/**\n")
    (work / "recipe.json").write_text(json.dumps({"sha256": recipe, "inputs": inputs}, indent=2) + "\n")
    return context, recipe


def build(args: argparse.Namespace, pins: dict[str, object]) -> None:
    """Build foreground; each separately selected stage can reuse the same cache."""
    work = args.work.resolve()
    if work.is_relative_to(ROOT) or work == ROOT:
        raise ValueError("build storage must be outside the checkout")
    if args.check_lock:
        validate_pins(pins)
        lock = json.loads((HERE / "image.lock.json").read_text())
        if lock["recipe_digest"] != recipe_digest():
            raise ValueError("image lock does not describe the current recipe")
        print("PASS: image lock describes the current recipe")
        return
    context, recipe = prepare(work, pins)
    if args.prepare_only:
        print(f"Verified context; recipe sha256:{recipe}")
        return
    docker = shlex.split(args.docker_command)
    tag = f"{args.repository}:{recipe}-{args.stage}"
    metadata = work / f"{args.stage}.metadata.json"
    command = [*docker, "buildx", "build", "--load", "--provenance=false", "--network=none",
               "--platform", pins["platform"], "--target", args.stage, "--tag", tag,
               "--metadata-file", str(metadata), "--cache-to", f"type=local,dest={work / 'build-cache'}",
               "--file", str(context / "Dockerfile"), str(context)]
    started = time.monotonic()
    with (work / f"{args.stage}.build.log").open("w") as stream:
        subprocess.run(command, check=True, stdout=stream, stderr=subprocess.STDOUT)
    elapsed_ms = round((time.monotonic() - started) * 1000)
    inspected = json.loads(subprocess.check_output([*docker, "image", "inspect", tag], text=True))[0]
    produced = json.loads(metadata.read_text())
    receipt = {"recipe_sha256": recipe, "stage": args.stage, "image_id": inspected["Id"],
               "image_digest": produced["containerimage.digest"], "size_bytes": inspected["Size"],
               "build_ms": elapsed_ms, "tag": tag}
    (work / f"{args.stage}.receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    if args.stage == "validation-tools":
        subprocess.run([*docker, "tag", tag, f"{args.repository}:{recipe}"], check=True)
        groups = {"system": [row for row in pins["packages"] if row["tool"] not in GTEST],
                  "gtest": [row for row in pins["packages"] if row["tool"] in GTEST]}
        groups.update({name: layer_sources(pins, name) for name in ("python", *LAYER_ROOTS)})
        layers = [{"tool": name, "tools": [{"tool": row["tool"], "version": row["version"],
                                             "source_digest": row["sha256"]} for row in rows],
                   "source_digest": hashlib.sha256(canonical(rows)).hexdigest(), "recipe_digest": recipe}
                  for name, rows in groups.items()]
        lock = {"schema": 1, "platform": pins["platform"], "base": pins["base"],
                "recipe_digest": recipe, "image_digest": receipt["image_digest"],
                "image_id": receipt["image_id"], "layers": layers}
        (HERE / "image.lock.json").write_text(json.dumps(lock, sort_keys=True, indent=2) + "\n")
    print(json.dumps(receipt, sort_keys=True))


def main() -> int:
    """Build a selected stage; failures never produce a final image lock."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--stage", choices=STAGES, default="validation-tools")
    parser.add_argument("--repository", default="fpga-validation")
    parser.add_argument("--docker-command", default="docker")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--check-lock", action="store_true")
    args = parser.parse_args()
    try:
        build(args, json.loads((HERE / "sources.lock.json").read_text()))
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
