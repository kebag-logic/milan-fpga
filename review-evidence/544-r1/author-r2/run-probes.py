from pathlib import Path
import argparse, hashlib, json, os, subprocess
parser = argparse.ArgumentParser()
parser.add_argument("mode", choices=("sdk", "absent"))
parser.add_argument("--tag", required=True)
args = parser.parse_args()
out = Path(__file__).resolve().parent
scratch = Path((out / "scratch-path.txt").read_text().strip())
sdk = "$VALIDATION_STORAGE/504-manager-r1/sdk-install"
env = os.environ.copy()
env["PATH"] = "$VALIDATION_STORAGE/408-manager-r7/pinned-tool-bin:" + env["PATH"]
env["PYTHONDONTWRITEBYTECODE"] = "1"
env["PYTHONUNBUFFERED"] = "1"
results = []
for reviewer in ("R316-1", "R317-1"):
    for disconnected in (False, True):
        tag = args.tag + "-" + reviewer + ("-disconnected" if disconnected else "")
        if reviewer == "R316-1":
            command = ["python3", "-B", str(scratch / reviewer / "scripts/probe.py"),
                       args.mode, "--out", str(out / (tag + ".json")),
                       "--scratch", str(scratch / "runs")]
            if args.mode == "sdk":
                command += ["--sdk", sdk]
            if disconnected:
                command += ["--disable", "assert_preprocessed_identity_sample"
                            if args.mode == "sdk" else "assert_identity_macro_free"]
        else:
            command = ["python3", "-B", str(scratch / reviewer / "probe_gate1b.py"),
                       "--mode", args.mode, "--rev", "head", "--tag", tag,
                       "--outdir", str(out)]
            if args.mode == "sdk":
                command += ["--sdk", sdk]
            if disconnected:
                command += ["--disconnect"]
        with (out / (tag + ".log")).open("w") as f:
            result = subprocess.run(command, env=env, stdout=f, stderr=subprocess.STDOUT,
                                    timeout=3600)
        results.append(dict(tag=tag, command=command, rc=result.returncode))
        print(tag, result.returncode, flush=True)
        if result.returncode:
            print((out / (tag + ".log")).read_text()[-3000:], flush=True)
(out / (args.tag + "-probe-results.json")).write_text(json.dumps(results, indent=2) + "\n")
