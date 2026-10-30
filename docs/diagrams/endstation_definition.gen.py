#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate the source-derived blocks of the end-station definition guide.

docs/guides/DEFINING_THE_END_STATION.md carries no hand-copied value (#797).
Every number, artifact name and descriptor count on it sits between a pair of
markers this script owns, and each comes from running the builder:

- `flow`: the data flow from the YAML to the entity on the wire. Each artifact
  is one the builder really writes, and each consumer is checked to name the
  file it reads;
- `aem-tree`: the 1x1 descriptor tree, drawn from the builder's own overlay
  and checked against its descriptor counts;
- `resources`: the estimate for every tracked shape and three widened probes;
- `example-*`: the worked example, run through the builder's command line;
- `moves`: what a shape change and a channel change move;
- `sim-legs`: which simulation suites include each tracked shape.

Probe configurations live in a temporary directory, never in the tree.

Usage:
    python3 docs/diagrams/endstation_definition.gen.py             # rewrite the blocks
    python3 docs/diagrams/endstation_definition.gen.py --check     # fail on a stale block
    python3 docs/diagrams/endstation_definition.gen.py --selftest  # prove each check bites
"""

from __future__ import annotations

import argparse
import contextlib
import copy
import difflib
import json
import os
import re
import subprocess
import sys
import tempfile
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "docs" / "guides" / "DEFINING_THE_END_STATION.md"
BUILDER = "sw/builder/endstation_builder.py"
BASE = "configs/endstation_ax7101_1x1_tdm8.yaml"
sys.path.insert(0, str(ROOT / "sw" / "builder"))
import endstation_builder as eb  # noqa: E402

#: (artifact, consumer, the text the consumer must contain to read it). A
#: label whose consumer no longer names its file is refused, so the diagram
#: cannot outlive the code it shows.
CONSUMERS = (
    ("soc_params.json", "sw/litex/build.sh", "soc_params.json"),
    ("platform_shape.json", "sw/litex/milan_soc.py", "platform_shape.json"),
    ("gptp_ucode.hex", "sw/litex/milan_soc.py", "gptp_ucode.hex"),
    ("aem_overlay.json", "sw/litex/milan_soc.py", "aem_overlay.json"),
    ("lwsrp_table.json", "sw/litex/milan_soc.py", "lwsrp_table.json"),
    ("adp_shape_defaults.svh", "hdl/common/csr/milan_csr.sv", "adp_shape_defaults.svh"),
    ("adp_shape_defaults.svh", "hdl/milan/milan_datapath.sv", "adp_shape_defaults.svh"),
    ("lwsrp_csr_defaults.svh", "hdl/common/csr/milan_csr.sv", "lwsrp_csr_defaults.svh"),
    ("sweep_opts_ax7101.sh", "sw/litex/sweep.sh", "sweep_opts_"),
)
#: Downstream steps the flow names, each checked the same way.
STEPS = (
    ("aem_desc.bin", "sw/litex/milan_soc.py", "aem_desc.bin"),
    ("flashboot_layout.json", "sw/litex/milan_soc.py", "flashboot_layout.json"),
    ("flash-pair", "sw/litex/deploy.sh", "flash-pair"),
    ("check_entity_shape.py --built-config", "sw/litex/build.sh", "check_entity_shape.py"),
    ("MILAN_AEM_FLASH_OFFSET", "sw/firmware/milan_baremetal/milan_baremetal.c", "MILAN_AEM_FLASH_OFFSET"),
    ("READ_DESCRIPTOR", "protocol-processor/hdl/top/protocol_processor_top.sv", "READ_DESCRIPTOR"),
)
#: Widths the resource table widens the shipping shape to.
WIDENED = (2, 4, 8)
#: The channel count of the worked example's change that fits.
NARROW = 4


class GenerationError(Exception):
    """The page cannot be generated truthfully; nothing is written."""


def marker(name: str) -> tuple[str, str]:
    """The start and end markers of one generated block."""
    return (f"<!-- generated:{name}:start (docs/diagrams/endstation_definition.gen.py; do not edit) -->",
            f"<!-- generated:{name}:end -->")


def base_doc() -> dict:
    """The shipping 1x1 configuration, parsed."""
    return yaml.safe_load((ROOT / BASE).read_text(encoding="utf-8"))


def widened(n: int) -> dict:
    """The shipping shape with n eight-channel streams each way."""
    doc = base_doc()
    doc["streams"]["listeners"] = [
        {"name": f"Stream In {k}", "channels": 8, "map_mode": "dynamic"} for k in range(n)]
    doc["streams"]["talkers"] = [
        {"name": f"Stream Out {k}", "channels": 8, "map_mode": "dynamic"} for k in range(n)]
    return doc


def narrowed(channels: int) -> dict:
    """The shipping shape with every stream at `channels` channels."""
    doc = base_doc()
    for stream in doc["streams"]["listeners"] + doc["streams"]["talkers"]:
        stream["channels"] = channels
    return doc


@contextlib.contextmanager
def probe_dir() -> Iterator[Path]:
    """A temporary directory outside the tree for probe configs and outputs."""
    with tempfile.TemporaryDirectory(prefix="endstation-definition-") as tmp:
        yield Path(tmp)


def write_probe(tmp: Path, stem: str, doc: dict) -> Path:
    """One probe config under `tmp`. A probe that would take ownership of a
    tracked header is refused rather than written."""
    if (doc.get("srp") or {}).get("rtl_table"):
        raise GenerationError(f"{stem}: a probe may not own the tracked CSR header")
    path = tmp / f"{stem}.yaml"
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    return path


def _clean(text: str, tmp: Path | None = None) -> str:
    """Builder text without this host's paths or source line numbers, which
    would tie the page to lines nobody edits for it."""
    if tmp is not None:
        text = text.replace(str(tmp) + os.sep, "")
    text = text.replace(str(ROOT) + os.sep, "")
    text = re.sub(r"(\.(?:sv|svh|py)):\d+", r"\1", text)
    if re.search(r"(?<![\w.])/(?:home|tmp|data|Users)/", text):
        raise GenerationError(f"builder output names a host path: {text[:60]}")
    return text


def run_cli(tmp: Path, config: Path) -> str:
    """The builder command line's verdict on `config`: its summary line, or
    the refusal it exits with."""
    proc = subprocess.run([sys.executable, BUILDER, str(config), "-o", str(tmp / "out")],
                          cwd=ROOT, capture_output=True, text=True, check=False)
    if proc.returncode == 0:
        return _clean(proc.stdout.splitlines()[0], tmp)
    return _clean(proc.stderr.strip().splitlines()[-1], tmp)


def derive(config: Path) -> Any:
    """Every artifact one config implies, in memory, or its refusal."""
    try:
        return eb._derive_artifacts(str(config))
    except eb.ConfigError as exc:
        return exc


# ------------------------------------------------------------------ blocks --
def block_flow(tmp: Path, consumers=CONSUMERS, steps=STEPS) -> str:
    """The builder data flow, every label checked against the implementation."""
    config = write_probe(tmp, Path(BASE).stem, base_doc())
    # The builder's own account of its outputs: every path build() returns.
    written = {Path(p).name for p in eb.build(str(config), str(tmp / "flow"))["paths"].values()}
    for artifact, consumer, token in (*consumers, *steps):
        source = ROOT / consumer
        if not source.is_file() or token not in source.read_text(encoding="utf-8", errors="replace"):
            raise GenerationError(f"{consumer} does not name {token!r}; the {artifact} label is stale")
    for artifact, _consumer, _token in consumers:
        if artifact not in written:
            raise GenerationError(f"the builder writes no {artifact}; its node is stale")
    lines = [
        "```mermaid",
        "flowchart LR",
        '    YAML["configs/endstation_NAME.yaml<br/>the entity definition"] --> B["endstation_builder.py"]',
        '    B --> SOC["soc_params.json<br/>design argv"]',
        '    B --> PSH["platform_shape.json<br/>processor DRAM window"]',
        '    B --> UC["gptp_ucode.hex<br/>gPTP engine program"]',
        '    B --> OVL["aem_overlay.json<br/>entity model"]',
        '    B --> LWS["lwsrp_table.json<br/>reservation budget"]',
        '    B --> PLAN["build_plan.md<br/>estimate and marks"]',
        f'    B -->|"--write-rtl"| ADP["{eb.ADP_SHAPE_REL.replace("/gen/", "/gen/<br/>")}"]',
        f'    B -->|"srp.rtl_table"| CSR["{eb.CSR_DEFAULTS_REL.replace("/gen/", "/gen/<br/>")}"]',
        f'    B -->|"--write-fragment"| FRAG["{eb.GEN_CONFIG_DIR}/<br/>sweep_opts_BOARD.sh"]',
        '    SOC --> BUILD["sw/litex/build.sh"]',
        '    FRAG --> SWEEP["sw/litex/sweep.sh"]',
        '    BUILD --> MSOC["sw/litex/milan_soc.py<br/>and Vivado"]',
        "    SWEEP --> MSOC",
        "    PSH --> MSOC",
        "    UC --> MSOC",
        "    LWS --> MSOC",
        "    ADP --> RTL[\"milan_csr.sv<br/>milan_datapath.sv\"]",
        "    CSR --> RTL",
        "    RTL --> MSOC",
        '    OVL -->|"build_desc_image"| IMG["aem_desc.bin<br/>aem_desc.json, aem_desc.map"]',
        '    MSOC --> BIT["bitstream<br/>flashboot_layout.json"]',
        '    BIT --> FP["deploy.sh flash-pair<br/>QSPI"]',
        "    IMG --> FP",
        '    FP --> BOOT["bare-metal boot<br/>verify and copy the image"]',
        '    BOOT --> WIRE["entity on the wire<br/>ADP advertise, AECP READ_DESCRIPTOR"]',
        '    BUILD -.->|"check_entity_shape.py --built-config"| ADP',
        "```",
    ]
    return "\n".join(lines)


def _names(overlay: dict) -> dict:
    """The singleton object names the image carries."""
    return {**eb.OBJECT_NAMES, **(overlay.get("names") or {})}


def block_aem_tree(tmp: Path, counts_override: dict | None = None) -> str:
    """The 1x1 descriptor tree from the builder's overlay, counted against it."""
    art = derive(ROOT / BASE)
    if isinstance(art, Exception):
        raise GenerationError(f"{BASE} does not build: {art}")
    ovl = art.overlay
    counts = dict(counts_override or ovl["descriptor_counts"])
    names = _names(ovl)
    drawn: dict[str, int] = {}
    lines = ["```mermaid", "flowchart TD"]

    def node(ident: str, kind: str, label: str, n: int = 1) -> None:
        drawn[kind] = drawn.get(kind, 0) + n
        lines.append(f'    {ident}["{label}"]')

    node("E", "ENTITY", f"ENTITY<br/>{ovl['entity']['name']}")
    node("C", "CONFIGURATION", f"CONFIGURATION 0<br/>{names['configuration']}")
    lines.append("    E --> C")
    node("AU", "AUDIO_UNIT", f"AUDIO_UNIT 0<br/>{names['audio_unit']}, {ovl['current_sampling_rate_hz']} Hz")
    lines.append("    C --> AU")
    clusters = ovl["audio_clusters"]
    for direction, kind in (("input", "STREAM_PORT_INPUT"), ("output", "STREAM_PORT_OUTPUT")):
        for port in ovl["stream_ports"][direction]:
            pid = f"P{direction[0]}{port['index']}"
            node(pid, kind, f"{kind} {port['index']}<br/>{port['clusters']} clusters, "
                            f"{port['map_mode']} map")
            lines.append(f"    AU --> {pid}")
            for seg in port["pool"]:
                first = port["base_cluster"] + seg["offset"]
                last = first + seg["width"] - 1
                members = clusters[first:last + 1]
                if any(c["role"] != seg["role"] for c in members):
                    raise GenerationError(f"{kind} {port['index']}: pool and cluster roles disagree")
                span = f"{first}" if first == last else f"{first} to {last}"
                sample = members[0]["name"] if len(members) == 1 else \
                    f"{members[0]['name']} ... {members[-1]['name']}"
                cid = f"{pid}{seg['role'][:2]}"
                node(cid, "AUDIO_CLUSTER", f"AUDIO_CLUSTER {span}<br/>{seg['role']}: {sample}",
                     seg["width"])
                lines.append(f"    {pid} --> {cid}")
    for key, kind, prefix in (("stream_inputs", "STREAM_INPUT", "SI"),
                              ("stream_outputs", "STREAM_OUTPUT", "SO")):
        for s in ovl[key]:
            detail = f"AAF, {s['channels']} ch" if s["kind"] == "aaf" else "media clock"
            node(f"{prefix}{s['index']}", kind, f"{kind} {s['index']}<br/>{s['name']}, {detail}")
            lines.append(f"    C --> {prefix}{s['index']}")
    for port in ovl["stream_ports"]["input"]:
        lines.append(f"    Pi{port['index']} -.->|stream| SI{port['stream_index']}")
    for port in ovl["stream_ports"]["output"]:
        lines.append(f"    Po{port['index']} -.->|stream| SO{port['stream_index']}")
    node("AVB", "AVB_INTERFACE", f"AVB_INTERFACE 0<br/>{names['avb_interface']}")
    lines.append("    C --> AVB")
    node("CD", "CLOCK_DOMAIN", f"CLOCK_DOMAIN 0<br/>{names['clock_domain']}")
    lines.append("    C --> CD")
    for cs in ovl["clock_sources"]:
        node(f"CS{cs['index']}", "CLOCK_SOURCE", f"CLOCK_SOURCE {cs['index']}<br/>{cs['name']}")
        lines.append(f"    C --> CS{cs['index']}")
        lines.append(f"    CD -.-> CS{cs['index']}")
        if cs["location_type"] == "STREAM_INPUT":
            lines.append(f"    CS{cs['index']} -.->|located on| SI{cs['location_index']}")
    node("CTL", "CONTROL", f"CONTROL 0<br/>{names['control_identify']}")
    lines.append("    C --> CTL")
    node("LOC", "LOCALE", "LOCALE 0")
    node("STR", "STRINGS", "STRINGS 0")
    lines += ["    C --> LOC", "    LOC --> STR", "```"]
    want = {k: v for k, v in counts.items() if v}
    if drawn != want:
        raise GenerationError(f"the tree draws {drawn}, the overlay counts {want}")
    # The CONFIGURATION's children must be the types the descriptor layer
    # lists in its descriptor_counts; the rest are reached through a parent.
    layer = (ROOT / "avdecc" / "aem_descriptors.py").read_text(encoding="utf-8")
    listed = re.search(r"def d_configuration.*?counts = \[(.*?)\]\n", layer, re.S)
    top = set(re.findall(r"\(([A-Z_]+),", listed.group(1))) if listed else set()
    ids = {"AU": "AUDIO_UNIT", "SI": "STREAM_INPUT", "SO": "STREAM_OUTPUT", "AVB": "AVB_INTERFACE",
           "CD": "CLOCK_DOMAIN", "CS": "CLOCK_SOURCE", "CTL": "CONTROL", "LOC": "LOCALE"}
    children = {ids[m] for m in re.findall(r"^    C --> ([A-Z]+?)\d*$", "\n".join(lines), re.M)}
    if children != top:
        raise GenerationError(f"CONFIGURATION children {sorted(children)} differ from the "
                              f"descriptor layer's top-level counts {sorted(top)}")
    return "\n".join(lines)


def _estimate(art: Any) -> tuple[str, str, str, str]:
    """(streams, clusters, worst category, verdict) of one derivation."""
    if isinstance(art, Exception):
        return "-", "-", "-", f"refused: {_clean(str(art)).split(' (')[0]}"
    est, cfg = art.est, art.cfg
    return (f"{len(cfg['listeners'])}x{len(cfg['talkers'])}",
            str(art.overlay["descriptor_counts"]["AUDIO_CLUSTER"]),
            f"{est['worst_category'].upper()} {est['worst_pct']} %", est["verdict"])


def block_resources(tmp: Path) -> str:
    """The builder's estimate for every tracked config and the widened probes."""
    rows = []
    for path in sorted((ROOT / "configs").glob("endstation_*.yaml")):
        rows.append((f"`{path.name}`", *_estimate(derive(path))))
    for n in WIDENED:
        probe = write_probe(tmp, f"endstation_try_{n}x{n}", widened(n))
        rows.append((f"1x1 widened to {n}x{n}", *_estimate(derive(probe))))
    out = ["| Configuration | Streams | AUDIO_CLUSTERs | Worst | Verdict |",
           "|---|---|---|---|---|"]
    out += [f"| {' | '.join(r)} |" for r in rows]
    return "\n".join(out)


def block_example_yaml(tmp: Path) -> str:
    """The `streams:` block the 2x2 example declares."""
    text = yaml.safe_dump({"streams": widened(2)["streams"]}, sort_keys=False,
                          default_flow_style=None)
    return "```yaml\n" + text.rstrip() + "\n```"


def block_example_2x2(tmp: Path) -> str:
    """The builder's verdict on the 2x2 probe, and its plan's verdict line."""
    probe = write_probe(tmp, "endstation_try_2x2", widened(2))
    line = run_cli(tmp, probe)
    plan = (tmp / "out" / "endstation_try_2x2" / "build_plan.md").read_text(encoding="utf-8")
    verdict = next(ln for ln in plan.splitlines() if ln.startswith("**Verdict:"))
    return "```console\n" + line + "\n" + verdict.replace("**", "") + "\n```"


def block_example_wide(tmp: Path) -> str:
    """The builder's refusal of the widest probe."""
    probe = write_probe(tmp, f"endstation_try_{WIDENED[-1]}x{WIDENED[-1]}", widened(WIDENED[-1]))
    return "```console\n" + run_cli(tmp, probe) + "\n```"


def block_example_narrow(tmp: Path) -> str:
    """The builder's verdict on the channel change that fits."""
    probe = write_probe(tmp, f"endstation_try_1x1_{NARROW}ch", narrowed(NARROW))
    return "```console\n" + run_cli(tmp, probe) + "\n```"


def _facts(art: Any) -> dict[str, str]:
    """The facts a shape edit can move, read off one derivation."""
    cfg, ovl = art.cfg, art.overlay
    talker = next(r for r in art.lwsrp["rows"] if r["direction"] == "talker")
    argv = art.argv
    wire = argv[argv.index("--talker-wire-chans") + 1] if "--talker-wire-chans" in argv else "2"
    shape = re.search(r"TALKER_WIRE_CHANS_C\s*=\s*(\d+)", art.adp_svh)
    counts = ovl["descriptor_counts"]
    return {
        "`entity_model_id`": f"`{ovl['model_id']['value']}`",
        "STREAM_INPUT / STREAM_OUTPUT": f"{counts['STREAM_INPUT']} / {counts['STREAM_OUTPUT']}",
        "AUDIO_CLUSTER": str(counts["AUDIO_CLUSTER"]),
        "ADP talker sources / listener sinks":
            f"{ovl['adp']['talker_stream_sources']} / {ovl['adp']['listener_stream_sinks']}",
        "Listener 0 formats": ", ".join(f"`{f}`" for f in ovl["stream_inputs"][0]["formats"]),
        "Talker 0 format": ", ".join(f"`{f}`" for f in ovl["stream_outputs"][0]["formats"]),
        "`--talker-wire-chans`": f"`{wire}`",
        "`TALKER_WIRE_CHANS_C`": f"`{shape.group(1) if shape else '-'}`",
        "Talker 0 MaxFrameSize": str(talker["max_frame_bytes"]),
        "Class A reservation, bit/s": str(art.lwsrp["bandwidth"]["total_idle_slope_bps"]),
        "Estimate": f"{art.est['verdict']}, {art.est['worst_category'].upper()} {art.est['worst_pct']} %",
    }


def block_moves(tmp: Path) -> str:
    """What the 2x2 edit and the channel edit move, against the shipping 1x1."""
    base = derive(ROOT / BASE)
    two = derive(write_probe(tmp, "endstation_try_2x2", widened(2)))
    narrow = derive(write_probe(tmp, f"endstation_try_1x1_{NARROW}ch", narrowed(NARROW)))
    for art in (base, two, narrow):
        if isinstance(art, Exception):
            raise GenerationError(f"a worked-example shape does not build: {art}")
    a, b, c = _facts(base), _facts(two), _facts(narrow)
    out = [f"| Fact | Shipping 1x1 | 2x2 | 1x1 at {NARROW} channels |", "|---|---|---|---|"]
    out += [f"| {k} | {a[k]} | {b[k]} | {c[k]} |" for k in a]
    return "\n".join(out)


def check_claims(tmp: Path, widths: tuple[int, ...] = WIDENED) -> None:
    """The page's prose about the generated values, held to them: each
    sentence named here is refused the moment the builder makes it false."""
    base = derive(ROOT / BASE)
    two = derive(write_probe(tmp, "endstation_try_2x2", widened(2)))
    narrow = derive(write_probe(tmp, f"endstation_try_1x1_{NARROW}ch", narrowed(NARROW)))
    wide = [derive(write_probe(tmp, f"endstation_try_{n}x{n}", widened(n))) for n in widths]
    proc = subprocess.run([sys.executable, BUILDER, str(tmp / "endstation_try_2x2.yaml"),
                           "-o", str(tmp / "claims")], cwd=ROOT, capture_output=True, text=True)
    written = tmp / "claims" / "endstation_try_2x2"
    claims = {
        "The shipping 1x1 TDM8 shape fits": base.est["verdict"] != "OVER",
        "Every widened shape exceeds the estimate's limit":
            all(isinstance(a, Exception) or a.est["verdict"] == "OVER" for a in wide),
        "The widest probe is refused for another reason: names":
            isinstance(wide[-1], eb.ConfigError) and "NAME records" in str(wide[-1]),
        "An OVER configuration still writes every artifact and exits zero":
            proc.returncode == 0 and two.est["verdict"] == "OVER"
            and all((written / f).is_file() for f in ("soc_params.json", "aem_overlay.json",
                                                       "platform_shape.json", "build_plan.md")),
        "The channel change: the estimate does not change": narrow.est == base.est,
        "Both edits move entity_model_id":
            len({a.overlay["model_id"]["value"] for a in (base, two, narrow)}) == 3,
        "The channel change moves formats, wire width and reservation":
            all(_facts(narrow)[k] != _facts(base)[k] for k in
                ("Talker 0 format", "`--talker-wire-chans`", "Class A reservation, bit/s")),
        "The 2x2 edit adds descriptors, clusters and estimate":
            all(_facts(two)[k] != _facts(base)[k] for k in
                ("STREAM_INPUT / STREAM_OUTPUT", "AUDIO_CLUSTER", "Estimate")),
    }
    # The page's section table names every top-level key the loaders read.
    import test_builder as tb  # noqa: PLC0415 - only this claim needs the key recorder
    tops = {k.split(".")[0].removesuffix("[]") for k in tb._loader_key_paths()}
    model = PAGE.read_text(encoding="utf-8").split("## The model", 1)[1].split("\n### ", 1)[0]
    listed = set(re.findall(r"`([a-z_]+)`", "\n".join(
        ln.split("|")[1] for ln in model.splitlines() if ln.startswith("| `"))))
    claims["The model table lists every top-level section"] = listed == tops
    false = [claim for claim, holds in claims.items() if not holds]
    if false:
        raise GenerationError(f"the page's prose no longer holds: {false}")


def block_sim_legs(tmp: Path) -> str:
    """The suites whose build files include each tracked shape."""
    files = sorted((ROOT / "tb" / "verilator").glob("*/Makefile")) + \
        sorted((ROOT / "tb" / "verilator").glob("*/*.mk"))
    out = ["| Configuration | Suites that include its shape |", "|---|---|"]
    for path in sorted((ROOT / "configs").glob("endstation_*.yaml")):
        suites = sorted({f.parent.name for f in files
                         if path.stem in f.read_text(encoding="utf-8", errors="replace")})
        out.append(f"| `{path.name}` | {', '.join(f'`{s}`' for s in suites) or 'none'} |")
    return "\n".join(out)


#: (artifact, where it lands, when it is written, who reads it). The tree
#: column is measured, the reader is one CONSUMERS or STEPS entry checks.
ARTIFACTS = (
    ("soc_params.json", "OUT", "every run", "`sw/litex/build.sh`, then `milan_soc.py`"),
    ("aem_overlay.json", "OUT", "every run", "`milan_soc.py` `build_desc_image`, which writes `aem_desc.bin`"),
    ("platform_shape.json", "OUT", "every run", "`milan_soc.py`"),
    ("gptp_ucode.hex", "OUT", "every run", "`milan_soc.py`"),
    ("lwsrp_table.json", "OUT", "every run", "`milan_soc.py`"),
    ("lwsrp_table.svh", "OUT", "every run", "no build step"),
    ("aecp_aem_rom.svh", "OUT", "every run", "no build step"),
    ("build_plan.md", "OUT", "every run", "a person"),
    ("adp_shape_defaults.svh", "GEN", "every run of a config under `configs/`",
     "simulation suites, by include path"),
    ("adp_shape_defaults.svh", "ADP", "`--write-rtl`", "`milan_csr.sv` and `milan_datapath.sv`"),
    ("lwsrp_csr_defaults.svh", "CSR", "`srp.rtl_table: true`", "`milan_csr.sv`"),
    ("sweep_opts_ax7101.sh", "FRAG", "`--write-fragment` or `--write-rtl`", "`sw/litex/sweep.sh`"),
)
#: Files no gateware, launcher, firmware or harness source names outside a comment.
ORPHANS = ("lwsrp_table.svh", "aecp_aem_rom.svh")
_C_COMMENT = re.compile(r"//[^\n]*|/\*.*?\*/", re.S)
_HASH_COMMENT = re.compile(r"(?m)#[^\n]*")
#: The comment syntax of each source kind a reader could be written in.
COMMENTS = {".sv": _C_COMMENT, ".svh": _C_COMMENT, ".v": _C_COMMENT, ".c": _C_COMMENT,
            ".h": _C_COMMENT, ".py": _HASH_COMMENT, ".sh": _HASH_COMMENT, ".mk": _HASH_COMMENT,
            ".tcl": _HASH_COMMENT}


def block_artifacts(tmp: Path) -> str:
    """Where each artifact lands and whether a copy is tracked, measured on
    the shipping config, with each orphan proved to have no reader."""
    stem = Path(BASE).stem
    places = {
        "OUT": ("`sw/builder/out/<config>/`", None),
        "GEN": (f"`{eb.GEN_CONFIG_DIR}/<config>/gen/`",
                ROOT / eb.GEN_CONFIG_DIR / stem / "gen" / "adp_shape_defaults.svh"),
        "ADP": (f"`{eb.ADP_SHAPE_REL}`", ROOT / eb.ADP_SHAPE_REL),
        "CSR": (f"`{eb.CSR_DEFAULTS_REL}`", ROOT / eb.CSR_DEFAULTS_REL),
        "FRAG": (f"`{eb.GEN_CONFIG_DIR}/sweep_opts_<board>.sh`",
                 ROOT / eb.GEN_CONFIG_DIR / "sweep_opts_ax7101.sh"),
    }
    # Build steps only: a gate may name an orphan to refuse it in a gen/ dir.
    readers = [ROOT / d for d in ("hdl", "sw/litex", "sw/firmware", "tb")]
    for top in readers:
        for f in top.rglob("*"):
            if not f.is_file() or f.suffix not in COMMENTS:
                continue
            code = COMMENTS[f.suffix].sub("", f.read_text(encoding="utf-8", errors="replace"))
            for orphan in ORPHANS:
                if orphan in code:
                    raise GenerationError(f"{f.relative_to(ROOT)} names {orphan}; it has a reader")
    out = ["| Artifact | Lands in | Tracked copy | Written | Read by |", "|---|---|---|---|---|"]
    for name, place, when, reader in ARTIFACTS:
        where, tree = places[place]
        tracked = "no" if tree is None else ("yes" if tree.is_file() else "no")
        out.append(f"| `{name}` | {where} | {tracked} | {when} | {reader} |")
    return "\n".join(out)


def block_model_id(tmp: Path) -> str:
    """How `load_config` resolves `entity_model_id`, its widths read off the builder."""
    source = Path(eb.__file__).read_text(encoding="utf-8")
    for token in ('"model_id_pin" in ent', 'raw == "hash-derived"', "hashlib.sha256(canon)",
                  "oui << MODEL_ID_HASH_BITS", "def model_shape"):
        if token not in source:
            raise GenerationError(f"endstation_builder.py no longer has {token!r}")
    hash_bits = eb.MODEL_ID_HASH_BITS
    oui_bits = eb.EUI64_MAX.bit_length() - hash_bits
    return "\n".join([
        "```mermaid",
        "flowchart LR",
        '    PIN{"entity.model_id_pin<br/>declared?"} -->|yes| USE["that EUI-64"]',
        '    PIN -->|no| HD{"entity_model_id is<br/>hash-derived?"}',
        '    HD -->|no| LIT["the literal EUI-64"]',
        '    HD -->|yes| SHAPE["model_shape(): counts, formats,<br/>clusters, clock sources, gPTP"]',
        '    SHAPE --> JSON["canonical JSON"]',
        f'    JSON --> SHA["SHA-256, low {hash_bits} bits<br/>of its first eight octets"]',
        f'    OUI["entity.vendor_oui<br/>{oui_bits} bits, default 0x{eb.MODEL_ID_OUI:06X}"] --> ID',
        '    SHA --> ID["entity_model_id"]',
        '    USE --> OUTID["ENTITY and ADPDU<br/>entity_model_id"]',
        "    LIT --> OUTID",
        "    ID --> OUTID",
        "```",
    ])


BLOCKS: dict[str, Callable[[Path], str]] = {
    "flow": block_flow,
    "artifacts": block_artifacts,
    "model-id": block_model_id,
    "aem-tree": block_aem_tree,
    "resources": block_resources,
    "example-yaml": block_example_yaml,
    "example-2x2": block_example_2x2,
    "example-wide": block_example_wide,
    "example-narrow": block_example_narrow,
    "moves": block_moves,
    "sim-legs": block_sim_legs,
}


def splice(page: str, blocks: dict[str, str]) -> str:
    """`page` with every generated block replaced; each marker pair once."""
    for name, body in blocks.items():
        start, end = marker(name)
        if page.count(start) != 1 or page.count(end) != 1:
            raise GenerationError(f"{PAGE.name}: needs exactly one {name} marker pair")
        head, rest = page.split(start, 1)
        _old, tail = rest.split(end, 1)
        page = f"{head}{start}\n{body}\n{end}{tail}"
    return page


def generate() -> dict[str, str]:
    """Every block, built in one temporary directory, after the prose claims."""
    with probe_dir() as tmp:
        check_claims(tmp)
        return {name: fn(tmp) for name, fn in BLOCKS.items()}


def diff(page: str, fresh: str) -> list[str]:
    """The unified difference between the tracked and the generated page."""
    return list(difflib.unified_diff(page.splitlines(), fresh.splitlines(),
                                     f"{PAGE.name} (tracked)", f"{PAGE.name} (generated)",
                                     lineterm="", n=0))


def selftest() -> int:
    """The stale-page mutant must be reported, and each label check, the
    descriptor count check and the marker check must refuse."""
    page = PAGE.read_text(encoding="utf-8")
    blocks = generate()
    failures = []
    if diff(page, splice(page, blocks)):
        failures.append("the tracked page is not fresh, so the stale-page arm proves nothing")
    start, _end = marker("resources")
    cut = page.index("|", page.index(start)) + 1
    stale = page[:cut] + " stale" + page[cut:]
    if not diff(stale, splice(stale, blocks)):
        failures.append("a planted stale cell was not reported")
    with probe_dir() as tmp:
        arms = {
            "a consumer that no longer names its file":
                lambda: block_flow(tmp, consumers=(("soc_params.json", "sw/litex/build.sh",
                                                    "no_such_artifact.json"),)),
            "an artifact the builder does not write":
                lambda: block_flow(tmp, consumers=(("no_such_artifact.json", "sw/litex/build.sh",
                                                    "soc_params.json"),)),
            "a descriptor count the tree does not draw":
                lambda: block_aem_tree(tmp, counts_override={"ENTITY": 1, "AUDIO_CLUSTER": 99}),
            "a missing marker pair":
                lambda: splice(page.replace(marker("flow")[0], ""), blocks),
            # a 1x1 "widening" fits, so "every widened shape exceeds" is false
            "a prose claim the builder no longer bears out":
                lambda: check_claims(tmp, widths=(1, WIDENED[-1])),
        }
        for name, arm in arms.items():
            try:
                arm()
            except GenerationError:
                continue
            failures.append(f"{name}: was not refused")
    for failure in failures:
        print(f"selftest: {failure}")
    if failures:
        return 1
    print(f"endstation definition selftest: OK (stale page and {len(arms)} planted defects refused)")
    return 0


def main() -> int:
    """Rewrite the generated blocks, check them, or prove the checks bite."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="fail when a block is stale")
    mode.add_argument("--selftest", action="store_true", help="prove each check bites")
    args = parser.parse_args()
    try:
        if args.selftest:
            return selftest()
        page = PAGE.read_text(encoding="utf-8")
        fresh = splice(page, generate())
        if args.check:
            delta = diff(page, fresh)
            if delta:
                print("\n".join(delta[:40]))
                print(f"{PAGE.name}: generated blocks are stale; run "
                      "python3 docs/diagrams/endstation_definition.gen.py")
                return 1
            print(f"{PAGE.name}: generated blocks are fresh")
            return 0
        PAGE.write_text(fresh, encoding="utf-8")
        print(f"wrote {PAGE.relative_to(ROOT)}")
        return 0
    except GenerationError as exc:
        print(f"REFUSED: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
