[R784] POSITIVE - exact head c73be9b93101fde17c5545145b21066f24f7b99b

# R784-4: external review of #665 lane S5 (PR #844), round 4

Head `c73be9b93101fde17c5545145b21066f24f7b99b`, tree `ee578c56e1bec9dc3ce8e3d7f508b8fddc2887e0`. Delta judged: `3f8caae5..c73be9b9`, two commits, `hooks_selftest.py` and the README only, against the ruling in issuecomment-6694276050.

The verdict is POSITIVE. All five lenses are clean, and no BLOCKER, MAJOR or MINOR is open.

- **What holds:** every item of the ruling. Dropping the path term now fails the self-test, the renamed mutants agree with the rule table and the PR, and the author's open points are true as stated.
- **What does not hold:** one sentence of the PR's account of the rule table check. "Only a mutant that wraps a rule's output can step past that rule" is false: five of eight terms I dropped behind stand-in mutants survive. It is recorded as RESIDUE-1 with its exact fix, because only the PR body has to change. The survivors themselves are in code the delta does not touch and are listed under S-2.
- **The group term:** it hides no real defect, so there is no finding on it.
- **Not a claim of this review:** "each hook within its bound" stays open on #665 as ruled. This is a harness review, not hardware proof.

## Focus checks

| Asked | Result | Evidence |
|---|---|---|
| Dropping the path term fails the self-test | **Confirmed** | `sup-no-path`: rc 1, 27 of 28 checks, failing `another path`. With that assertion deleted as well, `a row of another path supersedes a refusal` escapes (`source_probes.txt`). |
| `sup-no-path` is killed by the right assertion | **Confirmed** | My own copy of the edit fails `another path`, `hooks_selftest.py:604`. The published `r783_source_probe.txt` agrees. |
| The new `another path` case tests what it says | **Confirmed** | `hooks_selftest.py:601-604`: `hooks-disc-aging` has a row of `acmp.entity_available` on interface 1 and its own `tmr_no_adp.if1` unmeasured. `acmp.entity_available` is the group's real second path (`hooks.py:473`). |
| The renamed mutants' names, rule table and PR sentence agree | **Confirmed** | 96 mutants, 96 unique names. README rows equal `MUTANTS` by name and check, `mutant_rules.json` has the same keys in the same order, and no old name remains in the tree (`audit_names.txt`). The PR's cited lines are right: `run.py:141`, `README.md:234-237`. |
| Each renamed or new mutant does what its name says | **Confirmed** | `every refusal is superseded` fires `:597`, then `:600`, then `:604`, and escapes only with all three deleted. `the table names a second path` fires `:600`. `the margin is taken from a timeout of zero` fails with `margin -160.0`. `its finding by name is dropped` leaves `LATE H-COUNTERS: ... never served`. |
| Round 3's text is corrected in place | **Confirmed** | Both "Corrected by Round 4" passages are present, and the `3f8caae5` row of the commit table says so. |
| One audit of the rule table, then stop | **Done, as ruled** | All 96 names were read and no name misstates what its mutant varies, which is the defect the ruling named. My audit's fire line agrees with the author's table on all 96. Kinds are 58 wrappers, 22 stand-ins and 16 constants, with 61 twins. |
| Nothing else moved | **Confirmed** | `run.py`, `hooks.py`, `hooks_build.py` and `hooks_soc.py` have the same blobs at `3f8caae5` and the head. Since the base, no file outside `tb/verilator/ctrl_service_hooks/` changed. |

### The author's open points

| Open point | Result | Evidence |
|---|---|---|
| Deleting `other interface` alone lets nothing escape, and the term is held by that assertion directly | **True** | `del-other-interface`: rc 0, 96 of 96. `sup-no-interface`: rc 1, failing `other interface`. |
| The group term has no assertion of its own, and is held by `the table names another group` escaping | **True** | `sup-no-group`: 28 of 28 checks, 95 of 96, that mutant escaped, rc 1. |
| 48 `expect` statements are fired first by no mutant, down from 49 | **True** | My own count: 117 sites, 69 fired, 48 not. At `3f8caae5`: 116 sites, 49 not. |
| `buckets: the window opens right after the registrations` is disclosed; it fires the wait's length, and its twin fails the group's assertion | **True** | The mutant fires `:630` and no mutant fires `:638`. Removing the wait from either group at the source fails `:638`, 0 bus cycles (`twins_spot.txt`). |
| "Each failing on the rule it names" stays a judgement | **True, and accepted** | See the rule table row above. |

The author's other statements hold too: the two reviewer scripts that stop on their anchors do so because the text they patch is gone, and the list of gates not run is plain.

### The group term

Checked because the brief says to report it only if it hides a real defect. It does not.

- **The term is correct at this head.** It decides one shape: the named group's own probe unmeasured while another group measured that path on that interface. The head keeps that refusal. With the term dropped it would be superseded as "measured by hooks-disc-aging", which would be false (`group_shape.txt`).
- **Dropping it is caught.** The self-test exits 1.
- **The eight published runs do not depend on it.** Across the four product-clock and four history runs there are 0 refusals and one supersession. That one is `acmp.tmr_no_adp.if1` at 8x8 idle, 50 MHz, where `acmp-disc` has no row on interface 1, so `hooks-disc-aging` is the only group that could supersede it.
- **What remains is what the author disclosed.** A loosened term can pass: `sup-group-prefix`, which compares the group's first word, stays rc 0. That is the same statement as "no case varies the group", and no real group makes it wrong.

## Findings

No BLOCKER, MAJOR or MINOR.

### RESIDUE-1 [R784] RESIDUE Tests, Docs - PR body, Round 4, "The one check of the rule table" - "Only a mutant that wraps a rule's output can step past that rule" is false

- **Authority/evidence.** The PR defines the mechanical form as "a mutant caught while the rule it names can lose a term at the source with nothing failing", then limits the twins to wrappers on that premise. A stand-in replaces the whole rule, so it steps past the rule's terms as well. Five of eight term drops behind stand-in mutants pass the whole self-test, rc 0, 28 of 28 and 96 of 96 (`twins_standin.txt`); they are listed under S-2.
- **Impact.** A reader concludes that the mechanical form was searched across the rule table and found nowhere. It was searched on 61 of 96 mutants, and "What this leaves, plainly" does not say so. No figure, verdict, test or code is affected: "61 twins" and "58 of the 96" are true as counts, and `rule_table_check.md` says only that 58 wrap.
- **Why RESIDUE.** The fix is to this PR-body passage alone. No test has to change, because the ruling stops the audit and the delta does not touch these rules. No row of the rule table has the ruling's defect: these mutants' names are true of what they vary.
- **Exact fix.** Replace "Only a mutant that wraps a rule's output can step past that rule, and 58 of the 96 do. Each has a twin, the same defect made in the rule's own source." with: "58 of the 96 wrap a rule's output, the shape of the finding's mutant, and each has a twin, the same defect made in the rule's own source. The 22 that stand in for a rule and the 16 that change a constant were read by name, and three of them have a twin; the rest were not tried at the source, and a rule behind them can lose a term with nothing failing (R784-4 S-2)." The packet's `author-r4/HANDOFF.md:75` repeats the sentence and needs no separate change unless it is republished.
- **Verification.** Reading the PR body.

### RESIDUE-2 [R784] RESIDUE Docs - PR body, Contents - the list's order differs from the body's

- **Evidence.** Contents lists Round 2, Round 3, Round 4, then Definition of Done. In the body, Definition of Done comes before Round 2.
- **Exact fix.** Move the Definition of Done bullet to directly after Known limitations.

### SUGGESTION (optional, none affects the verdict)

- **S-1 (Tests) - `hooks_selftest.py:594-595`, `run.py:141`.** `any` to `all` in the rule survives, rc 0 (`sup-any-to-all`). The positive case has exactly one row, while a real run always has others. It fails closed: under `all`, nothing would be superseded and the run would fail on a refusal. Adding `beside` to the positive case's rows would hold it.
- **S-2 (Tests) - pre-existing terms with no holder.** Each passes 28 of 28 and 96 of 96. The code is correct at this head, no figure moves, and the delta does not touch these lines, so they do not affect the Tests lens. The ruling said to stop, so taking them is the maintainer's call.
  - `hooks.py:669`, `next_adp_record`: dropping `inter == interface`, or dropping `k == CH['adp']`. Its mutant is `H-DISC: the window never ends`. The interface term matters at two interfaces.
  - `hooks.py:676`, `disc_decided_ms`: `TMR_DELAY_MAX_MS + bound_ms('disc')`, or `TMR_DELAY_MAX_MS` alone. `README.md:191` states 1040 ms, and no check pins it.
  - `hooks.py:861`, `adopted`: `bool(value)`, so any bit of the word reads as ADOPTED.
  - `run.py:108`, `slack_cycles`: dropping `r['unbounded']`. The path table at `run.py:217` would then print a positive slack for a path never served, against the function's docstring. The `missing` half of that line is equivalent, as a missing row is always unbounded (`run.py:93`).
- **S-3 (Docs) - evidence packet.** The PR cites `source_twins.txt` and the HANDOFF cites `supersede_terms.txt`, but neither `source_twins.py` nor `supersede_terms.py` is in the evidence tree. The receipts show each twin's name and fire lines, not its edit, so a cold reviewer cannot re-run or dispute a twin. `mutant_audit.py` is published; these two could join it, with no new head needed.

## Prior findings, resolved or retained at this head

Read after my verdict and ledger were recorded (`verdict_before_prior_findings.txt`).

| Finding | Status | Evidence at this head |
|---|---|---|
| R783-3 F1 = R784-3 F-1, the supersede mutant and the path term | **Resolved at its cause** | The case exists, a mutant fails on it and escapes when it is deleted, and `any later group` is renamed to what it does. `sup-no-path` is killed. The published `sup-any-path` and `sup-table-any-path` are killed, and `sup-second-entry`, which survived, now fails `a path the table does not name`. |
| R783-3 R1, the Grading row | **Resolved** | The PR's Grading row carries the exact words. |
| R784-3 S-3 | **Taken** | The `beside` and `own` rows are the docstring's "unmeasured there too" shape. |
| R783-3 S3 | **Taken in substance** | `supersede: every refusal is superseded`. |
| R783-3 S4 | **Taken** | The audit reports `ESCAPED` in `mutant_audit_plant_rc1_required.txt:113`. |
| R783-3 S1, S2; R784-3 S-1, S-2 | **Retained, optional** | Out of the ruling. The published survivor lists stand: 8 in `r783_source_probe.txt`, 10 in `source_mutants.txt`. |
| All earlier rounds' findings | **Resolved at their heads; nothing they depend on moved** | The four harness code blobs equal `3f8caae5`. |
| R783-4, this round's internal review | **Read after my verdict; not a prior finding** | Its S1 is my S-1, found independently. Its S2, a continuation line's indent, is retained as optional and I did not re-judge it. |

## Lens results

```text
[R784] PASS Conformance - ruling 6694276050 items 1 to 4, PR body Round 4, source_probes.txt, audit_names.txt - each item met; S5's "each hook within its bound" stays open as ruled, and the PR relates to #665 rather than closing it
[R784] PASS RTL - git diff --name-only 5b5f4336..c73be9b9 (nothing outside the harness), hooks_soc.py blob a84ac7c0 equal at 3f8caae5 and the head, six gitlinks in verify_clone.txt - no RTL or firmware in the delta, so the prior RTL result stands
[R784] PASS Robustness - run.py:139-144, group_shape.txt, selftest_head.txt - harness code unchanged; an unmeasured path stays a refusal in each shape probed; S-1's quantifier fails closed; the self-test gives the same result at three hash seeds from another directory
[R784] PASS Tests - hooks_selftest.py:586-604,747-757,815-821,880, selftest_head.txt, source_probes.txt, audit_names.txt, twins_spot.txt - 28 of 28 and 96 of 96 reproduced line for line against the published receipt; each new assertion can fail for its defect and each new mutant escapes when its assertion is deleted
[R784] PASS Docs - README.md:215,234-237,269, PR body, audit_names.txt - README, rule table and code agree on 96 rows; added lines carry no lane label, round, reviewer ID or comment ID; two RESIDUE items in the PR body only
```

Source gates are the author's published receipts: 0 of 98 nonzero, `git diff --check` rc 0, recorded at this head. I did not re-run them. I ran `git diff --check` on the delta only, rc 0. Both commits are one line with no trailer, and no line of `hooks_selftest.py` exceeds 120 columns.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling 6694276050; REVIEW READY 6695246318; PR body Round 4; `source_probes.txt`; `audit_names.txt` | R784-4 | `c73be9b93101fde17c5545145b21066f24f7b99b` |
| RTL | CLEAN | Delta file list; `hooks_soc.py` blob; six gitlinks in `verify_clone.txt` | R784-4 | `c73be9b93101fde17c5545145b21066f24f7b99b` |
| Robustness | CLEAN | `run.py:139-144`; `hooks.py:446`; `group_shape.txt`; eight published `results.json` | R784-4 | `c73be9b93101fde17c5545145b21066f24f7b99b` |
| Tests | CLEAN | `hooks_selftest.py` delta; `selftest_head.txt`; `source_probes.txt`; `audit_names.txt`; `twins_spot.txt`; `twins_standin.txt` | R784-4 | `c73be9b93101fde17c5545145b21066f24f7b99b` |
| Docs | CLEAN | `README.md` delta and 96-row table; PR body; `mutant_rules.json`; `rule_table_check.md`; `packet_verify.txt` | R784-4 | `c73be9b93101fde17c5545145b21066f24f7b99b` |

## Real limits

- **Scope.** This is the round 4 delta. Code the delta does not touch keeps its prior lens verdict. The S-2 list comes from a spot-check of 23 source edits, not an audit of every rule.
- **Not run by me:** the four runs, the 16 plants, the firmware self-test, the CPU budget harness, the builder, the boundary gate, the docs gates and the candidate merge. No manager source bank runs at this head. Their evidence is the author's receipts at the heads the PR lists.
- **Packet.** All 144 author round 4 files match `MANIFEST.json`'s digests, unredacted. The packet commit `f640f816` is reported unsigned and the evidence tree holds no detached signature, so I verified digests, not a signature.
- **Hosted evidence.** All 6 check runs at this head were queued when last read, so none has executed and I claim none.
- **Hardware.** Physical calibration NOT RUN. Field skips are not hardware proof.
- **Clone.** Every source edit ran on a disposable copy. The clone was verified afterwards: HEAD, tree and index match, 1496 tracked files rehashed with 0 differences, 6 gitlinks match, status empty (`verify_clone.txt`).

## Pending manager duties

- Carry RESIDUE-1 and RESIDUE-2 to the residue checklist.
- Build and validate the current-dev merge candidate and link its receipts. The PR's target `dev-soft-core` is at `a68536fa`; `dev` is at `3f6bef88`.
- Own hosted and act acceptance at the exact head.
- Decide S-1 to S-3, and the author's two maintainer points: the column's scope, and the one-path or per-descriptor decision.
- Keep #665 open for S5's "each hook within its bound", and confirm the two-positive bar and explicit merge authorization.

R784-4 FINISHED
