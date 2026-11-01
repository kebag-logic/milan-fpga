[R757] NEGATIVE - exact head 6c7c0947c5d36e48005db94332e9a4308c55f254

# R757-9: composition review of PR #828 (issue #640)

Candidate tree `2299420e70cea4ce2dcb0450c5ff0fbb56bbf9f0`. Source head `20933ef48a9b174e58a9d17ddd59078a072024af`. Live dev `1f29f189279f9fc0132f4918e47342b87d22f33a`.

Abbreviations: FR = `docs/reference/FR_NFR.md`, AB = `docs/design/AREA_BUDGET.md`, AP = `docs/design/MARK_II_AREA_PLAN.md`, SE = `docs/design/MARK_II_STREAM_ENGINES.md`, SPLIT = `docs/ARCHITECTURE_HW_SW_SPLIT.md`.

## Result

- **The composition itself is clean.** The candidate's tree is byte-identical to the reviewed source head. It adds no defect beyond the reviewed sources, the signed local CI packet verifies, and every gate that reads the changed files passes.
- **The verdict is NEGATIVE because of two open MINOR findings, F1 and F2.** Both are in the source change, not the composition: PR #828 amends requirements, and pages it does not touch still state the old contract. A text search of the PR comments and PR body finds neither gap named by an earlier round.
- **This is a scope call the manager may want to see.** The assignment defines POSITIVE as "no defect beyond the reviewed sources", which holds. It also says an open MINOR makes the verdict NEGATIVE, with no scope exception. I applied the stricter rule, because AGENTS section 7 does not let a round bank a lens while leaving what it found open, and F1 and F2 cannot honestly be graded RESIDUE.
- **If F1 and F2 are fixed,** the delta is documentation on pages outside the seven changed here, and the composition checks below need repeating on the new candidate only.

## Composition

| Question | Answer | Evidence |
|---|---|---|
| Queued predecessors in the candidate | None. The set is `{}` | `receipts/candidate_commit.txt`: parents are dev `1f29f189` and source `20933ef4` |
| Files changed by this PR and by a predecessor | None | No predecessor exists |
| Candidate tree against source head | Identical, `2299420e` on both | `receipts/candidate_commit.txt`; empty diff in `receipts/clone_state.txt` |
| Candidate current against live dev | Yes. Remote dev is still `1f29f189` and PR head is still `20933ef4` | `receipts/clone_state.txt` |
| What the PR changes | Seven Markdown files, modes unchanged, one new | `receipts/candidate_diff_raw.txt` |
| Overlap with dev since the branch began (`e5b8405d..1f29f189`) | `REQUIREMENTS.md` and `docs/README.md`, resolved in source merge `22f3cedb`. Each merged side adds one line, and `docs/README.md` is +1/-0 against dev | `git show --cc 22f3cedb4`; dev's lines stay |
| Registries, workflow pins and gate inventories | Untouched. No workflow, script, JSON, YAML or HDL file is in the diff | `receipts/candidate_diff_raw.txt`; workflow digests in `receipts/localci_manifest_check.txt` |
| Docs tables, TOC and anchors | Clean. The new page has its one index row. My link probe resolved 421 links from or into the changed pages, 0 unresolved | `docs/README.md:81`; `receipts/probe_links.log` |

## Gates run on the candidate

Scripts: `run_gates.sh`, `run_gates_pinned.sh`. Logs: `receipts/gates/`, `receipts/gates_pinned/`.

| Gate | Result |
|---|---|
| `docs_check.py` | 0 findings over 213 Markdown and 1436 text files |
| `check_em_dash.py --base 1f29f189`, `--selftest` | 0 findings over 1792 added lines; 339/339 arms |
| `gen_toc.py --check`, `--verify-anchors`, `--selftest` | OK on 152 pages; 580 fragment links reproduced; 1501/1501 arms |
| `ci_events.py --check`, `--selftest` | OK on 2199 contract items; 5258 arms |
| `check_doc_style.py` with selftest, `check_doc_paths.py`, `check_archive.py` | Pass |
| `check_feature_status.py` with self-test, `gen_module_matrix.py --check` | Pass |
| `DOC_MAP.gen.py --check`, `check_solution_docs.py`, `check_submodule_docs.py`, `check_diagram_pngs.py` | Pass |
| `check_gptp_docs.py`, also `--with-submodule` | Pass |
| `check_hygiene.py --check`, `check_todo_ownership.py`, `check_wire_accountability.py` with self-test | Pass |

These gates passing does not contradict F1 or F2. None of them compares a requirement's value with what another page says about it.

The first unpinned pass refused five renderer gates and two submodule gates, and the wire gate stopped on the missing submodule. Those logs stay in `receipts/gates/` as environment refusals, with non-zero rc. `receipts/gates_pinned/` holds the same gates rerun with the pinned renderer and submodules at their pinned gitlinks, all rc 0.

## Signed local CI

| Check | Result | Evidence |
|---|---|---|
| Manifest digest | `572f026e...d903`, as assigned | `receipts/localci_verify.txt` |
| `allowed_signers` key | One key, fingerprint `SHA256:dRI12tvJkhueTEGqsRutn2L+dT/5qqOCsCVzBU5CI7k`, as required | `receipts/localci_allowed_signers.txt` |
| `ssh-keygen -Y verify`, principal `milan-local-ci`, namespace `milan-local-ci` | Good signature, rc 0 | `receipts/localci_verify.txt` |
| Subject | Names candidate `6c7c0947`, parent `1f29f189`, head `20933ef4`, both trees `2299420e`, PR 828 | `receipts/localci_manifest_check.txt` |
| Coverage | 47 entries for 47 workflow jobs, none missing or extra, all ok: 25 by act, each a successful job; 22 not run with a named reason | same |
| Workflow digests | All four match the candidate's files | same |
| Not-run reason | "Only Markdown, 7 files, against 1f29f189" is true at this tree | `receipts/candidate_diff_raw.txt` |
| Banks | Builder 48 commands and native 5, all exit 0 | same |

## Findings

### F1 MINOR - Docs, Conformance - `docs/design/AREA_BUDGET.md:129-130, 135, 173, 175-177, 225, 349, 380, 497` - the budget page still states NFR-RES-01 as 60 percent, 38,040 LUTs

- **Authority and evidence:**
  - FR:473 now reads: "This ceiling replaces the earlier target of at most 60 % LUT (38,040)", and the shipping image "carries no other LUT bound".
  - The #640 body says the 20,000-LUT target "replaces the 60 % (38,040-LUT) target".
  - AB is unchanged by this PR and says, in the present tense:
    - "The baseline product must fit `xc7a100t` with at most 60 percent" (:130).
    - `at most 38,040 (60 %)`, "not met, 13,972 over", linked to the amended row (:135).
    - "The active #640 acceptance bar is the whole-image NFR-RES-01 target", needing the wrapper at 10,521 LUTs (:173-176).
    - "stays at 60 %" (:177).
    - M9 closure "<= 38,040 LUT" (:225).
    - "The binding bar remains 38,040" (:380).
  - AP handled its own copy: AP:318 marks that plan as "the Mark I plan against 38,040 LUTs" and says the Mark II sections supersede it. AB has no such marking, and AP:73 sends readers to AB for the resource policy.
  - Receipt: `receipts/stale_contract_search.txt`.
- **Not caused by the composition:** AB is identical at dev and at the candidate. FR:473's source change is what made it false.
- **Not previously handled:** no PR #828 comment names this page, and the PR's "Known limitations / out of scope" list does not exclude it.
- **Why not RESIDUE:** the fix changes a stated figure, a status ("not met") and a claim about what a requirement says.
- **Impact:** after merge, two current pages give different values for one requirement. A lane reading AB would size against 38,040 and read the shipping image as failing a bound it no longer has. No gate reads the figure, so no build result changes.
- **Required outcome:** AB agrees with FR:473. The 60 percent and 38,040 survive only as marked history, as AP:318 does. The target row and the active acceptance bar give the Mark II ceiling, and the shipping image shows no other LUT bound.
- **Verification:** `receipts/stale_contract_search.txt`'s first search, re-run, finds each line only in a passage marked as replaced; the documentation gates pass.

### F2 MINOR - Docs, Conformance - pages listed below - other current pages still state Mark II as selectable, with gPTP in fabric

- **Authority and evidence:**
  - `REQUIREMENTS.md:33`: "After the switch-over, no all-fabric build remains".
  - `REQUIREMENTS.md:36`: "After F6, firmware owns the gPTP protocol and servo".
  - SPLIT:4: "No retained-fabric option stays in the end state".
  - FR:84 says the same.
  - The PR corrected this same paragraph in `docs/overview/ARCHITECTURE.md:6-16` and nowhere else.
  - Receipt: `receipts/stale_contract_search.txt`.
- **Flatly wrong for Mark II after merge:**
  - `README.md:58-62`: Mark II "selects each control function at build time", and "gPTP and media remain in fabric".
  - `docs/overview/FULL_FPGA_SOLUTION.md:5-7`: Mark II defaults, "remain selectable", "Audio, gPTP ... remain in fabric".
  - `docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md:22-23`: "all-fabric remains supported", with no end to it.
  - `docs/GLOSSARY.md:29`: "Mark II selects firmware or fabric".
  - AB:201: "All-fabric remains supported", in the Mark II ledger.
- **Partly true, because "until F2 to F5 acceptance" bounds the shipping default, but silent on the end state.** Each says "Mark II placement is build-selectable" and "Its default is bare-metal":
  - `docs/design/MAAP_FABRIC.md:4-6`
  - `docs/fpga/DATAPLANE_WALKTHROUGH.md:4-6`
  - `docs/fpga/FPGA_DESIGN.md:4-6`
  - `docs/litex/LITEX_SOC.md:4-6`
  - `docs/overview/SYSTEM_DOMAIN_MAP.md:4-6`
  - `docs/traceability/ieee8021q.md:4-6`
- **Not caused by the composition:** none of these pages changed against dev (`receipts/stale_contract_search.txt`, last line).
- **Why MINOR rather than RESIDUE:** these lines make placement claims a requirement now contradicts, and the root README is the first page a reader sees. I am unsure they count as wording only, and the rule makes that MINOR.
- **Impact:** a reader of the root README or the solution overview concludes that Mark II keeps gPTP in fabric and keeps an all-fabric build, against the charter this PR sets. No code or gate depends on it.
- **Required outcome:** each page either states the transition and the end state as `docs/overview/ARCHITECTURE.md` now does, or points at the split contract without restating placement.
- **Verification:** the second search in `receipts/stale_contract_search.txt`, re-run, finds no line that describes Mark II as permanently selectable or as keeping gPTP in fabric after F6; the documentation style gate passes.

### Suggestions (optional)

- **S1 - Docs - SE:227, FR:306, AP:255:** the owner's 2026-11-01 19:53 answer ("for now leave 143 us", #640 comment 6562369400) post-dates the source head. The pages agree with it, because 143.347 µs is quoted as reached and the maximum stays with the lane. They cite only the 13:35 decision. Adding the later link would close the record for a cold reader.
- **S2 - Docs - FR:473, AP:71:** "It measures 52,008 LUTs" is present tense in a requirement row. AB:135 and `syn/ooc/pp_resource_baseline.json:29` record 52,012 as the gate's anchor, and AB:150 gives 52,021 for the #787 route now on dev. The difference is at most 13 LUTs and no decision depends on it. AP:37-39 dates 52,008 as the measured basis; "measured 52,008 LUTs on 2026-10-31" would fit in FR:473 and AP:71 too.

## Prior findings

Read after my independent pass over the diff. The delta from source head to candidate is empty, so nothing below changes state through this round's composition.

| Finding | State at this head | Evidence |
|---|---|---|
| R757-8-R1, R758-8-R1 RESIDUE | Retained, with the exact fixes those reports give | SE:450-451 still reads "So that row may be low" |
| R757-8-R2 RESIDUE | Retained | FR:306 still reads "that derivation" |
| R758-8-R2 RESIDUE | Retained, including the PR body | AP:60, AP:255 and PR body line 27 still read as the whole class |
| R757-7 RR13 RESIDUE | Retained, the manager's | The #640 body still says "Every talker stream meets the 65 µs target" |
| R757-7-F1 MINOR | Stays resolved, and the owner has now answered | FR:306, SE:230-243; #640 comment 6562369400 confirms the 13:35 decision stands |
| R757-8 S1-S5, R758-8 S1-S2 and earlier optional items | Retained, optional | Unchanged text |

No RESIDUE from earlier rounds is a new defect, and none is re-graded here.

## Lens results

```text
[R757] MINOR Conformance - docs/design/AREA_BUDGET.md:135; README.md:62 - F1 and F2: pages state requirement values and placements the amended rows replace
[R757] PASS RTL - receipts/candidate_diff_raw.txt - no RTL, register, generator or constraint file in the candidate's diff; candidate tree equals source head
[R757] PASS Robustness - receipts/candidate_diff_raw.txt; receipts/localci_manifest_check.txt - Markdown only, no runtime path changes; the fault-path text is as the source reviews judged it
[R757] PASS Tests - receipts/gates_pinned/; receipts/localci_manifest_check.txt - no test or harness in the diff; docs gates and their selftests pass on this tree; 47/47 jobs mapped
[R757] MINOR Docs - docs/design/AREA_BUDGET.md:129-130; README.md:58-62 - F1 and F2; the composition's own docs checks (index row, TOC, anchors, em dash, style) are clean
```

## Ledger

The composition touches no lens's scope, because the candidate tree equals the source head. RTL, Robustness and Tests are therefore covered by the source reviews on that same tree. Conformance and Docs are unclean on this round's own findings, which come from the source change.

| Lens | Result | Composition touches its scope? | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | No | FR:84, 306, 473; `REQUIREMENTS.md:31-37`; SPLIT:4; AB lines in F1; pages in F2; #640 body and owner comments | None. R757-9 found F1 and F2 | `6c7c0947` |
| RTL | CLEAN | No | `receipts/candidate_diff_raw.txt`; tree comparison | R757-8 and R758-8, confirmed by R757-9 | `20933ef4`, same tree as `6c7c0947` |
| Robustness | CLEAN | No | `receipts/candidate_diff_raw.txt`; signed coverage | R757-8 and R758-8, confirmed by R757-9 | `20933ef4`, same tree as `6c7c0947` |
| Tests | CLEAN | No | `receipts/gates/`, `receipts/gates_pinned/`; `receipts/localci_manifest_check.txt` | R757-8 and R758-8, confirmed by R757-9 | `20933ef4`, same tree as `6c7c0947` |
| Docs | UNCLEAN (F1, F2), residue retained | No | Gate logs; `receipts/probe_links.log`; `receipts/stale_contract_search.txt`; AB, README and the F2 pages | None. R757-9 found F1 and F2 | `6c7c0947` |

## Real limits

- **Later-round review.** By the assignment, this round judged the composition and spot-checked the source. SE's derivations and figures were not re-derived; they keep the source reviews' verdicts. Sections read in SE and AP were latency, budget and target only.
- **F1 and F2 searches are text searches.** They cover the phrasings in the receipt, and other wordings of the old contract may exist. `docs/history` and `docs/findings` were excluded from F2 and not judged for F1, because they are dated records.
- **Link probe.** `probe_links.py` uses its own slug rule and does not fetch external links. The 182 external links from the changed pages were counted only.
- **Banks are taken from the signature.** The manifest records bank commands as argv digests with exit codes. I verified the signature and the digests' exit codes, and did not rerun any bank or see the commands' logs.
- **Author receipts.** I spot-checked `author-r8` gates 8, 9, 16, 43 and 45 at `868be2f6`: all rc 0, and gates 8, 16 and 45 give the same counts as my runs.
- **Hosted evidence is the manager's.** At source head, `rtl-fast`, `docs-check`, `docs-check-no-git`, `wire-accountability` and `elaborate` succeeded. `verilator-suites` and `yosys-portability` were skipped by the scope filter. A skipped context is not execution, and I accept nothing from it.
- **No hardware.** Physical calibration NOT RUN. Field skips are not hardware proof. Every latency figure in the pages is a derivation, not a measurement.
- **Comment rule.** The diff touches no source comment, so it has no instance to judge.
- **Process notes.**
  - The session's permission mode refused one compound command, which also deleted the superseded refusal logs. I reran the gates into a new directory and kept those logs.
  - Two small file lists went to the system temporary directory rather than the packet, by mistake. They hold only tracked path names.
- **Clone state.** The clone stayed at exact head with a clean status and no ignored files. Tree and index both give `2299420e`. The six gitlinks are unchanged and uninitialized there; the submodule gates ran in a disposable clone under `scratch/` (`receipts/clone_state.txt`).

## Pending manager duties

- Rule on F1 and F2: fix in this PR, which needs a new source head and review of that delta, or overrule the scope. AGENTS section 7 says moving a finding to another Issue does not resolve it.
- Carry the retained RESIDUE items and RR13 to the residue checklist.
- Decide whether the owner's approval of the requirement text, given as reviewed at `3f5fea24`, needs restating for NFR-LAT-03 as it now reads. This is carried over from R758-8.
- After merge, the daily area measurement's column "Against the 38,040 LUT floor (NFR-RES-01, 60 %)" no longer matches FR:473.
- Hosted and local-replica acceptance, the merge-turn candidate and its banks, and post-merge containment.

R757-9 FINISHED
