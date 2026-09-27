"""Round-3 supplementary probes: the matrix's 47-entry loader row, the `maap`
selector under the string-only rule, and the (out-of-lane) MAC-48 parser that
is not read through _eui64. Usage: python3 round3_extra_probes.py <tree root>
"""
from pathlib import Path
import sys
import tempfile

import yaml

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "sw/builder"))
import endstation_builder as eb  # noqa: E402


def run(label, text):
    path = Path(tempfile.mkdtemp(prefix="r340-3-extra-")) / "case.yaml"
    path.write_text(text)
    try:
        cfg = eb.load_config(path)
    except eb.ConfigError as exc:
        print(f"{label}: refused: {str(exc)[:160]}")
        return None
    print(f"{label}: accepted")
    return cfg


base = yaml.safe_load((ROOT / "configs/endstation_arty_current.yaml").read_text())
for count in (46, 47):
    raw = yaml.safe_load(yaml.safe_dump(base))
    raw["streams"]["talkers"][0]["formats"] = ["0x0205022000806000"] * count
    run(f"{count} identical AAF output format entries", yaml.safe_dump(raw))

raw = yaml.safe_load(yaml.safe_dump(base))
raw.setdefault("srp", {})["stream_dmac_base"] = "maap"
cfg = run("srp.stream_dmac_base: maap", yaml.safe_dump(raw))
if cfg:
    print(f"  resolved stream_dmac_base {cfg['srp']['stream_dmac_base']}")

text = (ROOT / "configs/endstation_arty_current.yaml").read_text()
declared = base["platform"]["mac_address"]
print(f"tracked platform.mac_address {declared!r} ({type(declared).__name__})")
for spelling in ('"10:20:30:40:50:02"', "10:20:30:40:50:02", "0x000000F42402"):
    parsed = yaml.safe_load(f"k: {spelling}")["k"]
    new = text.replace(f'"{declared}"', spelling, 1) if f'"{declared}"' in text \
        else text.replace(str(declared), spelling, 1)
    cfg = run(f"platform.mac_address {spelling} (YAML {type(parsed).__name__} {parsed!r})", new)
    if cfg:
        mac = eb._mac48(cfg["platform"]["mac_address"], "mac")
        print(f"  resolved MAC 0x{mac:012X}")
