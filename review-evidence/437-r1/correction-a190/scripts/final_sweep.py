#!/usr/bin/env python3
"""Every corpus against GitHub's recorded renderings, at the lane's HEAD.

Usage: final_sweep.py OUT.json
Walks: base 483a133e (its gen_toc.py is byte-identical to 88e9276b's), the
starting head 4741498f, and HEAD (three walk modules, loaded from the clean
checkout). Renderings: every public receipt (work/public-cache.json) and
this author's (work/render-cache.jsonl). A page whose new walk answers like
the base needs no rendering: it agrees exactly when the base does. The run
fails when any page REGRESSES (the base agrees, HEAD does not), when a page
where HEAD differs from the base has no rendering, or when a disagreement at
HEAD is not explained by the five family-two forms (headings GitHub renders
from a setext underline or inside a container, which the walk omits).
"""
import hashlib, json, re, subprocess, sys
from pathlib import Path

PKT = Path("$REVIEWS/437-a190-packet")
LANE = "$LANES/437-container-paragraph-scopes"
sys.path.insert(0, str(PKT / "scripts"))
from sweep import load_rev, walk_fn, caches, classify  # noqa: E402

CORPORA = ["work/r237-2-corpus.json", "work/probe-containers.json", "work/probe-comments.json",
           "work/probe-prose.json", "work/probe-fuzz.json", "work/probe-fuzz2.json",
           "work/probe-tabs.json", "work/probe-rules.json"]


def col0_only(page, rendered, walk):
    col0 = [m.group(2) for m in re.finditer(r"(?m)^(#{1,6})[ \t]+(.*?)[ \t]*$", page)]
    return [h for h in rendered if h[1] in col0] == walk


def main():
    head = subprocess.run(["git", "-C", LANE, "rev-parse", "HEAD"], capture_output=True,
                          text=True, check=True).stdout.strip()
    dirty = subprocess.run(["git", "-C", LANE, "status", "--porcelain"], capture_output=True,
                           text=True, check=True).stdout
    assert not dirty, "the checkout must be clean"
    base = walk_fn(load_rev("483a133ed08867ea0d300d2b4a027b5b48a4282f", "base"))
    start = walk_fn(load_rev("4741498f3b2b4f67f431037d327c96cf65691278", "start"))
    sys.path.insert(0, f"{LANE}/scripts")
    import gen_toc
    new = walk_fn(gen_toc)
    cache = caches()
    for line in (PKT / "receipts/walk-fixture-render.jsonl").read_text().splitlines():
        row = json.loads(line)
        cache.setdefault(row["page"], row["headings"])
    for f in ("gen_toc_family_one.json", "gen_toc_comment_shapes.json", "gen_toc_container_walk.json"):
        for shape in json.loads(Path(LANE, "scripts", f).read_text())["shapes"]:
            cache.setdefault(shape["page"], shape["headings"])
    public = json.loads((PKT / "work/public-cache.json").read_text())["pages"]
    sets = {"public receipts": list(public)}
    for c in CORPORA:
        sets[Path(c).stem] = list(dict.fromkeys(
            (i["page"] if isinstance(i, dict) else i) for i in json.loads((PKT / c).read_text())))
    sets["fixtures"] = [s["page"] for f in ("gen_toc_family_one.json", "gen_toc_comment_shapes.json",
                                            "gen_toc_container_walk.json")
                        for s in json.loads(Path(LANE, "scripts", f).read_text())["shapes"]]
    report, failures = {"head": head, "corpora": {}}, 0
    for name, pages in sets.items():
        counts, vs_start, unexplained, regress, unrendered = {}, {}, [], [], []
        for p in pages:
            b, s, h = base(p), start(p), new(p)
            r = cache.get(p)
            if r is None:
                c = "same-unrendered" if b == h else "DIFF-UNRENDERED"
                if b != h:
                    unrendered.append(p)
            else:
                c = classify(r, b, h)
                cs = classify(r, s, h)
                vs_start[cs] = vs_start.get(cs, 0) + 1
                if c == "REGRESSION":
                    regress.append(p)
                if h != r and not col0_only(p, r, h):
                    unexplained.append(p)
            counts[c] = counts.get(c, 0) + 1
        failures += len(regress) + len(unrendered) + len(unexplained)
        report["corpora"][name] = {"pages": len(pages), "vs_base": counts, "vs_start": vs_start,
                                   "regressions": regress, "unrendered_differences": unrendered,
                                   "disagreements_not_family_two": unexplained}
        print(f"{name:22} {len(pages):6} pages  vs base {json.dumps(counts, sort_keys=True)}")
        print(f"{'':22} {'':6}        vs start {json.dumps(vs_start, sort_keys=True)}")
        print(f"{'':22} {'':6}        regressions {len(regress)}, unrendered differences "
              f"{len(unrendered)}, disagreements not family two {len(unexplained)}")
    report["renderings"] = len(cache)
    report["render_cache_sha256"] = hashlib.sha256((PKT / "work/render-cache.jsonl").read_bytes()).hexdigest()
    Path(sys.argv[1]).write_text(json.dumps(report, indent=1) + "\n")
    print(f"{len(cache)} recorded renderings; failures {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
