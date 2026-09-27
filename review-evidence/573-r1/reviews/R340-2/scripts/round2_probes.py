"""Round-2 reviewer probes: YAML scalar spellings of EUI-64 identities, the
pin/literal precedence, empty clock-source lists and other _eui64 users.

Each case writes raw YAML text (so quoting is exactly as shown) and records the
loader outcome and the resolved entity_model_id / stream_dmac_base.
Usage: python3 round2_probes.py <tree root> <output json>
"""
import json
from pathlib import Path
import re
import sys
import tempfile

import yaml

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "sw/builder"))
import endstation_builder as eb  # noqa: E402


def template(pin: bool) -> str:
    """arty_current (no vendor_oui) with one line set to a placeholder."""
    raw = yaml.safe_load((ROOT / "configs/endstation_arty_current.yaml").read_text())
    raw["entity"].pop("model_id_pin", None)
    raw["entity"]["entity_model_id"] = "LITERAL_SLOT"
    if pin:
        raw["entity"]["entity_model_id"] = "hash-derived"
        raw["entity"]["model_id_pin"] = "LITERAL_SLOT"
    return yaml.safe_dump(raw)


def load_text(text, directory):
    path = directory / "case.yaml"
    path.write_text(text)
    try:
        cfg = eb.load_config(path)
    except eb.ConfigError as exc:
        return dict(loader="refused", reason=str(exc)[:220])
    except Exception as exc:  # noqa: BLE001
        return dict(loader=f"crashed:{type(exc).__name__}", reason=str(exc)[:220])
    return dict(loader="accepted", entity_model_id=cfg["entity"]["entity_model_id"],
                stream_dmac_base=cfg["srp"].get("stream_dmac_base") if isinstance(cfg.get("srp"), dict) else None)


def id_case(label, spelling, pin, directory):
    text = template(pin).replace("LITERAL_SLOT", spelling)
    parsed = yaml.safe_load(text)["entity"]["model_id_pin" if pin else "entity_model_id"]
    row = dict(case=label, field="model_id_pin" if pin else "entity_model_id",
               yaml_text=spelling, yaml_type=type(parsed).__name__,
               yaml_value=hex(parsed) if type(parsed) is int else parsed)
    row.update(load_text(text, directory))
    written_hex = spelling.strip("'\"").replace("_", "")
    if row["loader"] == "accepted":
        written = int(written_hex, 16)
        row["written_as_hex"] = f"0x{written:016X}"
        row["resolved_equals_written_hex"] = row["entity_model_id"] == f"0x{written:016X}"
    return row


def raw_case(label, mutate, directory):
    raw = yaml.safe_load((ROOT / "configs/endstation_arty_current.yaml").read_text())
    mutate(raw)
    row = dict(case=label)
    row.update(load_text(yaml.safe_dump(raw), directory))
    return row


def text_case(label, pattern, replacement, directory):
    text = (ROOT / "configs/endstation_arty_current.yaml").read_text()
    new, count = re.subn(pattern, replacement, text, count=1, flags=re.M)
    row = dict(case=label, substitutions=count)
    row.update(load_text(new, directory))
    return row


def main() -> None:
    rows = []
    with tempfile.TemporaryDirectory(prefix="r340-2-probes-") as tmp:
        d = Path(tmp)
        for pin in (False, True):
            for label, spelling in (
                    ("prefixed hex, unquoted", "0x001BC50AC1000005"),
                    ("prefixed hex, quoted", '"0x001BC50AC1000005"'),
                    ("prefixed hex with underscores, unquoted", "0x001B_C50A_C100_0005"),
                    ("unprefixed hex with letters, unquoted", "001BC50AC1000005"),
                    ("unprefixed all-decimal-digit hex, quoted", '"1234567890123456"'),
                    ("unprefixed all-decimal-digit hex, unquoted", "1234567890123456"),
                    ("unprefixed 0-7 digits leading zero, quoted", '"0012345670123456"'),
                    ("unprefixed 0-7 digits leading zero, unquoted (YAML 1.1 octal)", "0012345670123456"),
                    ("unprefixed digits with 8/9 and leading zero, unquoted", "0012345678901234"),
                    ("decimal all-ones, unquoted", "18446744073709551615"),
                    ("bool, unquoted", "true")):
                rows.append(id_case(label, spelling, pin, d))
        rows.append(raw_case("malformed literal shadowed by legal pin",
                             lambda c: c["entity"].update(entity_model_id="not-hex"), d))
        rows.append(raw_case("all-ones literal shadowed by legal pin",
                             lambda c: c["entity"].update(entity_model_id="0xFFFFFFFFFFFFFFFF"), d))
        rows.append(raw_case("legal literal + legal pin (pin wins)",
                             lambda c: c["entity"].update(entity_model_id="0x001BC50000000009"), d))
        rows.append(text_case("stream_dmac_base unquoted prefixed hex",
                              r'stream_dmac_base: "0x91E0F000FE01"', "stream_dmac_base: 0x91E0F000FE01", d))
        rows.append(text_case("media_clock_sources null (empty key)",
                              r"^(\s*)media_clock_sources:.*$", r"\1media_clock_sources:", d))
        rows.append(raw_case("media_clock_sources [] + crf_output enabled",
                             lambda c: c["clocking"].update(media_clock_sources=[],
                                                            crf_output={"enabled": True}), d))
        rows.append(raw_case("media_clock_sources [internal] only",
                             lambda c: c["clocking"].update(media_clock_sources=["internal"],
                                                            default_source="internal", crf_sink=False), d))
        rows.append(raw_case("media_clock_sources empty string",
                             lambda c: c["clocking"].update(media_clock_sources=""), d))
    for r in rows:
        extra = r.get("reason") or r.get("entity_model_id") or ""
        eq = r.get("resolved_equals_written_hex", "")
        print(f"{r.get('field', ''):16} {r['case'][:62]:62} {r.get('yaml_type', ''):5} "
              f"{r['loader']:10} {str(eq):5} {extra[:120]}")
    Path(sys.argv[2]).write_text(json.dumps(rows, indent=1) + "\n")


if __name__ == "__main__":
    main()
