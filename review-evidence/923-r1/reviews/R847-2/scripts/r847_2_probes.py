#!/usr/bin/env python3
"""r847_2_probes.py - disposable plants for the #923 round-3 delta, each on its own fresh export of the checkout.

usage: r847_2_probes.py <checkout> <tsn-c-stack checkout> <scratch dir> <receipts.jsonl> [probe ...]

Each probe: `git archive HEAD` of <checkout> into <scratch>/<probe>/, one exact single-site replacement, then the
copy's own aecp_arms.core_arm (app mode) at the named interface count with the named gtest filter. The checkout
itself is never written. A probe's verdict line names the failed tests and whether each expected test failed on
its expected words (the campaign's own reader, aecp_mutants.caught)."""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

FACE = "aecp/aecp_face.c"
TEST = "test/test_aecp.cpp"
ALL = "Core.*:Face.*:AppStore.*"
LATE_W = "Face.ALostReplyAfterTheReservedCommitLeavesTheStoreAndTheMapAgreeing"
LATE_R = "Face.ALostReplyInTheRestoresCommitLeavesTheStoreAndTheMapAgreeing"
UNANS = "Face.AnUnansweredEditFailsUntilItsCommitIsReserved"
PICK = "Face.AnEditCommitsTheMappingsTheCorePicksAndNoOthers"
AGREE = "GET_AUDIO_MAP and the datapath's store hold the same mappings"

APPLY_OLD = ("\tfor (size_t k = 0; k < count; ++k) {\n\t\t(void)record(f, request, APPLY, records, pick, k, &ok);\n\t}\n"
             "\t(void)beat(f, request, FINISH, 0u, 1u, 2u, &ok);\n\treturn AECP_SUCCESS;\n")

# name: (file, old, new, interfaces, filter, ((test, words), ...) expected to fail; () = control, all must pass)
PROBES = {
    "control-if1": (None, "", "", 1, "*", ()),
    "control-if2": (None, "", "", 2, "*", ()),
    # the table's two new rows, re-planted independently
    "window-lost-reply-stops-the-commit": (
        FACE, "\tfor (size_t k = 0; k < count; ++k) {\n\t\t(void)record(f, request, APPLY, records, pick, k, &ok);\n\t}\n",
        "\tfor (size_t k = 0; k < count && record(f, request, APPLY, records, pick, k, &ok); ++k) {\n\t}\n",
        1, ALL, ((LATE_W, AGREE), (LATE_R, AGREE))),
    "window-pick-ignored": (
        FACE, "\tconst uint8_t *r = records + 8u * (pick != NULL ? pick[k] : k);",
        "\tconst uint8_t *r = records + 8u * (pick != NULL ? k : k);",
        1, ALL, ((PICK, "the records the core picked are committed"),)),
    # the validation pass alone reads the command's first records (the commit pass still honours pick)
    "validate-pick-ignored": (
        FACE, "status = !record(f, request, VALIDATE, records, pick, k, &ok)",
        "status = !record(f, request, VALIDATE, records, NULL, k, &ok)",
        1, ALL, ((PICK, "the records the core picked are validated"),)),
    # a lost commit reply turns the answer into ENTITY_MISBEHAVING although the store took every write
    "lost-commit-reply-answers-misbehaving": (
        FACE, APPLY_OLD,
        "\tbool lost = false;\n\tfor (size_t k = 0; k < count; ++k) {\n"
        "\t\tlost |= !record(f, request, APPLY, records, pick, k, &ok);\n\t}\n"
        "\t(void)beat(f, request, FINISH, 0u, 1u, 2u, &ok);\n\treturn lost ? AECP_ENTITY_MISBEHAVING : AECP_SUCCESS;\n",
        1, ALL, ((LATE_W, "the reserved edit answers SUCCESS"),)),
    # control of the model: round 2's store, which drops the write with the reply on every phase
    "old-model-drops-the-write": (
        TEST,
        "        bool reserved=b.phase==5u||b.phase==2u;\n"
        "        if(verdict==2u&&!reserved){*reply=MBX_MODEL_SILENT;return 0;}\n"
        "        if(verdict==2u){*reply=MBX_MODEL_SILENT;verdict=0u;}   // taken; its reply lost\n",
        "        if(verdict==2u){*reply=MBX_MODEL_SILENT;return 0;}\n",
        1, ALL, ((LATE_W, AGREE), (LATE_R, AGREE), (UNANS, AGREE))),
}

RUNNER = r"""
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import aecp_arms, aecp_mutants, fw_gtest
from ctrl_build import Tree, ROOT, CTRL
out = Path(sys.argv[2])
tree = Tree(CTRL, out / "build", out / "reuse", fw_gtest.Build(jobs=2), Path(sys.argv[3]))
r = aecp_arms.core_arm(tree, ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml", int(sys.argv[4]), "app", sys.argv[5])
(out / "arm.log").write_text(r.log)
print(r.rc)
"""


def probe(name, checkout, stack, scratch):
    path, old, new, ifs, filt, expect = PROBES[name]
    root = scratch / name
    subprocess.run(["rm", "-rf", str(root)], check=True)
    root.mkdir(parents=True)
    tar = subprocess.run(["git", "-C", str(checkout), "archive", "HEAD"], check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(root)], input=tar, check=True)
    for sub in ("protocol-processor", "gptp-processor", "third_party/tsn-c-stack", "third_party/lwSRP", "third_party/verilog-axis"):  # read-only links to the checkout's gitlinks
        (root / sub).rmdir()
        (root / sub).symlink_to(checkout / sub)
    ctrl = root / "sw/firmware/ctrl"
    if path:
        target = ctrl / path
        text = target.read_text()
        if text.count(old) != 1:
            return {"probe": name, "error": f"planting sites {text.count(old)}"}
        target.write_text(text.replace(old, new))
    res = subprocess.run([sys.executable, "-B", "-c", RUNNER, str(ctrl / "test"), str(root / "out"), str(stack),
                          str(ifs), filt], capture_output=True, text=True)
    log = (root / "out/arm.log").read_text() if (root / "out/arm.log").exists() else res.stderr
    sys.path.insert(0, str(ctrl / "test"))
    import re
    failed = sorted(set(re.findall(r"^\[  FAILED  \] (\S+) \(", log, re.M)))
    ran = re.search(r"\[==========\] (\d+) tests? from", log)
    rc = int(res.stdout.strip().splitlines()[-1]) if res.stdout.strip() else -1

    def caught(test, words):
        m = re.search(r"\[ RUN      \] " + re.escape(test) + r"\n(.*?)\[  FAILED  \] " + re.escape(test) + r" \(",
                      log, re.S)
        return rc == 1 and "verdict: FAIL (its tallies report" in log and m is not None and words in m[1]

    checks = [{"test": t, "words": w, "caught": caught(t, w)} for t, w in expect]
    ok = (rc == 0 and not failed) if not expect else all(c["caught"] for c in checks)
    return {"probe": name, "interfaces": ifs, "filter": filt, "rc": rc, "tests_ran": ran[1] if ran else None,
            "failed": failed, "checks": checks, "verdict": "as-expected" if ok else "UNEXPECTED",
            "stderr_tail": "" if rc in (0, 1) else res.stderr[-2000:]}


def main():
    checkout, stack, scratch, receipts = map(Path, sys.argv[1:5])
    names = sys.argv[5:] or list(PROBES)
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda n: probe(n, checkout.resolve(), stack.resolve(), scratch.resolve()), names))
    with receipts.open("w") as fh:
        for r in results:
            fh.write(json.dumps(r) + "\n")
            print(json.dumps(r))
    return 0 if all(r.get("verdict") == "as-expected" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
