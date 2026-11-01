# HANDOFF - [A720d] issue #640 Mark II charter, round 4 (docs only)

Status: REVIEW READY at head 22f3cedb420992b7b776c5a842b0b210ac4191d3 (2026-11-01). Every docs-workflow gate step rc 0 on a clean clone of that head; `git diff --check 1f29f189 HEAD` rc 0. Local only, nothing pushed.

- Lane: $LANES/640-mark2-charter, branch 640-mark2-charter. Round-3 head 69fd18f1d8f9d428687c07ede0f9c14597cf2d61 (PR #828). Round-4 head 22f3cedb420992b7b776c5a842b0b210ac4191d3, tree aa3a82eae97231e462c5482c3d1f00a50b183004.
- Base: live dev 1f29f189279f9fc0132f4918e47342b87d22f33a (fetched 08:07 CET, unchanged since round 3 saw it), merged in by `git merge --no-ff origin/dev`; the merge base is now 1f29f189. Round 4 adds 152 lines and removes 32 over 3 pages (69fd18f1..2322c6d7); against 1f29f189 the PR adds 1,778 and removes 112 over 7 pages.
- Remote checked: https://github.com/kebag-logic/milan-fpga.git
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6554582319 (text: evidence/taken_posted.md)
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6555289214 (text: evidence/review_ready_posted.md)
- Reviews answered: R757-3 (PR #828 issuecomment-6554560197) and R758-3 (issuecomment-6554550201), both read in full.
- Decisions re-read: #640, #665 and #823 bodies and comments fetched 07:47 CET; no owner comment after 2026-10-31 (the 2026-11-01 comments are lane TAKEN/STOP/REVIEW READY posts, two manager rulings on #665 about the dev-soft-core sync, and the daily area measurement, none of which touches this charter).
- Scratch: $VALIDATION_STORAGE/640-a720d (models, gate clone, gate venv copied from round 3, a fresh scratch HOME for the pinned SDK). Evidence (small files): ./evidence/.

## Commits (one per finding group, one-line subjects, no body, no trailers)

| # | SHA | Files | Finding group |
|---|---|---|---|
| 1 | 309bfebc80ff1004bdacf2e824493dda99411def | SE, FR | R757-3-N4, R758-3-F3 (header read-back); R757-3 RR3 |
| 2 | 4d75675fa76e4d3ec16e161d86a2653f4bcec172 | SE | R757-3-N5 (conversion error); suggestion R758-3 S2 |
| 3 | 0f6ab84bd8926ba74b692771858bb6f8adb02347 | SE | R758-3-F1, F2 (merge rules); R757-3 RR4 |
| 4 | 2405f2be0b310f625f41430c3eb4e112e09ccce8 | SE, AP | R758-3-R1 |
| 5 | b4b719ea3823dc9f607ed91fdcef9b9bb3e24460 | SE | Suggestions R758-3 S1, R757-3 S3 |
| 6 | 2322c6d7be679f50f584d97a1135bff29ed4f91d | SE | Group 3 follow-up: only a jump out of the span leaves tu copies unplaced; a restart inside the span is open design item 2 |
| 7 | 22f3cedb420992b7b776c5a842b0b210ac4191d3 | merge | `Merge dev 1f29f189 into 640-mark2-charter` |

`SE` = docs/design/MARK_II_STREAM_ENGINES.md, `AP` = docs/design/MARK_II_AREA_PLAN.md, `FR` = docs/reference/FR_NFR.md. No rebase, no amend; nothing pushed. One local reset: a first dev merge (3556306017, made at 08:07 and never pushed) was dropped with `git reset --hard b4b719ea` so that commit 6 could land before the merge; the merge was redone after commit 6 with the same dev parent and subject.

## Finding closure (file:line at 22f3cedb, then verification)

### R757-3-N4, R758-3-F3: a header that fails its read-back (commit 1)

| Change, file:line | Source |
|---|---|
| SE:1101-1125 new "A header that fails its read-back": a read-back can fail on an intact header, which boot would then prefer (SE:1103-1104); saves keep waiting and the writer zeroes that page, a program only clears bits (SE:1106-1107, N25Q128 5.1.2: "changing bits from '1' to '0'"); #823's header format must make an all-zero header fail its check (SE:1109-1110); a zeroed page that fails its read-back too: the writer erases the header's sector, saves still held, a reported double fault outside the bound (SE:1112-1115); saves resume, on the old slot, once the header reads back zeroed or erased (SE:1117-1118); compaction then erases the standby and restarts from step 1 (SE:1120); a waiting save waits one more page, 365.10 ms, within 0.5 s (SE:1122-1125) | R757-3 required outcome ("making the header invalid first is one way"; "even a second page wait would give 365.10 ms"); R758-3 required outcome (program the check field so it never checks) |
| SE:1146 landing row: "Nothing until the header reads back zeroed or erased; then the old slot, still active"; SE:1147 the following row now reads "After a header that passes its read-back" | The finding's row SE:1038 at 69fd18f1 |
| SE:1153 RR3 exactly as written; SE:1154 new power-cut row "After a failed header read-back, until the header reads back zeroed or erased: Either slot"; SE:1155 new row "After that, during the standby's erase: The old slot"; SE:1156 "After a header that passes its read-back" | R757-3 RR3; both findings' "power-cut table gains the interval" |
| SE:1224 verification row adds a header that programs intact or torn and fails its read-back, its zeroing passing or failing, then a save, cuts before and after the standby's header sector is erased, and "fails if a save appends to the old slot before a failed header reads back zeroed or erased" | Both findings |
| FR:476 NFR-REL-03 verification: "a header that programs intact but fails its read-back followed by a save, and a power cut ... including before and after the standby's header sector is erased" | Both findings |
| SE:1008 "A record page failing read-back is rewritten further on." (was "A page ..."), so the record-page retry is not read as covering the header | Clarity, same commit |

Verification: host flash model `evidence/model/compaction_model.py` (round 4; the round-3 model extended). Every save boundary (12), a second save at each, with and without a save during the header page, and a power cut before, inside and after every page and erase step, for four header read-back cases: passes (14,831 runs, identical to round 3), fails with an intact header (22,943), fails with a torn header (22,943), fails with an intact header whose zeroing sticks and fails its read-back (23,957): 84,674 runs, 0 lose a change. The reviewers' sequence (intact header, failed read-back, the waiting save acknowledged, then a cut before or after each later operation, both halves of the standby erase included): 18 cuts after the acknowledgement, 0 boot without the save. Mutations: `no_invalidate` (the round-3 row) loses changes in 1,214 of 21,929 runs, first at a cut before the standby erase, and in the reviewers' sequence boots the new slot without the save; `ignore_zero_rb` loses 1,214 of 22,943; `split` 733 and `no_replay` 2,704 as in round 3.

Open point for the reviewers: in the double fault (the zeroed header also fails its read-back) saves wait for the header sector's erase. That is a reported fault path outside the bound, as the record-page retry has been since round 1 (SE:1008-1009); I read NFR-REL-03's "No flash erase may sit on the save path" as the fault-free path. If a reviewer reads it otherwise, the alternative is to repeat the zeroing (a program, not an erase) and report a flash failure while saves wait.

### R757-3-N5: conversion-error drift (commit 2)

| Change, file:line | Source |
|---|---|
| SE:538-539 "Read together, the offsets differ by at most 2 µs." (the B.3 term at one instant) | Unchanged reading of IEEE 802.1AS-2020 B.3 |
| SE:544-548 the offset drifts at most 200 ppm (B.1.1); talker and listener latch it at different instants; the talker latches at most 125 µs before stamping; the listener latches before the copy arrives | R757-3-N5 required outcome |
| SE:550-554 a rendered copy arrives before its presentation time (rule 1), at most capture plus offset plus 125 µs (Milan v1.2 5.3.7.6: "adds some fixed delay value (between 0 and 125 microseconds)"); the stamp comes after the capture it reads | Milan v1.2 5.3.7.6 |
| SE:556-560 Assumption A4: arrival within 2.792 ms of stamping; offsets up to the 2.667 ms span meet it; a larger offset needs queueing and transit within it; class A transit 2 ms (IEEE 802.1BA-2011 6.5, Table 6-2) | IEEE 802.1BA-2011 6.5 |
| SE:562-563 so the latches lie at most 2.917 ms apart; the drift term covers that whole interval | R757-3-N5 |
| SE:568-569 the capture stamp and the render point add no term: one reading serves both copies or both compared sides | Suggestion R758-3 S2 |
| SE:571-577 E_x block: latch to latch <= 125 µs + 2.792 ms = 2.917 ms; 200 ppm x 2.917 ms = 0.5834 µs; E_x = 2.000 + 0.584 + 0.160 = 2.744 µs | Derivation below |
| SE:604 "Clean partner copies differ by at most 2.744 µs."; SE:1219 merge row "jittered conversion error up to 2.744 µs"; SE:1220 conversion row: analysis cites B.1.1, B.1.2, B.3, Milan v1.2 5.3.7.6, A3 and A4, plus a host model that drifts two PHCs; bench: stamp to arrival within 2.792 ms, converted times within 2.744 µs | R757-3-N5 ("SE:582, SE:1109-1110 and the PR body carry the new figure") |

Verification: the window argument (SE:603-609) re-checked: 62.5 µs > 2.744 + 0.55 µs (22 packets at 200 ppm); neighbours stay at least 125 - 0.55 - 2.744 = 121.7 µs apart, above 62.5 µs. `evidence/model/conversion_error.py` derives the error instead of injecting it (suggestion R757-3 S2): two grandmasters at plus and minus 100 ppm, plus and minus 1 µs per network, 40 ns read truncation, talker and listener latch ages over [0, 125) µs, stamp to arrival up to 2.792 ms; 201,280 adversarial and random cases; largest latch separation 2,916.999 µs (bound 2,917 µs); worst error 2.640 µs, within 2.744 µs and above the round-3 2.210 µs. The round-3 merge model, unchanged but for its injected bound, passes all 15 cases at plus and minus 2.744 µs (`evidence/model/merge_model_r3_ex2744.out`). `grep -n '2\.210'` on the four Mark II pages: no hit.

### R758-3-F1: tu on both networks (commit 3)

| Change, file:line | Source |
|---|---|
| SE:648 rule 2: discarded only while a clean partner copy of its packet can still come: the partner's newest copy was clean (`LAST_TU` clear), `CLEAN_VALID` with `LCTX_CLEAN_PT` ahead of the render point, and either that time precedes this copy's counted packet by more than 62.5 µs or this copy has no valid reference | R758-3-F1 required outcome ("any rule that makes both-tu render is acceptable") |
| SE:662-663 "No tu copy writes while its clean partner may come. So uncertain time on one network cannot disturb the other." | Replaces "while clean partner data remains" |
| SE:675 every copy passing rule 1 updates its reference and `LAST_TU`; SE:886 new `LCTX_STATE` bit 12 `LAST_TU` (R, reset 0), SE:887 reserved 31:13 | Register map, TI style |
| SE:700-738 new "tu on both networks": a talker may set tu on both at once (SE:702-703); rule 2 waits only while the partner is still clean (SE:705-706); once the partner's newest copy has tu, rule 2 stops and each network's tu copies fill the other's gaps (SE:708-709); with both delivering, tu on both loses no sample (SE:711-712); placement by count follows IEEE 1722-2016 4.4.4.7; Milan v1.2 4.4.2.3's free-wheel after tu clears belongs to the media clock servo, not the merge (SE:714-718); the merge resumes placing clean copies by time, and a time step costs no more than on one network (SE:720-721); the gaps left: a network rejoining during tu has no reference and waits for a clean copy, its partner's losses unfilled (SE:723-727); a jump out of the span (SE:729-733, commit 6); an unpaired stream's gap of at most 22 packets (SE:735-736); "Like loss plus tu, these lie beyond Annex D.3" (SE:738) | Milan v1.2 4.4.2.3 ("should continue to let its media clock free-wheel for an appropriate amount of time"); IEEE 1722-2016 4.4.4.7 ("may stop attempting to correlate AVTP Presentation Time to gPTP time") |
| SE:1219 verification row adds tu on both (onsets together and 0.5 ms apart either way, skews of 5 and 200 µs, a period that ends, one to three packets), a time step as tu clears, and the bench row "tu set on both networks by one talker, both up, no lost samples"; the mutation "with rule 2 waiting on any clean partner data" | R758-3-F1 |

Verification: `evidence/model/merge_model.py` (round 4): "tu on both from packet 100, secondary 1.1-1.5 ms slower" missing 0 (R758's probe: 30); with skews of plus and minus 5 µs: 0; plus and minus 200 µs: 0; tu 100 to 600: 0; both at the primary's latency, onsets together: 0 (R758: 84); onsets 0.5 ms apart: 0 (R758: 60); the slower network's onset first: 0; tu on both for packet 100 only: 0; packets 100 to 102 with the secondary faster: 0. The one-network tu cases still pass (`SE_MERGE_TU` 3,900), so rule 2 still holds tu copies off a clean partner. Mutation `r3_rule2` (the round-3 rule) fails 13 cases. `evidence/model/probe_tu_step.py`: a time step of -1,000 to +1,000 µs as tu clears on both networks loses exactly what one network alone loses (-1,000 µs: 8 packets both; -300: 2; -100: 1; +100 and +300: 0), and at +1,000 µs the pair loses nothing where one network alone goes early.

### R758-3-F2: a tu copy far from the head (commits 3 and 6)

| Change, file:line | Source |
|---|---|
| SE:625-628 a tu copy must also land inside the render span; rule 4 checks its counted time for late and early; a copy counted outside the span is discarded, never written | R758-3-F2 required outcome ("discarding with its own count is another") |
| SE:649-650 rule 3 is "no valid head" only; new rule 4: a tu copy with no valid sequence reference, or whose counted packet fails the late or early check, is discarded ("no count can place it in the render span"), counted in `SE_MERGE_TU` | Same |
| SE:651-654 rules 5 to 8 renumbered (re-anchor, newer, older, duplicate); SE:671 "re-anchors by rule 5"; SE:808-810 `SE_MERGE_DUP` rule 8, `SE_MERGE_SEC` rules 3 and 5 to 7, `SE_MERGE_TU` rule 2 or rule 4; SE:883 `ANCHOR_TU` read by rule 5 | Consistency of every rule number (`grep -n 'rule [0-9]'`) |
| SE:660 "Rule 4 drops only tu copies no count can place."; SE:678 a tu copy with no valid reference cannot make one | Keeps R757-2 RR2 ("No rule drops the only valid copy of a packet", SE:659) true |
| SE:638-639 "No sample is written outside the render buffer. Open design item 1 covers its edges."; SE:1229-1236 new "Open design items", owned by lane 6 (linked to the area plan's lane sequence): item 1, the render-span edges (a packet crossing either end, a clean copy counted a sample behind the render point), with its simulation row | Manager convergence rule: the exact edge check is implementation detail |
| SE:729-733 (commit 6) only a jump out of the span leaves copies unplaced; smaller gaps are loss (IEEE 1722-2016 4.4.4.6); a restart inside the span is open design item 2 (SE:1237: no sample placed by a count across a talker restart; the lane picks the restart signal and drops the context's reference; simulation row) | My own round-4 sentence was too strong for jumps inside the span; fixed before the gates |

Verification: merge model cases "secondary tu from 100, its sequence jumps +40 / -40 at 1000, primary clean", "tu on both from 100, secondary sequence jumps +40 / -40", the same with the secondary faster, and "unpaired, tu from 100, sequence jumps +40 / -40": each writes 0 samples outside the render span (`outside` 0, checked at every write against the render point) and counts 0 jumped copies as duplicates (`jump_dup` 0); paired cases miss 0 samples; unpaired cases miss 84 samples (14 packets), within the stated 22. Mutation `no_rule4` (round 3's anchoring and no span check) fails 5 cases. A new check: in every case without loss or a cut, each packet's second copy is counted exactly once (`SE_MERGE_DUP` + `SE_MERGE_TU` + early + late = 4,000; the startup case, whose 10 tu-anchored packets are rewritten by the clean re-anchor, = 3,990). 33 cases pass; mutations `exact` 33, `own_time` 4, `no_rule2` 5, `r3_rule2` 13, `no_rule4` 5 cases.

### Residue

| Item | Change, file:line | Verification |
|---|---|---|
| R758-3-R1 | SE:1263 and AP:313 "Redundancy needs gPTP on both ports (#665 F6). One instance per port is one way." | The reviewer's exact words; the semicolon became a full stop because the sentence would be 15 words against the 10-word limit (`style_touched.py` finds 0) |
| R757-3 RR3 | SE:1153, exactly as written | Text compare with the finding |
| R757-3 RR4 | SE:1219 "`SE_MERGE_DUP` counts each packet's second copy once, or `SE_MERGE_TU` when rule 2 or rule 4 discards it" | As written, plus "or rule 4" because rule 4 is new this round; the model's count check above |

### Suggestions

| Item | Taken? | Where |
|---|---|---|
| R758-3 S1 | Taken | SE:1095-1096 the check is a cursor compare with no flash access, so no save is taken between it and the header |
| R758-3 S2 | Taken | SE:568-569 |
| R758-3 S3 (R758-2 S4 carried) | Not taken | Needs REQUIREMENTS.md text and owner approval; NFR-SCOUT-03 carries the obligation |
| R757-3 S1 | Not taken | It would change the talker's conversion design (take the odd copy's time from the port-1 stamp); the bound is restated for the design as written, and the merge window holds either way |
| R757-3 S2 | Taken | `evidence/model/conversion_error.py` |
| R757-3 S3 | Taken | SE:1140 landing row "While another save is in flight, at any step: The same slot, after that save" |

## Dev merge

- `git merge --no-ff origin/dev` (dev 1f29f189), subject "Merge dev 1f29f189 into 640-mark2-charter", no body. No conflict: dev's REQUIREMENTS.md line (REQUIREMENTS.md:472, "Each is the controller's AECP REBOOT of ENTITY 0 (IEEE 1722.1-2021 7.4.43, #787).") and docs/README.md row (docs/README.md:72, "Reset on an AECP REBOOT") sit in hunks this PR does not touch; both sides are kept.
- Scoping re-checked: dev's added REQUIREMENTS.md line names no placement. This PR's REQUIREMENTS.md scoping lists AECP among the control functions (REQUIREMENTS.md:25-26), build-selectable until the switch-over and firmware only after it (REQUIREMENTS.md:27-33), so the REBOOT soft reset is served by whichever AECP owner the image has. Nothing else dev added to REQUIREMENTS.md.
- For the manager (not changed here; docs-only scope and the posting rule allow no new issue): dev's docs/design/REBOOT_RESET.md:8 has the protocol processor answer REBOOT and raise `reboot_req_o`. After the switch-over the fabric processor is deleted, so the firmware AECP owner must raise the reboot request; lane 1 (switch-over) inherits that. The PR body lists it under known limitations.

## Derived numbers and derivations

### Conversion error (SE:530-577)

- Talker latch t_a: at most 125 µs before the stamp t_s, so t_a >= t_s - 125 µs. Listener latch t_b <= arrival t_r.
- A rendered copy passes the late check, so t_r <= presentation instant <= capture + offset + 125 µs (Milan v1.2 5.3.7.6), and t_s >= capture. So t_r - t_s <= offset + 125 µs, which is 2.792 ms for offsets up to the 2.667 ms render span: assumption A4.
- |t_b - t_a| <= 125 µs + 2.792 ms = 2.917 ms (the other side: t_a - t_b <= 125 µs).
- Drift: 200 ppm (two grandmasters at 100 ppm each, B.1.1) x 2.917 ms = 0.5834 µs, used as 0.584 µs.
- E_x = 2 x 1 µs (B.3, one per network) + 0.584 + 4 x 40 ns (B.1.2) = 2.744 µs. At Milan's 2 ms default offset the interval is 2.250 ms and E_x = 2.610 µs (not used on the page; shown for comparison with R757-3's 2.605 µs at 2.225 ms).

### Save with a failed header (SE:1122-1125)

- 359.75 ms (T_worst, unchanged) + one zeroing page 5.35 ms = 365.10 ms <= 500 ms. A zeroing that fails its read-back adds the header sector's erase (tSE at most 3 s, N25Q128 Table 32) with saves held: a reported double fault outside the bound.

### Unpaired gap after a jump (SE:735-736)

- The head is at most the 2.667 ms span ahead of the render point, so it lapses within 2.667 / 0.125 = 21.3 intervals of the last written packet; at most 22 packets (2.75 ms) are discarded before rule 3 anchors again. The model, at a 2 ms offset, loses 14 packets.

## Gate table

Every step of `.github/workflows/docs.yml` was run as its jobs run it, sequentially (no parallel sweeps), on $VALIDATION_STORAGE/640-a720d/gates/wt at 22f3cedb420992b7b776c5a842b0b210ac4191d3 (tree aa3a82ea), a fresh clean clone of the lane with the four submodules the jobs fetch (gptp-processor 135afd04, protocol-processor a9e84b66, tsn-c-stack 70936b77, verilog-axis 48ff7a7e, each cloned from round 3's scratch clone and its origin set to its .gitmodules URL, as the builder legs require). Gate venv: round 3's, copied. The pinned RV32 SDK was installed fresh into this lane's scratch HOME (downloaded and digest-checked by the installer; "SDK fresh installation: verified"); the shared SDK was not touched. dev's workflow is unchanged from round 3's base (`git diff e5b8405d 1f29f189 -- .github/` empty), so the step set is the same. After the run the clone's status was empty and its gitlinks unchanged. Logs and rc files: ./evidence/gates/ (the one log over 200 KB is listed with its digest in evidence/gates/LARGE_LOGS.txt); scripts run_all.sh and run_gates.sh beside them; summary run_all.out.

| Job | Step (workflow id) | Command | rc | Result |
|---|---|---|---:|---|
| wire-accountability | Advertised-vs-emitted gate | `check_wire_accountability.py --self-test` | 0 | RESULT: PASS |
| docs-check-no-git | Strip git metadata, then run the docs gate | `docs_check.py`, `check_feature_status.py` on `git archive HEAD` without .git | 0 | 0 findings |
| docs-gates-0 | gate_1 HDL reference | `gen_hdl_reference.py --selftest`; `--output` | 0 | index.html written |
| docs-gates-0 | gate_7 link health | `docs_check.py` | 0 | 0 findings, 213 md + 1436 scrubbed files |
| docs-gates-0 | gate_8 em dash | `check_em_dash.py --base 1f29f189` (merge base with live dev) | 0 | 0 findings over 1778 added lines in 7 pages |
| docs-gates-0 | gate_9 concise docs | `check_doc_style.py` (+ `--selftest`), `check_gptp_docs.py` (+ `--selftest`) | 0 | OK; 30 controls |
| docs-gates-0 | gate_10 diagram no-drift | `DOC_MAP.gen.py --check/--selftest`, `timesync_chain.gen.py --check/--selftest` | 0 | OK |
| docs-gates-0 | gate_11 solution docs | `check_solution_docs.py` (+ `--selftest`) | 0 | 45 controls |
| docs-gates-0 | gate_12 submodule docs | `submodule_boundaries.gen.py --check/--selftest`, `check_submodule_docs.py` (+ `--selftest`) | 0 | OK |
| docs-gates-0 | gate_13 WaveDrom | `gen_wavedrom.py --selftest` and the three `--check` runs | 0 | current |
| docs-gates-0 | gate_14 PNGs | `check_diagram_pngs.py` (+ `--selftest`) | 0 | 6 rasters, 28 controls |
| docs-gates-0 | gate_15 feature status | `check_feature_status.py --self-test` | 0 | 0 findings |
| docs-gates-0 | gate_16 traceability | `gen_module_matrix.py --check` | 0 | up to date, 80 modules |
| docs-gates-0 | gate_18 imported gPTP docs | `check_gptp_docs.py --with-submodule`; `make -C gptp-processor docs` | 0 | PASS |
| docs-gates-0 | gate_19 measurement self-tests | `measure_control_flow.py --selftest`, `measure_cohesion.py --selftest` | 0 | 18 PASS |
| docs-gates-0 | gate_21 bare-metal scope | `check_baremetal_only.py --check` and `--selftest` | 0 | 0 findings over 1434 files; 867 arms |
| docs-gates-0 | ci_step_28 RV32 SDK | `ci_rv32_sdk_selftest.py`; `ci_rv32_sdk.py --destination $HOME/br-milan-rv32/host` | 0 | SDK fresh installation: verified |
| docs-gates-0 | gate_24 compiler-absent controls | `test_firmware_compiler.py --selftest`; `--absent --audit` | 0 | GATE 1b PASS; 1 NOT RUN by design; 0 compiler invocations (674 s) |
| docs-gates-0 | gate_26 NVM record space | `check_nvm_record_space.py` (+ `--self-test`) | 0 | 0 findings, 5 configs |
| docs-gates-0 | gate_27 capture census | `check_nvm_capture.py` | 0 | PASS |
| docs-gates-0 | gate_28 saved-state writer | `test_nvm_firmware.py --self-test` | 0 | OK, 5 shapes |
| docs-gates-0 | gate_29 SoC sources | `check_soc_sources.py` (+ `--selftest`), `iob_pack_selftest.py` | 0 | 22 arms |
| docs-gates-0 | gate_30 RTL source lists | `check_rtl_source_lists.py` (+ `--selftest`) | 0 | 50 PASS |
| docs-gates-0 | gate_31 naming | `measure_naming.py --check/--selftest` | 0 | 66 PASS |
| docs-gates-0 | gate_32 port contracts | `check_port_contracts.py` (+ `--selftest`) | 0 | 82 PASS |
| docs-gates-0 | gate_33 fail-fast | `measure_fail_fast.py --check/--selftest` | 0 | 106 PASS |
| docs-gates-0 | gate_34 TODO ownership | `check_todo_ownership.py` (+ `--selftest`) | 0 | 45 PASS |
| docs-gates-0 | gate_35 test evidence | `measure_test_evidence.py --check/--selftest` | 0 | 105 PASS |
| docs-gates-0 | gate_36 hygiene | `check_hygiene.py --check/--selftest` | 0 | 35 PASS |
| docs-gates-0 | gate_37 to 40 idioms | `check_sv_idiom.py`, `check_cpp_idiom.py`, `check_py_idiom.py`, `check_sh_idiom.py` (+ `--selftest` each) | 0 | 55, 75, 54, 48 PASS |
| docs-gates-0 | gate_43 cited paths | `check_doc_paths.py` | 0 | 1084 paths resolve |
| docs-gates-0 | gate_44 archive | `check_archive.py` (+ `--selftest`) | 0 | OK, 24 controls |
| docs-gates-0 | gate_45 contents | `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0 | 152 pages; 578 cross-page links reproduced |
| docs-gates-0 | gate_46 to 49 | `gen_aem_store.py --self-test`, `check_sweep_shape.py`, `check_deploy_shape.py`, `check_entity_shape.py` (`--self-test`) | 0 | PASS |
| docs-gates-0 | gate_50 CI controls | `ci_gate_workflows.py --check` and the thirteen self-tests | 0 | PASS |
| docs-gates-1 | gate_25_0 builder leg 0 | `ci_builder_legs.py run 0 -- test_builder.py --require-rv32` | 0 | ALL GATES PASS (its 1 of 105 gates; 1127 s) |
| docs-gates-2 | gate_25_1 builder leg 1 | `ci_builder_legs.py run 1 -- test_builder.py --require-rv32` | 0 | ALL GATES PASS EXCEPT 16 NOT RUN (104 of 105) |
| docs-gates-2 | gate_41 CI events | `ci_events.py --check/--selftest` | 0 | 2199 items, 5258 arms |
| docs-gates-2 | gate_42 act runner contract | `act_ci.py --selftest`; installed copy `--selftest --worktree` | 0 | PASS |
| (lane) | Markdown gates, pinned venv $VALIDATION_STORAGE/818-mdvenv | `docs_check.py`; `check_em_dash.py --base 1f29f189`; `check_doc_style.py`; `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0 | same results as above |
| (lane) | whitespace | `git diff --check 1f29f189 HEAD` | 0 | no output |
| (lane) | style on touched pages | `style_touched.py` (check_doc_style's analyze()) over every changed block of the 7 pages against 1f29f189 | 0 | 0 findings |

Notes:
- The 16 NOT RUN arms of leg 1 are round 3's: 15 need an interpreter that imports migen, litex and litex_boards, which the docs workflow never installs, and gate 11 needs a local Arty build report. Leg 0 runs 1 of 105 gates by the leg split, as round 3's ran 1 of 103 (dev added two). Each leg's rc is 0; the verdict is judged on the union of the legs.
- docs-check "Require every gate exactly once" verifies the uploaded CI receipts and runs only on GitHub; ci-manifest, ci-fail-fast and ci-cancel-tail are CI orchestration. None was run locally. act was not used: it needs a pushed head, and this lane pushes nothing.
- Setup slip, no effect on the lane: the first submodule init in the scratch clone was refused (git forbids local file transport for submodules by default), and the follow-up `remote set-url` then ran in the scratch clone's superproject. That clone was deleted and recreated before any gate ran; the lane's own origin was checked unchanged (https://github.com/kebag-logic/milan-fpga.git).
- The models were run in this lane's scratch, before the gate run started, except one byte-for-byte reproduction check of three models (seconds) while chunk a of the gates ran.
- TMPDIR was not set for the gate run (as in round 3), so a tool that uses the system temporary directory may have used /tmp in passing. Nothing of this lane's remains there: `find /tmp -maxdepth 2 -user alex -newer run_all.sh` lists only the shell's own working-directory markers.

## Evidence (./evidence)

| File | What |
|---|---|
| model/compaction_model.py, .out | Host flash model of saves and compaction, round 4: four header read-back cases, 84,674 runs, the reviewers' sequence, four mutations |
| model/merge_model.py, .out | Listener merge rules, round 4: 33 cases, five mutations, the out-of-span write and jumped-duplicate checks |
| model/conversion_error.py, .out | Derives the cross-port conversion error from drifting PHCs: 201,280 cases, worst 2.640 µs |
| model/probe_tu_step.py, .out | A time step as tu clears on both networks against one network alone |
| model/merge_model_r3_ex2744.out | The round-3 merge model unchanged but for its injected bound, at 2.744 µs: 15 PASS |
| style_touched.py, style_touched.log | check_doc_style's analyze() over every changed block of the 7 touched pages against 1f29f189: 0 findings |
| taken_posted.md, review_ready_posted.md | The TAKEN and REVIEW READY texts as posted |
| gates/ | Every gate step's log and rc at 22f3cedb, run_all.out, run_all.sh, run_gates.sh; LARGE_LOGS.txt (gate_41_ci_events.log, 337,511 bytes, sha256 be0a6c1d2b39b849139381d0110abea6930832c139ed7334212c3580852c68d9) |
| SHA256SUMS | Digests of every file above |

Reproduce: `python3 -I compaction_model.py`, `python3 -I merge_model.py`, `python3 -I conversion_error.py`, `python3 -I probe_tu_step.py .` in evidence/model; each output above was reproduced byte for byte.

## Not done / not allowed

No push, PR edit, merge to dev, rebase, sub-agent, bench, flashing or Vivado. No RTL, firmware, generator, gate or configuration change. No existing comment edited. The shared RV32 SDK in the home directory was not touched.
