[R273] NEGATIVE - exact head a13b6e2e461695cdb8d978444ae499a5a6745429

External independent review R273-1 of PR #535 (issues #408 and #409). Head
`a13b6e2e461695cdb8d978444ae499a5a6745429`, tree
`44729af1c6f9e164d8ca82eda5a47d3708b96a6d`, source base
`759da623072358afdb0e9d570a7b4b6a788492c9`. Cleared context; reconstructed
from AGENTS.md, CONTRIBUTING.md, docs/README.md, the two issue bodies, the
manager's scope comments on #408 and #409 (2026-09-21, "Remaining scope after
PR #498"), the assignment and takeover comments, the PR body, the diff and
history, and executable evidence produced in this round. Receipts are listed
in `MANIFEST.sha256`; the scripts that produced them are in `scripts/`.

## Verdict in one paragraph

The retirement is real and, where a merge is graded, it does not weaken
protection. With the pinned RV32 SDK every retired rule's hostile controls are
refused on the replacing instrument's own sentence; each control passes the
whole gate once its replacement is disconnected; every accepted case is RED at
dev on the retired rule's own sentence in both environments and GREEN at the
head in both; and six additional splice and paste bypasses of surviving text
rules written for this review are all refused by the resolver. Both hosted
builder consumers still pass `--require-rv32`, and compiler absence is a
registered NOT RUN that never counts as coverage. One MINOR stays open: the
head's statements of what a compiler-absent runner still refuses are wrong in
two measured places (the narrowed macro-body rule's stated reason, and the
list of what nothing refuses). Separately, and not attributable to this PR,
three pre-existing escapes were measured GREEN at dev and at the head with
the compiler; they are SUGGESTIONs for follow-up Issues.

## Findings

### R273-F1 - MINOR - Conformance, Robustness, Tests, Docs

**Artifact:** `docs/integration/BAREMETAL_FIRMWARE.md:1258` (narrowed
macro-body row) and `:1367-1379` ("What a runner with no RV32 compiler
gets"); `sw/builder/test_builder.py:2266-2280` (the narrowed rule's comment
and message), `:9461-9472` (registered NOT RUN text), `:13399-13404` (the
verdict's first clause), `:13590-13593` (COSTS print), `:10896-10915` (the
narrowing's two controls).

**Title:** the compiler-absent coverage statements overstate what the
surviving text rules refuse.

**Authority/evidence:** #408 acceptance 2 (each rule is retired, narrowed, or
kept "with its cost restated and a reason"); the 2026-09-21 scope comments on
#409 and #408 ("Compiler absence remains an explicit NOT RUN for the new
measurements, rather than a claim of coverage"); #408 acceptance 1 (the
closing line names the arm). Measured with `scripts/probe.py`; receipts
`receipts/20-probes/{base,head}-{sdk,absent}.{json,txt}`:

- (a) The narrowed macro-body rule is justified by "every rule that reads a
  read fails closed when the read is hidden" (page row 1258, code 2268 and
  2280, gate print 13592). Probe H6 adds a second definition
  `#define MILAN_ID_MAGIC (milan_read(MILAN_ID))`, so the compiled identity
  guard becomes `id != milan_read(0x000u)` and never mismatches. No text rule
  fails closed: the identity rule reads `MILAN_ID_MAGIC` through the address
  model's first definition (`test_builder.py:3061-3066`, `setdefault`). H6 is
  REFUSED at dev in both environments (by the macro-body rule), REFUSED at the
  head with the SDK only by the `-E` comparison ("is not the boot path the
  compiler COMPILES": two `milan_read` tokens in `milan_init()` against one
  in the text), and ACCEPTED at the head with every cross compiler hidden.
  The narrowing's two controls (a store value built in a read macro, a forged
  identity sample) do not exercise a hidden read in a comparison operand.
- (b) Probe H10, the head's own product-only `0 &&` arm in the choke point's
  verdict test (an unverified entity advertised in the product), is REFUSED
  at dev without a compiler (conditional-reach ban) and ACCEPTED at the head
  without one. Its mutation entry is correctly counted among the 26 skipped,
  but the registered NOT RUN says NOTHING refuses what "the token-joining
  splice ban, the ## paste ban, the directory pin and the ordered ... sets
  used to refuse"; the verdict's first clause defines what the retired rules
  used to refuse as "a token-joining splice, a ## paste, a file beside the
  firmware, a cast, store or asm the resolver would place in the window"; and
  the page (1373-1379) repeats that list and adds that the text half of the
  per-selection grading still grades. None names the conditional-reach ban's
  product-only arms whose defect no text rule reads.

**Impact:** a reader of the one line gate 1b says must be read, or of the
page, concludes that a compiler-absent runner still refuses reach-ban shapes
and hidden reads through fail-closed text rules; it refuses neither. There is
no loss where a merge is graded: both are refused with the compiler. The
practical loss is small, because a pre-existing edit (R273-S2) already
defeats the same identity guard everywhere; the defect is the inaccurate
coverage statement that the scope decision asks to be exact.

**Required outcome:** the narrowed macro-body rule's reason states what
actually refuses a read hidden in a macro and what it does not cover without
a compiler (or the narrowing is drawn so that a surviving text rule refuses
H6); the registered NOT RUN text, the verdict's first clause and the page's
compiler-absent section name the conditional-reach ban's compiler-only half
(product-only arms such as H10) and the narrowed rule's hidden-read shapes
among what nothing refuses there; a reason-pinned control for H6 exists on the
sentence of whichever rule or instrument refuses it.

**Verification:** gate 1b in both environments; H6 and H10 through
`scripts/probe.py`: REFUSED with the SDK on the stated sentence, and without a
compiler either refused or explicitly named as NOT RUN; the page, the NOT RUN
text and the gate print agree.

### R273-S1 - SUGGESTION (pre-existing, follow-up Issue) - Robustness, Docs

**Artifact:** `sw/builder/test_builder.py:2543` (`cpp_directive_re`),
`:3544` (`directive_re`), `:3061-3063` (the address model's `#define`
reader), all anchored `(?m)^[ \t]*#`; the new page sentence
`docs/integration/BAREMETAL_FIRMWARE.md:270-277`.

**Evidence:** the pinned SDK's GCC 14.3 honours a directive after a lone CR,
a form feed or a vertical tab, and a backslash-CR splice
(`receipts/22-gcc-line-terminators.txt`). The gate's readers find a directive
only after LF, so these conditionals are invisible to the per-selection
grader, the directive-set closure and the address model. H12 and H13 (the
product-only `0 &&` choke-point arm behind lone CRs or form feeds), H14 (the
pre-AEM ADP clear kept in the census tree and dropped in the product) and H9
(the verifier's `#else` behind a lone CR, its hidden arm returning 1) are
ACCEPTED at dev AND at the head, with and without the compiler.

**Impact:** an unverified advertise, or a stale entity after a warm reboot,
in the product with every hosted gate green. Not a regression: dev's reach
ban read directives with the same regex. The new sentence "Every preprocessor
conditional is graded one arm selection at a time ... so no arm is read in
one state and compiled in another" is nonetheless untrue for these spellings.

**Recommended:** file an Issue; read directives with GCC's line terminators
(or refuse a lone CR, form feed or vertical tab before `#`), and qualify the
sentence until then.

### R273-S2 - SUGGESTION (pre-existing, follow-up Issue) - Robustness

**Evidence:** H7, a second `#define MILAN_ID_MAGIC id` (the identity guard
becomes `id != id`), is ACCEPTED at dev and at the head in both environments.
The PR's open risk 3 records a second `#define` of a register NAME as refused
by the resolver; `MILAN_ID_MAGIC` is a value, and nothing refuses it.
**Recommended:** an Issue for duplicate definitions of names the text model
reads (the first definition wins at `test_builder.py:3066`).

### R273-S3 - SUGGESTION (pre-existing) - Robustness, Tests

**Artifact:** `sw/builder/test_builder.py:3237-3258`
(`assert_verifier_other_arms`, which iterates `arms[1:]`).

**Evidence:** H8 deletes the verifier group's `#else` arm, so the no-slot
build falls off the end of the non-void `load_aem_image()`. It is ACCEPTED at
dev and at the head in both environments. The new pin covers the explicit
other arm, not the implicit one. **Recommended:** require the exempt group to
be closed by `#else` (or treat "no arm" as the pinned arm), with a control.

### #409 acceptance 4 (the author's open point): resolved, not a finding

The two helper-body stores are refused in the mutation table by the surviving
return-provenance rule (`milan_reg() must return exactly MILAN_CSR_BASE plus
the offset`), which answers first on every machine. The resolver's own
sentence (`STORES into the Milan CSR window`, naming the function and the
resolved address) is REQUIRED for both on every compiler run by the
blindness control (`test_builder.py:11132-11157`), with no text rule in front
of it, while the census is required to be blind. With the resolver
disconnected before the baseline the whole gate fails closed at that control
(`receipts/33-resolver-off-full.txt`). This meets #409 acceptance 1 (refused by
the resolved-value message naming function and address, with no cast or store
set active) and acceptance 4 in substance: nothing the cast set refused is
lost, and the resolver-side message is measured on its own. I accept the
interpretation.

## Rule-by-rule retirement judgment (compiler present unless stated)

| Rule (page row at 7fd04d45) | Head verdict | Replacing instrument in the page table | Accepted case RED at dev (both envs) / GREEN at head (both) | Controls fail with the replacement disconnected | Judgment |
|---|---|---|---|---|---|
| conditional reach (565) | RETIRED | per-selection grading | ACC1, ACC2: yes / yes | with `sel` off: 15 miss their pin, 4 pass the whole gate (SDK); 6 and 1 without a compiler | sound with the compiler; absent accounting is F1(b); lone-CR blind spot is pre-existing S1 |
| conditional carrying `#define` (565) | NARROWED | per-selection grading | ACC3: yes / yes | verifier-group `#define` RED now, GREEN at dev | sound |
| token-joining splice (564) | RETIRED | `-E` in the six bodies, resolver elsewhere | ACC5: yes / yes | 12/12 splice and paste controls pass with `-E`, census and resolver off; with `-E` alone off, 10 still refused by the resolver | sound; splice bypasses H1, H3, H5 refused by the resolver |
| `##` (585) | RETIRED | the same two | ACC4: yes / yes | in the 12/12 | sound; paste bypasses H2, H4, H11 refused by the resolver |
| `%:`/`??` (585) | KEPT | none | n/a | digraph control on every machine | honest reason |
| read-only `#define` accessor (584) | NARROWED | "read rules fail closed" | ACC6: yes / yes | n/a | reason inaccurate: F1(a) |
| directive set (566) | KEPT | none | n/a | existing | honest reason |
| directory pin (568) | RETIRED | `-H` by path opened and file reached | ACC11: yes / yes | 3/3 (`command.h`, `init.h`, link) pass with `-H` off | sound; link probe H15 (`init.h`) refused |
| include name pin (567) | KEPT | none | n/a | unchanged | honest reason |
| cast set, store set, reorder (563, 583) | RETIRED | resolver store census | ACC7, ACC8, ACC9: yes / yes | with resolver and census off, 48 entries pass, every retired-set control among them | sound |
| inline-asm set (563) | RETIRED | the same, reading the template | ACC10: yes / yes | asm and `lui` controls pass with resolver and census off | sound |

Table comparison (`receipts/32-table-compare-{sdk,absent}.txt`): every dev
mutation pinned on a retired rule is present at the head and refused on the
replacing instrument's sentence with the SDK (the reach-ban entries on the
selection sentence AND the property), or became an accepted case (the six dev
"retirement candidates" and the benign dropped-arm statement). Counts: 228
with the SDK and 167 without at the head, 217 and 182 at dev; 27 + 4 accepted
edits at the head and 17 + 4 at dev, in both environments; without a
compiler 35 census/resolver entries and 26 retired-rule entries are skipped.
Grader shapes (`receipts/21-grader`): `#elif`, nested groups, `#if 0` and the
16-selection bound behave as documented in both environments.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R273-F1) | #408/#409 bodies and 2026-09-21 scope comments; accepted cases RED at dev and GREEN at head (`receipts/20-probes`); table comparison (`receipts/32-*`); `.github/workflows/docs.yml:185-190` and `elaborate.yml:260` (`--require-rv32`); hosted exact-head check runs (`receipts/40-hosted-check-runs.tsv`) | R273-1 | a13b6e2e461695cdb8d978444ae499a5a6745429 |
| RTL | CLEAN | `git diff --stat 759da623..a13b6e2e` (no `hdl/` file); gate 1b's RTL and datapath rules unchanged and re-run for every selection (`test_builder.py:8396-8407`); 46/46 RTL mutation variants elaborated under Verilator 5.050 (`receipts/10-head-gate1b-sdk.log`); driver and CI interface (`test_firmware_compiler.py`, `--require-rv32`, SKIPPED registration) unchanged and exercised; grader error and default paths (`conditional_groups`, 16-selection bound, guards, verifier group) probed (`receipts/21-grader`) | R273-1 | a13b6e2e461695cdb8d978444ae499a5a6745429 |
| Robustness | UNCLEAN (R273-F1) | hostile probes H1-H15 at dev and head in both environments (`receipts/20-probes`); disconnect audits (`receipts/30-disconnect`); resolver-off fail-closed run (`receipts/33-*`) | R273-1 | a13b6e2e461695cdb8d978444ae499a5a6745429 |
| Tests | UNCLEAN (R273-F1) | full gate 1b in both environments (`receipts/10-head-gate1b-*`); each retired rule's controls failing with the replacement disconnected (`receipts/30-disconnect`); tuple reason-pin negative control (printed in `receipts/10-head-gate1b-sdk.log`); `test_firmware_compiler.py --selftest` (`receipts/50-static-gates.txt`) | R273-1 | a13b6e2e461695cdb8d978444ae499a5a6745429 |
| Docs | UNCLEAN (R273-F1) | `docs/integration/BAREMETAL_FIRMWARE.md` diff (ledger, caveats, compiler-absent section), `docs/testing/CI_WORKFLOWS.md:1126-1127`, gate prints; `docs_check.py`, `check_baremetal_only.py --check` and `--selftest`, `check_em_dash.py --base 759da623`, `git diff --check`: all exit 0 (`receipts/50-static-gates.txt`) | R273-1 | a13b6e2e461695cdb8d978444ae499a5a6745429 |

## Executable evidence produced in this round (this head unless stated)

- Pinned SDK verified: `scripts/ci_rv32_sdk.py --verify-only` exit 0
  (`receipts/01-sdk-verify.log`), Bootlin
  `riscv32-ilp32d--glibc--stable-2025.08-1`, GCC 14.3.0. The scoped Verilator
  was identified as 5.050 before use.
- Gate 1b through `sw/builder/test_firmware_compiler.py`: SDK mapped, exit 0,
  228/228, 27/27 + 4/4, 0 NOT RUN, 306 compiles; every cross compiler hidden,
  exit 0, 167/167, 27/27 + 4/4, 1 registered NOT RUN, verdict `TEXT RULES
  ONLY, AND WEAKER` (`receipts/10-head-gate1b-*`). Dev: 217/217 and 182/182,
  17/17 + 4/4 (`receipts/12-base-gate1b-*`).
- Probes (`scripts/probe.py`, `scripts/make_cases.py`): accepted cases and
  hostile shapes at dev and head in both environments; mutation-table audits
  with each replacement disconnected; one full head run with the resolver
  disconnected.
- Hosted exact-head contexts, read only: every required context `success`;
  docs-check ran the compiler-absent control and `test_builder.py
  --require-rv32` with `TEXT RULES + INSTRUMENTS`; elaborate ran
  `--require-elaboration --require-rv32` with `TEXT RULES + INSTRUMENTS`. The
  physical gPTP context was skipped. The manager owns hosted and act
  acceptance.
- The review clone was never edited: tracked bytes, modes, index and the
  submodule gitlinks equal the head tree (`receipts/02-clone-verify-*.txt`).

## Prior public review findings on this PR

(Completed after the verdict and ledger above were written; see the section
below.)

## Real limits

- No hardware and no physical calibration; field skips are not hardware proof.
- Only gate 1b and focused probes were run, not the whole builder bank, the
  parent, PP or gPTP suites, or Yosys; the manager's source banks are the
  evidence for those.
- Disconnects rebind gate closures in a disposable copy (`scripts/probe.py`);
  the results agree with the author's published disconnect table.
- Lone CR, form feed and vertical tab behaviour was measured with the pinned
  SDK's preprocessor, not with the LiteX product build.

## Pending manager duties

- Route R273-F1 to the author and re-review the corrected head.
- Decide follow-up Issues for R273-S1, S2 and S3 (pre-existing, measured at dev).
- Candidate-merge validation against live dev
  `26d855a9176d63625e6635a029a0c44e3d57ce9a`; hosted and act acceptance;
  reconcile with the internal review.

R273-1 FINISHED
