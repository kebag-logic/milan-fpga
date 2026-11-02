"""Write HANDOFF.md for [A720m]. The gate table is read from the logs; the step list is 640-a720l's (from 640-a720j's)."""
import ast, subprocess
from pathlib import Path

OUT = Path("$MANAGEMENT/2026-09-23/640-a720m")
G = Path("$VALIDATION_STORAGE/640-a720m/gates")
LANE = "$LANES/640-mark2-charter"
J = Path("$MANAGEMENT/2026-09-23/640-a720j/evidence/write_handoff.py").read_text()
src = J[J.index("STEPS = ["):]
src = src[:src.index("\n]\n") + 3]
STEPS = ast.literal_eval(src.split("=", 1)[1].strip())
STEPS = [s if s[2] != "style_touched" else ("(lane)", "style on changed blocks", "style_touched",
         "check_doc_style's `analyze()` on every changed block of the 4 pages against 503bc97c, and of this round's page against 30eb4834") for s in STEPS]
STEPS += [
    ("(lane)", "census coverage", "census_coverage", "`census_coverage.py` over the basis hierarchy, CSR map and placed rows, and the split-only parts"),
    ("(lane)", "census coverage control", "census_coverage_control", "`! census_coverage.py` against the round 1 page (3f8ed303): rc 0 means the check failed there, as it must"),
]
git = lambda *a: subprocess.run(["git", "-C", LANE, *a], capture_output=True, text=True, check=True).stdout.strip()
head, tree = git("rev-parse", "HEAD"), git("rev-parse", "HEAD^{tree}")
commits = [l.split("\t") for l in git("log", "--reverse", "--format=%H\t%s", "30eb4834..HEAD").splitlines()]
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
ctab = "\n".join(f"| {i} | {h} | {s} |" for i, (h, s) in enumerate(commits, 13))
start = (G / "run_all.start").read_text().strip()
end = (G / "run_all.end").read_text().strip() if (G / "run_all.end").exists() else "pending"
status = "REVIEW READY" if not bad and RR != "pending" else ("GATES DONE, REVIEW READY pending" if not bad else "GATES INCOMPLETE")
body = (OUT / "evidence/handoff_body.md").read_text(encoding="utf-8")
body = body.format(status=status, summary=summary, head=head, tree=tree, taken=TAKEN, rr=RR, ctab=ctab,
                   rows=rows, start=start, end=end, nsteps=len(STEPS))
(OUT / "HANDOFF.md").write_text(body, encoding="utf-8")
print(status, summary, len(STEPS))
