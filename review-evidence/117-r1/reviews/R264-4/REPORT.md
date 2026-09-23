[R264] POSITIVE - exact head dfe6a587c6dc8e01eaceded4eb8e96d79e68a5ba

Round R264-4. Internal independent review of issue #117 / PR #531, cleared context.

- Head `dfe6a587c6dc8e01eaceded4eb8e96d79e68a5ba`, tree `9c80255cbc74dfa1a57eb5979fd4e150c964cc14`.
- Source base `ede8d48ecd7c7f589a14b957951f040d92c99c70`. Live `dev` at review time: `26d855a9176d63625e6635a029a0c44e3d57ce9a`; its merge base with the head is the source base.
- Evidence pin `db842315015dda3d68c9687973c4803bb25ceefb`, an ancestor of the evidence branch tip `7626fb2b850e1e9c707ea247cab211b1e6833e0e`.
- Three commits: `c3eb95fa`, `0abf147f`, `dfe6a587`. Each message is one line with no trailer. The diff is three Markdown files (`docs/findings/117_GPTP_SILICON_EVIDENCE.md` added; `docs/design/GM_LOSS_RECOVERY.md` and `docs/findings/README.md` modified, mode 100644). No HDL, firmware, configuration or gitlink changes.
- All five lenses applied: Conformance, RTL, Robustness, Tests, Docs.

## Verdict in brief

POSITIVE. No BLOCKER, MAJOR or MINOR finding is open at this head, so every lens is covered clean. The three SUGGESTIONs below are optional.

- **The round-3 findings are closed, with no new defect in the corrected passages.** R264-3 F1/F2/S1/S2 and R265-3 F1/F2/S1: see the prior-findings table.
- **No bench identity at the pin, in the branch history or in the PR.** Every string the redactions replaced was checked across the whole evidence branch and all three PR commits. So were the repository's deny-list and local-info shapes. The encodings searched were raw text, hex (plain and six separator forms), base64 (three alignments), UTF-16LE/BE, decimal byte lists, NetBIOS-encoded names and URL escapes. The sweep finds none; every residual hit is a classified coincidence. A planted positive control fires in each planted encoding.
- **The captures were decoded, not only string-searched.** DHCP, mDNS/DNS-SD, ARP, IGMP, LLDP and AVDECC strings in all 22 captures. One unmasked host name remains (S1). The repository's own practice treats it as a role name.
- **Every page hash resolves.** 81 full hashes: 73 are archive originals in `MANIFEST.json`, and the other 8 are the ones the page declares outside the archive, each found where the page says. All 26 abbreviated hashes resolve as the page says. The counts 77 / 6 / 71 / 20 / 57 / 29 match the archive.
- **The B1/B3 and holdover facts match the captures and transcripts.** So does every Step 2, Step 3, Step 4 and Step 5 figure I re-derived with my own scripts.
- **No PR commit links a superseded archive commit.** The only archive locator in the PR is the current pin.

## Reconstruction order and authorities read

1. AGENTS.md sections 1 to 8. CONTRIBUTING.md sections 2 and 6 (privacy rules, lines 524-551). `docs/README.md`. `scripts/docs_check.py` `IDENTITY_RULES` and `LOCAL_RULES`.
2. Issue #117: body, frozen acceptance, and the scope decisions and records in comments 5561827955, 5565246390, 5789767491, 5794146393, 5794274143, 5794354283, 5794859125, 5794950660, 5795658105, 5795898094 and 5796668867.
3. Authorities: `REQUIREMENTS.md` REQ-PTP-05/07/08 and REQ-VER-04/05; `docs/reference/REGISTER_MAP.md`; `docs/reference/MILAN_COMPLIANCE_MATRIX.md` rows 4.2.6.1.1 and 4.2.6.2.6; `hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv`; `docs/design/GM_LOSS_RECOVERY.md`.
4. `git diff ede8d48e..dfe6a587` and the history. I also diffed the previous head against this one; the round-4 commit changes only the page lines it claims to (129, 339, 440, 527, 529, 535-536, 540).
5. The evidence at the pin and on the branch. Manager comments on the PR: 5799413596, 5800264651, 5802093720 and 5804430089. Hosted check runs at the exact head.
6. Only after my verdict and ledger were drafted: the prior review findings (PR comments 5798410684, 5798463789, 5800161462, 5800196179, 5801972860 and 5802037583). They changed neither.

## Findings

No BLOCKER, MAJOR or MINOR finding.

### S1 - SUGGESTION - Docs, Conformance

`[R264] SUGGESTION Docs, Conformance - docs/findings/117_GPTP_SILICON_EVIDENCE.md:540; pin db842315 bench-a200/bench/runA/tap-runA.pcap, bench-a202/bench/cycle{1,3,4,6}/tap-c*.pcap, bench-a202/bench/final/tap-final.pcap - the capture server's self-announced host name stays unmasked and the "stays" sentence does not name it`

- **Evidence.** The capture server's own frames on the tap link sit in the captures as host records without an envelope, which the page excludes from timing. They carry its host name in DHCP option 12 (Run A 18 frames; cycles 1, 3, 4 and 6: 9, 9, 10 and 9; final 4) and in mDNS (7; 4, 4, 4, 3; 2). Receipt: `receipts/pcap_census_pin.txt`. The other two DHCP host names are handled as the page says: the switch's is masked length-preserving, and the controller host's short role name stays.
- **Assessment.** The name has no bench prefix. It says what the repository already publishes about that host's role (`docs/integration/BUILDING.md:512`), so I do not judge it bench-identifying. CONTRIBUTING.md:542 does list "hostnames" as a class, however, and line 540 names only "short host role names" among what stays.
- **Suggested outcome, for the owner or manager.** Either name self-announced host names without the bench prefix in the "stays" sentence, or mask this one length-preserving (new pin, `MANIFEST.json`, re-pin).
- **Verification.** Re-read line 540, or rerun `scripts/pcap_census.py` on a new pin.

### S2 - SUGGESTION - Docs

`[R264] SUGGESTION Docs - docs/findings/117_GPTP_SILICON_EVIDENCE.md:540 and :529 against :129 - the page's privacy rationale for firmware versions disagrees with itself`

- **The two sides.**
  - Line 129 says "A firmware version is not bench-identifying (every unit of the product carries the same one)". That follows decision 5802093720.
  - Line 540 lists the peer's "firmware string" and the switch's "firmware version" among the "bench-identifying strings masked".
  - Line 529 says the archive masks the switch's firmware version "under CONTRIBUTING section 6".
- **Every fact holds.** Both values are masked in the archive. The peer digest recovers its value by design. The switch value is kept privately.
- **Only the category label conflicts.** A reader cannot tell whether the decision covers firmware versions in general or the peer's only.
- **Suggested outcome.** Say at line 540 that the firmware strings are masked with the identity fields they sit beside. Say at line 529 that the switch value is withheld by choice, or state the decision's scope.
- **Verification.** Re-read lines 129, 529 and 540 together.

### S3 - SUGGESTION - Docs

`[R264] SUGGESTION Docs - docs/findings/117_GPTP_SILICON_EVIDENCE.md:340 - one LINKG_STAT delay is stated for all six cycles`

- **Evidence.** Line 340 says, "in all six cycles", that `LINKG_STAT` went from `0x83` to `0x03` "2.73 s after the last received frame". Measured from the switch's last frame on the DUT link, the console brackets for the edge are:

  | Cycle | Edge lies in |
  |---|---|
  | 1 | (2.63, 2.73] s |
  | 2 | (2.62, 2.72] s |
  | 3 | (2.62, 2.72] s |
  | 4 | (2.54, 2.64] s |
  | 5 | (2.57, 2.67] s |
  | 6 | (2.61, 2.71] s |

  Receipt: `receipts/linkg_brackets.txt`. The value 2.73 s is cycle 1's later sample. Cycles 4 to 6 place the edge 0.02 to 0.09 s below it.
- **Impact.** None beyond precision. The difference is within one 0.1 s console sample, it is outside every acceptance box, and no verdict depends on it.
- **Suggested outcome.** Give the six-cycle range (later samples 2.64 to 2.73 s), or say "within one sample of 2.6 to 2.7 s".
- **Verification.** Rerun `scripts/linkg_brackets.py`.

## Prior public findings: resolved or retained at this head

| Prior finding | Severity | State at `dfe6a587` | Evidence |
|---|---|---|---|
| R264-3 F1: the USB by-id remainder published the console adapter's serial | MAJOR | CLOSED | `bench-a200/tools/run_a.sh:9`, `run_b.sh:8` and `bench-a202/tools/cycle_locked.sh:9` read `P=/dev/<adapter>` at the pin. The adapter's vendor, model and serial and the by-id path show 0 hits in every encoding: at the pin, in its 4-commit history, and in all 10 branch commits (`identity_sweep_archive.txt`). The only other `usb-by-id` class hits are generic path wording in an archived review record, with no device identity. `MANIFEST.json` maps the files, and line 540 says "whole USB by-id names". |
| R264-3 F2: the page published a digest recovering a value it called withheld | MINOR | CLOSED, "not private" arm | The decision is public (5802093720). Line 129 now says the digest identifies the value by design. I re-derived it: the field holds 7 octets plus 57 NUL octets and hashes to the page value. Its first 8 octets equal the `sha256_8` of comment 5670665596. The raw string is masked in both packets in every encoding (0 hits). A label inconsistency remains; see S2. |
| R264-3 S1: cite the 8-octet prefix and link it | SUGGESTION | TAKEN | Line 129. |
| R264-3 S2: name protocol identifiers under what stays | SUGGESTION | TAKEN | Line 540. |
| R265-3 F1: B1/B3 switch facts contradicted by the captures | MINOR | CLOSED | `check_b1_b3.txt` shows the following in every A202 cycle capture, tap and controller-host alike: ARP probe ×3 and announcement ×2 of a link-local address; IGMP from that address and from one other IPv4 address; one DNS-SD SRV for a `_tcp` service plus a TXT record. No ADPDU from the switch MAC in any of the 22 captures. DHCP every 15.00 s and no DHCP reply anywhere. No TCP frame at all. Lines 527 and 529 now state exactly this. |
| R265-3 F2: "holdover clear" while the grandmaster is absent | MINOR | CLOSED | `rederive_step3.jsonl`: at the identity change, holdover is set for 4, 4, 4, 5, 3 and 4 samples, 0.40, 0.40, 0.40, 0.52, 0.31 and 0.41 s, starting at the first `020000fffe000001` sample. That is the range lines 339 and 440 now state. The RTL arms it on any change of `gm_id_i` (`KL_ptp_clock_validity.sv:188-199`, 2 quarter-ticks = 0.25 to 0.5 s). |
| R265-3 S1: the switch's DNS-SD fields not named or masked | SUGGESTION | TAKEN | Masked. The DNS-SD key names, unit identifier and firmware value show 0 hits in every encoding. The remote identifier and the device-name product word show only classified coincidences: numeric substrings in analysis text and three random bytes in one capture. In the decoded TXT records every string is fully masked except the two generic version keys, and the instance name keeps only the MAC (`pcap_census_pin.txt`). Line 540 names them. |
| R264-2 F1 / R265-2 F1: peer identity hex-encoded in the archive | MAJOR | still CLOSED | Peer product, serial, firmware, entity name and group name show 0 hits in every encoding at the pin, in the branch history and in the PR commits. |
| R264-2 F2 / R265-2 F2: stale Tool revisions redaction paragraph | MINOR | still CLOSED | `verify_manifest.txt` / `redacted_list.txt`. `8c9f2885` is path-only. `45889a7d`, `c4ef8c9a` and `bdd228a1` are identity-redacted, and so are `run_a/b/c.sh`. `95d64fd5`, `ad579e18` and `0e9faf30` are in full on comment 5584039577. `8ef4b008` has no public full value, as stated (`external_hash_sources.txt`). |
| R264-2 S2: say what `sha256sum -c` reports | SUGGESTION | TAKEN, still true | A200 manifest: 61 OK, 20 FAILED. A202 manifest: 96 OK, 57 FAILED. |
| R264-2 S1; R265-2 S1, S2 | SUGGESTION | not taken | Optional. |
| R264-1 F1 / R265-1 F1: bare-metal-only gate red | BLOCKER | still CLOSED | `gate_baremetal_only.txt`: rc 0 over 839 files. Hosted `docs-check` succeeded at this head. |
| R264-1 F2 / R265-1 F4: follow-up issues | MINOR | still CLOSED | Lines 53 and 467 link #529. Lines 473-477, 479-481 and 486-492 link #530 and #495. Items 8 and 10 carry reasons for having no issue. |
| R264-1 F3 / R265-1 F2: descriptive statements against the raw artifacts | MINOR | still CLOSED | Re-derived: dark window, loss-edge holdover, console census, envelope records and daemon scope (tables below). |
| R265-1 F3: "reaches asCapable" row | MINOR | still CLOSED | `spot_checks.txt` item 3: asCapable rises within one sample of the second completed Pdelay exchange in all six cycles. |
| R264-1 F4: box 5 traceability | MINOR | still CLOSED | All 74 raw-artifact table rows resolve at the pin. 29 name redacted files: 18 captures, 6 analyses, 3 censuses, 1 entity dump and 1 lock log. The 8 hashes outside the archive are where the page says (`external_hash_sources.txt`). |
| R264-1 F5, F6; R265-1 S1, S2 | SUGGESTION | optional | R265-1 S1 is in effect taken (the pinned locator). The others are not re-judged. |

## Independent re-derivation at this head (page claim against the pinned raw artifacts)

None of the packet's analysis scripts was reused.

| Page claim | Re-derived | Receipt |
|---|---|---|
| 236 files; 77 redacted (6 path-only, 71 identity; 20 A200, 57 A202); 29 table hashes name redacted files | identical; tree set equals manifest set; 236/236 published hashes match | `verify_manifest.txt` |
| Step 3 table: off-for, sync 0, GM self, asCapable 0, switch first frame and first Announce, asCapable 1, GM switch, all-good, recovery | every cell within 0.01 s; recovery 0.51, 0.51, 1.51, 0.42, 1.46, 1.60 against the page's 0.51, 0.52, 1.51, 0.43, 1.46, 1.60 | `rederive_step3.jsonl` |
| Loss: sync 0.40-0.46 s after the last Sync; holdover 3-5 samples, 0.30-0.50 s; GM self 3.01-3.08 s after the last Announce; parent follows; generation +1, count 1 | 0.40-0.46; 3-5 samples, 0.30-0.50 s; 3.00-3.07 (tap fit ±0.01); yes; +1, 1 | `rederive_step3.jsonl` |
| Return: DUT master Syncs 1-4; self Announce (priority1 248) in cycles 3 and 5; `tu` clear 0.41-0.52 s after adoption; `CLKV_TUCNT` +40/+39/+41/+40/+40/+41; `RST_EPOCH` 1; largest cycle 1 gap 0.106 s over 1,600 samples | 3, 2, 4, 1, 3, 4; cycles 3 and 5 only; 0.41-0.52; identical; 1; identical | `rederive_step3.jsonl` |
| Switch carrier back 13.6-13.8 s after "on"; first frame 3.7-4.5 s later; first Announce 1.0-1.7 s after that; first Sync 0-18 ms behind | 13.63-13.80; 3.70-4.48; 1.00-1.71; -0.1 to 17.5 ms | `carrier_return.txt`, `rederive_step3.jsonl` |
| Observation 7 PHC steps -128.5/-355.9/-163.3/-154.5/-180.3/-154.1 s, equal to the power-on intervals within 0.04 s | steps identical; intervals 128.53/355.93/163.28/154.51/180.29/154.08 s | `phc_steps.txt` |
| Cycles 4-6: first `tu=1` PDU inside the console interval where `CLKV_STAT[0]` rose; 316/293/243 `tu=1` PDUs; relicence 0.83/2.38/0.72 s after all-good; every post-return PDU `tu=0`; PCP 3 VID 2 | yes; identical; identical; 0 `tu=1` among 32,579/32,033/32,899; TCI `0x6002` | `rederive_stream.txt` |
| No CONNECT_TX to the DUT between the loss and recovery; first after the return at 41.28/42.96/41.46 s | none; 41.29/42.96/41.46 | `spot_checks.txt` |
| Step 2: 4,556 Sync, 565 Announce, 564 and 566 Pdelay_Req intervals, all within 30 %; 568/568 and 570/570 exchanges; two switch answers at 18.33/18.36 ms; 570 s span | identical; span 569.6 s | `rederive_step2.txt` |
| DUT turnaround 10,984-11,009 ns (per-run medians 10,992-11,000); claimed `t3 - t2` 10,608-10,629 ns | identical, on the tap's integer nanosecond word | `turnaround_int.txt` |
| Run B: 34,061 CRF PDUs, all `tu=0`, no sequence gap; 116 console samples all `SYNC=1 ASCAPABLE=1 TU=0`; PDELAY 380-391 ns (median 385); controller 60/60 AS_CAPABLE, 381-391 ns; `CLKV_TUCNT` 11 | identical | `rederive_step2.txt`, `step2_step4_step5_checks.txt` |
| 38,954 console commands in 14 transcripts, read verbs only | 7,792 `milan_status` + 31,154 `mem_read` + 2 `mem_list` + 6 `crc` | notes below this table |
| Envelope-less records 76; 38, 0, 38, 45, 0, 37; 18; none elsewhere; 19 tcpdump logs with 0 dropped | identical | `spot_checks.txt` |
| Step 5 enumeration: 164 ms, average 3 ms, 0 retries/timeouts/unexpected; 5.3.8.10 downgrade; peer flags include Milan; 33 unsolicited notifications | identical (entity dump statistics; enumeration log) | `step2_step4_step5_checks.txt` |
| Build and grader hashes outside the archive | `.bit`, payload, `aem_desc.bin` and the ROM row are in the CRC table. `.bit`, `aem_desc.bin` and `flashboot_layout.json` are on 5794859125. The grader equals `scripts/baremetal_uart_smoke.py` at `ede8d48e`. `bios.bin` and `csr.csv` are on the page only, as stated. | `external_hash_sources.txt` |
| Redacted captures still parse | 20/20 length-preserving, every record header unchanged, each walks to its last octet | `redacted_capture_integrity.txt` |

- The console command census came from a direct count over the 14 transcripts at the pin, the same parser as `rederive_step3.py`. The A202 subset is in `rederive_step3.jsonl`.
- My tap-to-server line keeps every per-5 s minimum, so tap-derived times can differ from the page's fit by 0.01 s. No 0.1 s console claim depends on that.

## Per-lens results (all five applied at dfe6a587)

- `[R264] PASS Conformance - issue #117 acceptance and decisions 5561827955, 5789767491, 5795898094, 5802093720; docs/findings/117_GPTP_SILICON_EVIDENCE.md:34-64, :129, :524-529, :540; docs/design/GM_LOSS_RECOVERY.md:88-118; MILAN_COMPLIANCE_MATRIX.md:78, :83; CONTRIBUTING.md:524-551 against pin db842315 and its history - every box row reports what was measured, and none is ticked by the PR. The bound, start, end, media clause and the 3 + 0.375 + 1.625 s derivation match the owner decision and the Milan intervals. The evidence the page pins, and the PR commits, carry no bench identity (S1 is a naming suggestion).`
- `[R264] PASS RTL - hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv:122, :186-200, :211, :245-248; docs/reference/REGISTER_MAP.md:730-731, :770-771, :875-880; clone_restore_verify.txt - no RTL, firmware or gitlink in the diff. The page's register decodes match the map and the RTL: CLKV_STAT bits 0/1/3/16, the holdover armed on a grandmaster-identity change for 0.25-0.5 s, CRFT_CTRL 0x3002E3, LINKG_STAT 0x83/0x03, CLKV_TUCNT, RST_EPOCH.`
- `[R264] PASS Robustness - pin db842315 (22 captures, 14 console transcripts, attempt 1 records); page :288-299, :49, :53-57 - the aborted attempt, the NOT RUN and FAIL rows and the loss/absence/return ordering are recorded honestly. The redaction is length-preserving and complete in structure (20/20). Masking now covers whole by-id names and the whole DNS-SD self-advertisement, in every encoding, across the pinned history.`
- `[R264] PASS Tests - receipts/*: sweeps with a positive control that fires in every planted encoding; independent re-derivations; ten focused documentation gates at the head, all rc 0 (docs_check scrub self-test 23/23, em-dash arms 57/57); mutation probes P1-P4 refused by the gates that guard the page. Result: every re-derived figure matches, and the gates can fail for the defects they claim. P5 is an observation outside this PR.`
- `[R264] PASS Docs - docs/findings/117_GPTP_SILICON_EVIDENCE.md (628 lines), docs/design/GM_LOSS_RECOVERY.md, docs/findings/README.md; MANIFEST.json and both MANIFEST.sha256 at the pin; anchors_resolve.txt; gate_*.txt; commit_messages.txt - every hash resolves, all 38 fragment links resolve, the TOC, style, gPTP-docs, feature-status and em-dash gates pass (0 over 670 added lines), and commits are one line with no trailers. S1-S3 are optional wording.`

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #117 acceptance and decisions; page :34-64, :129, :524-529, :540; GM_LOSS_RECOVERY.md:88-118; MILAN_COMPLIANCE_MATRIX.md:78, :83; REQUIREMENTS.md REQ-PTP-07/08, REQ-VER-04/05; CONTRIBUTING.md:524-551 against pin `db842315`, the 10 branch commits and the 3 PR commits | R264-4 | dfe6a587c6dc8e01eaceded4eb8e96d79e68a5ba |
| RTL | CLEAN | KL_ptp_clock_validity.sv:122, :186-200, :211, :245-248; REGISTER_MAP.md:730-731, :770-771, :875-880; page :339-340, :415-420, :439-445; raw diff modes and gitlinks equal to the base | R264-4 | dfe6a587c6dc8e01eaceded4eb8e96d79e68a5ba |
| Robustness | CLEAN | Pin captures (22), console transcripts (14), attempt 1 records, tool scripts `run_a.sh:9`, `run_b.sh:8`, `cycle_locked.sh:9`; redacted-capture integrity 20/20; page :288-299, :49, :53-57 | R264-4 | dfe6a587c6dc8e01eaceded4eb8e96d79e68a5ba |
| Tests | CLEAN | `receipts/identity_sweep_*`, `shape_sweep_*`, `rederive_*`, `turnaround_int.txt`, `spot_checks.txt`, `gate_*.txt`, `mutation_probes.txt`; positive control `identity_sweep_positive_control.txt` | R264-4 | dfe6a587c6dc8e01eaceded4eb8e96d79e68a5ba |
| Docs | CLEAN | The three changed pages in full; MANIFEST.json and both MANIFEST.sha256 at the pin; 81 full and 26 abbreviated page hashes; 38 fragment links; commit messages | R264-4 | dfe6a587c6dc8e01eaceded4eb8e96d79e68a5ba |

S1-S3 are SUGGESTIONs and do not affect coverage. Any later commit that changes the page, the pin or the archive un-covers Conformance, Robustness, Tests and Docs for the changed scope. RTL stays covered while no register decode or product file changes.

## Real limits

- **Evidence, not the product.** I judged the evidence only.
  - Physical calibration was NOT RUN.
  - Field skips and the page's NOT RUN rows are not hardware proof: the reference peer's own recovery time, the first reach after the flash, Hive, behave on hardware, latency and audio.
  - I had no bench access.
- **The token set has two sources.**
  - What the redactions replaced, derived by comparing the earliest public redacted archive with the pin. That archive still carried the identity fields.
  - The repository's identity and local-info rules.

  Values never masked and never named by a rule can be found only by decoding. I decoded every name-bearing protocol field in the captures (S1 came from that). Six files were already path-redacted in the earliest public archive and five scripts were partly redacted, so for those the path originals could not be diffed.
- **Short tokens.** Base64 is searched only for tokens of six octets or more, and short tokens also match by coincidence. Every residual hit was classified by context and is listed in the receipts: the DUT's own serial, which is a committed configuration value; numeric coincidences; generic path wording; the repository's own code-point assembly.
- **My tap timebase is coarser than the page's.** It is a least-squares line through every per-5 s minimum. Tap-derived times agree within 0.01 s. I did not reproduce the page's 2.02 ms residual figure.
- **Tools not used.** The scoped Verilator was not used, because the diff contains no RTL. No full parent, PP, gPTP, Yosys or builder bank was run, by instruction.
- **Hosted checks at the exact head, as a record only** (`hosted_check_runs_dfe6a587.tsv`).
  - Executed with success: `rtl-fast`, `docs-check`, `docs-check-no-git`, `wire-accountability`, `elaborate`, `full-ci-gate`, `changes`, `bdd-conformance`.
  - Completed as skipped, not executed: `verilator-suites`, `yosys-portability`, both shard matrices, `verilator-lint`, `yosys-elaboration` and the physical gPTP job.

  I read no job logs. The manager owns hosted and act acceptance.
- **The source-bank evidence could not be reached from the link in the assignment.** That link resolves to a superseded archive commit whose id is withheld here under the 2026-09-23 history-link decision. It holds only the two bench packets and a manifest, with no bank results. The last public manager comment at this head (5802093720) says "Bank r4 running". I therefore did not verify the stated bank pass.
- **Prior review archives** on the evidence branch were swept mechanically for identity and for superseded ids. Their contents were not otherwise read. Prior findings were taken from the public PR comments.

## Pending manager duties

1. **Purge of superseded evidence objects** (decision 5800264651). At this round the public remote still serves all three superseded archive pins, and the earliest one carries the identity fields in raw form.
2. **Archived review records** on the evidence branch name superseded archive ids in 26 objects across 8 labels (`superseded_mentions.txt`; ids withheld). The PR commits name none. Decide whether these records fall under the history-link decision.
3. **S1 and S2 decisions** (optional): the capture server's self-announced host name, and the scope of the firmware-version decision.
4. **Observation for a separate Issue, if agreed.** No repository gate resolves same-page fragment links outside a Contents block. Probes P5, P5b and P5c pass with a planted broken link (`mutation_probes.txt`). Every such link in the three changed pages resolves at this head (`anchors_resolve.txt`). Cross-page links are covered (P3b).
5. **Merge-turn duties.** Build the final candidate against live `dev` `26d855a9176d63625e6635a029a0c44e3d57ce9a` (source base `ede8d48e`), distinct from source validation at this head. Then hosted and act acceptance, candidate validation and post-merge containment. Merge only with explicit maintainer authorization, and with the second independent positive review.
6. **Issue #117 boxes stay the owner's call.** Box 4 carries FAIL and NOT RUN rows, audio is deferred to 2026-12-31, and the PR only relates to the issue.

## Receipts (every file listed in MANIFEST.sha256)

`scripts/run_all.sh CLONE EVID_GITDIR PIN_ROOT TOKENS SUPERSEDED OUT` regenerates every receipt except the ones named in its header and `external_hash_sources.txt`, which reads the fetched issue comment JSON. The token table and the superseded-id list are private inputs and are not published. Receipts name tokens only by class and ids only by label.

- **Identity and links:**
  - `receipts/identity_sweep_positive_control.txt`
  - `receipts/identity_sweep_archive.txt`
  - `receipts/identity_sweep_pr_commits.txt`
  - `receipts/identity_sweep_head_tree.txt`
  - `receipts/shape_sweep_pin_history.txt`
  - `receipts/shape_sweep_review_commits.txt`
  - `receipts/shape_sweep_pr_commits.txt`
  - `receipts/pcap_census_pin.txt`
  - `receipts/superseded_mentions.txt`
- **Page against archive:**
  - `receipts/verify_manifest.txt`
  - `receipts/redacted_list.txt`
  - `receipts/redacted_capture_integrity.txt`
  - `receipts/external_hash_sources.txt`
  - `receipts/check_b1_b3.txt`
  - `receipts/rederive_step2.txt`
  - `receipts/turnaround_int.txt`
  - `receipts/rederive_step3.jsonl`
  - `receipts/rederive_stream.txt`
  - `receipts/spot_checks.txt`
  - `receipts/phc_steps.txt`
  - `receipts/carrier_return.txt`
  - `receipts/linkg_brackets.txt`
  - `receipts/step2_step4_step5_checks.txt`
  - `receipts/anchors_resolve.txt`
- **Gates, probes and state:**
  - `receipts/gate_*.txt`
  - `receipts/mutation_probes.txt`
  - `receipts/commit_messages.txt`
  - `receipts/hosted_check_runs_dfe6a587.tsv`
  - `receipts/state_before.txt`
  - `receipts/clone_restore_verify.txt`: 865 tracked files byte- and mode-exact, index tree `9c80255c`, no index flags, four gitlinks at stage 0 equal to the base, no untracked or ignored file; both initialised submodule checkouts clean at their pins.
- **Scripts:** `scripts/*.py`, `scripts/*.sh`

R264-4 FINISHED
