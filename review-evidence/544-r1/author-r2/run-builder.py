from pathlib import Path
import argparse, json, runpy, subprocess, sys
from unittest.mock import patch

parser = argparse.ArgumentParser()
parser.add_argument("mode", choices=("sdk", "absent"))
parser.add_argument("--gate-only", action="store_true")
parser.add_argument("--tag", required=True)
args = parser.parse_args()
root = Path.cwd()
out = Path(__file__).resolve().parent
sys.path.insert(0, str(root / "sw/builder"))
import test_firmware_compiler as tfc
sdk = Path("$VALIDATION_STORAGE/504-manager-r1/sdk-install")
if args.mode == "sdk":
    tfc.sdk.verify(sdk)
with (out / (args.tag + "-argv.jsonl")).open("w") as f:
    audit = tfc.CompilerAudit(f, sdk if args.mode == "sdk" else None)
    # Full-bank host compilation is a separate, authorized instrument.
    # Only gate 1b must forbid it from acting as the firmware compiler.
    native_run = subprocess.run
    def mapped_run(argv, *positional, **keyword):
        if isinstance(argv, (list, tuple)) and str(argv[0]) in audit.cross:
            return audit.invoke(argv, **keyword)
        return native_run(argv, *positional, **keyword)
    sys.argv = ["sw/builder/test_builder.py"]
    if args.mode == "sdk":
        sys.argv.append("--require-rv32")
    with patch("subprocess.run", mapped_run):
        if args.gate_only:
            tfc.builder.test_baremetal_profile_contract()
        else:
            runpy.run_path("sw/builder/test_builder.py", run_name="__main__")
    print("AUDIT", json.dumps(dict(mode=args.mode, compiles=audit.compiles,
                                   hidden=sorted(audit.hidden))))
