[R265] NEGATIVE - exact head f547a49bee5966a901d1e11981eb4dc94d038711

Round R265-2, external independent review of issue #117 / PR #531, cleared context.

- Head `f547a49bee5966a901d1e11981eb4dc94d038711`, tree `27e6488d3da9669f787662d49e40f2263995dcb7`.
- Source base `ede8d48ecd7c7f589a14b957951f040d92c99c70`, an ancestor. Four commits, each one line with no trailers (`receipts/rtl-lens.txt`).
- Diff: `docs/findings/117_GPTP_SILICON_EVIDENCE.md` (A), `docs/design/GM_LOSS_RECOVERY.md` (M), `docs/findings/README.md` (M). No HDL, firmware, constraint, config or gitlink change.
- Evidence archive pinned by the page: branch `117-review-evidence`, commit `32aec66197ba78ee431c27383bb958e5728c270a`, path `review-evidence/117-r1`.
- All five lenses applied: Conformance, RTL, Robustness, Tests, Docs.

## Verdict summary

Every R264-1 and R265-1 finding is closed at this head:

- the bare-metal-only gate passes locally and in the hosted `docs-check` job, where all 51 steps executed and succeeded;
- the corrected statements match the raw packets;
- the stale row now carries step 3 evidence that I re-derived;
- the links resolve;
- all 74 raw-artifact hashes name files at the pinned commit.

All seven required contexts are successful at this exact head.

I re-derived the bench evidence with my own standard-library decoders. The sources were the redacted captures, console transcripts, controller logs and power-strip logs. Every page value I sampled reproduces exactly or within 0.01 s:

- identity gate and step 2;
- all 13 columns of the step 3 table, the loss edges and the controller view;
- stream and `tu` behavior, and the PHC steps;
- steps 4 and 5.

The redacted captures still parse.

The head is still not mergeable:

- **F1 (MAJOR).** The pinned archive still publishes the reference peer's product name, vendor name and device serial number. They are hex-encoded in four unredacted files. The page says the archive was redacted of exactly those classes.
- **F2 (MINOR).** The Tool revisions paragraph says three tool files are published redacted. At the pinned commit there are four.

## Findings

### R265-2-F1 MAJOR - Docs, Conformance, Robustness - the pinned archive still carries the reference peer's identity and serial

Locations:

- `docs/findings/117_GPTP_SILICON_EVIDENCE.md:536`, with `:129` and `:530-533`;
- archive `32aec661`, under `review-evidence/117-r1/`:
  - `bench-a200/bench/peer-aem-1.jsonl`;
  - `bench-a200/bench/final/census-final.jsonl`;
  - `bench-a202/bench/census-start.jsonl`;
  - `bench-a202/bench/final/census-end.jsonl`.

The strings are hex-encoded, and the page's redaction statement says they were removed.

**Authority:**

- CONTRIBUTING.md section 6 (lines 532-545):
  - bench equipment is named by role, never by vendor or product;
  - no bench-identifying information, including serials.
- `scripts/docs_check.py` IDENTITY_RULES classes "peer product name" and "bench-switch vendor name".
- The page, line 536: "73 files are published redacted: local paths, and bench-identifying strings (equipment names, device serials, host names) under CONTRIBUTING section 6."
- The manager's rewrite note: the rewrite removes "equipment vendor and product names, device serials, host names, USB serial paths".

**Evidence** (`receipts/identity-scan.txt`, `receipts/redaction-status-selected.txt`):

- The token set is derived from what the redaction itself replaced: the scan diffs the pre-redaction commit `160debeb` against `32aec661`. No token is spelled in this packet.
- Three tokens the redaction replaced elsewhere are still present as lowercase hex in the four files:
  - token#2 (4 characters): the peer product name;
  - token#7 (12 characters): the vendor name;
  - token#5 (13 characters): a device serial, replaced elsewhere with `<device-serial>`.
- They are the reference peer's ENTITY descriptor fields `entity_name`, `group_name` and `serial_number`, inside the READ_DESCRIPTOR payload hex.
- All four files are published unredacted: in `MANIFEST.json`, original SHA-256 equals published SHA-256.
- The same strings in text form were redacted. For example, the peer's entity dump `bench/runC/entity_0x3cc0c60102030000.json` is identity-redacted at `32aec661`.
- The page sends readers to these files:
  - line 129 points to `bench/peer-aem-1.jsonl` for the raw ENTITY bytes;
  - lines 564, 576 and 577 list the three census files as primary artifacts.
- The pinned-history ancestors `6b14c6c0` and `204879ff` carry the same two A200 files.
- The serial number appears in no issue #117 or PR #531 text, in either raw or hex form.
- The PR tree itself is clean: the `docs_check.py` scrub finds 0, and the token scan finds 0 in the three changed files.

**Impact:**

- The pinned evidence exposes the reference peer's product identity and device serial. That defeats the stated purpose of the 2026-09-23 rewrite, and makes line 536 inaccurate.
- The redaction handled the text representation of these fields but not the hex-payload representation of the same data. That is why the finding is also filed under Robustness.
- A correct re-redaction moves the pin and changes the page's own counts, so the page cannot stand as written:
  - redacted files go from 73 to 77;
  - "26 of them" goes to 29, because three of the four files are raw-artifact table rows.

**Required outcome:**

- No file at the pinned commit, or in its pinned history, carries these strings in any encoding: raw, hex or capture bytes.
- The peer firmware-field hash on line 129 stays reproducible, or the page says it does not. That field is not an identity string.
- The pin, the redaction statement and the counts match the new archive.
- `MANIFEST.json` maps every changed file.

**Verification:**

- `scripts/scan_identity.py <pre-redaction> <new pin> <clone>` reports 0 residual hits over the new pin and its ancestors.
- `scripts/verify_archive.py` reports PASS.
- `scripts/page_hashes.py` reports PASS, with the page's counts equal to the script's.

### R265-2-F2 MINOR - Docs, Conformance - the Tool revisions paragraph names three redacted tool files; four are redacted

Location: `docs/findings/117_GPTP_SILICON_EVIDENCE.md:220-223`. At the pinned commit, four Tool revisions hashes name files that are published only in redacted form.

**Authority:**

- Issue #117 acceptance box 5: exact hashes and tool revisions.
- The page's own box 5 row (line 58) says Tool revisions tells the reader which hashes name files outside the published bytes.

**Evidence** (`receipts/redaction-status-selected.txt`, `receipts/page-hashes.txt`):

- Line 216 quotes `analyze_cycle.py` as `bdd228a1...`.
- At `32aec661` that file is path- and identity-redacted, so its published SHA-256 begins `2ca45609`.
- At `160debeb` the same file was published unredacted. The re-pin in `f547a49b` therefore made lines 220-223 stale. They still say: "Three of those files are published with local paths redacted: the enumerator binary, `run_cycle.sh` and `cycle_locked.sh`".
- Two of those three are now identity-redacted as well.

**Impact:** a cold verifier who hashes `tools/analyze_cycle.py` at the pin gets a different value from the quoted one, while the page's explicit list says that file is unredacted. Box 5 traceability depends on this paragraph.

**Required outcome:** the paragraph names every Tool revisions hash whose file is published only redacted, or it defers to `MANIFEST.json` without a wrong list.

**Verification:** every abbreviated tool hash equals its published file's SHA-256 or is named as redacted. Check against `MANIFEST.json` and `scripts/page_hashes.py`.

### R265-2-S1 SUGGESTION - Docs - docs/findings/117_GPTP_SILICON_EVIDENCE.md:415, :477

- Observation 3 and the step 4 row set "FRAMES_TX 16" beside 34,061 PDUs as a disagreement ("... do agree with the wire").
- The #530 decision of 14:52 UTC predates this head. It explains item 3 as the documented Milan Table 5.4 semantics, not a defect:
  - FRAMES_TX counts one-second observation intervals and resets at STREAM_START;
  - the last 15.00 s burst spans 16 intervals.
- Item 9 on the page already records that behavior. Citing the #530 disposition would stop readers counting item 3 as an open defect.

Optional.

### R265-2-S2 SUGGESTION - Docs - docs/findings/117_GPTP_SILICON_EVIDENCE.md:138, :418

- Line 138 says "Times below are the build box's UTC".
- The millisecond Run B times on line 418 (13:04:49.297 and 13:05:59.198) are the capture server's NTP times. They equal the first and last CRF host stamps in `receipts/step2-rederived.txt`.
- The bind at 13:04:49 is on the controller host's NTP clock.

This is inside the page's 1 s disclaimer, so no conclusion changes. Labelling the clock would help. Optional.

### Carried SUGGESTIONs (optional, not taken)

- R264-1 F5: cite the 30 % and 800 ns limits and the 2026-09-20 record.
- R264-1 F6: mark the operational reading of "the grandmaster's return", and give the index row's full state.
- The rest of R265-1 S2: the per-cycle fit windows and slope. The page now states the 2.02 ms residual.

## Prior public findings at this head

I read R264-1 (PR comment 5798410684) and R265-1 (PR comment 5798463789) only after my independent pass. Each is checked at this head against the raw evidence or the tree.

| Prior finding | Status at f547a49b | Evidence |
|---|---|---|
| R264-1 F1 / R265-1 F1 BLOCKER: bare-metal-only gate red | CLOSED | Locally, `check_baremetal_only.py --check` reports OK with 0 findings across 839 files (`receipts/doc-gates.txt`). Hosted `docs-check` job 107294772483 at this head ran 51/51 steps successfully, including step 21 "Bare-metal scope gate" (`receipts/hosted-docs-check-steps-f547a49b.tsv`). |
| R264-1 F3-A / R265-1 F2.3: dark window | CLOSED | Line 337 says 1.03 to 1.75 s, until 37.55 to 38.57 s. Re-derived: 1.03 to 1.76 s, then 37.56 to 38.58 s. The last record in each cycle is a DUT frame, a Pdelay_Req in cycle 2 (`receipts/step3c-rederived.txt`). |
| R264-1 F3-B / R265-1 F2.2: holdover | CLOSED | Line 322 says 3 to 5 samples over 0.30 to 0.50 s. Re-derived: 3/3/5/3/4/4 samples and 0.30/0.30/0.50/0.31/0.41/0.41 s (`step3c`, `step3b`). |
| R264-1 F3-C: "read-only AECP only" | CLOSED | Lines 47 and 392-395. The console carried 38,954 commands in 14 transcripts, all `milan_status`, `mem_read`, `mem_list` or `crc` (`receipts/console-census.txt`). |
| R264-1 F3-D / R265-1 F2.1: envelope-less records | CLOSED | Line 134. Re-derived: 76 in Run A; 38/0/38/45/0/37 in step 3; 18 in the step 3 final capture; 0 elsewhere. All 19 tcpdump logs report 0 dropped (`step2`, `step3`, `step3c`, `console-census`). |
| R265-1 F2.4: census | CLOSED | Line 501 now records the `stream_dest_mac` change. |
| R265-1 F2.5: daemon check scope | CLOSED | Line 45 names the two hosts that were checked. |
| R265-1 F3: stale "reaches asCapable" row | CLOSED | Line 41 is now PASS with a stated criterion. Re-derived: `CLKV_STAT[16]` rises 0.02 to 0.09 s after the DUT's second completed Pdelay exchange, within one 0.1 s sample. That is 1.02 to 1.64 s after the switch's first frame, with PDELAY 377 to 389 ns (`receipts/misc-checks.txt`). |
| R264-1 F2 / R265-1 F4: follow-ups | CLOSED | Items 1 to 3 and 9 link #530. Items 4 to 6 link #495, whose checklist carries them (`receipts/followups.txt`). Items 8 and 10 carry a reasoned "no issue" disposition. Items 7, 11 and 12 are bench facts. #529 is linked at lines 53 and 463. The PR body matches. |
| R264-1 F4: box 5 traceability | CLOSED on its stated points. The privacy clause is superseded by R265-2-F1. | The pinned locator is present. The narrowed "full hashes" sentence is true: `95d64fd5`, `ad579e18` and `0e9faf30` have full values on comment 5584039577, and `8ef4b008` has none, as stated. Build hashes are accounted for against `expected-crc.txt` and comment 5794859125. The new line 536 and lines 220-223 are not accurate (F1, F2). |
| R265-1 S1: point at the public mirror | TAKEN | Lines 528-537. |
| R265-1 S2, R264-1 F5, R264-1 F6 | Optional, carried | See above. |
| R265-1 manager duty: mirror hygiene | PARTLY DONE | Redacted: host names, capture interface names and USB serial paths. Not redacted: the peer ENTITY descriptor strings, including the serial (F1). The controller EUI-64 is unchanged (see limits). |

## Independent re-derivation (page against raw artifacts at 32aec661)

| Area | Page | Re-derived | Receipt |
|---|---|---|---|
| Archive integrity | 73 redacted; MANIFEST.json maps each | 236 entries plus MANIFEST.json itself; 73 differ from the original (67 identity, 6 path-only); every published hash matches its bytes. Packet manifests list originals, 81/81 and 153/153. The 11 path-redacted at `160debeb` were never public as run. 20/20 redacted captures keep their length. | archive-verify.txt |
| Page hashes | 74 rows resolve; 26 redacted | 74/74 resolve in the right packet; 26 name redacted files. Non-archive hashes are each accounted for as the page says. The grader hash equals the `ede8d48e` blob. | page-hashes.txt |
| Identity | ROM `f6afa4ec`, QSPI `02036e95`, AEM `93742dd2` | Both readbacks equal the `asl` row of `expected-crc.txt`, which is byte-identical in both packets. | (read directly) |
| Step 2 | 4,556, 565, 564 and 566 intervals; exchanges 568/568 and 570/570; 10,984 to 11,009 ns; 18.33 and 18.36 ms | Identical. Medians of tap minus claimed: 383 to 391 and 393 to 394. 570 s tapped; 569 Announces; PathTrace `[GM]`; Announce fields as on line 127. | step2-rederived.txt, announce-fields.txt |
| Retention | 116/116 samples; 60/60 polls; PDELAY 380 to 391 ns | Identical. AECP 381 to 391, median 385; flags `0x17`. | misc-checks.txt |
| Run B | 34,061 CRF, all `tu=0`; bursts 19.67, 18.45, 15.00 and 15.00 s; pauses 1,106, 578 and 148 ms | Identical. Sequence continuous; PCP 3, VID 2. | step2-rederived.txt |
| Step 3 table | 13 columns by 6 cycles | Every cell within 0.01 s. Recovery 0.51, 0.51, 1.51, 0.42, 1.46 and 1.60 s, against the page's 0.51, 0.52, 1.51, 0.43, 1.46 and 1.60 s. | step3-rederived.txt |
| Loss edges | 0.40 to 0.46, 3.01 to 3.08 and 5.0 to 5.1 s | 0.40 to 0.46, 3.00 to 3.07 and 5.02 to 5.09 s | step3b-rederived.txt |
| TUCNT and PHC | +40, 39, 41, 40, 40 and 41; steps of -128.5 to -355.9 s | Identical. Each step equals the on-to-on interval. | step3b-rederived.txt |
| Stream, cycles 4 to 6 | first `tu=1` at 1.08, 1.07 and 1.00 s; 316, 293 and 243 PDUs; all `tu=0` after return | 1.09, 1.07 and 1.00 s; 316, 293 and 243; all `tu=0`. Licence edges fall within one poll of the page. | step3b-rederived.txt |
| Controller view | peer table; +2 GPTP_GM_CHANGED; ADP 39.84 and 41.65 s; AS_CAPABLE while GM is the DUT in cycles 1, 3 and 6 | Identical. | step3-controller-rederived.txt |
| Step 5 | probe parity; DUT downgraded; peer IEEE17221 and Milan | Transcripts identical apart from the entity ID; the log lines are present. | misc-checks.txt |
| Peer firmware hash | 7 octets, `33f0e7f9...` | Recomputed from the raw ENTITY bytes. | (read directly) |

## Per-lens results

**RTL:**

```text
[R265] PASS RTL - receipts/rtl-lens.txt (git diff --raw ede8d48e..f547a49b; gitlinks equal base); docs/reference/REGISTER_MAP.md:730, :731, :770, :771, :875, :880, :942, :1161, :1347, :1392; receipts/hosted-check-runs-f547a49b.tsv - docs-only diff; the page's CSR decodes (CLKV_STAT 0x00010002 bits 0/1/3/16, CRFT_COUNT 0x850D = 34,061, GPTP_LAT 656/219 ns, ASP_CMD 0x11, LINKG_STAT bit 7) match the register map; exact-head elaborate, rtl-fast, verilator-suites (5 shards executed) and yosys-portability (4 shards executed) successful
```

**Tests:**

```text
[R265] PASS Tests - receipts/step2-rederived.txt, step3*.txt, misc-checks.txt, announce-fields.txt, console-census.txt, doc-gates.txt, hosted-docs-check-steps-f547a49b.tsv - every sampled page claim reproduced by an independent decoder that could fail; 16 local docs-workflow gates rc 0 at this head, the bare-metal-only gate included; hosted docs-check 51/51 steps executed and successful; the regeneration script reproduced every derived receipt byte for byte
```

**Conformance: UNCLEAN (F1, F2).** Judged against:

- the frozen acceptance;
- the owner decisions 5561827955, 5565246390, 5789767491 and 5795898094;
- BUILDING.md 4.1;
- CONTRIBUTING section 6.

The box results re-derive, as the table above shows. The asCapable partner being the bench switch is consistent with BUILDING.md 4.1, which says GM loss and return are induced "through the peer or the bench AVB switch". The page discloses that reading at lines 60-64. The recovery-bound section matches the owner's text: 3 + 0.375 + 1.625 = 5 s, the Milan intervals, and media within one further restart.

**Robustness: UNCLEAN (F1).** The redaction does not handle the hex representation of the same fields. Everything else is clean at this head:

- the aborted attempt is excluded and recorded;
- all 19 capture logs report 0 drops;
- envelope-less records are counted and excluded;
- `RST_EPOCH` reads 1 throughout, and the largest console gap is 0.113 s;
- each return costs one stream restart;
- clock-mapping error cannot move the verdict: the margin to the bound exceeds 3 s, and my simpler fit agrees within 0.01 s.

**Docs: UNCLEAN (F1, F2).** Everything else examined is clean:

- 16 gates rc 0: docs_check, em-dash (0 over 665 added lines), doc style, gPTP docs with and without the submodule, solution, submodule, bare-metal, doc paths, archive, TOC check and anchors, feature status, hygiene, TODO ownership, and test evidence;
- the issue links and comment anchors resolve;
- the index row and the recovery-bound section are consistent;
- the PR tree passes the privacy scrub and the token scan.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 MAJOR, F2 MINOR) | #117 acceptance and owner decisions; BUILDING.md 4.1; CONTRIBUTING section 6; GM_LOSS_RECOVERY.md:88-118; the box table against archive 32aec661 (identity, runs A/B/C/final, cycles 1-6, attempt 1) | R265-2 | f547a49bee5966a901d1e11981eb4dc94d038711 |
| RTL | CLEAN | diff --raw (3 Markdown files, gitlinks equal base); REGISTER_MAP rows listed above; exact-head hosted elaborate, rtl-fast, verilator-suites, yosys-portability | R265-2 | f547a49bee5966a901d1e11981eb4dc94d038711 |
| Robustness | UNCLEAN (F1 MAJOR) | attempt 1 (aborted); 19 tcpdump logs; host-record exclusion; RST_EPOCH and console gaps; stream restart per return; clock-fit sensitivity; redaction coverage across raw, hex and capture encodings | R265-2 | f547a49bee5966a901d1e11981eb4dc94d038711 |
| Tests | CLEAN | independent re-derivations for steps 2 to 5; 16 local docs gates; hosted docs-check steps; byte-identical receipt regeneration | R265-2 | f547a49bee5966a901d1e11981eb4dc94d038711 |
| Docs | UNCLEAN (F1 MAJOR, F2 MINOR) | 117_GPTP_SILICON_EVIDENCE.md, GM_LOSS_RECOVERY.md, findings/README.md and the PR body; archive MANIFEST.json and packet manifests; issues #110, #116, #495, #529, #530, #64, #213 and the #117 anchors | R265-2 | f547a49bee5966a901d1e11981eb4dc94d038711 |

SUGGESTIONs do not affect coverage. Fixing F1 and F2 changes the page, so Conformance, Docs and Robustness must be covered again at the new head. Tests and RTL stay banked at this head only until something in their scope changes.

## Real limits

- **No hardware access.** No bench, JTAG, console or power control was available. Physical calibration is NOT RUN, and field or hosted skips are not hardware proof. As the page states, these are also NOT RUN: the peer's own recovery time, the first reach after the flash, Hive, behave, latency and audio.
- **Build artifacts are not public.** Bitstream identity rests on a CRC32 readback. As the page says, the `bios.bin` and `csr.csv` hashes are recorded only on the page.
- **Eleven files were never public as run.** They were already path-redacted at `160debeb`. I checked them for manifest consistency only.
- **The identity scan's tokens come from what the redaction changed.** A private string the redaction never touched in any form would not be derived. The repository's SCRUB_RULES were applied as well.
- **Capture-tap product name.** Counted separately: 4 archive tool files, and 15 tracked files of the head tree (for example `docs/testing/TESTING.md:732`). It is in none of the three changed files. It is pre-existing and already public in the repository, so it is not filed against this head.
- **Left to a manager decision, not filed.**
  - The MAC inside the redacted interface name is still present, raw or hex, in 6 archive files.
  - The controller host's EUI-64 appears 833 times.
  - Archive file names keep the controller host's short role name, which BUILDING.md 4.1 publishes.
  - CONTRIBUTING section 6 lists interface names, not MAC or EUI-64 values, and the tree already commits bench clock identities.
- **My tap-to-host fit is simple.** It is an unweighted per-5 s-minima line, with a residual of up to 74 ms in one cycle. Every step 3 cell still agreed within 0.01 s. Two sub-sample differences:
  - The page stamps the `CRFT_CTRL` licence edges at the poll's `milan_status` send time, 0.07 to 0.08 s before the `mem_read` itself, which is within one console sample.
  - The single 2.73 s `LINKG_STAT` figure spans 2.69 to 2.77 s across cycles, which is also bounded by the sample.
- **Not run.** The scoped Verilator (the diff is docs-only, so no simulation was needed); any full bank, builder, Yosys, act or Docker job; any hardware step.
- **Bank evidence not inspected.** The manager's source static/builder and native bank results for this head are not in the public tree I was pointed to: `160debeb/review-evidence/117-r1` holds only the bench packets.
- **Clone restored and verified** (`receipts/restore-verify.txt`):
  - HEAD and tree exact, and the index equals the HEAD tree;
  - 865 tracked blobs byte- and mode-identical;
  - 4 gitlinks at their pins, with the two processor submodules initialized as found;
  - `status --porcelain --ignored` empty;
  - the bytecode cache my runs created under `scripts/` was removed.
- **Read order.**
  - The prior findings, the manager's assignment 5798470752 and the author's record 5798715557 were read only after the independent pass. That pass is recorded in the report skeleton: F1, S1 and S2.
  - F2 was found afterwards, while checking the page's traceability statements against `MANIFEST.json`.
  - Robustness was added to F1's lenses in the final pass, so the skeleton's draft ledger differs from this one on that lens.
  - No other reviewer's packet was read, nor the archived review directories on the evidence branch tip.

## Pending manager duties

- Re-redact the ENTITY descriptor string fields in the four files and re-pin (F1). Update line 536, the counts, and lines 220-223 (F2). Then rerun `scripts/scan_identity.py`, `verify_archive.py` and `page_hashes.py` from this packet.
- `160debeb` and its pre-rewrite ancestors are still served by SHA through the public API (`receipts/archive-commits.txt`). PR comment 5799413596 and this round's brief both name it. Rewriting the branch does not withdraw those commits. Decide whether to request removal from the hosting provider.
- Decide the MAC, EUI-64 and tap-product-name questions in the limits. The tap name is a tree-wide inconsistency with CONTRIBUTING section 6 that `docs_check.py` does not gate, so it would be a separate Issue.
- At the corrected head, obtain exact-head hosted required contexts again. All seven succeeded at this head.
- At the merge turn:
  - run act against live `dev` `759da623`;
  - build and validate the candidate merge;
  - run the containment check.
- Wait for the in-flight internal round R264-2. Obtain two positive reviews and a reviewer-accepted ledger.
- Publish the source static/builder and native bank evidence for this head, if it is to count as public evidence.

## Receipts (listed in MANIFEST.sha256)

`scripts/run_all.sh <clone at f547a49b> <workdir>` regenerates every derived receipt from the public repository. A rerun reproduced them byte for byte; only the scan's directory labels differed.

**Scripts:**

- `tapdec.py`;
- `verify_archive.py`, `page_hashes.py`;
- `scan_identity.py`: tokens are derived, never spelled, and hits are reported by index;
- `step2.py`, `step3.py`, `step3b.py`, `step3c.py`, `step3_ctl.py`;
- `misc_checks.py`, `announce_fields.py`, `console_census.py`;
- `restore_verify.py`.

**Receipts:**

- archive: `archive-verify.txt`, `page-hashes.txt`, `identity-scan.txt`, `redaction-status-selected.txt`, `archive-commits.txt`;
- re-derivations: `step2-rederived.txt`, `step3-rederived.txt`, `step3b-rederived.txt`, `step3c-rederived.txt`, `step3-controller-rederived.txt`, `misc-checks.txt`, `announce-fields.txt`, `console-census.txt`;
- gates and tracking: `doc-gates.txt`, `rtl-lens.txt`, `followups.txt`;
- hosted and restore: `hosted-check-runs-f547a49b.tsv`, `hosted-docs-check-steps-f547a49b.tsv`, `restore-verify.txt`.

R265-2 FINISHED
