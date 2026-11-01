[R758] POSITIVE - exact head c576fe540838c353a1cfc9455a6b89eff2b77ffc

# R758-11: external review of PR #828 (issue #640), round 10 delta

Tree `5936f42145c658cd9d939b6d33c9610235897c21`. Delta `d63b378d..c576fe54`: one one-line commit, four Markdown pages, 14 insertions and 9 deletions, no other file. Source base and live dev are both `1f29f189`.

**Result:** no BLOCKER, MAJOR or MINOR. R757-10-F1 and R758-10-R1 to R4 are resolved at their cause. This round adds four RESIDUE items and one SUGGESTION, and retains the earlier items listed below.

This is not a merge clearance on its own. The exact-head hosted gates had not finished at my snapshot (see "Pending manager duties").

Abbreviations: AB = `docs/design/AREA_BUDGET.md`, MS = `docs/design/MAILBOX_SPLIT.md`, MG = `docs/guides/gptp/MANAGER.md`, Q = `docs/traceability/ieee8021q.md`, FR = `docs/reference/FR_NFR.md`, SPLIT = `docs/ARCHITECTURE_HW_SW_SPLIT.md`.

## The named checks

| Item | Check | Result | Evidence |
|---|---|---|---|
| R757-10-F1 MINOR | MS bounds the gPTP plane at F6 | **Resolved**, the finding's suggested text | MS:42-44 against `REQUIREMENTS.md:36-37,43` and SPLIT:51,115. "Framing and timestamps" stay with the fabric, which matches `REQUIREMENTS.md:37`. |
| R758-10-R1 RESIDUE | The MRP text continues the Reservation bullet, and the Mark II sentences are their own paragraph | **Resolved** | Rendered with the pinned renderer: a list of two items, the second holding MRP-1, then a paragraph with the two Mark II sentences (`receipts/probe_delta.txt`, P4). "Splits cleanly in two" is true again. |
| R758-10-R2 RESIDUE | AB:130, 140 and 180 say "at 32x32" | **Resolved**, the exact three texts | Diff; FR:473 |
| R758-10-R3 RESIDUE | "The next three sentences are history" | **Resolved**, the exact text, and the count is right | P4 lists the three sentences at AB:183-186. AB:188 onward is current text. |
| R758-10-R4 RESIDUE | MG is scoped to the fabric plane until F6, with the split contract linked | **Resolved**, with shorter text than proposed | MG:8-9. The proposed text has 12 words and the gate's limit is 10 (P1 refuses it). Appending to the "Use this page" paragraph is refused too (P2). The control passes (P3), so the shortening and the separate paragraph were both needed. The link resolves, and SPLIT:332 defines the transition. |
| Nothing else changed | Only the four pages, modes unchanged, no figure, no gitlink | **Holds** | `receipts/delta_and_retained.txt`; `receipts/verify_restore.txt` |

Figures on the touched lines are unchanged: 52,012 - 38,040 = 13,972; 13,972 / 24,493 = 57 %; 24,493 - 13,972 = 10,521; 20,000 / 63,400 = 31.5 %. No stale-placement sweep was run, as ruled.

## Evidence

- **Packet.** `author-r10/HANDOFF.md` and `author-r10/PR-BODY.md` at evidence commit `a7e4faac` match their `MANIFEST.json` hashes (`receipts/packet_hashes.txt`). The live PR body differs from the packet copy only by the trailing newline my capture added.
- **Gates, re-run at this head.** All rc 0 (`receipts/gates/`): `check_doc_style.py`, `docs_check.py`, `check_gptp_docs.py`, `gen_toc.py --check`, `check_em_dash.py --base 1f29f189`, `check_feature_status.py`, `check_doc_paths.py`, `check_baremetal_only.py --check`, `syn/ooc/pp_resource_gate.py check-baseline` and `git diff --check`.
- **The mailbox page's reader.** Running `ctrl_service_bounds.py` does not exercise anything (see R758-11-R2). So I called `arm_service_bounds` directly, compiled against the pinned tsn-c-stack. It read MS at this head: 47 checks, 0 failures, 38/38 planted controls caught (`receipts/gates/service_bounds_arm.log`).
- **Comment rule.** The delta has no source file, so it adds no source comment.
- **Commit form.** The message is one line with no trailer (`receipts/verify_restore.txt`).

## Findings

### R758-11-R1 RESIDUE - Docs - `author-r10/PR-BODY.md` and the live PR body, lines 14-15, 24, 26, 220, 298 - the PR body stops at round 9

- **Evidence:** the only r9-to-r10 change is the first line, `[A720i, A10]`. The status line and the gate record still name head `d63b378d`, and there is no Round 10 entry. Both statements are true of that head, so no claim is false.
- **Impact:** a cold reader of the PR body cannot see the round 10 change or its gates without the packet handoff.
- **Exact fix:** add to the contents "**[Round 10](#round-10)** -- The gPTP plane bounded at F6 on the mailbox split page, and the last review's wording fixes." Add a `## Round 10` section with the handoff's table and gate line, naming head `c576fe540838c353a1cfc9455a6b89eff2b77ffc`. Update the status line's head once the exact-head evidence is in.
- **Verification:** read the PR body.

### R758-11-R2 RESIDUE - Tests, Docs - `author-r10/HANDOFF.md` gate line - `ctrl_service_bounds.py` is listed as a gate with rc 0, but the file has no entry point

- **Evidence:** `sw/firmware/ctrl/test/ctrl_service_bounds.py` defines `arm_service_bounds` and has no `__main__`. With its imports on the path it exits 0 with no output and reads nothing (`receipts/gates/ctrl_service_bounds_bare_file.log`). Without them it fails on `import fw_gtest`. I cannot tell from public state how the author ran it.
- **Why RESIDUE:** the handoff's description changes no result. The real arm passes at this head (above), and `test_ctrl_firmware.py:162` runs it in the `firmware-unit` job.
- **Impact:** a later reader could copy the bare command and take a silent exit 0 as proof that the page was read.
- **Exact fix:** in the handoff, replace `ctrl_service_bounds.py` with "`arm_service_bounds` (through `test_ctrl_firmware.py`, job `firmware-unit`)".
- **Verification:** the arm's log prints `checks: 47   failures: 0`.

### R758-11-R3 RESIDUE - Docs - `author-r10/HANDOFF.md` first line - "13 lines added"

- **Evidence:** `git diff --numstat` gives 14 insertions and 9 deletions (4+3+3+4).
- **Exact fix:** "14 lines added, 9 removed".

### R758-11-R4 RESIDUE, for #495 - Docs, Conformance - MS:56, MS:134 - the event source has no F6 bound

- **Evidence:** I saw this while reading MS around the F1 change, not through a search. MS:134 reads "grandmaster change published by the gPTP plane", and the node at MS:56 reads "gPTP plane: grandmaster change". After F6 the plane is gone (SPLIT:115, 227). MS:43 now states the bound once for the whole page, so a reader is no longer misled about ownership.
- **Exact fix:** MS:134: "grandmaster change published by the gPTP plane until F6". Leave the figure node as it is.
- **Disposition:** the sweep is closed by ruling, so this goes to #495.

### R758-11-S1 SUGGESTION - Docs - MS:43-44 - line wrap

The new sentence leaves "The two exchange" short at MS:44, before the rest of its sentence on MS:45. Reflowing the paragraph would tidy the source. The rendered page is not affected.

## Prior findings

My diff pass and first gate run came before I opened any prior report (see the first limit).

| Finding | State at this head | Evidence |
|---|---|---|
| R757-10-F1 MINOR | **Resolved** | MS:42-44 |
| R757-10-R1 RESIDUE | **Resolved**, same item as R758-10-R1 | P4 |
| R757-10-R2 RESIDUE | **Partly resolved.** The shape was added. **Retained:** AB:129 still says "accepted headroom target", and AB:180 has no "fitting Block RAM". Keep the `#headroom-target` heading. | AB:129, 180; FR:473 |
| R757-10-R3 RESIDUE | **Retained**, not taken | MS:13 "defines the Mark II default"; `docs/findings/README.md:26` "a tenth of the NFR-RES-01 gap" |
| R757-10-S1 SUGGESTION | **Retained**, optional | Delta does not touch either file |
| R758-10-R1 to R4 RESIDUE | **Resolved** | Named checks above |
| R758-10-S1 SUGGESTION | **Retained**, optional | PR body line 24 still says "documentation only" |
| R757-8-R1 (96 kHz row), R757-8-R2 RESIDUE | **Retained** | PR body line 233; FR:306 still reads "that derivation" |
| R757-7 RR13 RESIDUE | **Retained**, the manager's | The #640 acceptance still reads "Every talker stream meets the 65 µs target" |
| R757-9 S1, S2; R757-8 S1-S5; R758-8 S1, S2; earlier optional items | **Retained**, optional, not re-judged | Delta does not touch them |
| Earlier MINOR and higher findings | Stay resolved | The delta changes nothing they depend on |

## Lens results

```text
[R758] PASS Conformance - MS:42-44; REQUIREMENTS.md:36-37,43; SPLIT:51,115,332; FR:473; AB:130,140,180; Q:35-45 - each changed sentence read against its clause; F1 resolved; retained residue and R758-11-R4 recorded
[R758] PASS RTL - receipts/delta_and_retained.txt; receipts/verify_restore.txt - no HDL, register, generator or constraint file in the delta and no gitlink change against the base; earlier RTL verdicts depend on nothing the delta changed
[R758] PASS Robustness - receipts/delta_and_retained.txt; receipts/gates/pp_resource_gate.log; receipts/gates/service_bounds_arm.log - no runtime path changed; both gate readers of the changed pages pass, the AB:140 row edit leaves check-baseline passing, and the MS reader catches 38/38 planted controls
[R758] PASS Tests - receipts/gates/; receipts/probe_delta.txt; receipts/gates/service_bounds_arm.log - no test in the delta; 10 gates plus git diff --check rc 0; the style gate refuses both planted texts and passes the control; residue R758-11-R2 recorded
[R758] PASS Docs - the four delta pages at this head; receipts/probe_delta.txt; author-r10/HANDOFF.md; author-r10/PR-BODY.md - F1 and R1 to R4 checked at their lines and in rendered form; residue R758-11-R1 to R4 and S1 recorded with exact fixes
```

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN, residue R4 and retained items | MS:42-44, 56, 134; `REQUIREMENTS.md:36-37,43`; SPLIT:51,115,227,332; FR:473; AB:129-140,179-186; Q:35-45 | R758-11 | c576fe540838c353a1cfc9455a6b89eff2b77ffc |
| RTL | CLEAN | Delta path list; modes; six gitlinks against the base | R758-11 for the delta; earlier RTL verdicts carried, nothing they depend on changed | c576fe540838c353a1cfc9455a6b89eff2b77ffc |
| Robustness | CLEAN | Delta path list; `check-baseline`; `arm_service_bounds` planted controls | R758-11 for the delta; earlier verdicts carried, no runtime path changed | c576fe540838c353a1cfc9455a6b89eff2b77ffc |
| Tests | CLEAN, residue R2 | `receipts/gates/`; `receipts/probe_delta.txt`; `ctrl_service_bounds.py`; `test_ctrl_firmware.py:162` | R758-11 | c576fe540838c353a1cfc9455a6b89eff2b77ffc |
| Docs | CLEAN, residue R1 to R4, S1 and retained items | AB; MS; MG; Q; packet handoff; PR body | R758-11 | c576fe540838c353a1cfc9455a6b89eff2b77ffc |

## Real limits

- **Order of work.** I froze no draft verdict before opening prior reports. The diff pass and the first gate run came first. The style-gate probes, the render check and the reader arm ran after I had read the prior findings, because they test those findings' fixes.
- **Packet integrity.** Evidence commit `a7e4faac` and head `c576fe54` are both reported unsigned by the host. I verified the packet by hash against the manifest in that commit, so this shows consistency within that commit and does not establish who created it.
- **Scope.** By the assignment I read the delta and the author-r10 packet. I did not run a tree-wide search, and I did not re-read pages or RTL outside the delta. Lens verdicts outside the delta are carried from earlier rounds.
- **Not run.** No parent, processor, gPTP, Yosys or builder bank, no hardware, no local CI replica. The submodules are not initialized in this clone. Only tsn-c-stack was fetched, at its gitlink and into scratch, for the reader arm. Physical calibration is NOT RUN and field skips are not hardware proof.
- **Renderer.** The two renderer-dependent gates ran with the hash-pinned packages from `tools/markdown/requirements.txt`, installed under scratch only.
- **Concurrent internal review.** R757-11 started at the same head. I have not read it.
- **Clone state.** Exact-head bytes, modes, index and gitlinks are verified, with no untracked or ignored entry left (`receipts/verify_restore.txt`).

## Pending manager duties

- **Hosted evidence.** At 23:14 CET, the exact-head snapshot (`receipts/hosted_snapshot.txt`) showed these contexts complete and successful: `changes`, `full-ci-gate`, `docs-check-no-git`, `wire-accountability`, `bdd-conformance`, `verilator-lint`, `firmware-aecp-mutants` and both `Prepare pinned Yosys` jobs. `Physical gPTP` was SKIPPED. The Verilator and Yosys shards, the docs and elaborate gates and the other firmware jobs were queued or in progress. None of these is evidence until it concludes at this head.
- **Local records.** The long-gate and local replica duties carried from R758-10 still apply at this head or at the merge candidate.
- **Merge candidate.** Build and validate the current-dev candidate at the merge turn and link its receipts on the PR. No manager source bank is claimed or inferred here.
- **Residue checklist.** Carry R758-11-R1 to R3, R4 (to #495), R757-10-R2's remainder, R757-10-R3, R757-8-R1, R757-8-R2 and RR13.
- **Owner questions, carried unchanged.** Whether D8's 1 percent margin applies to the 20,000-LUT ceiling (AB:400-402), and whether the owner's approval of the requirement text needs restating for NFR-LAT-03.
- **Outside this repository.** The daily area measurement's column "Against the 38,040 LUT floor" no longer matches after merge.

R758-11 FINISHED
