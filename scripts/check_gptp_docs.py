#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Check current fabric-gPTP routing and source evidence."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WAVEDROM = ROOT / "docs" / "diagrams" / "wd_gptp_pdelay.json"
MANAGER = ROOT / "docs" / "guides" / "gptp" / "MANAGER.md"
FEATURE_STATUS = ROOT / "docs" / "reference" / "milan_feature_status.json"
DONOR_BLOB_ROOT = "https://github.com/Mister-M-alt/FPGA-gPTP/blob"
DONOR_RAW_ROOT = "https://raw.githubusercontent.com/Mister-M-alt/FPGA-gPTP"
MARKDOWN_TARGET_RE = re.compile(
    r"!?\[[^\]\n]*\]\((?:<([^>\n]+)>|([^\s)]+))"
)
MARKDOWN_REFERENCE_TARGET_RE = re.compile(
    r"^[ \t]{0,3}\[[^\]\n]+\]:[ \t]*(?:<([^>\n]+)>|([^\s]+))",
    re.MULTILINE,
)
MARKDOWN_AUTOLINK_RE = re.compile(r"<(https?://[^>\s]+)>")

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
    "accepted tap EOF",
    "frame FIFO commit",
    "engine RX SOF",
    "68-byte Pdelay_Resp",
    "nine accepted 64-bit beats",
    "sequence plus message type",
)

# KL_gptp_txstamp captures sequenceId on accepted beat 5 and raises its
# registered tuple before a normal Pdelay frame reaches tx_tlast_i. This order
# is the interface contract; labels alone cannot prove it.
WAVEDROM_ORDER = (
    ("accepted MAC SOF", "accepted sequence beat 5"),
    ("accepted sequence beat 5", "returned tuple"),
    ("returned tuple", "accepted MAC EOF"),
    ("accepted tap SOF", "accepted tap EOF"),
    ("accepted tap EOF", "frame FIFO commit"),
    ("frame FIFO commit", "engine RX SOF"),
)

# The published diagram is explicitly the unstalled 64-bit parent path. A
# 68-byte Pdelay_Resp occupies nine accepted beats, hence eight cycle intervals
# from the accepted SOF beat to the accepted EOF beat. axis_fifo commits on the
# following cycle; its default one-stage RAM pipeline and the shadow serializer
# then put engine SOF two cycles after the visible commit pulse.
WAVEDROM_SAME_CYCLE = (
    ("accepted MAC SOF", "TX PHC capture"),
    ("accepted tap SOF", "RX PHC capture"),
)
WAVEDROM_EXACT_DELTA = (
    ("accepted tap SOF", "accepted tap EOF", 8),
    ("accepted tap EOF", "frame FIFO commit", 1),
    ("frame FIFO commit", "engine RX SOF", 2),
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
    """One finding per required token that `text` does not contain."""
    return [f"{path}: missing token: {token}" for token in tokens if token not in text]


def file_token_findings(root: Path, mapping: dict[str, tuple[str, ...]]) -> list[str]:
    """Token findings for every file of `mapping`, missing files included."""
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


def markdown_targets(text: str) -> list[str]:
    """Return inline, reference-style and autolink Markdown destinations."""
    targets = [
        match.group(1) or match.group(2)
        for match in MARKDOWN_TARGET_RE.finditer(text)
    ]
    targets.extend(
        match.group(1) or match.group(2)
        for match in MARKDOWN_REFERENCE_TARGET_RE.finditer(text)
    )
    targets.extend(match.group(1) for match in MARKDOWN_AUTOLINK_RE.finditer(text))
    return list(dict.fromkeys(targets))


def donor_target_findings(
    document: Path,
    target: str,
    pin: str,
    *,
    root: Path = ROOT,
    checkout: Path | None = None,
) -> list[str]:
    """Reject unpublished gitlink children and drifted donor deep links."""
    try:
        label = document.relative_to(root).as_posix()
    except ValueError:
        label = document.as_posix()
    destination = re.split(r"[?#]", target, maxsplit=1)[0]
    if not destination:
        return []

    # GitHub publishes the gitlink itself, but it does not publish a relative
    # child such as gptp-processor/docs/MANAGER.md. Those links work in a
    # populated checkout and 404 in the rendered repository documentation.
    if (
        not destination.startswith("/")
        and not re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", destination)
    ):
        try:
            relative = (document.parent / destination).resolve().relative_to(root)
        except ValueError:
            return []
        if (
            len(relative.parts) > 1
            and relative.parts[0] == "gptp-processor"
        ):
            return [
                f"{label}: relative donor deep link is not published by GitHub: "
                f"{target}"
            ]
        return []

    for prefix in (DONOR_BLOB_ROOT, DONOR_RAW_ROOT):
        marker = prefix + "/"
        if not destination.startswith(marker):
            continue
        suffix = destination[len(marker):]
        linked_pin, separator, donor_path = suffix.partition("/")
        if linked_pin != pin:
            return [
                f"{label}: donor deep link must use gitlink {pin}, found "
                f"{linked_pin or '<empty>'}: {target}"
            ]
        if not separator or not donor_path:
            return [f"{label}: donor deep link has no path: {target}"]
        if checkout is not None and not (checkout / donor_path).is_file():
            return [
                f"{label}: pinned donor target is missing from checkout: "
                f"gptp-processor/{donor_path}"
            ]
        return []
    return []


def donor_link_findings(
    pin: str,
    *,
    root: Path = ROOT,
    checkout: Path | None = None,
) -> list[str]:
    """Check every current documentation link into the donor repository."""
    findings: list[str] = []
    for document in sorted((root / "docs").rglob("*.md")):
        relative = document.relative_to(root)
        if "history" in relative.parts:
            continue
        try:
            targets = markdown_targets(document.read_text(encoding="utf-8"))
        except OSError as error:
            findings.append(f"{relative.as_posix()}: cannot read links: {error}")
            continue
        for target in targets:
            findings.extend(
                donor_target_findings(
                    document, target, pin, root=root, checkout=checkout
                )
            )
    return findings


def flatten_json(value: object) -> list[str]:
    """Every scalar of a parsed JSON document, as text, in document order."""
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
    """Label, order, same-cycle and exact-interval findings for one parsed
    WaveDrom document; `label` names it in each finding."""
    findings = token_findings(label, "\n".join(flatten_json(value)), WAVEDROM_TOKENS)
    waves = named_waves(value)
    cycles: dict[str, int] = {}
    ordered_names = {name for pair in WAVEDROM_ORDER for name in pair}
    ordered_names.update(name for pair in WAVEDROM_SAME_CYCLE for name in pair)
    ordered_names.update(
        name for before, after, _ in WAVEDROM_EXACT_DELTA
        for name in (before, after)
    )
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
    for event, capture in WAVEDROM_SAME_CYCLE:
        if event in cycles and capture in cycles and cycles[event] != cycles[capture]:
            findings.append(
                f"{label}: {event!r} and {capture!r} must occur in the same "
                f"cycle; cycles are {cycles[event]} and {cycles[capture]}"
            )
    for before, after, expected in WAVEDROM_EXACT_DELTA:
        if before in cycles and after in cycles:
            actual = cycles[after] - cycles[before]
            if actual != expected:
                findings.append(
                    f"{label}: {before!r} to {after!r} must be exactly "
                    f"{expected} cycles on the unstalled path, found {actual}"
                )
    return findings


def wavedrom_findings(path: Path = WAVEDROM) -> list[str]:
    """The findings of the production Pdelay WaveDrom, or one for an unreadable file."""
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
    """The exact gptp-processor gitlink at stage zero, read from the index."""
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
    """Findings for a donor checkout that is absent, off-pin, or missing a page."""
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


class SelftestFailure(Exception):
    """One fixture arm did not bite; the message names which."""


def move_event(value: object, name: str, cycle: int) -> int:
    """Move the single asserted event of every signal named `name` to `cycle`
    inside a parsed WaveDrom document; returns how many signals moved."""
    moved = 0
    if isinstance(value, dict):
        if value.get("name") == name and isinstance(value.get("wave"), str):
            symbols = list(value["wave"])
            if cycle >= len(symbols):
                raise ValueError(f"cycle {cycle} is outside {name!r}")
            symbols = ["." if symbol == "1" else symbol for symbol in symbols]
            symbols[cycle] = "1"
            value["wave"] = "".join(symbols)
            moved += 1
        children = value.values()
    elif isinstance(value, list):
        children = value
    else:
        children = ()
    return moved + sum(move_event(child, name, cycle) for child in children)


def link_selftest(pin: str) -> int:
    """The donor-link arms: target parsing, an unpublished gitlink child, a
    stale pin, valid pinned forms, a missing pinned target and production."""
    parsed_targets = markdown_targets(
        "[guide](../gptp-processor/docs/MANAGER.md) "
        "![wave](https://example.invalid/wave.svg)\n"
        "[source]: ../gptp-processor/docs/SOURCE_EVIDENCE.md\n"
        "<https://example.invalid/auto>"
    )
    if parsed_targets != [
        "../gptp-processor/docs/MANAGER.md",
        "https://example.invalid/wave.svg",
        "../gptp-processor/docs/SOURCE_EVIDENCE.md",
        "https://example.invalid/auto",
    ]:
        raise SelftestFailure("Markdown target parsing failed")
    fixture_document = ROOT / "docs" / "fixture.md"
    if not donor_target_findings(
        fixture_document,
        "../gptp-processor/docs/MANAGER.md",
        pin,
    ):
        raise SelftestFailure("relative donor deep link escaped")
    stale = "0" * 40 if pin != "0" * 40 else "1" * 40
    stale_target = f"{DONOR_BLOB_ROOT}/{stale}/docs/MANAGER.md"
    if not donor_target_findings(fixture_document, stale_target, pin):
        raise SelftestFailure("stale donor pin escaped")
    valid_targets = (
        f"{DONOR_BLOB_ROOT}/{pin}/docs/MANAGER.md",
        f"{DONOR_RAW_ROOT}/{pin}/docs/diagrams/wavedrom/rx_accept.svg",
    )
    if any(
        donor_target_findings(fixture_document, target, pin)
        for target in valid_targets
    ):
        raise SelftestFailure("valid pinned donor URL failed")
    missing_target = f"{DONOR_BLOB_ROOT}/{pin}/definitely-not-present.md"
    if not donor_target_findings(
        fixture_document, missing_target, pin, checkout=ROOT
    ):
        raise SelftestFailure("missing pinned donor target escaped")
    if donor_link_findings(pin):
        raise SelftestFailure("production donor links failed")
    return 6


def token_selftest() -> int:
    """The token arms: a complete fixture passes, a missing token is found."""
    if token_findings("fixture", "alpha beta", ("alpha", "beta")):
        raise SelftestFailure("valid token fixture failed")
    if not token_findings("fixture", "alpha", ("alpha", "beta")):
        raise SelftestFailure("missing token escaped")
    return 2


def wavedrom_selftest() -> int:
    """The timing arms: flattening, a removed label, swapped egress order,
    reversed ingress order, a short ingress frame and a displaced capture."""
    nested = {"signal": [{"name": "accepted MAC SOF"}], "data": [2]}
    flattened = "\n".join(flatten_json(nested))
    if "accepted MAC SOF" not in flattened or "2" not in flattened:
        raise SelftestFailure("JSON flattening failed")
    if wavedrom_findings():
        raise SelftestFailure("production WaveDrom precondition failed")
    production = WAVEDROM.read_text(encoding="utf-8")
    mutated = production.replace(WAVEDROM_TOKENS[0], "missing", 1)
    if not wavedrom_value_findings(json.loads(mutated), "fixture"):
        raise SelftestFailure("WaveDrom token mutation escaped")
    reordered = json.loads(production)
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
        raise SelftestFailure("WaveDrom order mutation escaped")
    ingress_reordered = json.loads(production)
    ingress_signals = named_waves(ingress_reordered)
    tap_eof_wave = ingress_signals["accepted tap EOF"][0]
    commit_wave = ingress_signals["frame FIFO commit"][0]
    if (
        move_event(ingress_reordered, "accepted tap EOF", commit_wave.index("1"))
        != 1
        or move_event(
            ingress_reordered, "frame FIFO commit", tap_eof_wave.index("1")
        )
        != 1
    ):
        raise SelftestFailure("ingress fixture drift")
    ingress_findings = wavedrom_value_findings(ingress_reordered, "fixture")
    if not any("must precede" in finding for finding in ingress_findings):
        raise SelftestFailure("ingress commit-order mutation escaped")
    shortened = json.loads(production)
    tap_sof_cycle = named_waves(shortened)["accepted tap SOF"][0].index("1")
    if move_event(shortened, "accepted tap EOF", tap_sof_cycle + 2) != 1:
        raise SelftestFailure("ingress interval fixture drift")
    interval_findings = wavedrom_value_findings(shortened, "fixture")
    if not any("must be exactly 8 cycles" in finding for finding in interval_findings):
        raise SelftestFailure("short ingress frame mutation escaped")
    displaced_capture = json.loads(production)
    if move_event(displaced_capture, "RX PHC capture", tap_sof_cycle + 1) != 1:
        raise SelftestFailure("capture fixture drift")
    capture_findings = wavedrom_value_findings(displaced_capture, "fixture")
    if not any("must occur in the same cycle" in finding
               for finding in capture_findings):
        raise SelftestFailure("displaced capture mutation escaped")
    return 6


def document_selftest() -> int:
    """The page arms: production pages and source pass, and both manager
    contradictions - a wrong status row, a retired risk sentence - are found."""
    if file_token_findings(ROOT, DOCUMENT_TOKENS):
        raise SelftestFailure("production documents failed")
    if manager_status_findings():
        raise SelftestFailure("manager status precondition failed")
    manager = MANAGER.read_text(encoding="utf-8")
    wrong_manager = manager.replace(
        "| Media clock selection | Implemented | Feature-status ledger |",
        "| Media clock selection | Missing | Feature-status ledger |",
        1,
    )
    if wrong_manager == manager or not manager_status_findings(wrong_manager):
        raise SelftestFailure("manager-status mutation escaped")
    wrong_risk = manager.replace(
        "Issue #74 media-clock bench acceptance remains open.",
        "Media clock selection remains unconsumed.",
        1,
    )
    if wrong_risk == manager or not manager_status_findings(wrong_risk):
        raise SelftestFailure("manager-risk mutation escaped")
    if file_token_findings(ROOT, SOURCE_TOKENS):
        raise SelftestFailure("source evidence failed")
    return 4


def selftest() -> int:
    """Run every fixture arm against the production gitlink; 1 names the first
    arm that did not bite."""
    try:
        pin = gitlink_pin()
    except (OSError, subprocess.CalledProcessError, ValueError) as error:
        print(f"gPTP docs selftest: cannot read production gitlink: {error}")
        return 1
    try:
        arms = (
            link_selftest(pin)
            + token_selftest()
            + wavedrom_selftest()
            + document_selftest()
        )
    except SelftestFailure as failure:
        print(f"gPTP docs selftest: {failure}")
        return 1
    print(f"gPTP documentation selftest: OK ({arms} controls)")
    return 0


def main() -> int:
    """Check the current pages; --selftest runs the arms, --with-submodule the checkout."""
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
    try:
        pin = gitlink_pin()
    except (OSError, subprocess.CalledProcessError, ValueError) as error:
        findings.append(f"gptp-processor: cannot read gitlink for links: {error}")
    else:
        checkout = ROOT / "gptp-processor" if with_submodule else None
        findings.extend(donor_link_findings(pin, checkout=checkout))
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
