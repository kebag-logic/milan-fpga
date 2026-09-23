#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Run actual gate 1b with an audited disposable SDK or absent cross tools.

--sdk-destination maps only the existing absolute selector's argv[0]. It
changes neither HOME, PATH, the shared compiler nor any remaining argument.
This is local compatibility evidence, not proof of hosted selector adoption.
--absent hides cross candidates while retaining real host version/RV32 probes;
any attempted firmware compilation through a host compiler is an error.
"""

import argparse
import contextlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any, TextIO
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import ci_rv32_sdk as sdk  # noqa: E402
import test_builder as builder  # noqa: E402


class CompilerAudit:
    """Intercept only compiler candidate calls; preserve argv and subprocess options."""

    def __init__(self, stream: TextIO, destination: Path | None) -> None:
        self.stream = stream
        self.destination = destination
        self.selector = str(Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc")
        self.cross = {self.selector, "riscv64-elf-gcc", "riscv32-unknown-elf-gcc"}
        self.native = {"cc", "gcc"}
        self.run = subprocess.run
        self.compiles = 0
        self.hidden = set()

    def invoke(self, argv: list[str], **kwargs: Any) -> subprocess.CompletedProcess:
        """Log requested and executed argv with the actual return code."""
        requested = [str(arg) for arg in argv]
        if requested[0] not in self.cross | self.native:
            return self.run(argv, **kwargs)
        record = {"requested_argv": requested}
        if self.destination is None and requested[0] in self.cross:
            self.hidden.add(requested[0])
            record.update(actual_argv=None, result="deliberately absent")
            self.stream.write(json.dumps(record) + "\n")
            raise FileNotFoundError("deliberately absent RV32 candidate")
        actual = requested.copy()
        if self.destination is not None and requested[0] == self.selector:
            actual[0] = str(self.destination / sdk.COMPILER)
        elif requested[1:] != ["--version"]:
            if not any(Path(arg).name == "probe.c" for arg in requested[1:]):
                raise AssertionError("host/alternate compiler attempted firmware compilation")
        result = self.run(actual, **kwargs)
        record.update(actual_argv=actual, returncode=result.returncode)
        if "-std=gnu99" in actual:
            self.compiles += 1
        if "-S" in actual and "-std=gnu99" in actual:
            assembly = Path(actual[actual.index("-o") + 1])
            if result.returncode == 0 and assembly.is_file():
                arch = re.search(r'\.attribute\s+arch,\s*"([^"]+)"',
                                 assembly.read_text())
                record["assembly_arch"] = arch.group(1) if arch else None
        self.stream.write(json.dumps(record) + "\n")
        self.stream.flush()
        return result


def run_gate(destination: Path | None, audit_path: Path, require: bool) -> None:
    """Execute all retained gate 1b controls and report every registered skip."""
    if destination is not None:
        sdk.verify(destination)
    with audit_path.open("w") as stream:
        audit = CompilerAudit(stream, destination)
        print(f"Compiler mode: {'mapped disposable SDK' if destination else 'absent cross tools'}")
        print(f"Compiler audit: {audit_path}")
        if destination is not None:
            print(f"argv[0] mapping: {audit.selector} -> {destination / sdk.COMPILER}")
        with tempfile.TemporaryDirectory(prefix="milan-firmware-gate-") as tmp:
            argv = [__file__] + (["--require-rv32"] if require or destination else [])
            with patch.object(subprocess, "run", side_effect=audit.invoke), \
                    patch.object(sys, "argv", argv), \
                    patch.object(builder, "OUT", Path(tmp)), \
                    patch.object(builder, "SKIPPED", []):
                builder.test_baremetal_profile_contract()
                if destination is not None:
                    assert audit.compiles > 0, "no SDK firmware compilation executed"
                    assert not any("THREE INSTRUMENTS" in why
                                   for _, why, _ in builder.SKIPPED), builder.SKIPPED
                else:
                    assert audit.hidden == audit.cross, audit.hidden
                    assert audit.compiles == 0, "absent mode compiled firmware"
                    assert any("THREE INSTRUMENTS" in why for _, why, _ in builder.SKIPPED), \
                        "absent instruments were not registered NOT RUN"
                for gate, why, _ in builder.SKIPPED:
                    print(f"NOT RUN [{gate}]: {why}")
                print(f"GATE 1b PASS; {len(builder.SKIPPED)} NOT RUN; "
                      f"{audit.compiles} actual firmware compiler invocations")


def selftest() -> None:
    """Prove argv preservation, cross-tool absence, and host fallback refusal."""
    import io

    stream = io.StringIO()
    audit = CompilerAudit(stream, Path("/disposable/sdk"))
    original = [audit.selector, "-S", "-o", "file.s", "unit.c"]
    with patch.object(audit, "run", return_value=subprocess.CompletedProcess([], 7)) as run:
        assert audit.invoke(original, cwd="/tmp", text=True).returncode == 7
        run.assert_called_once_with(
            ["/disposable/sdk/bin/riscv32-linux-gcc", *original[1:]],
            cwd="/tmp", text=True)
    assert original[0] == audit.selector
    record = json.loads(stream.getvalue())
    assert record["requested_argv"] == original and record["returncode"] == 7
    absent = CompilerAudit(io.StringIO(), None)
    with patch.object(absent, "run") as run:
        for candidate in absent.cross:
            try:
                absent.invoke([candidate, "--version"])
            except FileNotFoundError:
                pass
            else:
                raise AssertionError("absent candidate was executed")
        for candidate in absent.native:
            try:
                absent.invoke([candidate, "-S", "firmware.c"])
            except AssertionError as exc:
                assert "attempted firmware compilation" in str(exc)
            else:
                raise AssertionError("host fallback was accepted")
        run.assert_not_called()
    with tempfile.TemporaryDirectory(prefix="rv32-require-test-") as tmp:
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                run_gate(None, Path(tmp) / "absent.jsonl", require=True)
            except AssertionError as exc:
                assert "--require-rv32: the hosted firmware instruments must run" in str(exc), exc
            else:
                raise AssertionError("--require-rv32 accepted an absent compiler")
        real_run = subprocess.run

        def alternate_candidate(argv: list[str], **kwargs: Any) -> subprocess.CompletedProcess:
            """An alternate RV32 tool answers while the settled selector is absent."""
            if str(argv[0]) == "riscv32-unknown-elf-gcc":
                return subprocess.CompletedProcess(argv, 0, "fixture RV32\n", "")
            if str(argv[0]) in absent.cross:
                raise FileNotFoundError("settled compiler absent")
            return real_run(argv, **kwargs)

        with patch.object(subprocess, "run", side_effect=alternate_candidate), \
                patch.object(sys, "argv", [__file__, "--require-rv32"]), \
                patch.object(builder, "OUT", Path(tmp)), \
                contextlib.redirect_stdout(io.StringIO()):
            try:
                builder.test_baremetal_profile_contract()
            except AssertionError as exc:
                assert "the provisioned absolute SDK selector must be adopted" in str(exc), exc
            else:
                raise AssertionError("--require-rv32 accepted an alternate compiler")
    print("compiler audit selftest: argv mapping, result propagation, absence, "
          "host refusal and actual absent/alternate --require-rv32 refusals PASS")


def main() -> None:
    """Keep the weaker mode explicit and the audit durable."""
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--sdk-destination", type=Path)
    modes.add_argument("--absent", action="store_true")
    modes.add_argument("--selftest", action="store_true")
    parser.add_argument("--audit", type=Path)
    parser.add_argument("--require-rv32", action="store_true",
                        help="negative control: --absent must fail with this requirement")
    args = parser.parse_args()
    if args.selftest:
        selftest()
    else:
        if args.audit is None:
            parser.error("--audit is required for a measured run")
        run_gate(args.sdk_destination, args.audit, args.require_rv32)


if __name__ == "__main__":
    main()
