#!/usr/bin/env python3
"""Check product recipe facts and every integration boundary group."""

from __future__ import annotations

import ast
import re
import shlex
import shutil
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOC = Path("sw/litex/milan_soc.py")
DEPLOY = Path("sw/litex/deploy.sh")
DATAPATH = Path("hdl/milan/milan_datapath.sv")
LITEX_DOC = Path("docs/litex/LITEX_SOC.md")
SOLUTION_DOC = Path("docs/overview/FULL_FPGA_SOLUTION.md")
BUILD_DOC = Path("docs/integration/BUILDING.md")
INTEGRATOR_DOC = Path("docs/guides/SYSTEM_INTEGRATOR.md")
INTEGRATION_DOC = Path("docs/integration/INTEGRATION_GUIDE.md")
SIMULATION_DOC = Path("docs/testing/SIMULATION.md")
FPGA_DOC = Path("docs/fpga/FPGA_DESIGN.md")

CPU_START = "<!-- solution-cpu-contract:start -->"
CPU_END = "<!-- solution-cpu-contract:end -->"
MEMORY_START = "<!-- solution-memory-faces:start -->"
MEMORY_END = "<!-- solution-memory-faces:end -->"
INTERFACE_START = "<!-- solution-interface-groups:start -->"
INTERFACE_END = "<!-- solution-interface-groups:end -->"

PRODUCT_OPTIONS = (
    "--cpu",
    "--cpu-count",
    "--xlen",
    "--software-profile",
    "--l2-bytes",
    "--milan-clk-freq",
)
SYSTEM_CLOCK_OPTION = "--sys-clk-freq"
SYSTEM_CLOCK_CLI = "100000000"
SYSTEM_CLOCK_DEPLOY = "100000000"
PRODUCT_CLI = {
    "--cpu": "vexiiriscv",
    "--cpu-count": "1",
    "--xlen": "32",
    "--software-profile": "baremetal",
    "--l2-bytes": "unset",
    "--milan-clk-freq": "unset",
}
PRODUCT_DEPLOY = {
    **PRODUCT_CLI,
    "--l2-bytes": "0",
    "--milan-clk-freq": "50000000",
}

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
    "Record image memory": (
        "nvm_mem_*",
        (
            "o_nvm_mem_req_valid",
            "o_nvm_mem_wr_valid",
            "i_nvm_mem_wr_done",
        ),
    ),
}


@dataclass(frozen=True)
class PortGroup:
    label: str
    rtl_names: str
    duty: str
    safe_start: str
    patterns: tuple[str, ...]

    def matches(self, port: str) -> bool:
        """Whether this group claims one RTL boundary port by name."""
        return any(re.fullmatch(pattern, port) for pattern in self.patterns)

    def row(self) -> str:
        """The group as the one Markdown table row the docs must carry."""
        return (
            f"| {self.label} | {self.rtl_names} | {self.duty} | "
            f"{self.safe_start} |"
        )


PORT_GROUPS = (
    PortGroup(
        "Clocks and resets",
        "`axis_clk`, `axis_resetn`, `gtx_*`, `clk_audio_i`, `clk_tdm_i`",
        "Drive selected domains and reset sequencing",
        "Drive required clocks; assert resets",
        (
            r"axis_clk",
            r"axis_resetn",
            r"gtx_clk",
            r"gtx_resetn",
            r"clk_audio_i",
            r"clk_tdm_i",
        ),
    ),
    PortGroup(
        "AXI4-Lite CSR",
        "`s_axi_*`",
        "Map the complete 64 KiB window",
        "Connect fully; never tie handshakes",
        (r"s_axi_.*",),
    ),
    PortGroup(
        "MAC streams",
        "`m_axis_mac_tx_*`, `s_axis_mac_rx_*`",
        "Preserve final-boundary backpressure",
        "Set `s_axis_mac_rx_tvalid=0`; set `m_axis_mac_tx_tready=0`",
        (r"m_axis_mac_tx_.*", r"s_axis_mac_rx_.*"),
    ),
    PortGroup(
        "Descriptor memory",
        "`o_desc_mem_*`, `i_desc_mem_*`",
        "Serve the generated entity image",
        "Set `i_desc_mem_req_ready=0`; clear every response input",
        (r"[io]_desc_mem_.*",),
    ),
    PortGroup(
        "Response memory",
        "`o_resp_mem_*`, `i_resp_mem_*`",
        "Complete every accepted response operation",
        "Set `i_resp_mem_req_ready=0`, `i_resp_mem_wr_ready=0`; clear response and completion inputs",
        (r"[io]_resp_mem_.*",),
    ),
    PortGroup(
        "Record image memory",
        "`o_nvm_mem_*`, `i_nvm_mem_*`",
        "Complete every accepted saved-state record operation",
        "Set `i_nvm_mem_req_ready=0`, `i_nvm_mem_wr_ready=0`; clear response and completion inputs",
        (r"[io]_nvm_mem_.*",),
    ),
    PortGroup(
        "MAC control and status",
        "`o_mac_*`, `i_mac_*`, link, PHY, Ethernet guards",
        "Report honest capabilities and status",
        "Set `i_mac_speed=2'b10`, `i_link_up=1`, `i_full_duplex=1`; clear events, capabilities, toggles",
        (
            r"[io]_mac_.*",
            r"o_mc_hash",
            r"o_phy_reset_n",
            r"i_link_up",
            r"i_full_duplex",
            r"i_ethrx_tgl",
            r"i_ethtx_tgl",
            r"i_ethact_tgl",
            r"o_eth_rst",
            r"o_eth_guard",
        ),
    ),
    PortGroup(
        "Interrupt",
        "`o_irq_csr`",
        "Route the aggregate CSR interrupt",
        "Leave the output open during smoke tests",
        (r"o_irq_csr",),
    ),
    PortGroup(
        "Identify output",
        "`o_identify`",
        "Route the requested visual indication",
        "Leave the output open during smoke tests",
        (r"o_identify",),
    ),
    PortGroup(
        "MMCM controls",
        "`o_mmcm_*`, `i_mmcm_*`, `i_ps_clk`",
        "Bridge DRP and phase handshakes",
        "Set `i_ps_clk=axis_clk`, DRP inputs zero, `i_mmcm_locked=1`, `i_mmcm_ps_done=0`",
        (r"[io]_mmcm_.*", r"i_ps_clk"),
    ),
    PortGroup(
        "Audio pins",
        "`i2s_*`, `tdm_*`, `media_lrclk_o`",
        "Match the selected audio geometry",
        "Set `i2s_sdout_i=0`, every `tdm_*_i=0`; leave outputs open",
        (r"i2s_.*", r"tdm_.*", r"media_lrclk_o"),
    ),
)

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
SHIPPING_CONTEXT = re.compile(
    r"\b(?:ship|shipping|shipped|product|deploy(?:ment)?|mandatory|required|canonical)\b",
    re.IGNORECASE,
)
STALE_CACHE = re.compile(r"\b(?:32\s*kib|l2[- ]?32k|32768)\b", re.IGNORECASE)
STALE_CLOCK = re.compile(r"\b(?:100\s*mhz|100e6)\b", re.IGNORECASE)


def scalar(value: object) -> str:
    """One argparse or shell default as the docs spell it: an absent value is
    the word "unset", and a whole float is written without its ".0"."""
    if value is None:
        return "unset"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def argparse_defaults(
    path: Path,
    options: tuple[str, ...] = PRODUCT_OPTIONS,
) -> dict[str, str]:
    """Read required argparse defaults without importing the SoC."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: dict[str, list[str]] = {option: [] for option in options}
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
        selected = [flag for flag in flags if flag in options]
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


def deploy_override(path: Path, option: str) -> str | None:
    """Read one optional value from the fixed deployment recipe."""
    text = path.read_text(encoding="utf-8")
    matches = re.findall(r'^MILAN_OPTS="([^"\n]*)"$', text, re.MULTILINE)
    if len(matches) != 1:
        raise ValueError("expected one double-quoted MILAN_OPTS assignment")
    tokens = shlex.split(matches[0])
    values: list[str] = []
    index = 0
    while index < len(tokens):
        token, equals, embedded = tokens[index].partition("=")
        if token != option:
            index += 1
            continue
        if equals:
            values.append(embedded)
            index += 1
            continue
        if index + 1 >= len(tokens) or tokens[index + 1].startswith("--"):
            raise ValueError(f"{option}: deployment value is missing")
        values.append(tokens[index + 1])
        index += 2
    if len(values) > 1:
        raise ValueError(f"{option}: duplicate deployment values")
    if not values:
        return None
    value = values[0]
    return scalar(float(value)) if re.fullmatch(
        r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", value
    ) else value


def deploy_options(path: Path) -> dict[str, str]:
    """Read required values from the fixed deployment recipe."""
    text = path.read_text(encoding="utf-8")
    matches = re.findall(r'^MILAN_OPTS="([^"\n]*)"$', text, re.MULTILINE)
    if len(matches) != 1:
        raise ValueError("expected one double-quoted MILAN_OPTS assignment")
    tokens = shlex.split(matches[0])
    found: dict[str, list[str]] = {option: [] for option in PRODUCT_OPTIONS}
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
        value = entries[0]
        values[option] = scalar(float(value)) if re.fullmatch(
            r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", value
        ) else value
    return values


def clock_label(value: str) -> str:
    """A frequency in the docs' own units - MHz when it divides evenly, Hz
    otherwise - so the table and the recipe cannot disagree by notation."""
    if value == "unset":
        return value
    frequency = int(value)
    if frequency % 1_000_000 == 0:
        return f"{frequency // 1_000_000} MHz"
    return f"{frequency} Hz"


def product_table(cli: dict[str, str], deploy: dict[str, str]) -> str:
    """The CPU-contract block the docs must carry verbatim: CLI defaults and
    the deployment recipe side by side, generated from what the tree says."""

    def row(label: str, values: dict[str, str]) -> str:
        """One invocation as a table row."""
        return (
            f"| {label} | `{values['--cpu']}` | `{values['--cpu-count']}` | "
            f"`{values['--xlen']}` | `{values['--software-profile']}` | "
            f"`{values['--l2-bytes']}` | "
            f"`{clock_label(values['--milan-clk-freq'])}` |"
        )

    return "\n".join(
        (
            CPU_START,
            "| Invocation | CPU | Harts | XLEN | Firmware | L2 bytes | Datapath clock |",
            "|---|---|---:|---:|---|---:|---:|",
            row("CLI defaults", cli),
            row("`deploy.sh`", deploy),
            CPU_END,
        )
    )


def interface_table() -> str:
    """The interface-group block the docs must carry: one row per PORT_GROUPS
    entry, so a new boundary group reaches the document by regeneration."""
    return "\n".join(
        (
            INTERFACE_START,
            "| Group | RTL names | Integration duty | Safe inactive start |",
            "|---|---|---|---|",
            *(group.row() for group in PORT_GROUPS),
            INTERFACE_END,
        )
    )


def marked(text: str, start: str, end: str) -> str:
    """The generated block between its two markers, markers included.

    Ambiguity is refused rather than resolved: a marker appearing twice means
    the document has two blocks claiming to be the generated one.
    """
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError(f"markers must appear exactly once: {start}, {end}")
    _before, remainder = text.split(start, 1)
    body, _after = remainder.split(end, 1)
    return start + body + end


def without_marked(text: str, start: str, end: str) -> str:
    """The document with a generated block blanked to its own line count, so
    prose can be searched for a stale claim the block legitimately repeats."""
    try:
        section = marked(text, start, end)
    except ValueError:
        return text
    return text.replace(section, "\n" * section.count("\n"), 1)


def table_rows(text: str) -> list[list[str]]:
    """The Markdown table's data rows as stripped fields - header and the
    `---` separator dropped, backticks removed so a cell compares as text."""
    rows: list[list[str]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        fields = [field.strip().strip("`") for field in stripped.strip("|").split("|")]
        if not fields or fields[0] in ("Interface group", "Memory face", "Group"):
            continue
        if set(fields[0]) <= {"-", ":"}:
            continue
        rows.append(fields)
    return rows


def validate_memory_table(path: Path, text: str) -> list[str]:
    """Findings against the memory-face table: a face missing, a face claimed
    twice, or a face naming a signal prefix the RTL does not use."""
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


def datapath_ports(text: str) -> dict[str, str]:
    """{port: "input"|"output"} for the whole milan_datapath boundary.

    A declaration line the regex did not parse is an error rather than a port
    silently absent: the group check downstream is only exhaustive if this is.
    """
    start = text.find("\n)(\n")
    if start < 0:
        raise ValueError("cannot locate module port-list start")
    end = text.find("\n);", start)
    if end < 0:
        raise ValueError("cannot locate module port-list end")
    block = text[start + 4:end]
    declarations = re.findall(
        r"^\s*(input|output)\s+wire(?:\s+\[[^\]\n]+\])?\s+"
        r"([A-Za-z_][A-Za-z0-9_]*)\b",
        block,
        re.MULTILINE,
    )
    declaration_lines = re.findall(
        r"^\s*(?:input|output)\s+wire\b", block, re.MULTILINE
    )
    if len(declarations) != len(declaration_lines):
        raise ValueError("not every boundary declaration was parsed")
    counts = Counter(name for _direction, name in declarations)
    duplicates = sorted(name for name, count in counts.items() if count != 1)
    if duplicates:
        raise ValueError("duplicate boundary ports: " + ", ".join(duplicates))
    if not declarations:
        raise ValueError("no boundary ports found")
    return {name: direction for direction, name in declarations}


def validate_port_groups(ports: dict[str, str]) -> list[str]:
    """Findings against the group partition: every RTL port must land in
    exactly one documented group, and no group may be left with none."""
    errors: list[str] = []
    members: dict[str, list[str]] = {group.label: [] for group in PORT_GROUPS}
    for port in sorted(ports):
        matches = [group for group in PORT_GROUPS if group.matches(port)]
        if not matches:
            errors.append(f"{DATAPATH}: unclassified RTL port {port}")
            continue
        if len(matches) != 1:
            labels = ", ".join(group.label for group in matches)
            errors.append(f"{DATAPATH}: multiply classified RTL port {port}: {labels}")
            continue
        members[matches[0].label].append(port)
    for label, ports_in_group in members.items():
        if not ports_in_group:
            errors.append(f"{DATAPATH}: empty RTL port group {label}")
    return errors


def normalized(text: str) -> str:
    """Prose flattened for phrase matching: Markdown emphasis dropped and the
    case folded, so a stale claim cannot hide behind bold or a code span."""
    return re.sub(r"[*_`]", "", text).lower()


def _contract_errors(
    cli: dict[str, str],
    deploy: dict[str, str],
    system_cli: str,
    system_deploy: str,
) -> list[str]:
    """Where the source facts read out of the tree differ from the contract."""
    errors: list[str] = []
    if cli != PRODUCT_CLI:
        errors.append(f"{SOC}: CLI defaults differ from product contract: {cli}")
    if deploy != PRODUCT_DEPLOY:
        errors.append(
            f"{DEPLOY}: deployment values differ from product contract: {deploy}"
        )
    if system_cli != SYSTEM_CLOCK_CLI:
        errors.append(
            f"{SOC}: system clock default differs from product contract: "
            f"{system_cli}"
        )
    if system_deploy != SYSTEM_CLOCK_DEPLOY:
        errors.append(
            f"{DEPLOY}: deployment system clock differs from product contract: "
            f"{system_deploy}"
        )
    return errors


def _read_documents(root: Path) -> tuple[dict[Path, str], list[str]]:
    """The documents the contract is restated in, and the ones that would not read."""
    errors: list[str] = []
    document_paths = (
        LITEX_DOC,
        SOLUTION_DOC,
        BUILD_DOC,
        INTEGRATOR_DOC,
        INTEGRATION_DOC,
        SIMULATION_DOC,
        FPGA_DOC,
    )
    documents: dict[Path, str] = {}
    for path in document_paths:
        try:
            documents[path] = (root / path).read_text(encoding="utf-8")
        except OSError as error:
            errors.append(f"{path}: unreadable: {error}")
    return documents, errors


def _table_errors(
    documents: dict[Path, str], cli: dict[str, str], deploy: dict[str, str]
) -> list[str]:
    """Where a generated table or a source-derived sentence has drifted."""
    errors: list[str] = []
    expected_product = product_table(cli, deploy)
    for path in (LITEX_DOC, SOLUTION_DOC, BUILD_DOC):
        text = documents.get(path)
        if text is None:
            continue
        try:
            actual = marked(text, CPU_START, CPU_END)
        except ValueError as error:
            errors.append(f"{path}: {error}")
        else:
            if actual.strip() != expected_product:
                errors.append(f"{path}: product contract table differs from source")

    integration = documents.get(INTEGRATION_DOC)
    shipping_clock_sentence = (
        "Shipping deployment selects "
        f"{clock_label(deploy['--milan-clk-freq'])} for `axis_clk`."
    )
    if integration is not None and shipping_clock_sentence not in integration:
        errors.append(f"{INTEGRATION_DOC}: source-derived shipping clock is missing")

    fpga = documents.get(FPGA_DOC)
    fpga_clock_phrase = (
        "`axis_clk` (`cd_milan`: "
        f"{clock_label(deploy['--milan-clk-freq'])} deployed;"
    )
    if fpga is not None and fpga_clock_phrase not in fpga:
        errors.append(f"{FPGA_DOC}: source-derived deployed clock is missing")

    solution = documents.get(SOLUTION_DOC)
    if solution is not None:
        errors.extend(validate_memory_table(SOLUTION_DOC, solution))

    expected_interfaces = interface_table()
    for path in (INTEGRATOR_DOC, INTEGRATION_DOC):
        text = documents.get(path)
        if text is None:
            continue
        try:
            actual = marked(text, INTERFACE_START, INTERFACE_END)
        except ValueError as error:
            errors.append(f"{path}: {error}")
        else:
            if actual.strip() != expected_interfaces:
                errors.append(f"{path}: interface contract table differs from source map")
    return errors


def _boundary_errors(root: Path) -> list[str]:
    """Where the datapath's port boundary no longer answers the contract."""
    errors: list[str] = []
    try:
        rtl_text = (root / DATAPATH).read_text(encoding="utf-8")
        ports = datapath_ports(rtl_text)
    except (OSError, ValueError) as error:
        errors.append(f"{DATAPATH}: boundary unavailable: {error}")
    else:
        errors.extend(validate_port_groups(ports))
        for _name, (_prefix, required_ports) in MEMORY_FACES.items():
            for port in required_ports:
                if port not in ports:
                    errors.append(f"{DATAPATH}: missing RTL port {port}")
    return errors


def _stale_claim_errors(documents: dict[Path, str]) -> list[str]:
    """Superseded prose: a stale default, cache, clock, command or boundary."""
    errors: list[str] = []
    solution = documents.get(SOLUTION_DOC)
    for path in (
        LITEX_DOC,
        SOLUTION_DOC,
        BUILD_DOC,
        INTEGRATOR_DOC,
        INTEGRATION_DOC,
        SIMULATION_DOC,
        FPGA_DOC,
    ):
        text = documents.get(path)
        if text is None:
            continue
        plain = normalized(text)
        for phrase in STALE_DEFAULT_PHRASES:
            if phrase in plain:
                errors.append(f"{path}: stale CPU-default phrase: {phrase}")
        outside = without_marked(text, CPU_START, CPU_END)
        for line_number, line in enumerate(outside.splitlines(), start=1):
            if not SHIPPING_CONTEXT.search(line):
                continue
            if STALE_CACHE.search(line):
                errors.append(f"{path}:{line_number}: stale shipping cache claim")
            if STALE_CLOCK.search(line):
                errors.append(f"{path}:{line_number}: stale shipping clock claim")

    for path in (LITEX_DOC, BUILD_DOC):
        text = documents.get(path)
        if text is not None and "./deploy.sh build" not in text:
            errors.append(f"{path}: canonical deploy build command is missing")

    if solution is not None:
        plain = normalized(solution)
        for phrase in STALE_BOUNDARY_PHRASES:
            if phrase in plain:
                errors.append(f"{SOLUTION_DOC}: stale boundary phrase: {phrase}")
    return errors


def validate(root: Path) -> list[str]:
    """Every finding against one tree - source facts, generated blocks, the
    boundary contract and the stale claims. Empty means the docs agree."""
    try:
        cli = argparse_defaults(root / SOC)
        system_cli = argparse_defaults(
            root / SOC,
            (SYSTEM_CLOCK_OPTION,),
        )[SYSTEM_CLOCK_OPTION]
        deploy = deploy_options(root / DEPLOY)
        system_override = deploy_override(root / DEPLOY, SYSTEM_CLOCK_OPTION)
        system_deploy = system_override or system_cli
    except (OSError, SyntaxError, ValueError) as error:
        return [f"solution source facts unavailable: {error}"]

    errors = _contract_errors(cli, deploy, system_cli, system_deploy)
    documents, unreadable = _read_documents(root)
    errors.extend(unreadable)
    errors.extend(_table_errors(documents, cli, deploy))
    errors.extend(_boundary_errors(root))
    errors.extend(_stale_claim_errors(documents))
    return errors


def copy_fixture(destination: Path) -> None:
    """Copy the sources and documents this gate reads into a scratch tree, so
    the self-test mutates a copy and never the working tree."""
    for relative in (
        SOC,
        DEPLOY,
        DATAPATH,
        LITEX_DOC,
        SOLUTION_DOC,
        BUILD_DOC,
        INTEGRATOR_DOC,
        INTEGRATION_DOC,
        SIMULATION_DOC,
        FPGA_DOC,
    ):
        source = ROOT / relative
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def _source_fact_mutations() -> list[tuple[str, Path, str, str, str]]:
    """Mutations of the two source files the product contract is read from."""
    return [
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
        "deployment clock",
        DEPLOY,
        "--milan-clk-freq 50e6",
        "--milan-clk-freq 100e6",
        "deployment values differ",
    ),
    (
        "system clock default",
        SOC,
        'ap.add_argument("--sys-clk-freq", default=100e6, type=float)',
        'ap.add_argument("--sys-clk-freq", default=80e6, type=float)',
        "system clock default differs",
    ),
    (
        "deployment system clock override",
        DEPLOY,
        "--milan-clk-freq 50e6",
        "--sys-clk-freq 80e6 --milan-clk-freq 50e6",
        "deployment system clock differs",
    ),
    ]


def _document_claim_mutations() -> list[tuple[str, Path, str, str, str]]:
    """Mutations of the prose and tables the documents restate those facts in."""
    return [
    (
        "stale shipping cache prose",
        LITEX_DOC,
        CPU_END,
        CPU_END + "\n\nThe current ship uses 32 KiB.",
        "stale shipping cache claim",
    ),
    (
        "stale shipping clock prose",
        LITEX_DOC,
        CPU_END,
        CPU_END + "\n\nThe current ship uses 100 MHz.",
        "stale shipping clock claim",
    ),
    (
        "integration shipping clock",
        INTEGRATION_DOC,
        "Shipping deployment selects 50 MHz for `axis_clk`.",
        "Shipping deployment selects 25 MHz for `axis_clk`.",
        "source-derived shipping clock is missing",
    ),
    (
        "implementation-path deployed clock",
        FPGA_DOC,
        "`axis_clk` (`cd_milan`: 50 MHz deployed;",
        "`axis_clk` (`cd_milan`: 100 MHz deployed;",
        "source-derived deployed clock is missing",
    ),
    (
        "product clock table",
        SOLUTION_DOC,
        "| `deploy.sh` | `vexiiriscv` | `1` | `32` | `baremetal` | `0` | `50 MHz` |",
        "| `deploy.sh` | `vexiiriscv` | `1` | `32` | `baremetal` | `0` | `100 MHz` |",
        "product contract table differs",
    ),
    ]


def _boundary_contract_mutations() -> list[tuple[str, Path, str, str, str]]:
    """Mutations of the RTL boundary and of the contract rows describing it."""
    return [
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
        "unclassified future port",
        DATAPATH,
        "\n);",
        "\n  input wire future_unclassified_i\n);",
        "unclassified RTL port future_unclassified_i",
    ),
    (
        "boundary count claim",
        SOLUTION_DOC,
        MEMORY_END,
        MEMORY_END + "\n\nThe wrapper exposes exactly three interfaces.",
        "stale boundary phrase: exactly three",
    ),
    (
        "canonical build command",
        LITEX_DOC,
        "./deploy.sh build --dry-run\n"
        "./deploy.sh build",
        "./deploy.sh compile --dry-run\n"
        "./deploy.sh compile",
        "canonical deploy build command is missing",
    ),
    (
        "system guide response row",
        INTEGRATOR_DOC,
        next(group.row() for group in PORT_GROUPS if group.label == "Response memory") + "\n",
        "",
        "interface contract table differs",
    ),
    ]


def _port_group_mutations() -> list[tuple[str, Path, str, str, str]]:
    """One row-removal and one safe-start mutation for every port group."""
    mutations: list[tuple[str, Path, str, str, str]] = []
    for group in PORT_GROUPS:
        mutations.append(
            (
                f"integration group {group.label}",
                INTEGRATION_DOC,
                group.row() + "\n",
                "",
                "interface contract table differs",
            )
        )
        mutations.append(
            (
                f"integration safe start {group.label}",
                INTEGRATION_DOC,
                group.row(),
                group.row().replace(group.safe_start, "", 1),
                "interface contract table differs",
            )
        )
    return mutations


def _mutations() -> list[tuple[str, Path, str, str, str]]:
    """Every mutation control, in the order the self-test applies them."""
    return (_source_fact_mutations() + _document_claim_mutations()
            + _boundary_contract_mutations() + _port_group_mutations())


def selftest() -> int:
    """Grade the gate itself: the live tree must be clean, and every mutation
    control must be caught - an arm that escapes is a check that has stopped
    being able to say no."""
    baseline = validate(ROOT)
    if baseline:
        print("solution documentation selftest: baseline failed")
        for error in baseline:
            print(error)
        return 1

    mutations = _mutations()
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
    print(
        "solution documentation selftest: OK "
        f"({len(mutations)} mutation controls)"
    )
    return 0


def main() -> int:
    """The gate: 0 when the documents agree with the tree, 1 on findings,
    2 when the invocation was not one this script offers."""
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
    print(
        "solution documentation: OK "
        f"(product recipe, {len(MEMORY_FACES)} memory faces, "
        f"{len(PORT_GROUPS)} exhaustive port groups)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
