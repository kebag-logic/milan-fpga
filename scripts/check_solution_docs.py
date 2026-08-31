#!/usr/bin/env python3
"""Check product CPU defaults and integration-memory documentation."""

from __future__ import annotations

import ast
import re
import shlex
import shutil
import sys
import tempfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOC = Path("sw/litex/milan_soc.py")
DEPLOY = Path("sw/litex/deploy.sh")
DATAPATH = Path("hdl/milan/milan_datapath.sv")
LITEX_DOC = Path("docs/litex/LITEX_SOC.md")
SOLUTION_DOC = Path("docs/overview/FULL_FPGA_SOLUTION.md")
INTEGRATOR_DOC = Path("docs/guides/SYSTEM_INTEGRATOR.md")

CPU_START = "<!-- solution-cpu-contract:start -->"
CPU_END = "<!-- solution-cpu-contract:end -->"
MEMORY_START = "<!-- solution-memory-faces:start -->"
MEMORY_END = "<!-- solution-memory-faces:end -->"

CPU_OPTIONS = (
    "--cpu",
    "--cpu-count",
    "--xlen",
    "--software-profile",
    "--l2-bytes",
)
PRODUCT_CLI = {
    "--cpu": "vexiiriscv",
    "--cpu-count": "1",
    "--xlen": "32",
    "--software-profile": "baremetal",
    "--l2-bytes": "unset",
}
PRODUCT_DEPLOY = {**PRODUCT_CLI, "--l2-bytes": "0"}

MEMORY_FACES = {
    "Descriptor memory": (
        "desc_mem_*",
        ("o_desc_mem_req_valid", "i_desc_mem_rsp_err"),
    ),
    "Response memory": (
        "resp_mem_*",
        (
            "o_resp_mem_req_valid",
            "o_resp_mem_wr_valid",
            "i_resp_mem_wr_done",
        ),
    ),
    "Playback memory": (
        "pb_mem_*",
        ("pb_mem_addr_o", "pb_mem_rd_o", "pb_mem_data_i", "pb_mem_valid_i"),
    ),
}

STALE_DEFAULT_PHRASES = (
    "cli default is naxriscv",
    "naxriscv stays the cli default",
    "naxriscv remains the cli default",
    "naxriscv (default",
    "deploy.sh build gives you a naxriscv",
)
STALE_BOUNDARY_PHRASES = (
    "exactly three",
    "three clean boundaries",
    "the three datapath boundaries",
)


def scalar(value: object) -> str:
    if value is None:
        return "unset"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def argparse_defaults(path: Path) -> dict[str, str]:
    """Read required argparse defaults without importing the SoC."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: dict[str, list[str]] = {option: [] for option in CPU_OPTIONS}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        flags = [
            argument.value
            for argument in node.args
            if isinstance(argument, ast.Constant)
            and isinstance(argument.value, str)
            and argument.value.startswith("--")
        ]
        selected = [flag for flag in flags if flag in CPU_OPTIONS]
        if not selected:
            continue
        defaults = [item.value for item in node.keywords if item.arg == "default"]
        if len(selected) != 1 or len(defaults) != 1:
            raise ValueError(f"ambiguous argparse declaration: {selected}")
        found[selected[0]].append(scalar(ast.literal_eval(defaults[0])))
    missing = sorted(option for option, values in found.items() if not values)
    if missing:
        raise ValueError("missing argparse defaults: " + ", ".join(missing))
    duplicates = sorted(option for option, values in found.items() if len(values) != 1)
    if duplicates:
        raise ValueError("duplicate argparse defaults: " + ", ".join(duplicates))
    return {option: values[0] for option, values in found.items()}


def deploy_options(path: Path) -> dict[str, str]:
    """Read required values from the fixed deployment recipe."""
    text = path.read_text(encoding="utf-8")
    matches = re.findall(r'^MILAN_OPTS="([^"\n]*)"$', text, re.MULTILINE)
    if len(matches) != 1:
        raise ValueError("expected one double-quoted MILAN_OPTS assignment")
    tokens = shlex.split(matches[0])
    found: dict[str, list[str]] = {option: [] for option in CPU_OPTIONS}
    index = 0
    while index < len(tokens):
        token = tokens[index]
        option, equals, embedded = token.partition("=")
        if option not in found:
            index += 1
            continue
        if equals:
            found[option].append(embedded)
            index += 1
            continue
        if index + 1 >= len(tokens) or tokens[index + 1].startswith("--"):
            raise ValueError(f"{option}: deployment value is missing")
        found[option].append(tokens[index + 1])
        index += 2
    values: dict[str, str] = {}
    for option, entries in found.items():
        if len(entries) != 1:
            raise ValueError(
                f"{option}: expected one deployment value, found {len(entries)}"
            )
        values[option] = scalar(float(entries[0])) if re.fullmatch(
            r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)", entries[0]
        ) else entries[0]
    return values


def cpu_table(cli: dict[str, str], deploy: dict[str, str]) -> str:
    def row(label: str, values: dict[str, str]) -> str:
        return (
            f"| {label} | `{values['--cpu']}` | `{values['--cpu-count']}` | "
            f"`{values['--xlen']}` | `{values['--software-profile']}` | "
            f"`{values['--l2-bytes']}` |"
        )

    return "\n".join(
        (
            CPU_START,
            "| Invocation | CPU | Harts | XLEN | Firmware | L2 bytes |",
            "|---|---|---:|---:|---|---:|",
            row("CLI defaults", cli),
            row("`deploy.sh`", deploy),
            CPU_END,
        )
    )


def marked(text: str, start: str, end: str) -> str:
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError(f"markers must appear exactly once: {start}, {end}")
    before, remainder = text.split(start, 1)
    body, after = remainder.split(end, 1)
    del before, after
    return start + body + end


def table_rows(text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        fields = [field.strip().strip("`") for field in stripped.strip("|").split("|")]
        if not fields or fields[0] in ("Interface group", "Memory face"):
            continue
        if set(fields[0]) <= {"-", ":"}:
            continue
        rows.append(fields)
    return rows


def validate_memory_table(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    try:
        section = marked(text, MEMORY_START, MEMORY_END)
    except ValueError as error:
        return [f"{path}: {error}"]
    rows = table_rows(section)
    counts = Counter(row[0] for row in rows if row)
    missing = sorted(set(MEMORY_FACES) - set(counts))
    if missing:
        errors.append(f"{path}: missing memory faces: {', '.join(missing)}")
    duplicates = sorted(
        name for name in MEMORY_FACES if counts[name] != 1 and name in counts
    )
    if duplicates:
        errors.append(f"{path}: duplicate memory faces: {', '.join(duplicates)}")
    by_name = {row[0]: row for row in rows if row and counts[row[0]] == 1}
    for name, (prefix, _ports) in MEMORY_FACES.items():
        row = by_name.get(name)
        if row is None:
            continue
        if len(row) < 2 or row[1] != prefix:
            errors.append(f"{path}: {name} must name `{prefix}`")
    return errors


def normalized(text: str) -> str:
    return re.sub(r"[*_`]", "", text).lower()


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    try:
        cli = argparse_defaults(root / SOC)
        deploy = deploy_options(root / DEPLOY)
    except (OSError, SyntaxError, ValueError) as error:
        return [f"solution source facts unavailable: {error}"]

    if cli != PRODUCT_CLI:
        errors.append(f"{SOC}: CLI defaults differ from product contract: {cli}")
    if deploy != PRODUCT_DEPLOY:
        errors.append(
            f"{DEPLOY}: deployment values differ from product contract: {deploy}"
        )

    expected_cpu = cpu_table(cli, deploy)
    documents: dict[Path, str] = {}
    for path in (LITEX_DOC, SOLUTION_DOC, INTEGRATOR_DOC):
        try:
            documents[path] = (root / path).read_text(encoding="utf-8")
        except OSError as error:
            errors.append(f"{path}: unreadable: {error}")
    for path in (LITEX_DOC, SOLUTION_DOC):
        if path not in documents:
            continue
        try:
            actual = marked(documents[path], CPU_START, CPU_END)
        except ValueError as error:
            errors.append(f"{path}: {error}")
        else:
            if actual.strip() != expected_cpu:
                errors.append(f"{path}: CPU contract table differs from source")

    for path in (SOLUTION_DOC, INTEGRATOR_DOC):
        if path in documents:
            errors.extend(validate_memory_table(path, documents[path]))

    try:
        rtl = (root / DATAPATH).read_text(encoding="utf-8")
    except OSError as error:
        errors.append(f"{DATAPATH}: unreadable: {error}")
    else:
        for _name, (_prefix, ports) in MEMORY_FACES.items():
            for port in ports:
                declaration = (
                    rf"^\s*(?:input|output)\s+wire"
                    rf"(?:\s+\[[^\]]+\])?\s+{re.escape(port)}\b"
                )
                if not re.search(declaration, rtl, re.MULTILINE):
                    errors.append(f"{DATAPATH}: missing RTL port {port}")

    for path in (LITEX_DOC, SOLUTION_DOC):
        text = documents.get(path)
        if text is None:
            continue
        plain = normalized(text)
        for phrase in STALE_DEFAULT_PHRASES:
            if phrase in plain:
                errors.append(f"{path}: stale CPU-default phrase: {phrase}")
    solution = documents.get(SOLUTION_DOC)
    if solution is not None:
        plain = normalized(solution)
        for phrase in STALE_BOUNDARY_PHRASES:
            if phrase in plain:
                errors.append(f"{SOLUTION_DOC}: stale boundary phrase: {phrase}")
    return errors


def copy_fixture(destination: Path) -> None:
    for relative in (SOC, DEPLOY, DATAPATH, LITEX_DOC, SOLUTION_DOC, INTEGRATOR_DOC):
        source = ROOT / relative
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def selftest() -> int:
    baseline = validate(ROOT)
    if baseline:
        print("solution documentation selftest: baseline failed")
        for error in baseline:
            print(error)
        return 1
    mutations = (
        (
            "CLI CPU default",
            SOC,
            'default="vexiiriscv"',
            'default="naxriscv"',
            "CLI defaults differ",
        ),
        (
            "deployment CPU",
            DEPLOY,
            "--cpu vexiiriscv",
            "--cpu naxriscv",
            "deployment values differ",
        ),
        (
            "integrator response row",
            INTEGRATOR_DOC,
            "| Response memory | `resp_mem_*` | Datapath read-write master | Complete every accepted operation |\n",
            "",
            "missing memory faces: Response memory",
        ),
        (
            "solution response row",
            SOLUTION_DOC,
            "| Response memory | `resp_mem_*` | Read-write | Build AECP responses |\n",
            "",
            "missing memory faces: Response memory",
        ),
        (
            "response write port",
            DATAPATH,
            "output wire        o_resp_mem_wr_valid,",
            "output wire        o_resp_mem_wr_removed,",
            "missing RTL port o_resp_mem_wr_valid",
        ),
        (
            "boundary count claim",
            SOLUTION_DOC,
            MEMORY_END,
            MEMORY_END + "\n\nThe wrapper exposes exactly three interfaces.",
            "stale boundary phrase: exactly three",
        ),
    )
    with tempfile.TemporaryDirectory(prefix="solution-doc-selftest-") as directory:
        fixture = Path(directory)
        copy_fixture(fixture)
        if validate(fixture):
            print("solution documentation selftest: copied baseline failed")
            return 1
        for label, relative, old, new, expected in mutations:
            path = fixture / relative
            original = path.read_text(encoding="utf-8")
            if old not in original:
                print(f"solution documentation selftest: missing fixture for {label}")
                return 1
            path.write_text(original.replace(old, new, 1), encoding="utf-8")
            findings = validate(fixture)
            if not any(expected in finding for finding in findings):
                print(f"solution documentation selftest: {label} escaped: {findings}")
                return 1
            path.write_text(original, encoding="utf-8")
    print("solution documentation selftest: OK (6 mutation controls)")
    return 0


def main() -> int:
    if sys.argv[1:] == ["--selftest"]:
        return selftest()
    if sys.argv[1:]:
        print(__doc__)
        return 2
    errors = validate(ROOT)
    if errors:
        for error in errors:
            print(error)
        print(f"solution documentation: FAIL ({len(errors)} findings)")
        return 1
    print("solution documentation: OK (CPU contract and three memory faces)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
