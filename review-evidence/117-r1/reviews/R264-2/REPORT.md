[R264] NEGATIVE - exact head f547a49bee5966a901d1e11981eb4dc94d038711

Round R264-2: internal independent review of issue #117 / PR #531, in a cleared context.

- Head `f547a49bee5966a901d1e11981eb4dc94d038711`, tree `27e6488d3da9669f787662d49e40f2263995dcb7`.
- Source base `ede8d48ecd7c7f589a14b957951f040d92c99c70`, an ancestor.
- Four commits on the base. Each message is one line with no trailers.
- `git diff --raw ede8d48e..f547a49b` shows three Markdown files and nothing else:
  - `docs/findings/117_GPTP_SILICON_EVIDENCE.md` (A);
  - `docs/design/GM_LOSS_RECOVERY.md` (M);
  - `docs/findings/README.md` (M).
- All four gitlinks equal the base.
- The page pins its raw-artifact archive at `117-review-evidence` commit `32aec66197ba78ee431c27383bb958e5728c270a`, path `review-evidence/117-r1`.

## Verdict in brief

The bench evidence holds at this head. I re-derived it again with my own decoders from the published captures, console transcripts, controller logs and power-strip logs. That covers:

- the identity gate;
- the step 2 cadence and turnaround;
- all 60 cells of the six-cycle step 3 table: recovery 0.43 to 1.60 s against the 5 s bound;
- the loss and return edges, the stream restarts and `tu`;
- the step 5 parity and FAIL;
- bench restoration.

Every R264-1 and R265-1 finding is closed at this head, with one exception. The privacy half of R264-1 F4 is retained, and so is the evidence-mirror duty that both rounds left for the manager. The manager's archive rewrite did not close either of them. The re-pin commit also brought two new defects:

- **F1, MAJOR.** The pinned archive still publishes the reference peer's identity strings, hex-encoded. That includes its serial number and the product name the repository's scrub forbids. The same strings were redacted elsewhere in the same archive. Page line 536 says those classes are redacted.
- **F2, MINOR.** The tool-revision paragraph's redaction statement is stale at the new pin. It names three redacted files; seven are redacted, including one whose hash the page quotes.

Both leave their lenses unclean, so the verdict is NEGATIVE. RTL, Robustness and Tests are covered clean at this head.

## Reconstruction order and authorities read

1. AGENTS.md, then CONTRIBUTING.md:
   - sections 2.1 and 2.2, including the seven required contexts and the PR template rule;
   - section 3;
   - section 6 and 6.1: naming by role, no bench-identifying information, the em-dash rule;
   - `scripts/docs_check.py` `IDENTITY_RULES` and `LOCAL_RULES`.
2. docs/README.md (authority order).
3. Issue #117: the body with its frozen acceptance and scheduling preface, and these decisions:
   - 5561827955 and 5565246390: the one-DUT contract;
   - 5674663121: the audio deferral;
   - 5789767491, 5794146393, 5794354283, 5794950660 and 5794954599: the 2026-09-23 bench decisions and flash;
   - 5795898094: switch power-cycling and the 5 s bound;
   - 5670665596 and 5671174308: the 2026-09-14 peer record, which published hash prefixes only.
4. Interface documents: `docs/reference/REGISTER_MAP.md` rows 0x624/0x628, 0x62C, 0x6E4, 0x720, 0x730/0x734, 0x750, 0x764, 0x774, 0x77C, 0x780 and 0x7F0, plus `docs/design/GM_LOSS_RECOVERY.md`.
5. The diff and its history: c3eb95fa, 0abf147f, 67aa00e5 and f547a49b.
6. Evidence:
   - the archive at `32aec661`, with both packets and `MANIFEST.json`;
   - its predecessor `160debeb`, which is still fetchable by SHA, used for redaction diffing only;
   - issues #495, #529 and #530;
   - the exact-head hosted check runs;
   - the A210 REVIEW READY record (5798715557) and the manager's PR comments.
7. Only after my own pass over the diff and evidence: the prior public findings, R264-1 (5798410684) and R265-1 (5798463789).

## Findings

### F1 - MAJOR - Conformance, Docs

`[R264] MAJOR Conformance, Docs - docs/findings/117_GPTP_SILICON_EVIDENCE.md:536, :129, :531-533; archive 32aec661 review-evidence/117-r1/bench-a200/bench/peer-aem-1.jsonl:2, bench-a200/bench/final/census-final.jsonl:59, bench-a202/bench/census-start.jsonl:59, bench-a202/bench/final/census-end.jsonl:59 - the pinned evidence archive still publishes the reference peer's identity strings that the page says are redacted`

**Requirement and evidence**

- **The rules.**
  - CONTRIBUTING.md:532-545: bench equipment is named by role, never by vendor or product, and no bench-identifying information is published.
  - `scripts/docs_check.py` `IDENTITY_RULES` denies the peer product name in any tracked text.
  - The 2026-09-14 public peer record (issue comment 5670665596) published `entity_name`, `firmware_version` and `serial_number` only as hash prefixes: "exact string retained privately".
- **What the page claims.**
  - Line 536: "73 files are published redacted: local paths, and bench-identifying strings (equipment names, device serials, host names)".
  - Line 129 tells the reader that "the raw ENTITY descriptor bytes are in the A200 packet (`bench/peer-aem-1.jsonl`)".
- **What the archive at `32aec661` actually carries** (`receipts/identity_hits_located.txt`, `receipts/token_counts_orig_vs_pub.txt`):
  - Four JSONL files carry the reference peer's ENTITY READ_DESCRIPTOR payload, hex-encoded in `/payload`: `peer-aem-1.jsonl` line 2, and line 59 of each census file listed above.
  - In each payload, the octets for `entity_name` begin with the deny-listed peer product token (T9).
  - `group_name` carries a 12-octet token (T4) and `serial_number` a 13-octet serial (T8).
  - `firmware_version` is there in full, and the page's field hash can be recomputed from it.
- **The same rewrite already treated these values as identifying.**
  - It replaced T8 with `<device-serial>` and T9 with `<peer-product-name>` in the peer's Run C entity dump (`MANIFEST.json`: `bench-a200/bench/runC/entity_0x3cc0c60102030000.json`, `identity_redacted` true).
  - It masked T4 with `#` in the captures.
  - Only the hex form was missed. Sweeps for raw, UTF-16, base64 and decimal-array forms find no other copy (`receipts/identity_sweep_archive.txt`, `receipts/encoded_forms_sweep.txt`).
- **Excluded:** the 11-octet device serial (T7). It is the DUT's own serial, a repository constant already in `configs/*.yaml` and `avdecc/aem_rom.json` (`receipts/tokens_in_pr_tree.txt`). Its remaining raw and hex copies disclose nothing new.
- **Both prior rounds named this material as a pending manager duty:** R264-1 ("raw peer descriptor bytes") and R265-1 ("the reference peer's ENTITY descriptor strings, including its serial number"). The rewrite was meant to discharge that duty, and the page now asserts that it did.
- **The PR tree itself is clean.** `docs_check.py` scrub passes (0 findings over 841 files), and no recovered token occurs in the head tree except T7.

**Other identifying material in the archive**

These remain but are not raised as defects: the repository's own gate and its current docs already carry them.

- short host role names in file names and logs;
- generic capture interface names;
- the tap's vendor and product name, in two packet scripts' docstrings and a tool-version file;
- the capture server's own DHCP host name and the matching mDNS records, in the host-traffic records of six tap captures. The page already excludes those records from its analysis (`receipts/pcap_name_fields_published.txt`).

Line 536's "equipment names ... host names" is broader than what the archive actually withholds.

**Impact**

- The public archive that box 5 depends on publishes identity the repository and its prior reviewed record withheld.
- The page's privacy statement is false.
- The merged dev page would send readers to those bytes (line 129 and the locator at lines 531-533).
- The pre-rewrite archive `160debeb` is also still fetchable by SHA. PR commit `67aa00e5`'s tree links it, so a merge commit would carry that link into dev history.

**Required change**

- The pinned archive carries none of the reference peer's ENTITY identity fields in any encoding: `entity_name`, `group_name`, `serial_number` and the firmware string. `MANIFEST.json` records every file changed.
- The page is re-pinned to that commit, and every quoted hash still resolves through the manifest.
- Line 536 states exactly which classes the archive withholds.
- Line 129 no longer promises recomputation from published bytes that no longer exist. For example, it cites the field hash as recorded, with the original kept privately as the 2026-09-14 record did.
- The manager publicly decides whether the predecessor objects, and the PR-history link to them, are acceptable. That decision covers the merge method and any purge request.

**Verification**

- `scripts/run_all.sh <clone at new head> <work> <out>` runs with the new pin as the published root and its predecessor as the original.
- Its outputs must show:
  - no raw or hex hit for T3, T4, T8 or T9 in `identity_sweep_archive.txt`;
  - `encoded_forms_sweep.txt` hits 0;
  - every page hash resolved in `page_hash_resolution.txt`.
- The documentation gates stay green.

### F2 - MINOR - Docs

`[R264] MINOR Docs - docs/findings/117_GPTP_SILICON_EVIDENCE.md:218-224 (with :216) - the tool-revision redaction statement is stale at the new pin: it names three redacted tool files, but seven are published redacted, including analyze_cycle.py whose as-run hash the page quotes`

**Requirement and evidence**

- Issue #117 box 5 requires exact hashes, and the box 5 row (`:58`) says Tool revisions states "which hashes name files outside it".
- Lines 220-224 read: "Three of those files are published with local paths redacted: the enumerator binary `8c9f2885...`, `run_cycle.sh` `45889a7d...` and `cycle_locked.sh` `c4ef8c9a...`".
- At `32aec661` seven packet tool files are published redacted (`receipts/tool_redaction_vs_page.txt`):
  - `a200_enum.bin`;
  - `run_a.sh`, `run_b.sh` and `run_c.sh`;
  - `analyze_cycle.py`;
  - `cycle_locked.sh` and `run_cycle.sh`.

  Six of them are identity-redacted, not only path-redacted.
- Line 216 quotes `analyze_cycle.py` `bdd228a1...`, which matched its published file at the previous pin, `160debeb`. At `32aec661` the published copy hashes to `2ca45609...`, and the paragraph does not mention it.
- Commit f547a49b updated the Raw artifacts counts ("Eleven" to "73", "One" to "26") but not this paragraph.

**Impact:** a cold reader checking a quoted tool hash against the pinned archive finds a mismatch the page says cannot happen. Box 5 traceability is overstated.

**Required change:** the paragraph names every quoted tool hash whose file is published only in redacted form at the pinned commit. That is `8c9f2885`, `45889a7d`, `c4ef8c9a` and `bdd228a1` at `32aec661`, or whatever the new pin gives. It also gives a correct count or no count, and the kind of redaction.

**Verification:** at the new head and pin, `scripts/misc_checks.py` writes `tool_redaction_vs_page.txt`. Every row with `quoted-on-page=True` must be named in the paragraph.

### S1 - SUGGESTION - Docs

`[R264] SUGGESTION Docs - PR #531 body - adopt the PR template sections`

- CONTRIBUTING.md:365-367 and `.github/PULL_REQUEST_TEMPLATE.md` ask for these sections: Status, Linked Issue / roles, How to get into the same state, How to validate, Known limitations and Definition of Done.
- The body has none of them (`receipts/pr_body_template_check.txt`).
- Recent merged PRs are mixed on this (`receipts/merged_pr_template_practice.tsv`), so this is not raised as a defect.
- The roles and the exact-head validation would help the merge record.

### S2 - SUGGESTION - Docs

`[R264] SUGGESTION Docs - docs/findings/117_GPTP_SILICON_EVIDENCE.md:535-537 - say what a manifest check reports`

- Each packet's `MANIFEST.sha256` lists as-recorded hashes. `sha256sum -c` in the packets therefore reports the 73 redacted files as FAILED by design: 18 in A200 and 55 in A202.
- Say so, and point to `MANIFEST.json` for them.
- "most captures" understates the redaction: all 18 captures in the tables are published redacted, and so is the Run C DUT entity dump.

## Prior public findings: resolved or retained at this head

| Prior finding | Severity | State at f547a49b | Evidence |
|---|---|---|---|
| R264-1 F1 = R265-1 F1: bare-metal-only gate red | BLOCKER | CLOSED | `receipts/gates/baremetal_check.log`: OK, 0 findings over 839 files. Hosted docs-check job 107294772483: 51 of 51 steps success, including step 21 "Bare-metal scope gate" (`receipts/hosted_docs_check_steps.txt`). The recorded gate set (A210, 5798715557) now lists the gate. |
| R264-1 F2 = R265-1 F4: observation issues | MINOR | CLOSED | Page :468-495 gives each item a disposition. #530 is linked for items 1-3 and 9, and its lane cites them. The #495 checklist comment 5798471063 carries items 4-6. Items 8 and 10 state why no issue is needed. The PR body matches (`receipts/verify_followup_tracking.txt`). |
| R264-1 F3 A = R265-1 F2.3: dark-window start | MINOR | CLOSED | Page :337 says 1.03 to 1.75 s. Re-derived: last record 1.034 to 1.752 s, every one DUT-sent; cycle 2's is a Pdelay_Req at 1.752 s. First record 37.553 to 38.573 s (`receipts/verify_dark_window_hostrecs.txt`). |
| R264-1 F3 B = R265-1 F2.2: holdover span | MINOR | CLOSED | Page :322 says 3 to 5 samples. Re-derived: 3, 3, 5, 3, 4, 4 (`receipts/rederive_step3.txt`). |
| R264-1 F3 C: "read-only AECP only" | MINOR | CLOSED | Page :47 and :392-395. Re-derived: 38,954 commands in 14 transcripts, all `milan_status`, `mem_read`, `mem_list` or `crc`. No CONNECT_TX reached the DUT between loss and all-good. The first after return came at 41.28, 42.96 and 41.46 s (`receipts/rederive_step3_extra.txt`). |
| R264-1 F3 D = R265-1 F2.1: envelope-less records | MINOR | CLOSED | Page :134. Re-derived: Run A 76, other A200 captures 0. Cycles 1-6: 38, 0, 38, 45, 0, 37. Step 3 final 18, attempt 1 0 (`receipts/rederive_step2.txt`, `verify_dark_window_hostrecs.txt`). |
| R265-1 F2.4: binding census | MINOR | CLOSED | Page :501 and :511. A200: 18 of 18 states, all connection count 0; one field differs (DUT Stream Output 1 dest MAC). A202: 18 of 18 identical (`receipts/verify_census_daemons.txt`). |
| R265-1 F2.5: daemon check scope | MINOR | CLOSED | Page :45 and :256. Two hosts were checked, the controller host and the capture server (same receipt). |
| R265-1 F3: stale "reaches asCapable" row | MINOR | CLOSED | Page :41 and :438. In all six cycles `CLKV_STAT[16]` rose 0.015 to 0.094 s after the DUT's second completed Pdelay exchange, inside one sample. PDELAY_NS was 377 to 389 ns (`receipts/verify_reach_row.txt`). |
| R264-1 F4: box 5 traceability and privacy statements | MINOR | Locator and hash part CLOSED. Privacy part RETAINED as F1. | 74 of 74 Raw artifacts hashes name files at `32aec661`: 48 as recorded, 26 redacted and mapped by `MANIFEST.json`, matching the page's "26". Every abbreviated tool hash resolves or is placed on 5584039577 as stated; `8ef4b008` has no public full value, as stated (`receipts/page_hash_resolution.txt`, `external_hash_sources.txt`). The privacy statement at :536 contradicts the archive (F1). A new stale sentence is F2. |
| R264-1 F5, F6; R265-1 S2 | SUGGESTION | Not taken, or taken in part (the 2.02 ms residual) | Optional; no effect on coverage. |
| R265-1 S1: link the public mirror | SUGGESTION | Taken | Page :530-533. |
| R264-1 / R265-1 pending duty: evidence-mirror hygiene | Manager duty | NOT discharged for the peer ENTITY strings | F1. |

## Independent re-derivation at this head (page claim against the published raw artifacts)

| Area | Page | Re-derived | Receipt |
|---|---|---|---|
| Identity | ROM `f6afa4ec`, QSPI `02036e95`, AEM `93742dd2`, VERSION `00020060`, grader 10/10, grader `bc41ab03...` | same in both packets; CRC table byte-identical; grader hash equals `ede8d48e:scripts/baremetal_uart_smoke.py` | identity_gate_check.txt |
| Peer firmware field | seven octets, `33f0e7f9...` | same, from the published payload | identity_gate_check.txt |
| Cadence | 4,556 Sync, 565 Announce, 564 and 566 Pdelay_Req intervals; max 149.4, 1010.6 and 1029.6 ms; DUT 1000.002 ms | same; all within 30 % | rederive_step2.txt |
| Turnaround | 568/568 and 570/570; 10,984 to 11,009 ns; 18.33 and 18.36 ms; tap minus claimed 383 to 391 and 393 to 394 ns | same | rederive_step2.txt |
| Retention | 116 samples; 60/60 AS_CAPABLE; CSR 380 to 391 ns, AECP 381 to 391 ns, medians 385 | same | rederive_steps4_5.txt |
| Run B CRF | 34,061 PDUs, all `tu=0`, continuous; bursts 19.67/18.45/15.00/15.00 s; pauses 1,106/578/148 ms | same | rederive_step2.txt |
| Step 3 table | recovery 0.51, 0.52, 1.51, 0.43, 1.46, 1.60 s | 0.507, 0.514, 1.507, 0.426, 1.463, 1.601 s; every other cell agrees to rounding | rederive_step3.txt |
| Loss edges | 0.40-0.46 s after last Sync; 3.01-3.08 s after last Announce; switch's last frame 0.63-0.73 s | 0.404-0.464; 3.008-3.077; 0.626-0.733 | rederive_step3.txt |
| DUT as master | 1 to 4 Sync pairs; own Announce, priority1 248, in cycles 3 and 5 | same | rederive_step3.txt |
| Counters | `CLKV_TUCNT` +40/+39/+41/+40/+40/+41; path generation +1 per identity edge | same | rederive_step3_extra.txt |
| Stream, cycles 4-6 | first `tu=1` PDU 1.08/1.07/1.00 s; 316/293/243 `tu=1` PDUs; licence drop 2.21/5.23/1.89; relicensed 41.25/42.92/41.45; first PDU 41.28/42.96/41.46, all `tu=0` | 1.080/1.067/1.001; 316/293/243; 2.20/5.23/1.89; 41.25/42.92/41.44; 41.283/42.960/41.459 | rederive_step3_extra.txt |
| Observation 7 | PHC steps equal on-to-on intervals within 0.04 s | within 0.036 s; cycle 1 measured against the guard's early power-on recorded in the attempt 1 lock log | verify_phc_steps.txt |
| Step 5 | probe transcripts identical; DUT downgraded at 5.3.8.10; peer IEEE17221 and Milan | same | rederive_steps4_5.txt |

The design page's recovery bound (`GM_LOSS_RECOVERY.md:88-118`) matches decision 5795898094 in three respects:

- its start and end points;
- the sum 3 + 0.375 + 1.625 = 5 s;
- the Milan intervals.

Its reading of "return" as the first Announce or Sync is stated publicly. The page also reports the first-frame reading (1.83 to 2.60 s; 1.82 under my fit) and the power-on reading (19.18 to 20.32 s).

## Per-lens results (all five applied at f547a49b)

`[R264] PASS RTL - git diff --raw ede8d48e..f547a49b; git ls-tree gitlinks at base and head; docs/reference/REGISTER_MAP.md:730, :731, :770, :771, :816-817, :875, :880, :942-944, :1161, :1392 (receipts/register_rows.txt) - the diff is three Markdown files and the gitlinks equal the base. Every register decode the page relies on agrees with the register map: CLKV_STAT 0x00010002, 0x00010009 and 0x0001000B (bits 0, 1, 3 and 16); LINKG_STAT 0x83/0x03 (act_recent over 2^27 cycles, 2.7 s at 50 MHz, against the page's 2.73 s); GPTP_LAT 0x029000DB = 656/219 ns; CRFT_COUNT 0x850D = 34,061; CLKV_TUCNT counting 1 s intervals.`

`[R264] PASS Robustness - archive 32aec661 bench-a202/bench/attempt1-aborted/{lock.txt,NOTE.md,powerstrip.txt}, cycle1-6/*, final/*; bench-a200/bench/census-start.jsonl, final/census-final.jsonl; receipts/verify_dark_window_hostrecs.txt, verify_census_daemons.txt, rederive_step3.txt, verify_phc_steps.txt - the failure and cleanup paths of the method were checked against the page:`

- the aborted attempt: the guard powered on after 5.95 s, and the attempt was excluded from the cycles and used correctly as cycle 1's reference;
- the dark window and the host-record exclusions in all eight step 3 captures;
- `RST_EPOCH` 1 and a largest console gap of 0.113 s;
- the bench restored in both censuses;
- the NOT RUN and FAIL rows (peer recovery time, Hive, behave, latency, audio, Milan compatibility) are honest;
- DUT link-loss observations 8 and 10 have public dispositions.

`[R264] PASS Tests - receipts/gates/SUMMARY.txt; receipts/hosted_checks_head.txt; receipts/hosted_docs_check_steps.txt; issue comment 5798715557 validation table; receipts/rederive_*.txt - the validation behind the page was checked:`

- The recorded gate set includes the previously missing bare-metal gate.
- Eight documentation gates run locally at the head, all rc 0: docs_check, em-dash against `ede8d48e`, bare-metal, doc style, gPTP docs, feature status, and TOC check and anchors.
- All seven required hosted contexts are executed and successful at the head. docs-check completed 51 of 51 steps.
- My re-derivations are able to fail, and one did. The Observation 7 check first used the attempt 1 sequence's later "on" and reported a 14.3 s mismatch. It matched only once measured against the guard's recorded power-on.

Conformance is covered and UNCLEAN (F1). It was judged against:

- the frozen acceptance;
- the one-DUT decision, the 2026-09-23 decisions and the 5 s bound;
- CONTRIBUTING section 6 and the scrub rules, applied to the pinned evidence.

Boxes 1 to 4 re-derive as the table states: FAIL and NOT RUN where stated. Box 5's evidence is traceable, but its archive violates section 6 (F1).

Docs is covered and UNCLEAN (F1, F2). Also checked:

- the em-dash rule (0 findings over 665 added lines);
- the Contents separator switch in GM_LOSS_RECOVERY.md;
- the findings index row;
- the recovery-bound section;
- every relative link and anchor, through docs_check and `gen_toc.py --verify-anchors`;
- the PR body (S1).

## Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 MAJOR) | #117 acceptance and decisions 5561827955, 5565246390, 5789767491, 5795898094; CONTRIBUTING.md:532-545 and docs_check IDENTITY_RULES; page :38-58 against the re-derivation receipts; GM_LOSS_RECOVERY.md:88-118; archive 32aec661 identity sweep | R264-2 | f547a49bee5966a901d1e11981eb4dc94d038711 |
| RTL | CLEAN | diff --raw (docs only; gitlinks equal base); REGISTER_MAP.md rows listed above against the page's CSR decodes | R264-2 | f547a49bee5966a901d1e11981eb4dc94d038711 |
| Robustness | CLEAN | attempt 1 lock log, note and power-strip log; cycle1-6 and final captures (dark window, host records); console gaps and RST_EPOCH; both censuses; NOT RUN/FAIL rows; observation dispositions | R264-2 | f547a49bee5966a901d1e11981eb4dc94d038711 |
| Tests | CLEAN | local docs gates at head; hosted required contexts and docs-check steps at head; A210 recorded gate set; independent re-derivations for identity and steps 2 to 5 | R264-2 | f547a49bee5966a901d1e11981eb4dc94d038711 |
| Docs | UNCLEAN (F1 MAJOR, F2 MINOR) | 117_GPTP_SILICON_EVIDENCE.md, GM_LOSS_RECOVERY.md, findings/README.md; page hash resolution through MANIFEST.json; tool-redaction table; PR body | R264-2 | f547a49bee5966a901d1e11981eb4dc94d038711 |

S1 and S2 are SUGGESTIONs and do not affect coverage. The F1 and F2 fix will un-cover lenses:

- a commit to the page un-covers Conformance, Tests and Docs;
- re-pinning to a rewritten archive un-covers Robustness, whose evidence is that archive.

Each must be covered again at the new head.

## Real limits

- **Public evidence only.** I had no bench, console, JTAG or power access; every conclusion comes from public artifacts.
- **Token recovery.** The redacted tokens were recovered by diffing the pinned archive against its predecessor `160debeb`. The receipts print only neutral token IDs, classes and lengths, never the strings or their hashes.
- **Sweep coverage.** The identity sweep searched raw, hex, UTF-16LE, base64 and decimal-array forms, plus the repository's scrub rules. It can only find strings the rewrite redacted somewhere. I added a word survey for host, path and equipment names, whose residuals are listed under F1. Identifying data of a kind never redacted anywhere could still exist unrecognised.
- **Clock fit.** The tap-to-host mapping is my own lower-envelope fit. It is cruder than the packet's in cycles 1 and 2, with residuals up to 12 ms. Every table cell still agrees to rounding. Two derived boundary values differ from the page by at most 0.006 s: cycle 2, 1.82 against 1.83 s and 1.02 against 1.03 s. That is within the fit difference, so they are not findings.
- **Build artifacts are not public.** The `bios.bin` and `csr.csv` hashes exist on the page only, as the page says. Identity rests on a CRC32 readback without a JTAG configuration readback, as the page says.
- **Box 1 topology.** The asCapable partner is the bench switch. The page publishes that interpretation under the owner's one-DUT decision. Ticking the box is the maintainer's call.
- **Not run, and not proof.** Physical calibration, latency, audio continuity, Hive and behave-on-hardware were NOT RUN. The hosted "Physical gPTP" context was skipped. No hosted or field skip is hardware proof.
- **Bank evidence.** I found no public transcript of the manager's source static/builder and native banks for this head. The linked `160debeb` tree is the pre-rewrite evidence archive, with no bank result for f547a49b. The hosted required contexts at this head are executed and green, read at 17:53 UTC.
- **Nothing heavy was run:** no bank, builder, Verilator, Yosys, act, Docker or hardware step. Because nothing was simulated, the pinned simulator was not used and its identity was not checked.
- **Clone restored.** My runs created one bytecode cache in the clone, and I removed it. The final check (`receipts/restore_verify.txt`) shows:
  - HEAD and tree exact, and the index equal to HEAD;
  - 865 tracked files byte- and mode-identical;
  - four gitlinks at their pins, with the processor submodules initialized as found and the other two uninitialized as found;
  - an empty porcelain status, ignored files included.

## Pending manager duties

- **F1.**
  - Complete the redaction of the peer ENTITY fields in the four JSONL payloads.
  - Republish `MANIFEST.json` and re-pin the page.
  - Scope the redaction sentence.
  - Decide publicly on the still-fetchable predecessor objects: `160debeb` and its pre-rewrite ancestors `e76011d5`, `58d5419e` and `5ff947b4`.
  - Decide on the link to them in PR commit `67aa00e5`'s tree, which a merge commit would carry into dev history. The review-start instruction for this round also links `160debeb`.
- **F2.** Fix at a new head, then re-review every lens that the change un-covers.
- **Bank transcripts.** Publish the bank transcripts claimed for the head under review.
- **Merge turn.** Validate the final current-dev candidate: source base `ede8d48e`, live dev `759da623`. Then run act and hosted acceptance, and check containment after merge.
- **Reviews.** Obtain the external review, and a reviewer-accepted ledger at the merge head.

## Receipts (every file listed in MANIFEST.sha256)

- `scripts/run_all.sh CLONE WORK OUT` regenerates the archive-derived receipts from public sources in about 35 s. It fetches `32aec661` and `160debeb`.
- `scripts/gates.sh CLONE OUT BASE` produces `receipts/gates/*`.
- `scripts/misc_checks.py CLONE ARCHIVE_ROOT OUT` produces:
  - `identity_gate_check.txt`, `register_rows.txt`, `tool_redaction_vs_page.txt` and `rederive_steps4_5.txt`;
  - the read-only GitHub extracts: `external_hash_sources.txt`, `verify_followup_tracking.txt`, `pr_body_template_check.txt`, `merged_pr_template_practice.tsv`, `hosted_checks_head.txt` and `hosted_docs_check_steps.txt`.
- `scripts/restore_verify.sh CLONE HEAD TREE` produces `restore_verify.txt`.
- Each script's docstring states its inputs, and none writes into the clone.

R264-2 FINISHED
