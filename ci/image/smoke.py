#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Exercise the installed tool families without a product build or networking."""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def run(argv: list[str], cwd: Path | None = None) -> str:
    """Record commands and retain every nonzero exit as a smoke failure."""
    result = subprocess.run(argv, cwd=cwd, check=True, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(json.dumps({"argv": argv, "output": result.stdout.strip(), "rc": result.returncode}), flush=True)
    return result.stdout


def versions(pins: dict[str, object]) -> None:
    """Compare installed distribution and Python package versions to the lock."""
    assert sys.version_info[:3] == (3, 12, 3), sys.version
    print(json.dumps({"python": sys.version}))
    names = [row["tool"] for row in pins["packages"]]
    output = run(["dpkg-query", "-W", "-f=${Package}\t${Version}\n", *names])
    actual = dict(line.split("\t") for line in output.splitlines())
    for row in pins["packages"]:
        assert actual[row["tool"]] == row["version"], row["tool"]
    for row in pins["sources"]:
        if row.get("kind") == "python":
            version = importlib.metadata.version(row["tool"])
            assert version == row["version"], (row["tool"], version)
            print(json.dumps({"package": row["tool"], "version": version}))
    for name in ("migen", "litex", "liteeth", "litedram", "litespi", "litex-boards",
                 "pythondata-cpu-vexiiriscv"):
        print(json.dumps({"package": name, "version": importlib.metadata.version(name)}))
    source_versions = {row["tool"]: row["version"] for row in pins["sources"]}
    package_versions = {row["tool"]: row["version"].split(":")[-1].split("-")[0] for row in pins["packages"]}
    checks = ((["verilator", "--version"], "rev " + source_versions["verilator"]),
              (["yosys", "-V"], "Yosys " + source_versions["yosys"].removeprefix("v")),
              (["sv2v", "--version"], source_versions["sv2v"]),
              (["riscv32-linux-gcc", "-dumpfullversion"], "14.3.0"),
              (["sbt", "--script-version"], "1.10.7"),
              (["node", "--version"], "v22.23.3"), (["gh", "--version"], "2.102.0"))
    for argv, expected in checks:
        assert expected in run(argv), (argv, expected)
    distribution = (("git", "git"), ("cmake", "cmake"), ("ninja", "ninja-build"),
                    ("gcc", "gcc-13"), ("g++", "g++-13"), ("clang", "clang-18"),
                    ("gcov", "gcc-13"), ("make", "make"), ("autoconf", "autoconf"),
                    ("flex", "flex"), ("bison", "bison"), ("automake", "automake"),
                    ("help2man", "help2man"), ("curl", "curl"), ("pkg-config", "pkg-config"),
                    ("rsvg-convert", "librsvg2-bin"), ("java", "openjdk-17-jre-headless"),
                    ("xz", "xz-utils"), ("sudo", "sudo"))
    for tool, package in distribution:
        expected = package_versions[package].rsplit("really", 1)[-1].split("+")[0]
        option = "-version" if tool == "java" else "--version"
        assert expected in run([tool, option]), (tool, expected)
    for argv in (["gcc", "--version"], ["g++", "--version"], ["clang", "--version"],
                 ["gcov", "--version"], ["cmake", "--version"], ["git", "--version"],
                 ["make", "--version"], ["autoconf", "--version"], ["flex", "--version"],
                 ["bison", "--version"], ["automake", "--version"], ["help2man", "--version"],
                 ["ninja", "--version"], ["curl", "--version"], ["python3", "-m", "pip", "--version"],
                 ["perl", "-v"], ["pkg-config", "--version"],
                 ["rsvg-convert", "--version"], ["java", "-version"],
                 ["/opt/tsn-gen/build/traffic-gen/packet_gen", "--version"]):
        run(argv)


def native_smokes(work: Path) -> None:
    """Compile, link and run host, coverage, unit-test and build-system checks."""
    source = work / "smoke.c"
    source.write_text("int main(void) { return 0; }\n")
    for cc in ("gcc", "clang"):
        run([cc, "-std=c11", "-Wall", "-Werror", str(source), "-o", str(work / cc)])
        run([str(work / cc)])
    run(["gcc", "--coverage", "-c", "smoke.c", "-o", "smoke.o"], work)
    run(["gcc", "--coverage", "smoke.o", "-o", "covered"], work)
    run([str(work / "covered")])
    assert "100.00%" in run(["gcov", "-b", "smoke.c"], work)
    (work / "gtest.cpp").write_text(
        '#include <gmock/gmock.h>\nTEST(Image, Checks) { EXPECT_THAT(7, testing::Eq(7)); }\n')
    run(["g++", "-std=c++20", "gtest.cpp", "-lgmock", "-lgtest_main", "-lgtest", "-pthread", "-o", "gtest"], work)
    assert "PASSED" in run([str(work / "gtest")])
    (work / "CMakeLists.txt").write_text(
        "cmake_minimum_required(VERSION 3.21)\nproject(smoke C)\nadd_executable(smoke smoke.c)\n")
    run(["cmake", "-G", "Ninja", "-S", str(work), "-B", str(work / "cmake")])
    run(["cmake", "--build", str(work / "cmake"), "--parallel", "2"])
    run([str(work / "cmake/smoke")])
    (work / "configure.ac").write_text("AC_INIT([smoke], [1])\nAC_PROG_CC\nAC_OUTPUT\n")
    run(["autoconf"], work)
    run(["bash", "configure"], work)
    run(["git", "init", "--quiet", str(work / "git")])
    assert run(["git", "-C", str(work / "git"), "rev-parse", "--is-inside-work-tree"]).strip() == "true"
    assert run(["perl", "-e", "print 6*7"]).strip() == "42"
    assert run(["pkg-config", "--modversion", "gtest"]).strip() == "1.14.0"
    (work / "smoke.tcl").write_text('puts [expr {6 * 7}]\n')
    assert run(["tclsh", str(work / "smoke.tcl")]).strip() == "42"
    (work / "scanner.l").write_text(
        '%option noyywrap\n%%\n. { }\n\\n { }\n%%\nint main(void) { return yylex(); }\n')
    run(["flex", "scanner.l"], work)
    run(["gcc", "lex.yy.c", "-o", "scanner"], work)
    with (work / "smoke.c").open() as stream:
        subprocess.run([str(work / "scanner")], stdin=stream, check=True)
    (work / "parser.y").write_text(
        '%{\nint yylex(void) { return 0; }\nvoid yyerror(const char *s) { (void)s; }\n%}\n'
        '%%\nstart: %empty;\n%%\nint main(void) { return yyparse(); }\n')
    run(["bison", "parser.y"], work)
    run(["gcc", "parser.tab.c", "-o", "parser"], work)
    run([str(work / "parser")])
    run(["help2man", "--no-info", "--output", str(work / "gcc.1"), "gcc"])
    assert (work / "gcc.1").stat().st_size > 100
    assert run(["curl", "--silent", "--fail", source.as_uri()]) == source.read_text()
    run(["xz", "--keep", str(source)])
    assert run(["xz", "--decompress", "--stdout", str(source) + ".xz"]) == source.read_text()
    assert "sudo" in run(["sudo", "--help"])
    assert run(["node", "-e", "require('assert').strictEqual(6*7, 42); console.log('JS_OK')"]).strip() == "JS_OK"
    assert "gh api" in run(["gh", "api", "--help"])
    run(["python3", "-m", "pip", "check"])


def hdl_smokes(work: Path) -> None:
    """Exercise simulation, conversion, synthesis and the bundled mapper."""
    simulation = work / "simulation.sv"
    simulation.write_text(
        'module simulation; initial begin assert (6*7 == 42) else $fatal; $finish; end endmodule\n')
    run(["verilator", "--binary", "--assert", "--top-module", "simulation", "-j", "2",
         "--Mdir", str(work / "verilated"), str(simulation)])
    run([str(work / "verilated/Vsimulation")])
    rtl = work / "logic.sv"
    rtl.write_text("module smoke(input logic a, b, output logic y); assign y = a & b; endmodule\n")
    converted = run(["sv2v", str(rtl)])
    (work / "logic.v").write_text(converted)
    run(["yosys", "-p", "read_verilog logic.v; synth -top smoke; abc -g AND; check -assert"], work)
    run(["yosys-abc", "-c", "version"])
    source = work / "rv32.c"
    source.write_text("void _start(void) { for (;;) {} }\n")
    elf = work / "rv32.elf"
    run(["riscv32-linux-gcc", "-march=rv32i", "-mabi=ilp32", "-ffreestanding", "-fno-stack-protector",
         "-nostdlib", "-nostartfiles", "-static", "-Wl,-e,_start", str(source), "-o", str(elf)])
    header = run(["riscv32-linux-readelf", "-h", "-A", str(elf)])
    assert "ELF32" in header and "RISC-V" in header and "rv32i" in header


def python_smokes(work: Path) -> None:
    """Exercise the rendering, parsing, BDD and hardware-description libraries."""
    import cffi
    import cmarkgfm
    import html5lib
    import pycparser
    import pyslang
    import six
    import wavedrom
    import webencodings
    import yaml
    from migen import Module, Signal
    from migen.fhdl import verilog
    from litex.soc.interconnect.csr import CSRStorage

    assert yaml.safe_load("smoke: 42")["smoke"] == 42
    assert "<h1>smoke</h1>" in cmarkgfm.github_flavored_markdown_to_html("# smoke\n")
    assert len(html5lib.parseFragment("<p>smoke</p>")) == 1
    assert cffi.FFI().sizeof("int") >= 2
    assert pycparser.CParser().parse("int smoke;").ext
    assert six.StringIO("smoke").read() == "smoke"
    assert webencodings.lookup("utf-8").name == "utf-8"
    assert not list(pyslang.syntax.SyntaxTree.fromText("module smoke; endmodule").diagnostics)
    diagram = wavedrom.render('{"signal":[{"name":"clk","wave":"p..."}]}')
    diagram.saveas(str(work / "wave.svg"))
    run(["rsvg-convert", "-o", str(work / "wave.png"), str(work / "wave.svg")])
    assert (work / "wave.png").read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    module = Module()
    a, b = Signal(name="a"), Signal(name="b")
    module.comb += b.eq(a)
    assert "assign" in str(verilog.convert(module, ios={a, b}))
    assert CSRStorage(1, name="smoke").size == 1
    for name in ("litedram", "liteeth", "litespi", "litex_boards", "pythondata_cpu_vexiiriscv"):
        importlib.import_module(name)
    features = work / "features"
    (features / "steps").mkdir(parents=True)
    (features / "smoke.feature").write_text("Feature: image\n  Scenario: arithmetic\n    Given arithmetic works\n")
    (features / "steps/steps.py").write_text(
        'from behave import given\n@given("arithmetic works")\ndef smoke(context):\n    assert 6 * 7 == 42\n')
    run(["behave", str(features), "--no-capture", "-f", "plain"])
    print("PASS: Python, renderer, diagram, BDD and LiteX smoke checks", flush=True)


def scala_oracle_smokes(work: Path) -> None:
    """Run a Scala program and generate a real deterministic oracle packet."""
    (work / "Smoke.java").write_text(
        'class Smoke { public static void main(String[] args) { System.out.println(42); } }\n')
    run(["javac", str(work / "Smoke.java")])
    assert run(["java", "-cp", str(work), "Smoke"]).strip() == "42"
    scala = work / "scala"
    (scala / "project").mkdir(parents=True)
    (scala / "project/build.properties").write_text("sbt.version=1.10.0\n")
    (scala / "build.sbt").write_text('scalaVersion := "2.12.19"\n')
    (scala / "Smoke.scala").write_text('object Smoke extends App { assert(6 * 7 == 42); println("SCALA_OK") }\n')
    assert "SCALA_OK" in run(["sbt", "--batch", "show sbtVersion", "runMain Smoke"], scala)
    oracle = "/opt/tsn-gen/build/traffic-gen/packet_gen"
    output = run([oracle, "--yaml-dir", "/opt/tsn-gen/protocols/application/1722_1/aecp",
                  "--interface", "atdecc_aecp_acquire_entity::AECP_ACQUIRE_ENTITY::AECP_ACQUIRE_ENTITY_IF",
                  "--count", "1", "--seed", "42", "--output", "json"])
    packet = json.loads(output)
    assert packet["hex"] and packet["fields"]


def main() -> int:
    """Run inside the image with networking disabled and external scratch mounted."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    pins = json.loads(Path(__file__).with_name("sources.lock.json").read_text())
    versions(pins)
    with tempfile.TemporaryDirectory(dir=args.work, prefix="smoke-") as directory:
        work = Path(directory)
        native_smokes(work)
        hdl_smokes(work)
        python_smokes(work)
        scala_oracle_smokes(work)
    print("PASS: all image tool families", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
