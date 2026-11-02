"""Write HANDOFF.md for [A720k]. The gate table is read from the logs; the step list is 640-a720j's."""
import ast, subprocess
from pathlib import Path

OUT = Path("$MANAGEMENT/2026-09-23/640-a720k")
G = Path("$VALIDATION_STORAGE/640-a720k/gates")
LANE = "$LANES/640-mark2-charter"
J = Path("$MANAGEMENT/2026-09-23/640-a720j/evidence/write_handoff.py").read_text()
src = J[J.index("STEPS = ["):]
src = src[:src.index("\n]\n") + 3]
STEPS = ast.literal_eval(src.split("=", 1)[1].strip())
STEPS.append(("(lane)", "style on this pass's changed blocks", "style_touched_pass2", "check_doc_style's `analyze()` on AP's changed blocks against 7aa996e3"))
git = lambda *a: subprocess.run(["git", "-C", LANE, *a], capture_output=True, text=True, check=True).stdout.strip()
head, tree = git("rev-parse", "HEAD"), git("rev-parse", "HEAD^{tree}")
commits = [l.split("\t") for l in git("log", "--reverse", "--format=%H\t%s", "7aa996e3..HEAD").splitlines()]
TAKEN = (OUT / "evidence/taken_url.txt").read_text().strip()
RR = OUT / "evidence/review_ready_url.txt"
RR = RR.read_text().strip() if RR.exists() else "pending"

def rc(n):
    p = G / "logs" / f"{n}.rc"
    return p.read_text().strip() if p.exists() else "pending"

def last(n):
    p = G / "logs" / f"{n}.log"
    ls = [l for l in p.read_text(errors="replace").splitlines() if l.strip()] if p.exists() else ["pending"]
    return (ls[-1] if ls else "").replace("|", "/")[:150]

rows = "\n".join(f"| {j} | {s} | {c} | {rc(n)} | {last(n)} |" for j, s, n, c in STEPS)
bad = [n for _, _, n, _ in STEPS if rc(n) != "0"]
summary = f"All {len(STEPS)} rc files read 0." if not bad else "NOT ALL 0: " + ", ".join(bad)
ctab = "\n".join(f"| {i} | {h} | {s} |" for i, (h, s) in enumerate(commits, 6))
start, end = (G / "run_all.start").read_text().strip(), (G / "run_all.end").read_text().strip()

body = f"""# HANDOFF - [A720k] issue #640 Mark II charter follow-up, second pass (docs only)

Status: REVIEW READY (2026-11-02). {summary} git diff --check 503bc97c HEAD rc 0. Head {head} (tree {tree}). Local only, nothing pushed.

- Lane: $LANES/640-mark2-charter, branch 640-charter-followup. Started at 7aa996e3 (640-a720j's head) on dev 503bc97c; `git merge-base HEAD origin/dev` is 503bc97cd4f24ad07596c17e7188f2024617972d, and origin/dev is still 503bc97c.
- Remote checked: https://github.com/kebag-logic/milan-fpga.git
- Source of both items: #640 issuecomment-6575277828 ([A10], 2026-11-02 10:50 UTC), the manager's answer to 640-a720j's open points 1 and 2.
- TAKEN: {TAKEN} (text: evidence/taken.md)
- REVIEW READY: {RR} (text: evidence/review_ready.md)
- Scratch: $VALIDATION_STORAGE/640-a720k (gate clone, venv copied from 640-a720j, fresh scratch HOME with a freshly installed pinned SDK). Evidence: ./evidence/.
- One page changes in this pass: docs/design/MARK_II_AREA_PLAN.md (AP). No RTL, firmware, generator, gate or configuration file. docs/integration/QSPI_FLASHBOOT.md not edited. No generated page reads AP; DOC_MAP and the TOC gate pass unchanged.

## Read this first

1. **D21 is a new decision row, a manager decision.** The assignment said to move open decision 4 into the decisions table, so I numbered it D21, after D20. Its outcome text follows the comment's bullets; the offset and budget are left to the stage 1 lane (`FLASHBOOT_LAYOUT` and the generated layout page).
2. **The census held no layout statement.** The census (AP:287-320) never said the layout stays or lacks a slot. The statements were in the stage table row (AP:231), the stage 1 text (AP:264-273), the D18 consequence (AP:381), lane 2's dependency (AP:398) and open decision 4. All are gone; `grep -n -i "open decision 4\\|stay as is\\|layout is unchanged\\|no firmware slot"` on AP finds nothing.
3. **One contents line changed with item 2.** AP:20 now reads "Owner and manager rulings, 2026-10-31 and 2026-11-02.", since the table now holds a manager row. "The owner and manager rulings of ..." broke the 10-word sentence limit.
4. **Line numbers in 640-a720j's HANDOFF shift.** Add 8 to its AP line numbers 266 to 375, and 9 to 376 to 431. Its 432 to 441 (open decision 4) are gone; from 442 on, subtract 1.

## Commits (one-line subjects, no body, no trailers)

640-a720j's five commits (1 to 5) are unchanged; this pass adds:

| # | SHA | Subject |
|---|---|---|
{ctab}

## 1. D18 to D20 links (commit 6)

| Where (at head) | Change |
|---|---|
| AP:381 | D18 link: `issues/640` -> `issues/640#issuecomment-6575277828` |
| AP:382 | D19 link: the same |
| AP:383 | D20 link: the same |

No other link the first pass made for these decisions points at #640: the census and UART rows link to the D18 to D20 anchors on the page (AP:289, :306, :315, :324), not to the issue. The other bare `issues/640` links in the branch (AP:3, MAILBOX_SPLIT.md:27, AREA_BUDGET.md) are not about D18 to D20.

## 2. Open decision 4 -> D21, manager decision (commit 7)

| Where (at head) | Before | After |
|---|---|---|
| AP:20 | "The owner rulings of 2026-10-31 and 2026-11-02." | "Owner and manager rulings, 2026-10-31 and 2026-11-02." |
| AP:231 (stage table, stage 1) | "the flash layout is unchanged" | "the image has its own flash slot ([D21](#mark-ii-decisions))" |
| AP:264-273 (stage 1 boot and bus) | "The layout in QSPI_FLASHBOOT.md stays unchanged. That layout has no firmware slot (open decision 4)." | Own slot (D21); free, erase-aligned, never reserved or used; bitstream and AEM keep offsets and budgets; no image in the bitstream slot's tail; the stage 1 lane states offset and budget in `FLASHBOOT_LAYOUT` and the generated layout page; until then QSPI_FLASHBOOT.md describes the shipping layout |
| AP:381 (D18 consequence) | "where the image sits in flash is open decision 4" | "the image sits in its own flash slot (D21)" |
| AP:384 (new D21 row) | - | "[Manager, 2026-11-02](...#issuecomment-6575277828)": own slot sized for the image, free erase-aligned range, neither reserved (`journal`, `user`) nor used; bitstream and AEM keep offsets and budgets; not in the bitstream slot's tail, which would tie the offset to the bitstream's size. Consequence: the stage 1 lane adds the slot to `FLASHBOOT_LAYOUT` and the generated layout page, and states its offset and budget there |
| AP:398 (lane 2) | Scope without the slot; depends on "Lane 1; open decision 4" | Scope adds "the firmware's own flash slot (D21)"; depends on "Lane 1" |
| AP:417-441 (open list) | Items 1 to 4 | Items 1 to 3; item 4 (nine bullets: the no-slot premise, AEM 64 KiB, rom 96,624 B, bitstream 3,825,992 B, 368,312 B tail, the two choices) removed |

Not chosen: the slot's offset and budget. Not edited: docs/integration/QSPI_FLASHBOOT.md, sw/litex/milan_soc.py (`FLASHBOOT_LAYOUT`), docs/diagrams/flash_layout.gen.py.

## Gate table

{summary}

Every run step of `.github/workflows/docs.yml` at 503bc97c (no `.github/` or `scripts/` diff on the branch), as its jobs run it, sequentially, on $VALIDATION_STORAGE/640-a720k/gates/wt: a fresh clone of the lane at {head}, with gptp-processor 135afd04, protocol-processor a9e84b66, tsn-c-stack 70936b77 and verilog-axis 48ff7a7e (depth 1 from 640-a720j's clone, each origin its .gitmodules URL; the same pins as HEAD's gitlinks). Venv: 640-a720j's, copied. RV32 SDK: installed fresh into $VALIDATION_STORAGE/640-a720k/home; the shared SDK was not touched. TMPDIR and RUNNER_TEMP point into scratch. Run {start} to {end}. Step list: evidence/gates/run_gates.sh, run_all.sh.

| Job | Step | Command | rc | Last line |
|---|---|---|---:|---|
{rows}

Notes:
- docs-check's "Require every gate exactly once" verifies uploaded CI receipts and runs only on GitHub; ci-manifest, ci-fail-fast and ci-cancel-tail are CI orchestration. Not run locally. act was not used: it needs a pushed head, and this lane pushes nothing.
- Builder leg 1's 16 NOT RUN arms need migen, LiteX and an Arty report, which the docs workflow never installs; the leg's rc is what counts.
- The readers of AREA_BUDGET.md and MAILBOX_SPLIT.md re-ran at this head though this pass does not touch those pages.
- Clone status after the run: empty (evidence/gates/logs/final_status.txt).
- gate_41's log is 337,511 B, listed in evidence/gates/LARGE_LOGS.txt by sha256 and size, not copied.

## Open points for the manager (as they now stand)

1. ~~Post the owner's 2026-11-02 decisions on #640.~~ Done by the manager (issuecomment-6575277828); D18 to D20 link to it.
2. ~~Open owner decision 4.~~ Decided by the manager; recorded as D21. The slot's offset and budget remain for the stage 1 lane.
3. #640's body still shows 34.2k, 26.9k and 20.7k (640-a720j, Read this first, 3). Unchanged.
4. Exact-head long gates apply when the PR is ready: AREA_BUDGET.md and MAILBOX_SPLIT.md are gate-read (640-a720j, Read this first, 4). Unchanged.
5. The UART buffer rests on the 2.0 ms per-pass share, S2b's unmerged rule (640-a720j, section 3). Unchanged.
6. Coverage: every touched scope is Conformance and Docs. No RTL, firmware, generator, gate or configuration file changed.
7. New: D21 is numbered by me (Read this first, 1); the reviewer may prefer another label.

## Evidence (./evidence)

| File | What |
|---|---|
| taken.md, taken_url.txt | The TAKEN text as posted, and its URL |
| review_ready.md, review_ready_url.txt | The REVIEW READY text as posted, and its URL |
| style_touched.py | check_doc_style's analyze() over every changed block of a page against a base |
| service_bounds_arm.py | Runs MAILBOX_SPLIT.md's gate reader on the clone |
| write_handoff.py, make_pr_body.py | Build this file and PR-BODY.md |
| gates/ | Every step's log and rc, run_all.out, run_all.sh, run_gates.sh, setup_clone.sh; LARGE_LOGS.txt |
| SHA256SUMS | Digests of every file above |

## Not done / not allowed

No push, PR creation or edit, merge, rebase, sub-agent, bench, flashing or Vivado. No existing comment edited. Only TAKEN and REVIEW READY posted on #640.
"""
(OUT / "HANDOFF.md").write_text(body, encoding="utf-8")
print("written;", summary)
