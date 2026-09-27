"""Round-3 reviewer probes: the quoted-string rule for every 64-bit hex key
read through _eui64/_fmt64, edge spellings Python's int(v, 16) tolerates,
explicit null keys, and the be32 u32 range.

Each case writes raw YAML text (quoting exactly as shown) into a copy of a
tracked configuration and records the loader outcome and resolved value.
Usage: python3 round3_probes.py <tree root> <output json>
"""
import json
from pathlib import Path
import sys
import tempfile

import yaml

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "sw/builder"))
sys.path.insert(0, str(ROOT / "avdecc"))
import endstation_builder as eb  # noqa: E402

BASE = "configs/endstation_arty_4x4.yaml"

# field label, key path, resolver of the loaded value, legal written hex
FIELDS = (
    ("entity.entity_model_id", ("entity", "entity_model_id"),
     lambda c: c["entity"]["entity_model_id"], "0x001BC50AC1000005"),
    ("entity.model_id_pin", ("entity", "model_id_pin"),
     lambda c: c["entity"]["entity_model_id"], "0x001BC50AC1000005"),
    ("entity.entity_id", ("entity", "entity_id"),
     lambda c: c["entity"]["entity_id"], "0x001BC50AC1000005"),
    ("srp.stream_dmac_base", ("srp", "stream_dmac_base"),
     lambda c: f"0x{int(c['srp']['stream_dmac_base'], 16):012X}", "0x91E0F000FE01"),
    ("streams.talkers[0].formats", ("streams", "talkers", 0, "formats", 0),
     lambda c: c["talkers"][0]["formats"][0], "0x0205022000806000"),
    ("streams.listeners[0].formats", ("streams", "listeners", 0, "formats", 0),
     lambda c: c["listeners"][0]["formats"][0], "0x0205022000806000"),
    ("clocking.crf_format", ("clocking", "crf_format"),
     lambda c: c["clocking"].get("crf_format"), "0x041060010000BB80"),
    ("clocking.crf_output.format", ("clocking", "crf_output", "format"),
     lambda c: c["clocking"].get("crf_output_format"), "0x041060010000BB80"),
)


def template(keys):
    raw = yaml.safe_load((ROOT / BASE).read_text())
    raw["entity"].pop("model_id_pin", None)
    raw["entity"].pop("vendor_oui", None)
    for direction in ("talkers", "listeners"):
        raw["streams"][direction][0]["formats"] = ["0x0205022000806000"]
    raw.setdefault("srp", {})
    node = raw
    for key in keys[:-1]:
        node = node.setdefault(key, {}) if isinstance(key, str) else node[key]
    node[keys[-1]] = "HEX_SLOT"
    text = yaml.safe_dump(raw)
    assert text.count("HEX_SLOT") == 1
    return text


def load(text, directory, resolve):
    path = directory / "case.yaml"
    path.write_text(text)
    try:
        cfg = eb.load_config(path)
    except eb.ConfigError as exc:
        return dict(loader="refused", reason=str(exc)[:200])
    except Exception as exc:  # noqa: BLE001
        return dict(loader=f"crashed:{type(exc).__name__}", reason=str(exc)[:200])
    try:
        value = resolve(cfg)
    except Exception as exc:  # noqa: BLE001
        value = f"unresolved:{type(exc).__name__}"
    return dict(loader="accepted", resolved=value)


def main() -> None:
    rows = []
    with tempfile.TemporaryDirectory(prefix="r340-3-probes-") as tmp:
        d = Path(tmp)
        for field, keys, resolve, legal in FIELDS:
            text = template(keys)
            digits = legal.removeprefix("0x")
            spellings = [
                ("quoted prefixed", f'"{legal}"', "accept"),
                ("quoted unprefixed", f'"{digits}"', "accept"),
                ("quoted with underscores", f'"0x{digits[:4]}_{digits[4:]}"', "accept"),
                ("unquoted prefixed", legal, "quote"),
                ("unquoted 1234567890123456", "1234567890123456", "quote"),
                ("unquoted 0012345670123456 (YAML 1.1 octal)", "0012345670123456", "quote"),
                ("unquoted legal digits as octal-looking", "0" + "1" * (len(digits) - 1), "quote"),
                ("unquoted true", "true", "quote"),
                ("explicit null", "null", "quote"),
                ("empty value", "", "quote"),
                ("unquoted float", "1.5", "quote"),
                ("flow list", "[]", "quote"),
                ("flow map", "{}", "quote"),
                ("quoted empty string", '""', "refuse"),
                ("quoted 0x only", '"0x"', "refuse"),
                ("quoted negative", '"-0x1"', "refuse"),
                # Python int(v, 16) leniencies: value-preserving, recorded only
                ("quoted leading plus", f'"+{legal}"', "record"),
                ("quoted surrounding spaces", f'" {legal} "', "record"),
                ("quoted uppercase 0X", f'"0X{digits}"', "record"),
                ("quoted fullwidth digits", '"' + "".join(
                    chr(0xFF10 + int(ch)) if ch.isdigit() else ch for ch in digits) + '"', "record"),
            ]
            for label, spelling, expect in spellings:
                row = dict(field=field, case=label, yaml_text=spelling, expect=expect)
                row.update(load(text.replace("HEX_SLOT", spelling), d, resolve))
                if expect == "accept":
                    row["ok"] = row["loader"] == "accepted" and row["resolved"] == legal
                elif expect == "quote":
                    row["ok"] = (row["loader"] == "refused" and field in row["reason"]
                                 and "quote" in row["reason"])
                elif expect == "refuse":
                    row["ok"] = row["loader"] == "refused"
                else:
                    row["ok"] = None
                rows.append(row)
        # the literal all-decimal spelling of an identity resolves to written hex
        for field, keys, resolve, _legal in FIELDS[:3]:
            row = dict(field=field, case="quoted 1234567890123456", expect="accept")
            row.update(load(template(keys).replace("HEX_SLOT", '"1234567890123456"'), d, resolve))
            row["ok"] = row["loader"] == "accepted" and row["resolved"] == "0x1234567890123456"
            rows.append(row)
        # formats given as a scalar instead of a list (pre-existing structure path)
        for label, spelling in (("formats unquoted int scalar", "0x0205022000806000"),
                                ("formats quoted string scalar", '"0x0205022000806000"')):
            text = template(("streams", "talkers", 0, "formats")).replace("HEX_SLOT", spelling)
            row = dict(field="streams.talkers[0].formats", case=label, expect="record")
            row.update(load(text, d, lambda c: c["talkers"][0]["formats"]))
            row["ok"] = None
            rows.append(row)
    # be32 range
    from aem_descriptors import be32
    for value in (0, 1, 0xFFFFFFFF, -1, 1 << 32, (1 << 32) + 2125999, True):
        try:
            out = be32(value).hex()
        except Exception as exc:  # noqa: BLE001
            out = f"raised:{type(exc).__name__}"
        legal = isinstance(value, int) and 0 <= value <= 0xFFFFFFFF
        rows.append(dict(field="aem_descriptors.be32", case=repr(value), result=out,
                         ok=(out == int(value).to_bytes(4, "big").hex()) if legal
                         else out.startswith("raised:")))
    bad = [r for r in rows if r.get("ok") is False]
    for r in rows:
        print(f"{str(r.get('ok')):5} {r['field'][:30]:30} {r['case'][:44]:44} "
              f"{r.get('loader', r.get('result', '')):10} "
              f"{str(r.get('reason') or r.get('resolved') or '')[:110]}")
    print(f"ROWS {len(rows)} FAILED {len(bad)}")
    Path(sys.argv[2]).write_text(json.dumps(rows, indent=1, default=str) + "\n")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
