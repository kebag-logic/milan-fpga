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
ARCHIVE_PARTS = {"historical_now_obsolete", "archive", "archived", "archives"}
VERSION_SOURCE = REPO / "hdl/common/csr/milan_csr.sv"
COMMAND_SOURCE = REPO / "tests/steps/aecp_engine_steps.py"


class DuplicateKey(ValueError):
    """Raised when a JSON object repeats a key."""


def _object_without_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKey(f"duplicate JSON key '{key}'")
        result[key] = value
    return result


def load_ledger_text(text, source="ledger"):
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

    features = data.get("features")
    if not isinstance(features, list):
        findings.append(f"{source}: features must be a list")
        return None, findings

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

    if findings:
        return None, findings
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
    if findings:
        return None, findings
    data["by_id"] = by_id
    return data, []


def check_source_facts(ledger, version_text, command_text,
                       version_source="milan_csr.sv",
                       command_source="aecp_engine_steps.py"):
    """Tie version and served-command facts to their source declarations."""
    findings = []
    version_code = re.sub(r"/\*.*?\*/", "", version_text, flags=re.DOTALL)
    version_code = re.sub(r"//[^\n]*", "", version_code)
    matches = re.findall(
        r"parameter\s+logic\s*\[31:0\]\s+VERSION\s*=\s*32'h"
        r"([0-9A-Fa-f]{4})_([0-9A-Fa-f]{4})", version_code)
    if len(matches) != 1:
        findings.append(f"{version_source}: cannot locate VERSION parameter")
    else:
        actual = f"0x{matches[0][0].upper()}_{matches[0][1].upper()}"
        expected = ledger["facts"]["gateware_version"]
        if actual != expected:
            findings.append(
                f"gateware version conflict: ledger={expected}; "
                f"{version_source}={actual}")

    try:
        tree = ast.parse(command_text, filename=command_source)
    except SyntaxError as exc:
        findings.append(f"{command_source}: cannot parse source: {exc.msg}")
        tree = None
    served_nodes = [] if tree is None else [
        node.value for node in tree.body
        if isinstance(node, (ast.Assign, ast.AnnAssign)) and any(
            isinstance(target, ast.Name) and target.id == "SERVED"
            for target in (node.targets if isinstance(node, ast.Assign)
                           else [node.target]))
    ]
    if len(served_nodes) != 1 or not isinstance(served_nodes[0], ast.Dict):
        findings.append(f"{command_source}: cannot locate SERVED table")
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
            findings.append(f"{command_source}: SERVED has a malformed entry")
        expected = ledger["facts"]["served_aem_operations"]
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        if len(actual) != len(set(actual)):
            findings.append(f"{command_source}: SERVED repeats a command name")
        if missing or extra:
            findings.append(
                "served AEM inventory conflict: "
                f"missing-from-source={missing}; missing-from-ledger={extra}")
    return findings


def is_active_document(path, relpath):
    """Return whether a Markdown path is an active authority."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return True
    return is_active_document_text(text, relpath)


def parse_document(text, relpath):
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


def check_claims(ledger, documents):
    """Check active ``documents`` mapping against a parsed ledger."""
    findings = []
    occurrences = defaultdict(list)
    per_file_ids = defaultdict(set)

    for relpath, text in sorted(documents.items()):
        claims, parse_findings = parse_document(text, relpath)
        findings.extend(parse_findings)
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
    return sorted(set(findings))


def active_markdown_documents(repo):
    """Read active tracked Markdown, with a filesystem fallback for archives."""
    sys.path.insert(0, str(repo / "scripts"))
    import docs_check  # pylint: disable=import-outside-toplevel

    documents = {}
    for relpath in docs_check.tracked("*.md"):
        path = repo / relpath
        if is_active_document(path, relpath):
            documents[relpath] = path.read_text(encoding="utf-8")
    return documents


def run_self_test():
    """Exercise a clean case and every required negative control."""
    base = {
        "schema_version": 1,
        "facts": {
            "gateware_version": "0x0002_0051",
            "served_aem_operations": ["READ_DESCRIPTOR"],
            "served_mvu_operations": ["GET_MILAN_INFO"],
            "missing_mandatory_aem_operations": ["SET_NAME"]
        },
        "features": [{
            "id": "aem.read-descriptor",
            "status": "implemented",
            "summary": "fixture",
            "documents": ["one.md", "two.md"]
        }]
    }
    row = (f"{BLOCK_START}\n| Feature ID | Status | Canonical value |\n"
           "|---|---|---|\n"
           "| `aem.read-descriptor` | `implemented` | - |\n"
           f"{BLOCK_END}\n")

    ledger, findings = load_ledger_text(json.dumps(base), "fixture")
    cases = []
    cases.append(("clean", not findings and not check_claims(
        ledger, {"one.md": row, "two.md": row})))

    conflict = row.replace("`implemented`", "`missing`")
    conflict_findings = check_claims(
        ledger, {"one.md": row, "two.md": conflict})
    cases.append(("status conflict", any(
        "aem.read-descriptor" in item and "one.md" in item and "two.md" in item
        for item in conflict_findings)))

    duplicate = json.loads(json.dumps(base))
    duplicate["features"].append(dict(duplicate["features"][0]))
    _, duplicate_findings = load_ledger_text(json.dumps(duplicate), "fixture")
    cases.append(("duplicate identifier", any(
        "duplicate feature identifier" in item for item in duplicate_findings)))

    unknown_status = json.loads(json.dumps(base))
    unknown_status["features"][0]["status"] = "available"
    _, status_findings = load_ledger_text(json.dumps(unknown_status), "fixture")
    cases.append(("unknown status", any(
        "unknown status" in item for item in status_findings)))

    non_string_status = json.loads(json.dumps(base))
    non_string_status["features"][0]["status"] = []
    _, non_string_findings = load_ledger_text(
        json.dumps(non_string_status), "fixture")
    cases.append(("non-string status", any(
        "unknown status" in item for item in non_string_findings)))

    unknown_row = row.replace("aem.read-descriptor", "aem.unknown")
    unknown_findings = check_claims(
        ledger, {"one.md": unknown_row, "two.md": row})
    cases.append(("unknown reference", any(
        "unknown feature identifier 'aem.unknown'" in item
        for item in unknown_findings)))

    header_value_row = row.replace(
        "| `aem.read-descriptor` | `implemented` | - |",
        "| `aem.unknown` | `implemented` | Feature ID |")
    header_value_findings = check_claims(
        ledger, {"one.md": header_value_row, "two.md": row})
    cases.append(("header text in value", any(
        "unknown feature identifier 'aem.unknown'" in item
        for item in header_value_findings)))

    fenced = f"```markdown\n{row}```\n"
    fenced_findings = check_claims(
        ledger, {"one.md": row, "two.md": fenced})
    cases.append(("fenced claim ignored", any(
        "not marked in two.md" in item for item in fenced_findings)))

    fenced_example = row + "\n~~~markdown\n" + unknown_row + "~~~\n"
    fenced_example_findings = check_claims(
        ledger, {"one.md": fenced_example, "two.md": row})
    cases.append(("fenced example ignored", not any(
        "aem.unknown" in item for item in fenced_example_findings)))

    unmarked_findings = check_claims(
        ledger, {"one.md": row, "two.md": row.replace(
            f"{BLOCK_START}\n", "").replace(f"{BLOCK_END}\n", "")})
    cases.append(("unmarked claim rejected", any(
        "outside a marked block" in item for item in unmarked_findings)))

    obsolete = "[OBSOLETE + 2026-08-18]\n" + conflict
    cases.append(("obsolete banner", not is_active_document_text(obsolete,
                                                                  "old.md")))
    cases.append(("archive path", not is_active_document_text(
        conflict, "historical_now_obsolete/old.md")))

    version_text = "parameter logic [31:0] VERSION = 32'h0002_0051;"
    command_text = 'SERVED = {0: dict(name="READ_DESCRIPTOR")}\n'
    cases.append(("source facts", not check_source_facts(
        ledger, version_text, command_text)))
    cases.append(("source version drift", any(
        "gateware version conflict" in item for item in check_source_facts(
            ledger, version_text.replace("0051", "0052"), command_text))))
    cases.append(("source inventory drift", any(
        "served AEM inventory conflict" in item for item in check_source_facts(
            ledger, version_text,
            command_text.replace("READ_DESCRIPTOR", "SET_NAME")))))
    cases.append(("commented source ignored", not check_source_facts(
        ledger,
        "// parameter logic [31:0] VERSION = 32'h0002_0052;\n" + version_text,
        '# SERVED = {0: dict(name="SET_NAME")}\n' + command_text)))

    for name, passed in cases:
        print(f"  {'PASS' if passed else 'FAIL'}  {name}")
    failed = [name for name, passed in cases if not passed]
    print(f"feature_status self-test: {len(cases) - len(failed)}/{len(cases)} passed")
    return failed


def is_active_document_text(text, relpath):
    """Text-only twin used by the archive and obsolete fixtures."""
    if ARCHIVE_PARTS.intersection(Path(relpath).parts):
        return False
    lines = text.splitlines()
    return not lines or not OBSOLETE_RE.fullmatch(lines[0])


def main():
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
        except OSError as exc:
            findings.append(str(exc))
        else:
            findings.extend(check_source_facts(
                ledger, version_text, command_text,
                str(VERSION_SOURCE.relative_to(REPO)),
                str(COMMAND_SOURCE.relative_to(REPO))))
        findings.extend(check_claims(ledger, active_markdown_documents(REPO)))
    for finding in findings:
        print(finding)
    print(f"feature_status: {len(findings)} finding(s)")
    return 1 if failed or findings else 0


if __name__ == "__main__":
    sys.exit(main())
