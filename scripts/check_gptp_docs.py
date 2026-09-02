#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Check current fabric-gPTP routing and source evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WAVEDROM = ROOT / "docs" / "diagrams" / "wd_gptp_pdelay.json"
MANAGER = ROOT / "docs" / "guides" / "gptp" / "MANAGER.md"
FEATURE_STATUS = ROOT / "docs" / "reference" / "milan_feature_status.json"

DOCUMENT_TOKENS = {
    "docs/design/GPTP_PLANE.md": (
        "guides/gptp/MANAGER.md",
        "guides/gptp/SYSTEM_INTEGRATOR.md",
        "guides/gptp/HDL_DEVELOPER.md",
        "guides/gptp/TEST_DEVELOPER.md",
        "RX",
        "TX",
        "PHC",
        "Publication",
        "make -C gptp-processor",
        "make -C tb/verilator/gptp_shadow",
    ),
    "docs/design/TIME_SYNC.md": (
        "crf.media-clock-consumption",
        "gptp.fabric-product-owner",
        "PHC",
        "Processor timebase",
        "Media clock",
        "KL_media_grid_align",
        "tu",
    ),
    "docs/design/GM_LOSS_RECOVERY.md": (
        "Announce timeout",
        "Sync timeout",
        "Pdelay failure",
        "pub_commit_o",
        "pub_disc_o",
        "0.25 seconds",
        "HOLDOVER",
    ),
    "docs/traceability/ieee8021as.md": tuple(
        f"AS-{number}" for number in range(1, 13)
    ),
    "docs/guides/gptp/MANAGER.md": (
        "Value",
        "Status",
        "Risks",
        "Issue #74",
        "Issue #117",
    ),
    "docs/guides/gptp/SYSTEM_INTEGRATOR.md": (
        "Configure",
        "Connect",
        "Observe",
        "Verify",
    ),
    "docs/guides/gptp/HDL_DEVELOPER.md": (
        "KL_gptp_shadow",
        "KL_gptp_txstamp",
        "rx_accept.svg",
        "tx_backpressure.svg",
    ),
    "docs/guides/gptp/TEST_DEVELOPER.md": (
        "| Python |",
        "| C |",
        "| C++ |",
        "gptp_shadow",
        "tsn_fuzz",
    ),
}

SOURCE_TOKENS = {
    "hdl/milan/milan_datapath.sv": (
        "parameter bit GPTP_PLANE_EN_P = 1'b1",
        "always_ff @(posedge axis_clk) begin : media_clk_resolve",
        "pp_aecp_clk_src_index_w == AEM_CRF_CLKSRC_C",
        "KL_media_grid_align #(",
        "KL_gptp_shadow #(",
        "KL_gptp_txstamp #(",
    ),
    "hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv": (
        "assign beat_w = rx_tvalid_i & rx_tready_i",
        "input  wire [3:0]  txts_type_i",
        "output logic        pub_commit_o",
        "output wire         pub_disc_o",
    ),
    "hdl/ieee8021as/gptp_plane/KL_gptp_txstamp.sv": (
        "assign beat_w = tx_tvalid_i & tx_tready_i",
        "if ((bcnt_r == 3'd5) && is_gptp_r && take_r) begin",
        "if (tx_tlast_i)          bcnt_r <= 3'd0;",
        "output logic [15:0] ts_seq_o",
        "output logic [3:0]  ts_type_o",
    ),
    "hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv": (
        "assign ts_uncertain_o = (~sync_ok_w) | hold_w | disc_p_w",
        "assign as_capable_o = as_cap_w",
    ),
}

WAVEDROM_TOKENS = (
    "accepted MAC SOF",
    "TX PHC capture",
    "accepted sequence beat 5",
    "{t1, seq, type=2}",
    "accepted tap SOF",
    "RX PHC capture",
    "frame FIFO commit",
    "engine RX SOF",
    "sequence plus message type",
)

# KL_gptp_txstamp captures sequenceId on accepted beat 5 and raises its
# registered tuple before a normal Pdelay frame reaches tx_tlast_i. This order
# is the interface contract; labels alone cannot prove it.
WAVEDROM_ORDER = (
    ("accepted MAC SOF", "accepted sequence beat 5"),
    ("accepted sequence beat 5", "returned tuple"),
    ("returned tuple", "accepted MAC EOF"),
)

SUBMODULE_DOCS = (
    "README.md",
    "docs/README.md",
    "docs/MANAGER.md",
    "docs/INTEGRATION.md",
    "docs/HDL_DEVELOPER.md",
    "docs/TEST_DEVELOPER.md",
    "docs/SOURCE_EVIDENCE.md",
    "docs/diagrams/gptp_architecture.drawio",
    "docs/diagrams/wavedrom/rx_accept.json",
    "docs/diagrams/wavedrom/tx_backpressure.json",
    "scripts/check_docs.py",
    "scripts/generate_diagrams.py",
)


def token_findings(path: str, text: str, tokens: tuple[str, ...]) -> list[str]:
    return [f"{path}: missing token: {token}" for token in tokens if token not in text]


def file_token_findings(root: Path, mapping: dict[str, tuple[str, ...]]) -> list[str]:
    findings: list[str] = []
    for relative, tokens in mapping.items():
        path = root / relative
        if not path.is_file():
            findings.append(f"{relative}: required file is missing")
            continue
        findings.extend(
            token_findings(relative, path.read_text(encoding="utf-8"), tokens)
        )
    return findings


def flatten_json(value: object) -> list[str]:
    if isinstance(value, dict):
        return [item for child in value.values() for item in flatten_json(child)]
    if isinstance(value, list):
        return [item for child in value for item in flatten_json(child)]
    return [str(value)]


def named_waves(value: object) -> dict[str, list[str]]:
    """Collect every named WaveDrom signal without assuming group layout."""
    waves: dict[str, list[str]] = {}
    if isinstance(value, dict):
        name = value.get("name")
        wave = value.get("wave")
        if isinstance(name, str) and isinstance(wave, str):
            waves.setdefault(name, []).append(wave)
        children = value.values()
    elif isinstance(value, list):
        children = value
    else:
        children = ()
    for child in children:
        for child_name, items in named_waves(child).items():
            waves.setdefault(child_name, []).extend(items)
    return waves


def wavedrom_value_findings(value: object, label: str) -> list[str]:
    findings = token_findings(label, "\n".join(flatten_json(value)), WAVEDROM_TOKENS)
    waves = named_waves(value)
    cycles: dict[str, int] = {}
    ordered_names = {name for pair in WAVEDROM_ORDER for name in pair}
    for name in sorted(ordered_names):
        matches = waves.get(name, [])
        if len(matches) != 1:
            findings.append(
                f"{label}: expected one named signal {name!r}, found {len(matches)}"
            )
            continue
        rises = [index for index, symbol in enumerate(matches[0]) if symbol == "1"]
        if len(rises) != 1:
            findings.append(
                f"{label}: signal {name!r} must contain one asserted event"
            )
            continue
        cycles[name] = rises[0]
    for before, after in WAVEDROM_ORDER:
        if before in cycles and after in cycles and cycles[before] >= cycles[after]:
            findings.append(
                f"{label}: {before!r} must precede {after!r}; "
                f"cycles are {cycles[before]} and {cycles[after]}"
            )
    return findings


def wavedrom_findings(path: Path = WAVEDROM) -> list[str]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"{path.relative_to(ROOT)}: unreadable WaveDrom: {error}"]
    return wavedrom_value_findings(value, path.relative_to(ROOT).as_posix())


def manager_status_findings(text: str | None = None) -> list[str]:
    """Keep the manager status tied to its named canonical ledger."""
    label = MANAGER.relative_to(ROOT).as_posix()
    try:
        if text is None:
            text = MANAGER.read_text(encoding="utf-8")
        ledger = json.loads(FEATURE_STATUS.read_text(encoding="utf-8"))
        feature = next(
            item for item in ledger["features"]
            if item["id"] == "crf.media-clock-consumption"
        )
        status = feature["status"]
        if not isinstance(status, str):
            raise TypeError("feature status is not text")
    except (OSError, json.JSONDecodeError, KeyError, StopIteration, TypeError) as error:
        return [f"{label}: cannot verify media-clock status: {error}"]
    display_status = status.replace("-", " ").replace("_", " ").title()
    expected = (
        f"| Media clock selection | {display_status} | Feature-status ledger |"
    )
    findings = []
    if expected not in text:
        findings.append(
            f"{label}: media-clock row does not match canonical status "
            f"{status!r}; expected {expected}"
        )
    if "Media clock selection remains unconsumed." in text:
        findings.append(
            f"{label}: media-clock risk contradicts canonical status {status!r}"
        )
    return findings


def gitlink_pin() -> str:
    fields = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "--stage", "--", "gptp-processor"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.split()
    if len(fields) < 4 or fields[0] != "160000" or fields[2] != "0":
        raise ValueError("gptp-processor is not one stage-zero gitlink")
    return fields[1]


def submodule_findings(root: Path = ROOT) -> list[str]:
    checkout = root / "gptp-processor"
    if not checkout.is_dir():
        return ["gptp-processor: checkout is missing"]
    try:
        head = subprocess.run(
            ["git", "-C", str(checkout), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        pin = gitlink_pin()
    except (OSError, subprocess.CalledProcessError, ValueError) as error:
        return [f"gptp-processor: cannot verify checkout: {error}"]
    findings = []
    if head != pin:
        findings.append(f"gptp-processor: checkout {head} differs from pin {pin}")
    findings.extend(
        f"gptp-processor/{relative}: required donor documentation is missing"
        for relative in SUBMODULE_DOCS
        if not (checkout / relative).is_file()
    )
    return findings


def selftest() -> int:
    arms = 0
    arms += 1
    if token_findings("fixture", "alpha beta", ("alpha", "beta")):
        print("gPTP docs selftest: valid token fixture failed")
        return 1
    arms += 1
    if not token_findings("fixture", "alpha", ("alpha", "beta")):
        print("gPTP docs selftest: missing token escaped")
        return 1
    arms += 1
    nested = {"signal": [{"name": "accepted MAC SOF"}], "data": [2]}
    flattened = "\n".join(flatten_json(nested))
    if "accepted MAC SOF" not in flattened or "2" not in flattened:
        print("gPTP docs selftest: JSON flattening failed")
        return 1
    if wavedrom_findings():
        print("gPTP docs selftest: production WaveDrom precondition failed")
        return 1
    arms += 1
    mutated = WAVEDROM.read_text(encoding="utf-8").replace(
        WAVEDROM_TOKENS[0], "missing", 1
    )
    if not wavedrom_value_findings(json.loads(mutated), "fixture"):
        print("gPTP docs selftest: WaveDrom token mutation escaped")
        return 1
    arms += 1
    reordered = json.loads(WAVEDROM.read_text(encoding="utf-8"))
    signals = named_waves(reordered)
    tuple_wave = signals["returned tuple"][0]
    eof_wave = signals["accepted MAC EOF"][0]
    for group in reordered["signal"]:
        if not isinstance(group, list):
            continue
        for signal in group:
            if not isinstance(signal, dict):
                continue
            if signal.get("name") == "returned tuple":
                signal["wave"] = eof_wave
            elif signal.get("name") == "accepted MAC EOF":
                signal["wave"] = tuple_wave
    order_findings = wavedrom_value_findings(reordered, "fixture")
    if not any("must precede" in finding for finding in order_findings):
        print("gPTP docs selftest: WaveDrom order mutation escaped")
        return 1
    arms += 1
    if file_token_findings(ROOT, DOCUMENT_TOKENS):
        print("gPTP docs selftest: production documents failed")
        return 1
    if manager_status_findings():
        print("gPTP docs selftest: manager status precondition failed")
        return 1
    arms += 1
    manager = MANAGER.read_text(encoding="utf-8")
    wrong_manager = manager.replace(
        "| Media clock selection | Implemented | Feature-status ledger |",
        "| Media clock selection | Missing | Feature-status ledger |",
        1,
    )
    if wrong_manager == manager or not manager_status_findings(wrong_manager):
        print("gPTP docs selftest: manager-status mutation escaped")
        return 1
    arms += 1
    wrong_risk = manager.replace(
        "Issue #74 media-clock bench acceptance remains open.",
        "Media clock selection remains unconsumed.",
        1,
    )
    if wrong_risk == manager or not manager_status_findings(wrong_risk):
        print("gPTP docs selftest: manager-risk mutation escaped")
        return 1
    arms += 1
    if file_token_findings(ROOT, SOURCE_TOKENS):
        print("gPTP docs selftest: source evidence failed")
        return 1
    print(f"gPTP documentation selftest: OK ({arms} controls)")
    return 0


def main() -> int:
    if sys.argv[1:] == ["--selftest"]:
        return selftest()
    with_submodule = sys.argv[1:] == ["--with-submodule"]
    if sys.argv[1:] not in ([], ["--with-submodule"]):
        print("usage: check_gptp_docs.py [--selftest|--with-submodule]")
        return 2
    findings = file_token_findings(ROOT, DOCUMENT_TOKENS)
    findings.extend(manager_status_findings())
    findings.extend(file_token_findings(ROOT, SOURCE_TOKENS))
    findings.extend(wavedrom_findings())
    if with_submodule:
        findings.extend(submodule_findings())
    if findings:
        for finding in findings:
            print(finding)
        print(f"gPTP documentation: FAIL ({len(findings)} findings)")
        return 1
    suffix = ", donor checkout verified" if with_submodule else ""
    print(
        f"gPTP documentation: OK ({len(DOCUMENT_TOKENS)} current pages{suffix})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
