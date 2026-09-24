#!/usr/bin/env python3
"""Disposable probe: does the end-station builder refuse a planted gPTP
asymmetry key?

Usage: python3 -B probe_builder_asym_key.py <repo-root> <scratch-dir>

Copies the shipping configuration into <scratch-dir>, plants one candidate
asymmetry key under `gptp:` per case, and calls the builder's own
load_config() on the copy. The unmodified copy is loaded first as the
positive control (it must load); every planted case must raise the builder's
ConfigError naming the planted key. Nothing in <repo-root> is written.
Exit 0 when every expectation holds, 1 otherwise.
"""
import importlib.util
import os
import shutil
import sys

KEYS = ["delay_asymmetry", "delay_asymmetry_ns", "asymmetry_ns",
        "delayAsymmetry"]
CONFIG = "configs/endstation_ax7101_1x1_tdm8.yaml"


def load_builder(root):
    path = os.path.join(root, "sw", "builder", "endstation_builder.py")
    sys.path.insert(0, os.path.dirname(path))
    spec = importlib.util.spec_from_file_location("endstation_builder", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def plant(src_text, key):
    lines = src_text.splitlines(keepends=True)
    out, done = [], False
    for line in lines:
        out.append(line)
        if not done and line.rstrip("\n") == "gptp:":
            out.append(f"  {key}: 0\n")
            done = True
    if not done:
        raise SystemExit("probe setup error: no top-level 'gptp:' line")
    return "".join(out)


def main():
    root, scratch = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    os.makedirs(scratch, exist_ok=True)
    b = load_builder(root)
    src = os.path.join(root, CONFIG)
    with open(src, encoding="utf-8") as f:
        text = f.read()
    ok = True

    ctrl = os.path.join(scratch, "control.yaml")
    shutil.copyfile(src, ctrl)
    cwd = os.getcwd()
    os.chdir(root)
    try:
        try:
            b.load_config(ctrl)
            print(f"CONTROL  unmodified copy loads: PASS")
        except Exception as e:  # noqa: BLE001 - the probe reports any failure
            print(f"CONTROL  unmodified copy failed to load: FAIL "
                  f"({type(e).__name__}: {e})")
            ok = False
        for key in KEYS:
            p = os.path.join(scratch, f"planted_{key}.yaml")
            with open(p, "w", encoding="utf-8") as f:
                f.write(plant(text, key))
            try:
                b.load_config(p)
                print(f"PLANT    gptp.{key}: ACCEPTED -> FAIL")
                ok = False
            except b.ConfigError as e:
                msg = str(e)
                named = key in msg and "unknown keys" in msg
                print(f"PLANT    gptp.{key}: refused "
                      f"({'names key' if named else 'does NOT name key'}) "
                      f"-> {'PASS' if named else 'FAIL'}")
                print(f"         message: {msg[:160]}")
                ok = ok and named
    finally:
        os.chdir(cwd)
    print("RESULT", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
