"""Render the handoff from committed identity and recorded gate receipts."""
import hashlib
import json
from pathlib import Path
import shlex

OUT = Path(__file__).resolve().parent
identity = json.loads((OUT/'source-identity.json').read_text())
head = identity['head']
base = identity['base']
text = f"""# Round 2 handoff

Author: [A352]. Issues #573-#576; PR #585.
Branch: `{identity['branch']}`.
Starting head: `4f746408a15f494c4b30bdc9add6d7295309dff9`.
Final head: `{head}`.
Comparison base: `{base}`.
Remote verified: `https://github.com/kebag-logic/milan-fpga.git`.

Implementation is complete in five item-group commits.
Both full builder modes and the code/documentation gates return zero.
The unchanged historical format-length reproducer has the documented rc 1.
Independent re-review of all five lenses is required.
This author evidence does not clear the reviewer-owned completion ledger.
No tracked configuration was refused; the STOP rule did not trigger.
No push, PR change, merge, hardware activity or submodule edit occurred.

## Public contract and authorities

- [Assignment and decisions](https://github.com/kebag-logic/milan-fpga/issues/573#issuecomment-5854262940).
- [Internal review](https://github.com/kebag-logic/milan-fpga/pull/585#issuecomment-5854235849).
- [External review](https://github.com/kebag-logic/milan-fpga/pull/585#issuecomment-5854260028).
- Full reports and unchanged scripts came from branch `573-review-evidence`,
  under `review-evidence/573-r1/reviews/R340-1/` and `R341-1/`.
  Fetched evidence commit: `{identity['review_evidence_head']}`.
- IEEE 1722.1-2021 section 7.2: descriptor maximum 508 octets.
  Table 7-8: formats_offset 138, number_of_formats maximum 46,
  buffer_length width four octets.
- Milan v1.2 5.3.3.1 applies the reserved-ID rule to ENTITY;
  5.6.2 applies it to ADPDUs. Section 5.3.1 remains evolution-only.
- Only PDF pages 64-65, 73-74 (IEEE) and 32, 108 (Milan) were
  extracted with `pdftotext -layout -f/-l`; extracts remain under `/tmp`.
  Processor-owned cap statements remain assigned to processor issue 60.

## Change list

| Group | Commit | Files and behavior |
|---|---|---|
| 1 | `2a15d68b7cf8475547ab9ae43cba93266b0be627` | `avdecc/aem_descriptors.py:272` owns layout-derived `MAX_STREAM_FORMATS`; `sw/builder/endstation_builder.py:1395` enforces it after completion; `sw/builder/test_declarations.py:153` checks 46/47 final entries and packed length; README:128 and matrix:62,243 state 46. |
| 2 | `71b614ba6061c147d7781985c20309e3c0af8b96` | `avdecc/aem_descriptors.py:183` shares u32 encoding and maximum; `sw/builder/endstation_builder.py:1380` refuses overflow; `sw/builder/test_declarations.py:103` verifies packed equality at every listener index; README:131 and matrix:62,242 describe both bounds. |
| 3 | `d20eeb892b669060278f669be977b0540f7c0d34` | `sw/builder/endstation_builder.py:1339`, `sw/builder/test_declarations.py:36,46`, README:153 and matrix:67 cite the correct ENTITY/ADPDU clauses. |
| 4 | `5cf31b2c2628903b03998b3a19623a13a313db5e` | `docs/ENDSTATION_BUILDER.md:443` states the enforced refusal. Optional parameter-table expansion was unnecessary. |
| 5 | `{head}` | `sw/builder/endstation_builder.py:1329,3841,4373` preserves numeric EUI-64 values, refuses empty sources and validates shadowed/derived identities. `sw/builder/test_declarations.py:69,218` covers each accepted suggestion. README:121,150 and matrix:64,193 describe the resulting contracts. |

All line references name the final head. README means
`sw/builder/README-parameters.md`; matrix means
`docs/reference/PP_DESCRIPTOR_OWNERSHIP.md`.

## Finding and disposition table

| Finding | Reviewer severity and lenses | Disposition | Discriminating evidence |
|---|---|---|---|
| R341-1 F1 | MAJOR; Conformance, Robustness, Tests, Docs | Fixed; re-review pending | 46 final entries accepted in both directions; 47 refused. Listeners accept 45+1 and refuse 46+1. Accepted boundary packs to 506 bytes. Raising the cap is killed. |
| R340-F1 / R341-1 F2 | MAJOR governs; Conformance, RTL, Robustness, Tests | Fixed; re-review pending | Every listener accepts and packs 0xFFFFFFFF unchanged; 2^32 and 2^32+2125999 refuse. Width comes from the same Struct used to pack. Removing the upper guard is killed. Unchanged buffer probe confirms results. |
| R340-F3 / R341-1 F3 | MINOR; Conformance, Docs | Fixed under public clause decision; re-review pending | Message, test comments, README and L9 cite 5.3.3.1/5.6.2. Evolution keeps 5.3.1. |
| R340-F2 | MINOR; Docs | Fixed; re-review pending | Builder design doc now describes named reserved-ID refusal. |
| R340-S1 | SUGGESTION; Tests | Implemented | Direct helper call with no AAF talker refuses CRF output without INTERNAL. Removed CRF arm fails that exact assertion. |
| R340-S2 | SUGGESTION; Robustness | Implemented; also addresses #495 R331-1 S3 | Empty sources refuse with L6 ConfigError, with default present or omitted. `[internal]` remains accepted. |
| R340-S3 | SUGGESTION; Robustness | Implemented | Literal guard runs even with a pin; both reserved literals refuse. A valid pin still wins over a valid literal. |
| R341-1 S1 | SUGGESTION; Robustness | Implemented using exact numeric parsing | Quoted/unquoted YAML hex IDs preserve the written value for literal and pin keys. Reinterpretation mutant is killed. |
| R341-1 S2 | SUGGESTION; Conformance | Implemented | Literal, pin and resolved hash use `_model_id`; forced derived endpoints refuse and legal derived control passes. Bypass mutant is killed. |

## Mutation evidence

Unchanged reviewer runners execute only in a committed archive export.
Each mutation is restored before the next; restored controls pass.
The first runner detects 30/30 original mutations.
The second detects 26/26 applicable original mutations.
Its R-M8 and R-M14 patterns name the removed `MAX_STREAM_FORMATS = 47`
assignment. They remain unchanged and report `applied: false`.
A new cap-plus-one mutation independently covers the current derived bound.
Eight round-2 mutations are detected. Counts include overlapping executions.

| Runner | Mutation | Result | Observable failure |
|---|---|---|---|
"""
for file, label in [('review-mutants-340.json','Internal original'), ('round2-mutants-result.json','Round 2')]:
    for row in json.loads((OUT/file).read_text())[:-2]:
        failure = row['last_line'].replace('|','/').replace('\n',' ')
        text += f"| {label} | {row['id']} | {row['verdict']} (rc {row['returncode']}) | {failure} |\n"
for row in json.loads((OUT/'review-mutants-341.json').read_text())['cases']:
    state = row.get('verdict','NOT APPLIED: obsolete literal pattern')
    failure = row.get('last_line','No current source match').replace('|','/')
    text += f"| External original | {row['case']} | {state} | {failure} |\n"
text += """
## Five-configuration SHA256 tables

The unchanged internal artifact script produced 85 records per revision:
17 artifacts for each of five configurations. Sizes and SHA256 agree 85/85.
The unchanged external shipping script independently agrees for 80/80 files.
Its inventory omits the five in-memory sweep option strings.
Full JSON receipts are `hashes-base.json` and `hashes-head.json`;
external tables are `shipping-base.sha256` and `shipping-head.sha256`.

Builds include all three Arty configurations, preserving #583 behavior.
Exports came from `git archive` at the two commits, with pinned inputs
exported independently. No other implementation lane was read or changed.
Disposable Git metadata supplies the original HEAD and tracked inventory
required by the unchanged reviewer scripts. All trees remain under `/tmp`.
`export_archives.py` records the exact procedure.

"""
before = json.loads((OUT/'hashes-base.json').read_text())
after = {(r['configuration'],r['artifact']):r for r in json.loads((OUT/'hashes-head.json').read_text())}
for name in sorted({r['configuration'] for r in before}):
    text += f"### {name}\n\n| Artifact | Bytes | Base SHA256 | Head SHA256 |\n|---|---:|---|---|\n"
    for row in [r for r in before if r['configuration']==name]:
        final = after[name,row['artifact']]
        text += f"| `{row['artifact']}` | {row['bytes']} | `{row['sha256']}` | `{final['sha256']}` |\n"
    text += '\n'
text += """## Gate table

All commands run from `$LANES/573-builder-refusals`.
Reviewer arguments point to disposable archive exports as assigned.
`$EVIDENCE` denotes this directory. `run_gate.py` runs the command directly,
without a pipeline, with a 10800-second limit and its actual return code.
Raw logs remain under `/tmp/573-a352`; public logs scrub home-path identity.
Large text logs are split below 200 KB per file, preserving their contents.
Required Markdown packages live only in `/tmp/573-a352/env`.

| Gate | Exact command | rc | Seconds | Receipt |
|---|---|---:|---:|---|
"""
for p in sorted(OUT.glob('*.result.json')):
    row = json.loads(p.read_text())
    command = shlex.join(row['command']).replace(str(OUT), '$EVIDENCE')
    text += f"| {row['gate']} | `{command}` | {row['returncode']} | {row['seconds']} | `{p.name}` |\n"
for name in ('builder-present','builder-absent'):
    if not (OUT/f'{name}.result.json').exists():
        text += f'| {name} | Full builder entry | Pending | Pending | Pending |\n'
text += """
### Full builder limits

The full compiler-present bank returns rc 0. Its gate 11 utilization
calibration arm is NOT RUN because the pre-existing build report is absent.
The full compiler-absent bank also returns rc 0. Its gate 1b compiled
instruments are deliberately NOT RUN; gate 11 is likewise NOT RUN.
All three RV32 candidates were audited as hidden. The absent result
is not compiler evidence. No hardware or
physical calibration was run. These limits do not affect descriptor bytes.

### Historical script exception

`format_cap_length.py` is preserved byte-for-byte. It has no ConfigError
handler and assumes both 46 and 47 are accepted. At this head it prints the
accepted 46-format / 506-byte result, then exits 1 on the mandated named
47-format refusal. Consequently, the requested all-zero raw reviewer-script
exit condition cannot coexist with the required fix and unchanged script.
No failed return code is relabeled zero. `verify_round2.py` separately checks
this exact expected rejection, artifact identity, mutation kills, source
restoration and passing controls; its own result is rc 0.
The obsolete R-M8/R-M14 source patterns are likewise reported, not counted killed.

## Remaining responsibilities

Independent reviewers must re-cover Conformance, RTL, Robustness, Tests and Docs
at the final head and publish their own completion ledger.
The coordinator owns publication, hosted/local workflow evidence and any later
candidate-merge validation. No merge approval is requested or inferred here.
Processor-owned cap corrections remain in processor issue 60.
Evolution and model-history comparison remain with #495 and processor issue 38.
`PR-BODY.md` is a replacement draft only; the PR has not been edited.
Both full builder modes have finished. The final integrity record is
`final-integrity.json`; the prepared issue comment is `REVIEW-READY.md`.
"""
if (OUT/'final-integrity.json').exists():
    integrity = json.loads((OUT/'final-integrity.json').read_text())
    text += '\n## Final integrity\n\n'
    text += f"Head: `{integrity['head']}`. Worktree and index: clean.\n"
    text += 'Pinned submodule revisions and tracked bytes are unchanged.\n'
    text += 'The five round-2 commit messages are single subjects without trailers.\n'
if (OUT/'review-ready-url.txt').exists():
    url = (OUT/'review-ready-url.txt').read_text().strip()
    text += f'\n[A352] REVIEW READY posted on [issue #573]({url}).\n'
(OUT/'HANDOFF.md').write_text(text)
