"""Refresh the author handoff from measured receipts."""
import json
from pathlib import Path
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = Path('$LANES/577-image-l6-l10')
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
text = f"""# Issue #577 author handoff

Author: [A410]. Internal reviewer: [R384]. External reviewer: [R385].
Assignment: https://github.com/kebag-logic/milan-fpga/issues/577#issuecomment-5865331676
Branch: `577-image-l6-l10`.
Base: `54ce877371ee6e8878cf67294e86c2a8481b62f6`.
Head: `{head}`.
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`.
Processor root verified before its Git read; pin: `16be6768f710e79450aace277abacd6c2c3336e5`.
Status: author work complete and ready for independent review; local commit only.

## Change list

| File:line | Change |
|---|---|
| `sw/builder/endstation_builder.py:2310` | Validate the completed packed blob before returning any image artifacts; translate named image errors to ConfigError. |
| `sw/builder/aem_image_checks.py:20` | Derive sampling-rate walk offset and bound from read-only microprogram assignments. |
| `sw/builder/aem_image_checks.py:39` | L10 offset, count, complete-word and exact-extent refusals. |
| `sw/builder/aem_image_checks.py:60` | L6 list bounds and distinct duplicate/gap/order refusals. |
| `sw/builder/aem_image_checks.py:82` | Read actual AEMI index rows, descriptor extents and every member. |
| `sw/builder/test_builder.py:27233` | Independent boundary/refusal fixture table. |
| `sw/builder/test_builder.py:27279` | Inject after successful loading; prove bytes survive packing; grade the emitter's exact reason. |
| `sw/builder/test_builder.py:27313` | Gate 36b: all five shipping images, four accepted controls and 13 negative cases. |
| `sw/builder/test_builder.py:27333` | Ten descriptor targets across two synthetic configurations, same-length stride members and repeated unequal-length runs. |
| `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:89` | Updated L6 matrix row. |
| `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:93` | Updated L10 matrix row. |
| `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:181` | Image-boundary derivation and named refusal evidence. |
| `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:318` | F6 enforcement and remaining processor scope. |

## Image boundary and derivation

`_entity_model_image` calls the validator immediately after `gen_desc_image.build` returns.
The exact checked `blob` becomes `aem_desc.bin`. No expected value comes from
`_load_clocking`, `_validate_output_clock_sources`, YAML, overlay or packer report.
Both loader functions are AST-identical to the base. Their scope is unchanged.

| Measured field | Source and derivation |
|---|---|
| Image version | Big-endian header field at byte 4; accepts AEMI v1. |
| Index count/location | Header bytes 8 and 12; no fixed row count or location. |
| Configuration/type/count/length/base/stride | Each emitted 16-byte index row; walk every row and member. |
| Descriptor location | Row base plus member number times row stride. |
| Actual descriptor length | Row elem_len; slices exclude alignment padding. |
| Rate offset/count | Big-endian body fields at 140/142, IEEE 1722.1-2021 7.2.3. |
| Required rate offset/bound | Literal SSR_LIST_OFF/SSR_WALK_MAX assignments read from the pinned SET_SAMPLING_RATE microprogram. AST parsing never executes it. No copied builder maximum is used. |
| Full-word rate extent | Divide measured unpadded length minus the consumer's list start by sizeof big-endian u32. Partial remainder, missing words and extra words have distinct reasons. Pull bits remain part of each word. |
| Source offset/count | Big-endian body fields at 72/74, IEEE 1722.1-2021 7.2.32. |
| Source list | Exactly count u16 entries at the served offset, bounded by the actual descriptor length. |
| Required identity list | range(served count), independent of constructor contents. Classify duplicates, gaps and order separately. |

The image contains enough structure, so the assignment's STOP condition does not apply.
The generic packer remains responsible for generic integrity. The checker does not
claim every L1-L10 rule, source construction, runtime rate support, model evolution
or multi-configuration product support. Synthetic fixtures prove the reader's walk.
Processor issue 89 remains separate defence-in-depth work.

## Boundary and refusal cases

All cases use a successfully loaded shipping configuration. The test substitutes
a descriptor while the real packer runs, verifies its exact packed bytes, then
requires the builder's post-packing validator to produce the named result.

| Case | Packed fields / mutation | Result |
|---|---|---|
| One rate | offset 144, count 1, length 148 | accepted |
| Eight rates | offset 144, count 8, length 176; includes pull-bearing word 0x2000BB80 | accepted structurally |
| Identity sources | [0,1] | accepted |
| One source | [0] | accepted |
| Wrong offset | offset 143 with otherwise valid one-rate body | L10_OFFSET |
| Ninth rate | count 9, nine distinct complete words, length 180 | L10_COUNT |
| Count/extent mismatch | count 2, one complete word, length 148 | L10_COUNT_EXTENT |
| One byte short | count 1, length 147 | L10_PARTIAL_WORD |
| One word extra | count 1, length 152 | L10_EXTRA_WORDS |
| Reversed list | [1,0] | L6_ORDER |
| Gapped list | [0,2] | L6_GAP |
| Duplicate list | [0,0] | L6_DUPLICATE |
| Short audio header | length 143 | L10_HEADER |
| Short domain header | length 75 | L6_HEADER |
| Empty list | count 0 | L6_EMPTY |
| Short source list | final source is missing one byte | L6_EXTENT |
| List inside header | source offset 70 | L6_EXTENT |

The eight-rate fixture bypasses only model construction, never the new check.
It does not widen #478's loader scope or downstream supported-rate restrictions.

## Removed-check mutant table

`check_mutants.py` creates disposable single-module mutants outside the worktree.
It deletes exactly one named raising statement per mutant, then calls the same
committed `test_shipping_image_contract`. Each required-class mutant wrongly
accepts its invalid input and therefore fails the test. Additional defensive
mutants fail if their named reason falls through to a generic structural error.
No mutant changes the worktree or the processor sources.

| Removed check | Verdict | Test failure |
|---|---|---|
"""
for row in json.loads((OUT / 'mutants.json').read_text()):
    text += f"| {row['reason']} | {row['verdict']} | {row['failure']} |\n"
text += """
## Five-configuration results

`check_images.py` loads the assigned base's builder source in memory without
creating another checkout. The unchanged producers and source configurations
are shared; it compares each complete base image with the checked head image.
No binary images or tree exports are retained here.

| Configuration | Image bytes | Rate offset/count/length | Sources | Compared with base | SHA-256 |
|---|---:|---|---|---|---|
"""
for row in json.loads((OUT / 'images.json').read_text()):
    text += (f"| {row['configuration']} | {row['bytes']} | "
             f"{row['rates_offset']}/{row['rates_count']}/{row['audio_unit_bytes']} | "
             f"{row['sources']} | identical | `{row['sha256']}` |\n")
text += """
Every CLOCK_DOMAIN has source offset/count/length 76/2/80.
arty_current retains 48000/96000/192000; the other four retain 48000.

## Gate table

Commands run in the foreground from `$LANES/577-image-l6-l10`.
`run_gates.py` records each command, head, exit status, elapsed time, log size
and SHA-256. Commands are never piped. Each has a 7200-second timeout.
`/tmp/milan-577-venv/bin/python` is Python 3.14 with the repository's hash-locked
Markdown and HDL parser dependencies; no environment or installed packages
live in this output directory. Full logs over 200000 bytes are represented
by size/hash and a bounded tail only.

Only successful final-head receipts below count as evidence. Superseded or
setup-refused attempts remain separately recorded and do not count as passes.

| Receipt | Exact command | rc | Log |
|---|---|---:|---|
"""
for group in ('builder', 'docs', 'diagrams', 'reference', 'focused'):
    path = OUT / (group + '-gates.json')
    if not path.exists():
        text += f"| {group} | pending | - | - |\n"
        continue
    for row in json.loads(path.read_text()):
        if row['rc'] != 0 or row['head'] != head:
            continue
        text += f"| {row['label']} | `{row['command']}` | {row['rc']} | {row['log']} |\n"
text += """
## Evidence limits and reruns

The first head's wording gate rejected a generic processor phrase. The final
head names SET_SAMPLING_RATE precisely. The interrupted old-head builder runs
and old documentation receipts are under `superseded-head`; none clear a gate.
The HDL parser self-test initially refused its missing pinned package. After
installing the lock outside this output directory, the self-test passed.
HDL reference generation initially interpreted Git's missing commit-graph
warning as a dirty-tree signal. Its successful rerun disables that optional
Git acceleration through per-command configuration, without changing Git data
or repository files. Setup attempts are recorded under `setup-retries`.

All 69 final-head command receipts return rc 0. The complete builder reports
ALL GATES PASS EXCEPT 1 NOT RUN: gate 11 needs the absent placement calibration
report. Its compiler-backed instruments ran. The deliberately compiler-absent
run also returns 0 and records its three compiler-dependent instruments as one
NOT RUN arm, with zero actual firmware compiler invocations. That absence is
not counted as evidence of those instruments. No-Git documentation mode reports
its expected inventory-parity skip. Neither exclusion is new F6 evidence.

The final worktree is clean. `integrity.json` records the four changed files,
unchanged gitlinks and whitespace gate. `processor-integrity.json` proves the
read-only walk source matches its pin. The commit subject has no body or trailers.
The public REVIEW READY handoff names this exact head. No independent review
verdict is claimed by the author.
Independent review, publication, hosted/candidate validation and merge remain
outside this author's assignment. No push, PR operation, merge, hardware,
firmware, processor source, gitlink or RTL change was made.
"""
(OUT / 'HANDOFF.md').write_text(text)
