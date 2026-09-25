# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Emit declaration-test headers from a committed fixture and the real builder.

The optional emitter VID changes the normalized test input only. Shipping
validation still requires VID 2; a distinct test value exposes dropped bindings.
The harness expectations live independently in the suite recipes.
"""

import argparse
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "sw" / "builder"))
import endstation_builder as eb  # noqa: E402


def merge_overrides(config: dict, overrides: dict) -> None:
    """Apply the fixture's explicit leaf overrides to its base configuration."""
    for key, value in overrides.items():
        if isinstance(value, dict):
            merge_overrides(config.setdefault(key, {}), value)
        else:
            config[key] = value


def main() -> None:
    """Validate the fixture, then emit both headers with the builder."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path)
    parser.add_argument("outdir", type=Path)
    args = parser.parse_args()
    fixture = yaml.safe_load(args.fixture.read_text())
    raw = yaml.safe_load((ROOT / fixture["base"]).read_text())
    merge_overrides(raw, fixture.get("overrides", {}))
    args.outdir.mkdir(parents=True, exist_ok=True)
    config_path = args.outdir / "config.yaml"
    config_path.write_text(yaml.safe_dump(raw, sort_keys=False))
    cfg = eb.load_config(str(config_path))
    if "emitter_srp_vid" in fixture:
        vid = fixture["emitter_srp_vid"]
        assert type(vid) is int and 1 <= vid <= 4094 and vid != 2
        cfg["srp"]["vid"] = vid
    (args.outdir / "gen").mkdir(exist_ok=True)
    (args.outdir / "gen/adp_shape_defaults.svh").write_text(eb.emit_adp_shape_svh(cfg))
    (args.outdir / "gen/lwsrp_csr_defaults.svh").write_text(eb.emit_csr_defaults_svh(cfg))
    print(f"declaration fixture: {args.fixture.name}")


if __name__ == "__main__":
    main()
