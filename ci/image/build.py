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
import tempfile
import time
import urllib.error
import urllib.request

import image_archive
import image_lock
import privacy


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
STAGES = ("system-tools", "gtest-tools", "python-tools", "litex-tools", "verilator-tools", "yosys-tools",
          "rv32-tools", "sv2v-tools", "sbt-tools", "oracle-tools", "node-tools", "gh-tools", "validation-tools")
GTEST = {"googletest", "libgtest-dev", "libgmock-dev"}
SOURCE_DATE_EPOCH = 1791940308
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
    urls = [row["url"], *row.get("fallback_urls", [])]
    if any(not str(url).startswith("https://") for url in urls):
        raise ValueError("source must use public HTTPS")
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=target.parent, prefix=target.name + ".", suffix=".part") as stream:
        temporary = Path(stream.name)
        for index, url in enumerate(urls):
            try:
                with urllib.request.urlopen(str(url), timeout=120) as response:
                    shutil.copyfileobj(response, stream, length=1024 * 1024)
                break
            except urllib.error.HTTPError as error:
                if error.code != 404 or index == len(urls) - 1:
                    raise
                stream.seek(0)
                stream.truncate()
        stream.flush()
        if temporary.stat().st_size != row["size"] or sha256(temporary) != row["sha256"]:
            raise ValueError(f"source digest mismatch: {row['tool']}")
        # Copy to the target atomically while keeping the temporary file's
        # context manager responsible for cleanup, even on failed downloads.
        staged = temporary.with_suffix(".verified")
        stage_file(temporary, staged)
        staged.replace(target)


def recipe_inputs() -> dict[str, str]:
    """Bind pins, installers, smoke proof and the existing patch series."""
    files = [HERE / name for name in ("Dockerfile", "install.py", "sources.lock.json",
                                      "build.py", "smoke.py", "sbt-repositories", "normalize.py",
                                      "image_lock.py", "image_archive.py", "privacy.py", "privacy.json",
                                      "patch_provenance.py")]
    files += [ROOT / "scripts/ci_rv32_sdk.py", ROOT / "scripts/ci_tool_inventory.py",
              HERE / "tool-inventory.json", HERE / "command-table.json",
              ROOT / "scripts/ci_command_table.py", ROOT / "sw/litex/patches/apply.sh"]
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


def layer_records(pins: dict[str, object]) -> list[dict[str, object]]:
    """Bind each final filesystem layer to its own inputs and installer recipe."""
    groups = {"system": [row for row in pins["packages"] if row["tool"] not in GTEST],
              "gtest": [row for row in pins["packages"] if row["tool"] in GTEST]}
    for name in ("python", "litex", "verilator", "yosys", "rv32", "sv2v", "sbt", "oracle", "node", "gh"):
        groups[name] = layer_sources(pins, name)
    groups["validation"] = []
    dockerfile = (HERE / "Dockerfile").read_text()
    stages = [part for part in re.split(r"(?m)^FROM ", dockerfile) if part]
    result = []
    for name, rows in groups.items():
        stage = next(part for part in stages if part.splitlines()[0].endswith(f"AS {name}-tools"))
        selected = {"stage": stage, "base": pins["base"], "epoch": SOURCE_DATE_EPOCH,
                    "sources": rows, "normalizer": sha256(HERE / "normalize.py")}
        parent = stage.split()[0].removesuffix("-tools")
        if parent in groups:
            selected["parent_recipe_digest"] = next(row["recipe_digest"] for row in result if row["tool"] == parent)
        if name not in ("system", "gtest", "validation"):
            selected["installer"] = sha256(HERE / "install.py")
        if name == "sbt":
            selected["boot"] = pins["sbt_boot"]
            selected["repositories"] = sha256(HERE / "sbt-repositories")
        if name == "litex":
            patches = sorted((ROOT / "sw/litex/patches").glob("*"))
            selected["patches"] = {p.name: sha256(p) for p in patches if p.is_file()}
        if name == "rv32":
            selected["sdk_installer"] = sha256(ROOT / "scripts/ci_rv32_sdk.py")
        if name == "validation":
            selected["smoke"] = sha256(HERE / "smoke.py")
            selected["pins"] = sha256(HERE / "sources.lock.json")
        result.append({"tool": name, "tools": [{"tool": row["tool"], "version": row["version"],
                                                "source_digest": row["sha256"]} for row in rows],
                       "source_digest": image_lock.digest(rows), "recipe_digest": image_lock.digest(selected)})
    return result


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
    for name in ("install.py", "sources.lock.json", "smoke.py", "sbt-repositories", "normalize.py"):
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


def checked_artifact(path: Path, work: Path, pins: dict[str, object]) -> dict[str, object]:
    """Re-prove upstream allowances from authenticated public source archives."""
    upstream = privacy.provenance(pins, work / "context", privacy.Policy())
    artifact = image_archive.inspect(path, pins["platform"], upstream)
    (work / "privacy-report.json").write_text(json.dumps(artifact, sort_keys=True, indent=2) + "\n")
    return artifact


def record_lock(work: Path, pins: dict[str, object], receipt: dict[str, object]) -> None:
    """Write a complete lock only after recipe, image and privacy verification."""
    recipe = receipt["recipe_sha256"]
    if recipe_digest() != recipe:
        raise ValueError("recipe changed during the build; final lock was not written")
    artifact = checked_artifact(work / "image.tar", work, pins)
    if recipe_digest() != recipe:
        raise ValueError("recipe changed during artifact verification; final lock was not written")
    if artifact["image_digest"] != receipt["image_digest"] or artifact["image_id"] != receipt["image_id"]:
        raise ValueError("exported image differs from build receipt")
    layers = layer_records(pins)
    base_count = len(pins["base_layers"])
    if artifact["layers"][:base_count] != pins["base_layers"]:
        raise ValueError("built image base layers differ from the pinned base")
    for row, measured in zip(layers, artifact["layers"][base_count:], strict=True):
        row.update(measured)
    lock = {"schema": 2, "platform": pins["platform"], "base": pins["base"], "base_layers": pins["base_layers"],
            "recipe_digest": recipe, "image_digest": receipt["image_digest"],
            "image_id": receipt["image_id"], "layers": layers}
    image_lock.validate(lock, pins, recipe, layer_records(pins))
    image_lock.verify_artifact(lock, artifact)
    (HERE / "image.lock.json").write_text(json.dumps(lock, sort_keys=True, indent=2) + "\n")


def build(args: argparse.Namespace, pins: dict[str, object]) -> None:
    """Build foreground; each separately selected stage can reuse the same cache."""
    work = args.work.resolve()
    if work.is_relative_to(ROOT) or work == ROOT:
        raise ValueError("build storage must be outside the checkout")
    if args.check_lock:
        validate_pins(pins)
        lock = json.loads((HERE / "image.lock.json").read_text())
        image_lock.validate(lock, pins, recipe_digest(), layer_records(pins))
        if args.verify_archive:
            image_lock.verify_artifact(lock, checked_artifact(args.verify_archive, work, pins))
            print("PASS: image identity verified against exported manifest, config and every layer")
        else:
            print("PASS: complete recipe consistency; image identity UNVERIFIED without --verify-archive")
        return
    if args.record_lock:
        record_lock(work, pins, json.loads((work / "validation-tools.receipt.json").read_text()))
        print("PASS: exported image authenticated; final lock recorded")
        return
    context, recipe = prepare(work, pins)
    if args.prepare_only:
        print(f"Verified context; recipe sha256:{recipe}")
        return
    docker = shlex.split(args.docker_command)
    tag = f"{args.repository}:{recipe}-{args.stage}"
    metadata = work / f"{args.stage}.metadata.json"
    command = [*docker, "buildx", "build", "--output", "type=image,rewrite-timestamp=true",
               "--build-arg", f"SOURCE_DATE_EPOCH={SOURCE_DATE_EPOCH}", "--provenance=false", "--network=none",
               "--platform", pins["platform"], "--target", args.stage, "--tag", tag,
               "--metadata-file", str(metadata), "--cache-to", f"type=local,dest={work / 'build-cache'}",
               "--file", str(context / "Dockerfile"), str(context)]
    if args.no_cache:
        command.insert(len(docker) + 2, "--no-cache")
    started = time.monotonic()
    with (work / f"{args.stage}.build.log").open("w") as stream:
        subprocess.run(command, check=True, stdout=stream, stderr=subprocess.STDOUT)
    elapsed_ms = round((time.monotonic() - started) * 1000)
    inspected = json.loads(subprocess.check_output([*docker, "image", "inspect", tag], text=True))[0]
    produced = json.loads(metadata.read_text())
    archive = work / ("image.tar" if args.stage == "validation-tools" else f"{args.stage}.tar")
    subprocess.run([*docker, "image", "save", "--output", str(archive), tag], check=True)
    descriptor, manifest, _ = image_archive.metadata(archive, pins["platform"])
    if descriptor["digest"] != produced["containerimage.digest"]:
        raise ValueError("exported manifest differs from the build result")
    receipt = {"recipe_sha256": recipe, "stage": args.stage, "image_id": manifest["config"]["digest"],
               "image_digest": produced["containerimage.digest"], "size_bytes": inspected["Size"],
               "build_ms": elapsed_ms, "tag": tag}
    (work / f"{args.stage}.receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    if args.stage == "validation-tools":
        if not args.defer_lock:
            record_lock(work, pins, receipt)
        subprocess.run([*docker, "tag", tag, f"{args.repository}:{recipe}"], check=True)
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
    parser.add_argument("--verify-archive", type=Path)
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument("--defer-lock", action="store_true", help="export only; complete with --record-lock")
    parser.add_argument("--record-lock", action="store_true", help="authenticate an existing build export")
    args = parser.parse_args()
    try:
        build(args, json.loads((HERE / "sources.lock.json").read_text()))
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
