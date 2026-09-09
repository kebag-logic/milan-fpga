#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The acquisition-layer self-test for `check_merge_review_integrity.py`.

WHY THIS EXISTS (issue #426). The pure cases in the checker hand `assess_pr`
complete event arrays by hand, so they cannot see the defect that actually
merged PR #425: the arrays were a PREFIX of the history and nothing said so.
These arms drive the SHIPPED acquisition adapter over mocked `gh` responses and
then the SHIPPED, unchanged assessment core, so the property under test is the
whole path from a paginated response to a verdict.

`FakeGh` models the server rather than replaying a canned list. It reads
`first:` and `after:` out of the query it is handed and serves the matching
slice of a node bank, which is why an omitted-pagination regression can be
killed honestly: a query that never advances its cursor gets its first page
again, and that is what this fake returns too.

`selftest(acquire, checker)` takes both modules rather than importing either,
for the reason `merge_containment_selftest` does: the arms patch the very
namespaces `run()` and `fetch_merged_prs()` resolve their helpers from, and
importing by name would build a second copy nothing here could reach.

THE ROSTER IS THE FROZEN CONTROL PLAN. `CASE_NAMES` lists every case by name,
and the meta-arm refuses a run whose executed roster differs from it. A case
lost to an early return, a duplicated name and a silently added arm are all
findings, so the count the checker prints cannot drift from what ran.
"""

import contextlib
import io
import json
import re
import subprocess
import sys
from collections.abc import Callable
from types import ModuleType
from typing import Any, NamedTuple

#: The merge instant every fixture PR uses, and the ordinal-to-clock map for
#: its events: node `i` is stamped `i` minutes after 08:00 on the merge day, so
#: an ordinal is a chronology and 266 of them still land before the merge.
MERGED_AT = "2026-09-08T15:37:15Z"
#: A filler body that decides nothing: `[A<n>]` is an author line, which the
#: verdict grammar deliberately does not match, so bulk never votes.
FILLER = "[A1] routine lane note %d; nothing here decides a merge"
#: An early rejection and the later report that succeeds it, in the corpus
#: dialect the unchanged parser reads.
NEGATIVE = "[R66] NEGATIVE - blockers stand at head 1d5c03cd"
POSITIVE = "[R66] POSITIVE - exact head af501566"

_KINDS = {"comments": ("IC", "createdAt"), "reviews": ("PRR", "submittedAt")}

#: Every case this module runs, frozen before the first control. The meta-arm
#: compares it against the roster that actually executed.
CASE_NAMES = (
    # page boundaries, empty streams, and the terminal forms that exist
    "page-99-single",
    "page-100-exactly-full",
    "page-101-two-pages",
    "three-pages-266",
    "page-200-two-full-pages-no-empty-terminal",
    "terminal-empty-page-accepted",
    "empty-histories-complete",
    "pending-review-null-submitted-at",
    # verdict semantics over complete streams, in BOTH stream types
    "comments-late-positive-clears",
    "comments-late-negative-stands",
    "reviews-late-positive-clears",
    "reviews-late-negative-stands",
    "reviews-late-blocker-open",
    "mixed-streams-chronological",
    "post-merge-positive-cannot-clear",
    "long-introduction-does-not-hide-later-headline",
    "body-closes-open-issue-survives-hydration",
    "review-submitted-at-null-beyond-first-page-clears",
    # acquisition refusals: unknown, never a product finding
    "gh-absent",
    "gh-nonzero-exit",
    "non-json-stdout",
    "slurp-not-a-list",
    "slurp-empty-array",
    "graphql-errors-member",
    "null-pull-request",
    "missing-connection-object",
    "missing-total-count",
    "missing-has-next-page",
    "node-missing-body",
    "node-missing-id",
    "comment-missing-created-at",
    "duplicate-node-id",
    "total-count-changed",
    "lost-page-short-population",
    "unterminated-final-page",
    "mid-stream-terminal-page",
    "repeated-end-cursor",
    "empty-non-terminal-page",
    "page-bound-exceeded",
    "command-timeout",
    "acquisition-deadline-expired",
    "reviews-stream-failure-refuses",
    "refusal-retains-complete-stderr",
    "refusal-retains-complete-graphql-errors",
    "repository-identity-malformed",
    "non-integer-pr-number",
    "review-submitted-at-absent-refuses",
    # the whole gate, through its real entry points
    "run-clean-exit-0",
    "outer-list-requests-no-nested-projections",
    "run-finding-exit-1",
    "main-incomplete-acquisition-exit-2",
    "prefix-discrimination-anti-vacuity",
    "outer-window-and-limit-preserved",
    "repository-identity-resolved-once",
    "main-absent-review-timestamp-exit-2",
    "main-refusal-diagnostic-complete-exit-2",
    # a repository response that is not an object at all, end to end
    "repository-identity-array-refuses-exit-2",
    "repository-identity-string-refuses-exit-2",
    "repository-identity-number-refuses-exit-2",
    "repository-identity-valid-empty-histories-exit-0",
    "repository-identity-diagnostic-complete",
)


class _Raw(NamedTuple):
    """What a runner returns.

    Spelled here rather than imported so a fake can never be mistaken for the
    shipped `Raw`, and duck-typed on purpose: the adapter reads exactly these
    three attributes and nothing else.
    """

    stdout: str
    stderr: str = ""
    returncode: int = 0


def at(minute: int) -> str:
    """The UTC stamp `minute` minutes after 08:00 on the fixture merge day."""
    return "2026-09-08T%02d:%02d:00Z" % (8 + minute // 60, minute % 60)


def nodes(kind: str, count: int, verdicts: dict[int, str] | None = None,
          times: dict[int, str] | None = None) -> list[dict[str, str]]:
    """`count` fixture nodes of `kind`, with bodies/stamps at 1-based ordinals."""
    prefix, field = _KINDS[kind]
    verdicts, times = verdicts or {}, times or {}
    return [{"id": "%s_%04d" % (prefix, i),
             field: times.get(i, at(i)),
             "body": verdicts.get(i, FILLER % i)}
            for i in range(1, count + 1)]


def connection_of(page: dict[str, Any]) -> dict[str, Any]:
    """The connection object inside one well-formed fixture page."""
    return next(iter(page["data"]["repository"]["pullRequest"].values()))


def page_shape(page: dict[str, Any]) -> tuple[int, bool] | None:
    """(nodes, hasNextPage) for a served page, or None when it is damaged.

    A mutator that removes the connection, its pageInfo or the flag has built
    a page whose shape is undefined by construction. The fake has to be able
    to serve that page without pretending it can describe it, which is why
    this reads defensively where `connection_of` may subscript.
    """
    data = page.get("data") if isinstance(page, dict) else None
    repo = data.get("repository") if isinstance(data, dict) else None
    pull = repo.get("pullRequest") if isinstance(repo, dict) else None
    conn = next(iter(pull.values()), None) if isinstance(pull, dict) else None
    if not isinstance(conn, dict) or not isinstance(conn.get("nodes"), list):
        return None
    info = conn.get("pageInfo")
    if not isinstance(info, dict) or not isinstance(info.get("hasNextPage"),
                                                    bool):
        return None
    return len(conn["nodes"]), info["hasNextPage"]


def response_page(kind: str, total: int, chunk: list[dict[str, str]],
                  more: bool, cursor: str | None) -> dict[str, Any]:
    """One response page in the exact shape `gh api graphql --slurp` emits.

    The nodes are copied out of the bank, so a mutator that damages a served
    page cannot reach back and corrupt the fixture every other arm reads.
    """
    return {"data": {"repository": {"pullRequest": {kind: {
        "totalCount": total,
        "pageInfo": {"hasNextPage": more, "endCursor": cursor},
        "nodes": [dict(node) for node in chunk]}}}}}


class FakeGh:
    """A GitHub stand-in answering `gh` argument arrays from a node bank."""

    def __init__(self, banks: dict[tuple[int, str], list[dict[str, str]]],
                 mutators: dict[tuple[int, str], Callable[[Any], Any]] | None = None,
                 page_cap: int = 12, repo: Any = None) -> None:
        """Serve `banks`; `mutators` damage one connection's built pages, and
        `repo` overrides the identity answer."""
        self.banks = banks
        self.mutators = mutators or {}
        self.page_cap = page_cap
        self.repo = {"owner": {"login": "kebag-logic"}, "name": "milan-fpga"} \
            if repo is None else repo
        self.calls: list[list[str]] = []
        #: (nodes, hasNextPage) per served page, so an arm can pin the exact
        #: terminal form this protocol produces rather than describe it.
        self.shapes: dict[tuple[int, str], list[tuple[int, bool]]] = {}

    def __call__(self, args: list[str], timeout: float) -> _Raw:
        """Answer one gh invocation exactly as the real one would be read."""
        self.calls.append(list(args))
        if args[:2] == ["repo", "view"]:
            return _Raw(json.dumps(self.repo))
        query = next(a[len("query="):] for a in args if a.startswith("query="))
        number = int(next(a[len("number="):] for a in args
                          if a.startswith("number=")))
        kind = "comments" if "comments(" in query else "reviews"
        pages = self._pages(query, number, kind)
        mutate = self.mutators.get((number, kind))
        if mutate is not None:
            pages = mutate(pages)
        if isinstance(pages, _Raw):
            return pages
        self.shapes[(number, kind)] = [page_shape(p) for p in pages]
        return _Raw(json.dumps(pages))

    def pages_served(self, number: int, kind: str) -> int:
        """How many pages the last read of that connection delivered."""
        return len(self.shapes[(number, kind)])

    def _pages(self, query: str, number: int,
               kind: str) -> list[dict[str, Any]]:
        """Paginate one bank the way `--paginate --slurp` accumulates pages.

        The page size comes from the query's own `first:`, and the cursor only
        advances when the query actually spends it: a document that drops
        `after: $endCursor` is served its first page for as long as it keeps
        asking, which is the omitted-pagination failure this suite has to be
        able to see.
        """
        bank = self.banks.get((number, kind), [])
        size = int(re.search(r"first:\s*(\d+)", query).group(1))
        advances = "after: $endCursor" in query
        pages: list[dict[str, Any]] = []
        offset = 0
        while True:
            chunk = bank[offset:offset + size]
            more = offset + len(chunk) < len(bank)
            cursor = "cursor:%s:%d" % (kind, offset + len(chunk)) if more \
                else None
            pages.append(response_page(kind, len(bank), chunk, more, cursor))
            if not more or len(pages) >= self.page_cap:
                return pages
            offset = offset + len(chunk) if advances else 0


def summarize(value: object) -> str:
    """A short description of a value a refusal arm was not supposed to get.

    A hydrated PR carries every body it acquired, so the bare repr of one runs
    to tens of thousands of characters and hides every other finding in the
    report. The stream lengths are what actually identifies the arm.
    """
    if isinstance(value, tuple) and value and isinstance(value[0], dict):
        pr = value[0]
        return "a hydrated PR #%s with %d comment(s) and %d review(s)" % (
            pr.get("number"), len(pr.get("comments") or []),
            len(pr.get("reviews") or []))
    text = repr(value)
    return text if len(text) <= 200 else text[:200] + "... (truncated)"


class Cases:
    """Counts the cases that run and records the ones that disagree."""

    def __init__(self, error: type[BaseException]) -> None:
        """`error` is the acquisition refusal type these arms expect."""
        self.error = error
        self.problems: list[str] = []
        self.names: list[str] = []

    def outcome(self, name: str, thunk: Callable[[], object],
                want: object) -> None:
        """One comparison whose value `thunk` produces.

        The value is produced INSIDE the case so that a regression which makes
        acquisition raise kills exactly the controls it breaks, by name,
        instead of aborting the group and leaving every later arm unreported.
        """
        self.names.append(name)
        try:
            got = thunk()
        except Exception as exc:
            self.problems.append(
                "%s: raised %s: %s" % (name, type(exc).__name__, exc))
            return
        if got != want:
            self.problems.append("%s: got %r, expected %r" % (name, got, want))

    def refuses(self, name: str, call: Callable[[], object],
                expect: str) -> None:
        """`call` must refuse the acquisition, naming `expect` in its reason.

        Any other exception is reported rather than swallowed: an arm that
        dies of a typo would otherwise look exactly like a caught refusal.
        """
        self.names.append(name)
        try:
            got = call()
        except self.error as exc:
            if expect.lower() not in str(exc).lower():
                self.problems.append(
                    "%s: refusal did not name %r: %s" % (name, expect, exc))
            return
        except Exception as exc:
            self.problems.append(
                "%s: expected an acquisition refusal, got %s: %s"
                % (name, type(exc).__name__, exc))
            return
        # An arm that wrongly SUCCEEDS returns a whole hydrated history, and
        # printing it buries the twenty other findings under 266 bodies. The
        # summary says which arm passed data through and how much, which is
        # the fact a reader needs; the case still fails either way.
        self.problems.append(
            "%s: expected a refusal naming %r, got %s"
            % (name, expect, summarize(got)))


class Env(NamedTuple):
    """The two shipped modules under test, and the case reporter."""

    acquire: ModuleType
    checker: ModuleType
    cases: Cases


def hydrated(env: Env, number: int, banks: dict[tuple[int, str], Any],
             fake: FakeGh | None = None) -> tuple[dict[str, Any], FakeGh]:
    """Hydrate one fixture PR through the shipped acquirer; (pr, fake)."""
    fake = fake or FakeGh(banks)
    pr = {"number": number, "mergedAt": MERGED_AT, "body": "x"}
    return env.acquire.Acquirer(runner=fake).hydrate([pr])[0], fake


def reasons(env: Env, pr: dict[str, Any],
            open_issues: set[int] | None = None) -> list[str]:
    """The UNCHANGED assessment core's findings for one hydrated PR."""
    open_set = open_issues or set()
    return [f.reason for f in env.checker.assess_pr(pr, lambda n: n in open_set)]


# ------------------------------------------------- boundaries and terminals

def boundary_cases(env: Env) -> None:
    """Page boundaries, empty streams, and the terminal forms that exist."""
    case = env.cases.outcome

    def paginates(count: int) -> tuple[int, int]:
        """How many comments hydrated, over how many delivered pages."""
        pr, fake = hydrated(env, 1, {(1, "comments"): nodes("comments", count)})
        return len(pr["comments"]), fake.pages_served(1, "comments")

    for name, count, pages in (("page-99-single", 99, 1),
                               ("page-100-exactly-full", 100, 1),
                               ("page-101-two-pages", 101, 2),
                               ("three-pages-266", 266, 3)):
        case(name, lambda c=count: paginates(c), (count, pages))

    # A population that is an exact multiple of the page size ends on a FULL
    # page carrying hasNextPage false; gh stops there and no empty page is
    # ever delivered. "Two full pages then a terminal empty page" is not a
    # form this API produces, so this arm pins the form it does produce
    # instead of asserting a fabricated one.
    def two_full_pages() -> tuple[int, list[tuple[int, bool] | None]]:
        """The hydrated count and the exact page shapes for 200 comments."""
        pr, fake = hydrated(env, 1, {(1, "comments"): nodes("comments", 200)})
        return len(pr["comments"]), fake.shapes[(1, "comments")]

    case("page-200-two-full-pages-no-empty-terminal", two_full_pages,
         (200, [(100, True), (100, False)]))

    # ...and a terminal EMPTY page is still accepted when a server sends one,
    # because it reconciles: no next page, and a total the nodes already meet.
    def add_empty_terminal(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Append the empty terminal page a stricter server might emit."""
        connection_of(pages[-1])["pageInfo"] = {"hasNextPage": True,
                                                "endCursor": "cursor:tail"}
        return pages + [response_page("comments", 100, [], False, None)]

    def empty_terminal() -> tuple[int, tuple[int, bool] | None]:
        """The hydrated count, and the shape of the last page served."""
        bank = {(1, "comments"): nodes("comments", 100)}
        pr, fake = hydrated(env, 1, {},
                            FakeGh(bank, {(1, "comments"): add_empty_terminal}))
        return len(pr["comments"]), fake.shapes[(1, "comments")][-1]

    case("terminal-empty-page-accepted", empty_terminal, (100, (0, False)))

    # An empty history is COMPLETE, not missing: totalCount 0, one page, no
    # node, no next page. It must hydrate to [] and assess to nothing.
    def empty_history() -> tuple[Any, Any, int, list[str]]:
        """Both hydrated streams, the pages served, and the findings."""
        pr, fake = hydrated(env, 1, {})
        return (pr["comments"], pr["reviews"], fake.pages_served(1, "reviews"),
                reasons(env, pr))

    case("empty-histories-complete", empty_history, ([], [], 1, []))

    # A PENDING review carries an EXPLICIT null submittedAt: the member is
    # present, its value null. It normalizes to "" and sorts first, so a later
    # POSITIVE still clears it; an ABSENT member is refused instead.
    def pending_review() -> tuple[str, list[str]]:
        """The normalized stamp, and what the unchanged core makes of it."""
        pending = nodes("reviews", 2, {1: "[R0] NEGATIVE - pending draft",
                                       2: "[R1] POSITIVE - exact head 9812e47d"})
        pending[0]["submittedAt"] = None
        pr, _ = hydrated(env, 1, {(1, "reviews"): pending})
        return pr["reviews"][0]["submittedAt"], reasons(env, pr)

    case("pending-review-null-submitted-at", pending_review, ("", []))


# --------------------------------------------- verdicts over complete streams

def _findings(env: Env, number: int, banks: dict[tuple[int, str], Any],
              body: str | None = None,
              open_issues: set[int] | None = None) -> list[str]:
    """Hydrate one fixture PR and assess it: the reasons the core reports."""
    pr, _ = hydrated(env, number, banks)
    if body is not None:
        pr["body"] = body
    return reasons(env, pr, open_issues)


def stream_cases(env: Env) -> None:
    """Late verdicts, both stream types, mixed order, and the merge cutoff."""
    case = env.cases.outcome

    # The PR #425 shape: an early NEGATIVE inside the first page, both
    # clearing POSITIVE reports past it, at ordinals 215 and 232.
    case("comments-late-positive-clears",
         lambda: _findings(env, 425, {(425, "comments"): nodes(
             "comments", 266, {89: NEGATIVE, 215: POSITIVE,
                               232: "[R65] POSITIVE - exact head af501566"})}),
         [])

    # ...and the same defect in the other direction: a NEGATIVE past the first
    # page, after an early POSITIVE, is a negative merge and not a clean one.
    case("comments-late-negative-stands",
         lambda: _findings(env, 426, {(426, "comments"): nodes(
             "comments", 266, {5: POSITIVE, 215: NEGATIVE})}),
         ["negative-merge"])

    # The same three properties in the OTHER stream. Formal reviews were the
    # connection whose 100-node cap was proved from source rather than
    # observed, so they are exercised exactly as hard as comments.
    for name, verdicts, want in (
            ("reviews-late-positive-clears", {10: NEGATIVE, 130: POSITIVE}, []),
            ("reviews-late-negative-stands", {10: POSITIVE, 130: NEGATIVE},
             ["negative-merge"]),
            ("reviews-late-blocker-open",
             {10: POSITIVE,
              130: "[R0-b] BLOCKER Tests - scripts/x.py:1 - it lies"},
             ["open-blocker"])):
        case(name, lambda v=verdicts: _findings(
            env, 427, {(427, "reviews"): nodes("reviews", 150, v)}), want)

    # Both streams at once, ordered by time across them: the NEGATIVE is a
    # comment on page 3, the clearing POSITIVE a review on page 2.
    case("mixed-streams-chronological",
         lambda: _findings(env, 428, {
             (428, "comments"): nodes("comments", 266, {215: NEGATIVE}),
             (428, "reviews"): nodes("reviews", 150, {130: POSITIVE},
                                     {130: "2026-09-08T14:45:56Z"})}),
         [])

    # A POSITIVE published AFTER the merge is post-merge commentary. Completing
    # the history must not let a fresh positive rewrite a pre-merge rejection.
    case("post-merge-positive-cannot-clear",
         lambda: _findings(env, 429, {(429, "comments"): nodes(
             "comments", 266, {215: NEGATIVE, 260: POSITIVE},
             {260: "2026-09-08T16:10:00Z"})}),
         ["negative-merge"])

    # A very long manager introduction on page 1 must not hide the R-led
    # headline that decides the merge, which here sits on line 23 of a body on
    # page 3 - the shape the retained PR #425 record actually has.
    introduction = "\n".join("[A0] Manager round-up %d" % i for i in range(300))
    late = "\n".join(["Context line %d" % i for i in range(22)] + [POSITIVE])
    case("long-introduction-does-not-hide-later-headline",
         lambda: _findings(env, 430, {(430, "comments"): nodes(
             "comments", 266, {1: introduction, 89: NEGATIVE, 215: late})}),
         [])

    # The linked-issue check is unchanged and still reads the PR BODY, which
    # hydration never touches.
    case("body-closes-open-issue-survives-hydration",
         lambda: _findings(
             env, 431, {(431, "comments"): nodes("comments", 101,
                                                 {101: POSITIVE})},
             "[A1]\n\nCloses #777. Restores the docs gates.", {777}),
         ["open-issue"])

    # An explicit null BEYOND page one normalizes too; the refusal is not
    # about nulls: the later POSITIVE still clears.
    def null_beyond_first_page() -> tuple[str, list[str]]:
        """The stamp hydrated for the null node on page 2, and the findings."""
        bank = nodes("reviews", 150, {110: NEGATIVE, 130: POSITIVE})
        bank[109]["submittedAt"] = None
        pr, _ = hydrated(env, 432, {(432, "reviews"): bank})
        return pr["reviews"][109]["submittedAt"], reasons(env, pr)

    case("review-submitted-at-null-beyond-first-page-clears",
         null_beyond_first_page, ("", []))


# ------------------------------------------------------- acquisition refusals

def _blank_page(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Empty a non-terminal page while it still advertises another."""
    connection_of(pages[0])["nodes"] = []
    return pages


def _drop_last_page(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Lose the final page while still terminating the stream cleanly."""
    kept = pages[:-1]
    connection_of(kept[-1])["pageInfo"]["hasNextPage"] = False
    return kept


def _repeat_cursor(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Serve page 1 the cursor page 0 already spent."""
    connection_of(pages[1])["pageInfo"]["endCursor"] = \
        connection_of(pages[0])["pageInfo"]["endCursor"]
    return pages


def _duplicate_id(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Repeat a node id across two pages, as a non-advancing read would."""
    connection_of(pages[1])["nodes"][0]["id"] = \
        connection_of(pages[0])["nodes"][0]["id"]
    return pages


def _bump_total(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Let the advertised population change under the read."""
    for page in pages[1:]:
        connection_of(page)["totalCount"] += 1
    return pages


def _unterminate(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """End the stream while it still advertises another page."""
    connection_of(pages[-1])["pageInfo"] = {"hasNextPage": True,
                                            "endCursor": "cursor:more"}
    return pages


def _terminate_early(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Advertise the end of the stream on a page that is not the last."""
    connection_of(pages[0])["pageInfo"] = {"hasNextPage": False,
                                           "endCursor": None}
    return pages


def _overlong(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """A stream that never terminates, one page past the adapter's bound."""
    return [response_page("comments", 9999,
                          [{"id": "IC_over_%03d" % index,
                            "createdAt": at(index), "body": FILLER % index}],
                          True, "cursor:over:%d" % index)
            for index in range(101)]


def _drop_field(field: str) -> Callable[[list[dict[str, Any]]],
                                        list[dict[str, Any]]]:
    """A mutator deleting `field` from the first page's connection object."""
    def mutate(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Delete the named field and hand the damaged pages back."""
        del connection_of(pages[0])[field]
        return pages
    return mutate


def _drop_page_info(field: str) -> Callable[[list[dict[str, Any]]],
                                            list[dict[str, Any]]]:
    """A mutator deleting `field` from the first page's pageInfo."""
    def mutate(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Delete the named pageInfo field and hand the pages back."""
        del connection_of(pages[0])["pageInfo"][field]
        return pages
    return mutate


def _drop_node_field(field: str, at: int = 0) -> Callable[
        [list[dict[str, Any]]], list[dict[str, Any]]]:
    """A mutator deleting `field` from node `at` of page `at`.

    -1 is the last node of the LAST page and refuses a single-page stream, so
    the damage it does is provably not a first-page effect.
    """
    def mutate(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Delete the named node field and hand the damaged pages back."""
        if at and len(pages) < 2:
            raise AssertionError("one page cannot place node %d" % at)
        del connection_of(pages[at])["nodes"][at][field]
        return pages
    return mutate


#: What a refusal must carry whole. Every fixture places it PAST the 400/200
#: characters the refusals cut at before #426 round 3; `_past` enforces that.
TAIL = "ACTIONABLE_TAIL: token expired; run the auth refresh"


def _past(text: str, width: int) -> str:
    """`text`, checked to carry `TAIL` only beyond `width` characters."""
    if text.find(TAIL) <= width:
        raise AssertionError("tail at %d, not beyond %d" % (text.find(TAIL), width))
    return text


def _long_stderr(pages: list[dict[str, Any]]) -> _Raw:
    """A nonzero gh exit whose stderr puts the actionable line last."""
    noise = ["gh: retrying request %02d after HTTP 502" % i for i in range(16)]
    return _Raw("", _past("\n".join(noise + [TAIL]), 400), 1)


def _long_errors(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Page 0 carrying an `errors` member whose serialization is long."""
    errors = [{"message": "field context %02d" % i, "path": ["repository"]}
              for i in range(12)] + [{"message": TAIL}]
    _past(json.dumps(errors), 400)
    return [dict(pages[0], errors=errors)] + pages[1:]


#: (case name, connection, mutator, the text the refusal must name). Each is a
#: response a real server or a broken read can produce, and none of them may
#: be repaired into a verdict.
PAGE_FAULTS = (
    ("non-json-stdout", "comments",
     lambda pages: _Raw("<html>rate limited</html>"), "non-JSON"),
    ("slurp-not-a-list", "comments",
     lambda pages: _Raw(json.dumps(pages[0])), "non-empty page array"),
    ("slurp-empty-array", "comments", lambda pages: _Raw("[]"),
     "non-empty page array"),
    ("gh-nonzero-exit", "comments",
     lambda pages: _Raw("", "GraphQL: Bad credentials", 1),
     "failed with exit 1"),
    ("graphql-errors-member", "comments",
     lambda pages: [dict(pages[0], errors=[{"message": "timeout"}])]
     + pages[1:], "GraphQL errors"),
    ("null-pull-request", "comments",
     lambda pages: [{"data": {"repository": {"pullRequest": None}}}],
     "no pullRequest object"),
    ("missing-connection-object", "comments",
     lambda pages: [{"data": {"repository": {"pullRequest": {}}}}],
     "no comments object"),
    ("missing-total-count", "comments", _drop_field("totalCount"),
     "no totalCount"),
    ("missing-has-next-page", "comments", _drop_page_info("hasNextPage"),
     "no boolean pageInfo.hasNextPage"),
    ("node-missing-body", "comments", _drop_node_field("body"),
     "has no body string"),
    ("node-missing-id", "comments", _drop_node_field("id"), "no stable id"),
    ("comment-missing-created-at", "comments", _drop_node_field("createdAt"),
     "has no createdAt"),
    ("duplicate-node-id", "comments", _duplicate_id, "repeats node id"),
    ("total-count-changed", "comments", _bump_total,
     "the population changed under the read"),
    ("lost-page-short-population", "comments", _drop_last_page,
     "a page was lost"),
    ("unterminated-final-page", "comments", _unterminate,
     "still advertising another page"),
    ("mid-stream-terminal-page", "comments", _terminate_early,
     "advertises no further page mid-stream"),
    ("repeated-end-cursor", "comments", _repeat_cursor, "repeats endCursor"),
    ("empty-non-terminal-page", "comments", _blank_page,
     "carries no node but advertises another page"),
    ("page-bound-exceeded", "comments", _overlong, "page bound"),
    ("reviews-stream-failure-refuses", "reviews",
     lambda pages: _Raw("", "connection reset", 1), "PR #500 reviews"),
    # F2 (#426 round 3): the refusal carries the WHOLE diagnostic.
    ("refusal-retains-complete-stderr", "comments", _long_stderr, TAIL),
    ("refusal-retains-complete-graphql-errors", "comments", _long_errors, TAIL),
)


def refusal_cases(env: Env) -> None:
    """Every acquisition failure mode: unknown, never a product finding."""
    cases = env.cases
    bank = {(500, "comments"): nodes("comments", 266),
            (500, "reviews"): nodes("reviews", 150)}

    for name, kind, mutator, expect in PAGE_FAULTS:
        fake = FakeGh(dict(bank), {(500, kind): mutator})
        cases.refuses(name, lambda f=fake: hydrated(env, 500, {}, f), expect)

    def absent(args: list[str], timeout: float) -> _Raw:
        """A host with no gh on its PATH."""
        raise FileNotFoundError(2, "No such file or directory", "gh")

    def stalled(args: list[str], timeout: float) -> _Raw:
        """A gh call that never returns inside its command budget."""
        raise subprocess.TimeoutExpired(["gh", *args], timeout)

    cases.refuses("gh-absent",
                  lambda: env.acquire.Acquirer(runner=absent).hydrate(
                      [{"number": 500}]), "gh is not installed")
    cases.refuses("command-timeout",
                  lambda: env.acquire.Acquirer(runner=stalled).hydrate(
                      [{"number": 500}]), "command deadline")

    # The bounded acquisition deadline is an operational limit, so its expiry
    # is unknown. A clock that has already spent the budget must refuse before
    # the next call rather than assess whatever arrived first.
    ticks = iter([0.0, 0.0, 1000.0, 1000.0, 1000.0])
    cases.refuses("acquisition-deadline-expired",
                  lambda: env.acquire.Acquirer(
                      runner=FakeGh(dict(bank)),
                      clock=lambda: next(ticks),
                      deadline_s=10.0).hydrate([{"number": 500}]),
                  "acquisition deadline expired")

    cases.refuses("repository-identity-malformed",
                  lambda: hydrated(env, 500, {},
                                   FakeGh(dict(bank), repo={"name": ""})),
                  "no owner/name pair")
    cases.refuses("non-integer-pr-number",
                  lambda: env.acquire.Acquirer(
                      runner=FakeGh(dict(bank))).hydrate([{"number": "500"}]),
                  "no integer number")

    # F1 (#426 round 3): a submittedAt MEMBER absent on the last of three
    # pages is a partial response, not a PENDING review's null; it used to
    # normalize to "" and sort the unread NEGATIVE first: a clean verdict.
    absent = FakeGh({(500, "reviews"): nodes("reviews", 201,
                                            {5: POSITIVE, 201: NEGATIVE})},
                    {(500, "reviews"): _drop_node_field("submittedAt", -1)})
    cases.refuses("review-submitted-at-absent-refuses",
                  lambda: hydrated(env, 500, {}, absent), "submittedAt")


# ------------------------------------------------------ the gate end to end

class FakeGhJson:
    """A `_gh_json` stand-in: the outer PR list, then issue states."""

    def __init__(self, rows: list[dict[str, Any]],
                 open_issues: set[int]) -> None:
        """Answer from `rows`, reporting exactly `open_issues` as OPEN."""
        self.rows = rows
        self.open_issues = open_issues
        self.calls: list[list[str]] = []

    def __call__(self, args: list[str]) -> Any:
        """Answer the two calls the checker makes outside acquisition."""
        self.calls.append(list(args))
        if args[:2] == ["pr", "list"]:
            return [dict(row) for row in self.rows]
        if args[:2] == ["issue", "view"]:
            return {"state": "OPEN" if int(args[2]) in self.open_issues
                    else "CLOSED"}
        raise AssertionError("unexpected gh call: %r" % (args,))

    def flag(self, name: str) -> str:
        """The value the outer `pr list` call passed for `name`."""
        args = self.calls[0]
        return args[args.index(name) + 1]


def drive(env: Env, rows: list[dict[str, Any]], fake: FakeGh, argv: list[str],
          seen: list[dict[str, Any]] | None = None
          ) -> tuple[int, str, str, FakeGhJson]:
    """Run the shipped `main()` with both live seams replaced.

    Each PR the assessor is handed is appended to `seen`: `run()` resolves
    `assess_pr` from the checker's namespace at call time, so a wrapper there
    observes every call, and the finally restores it whatever main() does.
    """
    checker = env.checker
    outer = FakeGhJson(rows, set())
    saved = (checker._gh_json, checker._new_acquirer, checker.assess_pr)
    sink: list[dict[str, Any]] = [] if seen is None else seen

    def observed(pr: dict[str, Any], is_open: Callable[[int], bool]) -> Any:
        """`assess_pr`, recording the PR it is handed first."""
        sink.append(pr)
        return saved[2](pr, is_open)

    out, err = io.StringIO(), io.StringIO()
    try:
        checker._gh_json = outer
        checker._new_acquirer = lambda: env.acquire.Acquirer(runner=fake)
        checker.assess_pr = observed
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = checker.main([sys.argv[0], *argv])
    finally:
        checker._gh_json, checker._new_acquirer, checker.assess_pr = saved
    return code, out.getvalue(), err.getvalue(), outer


def hydrated_numbers(fake: FakeGh) -> list[int]:
    """Which PR numbers the acquirer actually asked GitHub about."""
    return sorted({int(a[len("number="):]) for call in fake.calls
                   for a in call if a.startswith("number=")})


def end_to_end_cases(env: Env) -> None:
    """The real entry point, its exit codes, and the outer window it keeps."""
    case = env.cases.outcome
    clean = nodes("comments", 266, {89: NEGATIVE, 215: POSITIVE})
    dirty = nodes("comments", 266, {5: POSITIVE, 215: NEGATIVE})
    rows = [{"number": 425, "mergedAt": MERGED_AT, "body": "no closes"}]

    def gate(bank: list[dict[str, str]],
             mutators: Any = None) -> tuple[int, str, str, FakeGhJson]:
        """Drive main() over one bank; (exit, stdout, stderr, outer call log)."""
        return drive(env, rows, FakeGh({(425, "comments"): bank}, mutators),
                     ["--limit", "1"])

    def clean_run() -> tuple[int, bool]:
        """The exit code and the verdict line of a complete, cleared history."""
        code, out, _, _ = gate(clean)
        return code, "clean over the last 1 merged PR(s)" in out

    def outer_json() -> str:
        """The `--json` field list the outer candidate query asked for.

        It must not name the nested projections again: they stop at 100 nodes
        and say nothing about it, which is the whole defect.
        """
        return gate(clean)[3].flag("--json")

    def finding_run() -> tuple[int, bool]:
        """The exit code and report of a history whose late verdict rejects."""
        code, out, _, _ = gate(dirty)
        return code, "negative-merge" in out

    def refused_run() -> tuple[int, bool]:
        """The exit code and diagnostic when a page is lost mid-acquisition."""
        code, _, err, _ = gate(clean, {(425, "comments"): _drop_last_page})
        return code, "incomplete acquisition" in err

    case("run-clean-exit-0", clean_run, (0, True))
    case("outer-list-requests-no-nested-projections", outer_json,
         "number,mergedAt,body")
    case("run-finding-exit-1", finding_run, (1, True))
    # An acquisition that cannot be proved complete is cannot-run, and says so.
    case("main-incomplete-acquisition-exit-2", refused_run, (2, True))

    # ANTI-VACUITY. The same bank truncated to its first 100 comments - what
    # the old path actually fed the core - reports the negative merge the
    # complete history does not support. Without this arm the semantic cases
    # above could all pass over a fixture that never discriminated.
    case("prefix-discrimination-anti-vacuity",
         lambda: reasons(env, {"number": 425, "mergedAt": MERGED_AT,
                               "body": "x", "comments": clean[:100],
                               "reviews": []}),
         ["negative-merge"])

    # The creation-ordered candidate window and the limit are unchanged:
    # max(limit * 3, 60) candidates fetched, sorted by mergedAt, the newest
    # `limit` assessed, and only those hydrated.
    window = [{"number": 400 + i, "mergedAt": at(i), "body": "x"}
              for i in range(5)]
    windowed = FakeGh({})

    def two_of_five() -> tuple[str, list[int], bool]:
        """The limit gh was asked for, the PRs hydrated, and the verdict line."""
        _, out, _, outer = drive(env, window, windowed, ["--limit", "2"])
        return (outer.flag("--limit"), hydrated_numbers(windowed),
                "clean over the last 2 merged PR(s)" in out)

    case("outer-window-and-limit-preserved", two_of_five,
         ("60", [403, 404], True))
    # ...and repository identity is resolved once for the whole pass, not once
    # per connection: one identity call, then two connections for each of the
    # two selected PRs.
    case("repository-identity-resolved-once",
         lambda: (sum(1 for c in windowed.calls if c[:2] == ["repo", "view"]),
                  sum(1 for c in windowed.calls if c[:2] == ["api", "graphql"])),
         (1, 4))


def completeness_cases(env: Env) -> None:
    """The #426 round-3 corrections, through the real entry point."""
    case = env.cases.outcome
    rows = [{"number": 425, "mergedAt": MERGED_AT, "body": "no closes"}]
    bank = {(425, "reviews"): nodes("reviews", 201,
                                    {5: POSITIVE, 201: NEGATIVE})}
    # F1: a last-page review with no submittedAt MEMBER exits 2 naming the
    # field, and the assessor sees NOTHING; over the complete stream the same
    # observer sees one PR, so an observer that never fired could not pass.
    def absent_stamp_run() -> tuple[int, bool, int, int]:
        """Exit, stderr names the field, PRs assessed; then the live control."""
        seen: list[dict[str, Any]] = []
        damaged = FakeGh(bank, {(425, "reviews"):
                                _drop_node_field("submittedAt", -1)})
        code, _, err, _ = drive(env, rows, damaged, ["--limit", "1"], seen)
        refused = len(seen)
        drive(env, rows, FakeGh(bank), ["--limit", "1"], seen)
        return code, "submittedAt" in err, refused, len(seen) - refused

    case("main-absent-review-timestamp-exit-2", absent_stamp_run, (2, True, 0, 1))

    # F2: the cannot-run line carries both diagnostics past the old 400 slice.
    def diagnostic(mutator: Callable[[Any], Any]) -> tuple[int, bool]:
        """The exit, and whether stderr carries the tail, for one refusal."""
        fake = FakeGh({}, {(425, "comments"): mutator})
        code, _, err, _ = drive(env, rows, fake, ["--limit", "1"])
        return code, TAIL in err

    case("main-refusal-diagnostic-complete-exit-2",
         lambda: diagnostic(_long_stderr) + diagnostic(_long_errors),
         (2, True, 2, True))


def identity_cases(env: Env) -> None:
    """A repository response that is not an object, through the whole gate.

    `gh repo view --json` answers with an object, but a proxy, a rate limiter
    or a future flag can put an array, a bare string or a number on stdout, and
    each of those parses. Reading a member off one used to be an uncaught
    AttributeError, which is a crash where this gate owes its caller a named
    cannot-run: these arms are end to end, so what they pin is the EXIT the
    caller sees, not an internal refusal.
    """
    case = env.cases.outcome
    rows = [{"number": 425, "mergedAt": MERGED_AT, "body": "no closes"}]

    def identity_gate(repo: Any) -> tuple[int, bool]:
        """main()'s exit, and whether its diagnostic names the type observed."""
        code, _, err, _ = drive(env, rows, FakeGh({}, repo=repo),
                                ["--limit", "1"])
        named = ("repository identity: gh repo view returned a %s"
                 % type(repo).__name__) in err
        return code, named

    for name, repo in (("repository-identity-array-refuses-exit-2", [1]),
                       ("repository-identity-string-refuses-exit-2", "broken"),
                       ("repository-identity-number-refuses-exit-2", 7)):
        case(name, lambda r=repo: identity_gate(r), (2, True))

    # ANTI-VACUITY for the guard above: the same path over a well-formed
    # identity and two empty histories is still a normal clean run, so what
    # was added refuses malformed responses rather than every response.
    def valid_identity() -> tuple[int, bool]:
        """The exit and verdict line for a valid identity with no events."""
        code, out, _, _ = drive(env, rows, FakeGh({}), ["--limit", "1"])
        return code, "clean over the last 1 merged PR(s)" in out

    case("repository-identity-valid-empty-histories-exit-0", valid_identity,
         (0, True))

    # F2 (#426 round 3): a no-owner payload is quoted WHOLE, past the old 200.
    def diagnostic_complete() -> tuple[int, bool]:
        """main()'s exit, and whether its diagnostic carries the payload tail."""
        repo = {"name": "milan-fpga", "context": [
            "identity context %02d" % i for i in range(12)], "note": TAIL}
        _past(json.dumps(repo), 200)
        code, _, err, _ = drive(env, rows, FakeGh({}, repo=repo),
                                ["--limit", "1"])
        return code, TAIL in err

    case("repository-identity-diagnostic-complete", diagnostic_complete, (2, True))


def selftest(acquire: ModuleType, checker: ModuleType) -> tuple[list[str], int]:
    """Run every acquisition case; (problems, how many cases actually ran)."""
    cases = Cases(acquire.AcquisitionError)
    env = Env(acquire, checker, cases)
    # A group that dies in its own scaffolding is a named problem, not a
    # traceback: every case it had not reached is then reported by name by the
    # roster arm below, which is what makes an aborted group readable.
    for group in (boundary_cases, stream_cases, refusal_cases,
                  end_to_end_cases, completeness_cases, identity_cases):
        try:
            group(env)
        except Exception as exc:
            cases.problems.append("%s raised %s: %s"
                                  % (group.__name__, type(exc).__name__, exc))

    # META-ARM, the same argument as the checker's own: the roster is frozen
    # in CASE_NAMES, so an arm lost to an early return, a duplicated name and
    # a silently added case are findings rather than a smaller number nobody
    # reads.
    if sorted(cases.names) != sorted(CASE_NAMES):
        missing = sorted(set(CASE_NAMES) - set(cases.names))
        extra = sorted(set(cases.names) - set(CASE_NAMES))
        cases.problems.append(
            "acquisition roster drift: %d ran of %d frozen; missing %s, "
            "unexpected %s" % (len(cases.names), len(CASE_NAMES), missing,
                               extra))
    return cases.problems, len(cases.names)
