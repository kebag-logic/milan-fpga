#!/usr/bin/env python3
"""Build the SCRATCH-only prototype: copies of the trusted checker + self-test
with scripts/candidate_arm.py inserted into the checker COPY.

    python3 -B make_prototype.py /path/to/trusted/checkout OUTDIR

Reads the trusted checkout only (blobs verified against its index/HEAD); never
writes there.  Prints the inserted diff.  Not an implementation proposal.
"""
import difflib
import hashlib
import os
import subprocess
import sys

FILES = ("check_merge_containment.py", "merge_containment_selftest.py",
         "merge_containment_selftest_content.py",
         "merge_containment_selftest_scratch.py")
ANCHOR_DEF = "def contained(branch: str,\n"
ANCHOR_CALL = ("    verdict = _patch_id_verdict(branch, base, ahead)\n"
               "    if verdict is not None:\n"
               "        return verdict\n")
CALL = ("    #! R242 SCRATCH: the candidate #423 arm runs last, before STRANDED.\n"
        "    verdict = _redundant_merge_replay_verdict(branch, base, ahead)\n"
        "    if verdict is not None:\n"
        "        return verdict\n")


def main(checkout, outdir):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
    head_blobs = {}
    for name in FILES:
        out = subprocess.run(["git", "-C", checkout, "ls-tree", "HEAD",
                              "scripts/" + name], env=env, check=True,
                             capture_output=True, text=True).stdout.split()
        head_blobs[name] = out[2]
    arm = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "candidate_arm.py")).read()
    os.makedirs(outdir, exist_ok=True)
    for name in FILES:
        with open(os.path.join(checkout, "scripts", name), "rb") as fh:
            data = fh.read()
        oid = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
        if oid != head_blobs[name]:
            sys.exit(f"{name}: working copy {oid} != HEAD blob {head_blobs[name]}")
        text = data.decode()
        if name == "check_merge_containment.py":
            assert text.count(ANCHOR_DEF) == 1 and text.count(ANCHOR_CALL) == 1
            patched = text.replace(ANCHOR_DEF, arm + "\n\n" + ANCHOR_DEF)
            patched = patched.replace(ANCHOR_CALL, ANCHOR_CALL + "\n" + CALL)
            sys.stdout.writelines(difflib.unified_diff(
                text.splitlines(True), patched.splitlines(True),
                "trusted/scripts/" + name, "prototype/" + name))
            text = patched
        with open(os.path.join(outdir, name), "w") as fh:
            fh.write(text)
        print(f"# {name}: trusted blob {oid} -> prototype sha256 "
              f"{hashlib.sha256(text.encode()).hexdigest()}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
