# The rule table, read once for the defect of R783-3 F1 = R784-3 F-1

96 mutants. 58 wrap a rule's output, each with a twin; 60 of 61 twins fail the mutant's own assertion, 1 another, 0 survive.

A row with no reading note: name read beside the mutant and what it fires, and they agree.

| Mutant | Replaces | Kind | Fires | Deletions to escape | Twin at the source | Reading |
|---|---|---|---:|---:|---|---|
| bound: a stale T_svc of 10 ms | `hooks.T_SVC_MS` | constant | L100 | 2 | - |  |
| bound: SRP graded against T_svc alone | `hooks.bound_ms` | stands in | L109 | 1 | - |  |
| bound: the ceiling alone | `hooks.bound_ms` | stands in | L102 | 1 | - |  |
| bound: the normative wait is not added | `run.hook_row` | wraps HOOK_ROW | L119 | 2 | same assertion |  |
| bound: the margin is taken from a timeout of zero | `hooks.normative_ms` | stands in | L123 | 1 | same assertion | RENAMED from `the margin is not recorded`: a margin is recorded, of -160, from a timeout of zero. |
| map: the counter push is a notification | `hooks.COUNTERS_PREFIX` | constant | L130 | 2 | - |  |
| map: no composed row of this harness is loaded | `run.LOADED` | constant | L132 | 1 | - |  |
| label: the Milan clock labelled the product's (the earlier rule) | `run.clock_label` | stands in | L144 | 1 | - |  |
| label: the Milan clock the default (the earlier rule) | `hooks_build.CPU_CLOCKS` | constant | L140 | 3 | - |  |
| split: the counter change is no pad | `hooks.parsed` | wraps ORIGINAL_PARSE | L175 | 1 | same assertion |  |
| H-ADP: the grandmaster is not checked | `hooks.gm_steps` | stands in | L192 | 1 | - |  |
| H-DISC: the sink's PROBE_TX_COMMAND is never recognised | `frames.ACMP` | constant | L211 | 1 | - |  |
| H-DISC: the window never ends (the earlier rule ended it at the next tagged record) | `hooks.next_adp_record` | stands in | L215 | 2 | - |  |
| H-DISC: a window shorter than the sink's TMR_DELAY decides (the earlier rule) | `hooks.disc_decided_ms` | stands in | L217 | 1 | - |  |
| H-ACMP: no response is matched to its command | `grade.response_sequence` | stands in | L236 | 2 | - |  |
| H-AECP: no face commit is recognised | `hooks.face_commit_words` | stands in | L258 | 1 | - |  |
| H-NOTIFY: the notification is not found | `Grader.recipients` | stands in | L273 | 2 | - |  |
| H-COUNTERS: spacing of 0.1 s accepted | `hooks.COUNTERS_SPACING_MS` | constant | L292 | 1 | - |  |
| H-COUNTERS: the held push from its change | `hooks.COUNTERS_SPACING_MS` | constant | L305 | 2 | same assertion |  |
| H-MAAP: no allocation report is recognised | `hooks.MAAP_REPORT_START` | constant | L318 | 2 | - |  |
| H-MAAP: every AAF_CTRL store is a report (earlier rule) | `hooks.MAAP_REPORT_START` | constant | L318 | 1 | - |  |
| H-SRP: the ADOPTED bit is never seen set | `hooks.adopted` | stands in | L333 | 1 | - |  |
| plants: a plant edits nothing | `hooks_build.plant_text` | stands in | L157 | 1 | - |  |
| supersede: the table names another group | `hooks.SUPERSEDED` | constant | L595 | 1 | - |  |
| supersede: the table names a second path | `hooks.SUPERSEDED` | constant | L600 | 1 | - | NEW. The old `another path` case stopped at the table lookup, so no row comparison ran; it now has a row of its own path and only the table stops it, and this mutant holds that. |
| supersede: a row of another path supersedes a refusal | `run.hook_row` | wraps HOOK_ROW | L604 | 1 | same assertion | NEW, the finding's fix. Goes through the rule at `run.py:141` as written: its path comparison compares nothing. |
| supersede: every refusal is superseded | `run.grade_all` | wraps GRADE_ALL | L597 | 3 | same assertion | RENAMED from `any later group supersedes a refusal`, which it did not vary: it clears every refusal, with no regard to any row, so all three refusal cases hold it and it escapes only with all three deleted. |
| aging: the window opens before the arm (the earlier rule) | `hooks.aging_group` | wraps AGING_GROUP | L624 | 1 | same assertion |  |
| aging: the sink still waits for its PROBE_TX_RESPONSE (the earlier rule) | `scenario.probe_answer` | stands in | L614 | 2 | - |  |
| aging: both sinks bound before either is answered (the earlier rule) | `hooks.aging_group` | stands in | L618 | 1 | - |  |
| buckets: the window opens right after the registrations (the earlier rule) | `hooks.refilled_ms` | stands in | L630 | 1 | another assertion, L638 | Agrees, and disclosed: the wait goes to 0, so the groups do open right after the registrations, and it fires the wait's length, the half of the rule that mutant reaches. The group's own assertion compares against the same value, so no mutant fires it; the twin, which removes the wait, fails that assertion. The rule is held. |
| findings: a path over its bound is not a finding | `run.hook_row` | wraps HOOK_ROW | L342 | 1 | same assertion |  |
| narrow: the layout swing is not applied | `hooks.LAYOUT_SWING_CYCLES` | constant | L349 | 3 | - |  |
| narrow: the slack counted at the 50 MHz CPU (the earlier clock) | `run.slack_cycles` | wraps SLACK | L356 | 2 | same assertion |  |
| plant: any finding of the hook catches it (the earlier rule) | `run.plant_findings` | stands in | L432 | 2 | - |  |
| plant: any finding of its kind catches it | `run.plant_findings` | stands in | L432 | 2 | - |  |
| plant: a path that only starts with its own catches it | `run.plant_findings` | stands in | L432 | 2 | - |  |
| plant: a late plant names no path | `hooks.plants` | stands in | L425 | 4 | - |  |
| plant: every run is caught | `run.plant_findings` | stands in | L432 | 2 | - |  |
| plant: an escape exits 0 | `run.main` | wraps MAIN | L432 | 1 | same assertion |  |
| held: W added to its bound | `run.held_row` | wraps HELD_ROW | L448 | 2 | same assertion |  |
| held: the exact bound misses | `run.held_row` | wraps HELD_ROW | L449 | 1 | same assertion |  |
| held: the verdict is relaxed by 1 ms | `run.held_row` | wraps HELD_ROW | L450 | 1 | same assertion |  |
| held: its row reports no time | `run.held_row` | wraps HELD_ROW | L451 | 1 | same assertion |  |
| held: its row reports a millisecond more | `run.held_row` | wraps HELD_ROW | L451 | 1 | same assertion |  |
| held: W is not recorded | `run.held_row` | wraps HELD_ROW | L452 | 1 | same assertion |  |
| held: its cycles round down | `run.held_row` | wraps HELD_ROW | L454 | 1 | same assertion |  |
| held: its cycles are the bus's | `run.held_row` | wraps HELD_ROW | L454 | 1 | same assertion |  |
| held: its margin omits W | `run.held_row` | wraps HELD_ROW | L456 | 2 | same assertion |  |
| held: its margin is rounded to the millisecond | `run.held_row` | wraps HELD_ROW | L457 | 1 | same assertion |  |
| held: its timeout is the notification family's | `run.held_row` | wraps HELD_ROW | L455 | 1 | same assertion |  |
| held: it counts as under the composed load | `run.held_row` | wraps HELD_ROW | L460 | 1 | same assertion |  |
| held: it counts as never served | `run.held_row` | wraps HELD_ROW | L460 | 1 | same assertion |  |
| held: it is H-NOTIFY's | `run.held_row` | wraps HELD_ROW | L459 | 1 | same assertion |  |
| held: it names another probe | `run.held_row` | wraps HELD_ROW | L459 | 1 | same assertion |  |
| held missing: silently accepted | `run.held_row` | wraps HELD_ROW | L474 | 2 | same assertion |  |
| held missing: it fits | `run.held_row` | wraps HELD_ROW | L477 | 1 | same assertion |  |
| held missing: it counts as served | `run.held_row` | wraps HELD_ROW | L477 | 1 | same assertion |  |
| held missing: its finding by name is dropped | `run.held_row` | wraps HELD_ROW | L474 | 2 | same assertion | RENAMED from `its finding is dropped`: the generic `LATE ... never served` finding stays; only the finding by name goes. |
| held missing: its timeout is the notification family's | `run.held_row` | wraps HELD_ROW | L478 | 1 | same assertion |  |
| held missing: it records CPU cycles | `run.held_row` | wraps HELD_ROW | L479 | 1 | same assertion |  |
| held missing: it records a W | `run.held_row` | wraps HELD_ROW | L479 | 1 | same assertion |  |
| held missing: it records a margin | `run.held_row` | wraps HELD_ROW | L479 | 1 | same assertion |  |
| held missing: it is another group's | `run.held_row` | wraps HELD_ROW | L482 | 1 | same assertion |  |
| held missing: it is another path's | `run.held_row` | wraps HELD_ROW | L482 | 1 | same assertion |  |
| held missing: it is another interface's | `run.held_row` | wraps HELD_ROW | L482 | 1 | same assertion |  |
| held missing: it is another family's | `run.held_row` | wraps HELD_ROW | L482 | 1 | same assertion |  |
| summary: the fastest path is the worst | `run.summary` | wraps SUMMARY | L506 | 1 | same assertion |  |
| summary: W is left in the service | `run.summary` | wraps SUMMARY | L506 | 1 | same assertion |  |
| summary: a path never served is not worst first | `run.summary` | wraps SUMMARY | L507 | 1 | same assertion |  |
| summary: alone and under load are not apart | `run.summary` | wraps SUMMARY | L506 | 2 | same assertion |  |
| summary: alone and under load are swapped | `run.summary` | wraps SUMMARY | L506 | 2 | same assertion |  |
| summary: another hook's paths are its own | `run.summary` | wraps SUMMARY | L506 | 5 | same assertion |  |
| summary: a miss counts as a narrow fit | `run.summary` | wraps SUMMARY | L512 | 1 | same assertion |  |
| summary: no narrow fit is counted | `run.summary` | wraps SUMMARY | L512 | 1 | same assertion |  |
| summary: a fit by the swing itself is narrow | `run.summary` | wraps SUMMARY | L512 | 1 | same assertion |  |
| summary: a fit one cycle under the swing is not narrow | `run.summary` | wraps SUMMARY | L512 | 1 | same assertion |  |
| summary: no miss is counted | `run.summary` | wraps SUMMARY | L511 | 1 | same assertion |  |
| summary: the path count is every hook's | `run.summary` | wraps SUMMARY | L509 | 2 | same assertion |  |
| summary: the applied count is dropped | `run.summary` | wraps SUMMARY | L514 | 1 | same assertion |  |
| summary: the undecided count is dropped | `run.summary` | wraps SUMMARY | L514 | 1 | same assertion |  |
| summary: the ordering findings are dropped | `run.summary` | wraps SUMMARY | L514 | 1 | same assertion |  |
| summary: the obligation is dropped | `run.summary` | wraps SUMMARY | L517 | 1 | same assertion |  |
| summary: the clauses are dropped | `run.summary` | wraps SUMMARY | L517 | 1 | same assertion |  |
| ALL: the push ends at its first descriptor | `hooks.counters_groups` | wraps COUNTERS_GROUPS | L527 | 3 | same assertion |  |
| ALL: no descriptor has a row | `hooks.counters_groups` | wraps COUNTERS_GROUPS | L528 | 3 | same assertion |  |
| ALL: a descriptor's row ends at the whole push | `hooks.counters_groups` | wraps COUNTERS_GROUPS | L532 | 3 | same assertion |  |
| ALL: a descriptor's row opens after the change | `hooks.counters_groups` | wraps COUNTERS_GROUPS | L535 | 2 | same assertion |  |
| amended: SRP keeps its ceiling | `hooks.AMENDED_SRP_MS` | constant | L552 | 3 | - |  |
| amended: the ceiling at two interfaces is 20 ms | `hooks.AMENDED_QUEUED_CEILING_MS` | constant | L552 | 4 | - |  |
| amended: every counter push is queued | `hooks.QUEUED_PATH` | constant | L567 | 3 | - |  |
| amended: W is left off | `hooks.amended_ms` | stands in | L564 | 1 | - |  |
| amended: the column grades a path | `run.hook_row` | wraps HOOK_ROW | L572 | 2 | same assertion |  |
| amended: a finding reads the column | `run.grade_all` | wraps GRADE_ALL | L575 | 1 | same assertion |  |
| amended: the table does not say which bounds graded | `run.BOUNDS_NOTE` | constant | L578 | 1 | - |  |
| amended: the column repeats the bound | `hooks.amended_ms` | stands in | L563 | 4 | - |  |
