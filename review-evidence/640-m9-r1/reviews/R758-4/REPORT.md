[R758] NEGATIVE - exact head 22f3cedb420992b7b776c5a842b0b210ac4191d3

Round R758-4: external independent review of PR #828 (issue #640, with #665 and #823), round-4 delta.
- Head `22f3cedb420992b7b776c5a842b0b210ac4191d3`, tree `aa3a82eae97231e462c5482c3d1f00a50b183004`.
- Previous head `69fd18f1d8f9d428687c07ede0f9c14597cf2d61`. Merge base and live dev `1f29f189279f9fc0132f4918e47342b87d22f33a`.
- Delta: six one-line commits on three Markdown pages (152 lines added, 32 removed), then a merge of dev. Against dev the PR is 1,778 added and 112 removed over seven Markdown pages, with no code, generator, gate, configuration or gitlink.
- SE below is `docs/design/MARK_II_STREAM_ENGINES.md`; AP is `docs/design/MARK_II_AREA_PLAN.md`; FR is `docs/reference/FR_NFR.md`.

**Verdict basis.**
- Every R758-3 and R757-3 finding and residue item is closed at its cause.
- The header read-back path, the conversion error and the merge's REQUIREMENTS.md and docs/README.md results all hold under my own checks.
- The verdict is NEGATIVE on two new MINOR findings in the round-4 listener-merge text:
  - F1: "tu on both loses no sample" and "a time step costs no more than on one network" are stated as fact, and the published model falsifies both outside the cases the page tests.
  - F2: one new sentence contradicts rule 3 and the model.
- Neither finding asks for a rule to change. Under the convergence rule, conditions on those sentences plus an open design item with a verification row are enough for F1, and one replaced sentence is enough for F2. No stated latency, load, save or area figure moves.
- The 2026-10-31 owner decisions are out of review.

## Findings

### R758-4-F1 MINOR - Conformance, RTL, Robustness, Tests, Docs - SE:711, :721, :723-738, :647, :680-681, :1219 - tu on both networks still loses samples in cases the page does not state

- **Authority/evidence:**
  - SE:711 says "With both networks delivering, tu on both loses no sample." SE:723-738 then lists the gaps left; the PR body and the page present that list as the behaviour against Milan v1.2 4.4.2.3. SE:721 says "A time step costs no more than on one network."
  - The probes use the published `merge_model.py` unchanged (`scripts/probe_merge_r4.py`, `scripts/probe_tu_step_apart.py`; `receipts/model/probe_merge_r4.out`, `probe_tu_step_apart.out`). Both networks deliver every packet in each case below.
  - **(a) Own-time skew during tu.**
    - SE:616 says a tu copy's time names no packet, but rule 1 (SE:647) still applies the late and early check to that time. Rule 4 adds the counted check; it does not replace this one.
    - Both networks at the primary's latency, tu on packets 100 to 600 (62.5 ms), every copy skewed +1 ms: 3,000 samples missing, which is the whole tu period (`early` 1,000). At -2.5 ms the same (`late` 1,000). At -1.9 ms: 1,752 samples missing.
    - At the model's default latencies (secondary 1.1 to 1.5 ms), skew of plus or minus 1 ms: 78 samples missing (13 packets, 1.625 ms). The network whose tu copies fail rule 1 keeps `LAST_TU` clear, so rule 2 holds the other network's copies off until the old clean time passes. With +1 ms the audio also resumes at its own time, 2,922 samples off their packets, until a clean copy re-anchors.
    - The window is 0.667 ms plus the arrival latency on the early side and the arrival margin on the late side. The largest both-tu skew SE:1219 and the model test is 200 µs.
    - An unpaired stream loses the same period (3,000 samples), so a pair is no worse here. The claim is still unconditional and the listed gaps omit it.
  - **(b) Arrival margin under one packet interval.**
    - SE:680-681 treats a reference the render point passed as invalid. If a network's copies arrive less than 125 µs before their time, its reference lapses before its next copy, so with tu it has no reference and rule 4 discards its copies.
    - Meanwhile the faster network's copies wait on rule 2 until the slower network's first tu copy arrives. So the packets between are lost.
    - Secondary 110 to 120 µs before its time, no skew: 72 samples missing (12 packets, 1.5 ms). At 50 to 100 µs: 36. At 10 to 50 µs: 24. At 150 to 200 µs: 0.
    - The margin is legal: a 2 ms offset with a class A transit near its 2 ms bound (IEEE 802.1BA-2011 6.5, cited at SE:560) leaves it. SE:723 lists "a network rejoining during tu", which does not describe a network that never left.
  - **(c) A time step with the networks clearing apart.**
    - The author's probe clears both networks on one packet. Letting the slower network clear first and the faster one up to 80 packets later (10 ms):

      | Step | Pair | Primary alone | Secondary alone |
      |---:|---:|---:|---:|
      | -200 µs | 3 packets | 2 | 2 |
      | -300 µs | 4 packets | 2 | 2 |
      | -500 µs | 9 packets | 4 | 8 |

    - Cause: rule 2 discards the faster network's tu copies once the slower network's newest copy is clean, while that network's stepped-back copies land on packets already written.
    - The cost is small, but SE:721 is stated without the condition.
- **Impact:** a design lane or a bench test built to SE:711 finds audio gaps of 1.5 ms up to the whole tu period with both networks up. This is the same event family R758-3-F1 raised (a talker's gPTP uncertainty on both ports). The stated limits and the requirement's verification row do not cover it, so the owner cannot read the limit from the page.
- **Required outcome:** any one of these for each of (a), (b) and (c).
  - Change the rule. For (a), a tu copy with a valid reference could take its late and early check from its counted time only. For (b), keep the reference valid for the count across the render point, with a separate bound against wrap.
  - Or state the limit: SE:711 and SE:721 carry their conditions (own time inside rule 1's window on both networks; arrival more than 125 µs ahead; both networks clearing together), SE:723-738 and the PR's known limitations list the gaps with their sizes, and the requirement goes in the open design items with a verification row for lane 6.
  - Either way, SE:1219 and the model gain the cases.
- **Verification:** `probe_merge_r4.py` sections A and D and `probe_tu_step_apart.py` on the updated model. Each case shows 0 missing samples, or the page states that gap and its size.

### R758-4-F2 MINOR - RTL, Robustness, Docs - SE:678 (with :649, :675, :735-736) - "A tu copy with no valid reference cannot make one" contradicts rule 3 and the model

- **Authority/evidence:**
  - Rule 3 (SE:649) renders a tu copy with no valid head at its own time and anchors on it, whatever its reference state. Reference upkeep then says that copy cannot make a reference (SE:678).
  - The model does the opposite: `merge_model.py:170` makes a reference for every anchoring copy, and its "at most 22 packets" result depends on that.
  - `probe_merge_r4.py` section B applies the sentence as written:
    - unpaired, tu from the first packet: 22,452 samples missing, against 0 in the model;
    - unpaired, tu from 100 with a -40 sequence jump: 16,842 missing, against 84.
  - The stream then renders one packet per head lapse for as long as tu lasts, so the bound at SE:735-736 no longer holds.
- **Impact:** the page is the design basis and the model is lane evidence, so a lane following the sentence ships the larger loss, while a test modelled on the published model expects otherwise. I cannot call this wording only, because the sentence decides state-machine behaviour.
- **Required outcome:** SE:678 excepts the anchor. Exact fix: "Only rule 3's anchor lets a tu copy make one."
- **Verification:** the page, the register text at SE:884 and `_anchor`/`_seen` in the model say the same thing.

### R758-4-R1 RESIDUE - Docs - PR body, round 4 "Merge model" row; author-r4/HANDOFF.md:83 - mutation count

- Both say removing rule 4 fails 5 cases. The published receipt (`author-r4/evidence/model/merge_model.out:39`) and my rerun say 7. The receipt is right and the mutation is caught either way.
- Exact fix: "removing rule 4 fails 7", and `no_rule4` 7 in the handoff.

### R758-4-R2 RESIDUE - Docs - SE:659-660 - "the only valid copy"

- SE:660 excepts rule 4, which reads tu copies into SE:659's claim, but rule 2 can also drop what turns out to be a packet's only copy: a faster tu copy, when the clean partner frame is then lost. With 1 % loss on the clean network: 318 samples missing (`probe_merge_r4.py` section E). SE:693-695 already covers the behaviour as loss plus tu, so only these two sentences need to change.
- Exact fix: SE:659 "Past rule 1, a packet's only clean copy always renders."; SE:660 "Rule 2 and rule 4 drop only tu copies."

### Suggestions (optional, do not affect coverage)

- **S1, the author's open point on the double fault (handoff line 43):** I agree that holding saves across a sector erase after a zeroed header also fails its read-back is a reported fault path, like the record-page retry at SE:1008-1009. A stuck header cannot be invalidated any other way, and repeating the zeroing could not make the old slot safe to append to. NFR-REL-03's "No flash erase may sit on the save path" does not say this. One clause there ("A reported flash fault is outside this bound") would remove the reading question, at the owner's next requirement approval.
- **S2, open design item 2 (SE:1237):**
  - The requirement is right and verifiable. Its second sentence names tu on every copy or an unpaired stream, but tu on one network with a clean partner that loses frames also misplaces samples: a +3 step gives 228 wrong samples (`probe_merge_r4.py` section F). The verification row could add that case.
  - The item could name the candidates: the AVTP `mr` toggle (the page never mentions it), and a stop longer than the span, which already lapses the reference.
- **S3, a failed header and the append space:** the page shows 70 appends fit 392 free pages (SE:1192) only for the fault-free path. Restart fits too: 2.046 + 13.88 + 2.046 = 17.97 s, at most 367.9 pages under S1 and S2. With a double fault's held erase it is at most 430.2 pages, above 392, and the page has no rule for a full old slot. One sentence could say so.
- **Carried, not taken:** R757-3 S1 and R758-3 S3. The author's reasons are recorded and acceptable.

## Round-3 findings at this head

| ID | Status | Evidence at 22f3cedb |
|---|---|---|
| R758-3-F1 tu on both | Closed at its stated verification | Rule 2 (SE:648) with `LAST_TU` (SE:886); the model's "tu on both from packet 100" misses 0 samples (30 at round 3), equal latencies with onsets together or 0.5 ms apart miss 0 (84 and 60). The `r3_rule2` mutation fails 13 cases. SE:700-738 states the behaviour against Milan v1.2 4.4.2.3. The remaining unstated cases are R758-4-F1 |
| R758-3-F2 far tu copy | Closed | Rule 4 (SE:650), SE:625-628; jumps of plus and minus 40 with the partner clean, with tu, faster, and unpaired: `outside` 0, `jump_dup` 0, unpaired gap 84 samples (14 packets, within 22). `SE_MERGE_TU` text at SE:810 names rules 2 and 4. All rule numbers re-checked: SE:651, :671, :808-810, :883. Span edges are open design item 1 |
| R758-3-F3 header read-back | Closed | SE:1101-1125, :1146, :1154-1155, :1224, FR:476. Details under focus 2 below |
| R758-3-R1 | Closed | SE:1263 and AP:313 read "Redundancy needs gPTP on both ports (#665 F6). One instance per port is one way." The full stop for the semicolon is required by the sentence limit |
| R758-3 S1, S2 | Taken | SE:1095-1096; SE:568-569 |
| R757-3-N4 | Closed | Same text as R758-3-F3. The author's `no_invalidate` mutation loses changes; the reviewers' sequence boots with the save in all 18 cuts. Read after my draft |
| R757-3-N5 | Closed | SE:544-577; SE:604, :1219, :1220 carry 2.744 µs; no `2.210` on the Mark II pages, FR, the split page or REQUIREMENTS.md; the PR body uses 2.210 only as history. Details under focus 3 below |
| R757-3 RR3, RR4 | Closed | SE:1153 as written; SE:1219 as written plus "or rule 4", correct because rule 4 is new |
| R757-3 S2, S3 | Taken | `conversion_error.py`; SE:1140 |

The internal round-3 report was read after my draft verdict and ledger. The draft's sha256 is in `receipts/draft_sha256.txt`; the draft is not published. Earlier rounds' findings were closed at earlier heads and the delta does not touch them.

## Independently verified at this head (no finding)

- **Packet** (`receipts/packet_verify.txt`): evidence commit `993a5bb5`, author-r4.
  - 119 manifest entries, 0 published-digest mismatches, 0 unlisted files.
  - SHA256SUMS: 118 lines, all equal to the manifest's original digests. The 12 that differ from the published bytes are exactly the path-redacted files. One large log is listed in `LARGE_LOGS.txt` by digest and is not published.
  - The commit itself carries no cryptographic signature (the host reports it unsigned), so this is digest integrity only.
- **Focus 2, header read-back:**
  - Host flash model rerun (`receipts/model/compaction_model.out`, rc 0), byte-equal to the author's apart from its trailing rc line: 84,674 runs, 0 lose a change. Reviewers' sequence: 18 cuts, 0 boot without the save.
  - Mutations all lose changes: `split` 733, `no_replay` 2,704, `no_invalidate` 1,214, `ignore_zero_rb` 1,214.
  - Own probe (`scripts/probe_compaction_r4.py`): saves between the standby's erase steps, one or two failed headers in a row, every cut point: 11,496 runs, 0 lost.
  - A header format whose all-zero page passes its check loses 1,214 of 22,943 runs, so SE:1109-1110's demand on #823 is needed.
  - 365.10 ms = 359.75 + one 5.35 ms zeroing page, both re-derived. The landing and power-cut tables cover save, zeroing, zeroing read-back and erase in order. Boot can select that header only while saves are held, and both slots then hold every durable save.
- **Focus 3, conversion error:**
  - Re-derived: the difference of applied offsets splits into two B.3 terms at one instant plus the offset's drift between the two latches. So |latch to latch| is at most 125 µs + 2.792 ms. 200 ppm x 2.917 ms = 0.5834 µs, and 2.000 + 0.584 + 0.160 = 2.744 µs.
  - A4 is stated (SE:556-560) and bench-checked at SE:1220. It is sound for offsets up to the span: arrival precedes presentation by rule 1, and presentation is the crossing estimate plus 0 to 125 µs plus the offset (Milan v1.2 5.3.7.6, as `docs/reference/MILAN_COMPLIANCE_MATRIX.md:191` records it).
  - Window: 2.744 + 0.550 is well below 62.5 µs, with 59.21 µs spare; neighbours stay 121.71 µs apart.
  - `conversion_error.py` rerun: worst 2.640 µs over 201,280 cases, rc 0, equal to the author's.
- **Focus 4, merge:** the merge model rerun passes 33 cases, and every mutation is caught (`exact` 33, `own_time` 4, `no_rule2` 5, `r3_rule2` 13, `no_rule4` 7), byte-equal to the author's. `probe_tu_step.py` output is identical. LAST_TU, the held tu copy, and rule 4 discarding and counting in `SE_MERGE_TU` all match between page and model, apart from F2.
- **Focus 5, open design items:** items 1 and 2 (SE:1236-1237) each carry a requirement and a verification row, owned by lane 6 (AP:276). Neither is wrong, unsafe or unverifiable. See S2.
- **Focus 6, merge result:**
  - A clean merge of the two parents reproduces the head's tree exactly, so the merge hand-edited nothing.
  - Dev's one REQUIREMENTS.md addition (REQUIREMENTS.md:472, the soft reset as the controller's AECP REBOOT) names no placement. The PR's scoping at REQUIREMENTS.md:25-33 lists AECP, so it covers it.
  - `docs/README.md` keeps both rows (:72 reset page, :81 stream engines). The merge changes none of FR, SE, AP, the split page or the overview.
  - Dev's `docs/design/REBOOT_RESET.md` has the protocol processor raise the request. The PR body records that a firmware owner must raise it after the switch-over.
- **Focus 7, docs workflow:**
  - Own clean clone with the four submodules and the pinned Markdown renderer (`receipts/gates/`, `gates_summary.txt`): 33 of 33 gates rc 0, including `docs_check` (0 findings, 213 pages), `check_em_dash` (0 over 1,778 added lines in 7 pages), `check_baremetal_only` (0 over 1,434 files), `gen_toc` all three modes, hygiene, TODO ownership and imported gPTP docs. `git diff --check 1f29f189 HEAD`: rc 0.
  - Author receipts for the steps I did not run, such as both builder legs, the RV32 SDK and the ratchets: all 50 rc files are 0. Builder leg 0 reads ALL GATES PASS; leg 1 reads ALL GATES PASS EXCEPT 16 NOT RUN, by their own skip rules.
  - Page style: `check_doc_style` passes in my run, and the author's `style_touched.log` over the changed blocks reports 0 findings. I did not rerun that script.
- **Comment rule and privacy:** the PR's delta has no source file, so no comment-rule instance. The docs scrub is clean, and no reviewer or lane ID appears on the touched pages. Their issue-comment links are owner and survey citations, and the rule covers source comments. The live PR body equals the packet's apart from a trailing newline.
- **RTL lens on the delta:** `LAST_TU` fills bit 12 of `LCTX_STATE` with 31:13 reserved (SE:886-887), so no word or Block RAM figure changes. |k| from a tu copy stays within 21 because rule 4 bounds its counted time to the span, so the map width holds. A rule 4 failure leaves the reference following the jump, so that network waits for a clean copy or a new anchor, as SE:726 and :730 say.
- **Clone restored** (`receipts/clone_restore_check.txt`): HEAD and tree as above, index tree equal, 0 untracked or ignored entries, index entries equal to the tree, six gitlinks unchanged. All probes ran in scratch; nothing ran in the clone.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | SE:530-577 against IEEE 802.1AS-2020 B.1.1, B.1.2, B.3 and Milan v1.2 5.3.7.6; SE:700-738 against Milan v1.2 4.4.2.3 and IEEE 1722-2016 4.4.4.6, 4.4.4.7; NFR-REL-03 at FR:476; REQUIREMENTS.md:25-33 and :472 | R758-4 | 22f3cedb420992b7b776c5a842b0b210ac4191d3 |
| RTL | UNCLEAN (F1, F2) | Merge rules and upkeep SE:582-738; `LCTX_STATE` and merge registers SE:808-810, :881-887, :902-903; open design items SE:1229-1237 | R758-4 | 22f3cedb420992b7b776c5a842b0b210ac4191d3 |
| Robustness | UNCLEAN (F1, F2) | Both-tu skew, margin, step, jump, loss and restart probes; failed header paths and tables SE:1101-1159; restart append space | R758-4 | 22f3cedb420992b7b776c5a842b0b210ac4191d3 |
| Tests | UNCLEAN (F1) | `merge_model.py`, `compaction_model.py`, `conversion_error.py`, `probe_tu_step.py` rerun with mutations; own probes in `scripts/`; verification rows SE:1219-1224; 33 gates; author gate receipts | R758-4 | 22f3cedb420992b7b776c5a842b0b210ac4191d3 |
| Docs | UNCLEAN (F1, F2; R1, R2 residue) | SE, AP, FR delta and history `69fd18f1..22f3cedb`; merge result; docs/README.md; author HANDOFF, live PR body, TOC and anchors | R758-4 | 22f3cedb420992b7b776c5a842b0b210ac4191d3 |

## Real limits

- I did not open the standards' text this round; no copy is in the repository. Clause readings rest on my earlier rounds, the repository's own records of Milan v1.2 5.3.7.6 and 4.4.2.3, and the author's quotations. IEEE 802.1BA-2011 6.5 and N25Q128 5.1.2 are accepted as cited.
- Every result comes from the author's models and my probes on them, not an implementation. F1 and F2 are design-level. The models run at 48 kHz, and the rule logic is the same at every rate because the packet interval is the same.
- I did not run the builder legs, the RV32 SDK steps or the ratchet gates. For those I rely on the author's receipts, and they are not manager evidence.
- **Hosted evidence at this head, snapshot** (`receipts/hosted_check_runs.tsv`): 20 completed success, 22 skipped, 2 in progress (docs-gates-0 and one fail-fast context), 0 failed. docs-check-no-git, docs-gates-1, docs-gates-2, rtl-fast, wire-accountability and full-ci-gate passed. This is not acceptance evidence.
- No physical calibration, bench or hardware run took place. No manager source bank ran at this head, and none is claimed or inferred.

## Pending manager duties

- Hosted and act acceptance of the exact head, including docs-gates-0.
- Builder and native banks on the current-dev merge candidate at the merge turn (source base and live dev `1f29f189` at this review).
- Owner approval of the requirement text and of the open owner decisions: latency with mixed formats or fewer reservations; save bursts, Block RAM and the commit timeout; lever 5 against media ownership, lever 2 after lever 3; `flexptpd` on two ports and its surveyed source.
- Carry R758-4-R1 and R758-4-R2 to the residue checklist.

R758-4 FINISHED
