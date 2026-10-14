#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Build one tools layer from verified, locally staged public sources."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import zipfile


INPUT = Path("/inputs")
WORK = Path("/build")
PYTHON = "/opt/python/bin/python3"
PINS = json.loads(Path("/recipe/sources.lock.json").read_text())
SOURCES = {row["tool"]: row for row in PINS["sources"]}


def run(argv: list[str], cwd: Path | None = None) -> None:
    """Keep the command's failure as the layer's failure."""
    subprocess.run(argv, cwd=cwd, check=True)


def artifact(name: str) -> Path:
    """Verify a source again at the build boundary."""
    row = SOURCES[name]
    path = INPUT / row["filename"]
    with path.open("rb") as stream:
        actual = hashlib.file_digest(stream, "sha256").hexdigest()
    if actual != row["sha256"] or path.stat().st_size != row["size"]:
        raise ValueError(f"source checksum or size mismatch: {name}")
    return path


def unpack(name: str, destination: Path | None = None) -> Path:
    """Remove one release directory while retaining checked source contents."""
    target = destination or WORK / name
    target.mkdir(parents=True, exist_ok=True)
    with tarfile.open(artifact(name)) as archive:
        for member in archive.getmembers():
            parts = member.name.split("/", 1)
            if len(parts) < 2 or not parts[1]:
                continue
            member.name = parts[1]
            archive.extract(member, target, filter="data")
    return target


def verilator() -> None:
    """Use the workflow's configuration and bounded compilation parallelism."""
    source = unpack("verilator")
    os.environ["VERILATOR_SRC_VERSION"] = SOURCES["verilator"]["version"]
    run(["autoconf"], source)
    run(["./configure", "--prefix=/opt/verilator"], source)
    run(["make", "-j8"], source)
    run(["make", "install"], source)


def yosys() -> None:
    """Build the workflow's exact synthesis and bundled ABC configuration."""
    source = unpack("yosys")
    unpack("abc", source / "abc")
    unpack("cxxopts", source / "libs/cxxopts")
    run(["make", "config-gcc"], source)
    with (source / "Makefile.conf").open("a") as stream:
        stream.write("ENABLE_TCL := 0\nENABLE_READLINE := 0\nENABLE_PLUGINS := 0\n")
    run(["make", "-j8", "PREFIX=/opt/yosys"], source)
    run(["make", "install", "PREFIX=/opt/yosys"], source)
    Path("/opt/yosys/ABC_REV").write_text(SOURCES["abc"]["version"] + "\n")


def sv2v() -> None:
    """Install the one executable from the workflow's checked release ZIP."""
    target = Path("/opt/sv2v/bin")
    target.mkdir(parents=True)
    with zipfile.ZipFile(artifact("sv2v")) as archive:
        names = [name for name in archive.namelist() if name.split("/")[-1] == "sv2v"]
        if len(names) != 1:
            raise ValueError("sv2v archive must contain exactly one executable")
        (target / "sv2v").write_bytes(archive.read(names[0]))
    (target / "sv2v").chmod(0o755)


def sdk() -> None:
    """Retain the existing installer's source verification and relocation proof."""
    run(["python3", "/recipe/ci_rv32_sdk.py", "--destination", "/opt/rv32-sdk",
         "--archive", str(artifact("rv32-sdk"))])


def python_packages() -> None:
    """Install checked wheels, then build the two checked source distributions."""
    run(["python3", "-m", "venv", "/opt/python"])
    rows = [row for row in PINS["sources"] if row.get("kind") == "python"]
    wheels = [str(artifact(row["tool"])) for row in rows if row["filename"].endswith(".whl")]
    run([PYTHON, "-m", "pip", "install", "--no-index", "--no-deps", *wheels])
    archives = [row for row in rows if not row["filename"].endswith(".whl")]
    for row in archives:
        run([PYTHON, "-m", "pip", "install", "--no-index", "--no-deps", "--no-build-isolation",
             str(artifact(row["tool"]))])


def litex() -> None:
    """Install the workflow's Git pins and apply its unmodified patch series."""
    names = ("migen", "litex", "litedram", "liteeth", "litespi", "litex-boards", "pythondata-cpu-vexiiriscv")
    for name in names:
        run([PYTHON, "-m", "pip", "install", "--prefix=/opt/litex", "--no-index", "--no-deps", "--no-build-isolation",
             str(unpack(name))])
    destination = subprocess.check_output(
        [PYTHON, "-c", "import pythondata_cpu_vexiiriscv as p; print(p.data_location)"], text=True).strip()
    cpu = unpack("VexiiRiscv", Path(destination) / "ext/VexiiRiscv")
    placed = {"VexiiRiscv": cpu}
    pending = [row for row in PINS["sources"] if row.get("parent")]
    while pending:
        ready = [row for row in pending if row["parent"] in placed]
        if not ready:
            raise ValueError("unresolved recursive CPU source")
        for row in ready:
            placed[row["tool"]] = unpack(row["tool"], placed[row["parent"]] / row["path"])
            pending.remove(row)
    run(["bash", "/recipe/patches/apply.sh"])
    run([PYTHON, "-m", "pip", "check"])


def oracle() -> None:
    """Compile the exact field oracle and its required recursive source closure."""
    source = unpack("tsn-gen")
    yaml = unpack("rapidyaml", source / "external/rapidyaml")
    core = unpack("c4core", yaml / "ext/c4core")
    for name in ("c4-cmake", "debugbreak", "fast_float"):
        unpack(name, core / SOURCES[name]["path"])
    run(["cmake", "-S", str(source), "-B", str(source / "build"),
         "-DCMAKE_BUILD_TYPE=Release", "-DENABLE_PARSER_TESTS=OFF"])
    run(["cmake", "--build", str(source / "build"), "--target", "packet_gen", "--parallel", "8"])
    destination = Path("/opt/tsn-gen")
    (destination / "build/traffic-gen").mkdir(parents=True)
    shutil.copyfile(source / "build/traffic-gen/packet_gen", destination / "build/traffic-gen/packet_gen")
    (destination / "build/traffic-gen/packet_gen").chmod(0o755)
    shutil.copytree(source / "protocols", destination / "protocols")
    for name in ("LICENSE", "LICENSE.md", "LICENSE.txt"):
        if (source / name).is_file():
            shutil.copyfile(source / name, destination / name)
    Path("/opt/tsn-gen/SOURCE_REV").write_text(SOURCES["tsn-gen"]["version"] + "\n")


def sbt() -> None:
    """Install the launcher and its checksummed offline dependency cache."""
    unpack("sbt", Path("/opt/sbt"))
    cache = Path("/opt/sbt/cache")
    by_hash = {}
    for row in PINS["sources"]:
        if row.get("kind") != "maven":
            continue
        source = artifact(row["tool"])
        by_hash[row["sha256"]] = source
        if "cache_path" not in row:
            continue
        target = cache / row["cache_path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        data = source.read_bytes()
        (target.parent / ("." + target.name + "__sha1")).write_text(hashlib.sha1(data).hexdigest())
        (target.parent / ("." + target.name + "__sha1.computed")).write_bytes(hashlib.sha1(data).digest())
        (target.parent / ("." + target.name + ".checked")).touch()
    for row in PINS["sbt_boot"]:
        target = cache / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(by_hash[row["sha256"]], target)
    shutil.copyfile("/recipe/sbt-repositories", "/opt/sbt/repositories")


def main() -> int:
    """Build one named layer without fetching or resolving a dependency."""
    WORK.mkdir(exist_ok=True)
    installers = {"verilator": verilator, "yosys": yosys, "sv2v": sv2v,
                  "rv32-sdk": sdk, "python": python_packages, "litex": litex,
                  "tsn-gen": oracle, "sbt": sbt}
    name = sys.argv[1]
    if name in ("node", "gh"):
        unpack(name, Path("/opt") / name)
    else:
        installers[name]()
    shutil.rmtree(WORK)
    run(["python3", "/recipe/normalize.py", "/opt"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
