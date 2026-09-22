[A159] MUTATION DEFINITIONS AND CONTROLS

Mutations execute only scratch copies of `scripts/ci_events.py` with explicit `--root` pointing to copied workflow/policy inputs. No gate-input mutation ever touches tracked source. The before population is the required starting head. The after source is the committed revision. Complete source variants, generated patches, exact argv/result JSON and stdout/stderr logs are under `before/` and `after/`.

Each source mutation targets only `check_carrier_script`; specialized comparators remain intact. The initial instrument guard found multiple matching comparator strings in the entire module and refused before execution; the instrument was narrowed to this named function. Assertions require exactly one matching comparison and one record item within it.

| Mutant | Definition |
|---|---|
| real | Unchanged checker, positive control. |
| M5b | Require equal line counts; strip trailing ` || true` from each non-last actual/expected line before comparison; compare last line exactly. This is R220's published comparator semantics. |
| prefix-only | Compare the actual prefix of canonical length with the canonical tuple. Extra actual lines become acceptable. |
| order-insensitive | Compare sorted actual/canonical line lists. |
| removed-comparator | Replace only the canonical equality item's predicate with True; record enforcement remains. |
| removed-record-enforcement | Replace only the record-validity item's predicate with True; retain missing-record early return and real comparison. |

Every mutant still passes pristine `--check`. Their detection comes from the full self-test, not a deliberately broken pristine fixture.

| Variant | Before check exit | Before complete self-test | After check exit | After complete self-test |
|---|---|---|---|---|
| real | 0 | selftest: PASS (1505 contract items, 931 arms) | 0 | selftest: PASS (1505 contract items, 1144 arms) |
| M5b | 0 | selftest: PASS (1505 contract items, 931 arms) | 0 | selftest: 117 FAILURE(S) |
| prefix-only | 0 | selftest: PASS (1505 contract items, 931 arms) | 0 | selftest: 56 FAILURE(S) |
| order-insensitive | 0 | selftest: PASS (1505 contract items, 931 arms) | 0 | selftest: 40 FAILURE(S) |
| removed-comparator | 0 | selftest: 187 FAILURE(S) | 0 | selftest: 400 FAILURE(S) |
| removed-record-enforcement | 0 | selftest: 56 FAILURE(S) | 0 | selftest: 56 FAILURE(S) |

M5b accepts the exact AC5 first-line mutation at both source versions, as intended for this defective comparator. The real checker rejects it at both. The regression is that the revised self-test now catches the defective comparator, including this exact call:

```text
carrier-script-407 docs-check step 34 or-true-line-1
job `docs-check` step 34 (`Python idiom gate`) script is not the canonical form: line 1 must be 'python3 scripts/check_py_idiom.py'
```

Population and reason controls:

- 117 new non-last swallowing arms, 56 append controls, 40 reorder controls; each of 213 new arms must find its exact job/step/line reason. Details: `controls/new-arm-reasons.json`.
- Every one of 173 normalized carrier lines has a swallowing arm. All 14 live `--check` lines are listed separately in `controls/check-call-inventory.json`, including bounded ratchets at steps 26/28/30/31.
- 833 pre-existing mutation labels, reasons and actual edited worlds match exactly. All 590 specialized arms still refuse their intended reason with the carrier helper disabled.
- The existing stub-vacuity stage misses all 1,046 workflow mutation arms. The full 1,144 total also contains positive and fixture/control stages; vacuity is not claimed for all 1,144.
- Retained missing-record and matching-record stage: 57 arms. Retained whitespace positive: one arm reformats every carrier body plus the existing specialized scripts.
- Maintenance scratch edit appends `echo maintenance` after Python idiom's self-test. Workflow-only edit refuses line 3. Adding that exact line to its static record passes actual `--check` and full `--selftest`; the latter grows automatically to 1,145 arms. No manual mutation entry changes.
- Production AST functions change only `_carrier_script_edits` and `_carrier_script_arms`; canonical tables match the starting head. No production relaxation or normalization change is part of the revision.

`archive-probes/` contains the public R220 instruments read from immutable archive 1833a21210b40d64f2c1275ff476168b4a62b0c0, not private transcripts. Our `probe_mutants.py` executes the corresponding real source mutants through the actual CLI. `probe_controls.py` supplies preservation, reason and maintenance measurements. These instruments are evidence outside tracked source, not installed workflow flags.
