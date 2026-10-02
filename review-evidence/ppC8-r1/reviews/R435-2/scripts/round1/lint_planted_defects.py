#!/usr/bin/env python3
"""Reviewer-planted defects in the model lint and the packer: each mutant is
one textual replacement in an isolated copy of the processor tree; the
generator gate (tb/desc_store/test_gen_desc_image.py) is run on the copy and
must fail (KILLED). A SURVIVED mutant is a defect the gate does not catch.

usage: lint_planted_defects.py <clean-processor-tree> <work-dir> [--jobs N]
"""
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

R = "hdl/aecp/desc/model_rules.py"
L = "hdl/aecp/desc/model_lint.py"
G = "hdl/aecp/desc/gen_desc_image.py"

# id, file, old text (must occur exactly once), new text, what it plants
MUTANTS = [
    ("cap45", R, "FORMATS_MAX = 46 ", "FORMATS_MAX = 45 ", "N cap one too strict (45)"),
    ("cap47", R, "FORMATS_MAX = 46 ", "FORMATS_MAX = 47 ", "N cap one too loose (47)"),
    ("buf-1", R, "BUFFER_MIN_NS = 2_126_000", "BUFFER_MIN_NS = 2_125_999", "buffer floor 1 ns low"),
    ("buf-le", R, "length < BUFFER_MIN_NS", "length <= BUFFER_MIN_NS", "buffer floor 1 ns high"),
    ("rates7", R, "RATES_MAX = 8 ", "RATES_MAX = 7 ", "rate cap one too strict (7)"),
    ("rates9", R, "RATES_MAX = 8 ", "RATES_MAX = 9 ", "rate cap one too loose (9)"),
    ("ratelen-lt", R, "if len(body) != RATES_OFFSET + 4 * count:",
     "if len(body) < RATES_OFFSET + 4 * count:", "AUDIO_UNIT may be longer than its list"),
    ("ident-perm", R, "if listed != list(range(count)):",
     "if sorted(listed) != list(range(count)):", "clock_sources permutation accepted"),
    ("aaf-ge1", R, "if total != 1:", "if total < 1:", "several INPUT_STREAM sources at AAF inputs accepted"),
    ("crf-ge1", R, "if at_input[stream] != 1:", "if at_input[stream] < 1:",
     "two INPUT_STREAM sources at one CRF input accepted"),
    ("l11-min", R, "most_out = max(", "most_out = min(", "talker maximum taken as minimum"),
    ("emid-ones", R, "if model_id in (0, (1 << 64) - 1):", "if model_id in (0,):",
     "all-ones entity_model_id accepted"),
    ("stale-off", L, "elif index not in covered[waiver.number]:", "elif False:",
     "a waiver whose check passes is not stale"),
    ("waiver-anytype", L, "if finding.check != self.check or (cfg, dtype) != self.where[:2]:",
     "if finding.check != self.check or cfg != self.where[0]:",
     "a waiver excuses its check on every descriptor type of the configuration"),
    ("waiver-anycfg", L, "if finding.check != self.check or (cfg, dtype) != self.where[:2]:",
     "if finding.check != self.check or dtype != self.where[1]:",
     "a waiver excuses its check in every configuration"),
    ("reason-any", L, 'ISSUE_REF = re.compile(r"[\\w.-]+(?:/[\\w.-]+)?#\\d+")',
     'ISSUE_REF = re.compile(r".")', "any reason accepted"),
    ("class-b", R, "CLASS_A = 0x0002 ", "CLASS_A = 0x0004 ", "CLASS_B bit tested for CLASS_A"),
    ("chan-no8", R, "BASE_CHANNELS = (1, 2, 4, 6, 8)", "BASE_CHANNELS = (1, 2, 4, 6)",
     "8-channel Base format dropped from completeness"),
    ("covers-eq", R, "    if entry == current:\n        return True\n    up_to",
     "    if entry == current:\n        return True\n    return False\n    up_to",
     "the ut (up to) bit ignored for current_format"),
    ("gptp-gt2", R, "if gptp and len(ctx.of(cfg, D.AVB_INTERFACE)) != 1:",
     "if gptp and len(ctx.of(cfg, D.AVB_INTERFACE)) > 2:", "gPTP media clock with two interfaces"),
    ("order-control-only", R, "            if parent[0] == D.AVB_INTERFACE:\n                continue",
     "            if parent[0] == D.AVB_INTERFACE or child != D.CONTROL:\n                continue",
     "L2 ordering applied to multi-level CONTROL only (IEEE 7.2 wording)"),
    ("map-key3", R, 'key = struct.unpack_from(">HH", body, offset + 8 * k)',
     'key = struct.unpack_from(">HHH", body, offset + 8 * k)',
     "a duplicate mapping differing in cluster offset accepted"),
    ("entity-cfg", R, "        if cfg != 0:\n            ctx.bad(\"entity-count\"",
     "        if False:\n            ctx.bad(\"entity-count\"", "an ENTITY outside configuration 0 accepted"),
    ("curcfg-gt", R, "current >= count:", "current > count:", "current_configuration == count accepted"),
    ("tail-off", R, "    if tail:\n", "    if False:\n", "redundant streams accepted"),
    ("iface-subset", R, "        if shapes[cfg] != first:",
     "        if any(first.get(k, v) != v for k, v in shapes[cfg].items()):",
     "L5 compares only the indices both configurations hold"),
    ("lint-default-off", G, "line_bytes: int = 576, *, lint: bool = True,",
     "line_bytes: int = 576, *, lint: bool = False,", "lint off by default"),
    ("cli-never-lints", G, "lint=not args.no_lint,", "lint=False,", "the CLI never lints"),
    ("digest-no-curfmt", L, "D.STREAM_INPUT: ((74, 82),), D.STREAM_OUTPUT: ((74, 82),),",
     "", "current_format no longer excluded from the digest"),
    ("rate-empty-off", R, "            if count == 0:\n                ctx.bad(\"rate-empty\"",
     "            if False:\n                ctx.bad(\"rate-empty\"", "an empty rate list accepted"),
    ("parent-single", R, "            if len(parents) > 1:", "            if len(parents) > 2:",
     "a descriptor with two parents accepted"),
    ("lint-before-layout", G,
     "    lint_lines = _lint_lines(groups, model, lint, (adp, model_ids))\n    img, layout",
     "    img, layout", "the lint result discarded (never called)"),
]


def run(tree: Path, work: Path, mutant) -> str:
    ident, path, old, new, what = mutant
    copy = work / ident
    if copy.exists():
        shutil.rmtree(copy)
    shutil.copytree(tree, copy, ignore=shutil.ignore_patterns("obj_dir", "__pycache__"))
    target = copy / path
    text = target.read_text(encoding="utf-8")
    if text.count(old) != 1:
        return f"{ident} INVALID (pattern occurs {text.count(old)} times) | {what}"
    target.write_text(text.replace(old, new), encoding="utf-8")
    proc = subprocess.run([sys.executable, "-B", "test_gen_desc_image.py"],
                          cwd=copy / "tb/desc_store", capture_output=True, text=True)
    tail = [ln for ln in proc.stderr.splitlines() if ln.startswith(("FAILED", "OK", "Ran"))]
    verdict = "KILLED" if proc.returncode else "SURVIVED"
    (work / f"{ident}.log").write_text(proc.stderr, encoding="utf-8")
    shutil.rmtree(copy)
    return f"{ident} {verdict} rc={proc.returncode} {' '.join(tail)} | {what}"


def main() -> int:
    tree, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 8
    work.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        for line in pool.map(lambda m: run(tree, work, m), MUTANTS):
            print(line, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
