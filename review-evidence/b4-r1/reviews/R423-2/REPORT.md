[R423] POSITIVE - exact head c39312b4871c8cc3ca604eb7c57f4b0b45d914e0

# R423-2: external review of PR #627 (Refs #451, bench lane B4, the timing item)

Round R423-2. Exact head `c39312b4871c8cc3ca604eb7c57f4b0b45d914e0`, tree
`d9b3febc6f776dce41435775941fe960f1e1b6f1`. This head is one docs-only commit on
the round-1 head `35a60c8d6ee742216f98232c85926b435ab01b91`, and four commits
on dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`. That dev commit was the live
dev tip at review time, and it is an ancestor of the head. Assignment: #451
comment 5925185587. Round-2 author packet: `review-evidence/b4-r1/author-r2` at
evidence commit `5a756676db8aa3a7a1d48fe49a157ef840540ae2`.

I wrote the verdict, findings and ledger below after an independent pass over
the issue, the assignment, the diff and the public evidence, and before I
opened any prior review report. The section on prior findings follows the
ledger. In this report, "Resolved" means the finding's required outcome holds
at this head.

## Context reconstructed

- AGENTS.md sections 3, 6 and 7 (lens tokens, finding format, coverage ledger);
  CONTRIBUTING.md 6.1 (the em-dash rule and the Markdown gate environment);
  docs/README.md.
- The #451 body, including the recipe item "Scope BCLK, FSYNC and DOUT at the
  AM62x end: 12.288 MHz, a one-BCLK FSYNC pulse at 48 kHz, data starting one
  BCLK after it".
- The #451 scope decisions:
  - 5916029287: the capture uses the SoC board's McASP; UAC is out of scope.
  - 5916044815: the UAC2 bridge defect is #625.
  - 5924157808: the continuity check is satisfied.
  - 5924192573: the lane B4 assignment (framing, a long capture, fs and BCLK
    with stated uncertainty, limits pointed to #626, restore).
  - 5924950994: the 475.6 s capture is ruled sufficient.
  - 5925185587: round-2 items 1 to 4, tables byte-identical, docs gates.
  - The executor's REVIEW READY, 5925296626.
- Interface authorities the page cites or relies on:
  - `docs/litex/CLOCK_DOMAINS.md:119`: plan A, audio 24,575,738.529 Hz, about
    -10.64 ppm.
  - `hdl/ieee1722/aaf/KL_tdm_capture_master.sv`,
    `hdl/ieee1722/aaf/KL_tdm_render_master.sv` and `hdl/milan/milan_datapath.sv`:
    frame geometry and data delay.
- Diff `e4b771f9..c39312b4`: `docs/findings/451_TDM8_TIMING_SOC_BOARD.md` (added,
  392 lines) and `docs/findings/README.md` (one index row). Round-2 delta
  `35a60c8d..c39312b4`: the page only, +47/-28.

## Findings

No BLOCKER, MAJOR or MINOR finding at this head.

```text
[R423] SUGGESTION Docs - docs/findings/451_TDM8_TIMING_SOC_BOARD.md:59-61 - "every identity value equals that page's" leaves one #617 identity row unexplained
ID: R423-2 S1
Requirement/evidence: the #617 page's identity table (docs/findings/617_DIN_FRAME_COHERENCE_BENCH.md,
  "Identity and setup") has an NVM row, "Slot B seq 230 authoritative". This lane's gate readback,
  author/identity/console-identity.txt:13, reads "authoritative B, image seq 236". The page records
  seq 236 under "As found" (:81-82) but leaves the NVM row out of its own identity table. So a reader
  comparing the two identity tables finds a difference that the sentence does not name.
Impact: no figure or verdict changes. The NVM sequence is persistence state, not image identity, and
  the page states 236 elsewhere. This is about readability only.
Required change: optional. For example: "every value in the table below equals that page's; the NVM
  sequence, which is state rather than identity, reads 236 against that page's 230".
Verification: read :59-61 against the #617 identity table.
```

## Lens results at c39312b4

```text
[R423] PASS Conformance - docs/findings/451_TDM8_TIMING_SOC_BOARD.md:36,116-117,244-250,303-320,350 and receipts/r423_2_probe.json - round-2 assignment items 1 to 4 against the public evidence and the #451 scope decisions
[R423] PASS RTL - hdl/ieee1722/aaf/KL_tdm_capture_master.sv:144,203,293-298; hdl/ieee1722/aaf/KL_tdm_render_master.sv:36-44; hdl/milan/milan_datapath.sv:1008-1013,6566-6571 - the page's RTL-referential claims (one-bit data delay, 256 bit clocks per frame, no idle bit clocks); no RTL in the diff
[R423] PASS Robustness - receipts/r423_2_probe.json (offset part) - the page's failure-mode claims for a one-bit offset in each direction, on a bit-serial line with a wrap, repeats, skips and forward jumps
[R423] PASS Tests - scripts/r423_2_probe.py, receipts/r423_2_probe.json, receipts/docs-gates.txt, receipts/evidence-publication-manifest.txt - the round-2 probe evidence reproduced independently, the gates rerun, a probe that can fail
[R423] PASS Docs - docs/findings/451_TDM8_TIMING_SOC_BOARD.md (whole page), docs/findings/README.md:12, the live PR #627 body, four commit messages, receipts/public-safety-scan.txt - wording, tables, links, gates and public safety (one SUGGESTION, above)
```

### Conformance

Each round-2 item, judged against the public evidence:

| Item | Page at c39312b4 | Evidence | Result |
|---|---|---|---|
| R422-1 F1: recording size for 630 s | :116-117 "967.7 MB at the full 630 s" | 630 x 48,000 x 8 x 4 = 967,680,000 B. 600 s gives the old 921.6 MB. The `events.jsonl` start record has `capture_s` 630.0 | Resolved |
| R422-1 F2 and R423-1 S1: verdict cell | :36 "47,997.947 Hz on the SoC board's uncalibrated clock". The evidence cell gives -42.8 ppm, of which -10.64 ppm is the plan, and the remaining -32.1 ppm is the DUT oscillator's error relative to the SoC board's clock, unsplit and unquantified | An independent fit of the 95 raw status samples in `soc-capture.log`: 47,997.9474 Hz at the endpoints and 47,997.9464 Hz by least squares. That is -42.76/-42.78 ppm against 48 kHz and -32.12 ppm against the plan's 47,999.4893 Hz (plan -10.639 ppm, from `CLOCK_DOMAINS.md:119`) | Resolved |
| Same: fs bullet | :315-320 states -42.8 ppm on an uncalibrated clock and -10.64 ppm as the plan. The -32.1 ppm relative error is unsplit, neither board's error is quantified, and the figure cannot resolve -10.64 ppm | As above | Resolved |
| Same: :241 "sum of both boards' clock errors" | :244-250 "the DUT oscillator's error relative to the SoC board's clock: about the DUT oscillator's error minus the SoC board clock's, since a fast SoC board clock lowers the measured fs" | To first order, a SoC clock fast by e_s counts T(1+e_s), so fs_meas/fs_plan - 1 = e_d - e_s. The stated sign is correct | Resolved |
| No "48 kHz within accuracy" verdict anywhere | The phrase is absent from the page, the index row (README.md:12) and the live PR body | Text part of `r423_2_probe.json`, and a grep of the PR body | Resolved |
| R423-1 F1: one-bit-offset sentence | :303-314 names the checks each direction trips | An independent bit-serial probe in both directions matches every clause (see Robustness) | Resolved |
| R422-1 S1 | :61 "every identity value equals that page's" | The identity-table values equal #617's. See R423-2 S1 | Taken |
| R422-1 S2 | :350 "58.7 s before the unbind" | The talker `end` record is at t 1790828918.128055 (`controller-logs.txt`) and the unbind at t 1790828976.782734 (`events.jsonl`): 58.655 s apart | Taken, correct |
| R423-1 S2 | :153-157 and :303-305 say the one-bit delay is the driver's mapping of `dsp_a`, not a register readback | The upstream Linux `sound/soc/ti/davinci-mcasp.c` DSP_A case sets `data_delay = 1`, which it writes to FSRDLY/FSXDLY (`receipts/mcasp-dsp_a-mapping.txt`). The lane assignment forbade `devmem` on any peripheral | Taken, correct |
| R423-1 S3 | :16-18 and :97-99: the root shell was confirmed with `id` (uid 0), and no credential was typed or stored | `author/soc/r2-shell-check.log`: `uid=0(root)`, `/dev/ttyS3`. `author/STOP-2.md:7` | Taken, correct |
| Tables byte-identical | 11 of the 12 tables are identical to 35a60c8d. The verdict table differs only in the FSYNC row the assignment names | My own table extraction, with a SHA-256 per table and a row diff (text part of `r423_2_probe.json`). It matches the hashes in the author's `table-proof.txt` | Confirmed |
| The PR says Refs #451 only | The live PR body has one "Refs #451" and no closing keyword, and GitHub's closingIssuesReferences is empty. The body is byte-equal to the packet's PR-BODY.md (SHA-256 c2247ff4...) | `receipts/pr627.json`, `receipts/pr-body-compare.txt` | Confirmed |

The page still claims nothing beyond what the SoC board can show for the #451
item. It leaves the pulse width, edge timing, levels and absolute ppm to #626
(:323-329), as step 4 of 5924192573 requires. The measured figures are
unchanged from round 1.

### RTL

The diff changes no RTL. The page's RTL-referential claims hold at this head:

- **256 bit clocks per frame, with no idle bits.** `KL_tdm_capture_master.sv:203`
  defines `FRAME_C = SLOTS_P * WORD_BITS_P`, and `fpos_r` wraps at `FRAME_C - 1`
  (:298). The page's "256 x fs assumes no idle bit clocks" (:252-255, :321-322)
  relies on this.
- **One-bit data delay on DOUT.** `KL_tdm_render_master.sv:36-44` starts data
  in bit period 1, one rise after the fsync pulse: the dsp_a shape. The master
  is instantiated at `milan_datapath.sv:6566-6571`.
- **Capture side.** The capture master instantiation at
  `milan_datapath.sv:1008-1013` sets `DATA_DELAY_P (1'b1)`.
- **Direction convention.** The module's own convention (0 = slot-0 MSB on the
  fsync edge) matches the page's "one bit early" direction.

### Robustness

`scripts/r423_2_probe.py` builds a bit-serial TDM8 line for data delays 0, 1
and 2, against a receiver fixed at 1. The line has 70,000 frames from a seeded
random first ordinal (42,338). It crosses 0xffff to 0 once, with 28 repeats,
51 skips and 14 forward jumps of 7. An independent checker judges each capture,
and so does the packet's `decode_capture.py` (SHA-256 `cfb7121b...`, equal to
the author manifest). The two agree:

| Case | Torn | Zero | Low byte | Invalid words per channel | Tags | Steps |
|---|---|---|---|---|---|---|
| D = 1 | 0 | 0 | 0 | 0 | Channel c carries tag c+1 | 0, 1, 2 and 7, as generated |
| D = 0 (early) | 0 | 0 | 0 | ch3 37,278; ch4-7 70,000 (tags above 8) | ch0-2 wrong in every frame; ch3 reads tag 8 or 9 | All doubled: 0, 2, 4 and 14 |
| D = 2 (late) | 70,000 | 0 | 34,999 per channel (odd ordinals) | ch0 70,000 (tag 0); ch1-7 34,999 | ch1-7 wrong (t >> 1) | None; every frame is torn |

Every clause of :306-314 matches. The Framing paragraph (:157-161) is
consistent with the same rows.

### Tests

- **The probe can fail.** The aligned case recovers exactly the generated step
  histogram, and each shifted case trips a different set of checks. So a wrong
  claim about any check would show.
- **The author's round-2 receipts are reproduced.** `offset-probe.json` (4,096
  frames) has the same per-check pattern as this probe at 70,000 frames. The
  per-table hashes in `table-proof.txt` equal this extraction's.
- **Docs gates at this head**, run in the pinned Markdown environment
  (cmarkgfm 2025.10.22, html5lib 1.1). All return rc 0
  (`receipts/docs-gates.txt`):
  - `docs_check.py` (0 findings) and `check_doc_style.py`;
  - `gen_toc.py --check` and `gen_toc.py --verify-anchors` (283 links);
  - `check_em_dash.py --base e4b771f9` (0 findings over 393 added lines) and
    `--selftest` (339 arms);
  - `check_doc_paths.py` (861 paths) and `ci_scope.py --selftest`;
  - `check_baremetal_only.py --check` and `check_feature_status.py --self-test`
    (46/46, 0 findings);
  - `git diff --check` against e4b771f9 and 35a60c8d.
- **Public evidence integrity.** All 185 entries of
  `review-evidence/b4-r1/MANIFEST.json` match their published SHA-256, and no
  file is unlisted (`receipts/evidence-publication-manifest.txt`). Two
  author-r2 files, `HANDOFF.md` and `gates/gates.txt`, differ from the author's
  own manifest. The publication manifest records both as path-redacted at
  publication, with original and published hashes.

### Docs

- The round-2 sentences read correctly against the evidence (see the
  Conformance table).
- The removed over-claims are gone: "48 kHz within the SoC board's clock
  accuracy", "48 kHz at the board's accuracy", "sum of both boards' clock
  errors", "every class of word check", "921.6 MB" and "about 55 s".
- The index row (README.md:12) is unchanged. It claims nothing beyond the page
  ("on the SoC board's clock ... crystal tolerance excluded").
- Commits: four, each a one-line subject with no body and no trailers.
- **Public safety** (`receipts/public-safety-scan.txt`). The page, the round-2
  added lines and the live PR body carry no MAC, IP address, home or data path,
  account name, interface name, or tool or model name. The only wiring or
  instrument words are the quoted recipe item ("Scope"), the #626 reference
  ("oscilloscope") and the method's "No ... wiring ... action occurred". There
  is no pin, cable, probe or instrument topology.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Page :16-18, :36, :59-61, :97-99, :116-117, :153-161, :244-250, :303-320, :350; #451 decisions 5916029287, 5924192573, 5924950994, 5925185587; `soc-capture.log`, `events.jsonl`, `controller-logs.txt`, `r2-shell-check.log`; `CLOCK_DOMAINS.md:119`; the live PR body | R423-2 | c39312b4871c8cc3ca604eb7c57f4b0b45d914e0 |
| RTL | CLEAN | `KL_tdm_capture_master.sv:144,203,293-298`, `KL_tdm_render_master.sv:36-44`, `milan_datapath.sv:1008-1013,6566-6571`, against the page's :252-255, :303-305, :321-322 | R423-2 | c39312b4871c8cc3ca604eb7c57f4b0b45d914e0 |
| Robustness | CLEAN | The bit-serial one-bit-offset probe in both directions, with a wrap and discontinuities, judged by two independent decoders, against :157-161 and :303-314 | R423-2 | c39312b4871c8cc3ca604eb7c57f4b0b45d914e0 |
| Tests | CLEAN | `scripts/r423_2_probe.py`, `receipts/r423_2_probe.json`, `receipts/docs-gates.txt`; author-r2 `offset-probe.json` and `table-proof.txt`; the publication manifest | R423-2 | c39312b4871c8cc3ca604eb7c57f4b0b45d914e0 |
| Docs | CLEAN (one SUGGESTION) | The whole page, `docs/findings/README.md:12`, the live PR body, four commit messages, the public-safety scan | R423-2 | c39312b4871c8cc3ca604eb7c57f4b0b45d914e0 |

## Prior findings at this head

I read the published round-1 reports (`reviews/R422-1/REPORT.md` and
`reviews/R423-1/REPORT.md` at evidence commit 5a756676) only after the sections
above were written. Each finding and suggestion, at c39312b4:

| Prior item | Severity, lenses | Status at c39312b4 | Evidence |
|---|---|---|---|
| R422-1 F1: the recording size for the 630 s capture | MINOR, Docs | Resolved | :116-117 reads "967.7 MB at the full 630 s", which equals 630 x 1.536 MB/s = 967.68 MB. "921.6 MB" is gone |
| R422-1 F2: the "48 kHz within the SoC board's clock accuracy" verdict | MINOR, Conformance and Docs | Resolved | :36 and :315-320 claim only fs -42.8 ppm on an uncalibrated clock. Of that, -10.64 ppm is the plan, and the remaining -32.1 ppm is the relative error, unsplit and unquantified. Neither over-claim phrase appears anywhere on the page, in the index row or in the PR body |
| R422-1 S1: "every identity value" | SUGGESTION, Docs | Taken as worded | :61. R423-2 S1 is an optional further clarification and does not reopen it |
| R422-1 S2: 58.7 s, not about 55 s | SUGGESTION, Docs | Taken, correct | :350. 58.655 s from the two published records |
| R423-1 F1: "every class of word check" | MINOR, Docs and Tests | Resolved | :303-314 names the checks each direction trips. Both my 70,000-frame bit-serial probe and the round-1 `probe_bit_offset` pattern (data late: every check fires except zero words; data early: torn, low byte and zero words stay clean) agree with every clause |
| R423-1 S1: the signed relative error, not "sum" | SUGGESTION, Docs | Taken, correct | :244-250, with the sign checked to first order |
| R423-1 S2: the delay is the driver's `dsp_a` mapping, not a readback | SUGGESTION, Docs | Taken, correct | :153-157 and :303-305. The upstream DSP_A case sets `data_delay = 1` |
| R423-1 S3: the `id` check and no credential | SUGGESTION, Docs | Taken, correct | :16-18 and :97-99, against `soc/r2-shell-check.log` |

No prior finding is retained. Both round-1 reports also record clean RTL,
Robustness and Tests lenses at 35a60c8d. Because the round-2 commit changes the
page that each lens examined, this round re-applied all five lenses at
c39312b4, as the ledger above shows.

## Clone integrity

I modified no file in the clone. After the work:

- HEAD and `git write-tree` equal the exact head and tree.
- `git status` is empty.
- All 977 tracked blobs match their index bytes and modes.
- The four gitlinks (`external` efeb541a, `gptp-processor` 5dce647a,
  `protocol-processor` b2db3a97, `third_party/verilog-axis` 48ff7a7e) are the
  same in the tree and the index (`receipts/clone-integrity.txt`).

The probes ran on public evidence copies under the packet's scratch directory.
A session restart interrupted the round after this report was written. The
same checks were rerun afterwards and gave identical results, which are
appended to `receipts/clone-integrity.txt`.

## Limits

- **No hardware.** Physical calibration was NOT RUN, and nothing here is
  hardware proof. I re-derived the fs figures from the published status
  samples; I did not re-measure them. The raw 730,595,328-byte capture is not
  public, so I did not re-decode it; the decode figures rest on the published
  `decode.json`.
- **Driver source.** I checked the `dsp_a` to one-bit-delay mapping against an
  upstream Linux 7.1.13 copy of `davinci-mcasp.c`, not against the SoC board's
  own kernel build.
- **No simulation.** The scoped simulator named in the assignment was not at
  its stated path, so no simulation ran. I applied the RTL lens by reading the
  source only; the change has no RTL.
- **Hosted checks at this head** (a snapshot, in
  `receipts/hosted-checks-snapshot.txt`):
  - succeeded: rtl-fast, elaborate, bdd-conformance, wire-accountability,
    docs-check-no-git, changes and full-ci-gate;
  - in progress: docs-check;
  - skipped, which is not executed evidence: verilator-suites,
    yosys-portability, yosys-elaboration, verilator-lint, the shard matrices
    and physical gPTP.

## Pending manager duties

- Hosted and local-replica acceptance at the exact head, including the
  docs-check that was still in progress.
- The final current-dev candidate at the merge turn (the source base and live
  dev were both e4b771f9 at review time), and post-merge containment.
- The owner items the PR leaves open: the SoC board's USB re-attach, the 1,016
  unmatched discontinuity clusters, and the #451 issue state, which this PR
  does not change.

R423-2 FINISHED
