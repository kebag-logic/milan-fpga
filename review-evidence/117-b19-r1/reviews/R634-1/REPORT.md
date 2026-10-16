[R634] NEGATIVE - exact head 18b98bbcecf478b903610a07667f232d944d6feb

# R634-1: internal independent review of PR #751 (issue #117, #387, #621; bench lane B19)

Round R634-1. Cleared-context internal review at exact head `18b98bbcecf478b903610a07667f232d944d6feb`, tree `b9e4e014079cc9497a51ccfc3870e086143b8816`, base `734eb780dc93896a5961cd95180f79475a401650`. This is a findings-only change: two dated sections, `docs/findings/117_GPTP_SILICON_EVIDENCE.md` (+261) and `docs/findings/387_SOFTWARE_GM_STEP.md` (+164). I applied all five lenses. Every PASS/FAIL grade I could re-derive from the published packet re-derives exactly: the six switch cycles, the recovery against the 5 s bound, the ten grandmaster edges, the first reach, retention and cadence, the box 4 probe and enumerations, and the restore. The verdict is NEGATIVE.

My five MINOR findings are each about what the pages claim, or what the public record can show, not about a graded result:

- the image identity binding;
- the box 3 verdict sentence and its time base;
- figures with no published derivation, and a grader arm that its code does not implement;
- where the raw captures are kept;
- one host-derived identifier.

I also retain at this head the external round's three findings (R635-1-F1, F2, F3), each independently verified. See [Reconciliation](#reconciliation-with-the-other-public-review-at-this-head).

No bench, hardware, Docker or act was used. I made no GitHub write and no source edit.

## Reconstruction

- Contract: `AGENTS.md`, `CONTRIBUTING.md` (sections 2, 3 and 6, including the em-dash rule and the privacy rules), `docs/README.md`.
- Scope: the #117 body (boxes 1 to 5), the B19 assignment (#117 comment 6207451080, items 1 to 8 and the render re-base decision), the executor's TAKEN (6207516834) and REVIEW READY (6208250865), the owner decisions of 2026-10-16 (6208109700, 6208207821), the #387 body (item 4) and the #621 body (item 3), and lane B1's 2026-09-29 record at the base.
- Authorities: `docs/design/GM_LOSS_RECOVERY.md` "Recovery bound" (starts at the grandmaster's first Announce or Sync; 5 s; terms 3 s + 0.375 s + 1.625 s), `docs/testing/726_STREAM_COUNTERS.md` "Counter contract", and the PR #747 manager provenance (comment 6200503436, evidence tree `bbc53aab`: `provenance.json`, `flash.log`, `console-after-flash.log`).
- Diff and history: `git diff 734eb780..18b98bbc`, one commit with a one-line subject and no trailer. `9ef71772` is an ancestor of the base, and PR #707, #729 and #742 are ancestors of `9ef71772`. `9ef71772..734eb780` changes six files, none in the product image.
- Evidence: the published packet `review-evidence/117-b19-r1` at `2c4ca68a`. All 249 files match the publisher's `MANIFEST.json`. 207 match the author's `MANIFEST.sha256`; the 41 that differ are exactly the 41 the publisher marks as redacted, and one large raw is absent (`receipts/packet-verify.txt`).
- Hosted state at exact head, observed only: executed and successful are `rtl-fast`, `docs-check-no-git`, `wire-accountability`, `elaborate`, `bdd-conformance` and `full-ci-gate`. `verilator-suites`, `yosys-portability` and the firmware and Yosys jobs are skipped contexts. The `docs-gates-*` jobs were still in progress (`receipts/hosted-check-runs.tsv`). Hosted and act acceptance is the manager's.

## Findings

### R634-1-F1: MINOR (Conformance, Docs): nothing on the page binds the B19 run to the flashed `9ef71772` image

- **Where:** `docs/findings/117_GPTP_SILICON_EVIDENCE.md:835-837` (image and identity bullets), `:826` (box 5 "PASS for these runs"), and `docs/findings/387_SOFTWARE_GM_STEP.md:369-371`.
- **Authority and evidence:**
  - #117 box 5 requires exact hashes. The assignment's receipt 1 asks the identity gate to bind the run to the flashed `9ef71772` image through PR #747's manager provenance and `flash.log`.
  - The new section cites "PR #747's provenance record" as plain text. In a repository Markdown file that is not a link. Neither page links the provenance tree, and neither carries the image's bitstream SHA-256 (`4b5a391a...cffcca`) or AEM SHA-256 (`4fc8d615...b396d`).
  - The two identity reads it relies on, `VERSION=00020060` and AEM CRC `5ba355eb`, do not distinguish this image from its predecessor. The B18 section says so (`629_MEDIA_CLOCK_FOLLOWING_BENCH.md:5036-5039`), and this same page records `VERSION 0x0002_0060` on an earlier image (`:80-82`). My comparison of boot banners adds nothing that distinguishes them: BIOS CRC `b61c1b79` and LiteX sha `a1e1c36` are the same in both.
  - The provenance chain ends at the end of B18 (2026-10-15 18:59:53 UTC, comment 6200503436 item 5). The page states no basis for the gap from then to the B19 gate at 2026-10-16 03:37:20.
  - The timing itself is correct: the gate ran at 03:37:20-26, before the first power action at 03:42:18.25, and again at 04:30:48 (`receipts/f1-identity-binding.txt`).
- **Impact:** A cold reader of the #117 page takes "Identity gate PASS, 11 of 11" as proof that the run was on `9ef71772`. The reads cannot prove that, and box 5's "exact hashes" is marked PASS for a section that carries no image hash.
- **Required outcome:** The B19 image paragraph links the provenance record and gives the bitstream and AEM SHA-256. It states that the device reads do not distinguish the image from `5603c353`, so identity rests on the provenance. It names the basis for continuity after 18:59:53 UTC on 2026-10-15, for example the assignment's statement that the image stayed installed and unflashed, or the bench-lock record.
- **Verification:** Re-read both pages. The link resolves, and the hashes equal `provenance.json`. Docs gates rc 0.

### R634-1-F2: MINOR (Conformance, RTL, Robustness, Tests, Docs): the box 3 verdict sentence is not true for three graded edges, and its time base is not bounded

- **Where:** `docs/findings/117_GPTP_SILICON_EVIDENCE.md:821` ("each CSR edge follows its wire cause within one 0.25 s console sample") and `:975-977` ("Every loss edge and every return edge lies in the console interval that holds its wire cause or its receipt timeout").
- **Evidence:** I recomputed the edges from `bench/cycleNN/correlation.json` (`scripts/check_cycles.py`, `receipts/cycles-check.txt`):
  - **Cycle 1, grandmaster loss.** The console interval runs from 3.010 to 3.260 s after the switch's last Announce, so it does not contain the 3 s receipt timeout. The sample taken 10 ms after the timeout still named the switch, and the edge first appears 0.260 s after it.
  - **Cycles 3 and 5, grandmaster return.** The accepted Announce came 9.1 and 3.7 ms before the last sample that still named the DUT. The first sample showing the switch came 0.259 and 0.254 s after the Announce.
  - The table row at `:971` discloses cycles 3 and 5, which contradicts the verdict sentence. Cycle 1's loss edge is disclosed nowhere.
  - No packet tool grades the loss or return edges against their causes. `summ_b19.py` computes the brackets without grading them, and only the CRF `tu` rise carries a `wire_inside` flag. The published claim is therefore hand-composed.
  - The margins (4 to 10 ms) are small next to the placement uncertainty the page itself states (24 to 52 ms between methods), so the box 3 result may well hold.
- **Time base (added after reading R635-1-F2, which raised it; independently verified):**
  - `sw/firmware/milan_baremetal/milan_baremetal.c:1910-1938`: `milan_status_handler` reads the CSRs, then prints two lines, and only then reads the PHC (`print_tod(gettime_ns())`). The placement puts each sample at that PHC read.
  - The two lines are 271 bytes (`firstreach/post-boot-console.txt`). At the build's 115200 baud (`configs/endstation_ax7101_1x1_tdm8.yaml:51`) that is 23.5 ms, less a FIFO of at most 16 bytes. Each placed time is therefore about 20 to 23.5 ms later than its register reads, a systematic offset that the analyzer neither bounds nor corrects.
  - With that offset applied, all 27 graded edges are contained, the three exceptions included (`scripts/check_skew.py`, `receipts/box3-skew-check.txt`). But cycle 3's sync-loss edge and its first `tu=1` CRF PDU then sit 0.8 to 4.4 ms inside the end of their intervals. So the result depends on a model the page does not state.
  - This is an interface-latency assumption, so the finding is recorded under RTL as well.
- **Impact:** The criterion the assignment asked for (receipt 4), as worded, is false for three edges at the published time base. A reader cannot tell which tolerance or which time base the PASS used, and these edges sit on the timeout paths.
- **Required outcome:** State the box 3 criterion with its time base, including the read-to-PHC offset, and its tolerance. Re-place and re-grade every edge. List the edges that sit near a boundary, with their margins. Then make the verdict follow from that stated rule. Grading it mechanically would make the rule able to fail.
- **Verification:** `scripts/check_cycles.py` and `scripts/check_skew.py` over the packet. The page text agrees with each computed bracket under the stated model.

### R634-1-F3: MINOR (Conformance, Tests, Docs): figures stated as evidence with no published derivation, and a documented grader arm with no code

- **Where:**
  - `docs/findings/387_SOFTWARE_GM_STEP.md:378`: "0 of 600 controller polls" and "the published peer delay stayed 373 to 392 ns".
  - `:406`, the grade definition: "no console sample and no controller poll with asCapable 0".
  - `:453`: "peer delay 373 to 392 ns throughout".
  - `docs/findings/117_GPTP_SILICON_EVIDENCE.md:988` (the peer's CRF input "149,513") and `:993` ("Across 26 reads its FRAMES_RX trailed TIMESTAMP_VALID by 167 to 7,925 PDUs").
- **Evidence** (`receipts/f3-unreceipted-figures.txt`):
  - The docstring of `tools/gm_summary.py` (line 7) documents a controller-poll arm, but its code counts asCapable 0 only in the console samples (line 41).
  - `a624_analyze.py` keeps only the grandmaster identity from GET_AVB_INFO (line 143).
  - No `bench/gmNN/analysis.json` carries a per-poll AS_CAPABLE series or a PDELAY_NS series.
  - No packet file carries 149,513 or the 26-read lag as a value, and `avtpdu-parity.json` has neither.
  - Mutation probe on a disposable copy (`scripts/probe_gm_summary.py`, `receipts/gm-summary-mutation.txt`):
    - Console-side mutants fail the grade as they should: an asCapable-0 sample, a second `tu` episode, GPTP_GM_CHANGED +2, an `mr` toggle, and a peer MEDIA_UNLOCKED.
    - A controller-poll asCapable 0 cannot fail it.
  - The published summary and the page's ten-row table reproduce byte for byte.
- **Impact:** The #621 item 3 grade, as the page defines it, was applied only through its console arm. Four supporting figures cannot be checked from the public record, because the raws are private. The verdict itself stands on the console arm: 2,399 samples at 0.25 s, all with asCapable set, against lane B1's 2.0 s losses.
- **Required outcome:** For each figure, publish its derivation as a tool and output over the hashed raw controller and console transcripts, or remove it. Either implement the controller-poll arm, or restate the grade, the docstring and the page as console-only.
- **Verification:** Re-run the grader over the published outputs. A planted controller-poll asCapable 0 fails if the arm is kept. Each quoted figure appears in a published output.

### R634-1-F4: MINOR (Conformance, Docs): the pages say the large raws are in cold storage, but the packet records them only in a temporary directory

- **Where:** `docs/findings/117_GPTP_SILICON_EVIDENCE.md:1035-1038` and `docs/findings/387_SOFTWARE_GM_STEP.md:474-476`.
- **Evidence:** The published `RAW-ARTIFACTS.json` note and `HANDOFF.md:8,162` place all 151 raws, including the 54 over 200,000 bytes, under a temporary directory on the build box. Every large-artifact hash row on both pages refers to those 54 files (`receipts/f4-raw-retention.txt`). I have no public receipt that they reached durable retention.
- **Impact:** If that directory is cleared, the hash tables that discharge box 5 on both pages point at nothing. The two published statements disagree, and a cold reviewer cannot resolve which is true.
- **Required outcome:** Publish a receipt that the 54 files are in durable retention, with their SHA-256 re-verified at the retained location. Otherwise the pages must state where the files actually are.
- **Verification:** A manager receipt whose hash list equals `RAW-ARTIFACTS.json` for those 54 entries.

### R634-1-F5: MINOR (Docs): a hardware-derived identifier of the controller host on a public page

- **Where:** `docs/findings/387_SOFTWARE_GM_STEP.md:445`, the 16-digit clock identity of the takeover Announce.
- **Authority:** `CONTRIBUTING.md` section 6 forbids bench-identifying information. The assignment's receipt 8 asks that the public text name no private device, host or instrument.
- **Evidence:**
  - The identity is the controller host's NIC-derived EUI-64.
  - The publisher's own redaction of this packet replaces exactly this value with a host placeholder in `bench/gm01-05/analysis.json` and `summary/gm-steps.json`.
  - `docs/` carries no instance of it at the base (`receipts/f5-host-identity.txt`).
  - Related controller identifiers of the same NIC family already sit in four tracked test files at the base. I am unsure this crosses the rule, and a privacy question cannot be filed as RESIDUE, so it is MINOR.
  - `docs_check.py` passes; no rule covers this shape.
- **Impact:** The page publishes an identifier that the project's own publication policy treats as private.
- **Required outcome:** Replace it with a role label, such as "the controller host's clock identity, priority1 240, stepsRemoved 1", or record a manager ruling that the value is public.
- **Verification:** `git grep` of the value under `docs/` returns nothing, or the ruling is linked.

### RESIDUE (wording only; it does not affect the verdict or lens coverage)

- **R634-1-R1, PR #751 body, "Status":** "Operator evidence, local commit ... Not pushed. Independent review is pending." is stale, and "Reviewers: assigned by the manager" too. Fix: "Commit `18b98bbc` on branch `117-b19-bench`, pushed; PR open against `dev`; reviewers R634 (internal) and R635 (external)."
- **R634-1-R2, `docs/findings/387_SOFTWARE_GM_STEP.md:383-384`:** "the GPTP_GM_CHANGED count of 3 per edge" overstates the base record. The base records +3 at nine of ten edges and +1 at the tenth (`:210` at the base). Fix: "and the GPTP_GM_CHANGED rise of 3 at nine of the ten edges".

### SUGGESTION

- **R634-1-S1:** The 387 B19 section could add one line on #387 item 4's `A_MCSRV_STAT` observable. The servo stayed IDLE because the DUT ran on INTERNAL. Lane B1 last saw it LOCKED through steps on `13eda870`, before PR #707.

## Receipt checks requested by the assignment

| # | Check | Result at this head | Receipt |
|---|---|---|---|
| 1 | The identity gate binds the run to the flashed `9ef71772` image, before any power action and again at the end | Timing holds: 03:37:20-26 before OUT0 off at 03:42:18.25, and again at 04:30:48, each 11 of 11. The binding is not stated on the page: F1 | `f1-identity-binding.txt`, packet `identity/`, `identity-end/` |
| 2 | Box 1: first reach after the single OUT0 cycle, plus retention, cadence, turnaround and no daemon | All quoted figures match `firstreach/analysis.json` and `retention.json`: first frame 8.055 s; switch Announce at 9.794 s and Sync at 9.812 s; first AECP answer at 9.955 s, asCapable. Retention: 1,200 of 1,200 samples; 300 of 300 DUT polls and 300 of 300 peer polls; turnaround 10,976 to 13,432 ns. The DUT-end asCapable time is inferred, and the page says so. OUT0 was switched once | `packet-verify.txt`; packet files |
| 3 | Box 2: six OUT4 cycles, recovery against 5 s, one stream restart per return in the bound cycles | Table recomputed: all 54 values match. Recovery 0.474 to 1.768 s. STREAM_START and STOP +1/+1 in cycles 1 to 3; every PDU after the return has `tu=0`. Only OUT4 switched. RST_EPOCH stayed 1. A planted late recovery turns the grade to FAIL | `cycles-check.txt`, `cycle-streams.txt`, `cycles-summary-mutation.txt` |
| 4 | Box 3: each CSR edge within one console sample of its wire cause; placement of the first `tu=1` CRF PDU | The first `tu=1` PDU lies inside the `CLKV_STAT[0]` rise interval in cycles 1 to 3, and asCapable returns on the DUT's second completed exchange in all six cycles. Three edges sit outside the stated rule by 4 to 10 ms at the published time base. With the 20 to 23.5 ms read-to-PHC offset, all 27 are contained, some by under 5 ms: F2, R635-1-F2 | `cycles-check.txt`, `box3-skew-check.txt` |
| 5 | Box 4: counters-probe parity, per-AVTPDU counters, three headless Milan enumerations | The probe transcripts are identical apart from the entity ID, and both are CLEAN. FRAMES_TX 149,514 against 149,499 on the wire; the rates match. Three runs, `IEEE17221`+`MILAN`, 42 descriptors, identical static tree, 0 DUT complaints. Two figures have no derivation: F3 | packet `box4/`, `avtpdu-parity.json` |
| 6 | #621 item 3 and #387 item 4: ten edges; one `tu` per edge; no asCapable loss; one GM_CHANGED; no `mr` change; MEDIA_RESET flat; no unlock; render re-base carried by simulation | All ten re-graded PASS from the per-run analyses alone. The PHC steps match to 1 us. 2,399 console samples. The render re-base is scoped to simulation per the decision. The controller-poll arm is absent: F3. The `tu set` column is one sample late in four rows, and steady clear is 31 to 32 ms late in all ten: R635-1-F3 | `gm-steps-check.txt`, `gm-summary-mutation.txt`, `tu-set-check.txt` |
| 7 | The restore read-back equals the as-found state, including the music bindings and outlets | 41 of 46 census entries are equal. The 5 that differ are the DUT's live propagation delay and its re-claimed MAAP addresses (two DUT transmit states, two peer receive states). Both music bindings and the CRF binding, with their flags, are as found. Clock sources: DUT 0, peer 1. OUT0 to OUT6 on. The controller host is back to timestamping 0/0 and 0 ppb, 4,481 ns from its found trajectory | packet `restore/` |
| 8 | The public text names no private device, host or instrument | Roles are used throughout, and the docs gates pass. One host-derived identifier: F5, R635-1-F1 | `f5-host-identity.txt` |

## Gates I ran at the exact head

All in private environments under the packet's scratch directory, with the Markdown lock installed by hash (`receipts/gates/summary.txt`):

| Gate | Result |
|---|---|
| `docs_check.py` | rc 0; 0 findings, scrub self-test 23/23 |
| `check_doc_style.py` | rc 0 |
| `gen_toc.py --check` | rc 0 |
| `gen_toc.py --verify-anchors` | rc 0 |
| `check_em_dash.py --base 734eb780` | rc 0; 0 findings over 425 added lines, arms 339/339 |
| `check_doc_paths.py` | rc 0 |
| `check_feature_status.py --self-test` | rc 0 |
| `ci_scope.py --selftest` | rc 0 |
| `check_baremetal_only.py --check` | rc 0 on rerun. The first run returned rc 2 because the interpreter lacked the YAML module, an environment limit and not the head |
| `git diff --check 734eb780 HEAD` | rc 0 |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3, F4; retained R635-1-F2, R635-1-F3) | #117 boxes 1 to 5; B19 assignment items 1 to 8; #387 item 4; #621 item 3; `GM_LOSS_RECOVERY.md` recovery bound; `726_STREAM_COUNTERS.md`; the PR #747 provenance; both new sections against the packet's analyses | R634-1 | `18b98bbcecf478b903610a07667f232d944d6feb` |
| RTL | UNCLEAN (F2; retained R635-1-F2) | `git diff --stat 734eb780..18b98bbc`: two findings pages, no HDL, no source comment, so the comment rule has no new instance. `9ef71772..734eb780`: six files, none in the product image. The behaviour the pages report (0.375 s and 3 s receipt timeouts, asCapable return on the second completed exchange, DUT master Syncs before adoption, LINK counters) was checked against `correlation.json` and the recovery-bound terms, with no unrecorded break of an RTL contract. The status interface's read-to-PHC latency (`milan_baremetal.c:1910-1938`, 115200 baud) is not modelled by the evidence's time base: F2. My first pass held this lens clean. I widened it after verifying the interface point raised by R635-1-F2 | R634-1 | `18b98bbcecf478b903610a07667f232d944d6feb` |
| Robustness | UNCLEAN (F2; retained R635-1-F2) | Timeout-path edges and sample-boundary placement; link-dark samples placed by calibration (781 of 2,880); console gaps (at most 0.444 s); RST_EPOCH; the first-reach reader defect and the run-3 clock-read failure, both disclosed; the once-only OUT0 guard; restore residuals | R634-1 | `18b98bbcecf478b903610a07667f232d944d6feb` |
| Tests | UNCLEAN (F2, F3; retained R635-1-F2, R635-1-F3) | `gm_summary.py` and `summ_b19.py` reproduced byte-identical from the packet; mutation probes (six GM mutants, one late-recovery mutant); `cyc_check.py`, `avtpdu_parity.py` and the analyzers read; packet manifest verification; `tu set` and steady-clear derivation checked against the health history | R634-1 | `18b98bbcecf478b903610a07667f232d944d6feb` |
| Docs | UNCLEAN (F1, F2, F3, F4, F5; retained R635-1-F1, F2, F3) | Both new sections and their Contents entries; hash tables (65 hashes: 61 matched to the packet; the other 4 match lane B1's record and the controller host's build listing); the docs gates above; the privacy scan of the added lines; PR #751 body (R1) | R634-1 | `18b98bbcecf478b903610a07667f232d944d6feb` |

## Reproducing the receipts

1. Fetch evidence commit `2c4ca68a1d0b63651942ce2510f4fa5d19e944ab` and extract `review-evidence/117-b19-r1` into an empty directory.
2. Run each script with `python3 -I`, using the standard library only:
   - `scripts/verify_packet.py <packet>`
   - `scripts/check_page_hashes.py <repo at 18b98bbc> 734eb780dc93896a5961cd95180f79475a401650 <packet>/author`
   - `scripts/check_cycles.py`, `check_cycle_streams.py`, `check_gm_steps.py`, `check_skew.py` and `check_tu_set.py`, each with `<packet>/author`
   - `scripts/probe_gm_summary.py <copy of packet/author>`
   - `scripts/probe_summ_b19.py <copy of packet/author> <packet>/author`

   The two probes rewrite files in the copy they are given. The packet's own graders are run there with `-I`.
3. `MANIFEST.sha256` lists every published receipt and script.

## Real limits

- I had no bench access. Large raws (pcaps, console and controller transcripts) are private, so every figure that rests only on them is unverified here. This is why F3 exists.
- The DUT end's asCapable time at first reach is inferred from a rule seen in the switch cycles. The page discloses this.
- The capture server's daemon check has no receipt in the packet (the HANDOFF marks it private). The box 1 "no daemon" claim rests on the bare-metal DUT and on the controller host's `pgrep` receipts.
- Physical calibration NOT RUN. Field skips are not hardware proof. I neither ran nor claim a manager source bank.
- My clone is unchanged: HEAD and tree are as assigned, the index writes the same tree, there are no assume-unchanged or skip-worktree entries, and the six gitlinks equal the head's. All probes ran on copies under the packet's scratch directory.

## Pending manager duties

- Accept or rerun the GM-step deviation from lane B1's recipe. The DUT stayed on INTERNAL with the CRF servo IDLE, so #387 item 4's servo observable was not exercised on `9ef71772` (S1).
- Publish the raw-retention receipt (F4), the provenance link and hashes (F1), and rule on F5.
- Packet publication, outside this head: the redaction is inconsistent. The manager's comment 6208484697 says the evidence packet never carried the identity that F5 and R635-1-F1 concern. The published packet at `2c4ca68a` does carry it, in dotted form, in all ten grandmaster and alignment port logs (`bench/gm01-05/`). `bench/retention/wire-summary.txt` also carries an unredacted station MAC on the DUT link. R635-1-F1 asks for equivalent representations to be scrubbed too.
- Hosted `docs-gates-*` and `docs-check` were still running at my check. The hosted and act acceptance and the current-dev candidate validation at the merge turn are the manager's.
- The PR head has since moved to `d812a604`, through the manager's amend for R635-1-F1. This review covers `18b98bbc` only and does not review that amend.

## Reconciliation with the other public review at this head

When this round started, PR #751 carried no review findings. Only the two review-start notices were posted; there were no formal reviews and no inline comments. During the round, the external review R635-1 (comment 6208467023) posted a NEGATIVE at the same head, and the manager posted a privacy fix (6208484697). I read both only after my verdict and ledger above were written. Each R635-1 item is resolved or retained at `18b98bbc` as follows:

| Item | Severity, lenses | Disposition at `18b98bbc` | My independent check |
|---|---|---|---|
| R635-1-F1 | MAJOR, Docs | RETAINED. The line is present at this head. The manager reports the fix only at `d812a604`, outside this head and not reviewed here. Same defect as my F5, which I rated MINOR. The other reviewer's MAJOR stands | `f5-host-identity.txt`. The packet still carries the value in its port logs (pending duties) |
| R635-1-F2 | MAJOR, Conformance, RTL, Robustness, Tests, Docs | RETAINED. Same defect as my F2, which I rated MINOR and now record under RTL too. The three counterexamples reproduce exactly. The firmware read-then-print-then-PHC ordering is confirmed at `milan_baremetal.c:1910-1938`. With the measured print time applied, all edges are contained, some by under 5 ms, so the claim needs the stated model | `cycles-check.txt`, `box3-skew-check.txt` |
| R635-1-F3 | MINOR, Conformance, Tests, Docs | RETAINED, verified. `tu set` is 0.250 s late in run 1 takeover and in the run 2, 3 and 5 releases, because the window comes from the rounded step bracket. Steady clear is +0.031 to +0.032 s in all ten rows, because it is taken at command end. With the corrected times, the "0.28 to 0.78 s" steady-again range on the 387 page becomes 0.25 to 0.75 s | `tu-set-check.txt` |
| R635-1-R1 | RESIDUE, Docs | RETAINED. Same as my R1 | PR body read |
| R635-1-R2 | RESIDUE, Docs | RETAINED. The two probe logs differ only on the target-entity line | Diff after normalising the entity ID: identical |

R634-1 FINISHED
