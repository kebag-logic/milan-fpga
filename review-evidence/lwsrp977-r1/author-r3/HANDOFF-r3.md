REVIEW READY 16b6c950ca320d29876d84c33460c2652650f16d

<!-- SPDX-License-Identifier: Apache-2.0 -->

Author A861, PR #22, branch `opt-exec-3`, round 3.
Commit: `16b6c950ca320d29876d84c33460c2652650f16d`. Tree: `622309fdba8e09fdb334cf37f0e381e3a898b1bf`.
Parent and remote branch: `50a2106483141fcd7d1b20654bcf0803e7c3020a`. Source base: `d1bb4f4e5954af6dabe7f210a6bf7adbb76bdd6b`.

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

REVIEW READY 16b6c950ca320d29876d84c33460c2652650f16d
