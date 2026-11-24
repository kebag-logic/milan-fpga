#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Check retention refusal and the derived capture-stamp error budget."""
import argparse
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent


def main() -> None:
    """Run the bound controls and refusals, writing results under --output."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    results = []
    for shape, first, count, lead in [(1, 8, 8, 2), (8, 1, 63, 1)]:
        work = out / str(shape)
        base = ["make", "-s", "-C", str(HERE), "run", "VERILATOR_JOBS=4",
                f"STREAMS={shape}", f"FIRST={first}", f"CHANNELS={count}", f"MDIR={work}"]
        runs = [("control", base + [f"LEAD={lead}"], {}, "pass"),
                ("inside", [str(work / "Vinput_loopback")], {"STAMP_PPM": "1000", "STAMP_JITTER_NS": "84"}, "pass"),
                ("outside", [str(work / "Vinput_loopback")], {"STAMP_PPM": "1000", "STAMP_JITTER_NS": "87"}, "sample"),
                ("lead3", base + ["LEAD=3", f"MDIR={work}-lead3"], {}, "refuse")]
        for name, command, extra, expectation in runs:
            log = out / f"{shape}-{name}.log"
            with log.open("w") as sink:
                result = subprocess.run(command, env=dict(os.environ, **extra), stdout=sink,
                                        stderr=subprocess.STDOUT, timeout=3600)
            text = log.read_text()
            passed = ((result.returncode == 0 and "PASS input-loopback" in text) if expectation == "pass" else
                      (result.returncode != 0 and "FAIL COPY_SAMPLE" in text) if expectation == "sample" else
                      (result.returncode != 0 and "USERERROR" in text and "KMIN_C <= 2" in text
                       and not Path(str(work) + "-lead3/Vinput_loopback").exists()))
            results.append(dict(shape=shape, case=name, command=command, environment=extra,
                                exit=result.returncode, passed=passed))
            (out / "results.json").write_text(json.dumps(results, indent=2) + "\n")
            print(shape, name, "PASS" if passed else "FAIL", flush=True)
            if not passed:
                raise SystemExit(1)


if __name__ == "__main__":
    main()
