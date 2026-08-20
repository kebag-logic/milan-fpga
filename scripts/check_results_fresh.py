#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Gate: a committed `TEST_RESULTS.md` says what the campaign actually produces.

`tb/verilator/tsn_fuzz/` writes its verdict into the folder of the RTL it
validates, so a reader of a block sees that block's verification status in
place. The file says "Do not hand-edit" because it is generated - but nothing
made the committed copy and a fresh run agree, and on 2026-08-19 they stopped
agreeing without anybody noticing.

The mechanism is worth stating, because it is not the one people expect. The
gPTP artifact claimed `355 pass, 0 fail`; a fresh run at the CI-pinned tsn-gen
rev produced `353 pass, 0 fail`. Zero failures either way, so no test went red
and no sweep went red. What happened is that the field oracle moved underneath
the campaign: two tsn-gen model fields lost their `expected:` pin for good
spec reasons, and `grade_tx()` skips any field with no constraint. Two checks
simply stopped being graded. A stale evidence file that still reads **PASS** is
the worst shape this can take, because it answers the question a reader came to
ask, confidently, with a number that is no longer true.

This is the same contract `gen_module_matrix.py --check` enforces for
`docs/traceability/MODULE_MATRIX.md`, applied to the artifacts the campaigns
write. It is deliberately modelled on that gate.

TWO THINGS THIS GATE HAS TO GET RIGHT, and both are ways a naive version lies:

  * **The timestamp.** The artifact embeds its generation time, so a byte
    comparison would go red on every single run for a reason that means
    nothing. That is not hypothetical: on the day this gate was written the
    sibling AAF artifact was substantively current and differed from its
    committed copy in the timestamp alone. So the comparison is on SUBSTANCE -
    the trailing `· YYYY-MM-DD HH:MM` is normalised away on both sides, and
    everything else, counts and sections and gaps alike, is compared exactly.

  * **The honest skip.** The campaigns need tsn-gen and SKIP cleanly when it is
    absent, which means there is no fresh artifact to compare against. A gate
    that returned 0 there would be reporting "the committed copy is fresh" on
    the strength of having checked nothing. So absence is reported as a SKIP
    that says WHY, and never as a pass. The suite stays countable on a machine
    without tsn-gen through the traceability floor, not through this gate
    pretending.

The freshness verdict is guarded in turn: the artifact's own headline tally
must equal the tally in the log of the run being judged. Without that, the gate
would happily compare a committed copy against a stale file left on disk by
some earlier run and call the pair fresh. That check is what makes "fresh"
mean "produced by the run whose log I was handed" rather than "present".

Usage:
    python3 scripts/check_results_fresh.py --log <campaign.out> \\
                                           --artifact <TEST_RESULTS.md> \\
                                           [--label <name>]
    python3 scripts/check_results_fresh.py --self-test

Exit status: 0 fresh or honestly skipped, 1 stale or unverifiable.
"""
import argparse
import difflib
import os
import re
import subprocess
import sys

#: The generation stamp the report writer appends to its headline. Stripping it
#: is the whole reason this gate is not a `git diff --exit-code`.
STAMP_RE = re.compile(r"[ \t]*·[ \t]*\d{4}-\d{2}-\d{2}[ \t]+\d{2}:\d{2}[ \t]*$")

#: The artifact headline: `**PASS** - N pass, M fail, K known gaps  ·  <stamp>`.
ART_TALLY_RE = re.compile(
    r"^\*\*(?:PASS|FAIL)\*\*.*?(\d+)\s+pass,\s*(\d+)\s+fail,\s*(\d+)\s+known gaps")

#: The campaign's own closing line: `== <title>: N pass, M fail, K known gaps ==`.
LOG_TALLY_RE = re.compile(
    r"^==.*?:\s*(\d+)\s+pass,\s*(\d+)\s+fail,\s*(\d+)\s+known gaps\s*==\s*$",
    re.M)

#: One row of the `## Sections` table: a name then pass, fail and gap counts.
SECTION_ROW_RE = re.compile(
    r"^\|.*?\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*$")

#: The suite-wide marker a campaign prints when its optional dependency is
#: absent. Same token `scripts/suite_tally.py` reads, on purpose: one spelling
#: of "this did not run" for the whole suite.
SKIP_RE = re.compile(r"^[ \t]*SUITE-SKIP:[ \t]*(\S.*?)[ \t]*$", re.M)

OK, STALE, SKIP, UNVERIFIABLE = "OK", "STALE", "SKIP", "UNVERIFIABLE"


def strip_stamp(text):
    """Drop the generation timestamp from the headline, keep every other byte.

    Scoped to the headline deliberately. The stamp is a property of ONE line -
    the report writer appends it to the verdict and nowhere else - so a
    normaliser willing to strip a trailing stamp from any line is broader than
    the thing it is modelling, and every byte it is willing to discard is a
    byte this gate would stop comparing. A section row that happened to end in
    that shape would be silently equalised.
    """
    out = []
    for line in text.splitlines():
        if ART_TALLY_RE.match(line):
            line = STAMP_RE.sub("", line)
        out.append(line)
    return "\n".join(out)


def section_sums(text):
    """Column totals of the `## Sections` table, or None when there is none.

    Scoped to that one table by heading, not by row shape, so another table
    with three numeric columns cannot be swept into the total.
    """
    rows, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line.strip() == "## Sections"
            continue
        if not inside:
            continue
        m = SECTION_ROW_RE.match(line)
        if m:
            rows.append(tuple(int(g) for g in m.groups()))
    return tuple(sum(c) for c in zip(*rows)) if rows else None


def _tally(regex, text, multiline=False):
    m = regex.search(text) if multiline else None
    if m is None:
        for line in text.splitlines():
            m = regex.match(line)
            if m:
                break
        else:
            return None
    return tuple(int(g) for g in m.groups())


def artifact_tally(text):
    return _tally(ART_TALLY_RE, text)


def log_tally(text):
    m = LOG_TALLY_RE.search(text)
    return tuple(int(g) for g in m.groups()) if m else None


def verdict(log, fresh, committed, label="artifact"):
    """Judge one artifact. Returns (code, [lines to print]).

    Pure: it takes the three texts and no filesystem, so the self-test can
    drive every arm of it without a repository, a campaign or a clock.
    `committed` is None when the artifact is not committed at all.
    """
    skip = SKIP_RE.search(log or "")
    lt = log_tally(log or "")
    # A TALLY OUTRANKS A SKIP MARKER, and the order here is the whole content
    # of that rule. Read the other way round - marker first, whole log searched
    # - a log carrying a real tally AND a stray SUITE-SKIP line exits 0 while
    # printing "the campaign did not run", which is a false statement about
    # what happened from a gate whose entire job is not making false statements
    # about what happened. It is unreachable today, because both emitters
    # sys.exit(0) before a tally can be printed, but "unreachable" is a fact
    # about today's callers and not a property of this function. The tally is
    # positive evidence of a run; the marker is an explanation for its absence.
    # So the marker is only believed when there is an absence to explain.
    if skip and lt is None:
        return SKIP, [
            "SUITE-SKIP: %s freshness not checked (%s)" % (label, skip.group(1)),
            "  the campaign did not run, so there is no fresh result to compare;",
            "  this is NOT a statement that the committed copy is current."]

    if lt is None:
        return UNVERIFIABLE, [
            "CANNOT VERIFY %s: the campaign log carries neither a tally nor a"
            % label,
            "  SUITE-SKIP: line, so there is no evidence it ran. Refusing to",
            "  call the committed copy fresh on the strength of nothing."]

    if fresh is None:
        return UNVERIFIABLE, [
            "CANNOT VERIFY %s: the campaign reported %d pass, %d fail, %d known"
            % ((label,) + lt),
            "  gaps but wrote no artifact at all."]

    at = artifact_tally(fresh)
    if at is None:
        return UNVERIFIABLE, [
            "CANNOT VERIFY %s: no `**PASS**/**FAIL** - N pass, M fail, K known"
            % label,
            "  gaps` headline in the artifact, so it cannot be tied to a run."]
    if at != lt:
        return UNVERIFIABLE, [
            "CANNOT VERIFY %s: it holds %d pass, %d fail, %d known gaps but the"
            % ((label,) + at),
            "  run being judged reported %d pass, %d fail, %d known gaps." % lt,
            "  The file on disk is not this run's output - it is a leftover, and",
            "  comparing the committed copy against it would prove nothing."]

    # THE ARTIFACT MUST ALSO AGREE WITH ITSELF. Tying the headline to the log
    # proves the file came from this run; it says nothing about whether the
    # rest of the file describes that run. The sections table is the part a
    # reader actually reads - the headline says whether to worry, the table
    # says where - and a file whose columns do not add up to its own verdict is
    # not a record of anything, however fresh. Both real artifacts sum exactly
    # today (353 over 15 rows, 164 over 8), so this is a live invariant and not
    # an aspiration. A campaign with no sections table simply has nothing to
    # check here.
    ss = section_sums(fresh)
    if ss is not None and ss != at:
        return UNVERIFIABLE, [
            "CANNOT VERIFY %s: its headline says %d pass, %d fail, %d known"
            % ((label,) + at),
            "  gaps, but its own section rows add up to %d pass, %d fail, %d"
            % ss,
            "  known gaps. The file disagrees with itself, so neither number is",
            "  evidence and comparing it against the committed copy would only",
            "  decide which of the two inconsistent files is on disk."]

    if committed is None:
        return STALE, [
            "STALE %s: generated but never committed." % label,
            "  A generated evidence file that only exists on the author's disk",
            "  tells a reader of the tree nothing. Commit it."]

    a, b = strip_stamp(committed), strip_stamp(fresh)
    if a == b:
        return OK, []

    diff = list(difflib.unified_diff(
        a.splitlines(), b.splitlines(),
        fromfile="committed/%s" % label, tofile="fresh/%s" % label, lineterm=""))
    ct = artifact_tally(committed)
    head = ["STALE %s: the committed copy is not what the campaign produces."
            % label]
    if ct and ct != at:
        head.append(
            "  committed says %d pass, %d fail, %d known gaps; a fresh run says"
            % ct)
        head.append("  %d pass, %d fail, %d known gaps." % at)
        if ct[1] == at[1]:
            head.append(
                "  Failures are unchanged, so checks were ADDED or LOST rather")
            head.append(
                "  than broken - account for each one before regenerating.")
    else:
        head.append("  The counts agree; the difference is elsewhere below.")
    head.append("  The timestamp is normalised away, so this difference is real.")
    head.append("  Regenerate it: cd tb/verilator/tsn_fuzz && make")
    return STALE, head + [""] + ["  " + d for d in diff]


def committed_copy(path):
    """The tracked content of `path`, or None when it is not committed.

    Raises `LookupError` when git cannot answer at all (no metadata, as in an
    extracted tarball), which the caller turns into an honest skip rather than
    a verdict.
    """
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    inside = subprocess.run(["git", "-C", root, "rev-parse", "--git-dir"],
                            capture_output=True, text=True)
    if inside.returncode != 0:
        raise LookupError("no git metadata under %s" % root)
    rel = os.path.relpath(os.path.abspath(path), root)
    show = subprocess.run(["git", "-C", root, "show", "HEAD:%s" % rel],
                          capture_output=True, text=True)
    return show.stdout if show.returncode == 0 else None


def read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return None


def check(log_path, artifact_path, label):
    log = read(log_path)
    if log is None:
        print("CANNOT VERIFY %s: no campaign log at %s" % (label, log_path))
        return 1
    fresh = read(artifact_path)
    try:
        committed = committed_copy(artifact_path) if fresh is not None else None
    except LookupError as exc:
        print("SUITE-SKIP: %s freshness not checked (%s)" % (label, exc))
        print("  there is no committed copy to compare against without git;")
        print("  this is NOT a statement that the committed copy is current.")
        return 0
    code, lines = verdict(log, fresh, committed, label)
    for line in lines:
        print(line)
    if code == OK:
        print("campaign artifact freshness (%s): 1 checks: 1 PASS, 0 FAIL"
              % label)
    return 1 if code in (STALE, UNVERIFIABLE) else 0


# --------------------------------------------------------------- self-test
#
# A checker that cannot fail is not a gate. Each case below is one way the
# real thing has to behave, and several are ways a careless version would
# report a green it did not earn.
#
# The arms are also the gate's own mutation coverage, so each property gets one
# that names it. Three exist because a review mutation-tested this file and
# found the stamp normaliser was the one property nothing pinned: un-anchoring
# STAMP_RE changed no arm's verdict. `stamp shape off the headline` and `stamp
# not at end of line` close that, one per way the normaliser can be made too
# permissive.


def art(stamp, boot=23, total=353, gaps=9, tail=""):
    """A fixture artifact whose section rows always add up to its headline.

    Coherence is built in rather than typed out, because the gate now asserts
    it: a fixture that did not add up would fail every arm for a reason none of
    them is about.
    """
    return ("<!--\nSPDX-FileCopyrightText: 2026 Kebag Logic\n-->\n"
            "# gPTP/802.1AS field campaign (tsn-gen driven)\n\n"
            # The headline reproduces the report writer's own punctuation
            # verbatim, U+2014 and U+00B7 included. That is deliberate: a
            # fixture that tidied them would stop exercising the real parse,
            # and the stamp stripper keys on that middle dot.
            "**PASS** — %d pass, 0 fail, %d known gaps  ·  %s\n\n"
            "## Sections\n\n"
            "| section | pass | fail | gaps |\n"
            "|---|---:|---:|---:|\n"
            "| boot: the first Pdelay_Req | %d | 0 | 0 |\n"
            "| everything else | %d | 0 | %d |\n%s"
            % (total, gaps, stamp, boot, total - boot, gaps, tail))


LOG = "== gPTP/802.1AS field campaign (tsn-gen driven): %s ==\n"
RAN = LOG % "353 pass, 0 fail, 9 known gaps"
T1, T2 = "2026-08-20 09:41", "2026-08-19 21:09"

SELFTEST = [
    ("identical", RAN, art(T1), art(T1), OK),
    # THE reason this gate is not a byte comparison.
    ("timestamp moved only", RAN, art(T1), art(T2), OK),
    # A section row moved while the headline did not: the counts alone are not
    # the artifact, so the whole substance is compared.
    ("section row differs", RAN, art(T1, boot=23), art(T2, boot=24), STALE),
    # The defect this gate was written for.
    ("headline count differs", RAN, art(T1, boot=23, total=353),
     art(T2, boot=24, total=355), STALE),
    ("never committed", RAN, art(T1), None, STALE),
    # tsn-gen absent: honest skip, never a pass.
    ("campaign skipped", "SUITE-SKIP: gPTP campaign (tsn-gen absent)\n",
     None, art(T2), SKIP),
    # ...but a skip marker never outranks evidence that the campaign DID run.
    # Without the log_tally guard this returns SKIP and exits 0 while printing
    # "the campaign did not run", over a log that plainly says it did.
    ("stray skip beside a tally",
     RAN + "SUITE-SKIP: some unrelated leg (dep absent)\n",
     art(T1), art(T1), OK),
    # The stamp is a property of ONE line. A normaliser that strips a trailing
    # stamp from any line would equalise this pair and call it fresh.
    ("stamp shape off the headline", RAN,
     art(T1, tail="Regenerated  ·  2026-08-20 09:41\n"),
     art(T2, tail="Regenerated  ·  2026-08-19 21:09\n"), STALE),
    # ...and it is a TRAILING stamp. Un-anchor STAMP_RE and the stamp below is
    # stripped out of the middle of the headline, equalising a real difference.
    ("stamp not at end of line", RAN,
     art(T1).replace("  ·  %s\n" % T1, "  ·  %s  (rerun)\n" % T1),
     art(T2).replace("  ·  %s\n" % T2, "  ·  %s  (rerun)\n" % T2), STALE),
    # Silence is not evidence of a run.
    ("log says nothing", "== gPTP campaign ==\nsome noise\n",
     art(T1), art(T1), UNVERIFIABLE),
    # A leftover file that happens to match the committed copy must NOT be
    # allowed to vouch for it.
    ("artifact is a leftover", RAN, art(T2, boot=24, total=355),
     art(T2, boot=24, total=355), UNVERIFIABLE),
    # An artifact that contradicts itself is not a record, however fresh.
    ("sections do not sum", RAN,
     art(T1).replace("| everything else | 330 |", "| everything else | 331 |"),
     art(T2), UNVERIFIABLE),
    ("campaign wrote nothing", RAN, None, art(T2), UNVERIFIABLE),
    ("artifact has no headline", RAN, "# a report with no tally\n",
     "# a report with no tally\n", UNVERIFIABLE),
]


def self_test():
    bad = 0
    for name, log, fresh, committed, want in SELFTEST:
        got, _ = verdict(log, fresh, committed, "selftest")
        ok = got == want
        bad += not ok
        print("  [%s] %-26s want %-12s got %s"
              % ("ok" if ok else "FAIL", name, want, got))
    n = len(SELFTEST)
    print("check_results_fresh self-test: %d checks: %d PASS, %d FAIL"
          % (n, n - bad, bad))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--log", help="stdout of the campaign run being judged")
    ap.add_argument("--artifact", help="the TEST_RESULTS.md it writes")
    ap.add_argument("--label", help="name for the artifact in messages")
    ap.add_argument("--self-test", action="store_true",
                    help="prove the gate can fail, then exit")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.log or not args.artifact:
        ap.error("--log and --artifact are both required")
    return check(args.log, args.artifact,
                 args.label or os.path.basename(os.path.dirname(
                     os.path.dirname(os.path.abspath(args.artifact)))))


if __name__ == "__main__":
    sys.exit(main())
