#!/usr/bin/env python3
"""[R238] independent renderer probes for issue #437 / PR #515.

Each synthetic page is classified by the BASE walk (88e9276b) and the HEAD
walk (65df1df5), both loaded read-only from scratch clones, and rendered by
GitHub's Markdown API in gfm mode (`gh api markdown --input -`). Only the
synthetic page text below is sent; no repository content is sent and no
public state is created. Every exact request and response is kept in
receipts/renderer-cache.json and receipts/probes.jsonl.

Verdict per walk, for the probe heading `Old` and the recovery heading
`Real`: AGREE when the walk lists exactly the ATX headings the renderer
shows among {Old, Real}; INVENT when the walk lists one the renderer does not
show (the escape direction); WITHHOLD when the renderer shows one the walk
does not list (the safe direction).
"""
import datetime
import hashlib
import html
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent
SCRATCH = OUT / "scratch"
RECEIPTS = OUT / "receipts"
CACHE = RECEIPTS / "renderer-cache.json"
PROBE_WORDS = ("Old", "Real")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


BASE = load("gen_toc_base_r238", SCRATCH / "clone-base/scripts/gen_toc.py")
HEAD = load("gen_toc_head_r238", SCRATCH / "clone-head/scripts/gen_toc.py")


def page(prefix: str, tag: str = "span", indent: str = "") -> str:
    """The family-one probe: prefix, lone tag wrapping `## Old`, recovery."""
    return f"{prefix}\n{indent}<{tag}>\n## Old\n{indent}</{tag}>\n\n## Real\n"


FENCE = "```"
SHAPES = [
    # A: family one, independently respelled from R86-5's published words.
    ("A01 two spaces", page("- item\n\n  text")),
    ("A02 three spaces", page("- item\n\n   text")),
    ("A03 star item", page("* item\n\n  text")),
    ("A04 ordered item", page("1. item\n\n   text")),
    ("A05 two container paragraphs", page("- item\n\n  first\n\n  text")),
    ("A06 task item", page("- [ ] item\n\n  text")),
    ("A07 list after paragraph", page("para\n- item\n\n  text")),
    ("A08 b tag", page("- item\n\n  text", "b")),
    ("A09 two blank lines", page("- item\n\n\n  text")),
    ("A10 plus item", page("+ item\n\n  text")),
    ("A11 paren ordinal", page("1) item\n\n   text")),
    ("A12 custom tag", page("- item\n\n  text", "custom-tag")),
    ("A13 lone closing tag",
     "- item\n\n  text\n</b>\n## Old\n\n## Real\n"),
    ("A14 tag with attribute",
     "- item\n\n  text\n<span class=\"x\">\n## Old\n</span>\n\n## Real\n"),
    ("A15 self-closing tag", "- item\n\n  text\n<br/>\n## Old\n\n## Real\n"),
    ("A16 tag one column below col 2", page("- item\n\n  text", indent=" ")),
    ("A17 tag two columns below col 3", page("1. item\n\n   text", indent="  ")),
    ("A18 two-line first paragraph", page("- item\n  more\n\n  text")),
    ("A19 resumed twice", page("- item\n\n  text\n\n  again")),
    ("A20 zero ordinal", page("0. item\n\n   text")),
    # B: the boundaries acceptance 1 names.
    ("B01 one space", page("- item\n\n text")),
    ("B02 four spaces", page("- item\n\n    text")),
    ("B03 block quote", page("> item\n\n  text")),
    ("B04 footnote two spaces", page("[^1]: note\n\n  text")),
    ("B05 footnote four spaces", page("[^1]: note\n\n    text")),
    ("B06 tab", page("- item\n\n\ttext")),
    # C: a lone tag AT the item's content column below a resumed paragraph.
    ("C01 tag at col 2 under resumed paragraph", page("- item\n\n  text", indent="  ")),
    ("C02 tag at col 3 under resumed paragraph (col 2 item)",
     page("- item\n\n  text", indent="   ")),
    ("C03 tag at col 3 under resumed paragraph (col 3 item)",
     page("1. item\n\n   text", indent="   ")),
    ("C04 C01 then column-0 fence",
     f"- item\n\n  text\n  <span>\n{FENCE}\n\n## Old\n{FENCE}\n\n## Real\n"),
    ("C05 C01 then column-0 comment",
     "- item\n\n  text\n  <span>\n<!--\n\n## Old\n-->\n\n## Real\n"),
    ("C06 C01 then column-0 type-1 pre",
     "- item\n\n  text\n  <span>\n<pre>\n\n## Old\n</pre>\n\n## Real\n"),
    ("C07 C04 after a lazy line",
     f"- item\n\n  text\nlazy\n  <span>\n{FENCE}\n\n## Old\n{FENCE}\n\n## Real\n"),
    ("C08 C04 with a col-3 item",
     f"1. item\n\n   text\n   <span>\n{FENCE}\n\n## Old\n{FENCE}\n\n## Real\n"),
    # P: pre-existing flat-container escapes (base and head alike).
    ("P01 tag at col 2 under the FIRST item paragraph, then fence",
     f"- item\n  <span>\n{FENCE}\n\n## Old\n{FENCE}\n\n## Real\n"),
    ("P02 tag at col 2 after a blank inside the item, then fence",
     f"- item\n\n  <span>\n{FENCE}\n\n## Old\n{FENCE}\n\n## Real\n"),
    ("P03 type-6 div at col 2 inside the item, then fence",
     f"- item\n\n  <div>\n{FENCE}\n\n## Old\n{FENCE}\n\n## Real\n"),
    ("P04 tag at col 2 under the FIRST item paragraph",
     "- item\n  <span>\n## Old\n  </span>\n\n## Real\n"),
    # D: an item context the renderer has closed at a column-0 block.
    ("D01 column-0 quote after item, resumed text, tag",
     page("- item\n> quote\n\n  text")),
    ("D02 column-0 footnote after item, resumed text, tag",
     page("- item\n[^1]: note\n\n  text")),
    ("D03 D01 then column-0 fence",
     f"- item\n> quote\n\n  text\n<span>\n{FENCE}\n\n## Old\n{FENCE}\n\n## Real\n"),
    ("D04 D02 then column-0 fence",
     f"- item\n[^1]: note\n\n  text\n<span>\n{FENCE}\n\n## Old\n{FENCE}\n\n## Real\n"),
    ("D05 quote after a blank releases the item", page("- item\n\n> quote\n\n  text")),
    ("D06 quote inside the item keeps it", page("- item\n  > quote\n\n  text")),
    ("D07 indented quote below col 4 after item", page("-   item\n  > quote\n\n    text")),
    # F: context lifetime, independently spelled.
    ("F01 new ordered list after blank", page("- item\n\n2. other\n\n   text")),
    ("F02 new bullet type after blank", page("- item\n\n* other\n\n  text")),
    ("F03 sibling then one space", page("- item\n\n- other\n\n text")),
    ("F04 empty item then sibling", page("-\n- item\n\n  text")),
    ("F05 noninterrupting zero ordinal", page("text\n0. item\n\n   text")),
    ("F06 table inside item", page("- item\n\n  a | b\n  --|--")),
    ("F07 setext inside item", page("- item\n\n  text\n  ===")),
    ("F08 fence inside item", page(f"- item\n\n  {FENCE}\n  code\n  {FENCE}")),
    ("F09 tag at col 2 after blank (no paragraph)",
     "- item\n\n  text\n\n  <span>\n## Old\n  </span>\n\n## Real\n"),
    ("F10 type-1 below resumed paragraph", page("- item\n\n  text", "pre")),
    ("F11 dedented setext text ends nothing", page("- item\n\n  text\n===")),
    ("F12 empty star item then lazy", page("*\n  first\nlazy\n\n  text")),
    # G: family two, the five forms named as omitted.
    ("G01 equals setext", "Alpha\n===\n"),
    ("G02 hyphen setext", "text\n---\n"),
    ("G03 single hyphen setext", "text\n-\n"),
    ("G04 quoted heading", "> ## Q\n"),
    ("G05 list heading", "- item\n\n  ## Inner\n"),
]


def load_cache() -> dict:
    return json.loads(CACHE.read_text()) if CACHE.exists() else {}


def render(text: str, cache: dict) -> dict:
    request = json.dumps({"text": text, "mode": "gfm",
                          "context": "kebag-logic/milan-fpga"},
                         ensure_ascii=False, sort_keys=True)
    key = hashlib.sha256(request.encode()).hexdigest()
    if key not in cache:
        proc = subprocess.run(["gh", "api", "markdown", "--input", "-"],
                              input=request.encode(), capture_output=True)
        cache[key] = {"request": request, "exit": proc.returncode,
                      "response": proc.stdout.decode(),
                      "stderr": proc.stderr.decode(),
                      "utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
        CACHE.write_text(json.dumps(cache, indent=1, ensure_ascii=False, sort_keys=True))
    return cache[key] | {"request_sha256": key}


def rendered_headings(body: str) -> list[tuple[int, str]]:
    out = []
    for lvl, inner in re.findall(r"<h([1-6])[^>]*>(.*?)</h\1>", body, re.S):
        out.append((int(lvl), html.unescape(re.sub(r"<[^>]+>", "", inner)).strip()))
    return out


def verdict(walk: list[str], shown: list[str]) -> str:
    words = set(PROBE_WORDS) if set(PROBE_WORDS) & set(shown + walk) else set(shown + walk)
    walk_p = {w for w in walk if w in words}
    shown_p = {s for s in shown if s in words}
    if walk_p - shown_p:
        return "INVENT " + ",".join(sorted(walk_p - shown_p)) + (
            " +WITHHOLD " + ",".join(sorted(shown_p - walk_p)) if shown_p - walk_p else "")
    if shown_p - walk_p:
        return "WITHHOLD " + ",".join(sorted(shown_p - walk_p))
    return "AGREE"


def main() -> int:
    RECEIPTS.mkdir(exist_ok=True)
    cache = load_cache()
    rows = []
    for name, text in SHAPES:
        got = render(text, cache)
        if got["exit"] != 0:
            print(f"RENDER FAILED {name}: {got['stderr']}")
            return 2
        shown = rendered_headings(got["response"])
        base = [h[1] for h in BASE.headings(text)]
        head = [h[1] for h in HEAD.headings(text)]
        rows.append({"id": name, "page": text,
                     "request_sha256": got["request_sha256"],
                     "response_sha256": hashlib.sha256(got["response"].encode()).hexdigest(),
                     "render_utc": got["utc"],
                     "github": [s for _, s in shown], "github_levels": shown,
                     "base": base, "head": head,
                     "base_blocks": BASE.blocks(text), "head_blocks": HEAD.blocks(text),
                     "base_verdict": verdict(base, [s for _, s in shown]),
                     "head_verdict": verdict(head, [s for _, s in shown]),
                     "html": got["response"]})
    with (RECEIPTS / "probes.jsonl").open("w") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    width = max(len(r["id"]) for r in rows)
    lines = [f"{'id':<{width}}  {'github':<22} {'base':<22} {'head':<22} base-verdict / head-verdict"]
    for r in rows:
        lines.append(f"{r['id']:<{width}}  {str(r['github']):<22} {str(r['base']):<22} "
                     f"{str(r['head']):<22} {r['base_verdict']} / {r['head_verdict']}")
    (RECEIPTS / "probes-table.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
