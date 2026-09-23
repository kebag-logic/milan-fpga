#!/usr/bin/env python3
"""Validate the canonical Milan feature ledger and active documentation rows.

Run from any directory:

    python3 scripts/check_feature_status.py
    python3 scripts/check_feature_status.py --self-test

The checker uses only the Python standard library. With ``--self-test`` it
first runs positive and negative fixtures, then checks the working tree.
"""

import argparse
import ast
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, NamedTuple


REPO = Path(__file__).resolve().parent.parent
LEDGER = REPO / "docs/reference/milan_feature_status.json"
ALLOWED_STATUSES = {"implemented", "partial", "missing", "not-supported"}
FEATURE_ID_RE = re.compile(r"^[a-z0-9]+(?:[.-][a-z0-9]+)*$")
OBSOLETE_RE = re.compile(r"^\[OBSOLETE \+ \d{4}-\d{2}-\d{2}\]$")
BLOCK_START = "<!-- milan-feature-status:start -->"
BLOCK_END = "<!-- milan-feature-status:end -->"
ROW_RE = re.compile(
    r"^\|\s*`(?P<feature>[^`]+)`\s*\|\s*`(?P<status>[^`]+)`\s*\|"
    r"\s*`?(?P<value>[^|`]*?)`?\s*\|\s*$"
)
HEADER_RE = re.compile(
    r"^\|\s*Feature ID\s*\|\s*Status\s*\|\s*Canonical value\s*\|\s*$"
)
FENCE_RE = re.compile(r"^\s*(```|~~~)")
FACT_START_RE = re.compile(
    r"^<!-- milan-feature-fact:(?P<fact>[a-z0-9_]+):start -->$"
)
FACT_END_RE = re.compile(
    r"^<!-- milan-feature-fact:(?P<fact>[a-z0-9_]+):end -->$"
)
FACT_TOKEN_RE = re.compile(r"`([A-Z][A-Z0-9_]*)`")
FACT_NON_OPERATION_TOKENS = {
    "BAD_ARGUMENTS",
    "NOT_IMPLEMENTED",
    "NOT_SUPPORTED",
    "NO_SUCH_DESCRIPTOR",
    "SUCCESS",
}
ARCHIVE_PARTS = {
    "history",
    "archive",
    "archived",
    "archives",
}
VERSION_SOURCE = REPO / "hdl/common/csr/milan_csr.sv"
COMMAND_SOURCE = REPO / "tests/steps/aecp_engine_steps.py"
FIRMWARE_SOURCE = REPO / "sw/firmware/milan_baremetal/milan_baremetal.c"


class SourceNames(NamedTuple):
    """How each declaration source is spelled in a finding.

    The three names travel together because they answer one question - what
    a reader is told to open - and separating them from the texts keeps
    ``check_source_facts`` down to its real arguments: the ledger and the
    three sources it reads.
    """
    version: str = "milan_csr.sv"
    command: str = "aecp_engine_steps.py"
    firmware: str = "milan_baremetal.c"


#: The bare file names, used by the fixtures and by any caller that has no
#: repository-relative path to offer.
DEFAULT_SOURCE_NAMES = SourceNames()

# --------------------------------------------------------------------------
# Repeated values in PROSE (#98). The marked rows and fact blocks above carry
# the inventory; a sentence repeating the same value carried nothing, and a
# roadmap shipped for nine days with `0x0002_0053` in its opening line and
# `0x0002_0055` in its own marked row twenty-five lines below.
#
# These rules are deliberately NOT a scan for stale spellings. Each one reads
# the canonical fact and judges what the prose says against it, so the rule
# needs no maintenance when the value moves - only the prose does.

#: A current-version claim: the register/product name and the FULL two-word
#: spelling on one line, IN THE CANONICAL MAJOR. Two spellings are deliberately
#: not judged, because neither can be a claim about the current version and
#: gating them would mark seventy historical sentences with no drift behind
#: any of them: the minor-only idiom (`fixed at VERSION 0x000F`), and an older
#: major (`VERSION 0x0001_000B`), which the major bump already retired. When
#: the major next steps, today's `0x0002_xxxx` sentences leave the judged set
#: the same way - by then they are history, and the new era's are judged.
VERSION_CLAIM_RE = re.compile(
    r"\bVERSION\b.{0,40}?`?(0x[0-9A-Fa-f]{4}_[0-9A-Fa-f]{4})`?")

#: A served-inventory count. Keyed on the `opcodes` idiom the served claims
#: use, because `N AEM commands` means something else here (the roadmap counts
#: commands still to land, not commands served). The word before the noun is
#: judged only when it IS a number: `the served AEM opcodes` is a phrase, not
#: a claim, and reading every adjective as a count made this file's own
#: description of the rule its first false positive.
COUNT_CLAIM_RE = re.compile(
    r"(?:\*\*)?(?P<count>[A-Za-z][A-Za-z-]{2,}|\d{1,3})(?:\*\*)?\s+"
    r"(?P<kind>AEM opcodes?|MVU (?:command|operation)s?)\b")
COUNT_FACTS = {"AEM": "served_aem_operations", "MVU": "served_mvu_operations"}

#: Placed on the line before a claim that deliberately records a SUPERSEDED
#: value (a dated audit, a release note). A historic marker whose line carries
#: the canonical value is itself a finding: the value moved on to it and the
#: marker now hides a live claim.
VALUE_HISTORIC_RE = re.compile(
    r"^<!-- milan-feature-value:(?P<fact>[a-z0-9_]+):historic -->$")

#: An ORDERED fact: the block's tokens must reproduce the ledger sequence,
#: not merely its set. `firmware_boot_order` is what makes "the PHC does not
#: wait for the AEM image" a checkable claim rather than a sentence.
ORDER_START_RE = re.compile(
    r"^<!-- milan-feature-order:(?P<fact>[a-z0-9_]+):start -->$")
ORDER_END_RE = re.compile(
    r"^<!-- milan-feature-order:(?P<fact>[a-z0-9_]+):end -->$")
ORDER_TOKEN_RE = re.compile(r"`([a-z_][a-z0-9_]*)\(\)`")

_ONES = ("zero", "one", "two", "three", "four", "five", "six", "seven",
         "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen",
         "fifteen", "sixteen", "seventeen", "eighteen", "nineteen")
_TENS = {2: "twenty", 3: "thirty", 4: "forty", 5: "fifty", 6: "sixty",
         7: "seventy", 8: "eighty", 9: "ninety"}


def is_number_token(token: str) -> bool:
    """Whether ``token`` spells a number this corpus could mean as a count."""
    return bool(re.fullmatch(r"\d{1,3}", token)) or any(
        token == spelling for value in range(100)
        for spelling in number_spellings(value))


def number_spellings(count: int) -> set[str]:
    """Every spelling of ``count`` this corpus accepts, lower-cased.

    Prose here writes small counts as words (`thirty AEM opcodes`); tables
    write numerals. Both are the same claim, so both are accepted rather than
    forcing a house number style on a consistency gate.
    """
    spellings = {str(count)}
    if 0 <= count < len(_ONES):
        spellings.add(_ONES[count])
    elif 20 <= count < 100:
        tens, ones = divmod(count, 10)
        spellings.add(_TENS[tens] if not ones
                      else f"{_TENS[tens]}-{_ONES[ones]}")
    return spellings


class DuplicateKey(ValueError):
    """Raised when a JSON object repeats a key."""


def _object_without_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKey(f"duplicate JSON key '{key}'")
        result[key] = value
    return result


def _facts_findings(facts, source):
    """Every shape complaint about the ledger's ``facts`` object."""
    findings = []
    version = facts.get("gateware_version")
    if not isinstance(version, str) or not re.fullmatch(
            r"0x[0-9A-F]{4}_[0-9A-F]{4}", version):
        findings.append(
            f"{source}: facts.gateware_version has invalid shape {version!r}")
    for name in ("served_aem_operations", "served_mvu_operations",
                 "missing_mandatory_aem_operations"):
        values = facts.get(name)
        if not isinstance(values, list) or not all(
                isinstance(value, str) and value for value in values):
            findings.append(f"{source}: facts.{name} must be a string list")
            continue
        duplicates = sorted({value for value in values
                             if values.count(value) > 1})
        for value in duplicates:
            findings.append(
                f"{source}: duplicate operation '{value}' in facts.{name}")
    order = facts.get("firmware_boot_order")
    if not isinstance(order, list) or len(order) < 2 or not all(
            isinstance(step, str) and re.fullmatch(r"[a-z_][a-z0-9_]*",
                                                   step)
            for step in order):
        findings.append(
            f"{source}: facts.firmware_boot_order must be a list of at "
            f"least two C identifiers")
    elif len(order) != len(set(order)):
        findings.append(
            f"{source}: facts.firmware_boot_order repeats a step")
    return findings


def _feature_findings(features, source):
    """``(by_id, findings)`` for the ledger's feature list."""
    findings = []
    by_id = {}
    for index, feature in enumerate(features):
        where = f"{source}: features[{index}]"
        if not isinstance(feature, dict):
            findings.append(f"{where} must be an object")
            continue
        feature_id = feature.get("id")
        if not isinstance(feature_id, str) or not FEATURE_ID_RE.fullmatch(feature_id):
            findings.append(f"{where}: invalid feature identifier {feature_id!r}")
            continue
        if feature_id in by_id:
            findings.append(f"{source}: duplicate feature identifier '{feature_id}'")
            continue
        by_id[feature_id] = feature

        status = feature.get("status")
        if not isinstance(status, str) or status not in ALLOWED_STATUSES:
            findings.append(
                f"{source}: feature '{feature_id}' has unknown status {status!r}")
        summary = feature.get("summary")
        if not isinstance(summary, str) or not summary.strip():
            findings.append(f"{source}: feature '{feature_id}' needs a summary")
        documents = feature.get("documents")
        if not isinstance(documents, list) or not documents or not all(
                isinstance(document, str) and document.endswith(".md")
                for document in documents):
            findings.append(
                f"{source}: feature '{feature_id}' needs a Markdown document list")
        elif len(documents) != len(set(documents)):
            findings.append(
                f"{source}: feature '{feature_id}' repeats a document")

    return by_id, findings


def _document_register_findings(data, facts, source):
    """Complaints about ``fact_documents`` and the two prose-claim
    registers that say which pages must repeat a value."""
    findings = []
    fact_documents = data.get("fact_documents")
    if not isinstance(fact_documents, dict):
        findings.append(f"{source}: fact_documents must be an object")
    else:
        list_facts = {
            name for name, value in facts.items() if isinstance(value, list)
        }
        for name, documents in fact_documents.items():
            if name not in list_facts:
                findings.append(
                    f"{source}: fact_documents has unknown list fact '{name}'")
                continue
            if not isinstance(documents, list) or not documents or not all(
                    isinstance(document, str) and document.endswith(".md")
                    for document in documents):
                findings.append(
                    f"{source}: fact_documents.{name} needs a Markdown "
                    "document list")
            elif len(documents) != len(set(documents)):
                findings.append(
                    f"{source}: fact_documents.{name} repeats a document")

    # The prose-claim registers (#98). Both are REQUIRED: an absent register
    # would silently retire the presence half of rules 1 and 4, and a page
    # that drops the claim entirely is exactly the drift they exist to catch.
    for key, allowed in (("value_documents", {"gateware_version"}),
                         ("order_documents", {"firmware_boot_order"})):
        register = data.get(key)
        if not isinstance(register, dict) or not register:
            findings.append(f"{source}: {key} must be a non-empty object")
            continue
        for name, documents in register.items():
            if name not in allowed:
                findings.append(f"{source}: {key} has unknown fact '{name}'")
                continue
            if not isinstance(documents, list) or not documents or not all(
                    isinstance(document, str) and document.endswith(".md")
                    for document in documents):
                findings.append(
                    f"{source}: {key}.{name} needs a Markdown document list")
            elif len(documents) != len(set(documents)):
                findings.append(f"{source}: {key}.{name} repeats a document")
    return findings


def _cross_fact_findings(facts, by_id, source):
    """Complaints that need two already-valid sections compared."""
    findings = []
    version_feature = by_id.get("gateware.current-version")
    if (version_feature is not None and
            version_feature.get("value") != facts["gateware_version"]):
        findings.append(
            f"{source}: gateware.current-version value does not match "
            "facts.gateware_version")
    served = set(facts["served_aem_operations"])
    missing = set(facts["missing_mandatory_aem_operations"])
    for operation in sorted(served & missing):
        findings.append(
            f"{source}: operation '{operation}' is both served and missing")
    return findings


def load_ledger_text(text: str, source: str = "ledger"
                     ) -> tuple[dict[str, Any] | None, list[str]]:
    """Return ``(ledger, findings)`` for raw JSON text."""
    try:
        data = json.loads(text, object_pairs_hook=_object_without_duplicates)
    except (json.JSONDecodeError, DuplicateKey) as exc:
        return None, [f"{source}: {exc}"]

    findings = []
    if not isinstance(data, dict):
        return None, [f"{source}: root must be an object"]
    if data.get("schema_version") != 1:
        findings.append(f"{source}: schema_version must be 1")

    facts = data.get("facts")
    if not isinstance(facts, dict):
        findings.append(f"{source}: facts must be an object")
    else:
        findings.extend(_facts_findings(facts, source))

    features = data.get("features")
    if not isinstance(features, list):
        findings.append(f"{source}: features must be a list")
        return None, findings

    by_id, feature_findings = _feature_findings(features, source)
    findings.extend(feature_findings)
    if findings:
        return None, findings

    findings.extend(_document_register_findings(data, facts, source))
    if findings:
        return None, findings

    findings.extend(_cross_fact_findings(facts, by_id, source))
    if findings:
        return None, findings
    data["by_id"] = by_id
    return data, []


def boot_order_findings(ledger: dict[str, Any], firmware_text: str, firmware_source: str) -> list[str]:
    """Tie ``facts.firmware_boot_order`` to ``milan_init()``'s call order.

    The order is read from the ONE function that runs at init, with comments
    and strings removed first so a printf naming a step cannot supply it. Only
    the relative order of the ledger's steps is judged: the firmware is free
    to log or read a register between them, and the claim documentation makes
    is "the PHC is up before the AEM image is looked at", not "nothing else
    happens".
    """
    findings = []
    body = re.search(r"\bmilan_init\s*\([^)]*\)\s*\{(?P<body>.*?)\n\}",
                     firmware_text, re.DOTALL)
    if body is None:
        findings.append(f"{firmware_source}: cannot locate milan_init()")
        return findings
    code = re.sub(r"/\*.*?\*/", " ", body.group("body"), flags=re.DOTALL)
    code = re.sub(r"//[^\n]*", " ", code)
    code = re.sub(r'"(?:[^"\\]|\\.)*"', ' ', code)
    positions = []
    for step in ledger["facts"]["firmware_boot_order"]:
        call = re.search(r"\b%s\s*\(" % re.escape(step), code)
        if call is None:
            findings.append(
                f"{firmware_source}: milan_init() does not call {step}()")
        else:
            positions.append((step, call.start()))
    if len(positions) != len(ledger["facts"]["firmware_boot_order"]):
        return findings
    actual = [step for step, _ in sorted(positions, key=lambda item: item[1])]
    if actual != ledger["facts"]["firmware_boot_order"]:
        findings.append(
            f"firmware boot-order conflict: ledger="
            f"{ledger['facts']['firmware_boot_order']}; "
            f"{firmware_source}={actual}")
    return findings


def check_source_facts(ledger: dict[str, Any], version_text: str,
                       command_text: str, firmware_text: str | None = None,
                       names: SourceNames = DEFAULT_SOURCE_NAMES) -> list[str]:
    """Tie version and served-command facts to their source declarations."""
    findings = []
    version_code = re.sub(r"/\*.*?\*/", "", version_text, flags=re.DOTALL)
    version_code = re.sub(r"//[^\n]*", "", version_code)
    matches = re.findall(
        r"parameter\s+logic\s*\[31:0\]\s+VERSION\s*=\s*32'h"
        r"([0-9A-Fa-f]{4})_([0-9A-Fa-f]{4})", version_code)
    if len(matches) != 1:
        findings.append(f"{names.version}: cannot locate VERSION parameter")
    else:
        actual = f"0x{matches[0][0].upper()}_{matches[0][1].upper()}"
        expected = ledger["facts"]["gateware_version"]
        if actual != expected:
            findings.append(
                f"gateware version conflict: ledger={expected}; "
                f"{names.version}={actual}")

    try:
        tree = ast.parse(command_text, filename=names.command)
    except SyntaxError as exc:
        findings.append(f"{names.command}: cannot parse source: {exc.msg}")
        tree = None
    served_nodes = [] if tree is None else [
        node.value for node in tree.body
        if isinstance(node, (ast.Assign, ast.AnnAssign)) and any(
            isinstance(target, ast.Name) and target.id == "SERVED"
            for target in (node.targets if isinstance(node, ast.Assign)
                           else [node.target]))
    ]
    if len(served_nodes) != 1 or not isinstance(served_nodes[0], ast.Dict):
        findings.append(f"{names.command}: cannot locate SERVED table")
    else:
        actual = []
        malformed = False
        for entry in served_nodes[0].values:
            if not (isinstance(entry, ast.Call) and
                    isinstance(entry.func, ast.Name) and
                    entry.func.id == "dict"):
                malformed = True
                continue
            name_values = [keyword.value for keyword in entry.keywords
                           if keyword.arg == "name"]
            if (len(name_values) != 1 or
                    not isinstance(name_values[0], ast.Constant) or
                    not isinstance(name_values[0].value, str)):
                malformed = True
                continue
            actual.append(name_values[0].value)
        if malformed:
            findings.append(f"{names.command}: SERVED has a malformed entry")
        expected = ledger["facts"]["served_aem_operations"]
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        if len(actual) != len(set(actual)):
            findings.append(f"{names.command}: SERVED repeats a command name")
        if missing or extra:
            findings.append(
                "served AEM inventory conflict: "
                f"missing-from-source={missing}; missing-from-ledger={extra}")
    if firmware_text is not None:
        findings.extend(
            boot_order_findings(ledger, firmware_text, names.firmware))
    return findings


def is_active_document(path: Path, relpath: str) -> bool:
    """Return whether a Markdown path is an active authority."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return True
    return is_active_document_text(text, relpath)


def parse_document(text: str, relpath: str) -> tuple[list[tuple[str, str, str, int]], list[str]]:
    """Return ``(claims, findings)`` from marked status blocks."""
    claims = []
    findings = []
    inside = in_comment = in_fence = False
    block_line = 0
    for lineno, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        if "<!--" in line and "-->" not in line:
            in_comment = True
            continue
        if stripped == BLOCK_START:
            if inside:
                findings.append(f"{relpath}:{lineno}: nested feature-status block")
            inside = True
            block_line = lineno
            continue
        if stripped == BLOCK_END:
            if not inside:
                findings.append(f"{relpath}:{lineno}: unmatched feature-status end")
            inside = False
            continue
        if not stripped.startswith("|"):
            continue
        if not inside:
            unmarked = ROW_RE.fullmatch(stripped)
            if (HEADER_RE.fullmatch(stripped) or
                    (unmarked and unmarked.group("status") in ALLOWED_STATUSES)):
                findings.append(
                    f"{relpath}:{lineno}: feature-status row is outside a "
                    "marked block")
            continue
        if HEADER_RE.fullmatch(stripped) or re.fullmatch(r"[|:\- ]+", stripped):
            continue
        match = ROW_RE.fullmatch(stripped)
        if not match:
            findings.append(f"{relpath}:{lineno}: malformed feature-status row")
            continue
        claims.append((match.group("feature"), match.group("status"),
                       match.group("value").strip(), lineno))
    if inside:
        findings.append(f"{relpath}:{block_line}: unclosed feature-status block")
    return claims, findings


def parse_fact_blocks(text: str, relpath: str) -> tuple[dict[str, tuple[list[str], int]], list[str]]:
    """Return machine-readable operation inventories from one document."""
    blocks = {}
    findings = []
    active_fact = None
    active_line = 0
    tokens = []
    in_comment = in_fence = False

    for lineno, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        if "<!--" in line and "-->" not in line:
            in_comment = True
            continue

        start = FACT_START_RE.fullmatch(stripped)
        if start:
            fact = start.group("fact")
            if active_fact is not None:
                findings.append(
                    f"{relpath}:{lineno}: nested feature-fact block")
            active_fact = fact
            active_line = lineno
            tokens = []
            continue

        end = FACT_END_RE.fullmatch(stripped)
        if end:
            fact = end.group("fact")
            if active_fact is None:
                findings.append(
                    f"{relpath}:{lineno}: unmatched feature-fact end")
            elif fact != active_fact:
                findings.append(
                    f"{relpath}:{lineno}: feature-fact end '{fact}' does not "
                    f"match '{active_fact}'")
            elif fact in blocks:
                findings.append(
                    f"{relpath}:{lineno}: duplicate feature-fact '{fact}'")
            else:
                blocks[fact] = (tokens, active_line)
            active_fact = None
            tokens = []
            continue

        if active_fact is not None:
            tokens.extend(
                token for token in FACT_TOKEN_RE.findall(line)
                if token not in FACT_NON_OPERATION_TOKENS)

    if active_fact is not None:
        findings.append(
            f"{relpath}:{active_line}: unclosed feature-fact '{active_fact}'")
    return blocks, findings


def _judge_paragraph(paragraph, marked, version, counts):
    """Judge one paragraph, reporting the line each match STARTS on.

    Prose here wraps at about seventy-eight columns, so `serves **thirty**
    AEM` ends one line and `opcodes plus …` begins the next. A line-at-a-
    time reader never saw that claim at all - the first live claim this
    rule was written for, and a silent pass is the one failure mode a
    consistency gate cannot have. A table row is judged alone: rows are
    records, and joining them would let one row's `VERSION` reach the next
    row's hexadecimal.

    Matches are appended to ``version`` and ``counts`` in document order.
    """
    if not paragraph:
        return
    joined, spans = "", []
    for lineno, line in paragraph:
        spans.append((len(joined), lineno))
        joined += line + " "

    def line_of(pos: int) -> int:
        """The document line an offset into the JOINED paragraph came from."""
        found = paragraph[0][0]
        for start, lineno in spans:
            if start <= pos:
                found = lineno
        return found

    for match in VERSION_CLAIM_RE.finditer(joined):
        version.append((line_of(match.start()), match.group(1),
                        marked == "gateware_version"))
    for count in COUNT_CLAIM_RE.finditer(joined):
        spelled = count.group("count").lower()
        if not is_number_token(spelled):
            continue
        fact = COUNT_FACTS[count.group("kind").split()[0]]
        counts.append((line_of(count.start()), fact, spelled,
                       marked == fact))


def _order_end_finding(relpath, lineno, fact, active_order, orders):
    """The complaint an ordered-fact END line earns, or ``None`` to record it."""
    if active_order is None:
        return f"{relpath}:{lineno}: unmatched feature-order end"
    if fact != active_order:
        return (f"{relpath}:{lineno}: feature-order end '{fact}' does not "
                f"match '{active_order}'")
    if fact in orders:
        return f"{relpath}:{lineno}: duplicate feature-order '{fact}'"
    return None


def _scan_claim_blocks(text, relpath):
    """Split one document into what the claim rules judge.

    Returns ``(paragraphs, orders, findings)``. Each paragraph is
    ``(lines, marked)`` - the ``(lineno, text)`` lines that belong together
    and the fact a preceding historic marker excuses, if any - in document
    order. ``orders`` are the ordered-fact blocks; ``findings`` are the
    block-structure complaints found while scanning. Fenced code, HTML
    comments and the fact blocks are skipped: a fact block already states the
    inventory under its own check, and re-judging its text would report one
    drift twice.
    """
    paragraphs, orders, findings = [], {}, []
    in_fence = in_comment = False
    in_fact = False
    historic_for = None
    active_order = None
    order_line = 0
    tokens = []
    paragraph = []

    def flush(paragraph: list[tuple[int, str]], marked: str | None) -> None:
        """Close one paragraph, carrying the fact a historic marker excuses."""
        paragraphs.append((paragraph, marked))

    for lineno, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        # A block quote wraps like any other prose, and its `>` would sit
        # between `AEM` and `opcodes` when the lines are joined - which is how
        # the README's own served-count claim escaped the first cut of this
        # rule. The marker is punctuation here, not content.
        stripped = re.sub(r"^(?:>\s*)+", "", stripped)
        boundary = (FENCE_RE.match(line) or in_fence or in_comment or
                    not stripped or stripped.startswith("|") or
                    stripped.startswith("<!--"))
        if boundary and paragraph:
            flush(paragraph, historic_for[0] if historic_for else None)
            historic_for = None
            paragraph = []
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue

        historic = VALUE_HISTORIC_RE.fullmatch(stripped)
        if historic:
            historic_for = (historic.group("fact"), lineno)
            continue
        start = ORDER_START_RE.fullmatch(stripped)
        if start:
            if active_order is not None:
                findings.append(f"{relpath}:{lineno}: nested feature-order "
                                f"block")
            active_order, order_line, tokens = start.group("fact"), lineno, []
            continue
        end = ORDER_END_RE.fullmatch(stripped)
        if end:
            fact = end.group("fact")
            problem = _order_end_finding(relpath, lineno, fact, active_order,
                                         orders)
            if problem is not None:
                findings.append(problem)
            else:
                orders[fact] = (tokens, order_line)
            active_order, tokens = None, []
            continue
        if FACT_START_RE.fullmatch(stripped):
            in_fact = True
            continue
        if FACT_END_RE.fullmatch(stripped):
            in_fact = False
            continue
        if "<!--" in line and "-->" not in line:
            in_comment = True
            continue
        if active_order is not None:
            tokens.extend(ORDER_TOKEN_RE.findall(line))
            continue
        if not stripped or in_fact:
            continue

        # A table row is a paragraph of its own (see flush); prose lines
        # accumulate until a boundary closes them.
        if stripped.startswith("|"):
            flush([(lineno, stripped)],
                  historic_for[0] if historic_for else None)
            historic_for = None
            continue
        paragraph.append((lineno, stripped))

    flush(paragraph, historic_for[0] if historic_for else None)
    if active_order is not None:
        findings.append(
            f"{relpath}:{order_line}: unclosed feature-order '{active_order}'")
    return paragraphs, orders, findings


def parse_value_claims(text: str, relpath: str) -> tuple[
        list[tuple[int, str, bool]], list[tuple[int, str, str, bool]],
        dict[str, tuple[list[str], int]], list[str]]:
    """Return ``(version, counts, orders, findings)`` for one document.

    ``version`` and ``counts`` are the prose repetitions rule 1 and rule 3
    judge; ``orders`` are ordered-fact blocks.
    """
    version, counts = [], []
    paragraphs, orders, findings = _scan_claim_blocks(text, relpath)
    for paragraph, marked in paragraphs:
        _judge_paragraph(paragraph, marked, version, counts)
    return version, counts, orders, findings


def check_value_claims(ledger: dict[str, Any], documents: dict[str, str]) -> list[str]:
    """Judge prose repetitions of ledger values, and ordered-fact blocks."""
    findings = []
    facts = ledger["facts"]
    canonical_version = facts["gateware_version"]
    canonical_major = canonical_version.split("_")[0].upper()
    seen_version = set()
    order_occurrences = defaultdict(dict)

    for relpath, text in sorted(documents.items()):
        version, counts, orders, parse_findings = parse_value_claims(
            text, relpath)
        findings.extend(parse_findings)
        for fact, block in orders.items():
            order_occurrences[fact][relpath] = block

        for lineno, value, historic in version:
            if value.split("_")[0].upper() != canonical_major:
                continue        # a retired major: history, not a claim
            matches = value.upper() == canonical_version.upper()
            if historic and matches:
                findings.append(
                    f"{relpath}:{lineno}: historic marker on the CURRENT "
                    f"version {canonical_version} — the value moved on to "
                    f"this line; drop the marker or restate the claim")
            elif historic:
                continue
            elif not matches:
                findings.append(
                    f"{relpath}:{lineno}: version claim {value} conflicts "
                    f"with the canonical {canonical_version} — correct it, or "
                    f"mark the line a record with "
                    f"<!-- milan-feature-value:gateware_version:historic -->")
            else:
                seen_version.add(relpath)

        for lineno, fact, spelled, historic in counts:
            expected = len(facts[fact])
            matches = spelled in number_spellings(expected)
            if historic and matches:
                findings.append(
                    f"{relpath}:{lineno}: historic marker on the CURRENT "
                    f"{fact} count {expected} — drop the marker or restate "
                    f"the claim")
            elif historic:
                continue
            elif not matches:
                findings.append(
                    f"{relpath}:{lineno}: {fact} count '{spelled}' conflicts "
                    f"with the canonical {expected}")

    for relpath in sorted(ledger["value_documents"]["gateware_version"]):
        if relpath not in documents:
            findings.append(
                f"value 'gateware_version' requires missing or inactive "
                f"{relpath}")
        elif relpath not in seen_version:
            findings.append(
                f"value 'gateware_version' is not stated in {relpath}")

    order_documents = ledger["order_documents"]
    for fact, claims in sorted(order_occurrences.items()):
        if fact not in order_documents:
            files = ", ".join(sorted(claims))
            findings.append(f"unknown feature order '{fact}' in {files}")
            continue
        for relpath, (tokens, lineno) in sorted(claims.items()):
            if relpath not in set(order_documents[fact]):
                findings.append(
                    f"feature order '{fact}' is not registered for {relpath}")
            if tokens != facts[fact]:
                findings.append(
                    f"feature order conflict '{fact}' in {relpath}:{lineno}: "
                    f"documented={tokens}; canonical={facts[fact]}")
    for fact, expected_documents in sorted(order_documents.items()):
        for relpath in expected_documents:
            if relpath not in documents:
                findings.append(
                    f"feature order '{fact}' requires missing or inactive "
                    f"{relpath}")
            elif relpath not in order_occurrences[fact]:
                findings.append(
                    f"feature order '{fact}' is not marked in {relpath}")
    return findings


def check_claims(ledger: dict[str, Any], documents: dict[str, str]) -> list[str]:
    """Check active ``documents`` mapping against a parsed ledger."""
    findings = []
    occurrences = defaultdict(list)
    per_file_ids = defaultdict(set)
    fact_occurrences = defaultdict(dict)

    for relpath, text in sorted(documents.items()):
        claims, parse_findings = parse_document(text, relpath)
        findings.extend(parse_findings)
        fact_blocks, fact_findings = parse_fact_blocks(text, relpath)
        findings.extend(fact_findings)
        for fact, block in fact_blocks.items():
            fact_occurrences[fact][relpath] = block
        for feature_id, status, value, lineno in claims:
            if feature_id in per_file_ids[relpath]:
                findings.append(
                    f"{relpath}:{lineno}: duplicate feature identifier '{feature_id}'")
                continue
            per_file_ids[relpath].add(feature_id)
            occurrences[feature_id].append((relpath, lineno, status, value))
            if status not in ALLOWED_STATUSES:
                findings.append(
                    f"{relpath}:{lineno}: feature '{feature_id}' has unknown "
                    f"status '{status}'")

    by_id = ledger["by_id"]
    for feature_id, claims in sorted(occurrences.items()):
        if feature_id not in by_id:
            files = ", ".join(sorted({claim[0] for claim in claims}))
            findings.append(
                f"unknown feature identifier '{feature_id}' in {files}")
            continue
        expected = by_id[feature_id]
        expected_status = expected["status"]
        expected_value = expected.get("value", "-")
        wrong = [claim for claim in claims
                 if claim[2] != expected_status or claim[3] != expected_value]
        if wrong:
            rendered = ", ".join(
                f"{path}:{line}={status}/{value}"
                for path, line, status, value in claims)
            findings.append(
                f"feature status conflict '{feature_id}': canonical="
                f"{expected_status}/{expected_value}; claims: {rendered}")

    for feature_id, feature in sorted(by_id.items()):
        for relpath in feature["documents"]:
            if relpath not in documents:
                findings.append(
                    f"feature '{feature_id}' requires missing or inactive {relpath}")
            elif feature_id not in per_file_ids[relpath]:
                findings.append(
                    f"feature '{feature_id}' is not marked in {relpath}")

    fact_documents = ledger["fact_documents"]
    for fact, claims in sorted(fact_occurrences.items()):
        if fact not in fact_documents:
            files = ", ".join(sorted(claims))
            findings.append(f"unknown feature fact '{fact}' in {files}")
            continue
        expected_documents = set(fact_documents[fact])
        for relpath, (tokens, lineno) in sorted(claims.items()):
            if relpath not in expected_documents:
                findings.append(
                    f"feature fact '{fact}' is not registered for {relpath}")
            duplicates = sorted({token for token in tokens
                                 if tokens.count(token) > 1})
            missing = sorted(set(ledger["facts"][fact]) - set(tokens))
            extra = sorted(set(tokens) - set(ledger["facts"][fact]))
            if duplicates or missing or extra:
                findings.append(
                    f"feature fact conflict '{fact}' in {relpath}:{lineno}: "
                    f"missing={missing}; extra={extra}; "
                    f"duplicates={duplicates}")
    for fact, expected_documents in sorted(fact_documents.items()):
        for relpath in expected_documents:
            if relpath not in documents:
                findings.append(
                    f"feature fact '{fact}' requires missing or inactive "
                    f"{relpath}")
            elif relpath not in fact_occurrences[fact]:
                findings.append(
                    f"feature fact '{fact}' is not marked in {relpath}")
    findings.extend(check_value_claims(ledger, documents))
    return sorted(set(findings))


def active_markdown_documents(repo: Path) -> dict[str, str]:
    """Read active tracked Markdown, with a filesystem fallback for archives."""
    sys.path.insert(0, str(repo / "scripts"))
    import docs_check  # pylint: disable=import-outside-toplevel

    documents = {}
    for relpath in docs_check.tracked("*.md"):
        path = repo / relpath
        if is_active_document(path, relpath):
            documents[relpath] = path.read_text(encoding="utf-8")
    return documents


def run_self_test() -> list[str]:
    """Exercise a clean case and every required negative control.

    The arms themselves live in ``check_feature_status_selftest``: they are
    one long list of independent fixtures with no reader in common with the
    rules above, and importing them only when ``--self-test`` is asked for
    keeps the gate's own import free of them.
    """
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from check_feature_status_selftest import run_self_test as run_arms
    return run_arms()


def is_active_document_text(text: str, relpath: str) -> bool:
    """Text-only twin used by the archive and obsolete fixtures."""
    if ARCHIVE_PARTS.intersection(Path(relpath).parts):
        return False
    lines = text.splitlines()
    return not lines or not OBSOLETE_RE.fullmatch(lines[0])


def main() -> int:
    """Check the ledger, its sources and the active documentation; 1 on a finding."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true",
                        help="run fixture tests before checking the tree")
    args = parser.parse_args()

    failed = run_self_test() if args.self_test else []
    try:
        raw_ledger = LEDGER.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"{LEDGER.relative_to(REPO)}: {exc}")
        return 1
    ledger, findings = load_ledger_text(
        raw_ledger, str(LEDGER.relative_to(REPO)))
    if ledger is not None:
        try:
            version_text = VERSION_SOURCE.read_text(encoding="utf-8")
            command_text = COMMAND_SOURCE.read_text(encoding="utf-8")
            firmware_text = FIRMWARE_SOURCE.read_text(encoding="utf-8")
        except OSError as exc:
            findings.append(str(exc))
        else:
            findings.extend(check_source_facts(
                ledger, version_text, command_text, firmware_text,
                SourceNames(str(VERSION_SOURCE.relative_to(REPO)),
                            str(COMMAND_SOURCE.relative_to(REPO)),
                            str(FIRMWARE_SOURCE.relative_to(REPO)))))
        findings.extend(check_claims(ledger, active_markdown_documents(REPO)))
    for finding in findings:
        print(finding)
    print(f"feature_status: {len(findings)} finding(s)")
    return 1 if failed or findings else 0


if __name__ == "__main__":
    sys.exit(main())
