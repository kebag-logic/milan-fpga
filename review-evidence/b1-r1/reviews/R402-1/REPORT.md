[R402] NEGATIVE - exact head f9eab5bf55ca4471e6e48ae3d38018d7e804505b

# R402-1 review of PR #620 (issue #599, with #394 and #387)

Round R402-1, internal cleared-context review. Head `f9eab5bf55ca4471e6e48ae3d38018d7e804505b`, tree `72e4717edbe4638e83c342720c42987ad979770f`, one commit on dev `13eda870d1a6cf3f946fc228a98862366b08d102`. The diff adds two findings pages only: `docs/findings/599_394_E1_LINK_CYCLES.md` (372 lines) and `docs/findings/387_SOFTWARE_GM_STEP.md` (299 lines). The PR refers to #599, #394 and #387 and closes none of them (`closingIssuesReferences` is empty). The commit message is one line with no trailers.

Sources, in this order: AGENTS.md and CONTRIBUTING.md; docs/README; the bodies of issues #599, #394 and #387, the assignment (#599 comment 5884216527), TAKEN (5884282801) and REVIEW READY (5885028407); the owner decisions on #387 (5794731090 step rule, 5859048589, 5862116683, 5862731997); the #602 ruling (5859297355); the linked authorities `docs/design/TIME_SYNC.md#step-policy`, `docs/design/GM_LOSS_RECOVERY.md` (recovery bound, media re-base), `docs/integration/BAREMETAL_FIRMWARE.md:1960-1977`, `docs/reference/REGISTER_MAP.md`, `docs/testing/TESTING.md` 6b and `docs/findings/394_387_E1_SWITCH_CYCLES.md:349-355`; the diff and history; and the archived packet at `92e1d7a3c815dbf70faa8f0975cc063040edd967:review-evidence/b1-r1` (236 files).

## Verdict

**NEGATIVE.** Most of the evidence holds. The identity gate, the link-drop proof, all ten switch cycles and all ten grandmaster steps re-derive from the archived analyses cell by cell (483 checks, 0 failures). #599 acceptance 4 and #394 acceptance 2 (e1) are supported as PASS.

One MAJOR and two MINOR findings remain open:

- **F1 (MAJOR).** The #387 page records acceptance 4 as PASS, but the evidence meets it only partly. Two things are missing:
  - Every step produced 2-3 `tu` episodes. The recorded contract is one counted event per step.
  - The counted render re-base was not observed.

  The verdict row also claims a 5 s bound that the page's own body disclaims.
- **F2 (MINOR).** Two quantitative claims have no archived artifact or extraction behind them:
  - the peer-delay values in the deviation section;
  - the `asl` seed CRC.
- **F3 (MINOR).** The restore proof leaves out a DUT saved-state residue. The NVM image sequence went 228 to 230 and the pending flag went 0 to 1.

### Acceptance judgement (reviewer's)

| Item | Reviewer judgement | Basis |
|---|---|---|
| Identity gate | PASS | The console CRCs equal the build CRCs: ROM `acad92b9`, QSPI payload `d84bce7b` (seed `eto`), AEM `93742dd2`. VERSION `0x00020060` matches `CHANGELOG.md` at the head. ENTITY and CONFIGURATION are byte-exact (`identity/identity-aecp-comparison.txt`). The CSR map hash equals the page's value, and `milan_mac_link_status` sits at `0xf000181c` (`identity/csr.csv:36`). Grader 10/10. |
| #599 acc. 4, first half (does the link drop?) | PASS: the link drops | In `bench/bmsr-proof`, MAC_STATUS and `link_status` both go `0xd`, `0x0`, `0xd`. The down bracket is 2.31-2.56 s and the up bracket 37.07-37.32 s. No frames arrive from the switch from 5 s until ON. LINKG_STAT, carrier and gPTP corroborate the drop, and LINK_UP/LINK_DOWN go 1/0 to 2/1. The method was disclosed before the run (TAKEN, "material assumptions"): a firmware BMSR poll read-only instead of a direct Clause-22 read. |
| #599 acc. 4 (ten cycles, +1/+1) | PASS | Every cycle shows exactly one down edge and one up edge in both link words, in the same console round. LINK counters are +1/+1 and chain from 2/1 to 12/11. The dry-run and final raw consoles agree round by round (80/80 each). The total of 7,520 console rounds reproduces. |
| #599 acc. 1 poll-period claim | Consistent, not bench-measured | Page line 90 quotes the stated contract (`BAREMETAL_FIRMWARE.md:1971-1972`: 250 ms publication bound, 125 ms trigger). No bench number contradicts it. See S1. |
| #394 acc. 2 (e1) | PASS | Recovery is within the conditions in every cycle: CRF licence `0x3002e3` back, bindings `conn_count` 1 in every poll, asCapable and sync back, DUT MEDIA_LOCKED/UNLOCKED +1/+1. gPTP recovery was 0.544-1.786 s against 5 s and held to the end in every cycle. The event record holds only power actions, and the controller `watch` path is read-only. The restart time is recorded against #75. |
| #387 acc. 4 | **PARTLY MET**; the page's PASS is not supported (F1) | Met: the owner-decision stimulus, ten steps of +9.987/+9.988 ms and -10.003/-10.005 ms on a running locked CRF stream, `mr` unchanged, MEDIA_RESET +0, MEDIA_LOCKED/UNLOCKED +0/+0 on both listeners, `A_MCSRV_STAT` LOCKED in every sample, and `tu` set at the step with its first clear 0.40-0.61 s later on the wire. Not met: one counted event per step (2-3 `tu` episodes at every step, caused by the asCapable loss), and the counted render re-base (not observable). No bound is recorded in item 2 (#387 5859048589). The 5 s recovery bound is context only; step-to-steady was 3.00-4.53 s. |
| Restore | PASS, with an unrecorded DUT residue (F3) | Outlets were as found at start and end. The switch is grandmaster on the console, the wire and the controller. The census shows 53/53 equal. The controller clock returned to its trajectory (4.35 us residual), the temporary files were removed and no daemon runs. The grader passed 10/10. |
| Privacy and Markdown gates | PASS | The project deny-list (`scripts/docs_check.py` SCRUB_RULES) has 0 hits in the pages and the packet. All claimed gates are rc 0 in the pinned environment. See S3 for the packet's interface name. |

## Findings

### F1 - MAJOR - Conformance, Docs - `docs/findings/387_SOFTWARE_GM_STEP.md:12` (also :24, :143, :169, :174-175, :177-205) - #387 acceptance 4 recorded as PASS, but the evidence meets it only partly

**Authority and evidence.**

- The recorded contract:
  - `docs/design/GM_LOSS_RECOVERY.md:144`: "Each step of the step policy is one counted event."
  - `docs/design/TIME_SYNC.md` step policy: "Each step is one counted render re-base."
  - #387 comment 5859048589: "one counted `tu`/`mr`/MEDIA_RESET event per step on a running stream, with no time bound". #602 5859297355 narrows the `mr` and MEDIA_RESET part to `tu` only.
  - `docs/findings/394_387_E1_SWITCH_CYCLES.md:353`: the pending acceptance-4 measurement "must observe the step's counted render re-base and `tu`".
- What the evidence shows (my re-derivation, `receipts/rederive.txt`):
  - All ten steps show 2 or 3 `tu` episodes on the wire.
  - asCapable is lost for 2.0 s at every step.
  - DUT GPTP_GM_CHANGED rises by 3 at 9 of 10 edges, against one grandmaster change per edge.
  - The render re-base is stated as not observable (page :106, :174).
- The verdict cell says the DUT "was steady again 3.00-4.53 s after each step, inside the 5 s bound". The same page says the 5 s bound is "context, not #387's bound" (:143) and that item 2 has "No time bound" (:175).
- The page calls the asCapable loss "the one behaviour outside the contract" (:24). But it is exactly what breaks the one-counted-event contract.

**Impact.** A durable findings page would record #387 acceptance 4 as passed. The step contract is departed from at every step, and the media-side leg of the re-base went unmeasured. That record can support closing #387 on evidence that does not carry it.

**Required outcome.**

- The acceptance row, and the PR body and REVIEW READY summary that mirror it, state a non-PASS verdict ("PARTLY MET" or equivalent). The row names both gaps:
  - `tu` signalled 2-3 times per step instead of one counted event;
  - the counted render re-base was not observed.
- The bound sentence is consistent with the Contract check.
- The deviation is described as a departure from the one-counted-event contract.
- The measurement tables stay byte-identical.

**Verification.** Re-review the delta: only verdict and prose lines change. `scripts/rederive.py` from this packet still passes against the new head.

### F2 - MINOR - Tests, Docs - `docs/findings/387_SOFTWARE_GM_STEP.md:187-191`; `docs/findings/599_394_E1_LINK_CYCLES.md:39` - quantitative claims with no archived artifact or extraction

**Evidence.**

- **Peer-delay values.** The deviation section quotes a published peer delay of 0 ns at all five takeovers, 4,039-4,701 ns at all five releases, and 373-389 ns elsewhere.
  - The analyzer `tools/b1_analyze.py` does not extract `PDELAY_NS`. It keeps GPTP_GM, SYNC, ASCAPABLE, TU, CLKV_STAT and TAI_NS from `milan_status`.
  - No `analysis.json`, summary file or script in the packet contains these values.
  - The `gm01`-`gm05` console captures that would hold them exist only as hashes.
- **`asl` seed CRC.** The identity row says "`asl` reads `809fcffa`". `identity/expected-crc.txt` lists only the `eto` and `eppo` builds.

**Impact.** These numbers underpin the mechanism the page offers for the proposed follow-up issue. A cold reviewer cannot re-derive them from public state, so the claims cannot be checked or falsified.

**Required outcome.** For each claim, do one of the following:

- archive an extraction that reproduces it from the hashed raw captures (the extraction script plus its output), and the `asl` expected-CRC line; or
- qualify the claim in the page as not archived, or remove it.

**Verification.** The archived extraction reproduces the quoted values from captures whose hashes equal the page's raw-artifact rows (the `scripts/verify_hashes.py` pattern).

### F3 - MINOR - Conformance, Docs - `docs/findings/599_394_E1_LINK_CYCLES.md:123,260-278`; `docs/findings/387_SOFTWARE_GM_STEP.md:219-243` - DUT saved-state residue left out of the restore proof

**Evidence** (`receipts/nvm_residue.txt`, from `identity/console-identity.txt` and `restore/console-final.txt`):

| Field | Identity gate | Final restore |
|---|---|---|
| NVM image seq | 228 | 230 |
| Commits ok | 0 | 2 |
| `PP_NVM_STAT` | `c30000e4` (pend=0) | `c34000e4` (pend=1) |
| `PP_STAT` bit 11 (`nvm_pend`) | 0 | 1 |

- `CHANGELOG.md:275-300` at the head describes a sticky pending source that "only reset clears".
- Assignment step 5 requires restoring everything and proving it.
- The #387 page records a controller-host residue (:237-243), but no DUT residue.
- The #599 page says the DUT "was never ... flashed" (:123). In fact, its firmware wrote its saved state to flash twice.

**Impact.** "All restored and proven" overstates the end state. The next bench lane inherits an unexplained pending flag and a moved saved-state image.

**Required outcome.** The restore section records the residue and its cause. It also states whether the saved records equal the as-found records, or proves them benign. It says that the pending flag cannot be cleared without a reset, which the lane was not permitted to perform.

**Verification.** The page text matches `receipts/nvm_residue.txt`.

### Suggestions (optional; no effect on coverage)

- **S1 - Docs - `docs/findings/599_394_E1_LINK_CYCLES.md:98-100,215-216`.**
  - "The poll adds up to one further period" is ambiguous. The contract's stated publication bound is 250 ms, not the 125 ms trigger.
  - The "PHY link dropped/returned" ranges are published-edge brackets.
  - Suggest: "the physical edge may precede the bracket by up to the 250 ms publication bound".
- **S2 - Tests - archived packet.**
  - The per-cycle and per-step raw console, controller and tap captures are held only as hashes. TESTING 6b permits this.
  - The page-format tables `summary/page-*.md` have no generating script in the packet.
  - Archiving the raw files, or a generator, would let a cold reviewer re-derive from raw rather than from the author's extraction.
- **S3 - Docs - archived packet (publication step).**
  - The controller host's interface name appears on 55 lines: port logs, `tools/phc_restore.py` and `gm/slave-test.log`.
  - The tap's capture interface was redacted, and CONTRIBUTING section 6 lists interface names as bench-identifying.
  - It is not a host, peer, switch, instrument or suite name, and both pages are clean.

## Clean-lens evidence

- **[R402] PASS RTL** - `git diff --stat 13eda870..f9eab5bf` (docs only). Also examined:
  - the register decodes in `tools/b1_analyze.py` against `docs/reference/REGISTER_MAP.md` at the head:
    - `:406` MAC_STATUS;
    - `:744` LINKG_STAT;
    - `:783` CLKV_STAT[3] holdover;
    - `:784` CLKV_TUCNT per-interval semantics;
    - `:946` CRFT_CTRL;
    - `:2035` MCSRV_STAT state `[2:0]`, discards `[15:10]` and signed trim `[31:16]`;
  - `identity/csr.csv:36` (`link_status` at `0xf000181c`);
  - the page :90 poll claim against `BAREMETAL_FIRMWARE.md:1971-1977`;
  - the step-policy row (:168) against `TIME_SYNC.md:76-110`. There are exactly two console steps and two wire steps per run, and no re-armed link-up step after the asCapable return (`receipts/rederive.txt`).

  No RTL, firmware or interface contract changed, and the RTL behaviour the pages describe is described correctly.
- **[R402] PASS Robustness** - `receipts/rederive.txt`, `receipts/gm_prep_continuity.txt`, `bench/gm04/analysis.json` `phc_discontinuities`. Checked against the page claims:
  - the gm04 97.8 s cancelling ±2.7 ms console pair is correctly excluded: there is no wire jump;
  - both step signs were exercised;
  - console gaps are at most 0.255 s, and LINK counters are exactly +1/+1, so no sub-bracket bounce was missed;
  - recovery held to the end in every cycle (`gptp_steady_from == gptp_recovered_at`);
  - the alignment phases changed no grandmaster: GPTP_GM_CHANGED is continuous across all five runs;
  - the link-drop proof ran before any bound cycle, and its stop condition was defined;
  - every cycle and run ended at reset epoch 1.

## Completion ledger (reviewer-owned)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 MAJOR, F3 MINOR) | issues #599, #394, #387 acceptance; #387 decisions; #602 ruling; `GM_LOSS_RECOVERY.md:88-245`; `TIME_SYNC.md:76-134`; `BAREMETAL_FIRMWARE.md:1960-1977`; both pages; packet `identity/`, `restore/`, `bench/*/analysis.json`; `receipts/rederive.txt`, `nvm_residue.txt` | R402-1 | f9eab5bf55ca4471e6e48ae3d38018d7e804505b |
| RTL | CLEAN | see PASS RTL line above | R402-1 | f9eab5bf55ca4471e6e48ae3d38018d7e804505b |
| Robustness | CLEAN | see PASS Robustness line above | R402-1 | f9eab5bf55ca4471e6e48ae3d38018d7e804505b |
| Tests | UNCLEAN (F2 MINOR) | packet `tools/` (`b1_analyze.py`, `b1_summary.py`, `b1_action.py`, `a438_controller.py`, `phc_restore.py`); author analyzer re-run on archived raw (`receipts/analyzer_rerun.txt`: 52/52 non-wire fields identical); independent re-derivation (483 checks) with 6/6 planted errors killed (`receipts/mutation_probe.txt`); hash cross-check (`receipts/verify_hashes.txt`) | R402-1 | f9eab5bf55ca4471e6e48ae3d38018d7e804505b |
| Docs | UNCLEAN (F1, F2, F3) | both pages, full text; `receipts/gates.txt` (all rc 0); `receipts/anchors.txt` (32/32 links resolve); `receipts/privacy_scan.txt`; PR body; REVIEW READY | R402-1 | f9eab5bf55ca4471e6e48ae3d38018d7e804505b |

## Receipts and reproduction

All paths are relative to this packet. The scripts take the packet root `review-evidence/b1-r1` (from `92e1d7a3`) and a checkout at the head.

- `scripts/verify_hashes.py` produces `receipts/verify_hashes.txt`.
  - All 100 page raw-artifact rows equal their action's `raw-artifacts.json` entry (size and SHA-256), and no raw jsonl, pcap or log is unlisted.
  - All tool, configuration and grader hashes quoted in the pages match. The grader is checked at the head.
  - Every archived raw copy matches its index.
  - All 235 publication-manifest entries match.
  - The 13 author-manifest mismatches are expected: 3 files were redacted at publication (their original hash is recorded in `MANIFEST.json`), and the pcap and bytecode files were not published.
  - The image and tarball hashes are not verifiable from the packet: they are listed as INFO.
- `scripts/rederive.py` produces `receipts/rederive.txt` (483 PASS, 0 FAIL). `scripts/mutation_probe.sh` produces `receipts/mutation_probe.txt` (6/6 planted errors caught).
- `scripts/compare_rerun.py` produces `receipts/analyzer_rerun.txt`. The author's analyzer was re-run on the archived dry-run and final raw files, with the path patched in a scratch copy.
- `scripts/gm_prep_continuity.py`, `scripts/nvm_residue.py`, `scripts/privacy_scan.py`, `scripts/check_anchors.py` and `scripts/run_gates.sh` produce their same-named receipts. `receipts/gm_return_kind.txt` reproduces "Sync in six, Announce in four".
- `scripts/verify_clone.sh` produces `receipts/verify_clone.txt`.
  - HEAD and tree are exact, and the index writes the tree.
  - All 966 tree entries match in blob bytes and mode.
  - The initialised gitlinks match: `gptp-processor` 5dce647a, `protocol-processor` c951a9ff, `third_party/verilog-axis` 48ff7a7e.
  - `external` (efeb541a) is uninitialised in this clone and unchanged by the PR.
  - There are no untracked or ignored files.
- `receipts/hosted_checks.txt` is a snapshot of the exact-head check runs.
  - Executed and green: `rtl-fast`, `changes`, `full-ci-gate`, `elaborate`, `bdd-conformance`, `docs-check-no-git`, `wire-accountability`.
  - `docs-check` was in progress at the snapshot.
  - Skipped contexts, which are not evidence: `verilator-suites`, `yosys-portability`, the shards, `verilator-lint`, `yosys-elaboration` and Physical gPTP.
- Gates: `docs_check`, `check_doc_style`, `gen_toc --check`, `check_em_dash --base 13eda870` and `--selftest`, `check_doc_paths` and `ci_scope --selftest` were run with the pinned lock (`cmarkgfm==2025.10.22`, `html5lib==1.1`, installed with `--require-hashes` into a scratch environment). `check_baremetal_only --check` needs PyYAML, which that lock does not carry, so it ran with the system interpreter (0 findings over 936 files). `check_feature_status --self-test` and `git diff --check` also ran. All are rc 0.

## Real limits

- The per-cycle and per-step raw captures are not public, so the cycle and step tables were re-derived from the author's archived `analysis.json`, not from raw. The analyzer was shown to reproduce its own output from raw only for the two actions whose raw console and controller files are archived. Wire-derived fields (tap) could not be re-run at all, because no pcap is archived.
- The build directories the expected CRCs come from are tied to dev `13eda870` by their names and by the assignment's statement. I did not rebuild the image (builder banks are out of scope).
- "No re-bind" rests on the event record and the read-only `watch` path. The per-cycle controller transcripts are not archived.
- The scoped simulator was not used, because the diff has no RTL. Its identity was therefore not checked.
- Physical calibration was NOT RUN. No hardware was touched by this review. Skipped hosted contexts are not hardware or simulation proof.

## Prior public review findings

At head `f9eab5bf`, before the review started, the PR carried only the two review-start notices (R402-1 and R403-1) and no findings. There is nothing to resolve or retain.

## Pending manager duties

- Disposition F1-F3, then re-review at the corrected head.
- File the proposed follow-up issue: asCapable is lost for 2.0 s after every PHC step. That defect stays in the tree whatever this page says.
- Decide how #387 acceptance 4 is recorded given F1: partly met, with the render re-base leg still owed.
- Own hosted and act acceptance: `docs-check` was still in progress at the snapshot.
- Obtain the second independent review (R403-1).
- Build and validate the current-dev candidate (source base 13eda870, live dev 8e2967f9) at the merge turn.
- Route the `docs/findings/README.md` index entries for the two pages. The assignment forbade other doc edits.
- Publish this packet: only `REPORT.md` and the files listed in `MANIFEST.sha256`.

R402-1 FINISHED
