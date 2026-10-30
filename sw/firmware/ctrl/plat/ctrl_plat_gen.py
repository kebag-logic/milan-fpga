#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate the split platform's two headers (#665): its boot policy and its bus map.

policy CONFIG -o ctrl_plat_policy_gen.h
    The generated identity and static product policy the platform writes to the
    datapath CSR window (ctrl_plat_csr.h), from sw/litex/boot_policy.py's
    fabric_constants(): the one derivation sw/litex/milan_soc.py publishes for
    milan_baremetal.c's configure_fabric() and builder gate 35 runs it on. Its
    inputs are the config's AEM overlay and lwSRP table, as the builder emits
    them, the inputs adp_entity.py and aecp_entity.py read. Also the talker
    sources' streams (ctrl_plat.h struct ctrl_plat_stream): each AAF talker's
    row of the lwSRP table, then the CRF Media Clock Output's, at the builder's
    CRF_SRP_MAXFRAME_B, one frame per interval and the same class. The count
    must be ADP's talker_stream_sources, the count SRP and ACMP are sized by.

map CSR_CSV -o ctrl_plat_map_gen.h
    The bus addresses the image reaches, from the SoC's own csr.csv: the
    milan_csr and ctrl_mbx regions and the UART's four registers. The address
    map is independent of the image (docs/design/SPLIT_CONTROL_MEMORY.md
    section 4), so an export with any image gives the image's map. A csr.csv
    whose UART pops its receive FIFO on the RXTX read (rx_fifo_rx_we) is
    refused: the console pops it through EV_PENDING.

Exit 0 written; 2 refused (the input does not say what the header needs).
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]

#: ctrl_plat_policy field -> the fabric_constants() word that fills it, in the struct's order.
POLICY_FIELDS = (("entity_id_lo", "MILAN_ENTITY_ID_LO"), ("entity_id_hi", "MILAN_ENTITY_ID_HI"),
                 ("model_id_lo", "MILAN_MODEL_ID_LO"), ("model_id_hi", "MILAN_MODEL_ID_HI"),
                 ("station_mac_lo", "MILAN_STATION_MAC_LO"), ("station_mac_hi", "MILAN_STATION_MAC_HI"),
                 ("mac_ctrl_set", "MILAN_MAC_CTRL_SET"), ("tcam_ctrl", "MILAN_TCAM_CTRL_BOOT"),
                 ("aaf_ctrl", "MILAN_AAF_CTRL_BOOT"), ("sr_vid", "MILAN_SR_VID"),
                 ("lwsrp_ctrl_reset", "MILAN_LWSRP_CTRL_RESET"), ("maap_ctrl", "MILAN_MAAP_CTRL_BOOT"),
                 ("crf_tx_ctrl", "MILAN_CRF_TX_CTRL_BOOT"))
#: Map macro -> (csr.csv row kind, name).
MAP_ROWS = (("CTRL_PLAT_CSR_BASE", "memory_region", "milan_csr"),
            ("CTRL_MBX_BASE", "memory_region", "ctrl_mbx"),
            ("CTRL_PLAT_UART_RXTX", "csr_register", "uart_rxtx"),
            ("CTRL_PLAT_UART_TXFULL", "csr_register", "uart_txfull"),
            ("CTRL_PLAT_UART_RXEMPTY", "csr_register", "uart_rxempty"),
            ("CTRL_PLAT_UART_EV_PENDING", "csr_register", "uart_ev_pending"))
#: LiteX's constant when the UART pops on the RXTX read (soc.py add_uart).
RX_WE = "config_uart_rx_fifo_rx_we"


class Refusal(Exception):
    """The input does not say what the header needs."""


def builder_inputs(config: Path) -> tuple[dict, dict]:
    """The config's AEM overlay and lwSRP table, as the end-station builder emits them."""
    sys.path.insert(0, str(ROOT / "sw/builder"))
    import endstation_builder as eb  # noqa: E402
    try:
        cfg = eb.load_config(str(config))
        return eb.emit_aem_overlay(cfg), eb.emit_lwsrp_table(cfg)
    except eb.ConfigError as error:
        raise Refusal(f"{config.name}: {error}") from error


def streams(overlay: dict, lwsrp: dict) -> list[tuple[int, int, int, int]]:
    """(unique_id, max_frame_size, max_interval_frames, priority_and_rank) per talker source."""
    sys.path.insert(0, str(ROOT / "sw/builder"))
    import endstation_builder as eb  # noqa: E402
    rank = lwsrp["sr_class"]["prio_rank"]
    rows = sorted((r for r in lwsrp["rows"] if r["direction"] == "talker"), key=lambda r: r["stream_index"])
    out = [(r["unique_id"], r["max_frame_bytes"], r["interval_frames"], rank) for r in rows]
    kinds = [s.get("kind", "aaf") for s in overlay["stream_outputs"]]
    if kinds != ["aaf"] * len(rows) + ["crf"] * kinds.count("crf") or kinds.count("crf") > 1:
        raise Refusal(f"the STREAM_OUTPUTs {kinds} are not the lwSRP table's {len(rows)} AAF talkers "
                      "then at most one CRF output")
    if "crf" in kinds:
        out.append((len(rows), eb.CRF_SRP_MAXFRAME_B, 1, rank))
    return out


def policy_header(config: Path) -> str:
    """ctrl_plat_policy_gen.h for one config."""
    sys.path.insert(0, str(ROOT / "sw/litex"))
    sys.path.insert(0, str(ROOT / "sw/firmware/ctrl/adp"))
    import adp_entity  # noqa: E402
    import boot_policy  # noqa: E402
    overlay, lwsrp = builder_inputs(config)
    words = boot_policy.fabric_constants(overlay, lwsrp)
    talkers = streams(overlay, lwsrp)
    sources = adp_entity.entity_fields(config)["talker_stream_sources"]
    if len(talkers) != sources:
        raise Refusal(f"{len(talkers)} talker streams, but ADP advertises {sources} talker sources")
    aaf = words["MILAN_N_TALKERS"]
    policy = ", \\\n".join(f"\t.{field} = 0x{words[name]:08X}u" for field, name in POLICY_FIELDS)
    rows = ", \\\n".join(f"\t{{{u}u, {f}u, {i}u, 0x{r:02X}u}}" for u, f, i, r in talkers)
    return "\n".join([
        "// SPDX-FileCopyrightText: 2026 Kebag Logic",
        "// SPDX-License-Identifier: CERN-OHL-W-2.0",
        "//",
        f"// GENERATED by sw/firmware/ctrl/plat/ctrl_plat_gen.py from {config.name}; DO NOT EDIT.",
        "// The split platform's identity, boot policy and talker streams (ctrl_plat.h).",
        "",
        "#ifndef CTRL_PLAT_POLICY_GEN_H",
        "#define CTRL_PLAT_POLICY_GEN_H",
        "",
        "#define CTRL_PLAT_POLICY_INIT { \\",
        policy + " \\",
        "}",
        "#define CTRL_PLAT_STREAMS_INIT { \\",
        rows + " \\",
        "}",
        f"#define CTRL_PLAT_AAF_OUTPUTS {aaf}u",
        f"#define CTRL_PLAT_CRF_OUTPUT {'true' if len(talkers) > aaf else 'false'}",
        f"#define CTRL_PLAT_LINK_BPS {lwsrp['bandwidth']['link_bps']}u",
        "",
        "#endif // CTRL_PLAT_POLICY_GEN_H",
        ""])


def map_header(csr_csv: Path) -> str:
    """ctrl_plat_map_gen.h from one SoC export's csr.csv."""
    rows: dict[tuple[str, str], str] = {}
    with csr_csv.open(newline="", encoding="utf-8") as handle:
        for row in csv.reader(line for line in handle if not line.startswith("#")):
            if len(row) >= 3:
                rows.setdefault((row[0], row[1]), row[2])
    if ("constant", RX_WE) in rows:
        raise Refusal(f"{csr_csv.name}: the UART pops on the RXTX read ({RX_WE}); the console pops through "
                      "EV_PENDING")
    lines = []
    for macro, kind, name in MAP_ROWS:
        if (kind, name) not in rows:
            raise Refusal(f"{csr_csv.name} holds no {kind} {name}")
        lines.append(f"#define {macro} 0x{int(rows[(kind, name)], 16):08X}u")
    return "\n".join([
        "// SPDX-FileCopyrightText: 2026 Kebag Logic",
        "// SPDX-License-Identifier: CERN-OHL-W-2.0",
        "//",
        f"// GENERATED by sw/firmware/ctrl/plat/ctrl_plat_gen.py from {csr_csv.name}; DO NOT EDIT.",
        "// The split platform's bus addresses (ctrl_plat_main.c).",
        "",
        "#ifndef CTRL_PLAT_MAP_GEN_H",
        "#define CTRL_PLAT_MAP_GEN_H",
        "",
        *lines,
        "",
        "#endif // CTRL_PLAT_MAP_GEN_H",
        ""])


def main(argv: list[str] | None = None) -> int:
    """Write one header, or report why the input refuses it."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("kind", choices=("policy", "map"))
    parser.add_argument("source", type=Path, help="the config (policy) or the SoC's csr.csv (map)")
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        text = policy_header(args.source) if args.kind == "policy" else map_header(args.source)
        args.output.write_text(text, encoding="utf-8")
    except (Refusal, OSError, ValueError, KeyError) as error:
        print(f"ctrl_plat_gen: REFUSED: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
