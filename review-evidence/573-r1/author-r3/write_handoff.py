"""Assemble the author handoff from retained executable receipts."""
import json
from pathlib import Path
import shlex
import subprocess

out = Path(__file__).resolve().parent
root = Path('$LANES/573-builder-refusals')
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
results = [json.loads(line) for line in (out / 'gate-results.jsonl').read_text().splitlines()]
by_gate = {row['gate']: row for row in results}
complete = all(name in by_gate and by_gate[name]['returncode'] == 0
               for name in ('builder-present', 'builder-absent'))
status = 'Local assignment complete; ready for independent review.' if complete else 'Implementation complete; full builder gates still running.'
text = f'''# Round 3 author handoff

{status}

Head: `{head}`. Branch: `573-builder-model-refusals`.
Starting head: `08374721d958b32ade38e7e62d25a7ccea215119`.
Remote verified: `https://github.com/kebag-logic/milan-fpga.git`.
Working directory: `$LANES/573-builder-refusals`.

The author implements the [round-3 decision](https://github.com/kebag-logic/milan-fpga/issues/573#issuecomment-5854630094).
The internal [round-2 report](https://github.com/kebag-logic/milan-fpga/pull/585#issuecomment-5854625819)
and external [round-2 report](https://github.com/kebag-logic/milan-fpga/pull/585#issuecomment-5854626574)
were read with their full public evidence packets.

## Commits and change list

Each item group has one commit, with a one-line subject and no trailers.

| Group | Commit | Change and exact source location |
|---|---|---|
| F1 | `9e47e48c650ea70b2744696a10061d862f89a3bd` | `sw/builder/endstation_builder.py:1329`: reject non-string hex inputs with field name and quote instruction. `:4376`: a declared null pin refuses. `:4379`: format internal hash output as hex text before the reserved-ID guard. |
| F1 tests/docs | Same commit | `sw/builder/test_declarations.py:92`: eight field paths, actual YAML text, quoted prefixed/unprefixed digits, underscores, integer/octal spellings and non-string types. `sw/builder/README-parameters.md:152` and `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:198`: the string and quote contract. |
| F2 | `0d5820aee25e41d8bc9f83a36231c46986dfcfea` | `scripts/audit_pp_descriptors.py:210`: add the legal 46-entry/506-octet control; `:211`: label 47/514 as above the 2021 cap. `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:168`: report processor acceptance as PP60 defence-in-depth debt. |
| S1 | `8c956234699b5dec5e6c9aeada651be667974e9b` | `avdecc/aem_descriptors.py:187`: strict unsigned packing through the existing encoding, without a mask. `sw/builder/test_declarations.py:150`: exact bytes at zero and maximum; negative and overflow refusals. `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:38`: document the shared packing boundary. |

No tracked configuration was changed or refused. The STOP condition never occurred.
No HDL or submodule change was made. No push, pull-request edit, merge or hardware work was performed.

## Finding and disposition table

These are author dispositions, not reviewer approval or a completion ledger.

| Finding | Author disposition | Evidence and remaining ownership |
|---|---|---|
| R340-2 F1 / R341-2 F1 (MINOR: Conformance, Robustness, Tests, Docs) | Implemented | All eight `_eui64`/`_fmt64` input paths reject non-strings by field with a quote instruction. Both unchanged round-2 probes return zero; no accepted scalar changes its written hex value. A3-01 restores integer acceptance and is killed. |
| R340-2 F2 / R341-2 F2 (MINOR: Conformance, Docs; external report assigns Docs) | Implemented | Both legal 46/506 and invalid 47/514 packer probes remain accepted, accurately labelled. Parent declarations reject 47. `audit-l4-probes.json` retains the observed processor acceptance. PP60 owns its semantic refusal. |
| R341-2 S1, taken (SUGGESTION: Robustness) | Implemented | `be32` raises `struct.error` outside u32. A3-05 restores masking and is killed. Both artifact inventories remain identical. `be16` and `be64` were outside this assignment. |
| R340-2 S1, boolean part | Covered by assigned non-string rule | Boolean declarations are tested on all eight paths. The old mutation pattern no longer applies; current integer/boolean restoration is killed by A3-02. |
| R340-2 S1, null media-clock-source test suggestion | Optional, unchanged | Production refusal remains correct. The unchanged R2-17 PROBE mutation still survives the declaration suite; no clean coverage claim is made for that suggestion. |
| R340-2 S2, parameter-table expansion | Optional, not assigned | No expansion of the large design-document parameter table. Its primary identity discussion was already corrected in round 2. |
| Earlier round findings | Preserved | Format cap, listener floor/width, reserved-ID clauses, shadowed literals, hash endpoints and clock-source rules retain their controls. Both historical mutation banks and probes were rerun unchanged. |

The shared scalar tests decode arbitrary quoted hex digits independently of later field semantics.
`"1234567890123456"` is a valid 64-bit number but cannot be a MAC-48 destination or a supported AAF word.
Those fields use their own legal quoted controls through the complete loader, while all three assigned unquoted numeric spellings receive the quote refusal before their width/family checks.
All identity fields also resolve that quoted digit-only spelling through the complete loader.
The loader enforces YAML string type; a plain scalar already resolved as a string retains its hex value. Documentation tells users to quote values to avoid YAML numeric resolution.

## Standards evidence

Only cited pages were extracted with `pdftotext -f/-l` into `/tmp`.
IEEE 1722.1-2021 PDF page 64 supplies section 7.2; pages 73-74 supply Table 7-8.
The maximum descriptor is 508 octets, formats start at 138, and the count maximum is 46.
Milan v1.2 PDF pages 32 and 108 supply 5.3.3.1 and 5.6.2 respectively.
Both prohibit zero and all-ones model IDs. See [source hashes and extraction receipt](standards-receipt.txt).

## Mutation table

All mutation runs use an exact committed archive export under `/tmp`.
Every restored control returns zero, and every mutated source is restored byte-identically.
Old patterns absent from the new source are reported as not applied, never killed.
Current replacements cover the changed integer parser and hash-derived guard.

| Bank | Mutation | Outcome |
|---|---|---|
'''
banks = [
    ('Author round 3', 'author-mutants.json'),
    ('Internal round 2', 'internal-mutants.json'),
    ('External round 2', 'reviewer-external-mutants.log'),
    ('Internal historical', 'historical-internal-mutants.json'),
    ('External historical', 'historical-external-mutants.log'),
]
for bank, name in banks:
    data = json.loads((out / name).read_text())
    cases = data if isinstance(data, list) else data['cases']
    for case in cases:
        identity = case.get('id', case.get('case', ''))
        if 'control' in identity or 'restored' in identity:
            continue
        outcome = 'NOT APPLIED: old source pattern absent' if case.get('applied') is False else case['verdict']
        if case.get('expect') == 'PROBE':
            outcome += ' (optional PROBE)'
        text += f'| {bank} | {identity.replace("|", "/")} | {outcome} |\n'
text += '''
The historical format-length script has no exception handler for the corrected 47-entry refusal.
Its unchanged raw exit is 1, retained in [raw output](format-reproducer-raw.log).
The [separate evidence check](check_format_reproducer.py) requires that exact refusal plus the accepted 46-entry/506-octet boundary and returns zero.
This expected raw nonzero is not presented as a zero exit from the historical script.

## SHA-256 tables against e0920d77

Baseline: `e0920d77162284d8da52ffaf13a973e451e44f90`.
Both versions were generated from committed archive exports, including each pinned submodule's archive.
Both unchanged reviewer inventories match: 85/85 generated artifacts and 80/80 CLI artifacts.
All five configurations, including all three Arty configurations, are accepted.
These are source/artifact checks, not bitstream or hardware qualification.

### Generated artifact inventory

The SHA-256 column gives the exact shared baseline/head hash; sizes match too.
Full independent inputs: [baseline](artifacts-base.json) and [head](artifacts-head.json).

| Configuration | Artifact | Bytes | Baseline = head SHA-256 |
|---|---|---:|---|
'''
base = json.loads((out / 'artifacts-base.json').read_text())
candidate = json.loads((out / 'artifacts-head.json').read_text())
assert base == candidate and len(candidate) == 85
for row in candidate:
    text += f'| {row["configuration"].removeprefix("endstation_")} | `{row["artifact"]}` | {row["bytes"]} | `{row["sha256"]}` |\n'
text += '''
### Independent CLI inventory

The CLI inventory includes generated headers and the store/image boundaries.
Full inputs: [baseline](shipping-base.sha256) and [head](shipping-head.sha256).

| Artifact | Baseline = head SHA-256 |
|---|---|
'''
baseline = (out / 'shipping-base.sha256').read_text()
candidate = (out / 'shipping-head.sha256').read_text()
assert baseline == candidate and len(candidate.splitlines()) == 80
for line in candidate.splitlines():
    digest, path = line.split(maxsplit=1)
    text += f'| `{path}` | `{digest}` |\n'
text += '''
## Gate table

Commands ran in the foreground, without output pipelines. Each gate retains its actual exit.
The two builder modes and focused gates use the physical `/data` candidate path.
Reviewer mutations and artifact generation use committed archive exports.
`builder_absent.py` hides only the three RV32 compiler candidates in process; no compiler is modified.
The complete builder entry point runs in both modes.
The pinned Markdown dependencies are installed only in disposable scratch.

| Gate | Exit | Seconds | Evidence | Exact command |
|---|---:|---:|---|---|
'''
for row in results:
    command = shlex.join(row['command']).replace('|', '\\|')
    text += f'| {row["gate"]} | {row["returncode"]} | {row["seconds"]} | [{row["evidence"]}]({row["evidence"]}) | `{command}` |\n'
for name in ('builder-present', 'builder-absent'):
    if name not in by_gate:
        text += f'| {name} | PENDING | - | - | Full bank still pending |\n'
text += '''
The gate receipt also records working directories, complete-log sizes and SHA-256 hashes: [gate-results.jsonl](gate-results.jsonl).
Logs above 190000 bytes are retained as bounded excerpts; complete logs stay in `/tmp/573-a355/logs`.
No toolchain, environment, tree export, installed package or file over 200 KB is stored in this output directory.

## Reviewer script provenance and reproduction

The 17 extracted public script/case files are byte-identical to the evidence branch.
Their full commit and SHA-256 values are in [reviewer-script-sha256.tsv](reviewer-script-sha256.tsv).
Retrieve them with `git fetch origin 573-review-evidence` and `git show FETCH_HEAD:<path>`.
Use `git archive` of the candidate and baseline, with pinned submodule archives under their paths.
Archive-local Git metadata and a private index support the scripts' Git queries and temporary restoration; no implementation checkout or shared index is used for mutation.
The unchanged integrity script proves candidate archive bytes, index and tree agree after every bank.

The runners are [run_public_evidence.py](run_public_evidence.py), [run_additional_evidence.py](run_additional_evidence.py),
[run_local_gates.py](run_local_gates.py) and [run_gate.py](run_gate.py).
The current mutation definitions are [author-mutation-cases.json](author-mutation-cases.json).

## Limits and next steps

The absent compiler mode intentionally stands down compiler-dependent instruments.
The builder's unavailable utilization-calibration report remains an explicit skip.
No hardware result is claimed. The scoped lint gate is separate from exhaustive simulation/synthesis qualification.
No hosted or local workflow replica is run for this unpushed head.
The maintainer owns publication, exact-head workflow evidence and candidate-merge validation.
The two independent reviewers must re-cover all five lenses, including RTL because `be32` changed.
No review verdict or reviewer-owned completion ledger is supplied by the author.
The replacement body is [PR-BODY.md](PR-BODY.md); it is prepared but not applied to the PR.
After posting the prepared `[A355] REVIEW READY` comment on issue #573, this author session stops.
'''
(out / 'HANDOFF.md').write_text(text)
print(status, 'Handoff bytes:', len(text.encode()))
