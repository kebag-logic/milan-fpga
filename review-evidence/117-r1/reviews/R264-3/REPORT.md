[R264] NEGATIVE - exact head 8016f7ac843b0ae6764dc4ec0140cda5ac7d6cc1

Round R264-3. Internal independent review of issue #117 / PR #531, run with cleared context.

- Head `8016f7ac843b0ae6764dc4ec0140cda5ac7d6cc1`, tree `fe7079365e3d61364b7d6602a6e3abab20c1d222`.
- Source base `ede8d48ecd7c7f589a14b957951f040d92c99c70`.
- Evidence pin `74ac94e8eb331202f39d66cc006bc2640481e6da`. Evidence branch tip `4165beb89afe217931bc52a8aaf800303e7bee1b`.

I applied all five lenses at this head. My verdict and ledger were written before I read any prior review. Reading R264-2 and R265-2 afterwards changed neither.

## Verdict in brief

The corrections for R264-2 F1/F2/S2 and R265-2 F1/F2 are real, and I reproduced them from the raw packets:

- The peer's identity fields are gone from the pin and from all eight evidence-branch commits, in raw, hex, base64 and UTF-16 form. That includes capture bytes.
- Every page hash resolves through `MANIFEST.json`.
- The counts 77 / 6 / 71 / 20 / 57 / 29 match the archive.
- The Tool revisions paragraph is exact.
- No PR commit links a superseded archive.

Two defects remain. Both concern the privacy claims, not the measurements:

- **F1, MAJOR.** The pin still publishes the DUT console USB-UART adapter's USB serial number, in three redacted scripts. The masking removed only the part of the `/dev/serial/by-id/` path that the repository's detector regex matches. Page line 539 says USB serial paths are masked. CONTRIBUTING section 6 names USB serials as bench-identifying.
- **F2, MINOR.** Page line 129 publishes the full SHA-256 of the zero-padded firmware field. The page lists that firmware string as a withheld identity field that is "kept privately". An enumeration of 2.1 million version-shaped candidates finds the unique preimage in seconds, so the PR tree carries the value in a recoverable encoding. A merge to `dev` cannot be undone, so the owner's decision on whether this value is private must come first.

## Reconstruction order and authorities read

1. AGENTS.md sections 3 to 8. CONTRIBUTING.md sections 2 and 6 (privacy rules, lines 524-551). docs/README.md.
2. Issue #117 body and scope decisions: 5561827955 (one DUT), 5565246390, 5789767491, 5794146393, 5794354283, 5794950660, 5795898094 (the 5 s bound and switch power-cycling), 5798470752.
3. Authorities:
   - docs/reference/REGISTER_MAP.md;
   - docs/reference/MILAN_COMPLIANCE_MATRIX.md rows 4.2.6.1.1 and 4.2.6.2.6;
   - `hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv`;
   - `scripts/docs_check.py` `IDENTITY_RULES` and `LOCAL_RULES`.
4. `git diff ede8d48e..8016f7ac`: three files, docs only, no gitlink change. History: c3eb95fa, 0abf147f, 8016f7ac. I also read the full `0abf147f..8016f7ac` correction diff.
5. The evidence at the pin and on the branch. Manager comments 5799413596, 5800264651 and 5801260231. The exact-head hosted check runs.
6. Only after the verdict: R264-1 (5798410684), R265-1 (5798463789), R265-2 (5800161462) and R264-2 (5800196179).

## Findings

### F1 - MAJOR - Conformance, Robustness, Tests, Docs

`[R264] MAJOR Conformance, Robustness, Tests, Docs - docs/findings/117_GPTP_SILICON_EVIDENCE.md:539; evidence pin 74ac94e8 review-evidence/117-r1/bench-a200/tools/run_a.sh:9, bench-a200/tools/run_b.sh:8, bench-a202/tools/cycle_locked.sh:9 - the pinned archive still publishes the console adapter's USB serial number; only the detector-matched prefix of the by-id path was masked`

**Requirement and evidence**

- **The rule.** CONTRIBUTING.md:542-545 says: "No bench-identifying information: hostnames, home paths, bench subnets, USB serials, interface names." The repository's placeholder is `/dev/serial/by-id/<adapter>`, for example `docs/integration/BUILDING.md:455`.
- **The page's claim.** Line 539 says the 71 identity-redacted files "have bench-identifying strings masked: ... MAC-derived interface names and USB serial paths".
- **What the pin carries.** In all three files the line reads `/dev/<adapter>` followed by the rest of the by-id name.
  - That remainder is the adapter's vendor and product string, then its 32-hex-digit USB serial number, then `-if00-port0`.
  - The placeholder replaced exactly the text that `scripts/docs_check.py` `LOCAL_RULES` matches: `serial/by-id/usb-` plus one character.
  - The masked text therefore no longer trips the detector, but the identifier is still there (`receipts/sweep-evidence-branch.txt`, token L3).
- **Where else it appears.** The residue is in 7 of the 8 evidence-branch commits: 6af416d1 and c615dbba carry two of the files, and 74ac94e8 through 4165beb8 carry all three (`receipts/usb-serial-per-commit.txt`).
  - Only the empty packet opener 5ff947b4 is clean.
  - The PR tree carries none of it (`receipts/sweep-pr531.txt`).
- **Classification in the manifest.** `MANIFEST.json` marks all three files `identity_redacted`, and the page counts them among the 71.

**Lenses**

- Conformance: the evidence the page pins breaks CONTRIBUTING section 6.
- Docs: line 539 states a masking the bytes do not show.
- Robustness: the masking removed only the matched prefix, not the identifier.
- Tests: the check that backs the statement cannot fail for this defect. The detector passes by construction on text masked to its own match. The published 0-hit sweep (5800264651) covered only the reference peer's fields.

**Impact**

- A bench-identifying serial stays public on the branch that the merged page would permanently link as its evidence locator.
- The page's privacy statement is inaccurate for a class it names.
- This is the same kind of gap the two earlier rewrites closed for other classes.

**Required outcome**

- No file at the pinned commit, and no file in its pinned history, carries the adapter's USB serial number or the by-id remainder that embeds it, in any encoding.
- The whole by-id name is masked, as the repository's own placeholder does.
- `MANIFEST.json` maps every changed file. The page is re-pinned to the new commit, every quoted hash still resolves, and line 539 stays exact.
- Other identifiers the same regex-prefix masking touched are checked to their full extent. The host prefix and the MAC-derived interface names are already fully masked (tokens L1 and L2: 0 hits).

**Verification**

- `scripts/run_all.sh` at the new head and pin: token L3 reports 0 files at every branch commit in `usb-serial-per-commit.txt`.
- Also a raw search of the new pin for `by-id` remainders that end in a hex serial.
- `page-vs-archive.txt` reports `RESULT fails=0`.

### F2 - MINOR - Conformance, Robustness, Docs

`[R264] MINOR Conformance, Robustness, Docs - docs/findings/117_GPTP_SILICON_EVIDENCE.md:129 (with :539) - the page publishes a digest that recovers the peer firmware string it says is withheld`

**Requirement and evidence**

- Line 539 lists the "firmware string" among the reference peer's identity fields that are masked "in text and in hex payloads".
- Line 129 says "the original is kept privately", yet publishes the full SHA-256 of the 64-octet zero-padded `firmware_version` field.
- The field holds seven octets. I confirmed the digest against the bytes of the superseded original archive, and it matches the page (`receipts/superseded-original-checks.txt`, value withheld).
- `scripts/fw_digest_enumeration.py` enumerates 2,121,000 version-shaped candidates and finds exactly one match. The value is withheld in the receipt (`receipts/fw-digest-enumeration.txt`).
- The earlier rounds disagreed on the value's status:
  - R264-2 proposed citing the hash "as recorded", with the original kept private.
  - R265-2 said the firmware field "is not an identity string".
- The page adopted the "private" reading but chose an encoding that does not keep the value private.

**Impact**

- If the value is private, the PR puts it into `dev`, which forbids non-fast-forward updates, in a form recoverable within seconds.
- If it is not private, lines 129 and 539 overstate what is withheld.
- Either way the page's statements and its published bytes disagree.

**Required outcome**

The owner or manager decides publicly whether the reference peer's firmware version is private.

- **Not private:** lines 129 and 539 stop listing it as withheld, or say that the digest identifies it.
- **Private:** the PR tree carries no digest a small enumeration can invert. Record the identity privately, or with a keyed digest whose key is held privately. Line 129 then says how the identity is recorded, since issue step 1 asks for it.

**Verification**

- Private: `fw_digest_enumeration.py` over any value the page publishes reports `matches=0`.
- Not private: lines 129 and 539 no longer claim the value is withheld.

### S1 - SUGGESTION - Docs

`[R264] SUGGESTION Docs - docs/findings/117_GPTP_SILICON_EVIDENCE.md:129 - "the same value recorded on 2026-09-14"`

- The 2026-09-14 records (issue comments 5670665596 and 5671174308) published only an 8-octet prefix, `sha256_8` `33f0e7f9e86fe482`, not the full digest. Line 129 does not link them.
- The prefix does match the page's value.
- Suggested wording: "its first 8 octets match the prefix recorded on 2026-09-14", with a link to the record.

### S2 - SUGGESTION - Docs

`[R264] SUGGESTION Docs - docs/findings/117_GPTP_SILICON_EVIDENCE.md:539 - name protocol identifiers under what stays`

- These identifiers remain in the archive and on the page: MAC addresses, EUI-64 clock identities, entity IDs and entity model IDs.
- A public registry lookup of their OUI gives the manufacturer.
- The base tree already carries the switch's clock identity (`tests/features/gptp_announce_receipt_timeout.feature:52`) and the peer's entity ID and MAC (`tb/tools/torture_campaign.py:1942` and four other files). The peer's clock identity first appears on this page, but it follows directly from that MAC (`census-and-daemons.txt`). That is established practice, not a defect.
- Naming the class makes the "what stays" sentence exact.

Earlier optional suggestions, still not taken: R264-2 S1 (the PR template), R265-2 S1 (cite the #530 disposition for item 3), R265-2 S2 (label the clock of the Run B millisecond times), R264-1 F5/F6, and the rest of R265-1 S2.

## Prior public findings: resolved or retained at this head

| Prior finding | Severity | State at 8016f7ac | Evidence |
|---|---|---|---|
| R264-2 F1 = R265-2 F1: peer identity strings hex-encoded in the pinned archive | MAJOR | CLOSED | Tokens P1-P3 and V1-V3 (peer product, serial, firmware; vendor long name, mark, host stem) and S1-S2 (switch product, serial): 0 raw, hex, base64 or UTF-16 hits at the pin, in all 8 branch commits (the pinned history included) and in the PR commits. The only hits for V2 are 3-byte coincidences inside compressed PNG IDAT or PDF streams, in base-tree files the PR does not touch. The positive controls fire on both superseded archives: 742 and 29 hits (`sweep-controls.txt`, `sweep-evidence-branch.txt`, `sweep-pr531.txt`). The page is re-pinned. Line 129 cites the hash, and "cannot be recomputed from published bytes" is literally true, but see F2. The predecessor decision is published (5800264651). R264-2's clause "line 536 states exactly which classes are withheld" is met for every class except USB serial paths, which moves to F1. |
| R264-2 F2 = R265-2 F2: stale tool-revision redaction statement | MINOR | CLOSED | `page-vs-archive.txt`: exactly four quoted tool hashes name redacted files. They are `8c9f2885` (path-only), `45889a7d`, `c4ef8c9a` and `bdd228a1` (identity), each named with the right kind. `run_a.sh`, `run_b.sh` and `run_c.sh` are identity-redacted, as stated. `95d64fd5`, `ad579e18` and `0e9faf30` have full values on 5584039577. `8ef4b008` has none anywhere, as stated. |
| R264-2 S2: say what `sha256sum -c` reports | SUGGESTION | TAKEN | Line 540. Re-derived: 20 lines in the A200 manifest and 57 in the A202 manifest differ from the published bytes. Every manifest line equals its file's `original_sha256`. |
| R264-2 S1; R265-2 S1, S2 | SUGGESTION | Not taken | Optional, no effect on coverage. |
| R264-1 F1 = R265-1 F1: bare-metal-only gate | BLOCKER | CLOSED, still closed | `docs-gates.txt`: `check_baremetal_only.py --check` rc 0. Hosted `docs-check` succeeded at this head. |
| R264-1 F3 / R265-1 F2 (dark window, holdover, read-only commands, envelope records, census, daemon scope), R265-1 F3 ("reaches asCapable" row) | MINOR | CLOSED, still closed | Re-derived independently at this head; see the next table. |
| R264-1 F2 = R265-1 F4: follow-up tracking | MINOR | CLOSED, still closed | Lines 53 and 466 link #529. Lines 472-498 link #530 (items 1-3 and 9) and #495 (items 4-6). Items 8 and 10 give reasons for having no issue. This matches decision 5798470752. |
| R264-1 F4: box 5 traceability | MINOR | CLOSED, apart from the privacy clause (see F1, F2) | 74 of 74 raw-artifact hashes resolve as recorded. 29 name redacted files: 18 captures, 6 analyses, 3 censuses, 1 entity dump and 1 lock log. The page says the same. |

## Independent re-derivation at this head (page claim against the published raw artifacts)

| Page claim | Re-derived | Receipt |
|---|---|---|
| 77 redacted; 6 path-only; 71 identity; 20 / 57 per packet; `sha256sum -c` fails 20 / 57 | 77; 6; 71; 20 / 57; 20 / 57 | page-vs-archive.txt |
| Every hash names a file at the pin; 29 redacted: 18 / 6 / 3 / 1 / 1 | 74 rows resolve; 29 = capture 18, analysis 6, census 3, entity 1, lock 1 | page-vs-archive.txt |
| 8 page hashes are outside the archive (6 image hashes, the firmware digest, the grader) | as stated. `.bit`, payload and `aem_desc.bin` are in both `expected-crc.txt` tables. `.bit`, `aem_desc.bin` and `flashboot_layout.json` are in 5794859125. `bios.bin` and `csr.csv` are in no pin file and no issue or PR comment. The ROM row `e84e579c` is a different object. The grader equals `scripts/baremetal_uart_smoke.py` at ede8d48e (`bc41ab03...`). `95d64fd5`, `ad579e18` and `0e9faf30` are full on 5584039577; `8ef4b008` is nowhere | page-vs-archive.txt, external-hash-sources.txt, comment-hash-sources.txt |
| Non-envelope records: 76 in Run A; 38, 0, 38, 45, 0, 37; 18 in the final capture; none elsewhere; 19 tcpdump logs, 0 dropped; captures masked length-preserving and still parse | identical. Every pcap walks cleanly to its last octet, and all 20 redacted captures keep their original length | pcap-envelope-census.txt, superseded-original-checks.txt |
| 38,954 console commands in 14 transcripts, read verbs only | 38,954 = `milan_status` 7,792, `mem_read` 31,154, `mem_list` 2, `crc` 6; 14 transcripts | console-command-census.txt |
| Holdover set in 3 to 5 samples, 0.30 to 0.50 s | 3, 3, 5, 3, 4, 4 samples; 0.30, 0.30, 0.50, 0.31, 0.41, 0.41 s | step3-recheck.txt |
| asCapable returns within one sample of the DUT's second completed Pdelay exchange, 1.03 to 1.64 s after the switch's first frame, peer delay 377 to 389 ns | `CLKV_STAT[16]` rises in the first sample after the second exchange completes, in every cycle. That is 1.02 (1.03 with the page's fit) to 1.64 s after the first frame. PDELAY at that sample is 385, 377, 385, 385, 389, 382 | step3-recheck.txt |
| Per-cycle table: off-for, first frame, first Announce, asCapable 1, all-good, recovery | equal to 0.01 s, except where my coarser tap fit shifts a tap time by at most 0.01 s. Recovery 0.50/0.51/1.51/0.43/1.46/1.60 against the page's 0.51/0.52/1.51/0.43/1.46/1.60 | step3-recheck.txt |
| Dark window 1.03 to 1.75 s until 37.55 to 38.57 s | 1.04 / 1.75 / 1.47 / 1.71 / 1.65 / 1.48 s until 38.24 / 37.55 / 38.07 / 38.57 / 38.07 / 38.12 s | step3-recheck.txt |
| Cycles 4-6: no CONNECT_TX between the loss and recovery; first after return 41.28 / 42.96 / 41.46; first `tu=1` 1.08 / 1.07 / 1.00; 316 / 293 / 243 `tu=1` PDUs; emission ends 1.71 / 1.65 / 1.49; every post-return PDU `tu=0` | 0; 41.28 / 42.96 / 41.46; 1.08 / 1.07 / 1.00; 316 / 293 / 243; 1.71 / 1.65 / 1.48; 0 post-return `tu=1` | step3-acmp-crf.txt |
| 18 ACMP states agree; one field differs (DUT Stream Output 1 `stream_dest_mac` 00:... to 91:e0:f0:00:8d:6f); two hosts checked for daemons | identical; `hosts-clock-and-daemons.txt` covers exactly the controller host and the capture server | census-and-daemons.txt |
| Run A turnaround medians | `runA/pdelay-turnaround.txt`: DUT responds 10,992 ns, tap minus claimed 384 (375-400); switch responds, minus claimed 394 (385-524) | pin file |

## Per-lens results (all five applied at 8016f7ac)

- `[R264] UNCLEAN Conformance - F1, F2.` I also applied this lens to:
  - `docs/design/GM_LOSS_RECOVERY.md:88-118` against decision 5795898094: bound, start, end, media and the 3 + 0.375 + 1.625 derivation all match.
  - The Milan rows the page cites: MILAN_COMPLIANCE_MATRIX.md:78 and :83.
  - The one-DUT topology decision 5561827955, stated at page :60-64.
  - The PR says "Relates to #117" and changes no acceptance box.
- `[R264] PASS RTL - hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv:248; docs/reference/REGISTER_MAP.md:731, :770, :875, :1347, :1392 - every register decode on the page matches the RTL assignment and the register map at this head.` The decodes checked:
  - `CLKV_STAT` bits 0 `tu`, 1 sync, 3 holdover, 16 asCapable, giving `0x00010002` / `0x00010009` / `0x0001000b`;
  - `CRFT_CTRL` `0x3002E3`: bits 0, 1, 5, 6, 7, VID `[19:8]` = 2, PCP `[22:20]` = 3;
  - `LINKG_STAT` `0x83` to `0x03`: `act_recent`, bit 7, over a 2.7 s window;
  - `ASP_CMD` `0x11`: generation 1, count 1;
  - `GPTP_LAT` `0x029000DB` = 656 / 219 ns.

  The PR changes no HDL, firmware or gitlink (`receipts/clone-integrity.txt`).
- `[R264] UNCLEAN Robustness - F1, F2.` I also applied it to:
  - the loss, absence and return ordering in all six cycles;
  - no CONNECT_TX during the partition;
  - host-record exclusion and zero drops;
  - parse integrity of every length-preserving masked capture.
- `[R264] UNCLEAN Tests - F1.` I also applied it to:
  - my own sweeps, which carry positive controls that fire on both superseded archives;
  - ten focused documentation gates, all rc 0 (`docs-gates.txt`);
  - the manager's published checks: the peer-field sweep and the counts.
- `[R264] UNCLEAN Docs - F1, F2.` I also applied it to:
  - TOC and anchors (`gen_toc.py --check`, `--verify-anchors`);
  - the em-dash gate from base `ede8d48e`;
  - the index row in `docs/findings/README.md`;
  - every page hash and count;
  - one-line commits with no trailers (c3eb95fa, 0abf147f, 8016f7ac).

## Reviewer ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | CONTRIBUTING.md:524-551; issue #117 decisions; GM_LOSS_RECOVERY.md:88-118; page :34-64, :129, :539; pin `74ac94e8`, all 8 branch commits | R264-3 | 8016f7ac843b0ae6764dc4ec0140cda5ac7d6cc1 |
| RTL | CLEAN | KL_ptp_clock_validity.sv:248; REGISTER_MAP.md:731, :770, :875, :1347, :1392; page :404-451; gitlinks unchanged from ede8d48e | R264-3 | 8016f7ac843b0ae6764dc4ec0140cda5ac7d6cc1 |
| Robustness | UNCLEAN (F1, F2) | pin tools (run_a.sh:9, run_b.sh:8, cycle_locked.sh:9); 22 pcaps; 14 console transcripts; step 3 cycles 1-6 | R264-3 | 8016f7ac843b0ae6764dc4ec0140cda5ac7d6cc1 |
| Tests | UNCLEAN (F1) | scripts/docs_check.py `LOCAL_RULES`; manager sweep claim 5800264651; receipts/*.txt with positive controls | R264-3 | 8016f7ac843b0ae6764dc4ec0140cda5ac7d6cc1 |
| Docs | UNCLEAN (F1, F2) | docs/findings/117_GPTP_SILICON_EVIDENCE.md (all 628 lines); docs/design/GM_LOSS_RECOVERY.md; docs/findings/README.md; MANIFEST.json and both MANIFEST.sha256 at the pin | R264-3 | 8016f7ac843b0ae6764dc4ec0140cda5ac7d6cc1 |

S1 and S2 are SUGGESTIONs and do not affect coverage.

The F1 fix changes the pin, so it changes page :533-535 and the archive. That will un-cover Conformance, Tests and Docs, and Robustness for the archive. RTL stays covered at this head unless a later commit touches the register decodes or the product tree.

## Real limits

- **Evidence, not the product.** I judged the evidence only.
  - Physical calibration was NOT RUN.
  - Field skips and NOT RUN rows are not hardware proof.
  - I had no bench access.
- **Token set.** The identity tokens come from two sources:
  - what the redaction itself replaced, found by diffing the superseded original archive against the pin;
  - the repository's `IDENTITY_RULES` and `LOCAL_RULES`.

  An identifier that the redaction never touched and no rule names would be missed. I added a separate search for serial, by-id and host-name strings in the pin (F1 came from it).

  Eleven files were never published unredacted, so I could not diff them (`superseded-original-checks.txt`). Their "as run" hashes can be checked only through `MANIFEST.json`.
- **Base64 coverage.** Base64 is searched by stable core. For tokens shorter than four octets that covers alignment 0 only.
- **My tap timebase is coarser than the page's.**
  - It is a least-squares line through all per-5 s minima, with residuals up to 67 ms in cycle 1; the page reports at most 2.02 ms over its kept windows.
  - Tap-derived times agree to 0.01 s.
  - No 0.1 s console claim depends on the difference.
- **Coverage of the re-derivation.** I re-derived the statements the correction commit changed, the counts, the hashes and the step 3 edges.
  - The step 2 cadence statistics, the step 4 steady-state table and the step 5 transcripts have been unchanged since 0abf147f.
  - Both round-2 reviews re-derived them. I spot-checked only the Run A turnaround.
- **Hosted checks.** At this head eight contexts executed with success: `rtl-fast`, `docs-check`, `docs-check-no-git`, `elaborate`, `wire-accountability`, `full-ci-gate`, `changes` and `bdd-conformance`.
  - Seven are skipped. `verilator-suites` and `yosys-portability` are skipped on the docs-only path. The other five are the nightly and manual physical gPTP context, the two shard matrices, `yosys-elaboration` and `verilator-lint` (`hosted-check-runs-8016f7ac.tsv`).
  - A skipped context is not evidence of execution.
  - I read no job logs. The manager owns hosted and act acceptance.
- **Comments scanned.** The comment scan covered only issue #117 and PR #531.

## Pending manager duties

1. **F1.** Rewrite the evidence branch, re-pin, and correct the page at a new head.
2. **F2.** Get the owner's decision on the firmware value. Then re-review every lens the change un-covers.
3. **Superseded archive commits.** At this round, both commits named in the manager's 2026-09-23 note, the original and the first pass, still resolve by full SHA on the public remote.
   - The positive controls show the original carries the peer and switch identities in raw form, and the first pass carries them in hex (`sweep-controls.txt`, revisions withheld).
   - The owner's purge (5800264651) is still pending.
4. **Archived review records.** On the evidence branch, the archived review records name superseded archive commits in 12 files (`superseded-link-sweep.txt`, labels only). Decide whether these fall under the 2026-09-23 "history link" decision. This report and its receipts spell no superseded SHA.
5. **Public comments outside the PR tree.**
   - Issue comment 5561827955 names the reference peer's product in prose.
   - Issue comments 5670665596 and 5671174308 publish the 8-octet firmware-digest prefix, which F2's decision also covers.
   - PR comment 5799413596 lists superseded short SHAs.
6. **Merge-turn duties.**
   - Build the final candidate against live `dev` `26d855a9176d63625e6635a029a0c44e3d57ce9a` (source base `ede8d48e`).
   - Complete hosted and act acceptance, candidate validation and post-merge containment.
   - Merge only with explicit maintainer authorization.
7. **Issue #117 boxes.** They stay the owner's call:
   - box 4 carries FAIL and NOT RUN rows;
   - audio is deferred to 2026-12-31;
   - the PR only relates to the issue.

## Receipts (every file listed in MANIFEST.sha256)

`scripts/run_all.sh CLONE EVID_GITDIR TOKENS SUPERSEDED OUT` reproduces every receipt except these four:

- `comment-token-scan.txt`: `scripts/comment_token_scan.py` over the fetched issue and PR comment JSON;
- `comment-hash-sources.txt`: `scripts/comment_hash_sources.py` over the same JSON;
- `hosted-check-runs-8016f7ac.tsv`: from the read-only check-runs API;
- `clone-integrity.txt`: 865 tracked blobs, byte and mode exact; index tree equals `fe707936...`; three required gitlinks at stage 0, unchanged from base. The documentation gates had written a bytecode cache into the clone's ignored `scripts/__pycache__`. I removed it, and no untracked or ignored file remains.

The token file and the superseded-SHA file are private inputs and are not published. Receipts name tokens only by label and class.

- **Identity and links:**
  - `receipts/sweep-controls.txt`
  - `receipts/sweep-evidence-branch.txt`
  - `receipts/sweep-pr531.txt`
  - `receipts/usb-serial-per-commit.txt`
  - `receipts/superseded-link-sweep.txt`
  - `receipts/comment-token-scan.txt`
  - `receipts/fw-digest-enumeration.txt`
- **Page against archive:**
  - `receipts/page-vs-archive.txt`
  - `receipts/pcap-envelope-census.txt`
  - `receipts/console-command-census.txt`
  - `receipts/step3-recheck.txt`
  - `receipts/step3-acmp-crf.txt`
  - `receipts/superseded-original-checks.txt`
  - `receipts/external-hash-sources.txt`
  - `receipts/comment-hash-sources.txt`
  - `receipts/census-and-daemons.txt`
- **Gates and state:**
  - `receipts/docs-gates.txt`
  - `receipts/hosted-check-runs-8016f7ac.tsv`
  - `receipts/clone-integrity.txt`
- **Scripts:** `scripts/*.py`, `scripts/run_all.sh`

R264-3 FINISHED
