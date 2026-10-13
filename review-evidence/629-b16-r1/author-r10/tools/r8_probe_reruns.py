#!/usr/bin/env python3
"""Lane B16, round 8: the reviews' published probes, run unchanged against this packet's check (offline).

usage: <parser python> r8_probe_reruns.py <repo> <packet root> <probes dir> <scratch dir> <page commit>

Round 7's r7_probe_reruns.py with round 8's probes added, and one interpreter for all: the check now reads
its text through the pinned Markdown parser, so this tool runs under <parser python>, an interpreter with
tools/markdown/requirements.txt installed by hash, and runs every probe, and so the check, under it. The
added probes, copied unchanged from the same branch: R624-7's scripts/probe_r624_7_markdown_escapes.py
(image syntax and other Markdown that renders no character, between an identifier's digit and a unit) and
scripts/probe_r624_7_invisible.py (invisible format characters there), and R625-7's probe_markup.py
(markup in the index row's lane B16 part and on the page). What this tool reads from them:
  * R624-7's escape probe: each form's exit status, and the forms that escape (a reader sees a digit run
    before a unit and the check exits 0);
  * R624-7's invisible probe: each form's exit status;
  * R625-7's markup probe: each case's exit status, what the check names MARKUP and UNCOVERED at the
    case's line, whether both receipts were written, and whether the check raised an exception.
Results go to r8/<review>-probe-rerun.json.

Round 7's docstring follows.

Lane B16, round 7: the reviews' published probes, run unchanged against this packet's check (offline).

usage: r7_probe_reruns.py <repo> <packet root> <probes dir> <scratch dir> <page commit> <renderer python>

Round 6's r6_probe_reruns.py with round 7's probes added: R625-6's scripts/probe_rendered_comment.py and
scripts/probe_followers.py, and R624-6's probe_r624_6_escapes.py and probe_row3200_polls.py, copied
unchanged from the same branch. R625-6's rendered-comment probe imports the pinned renderer (cmarkgfm and
html5lib), so it runs under <renderer python>, an interpreter with tools/markdown/requirements.txt
installed by hash; the probe runs the check under that interpreter too. What this tool reads from them:
  * R625-6's rendered-comment probe: the exit statuses of its six forms, the probe's own exit status (its
    last assertion states the statuses before the fix, so it fails once they change), and for each form
    the lines the check names MARKUP and the numbers it names UNCOVERED at the form's line;
  * R625-6's follower probe: each form's exit status;
  * R624-6's escape probe: each form's exit status, and the forms that do not meet the probe's expectation;
  * R624-6's poll-count probe: whether the poll-count row of line 3200 turned MISMATCH.
Results go to r7/<review>-probe-rerun.json.

Round 6's docstring follows.

Round 5's r5_probe_reruns.py with round 6's probes added. The probes are the reviews' own scripts, copied
unchanged into <probes dir> from the branch 629-b16-review-evidence: R624-4's tools/probe_escape_forms.py,
R625-4's probe_coverage.py and R625-3's probe_figure_coverage.py, as in round 5; and R624-5's
scripts/probe_row3200.py and scripts/probe_r624_5_escapes.py and R625-5's probe_comment_separator.py. Each
is refused unless its SHA-256 equals the published one. Each runs with its own arguments and writes its
own results file, kept verbatim under "results" in r6/<review>-probe-rerun.json with the probe's exit
status and what this tool reads from it:
  * R624-4, R625-4, R625-3: a form is detected as the probe defines it (the check exits 1 and names it);
  * R624-5's row probe: the rows of the terms table's line, and whether its LOCKED row turned MISMATCH;
  * R624-5's escape probe: each form's detection, and which forms put an identifier before a word or a
    mark (its 'id+' forms) or a word for a number (its 'word:' forms, which name no digit to detect);
  * R625-5's comment probe: the exit statuses of its three forms, and the probe's own exit status.
Nothing on the bench is read or written.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO, PACKET, PROBES, SCRATCH = (Path(a).resolve() for a in sys.argv[1:5])
COMMIT = sys.argv[5]
PAGE = REPO / "docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"
CHK = PACKET / "tools/check_b16_figures.py"


def named(stdout, line, kind):
    """What the check names at a line: the MARKUP texts, or the UNCOVERED numbers."""
    return [x.split(" ", 2)[2].split(" (")[0] for x in stdout.splitlines() if x.startswith(kind + " ")
            and x.split(" ")[1].endswith(f":{line}")]


PROBE = {  # name: (file, published SHA-256, published path, argv after the script, its results file, reading)
    "r624-4": ("probe_escape_forms.py", "5c2dbc691e469d236227bc90d4d131ad1fc116f0b002813c02beef2374ae3c26",
               "R624-4/tools/probe_escape_forms.py", lambda o: [REPO, PACKET, o / "scratch", o / "out.json"],
               lambda o: o / "out.json", lambda r: dict(forms=len(r), detected=sum(x["detected"] for x in r))),
    "r625-4": ("probe_coverage.py", "e8749cbecfe73ef6f07261d1416122094d51745954a62fa6851d4e0521dfd0fb",
               "R625-4/probe_coverage.py", lambda o: [REPO, PACKET, o],
               lambda o: o / "coverage-probes.json", lambda r: dict(forms=len(r), detected=sum(x["rc"] == 1 for x in r))),
    "r625-3": ("probe_figure_coverage.py", "f4c4d91bdfea9b6428e3e5a587ba87577003cc9e67ba08c852149d2ec3cddb32",
               "R625-3/scripts/probe_figure_coverage.py and R625-4/probe_figure_coverage.py", lambda o: [REPO, PACKET, o],
               lambda o: o / "receipts/figure-coverage-probes.json",
               lambda r: dict(forms=len(r), detected=sum(x["detected"] for x in r))),
    "r624-5-row3200": ("probe_row3200.py", "11188752c3a8b4c9607102bc243163cb617edcde41db8a3125eb66cb8f15409d",
                       "R624-5/scripts/probe_row3200.py", lambda o: [REPO, PACKET, o / "scratch", o / "out.json"],
                       lambda o: o / "out.json",
                       lambda r: dict(row3200_insensitive=r["row3200_insensitive"],
                                      row3200=[(x["row"], x["receipt"], x["recomputed"], x["status"]) for x in r["rows"]
                                               if x["line"] == "3200"])),
    "r624-5-escapes": ("probe_r624_5_escapes.py", "c7ea04fb719dc0ef8d3e277cffd7c9b843304443f7dbf2cc97935163351b4b26",
                       "R624-5/scripts/probe_r624_5_escapes.py", lambda o: [REPO, PACKET, o / "scratch", o / "out.json"],
                       lambda o: o / "out.json",
                       lambda r: dict(forms=len(r["probes"]), detected=sum(x["detected"] for x in r["probes"]),
                                      id_forms=sum(x["probe"].startswith("id+") for x in r["probes"]),
                                      id_detected=sum(x["detected"] for x in r["probes"] if x["probe"].startswith("id+")),
                                      not_detected=[x["probe"] for x in r["probes"] if not x["detected"]])),
    "r625-5-comment": ("probe_comment_separator.py", "d799fce3787e5577d916b931b895e093cec8e74b76bd64b2691febae27009735",
                       "R625-5/probe_comment_separator.py", lambda o: [REPO, PACKET, o],
                       lambda o: o / "receipts/comment-probe.json",
                       lambda r: dict(statuses=[x["rc"] for x in r], names=[x["name"] for x in r])),
    "r625-6-rendered": ("probe_rendered_comment.py", "22c38feb3cd3cac780bf5a2f299716b125047c9703df0b60dbe54beccc3aed57",
                        "R625-6/scripts/probe_rendered_comment.py", lambda o: [REPO, PACKET, o],
                        lambda o: o / "receipts/rendered-comment.json",
                        lambda r: dict(versions=r["versions"], statuses=[x["rc"] for x in r["results"]],
                                       names=[x["name"] for x in r["results"]],
                                       markup=[named(x["stdout"], x["source_line"], "MARKUP") for x in r["results"]],
                                       uncovered=[named(x["stdout"], x["source_line"], "UNCOVERED") for x in r["results"]])),
    "r625-6-followers": ("probe_followers.py", "6703a34616f606f2be81d943646a1022fd6e8070d273f4aaaa459cf29a0e451b",
                         "R625-6/scripts/probe_followers.py", lambda o: [REPO, PACKET, o],
                         lambda o: o / "receipts/own-followers.json",
                         lambda r: dict(forms=len(r), statuses={x["name"]: x["rc"] for x in r},
                                        markup={x["name"]: named(x["stdout"], x["line"], "MARKUP") for x in r
                                                if named(x["stdout"], x["line"], "MARKUP")})),
    "r624-6-escapes": ("probe_r624_6_escapes.py", "f4c9d523e6ea15f87e160768c61dc5229f51306dd1f4429984e7e380a27facc2",
                       "R624-6/probe_r624_6_escapes.py", lambda o: [CHK, PAGE, PACKET, REPO, o / "scratch", o / "out.json"],
                       lambda o: o / "out.json",
                       lambda r: dict(forms=len(r), expect_fail=sum(x["expect"] == "fail" for x in r),
                                      fail_detected=sum(x["detected"] for x in r if x["expect"] == "fail"),
                                      not_meeting=[x["probe"] for x in r if not x["meets_expectation"]],
                                      any_statuses={x["probe"]: x["rc"] for x in r if x["expect"] == "any"})),
    "r624-6-row3200-polls": ("probe_row3200_polls.py", "13a323fd7a4609309fb900b2c654d8bcbacaf21e8646a4b703e709990bb5c3e5",
                             "R624-6/probe_row3200_polls.py", lambda o: [CHK, PAGE, PACKET, REPO, o / "work", o / "out.json"],
                             lambda o: o / "out.json",
                             lambda r: dict(row3200_polls_detected=r["row3200_polls_detected"],
                                            rows=[(x["row"], x["line"], x["recomputed"], x["status"]) for x in r["rows"]])),
    "r624-7-escapes": ("probe_r624_7_markdown_escapes.py", "4366f8caa9b6d320a515fa73a49d3e0fda80f77f35dbae5b781a7d529e627d29",
                       "R624-7/scripts/probe_r624_7_markdown_escapes.py",
                       lambda o: [REPO, PACKET, o / "work", o / "out.json"], lambda o: o / "out.json",
                       lambda r: dict(forms=len(r["forms"]), escaping=[x["name"] for x in r["forms"] if x["escapes"]],
                                      statuses={x["name"]: x["rc"] for x in r["forms"]},
                                      markup={x["name"]: [y.split(" (")[0] for y in x["named_at_or_near_line"]
                                                          if y.startswith("MARKUP ")] for x in r["forms"]})),
    "r624-7-invisible": ("probe_r624_7_invisible.py", "ef5ebaae7fc5cda62c98993c7bb1f4bdeb1ea98617950b0eba8cfb830d439e9f",
                         "R624-7/scripts/probe_r624_7_invisible.py",
                         lambda o: [REPO, PACKET, o / "work", o / "out.json"], lambda o: o / "out.json",
                         lambda r: dict(forms=len(r), statuses={x["form"]: x["rc"] for x in r})),
    "r625-7-markup": ("probe_markup.py", "d23a4cb52d0f4616efcad37a3f10620190bdf61e97a7eba3779cccf8769e691d",
                      "R625-7/probe_markup.py", lambda o: [REPO, PACKET, o], lambda o: o / "receipts/own-markup.json",
                      lambda r: dict(cases=len(r), statuses={x["name"]: x["rc"] for x in r},
                                     index={x["name"]: dict(rc=x["rc"], markup=named(x["stdout"], x["line"], "MARKUP"),
                                                            uncovered=named(x["stdout"], x["line"], "UNCOVERED"),
                                                            receipts=x["rows_written"] and x["coverage_written"],
                                                            exception="Traceback" in x["stderr"])
                                            for x in r if x["name"].startswith("index-")},
                                     all_receipts=all(x["rows_written"] and x["coverage_written"] for x in r),
                                     exceptions=sum("Traceback" in x["stderr"] for x in r))),
}


def main() -> int:
    ok = True
    for name, (script, want, where, argv, res, read) in PROBE.items():
        p = PROBES / script
        got = hashlib.sha256(p.read_bytes()).hexdigest()
        assert got == want, f"{script}: SHA-256 {got}, published {want}"
        o = SCRATCH / name
        (o / "receipts").mkdir(parents=True, exist_ok=True)
        (o / "scratch").mkdir(parents=True, exist_ok=True)
        run = subprocess.run([sys.executable, "-I", str(p), *map(str, argv(o))], capture_output=True, text=True,
                             timeout=1200)
        results = json.loads(res(o).read_text())
        got_ = read(results)
        out = dict(note=f"Lane B16 round 8: {name.upper()}'s published probe, {where} under "
                        "review-evidence/629-b16-r1/reviews/ on branch 629-b16-review-evidence, run unchanged against "
                        f"this packet's check and the page at {COMMIT[:8]}; its own results file, verbatim, under "
                        "'results'. Offline, no bench action",
                   probe=script, probe_sha256=got, page_commit=COMMIT, exit=run.returncode, reading=got_,
                   results=results)
        (PACKET / f"r8/{name}-probe-rerun.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
        print(name, "exit", run.returncode, json.dumps(got_))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
