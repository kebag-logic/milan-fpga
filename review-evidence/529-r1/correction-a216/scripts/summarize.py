#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""[A216] #529: tabulate the mutant receipts in logs/mutants/.

For every pairwise exchange (pw_<a>_<b>) run against the head harness, also
check that BOTH quadlets of the exchanged pair are red in the event arm's
per-quadlet row ("[CTRS-CRF] events, all ten: @<off> <NAME>"), so each
binding is shown discriminated by its own check, not by a side effect.
usage: summarize.py <packet dir>  (writes MUTATION-RESULTS.md there)
"""
import pathlib
import re
import sys

NAME = {"pdu": "FRAMES_RX", "fmt": "UNSUPPORTED_FORMAT",
        "seq": "SEQ_NUM_MISMATCH", "mr": "MEDIA_RESET",
        "tu": "TIMESTAMP_UNCERTAIN", "late": "LATE_TIMESTAMP",
        "early": "EARLY_TIMESTAMP", "lock": "MEDIA_LOCKED",
        "unlock": "MEDIA_UNLOCKED", "intr": "STREAM_INTERRUPTED"}


def parse(path):
    t = path.read_text()
    m = re.search(r"^checks:\s*(\d+)\s+failures:\s*(\d+)", t, re.M)
    fails = re.findall(r"^\s*\[FAIL\] (.*?)(?:\s+got=.*)?$", t, re.M)
    return {
        "leg": re.search(r"# leg=(\S+)", t).group(1),
        "dp": re.search(r"# datapath sha256 (\S+)", t).group(1),
        "harness": re.search(r"# harness  sha256 (\S+)", t).group(1),
        "build": re.search(r"# build exit (\d+)", t).group(1),
        "checks": m.group(1) if m else "-",
        "failures": m.group(2) if m else "-",
        "fails": fails,
    }


def main():
    o = pathlib.Path(sys.argv[1])
    rows, bad = [], []
    for p in sorted((o / "logs/mutants").glob("*.txt")):
        tag = p.stem
        r = parse(p)
        crf = [f for f in r["fails"] if re.match(r"\[(CTRS|NOTIFY)-CRF\]", f)]
        other = len(r["fails"]) - len(crf)
        pair = ""
        m = re.match(r"(?:base_)?(?:nxn8?|nxndv|nxn4c)_pw_([a-z]+)_([a-z]+)$", tag)
        if m and not tag.startswith("base_"):
            want = [NAME[m.group(1)], NAME[m.group(2)]]
            hit = [w for w in want if any(
                f.startswith("[CTRS-CRF] events, all ten:") and f.endswith(" " + w)
                for f in crf)]
            pair = "both" if len(hit) == 2 else f"ONLY {hit}"
            if len(hit) != 2:
                bad.append(tag)
        verdict = "RED" if r["failures"] not in ("0", "-") else (
            "green" if r["failures"] == "0" else "BUILD-FAILED")
        rows.append((tag, r["leg"], r["harness"][:8], r["dp"][:8], r["build"],
                     r["checks"], r["failures"], str(len(crf)), str(other),
                     pair, verdict))
    out = ["# [A216] #529 mutant receipts", "",
           "| tag | leg | harness | datapath | build | checks | failures | "
           "CRF-tag red | other red | pair's own quadlets red | verdict |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    out += ["", f"pairwise receipts missing a red on either own quadlet: {bad or 'none'}"]
    (o / "MUTATION-RESULTS.md").write_text("\n".join(out) + "\n")
    print(f"{len(rows)} receipts; pairwise own-quadlet gaps: {bad or 'none'}")


if __name__ == "__main__":
    main()
