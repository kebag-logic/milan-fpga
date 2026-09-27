"""Refresh the handoff from measured hashes, mutations, commits and gate receipts."""
import json
from pathlib import Path
import shlex
import subprocess

ROOT = Path('$LANES/573-builder-refusals')
OUT = Path(__file__).resolve().parent
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
commits = subprocess.check_output(['git', 'log', '--reverse', 'e0920d77..HEAD',
                                  '--format=%H %s'], cwd=ROOT, text=True).splitlines()
before = json.loads((OUT / 'before.json').read_text())
after = json.loads((OUT / 'after.json').read_text())
assert before == after
receipts = {p.name.removesuffix('.result.json'): json.loads(p.read_text())
            for p in OUT.glob('*.result.json')}
expected = ['builder-present', 'builder-absent', 'declarations', 'descriptor-audit',
            'store-self-test', 'rtl-lint', 'python-idiom', 'naming', 'docs-git',
            'docs-no-git', 'em-dash', 'doc-style', 'toc', 'toc-anchors',
            'doc-paths', 'diff-whitespace']
complete = all(name in receipts and receipts[name]['returncode'] == 0 for name in expected)
status = 'All requested local gates passed; ready for the assigned independent reviewers.' if complete else 'Implementation committed; remaining local gates are still in progress.'
text = f"""# [A347] Parent shipping-model refusals F1-F4

{status}

Head: `{head}`. Base: `e0920d77162284d8da52ffaf13a973e451e44f90`.
Branch: `573-builder-model-refusals`.
Physical worktree: `$LANES/573-builder-refusals`.
Origin confirmed: `https://github.com/kebag-logic/milan-fpga.git`.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/573#issuecomment-5853854503.
Executor: [A347]. Independent reviewers: [R340] and [R341].

All five tracked configurations remain accepted. No STOP condition occurred.
All 85 generated artifacts have identical before/after sizes and SHA-256 hashes.
No tracked configuration, submodule, hardware, or deployment changes were made.
No push, pull request mutation, merge, or other checkout was performed.

## Change list

- `sw/builder/endstation_builder.py:1341`: reserved model-ID refusal; literal and pin call sites at 4367/4371.
- `sw/builder/endstation_builder.py:1382`: per-listener integer buffer floor; called for every stream at 1501.
- `sw/builder/endstation_builder.py:1393`: final format count and family validation; AAF call at 1460 includes derived listener entries.
- `sw/builder/endstation_builder.py:1410`: exact Milan CRF word; both clocking inputs call it at 3869/3872.
- `sw/builder/endstation_builder.py:4214`: output INTERNAL availability; called before stream construction at 4226.
- `sw/builder/test_declarations.py:34`: model-ID controls and packed ENTITY/ADP equality; buffer tests at 68; AAF tests at 90; CRF tests at 118; source tests at 140.
- `sw/builder/test_declarations.py:207`: existing declaration entry executes all new tests; the full builder already calls this entry.
- `sw/builder/README-parameters.md:117`: user-visible clock, format and buffer rules; identity endpoints at 146.
- `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:239`: F1-F4 enforcement and evidence; L4/L6/L9 and reachable YAML probe rows updated consistently.

## Per-issue evidence

| Issue | Rule | Clause | Where enforced | Legal control | Refusals | Mutant result |
|---|---|---|---|---|---|---|
| #573 / F1 | Reserved model-ID endpoints | Milan v1.2 5.3.1; IEEE 1722.1-2021 6.2.2.8 and Table 7-2 | `_model_id`, literal/pin resolution | 1, max-minus-one and shipping ID on both forms; packed ENTITY and ADP boot constants agree | Zero and all ones on both forms | 4/4 killed: each endpoint guard, literal call, pin call |
| #574 / F2 | Every listener buffer at least 2126000 ns | Milan v1.2 5.3.3.4 | `_stream_buffer_ns`, every `_streams` row | 2126000 and 2126001 at all eight listener indices | 2125999, zero, negative, fraction, string and boolean at all eight indices | 1/1 killed: floor guard removed |
| #575 / F3 | At most 47 final formats; homogeneous declared family; exact CRF word | IEEE 1722.1-2021 Table 7-8; Milan 5.3.3.4, 6.4, 7.3.2 Table 7.1 | `_validate_stream_formats`, `_crf_format` | AAF controls and 47 final entries at every input/output index; both CRF directions accept 0x041060010000BB80 | 48 final/declared entries, mixed families in either order, wrong family/version, CRF word ending BB81 | 6/6 killed: count/family checks on inputs and outputs; exact CRF word checks in both directions |
| #576 / F4 | Any AAF/CRF output requires INTERNAL available | Milan v1.2 5.3.3.6 | `_validate_output_clock_sources` | INTERNAL+CRF with either selected; CRF-only input clock loading | AAF output without INTERNAL; AAF+CRF outputs without INTERNAL; isolated CRF-output obligation | 3/3 killed: complete guard, AAF arm, CRF arm |

Each invalid fixture requires `ConfigError` and its own field/rule text.
Production refusals are explicit exceptions, not assertions.
All numerical oracles in the new tests are independent specification boundaries.
Count controls repeat formats to isolate list cardinality; they do not claim new media modes.
The count bound applies after listener family completion, so 47 declared AAF entries
requiring one derived entry are refused as 48 final entries.

Input-only behavior is deliberately measured at the existing clock-loading boundary.
The complete product YAML loader still requires nonempty AAF directions.
The new output check imposes no INTERNAL requirement when there are no outputs.
Clock source selection may remain CRF when INTERNAL is available.

Only parent configuration validation changed. Generic processor packing remains unchanged.
Model evolution stays with #495. F5-F8 and other ownership-matrix debt remain separate.
`docs/spec-refs.md` was absent at the assigned base and in the processor documentation.
Clause references came from the ownership matrix, processor memory-map section 3.1,
integrator guide, and existing clause-backed builder/descriptor documentation.
No specification PDF or private transcript was read.

## Commits

"""
for line in commits:
    text += '- `' + line + '`\n'
text += """
## Gate table

Every command ran in the foreground from the physical worktree, without a pipeline.
`run_gate.py` applies a 7200-second deadline and records the actual exit status.
The Markdown gates use the already-installed pinned renderer environment.
An initial system-interpreter em-dash attempt lacked that dependency; its rerun passed.

| Gate | Exact command | Exit status | Seconds | Evidence |
|---|---|---|---|---|
"""
for name in expected:
    row = receipts.get(name)
    if row:
        text += f"| {name} | `{shlex.join(row['command'])}` | {row['returncode']} | {row['seconds']} | `{row.get('log', name + '.tail.log')}` |\n"
    else:
        text += f'| {name} | Pending | Pending | Pending | Pending |\n'
text += """
Compiler-absent mode runs the entire `test_builder.py` main entry via `runpy`.
`builder_absent.py` uses the existing compiler audit to hide only its three RV32
candidates. All other subprocesses execute normally; no host tool or SDK changes.
It verifies that all three candidates were hidden after the complete entry returns.
Compiler-present mode invokes the full entry directly with `--require-rv32`.

The filesystem-mode documentation gate records its expected Git-inventory parity skip.
Builder skip details, if any, are quoted below from the actual final verdicts.

"""
for name in ('builder-present', 'builder-absent'):
    row = receipts.get(name)
    if not row:
        continue
    log = Path(row['large_log']) if 'large_log' in row else OUT / row['log']
    content = log.read_text()
    marker = content.rfind('GATE ARM(S) DID NOT RUN')
    if marker >= 0:
        start = content.rfind('\n', 0, marker)
        text += f'### {name} recorded evidence limits\n\n```text\n' + content[start:].strip() + '\n```\n\n'
    else:
        text += f'{name}: ' + content.strip().splitlines()[-1] + '\n\n'
text += """## Removed-check evidence

`mutations.py` replaces one exact production guard per case, runs the existing
`test_declarations.py` entry, requires its discriminating assertion failure,
and restores the source in a `finally` block. No changed mutant source remains.
`mutations.json` contains the exact changes and required failure diagnostics.
The final campaign records the exact reviewed head in every result row.
Reproduce per issue: `python3 mutations.py 573` (then 574, 575, 576), from this bundle.

| Issue | Mutation | Result | Diagnostic |
|---|---|---|---|
"""
for issue in ('573', '574', '575', '576'):
    for row in json.loads((OUT / f'mutations-{issue}.json').read_text()):
        text += f"| #{issue} | {row['mutation']} | KILLED, rc {row['returncode']} | `{row['diagnostic']}` |\n"
text += """
## Five-configuration SHA-256 tables

`measure_artifacts.py` generated each tracked configuration into temporary scratch,
then called both generator CLIs on its overlay. Only hashes and sizes were retained.
The builder table includes the generated per-configuration shape and sweep text.
`before.json` was measured before the first source change; `after.json` after F1-F4.
`through-575.json` is an identical intermediate measurement.
No build tree, toolchain, package installation or generated artifact was stored here.

"""
for phase, rows in [('Before', before), ('After', after)]:
    text += f'### {phase}\n\n'
    for config in sorted({r['configuration'] for r in rows}):
        text += f'#### {config}\n\n| Artifact | Bytes | SHA-256 |\n|---|---|---|\n'
        for row in rows:
            if row['configuration'] == config:
                text += f"| `{row['artifact']}` | {row['bytes']} | `{row['sha256']}` |\n"
        text += '\n'
text += """## Delivery state

`PR-BODY.md` is prepared for the assigned publication role and starts with [A347].
It carries all four closing references on separate lines.
Independent review, push, pull request creation and merge are not performed here.
The final authorized action is the [A347] REVIEW READY comment on issue #573,
using the exact head above. All four project items are In review before that comment.
"""
(OUT / 'HANDOFF.md').write_text(text)
print(f'HANDOFF.md refreshed: {len(text.encode())} bytes; gates complete={complete}')
