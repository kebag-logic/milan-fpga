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
PERFORMANCE_DOC = Path("docs/findings/PERFORMANCE_GOAL.md")
FPGA_DOC = Path("docs/fpga/FPGA_DESIGN.md")
PIPELINE_DOC = Path("docs/fpga/PIPELINE_STAGES.md")

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
RSC_TOUT_RESET_CYCLES = 5000
RSC_AGEMAX_RESET_CYCLES = 200000
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
    "Playback memory": (
        "pb_mem_*",
        ("pb_mem_addr_o", "pb_mem_rd_o", "pb_mem_data_i", "pb_mem_valid_i"),
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
        return any(re.fullmatch(pattern, port) for pattern in self.patterns)

    def row(self) -> str:
        return (
            f"| {self.label} | {self.rtl_names} | {self.duty} | "
            f"{self.safe_start} |"
        )


@dataclass(frozen=True)
class RscTimerFacts:
    reset_cycles: int
    description: str
    age_reset_cycles: int
    age_description: str
    uses_default_sync: bool
    writer_is_unrenamed: bool
    crosses_to_datapath: bool


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
        "TX DMA stream",
        "`s_axis_tx_*`",
        "Supply complete transmit frames",
        "Set `s_axis_tx_tvalid=0`",
        (r"s_axis_tx_.*",),
    ),
    PortGroup(
        "RX DMA stream",
        "`m_axis_rx_*`",
        "Accept complete receive frames",
        "Set `m_axis_rx_tready=0`",
        (r"m_axis_rx_.*",),
    ),
    PortGroup(
        "Timestamp stream",
        "`m_axis_ts_*`",
        "Drain timestamp records",
        "Set `m_axis_ts_tready=0`",
        (r"m_axis_ts_.*",),
    ),
    PortGroup(
        "PCM DMA stream",
        "`m_axis_pcm_*`",
        "Drain framed PCM records",
        "Set `m_axis_pcm_tready=0`",
        (r"m_axis_pcm_.*",),
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
        "Playback memory",
        "`pb_*`",
        "Serve configured PCM rings",
        "Set every `pb_*_i=0`",
        (r"pb_.*",),
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
STALE_PIPELINE_CLOCK = re.compile(
    r"\b(?:datapath|mac\))\s+runs\s+at\s+(?:100\s*mhz|100e6)\b",
    re.IGNORECASE,
)
STALE_PIPELINE_OPTION = re.compile(
    r"--milan-clk-freq(?:=|\s+)100e6\b",
    re.IGNORECASE,
)
STALE_RSC_TIMER_DOMAIN = re.compile(
    r"`rsc_tout`[^\n]{0,120}\bdatapath-clock\s+ticks\b",
    re.IGNORECASE,
)


def scalar(value: object) -> str:
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


def rsc_timer_facts(text: str) -> RscTimerFacts:
    """Trace the RSC timer through its default domain and RX CDC."""
    tree = ast.parse(text, filename=str(SOC))
    writers = [
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == "RingDMAWriter"
    ]
    if len(writers) != 1:
        raise ValueError("expected one RingDMAWriter class")
    writer = writers[0]

    def self_attr(node: ast.AST, name: str) -> bool:
        return (
            isinstance(node, ast.Attribute)
            and node.attr == name
            and isinstance(node.value, ast.Name)
            and node.value.id == "self"
        )

    def csr_facts(name: str) -> tuple[int, str]:
        assignments = [
            node
            for node in ast.walk(writer)
            if isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and self_attr(node.targets[0], name)
            and isinstance(node.value, ast.Call)
        ]
        if len(assignments) != 1:
            raise ValueError(f"expected one {name} CSR declaration")
        call = assignments[0].value
        keywords = {item.arg: item.value for item in call.keywords if item.arg}
        if "reset" not in keywords or "description" not in keywords:
            raise ValueError(f"{name} must declare reset and description")
        reset = ast.literal_eval(keywords["reset"])
        description = ast.literal_eval(keywords["description"])
        if not isinstance(reset, int) or not isinstance(description, str):
            raise ValueError(f"{name} reset or description has the wrong type")
        return reset, description

    reset_cycles, description = csr_facts("rsc_tout")
    age_reset_cycles, age_description = csr_facts("rsc_agemax")

    slot_timers_use_default_sync = False
    ack_timer_uses_default_sync = False
    for node in ast.walk(writer):
        if not isinstance(node, ast.AugAssign) or not self_attr(node.target, "sync"):
            continue
        names = {item.id for item in ast.walk(node) if isinstance(item, ast.Name)}
        attrs = {
            item.attr for item in ast.walk(node) if isinstance(item, ast.Attribute)
        }
        if {"s_idle", "s_age", "agemax_v"} <= names and "rsc_tout" in attrs:
            slot_timers_use_default_sync = True
        if "ack_timer" in names:
            ack_timer_uses_default_sync = True
    ack_timer_uses_timeout = any(
        isinstance(node, ast.Compare)
        and "ack_timer" in {
            item.id for item in ast.walk(node) if isinstance(item, ast.Name)
        }
        and "rsc_tout" in {
            item.attr for item in ast.walk(node) if isinstance(item, ast.Attribute)
        }
        for node in ast.walk(writer)
    )
    uses_default_sync = (
        slot_timers_use_default_sync
        and ack_timer_uses_default_sync
        and ack_timer_uses_timeout
    )

    unrenamed_writers = {
        node.targets[0].attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Attribute)
        and isinstance(node.targets[0].value, ast.Name)
        and node.targets[0].value.id == "self"
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name)
        and node.value.func.id == "RingDMAWriter"
    }
    writer_is_unrenamed = {"rx", "rx1"} <= unrenamed_writers
    crosses_to_datapath = any(
        isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Name)
        and node.targets[0].id == "rx_dp"
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name)
        and node.value.func.id == "_axis_dp_cdc"
        and any(
            isinstance(argument, ast.Constant)
            and argument.value == "dma_rx_cdc"
            for argument in node.value.args
        )
        and any(
            isinstance(argument, ast.Name) and argument.id == "milan_cd"
            for argument in node.value.args
        )
        and any(
            keyword.arg == "to_datapath"
            and isinstance(keyword.value, ast.Constant)
            and keyword.value.value is False
            for keyword in node.value.keywords
        )
        for node in ast.walk(tree)
    )
    return RscTimerFacts(
        reset_cycles=reset_cycles,
        description=description,
        age_reset_cycles=age_reset_cycles,
        age_description=age_description,
        uses_default_sync=uses_default_sync,
        writer_is_unrenamed=writer_is_unrenamed,
        crosses_to_datapath=crosses_to_datapath,
    )


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
    if value == "unset":
        return value
    frequency = int(value)
    if frequency % 1_000_000 == 0:
        return f"{frequency // 1_000_000} MHz"
    return f"{frequency} Hz"


def clock_option(value: str) -> str:
    if value == "unset":
        return value
    frequency = int(value)
    if frequency % 1_000_000 == 0:
        return f"{frequency // 1_000_000}e6"
    return value


def product_table(cli: dict[str, str], deploy: dict[str, str]) -> str:
    def row(label: str, values: dict[str, str]) -> str:
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
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError(f"markers must appear exactly once: {start}, {end}")
    _before, remainder = text.split(start, 1)
    body, _after = remainder.split(end, 1)
    return start + body + end


def without_marked(text: str, start: str, end: str) -> str:
    try:
        section = marked(text, start, end)
    except ValueError:
        return text
    return text.replace(section, "\n" * section.count("\n"), 1)


def table_rows(text: str) -> list[list[str]]:
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
    return re.sub(r"[*_`]", "", text).lower()


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    try:
        cli = argparse_defaults(root / SOC)
        system_cli = argparse_defaults(
            root / SOC,
            (SYSTEM_CLOCK_OPTION,),
        )[SYSTEM_CLOCK_OPTION]
        deploy = deploy_options(root / DEPLOY)
        system_override = deploy_override(root / DEPLOY, SYSTEM_CLOCK_OPTION)
        system_deploy = system_override or system_cli
        soc_text = (root / SOC).read_text(encoding="utf-8")
        rsc_timer = rsc_timer_facts(soc_text)
        system_frequency = int(system_deploy)
    except (OSError, SyntaxError, ValueError) as error:
        return [f"solution source facts unavailable: {error}"]

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
    if not rsc_timer.uses_default_sync:
        errors.append(f"{SOC}: RSC timers must use the default system domain")
    if not rsc_timer.writer_is_unrenamed:
        errors.append(f"{SOC}: RX RingDMAWriter must remain unrenamed")
    if not rsc_timer.crosses_to_datapath:
        errors.append(f"{SOC}: RX DMA/datapath CDC is missing")
    if rsc_timer.reset_cycles != RSC_TOUT_RESET_CYCLES:
        errors.append(
            f"{SOC}: rsc_tout reset differs from product contract: "
            f"{rsc_timer.reset_cycles}"
        )
    if rsc_timer.age_reset_cycles != RSC_AGEMAX_RESET_CYCLES:
        errors.append(
            f"{SOC}: rsc_agemax reset differs from product contract: "
            f"{rsc_timer.age_reset_cycles}"
        )
    rsc_timeout_us = RSC_TOUT_RESET_CYCLES * 1_000_000 / system_frequency
    rsc_timeout_label = f"{rsc_timeout_us:g}"
    rsc_age_ms = RSC_AGEMAX_RESET_CYCLES * 1_000 / system_frequency
    rsc_age_label = f"{rsc_age_ms:g}"
    expected_rsc_description = (
        "RSC aggregate idle-close timeout "
        f"(sys_clk cycles; {RSC_TOUT_RESET_CYCLES} = "
        f"{rsc_timeout_label} us @ {clock_label(system_deploy)})."
    )
    if rsc_timer.description != expected_rsc_description:
        errors.append(f"{SOC}: source-derived RSC timeout description differs")
    expected_age_description = (
        "RSC aggregate lifetime cap in sys_clk cycles "
        f"({RSC_AGEMAX_RESET_CYCLES} = {rsc_age_label} ms @ "
        f"{clock_label(system_deploy)}); bounds CQ head-of-line hold."
    )
    if rsc_timer.age_description != expected_age_description:
        errors.append(f"{SOC}: source-derived RSC lifetime description differs")

    document_paths = (
        LITEX_DOC,
        SOLUTION_DOC,
        BUILD_DOC,
        INTEGRATOR_DOC,
        INTEGRATION_DOC,
        SIMULATION_DOC,
        PERFORMANCE_DOC,
        FPGA_DOC,
        PIPELINE_DOC,
    )
    documents: dict[Path, str] = {}
    for path in document_paths:
        try:
            documents[path] = (root / path).read_text(encoding="utf-8")
        except OSError as error:
            errors.append(f"{path}: unreadable: {error}")

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

    pipeline = documents.get(PIPELINE_DOC)
    pipeline_product_sentence = (
        f"The product uses `{deploy['--cpu-count']}` hart and "
        f"`{deploy['--l2-bytes']}` L2 bytes."
    )
    pipeline_clock_sentences = (
        "The deployed datapath runs at "
        f"{clock_label(deploy['--milan-clk-freq'])}.",
        f"- Recipe: `--milan-clk-freq "
        f"{clock_option(deploy['--milan-clk-freq'])}`.",
        "- T3 uses the deployed "
        f"{clock_label(deploy['--milan-clk-freq'])} datapath.",
    )
    pipeline_rsc_sentences = (
        "- `rsc_tout` at +0x48 uses system-clock ticks.",
        f"- System clock: {clock_label(system_deploy)}.",
        f"- Default: {RSC_TOUT_RESET_CYCLES:,} cycles, "
        f"or {rsc_timeout_label} us.",
        "- `rsc_agemax` uses identical system-clock ticks.",
        f"- Lifetime default: {RSC_AGEMAX_RESET_CYCLES:,} cycles, "
        f"or {rsc_age_label} ms.",
    )
    if pipeline is not None:
        if pipeline_product_sentence not in pipeline:
            errors.append(f"{PIPELINE_DOC}: source-derived product shape is missing")
        for sentence in pipeline_clock_sentences:
            if sentence not in pipeline:
                errors.append(
                    f"{PIPELINE_DOC}: source-derived datapath clock is missing: "
                    f"{sentence}"
                )
        for sentence in pipeline_rsc_sentences:
            if sentence not in pipeline:
                errors.append(
                    f"{PIPELINE_DOC}: source-derived RSC timeout is missing: "
                    f"{sentence}"
                )
        if STALE_PIPELINE_CLOCK.search(pipeline):
            errors.append(f"{PIPELINE_DOC}: stale deployed datapath clock claim")
        if STALE_PIPELINE_OPTION.search(pipeline):
            errors.append(f"{PIPELINE_DOC}: stale deployed datapath clock option")
        if STALE_RSC_TIMER_DOMAIN.search(pipeline):
            errors.append(f"{PIPELINE_DOC}: stale RSC datapath-clock claim")

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

    for path in (
        LITEX_DOC,
        SOLUTION_DOC,
        BUILD_DOC,
        INTEGRATOR_DOC,
        INTEGRATION_DOC,
        SIMULATION_DOC,
        PERFORMANCE_DOC,
        FPGA_DOC,
        PIPELINE_DOC,
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


def copy_fixture(destination: Path) -> None:
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
        PERFORMANCE_DOC,
        FPGA_DOC,
        PIPELINE_DOC,
    ):
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

    mutations = [
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
        (
            "RSC source description",
            SOC,
            "RSC aggregate idle-close timeout (sys_clk cycles; "
            "5000 = 50 us @ 100 MHz).",
            "RSC aggregate idle-close timeout (milan_clk cycles; "
            "5000 = 100 us @ 50 MHz).",
            "source-derived RSC timeout description differs",
        ),
        (
            "RSC reset cycles",
            SOC,
            "self.rsc_tout  = CSRStorage(24, reset=5000, description=",
            "self.rsc_tout  = CSRStorage(24, reset=6000, description=",
            "rsc_tout reset differs",
        ),
        (
            "RSC lifetime source description",
            SOC,
            "RSC aggregate lifetime cap in sys_clk cycles "
            "(200000 = 2 ms @ 100 MHz);",
            "RSC aggregate lifetime cap in milan_clk cycles "
            "(200000 = 4 ms @ 50 MHz);",
            "source-derived RSC lifetime description differs",
        ),
        (
            "RSC lifetime reset cycles",
            SOC,
            "self.rsc_agemax = CSRStorage(24, reset=200000, description=",
            "self.rsc_agemax = CSRStorage(24, reset=250000, description=",
            "rsc_agemax reset differs",
        ),
        (
            "RSC timer default domain",
            SOC,
            "            for i in range(NS):\n"
            "                self.sync += [",
            "            for i in range(NS):\n"
            "                self.sync.milan += [",
            "RSC timers must use the default system domain",
        ),
        (
            "RSC ACK timer default domain",
            SOC,
            "        if rsc_capable:                 # folded: "
            "ack_timer/rsc_dbg undriven (0)\n"
            "            self.sync += [",
            "        if rsc_capable:                 # folded: "
            "ack_timer/rsc_dbg undriven (0)\n"
            "            self.sync.milan += [",
            "RSC timers must use the default system domain",
        ),
        (
            "RSC writer domain rename",
            SOC,
            "self.rx = RingDMAWriter(",
            "self.rx_writer = RingDMAWriter(",
            "RX RingDMAWriter must remain unrenamed",
        ),
        (
            "RX DMA datapath CDC",
            SOC,
            'rx_dp = _axis_dp_cdc(self, "dma_rx_cdc"',
            'rx_dp = _axis_dp_direct(self, "dma_rx_cdc"',
            "RX DMA/datapath CDC is missing",
        ),
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
            "implementation-path product shape",
            PIPELINE_DOC,
            "The product uses `1` hart and `0` L2 bytes.",
            "The product uses `1` hart and `32768` L2 bytes.",
            "source-derived product shape is missing",
        ),
        (
            "pipeline receive clock",
            PIPELINE_DOC,
            "The deployed datapath runs at 50 MHz.",
            "The deployed datapath runs at 25 MHz.",
            "source-derived datapath clock is missing",
        ),
        (
            "pipeline transmit clock",
            PIPELINE_DOC,
            "- T3 uses the deployed 50 MHz datapath.",
            "- T3 uses the deployed 100 MHz datapath.",
            "source-derived datapath clock is missing",
        ),
        (
            "contradictory pipeline clock",
            PIPELINE_DOC,
            "The deployed datapath runs at 50 MHz.",
            "The deployed datapath runs at 50 MHz.\n\n"
            "The datapath runs at 100 MHz.",
            "stale deployed datapath clock claim",
        ),
        (
            "contradictory pipeline clock option",
            PIPELINE_DOC,
            "- Recipe: `--milan-clk-freq 50e6`.",
            "- Recipe: `--milan-clk-freq 50e6`.\n\n"
            "- Old recipe: `--milan-clk-freq 100e6`.",
            "stale deployed datapath clock option",
        ),
        (
            "pipeline RSC timer domain",
            PIPELINE_DOC,
            "- `rsc_tout` at +0x48 uses system-clock ticks.",
            "- `rsc_tout` at +0x48 uses datapath-clock ticks.",
            "source-derived RSC timeout is missing",
        ),
        (
            "pipeline RSC timeout conversion",
            PIPELINE_DOC,
            "- Default: 5,000 cycles, or 50 us.",
            "- Default: 5,000 cycles, or 100 us.",
            "source-derived RSC timeout is missing",
        ),
        (
            "pipeline RSC system clock",
            PIPELINE_DOC,
            "- System clock: 100 MHz.",
            "- System clock: 50 MHz.",
            "source-derived RSC timeout is missing",
        ),
        (
            "pipeline RSC lifetime conversion",
            PIPELINE_DOC,
            "- Lifetime default: 200,000 cycles, or 2 ms.",
            "- Lifetime default: 200,000 cycles, or 4 ms.",
            "source-derived RSC timeout is missing",
        ),
        (
            "contradictory RSC timer domain",
            PIPELINE_DOC,
            "- `rsc_tout` at +0x48 uses system-clock ticks.",
            "- `rsc_tout` at +0x48 uses system-clock ticks.\n"
            "- `rsc_tout` also uses datapath-clock ticks.",
            "stale RSC datapath-clock claim",
        ),
        (
            "product clock table",
            SOLUTION_DOC,
            "| `deploy.sh` | `vexiiriscv` | `1` | `32` | `baremetal` | `0` | `50 MHz` |",
            "| `deploy.sh` | `vexiiriscv` | `1` | `32` | `baremetal` | `0` | `100 MHz` |",
            "product contract table differs",
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
            "./deploy.sh build --dry-run    # inspect the exact product recipe\n"
            "./deploy.sh build              # build the product bitstream",
            "./deploy.sh compile --dry-run  # inspect the exact product recipe\n"
            "./deploy.sh compile            # build the product bitstream",
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
