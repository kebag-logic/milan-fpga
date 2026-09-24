#!/usr/bin/env python3
"""Disposable probe: does the end-station builder refuse a planted gPTP asymmetry key?

Usage: probe_builder_asym_refusal.py <repo-root> <scratch-dir>

Copies the shipping AX7101 configuration into <scratch-dir>, loads the
unmodified copy as a control (must load), then plants each candidate key under
the `gptp` section and requires load_config() to raise ConfigError naming that
key. Writes nothing inside <repo-root>. Exit 0 = every arm behaved as expected.
"""
import copy
import os
import sys

import yaml


def main() -> int:
    repo, scratch = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    os.makedirs(scratch, exist_ok=True)
    sys.path.insert(0, os.path.join(repo, "sw", "builder"))
    os.chdir(repo)
    import endstation_builder as eb  # noqa: E402

    src = os.path.join(repo, "configs", "endstation_ax7101_1x1_tdm8.yaml")
    with open(src, encoding="utf-8") as fh:
        base = yaml.safe_load(fh)
    if not isinstance(base.get("gptp"), dict):
        print("SETUP-FAIL: shipping config has no gptp mapping")
        return 2

    failures = 0

    def write(cfg, name):
        path = os.path.join(scratch, name)
        with open(path, "w", encoding="utf-8") as fh:
            yaml.safe_dump(cfg, fh, sort_keys=False)
        return path

    ctl = write(base, "control.yaml")
    try:
        eb.load_config(ctl)
        print("CONTROL PASS: unmodified shipping config loads")
    except Exception as exc:  # the control must load, or the arms prove nothing
        print(f"CONTROL FAIL: unmodified config raised {type(exc).__name__}: {exc}")
        return 2

    for key, val in (("delay_asymmetry_ns", 100), ("delayAsymmetry", -100),
                     ("asymmetry_ns", 0), ("delay_asymmetry", 1)):
        cfg = copy.deepcopy(base)
        cfg["gptp"][key] = val
        path = write(cfg, f"planted_{key}.yaml")
        try:
            eb.load_config(path)
            print(f"ARM FAIL: gptp.{key}={val} was ACCEPTED")
            failures += 1
        except eb.ConfigError as exc:
            if key in str(exc):
                print(f"ARM PASS: gptp.{key}={val} refused: {exc}")
            else:
                print(f"ARM FAIL: gptp.{key} refused for another reason: {exc}")
                failures += 1
    print(f"RESULT: {failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
