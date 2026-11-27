import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
from verify import PACKET, RECEIPTS, RAW, HEAD, PREVIOUS, BASE, run, receipt

def load(name):
    data = json.loads((RECEIPTS / name).read_text())
    assert data['head'] == HEAD and data.get('failures', 0) == 0
    return data

docs = load('docs.json')
units = load('units.json')
objects = load('objects.json')
differential = load('differential.json')
wording = load('wording.json')
integrity = load('integrity.json')
assert len(units['builds']) == 6
assert objects['identical'] == 260 and differential['identical'] == 800
assert wording['exact_replacements'] == 8 and integrity['worktree_clean']
tree = run(['git', 'rev-parse', 'HEAD^{tree}']).decode().strip()

receipt('cleanup.json', dict(explicit_cleanup_commands=0, scratch_retained=True,
    possible_build_output_removals_prelogged=6,
    logging='Before each build, its possible shared-library relink cleanup path was appended to the required external cleanup log as a literal absolute path.',
    mutation_scratch_removals=0, failures=0))

status = f'REVIEW READY {HEAD}'
handoff = f'''{status}

<!-- SPDX-License-Identifier: Apache-2.0 -->

Author A861, PR #22, branch `opt-exec-3`, round 3.
Commit: `{HEAD}`. Tree: `{tree}`.
Parent and remote branch: `{PREVIOUS}`. Source base: `{BASE}`.

The local commit is `Clarify option work and callback buffer length contracts`.
It has one subject line, no body and no trailers.
Nothing was pushed or posted.

| Requested item | Applied change | Evidence |
| --- | --- | --- |
| R959-2-R1 | Exact restore comment at src/core/mrp_mad.c:1225, including its issue reference | [Wording receipt](receipts/wording.json) |
| R959-2-R2 | Exact length qualifications in both callback contracts and both integrator sentences | [Wording receipt](receipts/wording.json) |
| R960-2-R1 | Exact lookup, tick and send reason sentences; existing requirement and issue references retained | [Wording receipt](receipts/wording.json) |
| R959-2-F1 | The manager already corrected the prior evidence index, as stated in the task | No source change required |

Four files changed, with nine added and nine removed lines.
All eight requested replacements are verified.
The three source files are identical outside comments; the fourth file is the integrator guide.
Line counts and all 45 source-anchor targets are unchanged.
Length wording agrees with the existing short-buffer checks in all three application codecs.
The reason sentences agree with the bucket, wheel-slot and transmit-event loops.

| Fresh verification at this head | Result |
| --- | --- |
| Documentation | 1,289 sentence fragments; zero over limit; zero unlinked references; 79 self-tests; 438 local links; 26 external URLs; 29 rendered graphs; zero failures |
| Default units, profiles OFF / ON | 112 tests; 27,348 / 27,336 assertions; direct and registered runs exit zero |
| End-station units with scale, profiles OFF / ON | 114 tests; 27,376 / 27,364 assertions; direct and registered runs exit zero |
| End-station units without scale, profiles OFF / ON | 112 tests; 27,348 / 27,336 assertions; direct and registered runs exit zero |
| Options-off differential, both profiles | Two drivers, seeds 1 through 200; 800 of 800 trace comparisons identical; zero exclusions and problems |
| Default objects against source base | All ten source files; two host compilers; thirteen flag sets; 260 of 260 pairs identical |
| Source inventory and added-line scan | 74 tracked text files; zero generated files; clean worktree; zero matches in both comparison ranges |

The object total contains 200 pairs built without debug information and 60 pairs compared after removing debug sections.
Flag sets cover optimization levels zero, one, two, three and size; profile variants and position-independent output are included.
The differential explicitly defines all nine optimization switches as zero.
Its wrapper selects only the existing default configuration, preserving both drivers, seed counts, steps and comparison logic.
No mutation or sanitizer campaign was selected for this wording-only round.

[The receipt index](receipts/INDEX.md) binds the delivered files by their actual content hashes.
It excludes itself to avoid a circular hash.
Raw outputs, reproduction scripts and the fetched review texts are retained alongside the receipts.
Scan pattern categories are described in words; receipts do not reproduce execution-product names.

The [PR body draft](PR-BODY.md) updates the fetched current body and separates fresh evidence from the previous head's campaigns.
The [review-ready note](REVIEW-READY.md) identifies the exact local head for the next review.

No explicit cleanup command was issued.
Possible shared-library relink output removals were logged before each build in the required cleanup log, using literal absolute paths.
Generated builds and graph outputs remain outside the checkout; none was committed.

Manager duties remain: publish only when authorized, obtain the next reviews, and exclude the historical bytecode blob when merging.
Current-parent integration banks, hosted acceptance, target linking, timing and physical hardware acceptance remain separate manager work.
No fresh claim is made for prior mutation, sanitizer, scenario, equivalence or target campaigns.

{status}
'''
(PACKET / 'HANDOFF-r3.md').write_text(handoff)

ready = f'''{status}

<!-- SPDX-License-Identifier: Apache-2.0 -->

PR #22 has one local wording-only follow-up commit: `{HEAD}`.
The remote branch remains at `{PREVIOUS}`.
Nothing was pushed or posted.

The exact requested residue fixes are applied in four files.
Callback contracts now admit buffer length; reason comments describe the work actually avoided.
No executable source changed, and all 45 source anchors retain their targets.

Fresh checks pass: documentation, six unit builds, 800 options-off differential comparisons, and 260 default-object comparisons against `{BASE}`.
The object total includes 200 non-debug pairs and 60 pairs after debug-section removal.
Both protocol profiles passed every unit and differential configuration selected for this round.

The checkout is clean, with 74 tracked text files and no generated artifacts.
The commit contains a single subject without a body or trailers.
The prior evidence-index defect was already corrected by the manager, per the task.

Review [the source delta](raw/source-delta.patch), [handoff](HANDOFF-r3.md), [draft PR body](PR-BODY.md), and [hashed evidence](receipts/INDEX.md).
Historical campaigns remain attributed to their earlier head; hardware and parent integration are not newly claimed.

{status}
'''
(PACKET / 'REVIEW-READY.md').write_text(ready)

before = (PACKET / 'inputs/pr-body-before.md').read_text()
assert 'Head: `opt-exec-3` (`50a2106`)' in before
body = before.replace('Head: `opt-exec-3` (`50a2106`)', 'Head: `opt-exec-3` (`16b6c95`)', 1)
body = body.replace('then the fixes for the two reviews at `73007b48`.',
                    'then the fixes for the two reviews at `73007b48`, and the wording follow-up at `16b6c95`.', 1)
old = "With every option at 0, every library object is byte-identical to `main`'s without debug information, at -O0, -O2 and\n-Os; with it, only the debug sections differ, as source lines moved."
new = "With every option at 0, all ten source objects match `main`'s in the recorded two-compiler, thirteen-flag-set matrix.\nThe 200 non-debug pairs match byte for byte; all 60 debug pairs match after debug sections are stripped."
assert old in body
body = body.replace(old, new, 1)
new_section = f'''## Wording follow-up at `16b6c95`

The follow-up changes comments and the integrator guide only.
The restore comment uses the exact reviewed wording and names the governing issue.
Both callback contracts now include buffer length among the inputs that determine the result.
The lookup, tick and send reason sentences describe the avoided work without implying constant work.
No executable source changed, and all 45 source anchors retain their previous targets.
The prior evidence-index correction was handled separately by the manager.

The local head is `{HEAD}`. These checks ran at that head; every exit code was zero.
This draft has not been posted, and the local commit has not been pushed.

| Fresh gate | Scope | Result |
| --- | --- | --- |
| Documentation | Sentence/reference checks, reference self-tests, authenticated links, graph rendering | Zero over-limit sentences or unlinked references; 79 self-tests; 438 local links; 26 external URLs; 29 graphs; zero failures |
| Default units | Both profiles, every optimization switch explicitly zero | 112 tests; 27,348 / 27,336 assertions; direct and registered runs pass |
| End-station units with scale | Both profiles, all five end-station switches enabled | 114 tests; 27,376 / 27,364 assertions; direct and registered runs pass |
| End-station units without scale | Both profiles, all five end-station switches enabled | 112 tests; 27,348 / 27,336 assertions; direct and registered runs pass |
| Options-off differential | Both existing drivers, both profiles, 200 seeds each | 800 of 800 traces identical; zero excluded seeds; zero problems |
| Default objects | All ten source files, two host compilers, thirteen flag sets | 260 of 260 pairs identical: 200 without debug information and 60 after stripping debug sections |
| Source integrity | Four changed files; source compared outside comments; tracked-file and added-line checks | Zero executable changes; 74 tracked text files; zero generated files; clean checkout |

Object flags cover -O0, -O1, -O2, -O3 and -Os; Milan variants at -O0/-O2/-Os; -fPIC at -O0/-O2; and -g at -O0/-O2/-Os.
The host compilers were GCC 16.2.1 and Clang 23.1.5, targeting x86-64.
Every optimization switch was explicitly zero for both revisions.
The differential wrapper selects the existing default configuration only and defines all nine optimization switches as zero.
It preserves the drivers, 200 seeds, 20,000 timer steps and 3,000 MAD steps per seed, and full trace comparison.
No mutation or sanitizer campaign was rerun for this wording-only follow-up.

## Earlier evidence (head `50a2106`)

The campaigns below belong to the previous head and were not all repeated for the wording follow-up.
'''
assert '## Evidence (head `50a2106`)' in body
body = body.replace('## Evidence (head `50a2106`)', new_section, 1)
(PACKET / 'PR-BODY.md').write_text(body)

categories = 'review and author identifiers; lane and round labels; private absolute paths and infrastructure markers; assistant, model and execution-product names'
index = f'''# Receipt index

Status: REVIEW READY `{HEAD}`.
Source base: `{BASE}`. Previous head: `{PREVIOUS}`.

All requested fresh gates passed at this head.
Six unit configurations passed; 800 differential comparisons and 260 object comparisons were identical.
Of the object pairs, 200 were non-debug and 60 had debug sections removed before comparison.
All eight exact wording replacements and 45 unchanged source anchors were verified.

The added-line scans covered 2,940 lines against the source base and nine lines against the previous head.
Their pattern categories were {categories}.
Every category returned zero matches.
The generated-file scan covered compiled outputs, binary archives, execution logs, bytecode caches and build directories.
It found zero tracked generated files; all 74 tracked files were text.
Commit checks found one new subject line, zero bodies and zero trailers.

The primary results are docs.json, units.json, differential.json, objects.json, wording.json, integrity.json and cleanup.json.
Supporting files include the fetched reviews, prior PR body, raw outputs, source patch and reproduction scripts.
The raw output hashes in the primary receipts bind the corresponding supporting logs.
Paths below are relative to the packet root.
Each hash was computed from the delivered file bytes after all content was finalized.
This index excludes itself to avoid a circular hash; it is an integrity record, not a signed attestation.

| File | SHA-256 |
| --- | --- |
'''
index_path = RECEIPTS / 'INDEX.md'
files = sorted(path for path in PACKET.rglob('*') if path.is_file() and path != index_path)
for path in files:
    index += f'| {path.relative_to(PACKET).as_posix()} | {hashlib.sha256(path.read_bytes()).hexdigest()} |\n'
index_path.write_text(index)

# Read the delivered index afresh and verify the listed bytes independently.
entries = re.findall(r'^\| ([^|]+) \| ([0-9a-f]{64}) \|$', index_path.read_text(), re.M)
assert len(entries) == len(files)
for name, wanted in entries:
    assert hashlib.sha256((PACKET / name).read_bytes()).hexdigest() == wanted, name
assert not run(['git', 'status', '--porcelain', '--untracked-files=all', '--ignored']).strip()
print(f'Packet finalized: {len(entries)} indexed files, all hashes verified; clean checkout; {HEAD}')
