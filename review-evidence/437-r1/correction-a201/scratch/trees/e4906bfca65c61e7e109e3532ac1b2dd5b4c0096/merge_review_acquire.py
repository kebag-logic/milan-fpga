#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Complete per-PR comment and review histories, or an explicit refusal.

WHY THIS EXISTS (issue #426). `check_merge_review_integrity.py` classified a
merged PR from the nested `reviews`/`comments` projections `gh pr list --json`
returns. Those projections are capped at the connection's first 100 nodes and
gh's JSON export drops the connection's `totalCount` and `pageInfo`, so the
caller cannot tell a complete history from a prefix of one. PR #425 merged
carrying 266 comments; the canonical run saw comments 1-100, missed the two
clearing POSITIVE reports published pre-merge at ordinals 215 and 232, and
reported a negative merge that the complete history does not support. The
defect is symmetric: an omitted later NEGATIVE or an uncleared later BLOCKER
would produce a false clean result the same way.

WHAT THIS DOES. One `Acquirer` hydrates each already-selected PR with BOTH its
complete comment history and its complete formal-review history, through two
single-connection paginated GraphQL queries per PR - one per connection, each
with its own `$endCursor`, so two independent cursors are never coupled - and
proves the result complete before the pure assessment core is allowed to see
it. Repository identity is resolved once. Every call is an argument array
through the `gh` the caller is already authenticated with; no new service,
credential or transport is introduced.

WHAT COMPLETE MEANS HERE, and what it does not. A connection is accepted only
when the command succeeded, every page parsed, no page carried a GraphQL
`errors` member, every page produced the expected object shape, every node
carried a stable non-empty id, no id repeated, every NON-TERMINAL page
advertised another page, carried at least one node and spent an endCursor no
earlier page in the stream had spent, the final page advertised
`hasNextPage: false`, the advertised `totalCount` was identical on every page,
and the number of nodes collected equals it. The cursor rule is written for
non-terminal pages because that is where a cursor is a claim about a further
read; a terminal page ends the stream, so what closes it is its terminal flag
reconciled against the population, not a cursor. All of that is an
observed-consistency proof about ONE acquisition. It is not a claim that a
body is immutable, and it recovers no comment edit history: a body edited
between two reads is two different strings under one stable id, and nothing
here would notice.

THE TERMINAL PAGE, as this protocol actually spells it. A GitHub connection
whose population is an exact multiple of the page size ends with a FULL page
carrying `hasNextPage: false`; gh stops there and no empty page is ever
delivered. So "two full pages then a terminal empty page" is not a form this
API produces, and nothing here fabricates one. A terminal empty page IS
accepted when a server sends one, because it reconciles: zero nodes, no next
page, and a `totalCount` the collected nodes already satisfy.

FAILURE IS UNKNOWN, NEVER A VERDICT. Every refusal raises `AcquisitionError`
with the connection, the PR and the observed inconsistency named, which the
caller reports as its existing cannot-run exit 2, printing the message whole.
The message carries the COMPLETE diagnostic: a failed command's whole stderr,
the whole serialized GraphQL `errors` member, the whole repository payload -
never a prefix of one, because a diagnostic cut at a fixed width loses the
line that says what to do. A node lacking a member the query asked for is a
partial page and is refused, whatever the schema says about that member's
nullability; only a member that is PRESENT and explicitly null is normalized,
and only where the schema allows the null (`submittedAt` of a PENDING review).
A partial, lost, repeated, inconsistent, malformed or timed-out acquisition
never degrades to the first page, the newest page, an empty history or a
skipped PR.
"""

import json
import subprocess
import time
from collections.abc import Callable
from typing import Any, NamedTuple

#: Nodes requested per page. 100 is the maximum a GitHub connection serves.
PAGE_SIZE = 100
#: Pages one connection may deliver before the acquisition is refused. At 100
#: nodes a page this is 10 000 events on one PR, an order of magnitude past
#: the largest history in this corpus (266). Its job is not to cap real data
#: but to end a stream that is not converging - a query that fails to advance
#: its cursor is served its first page for as long as anything keeps asking.
MAX_PAGES = 100
#: Wall-clock ceiling for ONE gh invocation. The observed complete paginated
#: read of the 266-comment PR #425 history took a few seconds, so two minutes
#: is far above any healthy call while still ending a connection that has
#: stalled rather than failed. A gate that hangs reports nothing at all, which
#: is strictly worse than reporting unknown.
COMMAND_TIMEOUT_S = 120.0
#: Wall-clock ceiling for one whole hydration pass. The default window is 20
#: PRs and each needs two connections plus a single identity call, so this
#: allows about 45 s per PR end to end. On expiry the run is unknown: an
#: assessment over the PRs that happened to finish first is a report about an
#: arbitrary subset, and nothing in the output would say so.
ACQUISITION_DEADLINE_S = 900.0


class AcquisitionError(Exception):
    """A history could not be acquired and proved complete.

    Raised for every failure mode: the tool, the command, the transport, the
    document shape, the pagination and the deadline. The caller maps it to its
    existing cannot-run exit, so nothing here has to decide what a partial
    history would have meant.
    """


class Connection(NamedTuple):
    """One GraphQL connection this adapter knows how to hydrate completely."""

    #: The connection field on `PullRequest`.
    name: str
    #: The timestamp field the existing assessment core reads for its events.
    time_field: str
    #: Whether the schema makes that timestamp non-null. `IssueComment
    #: .createdAt` is `DateTime!`; `PullRequestReview.submittedAt` is nullable
    #: and is null for a PENDING review, which the core already reads as the
    #: empty string, so an EXPLICIT null is normalized rather than refused.
    #: Nullable is not optional: the query names the field on every node, so
    #: the member must be present whatever its value, and a node without it
    #: is a partial response that is refused for either connection.
    time_required: bool


COMMENTS = Connection("comments", "createdAt", True)
REVIEWS = Connection("reviews", "submittedAt", False)


class Raw(NamedTuple):
    """What a runner returns: exactly what the child command produced."""

    stdout: str
    stderr: str = ""
    returncode: int = 0


def query_for(connection: Connection) -> str:
    """The single-connection paginated query for `connection`.

    One connection per query on purpose. A document asking for comments and
    reviews together shares one `$endCursor` between two independent cursors,
    so whichever connection is shorter starts being served a cursor from the
    other one, and the completeness evidence for both becomes unreadable.
    """
    return (
        "query($owner: String!, $name: String!, $number: Int!, "
        "$endCursor: String) {\n"
        "  repository(owner: $owner, name: $name) {\n"
        "    pullRequest(number: $number) {\n"
        f"      {connection.name}(first: {PAGE_SIZE}, after: $endCursor) {{\n"
        "        totalCount\n"
        "        pageInfo { hasNextPage endCursor }\n"
        f"        nodes {{ id {connection.time_field} body }}\n"
        "      }\n"
        "    }\n"
        "  }\n"
        "}\n")


def _default_runner(args: list[str], timeout: float) -> Raw:
    """Run `gh` with an argument array and a bounded wall-clock timeout.

    An argument array rather than a shell string, and the caller's existing gh
    authentication rather than any credential this module knows about.
    """
    done = subprocess.run(["gh", *args], capture_output=True, text=True,
                          timeout=timeout)
    return Raw(done.stdout, done.stderr, done.returncode)


class Acquirer:
    """Hydrates selected PRs with complete comment and review histories."""

    def __init__(self, runner: Callable[[list[str], float], Raw] | None = None,
                 clock: Callable[[], float] | None = None,
                 command_timeout_s: float = COMMAND_TIMEOUT_S,
                 deadline_s: float = ACQUISITION_DEADLINE_S) -> None:
        """Build an acquirer; `runner` and `clock` are the self-test's seams."""
        self._runner = runner or _default_runner
        self._clock = clock or time.monotonic
        self._command_timeout_s = command_timeout_s
        self._deadline_s = deadline_s
        self._deadline: float | None = None
        self._repo: tuple[str, str] | None = None

    # -------------------------------------------------------------- public

    def hydrate(self, prs: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Replace every PR's `comments` and `reviews` with complete histories.

        Mutates each dict in place and returns the same list, so the caller's
        selection - which PRs, in which order - is untouched. Raises
        `AcquisitionError` on the first PR whose history cannot be proved
        complete: an assessment over the PRs that happened to succeed is a
        report about an arbitrary subset.
        """
        self._deadline = self._clock() + self._deadline_s
        for pr in prs:
            number = pr.get("number")
            if not isinstance(number, int):
                raise AcquisitionError(
                    "selected PR carries no integer number: %r" % (number,))
            pr["comments"] = self.connection(number, COMMENTS)
            pr["reviews"] = self.connection(number, REVIEWS)
        return prs

    def connection(self, number: int,
                   connection: Connection) -> list[dict[str, str]]:
        """Every node of one connection for one PR, proved complete."""
        owner, name = self.repository()
        what = "PR #%d %s" % (number, connection.name)
        payload = self._json(
            ["api", "graphql", "--paginate", "--slurp",
             "-f", "query=" + query_for(connection),
             "-F", "owner=" + owner, "-F", "name=" + name,
             "-F", "number=%d" % number], what)
        if not isinstance(payload, list) or not payload:
            raise AcquisitionError(
                "%s: --slurp did not return a non-empty page array (%s)"
                % (what, type(payload).__name__))
        return _collect(payload, connection, what)

    def repository(self) -> tuple[str, str]:
        """The (owner, name) this gh checkout resolves to, asked once.

        A parsed response is not an object just because it is truthy: an array,
        a bare string and a number all survive `json.loads` and none of them
        answers `.get`. Reading a member off one is an uncaught AttributeError
        where this module owes its caller a named refusal and the gate's
        cannot-run exit, so the type is checked before any member is read.
        """
        if self._repo is None:
            payload = self._json(["repo", "view", "--json", "owner,name"],
                                 "repository identity")
            if not isinstance(payload, dict):
                raise AcquisitionError(
                    "repository identity: gh repo view returned a %s, not a "
                    "JSON object: %s"
                    % (type(payload).__name__, json.dumps(payload)))
            owner = payload.get("owner")
            name = payload.get("name")
            login = owner.get("login") if isinstance(owner, dict) else None
            if not isinstance(login, str) or not login \
                    or not isinstance(name, str) or not name:
                raise AcquisitionError(
                    "repository identity: gh repo view returned no owner/name "
                    "pair: %s" % json.dumps(payload))
            self._repo = (login, name)
        return self._repo

    # ------------------------------------------------------------- private

    def _json(self, args: list[str], what: str) -> Any:
        """One bounded gh call, its exit status honoured and its stdout parsed."""
        try:
            done = self._runner(args, self._budget(what))
        except FileNotFoundError as exc:
            raise AcquisitionError("%s: gh is not installed" % what) from exc
        except subprocess.TimeoutExpired as exc:
            raise AcquisitionError(
                "%s: gh exceeded the %.0fs command deadline; the history is "
                "unknown, not empty" % (what, self._command_timeout_s)) from exc
        if done.returncode != 0:
            raise AcquisitionError(
                "%s: gh %s failed with exit %d: %s"
                % (what, " ".join(args[:2]), done.returncode,
                   (done.stderr or "").strip()))
        try:
            return json.loads(done.stdout)
        except json.JSONDecodeError as exc:
            raise AcquisitionError(
                "%s: gh returned non-JSON: %s" % (what, exc)) from exc

    def _budget(self, what: str) -> float:
        """Seconds this call may take, refusing once the pass deadline is spent."""
        if self._deadline is None:
            return self._command_timeout_s
        left = self._deadline - self._clock()
        if left <= 0:
            raise AcquisitionError(
                "%s: the %.0fs acquisition deadline expired before the "
                "history was complete" % (what, self._deadline_s))
        return min(self._command_timeout_s, left)


# ------------------------------------------------------------- page algebra

def _collect(pages: list[Any], connection: Connection,
             what: str) -> list[dict[str, str]]:
    """Validate every page and return the connection's nodes, in order."""
    if not pages:
        raise AcquisitionError("%s: no response page was returned" % what)
    if len(pages) > MAX_PAGES:
        raise AcquisitionError(
            "%s: %d pages exceeds the %d-page bound; the cursor is not "
            "converging" % (what, len(pages), MAX_PAGES))
    nodes: list[dict[str, str]] = []
    ids: set[str] = set()
    cursors: set[str] = set()
    total: int | None = None
    for index, page in enumerate(pages):
        conn = _connection_object(page, connection, what, index)
        total = _reconcile_total(conn, total, what, index)
        _check_page_position(conn, what, index, index == len(pages) - 1,
                             cursors)
        for node in conn["nodes"]:
            record = _record(node, connection, what, index)
            if record["id"] in ids:
                raise AcquisitionError(
                    "%s: page %d repeats node id %s; the stream is not "
                    "advancing" % (what, index, record["id"]))
            ids.add(record["id"])
            nodes.append(record)
    if len(nodes) != total:
        raise AcquisitionError(
            "%s: collected %d node(s) for an advertised totalCount of %d; a "
            "page was lost" % (what, len(nodes), total))
    return nodes


def _connection_object(page: Any, connection: Connection, what: str,
                       index: int) -> dict[str, Any]:
    """The connection object inside one response page, or a named refusal."""
    if not isinstance(page, dict):
        raise AcquisitionError("%s: page %d is not a JSON object (%s)"
                               % (what, index, type(page).__name__))
    if page.get("errors"):
        raise AcquisitionError(
            "%s: page %d carries GraphQL errors: %s"
            % (what, index, json.dumps(page["errors"])))
    node: Any = page
    for step in ("data", "repository", "pullRequest", connection.name):
        node = node.get(step) if isinstance(node, dict) else None
        if not isinstance(node, dict):
            raise AcquisitionError(
                "%s: page %d has no %s object" % (what, index, step))
    for field, kind in (("totalCount", int), ("pageInfo", dict),
                        ("nodes", list)):
        if not isinstance(node.get(field), kind) \
                or isinstance(node.get(field), bool):
            raise AcquisitionError(
                "%s: page %d has no %s of the expected type"
                % (what, index, field))
    if not isinstance(node["pageInfo"].get("hasNextPage"), bool):
        raise AcquisitionError(
            "%s: page %d has no boolean pageInfo.hasNextPage" % (what, index))
    return node


def _reconcile_total(conn: dict[str, Any], total: int | None, what: str,
                     index: int) -> int:
    """The advertised population, refusing a value that changed mid-stream."""
    count = conn["totalCount"]
    if count < 0:
        raise AcquisitionError("%s: page %d advertises totalCount %d"
                               % (what, index, count))
    if total is not None and count != total:
        raise AcquisitionError(
            "%s: page %d advertises totalCount %d after %d; the population "
            "changed under the read" % (what, index, count, total))
    return count


def _check_page_position(conn: dict[str, Any], what: str, index: int,
                         last: bool, cursors: set[str]) -> None:
    """Terminal completion and cursor progress for one page.

    Every page but the last must advertise another page and carry at least one
    node, and the last must advertise none: gh stops paginating exactly when
    `hasNextPage` goes false, so a false in the middle means the array is not
    one stream and a true at the end means the stream was cut before it ended.

    The cursor check binds NON-TERMINAL pages only, which is where a cursor is
    a claim about a further read: each must carry a non-empty endCursor no
    earlier page has spent. The terminal page is reconciled through its node
    population and its terminal flag instead, so a valid terminal-empty page
    stays valid. Cursors are opaque, so they are checked for REPETITION rather
    than order - an ordering claim over a base64 blob would be a guess about a
    server's encoding.
    """
    has_next = conn["pageInfo"]["hasNextPage"]
    if has_next == last:
        problem = ("ends while still advertising another page"
                   if last else "advertises no further page mid-stream")
        raise AcquisitionError("%s: page %d %s" % (what, index, problem))
    if not has_next:
        return
    if not conn["nodes"]:
        raise AcquisitionError(
            "%s: page %d carries no node but advertises another page"
            % (what, index))
    cursor = conn["pageInfo"].get("endCursor")
    if not isinstance(cursor, str) or not cursor:
        raise AcquisitionError(
            "%s: page %d advertises another page with no endCursor"
            % (what, index))
    if cursor in cursors:
        raise AcquisitionError(
            "%s: page %d repeats endCursor %s; the stream is not advancing"
            % (what, index, cursor))
    cursors.add(cursor)


def _record(node: Any, connection: Connection, what: str,
            index: int) -> dict[str, str]:
    """One node reduced to what the assessment core reads, every member checked.

    Presence is tested before value. The query names `id`, the time field and
    `body` on every node, so a node that lacks any of them is a partial or
    malformed page and is refused whatever the schema says about nullability:
    `.get()` read an absent `submittedAt` as the same None an explicit null
    parses to, and the empty stamp it normalized to sorted an unread NEGATIVE
    ahead of an earlier POSITIVE (#426, review round 3). Only a time field
    that is PRESENT and explicitly null is normalized, and only for a
    nullable connection.
    """
    if not isinstance(node, dict):
        raise AcquisitionError("%s: page %d holds a non-object node (%s)"
                               % (what, index, type(node).__name__))
    ident = node.get("id")
    if not isinstance(ident, str) or not ident:
        raise AcquisitionError(
            "%s: page %d holds a node with no stable id" % (what, index))
    if connection.time_field not in node:
        raise AcquisitionError(
            "%s: node %s has no %s member; the query asked for it, so the "
            "page is partial" % (what, ident, connection.time_field))
    when = node[connection.time_field]
    if when is None and not connection.time_required:
        when = ""                 # an explicit null: a PENDING review
    if not isinstance(when, str) or (connection.time_required and not when):
        raise AcquisitionError(
            "%s: node %s has no %s" % (what, ident, connection.time_field))
    body = node.get("body")
    if not isinstance(body, str):
        raise AcquisitionError("%s: node %s has no body string" % (what, ident))
    return {"id": ident, connection.time_field: when, "body": body}
