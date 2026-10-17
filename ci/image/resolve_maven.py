#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Regenerate public Scala artifact declarations from a disposable resolution."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import urllib.request
import zipfile


def boot_coordinates(path: Path) -> tuple[str, str, str]:
    """Read the bootstrap JAR's coordinates, refusing an unidentified artifact."""
    with zipfile.ZipFile(path) as archive:
        manifest = archive.read("META-INF/MANIFEST.MF").decode().replace("\r\n ", "").replace("\r", "")
        fields = dict(line.split(": ", 1) for line in manifest.splitlines() if ": " in line)
        names = [name for name in archive.namelist() if name.endswith("/pom.properties")]
        properties = dict(line.split("=", 1) for line in archive.read(names[0]).decode().splitlines()
                          if "=" in line and not line.startswith("#")) if names else {}
    group = properties.get("groupId", fields.get("Implementation-Vendor-Id"))
    version = properties.get("version", fields.get("Implementation-Version"))
    if path.name in ("scala-library.jar", "scala-reflect.jar", "scala-compiler.jar"):
        return "org.scala-lang", path.stem, version
    if not version:
        match = re.match(r"(.+?)-(\d.*)\.jar$", path.name)
        version = match[2] if match else None
    artifact = path.name.removesuffix("-" + str(version) + ".jar")
    groups = {"ssl-config-core_2.12": "com.typesafe", "disruptor": "com.lmax",
              "caffeine": "com.github.ben-manes.caffeine", "jna": "net.java.dev.jna",
              "jna-platform": "net.java.dev.jna", "reactive-streams": "org.reactivestreams",
              "checker-qual": "org.checkerframework", "config": "com.typesafe"}
    group = group or groups.get(artifact)
    if artifact.startswith(("scala-xml", "scala-parser", "scala-collection")):
        group = "org.scala-lang.modules"
    if not group or not version:
        raise ValueError("bootstrap JAR has no public coordinates")
    return group, artifact, version


def row_for(path: Path, relative: str, version: str, url: str) -> dict[str, object]:
    """Describe resolved bytes without treating local cache provenance as proof."""
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    filename = url.rsplit("/", 1)[1]
    return {"tool": "sbt:" + relative, "version": version, "url": url,
            "sha256": digest, "size": len(data), "filename": "maven/" + digest + "-" + filename,
            "kind": "maven"}


def resolved(cache: Path) -> tuple[list[dict[str, object]], list[dict[str, str]]]:
    """Derive the downloaded closure and every bootstrap placement from files."""
    rows = []
    for path in sorted((cache / "coursier/https").rglob("*")):
        if not path.is_file() or path.name.startswith(".") or path.suffix not in (".jar", ".pom", ".xml"):
            continue
        relative = path.relative_to(cache / "coursier/https").as_posix()
        row = row_for(path, relative, path.parent.name, "https://" + relative)
        row["cache_path"] = path.relative_to(cache).as_posix()
        row["url"] = row["url"].replace("https://repo.scala-sbt.org/scalasbt/sbt-plugin-releases/",
                                       "https://scala.jfrog.io/artifactory/sbt-plugin-releases/")
        rows.append(row)
    hashes = {row["sha256"] for row in rows}
    boot = []
    for path in sorted((cache / "boot").rglob("*.jar")):
        if "-bin_" in path.name:
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest not in hashes:
            group, artifact, version = boot_coordinates(path)
            relative = f"{group.replace('.', '/')}/{artifact}/{version}/{artifact}-{version}.jar"
            rows.append(row_for(path, relative, version, "https://repo.maven.apache.org/maven2/" + relative))
            hashes.add(digest)
        boot.append({"sha256": digest, "path": path.relative_to(cache).as_posix()})
    if not rows or not boot:
        raise ValueError("empty Scala resolution or bootstrap closure")
    return sorted(rows, key=lambda row: row["tool"]), boot


def verify(row: dict[str, object]) -> None:
    """Accept a cache artifact only when its public download has identical bytes."""
    with urllib.request.urlopen(row["url"], timeout=120) as response:
        data = response.read()
    if len(data) != row["size"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
        raise ValueError("public Scala artifact differs from resolved bytes")


def main() -> int:
    """Require public-byte verification before writing a newly resolved closure."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    path = Path(__file__).with_name("sources.lock.json")
    pins = json.loads(path.read_text())
    rows, boot = resolved(args.cache)
    if args.write:
        with ThreadPoolExecutor(max_workers=4) as pool:
            list(pool.map(verify, rows))
        pins["sources"] = sorted([row for row in pins["sources"] if row.get("kind") != "maven"] + rows,
                                 key=lambda row: row["tool"])
        pins["sbt_boot"] = boot
        path.write_text(json.dumps(pins, sort_keys=True, indent=2) + "\n")
    elif rows != [row for row in pins["sources"] if row.get("kind") == "maven"] or boot != pins["sbt_boot"]:
        raise ValueError("Scala resolution differs from source lock")
    print(f"PASS: {len(rows)} Scala artifacts and {len(boot)} bootstrap placements")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
