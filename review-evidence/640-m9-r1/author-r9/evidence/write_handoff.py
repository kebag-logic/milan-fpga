"""Write HANDOFF.md; the gate table comes from round 8's, with this run's figures."""
import re, sys
O = "$MANAGEMENT/2026-09-23/640-a720i/"
prev = open("$MANAGEMENT/2026-09-23/640-a720h/HANDOFF.md", encoding="utf-8").read()
start = prev.index("| Job | Step (workflow id) |")
end = prev.index("\nNotes:\n", start)
table = prev[start:end].rstrip() + "\n"
def sub(a, b):
    global table
    assert table.count(a) == 1, a
    table = table.replace(a, b)
sub("0 findings over 1792 added lines in 7 pages", "0 findings over 1906 added lines in 21 pages")
sub("0 compiler invocations (710 s)", "0 compiler invocations (680 s)")
sub("ALL GATES PASS (1171 s)", "ALL GATES PASS (1176 s)")
sub("over every changed block of the 7 pages against 1f29f189", "over every changed block of the 21 pages against 1f29f189")
READY = sys.argv[1] if len(sys.argv) > 1 else "(posted last)"
text = f"""# HANDOFF - [A720i] issue #640 Mark II charter, round 9 (docs only)

Status: REVIEW READY at head d63b378d27c1c663034744a5b48a99c190271f58 (2026-11-01). Every docs-workflow gate step rc 0 on a clean clone of that head; `git diff --check 1f29f189 HEAD` rc 0. Local only, nothing pushed.

- Lane: $LANES/640-mark2-charter, branch 640-mark2-charter. Round-8 head 20933ef48a9b174e58a9d17ddd59078a072024af (PR #828, still the remote head). Round-9 head d63b378d27c1c663034744a5b48a99c190271f58, tree 1a46d16e200ffa03e23ebe520f152add55f25b1e.
- Base: live dev 1f29f189279f9fc0132f4918e47342b87d22f33a (re-read after the gates, unchanged); merge base 1f29f189. Round 9 adds 118 lines and removes 61 on 16 pages (20933ef4..HEAD); against 1f29f189 the PR adds 1,906 and removes 169 over 21 pages. All 16 are modified Markdown pages; no new file.
- Remote checked: https://github.com/kebag-logic/milan-fpga.git
- Review answered: R757-9 NEGATIVE (https://github.com/kebag-logic/milan-fpga/pull/828#issuecomment-6563425814, F1 and F2), with its report and `receipts/stale_contract_search.txt` read from branch 640-m9-review-evidence at 6f4aa39d. R758-8's and R757-8's residue read from their PR comments.
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6563447660 (text: evidence/taken.md)
- REVIEW READY: {READY} (text: evidence/review_ready_posted.md)
- Scratch: $VALIDATION_STORAGE/640-a720i. Evidence (small files): ./evidence/. Peak unit memory 7.78 GB.

## Read this first

- **The PR is no longer docs-only for CI.** `docs/design/AREA_BUDGET.md` is in `GATE_READ_DOCS` (`scripts/ci_scope.py:71`), so the classifier returns `false` at 20933ef4 and `true` at this head (evidence/scope_and_gate_read.txt). R757-9 expected a re-run of the composition checks only. In fact the exact-head `verilator-suites` and `yosys-portability` gates now apply, by AGENTS section 7, and the signed local candidate's "Only Markdown" not-run reason no longer holds. F1 cannot be fixed without this, since the assignment names that page. I ran only the page's gate reader, `check-baseline`: rc 0.
- **No gate reads a figure F1 changed.** `syn/ooc/pp_resource_gate.py:755-776` reads only the budget's `| Endpoint | LUT ...` policy table, whose digest is identical at both heads. No non-Markdown file names 38,040, 37,659, 13,972 or 10,521. So no figure had to stay for a gate. The measured 52,012 and 82.04 % are unchanged.
- **The reviewer's search commands are not published,** only their output. I re-ran them from the phrasings in the receipt and widened them (evidence/searches_at_head.txt).

## Commits (one-line subjects, no body, no trailers)

| # | SHA | Files | Finding |
|---|---|---|---|
| 1 | 2515b51f97367a3cea7e57eb1b3410bd1ba69d42 | AB | R757-9-F1 |
| 2 | 7e10647cacb3701aaf442989ced1f86feeb36199 | 14 pages | R757-9-F2 and the sweep |
| 3 | 26885333e47f9f6211962d9597ce84f2db4a0f17 | SE | R758-8-R1 |
| 4 | d63b378d27c1c663034744a5b48a99c190271f58 | AP | R758-8-R2 |

`AB` = docs/design/AREA_BUDGET.md, `SE` = docs/design/MARK_II_STREAM_ENGINES.md, `AP` = docs/design/MARK_II_AREA_PLAN.md. No rebase, no amend, nothing pushed. Commits carry no attribution trailer, as the assignment and CONTRIBUTING require.

## F1: AB against FR_NFR.md:473 (file:line at d63b378d)

| Was (at 20933ef4) | Now | Source |
|---|---|---|
| AB:129-131 "must fit ... at most 60 percent"; "does not meet it" | AB:129-136: Mark II ceiling; "That replaces the earlier 60 percent target, 38,040 LUTs."; "The route below was 13,972 over it."; shipping image must fit, resource gate holds it, no other LUT bound | FR:473 |
| AB:135 target "at most 38,040 (60 %)", status "not met, 13,972 over" | AB:140 target: Mark II fewer than 20,000 (about 31.5 %), this image must fit the device; status "fits; no other LUT bound on this image" | FR:473. 52,012 and 82.04 % unchanged |
| AB:173 acceptance bar | AB:179-180: bar is the NFR-RES-01 ceiling, fewer than 20,000 LUTs, timing met | FR:473; #640 body |
| AB:175-178 "needs", "stays at 60 %", "is met by" | AB:182-188: "What follows is history, against the replaced 60 percent."; 10,521 and 13,972 kept in the past tense; the redesign plan "answers the new ceiling" | FR:473, the #234 ruling |
| AB:186 section head, no marking | AB:199-203: "This section is the Mark I plan, kept as history." "Its target was 38,040 LUTs."; the area plan supersedes target and order | As AP:316-322 |
| AB:225 M9 row "<= 38,040" | AB:245 Mark II ceiling and timing met; "formerly <= 38,040 LUT" | FR:473 |
| AB:349 header | AB:369-372: columns stated as history, headers "Headroom to replaced 38,040" and "... 37,659"; every cell unchanged | FR:473 |
| AB:379-380 "is 37,659", "remains 38,040" | AB:402-405: "was", "was then", "NFR-RES-01 has replaced it" | FR:473 |
| AB:497 re-record rule | AB:524-525: names the Mark II ceiling; timing must also be met | FR:473 "re-recorded ... by the change that reaches the target" |

Headings are unchanged, so `#headroom-target` (linked from docs/findings/649) and `#the-resource-gate` still resolve. AB:129 and AB:398 still name NFR-RES-01 with no figure, which is correct against the amended row.

## F2: placement statements (file:line at d63b378d)

| Page, line | Now | Listed by R757-9? |
|---|---|---|
| README.md:59-71 | Transition and end state, as docs/overview/ARCHITECTURE.md:6-16. F0/F1 line kept | Yes |
| docs/overview/FULL_FPGA_SOLUTION.md:5-19 | Same. Mailbox fact and inventory scope kept | Yes |
| docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md:21-32 | Same. Mailbox boundary pointer kept | Yes |
| docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md:36-42 | "gPTP progress does too, until F6." The paragraph is split for style, content otherwise kept | No, sweep |
| docs/GLOSSARY.md:29 | AECP/AEM: after the switch-over, firmware serves it | Yes |
| docs/GLOSSARY.md:45 | gPTP: sole product owner until F6; firmware then owns protocol and servo | No, sweep |
| AB:219-220 | "All-fabric remains the current shipping default until the flip." "After the flip, no all-fabric build remains." | Yes |
| AB, "Unqualified functions retain fabric placement." | Removed: the wording SPLIT removed; the flip only happens once all are qualified | No, sweep |
| docs/design/MAAP_FABRIC.md, docs/fpga/DATAPLANE_WALKTHROUGH.md, docs/fpga/FPGA_DESIGN.md, docs/litex/LITEX_SOC.md, docs/overview/SYSTEM_DOMAIN_MAP.md, docs/traceability/ieee8021q.md, each :4-8 | The one-line pointer: "It stays the shipping default until F2 to F5 acceptance." and "The split contract defines the transition and end state." The acceptance line is kept | Yes |
| docs/traceability/ieee8021q.md:38 | "Mark II moves reservation to firmware after the switch-over." replaces "permits firmware placement" | No, sweep |
| docs/ENDSTATION_BUILDER.md:3-7 | Pointer replaces "adds selectable control placement" | No, sweep |
| docs/integration/INTEGRATION_GUIDE.md:5-6 | Pointer; "It preserves media interfaces, and gPTP interfaces until F6." | No, sweep |
| docs/design/GPTP_PLANE.md:6-7 | "Fabric gPTP owns product time synchronization until F6." plus a pointer | No, sweep |

## Sweep: what I left, and why

| Where | Text | Why it stays |
|---|---|---|
| docs/history/**, docs/findings/**, CHANGELOG.md | 60 percent, 38,040, sole owner | Dated records |
| AP:67, AP:712, AP:1465, AP:1579, AP:1594 | 60 percent; unqualified functions; gPTP remains fabric; 38,040 | The charter's own page, and all but AP:67 sit under its marked "Mark I plan history" (AP:316). The assignment leaves it unchanged |
| docs/design/MAILBOX_SPLIT.md:12-15, :439 | Mark II default; shipping placement unchanged | Bounded "until F2 to F5 acceptance", already points at the contract |
| docs/reference/MILAN_COMPLIANCE_MATRIX.md:5-6 | "each selected control owner before the default changes" | Bounded, and true before the switch |
| AB:228, AB:412 and the ledger rows | "either placement", "remains the shipping default", M-lane and partial-flip estimates | Inside the marked Mark I section, and true before the flip |
| docs/overview/FULL_FPGA_SOLUTION.md:104, docs/traceability/ieee8021q.md:115 | "both placements" | True until the switch-over; audio stays in fabric after it |
| docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md:44 | "Selected firmware control protocols" | An obligation on firmware protocols, not a retained option |
| docs/GLOSSARY.md:28, :30, :31 | "implemented by the protocol processor"; "currently" | Today's facts, with no Mark II claim |
| docs/design/GPTP_PLANE.md:22 | Contents line "only product time owner" | Generated contents; the page's first line now scopes it |
| docs/reference/REGISTER_MAP.md:293 | "the sole product owner" | The entry for VERSION 0x0056, dated, on a gate-read page |
| docs/litex/LITEX_SOC.md:119, docs/integration/BUILDING.md:253, docs/integration/BAREMETAL_FIRMWARE.md:116 | `--fabric-gptp`; fabric time plane | The current option and recipes |
| docs/guides/SYSTEM_INTEGRATOR.md:95 | "gPTP remains independent from entity enablement" | About enablement, not placement |
| docs/guides/gptp/TEST_DEVELOPER.md:26 | "C firmware never judges gPTP correctness" | About today's test judge |
| README.md:146, sw/firmware/**/README.md | "selected owner's"; "split placement"; "later default flip" | Today's facts; no permanent option stated |

The docs tree outside these has no line that makes the claim. The full output is evidence/f1_wide.txt, evidence/f2_wide.txt (both before the edits) and evidence/searches_at_head.txt.

## Residue

| Item | Closed by |
|---|---|
| R758-8-R1 | SE:450-453, the review's exact three sentences. Two paragraphs, for the two-sentence limit |
| R758-8-R2 | AP:60, AP:255, PR body line "With fewer reservations some cases exceed it, and no maximum is derived" |

Beyond the review's three lines, I made the PR body's Key results and known limitation say "some cases" too, because they read the same way. The Round 9 section says so.

Not taken: R757-8-R1 (the 96 kHz row, and the PR body's Round 8 row), R757-8-R2, R757-9 S1 and S2, R757-7 RR13, and the earlier optional items. The assignment names only R758-8's residue. R758-8-R1 overlaps R757-8-R1 for the 192 kHz row, not the 96 kHz row.

## Decisions taken inside the assignment

- **The AB target row names both bounds.** FR:473 gives two: Mark II fewer than 20,000, and the shipping image must fit. A row naming only the first would show the shipping image failing a bound it does not have.
- **Column headers carry "replaced", and no cell moves.** The cells are derived from 38,040, so they are correct as history.
- **"until F6" on interfaces and progress is my reading.** INTEGRATION_GUIDE:6 and AXIS_CORES:42 rest on REQUIREMENTS.md:36-37 and SPLIT. Firmware owns the protocol and servo after F6, so neither claim holds past it unchanged.

## Open points for the manager

- **Exact-head long gates now apply** (see "Read this first").
- **D8 is not restated for the new ceiling.** AB:400-402 keeps "requires at least 1 percent planning margin" and marks 37,659 as the replaced target's. No page says whether a 1 percent margin applies to 20,000 LUTs. No decision on it is in this round's sources, so I wrote none.
- **Daily area measurement.** R757-9 notes its column "Against the 38,040 LUT floor (NFR-RES-01, 60 %)" no longer matches after merge. It is outside this repository's pages.
- The R757 and R758 ledgers must be re-covered at this head: the delta touches the Conformance and Docs scopes. No RTL, firmware, generator, gate or configuration file changed.
- The owner-approval question R757-9 carries from R758-8 is unchanged: FR_NFR.md is not touched by this round.

## Finding closure

| Item | Closed by | Verification |
|---|---|---|
| R757-9-F1 | Commit 1 | Search 1 at head finds every 38,040, 37,659, 13,972 and 10,521 in AB only in a passage marked as replaced; documentation gates pass |
| R757-9-F2 | Commit 2 | Search 2 at head finds no line calling Mark II permanently selectable or keeping gPTP in fabric after F6, outside the marked AP history; style gate passes |

## Gate table

Every step of `.github/workflows/docs.yml` was run as its jobs run it, sequentially (no parallel sweeps), on $VALIDATION_STORAGE/640-a720i/gates/wt at d63b378d27c1c663034744a5b48a99c190271f58 (tree 1a46d16e), a fresh clean clone of the lane with the four submodules the jobs fetch (gptp-processor 135afd04, protocol-processor a9e84b66, tsn-c-stack 70936b77, verilog-axis 48ff7a7e, copied from round 8's scratch clone, each origin its .gitmodules URL). Gate venv: round 8's, copied. The pinned RV32 SDK was installed fresh into this lane's scratch HOME ("SDK fresh installation: verified"); the shared SDK was not touched. dev is unchanged since round 8's base, so the workflow is too. After the run the clone's status was empty and its gitlinks unchanged. All 50 rc files read 0. Logs and rc files: ./evidence/gates/.

{table}
Notes:
- The 16 NOT RUN arms of leg 1 are the same as round 8's: 15 need an interpreter that imports migen, litex and litex_boards, which the docs workflow never installs, and gate 11 needs a local Arty build report. Each leg's rc is 0.
- docs-check "Require every gate exactly once" verifies the uploaded CI receipts and runs only on GitHub; ci-manifest, ci-fail-fast and ci-cancel-tail are CI orchestration. None was run locally. act was not used: it needs a pushed head, and this lane pushes nothing.
- Not in the docs workflow, run as this page's reader: `pp_resource_gate.py check-baseline`, rc 0, "baseline PASS: 3 endpoints".
- /tmp: the gate run's TMPDIR pointed at scratch. A few quick checks in the lane before the run did not set it. `find /tmp -newer run_all.start` lists files from other sessions on this busy host, such as r741*; none is named by this lane's scripts or logs, and I cannot attribute each one by that listing alone.

## Evidence (./evidence)

| File | What |
|---|---|
| taken.md, review_ready_posted.md | The TAKEN and REVIEW READY texts as posted |
| edit_f1.py, edit_f2.py | The exact-text edits behind commits 1 and 2 |
| reviewer_stale_contract_search_r757-9.txt | The review's receipt, copied |
| f1_wide.txt, f2_wide.txt | My wide searches before the edits |
| searches_at_head.txt | The searches re-run at d63b378d |
| scope_and_gate_read.txt | ci_scope at both heads, check-baseline, policy-table digests, non-Markdown figure search |
| style_touched.py, style_touched.log | check_doc_style's analyze() over every changed block of the 21 pages against 1f29f189: 0 findings |
| make_pr_body.py, write_handoff.py | Build PR-BODY.md and this file |
| gates/ | Every gate step's log and rc at the head, run_all.out, run_all.sh, run_gates.sh; LARGE_LOGS.txt holds the one log over 200 KB by digest and size |
| SHA256SUMS | Digests of every file above |

## Not done / not allowed

No push, PR edit, merge to dev, rebase, sub-agent, bench, flashing or Vivado. No RTL, firmware, generator, gate or configuration change. No existing comment edited. R757-9 was read as the review of head 6c7c0947, a candidate whose tree equals 20933ef4; that commit is not in this clone.
"""
open(O + "HANDOFF.md", "w", encoding="utf-8").write(text)
