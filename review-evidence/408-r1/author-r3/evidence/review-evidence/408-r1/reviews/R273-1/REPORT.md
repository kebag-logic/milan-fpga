[R273] NEGATIVE - exact head a13b6e2e461695cdb8d978444ae499a5a6745429

External independent review R273-1 of PR #535 (issues #408 and #409). Head
`a13b6e2e461695cdb8d978444ae499a5a6745429`, tree
`44729af1c6f9e164d8ca82eda5a47d3708b96a6d`, source base
`759da623072358afdb0e9d570a7b4b6a788492c9`. Cleared context. The task was
reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the two issue
bodies, the manager's scope comments on #408 and #409 (2026-09-21, "Remaining
scope after PR #498"), the assignment and takeover comments, the PR body, the
diff and history, and executable evidence produced in this round. Receipts are
listed in `MANIFEST.sha256`; the scripts that produced them are in `scripts/`.

## Verdict in one paragraph

Most of the retirement ledger holds. Every accepted case is RED at dev on its
retired rule's own sentence in both compiler environments and GREEN at the
head in both. Every hostile control the head adds fails once its replacement
is disconnected. Six splice and paste bypasses of surviving text rules,
written for this review, are all refused by the resolver. Both hosted builder
consumers still pass `--require-rv32`, and compiler absence is a registered
NOT RUN that is never counted as coverage. The #409 acceptance-4 point is
satisfied in substance. The verdict is NEGATIVE for five open findings. One
is this round's own: R273-F1 (MINOR), about inaccurate compiler-absent
coverage statements. The other four are the internal review's R272-1
findings, each reproduced independently here and RETAINED at this head:
- a BLOCKER. With the pinned SDK, a product-only conditional whose `#` follows
  a form feed, vertical tab, NUL or lone CR hides a store into `ADP_CTRL`.
  Dev's ordered sets refused it and the head accepts it;
- a MAJOR. A splice or `##` paste forges the identity local inside
  `milan_init()`. Dev refused it and the head accepts it;
- two MINORs: an undisclosed cost of grading every arm combination, and the
  "every conditional is graded" claim, which needs bounding.

**Order of work, stated for the record.** This round's verdict and ledger were
written and frozen before the internal review was read. The frozen copy is
`receipts/60-report-before-reading-other-review.md`, and its hash and time are
in `.stamp`. That copy was already NEGATIVE, carrying R273-F1 and three
SUGGESTIONs. Its S1 recorded the lone-CR, form-feed and vertical-tab
directive gap as pre-existing, because its probes (H9, H12 to H14) tested
control-flow shapes that dev accepted too. The store shapes of R272-F1, and a
lone-CR variant added here (V1d), show that dev's ordered cast and asm sets
refused them whatever the directive reader saw. S1 is therefore withdrawn as a
separate SUGGESTION and folded into the retained BLOCKER.

## Findings raised by this round

### R273-F1 - MINOR - Conformance, Robustness, Tests, Docs

**Artifact:** `docs/integration/BAREMETAL_FIRMWARE.md:1258` (the narrowed
macro-body row) and `:1367-1379` ("What a runner with no RV32 compiler
gets"). In `sw/builder/test_builder.py`:
- `:2266-2280`, the narrowed rule's comment and message;
- `:9461-9472`, the registered NOT RUN text;
- `:13399-13404`, the verdict's first clause;
- `:13590-13593`, the COSTS print;
- `:10896-10915`, the narrowing's two controls.

**Title:** the compiler-absent coverage statements overstate what the
surviving text rules refuse.

**Authority/evidence:** three authorities apply:
- #408 acceptance 2: each rule is retired, narrowed, or kept "with its cost
  restated and a reason";
- the 2026-09-21 scope comments on #409 and #408: "Compiler absence remains
  an explicit NOT RUN for the new measurements, rather than a claim of
  coverage";
- #408 acceptance 1: the closing line names the arm.

Measured with `scripts/probe.py`; receipts are
`receipts/20-probes/{base,head}-{sdk,absent}.{json,txt}`.
- (a) The narrowed macro-body rule is justified by "every rule that reads a
  read fails closed when the read is hidden" (page row 1258, code 2268 and
  2280, gate print 13592). Probe H6 adds a second definition,
  `#define MILAN_ID_MAGIC (milan_read(MILAN_ID))`. The compiled identity guard
  becomes `id != milan_read(0x000u)`, which never mismatches.
  - No text rule fails closed. The identity rule reads `MILAN_ID_MAGIC` from
    the address model's first definition (`test_builder.py:3061-3066`,
    `setdefault`).
  - At dev H6 is REFUSED in both environments, by the macro-body rule.
  - At the head with the SDK it is REFUSED only by the `-E` comparison ("is
    not the boot path the compiler COMPILES": the `-E` text has two
    `milan_read` tokens in `milan_init()` and the source text has one).
  - At the head with every cross compiler hidden it is ACCEPTED.
  - The narrowing's two controls (a store value built in a read macro, a
    forged identity sample) do not exercise a hidden read in a comparison
    operand.
- (b) Probe H10 is the head's own product-only `0 &&` arm in the choke
  point's verdict test, which advertises an unverified entity in the product.
  Without a compiler it is REFUSED at dev (by the conditional-reach ban) and
  ACCEPTED at the head. Its mutation entry is correctly counted among the 26
  skipped. Yet the three places that say what nothing refuses there omit it:
  - the registered NOT RUN says NOTHING refuses what "the token-joining splice
    ban, the ## paste ban, the directory pin and the ordered ... sets used to
    refuse";
  - the verdict's first clause says the retired rules used to refuse "a
    token-joining splice, a ## paste, a file beside the firmware, a cast,
    store or asm the resolver would place in the window";
  - the page (1373-1379) repeats that list and adds that the text half of the
    per-selection grading still grades.

  None names the conditional-reach ban's product-only arms whose defect no
  text rule reads.

**Impact:** a reader of the page, or of the one line gate 1b says must be
read, concludes something false: that a compiler-absent runner still refuses
reach-ban shapes and hidden reads through fail-closed text rules. It refuses
neither. Nothing is lost where a merge is graded, because the compiler
refuses both. The practical loss is small, since a pre-existing edit
(R273-S2) already defeats the same identity guard everywhere. The defect is
the inaccurate coverage statement, which the scope decision asks to be exact.

**Required outcome:**
- The narrowed macro-body rule's reason states what actually refuses a read
  hidden in a macro, and what it does not cover without a compiler. The
  alternative is to draw the narrowing so that a surviving text rule refuses
  H6.
- The registered NOT RUN text, the verdict's first clause and the page's
  compiler-absent section name, among what nothing refuses there, the
  conditional-reach ban's compiler-only half (product-only arms such as H10)
  and the narrowed rule's hidden-read shapes.
- A reason-pinned control for H6 exists on the sentence of whichever rule or
  instrument refuses it.

**Verification:** run gate 1b in both environments, then H6 and H10 through
`scripts/probe.py`:
- with the SDK, both are REFUSED on the stated sentence;
- without a compiler, each is either refused or explicitly named as NOT RUN.

The page, the NOT RUN text and the gate print must agree.

## Prior public review findings on this PR: R272-1, resolved or retained

R272-1 (internal review) was published on this PR at 2026-09-23T20:42:34Z,
after this round had started. Before it, the PR carried no review, no inline
comment and no finding. Each finding below was re-measured here with this
round's own cases (`scripts/make_more_cases.py`, `cases/verify_r272.json`,
`scripts/run_verify.sh`). The receipts are `receipts/70-verify/`; the summary
table is `receipts/70-verify/r272-summary.txt`.

| Case | dev, SDK | dev, absent | head, SDK | head, absent |
|---|---|---|---|---|
| V1a form feed before `#`, product-only arm, literal-address cast store in a UART handler | REFUSED (cast set) | REFUSED | ACCEPTED | ACCEPTED |
| V1b vertical tab, same store | REFUSED (cast set) | REFUSED | ACCEPTED | ACCEPTED |
| V1c NUL, same store | REFUSED (cast set) | REFUSED | ACCEPTED | ACCEPTED |
| V1d lone CR, same store (added here) | REFUSED (cast set) | REFUSED | ACCEPTED | ACCEPTED |
| V1e form feed, `lui`/`sw` asm store | REFUSED (asm set) | REFUSED | ACCEPTED | ACCEPTED |
| V1f control, plain `#` | REFUSED | REFUSED | REFUSED (selection + census) | ACCEPTED (NOT RUN) |
| V2a `i\`-newline-`d = MILAN_ID_MAGIC;` before the identity guard | REFUSED (splice ban) | REFUSED | ACCEPTED | ACCEPTED |
| V2b `MILAN_CAT(i, d) = MILAN_ID_MAGIC;` | REFUSED (`##` ban) | REFUSED | ACCEPTED | ACCEPTED |
| V2c plain function-like macro forging `id` | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| V3a debug helper defined and called under two `#ifdef MILAN_DEBUG_TOD` | ACCEPTED | ACCEPTED | REFUSED | ACCEPTED |
| V3b debug counter, same pattern | ACCEPTED | ACCEPTED | REFUSED | ACCEPTED |
| V4 two unterminated `'` defines bracketing a product-only store | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |

### R272-F1 - BLOCKER - RETAINED - Conformance, Robustness, Tests, Docs

**Artifact:** `sw/builder/test_builder.py`:
- `:2543-2544`, `cpp_directive_re`;
- `:2609`, `error_line_re`;
- `:3544`, `directive_re`;
- `:3061-3063`, the `#define` reader;
- `:2700-2742`, `arm_selections()`, and `:8396`, its only call.

Every one of these readers anchors on `^[ \t]*#` after LF. The docs are
`docs/integration/BAREMETAL_FIRMWARE.md:270-277`, `:1282` and `:1317`.

**Evidence:** GCC 14.3 from the pinned SDK honours a directive after a lone
CR, a form feed or a vertical tab, and it honours a backslash-CR splice
(`receipts/22-gcc-line-terminators.txt`). The NUL case is reproduced by V1c.
None of the gate's readers sees such a conditional. The census compiles the
stub tree's arm, and the product's arm goes unread. V1a to V1e were REFUSED
at dev in both environments, by the ordered cast and asm sets, which read
every arm whatever the directive reader saw. They are ACCEPTED at the head
with the SDK. The head's grader, `-E` comparison, census and resolver all see
only the stub arm. Pre-existing shapes with the same root cause, measured by
this round's first pass, are ACCEPTED at dev and at the head:
- H12 and H13, the `0 &&` choke-point arm;
- H14, the pre-AEM clear kept in the census tree and dropped in the product;
- H9, the verifier's `#else` behind a lone CR.

**Impact:** on the configuration that grades a merge, gate 1b accepts a
firmware that sets `ADP_CTRL` bit 0 from a UART command handler with no AEM
verdict. Dev refused those spellings. That breaks #408 and #409 acceptance 4
("No reduction"). The page's new claim that "no arm is read in one state and
compiled in another" is false for spellings GCC honours.

**Required outcome:**
- Every line the pinned GCC treats as a directive must be a directive to every
  C directive reader in gate 1b: the conditional readers, the `#error`
  reader, the directive-set closure and the definition readers. Lone CR, form
  feed, vertical tab and NUL are all covered by this, whether as line
  terminators or as whitespace before `#`.
- Alternatively, those bytes are refused outside comments and literals.
- Hostile controls for each spelling are pinned on the replacement's sentence
  and fail when it is disconnected.
- The page and gate-print claims are bounded to what is measured.

**Verification:** V1a to V1e are REFUSED with the SDK at the fixed head; V1f
is still REFUSED; H9 and H12 to H14 are REFUSED; gate 1b still passes 27/27
and 4/4.

### R272-F2 - MAJOR - RETAINED - Conformance, Robustness, Tests, Docs

**Artifact:** `sw/builder/test_builder.py`:
- `:4208-4210`, `boot_path_tokens`;
- `:3960-3963`, the `PREPROCESSED_PIN` comment: "Every mutant that makes this
  gate read a boot path the compiler does not compile fails on it, whether a
  conditional, a token-joining splice or a paste spelled it";
- `:9095-9124`, the identity rules, which read blanked, unspliced text.

The docs are `docs/integration/BAREMETAL_FIRMWARE.md:292-307`, `:1283-1284`
and `:1318`.

**Evidence:** V2a and V2b were REFUSED at dev, by the splice ban and the `##`
ban, and are ACCEPTED at the head with the SDK. The statement count and the
eight boot tokens agree between the text and `-E`, and no resolver question
covers the identity sample. V2c, a plain function-like macro, is ACCEPTED at
both dev and the head, so the property itself was already exposed at dev.

**Impact:** the cost-table row at page line 1230 says the `MILAN_ID` local is
not assigned between its read and its guard. Two spellings dev refused now
defeat it. The retirement's stated carrier (`-E` inside the six bodies)
compares only eight tokens, not every name the surviving text rules read.

**Required outcome:** inside the six bodies, the text rules read names after
translation phases 1 and 2 and after pasting, or every identifier those rules
key on is compared. Otherwise the retirement is narrowed and the compared set
is stated exactly, at the site and on the page. The pre-existing plain-macro
exposure (V2c, and R273-S2) is recorded on a public Issue.

**Verification:** V2a and V2b are REFUSED with the SDK at the fixed head, or
the bound is published with the Issue link.

### R272-F3 - MINOR - RETAINED - Conformance, Docs

**Artifact:** `sw/builder/test_builder.py:2700-2742`, where
`arm_selections()` grades every combination. Its refusal sentence is at
`:4015` (`SELECTION_PIN`, "one of the firmwares the product may build") and
`:8405`. The page's cost row is `docs/integration/BAREMETAL_FIRMWARE.md:1236`.

**Evidence:** V3a and V3b were ACCEPTED at dev and are REFUSED at the head
with the SDK. The failing selection is "no arm taken; ... arm 1 of 1 taken"
for the same macro, which no build selects. The census compile fails because
GCC 14 treats an implicit declaration as an error. The cost table discloses
only `#if 0` and more than 16 selections.

**Impact:** a common debug pattern is newly refused. The message describes a
firmware the product cannot build, and neither the page nor the gate print
lists the cost (#408 acceptance 2 and 5).

**Required outcome:** either disclose the cost with a remedy and word the
selection sentence accurately, or grade correlated groups consistently.

**Verification:** read the page and the gate print, or confirm that V3a and
V3b are ACCEPTED with the SDK and pinned as accepted cases.

### R272-F4 - MINOR - RETAINED - Robustness, Docs

**Artifact:** `sw/builder/test_builder.py:2431-2436`, where `blanked()` scans
a character literal across newlines. `conditional_groups()` and
`arm_selections()` rely on it. The page claim is at
`docs/integration/BAREMETAL_FIRMWARE.md:270-277`.

**Evidence:** V4 is ACCEPTED at dev and at the head, in both environments. It
is not a regression, because dev's sets blanked the same region. The head's
new claim that every preprocessor conditional is graded does not hold for
text that `blanked()` lexes differently from GCC. GCC ends an unterminated
character literal at the end of its line, and the census compile has no
`-Werror`.

**Impact:** the retirement premise is stated without its bound.

**Required outcome:** refuse an unterminated literal outside comments, or
bound the claim at the site and on the page and record a public Issue. The
Issue alone does not clear the lens.

**Verification:** V4 is REFUSED at the fixed head, or the bound and the Issue
link are published.

**Where the two reviews differ, and why neither changes the other.**
- R272-1 accepted the read-only accessor narrowing and the compiler-absent
  accounting. R273-F1 shows both statements to be inaccurate, with no loss
  where a merge is graded.
- This round agrees with R272-1 on #409 acceptance 4, the directory pin and
  the kept rules.

## SUGGESTIONs (pre-existing, measured at dev, not regressions)

### R273-S2 - SUGGESTION - Robustness

**Evidence:** H7 is a second `#define MILAN_ID_MAGIC id`, which turns the
identity guard into `id != id`. It is ACCEPTED at dev and at the head, in
both environments. The PR's open risk 3 says the resolver refuses a second
`#define` of a register NAME. `MILAN_ID_MAGIC` is a value, and nothing
refuses it.

**Recommended:** open an Issue, together with R272-F2's plain-macro exposure,
for duplicate definitions of names the text model reads. The first definition
wins at `test_builder.py:3066`.

### R273-S3 - SUGGESTION - Robustness, Tests

**Artifact:** `sw/builder/test_builder.py:3237-3258`
(`assert_verifier_other_arms`, which iterates `arms[1:]`).

**Evidence:** H8 deletes the verifier group's `#else` arm, so the no-slot
build falls off the end of the non-void `load_aem_image()`. H8 is ACCEPTED at
dev and at the head, in both environments. The new pin covers the explicit
other arm but not the implicit one.

**Recommended:** require the exempt group to be closed by `#else`, or treat
"no arm" as the pinned arm, and add a control for it.

## #409 acceptance 4 (the author's open point): resolved, not a finding

The two helper-body stores are refused in the mutation table by the surviving
return-provenance rule ("milan_reg() must return exactly MILAN_CSR_BASE plus
the offset"). That rule answers first on every machine.

The blindness control (`test_builder.py:11132-11157`) REQUIRES the resolver's
own sentence for both stores on every compiler run. That sentence is
`STORES into the Milan CSR window`, naming the function and the resolved
address, and no text rule stands in front of it. The census is required to be
blind to the same stores. With the resolver disconnected before the baseline,
the whole gate fails closed at that control
(`receipts/33-resolver-off-full.txt`).

This meets #409 acceptance 1: the stores are refused by the resolved-value
message naming function and address, with no cast or store set active. It
meets acceptance 4 in substance, because nothing the cast set refused is
lost. The interpretation is accepted; R272-1 judged it the same way.

## Rule-by-rule retirement judgment at this head

| Rule (page row at 7fd04d45) | Head verdict | Replacing instrument in the page table | Accepted case RED at dev (both envs) / GREEN at head (both) | Controls fail with the replacement disconnected (`receipts/30-disconnect`) | Judgment |
|---|---|---|---|---|---|
| conditional reach (565) | RETIRED | per-selection grading | ACC1, ACC2: yes / yes | with `sel` off: 15 miss their pin, 4 pass the whole gate (SDK); 6 and 1 without a compiler | NOT ACCEPTED: R272-F1, F3, F4; absent accounting R273-F1(b) |
| conditional carrying `#define` (565) | NARROWED | per-selection grading | ACC3: yes / yes | verifier-group `#define` RED now, GREEN at dev | sound for plain `#`; R272-F1 applies |
| token-joining splice (564) | RETIRED | `-E` in the six bodies, resolver elsewhere | ACC5: yes / yes | 12/12 splice and paste controls pass with `-E`, census and resolver off; with `-E` alone off, 10 still refused by the resolver | NOT ACCEPTED: R272-F2 (H1, H3 and H5 are refused by the resolver) |
| `##` (585) | RETIRED | the same two | ACC4: yes / yes | in the 12/12 | NOT ACCEPTED: R272-F2 (H2, H4 and H11 are refused by the resolver) |
| `%:`/`??` (585) | KEPT | none | n/a | digraph control on every machine | honest reason |
| read-only `#define` accessor (584) | NARROWED | "read rules fail closed" | ACC6: yes / yes | n/a | reason inaccurate: R273-F1(a) |
| directive set (566) | KEPT | none | n/a | existing | honest reason; its reader shares R272-F1's anchor |
| directory pin (568) | RETIRED | `-H` by path opened and file reached | ACC11: yes / yes | 3/3 (`command.h`, `init.h`, link) pass with `-H` off | sound; link probe H15 (`init.h`) refused |
| include name pin (567) | KEPT | none | n/a | unchanged | honest reason |
| cast set, store set, reorder (563, 583) | RETIRED | resolver store census | ACC7, ACC8, ACC9: yes / yes | with resolver and census off, 48 entries pass, every retired-set control among them | NOT ACCEPTED: R272-F1 (the sets read every arm; the replacement sees only the arms the grader finds) |
| inline-asm set (563) | RETIRED | the same, reading the template | ACC10: yes / yes | asm and `lui` controls pass with resolver and census off | NOT ACCEPTED: R272-F1 (V1e) |

**Table comparison** (`receipts/32-table-compare-{sdk,absent}.txt`). Every
dev mutation pinned on a retired rule either:
- is present at the head and refused on the replacing instrument's sentence
  with the SDK (the reach-ban entries on the selection sentence AND the
  property), or
- became an accepted case: the six dev "retirement candidates" and the benign
  dropped-arm statement.

**Counts:**

| Measure | Head | Dev |
|---|---|---|
| Mutations refused, SDK | 228 | 217 |
| Mutations refused, no compiler | 167 | 182 |
| Accepted edits (firmware + Makefile), both environments | 27 + 4 | 17 + 4 |

Without a compiler, 35 census and resolver entries and 26 retired-rule
entries are skipped.

**Grader shapes** (`receipts/21-grader`): `#elif`, nested groups, `#if 0`
and the 16-selection bound behave as documented, in both environments.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R273-F1; R272-F1, F2, F3 retained) | #408/#409 bodies and the 2026-09-21 scope comments; accepted cases RED at dev and GREEN at head (`receipts/20-probes`); table comparison (`receipts/32-*`); `.github/workflows/docs.yml:185-190` and `elaborate.yml:260` (`--require-rv32`); hosted exact-head check runs (`receipts/40-hosted-check-runs.tsv`); re-measurement of R272-1 (`receipts/70-verify`) | R273-1 | a13b6e2e461695cdb8d978444ae499a5a6745429 |
| RTL | CLEAN | `git diff --stat 759da623..a13b6e2e` (no `hdl/` file); gate 1b's RTL and datapath rules, unchanged and re-run for every selection (`test_builder.py:8396-8407`); 46/46 RTL mutation variants elaborated under Verilator 5.050 (`receipts/10-head-gate1b-sdk.log`); driver and CI interface (`test_firmware_compiler.py`, `--require-rv32`, SKIPPED registration), unchanged and exercised | R273-1 | a13b6e2e461695cdb8d978444ae499a5a6745429 |
| Robustness | UNCLEAN (R273-F1; R272-F1, F2, F4 retained) | hostile probes H1-H15 (`receipts/20-probes`) and V1-V4 (`receipts/70-verify`), each at dev and head in both environments; disconnect audits (`receipts/30-disconnect`); resolver-off fail-closed run (`receipts/33-*`); GCC line-terminator receipt (`receipts/22-*`) | R273-1 | a13b6e2e461695cdb8d978444ae499a5a6745429 |
| Tests | UNCLEAN (R273-F1; R272-F1, F2 retained) | full gate 1b in both environments (`receipts/10-head-gate1b-*`); each retired rule's controls failing with the replacement disconnected (`receipts/30-disconnect`); tuple reason-pin negative control (`receipts/10-head-gate1b-sdk.log`); `test_firmware_compiler.py --selftest` (`receipts/50-static-gates.txt`) | R273-1 | a13b6e2e461695cdb8d978444ae499a5a6745429 |
| Docs | UNCLEAN (R273-F1; R272-F1, F2, F3, F4 retained) | `docs/integration/BAREMETAL_FIRMWARE.md` diff (ledger, caveats, compiler-absent section); `docs/testing/CI_WORKFLOWS.md:1126-1127`; gate prints. These all exit 0 (`receipts/50-static-gates.txt`): `docs_check.py`, `check_baremetal_only.py --check`, `check_baremetal_only.py --selftest`, `check_em_dash.py --base 759da623` and `git diff --check` | R273-1 | a13b6e2e461695cdb8d978444ae499a5a6745429 |

## Executable evidence produced in this round (this head unless stated)

**Tools identified before use.**
- `scripts/ci_rv32_sdk.py --verify-only` exited 0 (`receipts/01-sdk-verify.log`).
  It verified the pinned Bootlin SDK
  `riscv32-ilp32d--glibc--stable-2025.08-1`, GCC 14.3.0.
- The scoped Verilator reported version 5.050.

**Gate 1b through `sw/builder/test_firmware_compiler.py`**
(`receipts/10-head-gate1b-*`; dev in `receipts/12-base-gate1b-*`):

| Run | Exit | Mutations refused | Accepted edits (firmware + Makefile) | NOT RUN | Other |
|---|---|---|---|---|---|
| Head, SDK mapped | 0 | 228/228 | 27/27 + 4/4 | 0 | 306 compiles |
| Head, every cross compiler hidden | 0 | 167/167 | 27/27 + 4/4 | 1, registered | verdict `TEXT RULES ONLY, AND WEAKER` |
| Dev, SDK mapped | not stated | 217/217 | 17/17 + 4/4 | not stated | none |
| Dev, every cross compiler hidden | not stated | 182/182 | 17/17 + 4/4 | not stated | none |

**Probes** (`scripts/probe.py` with `scripts/make_cases.py` and
`scripts/make_more_cases.py`):
- accepted cases and hostile shapes, at dev and at the head, in both
  environments;
- mutation-table audits with each replacement disconnected;
- one full head run with the resolver disconnected.

**Hosted exact-head contexts,** inspected read only:
- Every required context concluded `success`.
- docs-check ran the compiler-absent control, and ran
  `test_builder.py --require-rv32` with `TEXT RULES + INSTRUMENTS`.
- elaborate ran `--require-elaboration --require-rv32` with
  `TEXT RULES + INSTRUMENTS`.
- The physical gPTP context was skipped.

The manager owns hosted and act acceptance.

**Clone integrity.** The review clone was never edited. Its tracked bytes,
modes, index and submodule gitlinks equal the head tree
(`receipts/02-clone-verify-mid.txt`, `receipts/03-clone-verify-end.txt`).

**Receipt redaction.** Local paths in receipts are replaced by `<sdk>`,
`<verilator-bin>`, `<packet>`, `<clone>` and `$HOME`. Each substitution is
listed in `receipts/95-redaction.txt`. The case JSON inputs are regenerated
byte-identically by the two case scripts from the tracked firmware, and are
not listed.

## Real limits

- There was no hardware and no physical calibration. Field skips are not
  hardware proof.
- Only gate 1b and focused probes were run. The whole builder bank, the
  parent, PP and gPTP suites, and Yosys were not; the manager's source banks
  are the evidence for those.
- Disconnects rebind gate closures in a disposable copy (`scripts/probe.py`).
  The results agree with the author's published disconnect table.
- Directive behaviour after a lone CR, form feed, vertical tab or NUL was
  measured with the pinned SDK's GCC, not through the LiteX product build.
- `_Pragma` macro stacking and `\f#undef`, noted in R272-1's limits, were not
  re-measured here.

## Pending manager duties

- Route R273-F1 and the retained R272-F1 to F4 to the author, then re-review
  every lens whose scope the fixes change, at the new head.
- Decide the follow-up Issues for R273-S2 and S3, and for the pre-existing
  exposures that R272-F2 and F4 name.
- Validate the candidate merge against live dev
  `26d855a9176d63625e6635a029a0c44e3d57ce9a`, and complete hosted and act
  acceptance.

R273-1 FINISHED
