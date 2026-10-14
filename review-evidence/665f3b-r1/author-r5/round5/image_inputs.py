"""Show that the dev side of the round 5 merge changes no firmware image input.

An image input is any production firmware source, header or link script under
sw/firmware/, the mailbox contract and its generator under sw/mailbox/, a
shape configuration under configs/, the tsn-c-stack gitlink, or one of the
image builders. Host tests and Markdown are not inputs. Planted controls add
one input of each kind to the dev change list and require each to be flagged.
"""
import argparse
import subprocess
from pathlib import Path

BASE = "d40e4e9827be2516f8f34b9d65f0a483fff2194c"
DEV = "fa7347fc59173f90e4feec2df207692e6e6e72ec"
BUILDERS = {
    "sw/firmware/ctrl/test/ctrl_image.py",
    "sw/firmware/ctrl/test/ctrl_srp_image.py",
    "sw/firmware/ctrl/test/ctrl_build.py",
    "sw/firmware/ctrl/test/ctrl_configs.py",
    "sw/firmware/ctrl/test/ctrl_image_selftest.py",
}


def is_input(path):
    if path in BUILDERS or path == "third_party/tsn-c-stack":
        return True
    if path.startswith(("sw/mailbox/", "configs/")):
        return True
    if path.startswith("sw/firmware/"):
        if path.endswith(".md") or "/test/" in path or path.startswith("sw/firmware/gtest/"):
            return False
        return path.endswith((".c", ".h", ".S", ".s", ".ld", ".lds", ".mk", "Makefile", ".py", ".yaml", ".cmake"))
    return False


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--repo", type=Path, required=True)
args = parser.parse_args()
paths = subprocess.check_output(["git", "-C", str(args.repo), "diff", "--no-renames", "--name-only", BASE, DEV],
                                text=True).splitlines()
print("dev side changed", len(paths), "paths")
flagged = [p for p in paths if is_input(p)]
for path in paths:
    print("  ", "INPUT" if is_input(path) else "not an image input", path)
assert not flagged, flagged
print("dev side image inputs: none")

controls = [
    "sw/firmware/ctrl/maap/maap_mbx.c",
    "sw/firmware/ctrl/mbx/mbx.h",
    "sw/mailbox/mailbox.yaml",
    "configs/endstation_arty_4x4.yaml",
    "third_party/tsn-c-stack",
    "sw/firmware/ctrl/test/ctrl_image.py",
]
for planted in controls:
    result = [p for p in paths + [planted] if is_input(p)]
    print("control", planted, "->", "flagged" if result == [planted] else "MISSED")
    assert result == [planted], planted
print("image-input controls: %d/%d flagged" % (len(controls), len(controls)))
