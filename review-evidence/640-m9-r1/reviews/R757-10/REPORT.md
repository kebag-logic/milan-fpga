[R757] NEGATIVE - exact head d63b378d27c1c663034744a5b48a99c190271f58

# R757-10: round 9 delta review of PR #828 (issue #640)

Head `d63b378d27c1c663034744a5b48a99c190271f58`, tree `1a46d16e200ffa03e23ebe520f152add55f25b1e`. Delta from round 8 head `20933ef4`: 4 commits, 16 modified Markdown pages. Source base and live dev `1f29f189`.

Abbreviations: FR = `docs/reference/FR_NFR.md`, AB = `docs/design/AREA_BUDGET.md`, AP = `docs/design/MARK_II_AREA_PLAN.md`, SE = `docs/design/MARK_II_STREAM_ENGINES.md`, SPLIT = `docs/ARCHITECTURE_HW_SW_SPLIT.md`, MS = `docs/design/MAILBOX_SPLIT.md`.

## Result

- **The verdict is NEGATIVE because of one open MINOR, F1:** MS:41-43 says, with no bound, that the fabric keeps the gPTP plane. It is the same defect class as R757-9-F2, on a page neither R757-9 nor the author's sweep caught. The fix is one clause.
- **R757-9-F1 is resolved.** AB agrees with NFR-RES-01, and the gate's check-baseline passes.
- **R757-9-F2 is resolved on every page it listed.** The author's added edits are also correct.
- **R758-8-R1 and R758-8-R2 are resolved,** with the exact text those findings gave.
- **Three new RESIDUE items and one SUGGESTION** are below, so the author can absorb everything in one pass.
- **The owner has one undecided point:** D8's 1 percent margin against 20,000 LUTs. It is named below and is not a finding.

## Findings

### F1 MINOR - Docs, Conformance - `docs/design/MAILBOX_SPLIT.md:41-43` - the split design page says the fabric keeps the gPTP plane, with no F6 bound

- **Authority and evidence:**
  - MS:41-43, under "What moves, and what the fabric keeps", reads: "The bare-metal core runs ADP, ACMP, MAAP, SRP (through lwSRP) and AECP. The fabric keeps framing and timestamps, the gPTP plane, the media path, the timers that carry hard deadlines, and an ingress filter."
  - `REQUIREMENTS.md:36`: "After F6, firmware owns the gPTP protocol and servo". `REQUIREMENTS.md:43`: "Until F6, the fabric MUST also retain the gPTP plane". SPLIT:115-117 deletes `KL_gptp_shadow` at F6.
  - The page never names the gPTP move: its only two "F6" hits (MS:718, MS:771) are test-case labels in `test_acmp_mbx.cpp`. MS:13 points at the placement contract, but the page still restates placement at MS:42, and F2's required outcome allows only one or the other.
  - Receipt: `receipts/stale_contract_search.txt`, group G6.
- **Not previously handled:** R757-9's receipt did not search this phrasing. The author's sweep lists MS:12-15 and MS:439 as bounded and does not list MS:42. The delta does not touch the page. The PR's amended requirements are what made the line false after F6, so it stands as R757-9 F2's other pages did.
- **Why MINOR rather than RESIDUE:** this is a placement claim a requirement contradicts after F6, the same grading R757-9 gave F2. It is true today and through the switch-over, and the page's status line is scoped to the shipping image. So I am unsure it is only wording, and the rule makes that MINOR.
- **Impact:** someone implementing Mark II from the split's design page would conclude that the gPTP plane stays in fabric, against the charter this PR sets. No code or gate depends on the line: `sw/firmware/ctrl/test/ctrl_service_bounds.py` is the page's only gate reader and checks its mailbox service figures.
- **Required outcome:** MS bounds the gPTP plane at F6, or points at the split contract in place of that clause. Suggested text: "The fabric keeps framing and timestamps, the media path, the timers that carry hard deadlines, and an ingress filter. It keeps the gPTP plane until F6, then firmware owns the protocol and servo."
- **Verification:** `stale_contract_search.sh` group G6 shows MS:42 bounded; the page's reader `ctrl_service_bounds.py` and the documentation gates pass. MS is a gate-read page, but the PR is already classified as relevant, so the classification does not change.

### R1 RESIDUE - Docs - `docs/traceability/ieee8021q.md:29-38` - the new bullet breaks "splits cleanly in two"

- **Evidence:** the delta turned the Mark II line into a third list item under "This clause splits cleanly in two now". Today's fact, "MRP-1..MRP-8 and SRP-1..SRP-10 are now PROCESSOR", now sits under the bullet that opens with Mark II instead of under "Reservation is the protocol processor's."
- **Impact:** a reader sees three parts where the sentence says two, and the current status under a future-placement bullet. No claim or figure changes.
- **Exact fix:** drop the `- ` at line 38 so the MRP text continues the Reservation bullet. Then put these two sentences in their own paragraph after the list: "Mark II moves reservation to firmware after the switch-over." "Both placements owe the same wire behavior." Re-run the style check on the block.

### R2 RESIDUE - Docs, Conformance - `docs/design/AREA_BUDGET.md:129-130, 140, 179-180` - the ceiling is stated without its shape

- **Evidence:** FR:473 sets the ceiling "at the 32x32 shape". AB:130 and AB:140 give "fewer than 20,000" without it, and AB:180 gives "fewer than 20,000 LUTs, with timing met". Each sits beside a link to the requirement and none gives a different value. AB:129 also still calls the requirement "the accepted headroom target".
- **Exact fix:** AB:129 "is the accepted target". AB:130 "Mark II must use fewer than 20,000 LUTs of `xc7a100t` at 32x32." AB:140 "Mark II fewer than 20,000 at 32x32 (about 31.5 %)". AB:180 "That is fewer than 20,000 LUTs at 32x32, fitting Block RAM, with timing met." These cells are outside the gate's policy table. Keep the `#headroom-target` heading, because `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:1073` links it.

### R3 RESIDUE - Docs - `docs/design/MAILBOX_SPLIT.md:13`, `docs/findings/README.md:26` - two leftover labels

- **MS:13** says the contract "defines the Mark II default". D11 removes the option, so Mark II has no default. MS:14 already bounds today's default. Exact fix: "The [placement contract](../ARCHITECTURE_HW_SW_SPLIT.md) defines the transition and end state." This can go in with F1.
- **`docs/findings/README.md:26`** marks #649 "Current" and says "a tenth of the NFR-RES-01 gap", with the gap undated. Its neighbour at line 25 already says "was then". The finding pages themselves are dated records and name 60 percent. Exact fix: "a tenth of the gap to NFR-RES-01's then 60 percent target".

### S1 SUGGESTION - Docs - `docs/guides/SYSTEM_INTEGRATOR.md:95`, `docs/BUILD_FLASH_BOOT.gen.py:44` - today's facts that could say so

"gPTP remains independent from entity enablement" and "fabric gPTP owns PHC + publication" describe the shipping image and make no Mark II claim, so neither is a miss. A page-level "shipping image" line would make that explicit. Optional.

## The five checks

### Check 1: AB against NFR-RES-01: holds, apart from wording R2

| Requirement of this round | Result | Evidence |
|---|---|---|
| 60 percent and 38,040 only as marked history | Holds. Every hit is in a passage saying replaced, formerly or "was": AB:132-133, 182-186, 200, 245, 370-372, 402-404 | `receipts/stale_contract_search.txt` G1 |
| Target row gives the Mark II ceiling | Holds, AB:140. It also names the shipping image's own bound, as FR:473 does | AB:130-140 |
| Acceptance bar gives the ceiling | Holds, AB:179-180 | AB:179-180 |
| Shipping image shows no other LUT bound | Holds, AB:135-136, 140 | FR:473 "carries no other LUT bound" |
| Measured figures unchanged | Holds. The only numbers new to the diff's added lines are 20,000 and 31.5, plus the 8 of "D8"; no number left the page. 52,012, 82.04 % and every headroom cell stand | `receipts/area_budget_arithmetic.txt` |
| Derived history correct | 13,972, 10,521, 57 %, 37,659 and 31.5 % all recompute | `receipts/area_budget_arithmetic.txt` |
| Marked section's reach | "This section" at AB:199-203 runs from AB:197 to AB:428, which contains the remaining ledger, the headroom columns and D8. AB:429 and later state no replaced figure | Heading list of AB; G1 |
| check-baseline | rc 0. Policy table digest identical at `1f29f189`, `20933ef4` and the head. Two mutants in a disposable copy fail with rc 2, so the page is really read | `receipts/check_baseline.txt`, `policy_table_digests.txt`, `check_baseline_mutant.txt` |

### Check 2: listed pages: holds

All of R757-9-F2's listed pages now state the transition and end state or point at the split contract, and SPLIT section 1 carries both. README:59-71, `docs/overview/FULL_FPGA_SOLUTION.md:5-19` and `docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md:21-32` match `docs/overview/ARCHITECTURE.md:6-16` and `REQUIREMENTS.md:27-45`.

Today's facts are not lost: the shipping default, the acceptance scope, the F0/F1 line, the mailbox boundary, the classifier line, the CSR uses, the LiteX memory pointer and the inventory scope all remain. The removed "Unqualified functions retain fabric placement" is the wording SPLIT removed.

### Check 3: stale-contract search: one miss, F1

`stale_contract_search.sh` covers groups G1 to G8 outside `docs/history`, `docs/findings` and `CHANGELOG.md`, and G9 lists the findings separately. Non-document paths appear in G1 to G5 only.

| Hits | State |
|---|---|
| **MS:42** | **MISS: F1** |
| MS:13 | Bounded by MS:14, wording: R3 |
| AB:228, 281, 353, 412 | Inside AB's marked section |
| AP:691, 712, 813, 846, 911, 1323, 1377, 1391, 1444, 1465, 1468-1469, 1472, 1579-1580, 1585, 1594 | Under AP's marker at AP:316-318; the charter's own page |
| AP:67, AP:251 | Say kept then, replaced now |
| README:62-69, `REQUIREMENTS.md`, SPLIT, FR:76-84, 305, 320, 328, 477, 500, `docs/overview/ARCHITECTURE.md`, FULL_FPGA_SOLUTION:9-16, AXIS_CORES:24-30, GLOSSARY:29, 45 | Scoped by "until the switch-over", "until F6" or "after" |
| GPTP_PLANE:22 | Generated contents line; the page's first line scopes it |
| `docs/reference/REGISTER_MAP.md:293` | The dated `0x0056` entry |
| `docs/reference/MILAN_COMPLIANCE_MATRIX.md:5-6`, `docs/design/SAVED_STATE_FASTCONNECT.md:1436`, MS:1078, MS:439, FR:72, FR:505, FULL_FPGA_SOLUTION:104, ieee8021q:115, AXIS_CORES:44 | True during the transition; no retained option stated |
| GLOSSARY:28, 30, 31; README:152; `docs/integration/BAREMETAL_FIRMWARE.md:111, 116, 195`; `docs/litex/LITEX_SOC.md:119`; `docs/guides/gptp/TEST_DEVELOPER.md:26`; SYSTEM_INTEGRATOR:95; `docs/BUILD_FLASH_BOOT.*` | Today's image, with no Mark II claim: S1 |
| FR:462 | A deadline obligation, placement-neutral |
| MS:55, MS:133, `docs/reference/MAILBOX_CONTRACT.md:447` | Name today's source of the grandmaster event; not ownership claims |
| `docs/findings/**` | Dated records naming 60 percent, except the index label: R3 |
| Hash digests, CI "60%" limits, REGISTER_MAP:634, MEDIA_CLOCK_FOLLOWING:2460, AP:1243, unrelated "selectable" and "default" hits | Unrelated to the contract |

### Check 4: author's added edits: hold

- **`docs/ENDSTATION_BUILDER.md:3-7`:** correct. The shipping-build and default lines are kept, and the pointer replaces "adds selectable control placement".
- **`docs/integration/INTEGRATION_GUIDE.md:5-6`:** correct. "gPTP interfaces until F6" rests on `REQUIREMENTS.md:34-45`, SPLIT:115-117 and SPLIT:237-238, and it says nothing false about what follows F6, where the PHC and timestamps stay. The author flagged this as a reading. I agree with it. "It preserves media interfaces" is carried over and no source contradicts it.
- **`docs/design/GPTP_PLANE.md:6-7`:** correct, and it scopes the page's later "only product time owner" contents line.
- **The other sweep edits are also correct:** AXIS_CORES:36-42 (matches `REQUIREMENTS.md:44-45`), GLOSSARY:45 (matches `REQUIREMENTS.md:34-37`), and the removal in AB. ieee8021q:38 is correct in substance; its structure is R1.

### Check 5: docs workflow and classifier: confirmed as the author reported

| Question | Answer | Evidence |
|---|---|---|
| Classifier at round 8's PR file list | `false` | `receipts/ci_scope.txt` |
| Classifier at this head | `true` | same |
| Head's list without AB | `false`, so AB alone flips it | same |
| Classifier selftest | PASS | `receipts/doc_gates.txt` |
| Workflows and scripts changed in the delta | None | `git diff` over the non-document roots is empty |
| Who reads AB | `rtl-fast.yml:430` runs check-baseline; `pp_resource_gate.py:755-776` reads only the policy table | Unchanged digest; mutants |
| Consequence | By AGENTS section 7, exact-head `verilator-suites` and `yosys-portability` apply. The "Only Markdown" not-run reason in the earlier local candidate no longer holds. The PR body's CI scope row says so | PR body line 234 |

"GREEN, documentation only" at PR body line 24 and "Documentation only" at line 317 remain true of the content, and line 24 limits itself to the docs workflow.

Hosted snapshot at 2026-11-01T22:00:56Z (`receipts/hosted_snapshot.txt`): `docs-gates-0/1/2`, `docs-check-no-git`, `wire-accountability`, `changes`, `full-ci-gate`, `elaborate-gates-0`, `bdd-conformance` and others had succeeded. The Verilator and Yosys shards and `yosys-elaboration` were queued or running, not skipped, which fits the classifier. The queued ones are not execution evidence. `Physical gPTP` was skipped, which is not hardware proof.

## For the owner, not a finding

**D8's 1 percent margin against the 20,000-LUT ceiling is undecided by any source.** AB:400-402 keeps "requires at least 1 percent planning margin" and marks 37,659 as the replaced target's. No page says whether a margin applies to 20,000, which would make it 19,800. The pages correctly decide nothing.

## Prior findings

Read after my own pass; see the first limit below.

| Finding | State at this head | Evidence |
|---|---|---|
| R757-9-F1 MINOR | **Resolved** | Check 1 |
| R757-9-F2 MINOR | **Resolved on every listed page.** The class continues as this round's F1 on an unlisted page | Checks 2 and 3 |
| R758-8-R1 RESIDUE | **Resolved**, the exact three sentences | SE:450-453 |
| R758-8-R2 RESIDUE | **Resolved**, the exact text | AP:60, AP:255, PR body line 28 |
| R757-8-R1 RESIDUE | 192 kHz row closed through R758-8-R1. **Retained** for the 96 kHz row and the PR body's Round 8 row | PR body line 233 |
| R757-8-R2 RESIDUE | **Retained** | FR:306 still reads "that derivation" |
| R757-7 RR13 RESIDUE | **Retained**, the manager's | #640 body line 36 still reads "Every talker stream meets the 65 µs target" |
| R757-9 S1, S2 | **Retained**, optional. FR:473 and AP:71 still give 52,008 undated; AB:140 and the baseline give 52,012 | Unchanged text; AB:140 |
| R758-8 S1, S2 and earlier optional items | **Retained**, optional, unchanged by the delta; not re-judged | Delta does not touch them |

## Lens results

```text
[R757] MINOR Conformance - docs/design/MAILBOX_SPLIT.md:41-43 - F1: the fabric keeps the gPTP plane, against REQUIREMENTS.md:36, 43. AB against FR:473 otherwise holds; R2 is wording
[R757] PASS RTL - receipts/delta_files.txt; git diff 20933ef4 d63b378d over hdl, syn, sw, tb, configs, scripts, ci, .github is empty - no RTL, constraint, register or generator file in the delta; prior verdict stands
[R757] PASS Robustness - receipts/delta_files.txt; receipts/check_baseline_mutant.txt - no runtime path in the delta; the one gate-read page refuses a changed or missing policy table with rc 2
[R757] PASS Tests - receipts/check_baseline.txt; receipts/check_baseline_mutant.txt; receipts/doc_gates.txt; receipts/packet_verify.txt - no test changed; check-baseline can fail for the defect it claims; docs gates and the classifier selftest pass at this head; 50 author rc files all 0
[R757] MINOR Docs - docs/design/MAILBOX_SPLIT.md:41-43 - F1; residue R1, R2, R3 recorded with exact fixes; S1; the rest of the delta holds, per checks 1 to 4
```

## Ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | AB; FR:473; `REQUIREMENTS.md:27-45`; SPLIT sections 1 and 3; MS:1-43; all delta pages | None. R757-10 found F1 | `d63b378d27c1c663034744a5b48a99c190271f58` |
| RTL | CLEAN | `receipts/delta_files.txt`; empty diff over the non-document roots | R757-10; the delta changes nothing in scope since R757-8 and R758-8 | `d63b378d27c1c663034744a5b48a99c190271f58` |
| Robustness | CLEAN | `receipts/delta_files.txt`; `receipts/check_baseline_mutant.txt` | R757-10; the delta changes no runtime path | `d63b378d27c1c663034744a5b48a99c190271f58` |
| Tests | CLEAN | `receipts/check_baseline.txt`; `check_baseline_mutant.txt`; `doc_gates.txt`; `ci_scope.txt`; `packet_verify.txt`; `author-r9/evidence/gates/` | R757-10 | `d63b378d27c1c663034744a5b48a99c190271f58` |
| Docs | UNCLEAN (F1); residue R1, R2, R3 and the retained items | All 16 delta pages; MS; `receipts/stale_contract_search.txt`; `area_budget_arithmetic.txt`; `doc_gates.txt` | None. R757-10 found F1 | `d63b378d27c1c663034744a5b48a99c190271f58` |

## Real limits

- **The interim note and the grading.** As assigned, I wrote an interim verdict and ledger before reading prior findings. That note read POSITIVE, subject to prior-finding resolution, and has been overwritten by this report. MS:42 was already in my search output then, but I had not read its context. I graded it after reading MS's scope and R757-9's grading of the same class, so F1's severity follows that precedent and is not independent of it. The manager may rule differently on the same facts.
- **The searches are text searches.** Groups G1 to G9 cover the phrasings in the script. Other wordings may exist, and MS:42 itself escaped two earlier searches. `docs/history`, `docs/findings` and `CHANGELOG.md` were not judged, apart from the G9 listing and R3.
- **Later-round scope.** By the assignment, I judged the delta only. SE's derivations, the charter's decisions and FR's text were not re-derived. I read the charter pages only where the delta depends on them. Earlier rounds are not reopened.
- **The packet is checked for integrity, not authenticity.** No signed local CI packet exists at this head. The 116 author-r9 evidence files match the publication manifest, and all 116 SHA256SUMS lines match the manifest's original digests. 16 published files differ from their originals only by the manifest's path redaction, which I cannot inspect byte for byte. The manifest travels in the same unsigned evidence commit.
- **Author logs do not name the head themselves.** I tied them to it by my own reruns at this head, whose counts match (docs_check 213 and 1436, em dash 1906 lines over 21 pages, contents 152 pages, paths 1084). I did not rerun builder legs, compiler gates or the other long docs-workflow steps. The delta changes no input to them other than Markdown, and they succeeded on hosted runners at this head. Leg 1's 16 NOT RUN arms are the author's report, confirmed only by the log's summary (`gate_25_1_builder.log:536, 553`).
- **Hosted evidence is a snapshot and the manager's to accept.** Long gates had not finished when it was taken.
- **Prior reports.** I read R757-9 in full, and from R758-8 only the residue items and the lines naming them.
- **No hardware.** Physical calibration NOT RUN; field skips are not hardware proof. Every latency figure in these pages is a derivation, not a measurement.
- **Comment rule.** The delta touches no source comment, so it has no instance to judge.
- **Process notes.**
  - My first gate attempts ran the repository's scripts in a mode that cannot import their sibling modules, and my first mutant hit the wrong table. All were rerun; the receipts hold only the corrected runs.
  - Gate runs left an ignored `scripts/__pycache__/` in the clone, which I removed.
  - The pinned Markdown renderer was installed into a disposable environment under `scratch/`.
- **Clone state.** Exact head, tree and index tree `1a46d16e`, no tracked or ignored change. The six gitlinks match head and index and are uninitialized (`receipts/clone_state.txt`). All probes ran on disposable copies.

## Pending manager duties

- Rule on F1: fix it in this PR, which needs a new source head and review of that delta, or overrule the grade. Moving it to another Issue does not resolve it, by AGENTS section 7.
- Take D8's margin question to the owner.
- Carry R1, R2, R3 and the retained RESIDUE items, including RR13, to the residue checklist.
- Accept exact-head `verilator-suites`, `yosys-portability` and the rest of the hosted set, and the local replica, on the final head. The "Only Markdown" not-run reason no longer applies.
- Decide whether the owner's approval of the requirement text needs restating for NFR-LAT-03, carried from R758-8.
- After merge, the daily area measurement's column "Against the 38,040 LUT floor (NFR-RES-01, 60 %)" no longer matches FR:473.
- The merge-turn candidate and its banks, and post-merge containment.

R757-10 FINISHED
