#!/usr/bin/env python3
"""l6_plants.py <processor-git-dir> <rev> <work-dir>

Reviewer-owned plants of stricter (or order-reading) L6 readings, each into
its own disposable `git archive` copy of the processor at <rev>. Each plant
is one text substitution in hdl/aecp/desc/model_rules.py's _rule_sources
(asserted to match exactly once). For every plant the packer gate
(tb/desc_store/test_gen_desc_image.py) runs twice: whole, and with
ConformingModelTest.test_a_source_per_aaf_input_beside_crf deleted from the
copy. KILLED = the gate fails. Prints the failing test ids."""
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

repo, rev, work = sys.argv[1], sys.argv[2], Path(sys.argv[3])
ANCHOR = "        if ctx.of(cfg, D.STREAM_OUTPUT) and not any(k[0] == INTERNAL for k in kinds.values()):\n"

def bad(cond: str, what: str) -> str:
    return (f"        if {cond}:\n"
            f"            ctx.bad(\"crf-input-source\", (cfg, D.CLOCK_SOURCE, None), \"PLANT {what}\")\n")

AAF_TOTAL = "sum(at_input[k] for k in aaf_in)"
PLANTS = {
    # control: no plant; the gate must pass in both variants (SURVIVED)
    "c0-control": "",
    # stricter readings of the source set main's L6 allows
    "x1-sources-at-most-9": bad("len(kinds) > 9", "at most nine CLOCK_SOURCEs"),
    "x2-sources-at-most-stream-inputs": bad("len(kinds) > len(ctx.of(cfg, D.STREAM_INPUT))",
                                            "no more sources than Stream Inputs"),
    "x3-beside-crf-at-most-one-aaf": bad(f"crf_in and {AAF_TOTAL} > 1",
                                         "beside CRF, one AAF source at most"),
    "x4-beside-crf-no-aaf": bad(f"crf_in and {AAF_TOTAL} > 0", "beside CRF, no AAF source"),
    "x5-input-stream-at-most-crf-plus-one": bad(
        "sum(at_input.values()) > len(crf_in) + 1", "INPUT_STREAM sources at most CRF inputs + 1"),
    "x6-aaf-sources-at-most-half": bad(
        f"crf_in and {AAF_TOTAL} > max(1, len(aaf_in) // 2)", "beside CRF, AAF sources at most half"),
    # order readings: main's L6 says the processor reads no order, and the
    # merged 07 L6 row says neither the processor nor the lint reads one
    "o1-internal-first": bad("kinds and kinds.get(0, (None,))[0] != INTERNAL",
                             "CLOCK_SOURCE 0 must be INTERNAL"),
    "o2-crf-source-at-1": bad(
        "crf_in and not (kinds.get(1, (None,))[0] == INPUT_STREAM and kinds[1][2] in crf_in)",
        "CLOCK_SOURCE 1 must be the CRF input's"),
    "o3-aaf-in-stream-order": bad(
        "[k[2] for i, k in sorted(kinds.items()) if k[0] == INPUT_STREAM and k[2] in aaf_in]"
        " != sorted(k[2] for k in kinds.values() if k[0] == INPUT_STREAM and k[2] in aaf_in)",
        "AAF sources in STREAM_INPUT order"),
}

TEST = "tb/desc_store/test_gen_desc_image.py"

def run(name: str, body: str) -> str:
    out = []
    for variant in ("whole", "without-new-test"):
        d = work / f"{name}-{variant}"
        d.mkdir(parents=True, exist_ok=False)
        arch = subprocess.run(["git", "-C", repo, "archive", rev], check=True, capture_output=True).stdout
        subprocess.run(["tar", "-x", "-C", str(d)], input=arch, check=True)
        rules = d / "hdl/aecp/desc/model_rules.py"
        text = rules.read_text()
        assert text.count(ANCHOR) == 1
        rules.write_text(text.replace(ANCHOR, body + ANCHOR))
        if variant == "without-new-test":
            t = d / TEST
            src = t.read_text()
            new = re.sub(r"\n    def test_a_source_per_aaf_input_beside_crf\(self\) -> None:\n.*?\n(?=    def )",
                         "\n", src, count=1, flags=re.S)
            assert new != src
            t.write_text(new)
        r = subprocess.run([sys.executable, "-B", TEST], cwd=d, capture_output=True, text=True)
        fails = sorted(set(re.findall(r"^(?:FAIL|ERROR): (\S+ \(\S+\))", r.stderr, re.M)))
        verdict = "KILLED" if r.returncode else "SURVIVED"
        out.append(f"{name} [{variant}]: {verdict} rc={r.returncode} failing={len(fails)}"
                   + "".join(f"\n    {f}" for f in fails))
    return "\n".join(out)

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=12) as pool:
        for line in pool.map(lambda kv: run(*kv), PLANTS.items()):
            print(line, flush=True)
